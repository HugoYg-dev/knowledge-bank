---
type: concept
tags:
- LLM/arch/MoE
summary: MoE 训练中的关键挑战：如果 Router 训练不当，所有 Token 会集中路由到少数"热门"专家，导致其他专家欠训练，整体性能下降。
sources:
- wiki/sources/手把手教你实现稀疏MoE语言模型.md
- wiki/sources/腾讯混元TurboS技术报告.md
updated: '2026-09-07'
---


# 概念_MoE负载均衡

MoE 训练中的关键挑战：如果 Router 训练不当，所有 Token 会集中路由到少数"热门"专家，导致其他专家欠训练，整体性能下降。

## 问题根源

Router 的 top-k 选择是不可微的，早期训练中随机初始化可能使某些专家略占优势，正反馈导致"专家坍塌"（Expert Collapse）。

## 解决方案

### 1. 噪声 Top-k 门控（Noisy Top-k Gating）
在 Router logits 上添加标准正态噪声，鼓励 Token 路由多样化：
```python
noise = torch.randn_like(logits) * F.softplus(noise_linear(hidden))
noisy_logits = logits + noise
```

### 2. 辅助负载均衡损失（Auxiliary Loss）
额外增加一个损失项，惩罚专家使用率的不均匀程度：
```python
balance_loss = torch.std(gating_weights)  # 专家使用率标准差
total_loss = cross_entropy_loss + lambda_balance * balance_loss
```

### 3. 专家容量限制（Expert Capacity）
为每个专家设置最大接受 Token 数量（capacity），超出容量的 Token 不做计算（溢出）。

### 4. 组奖励调整（Group Reward Normalization，GRPO）
混元 TurboS 的 RL 训练中，对每个提示的响应组内重新缩放奖励，确保稳定的策略更新。

## 相关来源

- [[手把手教你实现稀疏MoE语言模型]]
- [[腾讯混元TurboS技术报告]]

## 关联概念

- [[概念_MoE混合专家]] — MoE 整体架构
- [[概念_MoE_Router_专家路由门控网络]] — 门控网络机制