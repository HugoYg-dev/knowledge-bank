---
type: concept
tags:
- AI-Agent/AI-BI
summary: Schema Linking（Schema 联接）是 NL2SQL 流程中的关键预处理步骤，将用户自然语言查询与数据库表/列建立映射关系，从大型
  Schema 中筛选出与查询最相关的表和列。
sources:
- wiki/sources/企业落地NL2SQL_AI-ready_data与小模型.md
- wiki/sources/优图RAG技术详解.md
updated: '2026-09-21'
aliases:
- Schema Linking
- Schema联接
- 模式映射
- 概念_Schema_Linking
---

# 概念：Schema Linking

Schema Linking（Schema 联接）是 NL2SQL 流程中的关键预处理步骤，将用户自然语言查询与数据库表/列建立映射关系，从大型 Schema 中筛选出与查询最相关的表和列。

## 作用

在大型数据库（数十张表/数百列）场景中，直接把全量 Schema 输入给模型会导致：
- Context 超长，Lost in the middle 问题
- 无关表/列干扰生成，提高幻觉率

Schema Linking 通过**降维**解决此问题：从全量 Schema → 精简 Schema。

## 两级 Schema Linking 方案（BM25 + SIC）

### 第一级：BM25 粗排

- 将"表名 + 列名 + 注释"拼成文档
- 对用户问句做 BM25 打分
- 取 Top-k 候选表
- 延迟：**<5ms**，可支持在线服务

### 第二级：SIC 精排（Schema Item Classifier）

- Encoder + 交互层架构
- 对候选表/列逐项计算相关性分数
- 输出精简 Schema
- 资源：批量推理，显存 **<2GB**

## 工程实践要点

- BM25 与 SIC 结果合并后序列化为 M-Schema 格式
- 训练与推理使用**同一套 Schema Linking 流程**（Train-Infer 一致）
- Prompt 中重复注入问句，降低 Schema 噪声干扰

## 实测效果

- 配合小模型 + LoRA 微调后：
  - 结构幻觉率：7.9% → **1.3%**
  - 语义误配：约 **-18%**

## 关联

- [[企业落地NL2SQL_AI-ready_data与小模型]]
- [[概念_Text2SQL_自然语言转SQL]]
- [[概念_M_Schema_增强元数据模式]]
- [[概念_AI_Ready_Data_AI就绪数据]]
- [[概念_BM25_最佳匹配25算法]]