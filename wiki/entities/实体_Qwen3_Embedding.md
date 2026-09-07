---
type: entity
tags:
- RAG/embedding
summary: 阿里基于 Qwen3 训练的 SOTA 嵌入（Embedding）与重排模型系列。
sources:
- wiki/sources/Jina_AI创业复盘.md
- wiki/sources/为什么用Qwen3_embedding和rerank.md
updated: '2026-07-01'
---

## 简介

Qwen3 Embedding 与 Qwen3 Reranker 是基于 Qwen3 大语言模型训练的嵌入/重排模型系列。在 MTEB 排行榜上开源闭源均排名第一（Rerank 同样领先，4B 除 8B 外也基本第一）。提供 0.6B、4B、8B 等多种规模，支持 32K 长上下文。

## 与传统 BERT 派（如 BGE）的区别

- BGE 等基于 BERT（encoder only）训练，用 [CLS] 池化
- Qwen3 是 causal LLM（单向），用 [EOS] 标记池化——语义压缩到最后一个 special token
- [EOS] 的 hidden state 等价于 BERT 的 [CLS]

## 效果好的原因

1. 模型够大，维度大隐空间表征丰富
2. 基础模型太强（核心），Qwen3 语义理解远超 BERT
3. 训练方法：前两阶段对比学习 + 第三阶段 Slerp；约 1.5 亿对弱监督文本对（Qwen32 合成）；FT 阶段约 700 万人工标注 + 1200 万合成数据

## 核心能力

- **Instruct 机制**：编码查询时附带任务指令，支持多维度检索（详见 [[概念_Instruct_Embedding]]）
- **Reranker LLM 化**：用 system prompt 生成 yes/no，`score = P("yes")/(P("yes")+P("no"))`（详见 [[概念_重排序Rerank]]）
- 代码检索为强项

## 关联

- 相关概念：[[概念_Instruct_Embedding]]、[[概念_重排序Rerank]]、[[概念_Embedding与向量检索]]
- 实体：[[实体_Sentence_Transformers]]
- 来源：[[为什么用Qwen3_embedding和rerank]]
