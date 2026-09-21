---
type: source
tags:
- LLM/arch/Mamba
summary: 用 50+ 可视化图解 Mamba 与状态空间模型全流程：SSM 数学基础、离散化、三种表示、HiPPO 矩阵、选择扫描算法与硬件感知实现
sources:
- raw/articles/A Visual Guide to Mamba and State Space ....md
updated: '2026-07-01'
---
## 来源信息

- **标题**：A Visual Guide to Mamba and State Space Models
- **作者**：Maarten Grootendorst
- **URL**：https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-mamba-and-state
- **论文**：Gu & Dao, "Mamba: Linear-time sequence modeling with selective state spaces," arXiv:2312.00752

## 核心要点

- Transformer 训练可并行（自注意力一次计算全序列），但推理时每步需重算长度 L 的注意力矩阵，复杂度 O(L²)
- RNN 推理快（线性复杂度），但存在遗忘问题，历史信息随时间衰减
- SSM 核心：两个方程——状态方程 h'(t)=Ah(t)+Bx(t)，输出方程 y(t)=Ch(t)+Dx(t)；矩阵 A/B/C/D 均可学习
- 离散化用 Zero-Order Hold（ZOH）将连续信号转为离散序列，引入可学习步长参数 Δ
- SSM 有三种等价表示：连续（数学基础）、循环（高效推理）、卷积（并行训练）；训练用卷积、推理用循环
- Linear Time Invariance（LTI）：A/B/C 对所有时间步固定，导致 SSM 无内容感知能力，不能处理选择性复制和归纳头任务
- HiPPO 矩阵：用 Legendre 多项式系数构造矩阵 A，使隐状态能压缩并记忆历史，新 token 权重高、旧 token 衰减；S4 = SSM + HiPPO + 离散化
- Mamba 关键创新 1——选择扫描：让 B、C 和 Δ 依赖输入（input-dependent），A 保持静态；每个 token 有独立的 B/C 矩阵，实现内容感知
- Mamba 关键创新 2——硬件感知算法：仿照 FlashAttention 减少 SRAM↔DRAM 数据搬运；使用 kernel fusion 合并离散化、selective scan、乘 C 三步；反向传播时重新计算中间状态而非存储
- 并行扫描（parallel scan）：利用结合律将看似串行的循环计算拆分并行处理
- Mamba Block：线性投影扩展嵌入 → 1D 卷积（防止独立 token 计算）→ Selective SSM → 残差输出；可堆叠多块
- 实验结果：Mamba 模型在相同参数量下匹配甚至超过 Transformer 性能

## 关键引文

- [重点/高亮] "What is a State Space Model?" — SSM 核心概念
- [重点/高亮] "The importance of Matrix A" — HiPPO 矩阵是 Mamba 长程记忆的关键

## 关联

- [[概念_SSM_状态空间模型]] — SSM 数学基础（两方程/A/B/C/D）
- [[概念_Mamba选择机制]] — input-dependent B/C/Δ 实现内容感知
- [[概念_HiPPO矩阵]] — Legendre 多项式压缩历史状态
- [[概念_SSM三种表示]] — 连续/循环/卷积表示及训推切换
- [[概念_SSM离散化]] — ZOH + 步长 Δ 将连续 SSM 转为离散
- [[概念_Mamba硬件感知算法]] — kernel fusion + recomputation
- [[概念_LTI_线性时不变]] — LTI 局限与选择机制动机
- [[实体_Mamba]] — Mamba 模型整体
- [[实体_S4]] — Structured State Space for Sequences

---
> 📎 **物理文献**：[[raw/articles/A Visual Guide to Mamba and State Space ....md]]