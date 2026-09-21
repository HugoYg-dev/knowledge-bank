---
type: source
tags:
- RAG/retrieval
summary: 刘晓国（Elastic 中国社区首席布道师）QCon 演讲：基于 Elasticsearch 构建企业 AI 搜索应用，涵盖稠密/稀疏向量、混合检索
  RRF、量化、HNSW+GPU 加速、Serverless 架构与 Agentic RAG 落地实践
sources:
- raw/articles/基于 Elasticsearch 创建企业 AI 搜索应用实践.md
updated: '2026-07-01'
---
# ES企业AI搜索实践

## 摘要

刘晓国（Elastic 中国社区首席布道师）在 QCon 的演讲，介绍如何基于 [[实体_Elasticsearch|Elasticsearch]] 构建企业级 AI 搜索应用，涵盖稠密/稀疏向量、混合检索、重排序、量化、HNSW+GPU 加速、Serverless 架构以及 RAG/Agentic RAG 落地实践。

## 核心内容

### 向量类型：Dense vs Sparse

- ES 同时支持 **Dense Vector（稠密向量）** 与 **Sparse Vector（稀疏向量）**。
- **Dense**：低维（如 OpenAI 1536 维），捕捉语义，支持多模态；缺点是占内存、可解释性差。
- **Sparse**：大部分元素为零，无需微调即可跨行业使用。

### 架构流程

- 用 **Eland** 工具将模型上传到 ES 的 ML 节点。
- 创建 **Inference API**。
- 数据入库（ingest）时自动向量化。
- 查询时执行 **kNN search**。

### 混合检索（Hybrid Search）

- 结合传统 [[概念_BM25_最佳匹配25算法|BM25]] + 稀疏向量 + 稠密向量。
- 当数据特征未知时，使用 **RRF（Reciprocal Rank Fusion，倒数排名融合）** 做多路召回融合。
- 当数据被充分理解时，使用加权线性组合（weighted linear combination）。

### kNN 相似度阈值

- 可设置最小相似度阈值，避免返回不相关结果。

### 重排序（Reranking）

- learning to rank（基于用户标注的训练数据）。
- 通过第三方服务做多级重排序（multi-level re-ranking）。

### 切分策略（Chunking）

- 文本切分为带重叠（overlapping）的 chunk，提升语义精度。
- semantic text field 简化使用。

### 量化（Quantization）

- float32 → int8（内存降至 25%）、INT4、BBQ（Better Bit Quantization，源自南洋理工 NTU 论文的 1-bit 量化）。
- 索引速度提升 20~30 倍，查询速度提升 5~6 倍。

### 加速

- HNSW + GPU 加速的 CUDA ANN Graph search。
- Java SIMD 硬件加速。

### Serverless 架构

- 数据存储在对象存储（object storage）而非本地磁盘。
- 通过存算分离（storage-compute separation）降低成本。

### RAG 应用

- 流程：多路召回 → 重排序 → LLM 生成。
- 混合检索消除幻觉（eliminate hallucination）。
- Agentic RAG：通过工具调用实现日期过滤等能力。
- [[概念_HyDE_假设文档嵌入|HyDE]] 用于提升召回。
- 关键短语 + 实体抽取 + 潜在问题生成，用于丰富索引内容。

## 关联

- 相关概念：[[概念_向量数据库]]、[[概念_混合检索]]、[[概念_Agentic_RAG_智能体检索增强生成]]、[[概念_向量量化]]、[[概念_Embedding与向量检索]]、[[概念_BM25_最佳匹配25算法]]、[[概念_RRF_互易秩融合]]、[[概念_Sparse_Embedding_稀疏向量嵌入]]、[[概念_Dense_Embedding_稠密向量嵌入]]、[[概念_Quantized_Embedding_量化向量嵌入]]、[[概念_Rerank_重排序]]、[[概念_HyDE_假设文档嵌入]]、[[概念_Chunk_Size_分块大小与重叠]]、[[概念_RAG_Fusion_多查询融合生成]]、[[概念_问题生成检索增强]]
- 实体：[[实体_Elasticsearch]]、[[实体_HNSW]]
- 相关来源：[[向量数据库原理与应用全解析]]、[[从BM25到Multi-Vector_6种Embedding演进路线]]

---
> 📎 **物理文献**：[[raw/articles/基于 Elasticsearch 创建企业 AI 搜索应用实践.md]]