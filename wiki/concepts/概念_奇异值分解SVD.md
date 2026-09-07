---
type: concept
tags:
- LLM/arch
- DeepLearning
summary: 奇异值分解（Singular Value Decomposition）适用于任意矩阵的分解方法：A = UΣV^T。是矩阵分解、降维、压缩、特征学习的基础工具。
sources:
- wiki/sources/2025-11-12_25-most-important-mathematical-definitions-in-DS_19a79c.md
updated: '2026-09-07'
---
# 概念：奇异值分解（SVD）


## 定义

奇异值分解（Singular Value Decomposition）适用于任意矩阵的分解方法：A = UΣV^T。是矩阵分解、降维、压缩、特征学习的基础工具。

## 要点

- 任意 m×n 矩阵 A = UΣV^T
  - U：m×m 方阵，列为左奇异向量
  - Σ：m×n，对角线为奇异值（由大到小排列），其余为 0
  - V^T：n×n，列为右奇异向量
- 求解方法：
  - A^T A 特征分解 → 右奇异向量 V
  - AA^T 特征分解 → 左奇异向量 U
  - 特征值矩阵 = 奇异值矩阵的平方，σ = √λ
- **奇异值衰减极快**：前 10%（甚至 1%）的奇异值之和常占全部 99% 以上
- 可用前 r 个大奇异值近似矩阵（r << m,n），在精度与时空开销间权衡
- 优于特征值分解：不要求方阵

## 应用

- **降维**：用前 r 个奇异值/奇异向量表示主要特征
- **压缩**：仅存储 U、Σ、V 三个较小矩阵
- 用 SVD 解 PCA、潜在语义索引（LSI/LSA）

## 来源