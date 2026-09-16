---
type: source
tags:
- MachineLearning
summary: 介绍现代神经网络存在过度自信（overconfidence）的问题，说明为什么机器学习模型需要进行校准（calibration），并提供了一个医疗与政府决策的实例来说明非校准模型的潜在危害。
sources:
- raw/articles/2026-02-04_Why-ML-models-need-calibration_19c2a8.md
updated: 2026-08-03
---

# Why ML models need calibration?

## 来源信息
- **原邮件主题**: 4 Parallel Processing Techniques in Python
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Wed, 04 Feb 2026 21:13:10 +0000
- **ID**: 19c2a80854fc31f8
- **原文链接**: [Why ML models need calibration?](https://www.dailydoseofds.com/a-crash-course-of-model-calibration-classification-models/)

## 核心要点
1. **现代模型的过度自信**：现代神经网络（如 ResNet）相比于早期的模型（如 LeNet），其平均预测置信度（confidence）大幅超出了其实际准确率（accuracy）。例如，ResNet 在 CIFAR-100 上准确率只有约 70%，但平均置信度却达到了约 90%。
2. **模型校准（Calibration）的定义**：当模型的预测概率与实际发生结果的频率一致时，则该模型是已校准的。理想情况下，如果模型预测某个事件的概率为 70%，那么在 100 次相同的预测中，应该有大约 70 次该事件真正发生。
3. **决策中的潜在危害**：未校准的模型输出过度自信的预测，在高开支的医疗诊断、政府资金配置决策中可能导致资源分配偏差或决策失效的严重危害。

## 关键引文
> "Modern neural networks being trained today are highly misleading. They appear to be heavily overconfident in their predictions."
> "A model is calibrated if the predicted probabilities align with the actual outcomes."
> "If the model isn't calibrated, it will produce overly confident predictions."

## 联动概念与实体
- [[wiki/concepts/概念_分类模型校准]]

> 📎 **物理文献**：[[raw/articles/2026-02-04_Why-ML-models-need-calibration_19c2a8.md]]
