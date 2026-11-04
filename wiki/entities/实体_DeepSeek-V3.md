---
type: entity
tags:
- LLM/arch/MoE
summary: DeepSeek 发布的旗舰密集 MoE 模型，架构创新（MLA + MoE）影响了后续多个顶级模型设计。
sources:
- wiki/sources/2025年七大顶流大模型架构.md
- wiki/sources/DeepSeek-R1工作原理.md
- wiki/sources/RAGAS评估RAG系统.md
- wiki/sources/从DeepSeek-V3到Kimi_K2_八种现代LLM架构大比较.md
- wiki/sources/刚刚，DeepSeek Harness震撼开源：一切皆插件.md
- wiki/sources/近6年的大模型架构，我挨个试了个遍.md
updated: '2026-11-04'
---
# 实体_DeepSeek-V3

DeepSeek 发布的旗舰密集 MoE 模型，架构创新（MLA + MoE）影响了后续多个顶级模型设计。

## 基本信息

- **机构**：DeepSeek AI
- **发布时间**：2024 年 12 月
- **继承模型**：DeepSeek-R1（推理模型，基于 V3 构建）

## 规格

- 总参数：671B；激活参数：37B
- MoE 专家：256 个，每次激活 9 个（1 共享 + 8 路由选择）

## 架构特点

- **MLA（多头潜在注意力）**：KV 压缩进低维潜在空间，KV Cache 显著减小，建模性能优于 MHA
- **MoE**：每个 Transformer 层均为 MoE；共享专家对所有 Token 始终激活
- 每个 Transformer 层均使用 MoE（不交替使用密集层）

## 影响

- Kimi K2（1T 参数）、Llama 4（MoE）均参考 DeepSeek-V3 架构
- **开源架构红利集大成者（1000+ 消融实验验证）**：Nikita Pavlichenko 在 6 年架构消融研究中指出，现代开源大模型架构红利在 2024 年底 DeepSeek-V3（MLA + 细粒度 MoE）时代已基本释放完毕；后续架构层面的微调在大模型上的收益已逼近边际极限（在 Scaling Law 误差拆解中架构优化空间仅余约 2%），进一步的性能突破更多取决于优化器（如 Muon）与数据工程。

## 相关文件

- [[从DeepSeek-V3到Kimi_K2_八种现代LLM架构大比较]]
- [[2025年七大顶流大模型架构]]
- [[近6年的大模型架构，我挨个试了个遍]]
- [[概念_MLA_多头潜在注意力]]
- [[概念_MoE混合专家]]