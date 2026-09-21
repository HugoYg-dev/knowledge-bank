---
type: entity
tags:
- CV/detection
summary: SAM（Segment Anything Model），Meta AI 的图像分割基础模型，支持点/框/掩码/文本 Prompt，在 SA-1B
  数据集训练。
sources:
- wiki/sources/SAM_Segment_Anything模型.md
updated: '2026-06-26'
---

# 实体：SAM

## 简介

SAM（Segment Anything Model）由 Meta AI 开发，是图像分割的基础模型，支持点、框、掩码、文本等多种 Prompt 驱动分割。

## 架构（用户高亮重点）

> [重点/高亮] SAM 由 3 个主要部分组成：提示词编码器、图像编码器和轻量级掩码解码器。图像编码器是计算量最大的部分。

- **图像编码器**：ViT-H/16，输入 1024×1024，输出 64×64×256 embedding
- **Prompt 编码器**：点/框/掩码/文本（文本经 CLIP）
- **Mask 解码器**：轻量 Transformer，双向注意力，对模糊 prompt 输出 3 个 mask + IoU 分数


## 训练

- 损失：Focal Loss（α=0.25, γ=2）+ Dice Loss
- 数据集 SA-1B：11M 图像、1.1B mask，三阶段标注（人工 → 半自动 → 全自动）

## 关联

- [[SAM_Segment_Anything模型]]（来源）
- [[概念_Prompt驱动分割]]
- [[概念_图像分割]]
- [[概念_Focal_Loss_焦点损失]]
- [[实体_ViT]]
- [[实体_CLIP]]