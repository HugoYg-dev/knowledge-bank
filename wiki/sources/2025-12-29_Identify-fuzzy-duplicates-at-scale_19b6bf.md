---
type: source
tags:
- Skill/data-analysis
- Infra/storage
summary: 介绍在大规模模糊重复数据检测中，由于 pairwise 两两比对所面临的 O(N^2) 复杂度瓶颈，通过引入分块阻断（Blocking / Bucketing）技术来减少
  98% 以上的冗余计算，将原本需要数年的计算量压缩至数小时内完成。
sources:
- raw/articles/2025-12-29_Identify-fuzzy-duplicates-at-scale_19b6bf.md
updated: '2026-08-03'
---

# Identify fuzzy duplicates at scale

## 来源信息
- **来源**: Daily Dose of DS
- **原主题**: 6 Steps to Build an ML Model
- **作者**: Avi Chawla
- **链接**: [Bi-encoders and Cross-encoders for Sentence Pair Similarity Scoring – Part 1](https://www.dailydoseofds.com/bi-encoders-and-cross-encoders-for-sentence-pair-similarity-scoring-part-1/)
- **归档物理文献**: [[raw/articles/2025-12-29_Identify-fuzzy-duplicates-at-scale_19b6bf.md]]

## 关联概念/实体
- 分块阻断技术_Blocking

## 核心要点
1. **数据去重痛点**：对于精确重复，Pandas 的 `drop_duplicates()` 能够高效处理，但对模糊重复数据（如拼写略有不同、地址相似但有细微差异的记录）无能为力。
2. **两两比对的复杂度瓶颈**：在大规模数据集（例如 100万条记录）中，若采用朴素的两两比对（Pairwise Comparison），会产生 $O(N^2)$ 即 $10^{12}$ 次比对。即使每秒进行 10,000 次比对，也需要大约 3 年时间，在工程上是不可行的。
3. **模糊重复的词汇重叠特征**：如果两条记录是重复的，它们必然具有某种词汇（或文本）层面的重叠（Lexical Overlap）。没有重叠的记录（如 "Daniel" 与 "Philip"）绝对是不同的，无需进行两两对比。
4. **分块阻断机制（Blocking/Bucketing）**：根据特定规则（如名字的前三个字母、邮政编码等启发式规则）将数据划分至不同的小桶（Buckets）。只对同一个桶内的记录执行相似度比对。
5. **计算效益**：通过分块阻断，可以过滤掉约 98% - 99% 的冗余计算。分块后还可以结合 LLM 等更高级的算法对桶内数据进行深度去重，将处理时间从数年缩短至几小时。
6. **NLP/RAG 系统中的延展应用**：模糊重复检测技术不仅用于数据清洗，也是 NLP 系统（如 Quora 的相似问题推荐）以及 RAG（检索增强生成）系统中进行文本去重和相似度评分的核心基础模块。

## 关键引文
> "Data duplication is a big problem that many organizations face. ... Fuzzy duplicates are those records that are not exact copies of each other but appear to be the same"
> "Even if we assume a decent speed of 10,000 comparisons per second, this approach will take ~3 years to complete."
> "Segregating the records will eliminate about 98-99% of unnecessary comparisons that would have happened otherwise."

---
> 📎 **物理文献**：[[raw/articles/2025-12-29_Identify-fuzzy-duplicates-at-scale_19b6bf.md]]
