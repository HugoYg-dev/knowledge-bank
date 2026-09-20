# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyyaml>=6.0",
# ]
# ///

"""
Concept Upstream Sources Analysis and Deep Cleanup Tool
针对 wiki/concepts/ 目录下的所有概念页面进行「上游来源（Upstream Sources）独立分析与深度清理」
"""

import os
import sys
import re
import json
import yaml
import argparse
from datetime import datetime

def get_workspace():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(script_dir)

def load_file(path):
    if not os.path.exists(path):
        return ""
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def save_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def scan_sources_and_raw(workspace):
    """
    扫描 wiki/sources 和 raw 目录，建立真实存在的物理文件映射和正文缓存
    """
    target_to_relpaths = {}
    source_contents = {}
    
    folders = ['wiki/sources', 'raw']
    for folder in folders:
        folder_dir = os.path.join(workspace, folder)
        if not os.path.exists(folder_dir):
            continue
        for root, _, files in os.walk(folder_dir):
            for f in files:
                if not f.endswith('.md'):
                    continue
                abs_p = os.path.join(root, f)
                rel_p = os.path.relpath(abs_p, workspace)
                
                # 读取正文
                content = load_file(abs_p)
                source_contents[rel_p] = content
                
                # 建立多维度目标映射
                base_md = f  # e.g. xxx.md
                base_no_md = f[:-3]  # e.g. xxx
                
                keys = [
                    rel_p,                   # wiki/sources/xxx.md or raw/xxx.md
                    rel_p[:-3],              # wiki/sources/xxx or raw/xxx
                    base_md,                 # xxx.md
                    base_no_md,              # xxx
                    f"sources/{base_md}",    # sources/xxx.md (if in wiki/sources)
                    f"sources/{base_no_md}"  # sources/xxx
                ]
                for k in keys:
                    if k not in target_to_relpaths:
                        target_to_relpaths[k] = set()
                    target_to_relpaths[k].add(rel_p)
                    
    return target_to_relpaths, source_contents

def extract_wikilinks(text):
    """提取文本中的所有 [[link]] 目标"""
    link_regex = re.compile(r'\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]')
    return [m.strip() for m in link_regex.findall(text)]

