---
type: concept
tags:
- AI-Agent/AI-BI
summary: M-Schema 是一种面向 NL2SQL 的增强型数据库 Schema 表示格式，在传统表/列清单基础上补充多维语义信息，显著提升字段语义可读性与模型可对齐性。
sources:
- wiki/sources/企业落地NL2SQL_AI-ready_data与小模型.md
updated: '2026-09-21'
aliases:
- M-Schema
- MSchema
- 增强Schema表示
- 增强元数据模式
- 概念_M-Schema
---

# 概念_M_Schema_增强元数据模式

M-Schema 是一种面向 NL2SQL 的增强型数据库 Schema 表示格式，在传统表/列清单基础上补充多维语义信息，显著提升字段语义可读性与模型可对齐性。

## M-Schema 与传统 Schema 对比

| 信息维度 | 传统 Schema | M-Schema |
|----------|-------------|----------|
| 表名/列名 | ✅ | ✅ |
| 字段类型 | ✅ | ✅ |
| 主键/外键 | ✅ | ✅ |
| 中文业务释义 | ❌ | ✅ |
| 真实值示例 | ❌ | ✅ |
| 约束信息 | 部分 | ✅（约束池注入）|

## 约束池（Constraint Pool）

配合 M-Schema 使用的约束池，能自动识别查询语义类型并注入约束：

- **计数查询** → 自动添加 COUNT/DISTINCT
- **聚合查询** → 注入精度/去重约束
- **多行结果** → 注入排序/Top-K/窗口约束

作用：增强训练数据多样性与推理鲁棒性。

## 推理时处理

- 对不可读字段名做**临时可读映射**
- 推理完成后**后处理映回**原始字段名
- 提高"表/列命中"准确率

## 关联

- [[企业落地NL2SQL_AI-ready_data与小模型]]
- [[概念_AI_Ready_Data_AI就绪数据]]
- [[概念_Text2SQL_自然语言转SQL]]
- [[概念_Schema_Linking_数据库模式联接]]