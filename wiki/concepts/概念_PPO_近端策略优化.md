---
type: concept
tags:
- LLM/training/RL
summary: PPO（Proximal Policy Optimization）是 OpenAI 提出的强化学习算法，是 RLHF 的核心实现方式，也是 GRPO
  的前身。
sources:
- wiki/sources/375篇文献_推理大模型后训练技术综述.md
- wiki/sources/LLM后训练技术全景解读.md
- wiki/sources/强化学习入门指南_RLHF到GRPO.md
- wiki/sources/自适应快慢思考推理模型.md
updated: '2026-09-21'
aliases:
- PPO
- Proximal Policy Optimization
- 近端策略优化
- 概念_PPO近端策略优化
---

# 概念：PPO 近端策略优化

PPO（Proximal Policy Optimization）是 OpenAI 提出的强化学习算法，是 RLHF 的核心实现方式，也是 GRPO 的前身。

## 核心思想

- 通过 clip 操作限制策略更新幅度，避免训练不稳定
- 同时维护三个模型：生成策略（当前训练模型）+ 参考策略（原始模型）+ 价值模型（平均奖励估算器）
- 还需要独立的奖励模型评估当前环境奖励

## PPO 组成

| 组件 | 作用 |
|------|------|
| 生成策略（actor） | 当前被训练的 LLM |
| 参考策略（ref） | 原始模型，计算 KL 散度 |
| 价值模型（critic） | 与 actor 同规模，估算平均奖励 |
| 奖励模型 | 评估 response 质量 |

## 局限性

- 需要维护多个与 actor 同规模的模型，显存开销大
- 长 CoT 场景（上万 token 回复）下稳定性挑战更大
- 额外维护 critic_model 对训练框架稳定性要求高

## 与 GRPO 的关系

- GRPO 移除价值模型和神经网络奖励模型，用组内统计替代，显著降低开销
- 算法层面 PPO/GRPO/PRIME 均可涌现长 CoT 能力，具体算法不是复现 R1 的关键

## 关联

- [[概念_GRPO_群组相对策略优化]] — GRPO 是 PPO 的改进
- [[概念_RLVR_可验证奖励强化学习]] — 可验证奖励的 RL
- [[强化学习入门指南_RLHF到GRPO]]