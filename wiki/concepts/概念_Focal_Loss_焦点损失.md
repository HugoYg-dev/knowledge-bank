---
type: concept
tags:
- CV/detection
summary: Focal Loss 通过下调简单样本权重解决类别不平衡问题，由 RetinaNet 提出，SAM 训练中与 Dice Loss 组合使用。
sources:
- wiki/sources/SAM_Segment_Anything模型.md
updated: '2026-09-21'
aliases:
- Focal Loss
- 焦点损失
- 概念_Focal_Loss
---

# 概念：Focal Loss

## 定义

Focal Loss 解决前景/背景严重类别不平衡问题。由 RetinaNet（Lin et al. 2017）提出。

## 公式

`FL(pt) = -αt * (1-pt)^γ * log(pt)`

- αt：类别平衡因子
- γ：聚焦参数（通常为 2）
- 效果：下调易分类样本权重（pt 大时 (1-pt)^γ 趋近 0），聚焦于难分类样本

## 在 SAM 中的应用

SAM 训练使用组合损失：`20 × Focal Loss + Dice Loss`

- Focal Loss 处理前景/背景不平衡
- Dice Loss 衡量预测 mask 与 GT 重合度：`1 - 2|X∩Y|/(|X|+|Y|)`

## 关联

- [[SAM_Segment_Anything模型]]（来源）
- [[概念_图像分割]]
- [[实体_SAM]]