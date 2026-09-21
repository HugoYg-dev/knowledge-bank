---
type: concept
tags:
- LLM/arch/Mamba
summary: Selective State Space，Mamba 的核心创新，通过让 SSM 参数依赖输入实现内容感知推理。
sources:
- wiki/sources/A_Visual_Guide_to_Mamba_and_SSM.md
- wiki/sources/Mamba2_SSD_大一统.md
- wiki/sources/Mamba_Explained_Kola_Ayonrinde.md
- wiki/sources/Transformer被挑战_Mamba解析与PyTorch复现.md
- wiki/sources/一文读懂Mamba_知乎.md
updated: '2026-06-29'
---


# Mamba 选择机制

Selective State Space，Mamba 的核心创新，通过让 SSM 参数依赖输入实现内容感知推理。

## 动机

传统 SSM（S4）是线性时不变的——A/B/C 固定，无法区分不同输入内容，见 [[概念_LTI_线性时不变]]。Mamba 要在保持 SSM 效率的同时获得 Transformer 的内容感知能力。

## 做法

将 B、C 和步长 Δ 变为输入的函数（input-dependent）：

```
S4（固定）：  A ∈ R(N,N),  B ∈ R(N,1),   C ∈ R(1,N)
Mamba（动态）：A ∈ R(N,N),  B ∈ R(T,N,1), C ∈ R(T,1,N), Δ ∈ R(T,D)
```

- T：序列长度，B：batch size，D：input 维度，N：hidden state 维度
- 每个 token 有自己独立的 B、C 矩阵和步长
- A 保持静态（希望状态演化规律不变，但输入影响状态的方式动态调整）

## Δ 的作用

- 大 Δ → 更多关注当前 token，忽略历史上下文（聚焦）
- 小 Δ → 跳过当前 token，依赖历史上下文（忽略）

## 效果

解决了两类任务：
1. 选择性复制（Selective Copying）：选择性地复制特定 token
2. 归纳头（Induction Heads）：识别和重复序列中的模式

## 代价

选择机制使 B/C 动态变化，无法使用固定 kernel 的卷积形式进行并行训练，需要改用 parallel scan，见 [[概念_Mamba硬件感知算法]]。

## 来源

- [[A_Visual_Guide_to_Mamba_and_SSM]]
- [[Mamba_Explained_Kola_Ayonrinde]]
- [[Mamba2_SSD_大一统]]
- [[一文读懂Mamba_知乎]]
- [[Transformer被挑战_Mamba解析与PyTorch复现]]