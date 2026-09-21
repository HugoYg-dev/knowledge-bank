---
type: source
tags:
- DeepLearning
- LLM/arch/attention
summary: 介绍了 ModernBERT 如何通过交替注意力（Alternating Attention，每三层全局注意力，其余层 128 tokens 的滑动窗口局部注意力）来打破传统
  BERT 全局注意力二次方复杂度瓶颈，提升内存效率与长序列处理能力。
sources:
- raw/articles/2025-07-01_Full-global-attention-vs-alternating-attention_197c7a.md
updated: 2026-08-03
---

# Full global attention vs alternating attention (Source 摘要)

## 来源信息
- **主题**: uv Cheatsheet and Hands-on Guide for Python Devs (Daily Dose of DS)
- **发送人**: Daily Dose of DS \<avi@dailydoseofds.com\>
- **日期**: 2025-07-01
- **物理原始文件**: [[raw/articles/2025-07-01_Full-global-attention-vs-alternating-attention_197c7a.md]]

## 核心要点
- **ModernBERT 的改进**：ModernBERT 是 BERT 的升级版本，支持 16 倍的序列长度，具有更好的分类和检索下游任务性能，并且是内存效率最高的编码器。
- **瓶颈问题**：BERT 采用全局注意力（Full Global Attention），其计算复杂度与序列长度呈二次方关系，极大限制了处理长文本的能力。
- **交替注意力（Alternating Attention）**：ModernBERT 引入了交替注意力机制以突破上述瓶颈：
  - 每三层中有一层使用**全局注意力**。
  - 其余层使用**滑动窗口局部注意力**，即每个 token 仅关注最近的 128 个 token。
- **生动读书比喻**：原文将此机制比喻为读书。理解一句话往往只需关注当前章节（局部注意力），只有在特定时刻才需要回想其与整本书主线剧情的关联（全局注意力）。

## 关联概念/实体
- 概念: 交替注意力 (Alternating Attention)

## 关键引文
> Conceptually, the reason this works is pretty simple: Picture yourself reading a book. For every sentence you read, do you need to be fully aware of the entire plot to understand most of it (full global attention)? Or is awareness of the current chapter enough (local attention), as long as you occasionally think back on its significance to the main plot (global attention)? In the vast majority of cases, it’s the latter.

---
> 📎 **物理文献**：[[raw/articles/2025-07-01_Full-global-attention-vs-alternating-attention_197c7a.md]]
