---
type: entity
tags:
- LLM/arch/attention
summary: DeepSeek V2/V3 提出的低秩 KV 压缩注意力机制，通过矩阵吸收技术使注意力计算时 K/V 不含头信息，兼具 MQA 显存效率和 MHA
  表达能力
sources:
- wiki/sources/DeepSeek_MLA矩阵吸收原理.md
- wiki/sources/MiniMax_vs_Kimi_注意力路线之争.md
- wiki/sources/从DeepSeek-V3到Kimi_K2_八种现代LLM架构大比较.md
updated: '2026-06-29'
---

# 实体：DeepSeek V2（MLA 首发）

## 基本信息

- **机构**：DeepSeek
- **关键创新**：MLA（Multi-head Latent Attention）
- **后续**：DeepSeek V3、Kimi Linear（MLA 作为混合架构组件）

## MLA 核心贡献

- 低秩压缩 KV，KV Cache 仅存 `compressed_kv`（低维潜在向量）
- 矩阵吸收：K/V 升维矩阵吸收进 Q，注意力计算退化为广播，减少内存访问
- 128 个头时优化收益极大

## 影响

- Kimi Linear 将 MLA 作为混合架构中的全注意力组件（3:1 比例中的 1）
- 行业内 MLA 已成为高效注意力的重要参考方案

## 参见

- [[概念_MLA_多头潜在注意力]]
- [[DeepSeek_MLA矩阵吸收原理]]
- [[实体_Kimi_Linear]]
- [[从DeepSeek-V3到Kimi_K2_八种现代LLM架构大比较]]