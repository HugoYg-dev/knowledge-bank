---
type: "source"
tags: ["LLM/inference", "Infra/serving", "LLM/arch/attention"]
summary: "系统性解构 LLM 推理生产中管理与压缩 KV Cache 的 12 项工程技术，涵盖模型架构共享、局部与稀疏截断、潜空间压缩、固定状态替换、数值量化、块分页、前缀复用与跨层卸载，并建立按削减目标分类的选型决策框架"
sources: ["raw/articles/KV Cache Engineering for LLM Serving.md"]
updated: "2026-09-15"
---

# 来源摘要：KV Cache Engineering for LLM Serving

## 来源元信息
- **标题**：KV Cache Engineering for LLM Serving
- **作者**：Avi Chawla (Daily Dose of Data Science)
- **发布日期**：2026-09-07
- **原文链接**：https://www.dailydoseofds.com/p/kv-cache-engineering-for-llm-serving/
- **上游物理归档**：`raw/articles/KV Cache Engineering for LLM Serving.md`

---

## 核心要点提炼

1. **KV Cache 显存容量公式与优化靶点解构（The Cache Formula & Taxonomy）**：
   - 每一层注意力的每个保留 Token 均存储一个 Key 与一个 Value。单条序列的原始显存容量公式为：
     $$\text{KV Cache} = 2 \times \text{layers} \times \text{kv\_heads} \times \text{head\_dim} \times \text{tokens} \times \text{bytes\_per\_val}$$
   - 以 Llama 3.1 70B 为例，单条 128K 上下文在 BF16 精度下需要约 **40 GB** 显存；4 条并发全长序列将膨胀至 **160 GB**，远超模型权重自身的显存需求。
   - 生产中的 12 项优化技术精准对应公式中的各个变量：
     - 削减 KV 头数：[[concepts/概念_GQA分组查询注意力|GQA]] 与 MQA；
     - 削减独立层数：跨层注意力（Cross-Layer Attention, CLA）；
     - 削减保留 Token 数：[[concepts/概念_滑动窗口注意力|滑动窗口（Sliding Window）]] 与显式淘汰（Eviction）；
     - 压缩表示维度：[[concepts/概念_MLA多头潜在注意力|MLA（多头潜在注意力）]]；
     - 降低存储精度：数值量化（FP8, INT4, KIVI）；
     - 消除线性增长：[[concepts/概念_线性注意力与混合注意力|混合循环架构（Hybrid Recurrent Layers）]]；
     - 消除碎片与重复：块分页（PagedAttention）与自动前缀复用（Prefix Reuse）；
     - 减少带宽读取（不降容量）：查询感知稀疏读取（Quest）；
     - 释放显存容量：GPU 到 CPU 内存卸载（Cache Offloading）。

2. **模型架构级头数与层数压缩（GQA/MQA 与 Cross-Layer Attention）**：
   - **GQA / MQA**：在 Transformer 层内让多个 Query 头共享单对或少数对 KV 头。Llama 3.1 70B 采用 64 Query 头与 8 KV 头设计，使 128K 上下文下的缓存从 320 GB 缩减至 40 GB。
   - **Cross-Layer Attention (CLA)**：将共享范式从“层内”推广至“跨层”，使相邻 2 层共用一组缓存，在 GQA 基础上再实现 2x 显存缩减。CLA 改变了模型前向计算图，必须在预训练期训练完成，且推理引擎必须严格匹配层级所有权逻辑。

3. **序列长度截断与选择性淘汰（Sliding Windows 与 Eviction）**：
   - **滑动窗口注意力（SWA）**：将局部注意力层限制为仅保留最近 $W$ 个 Token 的环形缓冲区（Ring Buffer）。如 Gemma 3 采用“5 个局部层（1024 窗口）+ 1 个全局层（128K 全局）”的周期性交替设计，大幅减缓整体显存增速。
   - **动态淘汰机制（Eviction）**：在固定显存预算下剔除历史条目：
     - **H2O**：保留最近局部窗口以及累积注意力权重最高的“重击者”（Heavy Hitters）；
     - **SnapKV**：利用 Prompt 末尾观测窗口筛选重要前缀；
     - **PyramidKV**：依据浅层关注全局、深层关注局部的规律，为浅层分配大预算、深层分配小预算。
   - *风险边界*：淘汰具有不可逆的上下文损失风险，在 Agent 多轮工具调用、结构化 JSON 解析与延迟引用（Delayed Reference）场景下易产生静默失效。

4. **潜空间低秩压缩与混合循环模型（MLA 与 Hybrid Architectures）**：
   - **[[concepts/概念_MLA多头潜在注意力|MLA（Multi-head Latent Attention）]]**：不直接缓存完整的 Key 和 Value，而是将隐状态投影压缩为极低维度的潜向量（Latent Vector）及解耦 RoPE Key。[[entities/实体_DeepSeek|DeepSeek-V2/V3]] 借此实现 93.3% 的 KV Cache 显存缩减与 5.76x 吞吐提升。
   - **混合架构（Hybrid Recurrent）**：引入 Mamba 或 Gated DeltaNet 等线性循环层，其内部状态为固定大小矩阵（如 $64 \times 64$），不随序列长度增长。Qwen3-Next（3 个 DeltaNet 层交替 1 个全注意力层）将 128K 上下文的增长型缓存从 12 GB 压低至 3 GB；Jamba（1:7 比例交替）在 256K 序列下仅需 4 GB 缓存（对比 Mixtral 的 32 GB）。

