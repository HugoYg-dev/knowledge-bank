---
type: source
tags:
- RAG/retrieval
summary: Re-Rank：对检索到的候选文档进行重新排序，提高生成答案的相关性和精确度
sources:
- raw/articles/RAG从入门到精通系列6：Retrieval（检索）.md
updated: '2026-07-01'
---
# RAG检索_Retrieval入门到精通

## 来源信息

- **标题**：RAG检索_Retrieval入门到精通
- **作者**：南七无名式 / PyTorch研习社
- **发布时间**：2025-02-05
- **URL**：https://mp.weixin.qq.com/s?__biz=MzI2ODUyMTQyNA==&mid=2247495615&idx=1&sn=022d4b59324ae486b7b65b280b74eb80


> RAG从入门到精通系列6，主题为 Retrieval（检索）中的 Ranking 与 Refinement 两大优化方向。

## 主要内容

### Ranking（重排序）

- Re-Rank：对检索到的候选文档进行重新排序，提高生成答案的相关性和精确度
- 三种主要方法：
  1. 基于相似度的排序：余弦相似度、点积等度量
  2. 基于深度学习的排序模型：BERT/T5 等预训练模型评估文档-查询相关性
  3. 使用回归模型：文档特征（长度、相似度、标题等）输入回归模型预测重要性得分
- RAG Fusion：生成多个用户查询检索多篇文档，利用 [[概念_RRF_互易秩融合|RRF]] 对检索结果重新排名

### Refinement（检索细化）

#### CRAG（Corrective RAG）

- 自我反思/自我评分机制应用于检索到的文档
- 三种情况处理：
  - 文档正确 → 知识细化，去除无关部分
  - 文档模棱两可 → 知识细化 + 网络搜索
  - 文档不正确 → 进行网络搜索
- 论文：https://arxiv.org/pdf/2401.15884
- 实现：Qwen + BAAI + LangChain + LangGraph + Qdrant

#### Self-RAG（Self-Reflective RAG）

- 结合自我反思/自我评估的 RAG 策略
- 引入额外"自我检查"步骤，评估和改进检索与生成结果
- 论文：https://arxiv.org/abs/2310.11511
- 实现：LangGraph 工作流

## 实现代码

- GitHub: https://github.com/realyinchen/RAG/blob/main/06_Retrieval.ipynb

## 关联

- 相关概念：[[概念_Rerank_重排序]]、[[概念_CRAG_纠正性检索增强生成]]、[[概念_Self_RAG_自省式检索增强生成]]、[[概念_RAG_Fusion_多查询融合生成]]、[[概念_RRF_互易秩融合]]
- 系列前篇：[[RAG查询翻译_Query_Translation]]、[[RAG路由_Routing]]、[[RAG查询构造_Query_Construction]]、[[RAG索引进阶_Indexing]]
- 实体：[[实体_LangChain]]、[[实体_Qdrant]]

---
> 📎 **物理文献**：[[raw/articles/RAG从入门到精通系列6：Retrieval（检索）.md]]