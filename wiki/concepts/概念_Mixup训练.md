---
type: concept
tags:
- DeepLearning
- CV/data-augmentation
summary: Mixup 训练通过 Beta 分布采样混合系数 λ，对一对样本的图像和标签做线性插值（mixed = λ·a + (1-λ)·b），损失也按 λ
  加权两个标签的损失，是一种数据增强/正则化方法。
sources:
- wiki/sources/PyTorch常用代码段合集.md
updated: '2026-06-29'
---


# 概念：Mixup 训练

## 定义

Mixup 是一种数据增强方法，对成对样本的图像和标签做线性插值后再训练。

> 注：全文以 PyTorch 代码段形式给出实现，未展开理论动机，confidence 标 medium。

## 实现要点（全文代码）

- `beta_distribution = torch.distributions.beta.Beta(alpha, alpha)`
- 每个 batch 采样 `lambda_ = beta_distribution.sample()`
- 随机打乱索引 `index = torch.randperm(images.size(0))`
- 混合图像：`mixed_images = lambda_ * images + (1 - lambda_) * images[index, :]`
- 标签对：`label_a, label_b = labels, labels[index]`
- 混合损失：`loss = lambda_ * loss_fn(scores, label_a) + (1 - lambda_) * loss_fn(scores, label_b)`

## 关联

- [[PyTorch常用代码段合集]]（来源）
- [[概念_Label_Smoothing_标签平滑]]