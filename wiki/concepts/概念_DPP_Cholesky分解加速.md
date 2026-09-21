---
type: concept
tags:
- LLM/arch
- DeepLearning
summary: Cholesky 分解用于加速 DPP（行列式点过程）的贪婪 MAP 推断。对称半正定矩阵 L 可分解为 L = CC^T（C 为下三角矩阵），利用增量更新避免每步重新计算行列式。
sources:
- wiki/sources/DPP行列式点过程.md
updated: '2026-09-21'
aliases:
- DPP
- Determinantal Point Process
- Cholesky分解与DPP
- 概念_Cholesky分解与DPP
---

# 概念：Cholesky 分解与 DPP


## 定义

Cholesky 分解用于加速 DPP（行列式点过程）的贪婪 MAP 推断。对称半正定矩阵 L 可分解为 L = CC^T（C 为下三角矩阵），利用增量更新避免每步重新计算行列式。

## 要点

- L 矩阵（核函数为内积）是对称半正定的，因此存在 Cholesky 分解
- 选中集合 Y 的 L_Y 的 Cholesky 分解为 C·C^T，C 为 |Y|×|Y| 下三角矩阵
- 归一化后（向量模为 1），det(L_Y) = d_1² · d_2² · ... · d_k²（d_i 为 Cholesky 对角元素）
- 贪婪策略：每步选择使 d_i² 最大的元素
- 增量更新：新元素加入后，通过已有 c 向量计算新一行的 c 和 d，无需重新分解
- 复杂度从暴力 O(N·k⁴) 降至 O(N·k²)

## 来源

- [[DPP行列式点过程]]（Chen et al., 2018 贪婪算法）