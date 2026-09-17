---
type: "concept"
tags:
- CV/arch
summary: DiT（Diffusion Transformer）是用 Transformer 替换扩散模型 U-Net 的架构，作用于 latent patches；被认为是
  Sora 等视频生成模型的基础架构之一。
sources:
- wiki/sources/DiT_扩散模型与Transformer.md
updated: '2026-06-26'
---

# 概念_DiT（Diffusion Transformer）

## 简介

DiT（Diffusion Transformers）由 William Peebles、Saining Xie 等（UCB, NYU）提出，论文 Scalable Diffusion Models with Transformers（ICCV 2023 Oral）。在 Latent Diffusion 框架下用 Transformer 替换扩散模型常用的 U-Net 骨干，Transformer 作用于 latent patches 上。

## 要点

- 设计空间：Patch Size、DiT Block 架构（4 种条件注入，adaLN-Zero 最优）、模型尺寸（S/B/L/XL）
- 缩放性：GFLOPs 与 FID 强负相关；增大模型或减小 Patch Size 均改善 FID
- SOTA：DiT-XL/2 在 ImageNet 256×256 达 FID 2.27，512×512 达 FID 3.04，且计算量远低于 ADM
- 被文章称为「Sora 的幕后功臣」（全文标题，未在正文展开 Sora 细节，confidence: medium 仅指 Sora 关联）

## 关联

- [[DiT_扩散模型与Transformer]]（来源）
- [[实体_ViT]]