---
type: source
tags:
- MachineLearning
summary: 系统总结了 6 类主流聚类算法家族（质心、连通性、密度、图、分布、压缩），并探讨了其在不同形状和密度数据上的适用性。
sources:
- raw/articles/2026-06-01_Categorization-of-clustering-algorithms_19e84f.md
updated: '2026-08-04'
---

# Categorization of clustering algorithms

## 来源信息
- **来源**: Daily Dose of DS
- **原始链接**: [Gaussian Mixture Models (GMM)](https://www.dailydoseofds.com/gaussian-mixture-models-gmm/)
- **归档物理文件**: [[raw/articles/2026-06-01_Categorization-of-clustering-algorithms_19e84f.md]]

## 核心要点
1. **超越 KMeans 的聚类世界**：除了最常用的 KMeans 算法，数据科学家应该掌握各类针对不同数据分布设计的聚类方法。文章梳理并归纳了 6 种主流聚类家族。
2. **基于质心 (Centroid-based)**：根据点到质心的距离（如欧氏距离）进行聚类。核心代表为 KMeans，常需要配合 [[wiki/concepts/概念_Breathing_KMeans算法]] 克服初始敏感瓶颈。
3. **基于连通性 (Connectivity-based)**：根据聚类之间的临近程度来构建，例如层次凝聚聚类（Hierarchical Clustering）。
4. **基于密度 (Density-based)**：基于区域数据密度进行聚类。相比于质心算法，对不同形状（如环形、线形）和不同密度的聚类更为鲁棒。DBSCAN 是代表算法，但其运行时间长；而 **DBSCAN++** 提供了更快速且更具伸缩性的优化替代方案。
5. **基于图 (Graph-based)**：根据点在图结构中的图距离和拓扑相似性进行归簇，例如谱聚类（Spectral Clustering）。
6. **基于分布 (Distribution-based)**：基于点属于特定概率分布的 likelihood（似然度）进行划分。高斯混合模型（Gaussian Mixture Models, GMM）是典型代表，通过 NumPy 可以从零实现软聚类分配。
7. **基于压缩 (Compression-based)**：将高维数据转换/降维至较低维度的特征空间（例如使用 PCA、t-SNE、Autoencoder 等），在此基础上执行高效聚类。

## 关键引文
- "There’s a whole world of clustering algorithms beyond KMeans, which a data scientist must be familiar with."
- "Density-based: Cluster points based on their density. It is more robust to clusters with varying densities and shapes than centroid-based clustering."

---
关联概念：
- [[wiki/concepts/概念_聚类算法分类综述]]
- [[wiki/concepts/概念_Breathing_KMeans算法]]

> 📎 **物理文献**：[[raw/articles/2026-06-01_Categorization-of-clustering-algorithms_19e84f.md]]
