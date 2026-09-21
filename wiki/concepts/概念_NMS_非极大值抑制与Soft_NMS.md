---
type: concept
tags:
- CV/detection
summary: NMS（非极大抑制）用于过滤重叠检测框；Soft NMS 改为按 IoU 惩罚置信度而非硬性丢弃。
sources:
- wiki/sources/目标检测入门_评测与训练技巧.md
updated: '2026-09-21'
aliases:
- NMS
- Soft NMS
- 非极大值抑制
- 概念_NMS与Soft_NMS
---

# 概念：NMS 与 Soft NMS

## NMS（非极大抑制）

Non-Maximum Suppression 用于检测后处理：保留得分最高框，丢弃与其 IoU 超过阈值的重叠框，过滤冗余检测。YOLO、SSD 等均依赖 NMS。

## Soft NMS

由「Improving Object Detection With One Line of Code」提出。标准 NMS 硬性丢弃高 IoU 重叠框，损害相邻物体检测。Soft NMS 改为按 IoU 惩罚（降低）重叠框的置信度，软化函数可为线性或高斯（高斯略优）。结合 Deformable ConvNets 曾达 MS COCO SOTA。代价是引入需按数据集调参的超参数。

## 关联

- [[目标检测入门_评测与训练技巧]]（来源）
- [[概念_检测评测指标]]
- [[概念_位置敏感检测]]