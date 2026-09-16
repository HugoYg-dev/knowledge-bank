---
type: source
tags:
- MachineLearning
summary: 介绍在无标签情况下评估聚类质量的三种常用指标：轮廓系数（Silhouette Coefficient）、CH指数（Calinski-Harabasz
  Index）以及基于密度的聚类验证（DBCV），并对比了它们各自的计算开销与适用场景。
sources:
- raw/articles/2025-09-16_Clustering-evaluation-without-labels_199543.md
updated: '2026-08-03'
---

# 2025-09-16_Clustering-evaluation-without-labels_199543

## 来源信息
- **主题**: Clustering Evaluation Without Labels
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Tue, 16 Sep 2025
- **原始归档**: [[raw/articles/2025-09-16_Clustering-evaluation-without-labels_199543.md]]

## 核心要点
1. **无标签聚类评估的挑战**：由于缺乏外部地面真值标签，聚类评估通常非常困难，必须依赖数据的内在度量（intrinsic measures）。
2. **轮廓系数（Silhouette Coefficient）**：
   - 核心逻辑是计算数据点与其同簇内点的平均距离（$A$）与最近邻簇点的平均距离（$B$）的对比，公式为 $(B-A)/\max(B, A)$。
   - 越接近 1 说明簇间分离越好、越可靠。其主要瓶颈是计算复杂度随样本数呈二次方增长（$O(N^2)$）。
3. **Calinski-Harabasz Index (CH指数)**：
   - 基于簇间平方和（协方差）与簇内平方和的比值进行计算。
   - 在保持与轮廓系数类似物理直觉的同时，计算速度极快，在处理大规模数据集时优势明显。
4. **球形偏差（Globular Bias）**：
   - 轮廓系数和 CH 指数都偏好球形（globular/spherical）簇。若用于基于密度的聚类算法评估，可能会产生严重误导。
5. **DBCV (基于密度的聚类验证)**：
   - 专门用于解决非球形或基于密度聚类的评估问题。它同时评估簇内的密度和簇间的密度重叠度。
   - 簇内密度高且簇间重叠度低时得分高，能比传统指标更准确地评估非凸或复杂几何形状的聚类结果。

## 关键引文
- *"Evaluating clustering quality is usually difficult since we have no labels. Thus, we must rely on intrinsic measures to determine clustering quality."*
- *"Silhouette score and Calinski-Harabasz index are typically higher for globular (spherical in the case of 3D) clusters. Thus, using them on density-based clustering can produce misleading results."*

## 相关联动
- 概念页：[[concepts/概念_无标签聚类评估指标]]

---
> 📎 **物理文献**：[[raw/articles/2025-09-16_Clustering-evaluation-without-labels_199543.md]]
