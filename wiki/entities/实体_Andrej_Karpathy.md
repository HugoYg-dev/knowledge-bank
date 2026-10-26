---
type: entity
tags:
- DeepLearning
- AI-Agent/coding
summary: Andrej Karpathy 是著名的人工智能科学家，曾任 OpenAI 创始成员及研究科学家、特斯拉 AI 团队高级总监（负责 Autopilot
  和 FSD 计算机视觉开发），现任 AI 教育与产品创业者（创立 Eureka Labs）。
sources:
- wiki/sources/Claude Code与Obsidian飞书知识库搭建实践.md
- wiki/sources/Karpathy推文引发的LLM_Wiki知识库搭建实践.md
- wiki/sources/Transformer大模型3D可视化_NanoGPT.md
- wiki/sources/手把手教你实现稀疏MoE语言模型.md
- wiki/sources/从 LOOP 到图探索 —— 算法模型的 AutoResearch 自进化系统架构演进之路  美团 · 技术团队.md
updated: '2026-10-26'
---

# 实体：Andrej Karpathy

## 简介

**Andrej Karpathy** 是著名的人工智能科学家，曾任 OpenAI 创始成员及研究科学家、特斯拉 AI 团队高级总监（负责 Autopilot 和 FSD 计算机视觉开发），现任 AI 教育与产品创业者（创立 Eureka Labs）。

## 在 LLM 领域与知识库中的核心贡献

1. **提出 LLM Wiki 知识管理范式**：在 2026 年 4 月，他在 X 上发表推文并发布 GitHub Gist（引发超 2000 万阅读的全网讨论），提出了著名的 [[concepts/概念_LLM_Wiki范式|LLM Wiki 范式]]，深刻指出“不要在查询时让 RAG 临时去拼凑，而要在摄入（Ingest）时让 LLM 作为后台程序员编译生成结构化的维基代码库”，彻底推动了从被动搜索向主动“知识编译与复利”的转变。
2. **AI 与大模型普及与开源教育**：开源并主导了 `nanoGPT` 等极简训练与学习框架，其技术讲座（如“State of GPT”、“Let's build GPT”）被业界奉为现代大模型入门标准经典。
3. **开创 AutoResearch 算法自主研究范式**：在 2025 年底开源 [[entities/实体_AutoResearch|AutoResearch]] 原型（基于单卡 H100 训练 5000 万参数教学级 GPT），以三文件架构（program.md/train.py/prepare.py）与不可篡改裁判、keep/reset Git 棘轮机制，首次跑通了 LLM 驱动的夜间无人值守算法研究循环，成为工业界（如美团）演进图探索自进化架构的基石。

## 来源与参考

- [[Karpathy推文引发的LLM_Wiki知识库搭建实践]]
- [[Claude Code与Obsidian飞书知识库搭建实践]]
- [[从 LOOP 到图探索 —— 算法模型的 AutoResearch 自进化系统架构演进之路  美团 · 技术团队]]
- [[concepts/概念_LLM_Wiki范式]]
- [[entities/实体_AutoResearch]]