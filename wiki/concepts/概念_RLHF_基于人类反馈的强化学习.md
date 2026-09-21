---
type: concept
tags:
- LLM/training/RL
summary: RLHF（Reinforcement Learning from Human Feedback）是 OpenAI 使 ChatGPT 等模型与人类偏好对齐的核心技术框架。
sources:
- wiki/sources/强化学习入门指南_RLHF到GRPO.md
updated: '2026-09-21'
aliases:
- RLHF
- 基于人类反馈的强化学习
- 概念_RLHF基于人类反馈的强化学习
---

# 概念：RLHF 基于人类反馈的强化学习

RLHF（Reinforcement Learning from Human Feedback）是 OpenAI 使 ChatGPT 等模型与人类偏好对齐的核心技术框架。

## 基本流程

1. 收集人类偏好数据（如 👍/👎 标注）
2. 训练奖励模型（Reward Model）拟合人类偏好
3. 用 PPO 以奖励模型为信号优化 LLM

## RLHF 的局限

- 依赖人工标注，成本高、难以扩展
- 神经网络奖励模型可能被"奖励黑客"攻击
- 长 CoT 场景下维护多个大模型开销极大

## RLHF → RLVR 的演进

- RLVR（可验证奖励的 RL）：用自动可验证的规则奖励替代人工偏好奖励模型
- DeepSeek-R1 证明：规则奖励（准确性+格式）在数学/代码任务上足够有效
- 从"人类打分"到"规则验证"，极大降低成本并避免奖励黑客

## 关联

- [[概念_PPO_近端策略优化]] — RLHF 的实现算法
- [[概念_GRPO_群组相对策略优化]] — RLHF 的高效替代
- [[概念_RLVR_可验证奖励强化学习]] — RLHF 的演进方向
- [[强化学习入门指南_RLHF到GRPO]]