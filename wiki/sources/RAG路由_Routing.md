---
type: source
tags:
- RAG/retrieval
summary: 介绍 RAG 中的 Routing 技术：通过逻辑路由（规则分类）和语义路由（向量相似性）智能选择最合适的检索路径或数据源。
sources:
- raw/articles/RAG从入门到精通系列3：Routing（路由）.md
updated: '2026-07-01'
---
# RAG路由：Routing

> URL：https://mp.weixin.qq.com/s/4IOMT5JaL9flv6dbZjif4g
> Cubox 高亮：无

## 摘要

介绍 RAG 中的 Routing（路由）：根据用户查询内容智能选择最适合的检索路径或推理逻辑。在多数据源、多检索器、多任务场景下尤为重要。分为 Logical Routing 和 Semantic Routing 两类。

## 核心内容

### Logical Routing（逻辑路由）
- 基于明确的规则或分类模型对查询分流（如分到不同数据库、知识库、API）
- 适用于结构化问题或明确数据源场景
- 实现：定义多个数据源（如 python_docs、js_docs、golang_docs）
- 使用 `with_structured_output` 将模型输出格式化为结构化数据（JSON/字典）
- router chain 根据用户问题中的编程语言自动选择数据源

### Semantic Routing（语义路由）
- 基于向量化的语义相似性动态选择最优路径
- 适用于模糊查询或需要灵活响应的场景
- 实现：为不同领域（如物理、数学）编写不同 Prompt
- prompt_router 根据用户问题与每个 Prompt 的语义相似度（余弦相似度）选择合适 Prompt

## 关联

- 概念：[[概念_RAG_Routing_检索智能路由]]
- 实体：[[实体_LangChain]]
- 系列上一篇：[[RAG查询翻译_Query_Translation]]
- 系列下一篇：[[RAG查询构造_Query_Construction]]

---
> 📎 **物理文献**：[[raw/articles/RAG从入门到精通系列3：Routing（路由）.md]]