def analyze_all_concepts(workspace):
    target_to_relpaths, source_contents = scan_sources_and_raw(workspace)
    
    concepts_dir = os.path.join(workspace, 'wiki', 'concepts')
    if not os.path.exists(concepts_dir):
        print("❌ wiki/concepts/ 目录不存在！")
        return []
        
    concept_files = sorted([f for f in os.listdir(concepts_dir) if f.endswith('.md')])
    print(f"📊 共发现 {len(concept_files)} 个概念文件，开始独立分析...")
    
    results = []
    
    for f in concept_files:
        rel_p = f"wiki/concepts/{f}"
        abs_p = os.path.join(concepts_dir, f)
        content = load_file(abs_p)
        
        m = re.match(r'^(---\n.*?\n---)(.*)', content, re.DOTALL)
        if m:
            fm_str, body = m.group(1), m.group(2)
            content_inside = fm_str
            if content_inside.startswith('---\n'):
                content_inside = content_inside[4:]
            elif content_inside.startswith('---'):
                content_inside = content_inside[3:]
            if content_inside.endswith('\n---'):
                content_inside = content_inside[:-4]
            elif content_inside.endswith('---'):
                content_inside = content_inside[:-3]
            try:
                fm_data = yaml.safe_load(content_inside) or {}
            except Exception as e:
                print(f"⚠️ YAML 解析失败: {rel_p} ({e})")
                fm_data = {}
        else:
            fm_str, body, fm_data = "", content, {}
            
        # 1. 显式指向检查 (Condition 1)
        fm_sources_matched = set()
        raw_fm_sources = fm_data.get('sources', [])
        if isinstance(raw_fm_sources, str):
            raw_fm_sources = [raw_fm_sources]
        elif not isinstance(raw_fm_sources, list):
            raw_fm_sources = []
            
        for s_item in raw_fm_sources:
            if not isinstance(s_item, str):
                continue
            s_clean = s_item.strip()
            # 去除可能存在的 [[ ]]
            if s_clean.startswith('[[') and s_clean.endswith(']]'):
                s_clean = s_clean[2:-2].split('|')[0].split('#')[0].strip()
            if s_clean in target_to_relpaths:
                for matched_rel in target_to_relpaths[s_clean]:
                    fm_sources_matched.add(matched_rel)
            else:
                base = os.path.basename(s_clean)
                if base in target_to_relpaths:
                    for matched_rel in target_to_relpaths[base]:
                        fm_sources_matched.add(matched_rel)
                else:
                    base_no_ext = base[:-3] if base.endswith('.md') else base
                    if base_no_ext in target_to_relpaths:
                        for matched_rel in target_to_relpaths[base_no_ext]:
                            fm_sources_matched.add(matched_rel)
                    
        body_sources_matched = set()
        # (a) 正文中的所有 wikilink 是否指向真实 Source/Raw
        for wlink in extract_wikilinks(body):
            if wlink in target_to_relpaths:
                for matched_rel in target_to_relpaths[wlink]:
                    body_sources_matched.add(matched_rel)
                    
        # (b) 正文中包含 "来源" 或 "出处" 的行，是否包含真实 Source/Raw 标题
        for line in body.split('\n'):
            if '来源' in line or '出处' in line or 'Source' in line or 'source' in line:
                for target_key, rel_set in target_to_relpaths.items():
                    if len(target_key) >= 3 and target_key in line:
                        for matched_rel in rel_set:
                            body_sources_matched.add(matched_rel)
                            
        # 2. 隐式来历（反向关联）检查 (Condition 2)
        reverse_sources_matched = set()
        c_base = f[:-3]  # e.g. 概念_A2A协议
        c_clean = c_base[3:] if c_base.startswith('概念_') else c_base
        c_clean_space = c_clean.replace('_', ' ')
        c_clean_space2 = c_clean.replace(' ', '_')
        
        # 匹配词列表（过滤掉太短或没意义的关键词）
        search_terms = {c_base, c_clean, c_clean_space, c_clean_space2}
        search_terms = {t for t in search_terms if len(t) >= 2}
        
        for s_rel, s_text in source_contents.items():
            # 检查 wikilink
            s_links = extract_wikilinks(s_text)
            matched = False
            for slink in s_links:
                slink_base = os.path.basename(slink).replace('.md', '')
                if slink_base in {c_base, c_clean, c_clean_space, c_clean_space2}:
                    reverse_sources_matched.add(s_rel)
                    matched = True
                    break
            if matched:
                continue
                
            # 检查文本明确提及
            s_text_lower = s_text.lower()
            for term in search_terms:
                if term.lower() in s_text_lower:
                    reverse_sources_matched.add(s_rel)
                    break
                    
        # 综合判定
        all_valid_sources = sorted(list(fm_sources_matched | body_sources_matched | reverse_sources_matched))
        
        # 判定类别
        if not all_valid_sources:
            status = "ORPHAN_NO_SOURCE"
        elif set(all_valid_sources) == set(raw_fm_sources):
            status = "VALID_OK"
        else:
            status = "VALID_NEEDS_BACKFILL"
            
        results.append({
            'file': f,
            'rel_path': rel_p,
            'abs_path': abs_p,
            'status': status,
            'raw_fm_sources': raw_fm_sources,
            'all_valid_sources': all_valid_sources,
            'fm_matched': sorted(list(fm_sources_matched)),
            'body_matched': sorted(list(body_sources_matched)),
            'reverse_matched': sorted(list(reverse_sources_matched)),
            'fm_str': fm_str,
            'body': body
        })
        
    return results

def format_frontmatter_sources(fm_str, new_sources):
    """将新的 sources 数组更新到 Frontmatter 中"""
    if not fm_str:
        # 如果原来没有 Frontmatter，新建一个
        return f"---\nsources:\n" + "".join([f"- {s}\n" for s in new_sources]) + "---\n"
        
    # 尝试解析原 YAML
    content_inside = fm_str
    if content_inside.startswith('---\n'):
        content_inside = content_inside[4:]
    elif content_inside.startswith('---'):
        content_inside = content_inside[3:]
    if content_inside.endswith('\n---'):
        content_inside = content_inside[:-4]
    elif content_inside.endswith('---'):
        content_inside = content_inside[:-3]
        
    try:
        data = yaml.safe_load(content_inside) or {}
    except Exception:
        data = {}
        
    data['sources'] = new_sources
    new_yaml = yaml.dump(data, allow_unicode=True, sort_keys=False)
    return f"---\n{new_yaml}---\n"

