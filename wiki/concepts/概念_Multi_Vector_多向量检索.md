---
type: concept
tags:
- RAG/retrieval
- RAG/embedding
summary: Multi-Vector Retrieval（多向量检索）是用一种"代理表示"对原始内容进行索引、而非直接嵌入原始内容本身的检索模式，常用于处理低资源文件和长文件。基于
  David Wheeler 的思想——"几乎所有复杂问题都可以通过增加一层迂回（indirection）来解决"。
sources:
- wiki/sources/RAG系统设计_语义搜索与KG驱动选型.md
updated: '2026-09-21'
aliases:
- Multi-Vector
- Multi Vector
- 多向量检索
- 概念_Multi-Vector检索
---

# 概念_Multi_Vector_多向量检索


## 定义

Multi-Vector Retrieval（多向量检索）是用一种"代理表示"对原始内容进行索引、而非直接嵌入原始内容本身的检索模式，常用于处理低资源文件和长文件。基于 David Wheeler 的思想——"几乎所有复杂问题都可以通过增加一层迂回（indirection）来解决"。

## 应用场景

- **低资源数据索引**：embedding 模型训练时自然语言数据远多于代码，因此用自然语言（代码注释、README）索引 Rust 代码，查询时对比自然语言索引
- **超长文件索引**：用文本总结对长文本进行索引并向量化，无需切分成小块
- **多模态检索**：图像/表格/文本分别生成标签，通过自然语言统一检索；也可结合 Multi-embedding（原图嵌入 + 总结嵌入）

## 关联

- 相关概念：[[概念_Semantic_Search本质]]、[[概念_Multi_Representation_Indexing_多表征索引]]、[[概念_ColBERT_多向量延迟交互检索]]、[[概念_父页面检索]]
- 来源：[[RAG系统设计_语义搜索与KG驱动选型]]