---
type: entity
tags:
- RAG/embedding
- Infra/storage
summary: 开源云原生分布式向量数据库，采用存算分离架构，支持十亿级海量向量数据检索。
sources:
- wiki/sources/2026程序员必读的向量数据库原理与选型指南.md
- wiki/sources/向量数据库原理与应用全解析.md
updated: '2026-07-22'
---

# 实体：Milvus

## 简介

**Milvus** 是一款开源的云原生分布式向量数据库，专为海量高维向量数据的存储与相似度检索设计。采用存储与计算分离的现代云原生架构（依赖 etcd、MinIO、Kafka/Pulsar 等组件）。

## 核心特性与优势

- **索引丰富**：支持最多的向量索引类型，包括 [[entities/实体_HNSW|HNSW]]、[[concepts/概念_IVF倒排索引|IVF]]、[[concepts/概念_DiskANN|DiskANN]]、PQ 等。
- **海量扩展**：横向扩展能力极强，轻松支持千万级至十亿级（Billion-scale）数据规模。
- **混合查询**：支持高效的标量属性过滤与向量检索结合。
- **生态完善**：提供 PyMilvus SDK，与 LangChain、LlamaIndex 等 AI 框架无缝适配。

## 选型考量

- **适用场景**：大厂生产环境、十亿级海量向量检索、具备专职 DBA/运维团队。
- **局限性**：架构较重，小团队自建运维复杂度与资源开销较高。

## 关联

- 相关概念：[[concepts/概念_向量数据库]]、[[concepts/概念_DiskANN]]、[[concepts/概念_IVF倒排索引]]、[[concepts/概念_标量过滤]]
- 来源：[[2026程序员必读的向量数据库原理与选型指南]]、[[向量数据库原理与应用全解析]]
