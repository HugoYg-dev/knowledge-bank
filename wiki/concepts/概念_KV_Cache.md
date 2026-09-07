---
type: concept
tags:
- Infra/AI
- LLM/inference
summary: KV Cache 缓存 LLM 推理中 X@W_K 和 X@W_V 的已计算结果，空间换时间，避免自回归逐 token 生成时对历史 token
  的重复计算。几乎所有 LLM 推理框架（如 vLLM）均已支持。
sources:
- wiki/sources/2025年七大顶流大模型架构.md
- wiki/sources/2026-05-03_How-LLM-inference-works-internally_19deee.md
- wiki/sources/2026-07-07_Rethinking-KV-caching-for-production-inference_19f3d7.md
- wiki/sources/2026-07-14_NVIDIA-researchers-built-a-new-transformer-variant_19f617.md
- wiki/sources/DeepSeek_MLA矩阵吸收原理.md
- wiki/sources/KV_Cache原理图解.md
- wiki/sources/MCP遇上代码执行.md
- wiki/sources/Mamba_Explained_Kola_Ayonrinde.md
- wiki/sources/Manus创始人手把手拆解上下文工程.md
- wiki/sources/MiniMax_vs_Kimi_注意力路线之争.md
- wiki/sources/Transformer大模型3D可视化_NanoGPT.md
- wiki/sources/从DeepSeek-V3到Kimi_K2_八种现代LLM架构大比较.md
- wiki/sources/入局AI_Infra系统设计与挑战.md
- wiki/sources/大模型显存计算公式与优化.md
- wiki/sources/推测解码Speculative_Decoding综述.md
- wiki/sources/2026-07-24_Delta-attention-in-Kimi-K3-to-fix-growing-KV-cache_19f962.md
- wiki/sources/2026-08-10_Cross-model-KV-cache-transfer-in-LLM-families_19febef2c6003814.md
updated: '2026-09-07'
---


# 概念：KV Cache

## 定义

KV Cache 是 LLM 推理优化的核心机制。LLM 自回归生成时，每次推理都需将之前生成过的 token 重新输入模型计算 Key 和 Value，复杂度为 O(N²) 存在大量重复计算。KV Cache 将已计算的 K/V 矩阵缓存，后续只需计算新增 token 的 K/V 并拼接，以空间换时间减少计算量。

## 原理

- LLM 模型结构（因果注意力）使得历史 token 的 K/V 计算结果不变
- 缓存 X@W_K 和 X@W_V 的结果上半部分（历史 token 部分）
- 每步仅需计算当前新 token 的 K/V，与缓存拼接后执行注意力计算

### Prefill 与 Decode 阶段的读写流转

在推理的不同计算阶段，KV Cache 的读写流转有显著区别（参见 [[概念_LLM推理两阶段]]）：
- **Prefill（预填充）阶段**：大模型并行处理 prompt 中所有的 tokens，并一次性计算它们的 Key 和 Value 矩阵，将其**写入** KV Cache 中（Populate KV Cache）。此阶段只写不读。
- **Decode（解码）阶段**：自回归生成时，模型每步仅计算当前新生成 token 的 Query、Key 和 Value。此时，模型从 KV Cache 中**读取**（Retrieve）历史所有 tokens 的 K 和 V 矩阵，与新计算的 K/V 拼接，再进行注意力计算；计算完成后，再将新生成的 K 和 V **追加写入**到 KV Cache 中。此阶段既读又写，是典型的内存带宽瓶颈。

## 适用条件

- **仅适用于 Decoder 架构**（有 Causal Mask）
- Encoder 的 K/V 不可缓存，因为输入会整体变化

## 显存代价

$$\text{KV Cache} = 2 \times L \times H \times D \times S \times B \times \text{bytes}$$

示例：batch=32, head=32, layer=32, dim=4096, seq=2048, float32 → **约 64GB**

## 优化方向

| 方案 | 原理 |
|------|------|
| GQA/MQA | 减少头数，共享 K/V |
| MLA | 低秩压缩 K/V |
| Linear Attention | 无需 KV Cache |
| 量化 | K/V 低精度存储 |
| 滑动窗口 | 仅保留近邻 K/V |

## 生产应用中的挑战与优化演进

随着大模型在 Agent（智能体）与超长上下文（RAG）场景的落地，传统的 KV Cache 机制暴露出新的痛点：
- **Agent 推理中的冗余传输与计算**：斯坦福大学调研表明，在多轮交互的智能体工作流中，由于每一步都是从头计算，导致每次发送给模型的 Token 有约 **62%** 是重复的系统 Prompt、工具定义和历史文档。这不仅浪费带宽，也造成了极大的 Token 推理开销。为了突破这一瓶颈，采用 `[[概念_解耦式KV缓存与LMCache]]` 的架构应运而生，其将缓存管理从推理引擎中剥离为旁路进程，并结合 CacheBlend 算法在合并多文档时执行选择性重计算以复用已有缓存，实现高效加速。
- **长文本 CPU 卸载下的 I/O 延迟**：在超长上下文推理下，大体积的 KV Cache 需 Offload（卸载）到 CPU 内存。然而在解码时，GPU 等待所需块从 CPU 拷贝回显存的过程（I/O 传输延迟）会产生严重 stall。对此，NVIDIA 与 MIT 联合提出 `[[概念_SparDA预测式KV缓存预取]]` 架构，利用 Forecast 投影预测并异步预取下一层所需的 KV 块，实现数据传输与推理计算的重叠（Overlap）。

### 跨模型路由的缓存失效

传统 KV Cache 由生成它的模型参数决定，模型路由切换后不能直接被另一模型读取。[[概念_跨模型KV缓存转换]] 记录了一种针对同家族稠密全注意力模型的表示映射方案：先在去除 RoPE 位置旋转的空间中拟合跨层线性映射，再恢复目标模型旋转。[原文陈述] 该方案尚未验证跨家族或不匹配 KV 头配置，不能视为通用跨模型缓存互操作方案。

## 关联

- [[入局AI_Infra系统设计与挑战]]（来源）
- [[KV_Cache原理图解]]（详细图解来源）
- [[概念_MLA低秩KV压缩]]
- [[MiniMax_vs_Kimi_注意力路线之争]]
- [[实体_vLLM]]
- [[概念_自注意力复杂度]]
- [[概念_LLM推理两阶段]]
- [[概念_解耦式KV缓存与LMCache]]
- [[概念_SparDA预测式KV缓存预取]]
- [[2026-05-03_How-LLM-inference-works-internally_19deee]]
- [[概念_Delta_Attention与增量矩阵缓存]]
- [[概念_跨模型KV缓存转换]]
