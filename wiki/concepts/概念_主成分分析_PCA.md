---
type: concept
tags:
- Skill/data-analysis
summary: PCA 通过主成分进行降维，但只有前两个主成分解释了大部分原始方差时才适合二维可视化，累计解释方差曲线可用于验证并选择保留维数。
sources:
- wiki/sources/2025-10-18_Avoid-Using-PCA-for-Visualization-Unless..._199f91.md
- wiki/sources/2025-11-12_25-most-important-mathematical-definitions-in-DS_19a79c.md
- wiki/sources/2026-08-31_Sparse-random-projections_1a0580f9aa7f67f1.md
updated: '2026-09-09'
---
# 主成分分析 (Principal Component Analysis, PCA)

## 定义与数学降维原理

**主成分分析 (PCA)** 是一种最经典的线性降维方法。其基本思想是通过正交变换，将原始高维空间中可能存在线性相关的变量，投影到一组新的正交且线性无关的综合变量上，这组新变量被称为**主成分 (Principal Components, PCs)**。

### 数学原理与解释方差
在数学上，PCA 可以通过对协方差矩阵进行**特征值分解 (Eigenvalue Decomposition)** 或对数据矩阵进行**奇异值分解 (Singular Value Decomposition, SVD)** 来实现：
1. **方向选择**：投影后的第一主成分 $PC_1$ 指向数据方差最大的方向，第二主成分 $PC_2$ 在与 $PC_1$ 正交的超平面中指向方差最大的方向，依此类推。
2. **解释方差 (Explained Variance)**：每个特征向量对应的特征值 $\lambda_i$ 大小代表了该主成分所解释的原始数据方差的多寡。主成分 $i$ 的**解释方差占比 (Explained Variance Ratio)** 定义为：
   $$Ratio_i = \frac{\lambda_i}{\sum_{j=1}^{D} \lambda_j}$$
   方差占比越高，说明该主成分保留的原始信息量越多。

---

## 2D PCA 可视化的局限性

在工程实践中，开发者常直接将高维数据投影到二维平面（仅保留前两个主成分 $PC_1$ 和 $PC_2$）来进行数据可视化。**然而，这种做法在多数情况下是危险且具有误导性的。**

- **信息丢失风险**：2D PCA 可视化能真实反映原始高维空间结构的前提是——前两个主成分必须能解释原始数据中**绝大部分**的方差。
- **误导性结论**：如果在高维空间中，前两个主成分的累积方差占比很低（例如仅有 50% - 60%），说明还有将近一半的有用信息存在于剩下的维度中。此时直接基于 2D PCA 散点图得出的类别聚类边界、异常值分布等结论，极有可能是失真的。

---

## 累计解释方差 (CEV) 曲线的工程应用

为了科学校验可视化图像的可信度并确定最合理的降维维度，工程上通常使用**累计解释方差 (Cumulative Explained Variance, CEV)** 曲线。

### 1. 累计解释方差的计算与实现
在 Python Scikit-Learn 中，可以通过训练好的 `PCA` 对象的 `explained_variance_ratio_` 属性计算累积和，并绘制出阶梯状或折线图：

```python
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA

# 拟合 PCA
pca = PCA().fit(X)

# 计算累计解释方差
cumulative_variance = np.cumsum(pca.explained_variance_ratio_)

# 绘制 CEV 曲线
plt.plot(range(1, len(cumulative_variance) + 1), cumulative_variance, marker='o')
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance')
plt.show()
```

### 2. CEV 曲线的两个核心工程用途
- **可视化校验**：在进行 2D 可视化前，先检查 $PC_1$ 和 $PC_2$ 的累积解释方差。若累积值较高（如 > 80%），则 2D 散点图是可信的；若累积值过低，则应放弃 PCA 可视化。
- **确定降维维度**：如果降维是为了下游机器学习模型（如分类、聚类）提取特征，可以通过 CEV 曲线观察在不同维度下的信息保留度。通常选择曲线上的“拐点（Elbow）”，或是当累计解释方差达到某一预设容忍阈值（例如 90% 或 95%）时对应的维度数。

---

## 可视化替代方案

由于 PCA 是线性降维技术，对于具有复杂非线性结构（如流行流形结构）的高维数据，PCA 无法有效展平。若首要目的是进行**低维可视化**，建议选用专门为可视化设计的非线性流形学习算法：
- **[[wiki/concepts/概念_t-SNE算法]]**：通过概率分布匹配保留数据的局部邻域结构，尤其擅长聚类可视化。
- **UMAP (Uniform Manifold Approximation and Projection)**：基于黎曼几何和代数拓扑，在保留局部结构的同时能比 t-SNE 更好地保留全局结构，且计算效率更高。

---

## 超高维计算瓶颈与降维替代方案

- **三次时间复杂度限制**：PCA 的时间复杂度约为 $O(\min(d^3, n^3) + d^2 n)$，在特征维度 $d$ 极高（如 $d \ge 1000$）时，协方差矩阵分解或 SVD 计算开销急剧膨胀，在工程上往往导致超时或显存溢出。
- **超高维线性降维优选**：对于特征维度巨大的海量数据（$d \ge 700+$），推荐使用 [[concepts/概念_稀疏随机投影|概念_稀疏随机投影]]（Sparse Random Projection）。基于 Johnson-Lindenstrauss 引理，它通过轻量稀疏矩阵乘法在保持点对欧几里得距离的同时突破算力瓶颈。

