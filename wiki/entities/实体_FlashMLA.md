---
type: "entity"
tags:
  - "Infra/serving"
  - "LLM/inference"
summary: "DeepSeek 开源的专针对 Hopper 架构 GPU 的高性能 MLA 解码加速计算内核库"
sources:
  - "wiki/sources/DeepSeek开源FlashMLA从原理到代码详解.md"
updated: "2026-10-26"
---

# 实体：FlashMLA

## 简介
**FlashMLA** 是 DeepSeek 于 2025 年 2 月开源的高性能 MLA（Multi-Head Latent Attention）解码算子内核库，专为大语言模型生产环境的高并发、超长上下文自回归推理设计。

## 核心特征与技术实现
1. **硬件与平台约束**：
   - 底层基于 NVIDIA CUTLASS 模板库实现；
   - 专为 Hopper 架构 GPU（SM90，如 NVIDIA H100、H800）定制；
   - 强制采用 BF16 数值精度，充分释放 Tensor Core 算力。
2. **核心 API 体系**：
   - `get_mla_metadata`：预计算 tile scheduler 元数据与切分数量，协调多 SM 并行；
   - `flash_mla_with_kvcache`：配合 Paged KV Cache（Block Table）执行高效的 MLA 解码注意力计算。
3. **系统定位**：
   - 解决了 DeepSeek-V2 / V3 / R1 等采用 MLA 架构模型在底层算子执行层面缺乏原生产业级 Kernel 的瓶颈，与 FlashAttention、vLLM 等推理生态紧密协同。

## 关联
- [[concepts/概念_MLA_多头潜在注意力|概念_MLA_多头潜在注意力]]
- [[entities/实体_DeepSeek|实体_DeepSeek]]
- [[entities/实体_DeepSeek-V3|实体_DeepSeek-V3]]
- [[sources/DeepSeek开源FlashMLA从原理到代码详解|来源：DeepSeek开源FlashMLA从原理到代码详解]]
