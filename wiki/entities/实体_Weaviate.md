---
type: entity
tags:
- RAG/retrieval
- Infra/storage
summary: 开源一体化/平台化向量搜索引擎，基于 HNSW 索引与 GraphQL 查询接口。
sources:
- wiki/sources/2026程序员必读的向量数据库原理与选型指南.md
updated: '2026-07-22'
---

# 实体：Weaviate

## 简介

**Weaviate** 是一款开源的一体化向量搜索引擎，支持存储向量与数据对象，并支持通过 GraphQL 和 RESTful API 进行混合查询。

## 核心特性

- **一体化架构**：集成了内置向量化模块（Modules），可直接连接 OpenAI、Hugging Face 等 Embedding 服务。
- **GraphQL 支持**：提供面向对象的图与向量联合查询能力。

## 适用场景

- **适用场景**：偏好平台化、一体化开箱即用方案的团队（百万到千万级数据）。

## 关联

- 相关概念：[[concepts/概念_向量数据库]]
- 来源：[[2026程序员必读的向量数据库原理与选型指南]]
