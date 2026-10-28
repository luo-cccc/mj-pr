#!/usr/bin/env python3
"""Audit local targets and reachability from SKILL.md, including Python edges.

Human-facing documents are validated but do not provide agent reachability.
Fenced Markdown examples are ignored. Exit 1 for broken targets, or for
unreachable documents/scripts with --strict. Exit 2 for a missing SKILL.md.
"""
import argparse
import ast
import collections
import os
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

HUMAN_FACING = {'README.md', 'NOTICE.md', 'LICENSE', 'LICENSE.md'}
LINK_RE = re.compile(r'!?\[[^\]]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+[\"\'][^)]*)?\s*\)')
SCRIPT_RE = re.compile(r'(?<![\w/])((?:\.{1,2}/)?(?:[\w.-]+/)*[\w.-]+\.py)\b')


def collect(root):
    files = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {'.git', '__pycache__', 'node_modules'}]
        for name in filenames:
            full = Path(dirpath) / name
            files[full.relative_to(root).as_posix()] = full
    return files


def without_fences(text):
    lines, fence = [], None
    for line in text.splitlines():
        marker = re.match(r'^\s{0,3}(`{3,}|~{3,})', line)
        if fence:
            if re.fullmatch(r'\s{0,3}' + re.escape(fence[0]) + '{' + str(len(fence)) + r',}\s*', line):
                fence = None
            continue
        if marker:
            fence = marker.group(1)
            continue
        lines.append(line)
    return '\n'.join(lines)


def audit(root):
    root = Path(root).resolve()
    files = collect(root)
    graph = {p: set() for p in files}
    inbound = collections.defaultdict(set)
    broken, external = [], 0

    def add(source, target, root_relative=False):
        nonlocal external
        target = target.strip('<>')
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc:
            external += 1
            return
        if not parsed.path:
            return  # fragment-only links point at the current document
        local = unquote(parsed.path)
        base = root if root_relative else files[source].parent
        resolved = (base / local).resolve()
        if not resolved.is_relative_to(root) or not resolved.is_file():
            broken.append((source, target))
            return
        dest = resolved.relative_to(root).as_posix()
        if dest not in files:
            broken.append((source, target))
            return
        inbound[dest].add(source)
        if Path(source).name not in HUMAN_FACING:
            graph[source].add(dest)

    for path, full in files.items():
        if full.suffix not in {'.md', '.py'}:
            continue
        text = full.read_text(encoding='utf-8')
        if full.suffix == '.md':
            text = without_fences(text)
            for target in LINK_RE.findall(text):
                add(path, target)
            # Reference-style links, including collapsed/shortcut references.
            definitions = dict(re.findall(r'^\s{0,3}\[([^\]]+)\]:\s*(<[^>]+>|\S+)', text, re.M))
            for label, target in definitions.items():
                if re.search(r'\]\[' + re.escape(label) + r'\]|(?<!\!)\[' + re.escape(label) + r'\](?![:(])', text, re.I):
                    add(path, target)
            # Inline invocation paths in prose/tables resolve from skill root
            # first, then from the referring document's directory.
            for target in SCRIPT_RE.findall(LINK_RE.sub('', text)):
                add(path, target, root_relative=(root / target).is_file() or target.startswith('scripts/'))
        else:
            tree = ast.parse(text, filename=str(full))
            for node in ast.walk(tree):
                modules = []
                if isinstance(node, ast.Import):
                    modules = [(alias.name, 0) for alias in node.names]
                elif isinstance(node, ast.ImportFrom):
                    modules = [(node.module or '', node.level)]
                    if not node.module:
                        modules = [(alias.name, node.level) for alias in node.names]
                for module, level in modules:
                    base = full.parent
                    for _ in range(max(0, level - 1)):
                        base = base.parent
                    candidates = [base / (module.replace('.', '/') + '.py'),
                                  base / module.replace('.', '/') / '__init__.py',
                                  root / (module.replace('.', '/') + '.py'),
                                  root / module.replace('.', '/') / '__init__.py']
                    local = next((p for p in candidates if p.is_file()), None)
                    if local:
                        add(path, os.path.relpath(local, full.parent).replace(os.sep, '/'))
                    elif level:
                        broken.append((path, f'relative import {module}'))
                # Only inspect invocation arguments, not arbitrary strings or
                # docstrings containing illustrative/fake script filenames.
                if isinstance(node, ast.Call):
                    function = ast.unparse(node.func)
                    if function in {'subprocess.run', 'subprocess.call', 'subprocess.check_call',
                                    'subprocess.check_output', 'subprocess.Popen', 'os.system',
                                    'runpy.run_path'}:
                        for arg in node.args:
                            for value in ast.walk(arg):
                                if isinstance(value, ast.Constant) and isinstance(value.value, str):
                                    for target in SCRIPT_RE.findall(value.value):
                                        add(path, target, root_relative=(root / target).is_file())

    reachable, pending = set(), ['SKILL.md'] if 'SKILL.md' in files else []
    while pending:
        path = pending.pop()
        if path in reachable:
            continue
        reachable.add(path)
        pending.extend(graph[path] - reachable)
    unreachable = sorted(p for p in files if Path(p).suffix in {'.md', '.py'}
                         and Path(p).name not in HUMAN_FACING and p not in reachable)
    return {'files': files, 'graph': graph, 'inbound': inbound, 'broken': broken,
            'external': external, 'reachable': reachable, 'unreachable': unreachable}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument('--strict', action='store_true')
    args = ap.parse_args(argv)
    result = audit(args.root)
    if 'SKILL.md' not in result['files']:
        print('missing reachability root SKILL.md', file=sys.stderr)
        return 2
    print('=== BROKEN LOCAL TARGETS ===')
    for source, target in result['broken']:
        print(f'  {source} -> {target}')
    print('\n=== UNREACHABLE FROM SKILL.md ===')
    for path in result['unreachable']:
        print(f'  {path}')
    print('\n=== INBOUND COUNT (diagnostic only) ===')
    for path in sorted(result['files']):
        if Path(path).suffix in {'.md', '.py'}:
            print(f"  {len(result['inbound'][path]):2d}  {path}")
    print(f"\n{len(result['files'])} files, {result['external']} external links, "
          f"{len(result['broken'])} broken, {len(result['unreachable'])} unreachable")
    return int(bool(result['broken'] or (args.strict and result['unreachable'])))


if __name__ == '__main__':
    sys.exit(main())
