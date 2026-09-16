---
type: source
tags:
- MachineLearning
summary: 介绍了模型校准的定义和实际价值，阐述了现代深度学习模型过度自信的现象，并详细剖析了 Platt 缩放（Platt Scaling）的物理映射机制、算法步骤及局限性。
sources:
- raw/articles/2025-12-02_Platt-Scaling-for-model-calibration_19ae0c.md
updated: 2026-08-03
---

# Platt Scaling for model calibration

## 来源信息
- **主题**: Platt Scaling for Model Calibration
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Tue, 02 Dec 2025
- **原始物理文件**: [[raw/articles/2025-12-02_Platt-Scaling-for-model-calibration_19ae0c.md]]

## 核心要点
- **模型校准的定义**：预测置信度（Confidence）与实际准确率（Accuracy）匹配。即若预测为 75% 的概率，则 100 个此类样本中应约有 75 个正例。
- **过度自信问题**：现代深度模型（如 ResNet）虽准确率高于旧模型（如 LeNet），但普遍存在过度自信（Average Confidence 远大于 Accuracy，如 90% 对比 70%），必须校准后方可用于决策。
- **Platt Scaling 四步法**：
  1. 训练主模型；
  2. 获取验证集/校准集的 raw scores/logits；
  3. 用验证集 logits 拟合一个 Sigmoid 形的逻辑回归模型以预测真实类别；
  4. 推理时，将新样本的主模型 logit 输入该逻辑回归模型，输出校准概率。
- **物理映射与典型应用**：本质上是寻找一个逻辑回归函数去拟合验证集 logits 到 0-1 概率空间的映射。非常适用于 SVM 等非概率分类器的概率转换。
- **局限性**：对校准集的数据量十分敏感。当校准集太小时，Platt Scaling 拟合的参数不稳定，导致概率估计失真。

## 关联知识
- 核心概念：[[wiki/concepts/概念_分类模型校准]]

## 关键引文
> "This means the model is well calibrated, i.e., the confidence and accuracy resonate with each other."
> "Despite being more accurate, the ResNet model is overconfident in its predictions. While the model thinks it’s 90% confident in its predictions, in reality, it only turns out to be 70% accurate."
> "The primary goal is to find a logistic function that maps the raw scores (or logits) from a model to probabilities between 0 and 1."
> "One common issue with Platt scaling is that it can be sensitive to the amount of data available for calibration."

> 📎 **物理文献**：[[raw/articles/2025-12-02_Platt-Scaling-for-model-calibration_19ae0c.md]]
