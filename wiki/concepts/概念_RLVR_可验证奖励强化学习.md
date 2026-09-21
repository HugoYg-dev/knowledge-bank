---
type: concept
tags:
- LLM/training/RL
summary: RLVR（Reinforcement Learning with Verifiable Rewards）是设计可自动验证结果正确与否的任务和奖励，让
  RL 不过多依赖人类反馈、实现高度自主优化。是 RL Infra 提供商最直接和最强劲的增长动力。
sources:
- wiki/sources/DeepSeek-R1工作原理.md
- wiki/sources/GPT5通用验证器与RL探索.md
- wiki/sources/R1复现认知与误区.md
- wiki/sources/RL_Infra行业全景.md
- wiki/sources/强化学习入门指南_RLHF到GRPO.md
updated: '2026-09-21'
aliases:
- RLVR
- Reinforcement Learning with Verifiable Rewards
- 可验证奖励强化学习
- 概念_RLVR
---

# 概念_RLVR_可验证奖励强化学习

## 定义

RLVR（Reinforcement Learning with Verifiable Rewards）指设计出可自动验证结果正确与否的任务和奖励，让强化学习过程不用过多依赖人类反馈，实现高度自主的优化。

## 意义

- 是 RL Infra 提供商最直接和最强劲的增长动力
- 要让 RL 训练获得与 GPT-3 相当的"经验"规模，需显著 scale RL 环境的数量和多样性，并让这些环境能通过 RLVR 方式自动评估
- 当前热议趋势：DeepSeek-R1 RL 约 60 万道数学题（人类 6 年任务量），而 GPT-3 训练语料 3000 亿 token（数万年人类写作），差距巨大

## 与复制训练的关系

Mechanize 的复制训练本质是一种 RLVR 实现——用单元测试通过与否作为自动验证的奖励信号。

## 关联

- [[RL_Infra行业全景]]（来源）
- [[概念_复制训练]]
- [[概念_RL环境]]
- [[概念_RLaaS_强化学习即服务]]