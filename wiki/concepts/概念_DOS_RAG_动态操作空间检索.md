---
type: concept
tags:
- RAG/retrieval
summary: DOS RAG（Document's Original Structure RAG，保留文档原始结构的 RAG）是斯坦福 2025 论文提出的强基线方法。其与传统
  RAG 的唯一区别在于排序步骤：放弃按相关性得分排序，改为将检索到的片段按其在原始文档中出现的先后顺序重新排列后输入 LLM。
sources:
- wiki/sources/斯坦福RAG新基线_DOS_RAG.md
updated: '2026-09-21'
aliases:
- DOS-RAG
- DOS RAG
- 动态操作空间
- 概念_DOS_RAG
---

# 概念_DOS_RAG_动态操作空间检索


## 定义

DOS RAG（Document's Original Structure RAG，保留文档原始结构的 RAG）是斯坦福 2025 论文提出的强基线方法。其与传统 RAG 的唯一区别在于排序步骤：放弃按相关性得分排序，改为将检索到的片段按其在原始文档中出现的先后顺序重新排列后输入 LLM。

## 流程

1. **检索**：与传统 RAG 相同，向量检索找出最相关的文本片段（Chunks）
2. **排序**：放弃相关性得分排序，按片段在原文出现的先后顺序重排（**唯一关键区别**）
3. **生成**：按原文顺序排列的片段连同问题输入 LLM

## 成功原因

1. **保留叙事流与逻辑链**：维持上下文连贯性，减轻 LLM 理解负担
2. **信息保真度最大化**：直接从原文提取，避免摘要/重组的信息损失
3. **检索与阅读最佳平衡**：检索过滤无关信息，原始顺序让 LLM 在自然语境推理

## 实验结论

- 在 ∞Bench、NarrativeQA、QuALITY 等长文档 QA 基准上，几乎所有 Token 预算和场景下持平甚至超越 ReadAgent、RAPTOR
- RAPTOR 在这些任务中甚至不及朴素 RAG

## 意义

- 作为 RAG 项目最强基准（KISS 原则）
- 实现简单、计算开销小、延迟低

## 关联

- 相关概念：[[概念_RAPTOR_递归树状检索索引]]、[[概念_RAG基础流程]]、[[概念_检索后处理]]
- 来源：[[斯坦福RAG新基线_DOS_RAG]]