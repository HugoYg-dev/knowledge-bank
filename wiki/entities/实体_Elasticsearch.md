---
type: entity
tags:
- RAG/retrieval
- Infra/storage
summary: 广泛应用的全文分布式搜索引擎，原生支持向量字段与近邻搜索，用于构建混合检索。
sources:
- wiki/sources/2026程序员必读的向量数据库原理与选型指南.md
- wiki/sources/ES企业AI搜索实践.md
- wiki/sources/Jina_AI创业复盘.md
- wiki/sources/跨模态知识联邦与统一语义推理RAG.md
updated: '2026-07-22'
---

## 简介

Elasticsearch 是强大的搜索引擎技术，广泛应用于各类应用的搜索功能。除传统全文搜索外，原生支持向量搜索（向量字段内置而非插件实现），可用于构建 RAG 应用。由 Elastic 公司开发。

## 向量搜索能力

- 支持密集向量（Dense Vector，如 OpenAI 1536 维）和稀疏向量（Sparse Vector）
- 最高支持 4096 维向量
- 架构：Eland 工具上传模型到 ML 节点 → 创建 Inference API → 写入时自动向量化 → kNN 搜索
- 稀疏向量无需微调即可开箱即用，跨行业适用

## 混合搜索与优化

- 三路召回：密集向量 + 稀疏向量 + BM25，通过 RRF 或加权方式综合（见 [[概念_混合检索]]）
- kNN 相似度阈值过滤
- 学习排序（learning to rank）、多级重排序（可接第三方如 Hugging Face）
- 量化：float32→int8（内存 25%）、INT4、BBQ（1 位，南洋理工论文，ES 全球唯一实现）
- HNSW + GPU 加速 CUDA ANN Graph 搜索；Java SIMD 硬件加速
- Serverless 架构：数据存对象存储，存算分离降成本
- ESQL（类 SQL 查询语言）、semantic text 语义文本字段

## 关联

- 相关概念：[[概念_混合检索]]、[[概念_向量量化]]、[[概念_向量索引方法]]、[[概念_Reciprocal_Rank_Fusion]]、[[概念_Agentic_RAG]]、[[概念_HyDE]]
- 实体：[[实体_HNSW]]、[[实体_CLIP]]
- 来源：[[ES企业AI搜索实践]]
