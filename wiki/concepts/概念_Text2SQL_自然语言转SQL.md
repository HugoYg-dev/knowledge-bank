---
type: concept
tags:
- RAG/retrieval
summary: Text2SQL 是一项将自然语言查询转换为 SQL 语句的技术，允许用户通过日常语言与数据库交互而不需要掌握专业 SQL 语法。在 RAG 系统中用于结构化数据的精准查询，与文本切片检索互补。
sources:
- wiki/sources/TableRAG_文本表格异构问答.md
- wiki/sources/企业落地NL2SQL_AI-ready_data与小模型.md
- wiki/sources/优图RAG技术详解.md
- wiki/sources/腾讯ABI工程架构探索与实践.md
- wiki/sources/腾讯OlaChat_LLM智能数据分析平台实践.md
updated: '2026-09-21'
aliases:
- Text2SQL
- Text-to-SQL
- NL2SQL
- 自然语言转SQL
- 概念_Text2SQL
---

# 概念_Text2SQL_自然语言转SQL


## 定义

Text2SQL 是一项将自然语言查询转换为 SQL 语句的技术，允许用户通过日常语言与数据库交互而不需要掌握专业 SQL 语法。在 RAG 系统中用于结构化数据的精准查询，与文本切片检索互补。

## 核心挑战

- 领域知识泛化能力
- 自然语言表达的多样性与复杂性
- 语义不明确、不完整
- 不同数据库方言适配（SQLite/MySQL等）

## MAC-SQL 多智能体框架（优图，COLING 2025）

- Selector（筛选器）：从众多表中选择相关表和列，减轻不相关信息干扰
- Decomposer（分解器）：将复杂问题分解为子问题逐步解决
- Refiner（优化器）：执行SQL获取反馈，根据反馈优化错误SQL

## 关键技术

### Schema Linking 与 Value Linking
- Schema Linking：将 Query 与数据库模式元素关联（如"学生"→student表）
- Value Linking：将 Query 中具体值与数据库存储值匹配（如"上个月"→date条件）

### 双引擎执行
- MySQL：精确查询
- Elasticsearch：AST语法校验+泛化查询，提升模糊匹配召回

### 数据合成
- 自动生成多语言数据库表结构+自然语言问题+带推理过程SQL答案
- 快速适配新场景，降低人工标注成本

## 关联

- 相关概念：[[概念_Query_Construction_查询构建]]、[[概念_结构化输出]]、[[概念_迭代式表格推理]]
- 实体：[[实体_Elasticsearch]]、[[实体_MAC-SQL]]
- 来源：[[优图RAG技术详解]]、[[TableRAG_文本表格异构问答]]