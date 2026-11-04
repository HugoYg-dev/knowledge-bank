---
type: "source"
tags: ["LLM/inference", "Infra/serving"]
summary: "Daily Dose of DS 视觉图解 KV Cache 显存容量公式与 6 类压缩/量化技术路径：Llama 3.1 70B 显存基线、GQA/MQA 减头数、CLA 减层数、滑动窗口/淘汰减 Token、MLA 压缩维度及 FP8/INT8 量化压缩每个值字节数"
sources: ["raw/articles/2026-10-23_6-KV-cache-quantization-approaches,-explained-visually_1a16b008a2158dca.md"]
updated: "2026-11-04"
---

# 来源摘要：6 KV cache quantization approaches, explained visually

## 来源信息

- **原文标题**：6 KV cache quantization approaches, explained visually:
- **通讯来源**：Daily Dose of DS (Avi Chawla) `<avi@dailydoseofds.com>`
- **原文链接**：[Daily Dose of DS 官网长文](https://www.dailydoseofds.com/p/kv-cache-engineering-for-llm-serving/)
- **发布日期**：2026-10-23
- **邮件 ID**：`1a16b008a2158dca`
- **文章 ID**：`1a16b008a2158dca:2`
- **内容层级**：`web_canonical`
- **物理文献**：[[raw/articles/2026-10-23_6-KV-cache-quantization-approaches,-explained-visually_1a16b008a2158dca.md]]

---

## 核心要点（Executive Summary）

1. [原文陈述] **KV Cache 显存容量物理公式与基线压力**：
   - 单序列物理显存容量公式为：$\text{KV Cache} = 2 \times \text{layers} \times \text{kv\_heads} \times \text{head\_size} \times \text{tokens} \times \text{bytes\_per\_value}$（系数 2 计入 Key 与 Value，BF16 占 2 字节，FP8 占 1 字节）。
   - 以 Llama 3.1 70B（64 Query 头，8 对 KV 头）为例，单条 128K 上下文在 BF16 精度下即需约 40GB KV Cache，若使用 64 KV 头的标准 MHA 则需高达 320GB；4 条全长并发请求仅 KV Cache 即可消耗 160GB 显存，带来 GPU 显存容量与内存带宽访存墙双重瓶颈。
2. [原文陈述] **基于显存公式变量维度的 6 类压缩/量化技术路径分类**：
   - **削减 KV 头数（`kv_heads`）**：[[concepts/概念_GQA_分组查询注意力|GQA]] 与 MQA，多个 Query 头共享单对或几对 KV 头，大幅缩减每个注意力层维护的头数；
   - **削减独立层数（`layers`）**：Cross-Layer Attention (CLA)，在预训练期固化相邻层（如每 2 层）共用同一组缓存，模型层面直接将独立层级缓存减半；
   - **缩减保留序列（`tokens`）**：[[concepts/概念_滑动窗口注意力|滑动窗口 (SWA)]]（如 Gemma 3 采用 5 局部 + 1 全局交替架构，局部层仅保留最新 1024 Token）与动态淘汰（Eviction: H2O 重击者保留、SnapKV 观察窗口预筛、PyramidKV 跨层金字塔预算）；
   - **压缩表示维度（`head_size` / `width`）**：[[concepts/概念_MLA_多头潜在注意力|MLA (多头潜在注意力)]]，将隐藏状态压缩为低秩潜向量与解耦 RoPE 键存储，DeepSeek-V2 实现 93.3% 缓存缩减；
   - **降低数值精度（`bytes_per_value`）**：[[concepts/概念_量化|KV 量化]]（FP8 减半、INT4 压缩至 25%，以及 KIVI 的 Key 按特征通道、Value 按 Token 的分组量化）；
   - **固定状态替代线性增长**：混合循环架构（Hybrid Recurrent Layers，如 Mamba、Qwen3-Next 的 Gated DeltaNet 与 Jamba 1:7 交替），除少数全局全注意力层外保持固定大小状态。
3. [原文陈述] **服务引擎调度与显存分配治理（无损系统级优化）**：
   - **PagedAttention**：将显存划分为固定大小离散块，按需动态分配，消除内部内存碎片，实现高效内存复用；
   - **Prefix Caching（前缀复用）**：通过 Token 块哈希链跨并发请求复用 System Prompt 与 Tool Schema 等公共前缀，消除重复存储与 Prefill 计算；
   - **Cache Offloading（显存卸载）**：将挂起或冷会话的 KV 块换出至 Host CPU 内存，以 PCIe 传输延迟换取 GPU 显存容量。
4. [原文陈述] **稀疏注意力（Sparse Attention）与显存容量占用的本质区别**：
   - Quest 等查询感知稀疏读取（Query-aware sparse reads）通过分页维护 Min/Max 边界摘要，Decode 阶段仅计算 Top-K 页面以降低访存流量和注意力计算延迟（Quest 实现最高 7.03x 延迟降低），但**并未物理释放或删除显存中的 KV 张量**，因此当 GPU 显存打满时，单纯更快的注意力算子无法为新序列腾出空间；
   - 相比之下，量化、淘汰（Eviction）与架构级头数/维度压缩才直接物理减少驻留显存字节数。
5. [原文陈述] **技术的正交乘法叠加与生产落地决策闭环**：
   - 各技术作用于公式不同变量，可复合叠加（例如 GQA 40GB $\times$ CLA 20GB $\times$ FP8 10GB $\times$ 50% Token 淘汰 $\to$ 最终单序列显存可压至约 5GB）；
   - **权衡边界**：CLA/MLA/Hybrid 需模型架构原生支持或额外训练；FP8/INT4 引入量化误差；Eviction 抛弃上下文可能破坏多轮 Agent 工具调用与长依赖；
   - **落地原则**：模型选型期关注 GQA 头数与 MLA 维度；已有模型部署首选 FP8 量化与稳定 Prompt 前缀；延迟瓶颈排查访存稀疏；冷长会话采用 Offloading。

---

## 关键引文

> "The cache occupies GPU memory, and the attention layers must repeatedly read it while generating new tokens."
>
> "Sparse attention needs a separate line. It may read fewer tokens without removing them from memory, so it can cut attention work while leaving cache capacity unchanged. This distinction matters when the GPU is full. A faster attention kernel doesn’t create room for another sequence unless it also stores fewer bytes."
>
> "When choosing a model → Inspect KV head count, local and global layer ratios, latent-attention dimensions, and recurrent layers. These determine the starting cache before deployment. When serving an existing model → Test FP8 first, then standardize prefixes."

---

## 关联概念与实体

- **关联概念**：
  - [[concepts/概念_KV_Cache_键值缓存|概念_KV_Cache_键值缓存]]：自回归自注意力张量缓存机制、容量计算公式与 12 类工程优化靶点。
  - [[concepts/概念_量化|概念_量化]]：FP8、INT4 与 KIVI 分组非对称量化技术。
  - [[concepts/概念_GQA_分组查询注意力|概念_GQA_分组查询注意力]]：MHA、MQA 与 GQA 的 KV 头数共享架构权衡。
  - [[concepts/概念_MLA_多头潜在注意力|概念_MLA_多头潜在注意力]]：低秩潜向量压缩与计算解耦。
  - [[concepts/概念_滑动窗口注意力|概念_滑动窗口注意力]]：局部窗口与环形缓冲区机制。
  - [[concepts/概念_自注意力复杂度|概念_自注意力复杂度]]：自注意力计算与内存复杂度。
  - [[concepts/概念_线性注意力与混合注意力|概念_线性注意力与混合注意力]]：循环状态与全注意力交替架构。
- **关联实体**：
  - [[entities/实体_vLLM|实体_vLLM]]：支持 PagedAttention、Prefix Caching、FP8 KV Cache 与 CPU Offloading 的代表性开源推理引擎。
  - [[entities/实体_DeepSeek|实体_DeepSeek]]：MLA 架构与压缩稀疏注意力发明者。

---

> 📎 **物理文献**：[[raw/articles/2026-10-23_6-KV-cache-quantization-approaches,-explained-visually_1a16b008a2158dca.md]]
