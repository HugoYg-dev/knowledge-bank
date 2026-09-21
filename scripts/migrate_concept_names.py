# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyyaml>=6.0",
# ]
# ///

"""
scripts/migrate_concept_names.py - 概念命名标准化迁移执行工具

支持批量重命名概念文件、原子替换全库双链引用、更新 Frontmatter aliases、同步 wiki/index.md 与 wiki/log.md。
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any

from vault_utils import (
    extract_frontmatter,
    dump_frontmatter,
    get_workspace,
    read_text,
    write_text,
)


def load_batch_config(config_path: Path) -> list[dict[str, Any]]:
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def update_concept_frontmatter(
    content: str,
    old_stems: list[str],
    new_stem: str,
    added_aliases: list[str],
    updated_date: str = "2026-09-21",
) -> str:
    fm_data, _, body, err = extract_frontmatter(content)
    if err or fm_data is None:
        raise ValueError(f"Frontmatter 解析失败: {err}")

    # 规范化 aliases
    existing_aliases = fm_data.get("aliases", [])
    if isinstance(existing_aliases, str):
        existing_aliases = [existing_aliases]
    elif not isinstance(existing_aliases, list):
        existing_aliases = []

    merged_aliases: list[str] = []
    seen = set()

    for a in existing_aliases:
        a_str = str(a).strip()
        if a_str and a_str not in seen:
            seen.add(a_str)
            merged_aliases.append(a_str)

    for a in added_aliases:
        a_str = str(a).strip()
        if a_str and a_str not in seen:
            seen.add(a_str)
            merged_aliases.append(a_str)

    # 确保旧 stem 也作为别名以保证历史检索兼容
    for old_s in old_stems:
        if old_s not in seen:
            seen.add(old_s)
            merged_aliases.append(old_s)

    fm_data["aliases"] = merged_aliases
    fm_data["updated"] = updated_date

    # 更新正文首行一级标题（若匹配旧名）
    lines = body.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("# "):
            for old_s in old_stems:
                old_core = old_s.replace("概念_", "")
                if old_s in line or old_core in line:
                    lines[i] = f"# {new_stem}"
                    break
            break
    new_body = "\n".join(lines)
    return dump_frontmatter(fm_data, new_body)


def run_migration(batch_file: str, dry_run: bool = False) -> None:
    ws = get_workspace()
    config_path = ws / batch_file if not Path(batch_file).is_absolute() else Path(batch_file)
    batch = load_batch_config(config_path)

    print(f"============================================================")
    print(f"🚀 [Concept Migration] 载入批次配置: {config_path.name} (共 {len(batch)} 项)")
    print(f"模式: {'[DRY RUN 预演模式 - 不修改文件]' if dry_run else '[EXECUTE 执行模式 - 真实写入]'}")
    print(f"============================================================")

    # 建立 old_stem -> new_stem 映射
    stem_map: dict[str, str] = {}
    for item in batch:
        old_stem = item["old_stem"]
        new_stem = item["new_stem"]
        stem_map[old_stem] = new_stem
        if item.get("action") == "merge" and "secondary_stem" in item:
            stem_map[item["secondary_stem"]] = new_stem

    # 1. 概念文件重命名与 Frontmatter 处理
    concepts_dir = ws / "wiki" / "concepts"
    file_ops = []

    for item in batch:
        action = item.get("action", "rename")
        old_stem = item["old_stem"]
        new_stem = item["new_stem"]
        aliases = item.get("aliases", [])

        if action == "rename":
            old_path = concepts_dir / f"{old_stem}.md"
            new_path = concepts_dir / f"{new_stem}.md"

            if not old_path.exists():
                print(f"⚠️ [跳过] 原文件不存在: {old_path.name}")
                continue

            content = read_text(old_path)
            new_content = update_concept_frontmatter(
                content=content,
                old_stems=[old_stem],
                new_stem=new_stem,
                added_aliases=aliases,
            )
            file_ops.append(("rename", old_path, new_path, new_content))

        elif action == "merge":
            old_path = concepts_dir / f"{old_stem}.md"
            sec_stem = item.get("secondary_stem")
            sec_path = concepts_dir / f"{sec_stem}.md" if sec_stem else None
            new_path = concepts_dir / f"{new_stem}.md"

            if not old_path.exists() or (sec_path and not sec_path.exists()):
                print(f"⚠️ [跳过] 合并源文件不齐全: {old_stem} 或 {sec_stem}")
                continue

            # 特殊合并处理 IVF
            content_1 = read_text(old_path)
            content_2 = read_text(sec_path) if sec_path else ""

            fm_1, _, body_1, _ = extract_frontmatter(content_1)
            fm_2, _, body_2, _ = extract_frontmatter(content_2)

            sources_merged = list(dict.fromkeys((fm_1.get("sources", []) if fm_1 else []) + (fm_2.get("sources", []) if fm_2 else [])))
            tags_merged = list(dict.fromkeys((fm_1.get("tags", []) if fm_1 else []) + (fm_2.get("tags", []) if fm_2 else [])))
            summary_merged = "基于聚类空间划分的高维向量近似最近邻搜索（ANNS）索引算法，通过质心分组建立倒排映射，大幅缩小检索计算量。"

            merged_fm = {
                "type": "concept",
                "tags": tags_merged,
                "summary": summary_merged,
                "aliases": aliases,
                "sources": sources_merged,
                "updated": "2026-09-21",
            }

            # 结构化合并正文
            merged_body = r"""# 概念_IVF_倒排索引 (Inverted File Index)

