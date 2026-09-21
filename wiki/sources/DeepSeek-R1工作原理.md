---
type: source
tags:
- LLM/reasoning
- LLM/training/RL
summary: DeepSeek-R1 通过大规模强化学习（GRPO）+ 多阶段训练激励推理能力，达到 OpenAI-o1 水平
sources:
- raw/articles/万字长文详解DeepSeek-R1模型工作原理.md
updated: '2026-07-01'
---
## 来源信息

- **标题**：万字长文详解DeepSeek-R1模型工作原理
- **作者**：沙丘智库研究团队
- **URL**：https://mp.weixin.qq.com/s/bXcCZI5djlpRiNM4VbZ4nA
- **原文解析**：基于 DeepSeek-R1 论文《DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning》

## 核心要点

- DeepSeek-R1-Zero 是首个验证**纯强化学习无需 SFT** 即可激励 LLM 推理能力的公开工作，基础模型 DeepSeek-V3-Base + GRPO 算法
- DeepSeek-R1-Zero 在 AIME 2024 上 pass@1 从 15.6% 升至 71.0%，多数投票后达 86.7%，与 OpenAI-o1-0912 持平
- DeepSeek-R1-Zero 面临可读性差、语言混杂问题；DeepSeek-R1 引入**冷启动数据**（数千条长推理链 SFT）和**多阶段训练**解决此问题
- **DeepSeek-R1 四阶段训练管道**：
  1. 冷启动 SFT（长推理链数据，含 `|special_token|<reasoning_process>|special_token|<summary>` 格式）
  2. 面向推理的 RL（推理任务准确性奖励 + 语言一致性奖励）
  3. 拒绝采样 + SFT（60 万推理 + 20 万非推理，共 80 万样本）
  4. 面向所有场景的 RL（推理用规则奖励 + 通用用奖励模型）
- 奖励系统：基于规则（准确性奖励 + 格式奖励），不用神经网络奖励模型，避免奖励黑客
- 推理能力蒸馏：用 80 万 R1 数据直接 SFT 小型模型（Qwen2.5/Llama 系列），效果优于直接在小模型上做 RL
- DeepSeek-R1-Distill-Qwen-32B 在 AIME 2024 得 72.6%、MATH-500 得 94.3%，与 o1-mini 相当
- 蒸馏 vs RL：蒸馏更高效，但突破智能边界仍需更强基础模型和更大规模 RL
- 失败尝试：PRM（过程奖励模型）和 MCTS 均未成功——PRM 难以自动标注中间步骤、奖励作弊；MCTS 搜索空间过大易陷局部最优
- DeepSeek-R1 在 AIME 2024 pass@1 79.8%，MATH-500 97.3%，Codeforces Elo 2029（超 96.3% 人类）

## 关键引文

> DeepSeek首次尝试使用纯强化学习来提升语言模型的推理能力，旨在探索大语言模型在没有任何监督数据的情况下开发推理能力的潜力，重点关注其通过纯 RL 流程实现的自我演化。具体来说，DeepSeek使用 DeepSeek-V3-Base作为基础模型，并采用 GRPO强化学习框架来提升模型在推理任务中的性能。 `[重点/高亮]`

> 这是首次公开研究验证了通过纯强化学习即可激励大语言模型的推理能力，而无需依赖SFT。 `[重点/高亮]`

> DeepSeek证明了可以将大型模型的推理模式蒸馏到小型模型中，从而使小型模型的性能优于直接在小模型上通过强化学习获得的推理模式。 `[重点/高亮]`

## 关联

- [[概念_GRPO_群组相对策略优化]] — GRPO 算法原理
- [[概念_RLVR_可验证奖励强化学习]] — 可验证奖励的强化学习
- [[概念_大模型训练三阶段]] — 后训练阶段
- [[概念_CoT_高级思维链方法]] — CoT 推理
- [[实体_DeepSeek-V3]] — 基础模型
- [[实体_DeepSeek-R1]] — 本文主角

---
> 📎 **物理文献**：[[raw/articles/万字长文详解DeepSeek-R1模型工作原理.md]]