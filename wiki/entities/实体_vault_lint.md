---
type: entity
tags:
- AI-Agent/skill
summary: 知识库自动化治理与静态图谱诊断 Python 工具（`scripts/vault_lint.py`），支持语法污染扫描、死链审计与级联清理。
sources:
- wiki/sources/Vault死链治理与单向推导架构维护复盘.md
updated: '2026-07-22'
---

# 实体：vault_lint

## 简介

**vault_lint** 是为本知识库定制的自动化治理与诊断 Python 工具（物理脚本存放在 `scripts/vault_lint.py`）。

## 核心功能与能力

1. **图谱与死链审计 (`lint`)**：扫描全库 Markdown 文件的 YAML 解析合法性、未匹配死链与孤立无入链页面。
2. **语法净化 (`sanitize-raw`)**：检测并自动转义物理源文件中未转义的行内伪 Tag 或矩阵/张量伪出链。
3. **级联清理 (`prune <raw_path>`)**：实现自上而下四步级联清理 SOP，并具备**行内安全感知（Inline Safety Sensing）**，防止盲目整行销毁误伤合法双链。

## 来源与参考

- [[raw/out-blogs/知识库治理（一）Vault 死链治理与单向推导防线]]
- [[concepts/概念_级联清理安全边界]]
