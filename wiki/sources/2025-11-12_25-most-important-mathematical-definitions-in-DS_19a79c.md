---
type: source
tags:
- MachineLearning
summary: 汇总了数据科学中 25 个最核心的数学定义与公式，并对极大似然估计 (MLE)、标准分数 (Z-score)、最小二乘法 (OLS)、熵 (Entropy)、特征值与特征向量、R方系数
  (R-squared)、KL散度、奇异值分解 (SVD) 以及拉格朗日乘子法进行了重点释义和应用场景关联。
sources:
- raw/articles/2025-11-12_25-most-important-mathematical-definitions-in-DS_19a79c.md
updated: 2026-08-03
---

# 25 most important mathematical definitions in DS

## 来源信息
- **主题**: 25 most important mathematical definitions in DS
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Wed, 12 Nov 2025
- **原始物理文件**: [[raw/articles/2025-11-12_25-most-important-mathematical-definitions-in-DS_19a79c.md]]

## 核心要点
- **自明的基础术语**：
  - 梯度下降、正态分布、Sigmoid 函数、相关系数、余弦相似度、朴素贝叶斯、F1 分数、ReLU、Softmax、均方误差 (MSE)、带有 L2 正则化的 MSE、KMeans、线性回归、支持向量机 (SVM)、对数损失 (Log Loss)。
- **重点释义术语**：
  - **极大似然估计 (MLE)**：通过最大化观测数据的似然函数来估计统计模型参数的方法。
  - **标准分数 (Z-score)**：标准化数值，表示某数据点偏离平均值的标准差倍数。
  - **普通最小二乘法 (OLS)**：基于 MLE 步骤推导的线性回归闭式解（解析解）。
  - **熵 (Entropy)**：随机变量不确定性或随机性的度量，常用于决策树及 t-SNE 算法中。
  - **特征向量 (Eigen Vectors)**：在施加线性变换时不改变方向的非零向量，广泛用于 PCA 等降维技术中。
  - **R方系数 (R-squared)**：表示回归模型能够解释数据方差比例的统计指标。
  - **KL 散度 (KL Divergence)**：评估当使用一个概率分布去逼近另一个概率分布时**损失了多少信息**。常用作 t-SNE 算法的损失函数。
  - **奇异值分解 (SVD)**：将矩阵分解为三个矩阵（$U$、$\Sigma$、$V^T$）的分解技术，是降维、去噪和数据压缩的基础。
  - **拉格朗日乘子法 (Lagrange Multipliers)**：用于求解带约束条件的优化问题的数学技术，例如在从零推导 PCA 算法时的约束优化。

## 关联概念
- 核心概念：数据科学核心数学定义
- 关联概念：[[wiki/concepts/概念_t-SNE算法]]、[[wiki/concepts/概念_奇异值分解SVD]]、[[wiki/concepts/概念_主成分分析_PCA]]

## 关键引文
> "MLE (Maximum Likelihood Estimation): A method for estimating the parameters of a statistical model by maximizing the likelihood of the observed data."
> "KL divergence: Assess how much information is lost when one distribution is used to approximate another distribution. It is used as a loss function in the t-SNE algorithm."
> "Lagrange multipliers: They are commonly used mathematical techniques to solve constrained optimization problems... We covered them in detail when formulating PCA from scratch."

> 📎 **物理文献**：[[raw/articles/2025-11-12_25-most-important-mathematical-definitions-in-DS_19a79c.md]]
