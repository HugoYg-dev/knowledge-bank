---
type: source
tags:
- LLM/arch/Mamba
summary: Mamba2（ICML）SSD 框架：SSM 与 Attention 的数学等价、半可分离矩阵、分块矩阵算法、8倍推理加速与混合模型超越 Transformer
sources:
- raw/articles/Mamba2_ SSM和Transformer的大一统 - 知乎.md
updated: '2026-07-01'
---
## 来源信息

- **标题**：Mamba2: SSM 和 Transformer 的大一统
- **作者**：HongzhuzhuOptimistic Pessimist（知乎）
- **URL**：https://zhuanlan.zhihu.com/p/705138777
- **原论文**：Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality（ICML 2024）

## 核心要点

- Mamba1 局限：Δ、B、C 输入依赖但计算串行，张量并行需 2 次 allreduce，缺乏系统级优化
- SSD 框架三层含义：① SSD Model（DNN 层）；② SSD Framework（分析框架）；③ SSD Algorithm（GPU 高效算法）
- 数学核心——SSM 是半可分离矩阵变换：SSM 序列变换 Y=MX，M 是下三角矩阵，M_ij = C_i^T × A_{i:j}^× × B_j，这类矩阵即半可分离矩阵（semiseparable matrix），下三角子矩阵均为低秩
- SSM 与 Attention 等价：当 A_t 为标量时，M = L ∘ CB^T；对应 Attention 中 M = L ∘ QK^T V；(C,B,X) ↔ (Q,K,V) 完全等价
- 结构化掩码注意力（SMA）：四阶张量缩约，掩码矩阵为结构化矩阵；因果 mask 是 1-SS 矩阵的特殊形式（a_t=1）
- SSD 算法——分块矩阵分解：将 M 分成 T/Q × T/Q 子矩阵块；对角块（类 Attention 二次计算）、低秩块（矩阵乘）、扫描块（SSM scan，复杂度降低 Q 倍）并行处理
- SSD 算法——Chunking & State Passing：序列分 chunk，分四步：intra-chunk 输出、chunk 状态、状态传递（parallel scan）、初始状态对输出的贡献
- 数值稳定性：segsum 操作将累乘转为 log 域累加，避免 Catastrophic Cancellation；使用无减法版本防止 fp32 训练出现 nan
- 计算成本：设 N=P=Q，总 FLOP O(TN²)，内存 O(TN)，主要由 (N,N) 矩阵乘组成，充分利用 GPU 矩阵单元
- Mamba2 架构改进：① 并行参数投影（A,B,C,X 一次投影，类似 QKV 并行），减少参数，支持 Megatron 张量并行；② 块末加额外归一化层（LayerNorm/GroupNorm/RMSNorm）防止大模型不稳定
- 多头模式：MHS（等同 MHA）、MCS（等同 MQA，B 共享）、MIS（等同 MVA，B/C 单头 X 多头）、GIS（等同 GQA）
- 系统优化：张量并行从 2 次 allreduce 降至 1 次；序列并行直接复用 Megatron SP 方案；context parallel 通信复杂度线性（vs Transformer 的二次）；可变长度通过 A_t=0 截断跨序列状态传递
- 实验：纯 SSM 8B 在多任务媲美 Transformer；Mamba-2-Hybrid（43% Mamba2 + 7% Attention + 50% MLP）在 12 个标准任务全超 8B Transformer，推理 8× 加速；长文本 16K/32K/128K 达到或超过 Transformer

## 关键引文

- "SSD 连接了状态空间模型、结构化矩阵和注意力机制"
- "混合模型（43% Mamba-2, 7% self-attention, 50% MLP）在所有 12 个标准任务上超过了 8b 的 Transformer 模型，推理过程得到了 8 倍的提速"
- "segsum 操作将乘法转成加法操作……这个细节非常重要，如果是 unstable 版本的实现，可能用 fp32 训练刚开始没多久就出现了 nan"

## 关联

- [[概念_SSD_状态空间对偶]] — SSD 框架核心
- [[概念_半可分离矩阵]] — SSM 的矩阵代数基础
- [[概念_SSM_状态空间模型]] — SSM 基础
- [[概念_Mamba选择机制]] — Selective SSM 基础
- [[概念_MambaBlock架构]] — Mamba2 Block 改进
- [[实体_Mamba2]] — Mamba2 模型
- [[实体_Mamba]] — Mamba1

---
> 📎 **物理文献**：[[raw/articles/Mamba2_ SSM和Transformer的大一统 - 知乎.md]]