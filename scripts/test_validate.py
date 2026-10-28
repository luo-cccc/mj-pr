#!/usr/bin/env python3
"""Behavioral regressions with explicit allowed-warning assertions."""
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from prompt_analysis import expand_permutations, positive_people
from validate_prompt import analyze, check, main


class PromptTests(unittest.TestCase):
    def assertClean(self, prompt, mode='style'):
        fails, warns = check(prompt, mode)
        self.assertEqual(fails, [])
        self.assertEqual(warns, [])

    def test_optional_profile_and_aliases(self):
        for profile in ('--p', '--profile', '--p approved-profile'):
            self.assertClean('woodcut --v 8.2 --ar 1:1 ' + profile)
        self.assertEqual(len(check('ink --r 2 --repeat 3', 'style')[0]), 1)

    def test_required_values_and_malformed_syntax(self):
        for suffix in ('--no', '--sref', '--cref', '--oref', '--s', '--ar 1.5:1',
                       '--ar 0:9', '--s=100', '--raw landscape', '--q NaN'):
            with self.subTest(suffix=suffix):
                self.assertTrue(check('ink --v 8.2 ' + suffix, 'style')[0])

    def test_alias_duplicates(self):
        for suffix in ('--ar 1:1 --aspect 2:3', '--s 100 --stylize 200'):
            self.assertEqual(len(check('ink ' + suffix, 'style')[0]), 1)

    def test_numeric_format_is_not_compatibility(self):
        self.assertClean('ink --ar 1:1 --v 8.2 --q .5 --s -1')

    def test_edit_references(self):
        for count in range(1, 5):
            urls = ' '.join(f'https://example.org/{i}.png' for i in range(count))
            self.assertClean('change coat --ar 1:1 --v 8.2 --edit ' + urls)
        for refs in ('', 'not-a-url', ' '.join('https://example.org/a.png' for _ in range(5))):
            self.assertTrue(check('change coat --edit ' + refs, 'style')[0])

    def test_negated_people_share_one_vocabulary(self):
        for noun in ('people', 'person', 'figures', 'crowd', 'humans', 'soldiers', 'warriors', 'cavalry', 'infantry'):
            for negation in ('no', 'without', 'free of', 'empty of'):
                with self.subTest(noun=noun, negation=negation):
                    self.assertFalse(positive_people(f'courtyard, {negation} {noun}'))
                    self.assertClean(f'courtyard, {negation} {noun} --ar 16:9 --v 8.2', 'scene')
            self.assertTrue(positive_people(f'courtyard with {noun}'))
        self.assertTrue(positive_people('no soldiers, people at a market'))
        self.assertTrue(positive_people('no soldiers but people at a market'))
        self.assertTrue(positive_people('not only soldiers but civilians'))
        self.assertTrue(positive_people('without text showing people dancing'))
        self.assertFalse(positive_people('courtyard without people, soldiers or warriors'))

    def test_historical_waist_and_scene_inputs(self):
        self.assertClean('full body character sheet, eye level view, hands clasped, dark sash at the waist, black boots, white background --ar 9:16 --v 8.2', 'character')
        self.assertClean('wide angle scene plate, misty mountain valley, slightly elevated view, no people, layered pine ridges, distant waterfall, cold blue gray palette, morning fog, cinematic realistic CG render, 24mm lens, f5.6, 1/125s --ar 16:9 --v 8.2 --raw --s 100 --no text, watermark', 'scene')

    def test_artistic_choices_have_no_prescriptive_warnings(self):
        for mode in ('scene', 'style'):
            for body in ('silhouette, face in darkness', 'deep focus, sharp background',
                         'warm face, cool cyan robe, mixed lighting', 'BJD resin doll with realistic pores',
                         '50mm lens, shallow depth of field', 'night, bright lanterns', '中文山水，水墨。'):
                self.assertClean(body + ' --ar 16:9 --v 8.2', mode)
        self.assertClean('barefoot monk, hands clasped, dark background --ar 1:1 --v 8.2', 'character')

    def test_missing_defaults_are_advice(self):
        fails, warns = check('ink', 'style')
        self.assertEqual(fails, [])
        self.assertEqual(set(warns), {'no aspect ratio stated; model default applies unless image/edit input determines it',
                                      'no explicit model selected; account/model default applies'})
        self.assertClean('ink --ar 1:1 --niji 7')

    def test_semantic_conflicts_are_advice(self):
        for body, negative in (('legible text signage', 'text'), ('embroidered textured robe', 'texture'),
                               ('semi-realistic CG', 'realistic'), ('BJD resin doll', 'plastic'),
                               ('camera on a table', 'camera'), ('people dancing', 'people'),
                               ('soldiers marching', 'soldiers'), ('cavalry advancing', 'cavalry')):
            fails, warns = check(f'{body} --ar 1:1 --v 8.2 --no {negative}', 'style')
            self.assertEqual(fails, [])
            self.assertEqual(len(warns), 1, warns)
            self.assertIn('possible intent conflict:', warns[0])
        self.assertClean('no text --ar 1:1 --v 8.2 --no text')

    def test_multiword_exclusions_are_not_errors(self):
        fails, warns = check('portrait --ar 1:1 --v 8.2 --no modern clothing', 'style')
        self.assertEqual(fails, [])
        self.assertEqual(warns, ['multi-word --no term `modern clothing` may exclude individual words; check intent'])


