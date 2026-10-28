#!/usr/bin/env python3
"""Lint Discord-style text; compatibility and artistic advice are not syntax errors."""
import argparse
import json
import math
from pathlib import Path
import re
import sys

from prompt_analysis import expand_permutations, positive_people, semantic_warnings

ALIASES = {'aspect': 'ar', 'version': 'v', 'profile': 'p', 'r': 'repeat',
           'stylize': 's', 'chaos': 'c', 'weird': 'w', 'quality': 'q'}
NUMERIC = {'v', 's', 'c', 'w', 'q', 'seed', 'iw', 'sw', 'sv', 'repeat', 'niji'}
SWITCHES = {'raw', 'tile', 'hd', 'sd', 'draft', 'fast', 'relax', 'turbo', 'stealth', 'public', 'video'}
REQUIRED = {'no', 'sref', 'cref', 'oref'}
KNOWN_PARAMS = NUMERIC | SWITCHES | REQUIRED | {'ar', 'p', 'edit'}
FOOTWEAR = r'\b(boots?|shoes?|sandals?|slippers|sneakers|heels|greaves|barefoot|puttees)\b'
HAND_CUES = r'\b(hands?|fingers?|grip|gripping|holding|clasped|fists?|palms|gloves|gauntlets)\b'


def split_prompt(text):
    matches = list(re.finditer(r'(?<!\S)--([^\s]*)', text))
    if not matches:
        return text.strip(), []
    body = text[:matches[0].start()].strip()
    params = []
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        params.append((match.group(1).lower(), text[match.end():end].strip()))
    return body, params


def check(text, mode, allow_people=False):
    fails, warns = [], []
    body, params = split_prompt(text)
    low, pvals = body.lower(), {}
    for name, value in params:
        if not re.fullmatch(r'[a-z]+', name):
            fails.append(f'malformed parameter --{name}')
            continue
        canonical = ALIASES.get(name, name)
        if canonical in pvals:
            fails.append(f'duplicate parameter --{canonical}')
        pvals[canonical] = value
        if canonical == 'ar':
            if not re.fullmatch(r'[1-9]\d*:[1-9]\d*', value):
                fails.append(f'malformed --ar value {value!r}; use positive integers W:H')
        elif canonical in NUMERIC:
            valid = re.fullmatch(r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)', value)
            if not valid or not math.isfinite(float(value)):
                fails.append(f'malformed numeric value for --{name}: {value!r}')
        elif canonical in SWITCHES:
            if value:
                fails.append(f'--{name} takes no value; unexpected trailing text {value!r}')
        elif canonical == 'edit':
            refs = value.split()
            if len(refs) > 4:
                fails.append('--edit accepts at most four reference images')
            if not refs or any(not re.fullmatch(r'https?://\S+', ref) for ref in refs):
                fails.append('--edit requires reference image URLs; check Discord syntax')
        elif canonical in REQUIRED:
            if not value:
                fails.append(f'missing value for --{name}')
        elif canonical == 'p':
            pass
        else:
            warns.append(f'unknown parameter --{name}; check current model documentation')
    for choices in ({'v', 'niji'}, {'hd', 'sd'}, {'fast', 'relax', 'turbo'}, {'stealth', 'public'}):
        selected = sorted(choices & pvals.keys())
        if len(selected) > 1:
            warns.append('conflicting controls: ' + ', '.join('--' + name for name in selected) + '; check intent and model')
    if 'ar' not in pvals:
        warns.append('no aspect ratio stated; model default applies unless image/edit input determines it')
    if 'v' not in pvals and 'niji' not in pvals:
        warns.append('no explicit model selected; account/model default applies')
    if mode == 'character':
        if not re.search(FOOTWEAR, low):
            warns.append('character review: footwear unspecified; relevant only if visible')
        if not re.search(HAND_CUES, low):
            warns.append('character review: hand action unspecified; relevant only if visible')
        if re.search(r'\bwaist[ -]height\b', low) and re.search(r'\b(full[ -]body|head[ -]to[ -]toe)\b', low):
            warns.append('composition review: waist-height viewpoint and full body need explicit framing; viewpoint alone does not imply cropping')
    elif mode == 'scene' and not allow_people and positive_people(body):
        warns.append('scene includes people without --allow-people; keep if intentional')
    exclusions = [term.strip() for term in pvals.get('no', '').split(',') if term.strip()]
    for term in exclusions:
        if len(term.split()) > 1:
            warns.append(f'multi-word --no term `{term}` may exclude individual words; check intent')
        if re.search(r'\b(hands?|fingers?|arms?|legs?|feet|head|face|eyes?|body|background)\b', term, re.I):
            warns.append(f'--no `{term}` may remove a body part or background; check intent')
    warns.extend(semantic_warnings(body, exclusions))
    return fails, warns


