---
type: source
tags:
- MachineLearning
summary: 本文详细介绍了分位数回归（Quantile Regression）及其核心损失函数分位数损失（Quantile Loss / Pinball Loss）。对比了传统最小二乘（OLS）均值点预测的局限，详细探讨了如何通过不对称的误差加权拉伸来拟合特定的百分位数预测线，并介绍了其在树模型中的工程价值。
sources:
- raw/articles/2026-07-24_Quantile-regression_19f962.md
updated: '2026-08-04'
---

# 来源摘要：Quantile regression

## 来源信息
- **标题**: Quantile regression
- **作者/发布者**: Daily Dose of DS (Avi)
- **发布日期**: 2026-07-24
- **原始链接**: [Daily Dose of DS - Quantile regression](https://www.dailydoseofds.com/generalized-linear-models-glms-the-supercharged-linear-regression/)
- **关联概念**: [[概念_Pinball_Loss_分位数回归]], [[概念_机器学习损失函数]]

## 核心要点
- **均值回归的局限**：传统的普通最小二乘法（OLS）回归模型通常只生成一个标量点估计（Point Estimate），代表特定输入下输出的均值。但在实际应用（如薪资预测、预测区间评估等）中，单一点估计无法捕获目标变量的概率分布。
- **分位数回归的引入**：分位数回归能够估计目标变量在给定输入下的任意分位数（如 25th, 50th, 75th percentiles），帮助决策者评估最佳与最差场景，捕捉数据的不确定性。
- **误差的不对称加权机制**：
  - 传统线性回归的均方误差（MSE）对偏离预测线两侧相同距离的预测点施加同等的惩罚。
  - 分位数回归的核心技巧是对正误差（$y > \hat{y}$，即实际值高于预测线）和负误差（$y < \hat{y}$，即实际值低于预测线）施加不对称的权重。
- **分位数损失函数（Pinball Loss）**：分位数损失函数通过一个权重系数 $w$（通常表示分位数 $\tau$）对误差进行不对称参数化。
  - 拟合 75% 分位数线时，给正误差分配更高的权重（如 $w = 0.75$），将预测线往上拉。
  - 拟合 25% 分位数线时，给负误差分配更高的权重（如 $1-w = 0.75$，即 $w = 0.25$），将预测线往下拉。
- **工程应用**：通过训练针对不同分位数参数 $w$ 的多个独立回归模型，可以在推断时组合出预测区间。此外，分位数损失非常适合树模型，如 LightGBM 原生支持分位数损失目标函数，极大方便了不确定性区间的估算。

## 关键引文
> Regression models typically generate a point estimate, which isn’t always useful.

> To generate the 75th percentile line, assign more weight to the green points [positive error]. This pulls the prediction line upward.

> Quantile regression works particularly well with tree-based models. LightGBM regression, for instance, natively supports quantile objective functions.

---
> 📎 **物理文献**：[[raw/articles/2026-07-24_Quantile-regression_19f962.md]]
