#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/vault_utils.py - 知识库不可变基础工具库 (Pure Infrastructure Layer)

本模块严格作为知识库工程的不可变基础支持层，提供无副作用的路径、I/O、YAML/Frontmatter、
WikiLinks 解析与不可变文档快照能力。
严禁在此模块中编写任何针对特定知识层级（如低频实体定义、来源链规则等）的业务领域逻辑。
"""

from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


def get_workspace() -> Path:
    """获取知识库根目录路径（返回 Path 对象）。"""
    script_dir = Path(__file__).resolve().parent
    return script_dir.parent


def read_text(path: Path | str) -> str:
    """安全读取文件文本（强制 UTF-8，自动处理编码容错，不存在时返回空字符串）。"""
    p = Path(path)
    if not p.exists() or not p.is_file():
        return ""
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def write_text(path: Path | str, content: str) -> None:
    """安全写入文件文本（强制 UTF-8，自动创建缺失的父级目录）。"""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def compute_sha256(data: str | bytes | Path) -> str:
    """计算文本、字节流或文件的 SHA-256 哈希散列值。"""
    if isinstance(data, Path):
        content = read_text(data).encode("utf-8")
    elif isinstance(data, str):
        content = data.encode("utf-8")
    else:
        content = data
    return hashlib.sha256(content).hexdigest()


class UniqueKeyLoader(yaml.SafeLoader):
    """YAML 安全加载器，当 Frontmatter 中存在重复键时主动抛出异常防范静默覆盖。"""

    def construct_mapping(self, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
        self.flatten_mapping(node)
        mapping: dict[Any, Any] = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in mapping:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    f"found duplicate key: {key}",
                    key_node.start_mark,
                )
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping


_FRONTMATTER_PATTERN = re.compile(r"^---\r?\n(?:(.*?)\r?\n)?---\r?\n?", re.DOTALL)
_WIKILINK_PATTERN = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")


def extract_frontmatter(content: str) -> tuple[dict[str, Any] | None, str, str, str | None]:
    """
    从 Markdown 文本中提取 YAML Frontmatter 与正文 Body。

    返回元组: (data, raw_yaml, body, error_message)
    - 若无 Frontmatter: (None, "", content, "未找到 Frontmatter (必须以 --- 包围)")
    - 若 YAML 语法错误或含有重复键: (None, raw_yaml, body, error_message)
    - 若成功: (dict, raw_yaml, body, None)
    """
    match = _FRONTMATTER_PATTERN.match(content)
    if not match:
        return None, "", content, "未找到 Frontmatter (必须以 --- 包围)"

    raw_yaml = match.group(1) or ""
    body = content[match.end() :]

    try:
        data = yaml.load(raw_yaml, Loader=UniqueKeyLoader)
        if data is None:
            return {}, raw_yaml, body, None
        if not isinstance(data, dict):
            return None, raw_yaml, body, "Frontmatter 根节点必须是映射 (dict)"
        return data, raw_yaml, body, None
    except Exception as e:
        return None, raw_yaml, body, f"YAML 解析失败: {str(e)}"


def dump_frontmatter(data: dict[str, Any], body: str = "") -> str:
    """将数据序列化为 YAML Frontmatter 格式并拼合正文。"""
    yaml_text = yaml.dump(
        data,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
    ).strip()
    if body:
        cleaned_body = body.lstrip("\r\n")
        return f"---\n{yaml_text}\n---\n\n{cleaned_body}"
    return f"---\n{yaml_text}\n---\n"


def extract_wikilinks(text: str) -> list[str]:
    """
    从 Markdown 文本中提取所有 WikiLinks 目标路径（规范化剔除别名与锚点）。
    例如:
      [[concepts/概念_RAG|检索增强]] -> 'concepts/概念_RAG'
      [[raw/articles/sample.md#heading]] -> 'raw/articles/sample.md'
    """
    matches = _WIKILINK_PATTERN.findall(text)
    targets: list[str] = []
    for target in matches:
        cleaned = target.strip()
        if cleaned and not cleaned.startswith("http://") and not cleaned.startswith("https://"):
            targets.append(cleaned)
    return targets


@dataclass(frozen=True)
class DocumentSnapshot:
    """知识库单篇文档的不可变内存分析快照 (Immutable Snapshot)"""

    rel_path: str
    abs_path: str
    content: str
    frontmatter: dict[str, Any] | None
    frontmatter_error: str | None
    body: str
    wikilinks: list[str]
    sha256: str


def build_vault_snapshot(
    workspace: Path | str | None = None,
    folders: tuple[str, ...] = ("wiki", "raw", "notes"),
) -> dict[str, DocumentSnapshot]:
    """
    执行单一扫描 Pass 遍历知识库，构建全量文档的只读内存快照集合。

    仅供 L0 只读诊断、统计与分析阶段使用。
    写操作（L3 高危修改）落盘前必须逐文件实时重验 SHA-256，严禁依赖陈旧快照。
    """
    ws = Path(workspace) if workspace else get_workspace()
    snapshot_map: dict[str, DocumentSnapshot] = {}

    for folder in folders:
        folder_path = ws / folder
        if not folder_path.exists():
            continue

        for root, dirs, files in os.walk(folder_path):
            # 排除版本控制与临时目录
            dirs[:] = [d for d in dirs if d not in {".git", ".obsidian", "tmp", ".pipeline"}]
            for f in files:
                if not f.endswith(".md"):
                    continue

                abs_p = Path(root) / f
                try:
                    rel_p = str(abs_p.relative_to(ws))
                except ValueError:
                    rel_p = str(abs_p)

                content = read_text(abs_p)
                fm_data, _, body, fm_err = extract_frontmatter(content)
                links = extract_wikilinks(content)
                sha = compute_sha256(content)

                snapshot_map[rel_p] = DocumentSnapshot(
                    rel_path=rel_p,
                    abs_path=str(abs_p),
                    content=content,
                    frontmatter=fm_data,
                    frontmatter_error=fm_err,
                    body=body,
                    wikilinks=links,
                    sha256=sha,
                )

    return snapshot_map
