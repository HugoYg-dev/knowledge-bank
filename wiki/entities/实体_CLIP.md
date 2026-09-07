---
type: entity
tags:
- CV/detection
summary: CLIP（Contrastive Language-Image Pre-training），OpenAI 视觉-语言对齐模型，为 SAM 提供文本
  Prompt 能力。
sources:
- wiki/sources/PyTorch图像增强方法总结.md
- wiki/sources/R1复现认知与误区.md
- wiki/sources/SAM_Segment_Anything模型.md
- wiki/sources/从LLaVA到Qwen3-VL_多模态架构演进.md
- wiki/sources/向量数据库原理与应用全解析.md
updated: '2026-06-26'
---

# 实体：CLIP

## 简介

CLIP（Contrastive Language-Image Pre-training）由 OpenAI 提出，用于视觉-语言理解，通过对比学习对齐图像与文本嵌入。

## 关键信息（全文所述）

- 训练使用对比损失对齐图文嵌入
- 在 SAM 中的作用：提供文本 Prompt 能力，使 SAM 可接受文本指定分割目标（SAM 基础模型不原生支持文本，需 CLIP 集成）

## 补充知识（非本文）

- 双编码器架构：图像编码器（ViT 或 ResNet）+ 文本编码器（Transformer）

## 备注

全文在 SAM 多模态集成语境下介绍 CLIP，细节有限（confidence: medium）。

## 关联

- [[SAM_Segment_Anything模型]]（来源）
- [[概念_Prompt驱动分割]]
- [[实体_SAM]]
- [[实体_ViT]]