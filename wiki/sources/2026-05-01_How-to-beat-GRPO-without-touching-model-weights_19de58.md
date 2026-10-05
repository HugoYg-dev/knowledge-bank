---
type: source
tags:
- LLM/training/RL
- AI-Agent/prompt-engineering
- LLM/training/post-train
summary: 详细阐述 GEPA 无梯度提示词进化算法，并横向对比其与 GRPO 等强化学习算法的优劣与应用场景。
sources:
- raw/articles/2026-05-01_How-to-beat-GRPO-without-touching-model-weights_19de58.md
updated: '2026-08-04'
---

# How to beat GRPO without touching model weights

## 来源信息
- **来源**: Daily Dose of DS
- **日期**: 2026-05-01
- **原文链接**: [RL 课程系列第一部分](https://www.dailydoseofds.com/rl-course-part-1/)
- **物理文献**: [[raw/articles/2026-05-01_How-to-beat-GRPO-without-touching-model-weights_19de58.md]]

## 核心要点
- **RL 中的信号压缩问题**: 传统 RL 算法（如 GRPO/PPO）在训练 LLM 时，每次 Rollout 产生海量结构化 Token（如思考步骤、工具调用、报错等），但最后都被压缩成一个标量 Reward，极大地浪费了诊断性信号，导致需要成千上万次 Rollout 才能收敛。
- **GEPA 算法核心思想**: 无需更新模型权重，而是将包含具体报错与反馈的完整 Trace 传给 Reflection LLM，由其分析并直接对 Prompt 进行进化改写。这种通过自然语言反思而非策略梯度的机制能大幅减少计算量（10-50x）。
- **反馈函数 $\mu_f$ 与 Pareto 采样**:
  - 反馈函数包含数值分数以及极度详尽的自然语言描述（如具体的编译器错误、未命中的实体等）。
  - 使用 Pareto 采样保留在单个子任务中表现最佳的 Prompt，防止收敛到局部均值最优。
- **2026 年应用实践纪律**:
  - 使用小而精的黄金样本库（20-100个样本）是最佳实践，过多样本反而会导致 Reflection 模型在反思过程中拟合噪音、过度拟合。
  - GEPA 适用于有具体文本反馈的复杂管道，而 GRPO 适用于拥有海量便宜 Rollout、开放权重和明确终态评估的场景。

## 关联概念
- [[concepts/概念_Agent系统自动优化闭环|概念_Agent系统自动优化闭环 (GEPA提示词进化算法)]]

## 关键引文
> "GRPO needs tens of thousands of rollouts to converge... So we end up backpropagating on one bit per trajectory while throwing away thousands of bits of structured signal."
> "GEPA’s core idea is that the rollout is already a natural language artifact, so let an LLM read it. Don’t reduce the trace to a number."
> "Reflection is far more sample-efficient than RL on compound systems. The two are increasingly combined, not pitted against each other."

---
> 📎 **物理文献**：[[raw/articles/2026-05-01_How-to-beat-GRPO-without-touching-model-weights_19de58.md]]
