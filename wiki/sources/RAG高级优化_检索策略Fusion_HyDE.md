---
type: source
tags:
- RAG/retrieval
summary: 介绍 Fusion Retrieval、HyDE、RAG-Fusion 三种检索优化方法，结合可创建更健壮准确的检索系统，并给出实现代码。
sources:
- raw/articles/RAG高级优化：检索策略探讨Fusion, HyDE安排上(含代码).md
updated: '2026-07-01'
url: https://mp.weixin.qq.com/s?__biz=Mzk0NTcyNTMzNw==&mid=2247484218&idx=1&sn=656549e48f411b94ebe72ecd61259324
---
# RAG高级优化：检索策略探讨 Fusion, HyDE（含代码）

## 摘要

传统检索方法依赖语义理解（向量）或关键字匹配（BM25），各有优缺点。本文介绍三种检索优化方法，结合可创建更健壮准确的检索系统：Fusion Retrieval、HyDE、RAG-Fusion，并给出实现代码。

## 核心内容

### Fusion Retrieval（融合检索）

结合语义理解（向量）和关键字匹配（BM25）的优势。

**实现方法：**
1. 接受查询，分别执行向量检索和 BM25 检索
2. 两种方法的得分归一化到共同尺度
3. 计算加权组合（由 alpha 参数控制）
4. 按综合得分排名，返回前 k 个结果

**优点：**
- **提高检索质量**：同时捕获概念相似度和精确关键字匹配
- **灵活性**：alpha 参数调整向量与关键字搜索之间的平衡
- **健壮性**：组合方法减轻单个方法的弱点
- **可定制性**：易适配不同向量存储或关键字检索方法

**关键代码：**
- `create_bm25_index()` 用 `rank_bm25` 库的 BM25Okapi 建索引（按空白分词）
- `fusion_retrieval(vectorstore, bm25, query, k, alpha)`：
  - 向量得分与 BM25 得分各自 min-max 归一化
  - `combined_scores = alpha * vector_scores + (1-alpha) * bm25_scores`
  - 按综合得分排序返回 top k

### HyDE（假设文档嵌入）

增强密集检索，尤其适用于零样本场景：
1. **查询扩展**：LLM 根据用户查询生成假设答案或文档
2. **增强嵌入**：嵌入假设文档，创建更丰富的语义搜索空间
3. **相似性搜索**：用嵌入查找数据库中最相关的实际文档
4. **知情生成**：检索文档 + 原始查询生成最终响应

### RAG-Fusion

将 RAG 与互易秩融合（RRF）相结合：
1. **查询扩展**：利用原始查询生成多个相关查询，提供不同视角
2. **多次检索**：每个生成查询都用于检索文档
3. **倒数秩融合**：用 RRF 算法对检索文档重新排序，结合多次检索的排名
4. **增强 RAG**：重排序文档 + 原始/生成查询生成最终响应

[重点/高亮] 倒数秩融合：使用 RRF 算法对检索到的文档重新排序，结合多次检索尝试的排名。

**RRF 实现（Cubox 高亮附带代码）：**
```python
def rrf_fusion(rankings, k=60):
    scores = defaultdict(float)
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking):
            scores[doc_id] += 1 / (k + rank + 1)
    return sorted(scores.keys(), key=lambda d: scores[d], reverse=True)
```
平滑常数 k 默认 60。

## 关联

- 概念：[[概念_Fusion_Retrieval]]、[[概念_HyDE]]、[[概念_RAG_Fusion]]、[[概念_BM25]]、[[概念_Reciprocal_Rank_Fusion]]
- 实体：`rank_bm25`、[[实体_LangChain]]
- 同系列：[[RAG高级优化_query转换之路]]、[[RAG高级优化_问题生成检索增强]]、[[RAG高级优化_检索后处理]]

---
> 📎 **物理文献**：[[raw/articles/RAG高级优化：检索策略探讨Fusion, HyDE安排上(含代码).md]]