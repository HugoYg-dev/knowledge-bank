---
type: source
tags:
- RAG/retrieval
- RAG/query
summary: 介绍 RAG 高阶查询翻译技巧，覆盖 Multi-Query、RAG Fusion、Sub-question 分解、Step-back Question
  和 HyDE 五种改写方法。
sources:
- raw/articles/RAG从入门到精通系列2：Query Translation（查询翻译）.md
updated: '2026-07-01'
---
# RAG查询翻译：Query Translation

> URL：https://mp.weixin.qq.com/s/8aUzRjpO5ve0C5ndhgI6ng
> Cubox 高亮：无（Cubox 摘要提及 Multi-query/RAG fusion/decomposition/step-back 四种方法）

## 摘要

介绍 RAG 高阶技巧 Query Translation（查询翻译），通过改写/优化/分解用户 Query 提升检索效果。覆盖 Re-written（Multi-Query、RAG Fusion）、Decomposition（Sub-question）、Step-back Question、HyDE 五种方法。

## 核心内容

### Re-written（改写）
- 对原始查询进行语义重写，保持核心意思不变
- **Multi-Query**：生成多个不同表述的查询，分别检索后去重合并
- **RAG Fusion**：生成多个相关问题，使用 Reciprocal Rank Fusion (RRF) 对检索结果排序过滤

### Decomposition（分解）
- 将复杂问题拆解为多个独立子问题（Sub-question）
- **流程一**（递归求解）：前一个子问题答案结合下一个子问题检索文档，逐步推进
- **流程二**（并行汇总）：分别获得每个子问题答案，最后集中汇总
- 适用于多跳问题、逻辑操作/条件限制问题

### Step-back Question
- 当问题太具体时，退一步问更广泛的问题获取更大上下文
- 提高检索召回率和上下文覆盖率
- 需提供 few-shot example 给 LLM

### HyDE（Hypothetical Document Embedding）
- 用 LLM 生成"假设文档"（假设答案）
- 将假设文档嵌入向量空间作为检索输入
- 检索到真实文档后结合原始问题生成最终答案

### Prompt 的威力
- 所有方法本质都借助 Prompt 能力
- 可先翻译中文问题为英文再检索英文资料库

## 关联

- 概念：[[概念_Query_Translation_查询改写与翻译]]、[[概念_RAG_Fusion_多查询融合生成]]、[[概念_HyDE_假设文档嵌入]]
- 实体：[[实体_LangChain]]
- 系列上一篇：[[RAG基础_索引检索生成]]
- 系列下一篇：[[RAG路由_Routing]]

---
> 📎 **物理文献**：[[raw/articles/RAG从入门到精通系列2：Query Translation（查询翻译）.md]]