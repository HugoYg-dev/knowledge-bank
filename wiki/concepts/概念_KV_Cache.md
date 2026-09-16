---
type: concept
tags:
- Infra/serving
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
- wiki/sources/2026-08-27_KV-vs-Prefix-vs-Prompt-vs-Semantic-Caching_1a044d0b132124de.md
- wiki/sources/2026-09-03_Attention-Mechanisms-in-LLMs,-clearly-explained_1a068e0f112668fe.md
- wiki/sources/KV_Cache_Engineering_for_LLM_Serving.md
updated: '2026-09-15'
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

## 显存代价与访存墙

$$\text{KV Cache} = 2 \times L \times H \times D \times S \times B \times \text{bytes}$$

- 示例 1：batch=32, head=32, layer=32, dim=4096, seq=2048, float32 → **约 64GB**
- 示例 2：70B 模型在 BF16 精度下，单条 128K 超长上下文的 KV Cache 高达 **约 40GB**，已与 4-bit 量化后的模型整机权重相当。
- 自回归解码瓶颈：生成阶段受制于 GPU 内存带宽（Memory-Bandwidth Bound）而非浮点算力。

## 优化方向与生产工程体系 (12 项核心技术靶点映射)

KV Cache 的单序列物理容量可严格拆解为如下乘积公式：
$$\text{KV Cache 容量} = 2 \times \text{layers} \times \text{kv\_heads} \times \text{head\_dim} \times \text{tokens} \times \text{bytes\_per\_val}$$

大模型生产推理中的 12 项 KV Cache 工程技术精准对应公式中的各个变量，涵盖从模型架构设计到推理引擎调度的全生命周期：

| 优化靶点 | 代表技术 / 机制 | 作用机理与收益 | 工程边界与前置代价 |
| :--- | :--- | :--- | :--- |
| **削减 KV 头数 (`heads`)** | [[概念_GQA分组查询注意力|GQA]] / MQA | 多个 Query 头共享单对或少数对 K/V 头（如 Llama 3.1 70B 8 对 KV 头使显存从 320GB 降至 40GB） | 需在模型训练阶段固化，无法在推理期动态启用 |
| **削减独立层数 (`layers`)** | Cross-Layer Attention (CLA) | 相邻层（如每 2 层）共用同一组已缓存的 K/V 张量，再缩减 2x 层级显存 | 需预训练支持；检查点与推理引擎必须强约定层级所有权 |
| **截断保留序列 (`tokens`)** | [[概念_滑动窗口注意力|滑动窗口 (SWA)]] | 局部注意力层采用环形缓冲区（Ring Buffer）仅保留最近 $W$ 个 Token（如 Gemma 3 5局部+1全局交替） | 超出窗口的历史上下文无法被局部层直接注意力覆盖 |
| **淘汰历史序列 (`tokens`)** | 动态淘汰 (Eviction: H2O, SnapKV, PyramidKV) | 在固定预算下基于累积注意力或观察窗口丢弃非重击者（Heavy Hitters） | **不可逆损失**：多轮 Agent 工具调用、结构化 JSON 解析有失效风险 |
| **压缩表示维度 (`dim`)** | [[概念_MLA多头潜在注意力|MLA (多头潜在注意力)]] | 将隐藏状态压缩为低秩潜向量（Latent Vector），解码时通过吸收投影直接计算，显存压至 MHA 的 5%–13% | 需模型架构原生设计（如 [[entities/实体_DeepSeek|DeepSeek]]），非普通模型推理开关 |
| **固定状态替代线性增长** | [[概念_线性注意力与混合注意力|混合循环架构 (Hybrid)]] | 引入 Mamba 或 Gated DeltaNet 等固定大小状态矩阵（如 $64 \times 64$），仅保留少数全注意力层承载精确检索 | 架构原生决定（如 Qwen3-Next 1:3 交替、Jamba 1:7 交替） |
| **降低数值精度 (`bytes`)** | K/V 量化 (Quantization) | 采用 FP8、INT4 或 KIVI（Key 按特征通道、Value 按 Token 的分组非对称量化），显存减少 50%–75% | 存在量化精度损失；[[entities/实体_vLLM|vLLM]] 支持跳过敏感局部窗口层 |
| **降低访存流量 (不降容量)** | 查询感知稀疏读取 (Quest) | 将缓存分页并记录 Min/Max 边界摘要，Decode 每步先对 Page 估分再仅加载 Top-K 页面，延迟降 7x | **显存容量并未释放**，仅节省 GPU 显存读取带宽与计算量 |
| **消除内存碎片与浪费** | PagedAttention | 借鉴操作系统虚拟内存分页，以固定大小离散 Block 动态分配，显存浪费从 60%–80% 降至 <4% | 需推理引擎底层支持（如 [[entities/实体_vLLM|vLLM]]） |
| **跨并发请求复用** | 自动前缀缓存 (Prefix Caching / RadixAttention) | 基于 Token 块哈希链跨并发请求复用 System Prompt 与 Tool Schema，消除重复存储与 Prefill | 前缀注入动态变量（时间戳/UUID）会导致哈希链失效 |
| **多级存储层级置换** | GPU 到 CPU 内存卸载 (Cache Offloading) | 将被调度挂起或冷会话的 KV 块换出至 Host RAM（如 vLLM `--kv-offloading-size`），按需换回 | 引入 Host-Device 传输延迟；需结合预取与会话亲和性调度 |
| **算子硬件执行加速** | [[概念_FlashAttention]] | 片上 SRAM Tiling 分块与在线增量 Softmax，避免频繁存取全局显存（HBM） | 不改变显存中持久保留的 KV Cache 尺寸，仅加速注意力算子执行 |

