---
type: concept
tags:
- Skill/data-analysis
- Skill/python
summary: 用几行 Python 代码完成完整探索性数据分析的工具集，10 个主流自动 EDA 包分为全自动报告型、自动可视化型、半自动定制型和 ML 集成型四类。
sources:
- wiki/sources/自动探索性数据分析EDA_10个Python包.md
updated: '2026-09-07'
---


# 概念_自动EDA工具

## 简介

EDA（Exploratory Data Analysis，探索性数据分析）自动化，指用几行 Python 代码即可执行完整的探索性数据分析——自动生成数据概览、缺失值统计、分布图、相关性分析等报告，省去手写大量分析代码的工作。

## 10 个主流自动 EDA 包分类

### 全自动报告型

- **D-Tale**：基于 Flask 后端 + React 前端的交互式分析工具，可在浏览器中交互查看数据
- **Pandas-Profiling**：一行 `df.profile_report()` 生成完整 HTML 报告
- **Sweetviz**：强项是目标值比较与数据集对比
- **Dataprep**：运行速度最快，基于 Pandas + Dask，可处理大规模数据
- **DataTile**：对 `describe` 的扩展增强

### 自动可视化型

- **AutoViz**：一行代码自动可视化任意数据集
- **edaviz**：已并入 bamboolib

### 半自动定制型

- **KLib**：需手动编写每个分析函数，适合定制化场景

### ML 集成型

- **Dabl**：关注数据预处理 + 模型搜索
- **SpeedML**：整合 Pandas + Numpy + Sklearn + XGBoost

## 选型建议

- **Dataprep**：最快，常用首选
- **AutoViz / D-Tale**：交互体验好
- **KLib**：适合需要定制化分析流程的场景

## 关联

- [[实体_Dataprep]]
- [[实体_Pandas]]
- [[自动探索性数据分析EDA_10个Python包]]（来源）