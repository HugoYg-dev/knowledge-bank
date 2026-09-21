---
type: concept
tags:
- LLM/arch/MoE
summary: MoE（Mixture of Experts，混合专家模型）是一种高效 Scaling 技术，用较少的计算量实现更大模型规模，从而获得更好性能。
sources:
- wiki/sources/2025年七大顶流大模型架构.md
- wiki/sources/从DeepSeek-V3到Kimi_K2_八种现代LLM架构大比较.md
- wiki/sources/手把手教你实现稀疏MoE语言模型.md
- wiki/sources/腾讯混元TurboS技术报告.md
updated: '2026-09-07'
---


# 概念_MoE混合专家

MoE（Mixture of Experts，混合专家模型）是一种高效 Scaling 技术，用较少的计算量实现更大模型规模，从而获得更好性能。

## 核心结构

MoE 由两个关键部分组成：

1. **稀疏 MoE 层**：替换传统 Transformer 中的 FFN（前馈网络）层。包含若干"专家"（每个专家本身是一个 FFN 子网络）。
2. **门控网络/Router**：由可学习参数（Linear + Softmax）组成，与网络其余部分一同预训练，决定每个 Token 被发送到哪个/哪些专家。

## 工作机制

- Router 将 Token 的 hidden 表示投影到 Expert 数量的维度，取 top-k 分数对应的专家进行处理
- 多个专家处理同一 Token 时，各专家输出按门控权重加权求和
- 关键：每次只激活 top-k 个专家，其余专家不参与计算，保持"稀疏性"

## 优势

- 相同计算预算下，可显著扩大模型总参数（容量），吸收更多知识
- 预训练效率高于同等参数稠密模型
- 推理时只激活少数专家，FLOPs 远低于总参数量

## 挑战

- 所有专家参数必须加载进 VRAM，内存需求大（Mixtral 8x7B 实际需要 47B 参数 VRAM）
- 分布式部署存在专家并行通信带宽瓶颈
- 微调易过拟合，负载均衡需要专门设计

## 现代 LLM 应用实例

| 模型 | 总参数 | 激活参数 | 专家数 | 每次激活 |
|------|--------|----------|--------|----------|
| DeepSeek-V3 | 671B | 37B | 256 | 9（1共享+8路由） |
| Kimi K2 | 1T | — | 更多 | — |
| Llama 4 Maverick | 400B | 17B | 较少 | 2 |
| Qwen3 235B | 235B | 22B | — | — |
| 混元 TurboS | 560B | 56B | 33（1+32） | 3（1+2） |

## 相关来源

- [[手把手教你实现稀疏MoE语言模型]]
- [[从DeepSeek-V3到Kimi_K2_八种现代LLM架构大比较]]
- [[腾讯混元TurboS技术报告]]

## 关联概念

- [[概念_MoE_Router_专家路由门控网络]] — 门控/路由机制细节
- [[概念_MoE负载均衡]] — 负载均衡策略
- [[概念_Transformer架构]] — MoE 所替换的 FFN 所在架构