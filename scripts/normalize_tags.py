# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyyaml>=6.0",
# ]
# ///

"""
Knowledge Bank Tag Normalization & Cleanup Tool
遵循 AGENTS.md §5 规范的全局 Tag 规范化、去噪与 Frontmatter 清洗工具。

用法:
  uv run scripts/normalize_tags.py           # 默认 Dry-run 预演
  uv run scripts/normalize_tags.py --dry-run # 显式 Dry-run 预演
  uv run scripts/normalize_tags.py --apply   # 确认执行全库清洗与落盘
"""

import os
import sys
import re
import argparse
import yaml
from pathlib import Path
from collections import defaultdict, Counter

# 从 tag_manager 动态载入 tags.json 权威定义
try:
    from tag_manager import (
        load_tag_config,
        get_top_level_tags,
        get_tag_branches,
        get_all_approved_tags,
        validate_tag
    )
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from tag_manager import (
        load_tag_config,
        get_top_level_tags,
        get_tag_branches,
        get_all_approved_tags,
        validate_tag
    )

FORBIDDEN_FIELDS = {"confidence", "created", "ai-first"}

def normalize_tag_list(tags, ptype="source", content=""):
    if not isinstance(tags, list):
        if isinstance(tags, str):
            tags = [tags]
        else:
            tags = []
    
    approved_set = get_all_approved_tags()
    branches = get_tag_branches()
    normalized = []

    for t in tags:
        if not t:
            continue
        t_str = str(t).strip()
        
        # 针对 Overview 页面的顶层标签特殊保留
        if ptype == "overview" and t_str in branches:
            if t_str not in normalized:
                normalized.append(t_str)
            continue
        
        # 1. 优先使用权威门禁校验器进行校验
        is_valid, _ = validate_tag(t_str, ptype)
        if is_valid:
            if t_str not in normalized:
                normalized.append(t_str)
            continue
        
        # 2. 尝试大小写不敏感匹配合法标签 (如 skill/python -> Skill/python)
        matched = False
        for app in approved_set:
            if t_str.lower() == app.lower():
                is_valid, _ = validate_tag(app, ptype)
                if is_valid and app not in normalized:
                    normalized.append(app)
                matched = True
                break
        if matched:
            continue
        
        print(f"  ⚠️ 非标 Tag 拦截并剔除: {t_str}")

    # 若原始 Tags 全被清除则置为 [] 并打印警告待人工介入
    if not normalized and tags:
        print(f"  ⚠️ 原始 Tags {tags} 经清理/去噪后为空，置为 [] (待人工复核)")

    return normalized

def process_file(file_path, workspace, apply=False):
    rel_path = os.path.relpath(file_path, workspace)
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        return False, None, None, f"读取失败: {e}"

    m = re.match(r"^---\n(.*?)\n---(.*)", content, re.DOTALL)
    if not m:
        return False, None, None, None

    fm_str = m.group(1)
    body = m.group(2)

    try:
        data = yaml.safe_load(fm_str)
        if not isinstance(data, dict):
            return False, None, None, None
    except Exception as e:
        return False, None, None, f"YAML 解析失败: {e}"

    original_data = dict(data)
    modified = False
    diffs = []

    # 1. 移除违规非标字段 (仅针对 wiki/ 文件)
    if rel_path.startswith("wiki/"):
        for ff in FORBIDDEN_FIELDS:
            if ff in data:
                del data[ff]
                modified = True
                diffs.append(f"移除禁止字段 '{ff}'")

    # 2. 规范化 tags
    ptype = data.get("type", "source" if rel_path.startswith("wiki/sources") else "concept")
    orig_tags = data.get("tags", [])
    if orig_tags is None:
        orig_tags = []
    new_tags = normalize_tag_list(orig_tags, ptype=ptype, content=content)

    if orig_tags != new_tags:
        data["tags"] = new_tags
        modified = True
        diffs.append(f"Tags 变更: {orig_tags} -> {new_tags}")

    if not modified:
        return False, original_data, data, None

    # 重构 Frontmatter
    if rel_path.startswith("wiki/"):
        field_order = ["type", "tags", "summary", "sources", "updated", "timeline"]
        reconstructed_fm = {}
        for key in field_order:
            if key in data:
                reconstructed_fm[key] = data[key]
        for key in data:
            if key not in reconstructed_fm:
                reconstructed_fm[key] = data[key]
    else:
        # raw/articles
        reconstructed_fm = data

    new_fm_str = yaml.dump(reconstructed_fm, allow_unicode=True, sort_keys=False, default_flow_style=False).strip()
    new_full_content = f"---\n{new_fm_str}\n---{body}"

    if apply:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_full_content)

    return True, original_data, reconstructed_fm, "; ".join(diffs)

def main():
    parser = argparse.ArgumentParser(description="Knowledge Bank Tag Normalizer")
    parser.add_argument("--dry-run", action="store_true", help="预演模式（不修改文件）")
    parser.add_argument("--apply", action="store_true", help="正式落盘应用更改")
    args = parser.parse_args()

    apply = args.apply
    if not apply:
        print("=" * 60)
        print("🔍 [Tag Normalizer] 正在以 Dry-Run 预演模式运行（不会修改任何文件）...")
        print("=" * 60)
    else:
        print("=" * 60)
        print("🚀 [Tag Normalizer] 正在执行全库 Tag 规范化与清洗落盘...")
        print("=" * 60)

    workspace = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    target_dirs = [
        os.path.join(workspace, "wiki/sources"),
        os.path.join(workspace, "wiki/concepts"),
        os.path.join(workspace, "wiki/entities"),
        os.path.join(workspace, "wiki/comparisons"),
        os.path.join(workspace, "wiki/overview"),
        os.path.join(workspace, "raw/articles"),
        os.path.join(workspace, "raw/insights"),
        os.path.join(workspace, "Clippings")
    ]

    total_scanned = 0
    modified_files = []
    stats_by_dir = defaultdict(int)

    for tdir in target_dirs:
        if not os.path.exists(tdir):
            continue
        for root, _, files in os.walk(tdir):
            for file in sorted(files):
                if file.endswith(".md"):
                    total_scanned += 1
                    full_p = os.path.join(root, file)
                    rel_p = os.path.relpath(full_p, workspace)
                    mod, orig, new_fm, diff_summary = process_file(full_p, workspace, apply=apply)
                    if mod:
                        modified_files.append((rel_p, orig, new_fm, diff_summary))
                        top_dir = "/".join(rel_p.split("/")[:2])
                        stats_by_dir[top_dir] += 1

    print(f"\n📊 扫描完成！共扫描文件 {total_scanned} 篇，拟修改文件 {len(modified_files)} 篇。")
    print("-" * 60)
    for sdir, count in sorted(stats_by_dir.items()):
        print(f"  📁 {sdir:20}: {count} 篇文件变更")
    print("-" * 60)

    print(f"\n📝 详细变更清单（共 {len(modified_files)} 篇）:")
    for rel_p, orig, new_fm, diff_summary in modified_files:
        print(f"  📄 [{rel_p}]")
        print(f"     ↳ {diff_summary}")

    if not apply:
        print("\n" + "=" * 60)
        print("✅ Dry-run 预演完成！若确认无误，请运行以下命令正式执行落盘:")
        print("   uv run scripts/normalize_tags.py --apply")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print(f"✅ 全库清洗完成！已成功将变更落盘至 {len(modified_files)} 篇文件。")
        print("=" * 60)

if __name__ == "__main__":
    main()
