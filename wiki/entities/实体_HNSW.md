---
type: entity
tags:
- RAG/retrieval
summary: 当前业界主流的基于分层导航图结构的近似最近邻搜索（ANN）算法。
sources:
- wiki/sources/2026程序员必读的向量数据库原理与选型指南.md
- wiki/sources/ES企业AI搜索实践.md
- wiki/sources/RAG挑战赛冠军方案.md
- wiki/sources/RAG系统设计_语义搜索与KG驱动选型.md
- wiki/sources/向量数据库原理与应用全解析.md
- wiki/sources/美团搜索查询改写实践.md
updated: '2026-07-01'
---
## 简介

HNSW（Hierarchical Navigable Small World）是当前业界最先进的基于图的近似最近邻搜索算法，被主流向量数据库广泛采用。

## 技术原理

- 构建多层图结构：高层节点数量少且连接长距离"跳跃"边，低层节点连接局部邻居
- 查询时从最高层入口点出发，逐层贪心跳转到更接近查询向量的节点，最终在底层找到最近邻
- 实现粗定位→精搜的分层策略

## 性能

- 毫秒级速度提供优异召回效果，大幅优于暴力搜索
- Elasticsearch 使用 HNSW 作为向量搜索默认算法，并支持 GPU 加速的 CUDA ANN Graph

## 局限

- 索引构建相对复杂
- 内存占用较大
- 动态更新（如删除向量）时需维护图结构，操作难度较高

## 关联

- 相关概念：[[概念_向量索引方法]]、[[概念_近似最近邻搜索]]、[[概念_向量数据库]]
- 实体：[[实体_Elasticsearch]]、[[实体_Faiss]]、[[实体_Qdrant]]
- 来源：[[向量数据库原理与应用全解析]]、[[ES企业AI搜索实践]]
