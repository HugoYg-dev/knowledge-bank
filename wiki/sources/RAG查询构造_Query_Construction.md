---
type: source
tags:
- RAG/retrieval
- RAG/query
summary: 介绍 RAG 中 Query Construction 技术：将自然语言查询转换为结构化查询语句，结合元数据过滤提升检索准确性。
sources:
- raw/articles/RAG从入门到精通系列4：Query Construction（查询构造）.md
updated: '2026-07-01'
---
# RAG查询构造：Query Construction

> URL：https://mp.weixin.qq.com/s/qG02XjSV9nuRIonGy_VOwQ
> Cubox 高亮：无

## 摘要

介绍 RAG 中的 Query Construction（查询构造）：根据用户自然语言问题，通过语义解析、上下文理解及路由结果，生成特定领域数据源所需的查询语句或格式化内容，目标是最大化检索的准确性和相关性。

## 核心内容

### 核心思想
- 许多 Vector Store 都有 meta data（元数据）
- 将自然语言查询（如 "Videos on chat langchain published after 2024"）转成可用于元数据过滤的结构化查询

### 实现流程（示例）
- 构造带元数据的 Document 对象
- 建立索引：对 content/title 做非结构化搜索；对 view count、publication date、length 做范围过滤
- 为结构化搜索查询定义一个架构（schema）
- 编写 Prompt 让 LLM 将自然语言转成合适的结构化查询

## 关联

- 概念：[[概念_Query_Construction_查询构建]]
- 实体：[[实体_LangChain]]
- 系列上一篇：[[RAG路由_Routing]]
- 系列下一篇：[[RAG索引进阶_Indexing]]

---
> 📎 **物理文献**：[[raw/articles/RAG从入门到精通系列4：Query Construction（查询构造）.md]]