---
type: concept
tags:
- LLM/training
summary: 大模型的三大缩放定律描述了计算资源的不同使用方式如何影响模型性能，分别对应预训练、后训练、推理三个阶段。
sources:
- wiki/sources/大规模神经网络优化_超参实践与规模律.md
updated: '2026-07-06'
---


# 概念：Scaling Law 三大规律

大模型的三大缩放定律描述了计算资源的不同使用方式如何影响模型性能，分别对应预训练、后训练、推理三个阶段。

## 预训练 Scaling Law（Kaplan 2022，arxiv 2203.15556）

- 扩大训练数据集规模、模型参数量和算力，模型性能系统性提升
- 性能 L 与参数量 N、数据量 D 成幂律分布：L ∝ N^(-α)，L ∝ D^(-β)
- Kaplan（OpenAI）结论：模型增大 5 倍，数据量增大 8 倍
- **Chinchilla 纠正**（Hoffmann 2022）：给定计算量 C，N_opt ≈ D_opt，即参数量翻倍时数据量也应翻倍
- 推动了 MoE、万亿参数 Transformer、分布式训练的发展

## 后训练 Scaling Law（arxiv 2410.12119）

- 通过微调、蒸馏、强化学习（RLHF/RLAIF）、Best-of-n 采样、搜索方法进一步提升预训练模型
- 后训练 = "职场培训"，使模型适应具体任务/领域
- 合成数据可扩充微调数据集，补充稀少场景

## 推理阶段 Scaling Law（Long Thinking，arxiv 2504.02495）

- 推理时投入更多计算资源，探索多条推理路径后选最佳
- 强调动态调整奖励机制而非增加模型参数
- 计算方法：多次/并行采样（多样性奖励）、SPCT（拒绝式微调+在线 RL）、元奖励模型
- 对多步推理与规划类开放性问题效果显著
- 代表模型：DeepSeek R1、OpenAI o1、Qwen3 推理模型

## 三大规律的层次

```
预训练 Scaling → 训练更大模型（参数+数据+算力）
后训练 Scaling → 让预训练模型适应任务（微调/RL/蒸馏）
推理 Scaling   → 推理时消耗更多算力换更好答案（Long Thinking）
```

## 相关资源

- [[大规模神经网络优化_超参实践与规模律]] — Kaplan/Chinchilla 详细推导
- [[概念_Fine_Tuning_模型微调]] — 后训练技术之一
- [[概念_RLHF_基于人类反馈的强化学习]] — 后训练技术之一
- [[实体_DeepSeek-R1]] — 推理 Scaling 代表模型