---
type: concept
tags:
- AI-Agent/deep-research
summary: Deep Research Agent 是由 LLM 驱动的 AI 系统，核心能力在于集成了动态推理、自适应规划、多轮迭代的外部数据检索与工具使用，并能生成全面的综合性分析报告。
sources:
- wiki/sources/DeepResearch的概念、核心挑战与进化路径.md
- wiki/sources/Tongyi DeepResearch的技术报告探秘.md
- wiki/sources/一篇95页最新80种Deep Research系统全面综述.md
- wiki/sources/通义 DeepResearch：开源 AI 智能体的新纪元.md
updated: '2026-09-21'
aliases:
- Deep-Research-Agent
- Deep Research Agent
- 深度研究智能体
- 概念_Deep-Research-Agent定义与分类
---

# 概念：Deep Research Agent 定义与分类

## 定义

Deep Research Agent 是由 LLM 驱动的 AI 系统，核心能力在于集成了**动态推理、自适应规划、多轮迭代的外部数据检索与工具使用，并能生成全面的综合性分析报告**。

来源：华为/利物浦/牛津综述论文《DEEP RESEARCH AGENTS: A SYSTEMATIC EXAMINATION AND ROADMAP》（arxiv:2506.18096）

## 与已有技术的边界

| 技术 | 特点 | DR Agent 的超越 |
|------|------|----------------|
| RAG | 单次检索回答事实性问题 | 处理需持续推理和多步骤探索的复杂任务 |
| 传统 Tool Use | 固定预设流程 | 高度自主，根据实时反馈动态调整策略 |
| Web-enhanced LLM | 将用户请求交给搜索引擎，LLM 总结结果 | 主动发起多轮工具调用，自主规划研究路径 |
| Deep Search/AI Search | 循环查询直到可回答 | 更复杂的多步推理、规划和工具使用 |

## 规划策略三种成熟度

| 模式 | 描述 | 代表系统 |
|------|------|----------|
| 仅规划（Planning-Only） | 直接根据初始指令执行，效率高但可能偏离意图 | Grok |
| 意图-规划（Intent-to-Planning） | 规划前先提问澄清用户意图 | OpenAI Deep Research |
| 统一意图-规划（Unified Intent-Planning） | 生成初步计划后呈现给用户确认或修改 | Gemini Deep Research |

## 架构维度分类（浙大综述，arxiv:2506.12594）

**4 维度分层分类法**：
1. 基础模型与推理引擎（上下文/记忆/推理框架）
2. 工具利用与环境交互（信息获取/专用工具集成）
3. 任务规划与执行控制（研究规划/多智能体协作）
4. 知识综合与输出生成（报告生成/交互式呈现）

## 实现架构四类

见 [[概念_Deep_Research_四类实现架构]]

## 四大核心挑战

见 [[概念_Deep_Research_四大挑战]]

## 来源

- [[DeepResearch的概念、核心挑战与进化路径]]
- [[一篇95页最新80种Deep Research系统全面综述]]
- [[通义 DeepResearch：开源 AI 智能体的新纪元]]
- [[Tongyi DeepResearch的技术报告探秘]]