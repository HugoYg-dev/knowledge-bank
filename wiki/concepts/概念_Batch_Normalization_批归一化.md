---
type: concept
tags:
- DeepLearning
- 面试
summary: Batch Normalization 沿通道在 batch 维度（N,H,W）计算均值方差，强迫数据为均值0方差1分布，缓解 Internal
  Covariate Shift 与梯度消失；用于激活函数之前。
sources:
- wiki/sources/PyTorch常用代码段合集.md
updated: '2026-09-21'
aliases:
- Batch Normalization
- BatchNorm
- BN
- 批归一化
- 概念_Batch_Normalization
---

# 概念：Batch Normalization（BN）

## 定义

BN（2015）针对每个神经元，使数据进入激活函数前沿通道计算每个 batch 的均值、方差（除以 N×H×W），强迫数据保持均值 0、方差 1 的正态分布，再加可学习的缩放平移参数 γ、β。

## 动机

- mini-batch 分布不一致使模型训练困难
- Internal Covariate Shift（ICS）：训练中各层数据分布随网络加深差异越来越大，收敛慢、梯度消失

## 算法过程

1. 沿通道计算 batch 均值
2. 沿通道计算 batch 方差
3. 做归一化（除以 √(方差+ε)）
4. 加缩放平移变量 γ、β（可学习，保证保留原有特征同时完成归一化）

## 使用位置

全连接层或卷积操作之后，激活函数之前。

## 作用

- 允许较大学习率
- 减弱对初始化的强依赖
- 数值更稳定
- 轻微正则化（类似 Dropout，相当于给隐藏层加噪声）

## 问题

- batch 太小：均值方差不足以代表整体分布
- batch 太大：超内存、需更多 epoch、固定梯度方向难更新

## 关联

- [[概念_Normalization方法对比]]