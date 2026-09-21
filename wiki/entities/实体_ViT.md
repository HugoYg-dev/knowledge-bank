---
type: entity
tags:
- CV/detection
summary: ViT（Vision Transformer），将图像分 patch 序列输入 Transformer 的视觉 Backbone；SAM 用 ViT-H
  作图像编码器。
sources:
- wiki/sources/DiT_扩散模型与Transformer.md
- wiki/sources/SAM_Segment_Anything模型.md
- wiki/sources/从LLaVA到Qwen3-VL_多模态架构演进.md
- wiki/sources/向量数据库原理与应用全解析.md
updated: '2026-06-26'
---

# 实体：ViT

## 简介

ViT（Vision Transformer）将图像分割为 patch，作为序列 token 输入标准 Transformer 编码器，借自注意力获取全局上下文。

## 在 SAM 中的应用

- SAM 图像编码器使用 ViT-H/16（Huge，16×16 patch）

## 备注

全文主要在 SAM 架构语境下介绍 ViT（confidence: medium）。

## 关联

- [[SAM_Segment_Anything模型]]（来源）
- [[概念_Vision_Transformer_视觉Transformer]]
- [[实体_SAM]]
- [[实体_CLIP]]