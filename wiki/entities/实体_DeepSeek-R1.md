---
type: entity
tags:
- LLM/reasoning
- LLM/training/RL
summary: DeepSeek-R1 是深度求索（DeepSeek）发布的推理模型，通过大规模强化学习（GRPO）激励推理能力，性能与 OpenAI-o1-1217
  相当。
sources:
- wiki/sources/DeepSeek-R1工作原理.md
- wiki/sources/R1复现认知与误区.md
- wiki/sources/RL_Infra行业全景.md
- wiki/sources/入局AI_Infra系统设计与挑战.md
- wiki/sources/刚刚，DeepSeek Harness震撼开源：一切皆插件.md
- wiki/sources/大模型幻觉陷阱_AGI之路04期.md
- wiki/sources/强化学习入门指南_RLHF到GRPO.md
- wiki/sources/淘宝直播数字人_LLM文案生成技术.md
- wiki/sources/腾讯混元TurboS技术报告.md
updated: '2026-06-29'
---
# 实体：DeepSeek-R1

DeepSeek-R1 是深度求索（DeepSeek）发布的推理模型，通过大规模强化学习（GRPO）激励推理能力，性能与 OpenAI-o1-1217 相当。

## 关键数据

| 基准 | 得分 |
|------|------|
| AIME 2024 pass@1 | 79.8% |
| MATH-500 | 97.3% |
| Codeforces Elo | 2029（超 96.3% 人类） |
| AlpacaEval 2.0 LC胜率 | 87.6% |
| ArenaHard 胜率 | 92.3% |

## 训练方法

- 基础模型：DeepSeek-V3-Base
- 算法：GRPO（组相对策略优化）
- 四阶段管道：冷启动 SFT → 推理 RL → 拒绝采样 SFT → 全场景 RL
- 详见：[[概念_DeepSeek-R1训练管道]]

## 蒸馏版本

| 模型 | AIME 2024 | MATH-500 | 备注 |
|------|-----------|----------|------|
| R1-Distill-Qwen-7B | 55.5% | — | 超 QwQ-32B-Preview |
| R1-Distill-Qwen-32B | 72.6% | 94.3% | 与 o1-mini 相当 |
| R1-Distill-Qwen-14B | — | — | 超 QwQ-32B-Preview |
| R1-Distill-Llama-70B | — | — | 显著超 o1-mini |

## 前驱：DeepSeek-R1-Zero

- 纯 RL，无 SFT 冷启动
- AIME 2024: 15.6% → 71.0%（多数投票后 86.7%）
- 问题：可读性差、语言混杂

## 相关来源

- [[DeepSeek-R1工作原理]]
- [[R1复现认知与误区]]

## 关联

- [[实体_DeepSeek-V3]] — 基础模型
- [[概念_GRPO强化学习]] — 训练算法
- [[概念_DeepSeek-R1训练管道]] — 训练细节