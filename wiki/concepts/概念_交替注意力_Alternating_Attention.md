---
type: concept
tags:
- LLM/arch/attention
- DeepLearning
- Infra/serving
summary: 交替注意力（Alternating Attention）是 ModernBERT 采用的记忆体高效注意力机制，通过在每三层交替使用一层全局注意力与滑动窗口局部注意力（128个最近
  token），打破了传统 BERT 全局注意力二次方复杂度的瓶颈。
sources:
- wiki/sources/2025-07-01_Full-global-attention-vs-alternating-attention_197c7a.md
updated: 2026-08-03
---

# 交替注意力 (Alternating Attention)

## 定义与实现原理
**交替注意力（Alternating Attention）**是 ModernBERT 模型中提出的一种高度内存高效的注意力机制，旨在打破传统 Transformer 编码器中全局注意力计算的二次方复杂度限制。

在具体实现中，ModernBERT 将注意力层进行交替配置：
1. **全局注意力（Full Global Attention）**：仅在每三层中使用一层。这一层允许序列中的所有 token 进行两两交互，确保模型能够捕捉和保留长距离的全局语义依赖。
2. **滑动窗口局部注意力（Sliding Window Local Attention）**：在其余的所有层中使用。每个 token 仅关注其最近邻的 128 个 token，大幅缩减了非必要的计算开销。

通过这种交替机制，ModernBERT 在保持长文本理解能力的同时，实现了 16 倍的序列长度扩展，并成为当前内存效率极高的编码器模型。

## 读书比喻与直觉解释
ModernBERT 官方在发布时提供了一个直观的读书比喻来解释为什么这种设计在实际中非常有效：
> 想象你在读一本书。为了理解你当前正在阅读的每一句话，你需要无时无刻不在脑海中回忆整本书的完整剧情（类似于**全全局注意力**）吗？还是说，只要理解当前的章节（类似于**局部注意力**）就足够了，前提是你只需要偶尔思考当前章节对整本书主线剧情的意义（类似于**全局注意力**）？在绝大多数情况下，答案显然是后者。

## 关联来源
- [[wiki/sources/2025-07-01_Full-global-attention-vs-alternating-attention_197c7a.md|Full global attention vs alternating attention (Source 摘要)]]
