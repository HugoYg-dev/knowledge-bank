---
type: concept
tags:
- RAG/retrieval
- RAG/query
summary: DMQR-RAG（Diverse Multi-Query Rewriting for RAG）是 ICLR2025 提出的多样化多查询改写框架。核心思想：基于不同信息层面设计多种改写策略，使每个改写结果提供独特信息，最大化检索文档覆盖率。
sources:
- wiki/sources/DMQR-RAG_多样查询改写.md
- wiki/sources/腾讯查询优化四大类综述.md
updated: '2026-09-21'
aliases:
- DMQR-RAG
- DMQR RAG
- 动态多查询改写
- 概念_DMQR-RAG
---

# 概念_DMQR_RAG_动态多查询改写检索


## 定义

DMQR-RAG（Diverse Multi-Query Rewriting for RAG）是 ICLR2025 提出的多样化多查询改写框架。核心思想：基于不同信息层面设计多种改写策略，使每个改写结果提供独特信息，最大化检索文档覆盖率。

## 四种改写策略

### 信息等同
- **GQR（通用查询改写）**：保留原始查询关键信息，消除噪音
- **KWR（关键词提取改写）**：直接提取关键词提升检索精度

### 信息扩展
- **PAR（伪答案改写）**：整合 LLM 先验知识生成伪答案，扩展查询信息量（贡献最大）

### 信息缩减
- **CCE（核心内容提取）**：当查询含过多细节时提取核心简化查询

## 自适应策略选择

- 轻量级 Prompt + few-shot 实现
- 根据查询特性动态选择改写策略
- 平均改写次数从 4 次减少至约 2.48 次（呈高斯分布）
- 有效减少检索噪声文档

## 实验表现

- FreshQA P@5 比最佳基线提升 14.46%
- HotpotQA P@5 提升约 8%
- AmbigNQ P@5 比 RAG-Fusion 提升约 10%
- PAR 贡献最大（移除后 P@5 平均减少 1.34%）
- 在 Llama3-8B、Qwen2-7B、GPT-4 上均有效

## 与 RAG-Fusion 区别

- RAG-Fusion 多个查询均为同义改写（信息等同）
- DMQR-RAG 从不同信息层面（等同/扩展/缩减）生成多样化改写
- DMQR-RAG 支持自适应动态选择策略

## 关联

- 相关概念：[[概念_Query_Translation_查询改写与翻译]]、[[概念_RAG_Fusion_多查询融合生成]]、[[概念_HyDE_假设文档嵌入]]、[[概念_查询重写]]、[[概念_子查询分解]]
- 来源：[[DMQR-RAG_多样查询改写]]