## 定义与核心机制

**倒排文件索引（Inverted File Index, IVF）**是一种高维向量的近似最近邻搜索（ANNS）索引技术。其核心思想源于传统信息检索中的“倒排索引”（将文档映射到词项），在向量空间中，它通过聚类算法（通常是 K-Means）将向量数据集划分到不同的空间胞腔（Voronoi Partitions/Cells）中，并建立“质心 $\\to$ 胞腔内向量列表”的倒排映射。

在检索时，只需计算查询向量与各个胞腔质心的距离，找出最邻近的质心，然后仅在这些胞腔的倒排列表中进行细粒度距离计算，从而避免全库暴力扫描。

## 索引构建与两阶段检索

1. **聚类空间划分（Partitioning）**：使用 K-Means 将全量 $N$ 个 $D$ 维向量聚类为 $K$ 个簇（Partitions），产生 $K$ 个中心点向量（Centroids）。
2. **倒排列表挂载（Inverted Lists）**：每个数据向量按最近距离归属于某一个质心，挂载在该质心的倒排列表中。
3. **两阶段检索流程**：
   - **粗粒度过滤（Coarse Filtering）**：计算查询向量与 $K$ 个质心的距离，选出最近的 $n_{\\text{probe}}$ 个质心。时间复杂度为 $O(KD)$。
   - **细粒度精搜（Fine Search）**：仅在这 $n_{\\text{probe}}$ 个胞腔的并集倒排列表中计算详细距离。在均布假设下时间复杂度为 $O(\\frac{n_{\\text{probe}} \\cdot ND}{K})$。

相比暴力 kNN 的 $O(ND)$ 复杂度，IVF 检索复杂度为 $O(KD + \\frac{n_{\\text{probe}}ND}{K})$。例如在 $N=10\\text{M}, K=100, n_{\\text{probe}}=1$ 时，计算量由 10,000,000 降至约 100,100，实现接近 **100 倍**的检索加速。

## 精度与延迟折中 (Accuracy-Latency Trade-off)

- **边界向量遗漏**：若查询向量落在胞腔边界，真实最近邻可能分布在相邻胞腔，仅探查最近单个胞腔会导致漏检。
- **探查参数 $n_{\\text{probe}}$**：增大 $n_{\\text{probe}}$ 会探查更多相邻胞腔，显著提升召回率（Recall），但会线性增加距离计算耗时。
- **内存与工程选型**：IVF 内存占用远低于 [[entities/实体_HNSW|HNSW]]，且非常适合结合 PQ（乘积量化，形成 IVF-PQ）在超大规模数据集上运行。代表实现包括 [[entities/实体_Faiss|Faiss]]、[[entities/实体_Milvus|Milvus]] 与 [[entities/实体_pgvector|pgvector]]。

## 关联

