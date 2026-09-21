---
type: entity
tags:
- LLM/arch/Mamba
summary: Albert Gu 和 Tri Dao 于 2024 年提出，在 Mamba1 基础上引入 SSD（状态空间对偶）框架，ICML 2024 收录。
sources:
- wiki/sources/Mamba2_SSD_大一统.md
- wiki/sources/腾讯混元TurboS技术报告.md
updated: '2026-06-29'
---

# Mamba2

Albert Gu 和 Tri Dao 于 2024 年提出，在 Mamba1 基础上引入 SSD（状态空间对偶）框架，ICML 2024 收录。

## 基本信息

- **论文**：Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality
- **会议**：ICML 2024
- **代码**：https://github.com/state-spaces/mamba

## 核心改进

- SSD 框架：证明 SSM 与线性 Attention 等价，见 [[概念_SSD_状态空间对偶]]
- 并行参数投影：A/B/C/X 一次投影并行产生（类似 QKV），减少参数，支持张量并行
- 额外归一化层：块末加 RMSNorm/GroupNorm，防止大模型不稳定
- 多头模式：MHS/MCS/MIS/GIS（对应 Attention 的 MHA/MQA/MVA/GQA）
- 系统优化：张量并行 2→1 次 allreduce；序列并行线性通信；可变长度支持

## 性能

- Mamba-2-Hybrid（43% Mamba2 + 7% Attention + 50% MLP）在 12 个标准任务全超 8B Transformer
- 推理 8× 加速（相比纯 Transformer）
- 长文本 16K/32K/128K 达到或超过 Transformer 水平

## 架构关系

- 前置：[[实体_Mamba]]
- 理论基础：[[概念_SSD_状态空间对偶]]、[[概念_半可分离矩阵]]

## 来源

- [[Mamba2_SSD_大一统]]