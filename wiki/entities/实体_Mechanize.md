---
type: entity
tags:
- LLM/training/RL
- Infra/rl
summary: Mechanize 是 RL 环境平台初创公司，提出复制训练（Replication Training）新范式——让 AI Agent 复现现有软件作为
  RL 训练任务，用单元测试做自动奖励验证。Founder 来自 Stripe 和 Epoch AI。
sources:
- wiki/sources/RL_Infra行业全景.md
updated: '2026-06-29'
---

# 实体：Mechanize

## 简介

Mechanize 是新锐 RL 环境平台公司，Founder 来自 Stripe 和 Epoch AI（AI frontier benchmark startup），获 Nat Fridman 和 Daniel Gross 天使支持。

## 核心创新：复制训练（Replication Training）

- 让 AI Agent 去完整复现现有软件产品或特定功能作为训练任务
- 通过自动化验证（如 agent 代码是否通过原始仓库所有单元测试）提供可验证奖励信号
- 将开放模糊的创造性任务转化为有明确奖励的 RL 问题
- 利用互联网中大量已有软件源源不断生成任务（类比预训练语料）

## 关联

- [[RL_Infra行业全景]]（来源）
- [[概念_复制训练]]
- [[概念_RL环境]]