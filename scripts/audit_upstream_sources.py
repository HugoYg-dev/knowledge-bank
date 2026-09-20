# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyyaml>=6.0",
# ]
# ///

"""
Knowledge Bank Upstream Sources Auditor and Cleaner
审查并纠偏 wiki/entities/ 与 wiki/concepts/ 页面中的 sources 上游来源字段。
严格遵循 AGENTS.md 规范：
1. 末端产物的 sources 必须且只能是真实存在的 wiki/sources/*.md
2. 剔除张冠李戴的虚假关联（Phantom Sources）
3. 补齐正文中明确双链引用的合法上游 Source
"""

import os
import sys
import re
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

def scan_sources(workspace):
    sources_dir = os.path.join(workspace, 'wiki', 'sources')
    source_files = {}
    if not os.path.exists(sources_dir):
        return source_files
        
    for sf in sorted(os.listdir(sources_dir)):
        if not sf.endswith('.md'):
            continue
        sp = os.path.join(sources_dir, sf)
        content = load_file(sp)
        # 提取所有 wikilinks
        links = set(re.findall(r'\[\[([^\]|#]+)', content))
        source_files[sf] = {
            'rel': f'wiki/sources/{sf}',
            'abs': sp,
            'content': content,
            'links': links
        }
    return source_files

def get_exact_variants(base_name, prefix):
    clean_name = base_name[len(prefix):] if base_name.startswith(prefix) else base_name
    variants = set()
    variants.add(clean_name)
    variants.add(clean_name.replace('_', ' '))
    variants.add(clean_name.replace('_', ''))
    variants.add(clean_name.replace('-', ' '))
    variants.add(clean_name.replace('-', ''))
    # 处理中英混合命名 如: 扩散大语言模型_dLLMs -> 扩散大语言模型, dLLMs
    if '_' in clean_name:
        for part in clean_name.split('_'):
            if len(part) >= 2:
                variants.add(part)
    return {v.strip() for v in variants if len(v.strip()) >= 2}

