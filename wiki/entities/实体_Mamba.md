---
type: entity
tags:
- LLM/arch/Mamba
summary: Albert Gu 和 Tri Dao 于 2023 年提出的选择性状态空间序列模型，是 Transformer 架构的强力竞争者。
sources:
- wiki/sources/A_Visual_Guide_to_Mamba_and_SSM.md
- wiki/sources/Mamba2_SSD_大一统.md
- wiki/sources/Mamba_Explained_Kola_Ayonrinde.md
- wiki/sources/RAG系统设计_语义搜索与KG驱动选型.md
- wiki/sources/Transformer被挑战_Mamba解析与PyTorch复现.md
- wiki/sources/一文读懂Mamba_知乎.md
- wiki/sources/从DeepSeek-V3到Kimi_K2_八种现代LLM架构大比较.md
- wiki/sources/腾讯混元TurboS技术报告.md
updated: '2026-09-07'
---
# Mamba

Albert Gu 和 Tri Dao 于 2023 年提出的选择性状态空间序列模型，是 Transformer 架构的强力竞争者。

## 基本信息

- **论文**：Mamba: Linear-Time Sequence Modeling with Selective State Spaces
- **arXiv**：2312.00752（2023 年 12 月）
- **代码**：https://github.com/state-spaces/mamba
- **作者**：Albert Gu（CMU）、Tri Dao（Princeton）

## 核心特性

- 序列长度线性复杂度 O(n)，推理时每 token 计算和内存为常量
- 选择机制（Selective SSM / S6）：B、C、Δ 依赖输入，实现内容感知
- 硬件感知算法：parallel scan + kernel fusion + recomputation
- HiPPO 矩阵初始化：支持长程依赖记忆
- 训练用卷积/并行扫描，推理用循环表示

## 性能

- Mamba-3B 在预训练和下游评测上超过同参数量 Transformer，并与 2× 参数量 Transformer 相当
- 推理速度最高 5× 快于同等 Transformer
- 支持百万 token 级别的超长上下文

## 架构关系

- 前置：[[实体_S4]]（Structured State Space for Sequences）
- 后续：[[实体_Mamba2]]（SSD 框架，ICML 2024）
- 作者：[[实体_Albert_Gu]]、[[实体_Tri_Dao]]

## 关键概念

- [[概念_Mamba选择机制]] — 核心创新
- [[概念_MambaBlock架构]] — Block 结构
- [[概念_Mamba硬件感知算法]] — GPU 优化
- [[概念_状态空间模型SSM]] — 数学基础
- [[概念_HiPPO矩阵]] — 矩阵 A 初始化

## 来源

- [[A_Visual_Guide_to_Mamba_and_SSM]]
- [[Mamba_Explained_Kola_Ayonrinde]]
- [[一文读懂Mamba_知乎]]
- [[Transformer被挑战_Mamba解析与PyTorch复现]]