def main():
    parser = argparse.ArgumentParser(description="Concept Upstream Sources Analysis and Deep Cleanup")
    parser.add_argument('--apply', action='store_true', help="执行实际清理与接骨回填")
    args = parser.parse_args()
    
    workspace = get_workspace()
    print(f"🏠 Workspace: {workspace}")
    print(f"🛡️ 运行模式: {'【执行动刀 (APPLY)】' if args.apply else '【预演报告 (DRY-RUN)】'}\n")
    
    results = analyze_all_concepts(workspace)
    if not results:
        return
        
    valid_ok = [r for r in results if r['status'] == 'VALID_OK']
    valid_backfill = [r for r in results if r['status'] == 'VALID_NEEDS_BACKFILL']
    orphans = [r for r in results if r['status'] == 'ORPHAN_NO_SOURCE']
    
    print("=" * 70)
    print("📑 【概念面上游来源独立分析与深度清理报告】")
    print("=" * 70)
    print(f"🔍 审查概念页面总数 : {len(results)} 个")
    print(f"✅ 来源完整无须调整 : {len(valid_ok)} 个")
    print(f"🛠️ 存在有效来源需接骨回填 : {len(valid_backfill)} 个")
    print(f"🗑️ 无源孤立/虚假生成需删除 : {len(orphans)} 个")
    print("-" * 70)
    
    if orphans:
        print("\n🚨 【无源孤立/虚假生成概念清单（物理删除候选项）】")
        for idx, o in enumerate(orphans, 1):
            print(f"  {idx:2d}. {o['rel_path']}")
            
    if valid_backfill[:10]:
        print("\n🛠️ 【需接骨回填概念示例（前10个）】")
        for idx, b in enumerate(valid_backfill[:10], 1):
            print(f"  {idx:2d}. {b['rel_path']}")
            print(f"      当前 FM sources: {b['raw_fm_sources']}")
            print(f"      溯源匹配有效 sources: {b['all_valid_sources']}")
            
    if not args.apply:
        print("\n" + "=" * 70)
        print("💡 当前为 Dry-run 预演模式，未对文件作任何实质修改。")
        print("👉 确认无误后，请执行: python3 scripts/concept_source_lint.py --apply")
        print("=" * 70)
        return
        
    print("\n⚡ 正式执行深度清理与接骨修护...")
    
    # 1. 执行接骨回填
    backfilled_count = 0
    for b in valid_backfill:
        new_fm = format_frontmatter_sources(b['fm_str'], b['all_valid_sources'])
        new_content = new_fm + b['body']
        save_file(b['abs_path'], new_content)
        backfilled_count += 1
    print(f"  ✅ 成功回填修复 {backfilled_count} 个概念页面的 sources 来源字段！")
    
    # 2. 物理删除无源孤立概念
    deleted_count = 0
    deleted_rel_paths = []
    for o in orphans:
        if os.path.exists(o['abs_path']):
            os.remove(o['abs_path'])
            deleted_count += 1
            deleted_rel_paths.append(o['rel_path'])
    print(f"  🗑️ 物理删除 {deleted_count} 个无源孤立概念文件！")
    
    # 3. 联动总索引 wiki/index.md
    index_path = os.path.join(workspace, 'wiki', 'index.md')
    index_content = load_file(index_path)
    index_lines_removed = 0
    if deleted_rel_paths:
        new_lines = []
        for line in index_content.split('\n'):
            should_remove = False
            for del_path in deleted_rel_paths:
                del_base = os.path.basename(del_path)[:-3]  # e.g. 概念_xxx
                if del_base in line or del_path in line:
                    should_remove = True
                    break
            if should_remove:
                index_lines_removed += 1
            else:
                new_lines.append(line)
        save_file(index_path, '\n'.join(new_lines))
    print(f"  ✅ 已精准剔除 wiki/index.md 中的相关废弃索引条目共 {index_lines_removed} 行！")
    
    # 4. 登记维护日志
    log_path = os.path.join(workspace, 'wiki', 'log.md')
    log_content = load_file(log_path)
    today = datetime.now().strftime("%Y-%m-%d")
    log_msg = (
        f"## [{today}] lint/clean-concepts | 上游来源（Upstream Sources）独立分析与深度清理（审查 {len(results)} 个概念，修复回填 {backfilled_count} 个，物理删除 {deleted_count} 个）\n"
        f"- **独立分析与接骨修护**：对 `wiki/concepts/` 下全部 {len(results)} 个概念页面进行了显式与反向隐式上游来源追踪，为 {backfilled_count} 个具备真实有效上游来源的概念页面完成了“接骨修护”与来源字段自动化回填。\n"
        f"- **无源孤立虚假生成清理**：识别并物理删除 {deleted_count} 个既无显式来源指向、全库正文亦无任何提及引用的无上游来源虚假/孤立概念文件。\n"
        f"- **总索引联动同步**：同步自 `wiki/index.md` 中精准移除被删概念对应的 {index_lines_removed} 行索引条目，确保总索引与物理文件 100% 对应。\n"
    )
    if "# Wiki Log\n\n" in log_content:
        new_log = log_content.replace("# Wiki Log\n\n", f"# Wiki Log\n\n{log_msg}\n")
    elif "# 维护日志\n\n" in log_content:
        new_log = log_content.replace("# 维护日志\n\n", f"# 维护日志\n\n{log_msg}\n")
    else:
        new_log = log_content + f"\n\n{log_msg}"
    save_file(log_path, new_log)
    print("  ✅ 已记录操作流水至 wiki/log.md！")
    
    print("\n🏁 「上游来源独立分析与深度清理」闭环任务全部完成！")

if __name__ == '__main__':
    main()
