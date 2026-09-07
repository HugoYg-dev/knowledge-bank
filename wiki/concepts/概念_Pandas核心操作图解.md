---
type: concept
tags:
- Skill/data-analysis
- Skill/python
- 面试
summary: Pandas 核心操作的图解总结——涵盖选择过滤、排序、分组聚合、连接合并、变形与索引管理，以及与 NumPy 的关键差异。
sources:
- wiki/sources/Pandas一行代码绘制25种美图.md
updated: '2026-09-07'
---


# 概念_Pandas核心操作图解

## 简介

以图解方式系统梳理 Pandas 的核心数据操作，适合面试复习和日常速查。

## 数据操作分类

### 选择与过滤

- `loc`：基于标签选择
- `iloc`：基于位置选择
- 布尔索引：条件筛选
- `query`：字符串表达式查询

### 排序

- `sort_values`：单列 / 多列排序
- 稳定排序（kind='mergesort'）保持相等元素原有顺序

### 分组聚合

- `groupby` + `mean` / `sum` / `agg` / `apply` / `transform`
- `agg` 支持多聚合函数字典
- `transform` 返回同形状 DataFrame

### 连接合并

- `join`：基于索引对齐
- `merge`：基于列匹配，支持 1:1 和 1:n 关系
- `concat`：垂直（axis=0）/ 水平（axis=1）堆叠

### 变形

- `pivot_table`：数据透视
- `melt`：宽表转长表
- `stack` / `unstack`：层级索引与列之间转换
- `pivot`：无聚合的简单重塑

### 索引管理

- `set_index` / `reset_index`
- `RangeIndex`：默认整数索引
- `MultiIndex`：层级索引

## NumPy vs Pandas 关键差异

| 维度 | NumPy | Pandas |
|------|-------|--------|
| 缺失值处理 | 需手动 nansum 等 | 自动正确处理 NaN |
| 大数组 nansum | 较慢 | 快约 1.5x |
| 添加列 | 需重分配内存 | O(1) |
| 元素查找 | 线性扫描 | Index O(1) |
| join/groupby/pivot | 需自行实现 | 开箱即用 |

## Series 内部结构

Series = NumPy vector + Index 对象，Index 提供 O(1) 元素查找和标签对齐。

## 缺失值处理

- 检测：`isna()` / `notna()`
- 填充：`fillna()`
- 删除：`dropna()`
- 插值：`interpolate()`
- 算术运算自动忽略 NaN

## 性能提示

确定无缺失值时使用 `df.column.values.sum()` 跳过 NaN 检查，可获 3-30x 提速。

## 关联

- [[实体_Pandas]]
- [[概念_Pandas可视化]]