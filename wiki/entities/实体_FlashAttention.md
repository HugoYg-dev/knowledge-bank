---
type: entity
tags:
- DeepLearning
- LLM/arch/attention
summary: FlashAttention 是 Tri Dao 等提出的精确、I/O 感知注意力实现，已成长上下文 LLM 训练/推理的行业标准；迭代至 FA-3
  利用 Hopper 新指令与 FP8。
sources:
- wiki/sources/2025年七大顶流大模型架构.md
- wiki/sources/A_Visual_Guide_to_Mamba_and_SSM.md
- wiki/sources/Attention复杂度解析与改进方向.md
- wiki/sources/Transformer被挑战_Mamba解析与PyTorch复现.md
- wiki/sources/一文读懂Mamba_知乎.md
- wiki/sources/从DeepSeek-V3到Kimi_K2_八种现代LLM架构大比较.md
- wiki/sources/大模型显存计算公式与优化.md
updated: '2026-06-26'
---
# 实体：FlashAttention

## 简介

FlashAttention 由 Tri Dao 等人于 2022 年提出，是一种 I/O 感知的精确注意力算法/CUDA 实现。已成为长上下文 LLM 训练和推理的行业标准，推动上下文长度从 2-4K 提升到数十万乃至百万级。

## 版本要点

- **FA-1（2022）**：验证 I/O 感知设计潜力；但对新硬件利用不足
- **FA-2**：深度工程优化，A100 FP16 约 70% 峰值，H100 540-570 TFLOPs，比初代快近一倍
- **FA-3（2024）**：利用 Hopper 的 WGMMA、TMA、FP8 指令；异步重叠 + 低精度，H100 FP16 740 TFLOPs（75% 峰值），FP8 接近 1.2 PFLOPs，误差比直接 FP8 量化降 2.6 倍

## 同类/替代方案（全文简介）

- Hyena：长卷积，亚二次复杂度
- 线性注意力（Performer 等）：随机特征线性化 Softmax，O(N)
- S2-Attention：硬件感知稀疏 + 上下文分片

## 关联

- [[Attention复杂度解析与改进方向]]（来源）
- [[概念_FlashAttention_快速注意力]]