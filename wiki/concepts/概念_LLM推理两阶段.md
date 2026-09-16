---
type: concept
tags:
- Infra/serving
- LLM/inference
summary: 大语言模型（LLM）推理过程可分为 Prefill（预填充）和 Decode（解码）两个不同的计算阶段。Prefill 阶段是计算密集型（Compute-bound），并行处理输入并填充
  KV Cache；Decode 阶段是内存带宽密集型（Memory-bound），自回归逐字生成 token。
sources:
- wiki/sources/2026-05-03_How-LLM-inference-works-internally_19deee.md
- wiki/sources/2026-07-14_NVIDIA-researchers-built-a-new-transformer-variant_19f617.md
- wiki/sources/2026-07-27_The-anatomy-of-diffusion-LLMs_19fa57.md
- wiki/sources/2026-08-10_Cross-model-KV-cache-transfer-in-LLM-families_19febef2c6003814.md
- wiki/sources/How_a_GPU_Actually_Works.md
- wiki/sources/KV_Cache_Engineering_for_LLM_Serving.md
updated: '2026-09-15'
---
# 概念：LLM 推理两阶段

## 定义

在大语言模型（LLM）的单次生成请求中，推理过程由两阶段构成：**Prefill（预填充）** 阶段和 **Decode（解码）** 阶段。由于这两个阶段的计算特征（并行度与存取比）存在本质差异，它们面临的硬件瓶颈、硬件利用率以及性能指标完全不同。

---

## 阶段对比分析与 Roofline 量化解构

| 维度 | Prefill 阶段 (预填充) | Decode 阶段 (解码) |
| :--- | :--- | :--- |
| **工作内容** | 一次性处理用户输入的所有 Prompt tokens，计算对应的注意力 Key 和 Value，并填充到 KV 缓存（[[concepts/概念_KV_Cache|KV Cache]]），同时生成首个输出 token。 | 自回归地逐个生成后续 tokens。每步仅将新生成的单个 token 输入模型计算其 QKV，并结合 KV Cache 里的历史 K/V 进行注意力计算。 |
| **硬件瓶颈** | **计算绑定（Compute-bound）**<br>所有输入 tokens 并行计算，以大矩阵相乘的形式在 GPU 运行，算力吞吐量（Throughput）是主要约束。 | **内存带宽绑定（Memory-bound）**<br>由于是一步步串行计算单向量与全权重的矩阵乘法，GPU 每一生成步都必须将全部权重从显存重新加载到 SRAM 中，算力极大闲置（利用率常低于 30%）。 |
| **算力强度 (Work per Byte)** | **$\gg 300$ ops/byte**<br>单次加载的权重在 Prompt 的 $N$ 个 token 上并行复用，算力强度高。 | **$\approx 1$ op/byte**<br>以 70B 模型在 BF16（140GB）为例：单步生成 1 个 token 产生约 1400 亿次浮点运算（140 GFLOPs），访存量为 140GB，算力强度仅 1 op/byte。 |
| **硬件平衡线对比** | 远高于 [[entities/实体_NVIDIA|NVIDIA]] H100（~295 ops/byte）平衡阈值，落在 [[concepts/概念_Roofline模型与算力强度|Roofline 模型]] 的算力天花板区。 | 比 H100 平衡阈值低约 **300 倍**，理论生成延迟下限被显存带宽锁死：$140\text{GB} / 3.3\text{TB/s} \approx 42\text{ms/token}$（单卡单序列极限约 24 tokens/s）。 |
| **核心性能指标** | **首字延迟 (Time to First Token, TTFT)**<br>用户发送请求到模型输出第一个 token 的等待时长。 | **词间延迟 (Inter-Token Latency, ITL)**<br>相邻两个输出 token 之间的平均生成间隔。 |
| **资源消耗规律** | 输入 prompt 越长，TTFT 呈非线性增加。 | 输出 sequence 越长，ITL 和 KV Cache 的显存开销越大。 |

---

## 系统级服务优化方案（Roofline 视角）

为了应对两阶段各自的瓶颈，现代推理服务引擎将优化手段划分为两大矢量：

### 1. 提升算力强度（增大 Work per Fetch，向计算密集区靠拢）
- **[[concepts/概念_连续批处理|连续批处理 (Continuous Batching)]]**：传统批处理受短请求等待长请求拖累；连续批处理在迭代边界动态重构批次。将单次权重搬运分摊给 $B$ 个并发请求，在 16-bit 精度下，并发需达到 ~300 才能将 Decode 阶段推入计算受限区。
- **[[concepts/概念_推测解码|推测解码 (Speculative Decoding)]]**：通过参数量极小的草稿模型快速自回归生成多个候选 tokens，再由目标大模型单次前向完成并行校验。本质是将 Decode 的多次串行访存，转化为一次利用 Prefill 计算密集特性的批量矩阵验证。

### 2. 削减访存搬运字节（Decrease Bytes Fetched，降低延迟下限）
- **权重与 KV 缓存量化（Quantization）**：将权重压缩为 FP8 或 INT4，直接将单步读取显存量减半（从 140GB 降至 70GB），使 70B 模型解码的理论时延下限从 42ms 压缩至 21ms（吞吐上限翻倍至 48 tok/s）。
- **PagedAttention 分页管理**：以固定大小物理块分配显存，消除内部碎片，支持更大并发 Batch Size。
- **[[concepts/概念_FlashAttention|FlashAttention]]**：利用 SRAM Tiling 分块与在线增量 Softmax，避免频繁存取 HBM $N \times N$ 矩阵。

---

## 关联

- [[2026-05-03_How-LLM-inference-works-internally_19deee]] （来源）
- [[sources/How_a_GPU_Actually_Works]]（来源）
- [[sources/KV_Cache_Engineering_for_LLM_Serving]]（来源）
- [[concepts/概念_Roofline模型与算力强度|概念_Roofline模型与算力强度]]
- [[concepts/概念_AI硬件加速芯片架构|概念_AI硬件加速芯片架构]]
- [[concepts/概念_KV_Cache|概念_KV_Cache]]
- [[concepts/概念_连续批处理|概念_连续批处理]]
- [[concepts/概念_推测解码|概念_推测解码]]
- [[concepts/概念_FlashAttention|概念_FlashAttention]]
- [[entities/实体_NVIDIA|实体_NVIDIA]]
- [[entities/实体_vLLM|实体_vLLM]]
