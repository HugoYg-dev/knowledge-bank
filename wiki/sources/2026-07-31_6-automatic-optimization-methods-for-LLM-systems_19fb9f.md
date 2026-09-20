---
type: source
tags:
- RSI
- AI-Agent/prompt-engineering
- LLM/arch
summary: 介绍了六种在大模型系统中实现自动化优化的前沿方法（OPRO, MIPROv2, TextGrad, GEPA, AlphaEvolve, AutoResearch），通过大模型自动反馈循环替代人工调优。
sources:
- raw/articles/2026-07-31_6-automatic-optimization-methods-for-LLM-systems_19fb9f.md
updated: 2026-08-04
---

# 6 automatic optimization methods for LLM systems

## 来源信息
- **来源**: Daily Dose of DS
- **作者**: Avi
- **日期**: 2026-07-31
- **原文链接**: [6 automatic optimization methods for LLM systems](https://fff97757.click.kit-mail3.com/v8uqlqw04vhrhvw8lw8ighvz3og4oi9hpqloo/m2h7h5h3d3rqm7imhq/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbGxtb3BzLWNyYXNoLWNvdXJzZS1wYXJ0LTEv)

## 核心要点
- **LLM 系统自动优化机制**：调优 AI 系统不再局限于训练模型参数，而是通过大模型编辑文本、提示词、代码乃至训练循环，并进行自动运行。这六种方法共享同一架构：**LLM 提出修改 -> 评估器评分 -> 保留最佳修改**。
- **OPRO (Google DeepMind)**：将语言模型本身作为优化器，维护一个包含过去提示词及得分的 Leaderboard，通过 Meta-prompt 提示词演进生成更强指令，适用于简单任务但易在困难任务上遇到瓶颈。
- **MIPROv2 (DSPy)**：同时优化指令文本和 few-shot 示例。通过在标注数据上运行程序保留成功样本生成 few-shot 示例，再通过贝叶斯搜索（Bayesian Search）寻找两者的最优组合。
- **TextGrad (Stanford)**：借鉴 PyTorch 反向传播机制，将多步 Pipeline 抽象为文本计算图，向后传导自然语言 Criticism 以实现梯度式文本优化。但图深度大于 3-4 层时容易发散。
- **GEPA (Berkeley)**：阅读完整执行 Trace，针对失败原因进行精准诊断；维持 Pareto 帕累托集以保留在特定切片上表现优异的 Specialist 样本，实现零权重修改下的高效强化。
- **AlphaEvolve (Google DeepMind)**：面向代码优化的演进机制，由两个 Gemini 模型（深度+广度）协同提出 Diff 进化修改代码，在矩阵乘法（突破 56 年前算法限制）和调度器上取得了人类未能发现的优化成果。
- **AutoResearch (Karpathy 实践)**：运行于 ML 训练脚本上的自主实验循环。编码 Agent 修改代码后进行 5 分钟实验，成功则 Git commit 锁死演进，失败则 Git reset 回滚。限制在于无法退回以获取更大收益，易陷入局部最优。

## 关联概念/实体
- 关联概念：[[wiki/concepts/概念_LLM系统自动优化方法论]]

## 关键引文
> "Tuning an AI system no longer means training it. Several methods now improve a system by editing its text, the prompt, the code, sometimes the training loop itself, and all of it runs automatically."
> "The pattern underneath all six is similar. Turn a system into text, define a way to measure it, and let a language model improve it in a loop."

---
> 📎 **物理文献**：[[raw/articles/2026-07-31_6-automatic-optimization-methods-for-LLM-systems_19fb9f.md]]
