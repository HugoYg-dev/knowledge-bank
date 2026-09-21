---
type: concept
tags:
- LLM/training/RL
summary: GRPO（Group Relative Policy Optimization，组相对策略优化）是 DeepSeek 提出的强化学习算法，被混元
  TurboS 等模型用于后训练阶段。
sources:
- wiki/sources/375篇文献_推理大模型后训练技术综述.md
- wiki/sources/DeepSeek-R1工作原理.md
- wiki/sources/GPT5通用验证器与RL探索.md
- wiki/sources/LLM后训练技术全景解读.md
- wiki/sources/R1复现认知与误区.md
- wiki/sources/后训练认知_SFT_vs_RL_记忆与遗忘机制.md
- wiki/sources/强化学习入门指南_RLHF到GRPO.md
- wiki/sources/腾讯混元TurboS技术报告.md
- wiki/sources/自适应快慢思考推理模型.md
updated: '2026-09-21'
aliases:
- GRPO
- Group Relative Policy Optimization
- 群组相对策略优化
- 概念_GRPO强化学习
---

# 概念_GRPO_群组相对策略优化

GRPO（Group Relative Policy Optimization，组相对策略优化）是 DeepSeek 提出的强化学习算法，被混元 TurboS 等模型用于后训练阶段。

## 核心思想

- 对同一提示采样一组响应（group），计算组内相对优势（advantage）
- 避免 PPO 需要独立 Critic 网络的开销，直接用组内奖励差值估计优势

## 混元 TurboS 的两阶段 GRPO

### 阶段一：推理 GRPO
- 目标领域：逻辑、代码、数学、科学
- 数据配比：代码:数学:逻辑&科学 = 2:2:1，共 30 万训练样本
- 较小 KL 散度约束，鼓励更广泛探索

### 阶段二：通用 GRPO
- 扩展到通用任务，保留 10% 阶段一推理数据
- 增大 KL 散度惩罚系数，缓解灾难性遗忘

## 实现细节

- **Token 级 GRPO 损失**：在 Token 级别重新制定，提高 KL 稳定性
- **提示过滤**：过滤掉模型总是成功或总是失败的极端案例，保留"不稳定"的提示作为对抗样本
- **采样温度**：设为 1.0（较低温度导致熵快速衰减，阻碍探索）
- **组奖励调整**：对每个提示的响应组内重新缩放奖励，确保不良响应获得负优势、良好响应获得正优势

## DeepSeek-R1 中的 GRPO

- DeepSeek 使用 GRPO 训练 DeepSeek-R1-Zero，从基础模型直接 RL，无 SFT
- 奖励来源：基于规则（准确性奖励 + 格式奖励），不用神经网络奖励模型
- 优势：相比 PPO 省去 Critic 模型，降低维护成本；长 CoT 场景下尤为关键

## GRPO vs PPO 对比

| 维度 | PPO | GRPO |
|------|-----|------|
| 价值模型 | 需要（与 actor 同规模）| 无，用组内采样统计替代 |
| 奖励模型 | 需要神经网络奖励模型 | 自定义规则函数即可 |
| 显存开销 | 高 | 低 |
| 适用场景 | 通用 RLHF | 推理模型、RLVR |

## 相关来源

- [[腾讯混元TurboS技术报告]]
- [[DeepSeek-R1工作原理]]
- [[强化学习入门指南_RLHF到GRPO]]

## 关联概念

- [[概念_CoT_自适应长短思考]] — GRPO 的应用之一
- [[概念_RLVR_可验证奖励强化学习]] — 可自动验证奖励的 RL
- [[概念_PPO_近端策略优化]] — GRPO 的前身
- [[实体_腾讯混元TurboS]] — 应用模型
- [[实体_DeepSeek-R1]] — GRPO 的代表性应用