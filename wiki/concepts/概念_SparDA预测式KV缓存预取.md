---
type: concept
tags:
- Infra/serving
- LLM/inference
summary: NVIDIA 与 MIT 提出的 SparDA 架构，通过引入 Forecast（第四投影）预测并异步预取下一层所需的 KV 块，实现长上下文下
  CPU offload 的计算与传输重叠，并利用分组选择器跳过 Softmax，显著提升长文本推理的解码速度和吞吐量。
sources:
- wiki/sources/2026-07-14_NVIDIA-researchers-built-a-new-transformer-variant_19f617.md
updated: '2026-08-04'
---

# 概念：SparDA 预测式 KV 缓存预取

## 定义
**SparDA (Sparse Attention with Forecast)** 是由 NVIDIA 与 MIT 联合提出的一种新型 Transformer 变体架构。与在每个 attention 层仅计算 $Q, K, V$ 三个投影向量的传统 Transformer 不同，SparDA 引入了第四投影通道——**Forecast（预测）**。Forecast 的参数量开销极小，对于一个 8B 大小的模型仅增加约 33.5M 参数（占比约 0.41%），但它能改变 KV Cache 的获取流程，将数据从 CPU 内存异步预取回 GPU。

## 传统 CPU Offload 稀疏选择的两大痛点
在超长文本（如 100K+ 上下文）场景下，由于 KV Cache 体积巨大无法全量驻留在 GPU 显存中，通常会将大部分块卸载（Offload）到 CPU 内存。采用传统稀疏注意力选择重要块时，面临两大痛点：
1. **搬运复制延迟严重阻塞 GPU**：传统的块选择算法是由当前层的 Query 向量驱动的。由于 Query 向量 $Q$ 必须等到当前层开始计算后才会生成，这意味着只有当 GPU 执行到该层时才知道需要搬运哪些 KV 块。此时 GPU 必须暂停推理计算（Stall），等待慢速的总线将数据从 CPU 内存搬运回 GPU 显存，每层均是如此，导致严重的性能卡顿。
2. **GQA 多头选择计算开销昂贵**：在分组查询注意力（GQA）架构下，多个 Query 头共享一个 KV 头。然而在决定哪些块需要被保留时，传统的选择器仍需要在每个 Query 头下对所有候选块打分，再对每个头进行 Softmax 计算并累加，此选择开销随着上下文长度暴增，使得稀疏注意力的“便宜”计算优势被高昂的“块选择算力”抵消。

## SparDA 异步预取与重叠（Overlap）机制
SparDA 通过解耦“块选择驱动源”来解决上述痛点：
- **Forecast 跨层预测**：SparDA 的第 $L$ 层输出中除了 $Q_L, K_L, V_L$ 之外，还会生成一个 `Forecast` 向量。该向量用来直接预测第 $L+1$ 层所需的 KV 块哈希。
- **双 CUDA Stream 异步预取**：由于在第 $L$ 层计算仍在执行时，下一层 $L+1$ 所需的 KV 块列表就已经被 Forecast 预测出来，运行时（Runtime）得以在**另一个独立的 CUDA Stream** 上异步启动从 CPU 内存向 GPU 显存的数据搬运。
- **传输与计算重叠（Overlap）**：这使得 $L+1$ 层的 I/O 拷贝过程与 $L$ 层的 GPU 推理计算时间上完全重叠。当第 $L$ 层计算完毕切换至 $L+1$ 层时，所需的 KV 块数据已经就绪在 GPU 中，从而彻底消除了 GPU 等待数据的 Stall 延迟。

## 廉价分组选择器
由于 Forecast 专门用于预测下一层的块而与当前的自注意力计算无关，SparDA 将 Forecast 与 Query 头解耦：
- **GQA 分组级 Forecast**：在 GQA 架构中，SparDA 不会为每个 Query 头单独进行打分，而是每个 GQA 分组（即共享同一个 KV 头的多个 Query 头）仅仅使用一个 Forecast 头进行统一预测。
- **跳过 Softmax**：该设计消除了 per-query-head 的打分循环，并直接跳过了 Softmax 的打分分布归一化过程，大大简化了选择器的计算开销。

## 物理收益与表现
通过测试 8B 规模的模型（如 NOSA-8B 及 MiniCPM4.1-8B），SparDA 表现出优异的性能：
- **推理加速**：预填充（Prefill）阶段提速 up to 1.25x；解码（Decode）阶段提速 up to **1.7x**。
- **吞吐量大增**：由于 Forecast 预取机制将 Offload 带来的传输延迟彻底隐藏，大批 KV Cache 能够安稳驻留在 CPU 内存中，这释放了宝贵的 GPU 显存用于塞入更大的 Batch Size，进而实现了高达 **5.3x** 的解码吞吐量飞跃。
- **推理准确率**：在长文本推理评测中不仅没有精度损失，甚至因为有效的注意力保留，在长推理（Long-reasoning）准确率上提升了 **6.5 点**。

## 关联
- [[概念_KV_Cache]]
- [[概念_LLM推理两阶段]]
- [[wiki/sources/2026-07-14_NVIDIA-researchers-built-a-new-transformer-variant_19f617]]（直接来源）
