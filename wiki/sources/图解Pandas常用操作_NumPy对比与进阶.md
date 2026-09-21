---
type: source
tags:
- Skill/data-analysis
- Skill/python
- 面试
summary: 四大部分完整图解 Pandas——Part 1 与 NumPy 对比 7 大优势及性能基准；Part 2 Series 与 Index 内部结构、loc/iloc、布尔索引、缺失值处理、统计函数、GroupBy；Part
  3 DataFrame 读写 CSV、构建方式、索引、算术对齐、concat/merge/join、分组与透视；Part 4 MultiIndex 多级索引。原文为
  Pandas Illustrated 翻译版。
sources:
- raw/playbooks/一图胜千言｜图解Pandas常用操作！.md
updated: '2026-07-01'
---
# 图解 Pandas 常用操作：NumPy 对比与进阶

## 来源信息

- 标题：一图胜千言｜图解Pandas常用操作！
- 作者：网络（via Python人工智能技术公众号，原文为 Pandas Illustrated 翻译）
- URL：https://mp.weixin.qq.com/s/mBAhShN4Z0FLg_r8wYXdAQ
- 基于全文 ingest（Cubox stub，无高亮）

## 核心内容

### Part 1：Pandas 展示——与 NumPy 对比

Pandas 相对 NumPy 的 7 大优势：

1. **排序**：Pandas 按标签自动对齐，NumPy 只能按位置
2. **多列排序**：DataFrame 原生支持多键排序
3. **添加列**：命名列直接赋值
4. **快速元素搜索**：Index 提供 O(1) 哈希查找
5. **列连接 join**：按索引自动对齐合并
6. **列分组 groupby**：内置分组聚合
7. **数据透视表 pivot_table**：一行生成透视表

**性能基准**：处理 NaN 后 Pandas 比 NumPy 快约 1.5x（NumPy 无原生 NaN 处理）。

### Part 2：Series 和 Index

#### Series 内部结构

- Series = NumPy vector + Index
- 两种索引方式：`loc`（按标签）与 `iloc`（按位置）
- 布尔索引：传入布尔 Series 过滤行
- Fancy indexing：传入标签列表批量选取

#### Index 对象

- RangeIndex：默认整数索引，内存高效
- Int64Index：显式整数索引
- 内存管理：Index 不可变，多个 Series 可共享同一 Index
- 唯一性：Index 不要求唯一，但唯一时性能更好（哈希查找）
- MultiIndex：多级层次索引

#### 缺失值处理

- `isna()` / `notna()`：检测缺失
- `fillna()`：填充缺失值
- `dropna()`：删除含缺失值的行/列
- 算术对齐：两个 Series 运算时按标签对齐，不匹配处产生 NaN

#### 比较与 NaN 陷阱

- `NaN != NaN` 为 True——直接 `==` 比较不可靠
- 使用 `equals()` 方法或 `isna()` 显式处理

#### 追加、插入、删除

- `pd.concat` 追加
- 按位置插入需重建
- `drop()` 按标签删除

#### 统计函数

- `std()` 默认使用 N-1 分母（样本标准差）
- `argmin` / `argmax`：返回位置索引
- `idxmin` / `idxmax`：返回标签索引
- `describe()`：自描述统计摘要

#### 重复数据与分组

- `duplicated()` / `drop_duplicates()`
- Series 级别 GroupBy：`s.groupby(keys).agg(func)`

### Part 3：DataFrames

#### 读写 CSV

- `read_csv`：自动检测分隔符、编码、日期等
- `to_csv`：导出，注意 `index=False` 避免多余索引列

#### 构建 DataFrame

- 字典构建：`{col_name: list}`
- 嵌套字典：外层 key 为列名
- NumPy 数组 + columns 参数
- 从 records 列表构建

#### 索引

- 列访问：`df['col']` 或 `df.col`
- `loc` / `iloc`：行列同时切片
- 布尔索引：`df[df['col'] > threshold]`
- `query()` 方法：字符串表达式过滤

#### DataFrame 算术

- 按标签对齐：两个 DataFrame 运算时行列标签自动对齐
- Series 广播问题：DataFrame 与 Series 运算时默认沿列广播，需注意轴方向

#### 结合 DataFrames

- `pd.concat`：垂直拼接（axis=0）或水平拼接（axis=1）
- `merge`：基于列的 SQL 风格连接（inner/left/right/outer）
- `join`：基于索引的连接
- 1:1 与 1:n 关系：merge 结果行数取决于关系类型

#### 插入与删除

- `insert()`：按位置插入列
- `drop()`：删除行或列
- `del df['col']`：原地删除列

#### 分组

- `as_index` 参数：控制分组键是否成为索引
- `agg()`：应用多个聚合函数
- `apply()`：自定义函数应用于每组
- `transform()`：返回与原 DataFrame 同形状的结果
- `pivot_table()`：分组 + 透视一步完成

#### 旋转与反旋转

- `pivot`：长转宽
- `melt`：宽转长
- `stack` / `unstack`：索引层级与列层级互转

### Part 4：MultiIndex

- 多级索引概念：用元组或 `pd.MultiIndex.from_tuples` / `from_product` 创建
- 多级切片：`loc` 支持元组索引定位到子层级
- `xs()` 方法：跨层级选取
- `swaplevel()` / `reorder_levels()`：调整层级顺序
- MultiIndex 与 GroupBy 天然配合：分组后结果常产生 MultiIndex

## 关联概念

- [[概念_Pandas核心操作图解]]
- [[概念_Pandas可视化]]
- [[概念_EDA_自动化分析工具]]

## 关联实体

- [[实体_Pandas]]

---
> 📎 **物理文献**：[[raw/playbooks/一图胜千言｜图解Pandas常用操作！.md]]