### 技术的正交乘法叠加与决策路径
- **乘法叠加效应**：不同靶点的技术可复合生效。例如：GQA（40GB） $\times$ CLA（20GB） $\times$ FP8 量化（10GB） $\times$ 50% Token Eviction $\to$ 最终单序列显存可压至 5GB。
- **生产决策闭环**：
  1. *模型选型阶段*：重点核查 GQA 头数、MLA 潜向量维度与混合循环层比例；
  2. *存量模型部署*：首选验证 FP8 量化与稳定 Prompt 前缀（收益直接且无语义丢失）；
  3. *显存监控排查*：在 PagedAttention 固定显存池机制下，启用量化可能表现为 `nvidia-smi` 显存占用不变，但实际可承载的最大并发 Token 容积成倍提升；
  4. *冷长会话调度*：结合 CPU Offloading 与旁路缓存解耦（如 [[概念_解耦式KV缓存与LMCache|LMCache]]）释放宝贵 GPU 显存。


## 生产应用中的挑战与优化演进

随着大模型在 Agent（智能体）与超长上下文（RAG）场景的落地，传统的 KV Cache 机制暴露出新的痛点：
- **Agent 推理中的冗余传输与计算**：斯坦福大学调研表明，在多轮交互的智能体工作流中，由于每一步都是从头计算，导致每次发送给模型的 Token 有约 **62%** 是重复的系统 Prompt、工具定义和历史文档。这不仅浪费带宽，也造成了极大的 Token 推理开销。为了突破这一瓶颈，采用 `[[概念_解耦式KV缓存与LMCache]]` 的架构应运而生，其将缓存管理从推理引擎中剥离为旁路进程，并结合 CacheBlend 算法在合并多文档时执行选择性重计算以复用已有缓存，实现高效加速。
- **长文本 CPU 卸载下的 I/O 延迟**：在超长上下文推理下，大体积的 KV Cache 需 Offload（卸载）到 CPU 内存。然而在解码时，GPU 等待所需块从 CPU 拷贝回显存的过程（I/O 传输延迟）会产生严重 stall。对此，NVIDIA 与 MIT 联合提出 `[[概念_SparDA预测式KV缓存预取]]` 架构，利用 Forecast 投影预测并异步预取下一层所需的 KV 块，实现数据传输与推理计算的重叠（Overlap）。

