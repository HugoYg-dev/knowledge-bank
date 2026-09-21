---
type: entity
tags:
- RAG/retrieval
- AI-Agent/tool-calling
summary: 专注于大模型数据连接、索引构建与检索增强的应用开发框架。
sources:
- wiki/sources/RAG_12痛点与解决方案.md
- wiki/sources/RAG文本切分_JSON文档切分.md
- wiki/sources/RAG文本切分_token优化.md
- wiki/sources/RAG文本切分_字符切分.md
updated: '2026-07-01'
---

> [!note] 说明
> 注：全文仅作为 LangChain 对比方案简要演示，未深入介绍框架本身，故标 medium。

## 简介

LlamaIndex 是构建 LLM/RAG 应用的框架，与 LangChain 同类。在文本切分系列中用于演示文档加载与切分。

## 全文涉及能力

- **文档加载**：`SimpleDirectoryReader(input_files=[...]).load_data()` 加载本地文档
- **文本切分**：`SentenceSplitter(chunk_size, chunk_overlap)` 字符级切分
- **JSON 切分**：`JSONNodeParser()` 处理 JSON 结构数据
- **Node 体系**：切分结果为 nodes，包含文本信息及元数据

## 关联

- 相关概念：[[概念_文本切分五层级]]、[[概念_字符切分]]、[[概念_文档结构切分]]、[[概念_Rerank_重排序]]、[[概念_Prompt_Compression_提示词压缩]]、[[概念_检索后处理]]
- 来源：[[RAG文本切分_字符切分]]、[[RAG文本切分_token优化]]、[[RAG文本切分_JSON文档切分]]、[[RAG_12痛点与解决方案]]
