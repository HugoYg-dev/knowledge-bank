---
type: concept
tags:
- AI-Agent/skill
- AI-Agent/coding
summary: LLM Wiki 范式中的核心入库操作 SOP，包含阅读原文、提炼要点、生成 Source 摘要、更新/新建 Entities & Concepts、检查矛盾与同步索引日志等标准动作。
sources:
- wiki/sources/Karpathy推文引发的LLM_Wiki知识库搭建实践.md
- wiki/sources/Claude Code与Obsidian飞书知识库搭建实践.md
- wiki/sources/Vault死链治理与单向推导架构维护复盘.md
updated: '2026-07-22'
---

# 概念：Ingest入库闭环

## 定义

**Ingest（摄入/入库闭环）** 是 [[concepts/概念_LLM_Wiki范式|LLM Wiki 范式]] 与知识库系统中最核心的操作流程。与传统 RAG 在查询时才检索零散片段不同，Ingest 强调在信息进入知识库的第一时间，由 LLM 完成全篇阅读、语法净化、提炼结构化摘要并深度编织维基图谱网络。

## Ingest 标准六步闭环 SOP

1. **阅读与净化**：深度阅读 Raw/Clippings 原文，完成行内伪 Tag（如 `#xxx`）与伪链接（如非 Obsidian 链接的 `\[\[`）转义。
2. **移动与归档 (Clippings -> raw)**：将剪藏暂存区的 Markdown 文件归档移动至 `raw/articles/` 等物理路径，保持零级底座不可变。
3. **生成 Source 摘要页**：在 `wiki/sources/` 创建结构化摘要，规范 Frontmatter 指向 `raw/articles/xxx.md`，正文总结核心要点，文末挂载物理文献插链 `> 📎 **物理文献**：` + `raw/articles/xxx.md`。
4. **联动 Entities & Concepts**：检查引用的 `wiki/entities/` 与 `wiki/concepts/` 页面：若存在则补充新要点并更新 `sources:` 指向 `wiki/sources/xxx.md`；若不存在且重要则新建对应页面。
5. **全量挂载索引 `wiki/index.md`**：在 `wiki/index.md` 对应分类区登记挂载本次新建的所有 Sources、Entities 与 Concepts 页面。
6. **记录日志 `wiki/log.md`**：追加流水记录 `## [YYYY-MM-DD] ingest | raw/articles/xxx -> wiki/sources/xxx.md (+ affected pages)`。

## 关联

- 相关概念：[[concepts/概念_LLM_Wiki范式]]、[[concepts/概念_单向推导数据管线]]、[[concepts/概念_假性死链鉴别]]
- 实体：[[entities/实体_Claude_Code]]、[[entities/实体_Obsidian]]、[[entities/实体_vault_lint]]
- 来源：[[Karpathy推文引发的LLM_Wiki知识库搭建实践]]、[[Claude Code与Obsidian飞书知识库搭建实践]]、[[raw/out-blogs/知识库治理（一）Vault 死链治理与单向推导防线]]
