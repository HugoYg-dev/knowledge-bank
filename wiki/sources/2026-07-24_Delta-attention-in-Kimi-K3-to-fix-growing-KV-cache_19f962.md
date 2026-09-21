---
type: source
tags:
- LLM/arch/attention
- LLM/inference
- LLM/arch
summary: 本文介绍了 Kimi K3 采用的 Delta Attention 机制。该机制摒弃了传统随序列无限增长的 KV 缓存，将历史关联压缩在固定大小的矩阵中，实现了
  $O(1)$ 空间与 $O(N)$ 计算的线性开销，并通过先读后写、只写差值（Delta Rule）来更新关联，结合混合交替方案以保证召回精度。
sources:
- raw/articles/2026-07-24_Delta-attention-in-Kimi-K3-to-fix-growing-KV-cache_19f962.md
updated: '2026-08-04'
---

# 来源摘要：Delta attention in Kimi K3 to fix growing KV cache

## 来源信息
- **标题**: Delta attention in Kimi K3 to fix growing KV cache
- **作者/发布者**: Daily Dose of DS (Avi)
- **发布日期**: 2026-07-24
- **原始链接**: [Kimi K3 Official Announcement Blog](https://kimi.com/blog/kimi-k3)
- **关联概念**: [[概念_Delta_Attention与增量矩阵缓存]], [[概念_KV_Cache_键值缓存]]

## 核心要点
- **KV 缓存的容量危机**：传统 Attention 需要将每一个 Token 的键值对（KV）保存在列表中（即 KV Cache），随着输入序列的增长，KV 缓存呈线性累积，且多轮注意力扫描带来二次方复杂度计算与严重的内存膨胀。
- **固定大小矩阵的增量检索**：Delta Attention 放弃了保存完整的 KV 对列表，而是将全部历史信息压缩折叠进一个固定大小的矩阵（Fixed-size matrix）中。这个矩阵仍然能够像哈希表或检索表一样运作：输入一个键，就会依据相似度权重输出过去混合的值向量。
- **Delta 写入规则（Delta Rule）**：
  1. **先读后写 (Read-before-write)**：将新 Token 的 Key 输入矩阵，读取出当前矩阵的预测关联值（旧有关联）。
  2. **只写差值 (Write the delta)**：将预测值与目标值对比，仅将两者之间的“差距（Delta）”写入矩阵进行纠正与覆盖，避免因无脑叠加而使矩阵信息过载。同时老旧关联会随着时间推移自然淡出。
- **效率与精度的权衡**：
  - **优势**：消除了不断累积的 KV cache 列表，开销上实现 $O(1)$ 空间复杂度与 $O(N)$ 计算复杂度。
  - **局限性**：有损压缩使得对单一 Token 的精确召回（Recall）转为了近似召回。
- **混合交替混合架构 (Interleaving)**：为了克服近似召回的缺陷，Kimi K3 在生产部署中采用了混合结构——将少数精确全注意力层（Exact Lookup）与多数 Delta Attention 线性层交替编织，以保证长文本召回质量。

## 关键引文
> The entire past collapses into one fixed-size matrix that still behaves like the lookup table.

> It reads before it writes. It hands the matrix the new token’s key and sees what value the memory currently returns, its existing guess for that address. It writes the difference, not the value.

> Of course, a compressed matrix cannot store every token exactly, so recall of any single token becomes approximate. That is why production models interleave the two, i.e., a few full-attention layers for exact lookup and the rest running linear.

---
> 📎 **物理文献**：[[raw/articles/2026-07-24_Delta-attention-in-Kimi-K3-to-fix-growing-KV-cache_19f962.md]]
