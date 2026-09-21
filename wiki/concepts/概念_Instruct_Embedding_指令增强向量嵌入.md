---
type: concept
tags:
- RAG/embedding
- RAG/retrieval
summary: Instruct Embedding 是一种在编码查询时附带任务指令（instruct）的嵌入方式，通过指令引导模型理解查询意图，使同一模型能适应不同检索/匹配任务。
sources:
- wiki/sources/为什么用Qwen3_embedding和rerank.md
updated: '2026-09-21'
aliases:
- Instruct Embedding
- 指令嵌入
- 指令向量
- 概念_Instruct_Embedding
---

# 概念_Instruct_Embedding_指令增强向量嵌入


## 定义

Instruct Embedding 是一种在编码查询时附带任务指令（instruct）的嵌入方式，通过指令引导模型理解查询意图，使同一模型能适应不同检索/匹配任务。

## 工作机制

- 查询连同 instruct 一起进入问题塔 encoder
- 默认 instruct（如 Qwen3）：`Given a web search query, retrieve relevant passages that answer the query`
- 用户可根据具体任务自定义 instruct，实现多维度检索

## 使用方式（Sentence Transformers）

```python
query_embeddings = model.encode(queries, prompt_name="query")
```

- `prompt_name="query"` 背后等价于传入默认检索 instruct
- 可自定义 instruct 替换默认值

## 应用示例

- **FAQ 问题→问题匹配**：`For the given user question, find the most similar question from the FAQ list`
- **主题推荐**：`Find other articles with a similar topic`
- **风格推荐**：`Find other documents written in a similar narrative style`
- **代码功能搜索**：`Find code snippets that perform a similar function`
- **细粒度情感分析**：`From the product reviews, retrieve passages that express a negative sentiment about battery life`

## 意义

- 同一套文档向量，通过查询时动态传入不同指令实现多维度检索
- 是 LLM 时代 embedding 的新范式，但现有大部分 RAG 系统暂不支持

## 关联

- 相关概念：[[概念_Embedding与向量检索]]、[[概念_Sentence_BERT_孪生网络句向量]]、[[概念_Rerank_重排序]]
- 实体：[[实体_Qwen3_Embedding]]
- 来源：[[为什么用Qwen3_embedding和rerank]]