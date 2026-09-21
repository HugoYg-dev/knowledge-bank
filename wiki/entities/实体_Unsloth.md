---
type: entity
tags:
- LLM/training/RL
- Skill/python
summary: Unsloth 是 Daniel Han 和 Michael Han 兄弟团队开发的开源 LLM 微调框架，专注于高效微调和强化学习训练，GitHub
  星数超过 4 万。
sources:
- wiki/sources/强化学习入门指南_RLHF到GRPO.md
updated: '2026-06-29'
---

# 实体：Unsloth

Unsloth 是 Daniel Han 和 Michael Han 兄弟团队开发的开源 LLM 微调框架，专注于高效微调和强化学习训练，GitHub 星数超过 4 万。

## 核心特性

- 支持 GRPO 训练推理模型
- 15GB 显存支持最多 17B 参数模型训练（Llama 3.1/Phi-4/Mistral/Qwen2.5）
- 最低 5GB 显存可训练 1.5B 以下模型
- 内置 GRPO 训练损失跟踪，无需 wandb 外部工具

## GRPO 训练工作流

1. 对每问答对生成多种候选答案（默认 8 种变体）
2. 奖励函数评估每个答案
3. 逐步更新权重

## 相关资源

- 官方文档：https://docs.unsloth.ai/basics/reinforcement-learning-guide
- GitHub：https://github.com/unslothai/unsloth

## 关联

- [[概念_GRPO_群组相对策略优化]] — 框架支持的核心算法
- [[强化学习入门指南_RLHF到GRPO]] — 出品的入门教程