- 相关概念：[[concepts/概念_向量数据库]]、[[concepts/概念_近似最近邻搜索]]、[[concepts/概念_向量索引方法]]、[[concepts/概念_向量量化]]
- 实体：[[entities/实体_Faiss]]、[[entities/实体_Milvus]]、[[entities/实体_pgvector|pgvector]]
- 物理文献：[[2025-10-27_ANN-search-using-inverted-file-index_19a274]]、[[2026程序员必读的向量数据库原理与选型指南]]
"""
            new_content = dump_frontmatter(merged_fm, merged_body)
            file_ops.append(("merge", [old_path, sec_path], new_path, new_content))

        elif action == "merge_existing":
            old_path = concepts_dir / f"{old_stem}.md"
            target_path = concepts_dir / f"{new_stem}.md"
            if not old_path.exists() or not target_path.exists():
                print(f"⚠️ [跳过] 目标或原文件不存在: {old_path.name} / {target_path.name}")
                continue

            content_old = read_text(old_path)
            content_target = read_text(target_path)
            fm_old, _, body_old, _ = extract_frontmatter(content_old)
            fm_target, _, body_target, _ = extract_frontmatter(content_target)

            sources_merged = list(dict.fromkeys((fm_target.get("sources", []) if fm_target else []) + (fm_old.get("sources", []) if fm_old else [])))
            tags_merged = list(dict.fromkeys((fm_target.get("tags", []) if fm_target else []) + (fm_old.get("tags", []) if fm_old else [])))
            aliases_merged = list(dict.fromkeys((fm_target.get("aliases", []) if fm_target else []) + aliases + [old_stem]))

            target_fm = fm_target.copy() if fm_target else {}
            target_fm["sources"] = sources_merged
            target_fm["tags"] = tags_merged
            target_fm["aliases"] = aliases_merged
            target_fm["updated"] = "2026-09-21"

            new_body = body_target
            if "## 两大类框架" in body_old and "## 两大类框架" not in body_target:
                m = re.search(r"(## 两大类框架[\s\S]*?)(?=\n## |\Z)", body_old)
                if m:
                    framework_section = m.group(1).strip()
                    if "## 关联" in new_body:
                        new_body = new_body.replace("## 关联", framework_section + "\n\n## 关联")
                    else:
                        new_body = new_body.rstrip() + "\n\n" + framework_section + "\n"

            new_content = dump_frontmatter(target_fm, new_body)
            file_ops.append(("merge_existing", [old_path], target_path, new_content))

    print(f"\n📂 计划执行物理文件变更 ({len(file_ops)} 项):")
    for op in file_ops:
        if op[0] == "rename":
            print(f"  [RENAME] {op[1].name} -> {op[2].name}")
        elif op[0] in ("merge", "merge_existing"):
            src_names = ", ".join(p.name for p in op[1] if p)
            print(f"  [MERGE]  {src_names} -> {op[2].name}")

    # 2. 全库双链替换
    def scan_and_replace_links(target_files: list[Path]) -> tuple[dict[Path, list[tuple[str, str]]], dict[Path, str]]:
        replacements: dict[Path, list[tuple[str, str]]] = {}
        new_contents: dict[Path, str] = {}

        for file_path in target_files:
            content = read_text(file_path)
            modified = False
            new_content = content

            for old_stem, new_stem in stem_map.items():
                pattern = re.compile(r"\[\[((?:wiki/)?(?:concepts/)?)(" + re.escape(old_stem) + r")(?:\.md)?(\|.*?)?\]\]")
                if pattern.search(new_content):
                    def make_repl(n_stem: str):
                        def repl(match: re.Match) -> str:
                            prefix = match.group(1) or ""
                            suffix = match.group(3) or ""
                            return f"[[{prefix}{n_stem}{suffix}]]"
                        return repl

                    new_c, count = pattern.subn(make_repl(new_stem), new_content)
                    if count > 0:
                        modified = True
                        new_content = new_c
                        if file_path not in replacements:
                            replacements[file_path] = []
                        replacements[file_path].append((old_stem, f"{new_stem} ({count}处)"))

            if modified:
                new_contents[file_path] = new_content

        return replacements, new_contents

    def get_all_md_files() -> list[Path]:
        res: list[Path] = []
        for folder in ("wiki", "raw"):
            folder_path = ws / folder
            if folder_path.exists():
                for root, dirs, files in os.walk(folder_path):
                    dirs[:] = [d for d in dirs if d not in {".git", ".obsidian", "tmp"}]
                    for f in files:
                        if f.endswith(".md"):
                            res.append(Path(root) / f)
        return res

    # 预演模式分析
    initial_files = get_all_md_files()
    link_replacements, file_new_contents = scan_and_replace_links(initial_files)

    total_refs = sum(len(v) for v in link_replacements.values())
    print(f"\n🔗 扫描全库双链引用：共发现 {len(link_replacements)} 个文件涉及 {total_refs} 组双链更新：")
    for fp, changes in sorted(link_replacements.items(), key=lambda x: str(x[0])):
        rel_p = fp.relative_to(ws)
        ch_str = ", ".join(f"{old} -> {new}" for old, new in changes)
        print(f"  - {rel_p}: {ch_str}")

    # 3. 执行写入
    if dry_run:
        print(f"\n✨ [DRY RUN] 预演完成，未对知识库进行任何修改。")
        return

    print(f"\n💾 [EXECUTE] 正在执行文件写入与双链原子替换...")

    # 执行物理重命名与文件创建
    for op in file_ops:
        if op[0] == "rename":
            old_p, new_p, content = op[1], op[2], op[3]
            write_text(new_p, content)
            if old_p.exists() and old_p != new_p:
                old_p.unlink()
        elif op[0] in ("merge", "merge_existing"):
            src_paths, new_p, content = op[1], op[2], op[3]
            write_text(new_p, content)
            for sp in src_paths:
                if sp and sp.exists() and sp != new_p:
                    sp.unlink()

    # 物理文件变更后重新扫描全库，对包括新文件在内的所有文档执行双链写入
    all_current_files = get_all_md_files()
    _, final_new_contents = scan_and_replace_links(all_current_files)

    # 对 wiki/index.md 专门检查与去重
    index_path = ws / "wiki" / "index.md"
    index_content = final_new_contents.get(index_path, read_text(index_path))

    merged_existing_stems = [item["old_stem"] for item in batch if item.get("action") == "merge_existing"]
    if merged_existing_stems:
        lines = index_content.splitlines()
        new_lines = [l for l in lines if not any(f"[[{stem}]]" in l or f"[[concepts/{stem}]]" in l for stem in merged_existing_stems)]
        index_content = "\n".join(new_lines) + "\n"
        final_new_contents[index_path] = index_content

    if "概念_IVF_倒排索引" in str(stem_map.values()):
        lines = index_content.splitlines()
        new_lines = []
        ivf_seen = False
        for line in lines:
            if "[[概念_IVF_倒排索引]]" in line:
                if not ivf_seen:
                    new_lines.append("- [[概念_IVF_倒排索引]] — 倒排文件索引 (Inverted File Index)，基于聚类空间划分的高维向量近似最近邻搜索 (ANNS) 算法（RAG/embedding, RAG/retrieval）")
                    ivf_seen = True
                else:
                    continue
            else:
                new_lines.append(line)
        index_content = "\n".join(new_lines) + "\n"
        final_new_contents[index_path] = index_content

    for fp, new_c in final_new_contents.items():
        write_text(fp, new_c)

    # 顶部插入 wiki/log.md
    log_path = ws / "wiki" / "log.md"
    if "p2" in config_path.name.lower():
        batch_desc = "Phase 2: 69 篇纯英文概念补全核心中文名规范化"
        desc_body = "全量补全存量纯英文概念的核心中文释义，统一迁移为「英文缩写/专名 + 中文核心名」规范格式。"
    elif "p3" in config_path.name.lower():
        batch_desc = "Phase 3: 20 篇标点与分界符统一标准化"
        desc_body = "全量清理连字符 - 与中英无缝紧贴命名，统一采用标准下划线 _ 分界符规范化。"
    else:
        batch_desc = f"批量重命名 ({len(batch)} 篇)"
        desc_body = "概念命名标准化规范化处理。"

    log_entry = (
        f"## [2026-09-21] refactor/concepts | 概念命名标准化迁移 ({batch_desc}) (+ index & backlinks)\n"
        f"- **命名标准化与分界符规范化 ({len(batch)} 篇)**：\n"
        f"  - {desc_body}\n"
        f"  - 自动向目标概念页 YAML Frontmatter 注入标准 aliases 别名矩阵（覆盖英文缩写、英文全称、核心中文名与旧文件名），激活未链接提及。\n"
        f"- **全库双链与总索引原子更新**：\n"
        f"  - 遍历全库 Markdown 文档，完成对应双链引用的精准正则原子替换，确保 0 死链。\n"
        f"  - 同步更新 `wiki/index.md`，对齐最新规范概念名称与去重。\n"
    )
    if log_path.exists():
        cur_log = read_text(log_path)
        write_text(log_path, log_entry + "\n" + cur_log.lstrip())

    print(f"✅ 物理重命名、Frontmatter 注入、双链更新及日志追加已全部完成！")


def main() -> None:
    parser = argparse.ArgumentParser(description="概念命名标准化迁移工具")
    parser.add_argument("--batch", required=True, help="迁移批次 JSON 配置文件路径")
    parser.add_argument("--dry-run", action="store_true", help="预演模式，仅输出分析报告，不修改任何文件")
    parser.add_argument("--execute", action="store_true", help="执行模式，真实写入变更")

    args = parser.parse_args()

    if not args.dry_run and not args.execute:
        print("请指定 --dry-run 进行预演或 --execute 确认执行！")
        return

    run_migration(args.batch, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
