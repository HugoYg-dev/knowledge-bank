---
type: source
tags:
- RAG/retrieval
summary: 介绍 RAG 基础流程：索引（Indexing）、检索（Retrieval）、生成（Generation）三步骤，使用 LangChain + 向量数据库实现完整管道。
sources:
- raw/articles/RAG从入门到精通系列1：基础RAG.md
updated: '2026-07-01'
---
# RAG基础：索引、检索与生成

> URL：https://mp.weixin.qq.com/s/TlFNOw7_3Q8qywKLpVUmfg
> Cubox 高亮：无

## 摘要

介绍 RAG（Retrieval Augmented Generation）基础流程：Indexing（索引）、Retrieval（检索）、Generation（生成）三步骤。使用 LangChain + Qwen + BAAI Embedding + Qdrant 向量数据库实现完整管道。

## 核心内容

### Indexing（索引）
- 加载外部文档（LangChain 有 160+ 文档加载器）
- 文本表示需转为数值表示（Embedding Vector）
- Embedding Model 的 Context Window 有限（512~8192 token），需将文档切分为 Split
- 对文档块建立索引并存入向量数据库

### Retrieval（检索）
- 根据问题的 Embedding Vector，按相似度（如余弦相似度）找出 k 个相关 Split
- Embedding Vector 存储在 [[概念_向量数据库|Vector Store]] 中

### Generation（生成）
- 将问题 + 检索到的知识片段组成 Prompt 输入 LLM
- LLM 根据有事实依据的知识片段生成回答
- LangChain 将检索和生成链（Chain）在一起

### [[entities/实体_LangSmith|LangSmith]]
- 用于构建生产级 LLM 应用的监控平台
- 可跟踪 LLM 调用和应用逻辑

### Token 说明
- 英文：1 token ≈ 3~4 字母
- 中文：1 token ≈ 1 汉字

## 关联

- 概念：[[概念_RAG基础流程]]、[[概念_Embedding与向量检索]]、[[概念_向量数据库]]
- 实体：[[实体_LangChain]]、[[entities/实体_LangSmith]]、[[实体_Qdrant]]
- 系列下一篇：[[RAG查询翻译_Query_Translation]]

---
> 📎 **物理文献**：[[raw/articles/RAG从入门到精通系列1：基础RAG.md]]