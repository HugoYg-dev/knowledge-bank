---
type: concept
tags:
- RAG/retrieval
summary: Text2SQL 是一项将自然语言查询转换为 SQL 语句的技术，允许用户通过日常语言与数据库交互而不需要掌握专业 SQL 语法。在 RAG 系统与 Data Agent 中用于结构化数据的精准查询，正从端到端直写转向受约束的业务语义中间态翻译。
sources:
- wiki/sources/TableRAG_文本表格异构问答.md
- wiki/sources/企业落地NL2SQL_AI-ready_data与小模型.md
- wiki/sources/优图RAG技术详解.md
- wiki/sources/腾讯ABI工程架构探索与实践.md
- wiki/sources/腾讯OlaChat_LLM智能数据分析平台实践.md
- wiki/sources/谈一谈最近对于Data Agent的学习.md
updated: '2026-11-12'
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

## 在 Data Agent 中的范式跃迁：从端到端直写到受约束业务语义中间态

随着企业级 [[concepts/概念_Data_Agent_数据智能体|Data Agent]] 的演进，工业界逐渐放弃了让大模型直接从自然语言跳到原生 SQL 的做法：
- **端到端直写的层叠风险**：单次生成迫使模型同时解决业务含义、表结构、字段匹配、JOIN 机制、过滤条件和聚合规则六项任务，错误率层层放大且无法精确定位归因。
- **业务语义中间态（Semantic Plan / IR）**：现代实践采用分阶段架构，模型仅输出受约束的业务语义表达（严禁直接出现物理表名与物理字段），再由确定性引擎结合版本化语义层编译为物理 SQL 或 BI API 调用，并在执行引擎侧实施只读拦截、行数上限与累计字段硬校验。

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

- 相关概念：[[concepts/概念_Data_Agent_数据智能体]]、[[概念_Query_Construction_查询构建]]、[[概念_结构化输出]]、[[概念_迭代式表格推理]]
- 实体：[[实体_Elasticsearch]]、[[实体_MAC-SQL]]、[[entities/实体_腾讯OlaChat]]
- 来源：[[优图RAG技术详解]]、[[TableRAG_文本表格异构问答]]、[[sources/谈一谈最近对于Data Agent的学习]]
