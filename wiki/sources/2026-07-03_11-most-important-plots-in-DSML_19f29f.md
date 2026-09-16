---
type: source
tags:
- MachineLearning
summary: 系统归纳了数据科学与机器学习中最重要且必须掌握的 11 种诊断、评估与可解释性图表，简要说明了其物理意义与主要应用准则。
sources:
- raw/articles/2026-07-03_11-most-important-plots-in-DSML_19f29f.md
updated: '2026-08-04'
---

## 来源信息

- **来源**: Daily Dose of DS
- **原标题**: [11 most important plots in DS/ML](https://www.dailydoseofds.com/11-most-important-plots-in-dsml/)
- **日期**: 2026-07-03
- **作者**: Avi Chawla

## 核心要点

1. **分布测定与对比**：
   - **KS Plot (Kolmogorov-Smirnov)**：通过计算两个累积分布函数（CDF）之间的最大垂直距离，评估两组数据分布的差异性。
   - **QQ Plot (Quantile-Quantile)**：通过绘制观测数据与理论分布的分位数对比，诊断数据是否符合某种特定分布（如正态分布）。
2. **分类评估指标**：
   - **ROC Curve (受试者工作特征曲线)**：描绘了在不同分类阈值下真阳性率（TPR）与假阳性率（FPR）之间的权衡，适合类别均衡场景。
   - **PR Curve (精确率-召回率曲线)**：展现了精确率与召回率在不同阈值下的权衡，特别适用于高度不平衡的类别场景。
3. **降维与聚类分析**：
   - **Cumulative Explained Variance Plot (累计解释方差图)**：在主成分分析（PCA）中，用于判断降维时需保留多少个主成分以捕获最大比例的信息。
   - **Elbow Curve (手肘法曲线)**：通过绘制畸变程度（Distortion）或 WCSS 随聚类数 $K$ 的变化，寻找手肘点以确定 KMeans 最佳聚类数。
   - **Silhouette Curve (轮廓系数曲线)**：当手肘法失效或难以分辨时，利用轮廓系数评估聚类的内聚度和分离度，进而确定最佳聚类数。
4. **树模型、训练优化与可解释性**：
   - **Gini-Impurity & Entropy Curve (基尼不纯度与熵曲线)**：用于决策树分裂中衡量节点纯度，以及比较这两种杂乱度量指标的权衡。
   - **Bias-Variance Tradeoff (偏差-方差折中曲线)**：探究模型复杂度与泛化误差之间的关系，用以在欠拟合与过拟合之间找到最佳平衡点。
   - **SHAP Plot (SHAP交互贡献图)**：结合博弈论 Shapley 值展示特征对单个或全局预测的贡献度和方向，兼顾特征间的交互效应。
   - **Partial Dependency Plots (PDP 偏依赖图)**：反映一个或两个特征与模型输出之间的边际效应，分 1-way PDP 和 2-way PDP。

## 关键引文

> "This visual depicts the 11 most important and must-know plots in DS:"
> "The Elbow curve is often ineffective when you have plenty of clusters. Silhouette Curve is a better alternative, as depicted above."

## 关联概念/实体

- **关联概念**：[[wiki/concepts/概念_机器学习诊断分析图表]]

> 📎 **物理文献**：[[raw/articles/2026-07-03_11-most-important-plots-in-DSML_19f29f.md]]
