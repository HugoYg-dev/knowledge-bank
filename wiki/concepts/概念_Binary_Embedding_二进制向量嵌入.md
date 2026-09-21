---
type: concept
tags:
- RAG/retrieval
- RAG/embedding
summary: Binary Embedding（极致 0/1 压缩）将浮点向量二值化为 0/1 表示，实现极致存储压缩与超快计算。
sources:
- wiki/sources/从BM25到Multi-Vector_6种Embedding演进路线.md
- wiki/sources/2026-09-04_5-embedding-compression-techniques_1a06e32ac6088201.md
updated: '2026-09-21'
aliases:
- Binary Embedding
- 二值向量
- 二进制嵌入
- 概念_Binary_Embedding
---

# 概念_Binary_Embedding_二进制向量嵌入


## 定义

Binary Embedding（二值量化嵌入，BQ）将连续浮点向量二值化为 0/1（或 $\pm 1$）比特表示，实现极致存储压缩与超高速硬件级位运算。

## 特点与显存对比

- **编码方式**：对 Float 向量执行符号阈值化 `sign()`（大于 0 为 1，小于 0 为 0）或 ITQ 旋转二值化；
- **存储开销**：单维仅占 1 个 bit，比 Float32 节省 **32×**：
  - 以 1,000 万个（10M）1536 维向量为例，Float32 占用 **62 GB**，而 Packed Bits 二值化后仅占 **2 GB**；
- **计算加速**：浮点内积退化为 CPU/GPU 原生 SIMD 指令——按位异或（XOR）与汉明权重（popcount），单核可执行每秒数亿次距离计算；
- **核心局限**：汉明距离丢失了向量的连续幅度（magnitude）信息，仅保留大致角度结构，直接排序精度平均下降 5%–15%。

## 工业级破局：两阶段检索范式 (Over-fetch + Rescoring)

为了消除 BQ 丢失幅度信息的缺陷，现代 RAG 与向量搜索引擎普遍采用两阶段架构：
1. **第一阶段（粗排 Over-fetch）**：基于 2GB 的 BQ 紧凑索引，利用极速位运算超额召回候选集合（例如请求 Top 10 时，粗排超额拉取 Top 100）；
2. **第二阶段（精排 Rescoring）**：从磁盘或低成本介质中读取这 100 个候选文档的完整 Float32 向量，重新计算精确余弦相似度并最终排序截取 Top 10；
3. **收益**：既将常驻内存降低 32 倍、大幅提升检索 QPS，又利用精排重排消除了 BQ 的精度损失（注：粗排未召回的漏检项无法被挽回）。

## 关联

- 相关概念：[[概念_Quantized_Embedding_量化向量嵌入]]、[[concepts/概念_MRL套娃表示学习|概念_MRL套娃表示学习]]、[[概念_PCA_主成分分析|概念_主成分分析_PCA]]、[[概念_Dense_Embedding_稠密向量嵌入]]、[[概念_向量量化]]
- 来源：[[从BM25到Multi-Vector_6种Embedding演进路线]]、[[wiki/sources/2026-09-04_5-embedding-compression-techniques_1a06e32ac6088201.md]]