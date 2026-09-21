---
type: concept
tags:
- LLM/training/post-train
- DeepLearning
summary: 一种最大化数据多样性的贪婪采样算法，目标是在高维空间中选出分布尽量均匀的样本子集。
sources:
- wiki/sources/SFT数据挑选方法_质量多样性必要性.md
updated: '2026-09-21'
aliases:
- K-Center-Greedy
- K-Center Greedy
- 中心贪婪算法
- 概念_K-Center-Greedy算法
---

# 概念：K-Center-Greedy 算法

## 定义

一种最大化数据多样性的贪婪采样算法，目标是在高维空间中选出分布尽量均匀的样本子集。

## 算法步骤

1. 随机选定初始中心点
2. 每次找出与当前所有中心点距离**最远**的那个点
3. 将其加入中心点集合
4. 重复直到选出目标数量的样本

## 在 SFT 数据筛选中的应用

- MoDS 方法使用 BERT 抽取数据特征后应用 K-Center-Greedy
- 确保每个选出的样本都与已选样本尽可能不同，最大化多样性

## 对比 K-Means 聚类

- K-Center-Greedy：增量式选取，直接选出最终样本集，适合给定预算下的样本选择
- K-Means：先聚类再从每簇采样，需设定簇数 k，结果依赖聚类质量

## 关联

- [[SFT数据挑选方法_质量多样性必要性]]
- [[概念_SFT数据三维度]]