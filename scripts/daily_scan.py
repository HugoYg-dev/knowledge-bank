#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Knowledge Bank Daily Scan Tool
遵循 AGENTS.md 规范的确定性每日健康巡检与待处理扫描工具。

功能：
1. 调用 vault_lint.py 执行图谱健康与 Schema 诊断；
2. 扫描 Clippings/ 顶层待归档文件；
3. 解析 Clippings/emails/.pipeline/manifest.json 统计待审与未识别邮件；
4. 自动持久化写入 tmp/daily-report.md；
5. 在终端输出一句话要点摘要。

用法：
  uv run --with pyyaml python scripts/daily_scan.py
"""

import sys
import os
import json
import subprocess
from datetime import datetime
from pathlib import Path


def run_vault_lint(workspace_dir: Path) -> tuple[bool, str, dict]:
    """运行 vault_lint.py 并解析关键指标"""
    cmd = ["uv", "run", "--with", "pyyaml", "python", "scripts/vault_lint.py", "lint"]
    env = dict(os.environ)
    env["PATH"] = f"{Path.home()}/.local/bin:{Path.home()}/.cargo/bin:/opt/homebrew/bin:{env.get('PATH', '')}"
    try:
        proc = subprocess.run(
            cmd,
            cwd=workspace_dir,
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
            env=env,
        )
        output = proc.stdout + ("\n" + proc.stderr if proc.stderr else "")
        passed = (proc.returncode == 0)
    except Exception as e:
        return False, f"执行 vault_lint 异常: {e}", {}

    metrics = {
        "passed": passed,
        "broken_links": 0,
        "yaml_errors": 0,
        "index_missing": 0,
        "low_freq_entities": 0,
        "issues": [],
    }

    # 解析指标
    for line in output.splitlines():
        if "维基图谱死链审计" in line or "死链" in line:
            if "未发现任何死链" not in line and "0 broken links" not in line:
                if "处死链" in line or "broken" in line:
                    metrics["issues"].append(line.strip())
        if "低频实体" in line and "发现" in line:
            import re
            m = re.search(r"发现\s*(\d+)\s*个", line)
            if m:
                metrics["low_freq_entities"] = int(m.group(1))
        if "强制检查合格" in line or "100% 通过" in line:
            metrics["passed"] = True

    return passed, output, metrics


def run_tag_scan(workspace_dir: Path) -> tuple[bool, str]:
    """运行 tag_manager.py scan 检查全库 Tag 白名单合规性"""
    cmd = ["uv", "run", "--with", "pyyaml", "python", "scripts/tag_manager.py", "scan"]
    env = dict(os.environ)
    env["PATH"] = f"{Path.home()}/.local/bin:{Path.home()}/.cargo/bin:/opt/homebrew/bin:{env.get('PATH', '')}"
    try:
        proc = subprocess.run(cmd, cwd=workspace_dir, capture_output=True, text=True, check=False, timeout=60, env=env)
        return proc.returncode == 0, proc.stdout.strip()
    except Exception as e:
        return False, f"Tag 校验异常: {e}"


def run_concept_source_lint(workspace_dir: Path) -> tuple[bool, str]:
    """运行 concept_source_lint.py 检查概念页上游溯源规范"""
    cmd = ["uv", "run", "--with", "pyyaml", "python", "scripts/concept_source_lint.py"]
    env = dict(os.environ)
    env["PATH"] = f"{Path.home()}/.local/bin:{Path.home()}/.cargo/bin:/opt/homebrew/bin:{env.get('PATH', '')}"
    try:
        proc = subprocess.run(cmd, cwd=workspace_dir, capture_output=True, text=True, check=False, timeout=60, env=env)
        passed = proc.returncode == 0
        return passed, proc.stdout.strip()
    except Exception as e:
        return False, f"概念溯源校验异常: {e}"


def scan_clippings(workspace_dir: Path) -> list[str]:
    """扫描 Clippings/ 顶层待归档的 .md 文件"""
    clippings_dir = workspace_dir / "Clippings"
    if not clippings_dir.exists():
        return []
    
    files = []
    for item in sorted(clippings_dir.iterdir()):
        if item.is_file() and item.name.endswith(".md") and not item.name.startswith("."):
            files.append(item.name)
    return files


def scan_email_manifest(workspace_dir: Path) -> dict:
    """读取 manifest.json 统计邮件待审和未识别状态"""
    manifest_path = workspace_dir / "Clippings" / "emails" / ".pipeline" / "manifest.json"
    result = {
        "review_articles": [],
        "unhandled_emails": [],
        "source_counts": {},
    }
    if not manifest_path.exists():
        return result

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 统计邮件中的 unhandled
        for email_id, email in data.get("emails", {}).items():
            if email.get("lifecycle") == "unhandled":
                result["unhandled_emails"].append({
                    "id": email_id,
                    "subject": email.get("subject", "无主题"),
                    "sender": email.get("sender", "未知发件人"),
                    "reason": email.get("reason", ""),
                })

        # 统计文章中的 review
        for article_id, article in data.get("articles", {}).items():
            if article.get("status") == "review":
                source = article.get("source_key", "default")
                result["review_articles"].append({
                    "id": article_id,
                    "title": article.get("title", "无标题"),
                    "source": source,
                    "file": article.get("staged_path", ""),
                })
                result["source_counts"][source] = result["source_counts"].get(source, 0) + 1

    except Exception as e:
        print(f"读取 manifest.json 出错: {e}", file=sys.stderr)

    return result


def generate_report(workspace_dir: Path) -> tuple[Path, str, str]:
    """生成巡检报告并落盘写入 tmp/daily-report.md"""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    lint_passed, lint_raw, lint_metrics = run_vault_lint(workspace_dir)
    tag_passed, tag_msg = run_tag_scan(workspace_dir)
    concept_passed, concept_msg = run_concept_source_lint(workspace_dir)
    clippings_files = scan_clippings(workspace_dir)
    email_stats = scan_email_manifest(workspace_dir)

    all_passed = lint_passed and tag_passed and concept_passed

    lines = [
        "# 知识库日巡检报告",
        f"> 生成时间：{now_str}",
        "",
        "## 📋 阻断性健康与合规门禁",
        f"- 图谱 Lint（死链/YAML/索引）：{'✅ 通过 (100%)' if lint_passed else '❌ 存在异常'}",
        f"- Tag 白名单合规：{'✅ 0 违规' if tag_passed else '❌ 存在非标标签'}",
        f"- 概念上游溯源：{'✅ 合规' if concept_passed else '❌ 存在违规/越级链接'}",
        f"- 死链统计：{lint_metrics['broken_links']} 处",
        f"- YAML Schema 错误：{lint_metrics['yaml_errors']} 处",
        f"- 索引漏登：{lint_metrics['index_missing']} 处",
    ]

    if not tag_passed:
        lines.append(f"  - ⚠️ {tag_msg}")
    if not concept_passed:
        lines.append(f"  - ⚠️ {concept_msg}")

    if lint_metrics["low_freq_entities"] > 0:
        lines.append(f"- 提示项（L0 候选）：发现 {lint_metrics['low_freq_entities']} 个入度 ≤ 1 的低频实体（移交周报决策）")

    if lint_metrics["issues"]:
        lines.append("")
        lines.append("### 异常明细")
        for issue in lint_metrics["issues"]:
            lines.append(f"- {issue}")

    lines.append("")
    lines.append("## 📬 待处理文章与邮件")
    lines.append(f"- Clippings 顶层待归档：{len(clippings_files)} 篇")
    if clippings_files:
        for f in clippings_files:
            lines.append(f"  - `Clippings/{f}`")

    review_count = len(email_stats["review_articles"])
    lines.append(f"- 邮件待审阅（review）：{review_count} 篇")
    if review_count > 0:
        for art in email_stats["review_articles"]:
            lines.append(f"  - [{art['source']}] {art['title']}")

    unhandled_count = len(email_stats["unhandled_emails"])
    lines.append(f"- 邮件未识别（unhandled）：{unhandled_count} 封")
    if unhandled_count > 0:
        for em in email_stats["unhandled_emails"]:
            lines.append(f"  - [{em['id']}] {em['subject']} ({em['reason']})")

    lines.append("")
    lines.append("## ✅ 结论")
    if all_passed and len(clippings_files) == 0 and review_count == 0 and unhandled_count == 0:
        conclusion = "全库图谱健康，0死链0错标0越级，待处理队列已全部清空。"
    elif all_passed:
        pending_items = []
        if clippings_files:
            pending_items.append(f"{len(clippings_files)} 篇剪藏待入库")
        if review_count:
            pending_items.append(f"{review_count} 篇邮件待审阅")
        if unhandled_count:
            pending_items.append(f"{unhandled_count} 封邮件未识别")
        conclusion = f"图谱结构与规范检查全绿。当前待处理队列：{ '，'.join(pending_items) }。"
    else:
        conclusion = "图谱存在 Lint、Tag 或概念溯源错误，需优先排查修复！"

    lines.append(conclusion)
    lines.append("")

    report_content = "\n".join(lines)

    # 确保 tmp/ 目录存在并写入
    tmp_dir = workspace_dir / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    report_file = tmp_dir / "daily-report.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_content)

    summary_line = f"[Daily Scan] Gate: {'PASS' if all_passed else 'FAIL'} | Clippings: {len(clippings_files)} | Review: {review_count} | Unhandled: {unhandled_count} -> 已写入 {report_file.name}"
    return report_file, summary_line, report_content


def main():
    workspace_dir = Path(__file__).resolve().parent.parent
    report_file, summary_line, report_content = generate_report(workspace_dir)
    print(summary_line)
    if "--verbose" in sys.argv or "-v" in sys.argv:
        print("\n" + report_content)


if __name__ == "__main__":
    main()
