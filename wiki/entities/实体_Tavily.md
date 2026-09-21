---
type: entity
tags:
- AI-Agent/deep-research
- RAG/retrieval
summary: 专注于面向 LLM 与 RAG 的 Web Search 搜索引擎供应商，主打网页降噪、正文抽取与高信息密度文本片段压缩。
sources:
- wiki/sources/搜索没有变便宜，但 Agent 把它拆成了新的供应链.md
updated: '2026-08-20'
---
# 实体：Tavily

## 简介

**Tavily** 是一家专注于为大语言模型（LLM）与智能体（Agentic Systems / RAG）提供网络检索服务的搜索基础设施供应商。它在搜索供应链中定位为**上下文精炼与混合检索层（Context Refinement Layer）**，被广泛集成于各类开源与生产级智能体框架（如 Codex、LangChain 等）中。

## 核心定位与技术特色

1. **面向 LLM 上下文优化**：
   - 与传统面向人类展示网页列表的搜索引擎不同，Tavily 的核心卖点在于对原始 HTML 进行实时降噪、正文精准抽取与多源内容融合压缩，直接向大模型输送高信息密度的干净文本片段。
2. **解决 Token 预算与抗噪痛点**：
   - 传统爬虫抓取常常夹带导航栏、广告、Cookie 弹窗等冗余信息，消耗大量 Context Window 并引发模型注意力漂移；Tavily 在检索端完成了格式净化与信息提炼。
3. **在 Agent Harness 中的应用**：
   - 在 [[entities/实体_Codex|Codex]] 等声明式 Harness 中，Tavily 常作为标准网络搜索 MCP 工具或 API 插件配置使用，支持单次交互与多步调研任务。

## 关联页面
- **核心概念**：[[concepts/概念_Agentic_Web_Search_智能体网络搜索|Agentic Web Search（Agent 网络搜索架构）]]、[[concepts/概念_上下文工程|上下文工程]]、[[concepts/概念_Harness_Engineering_宿主编排工程|Harness Engineering]]
- **同类搜索服务**：[[entities/实体_Exa|Exa]]
- **相关系统**：[[entities/实体_Codex|Codex]]

## 来源与参考
- [[sources/搜索没有变便宜，但 Agent 把它拆成了新的供应链|搜索没有变便宜，但 Agent 把它拆成了新的供应链]]
- [[sources/深度剖析 DeepSeek 最新的 Harness DSH：为了自进化这盘醋包了一整盘饺子|深度剖析 DeepSeek 最新的 Harness DSH：为了自进化这盘醋包了一整盘饺子]]
