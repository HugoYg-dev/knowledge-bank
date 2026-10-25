---
type: entity
tags:
- CaseStudy/data-agent
summary: '- 类型：智能数据分析平台（ABI 平台）'
sources:
- wiki/sources/腾讯ABI工程架构探索与实践.md
- wiki/sources/腾讯OlaChat_LLM智能数据分析平台实践.md
updated: '2026-06-29'
---

# 实体：腾讯 OlaChat

## 基本信息

- **类型**：智能数据分析平台（ABI 平台）
- **归属**：腾讯 PCG 大数据平台部
- **定位**：基于大语言模型的智能数据助手，可灵活集成到各种数据分析产品中

## 核心能力

- 多轮对话系统（意图理解/上下文跟踪）
- Text2SQL（70B 微调混元模型）
- Text2DSL（NL→SQL→DSL 中间层方案）
- FlattenedRAG/StructuredRAG 元数据检索增强
- 指标分析（对接 tMetric Headless BI）
- 数据解读（异常检测/归因分析/趋势预测）
- SQL 纠错/补全/解读

## 技术架构

- **编排层**：DAG 图 + 统一协议，原子 Agent 自动流转
- **大模型**：腾讯混元（通用）+ 域微调模型（SQL 场景）
- **数据服务**：SQL 类服务 + HeadlessBI + 图表服务 + RAG
- **接入方式**：SaaS / 页面组件 / API / 独立部署 / 云原生

## 相关文章

- [[腾讯OlaChat_LLM智能数据分析平台实践]] — 算法侧（谭云志）
- [[腾讯ABI工程架构探索与实践]] — 工程架构侧（霍琦）