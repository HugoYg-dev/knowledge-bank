---
type: concept
tags:
- RAG/retrieval
summary: Prompt 压缩（Prompt Compression）是在检索后、送入 LLM 前对上下文进行压缩的技术，解决长上下文场景下信息过载、噪声过多的问题（对应
  RAG 痛点 4：未提取）。
sources:
- wiki/sources/RAG_12痛点与解决方案.md
updated: '2026-09-21'
aliases:
- Prompt Compression
- 提示词压缩
- 上下文压缩
- 概念_Prompt_Compression
---

# 概念_Prompt_Compression_提示词压缩


## 定义

Prompt 压缩（Prompt Compression）是在检索后、送入 LLM 前对上下文进行压缩的技术，解决长上下文场景下信息过载、噪声过多的问题（对应 RAG 痛点 4：未提取）。

## 代表方法：LongLLMLingua

- 来自 LongLLMLingua 研究项目/论文
- 集成于 LlamaIndex，作为 node postprocessor 在检索步骤后压缩上下文
- 通过 `LongLLMLinguaPostprocessor` 设置目标 token 数、排序方法等参数
- 可启用文档重排序（reorder_context）

## 关联

- 相关概念：[[概念_检索后处理]]、[[概念_Long_Text_Reorder_长文本位置重排序]]、[[概念_Contextual_Compression_上下文压缩]]
- 来源：[[RAG_12痛点与解决方案]]

> 注：本页 confidence 为 medium，全文仅在 RAG 痛点 4 处提及 LongLLMLingua，未展开压缩算法原理。