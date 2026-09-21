---
type: concept
tags:
- RAG/retrieval
summary: 相关段落提取（Relevant Segment Extraction, RSE）是一种 RAG 检索后优化策略。不同于传统方法仅检索孤立文本块，RSE
  识别并重建连续的文本片段，为 LLM 提供更完整、有逻辑性的上下文信息。
sources:
- wiki/sources/RAG技巧与底层代码剖析.md
updated: '2026-07-06'
---

# 概念_RSE相关段落提取


## 定义

相关段落提取（Relevant Segment Extraction, RSE）是一种 RAG 检索后优化策略。不同于传统方法仅检索孤立文本块，RSE 识别并重建连续的文本片段，为 LLM 提供更完整、有逻辑性的上下文信息。

## 核心理念

- 与用户问题相关的文本块往往集中出现在文档的同一区域或连续段落中
- 将这些相关文本块按顺序组织成连贯的整体段落，显著提升 LLM 理解能力

## 算法流程

1. **初步检索**：语义搜索找出相关文本块
2. **计算块价值**：chunk_value = 相关性得分 - irrelevant_chunk_penalty（不相关块得负值）
3. **寻找最佳段落**：遍历可能的起止位置，找累加 value 最高的连续段落
4. **约束条件**：max_segment_length（单段最大长度）、total_max_length（总长度上限）、min_segment_value（段落最低价值阈值）
5. **段落重建**：将最佳段落的 chunks 拼接还原为连续文本
6. **格式化输入 LLM**：SEGMENT 1 (Chunks x-y): ...

## 与传统 RAG 的对比

| | 传统 RAG | RSE |
|---|---|---|
| 检索结果 | 多个不相连的文本块 | 连续段落 |
| 上下文 | 缺少过渡和背景 | 保留原文结构 |
| LLM 理解 | 可能断章取义 | 完整语义 |

## 关联

- 相关概念：[[概念_上下文增强检索]]、[[概念_检索后处理]]、[[概念_DOS_RAG_动态操作空间检索]]、[[概念_父页面检索]]
- 来源：[[RAG技巧与底层代码剖析]]