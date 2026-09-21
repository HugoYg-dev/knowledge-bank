---
type: source
tags:
- LLM/arch
- LLM/inference
- DeepLearning
summary: 解构控制大语言模型（LLM）文本生成的 7 个核心解码参数：Max tokens、Temperature、Top-k、Top-p (Nucleus
  Sampling)、Frequency Penalty、Presence Penalty 以及 Stop Sequences 的工作原理与应用场景。
sources:
- raw/articles/2026-06-14_7-LLM-generation-parameters_19ec7f.md
updated: 2026-08-04
---

# 7 LLM generation parameters (7 个 LLM 生成参数)

## 来源信息
- **来源**: Daily Dose of DS
- **作者**: Avi Chawla
- **日期**: 2026-06-14
- **原始物理文献**: [[raw/articles/2026-06-14_7-LLM-generation-parameters_19ec7f.md]]

## 核心要点
- **硬性截断参数**: **Max tokens** 限制了单次响应生成的最大 Token 数量，过低会导致内容截断，过高则会浪费计算资源。
- **随机性与创造性**: **Temperature** 控制生成词的选择概率分布。接近 0 时使模型表现为确定性，而 0.7~1.0 之间能提升创造性和多样性。
- **概率截断策略**: 
  - **Top-k**: 将候选 Token 限制在概率最高的前 $k$ 个，增强文本聚焦度。
  - **Top-p (核采样)**: 动态选择累积概率达到 $p$ 的最小 Token 集合，较 Top-k 更加自适应。
- **惩罚机制**:
  - **Frequency Penalty**: 根据 Token 在已生成文本中出现的绝对频次进行累加惩罚，防止词汇重复。
  - **Presence Penalty**: 只要 Token 出现过一次就施加固定惩罚，促使模型引入新话题和概念。
- **输出边界控制**: **Stop Sequences** 是用户自定义的停止字符序列，当模型生成该序列时立即终止生成，对 JSON 等结构化输出非常重要。

## 关键引文
- "Knowing how to tune is important so that you can produce sharp and more controlled outputs."
- "Temperature governs randomness. Low temperature (~0) makes the model deterministic. Higher temperature (0.7–1.0) boosts creativity, diversity, but also noise."
- "Stop sequences: Custom list of tokens that immediately halt generation. Critical in structured outputs (e.g., JSON), preventing spillover text."

## 联动概念
- LLM文本生成解码参数

> 📎 **物理文献**：[[raw/articles/2026-06-14_7-LLM-generation-parameters_19ec7f.md]]
