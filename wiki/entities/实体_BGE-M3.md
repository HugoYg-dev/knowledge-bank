---
type: entity
tags:
- RAG/embedding
summary: 智源推出的多语言混合嵌入模型，支持稠密检索与 ColBERT 多向量细粒度表示。
sources:
- wiki/sources/ColBERTv2残差压缩演进.md
- wiki/sources/ColBERT原理与延迟交互机制.md
- wiki/sources/Jina_AI创业复盘.md
- wiki/sources/RAGAS评估RAG系统.md
- wiki/sources/RAG文本切分_token优化.md
- wiki/sources/TableRAG_文本表格异构问答.md
updated: '2026-07-01'
---

## 简介

BGE-M3 是 BAAI（北京智源）推出的多语言嵌入模型，支持多种语言的文本检索。输出 1024 维向量，同时支持 dense embedding 和 ColBERT 多向量表示（colbert_vecs）。

## 技术特点

- 同时支持密集向量和 ColBERT 多向量输出
- 维度：1024
- 支持 FP16 加速
- 可通过 `FlagEmbedding` 库的 `BGEM3FlagModel` 调用
- `encode(sentences, return_colbert_vecs=True)` 同时返回 dense_vecs 和 colbert_vecs
- 内置 `colbert_score` 方法计算归一化后的 ColBERT 相似度

## 在 ColBERTv2 残差压缩中的应用

- 文中实验使用 BGE-M3 生成 ColBERT 向量后应用残差压缩
- 636KB 原始向量 → 159.16KB 压缩（约 4x 压缩比）
- MSE ≈ 0，相似度得分相对差异 <0.02%

## 关联

- 相关概念：[[概念_ColBERT_多向量延迟交互检索]]、[[概念_ColBERTv2残差压缩]]、[[概念_Dense_Embedding_稠密向量嵌入]]
- 来源：[[ColBERT原理与延迟交互机制]]、[[ColBERTv2残差压缩演进]]
