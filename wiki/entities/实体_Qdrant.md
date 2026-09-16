---
type: entity
tags:
- RAG/retrieval
- Infra/storage
summary: 使用 Rust 编写的高性能开源向量数据库，原生支持强大的 Payload 标量过滤，单机与中等规模集群性能极其强悍。
sources:
- wiki/sources/2026程序员必读的向量数据库原理与选型指南.md
- wiki/sources/RAG基础_索引检索生成.md
- wiki/sources/RAG检索_Retrieval入门到精通.md
- wiki/sources/向量数据库原理与应用全解析.md
updated: '2026-07-22'
---

## 简介

**Qdrant** 是使用 Rust 语言编写的高性能开源向量数据库与语义搜索引擎。凭借优秀的 Rust 内存管理、优雅的 API 交互以及原生的 Payload（标量属性）过滤能力，在现代 AI 选型中异军突起。

## 核心特性与优势

- **高性能 Rust 底层**：单机与中等集群性能极其强悍，部署轻量，无需复杂的依赖关系。
- **原生 Payload 过滤**：原生支持向量与关联标量数据的[[concepts/概念_标量过滤|标量过滤]]，混合检索体验优雅。
- **基于 HNSW**：核心采用优化过的 [[entities/实体_HNSW|HNSW]] 图索引。

## 适用场景与选型

- **适用场景**：中大型 RAG 项目的首选组件（数据量在百万到亿级），适合追求极致性能与优雅 API 的开发团队。

## 关联

- 相关概念：[[concepts/概念_向量数据库]]、[[concepts/概念_Embedding与向量检索]]、[[concepts/概念_标量过滤]]
- 实体：[[entities/实体_HNSW]]
- 来源：[[2026程序员必读的向量数据库原理与选型指南]]、[[RAG基础_索引检索生成]]

