---
type: concept
tags:
- RAG/retrieval
summary: 重排序（Rerank）是检索后对候选文档按与查询的相关性进行精细排序的环节，传统方式为单塔模型输出相关性 logit 分数。
sources:
- wiki/sources/ES企业AI搜索实践.md
- wiki/sources/Jina_AI创业复盘.md
- wiki/sources/OpenAI_LLM应用最佳实践.md
- wiki/sources/RAG_12痛点与解决方案.md
- wiki/sources/RAG技巧与底层代码剖析.md
- wiki/sources/RAG挑战赛冠军方案.md
- wiki/sources/RAG检索_Retrieval入门到精通.md
- wiki/sources/为什么用Qwen3_embedding和rerank.md
- wiki/sources/优图RAG技术详解.md
- wiki/sources/向量数据库原理与应用全解析.md
- wiki/sources/提升RAG问答质量的技术路线.md
updated: '2026-09-21'
aliases:
- Rerank
- Reranking
- 重排序
- 二次重排
- 概念_重排序Rerank
---

# 概念_Rerank_重排序


## 定义

重排序（Rerank）是检索后对候选文档按与查询的相关性进行精细排序的环节，传统方式为单塔模型输出相关性 logit 分数。

## 传统 Rerank

- 单塔架构：`[CLS] Query [SEP] Document` 拼接后输入模型
- 最后一层 linear 输出相关性 logit 分数
- 两阶段检索中，BM25 或双塔向量模型负责从大规模索引快速召回候选，Cross-Encoder 只对少量候选精排；全量使用 Cross-Encoder 会带来不可接受的线上延迟。

## Qwen3 Reranker 新范式（LLM 化）

- 将排序任务转化为二元分类问题（yes/no）
- 用 system prompt 设定角色，规定答案只能是 yes/no
- 输入采用类聊天模板：
  - System：判断规则
  - User：`<Instruct>` + `<Query>` + `<Document>`
  - Assistant：让模型生成 yes/no 判断
- 评分公式：`score = P("yes") / (P("yes") + P("no"))`，取值 0~1
- 通过"LLM 化"/"对话化"充分释放基础模型的理解和推理能力
- 支持自定义 Instruct，实现细粒度任务控制

## LLM Reranker 与分层蒸馏（优图）

- 传统 Reranker（BERT/RoBERTa，110M~400M，512 token）→ LLM Reranker（8k+ token，理解能力更强）
- 分层知识蒸馏：约束多个 Transformer 层输出一致，支持层级输出能力（详见 [[概念_分层知识蒸馏]]）

## Re-Rank 的三种基本做法

- 基于相似度的排序：余弦相似度、点积等度量
- 基于深度学习的排序模型：BERT/T5 等预训练模型评估文档-查询相关性
- 使用回归模型：将文档特征（长度、相似度、标题等）输入回归模型预测重要性得分

## 关联

- 相关概念：[[概念_检索后处理]]、[[概念_Instruct_Embedding_指令增强向量嵌入]]、[[概念_LLM重排序]]、[[概念_分层知识蒸馏]]、[[概念_RAG_Fusion_多查询融合生成]]
- 实体：[[实体_Qwen3_Embedding]]、[[实体_Cohere_Rerank]]
- 来源：[[为什么用Qwen3_embedding和rerank]]、[[RAG_12痛点与解决方案]]、[[RAG挑战赛冠军方案]]、[[提升RAG问答质量的技术路线]]、[[优图RAG技术详解]]、[[RAG检索_Retrieval入门到精通]]