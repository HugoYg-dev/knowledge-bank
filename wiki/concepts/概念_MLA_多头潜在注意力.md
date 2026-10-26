---
type: concept
tags:
  - LLM/arch/attention
  - LLM/inference
summary: "MLA（Multi-Head Latent Attention）通过低秩隐空间投影与解耦 RoPE 机制将 KV Cache 压缩至 MHA 的 5%–13%，并在推理自回归解码期通过矩阵吸收实现广播计算加速"
sources:
  - wiki/sources/2025年七大顶流大模型架构.md
  - wiki/sources/从DeepSeek-V3到Kimi_K2_八种现代LLM架构大比较.md
  - wiki/sources/2026-09-03_Attention-Mechanisms-in-LLMs,-clearly-explained_1a068e0f112668fe.md
  - wiki/sources/DeepSeek开源FlashMLA从原理到代码详解.md
  - wiki/sources/从代码角度彻底理解DeepSeek_MLA算法.md
  - wiki/sources/DeepSeek_MLA矩阵吸收原理.md
updated: '2026-10-26'
aliases:
  - MLA
  - Multi-head Latent Attention
  - 多头潜在注意力
  - 概念_MLA多头潜在注意力
---

# 概念_MLA_多头潜在注意力

MLA（Multi-Head Latent Attention，多头潜在注意力）是 DeepSeek 在 DeepSeek-V2 中首次引入并在 DeepSeek-V3 / R1 中持续采用的核心注意力架构变体。其核心设计理念是通过**低秩潜在向量投影（Low-Rank Compression）+ 解耦 RoPE 位置编码（Decoupled RoPE）+ 推理矩阵吸收（Matrix Absorption）**，在保持甚至超越多头注意力（MHA）建模容量的同时，将推理期 [[concepts/概念_KV_Cache_键值缓存|KV Cache]] 的显存占用大幅缩减至原生 MHA 的 **5%–13%**。

