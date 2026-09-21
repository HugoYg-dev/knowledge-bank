---
type: entity
tags:
- Skill/data-analysis
- Skill/python
summary: Python 数据分析核心库，基于 NumPy 构建，提供 Series/DataFrame 数据结构及完整的数据操作与可视化能力。
sources:
- wiki/sources/Pandas一行代码绘制25种美图.md
- wiki/sources/PyTorch训练代码模板.md
- wiki/sources/一行代码让matplotlib图表变高大上.md
- wiki/sources/自动探索性数据分析EDA_10个Python包.md
updated: '2026-09-07'
---

# 实体：Pandas

## 简介

Pandas 是 Python 数据分析核心库，基于 NumPy 构建，提供高性能、易用的数据结构和数据分析工具。

## 主要数据结构

- **Series**：一维带标签数组，内部由 NumPy vector + Index 对象组成
- **DataFrame**：二维带标签表格结构

## 核心能力

- 数据读写：CSV / Excel / SQL / JSON / Parquet
- 索引：`loc`（标签）/ `iloc`（位置）
- 分组聚合：`groupby` + `agg` / `apply` / `transform`
- 合并连接：`merge` / `join` / `concat`
- 数据透视：`pivot_table` / `melt` / `stack` / `unstack`
- 可视化：`.plot`（支持 line/bar/scatter/hist/box/pie 等多种图表）

## 特点

- 正确处理缺失值（NaN），算术运算自动忽略
- 标签对齐算术——不同索引的 Series 自动对齐后计算
- Index 提供 O(1) 元素查找
- 添加列 O(1)，无需重分配内存

## 生态扩展

自动 EDA 工具：[[实体_Dataprep]] / pandas-profiling / sweetviz / AutoViz / D-Tale 等

## 关联

- [[概念_EDA_自动化分析工具]]
- [[概念_Pandas可视化]]
- [[概念_Pandas核心操作图解]]

## 来源

- [[自动探索性数据分析EDA_10个Python包]]
- [[Pandas一行代码绘制25种美图]]