"""Bounded permutation expansion and conservative, clause-scoped intent review."""
import re

PEOPLE = r'people|persons?|figures?|crowds?|humans?|soldiers?|warriors?|cavalry|infantry'
NEGATION = r'no|without|never|not|free of|empty of'


def expand_permutations(text, limit=256):
    """Expand nested alternatives; escaped commas/braces remain literal text."""
    position = 0

    def sequence(in_group=False, depth=0):
        nonlocal position
        if depth > 32:
            raise ValueError('permutation nesting exceeds safety limit 32')
        results = ['']
        while position < len(text):
            char = text[position]
            if char == '\\' and position + 1 < len(text) and text[position + 1] in ',{}\\':
                parts = [text[position + 1]]
                position += 2
            elif char == '{':
                position += 1
                parts = []
                while True:
                    parts.extend(sequence(True, depth + 1))
                    if len(parts) > limit:
                        raise ValueError(f'permutation expansion exceeds safety limit {limit}')
                    if position >= len(text):
                        raise ValueError('unclosed permutation brace')
                    separator = text[position]
                    position += 1
                    if separator == '}':
                        break
                if any(not part.strip() for part in parts):
                    raise ValueError('empty permutation alternative')
            elif char in ',}' and in_group:
                break
            elif char == '}':
                raise ValueError('unmatched permutation closing brace')
            else:
                parts = [char]
                position += 1
            if len(results) * len(parts) > limit:
                raise ValueError(f'permutation expansion exceeds safety limit {limit}')
            results = [prefix + part for prefix in results for part in parts]
        return results

    return sequence()


def positive_clauses(body):
    """End a negation at a clause boundary, not at an arbitrary token distance."""
    normalized = body.lower()
    # Coordinated noun lists share their explicit negation, even across commas.
    people_list = r'(?:' + PEOPLE + r')(?:\s*(?:,\s*|\s+(?:and|or)\s+)(?:(?:and|or)\s+)?(?:' + PEOPLE + r'))*'
    normalized = re.sub(r'\bnot only\b', '', normalized)
    normalized = re.sub(r'\b(?:' + NEGATION + r')\s+(?:' + people_list + r')\b(?=\s*(?:$|--|[.;!?]|but\b))', '', normalized)
    normalized = re.sub(r'\b(?:' + NEGATION + r')\s+[\w-]+', '', normalized)
    for clause in re.split(r'[,;.!?\n，；。！？]+|\b(?:but|however|yet)\b', normalized):
        yield clause


def positive_people(body):
    return any(re.search(r'\b(?:' + PEOPLE + r')\b', clause) for clause in positive_clauses(body))


def semantic_warnings(body, exclusions):
    positive = ' '.join(positive_clauses(body))
    warns = []
    families = [
        ('lettering', r'\b(text|lettering|typography|signage|logo|wordmark)\b',
         {'text', 'lettering', 'typography', 'logo'}),
        ('surface detail', r'\b(texture[ds]?|embroidery|embroidered|weave|grain|pores)\b',
         {'texture', 'textures'}),
        ('realism', r'\b(realistic|photorealistic|semi-realistic|semirealistic)\b',
         {'realistic', 'photorealistic', 'realism'}),
        ('synthetic material', r'\b(plastic|resin|bjd|ball-jointed)\b', {'plastic', 'resin'}),
        ('visible equipment', r'\b(camera|tripod|camcorder)\b', {'camera', 'tripod', 'camcorder'}),
    ]
    excluded = {word for term in exclusions for word in re.findall(r'[\w-]+', term.lower())}
    for label, pattern, targets in families:
        if re.search(pattern, positive) and excluded & targets:
            warns.append(f'possible intent conflict: {label} requested in text and excluded by --no; review scope')
    if positive_people(body) and any(re.fullmatch(PEOPLE, word) for word in excluded):
        warns.append('possible intent conflict: people requested in text and excluded by --no; review scope')
    return warns