def audit_directory(workspace, source_files, folder_name, prefix):
    folder_dir = os.path.join(workspace, 'wiki', folder_name)
    if not os.path.exists(folder_dir):
        return []
        
    files = sorted([f for f in os.listdir(folder_dir) if f.endswith('.md')])
    results = []
    
    for f in files:
        rel_p = f'wiki/{folder_name}/{f}'
        abs_p = os.path.join(folder_dir, f)
        content = load_file(abs_p)
        
        m = re.match(r'^(---\n.*?\n---)(.*)', content, re.DOTALL)
        if not m:
            continue
        fm_str, body = m.group(1), m.group(2)
        
        content_inside = fm_str
        if content_inside.startswith('---\n'): content_inside = content_inside[4:]
        elif content_inside.startswith('---'): content_inside = content_inside[3:]
        if content_inside.endswith('\n---'): content_inside = content_inside[:-4]
        elif content_inside.endswith('---'): content_inside = content_inside[:-3]
        
        try:
            fm_data = yaml.safe_load(content_inside) or {}
        except Exception:
            continue
            
        current_sources = fm_data.get('sources', [])
        if isinstance(current_sources, str):
            current_sources = [current_sources]
        elif not isinstance(current_sources, list):
            current_sources = []
            
        base_name = f[:-3]
        variants = get_exact_variants(base_name, prefix)
        
        # 1. 发现正向与反向强关联 sources
        proven_sources = set()
        
        # A. 正向：Source 正文中明确包含指向本页面的 Wikilink
        for sf, sdata in source_files.items():
            for link in sdata['links']:
                link_clean = link.strip().split('|')[0].strip()
                link_base = os.path.basename(link_clean).replace('.md', '')
                if link_base == base_name or link_base == base_name[len(prefix):]:
                    proven_sources.add(sdata['rel'])
                    break
                    
        # B. 反向：本页面正文中明确通过 Wikilink 或标题引用了该 Source
        for sf, sdata in source_files.items():
            sf_no_ext = sf[:-3]
            if f'[[{sf_no_ext}]]' in body or f'[[wiki/sources/{sf_no_ext}]]' in body or f'[[{sf}]]' in body or f'[[wiki/sources/{sf}]]' in body:
                proven_sources.add(sdata['rel'])
                
        # 2. 校验当前 FM sources
        validated_sources = set()
        phantom_sources = []
        for s in current_sources:
            if not isinstance(s, str):
                continue
            s_clean = s.strip()
            if s_clean.startswith('[[') and s_clean.endswith(']]'):
                s_clean = s_clean[2:-2].split('|')[0].strip()
            if not s_clean.endswith('.md'):
                s_clean += '.md'
            base_sf = os.path.basename(s_clean)
            
            # 若不是合法的 Source 文件（例如指向 raw 或不存在的文件）
            if base_sf not in source_files:
                phantom_sources.append(s)
                continue
                
            sdata = source_files[base_sf]
            rel_s = sdata['rel']
            
            if rel_s in proven_sources:
                validated_sources.add(rel_s)
                continue
                
            # 正文文本匹配检查（必须匹配完整专名）
            text_matched = False
            for v in variants:
                if len(v) >= 3:
                    escaped_v = re.escape(v)
                    pattern = r'(?<![\\])\b' + escaped_v + r'\b'
                    if re.search(pattern, sdata['content'], re.IGNORECASE):
                        text_matched = True
                        break
                elif len(v) >= 2 and not v.isascii():
                    if v in sdata['content']:
                        text_matched = True
                        break
            if text_matched:
                validated_sources.add(rel_s)
            else:
                phantom_sources.append(s)
                
        # 综合最终合规 sources
        final_sources = sorted(list(validated_sources | proven_sources))
        
        # 保底机制：若全部过滤为空但当前有合法 source，保留第一个存在的 source，绝不产生空列表
        if not final_sources and current_sources:
            for s in current_sources:
                base_sf = os.path.basename(s)
                if not base_sf.endswith('.md'): base_sf += '.md'
                if base_sf in source_files:
                    final_sources.append(source_files[base_sf]['rel'])
                    break
                    
        # 判断是否有变更
        if set(final_sources) != set(current_sources):
            removed = [s for s in current_sources if s not in final_sources]
            added = [s for s in final_sources if s not in current_sources]
            results.append({
                'file': f,
                'rel_path': rel_p,
                'abs_path': abs_p,
                'fm_data': fm_data,
                'fm_str': fm_str,
                'body': body,
                'before': current_sources,
                'after': final_sources,
                'removed': removed,
                'added': added
            })
            
    return results

def format_frontmatter_sources(fm_str, new_sources):
    content_inside = fm_str
    if content_inside.startswith('---\n'): content_inside = content_inside[4:]
    elif content_inside.startswith('---'): content_inside = content_inside[3:]
    if content_inside.endswith('\n---'): content_inside = content_inside[:-4]
    elif content_inside.endswith('---'): content_inside = content_inside[:-3]
    
    try:
        data = yaml.safe_load(content_inside) or {}
    except Exception:
        data = {}
        
    data['sources'] = new_sources
    new_yaml = yaml.dump(data, allow_unicode=True, sort_keys=False)
    return f"---\n{new_yaml}---\n"

