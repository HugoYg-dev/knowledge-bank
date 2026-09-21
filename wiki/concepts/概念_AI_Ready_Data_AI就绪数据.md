---
type: concept
tags:
- AI-Agent/AI-BI
summary: AI-ready data 是指经过系统化整理、使 AI 模型（特别是 NL2SQL 场景）能够可靠使用的数据底座，是 NL2SQL 可靠落地的第一性问题。
sources:
- wiki/sources/企业落地NL2SQL_AI-ready_data与小模型.md
updated: '2026-09-21'
aliases:
- AI-ready data
- AI-ready Data
- AI就绪数据
- 概念_AI-ready_data
---

# 概念：AI-ready data

AI-ready data 是指经过系统化整理、使 AI 模型（特别是 NL2SQL 场景）能够可靠使用的数据底座，是 NL2SQL 可靠落地的第一性问题。

## 核心组成

AI-ready data 包含以下关键要素：

1. **元数据**：表/列的完整描述，包括字段类型、主外键关系
2. **业务语义**：字段别名词典、指标口径、实体映射（如 amt/dt/no 在不同库的不同含义）
3. **权限信息**：多租户/行列权限/审计配置
4. **样例 SQL**：历史查询样本，帮助模型对齐业务意图
5. **真实值示例**：字段中的实际枚举值，提升 Schema Linking 准确性

## M-Schema 格式

M-Schema 是 AI-ready data 的具体表示形式，在传统"表/列清单"基础上补充：

- 字段类型（int/varchar/date 等）
- 主键/外键关系
- 中文业务释义
- 真实值示例（如 status 字段的 "active"/"inactive"）

## 为什么重要

没有 AI-ready data，NL2SQL 面临：
- **业务语义缺席**：模型只能猜字段含义，生成错误 SQL
- **治理割裂**：能生成但不能执行（权限/合规限制）
- **幻觉高发**：模型填补语义空白导致结构/语义幻觉

## 关联

- [[企业落地NL2SQL_AI-ready_data与小模型]]
- [[概念_Text2SQL_自然语言转SQL]]
- [[概念_Schema_Linking_数据库模式联接]]
- [[概念_M_Schema_增强元数据模式]]