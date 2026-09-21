---
type: entity
tags:
- AI-Agent/multi-agent
- RAG/retrieval
summary: 腾讯优图实验室提出的面向复杂数据查询的 Text-to-SQL 多智能体协作框架。
sources:
- wiki/sources/优图RAG技术详解.md
updated: '2026-07-01'
---

## 简介

MAC-SQL（Multi-Agent Collaborative Framework for Text-to-SQL）是腾讯优图实验室提出的多智能体协作 Text2SQL 框架，发表于 COLING 2025。

## 架构

由三个 Agent 组成：
1. **Selector（筛选器）**：从众多表中选择相关表和列，减轻不相关信息干扰
2. **Decomposer（分解器）**：将复杂问题分解为子问题逐步解决
3. **Refiner（优化器）**：执行 SQL 获取反馈，根据反馈信息优化错误 SQL

## 效果

- 配合自研7B模型，执行准确率超 ChatGPT-3.5
- 配合 GPT-4 使用达 SOTA 水平，远超单独直接使用 GPT-4
- 基于 BIRD 和 Spider 数据集评测

## 关联

- 相关概念：[[概念_Text2SQL_自然语言转SQL]]
- 实体：[[实体_优图实验室]]
- 来源：[[优图RAG技术详解]]