5. **稀疏读取与数值量化（Quest Sparse Reads 与 K/V Quantization）**：
   - **Quest（查询感知稀疏读取）**：将缓存分页并存储每页键向量的最大/最小值边界，Decode 每步先对 Page 边界快速估分，仅加载 Top-K 候选页面进行注意力运算。实现高达 7.03x 的注意力延迟下降，但全量缓存依然驻留显存（不节省容量）。
   - **K/V 量化**：采用 FP8（减少 50% 显存）或 INT4（减少 75% 显存）。KIVI 提出对 Key 按特征通道（Per-channel）、对 Value 按 Token（Per-token）的分组非对称量化，实现 2-bit 极限压缩。[[entities/实体_vLLM|vLLM]] 原生支持 `--kv-cache-dtype fp8` 及局部窗口敏感层的 `--kv-cache-dtype-skip-layers sliding_window` 保护。

6. **服务引擎调度层优化（Paging, Prefix Reuse & Cache Offloading）**：
   - **PagedAttention**：引入虚拟内存分页机制，将 KV Cache 划分为离散物理块（Block），彻底消除传统预分配导致的显存碎片，使浪费率趋近于零。
   - **自动前缀复用（Automatic Prefix Caching, APC）**：针对多轮对话中的 System Prompt 和 Tool Schema，以 Token 块父子链哈希为 Key 跨并发请求复用已计算缓存，消减重复 Prefill 算力与显存副本。
   - **GPU 到 CPU 内存卸载（Cache Offloading）**：将因调度阻塞或空闲会话的冷 KV 块换出至 Host RAM（如 vLLM `--kv-offloading-size 16 --kv-offloading-backend native`），以 PCIe 传输延迟换取单卡更高的并发会话承载量。

7. **正交组合法则与生产选型决策矩阵**：
   - **乘法组合效应**：不同层级的技术可协同叠加，例如 GQA（40GB） $\times$ CLA（20GB） $\times$ FP8（10GB） $\times$ 50% Eviction $\to$ 最终缩减至 5GB。
   - **生产决策闭环**：
     1. **模型选型期**：审视 KV 头数、局部/全局层比例、MLA 潜向量维度及循环层交替模式；
     2. **存量模型部署**：首选 FP8 量化与标准前缀对齐（无精度损失风险）；
     3. **显存监控假象**：固定大小显存池（Fixed Block Pool）下启用 FP8 可能不会改变 `nvidia-smi` 显存占用，但可容纳的并发 Token 数量翻倍；
     4. **长尾与冷会话处理**：引入 CPU Offload 与预测预取机制（如 [[concepts/概念_解耦式KV缓存与LMCache|LMCache]] 与 [[concepts/概念_SparDA预测式KV缓存预取|SparDA]]）。

---

## 关键引文

> "Loading an LLM is only the first part of GPU memory planning. Model weights stay roughly fixed during inference. The KV cache does not. It grows with every token in the sequence."

> "For Llama 3.1 70B, one 128K-token sequence requires about 40 GB of BF16 KV cache. Four full-length sequences would add another 160 GB, before accounting for model weights and serving overhead."

> "A faster attention kernel doesn't create room for another sequence unless it also stores fewer bytes."

> "When choosing a model -> Inspect KV head count, local and global layer ratios, latent-attention dimensions, and recurrent layers... When serving an existing model -> Test FP8 first, then standardize prefixes."

---

## 关联页面与实体图谱

- **核心概念**：
  - [[concepts/概念_KV_Cache|概念_KV_Cache]]（KV Cache 基础原理、显存公式与生产治理总览）
  - [[concepts/概念_GQA分组查询注意力|概念_GQA分组查询注意力]]（组内共享 KV 头设计与 MHA/MQA 平衡）
  - [[concepts/概念_MLA多头潜在注意力|概念_MLA多头潜在注意力]]（低秩潜向量压缩与矩阵吸收机制）
  - [[concepts/概念_滑动窗口注意力|概念_滑动窗口注意力]]（局部注意力环形缓冲区与全局层混合架构）
  - [[concepts/概念_线性注意力与混合注意力|概念_线性注意力与混合注意力]]（Mamba / Gated DeltaNet 固定状态矩阵演进）
  - [[concepts/概念_LLM推理两阶段|概念_LLM推理两阶段]]（Prefill 与 Decode 阶段对 KV Cache 的读写特征）
  - [[concepts/概念_解耦式KV缓存与LMCache|概念_解耦式KV缓存与LMCache]]（跨节点/层级的 KV 缓存旁路解耦与重计算）
- **核心实体**：
  - [[entities/实体_vLLM|实体_vLLM]]（PagedAttention、FP8 量化、前缀复用与 CPU 卸载的开源参考实现）
  - [[entities/实体_DeepSeek|实体_DeepSeek]]（MLA 与压缩稀疏注意力的开创实践）

---

> 📎 **物理文献**：[[raw/articles/KV Cache Engineering for LLM Serving.md]]
