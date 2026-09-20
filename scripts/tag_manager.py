# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyyaml>=6.0",
# ]
# ///

"""
Knowledge Bank Tag Manager & Governance Tool
遵循 AGENTS.md 规范，基于根目录 tags.json 权威配置提供 Tag 白名单查询、门禁校验与 CRUD 治理工具。

用法:
  uv run scripts/tag_manager.py list                         # 查看全量标签树
  uv run scripts/tag_manager.py validate <tag> [--ptype ...] # 校验单个 Tag 合规性
  uv run scripts/tag_manager.py add <tag> [--desc ...]       # 新增 Tag 审批入库
  uv run scripts/tag_manager.py rename <old> <new> [--apply] # 全库级联重命名 Tag
  uv run scripts/tag_manager.py delete <tag> [--apply]       # 全库级联删除/下线 Tag
"""

import os
import sys
import re
import json
import argparse
import yaml
from pathlib import Path
from datetime import datetime


def get_tags_json_path(workspace=None):
    if workspace is not None:
        p = os.path.join(workspace, "tags.json")
        if os.path.exists(p):
            return p
    # 默认指向仓库根目录 (scripts/ 上一级)
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(repo_root, "tags.json")


def load_tag_config(tags_json_path=None):
    """从 tags.json 加载权威标签配置"""
    if tags_json_path is None:
        tags_json_path = get_tags_json_path()
    
    if not os.path.exists(tags_json_path):
        # 尝试仓库根目录
        fallback_p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tags.json")
        if os.path.exists(fallback_p):
            tags_json_path = fallback_p
        else:
            raise FileNotFoundError(f"标签配置文件不存在: {tags_json_path}")
    
    with open(tags_json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tag_config(config, tags_json_path=None):
    """将标签配置写回 tags.json 并更新时间戳"""
    if tags_json_path is None:
        tags_json_path = get_tags_json_path()
    
    config["updated_at"] = datetime.now().strftime("%Y-%m-%d")
    with open(tags_json_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
        f.write("\n")


def get_top_level_tags(config=None):
    if config is None:
        config = load_tag_config()
    return set(config.get("top_level_tags", []))


def get_tag_branches(config=None):
    if config is None:
        config = load_tag_config()
    branches = {}
    for branch, data in config.get("branches", {}).items():
        branches[branch] = set(data.get("leaves", []))
    return branches


def get_all_approved_tags(config=None):
    if config is None:
        config = load_tag_config()
    approved = set(config.get("top_level_tags", []))
    for branch, data in config.get("branches", {}).items():
        for leaf in data.get("leaves", []):
            approved.add(f"{branch}/{leaf}")
        for ml in data.get("multi_level", []):
            approved.add(f"{branch}/{ml}")
    return approved


def validate_tag(tag, ptype="source", config=None):
    """
    校验 tag 是否符合 tags.json 与 AGENTS.md 规范。
    返回 (is_valid, error_msg)
    """
    if not isinstance(tag, str) or not tag.strip():
        return False, f"Tag 必须是非空字符串: {tag!r}"
    
    tag = tag.strip()
    if config is None:
        try:
            config = load_tag_config()
        except Exception as e:
            return False, f"无法读取 tags.json: {e}"

    top_level_tags = get_top_level_tags(config)
    branches = get_tag_branches(config)
    
    if tag in top_level_tags:
        return True, ""
    
    # 宏观综述页允许特定顶层分类
    if ptype == "overview" and tag in branches:
        return True, ""
    
    if "/" not in tag:
        if tag in branches:
            return False, f"违反细分叶子优先纪律（禁止顶层池化）: '{tag}' 必须精准锚定细分叶子（如 '{tag}/...'）"
        return False, f"未批准的非标 Tag: '{tag}'"
    
    branch, rest = tag.split("/", 1)
    if branch not in branches:
        return False, f"未批准的 Tag 主分支: '{branch}' (完整 Tag: '{tag}')"
    
    leaf = rest.split("/")[0]
    if leaf not in branches[branch]:
        allowed = ", ".join(sorted(branches[branch]))
        return False, f"未批准的 Tag 细分叶子: '{leaf}' (分支 '{branch}' 仅允许: {allowed})"
    
    return True, ""


# ==================== CLI Operations ====================

def cmd_list(args):
    config = load_tag_config()
    print("=" * 60)
    print("🏷️  [Knowledge Bank 经审批的标准 Tag 白名单 (tags.json)]")
    print("=" * 60)
    print(f"版本: {config.get('version')} | 最近更新: {config.get('updated_at')}\n")

    print("📌 【独立顶层标签 (Top-Level Independent Tags)】:")
    for t in sorted(config.get("top_level_tags", [])):
        print(f"  - {t}")
    
    print("\n🌳 【分层树状分支 (Hierarchical Branches & Leaves)】:")
    for branch, data in sorted(config.get("branches", {}).items()):
        desc = data.get("description", "")
        print(f"  📂 {branch}/  ({desc})")
        for leaf in sorted(data.get("leaves", [])):
            print(f"     ├── {branch}/{leaf}")
        for ml in sorted(data.get("multi_level", [])):
            print(f"     └── {branch}/{ml}  (三级细分)")
    print("=" * 60)


def cmd_validate(args):
    tag = args.tag
    ptype = args.ptype or "source"
    ok, err = validate_tag(tag, ptype=ptype)
    if ok:
        print(f"✅ Tag '{tag}' 校验通过 (类型: {ptype})")
        sys.exit(0)
    else:
        print(f"❌ Tag 校验失败: {err}")
        sys.exit(1)


def cmd_scan(args, workspace=None):
    """全库扫描所有 Markdown 文件的 Tag 是否符合白名单"""
    if workspace is None:
        workspace = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config = load_tag_config()

    print("=" * 60)
    print("🔍 [Tag 全库合规性扫描]")
    print("=" * 60)

    scan_dirs = ["wiki"]
    invalid_records = []
    total_scanned = 0

    for sdir in scan_dirs:
        dir_p = os.path.join(workspace, sdir)
        if not os.path.exists(dir_p):
            continue
        for root, _, files in os.walk(dir_p):
            for file in sorted(files):
                if not file.endswith(".md"):
                    continue
                fpath = os.path.join(root, file)
                total_scanned += 1
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
                        content = fp.read()
                    m = re.match(r"^(---\n.*?\n---)", content, re.DOTALL)
                    if not m:
                        continue
                    fm_data = yaml.safe_load(m.group(1).strip("- \n"))
                    if not isinstance(fm_data, dict):
                        continue
                    tags = fm_data.get("tags", [])
                    ptype = fm_data.get("type", "source")
                    if isinstance(tags, str):
                        tags = [tags]
                    elif not isinstance(tags, list):
                        continue

                    for t in tags:
                        ok, err = validate_tag(t, ptype=ptype, config=config)
                        if not ok:
                            rel = os.path.relpath(fpath, workspace)
                            invalid_records.append((rel, t, err))
                except Exception:
                    continue

    print(f"📊 扫描完成：共扫描 {total_scanned} 篇文档。")
    if not invalid_records:
        print("✅ 全库所有 Tag 均符合 tags.json 白名单规范 (0 违规)！")
        sys.exit(0)
    else:
        print(f"❌ 发现 {len(invalid_records)} 处不合规 Tag：")
        for rel, t, err in invalid_records:
            print(f"  - [{rel}] '{t}': {err}")
        sys.exit(1)


def cmd_add(args, tags_json_path=None):
    tag = args.tag.strip()
    desc = args.desc or ""
    config = load_tag_config(tags_json_path)

    if "/" not in tag:
        top_tags = config.setdefault("top_level_tags", [])
        if tag in top_tags:
            print(f"⚠️ 顶层标签 '{tag}' 已存在，无需重复添加。")
            return
        top_tags.append(tag)
        save_tag_config(config, tags_json_path)
        print(f"✅ 成功添加顶层标签: '{tag}'")
    else:
        parts = tag.split("/")
        branch = parts[0]
        if branch not in config.setdefault("branches", {}):
            config["branches"][branch] = {"description": desc or f"{branch} 分支", "leaves": []}
            print(f"ℹ️ 新建分支: '{branch}'")
        
        if len(parts) == 2:
            leaf = parts[1]
            leaves = config["branches"][branch].setdefault("leaves", [])
            if leaf in leaves:
                print(f"⚠️ 细分标签 '{tag}' 已存在。")
                return
            leaves.append(leaf)
            save_tag_config(config, tags_json_path)
            print(f"✅ 成功添加细分标签: '{tag}'")
        else:
            ml_tag = "/".join(parts[1:])
            mls = config["branches"][branch].setdefault("multi_level", [])
            if ml_tag in mls:
                print(f"⚠️ 多级标签 '{tag}' 已存在。")
                return
            mls.append(ml_tag)
            parent_leaf = parts[1]
            if parent_leaf not in config["branches"][branch].setdefault("leaves", []):
                config["branches"][branch]["leaves"].append(parent_leaf)
            save_tag_config(config, tags_json_path)
            print(f"✅ 成功添加多级细分标签: '{tag}'")


def cmd_rename(args, tags_json_path=None, workspace=None):
    old_tag = args.old_tag.strip()
    new_tag = args.new_tag.strip()
    apply = getattr(args, "apply", False)
    if workspace is None:
        workspace = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config = load_tag_config(tags_json_path)

    print("=" * 60)
    mode_str = "正式执行落盘" if apply else "Dry-Run 预演"
    print(f"🔄 [Tag Rename 级联重命名] {old_tag} -> {new_tag} ({mode_str})")
    print("=" * 60)

    affected_files = []
    scan_dirs = ["wiki", "raw", "Clippings"]
    for sdir in scan_dirs:
        dir_p = os.path.join(workspace, sdir)
        if not os.path.exists(dir_p):
            continue
        for root, _, files in os.walk(dir_p):
            for file in sorted(files):
                if not file.endswith(".md"):
                    continue
                fpath = os.path.join(root, file)
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
                        content = fp.read()
                except Exception:
                    continue
                
                m = re.match(r"^---\n(.*?)\n---(.*)", content, re.DOTALL)
                if not m:
                    continue
                try:
                    data = yaml.safe_load(m.group(1))
                    if not isinstance(data, dict):
                        continue
                    tags = data.get("tags")
                    if isinstance(tags, list) and old_tag in tags:
                        affected_files.append((fpath, content, m.group(1), m.group(2), data))
                except Exception:
                    continue

    print(f"📊 扫描完成！发现全库共有 {len(affected_files)} 篇文档使用了标签 '{old_tag}'。")
    for fpath, _, _, _, _ in affected_files:
        rel = os.path.relpath(fpath, workspace)
        print(f"  📄 [{rel}]")

    if apply:
        for fpath, _, _, body, data in affected_files:
            new_tags = [new_tag if t == old_tag else t for t in data.get("tags", [])]
            seen = set()
            unique_tags = []
            for t in new_tags:
                if t not in seen:
                    unique_tags.append(t)
                    seen.add(t)
            data["tags"] = unique_tags
            new_fm = yaml.dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False).strip()
            with open(fpath, "w", encoding="utf-8") as fp:
                fp.write(f"---\n{new_fm}\n---{body}")
        
        # 更新 tags.json 中的定义
        if "/" not in old_tag:
            if old_tag in config.get("top_level_tags", []):
                config["top_level_tags"].remove(old_tag)
        else:
            b_old, l_old = old_tag.split("/", 1)
            if b_old in config.get("branches", {}):
                if l_old in config["branches"][b_old].get("leaves", []):
                    config["branches"][b_old]["leaves"].remove(l_old)
                if l_old in config["branches"][b_old].get("multi_level", []):
                    config["branches"][b_old]["multi_level"].remove(l_old)
        
        if "/" not in new_tag:
            if new_tag not in config.setdefault("top_level_tags", []):
                config["top_level_tags"].append(new_tag)
        else:
            parts = new_tag.split("/")
            b_new = parts[0]
            if len(parts) == 2:
                l_new = parts[1]
                b_dict = config.setdefault("branches", {}).setdefault(b_new, {"description": f"{b_new} 分支", "leaves": []})
                if l_new not in b_dict.setdefault("leaves", []):
                    b_dict["leaves"].append(l_new)
            else:
                ml_new = "/".join(parts[1:])
                b_dict = config.setdefault("branches", {}).setdefault(b_new, {"description": f"{b_new} 分支", "leaves": []})
                if ml_new not in b_dict.setdefault("multi_level", []):
                    b_dict.setdefault("multi_level", []).append(ml_new)
                if parts[1] not in b_dict.setdefault("leaves", []):
                    b_dict["leaves"].append(parts[1])

        save_tag_config(config, tags_json_path)
        print(f"\n✅ 级联重命名完成！已成功将 {len(affected_files)} 篇文档中的 '{old_tag}' 迁移至 '{new_tag}'，并更新 tags.json。")
    else:
        print("\n✅ Dry-run 预演完成！若确认执行级联修改，请追加 --apply 参数。")


def cmd_delete(args, tags_json_path=None, workspace=None):
    tag = args.tag.strip()
    apply = getattr(args, "apply", False)
    if workspace is None:
        workspace = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config = load_tag_config(tags_json_path)

    print("=" * 60)
    mode_str = "正式执行落盘" if apply else "Dry-Run 预演"
    print(f"🗑️  [Tag Delete 级联删除] {tag} ({mode_str})")
    print("=" * 60)

    affected_files = []
    scan_dirs = ["wiki", "raw", "Clippings"]
    for sdir in scan_dirs:
        dir_p = os.path.join(workspace, sdir)
        if not os.path.exists(dir_p):
            continue
        for root, _, files in os.walk(dir_p):
            for file in sorted(files):
                if not file.endswith(".md"):
                    continue
                fpath = os.path.join(root, file)
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
                        content = fp.read()
                except Exception:
                    continue
                
                m = re.match(r"^---\n(.*?)\n---(.*)", content, re.DOTALL)
                if not m:
                    continue
                try:
                    data = yaml.safe_load(m.group(1))
                    if not isinstance(data, dict):
                        continue
                    tags = data.get("tags")
                    if isinstance(tags, list) and tag in tags:
                        affected_files.append((fpath, content, m.group(1), m.group(2), data))
                except Exception:
                    continue

    print(f"📊 扫描完成！发现全库共有 {len(affected_files)} 篇文档使用了标签 '{tag}'。")
    for fpath, _, _, _, _ in affected_files:
        rel = os.path.relpath(fpath, workspace)
        print(f"  📄 [{rel}]")

    if apply:
        for fpath, _, _, body, data in affected_files:
            new_tags = [t for t in data.get("tags", []) if t != tag]
            data["tags"] = new_tags
            new_fm = yaml.dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False).strip()
            with open(fpath, "w", encoding="utf-8") as fp:
                fp.write(f"---\n{new_fm}\n---{body}")
        
        # 更新 tags.json 中的定义
        if "/" not in tag:
            if tag in config.get("top_level_tags", []):
                config["top_level_tags"].remove(tag)
        else:
            b, l = tag.split("/", 1)
            if b in config.get("branches", {}):
                if l in config["branches"][b].get("leaves", []):
                    config["branches"][b]["leaves"].remove(l)
                if l in config["branches"][b].get("multi_level", []):
                    config["branches"][b]["multi_level"].remove(l)

        save_tag_config(config, tags_json_path)
        print(f"\n✅ 级联删除完成！已成功从 {len(affected_files)} 篇文档及 tags.json 中移除标签 '{tag}'。")
    else:
        print("\n✅ Dry-run 预演完成！若确认执行级联删除，请追加 --apply 参数。")


