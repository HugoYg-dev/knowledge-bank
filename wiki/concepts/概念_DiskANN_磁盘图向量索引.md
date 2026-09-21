---
type: concept
tags:
- RAG/embedding
- RAG/retrieval
summary: 微软开源的基于 SSD 磁盘的高性能近似最近邻 (ANN) 检索算法，突破内存容量限制，实现十亿级向量检索。
sources:
- wiki/sources/2026程序员必读的向量数据库原理与选型指南.md
updated: '2026-09-21'
aliases:
- DiskANN
- 磁盘图索引
- 磁盘近似最近邻
- 概念_DiskANN
---

# 概念_DiskANN_磁盘图向量索引

## 定义

**DiskANN** 是由微软研究院（Microsoft Research）提出并开源的基于 SSD 磁盘的高性能[[concepts/概念_近似最近邻搜索|近似最近邻 (ANN) 检索算法]]。

## 核心技术突破

- **突破内存瓶颈**：传统 [[entities/实体_HNSW|HNSW]] 等图索引算法要求全量图结构与向量存放在内存中，当向量达到十亿级（Billion-scale）时内存成本不可承受。
- **磁盘+内存混合图**：DiskANN 将绝大部分图结构与压缩向量压缩存放于普通的 NVMe SSD 磁盘上，仅在内存中保留少量压缩导引节点。
- **高 QPS 与高召回**：通过优化磁盘 I/O 读取路径，在单机普通 SSD 上实现了高 QPS 和高召回率的十亿级向量检索。

## 工业界落地

- [[entities/实体_Milvus|Milvus]] 等主流向量数据库均集成了 DiskANN 算法（如 Knowhere 引擎中的 DiskANN 实现），用于大规模海量向量存储。

## 关联

- 相关概念：[[concepts/概念_向量数据库]]、[[concepts/概念_近似最近邻搜索]]、[[concepts/概念_向量索引方法]]
- 实体：[[entities/实体_Milvus]]、[[entities/实体_HNSW]]
- 来源：[[2026程序员必读的向量数据库原理与选型指南]]