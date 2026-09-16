---
type: entity
tags:
- LLM/training/RL
- Infra/rl
summary: Fireworks AI 是创立三年的 AI Inference Infra 公司，近期将强化微调（RFT）产品化——用户只需提供评分函数，平台处理
  GPU 资源/训练循环/实验管理。客户用其微调开源模型效果追平闭源顶尖模型且推理快 10-40 倍。
sources:
- wiki/sources/RL_Infra行业全景.md
updated: '2026-06-29'
---

# 实体：Fireworks AI

## 简介

Fireworks AI 是创立三年的 AI Inference Infra 公司，近期把强化微调（RFT，Reinforcement Fine-Tuning）也做得很好，代表了 RLaaS 从 Inference 到 RFT 标准定义的路线。

## 核心能力

- 用户只需提供一个评分函数，GPU 资源、训练循环、实验管理全部由平台处理
- 多家早期客户用其平台微调开源模型，效果追平甚至超过封闭顶尖模型，推理速度提升 10-40 倍
- 与 Vercel 合作用 RFT 训练代码自动修复模型，性能媲美 GPT-4 衍生模型而运行快数十倍
- 本质：降低 RL 使用门槛，用模型 inference customization 商业模式接住用户

## 关联

- [[RL_Infra行业全景]]（来源）
- [[概念_RLaaS]]