![DeepSeek MLA 核心架构与计算图谱](https://pic2.zhimg.com/v2-acae8afdfa53ee0d6e37dad51c810453_1440w.jpg)

---

## 1. 核心设计与工作机制

### 1.1 低秩隐空间压缩（Low-Rank Latent Compression）
传统注意力机制在自回归生成阶段必须缓存历史所有 Token 的全维 Key 与 Value 张量。在超大上下文（如 128K）与高并发场景下，GPU 显存带宽与容量成为绝对瓶颈。与 [[concepts/概念_GQA_分组查询注意力|GQA]] 靠裁剪 Key/Value 头数的方式不同，MLA 保持了丰富的多头表示（如 128 头），但通过线性降维将特征压缩至低秩潜在空间：

- **KV 压缩**：将输入状态 $h_t$ 投影至低维向量 $c_t^{KV} \in \mathbb{R}^{d_c}$（其中 $d_c \ll H \times d_h$，如 DeepSeek-V3 中 $d_c = 512$，压缩比达 1/14）：
  $$c_t^{KV} = W^{DKV} h_t$$
  自回归解码时，KV Cache **仅需存储 $c_t^{KV}$ 与轻量位置向量**，不再存储展开后的全尺寸多头张量。
- **Query 压缩**：训练阶段对 Query 同样进行降维投影（$c_t^Q = W^{DQ} h_t \in \mathbb{R}^{d'_c}$），以此大幅降低训练反向传播期间的激活值显存占用（Activation Memory）。推理期 Query 则直接投影以最大化计算效率。

### 1.2 解耦 RoPE 机制（Decoupled Rotary Position Embedding）
- **传统 RoPE 与低秩压缩的冲突**：RoPE 位置编码引入了随时间步 $t$ 变化的旋转矩阵 $\mathcal{R}_t$。由于旋转矩阵与位置强相关，数学上无法被吸收进静态的升维矩阵中；若对压缩后的张量直接施加 RoPE，自回归时将无法通过矩阵吸收避免多头 KV 展开，低秩压缩的显存红利将荡然无存。
- **维度显式解耦分离**：MLA 将 Query 与 Key 的投影通道正交切分为两部分：
  1. **非位置通道 (`nope`)**：不携带位置编码（维度为 $d_h = 128$），完全参与低秩压缩与矩阵吸收；
  2. **解耦 RoPE 通道 (`rope`)**：专门用于承载旋转位置编码（维度为 $d_h^R = 64$）。所有注意力头共享一个独立的 Key 位置投影通道（$k_{pe} \in \mathbb{R}^{d_h^R}$），兼顾位置感知与极小开销。

### 1.3 推理阶段的矩阵吸收（Matrix Absorption）
在推理自回归生成时，DeepSeek 采用**矩阵吸收（Matrix Absorption）**优化，避免在每一步解码时将 $c_t^{KV}$ 动态升维展开为多头 Key/Value：

- **Key 侧吸收**：将 Key 的升维投影矩阵 $W^{UK}$ 提前与 Query 的非位置向量相乘（即 $q'_{nope} = q_{nope} W^{UK}$），注意力得分计算退化为：
  $$\text{Score} = q'_{nope} \cdot (c_t^{KV})^T + q_{pe} \cdot (k_{pe})^T$$
  计算时 Key 不含多头维度 $H$，退化为矩阵广播计算，大幅节省了显存访问开销。
- **Value 侧吸收**：计算输出时，直接将注意力权重与压缩潜向量相乘后，再经由 Value 升维矩阵 $W^{UV}$ 与输出矩阵 $W^O$ 联合变换。

---

## 2. 算子优化与工业级落地（FlashMLA）

为了在底层硬件充分释放 MLA 的吞吐潜力，DeepSeek 于 2025 年 2 月开源了针对 Hopper 架构的计算内核 [[entities/实体_FlashMLA|FlashMLA]]：
- **底层架构**：基于 NVIDIA CUTLASS 模板库深度调优，强制支持 BF16 精度与 Hopper 架构（SM90，如 NVIDIA H100 / H800）；
- **执行协同**：提供 `get_mla_metadata` 与 `flash_mla_with_kvcache` 接口，支持 Paged KV Cache 分页显存管理与多 SM 分块并发调度，彻底解决了生产环境下长文本解码的算子瓶颈。

---

## 3. 注意力变体横向权衡对比

| 架构机制 | 代表模型 | KV 缓存对象 | KV Cache 显存占用 | 建模表达能力 | 推理瓶颈特点 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **MHA** | 原生 Transformer, GPT-3 | 全量独立多头 $K, V$ | 100%（基准最大） | 基准最高 | 严重受限于显存容量与读写带宽 |
| **MQA** | Falcon, PaLM | 共享 1 组单头 $K, V$ | $\approx 1/H$（极低） | 明显下降（复杂任务易掉点） | 计算简单，但语义容量受限 |
| **[[concepts/概念_GQA_分组查询注意力\|GQA]]** | Llama 2/3, Mistral, Qwen | 分组共享 $G$ 组 $K, V$ | $G/H$（如 25%） | 接近 MHA | 开源大模型主流标配 |
| **MLA** | DeepSeek-V2/V3/R1, Kimi K2 | 压缩潜向量 $c_t^{KV}$ + $k_{pe}$ | **5%–13%**（极低） | **匹敌甚至超越 MHA** | 增加少量投影计算，消除带宽瓶颈 |

---

## 4. 应用模型与关联图谱

### 4.1 核心落地模型
- [[entities/实体_DeepSeek-V3|DeepSeek-V3]]：671B MoE 基础模型，全面采用 MLA 架构；
- [[entities/实体_DeepSeek-R1|DeepSeek-R1]]：基于 DeepSeek-V3 架构的推理大模型；
- [[entities/实体_DeepSeek_V2|DeepSeek-V2]]：MLA 机制的首发模型；
- [[entities/实体_Kimi_K2|Kimi K2]]：基于 DeepSeek 架构扩展至 1 万亿参数规模；
- [[entities/实体_Kimi_Linear|Kimi Linear]]：采用 KDA（Delta Attention）与 MLA（3:1）的混合注意力架构。

### 4.2 关联概念与实体
- **关联概念**: 
  - [[concepts/概念_KV_Cache_键值缓存|概念_KV_Cache]] — MLA 旨在解决的核心瓶颈；
  - [[concepts/概念_GQA_分组查询注意力|概念_GQA_分组查询注意力]] — MLA 的主要性能对标架构；
  - [[concepts/概念_自注意力复杂度|概念_自注意力复杂度]] — 理论计算与访存复杂度分析；
  - [[concepts/概念_MoE混合专家|概念_MoE混合专家]] — DeepSeek 双引擎之一。
- **关联实体**:
  - [[entities/实体_DeepSeek|实体_DeepSeek]] — 架构提出者；
  - [[entities/实体_FlashMLA|实体_FlashMLA]] — 专用硬件加速内核。
- **相关支撑来源**:
  - [[sources/DeepSeek开源FlashMLA从原理到代码详解|来源：DeepSeek开源FlashMLA从原理到代码详解]]
  - [[sources/从代码角度彻底理解DeepSeek_MLA算法|来源：从代码角度彻底理解DeepSeek_MLA算法]]
  - [[sources/DeepSeek_MLA矩阵吸收原理|来源：DeepSeek_MLA矩阵吸收原理]]
  - [[sources/2026-09-03_Attention-Mechanisms-in-LLMs,-clearly-explained_1a068e0f112668fe|来源：Attention Mechanisms in LLMs, clearly explained]]
  - [[sources/从DeepSeek-V3到Kimi_K2_八种现代LLM架构大比较|来源：从DeepSeek-V3到Kimi K2：八种现代 LLM 架构大比较]]
  - [[sources/2025年七大顶流大模型架构|来源：2025年七大顶流大模型架构]]
