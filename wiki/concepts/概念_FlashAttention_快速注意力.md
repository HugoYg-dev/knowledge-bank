---
type: concept
tags:
- DeepLearning
- LLM/arch/attention
summary: FlashAttention 是 I/O 感知的精确注意力优化，通过 Kernel 融合、分块计算（Tiling）和在线 Softmax 避免在
  HBM 物化 N×N 中间矩阵，将注意力从内存密集型转为计算密集型。
sources:
- wiki/sources/2025年七大顶流大模型架构.md
- wiki/sources/A_Visual_Guide_to_Mamba_and_SSM.md
- wiki/sources/Attention复杂度解析与改进方向.md
- wiki/sources/Transformer大模型3D可视化_NanoGPT.md
- wiki/sources/Transformer被挑战_Mamba解析与PyTorch复现.md
- wiki/sources/一文读懂Mamba_知乎.md
- wiki/sources/从DeepSeek-V3到Kimi_K2_八种现代LLM架构大比较.md
- wiki/sources/大模型显存计算公式与优化.md
- wiki/sources/推测解码Speculative_Decoding综述.md
- wiki/sources/2025-11-28_Two-techniques-to-extend-the-context-length-of-LLMs_19acc3.md
- wiki/sources/2026-09-03_Attention-Mechanisms-in-LLMs,-clearly-explained_1a068e0f112668fe.md
updated: '2026-09-21'
aliases:
- FlashAttention
- Flash Attention
- 快速注意力
- 快速精确注意力
- 概念_FlashAttention
---

# 概念_FlashAttention_快速注意力

## 定义

FlashAttention（Tri Dao 等，2022）是一种 I/O 感知（I/O-aware）的精确注意力计算内核优化方法，核心是通过算法重组与硬件协同设计最大限度减少全局显存（HBM）访问，且不做任何数学近似、完全保持计算精度。需要明确的是，**FlashAttention 不是一种新的注意力架构类型，而是底层高效执行任何注意力机制（MHA、GQA、MLA 等）的标准执行内核（Standard Kernel）**。

## 硬件瓶颈背景 (SRAM 与 HBM)

在现代 GPU 架构中，内存层级（Memory Hierarchy）是决定计算效率的关键因素：
- **SRAM (Static Random-Access Memory)**：片上高速缓存，容量极其稀少，但速度极快。
- **HBM (High Bandwidth Memory)**：全局显存，容量非常充沛，但访问速度相对较慢（通常比 SRAM 慢 8-15x）。

传统的自注意力（Self-Attention）计算在计算 $QK^T$ 和 Softmax 时，需要频繁地在 SRAM 与 HBM 之间进行大矩阵（$N \times N$）的写回与读取（物化操作）。这种频繁的内存 I/O 搬运在长序列（大 $N$）情况下会彻底拖累 GPU 计算核心，引发极严重的物理读写限制，导致计算单元长期处于闲置等待状态。因此，内存 I/O 搬运而非计算本身成为了扩展 Transformer 上下文的最大瓶颈。

## 三大技术要点

1. **核融合（Kernel Fusion）与避免显存物化**：所有前/后向操作融合到一个 CUDA Kernel，在片上 SRAM 完成，只把 N×d 输出写回 HBM，不显式生成 N×N 中间矩阵
2. **分块计算（Tiling）**：Q/K/V 按序列长度分块，外层循环加载 K/V 块、内层加载 Q 块到 SRAM，逐对块算矩阵乘+Softmax 并累加，避免完整 N×N 矩阵
3. **在线 Softmax（Online Softmax）**：维护当前行最大值与归一化累积值，处理每个块时实时更新归一化因子，无需访问完整得分行

## 演进

- **FA-1**：空间复杂度降至线性，加速 2-4 倍
- **FA-2**：优化线程块布局/工作划分，A100 FP16 达约 70% 峰值，H100 540-570 TFLOPs
- **FA-3**：异步重叠（乒乓调度 GEMM/Softmax）+ FP8 低精度（非相干处理抑制异常值），H100 FP16 达 740 TFLOPs（75% 峰值），FP8 接近 1.2 PFLOPs

## 关联

- [[Attention复杂度解析与改进方向]]（来源）
- [[wiki/sources/2026-09-03_Attention-Mechanisms-in-LLMs,-clearly-explained_1a068e0f112668fe.md]]（来源）
- [[概念_自注意力复杂度]]
- [[concepts/概念_GQA_分组查询注意力]]
- [[concepts/概念_MLA_多头潜在注意力]]
- [[实体_FlashAttention]]