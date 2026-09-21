---
type: concept
tags:
- LLM/arch/attention
- LLM/inference
summary: GQA（Grouped-Query Attention，分组查询注意力）将多个 Query 头划分为组并共享单对 Key/Value 头，在大幅缩减
  KV Cache 显存开销的同时保留接近 MHA 的建模表达力，是现代开源 LLM 的标准基准架构
sources:
- wiki/sources/2026-09-03_Attention-Mechanisms-in-LLMs,-clearly-explained_1a068e0f112668fe.md
updated: '2026-09-21'
aliases:
- GQA
- Grouped Query Attention
- 分组查询注意力
- 概念_GQA分组查询注意力
---

# 概念_GQA_分组查询注意力

## 定义与架构原理

**分组查询注意力（Grouped-Query Attention, GQA）**（Ainslie 等，2023）是一种旨在降低大模型推理自回归解码期 [[concepts/概念_KV_Cache_键值缓存|KV Cache]] 显存开销的注意力架构变体。它在多头注意力（MHA）与多查询注意力（MQA）之间取得了极佳的精度与效率平衡：

- **MHA (Multi-Head Attention)**：$H$ 个 Query 头各自独立对应 1 个 Key 头和 1 个 Value 头，KV Cache 体积最大，显存随着并发 batch 与上下文长度线性爆炸；
- **MQA (Multi-Query Attention)**：所有 Query 头强制共享仅有的一对 Key/Value 头，KV Cache 缩减至 $1/H$，但由于强制共享键值表示，严重损失模型在复杂语义推理下的容量与精度；
- **GQA (Grouped-Query Attention)**：将 $H$ 个 Query 头划分为 $G$ 个组（Group），每组内的 Query 头共享同一个 Key 头和 Value 头。

```text
MHA:  [Q1] [Q2] [Q3] [Q4]      MQA:  [Q1] [Q2] [Q3] [Q4]      GQA (2 groups): [Q1] [Q2]   [Q3] [Q4]
       |    |    |    |                \   \   /   /                        \   /       \   /
      [K1] [K2] [K3] [K4]                 [K1]                                [K1]        [K2]
      [V1] [V2] [V3] [V4]                 [V1]                                [V1]        [V2]
   (4 KV heads per layer)          (1 KV head per layer)             (2 KV heads per layer)
```

---

## 性能与显存收益

1. **显存缩减倍率**：
   若模型拥有 32 个 Query 头并划分为 8 个 KV 组（即每组 4 个 Query 头），KV Cache 的物理体积直接缩减为 MHA 的 $8/32 = 1/4$（即节省 75% 显存）。
2. **缓解内存带宽墙（Memory-Bandwidth Bound）**：
   在 LLM 自回归解码阶段，计算瓶颈主要在于从 GPU HBM 显存加载历史 KV 张量的访存带宽。GQA 将每次解码步加载的 KV 数据量削减至原来的 $1/4$ 到 $1/8$，显著提升并发吞吐量与解码速度。
3. **精度无损**：
   原始 GQA 论文及后续工业界模型评估表明，8 组 GQA 的模型表现几乎无损复刻了 MHA 的各项 Benchmark 表现，彻底解决了 MQA 的质量衰减缺陷。

---

## 主流注意力方案横向对比

| 注意力方案 | Key/Value 头数 | KV Cache 占用比例 | 解码内存带宽压力 | 建模质量表现 | 典型应用模型 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **MHA** | 等同于 Query 头数 ($H$) | $100\%$（基准） | 极高（易受带宽限制） | 基准（最高） | Transformer (2017), GPT-3 |
| **MQA** | 全局唯一 ($1$) | $1/H$（如 $\approx 3.1\%$） | 极低 | 明显掉点（复杂长文受损） | Falcon, PaLM |
| **GQA** | 分组数 ($G$) | $G/H$（如 $25\%$） | 显著降低 | 几乎与 MHA 持平 | Llama 2/3, Mistral, Qwen, Gemma |
| **MLA** | 低秩潜向量升维映射 | $\approx 5\% - 13\%$ | 最低 | 匹敌甚至超过 MHA | DeepSeek-V2, DeepSeek-V3, DeepSeek-R1 |

---

## 工业界落地

GQA 已经成为当代开源大语言模型的主流事实标准架构：
- **Meta Llama 系列**：Llama 2 (70B) 首次引入 8 组 GQA；Llama 3 全尺寸（8B/70B/405B）全面采用 GQA；
- **Mistral AI**：Mistral-7B、Mixtral 8x7B、Mixtral 8x22B 全面采用 GQA；
- **通义千问 (Qwen)**：Qwen2 / Qwen2.5 系列全量默认采用 GQA；
- **Google Gemma**：Gemma 2 系列采用 GQA。

---

## 关联

- **相关概念**: [[concepts/概念_KV_Cache_键值缓存|概念_KV_Cache]]、[[concepts/概念_MLA_多头潜在注意力|概念_MLA多头潜在注意力]]、[[concepts/概念_FlashAttention_快速注意力|概念_FlashAttention]]
- **相关来源**: [[wiki/sources/2026-09-03_Attention-Mechanisms-in-LLMs,-clearly-explained_1a068e0f112668fe.md]]