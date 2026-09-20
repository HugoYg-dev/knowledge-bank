# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyyaml>=6.0",
# ]
# ///

"""
scripts/test_vault_utils.py - vault_utils 基础工具库单元测试套件
"""

import tempfile
import unittest
from pathlib import Path

from vault_utils import (
    DocumentSnapshot,
    UniqueKeyLoader,
    build_vault_snapshot,
    compute_sha256,
    dump_frontmatter,
    extract_frontmatter,
    extract_wikilinks,
    get_workspace,
    read_text,
    write_text,
)


class TestVaultUtils(unittest.TestCase):
    def test_get_workspace(self):
        ws = get_workspace()
        self.assertIsInstance(ws, Path)
        self.assertTrue((ws / "AGENTS.md").exists())

    def test_read_write_text(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            p = Path(tmpdir) / "sub" / "dir" / "test.md"
            write_text(p, "测试内容 UTF-8")
            self.assertEqual(read_text(p), "测试内容 UTF-8")

            # 读取不存在文件返回空串
            non_existent = Path(tmpdir) / "not_found.md"
            self.assertEqual(read_text(non_existent), "")

    def test_compute_sha256(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            p = Path(tmpdir) / "test.txt"
            write_text(p, "hello world")
            sha_str = compute_sha256("hello world")
            sha_bytes = compute_sha256(b"hello world")
            sha_path = compute_sha256(p)
            self.assertEqual(sha_str, sha_bytes)
            self.assertEqual(sha_str, sha_path)
            self.assertEqual(sha_str, "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9")

    def test_extract_frontmatter_valid(self):
        content = "---\ntitle: \"测试\"\ntags:\n  - RAG/retrieval\n---\n\n# 正文标题\n正文内容。"
        data, raw_yaml, body, err = extract_frontmatter(content)
        self.assertIsNone(err)
        self.assertIsInstance(data, dict)
        self.assertEqual(data.get("title"), "测试")
        self.assertEqual(data.get("tags"), ["RAG/retrieval"])
        self.assertIn("# 正文标题", body)

    def test_extract_frontmatter_missing(self):
        content = "# 没有 Frontmatter 的正文\n纯文本。"
        data, raw_yaml, body, err = extract_frontmatter(content)
        self.assertIsNone(data)
        self.assertIsNotNone(err)
        self.assertIn("未找到 Frontmatter", err)
        self.assertEqual(body, content)

    def test_extract_frontmatter_duplicate_key(self):
        content = "---\ntags: [a]\ntags: [b]\n---\n正文"
        data, raw_yaml, body, err = extract_frontmatter(content)
        self.assertIsNone(data)
        self.assertIsNotNone(err)
        self.assertIn("duplicate key", err)

    def test_extract_frontmatter_non_dict_root(self):
        content = "---\n- item1\n- item2\n---\n正文"
        data, raw_yaml, body, err = extract_frontmatter(content)
        self.assertIsNone(data)
        self.assertIsNotNone(err)
        self.assertIn("根节点必须是映射", err)

    def test_extract_frontmatter_empty(self):
        content = "---\n---\n正文"
        data, raw_yaml, body, err = extract_frontmatter(content)
        self.assertIsNone(err)
        self.assertEqual(data, {})

    def test_dump_frontmatter(self):
        data = {"title": "输出测试", "tags": ["AI-Agent/coding"]}
        body = "正文段落。"
        dumped = dump_frontmatter(data, body)
        self.assertTrue(dumped.startswith("---\n"))
        self.assertIn("title: 输出测试", dumped)
        self.assertIn("正文段落。", dumped)

    def test_extract_wikilinks(self):
        text = """
        这里引用了 [[concepts/概念_RAG]]，
        还有带别名的 [[entities/实体_OpenAI|OpenAI机构]]，
        以及带锚点的 [[raw/articles/sample.md#section-1]]，
        带别名与锚点的 [[concepts/概念_Attention#QKV|注意力机制]]，
        排除外部链接 [[http://example.com]] 和 [[https://example.com/page]]。
        """
        links = extract_wikilinks(text)
        expected = [
            "concepts/概念_RAG",
            "entities/实体_OpenAI",
            "raw/articles/sample.md",
            "concepts/概念_Attention",
        ]
        self.assertEqual(links, expected)

    def test_build_vault_snapshot(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            ws = Path(tmpdir)
            wiki_dir = ws / "wiki" / "sources"
            raw_dir = ws / "raw" / "articles"
            ignored_git = ws / ".git" / "hooks"

            write_text(
                wiki_dir / "test_source.md",
                "---\ntype: source\n---\n引用 [[concepts/概念_X]]\n",
            )
            write_text(
                raw_dir / "test_raw.md",
                "---\ntitle: 原始\n---\n底座内容\n",
            )
            write_text(
                ignored_git / "ignored.md",
                "---\ntitle: 忽略\n---\n不应被扫描\n",
            )

            snapshots = build_vault_snapshot(ws, folders=("wiki", "raw"))
            self.assertIn("wiki/sources/test_source.md", snapshots)
            self.assertIn("raw/articles/test_raw.md", snapshots)
            self.assertNotIn(".git/hooks/ignored.md", snapshots)

            snap = snapshots["wiki/sources/test_source.md"]
            self.assertEqual(snap.frontmatter, {"type": "source"})
            self.assertEqual(snap.wikilinks, ["concepts/概念_X"])
            self.assertIsInstance(snap.sha256, str)
            self.assertEqual(len(snap.sha256), 64)


if __name__ == "__main__":
    unittest.main()
