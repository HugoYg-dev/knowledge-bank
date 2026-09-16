---
type: source
tags:
- MachineLearning
summary: 介绍了数据集中常见的 11 种变量类型及其定义与应用场景，包括自变量、因变量、混杂变量、控制变量、潜变量、交互变量、平稳/非平稳变量、滞后变量和泄露变量。
sources:
- raw/articles/2025-04-23_11-Types-of-Variables-in-a-Dataset_196640.md
updated: 2026-08-03
---

# 11 Types of Variables in a Dataset

## 来源信息
- **主题**: 11 Types of Variables in a Dataset
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Wed, 23 Apr 2025
- **原始物理文件**: [[raw/articles/2025-04-23_11-Types-of-Variables-in-a-Dataset_196640.md]]

## 核心要点
- **自变量与因变量**：自变量是作为预测结果输入的特征，而因变量则是要预测的目标输出。
- **混杂变量与控制变量**：在因果推断中，混杂变量同时影响自变量 and 因变量，容易导致虚假相关。为了评估真实的因果效应，必须对混杂变量进行控制，使其成为控制变量。
- **潜变量**：无法直接观测，但可以通过其他可观测变量推断出的变量（例如聚类中的无监督类别标签或高斯混合模型中的隐变量）。
- **交互变量**：两个或多个变量相乘产生的复合特征，用于衡量变量间的协同效应（例如在回归分析中，将独热编码的两个特征相乘）。
- **时序相关变量**：
  - **平稳/非平稳变量**：平稳变量的统计属性（均值、方差）不随时间变化；统计学习模型通常假设样本独立同分布，因此应避免直接使用非平稳变量（如股票原始价格），而应使用其相对变化。
  - **滞后变量**：代表变量在过去时间点的值，在时序预测中作为重要特征（如前一个月的销售额）。
- **泄露变量**：提供了预测时无法获取的目标变量信息，这会导致模型在训练时表现过于乐观，但在新数据上无法泛化（例如前向滞后特征）。

## 关联知识
- 核心概念：[[concepts/概念_数据集变量分类]]

## 关键引文
> "It is due to the confounding variables that we say, 'Correlation does not imply causation.'"
> "Preserving stationarity is critical in statistical learning because these models assume samples are identically distributed."
> "Leaky variables provide information about the target variable that would not be available during prediction. This leads to overly optimistic model performance during training but fails to generalize to new data."

> 📎 **物理文献**：[[raw/articles/2025-04-23_11-Types-of-Variables-in-a-Dataset_196640.md]]
