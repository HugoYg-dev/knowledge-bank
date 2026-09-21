---
type: source
tags:
- MachineLearning
summary: 探讨了 kNN 算法在不平衡数据集上的局限性，并详细介绍了两种改进方案：距离权重 kNN（在 sklearn 中配置 weights='distance'）和动态调整超参数
  k 的算法。
sources:
- raw/articles/2025-11-28_How-to-use-kNNs-for-imbalanced-datasets_19acc3.md
updated: 2026-08-03
---

# 来源信息
- **标题**: How to Use kNNs for Imbalanced Datasets
- **作者**: Daily Dose of DS
- **日期**: 2025-11-28
- **原始物理文献**: [[raw/articles/2025-11-28_How-to-use-kNNs-for-imbalanced-datasets_19acc3.md]]

# 联动概念
- 不平衡数据的 kNN 优化

# 核心要点
1. **传统 kNN 易受大类支配**：kNN 算法对超参数 $k$ 高度敏感。在类别不平衡数据集上，传统的多数投票机制完全依赖邻居中各类别数量的绝对贡献，导致近邻中的大类容易淹没少数类，即使测试样本与少数类距离极近也可能无法被正确分类。
2. **优化方案一：距离权重 kNN（Distance-weighted kNN）**：考虑邻居到测试样本的距离，将表决权重设为距离的倒数。这样，距离极近的少数类样本将获得极高的权重，从而抵消远距离大类样本的支配。该方法可通过 Scikit-Learn 的 `weights='distance'` 配置启用。
3. **优化方案二：动态调整 $k$ 算法**：为每个测试样本动态更新超参数 $k$。步骤为：
   - 首先寻找常规的 $k$ 个最近邻。
   - 找出这 $k$ 个邻居中包含的所有类别，并获取这些类别在整个训练集中的样本总数。
   - 将超参数 $k$ 动态更新为 $k' = \min(k, \text{邻居类别训练集样本数})$，并在前 $k'$ 个邻居中进行投票。
4. **动态 $k$ 算法的优势**：若最近邻中包含少数类，该机制会缩减 $k$ 限制大类支配；若不包含少数类，则不更新 $k$ 保持全局评估模式。不过目前大多数主流开源库（如 sklearn）未原生实现该算法。

# 关键引文
- "The problem with Step 2 is that it is entirely based on class contribution. So the class that maximally contributes to the `k` nearest neighbors is picked. But this fails when you have imbalanced datasets."
- "If a minority class appears in the top `k` nearest neighbor, the update rule will reduce the value of `k` so that the majority class does not dominate."

> 📎 **物理文献**：[[raw/articles/2025-11-28_How-to-use-kNNs-for-imbalanced-datasets_19acc3.md]]
