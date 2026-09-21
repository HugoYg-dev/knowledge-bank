---
type: concept
tags:
- Skill/data-analysis
- Infra/gpu
summary: t-SNE 是一种流形学习降维与二维可视化算法。其 CPU 计算具有 O(N²) 二次方复杂度瓶颈，大样本下极其缓慢。tSNE-CUDA 可提供高达
  700 倍的 GPU 极速提升，但目前硬件上仅支持生成二维投影（n_components=2）。
sources:
- wiki/sources/2025-07-01_Accelerate-tSNE-with-GPU_197c7a.md
- wiki/sources/2025-10-18_Avoid-Using-PCA-for-Visualization-Unless..._199f91.md
- wiki/sources/2025-11-12_25-most-important-mathematical-definitions-in-DS_19a79c.md
updated: '2026-09-21'
aliases:
- t-SNE
- tSNE
- t分布随机邻域嵌入
- 概念_t-SNE算法
---

# 概念_t_SNE_降维算法

## 定义
t-SNE（t-Distributed Stochastic Neighbor Embedding，t-分布邻域嵌入）是一种非线性流形降维算法，主要用于高维数据的探索性分析、降维与低维（特别是二维）空间的可视化。

## 瓶颈与挑战
- **二次方时间复杂度**：标准 t-SNE 算法的计算复杂度与数据样本量 $N$ 的平方呈二次方关系（即 $O(N^2)$）。
- **样本量限制**：在标准的 CPU 实现（如 Scikit-Learn）中，当数据样本点超过 4 万（40k+）时，其运行时间会急剧增加，变得难以实用。

## GPU 加速与限制
- **tSNE-CUDA 极速提升**：tSNE-CUDA 是针对 GPU 优化并基于 CUDA 实现的 t-SNE 算法。在 CIFAR-10 数据集（50,000 张图像）的基准测试中，tSNE-CUDA 实现了相比标准 Sklearn (CPU) 达 **700 倍** 的加速。
- **维度限制**：目前 tSNE-CUDA 仅支持 `n_components=2`，即只能将高维数据投影至二维空间。由于若要支持更高维度需要对底层架构与核心代码进行大幅度重构，开发团队目前无意支持更多维度。
- **实用性折中**：虽然存在仅支持 2D 投影的限制，但在 99% 的实际应用场景中，使用 t-SNE 的核心目的就是为了生成二维可视化投影，因此该限制并不会影响其在绝大多数数据科学任务中的实用价值。

## 关联
- [[wiki/sources/2025-07-01_Accelerate-tSNE-with-GPU_197c7a]]（来源）