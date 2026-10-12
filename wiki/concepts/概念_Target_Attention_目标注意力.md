---
type: "concept"
tags: ["LLM/arch/attention", "Recommendation"]
summary: "在推荐系统长序列与精排建模中，使候选 Target 侧 Token 单向聚合用户长序列上下文、而省去历史序列间全自注意力的高效注意力机制，大幅缩减二次方计算复杂度与显存开销"
aliases:
  - "Target Attention"
  - "目标注意力"
  - "Target-Attention"
  - "概念_Target_Attention"
sources: ["wiki/sources/MTFM_美团统一推荐基座大模型在外卖多业务场景的落地实践.md"]
updated: "2026-10-12"
---

# 概念：Target Attention 目标注意力

## 定义

**Target Attention（目标注意力）** 是工业级推荐系统长序列行为建模与深度精排架构中的一种专用注意力机制。

在传统的标准自注意力（Full Self-Attention）中，全序列内任意两个 Token 之间均需要进行注意力权重计算，导致计算与显存开销随序列长度呈现平方级增长（$O(N^2)$）。而在推荐任务中，最终预估的 CTR/CVR 结果高度依赖于当前待预估的候选目标（Target，如待推荐的商品、商家或券包）。Target Attention 的核心思想是**算力非对称分配**：仅让候选 Target Token 作为 Query 去检索并聚合全序列（包括用户长期与实时行为历史）的 Key/Value 信息，而省略历史行为序列内部相互之间的注意力计算，将复杂度从 $O(N^2)$ 降低到 $O(M \cdot N)$（其中 $M \ll N$ 为候选 Target 数量）。

## 核心机制与演进脉络

### 1. 经典起源与发展

- **DIN（Deep Interest Network, 2018）**：阿里巴巴提出局部激活单元（Local Activation Unit），针对不同候选广告动态计算用户历史行为的注意力权重，开创了推荐系统引入 Target-Aware 注意力的先河。
- **STCA 与 OneRec V2（LazyDecoder, 2025-2026）**：快手与抖音在大规模长序列模型中验证了 Target Attention 可以用显著低于 Full Attention 的算力成本实现近乎无损的信息提取。

### 2. 混合注意力架构（Hybrid Target Attention）

单纯全部使用 Target Attention 会导致用户行为序列内部缺乏上下文交互与演化建模。为此，美团在 **[[entities/实体_MTFM|MTFM]]** 中借鉴前沿 LLM（如 Qwen3-Next）混合注意力思想，提出了交错堆叠结构：
- **Block 结构划分**：采用 4 个 Block 共 16 层网络，各 Block 内部按 **Target:Full = 3:1** 的比例配置（即 1 层 Full Attention 负责全序列全局依赖聚合，紧接着 3 层 Target Attention 专注候选相关特征提取）；
- **收益**：相比全 Full Attention 架构，混合结构使显存大幅降低，Batch Size 可扩大 1.7 倍，训练样本吞吐达到 2.9 倍，同时保持了最优的 GAUC 指标。

### 3. Target Scale-Up 与表征防坍缩

在工业多场景统一基座中，单个 Target Token 包含的特征维度（用户环境、上下文、候选商品及交叉特征）远高于序列中的单个行为，将其强行压入单个 Token 会引发表征过度压缩。
- **AutoSplit 映射**：将每个 Target 的多维特征通过线性映射拆分为多个（如 4 个）Target Tokens；
- **Target Token Mixing**：各个拆分后的 Target Token 独立与用户长序列进行 Cross Attention 计算；为防止多个 Target Token 在相同 KV 驱动下收敛到高度同质化的冗余表征（表征坍缩），引入低开销的 Mixing 模块进行目标间交互，迫使模型学习多样化的兴趣侧面。

## 优劣势与工程权衡

| 维度 | Full Self-Attention | Target Attention | 混合架构 (Target:Full=3:1) |
| :--- | :--- | :--- | :--- |
| **计算复杂度** | $O(N^2)$（$N$ 为千级至万级序列） | $O(M \cdot N)$（$M \ll N$） | 兼顾全局语义与低开销 |
| **显存占用** | 极高（易受限于 KV 显存） | 极低（无需维护大自注意力矩阵） | 显著低于 Full Attention |
| **用户序列交互** | 完备建模，但存在较多冗余 | 缺失历史行为内部的上下文交互 | 周期性重置并校准序列交互 |
| **适用场景** | 序列理解与语言建模 | 传统单目标轻量召回/精排 | 工业级千级长序列多场景基座 |

## 关联概念与实体

- **上游基础**：[[concepts/概念_Transformer架构]]、[[concepts/概念_自注意力复杂度]]
- **代表实践**：[[entities/实体_MTFM]]（美团统一推荐基座大模型）
- **关联机制**：[[concepts/概念_GQA_分组查询注意力]]
- **来源文献**：[[sources/MTFM_美团统一推荐基座大模型在外卖多业务场景的落地实践]]
