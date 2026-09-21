---
type: entity
tags:
- AI-Agent/coding
- AI-Agent/prompt-engineering
summary: DSPy 是由斯坦福大学（Stanford NLP）开发并开源的一个颠覆性 AI 系统编程与优化框架。它的核心理念是将大语言模型的提示词工程（Prompt
  Engineering）转变为系统化的程序编译与参数优化，用“声明式模块与评估驱动优化”取代人工编写脆弱的 Prompt 文本。
sources:
- wiki/sources/Dropbox基于DSPy优化Dash Chat评估与提示词.md
updated: '2026-07-06'
---

# 实体：DSPy

## 简介

**DSPy** 是由斯坦福大学（Stanford NLP）开发并开源的一个颠覆性 AI 系统编程与优化框架。它的核心理念是将**大语言模型的提示词工程（Prompt Engineering）转变为系统化的程序编译与参数优化**，用“声明式模块与评估驱动优化”取代人工编写脆弱的 Prompt 文本。

## 核心算法与机制

1. **模块化设计（Signatures & Modules）**：使用类似 PyTorch 的声明式类定义 LLM 输入输出格式与任务目标（如 `dspy.ChainOfThought`、`dspy.Retrieve`）。
2. **GEPA（Generative Error-Driven Prompt Adaptation）**：强大的生成式误差驱动优化器。利用 LLM 评判器给出的评分、错误归因代码与推理理由（Reasoning Notes），精准分析回答为何失败，自动生成修补后的指令与少样本提示词。
3. **MIPROv2**：在海量候选项与数据回放中进行离线联合搜索与指令权重优化的先进算法。

## 在工业界落地案例

在 [[实体_Dropbox]] 的 Dash Chat 智能客服系统中：
- 利用人工标注对准 DSPy 驱动的 LLM-as-a-Judge 评判器。
- 利用 GEPA 算法在离线反事实回放（Counterfactual Replay）中自动进化 Dash Chat 的系统提示词。
- 达成了不完整回答率降低 26%、关键点漏答降低 13%、Token 用量下降 5.4% 的工业级量化双赢。

## 来源与参考

- [[Dropbox基于DSPy优化Dash Chat评估与提示词]]
- [[概念_Agent系统自动优化闭环]]
- [[概念_Agent完整轨迹评估]]