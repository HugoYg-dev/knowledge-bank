---
type: concept
tags:
- RAG/retrieval
- RAG/chunking
summary: RAPTOR（Recursive Abstractive Processing for Tree-Organized Retrieval）是一种将文档组织成分层结构的索引技术，以"树"形式组织数据，叶节点代表原始文档或文档块，高层节点代表文档经过抽象后的总结。通过分层方式提升检索效率，适应不同粒度的...
sources:
- wiki/sources/RAG索引进阶_Indexing.md
- wiki/sources/优图RAG技术详解.md
- wiki/sources/提升RAG问答质量的技术路线.md
- wiki/sources/斯坦福RAG新基线_DOS_RAG.md
updated: '2026-09-21'
aliases:
- RAPTOR
- 递归树状检索
- RAPTOR索引
- 概念_RAPTOR索引
---

# 概念_RAPTOR_递归树状检索索引


## 定义

RAPTOR（Recursive Abstractive Processing for Tree-Organized Retrieval）是一种将文档组织成分层结构的索引技术，以"树"形式组织数据，叶节点代表原始文档或文档块，高层节点代表文档经过抽象后的总结。通过分层方式提升检索效率，适应不同粒度的查询需求。

## 构建流程

1. **叶节点初始化**：输入可以是文本块、完整文档、句子或短语
2. **嵌入与聚类**：生成嵌入向量，根据相似性聚类（K-means 或层次聚类）
3. **聚类摘要**：对每个聚类进行整合总结（可用 LLM）
4. **递归构建**：摘要作为新输入重复上述步骤，直到生成顶层全局摘要

## 建索引树的技术

### 高斯混合模型（GMM）
- 基于概率的聚类算法，拟合多维高斯分布
- 通过 BIC（贝叶斯信息准则）自动选择最佳聚类数量
- 数据点归属基于概率而非确定

### UMAP 降维
- 将高维嵌入（如 768 维）降到低维空间（如 10 维）
- 保留局部和全局结构
- 提高聚类效率

### 多尺度聚类
- **局部聚类**：捕获细节精确模式
- **全局聚类**：形成高层抽象总结

### 阈值处理
- 设定概率阈值判断数据点归属
- 允许多重归属：边界点同时归属多个簇，信息不丢失

## 优点

- 高效层次化信息检索（概览到细节）
- 灵活扩展性（段落到文档到集合）
- 适配长上下文 LLM

## 关联

- 相关概念：[[概念_Multi_Representation_Indexing_多表征索引]]、[[概念_ColBERT_多向量延迟交互检索]]、[[概念_RAG基础流程]]、[[概念_DOS_RAG_动态操作空间检索]]、[[概念_Graph_RAG_知识图谱增强检索]]
- 来源：[[RAG索引进阶_Indexing]]、[[提升RAG问答质量的技术路线]]、[[斯坦福RAG新基线_DOS_RAG]]、[[优图RAG技术详解]]