class BatchTests(unittest.TestCase):
    def test_cartesian_nested_and_escaped_options(self):
        self.assertEqual(expand_permutations('{a,{b,c}} {1,2}'), ['a 1', 'a 2', 'b 1', 'b 2', 'c 1', 'c 2'])
        self.assertEqual(expand_permutations(r'{red\, gold,blue}'), ['red, gold', 'blue'])
        for invalid in ('{a,b', 'a}', '{a,}', '{,b}'):
            with self.assertRaises(ValueError):
                expand_permutations(invalid)
        with self.assertRaises(ValueError):
            expand_permutations('{a,b}{a,b}', limit=3)
        with self.assertRaises(ValueError):
            expand_permutations('{' * 40 + 'a' + '}' * 40)
        with self.assertRaises(ValueError):
            expand_permutations('{' + ','.join('a' for _ in range(300)) + '}')

    def test_job_count_includes_repeats_and_versions(self):
        report = analyze('{a,b} --v {7,8.2} --r 2 --ar 1:1', 'style', expected_count=8, max_jobs=8)
        self.assertEqual(report['fails'], [])
        self.assertEqual(report['jobs'], 8)
        self.assertEqual(len(report['variants']), 4)
        self.assertTrue(analyze('{a,b}', 'style', expected_count=10)['fails'])
        self.assertTrue(analyze('{a,b}', 'style', max_jobs=1)['fails'])
        self.assertTrue(analyze('ink --r .5', 'style')['fails'])
        self.assertTrue(analyze('ink --r ' + '9' * 5000, 'style')['fails'])
        self.assertTrue(analyze('/imagine prompt:', 'style')['fails'])
        self.assertTrue(analyze('   ', 'style')['fails'])

    def test_all_variants_checked_and_full_command_measured(self):
        report = analyze('/imagine prompt: ink --ar {1:1,bad} --v 8.2', 'style', max_chars=10)
        self.assertEqual(len(report['fails']), 2)
        self.assertIn('chars exceeds', report['fails'][0])
        self.assertTrue(report['variants'][1]['fails'])

    def test_duplicate_and_multicommand_accounting(self):
        report = analyze('/imagine prompt: {a,a}\n/imagine prompt: b', 'style', expected_count=3, max_jobs=2)
        self.assertEqual(report['fails'], [])
        self.assertEqual(report['jobs'], 3)
        self.assertIn('duplicate expanded prompts; confirm repetitions are intentional', report['warns'])

    def test_repository_batches(self):
        root = Path(__file__).resolve().parents[1]
        paths = sorted((root / 'examples' / 'batches').glob('*.md'))
        self.assertEqual(len(paths), 6)
        for path in paths:
            commands = '\n'.join(line for line in path.read_text(encoding='utf-8').splitlines() if line.startswith('/imagine prompt:'))
            with self.subTest(path=path.name):
                report = analyze(commands, 'style', expected_count=10, max_jobs=4, max_chars=2000)
                self.assertEqual(report['fails'], [])
                self.assertEqual(report['commands'], 3)


class CliTests(unittest.TestCase):
    def test_json_report_and_error_exit(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            status = main(['--mode', 'style', '--json', 'ink --ar bad'])
        self.assertEqual(status, 1)
        self.assertTrue(json.loads(output.getvalue())['fails'])

    def test_usage_exit(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as error:
                main(['--mode', 'style', '--max-jobs', '0', 'ink'])
        self.assertEqual(error.exception.code, 2)

    def test_invalid_encoding_is_usage_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'prompt.txt'
            path.write_bytes(bytes([255]))
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as error:
                    main(['--mode', 'style', '--file', str(path)])
            self.assertEqual(error.exception.code, 2)

    def test_project_test_entry_propagates_failure(self):
        source = Path(__file__).read_text(encoding='utf-8')
        with patch.object(unittest, 'main', side_effect=SystemExit(1)) as entry:
            with self.assertRaises(SystemExit) as error:
                exec(compile(source, __file__, 'exec'), {'__name__': '__main__', '__file__': __file__})
        self.assertEqual(error.exception.code, 1)
        entry.assert_called_once_with(verbosity=2)

    @unittest.skipIf(sys.platform == 'emscripten', 'WebAssembly has no OS subprocess support')
    def test_cli_entry_exits_nonzero(self):
        result = subprocess.run([sys.executable, str(Path(__file__).with_name('validate_prompt.py')),
                                 '--mode', 'style', 'ink --ar bad'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('FAIL', result.stdout)


if __name__ == '__main__':
    unittest.main(verbosity=2)
