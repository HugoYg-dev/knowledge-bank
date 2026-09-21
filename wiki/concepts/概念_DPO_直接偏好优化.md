---
type: concept
tags:
- LLM/training/post-train
summary: 直接偏好优化，无需显式训练奖励模型，直接通过人类偏好数据优化策略模型
sources:
- wiki/sources/375篇文献_推理大模型后训练技术综述.md
- wiki/sources/LLM后训练技术全景解读.md
- wiki/sources/淘宝直播数字人_LLM文案生成技术.md
updated: '2026-09-21'
aliases:
- DPO
- Direct Preference Optimization
- 直接偏好优化
- 概念_DPO
---

# 概念_DPO_直接偏好优化

## 定义
直接偏好优化（Direct Preference Optimization, DPO）是一种轻量级且稳定的强化学习人类偏好对齐（RLHF）算法。与传统的 PPO 不同，DPO 将强化学习目标重新参数化，跳过了奖励模型（Reward Model）的显式训练，直接使用偏好数据（正例和负例）对策略模型进行交叉熵损失优化。

## 核心优势与特点
- **无需奖励模型**：降低了显存开销与训练管线的复杂性。
- **稳定性高**：避免了强化学习（如 PPO）中常见的模式崩溃（Mode Collapse）或梯度爆炸问题，优化过程等价于简单的监督学习。
- **依赖数据质量**：由于没有奖励模型泛化能力的兜底，DPO 对高质量成对偏好数据（Chosen vs Rejected）的要求非常高，尤其在微调推理大模型时。

## 关联实体 / 概念
- 概念：[[概念_RLHF_基于人类反馈的强化学习]]、[[概念_PPO_近端策略优化]]、[[概念_GRPO_群组相对策略优化]]