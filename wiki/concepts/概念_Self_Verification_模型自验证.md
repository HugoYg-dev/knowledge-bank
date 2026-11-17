---
type: "concept"
tags: ["LLM/training/RL", "RSI"]
summary: "大模型在不依赖外部标准答案的情况下，自主检验中间或最终产物正确性并依据验证反馈进行多轮纠错改进（Verification Loop）的能力与强化学习训练范式。"
aliases:
  - "Self-Verification"
  - "模型自验证"
  - "Self-Correction"
  - "自纠错"
  - "Verification Loop"
  - "验证闭环"
  - "Extended Verification Loops"
sources:
  - "wiki/sources/RSI，先会verify的模型先享受.md"
updated: "2026-11-17"
---

# 概念：Self-Verification（模型自验证）

## 定义

**Self-Verification（模型自验证）** 指大语言模型在推理或代码生成等任务中，不依赖外部标准答案或人工裁判，自主对生成产物进行检验、判断正误并定位缺陷的能力；将其嵌入多轮迭代流程，即构成 **Verification Loop（验证闭环）**：触发验证 $\to$ 基于证据给出结论 $\to$ 正确则继续、错误则探索修正路径。

在开放域真实任务缺乏简单 [[concepts/概念_Verifiable_Reward_可验证奖励机制|可验证奖励]] 的背景下，自验证与自纠错能力是推动 [[concepts/概念_RSI递归自我改进|RSI（递归自我改进）]] 从有界可验证任务走向通用复杂任务的核心环节。

## 核心机制与实证规律

### 1. 生成能力与验证能力分离（生成 != 验证）
- **核心发现** `[原文陈述]`：在 ICML 2026 *Learning to Self-Verify Makes Language Models Better Reasoners* 的 1,000 步 Math RL 对比实验中，仅训练做题（生成正确答案）并不必然提升判题（验证）能力；相反，专门训练判题的模型不仅验证能力显著高于 Base 模型，其做题准确率也接近纯做题模型，且平均输出长度更短。
- **纠错路径恢复**：在给定带错误 thinking prefix 的数学题续写实验中，判题模型的最终答对率高于纯做题模型与 Base 模型，表明自验证训练能够强化模型从错误中间状态中识别偏差并走回正确推理路径的能力。

### 2. 验证闭环（Verification Loop）的三类 RL 奖励设计

针对多轮「生成 $\to$ 验证 $\to$ 修正」轨迹难以直接评估的问题，学术界提出了三类代表性强化学习反馈机制：

| 方法 | 出处 | 核心思路 | 奖励设计要点 |
|------|------|----------|--------------|
| **ReVeal** | ICLR 2026（MSRA / 同济 / 中科大） | **奖励验证行为**（代码场景） | 模型交替写代码与写单元测试；训练期用参考实现过滤测试，奖励包含：① 测试通过参考实现的比例；② 下一轮代码修改的通过率差值（同步归功于上一轮写测试）；③ 终版测试通过率 $\times 5$ + 格式分。 |
| **SCoRe** | ICLR 2025（[[entities/实体_DeepMind|Google DeepMind]]） | **奖励有效修改**（两轮自纠错） | 针对单阶段 RL 导致模型首轮变强、次轮懒得修改的问题，采用两阶段训练：阶段一对首轮加较强 KL 约束保留错误样本供次轮练纠错；阶段二叠加 `(第二轮得分 - 第一轮得分)` 差值奖励，错改对加分、对改错扣分。 |
| **RepExp** | ICLR 2026（普林斯顿 / MSR） | **奖励多样探索**（批内采样） | 在 [[concepts/概念_GRPO_群组相对策略优化|GRPO]] 正确性奖励之外，利用模型隐藏表示衡量同批独立采样解答的差异度并给予探索奖励，使错误解答也能因提供多样路径获得正向信号。 |

## 演进趋势：从单轮 Judge 到多轮 Trajectory

早期工作（如 2023 年的 [[concepts/概念_LLM_as_a_Judge校准|LLM-as-a-Judge]] 与 Self-Rewarding）多聚焦于单轮生成打分；随着 Agentic Coding 与长程任务的发展，优化目标已转向多轮交互轨迹（Trajectory）。在交互闭环中，单步验证即便存在误差，只要能有效驱动下一步修改向正确方向收敛即具备工程价值，同时验证准确率也可依托环境反馈与交互上下文持续校准。

## 关联概念与来源

- **来源**：[[wiki/sources/RSI，先会verify的模型先享受|RSI，先会 verify 的模型先享受]]
- **关联概念**：[[concepts/概念_RSI递归自我改进]]、[[concepts/概念_GRPO_群组相对策略优化]]、[[concepts/概念_RLVR_可验证奖励强化学习]]、[[concepts/概念_LLM_as_a_Judge校准]]
- **关联实体**：[[entities/实体_DeepMind]]、[[entities/实体_DeepSeek]]、[[entities/实体_Gemini]]