def main():
    parser = argparse.ArgumentParser(description="Knowledge Bank Tag Manager")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    p_list = subparsers.add_parser("list", help="列出所有经审批的标准标签")
    p_list.set_defaults(func=cmd_list)

    p_val = subparsers.add_parser("validate", help="校验 Tag 合规性")
    p_val.add_argument("tag", help="待校验的 Tag 字符串")
    p_val.add_argument("--ptype", default="source", help="目标页面类型 (source/concept/entity/comparison/overview)")
    p_val.set_defaults(func=cmd_validate)

    p_scan = subparsers.add_parser("scan", help="全库扫描所有文档的 Tag 合规性")
    p_scan.set_defaults(func=cmd_scan)

    p_add = subparsers.add_parser("add", help="新增审批 Tag 到 tags.json")
    p_add.add_argument("tag", help="新增的 Tag 字符串 (如 AI-Agent/embodied)")
    p_add.add_argument("--desc", default="", help="标签描述")
    p_add.set_defaults(func=cmd_add)

    p_ren = subparsers.add_parser("rename", help="全库级联重命名 Tag")
    p_ren.add_argument("old_tag", help="原 Tag")
    p_ren.add_argument("new_tag", help="新 Tag")
    p_ren.add_argument("--apply", action="store_true", help="正式落盘应用更改")
    p_ren.set_defaults(func=cmd_rename)

    p_del = subparsers.add_parser("delete", help="全库级联删除 Tag")
    p_del.add_argument("tag", help="待删除的 Tag")
    p_del.add_argument("--apply", action="store_true", help="正式落盘应用更改")
    p_del.set_defaults(func=cmd_delete)

    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(0)
    args.func(args)


if __name__ == "__main__":
    main()
