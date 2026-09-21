---
type: concept
tags:
- RAG/retrieval
- RAG/embedding
summary: 基于聚类空间划分的高维向量近似最近邻搜索（ANNS）索引算法，通过质心分组建立倒排映射，大幅缩小检索计算量。
aliases:
- IVF
- Inverted File Index
- 倒排文件索引
- 倒排索引
- 概念_倒排文件索引_IVF
- 概念_IVF倒排索引
sources:
- wiki/sources/2025-10-27_ANN-search-using-inverted-file-index_19a274.md
- wiki/sources/2026程序员必读的向量数据库原理与选型指南.md
updated: '2026-09-21'
---

# 概念_IVF_倒排索引 (Inverted File Index)

## 定义与核心机制

**倒排文件索引（Inverted File Index, IVF）**是一种高维向量的近似最近邻搜索（ANNS）索引技术。其核心思想源于传统信息检索中的“倒排索引”（将文档映射到词项），在向量空间中，它通过聚类算法（通常是 K-Means）将向量数据集划分到不同的空间胞腔（Voronoi Partitions/Cells）中，并建立“质心 $\\to$ 胞腔内向量列表”的倒排映射。

在检索时，只需计算查询向量与各个胞腔质心的距离，找出最邻近的质心，然后仅在这些胞腔的倒排列表中进行细粒度距离计算，从而避免全库暴力扫描。

## 索引构建与两阶段检索

1. **聚类空间划分（Partitioning）**：使用 K-Means 将全量 $N$ 个 $D$ 维向量聚类为 $K$ 个簇（Partitions），产生 $K$ 个中心点向量（Centroids）。
2. **倒排列表挂载（Inverted Lists）**：每个数据向量按最近距离归属于某一个质心，挂载在该质心的倒排列表中。
3. **两阶段检索流程**：
   - **粗粒度过滤（Coarse Filtering）**：计算查询向量与 $K$ 个质心的距离，选出最近的 $n_{\\text{probe}}$ 个质心。时间复杂度为 $O(KD)$。
   - **细粒度精搜（Fine Search）**：仅在这 $n_{\\text{probe}}$ 个胞腔的并集倒排列表中计算详细距离。在均布假设下时间复杂度为 $O(\\frac{n_{\\text{probe}} \\cdot ND}{K})$。

相比暴力 kNN 的 $O(ND)$ 复杂度，IVF 检索复杂度为 $O(KD + \\frac{n_{\\text{probe}}ND}{K})$。例如在 $N=10\\text{M}, K=100, n_{\\text{probe}}=1$ 时，计算量由 10,000,000 降至约 100,100，实现接近 **100 倍**的检索加速。

## 精度与延迟折中 (Accuracy-Latency Trade-off)

- **边界向量遗漏**：若查询向量落在胞腔边界，真实最近邻可能分布在相邻胞腔，仅探查最近单个胞腔会导致漏检。
- **探查参数 $n_{\\text{probe}}$**：增大 $n_{\\text{probe}}$ 会探查更多相邻胞腔，显著提升召回率（Recall），但会线性增加距离计算耗时。
- **内存与工程选型**：IVF 内存占用远低于 [[entities/实体_HNSW|HNSW]]，且非常适合结合 PQ（乘积量化，形成 IVF-PQ）在超大规模数据集上运行。代表实现包括 [[entities/实体_Faiss|Faiss]]、[[entities/实体_Milvus|Milvus]] 与 [[entities/实体_pgvector|pgvector]]。

## 关联

- 相关概念：[[concepts/概念_向量数据库]]、[[concepts/概念_近似最近邻搜索]]、[[concepts/概念_向量索引方法]]、[[concepts/概念_向量量化]]
- 实体：[[entities/实体_Faiss]]、[[entities/实体_Milvus]]、[[entities/实体_pgvector|pgvector]]
- 物理文献：[[2025-10-27_ANN-search-using-inverted-file-index_19a274]]、[[2026程序员必读的向量数据库原理与选型指南]]
