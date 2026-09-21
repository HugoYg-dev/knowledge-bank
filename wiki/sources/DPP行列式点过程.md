---
type: source
tags:
- DeepLearning
summary: 介绍行列式点过程（DPP）在推荐系统中实现高质量且多样化子集采样的原理与贪婪算法实现。
sources:
- raw/articles/Determinantal Point Process：机器学习中行列式的妙用.md
updated: '2026-07-01'
---
# DPP 行列式点过程

> URL：https://mp.weixin.qq.com/s/fRFiyW9peyCO2yLzTzV0BQ

## 核心问题

从集合中采样子集，使子集同时具备高质量和多样性。典型应用：推荐系统中推荐结果去重与多样化。

## 主要内容

### 边缘分布与核矩阵

- DPP 边缘分布定义：采样子集"包括" A 的概率 = det(K_A)，K 为核矩阵
- K_ij 越大，i 和 j 同时出现的概率越小（核函数表达相似性）
- K 必须是半正定矩阵，特征值在 [0,1] 之间

### L-Ensemble

- 概率正比于 det(L_Y)，L 矩阵核函数为内积
- 归一化常数：det(L + I)
- L 与 K 的对应关系：K = L(L+I)^{-1}

### 多样性的直观解释

- 相似性 = 向量点积（余弦值）；多样性 = 正交性
- 子集多样性 = 构成的超平行体体积
- 行列式可表示体积：det(B^T B) = Vol²
- 从 L-Ensemble 角度看：被采样概率正比于超平行体体积，两两线性无关更易被采样

### 贪婪算法（Chen et al., 2018）

- k-DPP 问题（选 k 个使 det 最大）是 NP-Hard
- 暴力求解复杂度 O(N·k⁴)
- [[概念_DPP_Cholesky分解加速]] 利用 Cholesky 分解降至 O(N·k²)
- 核心思想：增量更新，每步选择使 d_i² 最大的元素
- d_i² 可通过上一轮的 c 向量增量更新

### Sliding Window

- 当 k 较大时相似样本开始出现
- 滑动窗口仅保证窗口内多样性
- 窗口大小建议为召回数目的 2 倍左右
- 多召回一个 window 大小再去重

### Demo 实验

- 使用 BERT 编码句子，DPP 采样比最大内积召回结果语义更多样
- BQ Corpus 实验：50 个召回样本中 DPP 选 10 个，无重复且语义多样

## 相关概念

- [[概念_DPP_Cholesky分解加速]]
- 行列式与多样性采样

## 相关实体

- （无独立实体需创建）

---
> 📎 **物理文献**：[[raw/articles/Determinantal Point Process：机器学习中行列式的妙用.md]]