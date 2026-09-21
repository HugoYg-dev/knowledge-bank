---
type: concept
tags:
- LLM/arch/Mamba
summary: State Space Duality，Mamba2 的核心理论框架，证明了 SSM 与线性 Attention 在数学上的等价性。
sources:
- wiki/sources/Mamba2_SSD_大一统.md
updated: '2026-09-21'
aliases:
- SSD
- State Space Duality
- 状态空间对偶
- 概念_状态空间对偶SSD
---

# 状态空间对偶 SSD

State Space Duality，Mamba2 的核心理论框架，证明了 SSM 与线性 Attention 在数学上的等价性。

## 核心命题

当 SSM 的矩阵 A_t 为标量时，SSM 序列变换矩阵 M 可以写成：

```
M = L ∘ CB^T
```

其中 L 是下三角掩码矩阵，∘ 表示逐元素乘。

对应 Attention：
```
Y = (L ∘ QK^T) V
```

因此 **(C, B, X) ↔ (Q, K, V)**，SSM 与因果线性 Attention 完全等价。

## 半可分离矩阵

SSM 的变换矩阵 M 是一类特殊矩阵——**半可分离矩阵（semiseparable matrix）**：
- 下三角矩阵
- 下三角部分的每个子矩阵都是低秩的
- M_ij = C_i^T · A_{i:j}^× · B_j

## SSD 统一框架

SSD 框架将 SSM 和 Attention 纳入同一理论体系：
- Linear Attention、RetNet 都是 SSD 的特殊形式
- 因果 mask 是 1-SS 矩阵（a_t=1 的特殊情况）

## SSD 算法

基于分块矩阵分解，利用对角块（类 Attention）+ 低秩块（矩阵乘）+ 扫描块（SSM scan）的分解：
- 不同块间可并行计算
- 中心扫描块复杂度比纯 SSM 低 Q 倍（Q 为块大小）
- 总 FLOP O(TN²)，内存 O(TN)

数值稳定性：用 segsum（log 域累加）替代直接累乘，避免梯度爆炸/nan。

## 来源

- [[Mamba2_SSD_大一统]]
- [[实体_Mamba2]]