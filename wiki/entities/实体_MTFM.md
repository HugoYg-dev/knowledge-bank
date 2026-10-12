---
type: "entity"
tags: ["Recommendation", "Infra/serving"]
summary: "美团外卖多业务场景统一推荐基座大模型（KDD 2026），首次实现外卖核心场景统一精排，采用异构 Tokenizer、动态因果掩码、混合注意力与 User-Level 训练架构"
sources: ["wiki/sources/MTFM_美团统一推荐基座大模型在外卖多业务场景的落地实践.md"]
updated: "2026-10-12"
---

# 实体：MTFM（美团统一推荐基座大模型）

## 简介

**MTFM（Meituan Foundation Model for Recommendation）** 是美团技术团队（搜索和推荐平台部）在 MTGR 基础上研发的工业级统一推荐基座大模型。该工作于 2026 年 5 月被顶级数据挖掘会议 KDD 2026 收录，首次在美团外卖多个核心业务场景（如外卖首页、拼好饭等）实现了跨域统一精排模型的全量落地。

## 研发背景与核心定位

传统工业推荐系统受限于 DLRM 架构与单场景孤岛建模，跨业务数据、算力与特征体系难以复用。MTFM 借鉴 LLM 基座模型的 Scaling 范式，面向**规模可扩展性（Scalability）**、**场景可延展性（Extensibility）**与**架构高效性（Efficiency）**三大挑战，将多业务异构信息建模为统一的 Token 序列，实现了免显式特征对齐的端到端学习。

## 关键技术特征

1. **异构 Tokenizer 与动态因果掩码**：
   - 将全域输入统一抽象为长期历史序列（`H-Token`）、近实时行为序列（`R-Token`）与待预估候选目标（`T-Token`）；
   - 通过动态掩码矩阵（Dynamic Mask）确保 H-Token 全局可见、R-Token 因果可见，而 T-Token 之间严格互不感知，杜绝信息泄漏。
2. **混合注意力（Hybrid Target Attention）与 Target Scale-Up**：
   - 堆叠 16 层（4 个 Block，Target:Full = 3:1）混合注意力结构并结合 GQA，有效打破传统 Full Attention 的二次方复杂度瓶颈，样本吞吐提升 2.9 倍；
   - 采用 AutoSplit 将单个候选映射为 4 个 Target Token，配合独立的 Q 投影、SwiGLU FFN 与 RankMixer Mixing 交叉模块，避免表征坍缩并提升容量。
3. **User-Level 聚合与一图多业务范式**：
   - 颠覆传统逐 PV 样本切分，将单用户当日全场景曝光聚合成 1 条样本，共享最耗算力的长序列 Attention 计算；
   - 线上部署图仅保留共享基座与对应业务独享任务塔，实现“统一训练、轻量化多业务部署”。
4. **LLM 级深度优化与定制 Triton 算子**：
   - 深度感知方差缩放初始化（$\frac{0.02}{\sqrt{16}}$）与 Muon 优化器升级（针对 Dense 矩阵参数，结合批处理并行 Newton-Schulz 迭代）；
   - 基于 Triton 重构 Jagged Mask 查找、扩展 FA2 支持动态掩码、融合 Group LayerNorm（GLN）算子，单算子延迟降低 50% 以上。

## 业务成效与指标

- **在线业务增益**：美团外卖核心业务全量推全后，各业务线订单量提升 2.06%~6.68%，在线效果最显著的业务线订单增长突破 6%；
- **算力经济性**：单样本计算量达 192 GFLOPs（较传统 DLRM 提升数百倍），但依托 User-Level 算力复用与定制算子，在线推理整体成本降低 24%；
- **Scaling Law 验证**：在网络层数（16层）、Token 维度（192~768）与序列长度（400~2000）上展现了清晰稳健的 Scaling 收益。

## 关联实体与概念

- **所属机构**：[[entities/实体_美团]]
- **核心算法机制**：[[concepts/概念_Target_Attention_目标注意力]]、[[concepts/概念_Muon优化器]]、[[concepts/概念_GQA_分组查询注意力]]
- **文献来源**：[[sources/MTFM_美团统一推荐基座大模型在外卖多业务场景的落地实践]]
