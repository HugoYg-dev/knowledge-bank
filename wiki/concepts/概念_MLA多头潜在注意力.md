---
type: concept
tags:
- LLM/arch
summary: MLA（Multi-Head Latent Attention，多头潜在注意力）是 DeepSeek-V2 首次引入的注意力变体，用于减少 KV
  Cache 内存占用，同时保持或提升建模性能。
sources:
- wiki/sources/2025年七大顶流大模型架构.md
- wiki/sources/从DeepSeek-V3到Kimi_K2_八种现代LLM架构大比较.md
- wiki/sources/2026-09-03_Attention-Mechanisms-in-LLMs,-clearly-explained_1a068e0f112668fe.md
updated: '2026-09-15'
---


# 概念_MLA多头潜在注意力

MLA（Multi-Head Latent Attention，多头潜在注意力）是 DeepSeek-V2 首次引入的注意力变体，用于减少 KV Cache 内存占用，同时保持或提升建模性能。

## 核心思想

与 [[概念_GQA分组查询注意力|GQA]] 通过共享 K/V 头减少显存不同，MLA 将全维度的 K 和 V 张量投影压缩到低秩潜在空间（Low-Rank Latent Space），缓存该潜在向量而非全维 KV 张量：

- **缓存对象**：仅缓存低维潜在向量，使 KV Cache 占用降低至 MHA 的 **5%–13%**（甚至低于常见 GQA 配置）；
- **动态解压**：推理自回归解码计算注意力时，通过矩阵乘法将潜在向量动态投影升维回原始尺寸；
- **带宽换算力**：虽然解压增加了额外的矩阵乘法 FLOPs，但在 LLM 推理场景中，内存带宽（Memory Bandwidth）远比计算能力更易成为瓶颈，因此极小的显存占用换取了显著更高的并发吞吐量与生成速度；
- 训练时 Q 也压缩，推理时 Q 不压缩。

## 与其他注意力方案对比

| 方案 | KV Cache 大小 | 建模性能 | 复杂度与计算代价 |
|------|--------------|----------|--------|
| MHA | 最大 (100%) | 基准 | 显存爆炸，无额外解压计算 |
| [[概念_GQA分组查询注意力]] (GQA) | 中等（如 25%） | 略低于或接近 MHA | 无额外投影计算，组内共享 |
| MLA | 极小（约 5%–13%） | 匹敌甚至优于 MHA | 解码时增加低秩投影解压 FLOPs |

来源：DeepSeek-V2 消融研究。

## 应用模型

- DeepSeek-V2、DeepSeek-V3、DeepSeek-R1
- Kimi K2（基于 DeepSeek-V3 架构扩展）

## 相关来源

- [[从DeepSeek-V3到Kimi_K2_八种现代LLM架构大比较]]
- [[2025年七大顶流大模型架构]]
- [[wiki/sources/2026-09-03_Attention-Mechanisms-in-LLMs,-clearly-explained_1a068e0f112668fe.md]]

## 关联概念与实体

- [[概念_自注意力复杂度]] — 注意力机制的基础复杂度分析
- [[概念_KV_Cache]] — KV Cache 原理
- [[概念_GQA分组查询注意力]] — 分组查询注意力
- [[概念_MoE混合专家]] — DeepSeek-V3 另一核心组件
- [[实体_DeepSeek-V3]] — MLA 应用模型
- [[实体_DeepSeek-R1]] — MLA 应用模型