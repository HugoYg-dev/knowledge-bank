---
type: entity
tags:
- CV/detection
summary: R-CNN 系列（R-CNN / Fast R-CNN / Faster R-CNN），开创 Region-based 两阶段目标检测范式。
sources:
- wiki/sources/目标检测入门_基础网络与分类定位权衡.md
- wiki/sources/目标检测入门_特征复用与实时性.md
- wiki/sources/目标检测入门_经典模型.md
- wiki/sources/目标检测入门_评测与训练技巧.md
updated: '2026-06-26'
---

# 实体：R-CNN

## 简介

R-CNN（Rich Feature Hierarchies for Accurate Object Detection and Semantic Segmentation）由 Ross Girshick 等人提出，首次将 CNN 用于区域检测。其后续改进构成检测领域最具影响力的方法线。

## 演进

| 模型 | 论文 | 核心改进 |
|------|------|----------|
| R-CNN | arXiv:1311.2524 | CNN 用于区域分类；Selective Search + AlexNet；引入 IoU / BBox Regression |
| Fast R-CNN | arXiv:1504.08083 | 共享特征图 + RoI Pooling；多任务联合训练 |
| Faster R-CNN | arXiv:1506.01497 | RPN 替代 Selective Search；Anchor 机制；全端到端训练；~5fps |

## 在本文语境中的角色

- 定义了两阶段检测的标准范式（RPN + RCNN head）
- Faster R-CNN 搭配不同 Backbone（ResNet、NASNet）作为后续工作基准

## 关联

- [[目标检测入门_经典模型]]（来源）
- [[概念_两阶段检测]]
- [[概念_Anchor机制]]
- [[概念_RoI_Pooling_候选区域池化]]