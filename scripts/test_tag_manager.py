# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyyaml>=6.0",
# ]
# ///

"""
Unit tests for tag_manager.py (Tag CRUD and Governance Engine)
"""

import os
import sys
import json
import tempfile
import shutil
import unittest
import yaml
from pathlib import Path
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tag_manager


class TestTagManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.tags_json = self.test_dir / "tags.json"
        
        # 初始 Mock 配置
        self.initial_config = {
            "version": "1.0.0",
            "updated_at": "2026-08-26",
            "top_level_tags": ["DeepLearning", "AIGC", "面试"],
            "branches": {
                "LLM": {
                    "description": "LLM 体系",
                    "leaves": ["arch", "inference", "training"],
                    "multi_level": ["arch/attention", "training/RL"]
                },
                "AI-Agent": {
                    "description": "Agent 体系",
                    "leaves": ["coding", "skill", "multi-agent"]
                }
            }
        }
        with open(self.tags_json, "w", encoding="utf-8") as f:
            json.dump(self.initial_config, f, ensure_ascii=False, indent=2)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_load_and_validate_tags(self):
        config = tag_manager.load_tag_config(str(self.tags_json))
        self.assertEqual(config["version"], "1.0.0")

        # 顶层标签
        ok, err = tag_manager.validate_tag("DeepLearning", ptype="source", config=config)
        self.assertTrue(ok)

        # 二级叶子
        ok, err = tag_manager.validate_tag("LLM/arch", ptype="source", config=config)
        self.assertTrue(ok)

        # 三级多级细分
        ok, err = tag_manager.validate_tag("LLM/arch/attention", ptype="source", config=config)
        self.assertTrue(ok)

        # 综述页特权允许顶层分支
        ok, err = tag_manager.validate_tag("LLM", ptype="overview", config=config)
        self.assertTrue(ok)

        # 普通页严禁顶层池化
        ok, err = tag_manager.validate_tag("LLM", ptype="source", config=config)
        self.assertFalse(ok)
        self.assertIn("禁止顶层池化", err)

        # 未批准标签
        ok, err = tag_manager.validate_tag("LLM/unapproved", ptype="source", config=config)
        self.assertFalse(ok)

    def test_add_tag_operations(self):
        # 1. 添加顶层标签
        args_top = argparse.Namespace(tag="NewTopTag", desc="")
        tag_manager.cmd_add(args_top, tags_json_path=str(self.tags_json))
        
        cfg = tag_manager.load_tag_config(str(self.tags_json))
        self.assertIn("NewTopTag", cfg["top_level_tags"])

        # 2. 添加细分分支标签
        args_leaf = argparse.Namespace(tag="AI-Agent/embodied", desc="具身智能")
        tag_manager.cmd_add(args_leaf, tags_json_path=str(self.tags_json))
        
        cfg = tag_manager.load_tag_config(str(self.tags_json))
        self.assertIn("embodied", cfg["branches"]["AI-Agent"]["leaves"])

        # 验证新标签合法性
        ok, _ = tag_manager.validate_tag("AI-Agent/embodied", config=cfg)
        self.assertTrue(ok)

    def test_cascade_rename_tag(self):
        # 创建包含旧标签的 mock markdown 文件
        md_file = self.test_dir / "wiki" / "sources" / "test_doc.md"
        md_file.parent.mkdir(parents=True, exist_ok=True)
        md_file.write_text(
            "---\n"
            "type: \"source\"\n"
            "tags: [\"LLM/arch\", \"AI-Agent/coding\"]\n"
            "summary: \"Test doc\"\n"
            "sources: [\"raw/articles/test.md\"]\n"
            "updated: \"2026-08-26\"\n"
            "---\n"
            "# Body\n",
            encoding="utf-8"
        )

        args = argparse.Namespace(old_tag="LLM/arch", new_tag="LLM/architecture", apply=True)
        tag_manager.cmd_rename(args, tags_json_path=str(self.tags_json), workspace=str(self.test_dir))

        # 验证 Markdown 文件的标签已被重命名
        content = md_file.read_text(encoding="utf-8")
        fm = yaml.safe_load(content.split("---")[1])
        self.assertIn("LLM/architecture", fm["tags"])
        self.assertNotIn("LLM/arch", fm["tags"])

        # 验证 tags.json 已更新
        cfg = tag_manager.load_tag_config(str(self.tags_json))
        self.assertIn("architecture", cfg["branches"]["LLM"]["leaves"])
        self.assertNotIn("arch", cfg["branches"]["LLM"]["leaves"])

    def test_cascade_delete_tag(self):
        md_file = self.test_dir / "wiki" / "sources" / "test_del.md"
        md_file.parent.mkdir(parents=True, exist_ok=True)
        md_file.write_text(
            "---\n"
            "type: \"source\"\n"
            "tags: [\"AIGC\", \"AI-Agent/coding\"]\n"
            "summary: \"Test doc\"\n"
            "sources: [\"raw/articles/test.md\"]\n"
            "updated: \"2026-08-26\"\n"
            "---\n"
            "# Body\n",
            encoding="utf-8"
        )

        args = argparse.Namespace(tag="AIGC", apply=True)
        tag_manager.cmd_delete(args, tags_json_path=str(self.tags_json), workspace=str(self.test_dir))

        # 验证 Markdown 文件的标签已被移除
        content = md_file.read_text(encoding="utf-8")
        fm = yaml.safe_load(content.split("---")[1])
        self.assertNotIn("AIGC", fm["tags"])
        self.assertIn("AI-Agent/coding", fm["tags"])

        # 验证 tags.json 已更新
        cfg = tag_manager.load_tag_config(str(self.tags_json))
        self.assertNotIn("AIGC", cfg["top_level_tags"])


if __name__ == "__main__":
    unittest.main()
