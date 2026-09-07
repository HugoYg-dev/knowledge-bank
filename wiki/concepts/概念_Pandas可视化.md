---
type: concept
tags:
- Skill/data-analysis
summary: Pandas 通过 DataFrame.plot / Series.plot 一行代码绘制多种图表，并通过 pandas.plotting 提供安德鲁斯曲线、平行坐标等高级可视化。
sources:
- wiki/sources/Pandas一行代码绘制25种美图.md
- wiki/sources/自动探索性数据分析EDA_10个Python包.md
updated: '2026-09-07'
---


# 概念_Pandas可视化

## 简介

Pandas 内置可视化能力，无需直接调用 matplotlib 即可一行代码绘图，覆盖从基础折线图到高级统计可视化。

## 核心 API

- `pandas.DataFrame.plot`
- `pandas.Series.plot`

## 支持的图表类型（kind 参数）

`line` / `bar` / `barh` / `box` / `density` / `hexbin` / `hist` / `kde` / `pie` / `scatter` / `area`

## 25 种常见可视化

折线图、条形图、堆积图、直方图、箱图、面积图、散点图、饼图、hexbin（六边形分箱）、核密度图、子图等，覆盖单变量分布、双变量关系与多子图布局。

## 高级可视化（pandas.plotting）

- `andrews_curves`：安德鲁斯曲线
- `parallel_coordinates`：平行坐标
- `autocorrelation_plot`：自相关图
- `radviz`：RadViz 多维可视化
- `bootstrap_plot`：自助法图
- `scatter_matrix`：散点矩阵
- `table`：表格

## 常用参数控制

`stacked`（堆叠）、`alpha`（透明度）、`figsize`（画布尺寸）、`subplots`（子图）、`layout`（布局）、`color`（颜色）、`legend`（图例）

## 关联

- [[实体_Pandas]]
- [[概念_Pandas核心操作图解]]
- [[Pandas一行代码绘制25种美图]]（来源）