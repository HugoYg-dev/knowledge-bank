# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyyaml>=6.0",
# ]
# ///

import hashlib
import json
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vault_lint


class TestVaultLint(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        for directory in (
            'raw/articles',
            'Clippings',
            'wiki/sources',
            'wiki/concepts',
            'wiki/entities',
            'wiki/comparisons',
            'wiki/overview',
        ):
            (self.test_dir / directory).mkdir(parents=True, exist_ok=True)
        self.write_file('wiki/index.md', '# Index\n')
        self.write_file('wiki/log.md', '# Log\n')

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def write_file(self, relative_path, content, binary=False):
        path = self.test_dir / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        if binary:
            path.write_bytes(content)
        else:
            path.write_text(content, encoding='utf-8')
        return path

    def append_to_index(self, relative_path):
        index_path = self.test_dir / 'wiki/index.md'
        with index_path.open('a', encoding='utf-8') as handle:
            handle.write(f'- [[{relative_path}]]\n')

    def frontmatter(self, page_type, sources, **overrides):
        fields = {
            'type': f'"{page_type}"',
            'tags': '["LLM/arch"]',
            'summary': '"A summary"',
            'sources': sources,
            'updated': '"2026-08-11"',
        }
        fields.update(overrides)
        lines = ['---'] + [f'{key}: {value}' for key, value in fields.items()] + ['---', '# Content']
        return '\n'.join(lines)

    def add_valid_source(self, source_name='source_a', raw_name='raw_a.md'):
        raw_path = f'raw/articles/{raw_name}'
        source_path = f'wiki/sources/{source_name}.md'
        self.write_file(raw_path, '# Raw')
        self.write_file(source_path, self.frontmatter('source', f'["{raw_path}"]'))
        self.append_to_index(source_path)
        return source_path

    def run_lint(self):
        output = StringIO()
        with redirect_stdout(output):
            vault_lint.cmd_lint(str(self.test_dir))
        return output.getvalue()

    def assert_lint_fails(self):
        output = StringIO()
        with redirect_stdout(output), self.assertRaises(SystemExit) as raised:
            vault_lint.cmd_lint(str(self.test_dir))
        self.assertEqual(raised.exception.code, 1)
        self.assertNotIn('Traceback', output.getvalue())
        return output.getvalue()

    def test_valid_five_page_types_and_overview_directory(self):
        source_path = self.add_valid_source()
        page_paths = {
            'entity': 'wiki/entities/entity_a.md',
            'concept': 'wiki/concepts/concept_a.md',
            'comparison': 'wiki/comparisons/comparison_a.md',
            'overview': 'wiki/overview/overview_a.md',
        }
        for page_type, page_path in page_paths.items():
            self.write_file(page_path, self.frontmatter(page_type, f'["{source_path}"]'))
            self.append_to_index(page_path)
        self.run_lint()

    def test_unquoted_valid_yaml_date_is_accepted(self):
        raw_path = 'raw/articles/raw_a.md'
        self.write_file(raw_path, '# Raw')
        source_path = 'wiki/sources/source_a.md'
        self.write_file(
            source_path,
            self.frontmatter('source', f'["{raw_path}"]', updated='2024-02-29'),
        )
        self.append_to_index(source_path)
        self.run_lint()

    def test_invalid_yaml_duplicate_key_and_non_mapping_fail(self):
        fixtures = {
            'invalid': '---\ninvalid: yaml:\n---\n',
            'duplicate': '---\ntype: source\ntype: concept\n---\n',
            'non_mapping': '---\n- source\n- concept\n---\n',
        }
        for name, content in fixtures.items():
            with self.subTest(name=name):
                path = self.write_file(f'wiki/sources/{name}.md', content)
                self.assert_lint_fails()
                path.unlink()

    def test_source_requires_exactly_one_existing_raw_upstream(self):
        self.write_file('raw/articles/raw_a.md', '# Raw A')
        cases = {
            'zero': '[]',
            'multiple': '["raw/articles/raw_a.md", "raw/articles/raw_b.md"]',
            'terminal': '["wiki/sources/other.md"]',
            'missing': '["raw/articles/missing.md"]',
        }
        for name, sources in cases.items():
            with self.subTest(name=name):
                path = self.write_file(
                    f'wiki/sources/{name}.md',
                    self.frontmatter('source', sources),
                )
                self.assert_lint_fails()
                path.unlink()

    def test_terminal_page_requires_existing_source_string_array(self):
        source_path = self.add_valid_source()
        cases = {
            'empty': '[]',
            'raw_bypass': '["raw/articles/raw_a.md"]',
            'non_string': '[42]',
            'empty_string': '[""]',
            'missing': '["wiki/sources/missing.md"]',
        }
        for name, sources in cases.items():
            with self.subTest(name=name):
                path = self.write_file(
                    f'wiki/concepts/{name}.md',
                    self.frontmatter('concept', sources),
                )
                self.append_to_index(path.relative_to(self.test_dir).as_posix())
                self.assert_lint_fails()
                path.unlink()
        self.assertTrue((self.test_dir / source_path).exists())

    def test_tags_summary_and_updated_schema(self):
        raw_path = 'raw/articles/raw_a.md'
        self.write_file(raw_path, '# Raw')
        cases = {
            'tags_scalar': {'tags': '"LLM/arch"'},
            'tags_item_type': {'tags': '["LLM/arch", 1]'},
            'tags_unapproved': {'tags': '["random-tag"]'},
            'tags_top_level_pooling': {'tags': '["RAG"]'},
            'forbidden_confidence': {'confidence': '"high"'},
            'forbidden_created': {'created': '"2026-08-01"'},
            'summary_empty': {'summary': '"   "'},
            'summary_type': {'summary': '["summary"]'},
            'invalid_calendar_date': {'updated': '"2026-02-30"'},
            'timestamp_not_date': {'updated': '"2026-08-11T12:00:00"'},
        }
        for name, overrides in cases.items():
            with self.subTest(name=name):
                path = self.write_file(
                    f'wiki/sources/{name}.md',
                    self.frontmatter('source', f'["{raw_path}"]', **overrides),
                )
                self.append_to_index(path.relative_to(self.test_dir).as_posix())
                self.assert_lint_fails()
                path.unlink()

    def test_tag_whitelist_and_disambiguation(self):
        raw_path = 'raw/articles/raw_a.md'
        self.write_file(raw_path, '# Raw')
        # Valid tags on source page
        valid_source = self.write_file(
            'wiki/sources/valid_source.md',
            self.frontmatter('source', f'["{raw_path}"]', tags='["LLM/arch", "Skill/python", "DeepLearning"]'),
        )
        self.append_to_index('wiki/sources/valid_source.md')
        # Valid top-level tag on overview page
        valid_overview = self.write_file(
            'wiki/overview/valid_overview.md',
            self.frontmatter('overview', '["wiki/sources/valid_source.md"]', tags='["RAG"]'),
        )
        self.append_to_index('wiki/overview/valid_overview.md')
        self.run_lint()

    def test_page_type_must_match_directory(self):
        source_path = self.add_valid_source()
        path = self.write_file(
            'wiki/concepts/wrong_directory.md',
            self.frontmatter('entity', f'["{source_path}"]'),
        )
        self.append_to_index(path.relative_to(self.test_dir).as_posix())
        self.assert_lint_fails()

    def test_valid_timeline(self):
        source_path = self.add_valid_source()
        entity_path = 'wiki/entities/entity_a.md'
        timeline = '''
timeline:
  - field: "status"
    value: "active"
    valid_from: "2026-01-01"
    valid_to: null
    observed_at: 2026-08-11
    sources: ["wiki/sources/source_a.md"]'''
        self.write_file(
            entity_path,
            self.frontmatter('entity', f'["{source_path}"]').replace('\n---\n# Content', f'{timeline}\n---\n# Content'),
        )
        self.append_to_index(entity_path)
        self.run_lint()

    def test_timeline_only_allowed_on_entity(self):
        source_path = self.add_valid_source()
        concept_path = 'wiki/concepts/concept_a.md'
        timeline = '\ntimeline: []'
        self.write_file(
            concept_path,
            self.frontmatter('concept', f'["{source_path}"]').replace('\n---\n# Content', f'{timeline}\n---\n# Content'),
        )
        self.append_to_index(concept_path)
        self.assert_lint_fails()

    def test_timeline_structure_types_dates_and_sources(self):
        source_path = self.add_valid_source()
        valid_item = '''
  - field: "status"
    value: "active"
    valid_from: "2026-01-01"
    valid_to: null
    observed_at: "2026-08-11"
    sources: ["wiki/sources/source_a.md"]'''
        cases = {
            'not_list': 'timeline: {}',
            'item_not_mapping': 'timeline: ["bad"]',
            'missing_field': 'timeline:' + valid_item.replace('    field: "status"\n', ''),
            'field_type': 'timeline:' + valid_item.replace('field: "status"', 'field: 7'),
            'value_empty': 'timeline:' + valid_item.replace('value: "active"', 'value: ""'),
            'valid_from_bad': 'timeline:' + valid_item.replace('"2026-01-01"', '"2026-02-30"'),
            'valid_to_bad': 'timeline:' + valid_item.replace('valid_to: null', 'valid_to: "2026-13-01"'),
            'observed_at_null': 'timeline:' + valid_item.replace('observed_at: "2026-08-11"', 'observed_at: null'),
            'sources_empty': 'timeline:' + valid_item.replace('sources: ["wiki/sources/source_a.md"]', 'sources: []'),
            'sources_type': 'timeline:' + valid_item.replace('sources: ["wiki/sources/source_a.md"]', 'sources: [9]'),
            'sources_raw': 'timeline:' + valid_item.replace('wiki/sources/source_a.md', 'raw/articles/raw_a.md'),
            'sources_missing': 'timeline:' + valid_item.replace('wiki/sources/source_a.md', 'wiki/sources/missing.md'),
        }
        for name, timeline in cases.items():
            with self.subTest(name=name):
                path = self.write_file(
                    f'wiki/entities/{name}.md',
                    self.frontmatter('entity', f'["{source_path}"]').replace(
                        '\n---\n# Content',
                        f'\n{timeline}\n---\n# Content',
                    ),
                )
                self.append_to_index(path.relative_to(self.test_dir).as_posix())
                self.assert_lint_fails()
                path.unlink()

    def test_sanitize_view_hashes_original_bytes_and_writes_metadata(self):
        original = b'prefix\xff<!-- remove --> [[1, 2]] suffix\n'
        source = self.write_file('raw/articles/test.md', original, binary=True)
        before = source.read_bytes()
        expected_hash = hashlib.sha256(before).hexdigest()

        with redirect_stdout(StringIO()):
            output_path = vault_lint.cmd_sanitize_view(str(self.test_dir), 'raw/articles/test.md')

        self.assertEqual(source.read_bytes(), before)
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), expected_hash)
        self.assertTrue(output_path.is_relative_to((self.test_dir / 'tmp/sanitized').resolve()))
        sanitized = output_path.read_text(encoding='utf-8')
        self.assertNotIn('<!-- remove -->', sanitized)
        self.assertIn(expected_hash, sanitized)

        metadata_path = output_path.with_suffix(output_path.suffix + '.json')
        metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
        self.assertEqual(metadata['original_path'], 'raw/articles/test.md')
        self.assertEqual(metadata['resolved_path'], str(source.resolve()))
        self.assertEqual(metadata['original_sha256'], expected_hash)
        self.assertEqual(metadata['original_size_bytes'], len(original))
        self.assertEqual(metadata['output_path'], output_path.relative_to(self.test_dir.resolve()).as_posix())
        self.assertTrue(metadata['actions'])
        self.assertEqual(metadata['sanitizer_version'], vault_lint.SANITIZER_VERSION)

    def test_sanitize_view_accepts_clippings(self):
        source = self.write_file('Clippings/test.md', 'Text <!-- comment -->')
        before = source.read_bytes()
        with redirect_stdout(StringIO()):
            output_path = vault_lint.cmd_sanitize_view(str(self.test_dir), 'Clippings/test.md')
        self.assertEqual(source.read_bytes(), before)
        self.assertTrue(output_path.is_file())

    def test_sanitize_view_rejects_absolute_traversal_and_non_allowed_paths_without_output(self):
        self.write_file('raw/articles/test.md', 'Text')
        cases = (
            str((self.test_dir / 'raw/articles/test.md').resolve()),
            'raw/../wiki/index.md',
            '../wiki/index.md',
            'wiki/index.md',
        )
        for value in cases:
            with self.subTest(value=value):
                shutil.rmtree(self.test_dir / 'tmp', ignore_errors=True)
                with redirect_stdout(StringIO()), self.assertRaises(SystemExit) as raised:
                    vault_lint.cmd_sanitize_view(str(self.test_dir), value)
                self.assertEqual(raised.exception.code, 1)
                self.assertFalse((self.test_dir / 'tmp/sanitized').exists())

    def test_sanitize_view_rejects_symlink_escape(self):
        outside_dir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, outside_dir)
        outside_file = outside_dir / 'secret.md'
        outside_file.write_text('secret', encoding='utf-8')
        (self.test_dir / 'raw/articles/escape.md').symlink_to(outside_file)

        with redirect_stdout(StringIO()), self.assertRaises(SystemExit) as raised:
            vault_lint.cmd_sanitize_view(str(self.test_dir), 'raw/articles/escape.md')
        self.assertEqual(raised.exception.code, 1)
        self.assertFalse((self.test_dir / 'tmp/sanitized').exists())

    def test_sanitize_view_rejects_output_symlink_escape(self):
        self.write_file('raw/articles/test.md', 'Text')
        outside_dir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, outside_dir)
        (self.test_dir / 'tmp/sanitized').mkdir(parents=True)
        (self.test_dir / 'tmp/sanitized/raw').symlink_to(outside_dir)

        with redirect_stdout(StringIO()), self.assertRaises(SystemExit) as raised:
            vault_lint.cmd_sanitize_view(str(self.test_dir), 'raw/articles/test.md')
        self.assertEqual(raised.exception.code, 1)
        self.assertFalse(any(outside_dir.iterdir()))

    def test_sanitize_view_rejects_final_output_file_symlink(self):
        source = self.write_file('raw/articles/test.md', 'Text')
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        output_parent = self.test_dir / 'tmp/sanitized/raw/articles'
        output_parent.mkdir(parents=True)
        output_path = output_parent / f'test_{digest[:12]}.md'
        outside = self.write_file('outside-output.md', 'do not overwrite')
        output_path.symlink_to(outside)

        with redirect_stdout(StringIO()), self.assertRaises(SystemExit) as raised:
            vault_lint.cmd_sanitize_view(str(self.test_dir), 'raw/articles/test.md')
        self.assertEqual(raised.exception.code, 1)
        self.assertEqual(outside.read_text(encoding='utf-8'), 'do not overwrite')
        self.assertTrue(output_path.is_symlink())
        self.assertFalse(output_path.with_suffix('.md.json').exists())

    def test_sanitize_view_rejects_final_metadata_symlink_before_writing_output(self):
        source = self.write_file('raw/articles/test.md', 'Text')
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        output_parent = self.test_dir / 'tmp/sanitized/raw/articles'
        output_parent.mkdir(parents=True)
        output_path = output_parent / f'test_{digest[:12]}.md'
        metadata_path = output_path.with_suffix('.md.json')
        outside = self.write_file('outside-metadata.json', 'do not overwrite')
        metadata_path.symlink_to(outside)

        with redirect_stdout(StringIO()), self.assertRaises(SystemExit) as raised:
            vault_lint.cmd_sanitize_view(str(self.test_dir), 'raw/articles/test.md')
        self.assertEqual(raised.exception.code, 1)
        self.assertEqual(outside.read_text(encoding='utf-8'), 'do not overwrite')
        self.assertFalse(output_path.exists())
        self.assertTrue(metadata_path.is_symlink())

    def test_sanitize_view_never_overwrites_existing_regular_output(self):
        source = self.write_file('raw/articles/test.md', 'Text')
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        output_parent = self.test_dir / 'tmp/sanitized/raw/articles'
        output_parent.mkdir(parents=True)
        output_path = output_parent / f'test_{digest[:12]}.md'
        output_path.write_text('existing output', encoding='utf-8')

        with redirect_stdout(StringIO()), self.assertRaises(SystemExit) as raised:
            vault_lint.cmd_sanitize_view(str(self.test_dir), 'raw/articles/test.md')
        self.assertEqual(raised.exception.code, 1)
        self.assertEqual(output_path.read_text(encoding='utf-8'), 'existing output')
        self.assertFalse(output_path.with_suffix('.md.json').exists())

    def test_sanitize_raw_is_disabled_and_does_not_write(self):
        source = self.write_file('raw/articles/test.md', b'\xff<!-- keep -->', binary=True)
        before = source.read_bytes()
        with redirect_stdout(StringIO()), self.assertRaises(SystemExit) as raised:
            vault_lint.cmd_sanitize(str(self.test_dir))
        self.assertEqual(raised.exception.code, 1)
        self.assertEqual(source.read_bytes(), before)

    def test_prune_matches_parsed_sources_not_body_text(self):
        target = self.write_file('raw/articles/target.md', '# Target')
        other = self.write_file('raw/articles/other.md', '# Other')
        exact = '''---
type: source
tags: [Test]
summary: Exact
sources:
  - "raw/articles/target.md"
updated: 2026-08-11
---
'''
        false_positive = '''---
type: source
tags: [Test]
summary: Other
sources:
  - "raw/articles/other.md"
updated: 2026-08-11
---
Body mentions raw/articles/target.md but is not its source.
'''
        self.write_file('wiki/sources/exact.md', exact)
        self.write_file('wiki/sources/false_positive.md', false_positive)

        output = StringIO()
        with redirect_stdout(output):
            vault_lint.cmd_prune(str(self.test_dir), 'raw/articles/target.md')
        report = output.getvalue()
        self.assertIn("1 篇 -> ['exact.md']", report)
        self.assertNotIn("['exact.md', 'false_positive.md']", report)
        self.assertTrue(target.exists())
        self.assertTrue(other.exists())

    def test_extract_raw_references_uses_yaml_parser(self):
        content = '''---
sources:
  - "raw/articles/name, with [brackets].md"
---
'''
        self.assertEqual(
            vault_lint.extract_raw_references(content, 'fixture.md'),
            ['articles/name, with [brackets].md'],
        )

    def test_warning_does_not_delete_low_frequency_entity(self):
        source_path = self.add_valid_source()
        entity_path = self.write_file(
            'wiki/entities/low_frequency.md',
            self.frontmatter('entity', f'["{source_path}"]'),
        )
        self.append_to_index('wiki/entities/low_frequency.md')
        output = self.run_lint()
        self.assertIn('低频实体', output)
        self.assertTrue(entity_path.exists())


if __name__ == '__main__':
    unittest.main()
