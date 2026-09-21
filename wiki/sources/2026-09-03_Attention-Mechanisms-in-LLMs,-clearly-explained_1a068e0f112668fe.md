---
type: "source"
tags:
  - "LLM/arch/attention"
  - "LLM/inference"
summary: "系统解析 LLM 注意力机制演化与 KV Cache 显存优化：涵盖 MHA、MQA、GQA、MLA 的架构压缩取舍，FlashAttention 计算访存优化，SWA 与 NSA 稀疏机制，以及 PagedAttention 与 RadixAttention 服务引擎管理"
sources:
  - "raw/articles/2026-09-03_Attention-Mechanisms-in-LLMs,-clearly-explained_1a068e0f112668fe.md"
updated: "2026-09-15"
---

# Attention Mechanisms in LLMs, clearly explained

- **来源**: Daily Dose of DS
- **作者**: Avi Chawla (`avi@dailydoseofds.com`)
- **原文链接**: [Daily Dose of DS - LLMOps Crash Course](https://www.dailydoseofds.com/llmops-crash-course-part-1/)
- **发布日期**: 2026-09-03
- **邮件/文章标识**: `1a068e0f112668fe:2`

---

## 核心要点

1. **核心制约因素是 [[concepts/概念_KV_Cache_键值缓存|KV Cache]] 的内存占用**：自注意力赋予模型全局依赖建模能力，但在自回归解码时必须缓存历史 token 的 Key 与 Value。以 70B 模型（BF16 精度）为例，单条 128K 上下文的 KV Cache 高达约 40 GB，几乎等同于 4-bit 量化后的整机模型权重。LLM 解码的真正瓶颈在于 GPU 显存带宽与容量（Memory-Bandwidth-Bound），而非计算 FLOPs。
2. **架构级 KV 压缩取舍（MHA → MQA → GQA → MLA）**：
   - **MHA (Multi-Head Attention)**：每个 Query Head 拥有独立的 Key/Value 投影（如 32 层 × 32 头 = 1,024 个独立 KV 张量/token），表达力最高但显存开销极大。
   - **MQA (Multi-Query Attention)**：所有 Query Head 强制共享 1 个 Key Head 和 1 个 Value Head，KV Cache 缩减至 $1/H$（如 32x），显著降低读取带宽，但牺牲了模型的召回与表达质量（Falcon、PaLM 采用）。
   - **[[concepts/概念_GQA_分组查询注意力|GQA (Grouped-Query Attention)]]**：折中方案，Query Head 分组共享 KV（例如 32 个 Query 头分 8 组，KV Cache 减少为 1/4），在保持接近 MHA 质量的前提下显著降低显存开销，成为主流开源大模型标配（Llama 2/3、Mistral、Qwen、Gemma）。
   - **[[concepts/概念_MLA_多头潜在注意力|MLA (Multi-Head Latent Attention)]]**：[[entities/实体_DeepSeek|DeepSeek]] 提出的创新机制，不靠减少头数，而是将高维 KV 投影至低秩潜空间（Low-Rank Latent Space）进行缓存，计算时动态升维解压。KV Cache 降至 MHA 的 5%–13%，推理质量匹敌甚至超越 MHA。
3. **计算核函数访存优化（[[concepts/概念_FlashAttention_快速注意力|FlashAttention]]）**：数学等价的前提下，通过 SRAM Tiling（分块分片）与在线增量 Softmax，避免将 $N \times N$ 注意力矩阵反复写回 HBM 显存，大幅消除内存 IO 搬运瓶颈，成为现代所有推理引擎的标准底层算子。
4. **长序列计算稀疏化（Sparse Attention）**：针对全注意力 $O(N^2)$ 复杂度，通过稀疏化扩展上下文：
   - **SWA (Sliding Window Attention)**：滑动窗口局部注意力（如 Mistral），仅计算邻近 $W$ 个 token。
   - **NSA (Native Sparse Attention)**：[[entities/实体_DeepSeek|DeepSeek]] 2025 年提出，在预训练阶段原生训练稀疏注意力，包含全局压缩粗粒度、关键块细粒度选择和局部滑动窗口三条并行分支，原生支持超长上下文（如 Qwen2.5-1M 等均采用稀疏注意力）。
5. **服务引擎级显存管理与前缀共享（[[entities/实体_vLLM|vLLM]] PagedAttention & SGLang RadixAttention）**：
   - **PagedAttention**：模仿操作系统虚拟内存分页机制，按需分配固定大小的物理显存块，将显存浪费与碎片率从 60%–80% 降至 4% 以下。
   - **RadixAttention**：利用基数树（Radix Tree）索引 KV Cache 前缀，使多轮对话与公共 System Prompt 命中率达到 75%–95%，完全避免重复前缀计算。

---

## 注意力机制与 KV 优化全景对比

| 优化层级 | 技术机制 | 核心原理 | 显存 / 速度收益 | 代价与权衡 | 代表模型 / 工具 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **模型架构** | **MHA** | 每个 Head 独立 $W_Q, W_K, W_V$ | 基准开销（最大） | 显存爆炸，长文本扩展受限 | 原生 Transformer, GPT-3 |
| **模型架构** | **MQA** | 所有 Query Head 共享 1 组 $K, V$ | KV Cache 缩减 $1/H$（如 32x） | 表达能力下降，复杂任务掉点 | Falcon, PaLM |
| **模型架构** | **[[concepts/概念_GQA_分组查询注意力|GQA]]** | Query 分组，组内共享 1 组 $K, V$ | KV Cache 缩减至组数比例（如 4x） | 质量几乎无损，显存大幅降低 | Llama 2/3, Mistral, Qwen |
| **模型架构** | **[[concepts/概念_MLA_多头潜在注意力|MLA]]** | 低秩潜空间压缩 KV，解码时动态投影恢复 | KV Cache 降至 MHA 的 5%–13% | 增加少量解压计算 FLOPs | DeepSeek-V2/V3/R1 |
| **计算内核** | **[[concepts/概念_FlashAttention_快速注意力|FlashAttention]]** | 片上 SRAM 分块 (Tiling) + 在线 Softmax | 显存 IO 访问减少数倍，速度提升 2-4x | 无数学近似，需专用 GPU Kernel | 工业界所有主流推理框架 |
| **稀疏计算** | **SWA** | 限制只对局部 $W$ 个 token 交互 | 降低长序列计算量至 $O(N \times W)$ | 截断长距离上下文依赖 | Mistral |
| **稀疏计算** | **NSA** | 预训练多分支稀疏（粗粒度+细粒度+局部） | 支持百万级 Token 高效前向计算 | 需在预训练阶段原生训练 | DeepSeek (2025) |
| **推理引擎** | **PagedAttention** | 虚拟内存分页映射，离散块分配 | 碎片率从 60%-80% 降至 <4% | 引擎调度与页表维护 | [[entities/实体_vLLM|vLLM]] |
| **推理引擎** | **RadixAttention** | 基数树前缀匹配与 KV 显存块跨请求复用 | 多轮请求命中率 75%–95% | 维护树结构与 LRU 淘汰逻辑 | SGLang |

---

## 关联

- **相关概念**: [[concepts/概念_KV_Cache_键值缓存|概念_KV_Cache]]、[[concepts/概念_GQA_分组查询注意力|概念_GQA分组查询注意力]]、[[concepts/概念_MLA_多头潜在注意力|概念_MLA多头潜在注意力]]、[[concepts/概念_FlashAttention_快速注意力|概念_FlashAttention]]
- **相关实体**: [[entities/实体_vLLM|实体_vLLM]]、[[entities/实体_DeepSeek|实体_DeepSeek]]、[[entities/实体_DeepSeek-V3|实体_DeepSeek-V3]]、[[entities/实体_DeepSeek-R1|实体_DeepSeek-R1]]
- **相关来源**: [[wiki/sources/2026-07-07_Rethinking-KV-caching-for-production-inference_19f3d7.md]]、[[wiki/sources/2026-08-27_KV-vs-Prefix-vs-Prompt-vs-Semantic-Caching_1a044d0b132124de.md]]

---
> 📎 **物理文献**：[[raw/articles/2026-09-03_Attention-Mechanisms-in-LLMs,-clearly-explained_1a068e0f112668fe.md]]
