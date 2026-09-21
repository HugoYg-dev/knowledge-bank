---
type: source
tags:
- Infra/serving
- LLM/inference
summary: 介绍 NVIDIA 与 MIT 联合提出的 SparDA 架构。该架构在传统 Transformer 的 Q/K/V 投影之上引入第四投影 Forecast，预测下一层所需的
  KV 块，从而实现从 CPU 内存异步预取 KV Cache，大幅缓解长文本 CPU offload 传输瓶颈。
sources:
- raw/articles/2026-07-14_NVIDIA-researchers-built-a-new-transformer-variant_19f617.md
updated: '2026-08-04'
---

# 来源摘要：NVIDIA researchers built a new transformer variant (SparDA)

## 来源信息
- **标题**: NVIDIA researchers built a new transformer variant (SparDA)
- **来源**: Daily Dose of DS
- **日期**: 2026-07-14
- **原文链接**: [arXiv:2606.04511](https://arxiv.org/abs/2606.04511)
- **物理文献**: [[raw/articles/2026-07-14_NVIDIA-researchers-built-a-new-transformer-variant_19f617.md]]

## 核心要点
1. **长文本 CPU Offload 瓶颈**：在长文本（100K+）推理中，KV Cache（键值缓存）体积过大无法全部驻留在 GPU 显存中，通常会被卸载（Offload）到 CPU 内存。然而在逐层解码时，GPU 需要等待所需块从 CPU 复制回显存，这种 I/O 拷贝极其缓慢，导致 GPU 频繁处于闲置（Stall）状态。
2. **传统稀疏选择的痛点**：传统的稀疏注意力方法是由当前层的 Query 向量决定注意力块的选择，这导致两点限制：
   - 块选择必须等到当前层开始计算、Q 向量产生后才能进行，无法实现数据提前预取。
   - 块选择算法在 GQA（Grouped-Query Attention）中开销昂贵，每个 query 头都需要对所有块打分、做 Softmax 并累加，计算成本随着上下文长度剧烈上升。
3. **Forecast 投影与异步预取设计**：SparDA 通过给每一层新增第四投影——**Forecast**（仅占 0.41% 参数，8B 模型约新增 33.5M 参数），利用 L 层的 Forecast 向量预测下一层（L+1 层）所需的 KV 块。这样在 L 层计算的同时，便可通过独立的 CUDA Stream 异步将 L+1 层所需的块从 CPU 预取回 GPU，使数据传输与计算重叠（Overlap）。
4. **廉价分组选择器**：SparDA 的 Forecast 投影不与具体的注意力头绑定，而是每个 GQA 组只配置一个 Forecast 头，这去除了对每个 Query 头的循环打分，且跳过了 Softmax 计算，极大地降低了块选择的算力开销。
5. **物理收益与表现**：在 8B 模型（如 NOSA-8B）测试中，长推理准确率提升 **6.5** 点，推理预填充（Prefill）阶段提速 up to 1.25x，解码（Decode）提速 up to 1.7x。更重要的是，预取机制隐藏了 Offload 的拷贝延迟，使得大多数 KV Cache 可以直接驻留在 CPU 内存中，从而释放出大量 GPU 显存用于增大 Batch Size，将 Decode 吞吐量推高至 5.3x。

## 关键引文
- > "NVIDIA's tweak adds a fourth projection, which predicts what the next layer will need."
- > "Since the next layer's block set is known while the current layer is still computing, the runtime fetches those blocks from CPU memory on a separate CUDA stream. The copy overlaps with the current layer's compute..."
- > "Because prefetch hides the offload cost, most of the KV cache can live in CPU RAM, and the freed GPU memory fits much bigger batches, pushing decode throughput up to 5.3x..."

## 相关实体与概念
- [[wiki/concepts/概念_KV_Cache_键值缓存]]
- [[wiki/concepts/概念_SparDA预测式KV缓存预取]]
- [[wiki/concepts/概念_LLM推理两阶段]]

---
> 📎 **物理文献**：[[raw/articles/2026-07-14_NVIDIA-researchers-built-a-new-transformer-variant_19f617.md]]
