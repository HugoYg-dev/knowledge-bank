---
type: source
tags:
- RAG/retrieval
summary: 本文介绍了有 30 年历史的经典稀疏检索算法 BM25，通过拆解 IDF（逆文档频率）、TF 词频饱和度以及文档长度惩罚三项核心要素，分析了其在专有名词与错误码精确匹配中的优势，以及其在混合检索（Hybrid
  Search）架构中的核心价值。
sources:
- raw/articles/2026-05-05_How-does-BM25-ranking-algorithm-work_19dfa2.md
updated: '2026-08-04'
---

# How does BM25 ranking algorithm work?

## 来源信息
- **来源**: Daily Dose of DS
- **作者**: Avi Chawla
- **原始链接**: [How does BM25 ranking algorithm work?](https://www.dailydoseofds.com/a-crash-course-on-building-rag-systems-part-1-with-implementations/)
- **归档物理文献**: [[raw/articles/2026-05-05_How-does-BM25-ranking-algorithm-work_19dfa2.md]]

## 核心要点
1. **BM25 的基石地位**：虽然已有 30 年历史且无需任何训练、向量 Embedding 或微调，BM25 至今依然是 Elasticsearch、OpenSearch 以及大多数生产级搜索引擎的核心支柱，代表了经典词袋稀疏检索（Sparse Retrieval）的最高水平。
2. **IDF（逆文档频率）衡量稀缺度**：BM25 会动态评估词语在语料库中的稀罕程度。常见无意义的停用词（如 "the"、"is"）权重会被降到极低甚至忽略，而特定罕见的专有名词（如 "transformer"）则会被赋予极高的相关性分数。
3. **TF 词频饱和度与参数 $k_1$**：虽然词频（Term Frequency）越高说明相关性越强，但 BM25 引入了边际递减效应（即出现 10 次与出现 100 次的差异并不大）。参数 $k_1$（通常在 1.2 至 2.0 之间）控制饱和速度，$k_1$ 越小，饱和越快。
4. **文档长度惩罚与参数 $b$**：长文档因为字数多，天然更容易命中更多关键词。BM25 将文档长度与语料库平均长度进行对比，用参数 $b$（通常为 0.75）调节惩罚力度，防止长文章因“注水”而排在前面。
5. **专有名词匹配与混合检索（Hybrid Search）**：BM25 在专有名词、错误代码（如 "error code 5012"）的精确匹配上优于语义 Embedding 检索（后者更倾向于返回语义相关但字面不匹配的结果）。最先进的 RAG 系统通过将两者结合（混合检索），兼得语义理解与精准匹配的优势。

## 关键引文
- "A 30-year-old algorithm with zero training, zero embeddings, and zero fine-tuning still powers Elasticsearch, OpenSearch, and most production search systems today."
- "BM25 asks three simple questions: 'How rare is this word?' ... 'How many times does it appear?' ... 'Is this document unusually long?'"
- "BM25 excels at exact keyword matching, which is something embeddings often struggle with. It also shines when your corpus has domain-specific terminology..."
- "Top RAG systems today combine BM25 with vector search. You get the best of both worlds: semantic understanding AND precise keyword matching."

## 联动概念
- BM25检索算法

> 📎 **物理文献**：[[raw/articles/2026-05-05_How-does-BM25-ranking-algorithm-work_19dfa2.md]]
