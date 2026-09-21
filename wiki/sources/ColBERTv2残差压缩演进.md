---
type: source
tags:
- RAG/embedding
- RAG/retrieval
summary: 从 ColBERT 到 ColBERTv2 的演进——早期交互/延迟交互对比、表示模型与交互模型，及 ColBERTv2 的残差压缩（residual
  compression）、知识蒸馏与 BGE-M3 压缩实验
sources:
- raw/articles/RAG之延迟交互与残差压缩：从ColBERT到ColBERTv2的演进及其应用.md
updated: '2026-07-01'
---
# ColBERTv2残差压缩演进

## 早期交互 vs 延迟交互

- **早期交互（Early Interaction）**：在编码阶段就融合查询与文档，精度高，但每次查询复杂度 O(n·m)，且无法预先存储文档表示。
- **延迟交互（Late Interaction）**：先独立编码，再做轻量级匹配。

## 表示模型 vs 交互模型

| 类型 | 代表 | 编码方式 | 查询复杂度 | 可否预计算 | 精度 |
|------|------|----------|-----------|-----------|------|
| 表示模型（Representation） | [[概念_Sentence_BERT_孪生网络句向量|Sentence-BERT]] | 独立编码为固定向量 | O(1) | 可预计算 | 较低 |
| 交互模型（Interaction） | BERT Cross-Encoder | 拼接查询+文档，深度交互 | O(n·m) | 不可预存 | 最高 |

## ColBERT（Stanford）

- 基于 BERT，独立多向量编码，采用 MaxSim 延迟交互。
- 文档可预先索引到 FAISS 中（见 [[实体_Faiss]]）。
- 精度接近 cross-encoder，延迟从秒级降至数十毫秒。

详见 [[ColBERT原理与延迟交互机制]] 与 [[概念_ColBERT_多向量延迟交互检索]]。

## ColBERTv2（SIGIR 2021）

解决存储问题。多向量存储开销大：

> 1000 token × 128 维 × 4 字节 = 每文档 0.5MB

改进点：

- **残差压缩（residual compression）**：存储减少 6–10 倍，性能损失 1–2%。
- **知识蒸馏（knowledge distillation）**。
- **改进的损失函数**。

### 残差压缩步骤

1. 对所有 token 向量做 K-means 聚类，找到质心（centroid）。
2. 计算残差 residual = 向量 − 最近质心。
3. 将残差量化（quantize）为 uint8（8-bit）。
4. 存储：质心索引（2 字节）+ 量化残差（128 字节）= 130 字节，对比原始 512 字节。

完整说明见 [[概念_ColBERTv2残差压缩]]。

### BGE-M3 压缩实验

使用 [[实体_BGE-M3]]，8 篇文档：

| 指标 | 数值 |
|------|------|
| 原始大小 | 636KB |
| 压缩后 | 159.16KB |
| 压缩比 | 约 4× |
| MSE | 约 0 |
| 相似度得分相对差异 | < 0.02% |

## 论文与代码

- 论文：https://arxiv.org/abs/2112.01488
- 代码：https://github.com/stanford-futuredata/ColBERT

## 关联

- 相关概念：[[概念_ColBERT_多向量延迟交互检索]]、[[概念_ColBERTv2残差压缩]]、[[概念_向量量化]]、[[概念_Sentence_BERT_孪生网络句向量]]
- 实体：[[实体_ColBERT]]、[[实体_BGE-M3]]、[[实体_Faiss]]
- 来源：[[ColBERT原理与延迟交互机制]]

---
> 📎 **物理文献**：[[raw/articles/RAG之延迟交互与残差压缩：从ColBERT到ColBERTv2的演进及其应用.md]]