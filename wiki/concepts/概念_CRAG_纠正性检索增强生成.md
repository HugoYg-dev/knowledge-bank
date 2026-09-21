---
type: concept
tags:
- RAG/retrieval
summary: CRAG（Corrective RAG，纠正型 RAG）是一种让 LLM 评估检索到的文档是否与查询相关，并根据需要触发额外检索来补充数据的 RAG
  生成策略。
sources:
- wiki/sources/LLM_32种消除幻觉技术综述.md
- wiki/sources/RAG检索_Retrieval入门到精通.md
- wiki/sources/提升RAG问答质量的技术路线.md
updated: '2026-09-21'
aliases:
- CRAG
- Corrective RAG
- 纠正性RAG
- 纠正性检索增强生成
- 概念_CRAG
---

# 概念_CRAG_纠正性检索增强生成


## 定义

CRAG（Corrective RAG，纠正型 RAG）是一种让 LLM 评估检索到的文档是否与查询相关，并根据需要触发额外检索来补充数据的 RAG 生成策略。

## 工作原理

- LLM 对检索到的文档进行相关性评估（自我反思/自我评分机制）
- 三种情况处理：
  - 文档正确 → 知识细化，去除与用户查询无关的部分
  - 文档模棱两可 → 知识细化 + 网络搜索补充
  - 文档不正确 → 进行网络搜索获取相关知识
- 最终基于质量更高的上下文生成答案
- 论文：https://arxiv.org/pdf/2401.15884

## 优势

- 减少错误答案，提高答案质量
- 适用于法律、医学、金融等需要答案符合行业标准的领域

## 实现参考

- Qwen + BAAI + LangChain + LangGraph + Qdrant 实现简单 CRAG

## 关联

- 相关概念：[[概念_Self_RAG_自省式检索增强生成]]、[[概念_Adaptive_RAG_自适应检索增强生成]]、[[概念_RAG基础流程]]、[[概念_Rerank_重排序]]
- 来源：[[提升RAG问答质量的技术路线]]、[[RAG检索_Retrieval入门到精通]]

> 注：本页 confidence 为 medium，全文仅概要介绍未展开算法细节。