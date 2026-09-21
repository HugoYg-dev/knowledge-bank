---
type: concept
tags:
- LLM/arch/MoE
summary: Router（门控网络）是 MoE 架构的核心组件，决定每个 Token 被分配到哪些专家。
sources:
- wiki/sources/手把手教你实现稀疏MoE语言模型.md
updated: '2026-09-21'
aliases:
- MoE Router
- Router
- 门控路由
- 专家路由
- 概念_MoE_Router
---

# 概念_MoE_Router_专家路由门控网络

Router（门控网络）是 MoE 架构的核心组件，决定每个 Token 被分配到哪些专家。

## 基本原理

- Router 由 Linear 层 + Softmax 组成，参数可学习，与模型其余部分联合训练
- 对 Token 的 hidden 向量（维度 d_model）做线性变换，投影到 Expert 数量维度，得到每个专家的"分数"
- 取 top-k 分数对应的专家激活，其余分数置 -inf 后做 Softmax 得到稀疏权重

## Top-k 门控

```
logits = Linear(hidden)                         # [batch, seq, num_experts]
top_k_logits, indices = logits.topk(k, dim=-1)  # 取前k个分数及索引
zeros = full_like(logits, -inf)
sparse_logits = zeros.scatter(-1, indices, top_k_logits)
weights = Softmax(sparse_logits)                # 非top-k位置权重为0
```

## 噪声 Top-k 门控

为防止少数专家被过度激活（"专家坍塌"），在 logits 上叠加缩放的标准正态噪声：

```
noise = randn_like(logits) * Softplus(noise_linear(hidden))
noisy_logits = logits + noise
```

训练时加噪声鼓励探索，推理时可不使用噪声。

## 共享专家（Shared Expert）

DeepSeek-V3 和混元 TurboS 的设计：每个 MoE 层包含 1 个对所有 Token 始终激活的共享专家。消融研究表明共享专家能提升整体建模性能。

## 相关来源

- [[手把手教你实现稀疏MoE语言模型]]

## 关联概念

- [[概念_MoE混合专家]] — MoE 整体架构
- [[概念_MoE负载均衡]] — Router 负载均衡问题