---
type: concept
tags:
- DeepLearning
- 面试
summary: BN/LN/IN/GN 四种归一化在 [N,C,H,W] 不同维度上计算均值方差——BN(N,H,W)、LN(C,H,W)、IN(H,W)、GN(分组)；用途、batch
  依赖性、参数维度各不同。
sources:
- wiki/sources/Transformer大模型3D可视化_NanoGPT.md
updated: '2026-09-07'
---


# 概念：Normalization 方法对比（BN/LN/IN/GN）

## 定义

四种常用归一化方法都对激活函数的输入做 Norm，区别在于在 feature map [N,C,H,W] 的哪些维度上计算均值和方差。

## 对比表

| 方法 | 归一化维度 | 保留维度 | batch 依赖 | 用途 |
|------|-----------|---------|-----------|------|
| BN | N、H、W | C | 是（小 batch 差）| CNN |
| LN | C、H、W | N | 否 | RNN、变长序列、batch=1 |
| IN | H、W | N、C | 否 | 风格迁移 |
| GN | 组内（C/G 页）| N | 否 | 小 batch（图像分割）|

## 要点

- GN 是 LN 和 IN 的折中，channel 分 G 组组内归一化，与 batch size 无关
- 参数维度：BN/IN/GN 的 γ、β 是长度 C 的向量；LN 的 γ、β 是 normalized_shape 矩阵
- BN/IN 可用 momentum + track_running_stats 估计整体数据均值方差；LN/GN 只算当前 batch 真实统计量
- "一摞书"记忆法：BN=平均书、LN=整本书平均字、IN=每页平均字、GN=小册子平均字

## 关联

- [[概念_Batch_Normalization]]