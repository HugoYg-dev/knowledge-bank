---
type: source
tags:
- MachineLearning
- DeepLearning
summary: 汇总了16种常见机器学习算法所采用的典型损失函数，并分析了部分非参数/贝叶斯算法在训练中不需要损失函数的物理本质。
sources:
- raw/articles/2025-12-26_Loss-Function-of-16-ML-Algos_19b5c7.md
updated: 2026-08-03
---

# 来源信息
- **标题**: Loss Function of 16 ML Algos
- **来源**: Daily Dose of DS
- **日期**: 2025-12-26
- **链接/ID**: 19b5c7637722a2ba

# 核心要点
- **常规算法的损失函数匹配**：
  - **线性回归**与**神经网络回归/Boosting回归**：通常使用均方误差（MSE）作为损失函数。
  - **逻辑回归**、**分类神经网络**与**Boosting分类**：通常使用交叉熵损失（Cross-Entropy Loss/Log Loss）。
  - **支持向量机（SVM）**：使用合页损失（Hinge Loss）以构建最大边距分类器。
  - **AdaBoost**：使用加权指数损失（Exponential Loss）。
- **无损失函数的特例**：
  - **k-Nearest Neighbors (kNN)**：作为非参数惰性学习算法，kNN不含训练和参数优化阶段，仅在推理时基于距离度量检索近邻，因此**无损失函数**。
  - **Naive Bayes**：直接基于概率乘积和条件独立性假设进行封闭式后验概率计算，不通过梯度下降或优化算法更新参数，因而也**无损失函数**。

# 关联概念与实体
- [[wiki/concepts/概念_机器学习损失函数|概念：机器学习损失函数]]

# 关键引文
> Since loss functions are a vital component of ML algorithms, knowing which loss functions are (typically) best suited for specific ML algorithms is extremely crucial.
> 
> kNN is a non-parametric lazy learning algorithm. It works by retrieving instances from the training data, and making predictions based on the k nearest neighbors to the test data instance.

---
> 📎 **物理文献**：[[raw/articles/2025-12-26_Loss-Function-of-16-ML-Algos_19b5c7.md]]
