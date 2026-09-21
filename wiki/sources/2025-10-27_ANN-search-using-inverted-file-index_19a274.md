---
type: source
tags:
- RAG/retrieval
summary: 介绍了在向量检索中使用倒排文件索引 (IVF) 进行近似最近邻 (ANN) 搜索的原理。相比暴力搜索 kNN 的 O(ND) 复杂度，IVF 通过
  k-means 聚类建立质心到分区的映射，将搜索复杂度降低到 O(KD + ND/K)，大幅度缩减耗时（N=10M，K=100 时可实现近 100 倍加速），同时客观阐述了其以精度折中换取低延迟的机制。
sources:
- raw/articles/2025-10-27_ANN-search-using-inverted-file-index_19a274.md
updated: 2026-08-03
---

# ANN search using inverted file index

## 来源信息
- **主题**: ANN search using inverted file index
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Mon, 27 Oct 2025
- **原始物理文件**: [[raw/articles/2025-10-27_ANN-search-using-inverted-file-index_19a274.md]]

## 核心要点
- **kNN 检索瓶颈**：随着数据规模的增大，传统的 kNN 暴力搜索需要对全部 $N$ 个高维向量进行距离计算，效率极低，时间复杂度为 $O(ND)$。
- **近似最近邻 (ANN) 检索**：为了提高检索效率，ANN 算法通过建立索引（Indexing）来缩小搜索空间。
- **倒排文件索引 (IVF) 的核心思想**：
  1. 使用 k-means 聚类算法将原始的 $N$ 个向量划分到 $K$ 个胞腔（Partitions）中。
  2. 计算每个胞腔的中心点（Centroid），每个数据向量只与其最近的质心关联。
  3. 构建映射（Map），存储每个质心所对应的所有向量点。
- **两阶段检索过程**：
  1. 比较查询向量与 $K$ 个质心，寻找距离最近的质心，复杂度为 $O(KD)$。
  2. 在该质心对应的胞腔/分区的向量中，进行最近邻搜索，复杂度为 $O(ND/K)$（假设每个分区 size 均匀）。
  3. 整体检索复杂度从 $O(ND)$ 降低至 $O(KD + ND/K)$。
- **性能与精度折中**：
  - 在 $N=10\text{M}$、$K=100$ 的情况下，kNN 复杂度比例为 10M，而 IVF 为 $100 + 100\text{k} = 100,100$，可实现接近 100 倍的加速。
  - 但作为近似检索，若有些数据向量事实上距离查询向量很近但被划分到了其他相邻胞腔，就会被检索遗漏，存在一定的精度损耗。

## 关联概念
- 核心概念：[[wiki/concepts/概念_IVF_倒排索引]]
- 关联概念：[[wiki/concepts/概念_向量索引方法]]、[[wiki/concepts/概念_近似最近邻搜索]]

## 关键引文
> "kNN performs an exhaustive search, which is inefficient at scale!"
> "Approximate nearest neighbor search algorithms solve this. The core idea is to narrow down the search space using indexing techniques, which improves the run-time performance."
> "In IVF, however, there are two steps: 1. Match to all centroids -> O(KD). 2. Find the nearest neighbor in the nearest partition -> O(ND/K)."
> "That said, ANN is not always accurate. If some data points are actually close to the query data point but not in the same partition, they may still get missed... We willingly accept such trade-offs to reduce latency."

> 📎 **物理文献**：[[raw/articles/2025-10-27_ANN-search-using-inverted-file-index_19a274.md]]
