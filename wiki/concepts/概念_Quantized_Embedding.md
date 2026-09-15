---
type: concept
tags:
- RAG/retrieval
- RAG/embedding
summary: Quantized Embedding（压缩版稠密向量）通过量化把高精度浮点向量压缩为低位宽整数，降低存储和内存占用。
sources:
- wiki/sources/ES企业AI搜索实践.md
- wiki/sources/从BM25到Multi-Vector_6种Embedding演进路线.md
- wiki/sources/向量数据库原理与应用全解析.md
- wiki/sources/2026-09-04_5-embedding-compression-techniques_1a06e32ac6088201.md
updated: '2026-09-15'
---

# 概念_Quantized_Embedding


## 定义

Quantized Embedding（量化嵌入，主要指标量量化 Scalar Quantization, SQ）通过将高精度浮点向量线性映射为低位宽整数（如 Int8），降低内存驻留开销并加速向量距离计算。

## 特点与工程收益

- **压缩手段**：Float32 → Int8 / UInt8；
- **容量对比**：带来约 **4×** 的物理体积缩减：
  - 例如 1,000 万个（10M）1536 维向量，Float32 需 **62 GB**，而 Int8 标量量化后仅需 **15 GB**；
- **元数据开销**：每个向量仅需额外附加少量的尺度因子（scale）和偏移量（offset）元数据；
- **效果**：内存×4↓，磁盘×4↓，向量检索 QPS×2↑，召回率下降极低（通常 <1%）；
- **适合场景**：一次性加载进内存的工业级 ANN 向量引擎（如 Milvus、Qdrant、Faiss-IVF、Elasticsearch）。

## 与正交技术的组合范式

- **与 MRL 串联**：可先利用 [[concepts/概念_MRL套娃表示学习|MRL]] 将高维嵌入在推理期截断（如 1536 维截断至 256 维），再对前缀向量进行 Int8 标量量化，同时在“维度数量”与“单维比特数”两个维度实现复合压缩。

## 关联

- 相关概念：[[概念_Dense_Embedding]]、[[概念_Binary_Embedding]]、[[concepts/概念_MRL套娃表示学习|概念_MRL套娃表示学习]]、[[概念_向量量化]]
- 来源：[[从BM25到Multi-Vector_6种Embedding演进路线]]、[[ES企业AI搜索实践]]、[[向量数据库原理与应用全解析]]、[[wiki/sources/2026-09-04_5-embedding-compression-techniques_1a06e32ac6088201.md]]