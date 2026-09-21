---
type: source
tags:
- MachineLearning
summary: 本文介绍了在处理无法完全载入内存的大规模数据集时，如何使用随机贴片法（Random Patches）来训练经典的集成学习模型（如随机森林）。分析了该方法通过在样本和特征两个维度上同时采样，降低决策树之间的相关性，从而提升方差降低效应（Variance
  Reduction）并显著减少内存占用的原理。
sources:
- raw/articles/2026-05-05_Train-classical-ML-models-on-large-datasets_19dfa2.md
updated: '2026-08-04'
---

# Train classical ML models on large datasets

## 来源信息
- **来源**: Daily Dose of DS
- **作者**: Avi Chawla
- **原始链接**: [Train classical ML models on large datasets](https://www.dailydoseofds.com/why-bagging-is-so-ridiculously-effective-at-variance-reduction/)
- **归档物理文献**: [[raw/articles/2026-05-05_Train-classical-ML-models-on-large-datasets_19dfa2.md]]

## 核心要点
1. **树集成模型的大数据内存瓶颈**：在企业级应用中，数据主要以结构化表格（Tabular Data）为主。经典树集成模型（如随机森林、梯度提升树等）在训练时通常需要将全部数据集一次性载入内存，这使得标准实现在面临大数据集时容易遭遇 OOM 瓶颈。
2. **解决大数据训练 of 两种途径**：解决内存瓶颈主要有两种思路：一是引入 Spark MLlib 等分布式大数据计算框架，但通常会增加部署 and 维护成本；二是利用算法层面的改进，即随机贴片（Random Patches）技术。
3. **随机贴片法（Random Patches）机制**：在集成学习中，通过在样本（行，Row）和特征（列，Column）两个维度上同时进行随机采样来构建不同的局部子空间（称为 Patch），并在每个 Patch 上训练一棵基模型决策树。
4. **方差降低（Variance Reduction）原理**：两棵树的数据重合度相比于普通的随机森林明显更低，这使得树之间的相关性被最小化。根据 Bagging（装袋法）的集成学习原理，当基学习器之间的相关性越低时，集成的方差降低效果就越显著，从而能得到一个更稳健的模型。
5. **内存友好的优势**：因为每棵树仅使用一小部分行和列训练，训练单个基模型所需的内存开销极大降低，允许在内存受限的环境中训练大规模集成模型。

## 关键引文
- "Classical ML algorithms, such as tree-based ensemble methods, are frequently used for modeling. However, typical implementations of these models are not “big-data-friendly” because they require the entire dataset to be in memory."
- "The idea is to sample random data patches (rows and columns) and train a tree model on each patch."
- "In a gist, building trees that are as different as possible guarantees a greater reduction in variance."
- "In this case, the dataset overlap between two trees will be less than that in a typical random forest. This aids in the Bagging objective and leads to a more robust model."

## 联动概念
- Random_Patches大数据训练

> 📎 **物理文献**：[[raw/articles/2026-05-05_Train-classical-ML-models-on-large-datasets_19dfa2.md]]