### 跨模型路由的缓存失效

传统 KV Cache 由生成它的模型参数决定，模型路由切换后不能直接被另一模型读取。[[概念_跨模型KV缓存转换]] 记录了一种针对同家族稠密全注意力模型的表示映射方案：先在去除 RoPE 位置旋转的空间中拟合跨层线性映射，再恢复目标模型旋转。[原文陈述] 该方案尚未验证跨家族或不匹配 KV 头配置，不能视为通用跨模型缓存互操作方案。

### 四种缓存机制横向解耦 (KV vs Prefix vs Prompt vs Semantic Caching)

在大模型服务技术栈中，四种不同机制常被笼统称为“Caching”，其底层存储对象、命中原理及失效风险存在根本差异：

| 缓存机制 | 存储对象 | 键构造方式 (Key) | 命中与正确性性质 | 典型失效风险 |
| :--- | :--- | :--- | :--- | :--- |
| **1. 基础 KV Cache** | 单请求内部各层注意力 K/V 张量 | 序列位置索引 | 精确计算（正确性中立） | 显存容量瓶颈，请求完成即释放 |
| **2. Prefix Caching** | 服务引擎跨请求复用的 KV 显存块 | Token ID 父子哈希链 (Hash Chain) | 精确匹配（正确性中立，仅影响性能） | 前缀插入动态变量、RAG 块乱序破坏链式哈希 |
| **3. Prompt Caching** | 云厂商托管的前缀 KV 复用（按差异费率计价） | 渲染后前缀文本精确哈希 | 精确匹配（读取 0.1x，写入 1.25x） | 超过 20 块回溯窗口、修改 Tool Schema 顺序、开启 Thinking |
| **4. 语义缓存 (Semantic)** | 最终文本回答字符串 (Response String) | Prompt Embedding 余弦相似度 | **模糊匹配（具有置信风险）** | 否定句与肯定句向量过近、相同模板数值微调引发误答 |

#### 生产环境五大静默缓存失效陷阱（Silent Invalidation）
1. **前缀注入动态变量**：在 System Prompt 头部插入时间戳、Request ID 或动态用户信息，会导致其后所有 Tokens 的链式哈希彻底作废；
2. **Tool Schema 顺序微调**：工具定义通常置于 System Prompt 之前，任何工具声明的增删改序都会推倒重算；
3. **渲染配置动态翻转**：切换 Web Search、Citations 开关或改动 `tool_choice` 会改写底层渲染文本；
4. **历史文本编辑破坏前缀**：应用层压缩摘要会改写历史头部，迫使原本可低成本读取的 Tokens 重新按高费率写入；
5. **跨模型路由导致冷启动**：由于不同模型隐空间不兼容，路由到轻量模型同样无法复用大模型已有缓存。

## 关联

- [[入局AI_Infra系统设计与挑战]]（来源）
- [[KV_Cache原理图解]]（详细图解来源）
- [[sources/2026-08-27_KV-vs-Prefix-vs-Prompt-vs-Semantic-Caching_1a044d0b132124de]]（来源）
- [[概念_MLA低秩KV压缩]]
- [[MiniMax_vs_Kimi_注意力路线之争]]
- [[entities/实体_vLLM]]
- [[概念_自注意力复杂度]]
- [[概念_LLM推理两阶段]]
- [[概念_解耦式KV缓存与LMCache]]
- [[概念_SparDA预测式KV缓存预取]]
- [[2026-05-03_How-LLM-inference-works-internally_19deee]]
- [[概念_Delta_Attention与增量矩阵缓存]]
- [[概念_跨模型KV缓存转换]]
- [[概念_GQA分组查询注意力]]
- [[wiki/sources/2026-09-03_Attention-Mechanisms-in-LLMs,-clearly-explained_1a068e0f112668fe.md]]
- [[wiki/sources/KV_Cache_Engineering_for_LLM_Serving.md]]
