---
type: entity
tags:
- AI-Agent/AI-BI
summary: Qwen2.5-Coder 是阿里巴巴通义团队发布的代码专用大模型系列，在 NL2SQL 等代码生成任务上表现优异。
sources:
- wiki/sources/企业落地NL2SQL_AI-ready_data与小模型.md
- wiki/sources/后训练认知_SFT_vs_RL_记忆与遗忘机制.md
updated: '2026-06-29'
---
# 实体：Qwen2.5-Coder

Qwen2.5-Coder 是阿里巴巴通义团队发布的代码专用大模型系列，在 NL2SQL 等代码生成任务上表现优异。

## 基本信息

- 开发方：阿里巴巴通义团队
- 参数规模：覆盖 3B/7B 等不同规格
- 专长：代码/SQL 生成

## 在 NL2SQL 中的应用

矩阵起源 NL2SQL 实践中选用 Qwen2.5-Coder 3B/7B 作为基座：
- **LoRA 微调**：轻量精调，适配业务 Schema 和 SQL 风格
- **DeepSpeed 优化**：显存/吞吐优化
- **低温度/束搜索**：确定性更强，按模板输出
- **训练格式**：ChatML 指令格式，仅在 assistant 段计算损失

## 为什么选代码向小模型

- 预训练偏置：代码/SQL 语料带来强语法与组合性偏置
- 确定性更强：配合保守解码更易"按模板出活"
- 工程优势：可本地/私有化部署，延迟与成本优势

## 实测结果

与 M-Schema + BM25→SIC 两级 Linking 配合：
- 结构幻觉率：7.9% → 1.3%
- Execution Accuracy 提升 +6.4%

## 关联

- [[企业落地NL2SQL_AI-ready_data与小模型]]
- [[概念_Text2SQL_自然语言转SQL]]
- [[概念_Schema_Linking_数据库模式联接]]
- [[实体_通义千问]]