def analyze(text, mode, allow_people=False, expected_count=None, max_jobs=None, max_chars=None):
    """Review every bounded expansion, preserving command and repeat accounting."""
    fails, warns, variants = [], [], []
    commands = [line.strip() for line in text.splitlines() if line.strip().startswith('/imagine prompt:')]
    if commands:
        other = [line for line in text.splitlines() if line.strip() and not line.strip().startswith('/imagine prompt:')]
        if other:
            fails.append('command input contains non-command lines; provide commands only')
    else:
        commands = [text.strip()]
    jobs = 0
    for index, command in enumerate(commands, 1):
        if max_chars is not None and len(command) > max_chars:
            fails.append(f'command {index}: {len(command)} chars exceeds requested budget {max_chars}')
        prompt = command[len('/imagine prompt:'):] if command.startswith('/imagine prompt:') else command
        prompt = prompt.strip()
        if not prompt:
            fails.append(f'command {index}: empty prompt')
            continue
        try:
            expanded = expand_permutations(prompt)
        except ValueError as error:
            fails.append(f'command {index}: {error}')
            continue
        command_jobs = 0
        for variant in expanded:
            errors, advice = check(variant, mode, allow_people)
            params = {ALIASES.get(name, name): value for name, value in split_prompt(variant)[1]}
            repeats = params.get('repeat', '1')
            if not re.fullmatch(r'[1-9]\d*', repeats) or len(repeats) > 9:
                errors.append('--repeat requires a positive integer of at most nine digits for safe job accounting')
                count = 0
            else:
                count = int(repeats)
            command_jobs += count
            variants.append({'prompt': variant, 'jobs': count, 'fails': errors, 'warns': advice})
            fails.extend(f'command {index}, variant {len(variants)}: {error}' for error in errors)
            warns.extend(advice)
        jobs += command_jobs
        if max_jobs is not None and command_jobs > max_jobs:
            fails.append(f'command {index}: {command_jobs} jobs exceeds requested cap {max_jobs}')
    if expected_count is not None and jobs != expected_count:
        fails.append(f'expected {expected_count} jobs, expanded {jobs}')
    prompts = [item['prompt'] for item in variants]
    if len(prompts) != len(set(prompts)):
        warns.append('duplicate expanded prompts; confirm repetitions are intentional')
    return {'fails': fails, 'warns': list(dict.fromkeys(warns)), 'jobs': jobs,
            'commands': len(commands), 'variants': variants, 'chars': len(text)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('prompt', nargs='?')
    ap.add_argument('--file')
    ap.add_argument('--mode', choices=['character', 'scene', 'style'], required=True)
    ap.add_argument('--allow-people', action='store_true')
    for option in ('expected-count', 'max-jobs', 'max-chars'):
        ap.add_argument('--' + option, type=int)
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args(argv)
    for field in ('expected_count', 'max_jobs', 'max_chars'):
        if getattr(args, field) is not None and getattr(args, field) < 1:
            ap.error(field.replace('_', '-') + ' must be positive')
    try:
        text = Path(args.file).read_text(encoding='utf-8').strip() if args.file else args.prompt
    except (OSError, UnicodeError) as error:
        ap.error(str(error))
    if not text or not text.strip():
        ap.error('provide a prompt or --file')
    report = analyze(text, args.mode, args.allow_people, args.expected_count, args.max_jobs, args.max_chars)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for label, field in (('FAIL', 'fails'), ('WARN', 'warns')):
            for message in report[field]:
                print(label, message)
        print(f"{len(report['fails'])} fail, {len(report['warns'])} warn, {report['jobs']} jobs, {report['chars']} chars")
    return int(bool(report['fails']))


if __name__ == '__main__':
    sys.exit(main())
