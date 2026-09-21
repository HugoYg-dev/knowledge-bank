---
type: concept
tags:
- CV/arch
summary: Latent Diffusion Models（LDM）先用 AutoEncoder 把图像压缩到低维 latent 空间，再在 latent 上训练扩散模型，大幅降低高分辨率像素空间的计算量。
sources:
- wiki/sources/DiT_扩散模型与Transformer.md
updated: '2026-09-21'
aliases:
- Latent Diffusion
- LDM
- 潜在扩散模型
- 潜空间扩散模型
- 概念_Latent_Diffusion
---

# 概念：Latent Diffusion Models（LDM）

## 定义

直接在高分辨率像素空间训练扩散模型计算量巨大。LDM 通过两阶段方法解决：先学习 AutoEncoder 将图像压缩为更小的空间表征 z，再在 z（而非原图）上训练扩散模型。

## 要点

- 两阶段流程：
  1. 学习 AutoEncoder，将图像压缩为 latent 表征 z
  2. 在 z 上训练扩散模型（AutoEncoder 冻结）
  3. 生成时从扩散模型采样 z，再经解码器解码回图像
- DiT 中使用 Stable Diffusion 预训练的 VAE，Encoder 下采样率为 8（256×256×3 → 32×32×4）

## 关联

- [[DiT_扩散模型与Transformer]]（来源）
- [[概念_扩散模型]]