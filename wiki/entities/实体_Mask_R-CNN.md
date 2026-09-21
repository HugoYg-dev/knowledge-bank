---
type: entity
tags:
- CV/detection
summary: Mask R-CNN，在 Faster R-CNN 基础上增加 mask 分支实现实例分割，提出 RoIAlign。
sources:
- wiki/sources/目标检测入门_基础网络与分类定位权衡.md
- wiki/sources/目标检测入门_评测与训练技巧.md
updated: '2026-06-26'
---

# 实体：Mask R-CNN

## 简介

Mask R-CNN（arXiv:1703.06870）在 Faster R-CNN 基础上增加并行 mask 预测分支，实现实例分割。

## 关键贡献：RoIAlign

- 标准 RoI Pooling 涉及量化取整，造成对齐误差，损害 mask 预测
- RoIAlign 用双线性插值在非整数坐标处计算特征值，消除量化误差，显著提升精度
- 后续 Light-Head R-CNN 等沿用

## 备注

全文（评测与训练技巧篇）主要在 RoIAlign 技巧语境下提及 Mask R-CNN，未展开 mask 分支细节（confidence: medium）。Facebook Detectron 中 Mask R-CNN 使用 ResNeXt backbone。

## 关联

- [[目标检测入门_评测与训练技巧]]（来源）
- [[概念_RoI_Pooling_候选区域池化]]
- [[实体_R-CNN]]