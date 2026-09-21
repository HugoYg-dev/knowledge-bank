---
type: concept
tags:
- CV/detection
summary: 将不同大小的候选区域（RoI）映射为固定长度特征向量的池化操作；RoIAlign 用双线性插值消除其量化误差。
sources:
- wiki/sources/目标检测入门_基础网络与分类定位权衡.md
- wiki/sources/目标检测入门_经典模型.md
- wiki/sources/目标检测入门_评测与训练技巧.md
updated: '2026-09-21'
aliases:
- RoI Pooling
- Region of Interest Pooling
- 感兴趣区域池化
- 候选区域池化
- 概念_RoI_Pooling
---

# 概念：RoI Pooling

## 定义

RoI Pooling 由 Fast R-CNN 提出，将共享特征图上每个候选区域（RoI）划分为固定网格，各格做 max pooling，产出与 RoI 大小无关的等长特征向量，便于批量处理。

## RoIAlign 改进

Mask R-CNN 提出 RoIAlign：标准 RoI Pooling 涉及量化取整（整数化），造成对齐误差，损害实例分割的 mask 预测。RoIAlign 用双线性插值在非整数坐标处计算特征值，消除量化误差，显著提升精度，后续 Light-Head R-CNN 等沿用。

## 关联

- [[目标检测入门_经典模型]]（来源）
- [[概念_两阶段检测]]
- [[实体_Mask_R-CNN]]