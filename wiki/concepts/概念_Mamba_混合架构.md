---
type: concept
tags:
- LLM/arch/MoE
- LLM/arch/Mamba
summary: Hybrid Transformer-Mamba 架构将 Transformer 的全局上下文理解能力与 Mamba/SSM 的长序列线性效率结合，取两者之长。
sources:
- wiki/sources/A_Visual_Guide_to_Mamba_and_SSM.md
- wiki/sources/Mamba2_SSD_大一统.md
- wiki/sources/腾讯混元TurboS技术报告.md
updated: '2026-09-21'
aliases:
- Hybrid Mamba
- Transformer-Mamba
- 混合Mamba架构
- 概念_混合Mamba架构
---

# 概念_Mamba_混合架构

Hybrid Transformer-Mamba 架构将 Transformer 的全局上下文理解能力与 Mamba/SSM 的长序列线性效率结合，取两者之长。

## 动机

- Transformer 自注意力复杂度 O(N²)，长序列开销大但上下文理解能力强
- Mamba（SSM）复杂度 O(N)，长序列高效但上下文理解相对弱
- 混合架构通过交错排列两种模块，实现效率与性能的平衡

## 混元 TurboS 的具体设计

- 总计 128 层，三种组件交错：Attention（5.5%）、Mamba2（44.5%）、FFN-MoE（50%）
- 核心模块模式：
  - **AMF 模块**：Attention → Mamba2 → FFN
  - **MF 模块**：Mamba2 → FFN
  - 两种模式交错排列
- FFN 层均为 MoE 结构（1 共享 + 32 专门专家，激活 1+2）

## 推理加速

与纯 Transformer MoE 对比，混合架构实现 **1.8x** 推理加速（AngelHCF 框架）：
- Mamba Kernel 优化：Prefill 阶段增强并行性，Decode 阶段 SelectiveScanUpdate Kernel 减轻显存带宽限制
- Mamba 状态使用 fp32 精度（而非 fp16/bf16），长文本生成质量与全 Attention 模型相当

## 相关来源

- [[腾讯混元TurboS技术报告]]
- [[A_Visual_Guide_to_Mamba_and_SSM]]
- [[Mamba2_SSD_大一统]]

## 关联概念

- [[概念_MambaBlock架构]] — Mamba Block 结构
- [[概念_SSM_状态空间模型]] — SSM 基础
- [[概念_MoE混合专家]] — FFN 替换为 MoE
- [[实体_腾讯混元TurboS]] — 应用模型