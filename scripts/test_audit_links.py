#!/usr/bin/env python3
"""Filesystem-isolated regressions for the skill dependency audit."""
import contextlib
import io
from pathlib import Path
import tempfile
import unittest

from audit_links import audit, main


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def put(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8')

    def status(self, strict=True):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return main(['--root', str(self.root)] + (['--strict'] if strict else []))

    def test_broken_link(self):
        self.put('SKILL.md', '[missing](references/missing.md)')
        self.assertEqual(audit(self.root)['broken'], [('SKILL.md', 'references/missing.md')])
        self.assertEqual(self.status(False), 1)

    def test_disconnected_cycle(self):
        self.put('SKILL.md', 'Entry point')
        self.put('references/a.md', '[b](b.md)')
        self.put('references/b.md', '[a](a.md)')
        result = audit(self.root)
        self.assertEqual(result['unreachable'], ['references/a.md', 'references/b.md'])
        self.assertEqual(len(result['inbound']['references/a.md']), 1)
        self.assertEqual(self.status(), 1)
        self.assertEqual(self.status(False), 0)

    def test_reachable_script_and_import(self):
        self.put('SKILL.md', 'Run `python scripts/runner.py`.')
        self.put('scripts/runner.py', 'from helper import check\n')
        self.put('scripts/helper.py', 'def check(): pass\n')
        self.assertEqual(audit(self.root)['unreachable'], [])
        self.assertEqual(self.status(), 0)

    def test_valid_graph(self):
        self.put('SKILL.md', '[guide](references/guide.md#usage)')
        self.put('references/guide.md', '[example](../examples/example.md)\nRun `python scripts/tool.py`.')
        self.put('examples/example.md', '[back](../SKILL.md)')
        self.put('scripts/tool.py', 'import json\n')
        self.put('README.md', 'Human instructions')
        self.put('NOTICE.md', 'Attribution')
        result = audit(self.root)
        self.assertEqual(result['broken'], [])
        self.assertEqual(result['unreachable'], [])
        self.assertEqual(self.status(), 0)

    def test_human_docs_do_not_supply_reachability(self):
        self.put('SKILL.md', '[README](README.md)')
        self.put('README.md', '[hidden](references/hidden.md)')
        self.put('references/hidden.md', 'not agent reachable')
        self.assertEqual(audit(self.root)['unreachable'], ['references/hidden.md'])
        self.assertEqual(self.status(), 1)

    def test_human_doc_broken_links_still_validated(self):
        self.put('SKILL.md', 'Entry')
        self.put('README.md', '[missing](missing.md)')
        self.assertEqual(self.status(False), 1)

    def test_fenced_fake_links_and_invocations_ignored(self):
        self.put('SKILL.md', '```python\n[fake](missing.md)\npython scripts/fake.py\n```\n'
                 '~~~text\n[fake](also-missing.md)\n~~~\n[real](guide.md)')
        self.put('guide.md', 'real')
        self.assertEqual(self.status(), 0)

    def test_script_invocation_edge(self):
        self.put('SKILL.md', 'Run `python scripts/runner.py`.')
        self.put('scripts/runner.py', 'import subprocess\nsubprocess.run(["python", "scripts/child.py"])\n')
        self.put('scripts/child.py', 'print("child")\n')
        self.assertEqual(self.status(), 0)

    def test_broken_script_invocation(self):
        self.put('SKILL.md', 'Run `python scripts/missing.py`.')
        self.assertEqual(self.status(False), 1)

    def test_broken_invocation_in_python(self):
        self.put('SKILL.md', 'Run `python scripts/runner.py`.')
        self.put('scripts/runner.py', 'import runpy\nrunpy.run_path("missing.py")\n')
        self.assertEqual(self.status(False), 1)

    def test_python_docstring_is_not_invocation(self):
        self.put('SKILL.md', 'Run `python scripts/runner.py`.')
        self.put('scripts/runner.py', '\"\"\"Example: scripts/fake.py\"\"\"\n')
        self.assertEqual(self.status(), 0)

    def test_encoded_local_target_and_fragment(self):
        self.put('SKILL.md', '[space](references/a%20b.md#section) [self](#top)')
        self.put('references/a b.md', 'section')
        self.assertEqual(self.status(), 0)

    def test_directory_is_not_valid_file_target(self):
        self.put('SKILL.md', '[directory](references)')
        self.put('references/guide.md', 'guide')
        self.assertEqual(self.status(False), 1)

    def test_reference_style_link(self):
        self.put('SKILL.md', '[guide][ref]\n\n[ref]: references/guide.md')
        self.put('references/guide.md', 'guide')
        self.assertEqual(self.status(), 0)

    def test_missing_entrypoint(self):
        self.put('guide.md', 'guide')
        self.assertEqual(self.status(), 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
