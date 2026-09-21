---
type: concept
tags:
- LLM/arch/Mamba
summary: State Space Model，用于对序列数据建模的数学框架，源自控制理论（Kalman 1960）。
sources:
- wiki/sources/A_Visual_Guide_to_Mamba_and_SSM.md
- wiki/sources/Mamba2_SSD_大一统.md
- wiki/sources/Mamba_Explained_Kola_Ayonrinde.md
- wiki/sources/Transformer被挑战_Mamba解析与PyTorch复现.md
- wiki/sources/一文读懂Mamba_知乎.md
updated: '2026-09-21'
aliases:
- SSM
- State Space Model
- 状态空间模型
- 概念_状态空间模型SSM
---

# 状态空间模型 SSM

State Space Model，用于对序列数据建模的数学框架，源自控制理论（Kalman 1960）。

## 核心方程

SSM 用两个方程描述系统：

**状态方程**（连续）：
```
h'(t) = A·h(t) + B·x(t)
```

**输出方程**（连续）：
```
y(t) = C·h(t) + D·x(t)
```

其中：
- x(t)：输入序列
- h(t)：隐状态（对历史的压缩表示）
- y(t)：预测输出
- A：状态转移矩阵（如何从上一状态演化到新状态）
- B：输入影响矩阵（输入如何影响状态）
- C：输出矩阵（状态如何映射到输出）
- D：跳跃连接（输入直接影响输出，可视为 skip connection）

## 本质

SSM 本质是 RNN 与 CNN 的结合：
- 循环表示（recurrent）→ 高效推理，O(1) 内存
- 卷积表示（convolutional）→ 并行训练

## 三种等价表示

见 [[概念_SSM三种表示]]

## 离散化

连续方程需要离散化才能处理文本等离散序列，见 [[概念_SSM离散化]]

## 局限：线性时不变（LTI）

传统 SSM 的 A/B/C 对所有时间步固定，导致无内容感知能力，见 [[概念_LTI_线性时不变]]

## 来源

- [[A_Visual_Guide_to_Mamba_and_SSM]] — 视觉化全流程讲解
- [[Mamba_Explained_Kola_Ayonrinde]] — 控制论直觉类比
- [[一文读懂Mamba_知乎]] — 中文论文解析
- [[Transformer被挑战_Mamba解析与PyTorch复现]] — PyTorch 实现对照