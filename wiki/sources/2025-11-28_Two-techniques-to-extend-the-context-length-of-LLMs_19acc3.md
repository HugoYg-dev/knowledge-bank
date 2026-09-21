---
type: source
tags:
- DeepLearning
- LLM/arch
- LLM/arch/attention
summary: 探讨了扩展大语言模型（LLM）上下文长度面临的二次方复杂度瓶颈，并详细介绍了两种主流优化技术：近似计算的稀疏注意力（Sparse Attention）和优化
  GPU 显存数据流搬运的 Flash Attention，同时指出选择合适位置编码（如 RoPE）在长上下文理解中的关键作用。
sources:
- raw/articles/2025-11-28_Two-techniques-to-extend-the-context-length-of-LLMs_19acc3.md
updated: 2026-08-03
---

# 来源信息
- **标题**: Two techniques to extend the context length of LLMs
- **作者**: Daily Dose of DS
- **日期**: 2025-11-28
- **原始物理文献**: [[raw/articles/2025-11-28_Two-techniques-to-extend-the-context-length-of-LLMs_19acc3.md]]

# 联动概念
- 稀疏注意力
- [[wiki/concepts/概念_FlashAttention_快速注意力|Flash Attention]]
- [[wiki/concepts/概念_自注意力复杂度|自注意力复杂度]]

# 核心要点
1. **注意力机制的二次方复杂度瓶颈**：传统 Transformer 的自注意力机制计算复杂度与序列长度呈二次方（$O(N^2)$）关系。处理长文本时算力与内存开销会急剧膨胀，限制了 LLM 上下文窗口的扩展。
2. **优化方案一：稀疏注意力（Sparse Attention）**：不计算所有 Token 对的注意力，而是将其限制在子集内以减少计算量。包括限制在邻近区域的局部窗口注意力（Local Attention）和让模型动态学习关注特定高价值长距 Token 的自适应选择。
3. **优化方案二：Flash Attention 硬件加速**：这是一种精确且内存高效的注意力计算方法。它主要优化了 GPU 内部高速、稀少的 SRAM 与慢速、充沛的 HBM（通常慢 8-15x）之间的数据传输。通过在 SRAM 中缓存 Softmax 等中间计算结果，避免了矩阵的重复搬运，在保持传统注意力精确性的同时提供了多倍的速度提升，并能线性扩展。
4. **长文本理解的配套机制**：算力优化仅仅解决了“能塞入长上下文”的物理问题，模型能否真正理解长距离 Token 的关系还需要依赖合理的位置编码，如旋转位置编码（RoPE）能够较好地保留相对位置和关联关系。

# 关键引文
- "In a traditional transformer, a model processing 4,096 tokens requires 64 times more computation (quadratic growth) than one handling 512 tokens due to the attention mechanism."
- "SRAM is scarce but extremely fast. HBM is much more abundant but slow (typically 8-15x slower)."
- "Flash attention reduces the repeated movements by utilizing SRAM to cache the intermediate results."
- "Rotary positional embeddings (RoPE) usually work the best since they preserve both the relative position and the relation."

> 📎 **物理文献**：[[raw/articles/2025-11-28_Two-techniques-to-extend-the-context-length-of-LLMs_19acc3.md]]
