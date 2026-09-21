---
type: concept
tags:
- RAG/retrieval
summary: Adaptive-RAG（自适应 RAG）是根据查询复杂度和要求自适应地选择检索和生成策略的 RAG 方法，避免对所有查询使用统一流程。
sources:
- wiki/sources/提升RAG问答质量的技术路线.md
updated: '2026-09-21'
aliases:
- Adaptive-RAG
- Adaptive RAG
- 自适应RAG
- 自适应检索增强生成
- 概念_Adaptive-RAG
---

# 概念_Adaptive_RAG_自适应检索增强生成


## 定义

Adaptive-RAG（自适应 RAG）是根据查询复杂度和要求自适应地选择检索和生成策略的 RAG 方法，避免对所有查询使用统一流程。

## 工作原理

- 动态评估查询需求和复杂度
- 简单问题直接检索回答，复杂问题启用多轮检索和推理
- 自适应选择检索策略和生成方式

## 优势

- 提高效率：减少不必要的计算
- 增强准确性：动态评估避免低质量答案
- 灵活应对多样化查询
- 减少计算开销：简单问题不做多轮生成

## 关联

- 相关概念：[[概念_CRAG_纠正性检索增强生成]]、[[概念_Self_RAG_自省式检索增强生成]]、[[概念_RAG_Routing_检索智能路由]]、[[概念_RAG基础流程]]
- 来源：[[提升RAG问答质量的技术路线]]

> 注：本页 confidence 为 medium，全文仅概要介绍未展开算法细节。