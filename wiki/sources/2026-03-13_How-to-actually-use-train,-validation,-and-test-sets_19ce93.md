---
type: source
tags:
- MachineLearning
summary: 探讨了机器学习中训练集、验证集和测试集的标准划分职责，重点阐述了多次迭代调整导致“验证集过拟合与信息泄露”的隐性瓶颈，并提出了 K 折交叉验证与嵌套交叉验证（Nested
  CV）的机制流程，以及时序、不平衡、分组数据等复杂环境下的划分规范与预处理防泄露指南。
sources:
- raw/articles/2026-03-13_How-to-actually-use-train,-validation,-and-test-sets_19ce93.md
updated: '2026-08-03'
---

## 来源信息

- **来源**: Daily Dose of DS
- **原标题**: [How to actually use train, validation, and test sets](https://www.dailydoseofds.com/8-fatal-yet-non-obvious-pitfalls-and-cautionary-measures-in-data-science/)
- **日期**: 2026-03-13
- **作者**: Avi Chawla

## 核心要点

1. **三数据集标准职责**：
   - **训练集 (Train)**：用于模型特征探索与参数拟合。
   - **验证集 (Validation)**：用于迭代评估模型效果，进而指导超参调整和算法改进。
   - **测试集 (Test)**：必须严格隔离，仅在模型最终确定后用于进行无偏的真实泛化性能评估。绝不能将测试集用于任何特征工程、调参或模型决策。
2. **验证集过拟合与信息泄露**：若频繁依据验证集的表现调整模型（例如尝试 1000 种超参组合选最优），验证集的信息实际上就泄露到了模型选择过程中，使验证集等同于“训练集”的一部分，导致隐性的验证集过拟合。
3. **K 折交叉验证 (K-Fold CV)**：为解决单次随机划分的高方差问题，将数据均分为 K 个折，依次用 K-1 个折训练、1 个折验证，可更稳健地估计模型泛化能力。
4. **嵌套交叉验证 (Nested Cross-Validation)**：严格超参调优的黄金标准。采用双重循环：
   - **内环 (Inner Loop)**：用于在训练集上寻找最佳超参数。
   - **外环 (Outer Loop)**：评估该最佳模型在独立外环验证折上的性能，从而彻底避免由于超参调优带来的评估偏差。
5. **复杂场景下的特殊划分规范**：
   - **时序数据 (Temporal)**：严禁随机划分，必须使用 chronological 按时间序列划分（Walk-forward validation），防止用未来预测过去。
   - **不平衡数据**：必须使用分层划分（Stratified Splits）以保持各类别的比例分布一致。
   - **分组数据 (Group-based)**：若样本存在天然组属（如同一病人的多次检查），必须确保同组数据全被划分到同一折（如 GroupKFold），防止模型依靠记忆主体特定特征来作弊。
   - **预处理防泄漏 (Data Leakage)**：如标准化缩放（Scaler）和编码器（Encoder）等组件，必须只在训练集上 `.fit()`，再应用于验证/测试集，严禁在全量数据上 fit。

## 关键引文

> "If you repeatedly tune your model based on validation performance over many iterations, you risk indirectly overfitting to the validation set."
> "Once you’ve selected your best model and hyperparameters via cross-validation, retrain it on the combined train + validation data."
> "Fit all preprocessors only on the training data."

## 关联概念/实体

- **关联概念**：训练验证测试集划分

> 📎 **物理文献**：[[raw/articles/2026-03-13_How-to-actually-use-train,-validation,-and-test-sets_19ce93.md]]
