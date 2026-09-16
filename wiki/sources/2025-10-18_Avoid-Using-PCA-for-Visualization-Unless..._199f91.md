---
type: source
tags:
- MachineLearning
summary: 探讨主成分分析（PCA）用于数据可视化时的局限性，并介绍如何通过累计解释方差（CEV）曲线来验证 2D PCA 可视化的可信度，最后指出 t-SNE、UMAP
  等专用算法更适合高维数据的可视化任务。
sources:
- raw/articles/2025-10-18_Avoid-Using-PCA-for-Visualization-Unless..._199f91.md
updated: '2026-08-03'
---

# Avoid Using PCA for Visualization Unless...

## 来源信息
- **来源**: Daily Dose of DS (Avi Chawla)
- **原始链接**: [Daily Dose of DS Website](https://www.dailydoseofds.com/formulating-the-principal-component-analysis-algorithm-from-scratch/)
- **归档物理文件**: [[raw/articles/2025-10-18_Avoid-Using-PCA-for-Visualization-Unless..._199f91.md]]

## 核心要点
1. **PCA 降维本质**：PCA 是一种线性降维技术，通过提取数据方差最大的主成分来压缩特征维度。但在实践中，人们常直接将高维数据降至 2D 以便进行可视化。
2. **2D 可视化的局限性**：只有当前两个主成分（PC1 和 PC2）能够解释原始数据中绝大部分的方差时，2D PCA 可视化才有实际意义。如果前两主成分的累计解释方差比例过低（例如仅有 55%），降维后的可视化图像将具有极大的误导性，无法准确反映原始数据的分布。
3. **累计解释方差（CEV）曲线**：可以使用累计解释方差（Cumulative Explained Variance）曲线来校验 PCA 可视化的可信度。在 Scikit-Learn 中，可以通过 `explained_variance_ratio_` 属性来获取各主成分的方差占比，并绘制累积图。
4. **降维维度的确定**：CEV 曲线除了校验 2D 可视化，更重要的用途是帮助确定降维时应该保留的主成分数量（例如，在方差损失容忍范围内保留 5 个维度）。
5. **专用可视化算法的推荐**：对于高维数据的可视化，PCA 往往表现不佳，应当使用专门为此设计的非线性降维可视化技术，例如 [[wiki/concepts/概念_t-SNE算法]]、UMAP 等。

## 关键引文
- "Thus, using PCA for visualization by projecting the data to 2-dimensions only makes sense if the first two principal components collectively capture most of the original data variance. This is rarely true in practice."
- "For visualization, however, use techniques specifically designed for it, like t-SNE, UMAP, etc."

---
关联概念：
- [[wiki/concepts/概念_主成分分析_PCA]]
- [[wiki/concepts/概念_t-SNE算法]]

> 📎 **物理文献**：[[raw/articles/2025-10-18_Avoid-Using-PCA-for-Visualization-Unless..._199f91.md]]
