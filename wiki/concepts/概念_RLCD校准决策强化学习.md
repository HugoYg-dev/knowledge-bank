---
type: "concept"
tags: ["LLM/training", "AI-Agent/tool-calling"]
summary: "Reinforcement Learning for Calibrated Decisions，校准决策强化学习。采用严格适当评分规则优化判别模型输出概率的统计一致性"
sources: ["wiki/sources/新模型Jev_爆红一周_不生成文字只输出概率却被玩出了花.md"]
updated: "2026-09-20"
---

# 概念：RLCD校准决策强化学习

## 定义

**RLCD（Reinforcement Learning for Calibrated Decisions，校准决策强化学习）** 是一种面向结构化决策与分类任务的强化学习优化范式。与旨在最大化生成质量或对齐偏好的传统 RLHF/DPO 不同，RLCD 的核心优化目标是**概率校准（Probability Calibration）**——确保模型输出的置信度在统计学上忠实反映预测正确的经验频率。

## 核心机制与数学基础

1. **严格适当评分规则（Proper Scoring Rules）**：采用交叉熵（Cross-Entropy）与 Brier Score 等损失函数，保证当且仅当模型报告真实后验概率分布时预期损失最小。
2. **评估指标**：核心衡量预期校准误差（Expected Calibration Error, ECE）与可靠性曲线（Reliability Diagram），防止模型产生盲目高置信度。
3. **与传统路线对比**：
   - **自回归生成预训练**：优化下一个 token 的困惑度（Perplexity），概率服务于词语连贯性而非单步决策；
   - **RLHF / DPO**：通过人类偏好对齐优化输出胜率，往往导致模型置信度极度膨胀（Overconfident）；
   - **RLCD**：直接以校准概率分布作为奖励与损失锚点，使输出概率具备统计决策有效性。

## 在 Agent 工程中的应用

在智能体架构中，RLCD 训练出的模型（如 Jev）可充当高可靠的**置信度门控器（Confidence Gating）**：
- 当模型对工具选择或路由分支的置信度高于预设阈值（如 `0.90`）时，直接执行自动化代码；
- 当置信度不足时，平滑降级至高推理成本大模型或人工审核（Human-in-the-loop），大幅压缩无人值守链路的级联崩溃率。

## 支撑来源

- [[wiki/sources/新模型Jev_爆红一周_不生成文字只输出概率却被玩出了花]]