def main():
    parser = argparse.ArgumentParser(description="Audit and clean upstream sources in Wiki Entities and Concepts")
    parser.add_argument('--apply', action='store_true', help="执行实际修复与回填")
    args = parser.parse_args()
    
    workspace = get_workspace()
    print(f"🏠 Workspace: {workspace}")
    print(f"🛡️ 运行模式: {'【执行动刀 (APPLY)】' if args.apply else '【预演报告 (DRY-RUN)】'}\n")
    
    source_files = scan_sources(workspace)
    print(f"📊 扫描到真实有效的 Source 摘要页共 {len(source_files)} 篇\n")
    
    entity_results = audit_directory(workspace, source_files, 'entities', '实体_')
    concept_results = audit_directory(workspace, source_files, 'concepts', '概念_')
    
    print("=" * 70)
    print("📑 【Wiki 实体与概念上游来源 (Upstream Sources) 深度审查报告】")
    print("=" * 70)
    print(f"🔍 实体页面待调整数 : {len(entity_results)} 个")
    print(f"🔍 概念页面待调整数 : {len(concept_results)} 个")
    print("-" * 70)
    
    if entity_results:
        print("\n🏛️ 【实体页典型修复示例 (前 5 个)】")
        for r in entity_results[:5]:
            print(f"  📄 {r['rel_path']}:")
            if r['removed']: print(f"     ❌ 剔除虚假来源 (Phantom): {r['removed']}")
            if r['added']:   print(f"     ➕ 补齐真实引用 (Added)  : {r['added']}")
            print(f"     👉 最终合规 sources: {r['after']}")
            
    if concept_results:
        print("\n💡 【概念页典型修复示例 (前 5 个)】")
        for r in concept_results[:5]:
            print(f"  📄 {r['rel_path']}:")
            if r['removed']: print(f"     ❌ 剔除虚假来源 (Phantom): {r['removed']}")
            if r['added']:   print(f"     ➕ 补齐真实引用 (Added)  : {r['added']}")
            print(f"     👉 最终合规 sources: {r['after']}")
            
    if not args.apply:
        print("\n" + "=" * 70)
        print("💡 当前为 Dry-run 预演模式，未对文件作任何实质修改。")
        print("👉 确认无误后，请执行: python3 scripts/audit_upstream_sources.py --apply")
        print("=" * 70)
        return
        
    print("\n⚡ 正式开始执行 Frontmatter sources 字段纠偏与规范化回填...")
    
    all_results = entity_results + concept_results
    modified_count = 0
    for r in all_results:
        new_fm = format_frontmatter_sources(r['fm_str'], r['after'])
        new_content = new_fm + r['body'].lstrip('\n')
        save_file(r['abs_path'], new_content)
        modified_count += 1
        
    print(f"  ✅ 成功清洗并规范化修复 {modified_count} 个页面（{len(entity_results)} 实体 + {len(concept_results)} 概念）的 sources 字段！")
    
    # 记录维护日志
    log_path = os.path.join(workspace, 'wiki', 'log.md')
    log_content = load_file(log_path)
    today = datetime.now().strftime("%Y-%m-%d")
    log_msg = (
        f"## [{today}] refactor/lint | 实体与概念上游来源 (sources) 全量纠偏与规范化（修复 {modified_count} 篇：{len(entity_results)} 实体 + {len(concept_results)} 概念）\n"
        f"- **虚假来源清洗 (Phantom Removal)**：严格比对全库双链与专名提及，剔除早期生成遗留的张冠李戴无关 Source（如 `实体_Gamma` 挂载 PyTorch 代码等）。\n"
        f"- **真实双链补全**：全面对齐 Source 摘要页的物理出链与末端页面的反向引用，补齐合规 sources 列表。\n"
        f"- **分层溯源纪律达成**：末端产物 100% 仅指向 `wiki/sources/`，彻底杜绝越级与断链。\n"
    )
    if "# Wiki Log\n\n" in log_content:
        new_log = log_content.replace("# Wiki Log\n\n", f"# Wiki Log\n\n{log_msg}\n")
    else:
        new_log = f"# Wiki Log\n\n{log_msg}\n" + log_content
    save_file(log_path, new_log)
    print("  ✅ 已记录操作流水至 wiki/log.md！")
    print("\n🏁 「上游 sources 全量纠偏与规范化」闭环执行完毕！")

if __name__ == '__main__':
    main()
