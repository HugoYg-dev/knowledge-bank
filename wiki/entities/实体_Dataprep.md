---
type: entity
tags:
- Skill/data-analysis
- Skill/python
summary: 开源 Python EDA 包，基于 Pandas + Dask，10 个自动 EDA 工具中运行速度最快，几秒内生成完整分析报告。
sources:
- wiki/sources/自动探索性数据分析EDA_10个Python包.md
updated: '2026-06-30'
---

# 实体：Dataprep

## 简介

Dataprep 是一个开源 Python 包，用于分析、准备和处理数据。基于 Pandas 和 Dask DataFrame 构建，能在几秒内生成完整的探索性数据分析报告。

## 要点

- 10 个自动 EDA 包中运行速度最快
- 核心函数：`create_report(df).show_browser()`
- 基于 Dask，可处理超出内存的大规模数据集
- 报告包含：数据概览、变量分布、缺失值、相关性、重复值等

## 使用示例

```python
from dataprep.eda import create_report

report = create_report(df)
report.show_browser()
```

## 关联

- [[实体_Pandas]]
- [[概念_EDA_自动化分析工具]]

## 来源

- [[自动探索性数据分析EDA_10个Python包]]