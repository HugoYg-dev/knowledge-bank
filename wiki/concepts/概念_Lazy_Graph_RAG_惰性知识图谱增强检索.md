---
type: concept
tags:
- RAG/retrieval
summary: Lazy Graph RAG 是微软研究人员提出的方法，核心思想是利用语义搜索来弥补知识图谱的不足，将知识图谱和语义搜索结合（二者并非互斥而是可共存）。
sources:
- wiki/sources/RAG系统设计_语义搜索与KG驱动选型.md
updated: '2026-09-21'
aliases:
- Lazy Graph RAG
- Lazy GraphRAG
- 惰性图RAG
- 概念_Lazy_Graph_RAG
---

# 概念_Lazy_Graph_RAG_惰性知识图谱增强检索


## 定义

Lazy Graph RAG 是微软研究人员提出的方法，核心思想是利用语义搜索来弥补知识图谱的不足，将知识图谱和语义搜索结合（二者并非互斥而是可共存）。

## 动机

- KG-RAG 理论强大但成本约为简单向量 RAG 的 1000 倍，"叫好不叫座"
- 语义搜索像"狙击枪"，直接找到最相关的几个结果
- 知识图谱像"breadth-first search"，从切入点找到所有相关信息

## 效果

- 显著降低索引构建成本，降至与简单向量 RAG 相当的水平（约为上一代产品的 0.1%）
- 低成本使系统可灵活扩展到大规模应用

## 关联

- 相关概念：[[概念_Graph_RAG_知识图谱增强检索]]、[[概念_Graph_RAG_知识图谱增强检索]]、[[概念_Semantic_Search本质]]
- 来源：[[RAG系统设计_语义搜索与KG驱动选型]]

> 注：本页 confidence 为 medium，全文仅介绍核心思想与成本数据，未展开算法细节。