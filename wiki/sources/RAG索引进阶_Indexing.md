---
type: source
tags:
- RAG/retrieval
- RAG/chunking
summary: 介绍 RAG 进阶索引技术：Multi-representation（命题索引）、RAPTOR（树状分层检索）和 ColBERT（token 级细粒度嵌入）三种方法。
sources:
- raw/articles/RAG从入门到精通系列5：Indexing（索引）.md
updated: '2026-07-01'
---
# RAG索引进阶：Indexing

> URL：https://mp.weixin.qq.com/s?__biz=MzI2ODUyMTQyNA==&mid=2247495567&idx=1&sn=3c2f6d114a792093f28e8a2b95851de6
> Cubox 高亮：3 处（见下方 [重点/高亮]）

## [重点/高亮]

1. **Multi-representation indexing**：通过结合多种表示（文档摘要、块或完整内容），在检索和生成过程中取得最佳效果。使用不同层次和粒度的表示弥补单一表示的不足。
2. **RAPTOR 定义**：将文档组织成分层结构的索引技术，以"树"形式组织数据，叶节点为原始文档/块，高层节点为抽象总结，通过分层方式提升检索效率并适应不同粒度查询。
3. **ColBERT**：基于细粒度的 token 级嵌入相似性计算（Contextualized Late Interaction over BERT）。

## 摘要

介绍 RAG 进阶 Indexing 技术：许多方法侧重于将文档拆分为块，但块大小和数量是容易出错的参数。本文介绍 Multi-representation、RAPTOR、ColBERT 三种进阶索引方法。

## 核心内容

### Multi-representation
- 结合多种表示（摘要、块、完整内容）取得最佳检索效果
- **Proposition Indexing**：用 LLM 对原始文本生成摘要 → 嵌入摘要存入 Vector Store + 原始文本存入 Doc Store → 检索时匹配摘要返回原始文本
- 对长上下文 LLM 更友好
- 摘要与原始文档通过 doc_id 关联

### RAPTOR（Recursive Abstractive Processing for Tree-Organized Retrieval）
- 将文档组织为树状分层结构
- 流程：叶节点初始化 → 嵌入与聚类 → 聚类摘要 → 递归构建树状结构
- 聚类方法：高斯混合模型（GMM）+ UMAP 降维 + 多尺度聚类
- **GMM**：基于概率的聚类，通过 BIC 自动选择最佳聚类数量
- **UMAP**：高维嵌入降维（如 768 维 → 10 维），保留局部和全局结构
- **多尺度聚类**：局部聚类捕获细节 + 全局聚类形成高层抽象
- **阈值处理**：允许数据点多重归属，模糊点不被过早剔除
- 优点：高效层次化检索、灵活扩展性、适配长上下文 LLM

### ColBERT（Contextualized Late Interaction over BERT）
- 基于 token 级嵌入相似性，而非整篇文档/块级别
- 步骤：Token 级别相似度计算 → MaxSim 最大池化操作 → 选择最相关文档
- 优势：关注细粒度匹配、兼顾上下文信息、处理词法变体/同义词的鲁棒性

## 关联

- 概念：[[概念_Multi_Representation_Indexing_多表征索引]]、[[概念_RAPTOR_递归树状检索索引]]、[[概念_ColBERT_多向量延迟交互检索]]
- 实体：[[实体_LangChain]]、[[实体_ColBERT]]
- 系列上一篇：[[RAG查询构造_Query_Construction]]

---
> 📎 **物理文献**：[[raw/articles/RAG从入门到精通系列5：Indexing（索引）.md]]