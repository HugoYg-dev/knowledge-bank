---
type: entity
tags:
- LLM/arch/MoE
summary: 月之暗面（Moonshot AI）发布的万亿参数开源权重 MoE 模型，基于 DeepSeek-V3 架构扩展，以 Muon 优化器为主要创新。
sources:
- wiki/sources/2025年七大顶流大模型架构.md
- wiki/sources/Manus创始人手把手拆解上下文工程.md
- wiki/sources/RL环境与智能体能力金字塔.md
- wiki/sources/从DeepSeek-V3到Kimi_K2_八种现代LLM架构大比较.md
updated: '2026-06-29'
---
# 实体_Kimi_K2

月之暗面（Moonshot AI）发布的万亿参数开源权重 MoE 模型，基于 DeepSeek-V3 架构扩展，以 Muon 优化器为主要创新。

## 基本信息

- **机构**：月之暗面（Moonshot AI）
- **发布时间**：2025 年（DeepSeek R2 发布前先行开源）

## 规格

- 总参数：1 万亿（1T）
- 基于 DeepSeek-V3 架构，MoE 专家更多，MLA 头更少

## 创新点

- **Muon 优化器**：首次在生产级大模型（1T 参数）中使用 Muon 取代 AdamW，训练 Loss 曲线极平滑
- 比 DeepSeek-V3 更多专家，MLA 中更少注意力头

## 性能

- 截至撰写时（2025 年）最令人印象深刻的开源权重模型之一
- 基准测试成绩可与 Gemini、Claude、ChatGPT 顶级模型相媲美

## 相关文件

- [[从DeepSeek-V3到Kimi_K2_八种现代LLM架构大比较]]
- [[2025年七大顶流大模型架构]]
- [[概念_Muon优化器]]
- [[概念_MLA_多头潜在注意力]]
- [[实体_DeepSeek-V3]]