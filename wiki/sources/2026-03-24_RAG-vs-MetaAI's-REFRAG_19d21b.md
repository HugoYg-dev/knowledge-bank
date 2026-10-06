---
type: source
tags:
- RAG/retrieval
- AI-Agent/coding
- LLM/arch
summary: 介绍 Meta AI 提出的 REFRAG 架构，该架构通过在向量层面压缩和过滤检索到的 Chunks，从而实现高效率的 RAG 检索，大幅降低延迟与
  token 消耗。
sources:
- raw/articles/2026-03-24_RAG-vs-MetaAI's-REFRAG_19d21b.md
updated: 2026-08-04
---

# Source: RAG vs MetaAI's REFRAG

## 来源信息
- **标题**: RAG vs MetaAI's REFRAG
- **原邮件主题**: How to Build an OS for Your AI Workforce?
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: 2026-03-24
- **原始归档**: [[raw/articles/2026-03-24_RAG-vs-MetaAI's-REFRAG_19d21b.md]]

## 关联概念/实体
- **实体**: [[entities/实体_Meta]]
- **概念**: [[wiki/concepts/概念_REFRAG_RAG压缩与过滤]]

## 核心要点
- **经典 RAG 的缺陷**：在传统 RAG 中，检索到的所有文本块直接注入到 LLM 上下文中，导致大量冗余 token 的计算，显著增加了延迟与计算开销。
- **REFRAG 核心思想**：由 Meta AI 提出，它在向量层面对上下文进行压缩和过滤，无需将每个块的每个 token 都输入 LLM。
- **四大核心机制**：通过块压缩将文本块表示为单嵌入向量，使用基于强化学习（RL）的相关性策略进行快速过滤，执行选择性展开以获取精细特征，并使用混合拼接机制组装最终输入。详细参考 [[wiki/concepts/概念_REFRAG_RAG压缩与过滤]]。
- **显著性能收益**：TTFT（首字时间）提速达 30.85x，支持 16x 更大上下文窗口，并在使用更少 token 的情况下，在 16 个基准测试中优于 LLaMA，且无精度损失。

## 关键引文
- > "Most of what we retrieve in RAG setups never actually helps the LLM."
- > "Instead of feeding the LLM every chunk and every token, REFRAG compresses and filters context at a vector level..."
- > "That means you can process 16x more context at 30x the speed, with the same accuracy."

---
> 📎 **物理文献**：[[raw/articles/2026-03-24_RAG-vs-MetaAI's-REFRAG_19d21b.md]]
