---
type: "source"
tags: ["Recommendation", "Infra/serving", "CaseStudy"]
summary: "美团技术团队在 MTGR 基础上提出统一推荐基座大模型 MTFM（KDD 2026），通过异构 Tokenizer、动态掩码、混合注意力（Target:Full=3:1）、Target Scale-Up 与 User-Level 聚合训练，首次在外卖核心场景实现多业务统一精排并达成订单量与推理成本双赢"
sources: ["raw/articles/MTFM：美团统一推荐基座大模型在外卖多业务场景的落地实践  美团 · 技术团队.md"]
updated: "2026-10-12"
---

# 来源摘要：MTFM：美团统一推荐基座大模型在外卖多业务场景的落地实践

- **来源信息**：美团技术团队 / 搜索和推荐平台部（2026-09-22）
- **核心议题**：突破推荐领域传统单场景建模与 DLRM 孤岛瓶颈，借鉴 LLM 基座模型 Scaling Law 路径，构建美团外卖多业务统一推荐基座大模型 MTFM（Meituan Foundation Model for Recommendation，已被 KDD 2026 接收），实现多业务跨域异构特征免人工对齐、万级长序列高效混合注意力与算力经济性。

## 核心要点

1. **核心挑战与三大设计支柱**：
   - **规模可扩展性（Scalability）**：采用类 Transformer/HSTU Block 堆叠作为骨干网络，通过 Target Token Scale-Up 扩大模型容量；
   - **场景可延展性（Extensibility）**：设计异构 Tokenizer 与动态因果掩码（Dynamic Mask），实现多场景特征免显式对齐与防信息泄漏；
   - **架构高效性（Efficiency）**：打破 Self-Attention 的平方复杂度瓶颈，引入混合注意力架构（Target:Full=3:1）、User-Level 样本复用与 GPU 定制高性能算子，实现 192 GFLOPs 单样本高计算量下在线推理成本降低 24%。

2. **多场景免对齐与动态掩码机制**：
   - **三类 Token 抽象**：
     - `H-Token（History）`：用户跨业务商家与商品长期行为序列，全场景共享；
     - `R-Token（Realtime）`：近实时点击、加购行为序列，按时间戳统一排序，全业务共享；
     - `T-Token（Target）`：待预估候选目标（商家/商品/券包）及其上下文特征，业务独立维护。
   - **动态因果掩码（Dynamic Mask）**：
     - `H-Token` 可被全序列所有 Token 观察，作为全场景共享上下文；
     - `R-Token` 遵循因果掩码（Causal Mask），T-Token 仅能观察发生在当前曝光时间之前的实时行为；
     - `T-Token` 之间相互隔离（仅可见自身），同一请求内的不同候选互不干扰，彻底消除信息泄露。

3. **高效注意力演进：混合架构与 Target Scale-Up**：
   - **MTFM V1（混合注意力架构）**：长序列中 T-Token 相比用户序列更聚焦于候选信息提取。借鉴 LLM（Qwen3-Next、MiMo-V2-Flash）混合注意力思路，采用 4 个 Block 共 16 层（每 Block 含 1 层 Full Attention 与 3 层 Target Attention），配合 GQA。相比纯 Full Attention，显存占用大幅下降，Batch Size 扩大 1.7 倍，吞吐达 2.9 倍且 GAUC 最优。
   - **MTFM V2（Target Scale-Up）**：避免单 Target Token 承载高维特征导致的表征过度压缩与信息丢失。通过 AutoSplit 将单个 Target 特征映射为 4 个 Token Embeddings，经过独立的 Q 投影与 SwiGLU FFN，并引入零参数的 RankMixer Mixing 模块进行交叉交互，杜绝相同 KV 驱动下的表征坍缩。

4. **User-Level 统一样本与跨场景联合训练范式**：
   - **User-Level 聚合**：彻底颠覆传统 DLRM 逐曝光（PV）切分样本的低效模式，将同一用户当日外卖各场景曝光聚合成 1 条样本；在训练阶段多 Target 共享最耗算力的长序列 Attention 计算，推理阶段按业务 Request-Level 聚合。
   - **一图多业务训练与部署**：共享 Attention 基座沉淀长序列兴趣表征，各业务 T-Token 表征送入 MMoE 与业务独立任务塔预测 CTR/CTCVR；线上部署导出图仅保留当前业务组件，杜绝无效计算。

5. **深层网络训练稳定性与优化器升级**：
   - **深度感知初始化**：针对 16 层残差 HSTU 结构，借鉴 GPT-2 初始化策略，对 Block 输出投影层按层数缩放标准差 $W_{o_{proj}} \sim \mathcal{N}(0,\frac{0.02}{\sqrt{16}})$，抑制方差随深度扩散导致的激活饱和。
   - **[[concepts/概念_Muon优化器|Muon 优化器升级]]**：针对 HSTU 的 UQKV 投影与 Output Projection 等 Dense 矩阵参数，采用基于 Newton-Schulz 迭代正交化的 Muon 优化器，结合 Weight Decay 与 Update RMS Scale 实践；随机实验 Train AUC 波动从 0.4pp 降至 0.1pp。
   - **全局动态损失归一化与跳过零梯度**：按 Batch 内全样本统一归一化消除小业务梯度噪声，并在优化器中批量检测并跳过未激活业务专家的零梯度 Weight Decay。

6. **软硬件协同（Co-Design）定制算子优化**：
   - **Triton 动态 Mask 与 FA2 扩展**：将多维 Mask 预处理为一维 Jagged Mask 存入共享内存，耗时从 22ms 降至 1ms；前向加速 128%、反向加速 152%。
   - **Group LayerNorm（GLN）融合算子**：基于 Triton 重构 GLN 算子并融合 ADD/MUL 操作，反向梯度分块归约，内存带宽利用率从 30% 跃升至 60%+。
   - **Flash-Muon 批量化改造**：针对推荐场景中小矩阵无法充分填满 GPU 的特点，将同形状参数堆叠为批量张量进行批量并行 Newton-Schulz 迭代，Kernel Launch 降至数十次，NS 阶段加速 241%，训练吞吐提升 19%。
   - **推理查表合并与跳算**：共享多表查询使显存从 22GB 降至 5.9GB；Attention 规则跳过 User→Item 无效计算使延迟再降 13%~50%。

7. **业务成效与 Scaling Law 验证**：
   - 稳步验证了网络层数（16层）、Token 维度（192~768）与序列长度（400~2000）上的经典 Scaling Law 现象。
   - 全量上线美团外卖多个核心业务，各业务订单增长 2.06%~6.68%（最显著业务突破 6%），在线推理成本降低 24%。

## 关联概念与实体

- **核心实体**：[[entities/实体_美团]]（模型所属机构与业务生态）、[[entities/实体_MTFM]]（美团统一推荐基座大模型）
- **核心概念**：[[concepts/概念_Target_Attention_目标注意力]]（推荐长序列目标注意力范式）、[[concepts/概念_Muon优化器]]（矩阵正交化优化器应用与批处理工程优化）、[[concepts/概念_GQA_分组查询注意力]]（高效注意力机制）
- **关联来源**：[[sources/美团搜索查询改写实践]]（美团搜索算法实践）、[[sources/从DeepSeek-V3到Kimi_K2_八种现代LLM架构大比较]]（Muon 与现代架构演进）

> 📎 **物理文献**：[[raw/articles/MTFM：美团统一推荐基座大模型在外卖多业务场景的落地实践  美团 · 技术团队.md]]
