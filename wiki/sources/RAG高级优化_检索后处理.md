---
type: source
tags:
- RAG/retrieval
summary: 介绍四种检索后处理优化手段（Long-text Reorder、Contextual Compression、Refine、Emotion Prompt），帮助大模型更好地理解上下文知识。
sources:
- raw/articles/RAG高级优化：检索后处理模块成竹在胸.md
updated: '2026-07-01'
url: https://mp.weixin.qq.com/s?__biz=Mzk0NTcyNTMzNw==&mid=2247484209&idx=1&sn=0ce7bb6bbb6a0ff5efb4ad10ce2765a7
---
# RAG高级优化：检索后处理模块

## 摘要

介绍在将召回片段送入大模型之前的四种优化手段：Long-text Reorder、Contextual Compression、Refine、Emotion Prompt。帮助大模型更好地理解上下文知识，给出最佳回答。

## 核心内容

### Long-text Reorder（长文本重排序）

- 依据论文 "Lost in the Middle: How Language Models Use Long Contexts"
- 实验表明：大模型更容易记忆开头和结尾文档，对中间部分记忆能力不强
- 方案：按相关性重排序，将更相关的文档放在开头和结尾，不太相关的放中间
- 实现：反转文档列表，奇数索引追加到末尾，偶数索引插入开头（LangChain `_litm_reordering`）

### Contextual Compression（上下文压缩）

- 本质：利用 LLM 判断检索文档与用户 query 的相关性
- 只返回相关度最高的 k 个文档片段
- LangChain 实现：`ContextualCompressionRetriever` + `LLMChainExtractor`
- 基于 base_retriever 召回后用 LLM compressor 过滤压缩

### Refine（答案精炼）

- 对大模型生成的回答进行进一步改写，保证准确性
- 主要涉及提示词工程
- 流程：给出原始查询 + 已有答案 + 新上下文，要求模型 refine 答案
- 若新上下文无用，返回原始答案

### Emotion Prompt（情绪提示）

- 来源：微软论文 "Large Language Models Understand and Can Be Enhanced by Emotional Stimuli"
- 在提示词中增加情绪情感相关提示，有助于大模型输出高质量回答
- 示例 stimuli：
  - "Write your answer and give me a confidence score between 0-1"
  - "This is very important to my career."
  - "You'd better be sure."
- 可组合多个 stimuli 叠加使用

## 关联

- 概念：[[概念_检索后处理]]、[[概念_Long_Text_Reorder_长文本位置重排序]]、[[概念_Contextual_Compression_上下文压缩]]
- 实体：[[实体_LangChain]]
- 同系列：[[RAG高级优化_query转换之路]]、[[RAG高级优化_检索策略Fusion_HyDE]]、[[RAG高级优化_问题生成检索增强]]

---
> 📎 **物理文献**：[[raw/articles/RAG高级优化：检索后处理模块成竹在胸.md]]