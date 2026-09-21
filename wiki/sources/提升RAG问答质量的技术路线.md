---
type: source
tags:
- RAG/retrieval
summary: RAG 系统问答质量提升技术路线总览：Query Translation（Multi-query/RAG-Fusion/Decomposition/Step-back/HyDE）、Routing（Logical/Semantic）、Query
  Construction、Indexing（Chunk优化/Multi-representation/ColBERT/RAPTOR）、Retrieval & Generation（CRAG/Self-RAG/Adaptive-RAG）
sources:
- raw/articles/探索提升RAG系统问答质量的技术路线.md
updated: '2026-07-01'
---
# 提升RAG问答质量的技术路线

## 摘要

系统梳理 RAG 系统中提升问答质量的关键技术路线，涵盖 Query Translation、Routing、Query Construction、Indexing、Retrieval & Generation 五大模块，各模块内含多种具体方法及其优劣对比。

## [重点/高亮] RAPTOR

用户高亮内容：

> RAPTOR（Recursive Abstractive Processing for Tree-Organized Retrieval）是一种将文档组织成分层结构的索引技术，它能够有效地实现递归式的信息抽象和检索。这种方法以"树"的形式组织文档数据，叶节点代表原始文档或者文档块，树的高层节点则代表这些文档经过抽象后的总结。RAPTOR 的目标是通过分层的方式，提升信息检索的效率，同时能够适应不同粒度的查询需求。

## Query Translation

将用户自然语言查询转换为更适合检索和生成的形式：

- **Multi-query**：生成多个查询扩大检索范围提高召回率
- **RAG-Fusion**：多查询结果通过 RRF 融合（侧重结果整合而非生成多查询）
- **Decomposition**：复杂问题拆解为多个简单子问题分别检索
- **Step-back**：先查询更高层次信息再细化检索
- **HyDE**：根据查询生成假设性文档嵌入用于检索

### Multi-query vs RAG-Fusion 区别
- Multi-query 关注检索层面扩展（生成多查询）
- RAG-Fusion 关注生成层面整合（如何融合多查询结果，使用 RRF 加权排序）

## Routing

智能选择合适的数据源或查询处理方法：

### Logical Routing
- 基于预定义规则/查询结构化特征
- 示例：结构化查询→关系数据库，图关系查询→图数据库

### Semantic Routing
- 基于查询语义与预定义 Prompt/嵌入的相似度
- 查询向量与模板比对，按语义相似度选择处理路径

## Query Construction

自然语言转换为适用于不同数据库的结构化查询：

- **关系型数据库**：自然语言→SQL（含向量搜索如 PGVector）
- **图数据库**：自然语言→Cypher/Gremlin
- **向量数据库**：自动生成元数据过滤条件（category/year 等），提高搜索精度

## Indexing

文档组织优化：

1. **Chunk Optimization（语义切分）**：按语义单元而非固定字符数切分
2. **Multi-representation Indexing**：LLM 总结摘要→嵌入存 Vector Store，原文存 Doc Store，检索摘要返回原文
3. **Specialized Embeddings**：
   - 领域微调嵌入模型
   - ColBERT：token 级嵌入 + MaxSim 细粒度相似度计算
4. **Hierarchical Indexing（RAPTOR）**：树状分层索引，叶节点=原文，高层=递归摘要

## Retrieval & Generation

### Retrieval 核心技术
- **RAG Fusion**：多角度查询 + RRF 融合
- **Re-Rank**：Cross-Encoder/RankGPT 二次排序
- **Hybrid Retrieval**：向量搜索 + BM25 + 知识图谱
- **Active Retrieval**：LLM 评估初步结果，决定是否额外查询

### Generation 核心技术
- **CRAG（Corrective RAG）**：LLM 评估检索文档相关性，不够则触发额外检索
- **Self-RAG（Self-Reflective RAG）**：生成初步答案后自我检查，决定是否需额外检索或调整
- **Adaptive-RAG**：根据查询复杂度自适应选择检索和生成策略

## 关联

- 相关概念：[[概念_Query_Translation_查询改写与翻译]]、[[概念_RAG_Fusion_多查询融合生成]]、[[概念_HyDE_假设文档嵌入]]、[[概念_子查询分解]]、[[概念_Step_Back_回退提示]]、[[概念_RAG_Routing_检索智能路由]]、[[概念_Query_Construction_查询构建]]、[[概念_Multi_Representation_Indexing_多表征索引]]、[[概念_RAPTOR_递归树状检索索引]]、[[概念_ColBERT_多向量延迟交互检索]]、[[概念_混合检索]]、[[概念_Rerank_重排序]]、[[概念_CRAG_纠正性检索增强生成]]、[[概念_Self_RAG_自省式检索增强生成]]、[[概念_Adaptive_RAG_自适应检索增强生成]]、[[概念_RRF_互易秩融合]]、[[概念_语义切分]]
- 实体：[[实体_ColBERT]]
- 相关来源：[[RAG查询翻译_Query_Translation]]、[[RAG路由_Routing]]、[[RAG查询构造_Query_Construction]]、[[RAG索引进阶_Indexing]]

---
> 📎 **物理文献**：[[raw/articles/探索提升RAG系统问答质量的技术路线.md]]