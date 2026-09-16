---
type: source
tags:
- LLM/inference
- Infra/serving
summary: 本文深入剖析了大模型推理内部的工作原理，详细对比了 Prefill（预填充）和 Decode（解码）两个不同的计算阶段及其硬件瓶颈，并讨论了 KV
  Cache、量化以及 Continuous Batching、Speculative Decoding 和 PagedAttention 等服务层优化技术。
sources:
- raw/articles/2026-05-03_How-LLM-inference-works-internally_19deee.md
updated: '2026-08-04'
---

# How LLM inference works internally

## 来源信息
- **来源**: Daily Dose of DS
- **作者**: Avi Chawla
- **原始链接**: [How LLM inference works internally](https://www.dailydoseofds.com/llmops-crash-course-part-1/)
- **归档物理文献**: [[raw/articles/2026-05-03_How-LLM-inference-works-internally_19deee.md]]

## 核心要点
1. **大模型推理两阶段**：推理被划分为 Prefill（预填充）阶段和 Decode（解码）阶段。Prefill 并行处理所有 prompt tokens 并填充 KV Cache，是计算密集型（Compute-bound）；Decode 则是自回归逐字生成，每步仅计算新 token 的 Q，并读取缓存的 K/V，由于需要频繁从内存加载权重和 KV Cache，属于内存带宽限制（Memory-bound），这导致 GPU 算力利用率在 Decode 阶段大幅闲置（通常降至 30% 左右）。
2. **硬件瓶颈与性能指标**：Prefill 阶段受限于 GPU 的算力吞吐量，核心指标是首字延迟（TTFT）；Decode 阶段受限于内存带宽，核心指标是词间延迟（ITL）。
3. **KV Cache 的开销与架构设计**：KV Cache 避免了 O(N²) 的重复计算，但其随着序列长度线性增长，对显存（VRAM）压力极大（如 13B 模型每 token 约需 1 MB），严重限制了并发服务的 Batch Size。最新的优化设计如 DeepSeek-V4 采用 CSA 和 HCA 混合注意力，大幅压缩了 KV Cache（可降至 10%）。
4. **服务框架三剑客**：主流推理服务引擎（如 vLLM、TensorRT-LLM）引入了三项关键优化：
   - **Continuous Batching（连续批处理）**：迭代级别交织任务，提高 Decode 阶段算力利用率。
   - **Speculative Decoding（推测解码）**：用轻量级草稿模型建议 tokens 并利用大模型进行并行验证，用计算换取串行步骤的减少。
   - **PagedAttention（分页注意力）**：将 KV Cache 在显存中像操作系统一样分页管理，彻底消除显存碎片，极大地增加了单卡并发容量。
5. **量化加速**：FP32/BF16 通常用于训练，而推理常采用 FP16/BF16，甚至量化至 INT8 或 INT4。这不仅能减少显存需求，还能提高存取速度并减少带宽占用，从而使 7B 级别的模型能运行在消费级硬件（4-6 GB VRAM）上。

## 关键引文
- "prefill (processing the prompt) is compute-bound, while decode (generating tokens one at a time) is memory-bound."
- "The arithmetic per step is tiny (one query vector against the cached key matrix instead of a full matrix-matrix multiply). But the GPU still loads every weight matrix and the entire cached K/V from memory for that small computation. The bottleneck flips from compute to memory bandwidth."
- "The cost is that the cache grows linearly with sequence length and exists per-layer. For a 13B-parameter model, the cache consumes roughly 1 MB per token."
- "DeepSeek's V4 series (released April 2025) takes a different approach: redesign attention so the cache is structurally smaller from the start."
- "continuous batching interleaves tokens from multiple requests on the same GPU step... Speculative decoding uses a small draft model to propose multiple tokens... PagedAttention manages KV cache memory in fixed-size blocks, eliminating fragmentation."

## 联动概念
- [[wiki/concepts/概念_LLM推理两阶段]]
- [[wiki/concepts/概念_KV_Cache]]

> 📎 **物理文献**：[[raw/articles/2026-05-03_How-LLM-inference-works-internally_19deee.md]]
