---
type: concept
tags:
- LLM/training/post-train
- LLM/training/RL
summary: '- on-policy 数据：训练数据由当前模型策略（当前参数）在训练时实时采样生成，数据分布与模型当前行为一致'
sources:
- wiki/sources/后训练认知_SFT_vs_RL_记忆与遗忘机制.md
updated: '2026-09-21'
aliases:
- on-policy
- off-policy
- 同策略与异策略
- 概念_on-policy与off-policy数据
---

# 概念：on-policy 与 off-policy 数据

## 定义

- **on-policy 数据**：训练数据由当前模型策略（当前参数）在训练时实时采样生成，数据分布与模型当前行为一致
- **off-policy 数据**：训练数据来自固定的静态数据集，与模型当前行为可能存在分布偏差

## 在后训练中的关键作用

- RL（如 GRPO、REINFORCE）天然使用 on-policy 采样，每轮训练前由当前策略生成候选输出
- SFT 使用预先收集的静态标注数据，属于 off-policy 训练
- 普林斯顿陈丹琦团队研究表明：**灾难性遗忘的根源是 off-policy 数据导致的分布错位**，而非算法形式（KL 方向）本身

## 实践含义

- Iterative-SFT：每个 epoch 用当前模型重新生成训练样本，模拟 on-policy，可复现 RL 的抗遗忘特性
- RL-to-SFT：先用 RL 采样，再用这些数据做 SFT，同样能继承 on-policy 的优势

## 关联

- [[后训练认知_SFT_vs_RL_记忆与遗忘机制]]
- [[概念_灾难性遗忘]]
- [[概念_GRPO_群组相对策略优化]]