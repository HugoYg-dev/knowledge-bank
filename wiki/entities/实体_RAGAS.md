---
type: entity
tags:
- RAG/eval
summary: 专为检索增强生成（RAG）系统设计的自动化多维量化评估指标框架。
sources:
- wiki/sources/Agent Loop使用语义早停比max_iterations硬截断节省38% Token 且质量不降.md
- wiki/sources/OpenAI_LLM应用最佳实践.md
- wiki/sources/RAGAS评估RAG系统.md
- wiki/sources/Agent时代，RAG怎么选？这份指南一次讲清！.md
updated: '2026-09-25'
---

## 简介

RAGAS 是专为 RAG（检索增强生成）系统设计的开源评估框架，提供多维度指标全面衡量 RAG 系统在检索和生成方面的表现，弥补传统指标（BLEU/ROUGE）的不足。

## 核心指标

- 上下文召回率（Context Recall）
- 上下文精确度（Context Precision）
- 上下文实体召回率（Context Entity Recall）
- 答案相似度（Answer Similarity）
- 回答相关性（Answer Relevance）
- 忠实性（Faithfulness）
- 答案正确性（Answer Correctness）
- 噪声敏感度（Noise Sensitivity）

## 技术特点

- 使用 LLM 辅助评估（提取关键点/反推问题）
- 使用 embedding 模型计算语义相似度
- 支持有标注和无标注两类指标
- Python 包：`pip install ragas`

## 关联

- 相关概念：[[概念_RAGAS_RAG评估框架]]、[[concepts/概念_Modular_RAG_模块化检索增强生成]]
- 来源：[[RAGAS评估RAG系统]]、[[OpenAI_LLM应用最佳实践]]、[[wiki/sources/Agent时代，RAG怎么选？这份指南一次讲清！.md]]
