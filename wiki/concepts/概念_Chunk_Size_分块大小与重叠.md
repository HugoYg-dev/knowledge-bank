---
type: concept
tags:
- RAG/retrieval
- RAG/chunking
summary: 文本切分中的两个基础参数：
sources:
- wiki/sources/ES企业AI搜索实践.md
- wiki/sources/RAG挑战赛冠军方案.md
- wiki/sources/RAG文本切分_字符切分.md
- wiki/sources/RAG文本切分_递归字符切分.md
updated: '2026-09-21'
aliases:
- Chunk Size
- Chunk Overlap
- 分块大小与重叠
- 概念_Chunk_Size与Overlap
---

# 概念_Chunk_Size_分块大小与重叠


## 定义

文本切分中的两个基础参数：

- **Chunk Size（块大小）**：每个切分片段中包含的字符（或 token）数量
- **Chunk Overlap（块重叠）**：为避免重要信息被切开，连续块之间重叠的字符（或 token）数

## 要点

- chunk_size 过小会导致切分过于零碎，丢失上下文
- chunk_size 过大可能超过模型输入限制或引入不相关信息
- overlap 确保跨块边界的语义连续性，避免关键信息被截断
- 实际工程中需根据语言、模型、任务场景调优

## 关联

- 相关概念：[[概念_字符切分]]、[[概念_递归字符切分]]、[[概念_Token切分优化]]
- 来源：[[RAG文本切分_字符切分]]、[[RAG文本切分_递归字符切分]]