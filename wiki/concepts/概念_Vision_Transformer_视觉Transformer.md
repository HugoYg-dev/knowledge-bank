---
type: concept
tags:
- CV/detection
summary: Vision Transformer 将图像分为 patch 序列输入 Transformer 编码器，替代 CNN 作为视觉 Backbone。SAM
  使用 ViT-H 作为图像编码器。
sources:
- wiki/sources/DiT_扩散模型与Transformer.md
- wiki/sources/SAM_Segment_Anything模型.md
- wiki/sources/从LLaVA到Qwen3-VL_多模态架构演进.md
updated: '2026-09-21'
aliases:
- Vision Transformer
- ViT
- 视觉Transformer
- 概念_Vision_Transformer
---

# 概念：Vision Transformer

## 定义

Vision Transformer（ViT）由 Google（Dosovitskiy et al.）提出，将图像分割为固定大小 patch，每个 patch 作为序列 token 输入标准 Transformer 编码器，通过自注意力机制获取全局上下文。

## 在 SAM 中的应用

- SAM 图像编码器基于 ViT-H/16（Huge 变体，16×16 patch）
- 使用 MAE（Masked Autoencoder）预训练提供强初始化
- 输入 1024×1024 RGB 图像，输出 64×64×256 embedding
- 三种规模：ViT-B(86M), ViT-L(308M), ViT-H(636M)

## 关联

- [[SAM_Segment_Anything模型]]（来源）
- [[实体_ViT]]
- [[实体_SAM]]