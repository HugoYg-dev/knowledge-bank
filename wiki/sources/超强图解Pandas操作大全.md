---
type: source
tags:
- Skill/data-analysis
- 面试
summary: 通过可视化图解讲解 Pandas 核心操作：sort_values 排序、列选择、groupby 分组聚合（单列/多列/多聚合函数）、loc 布尔索引过滤、删除列、join
  连接、merge 合并、pivot_table 透视表、melt 宽转长、pivot 长转宽、stack/unstack 压栈展开、reset_index/set_index
  索引操作，每个操作配图解释执行步骤。
sources:
- raw/playbooks/超强图解 Pandas，建议收藏.md
updated: '2026-07-01'
---
# 超强图解 Pandas 操作大全

## 来源信息

- 标题：超强图解 Pandas，建议收藏
- 作者：网络（via Python人工智能技术公众号）
- URL：mp.weixin.qq.com（MzI0MzU2NzQ1OA==...）
- 基于全文 ingest（Cubox stub，无高亮）

## 核心内容

文章通过可视化图解逐步讲解 Pandas 常用操作，每个操作配图说明执行过程。

### 排序与选择

- **sort_values**：按指定列的值排序
- **selecting**：选择一列或多列

### 分组聚合 Pandas核心操作图解

- **groupby + mean**：按某列分组并求均值
- **groupby 多列分组**：按多个列组合分组
- **groupby + 多聚合函数**：同时应用 sum / mean / std 等多个聚合函数

### 过滤与删除

- **filtering**：用 `loc` 布尔索引过滤行列
- **dropping columns**：删除指定列

### 连接与合并 Pandas核心操作图解

- **joining**：基于索引连接，如 `ppl.join(dogs)`
- **merging**：基于列连接，指定 `left_on` / `right_on` / `how`

### 透视与重塑

- **pivot_table**：数据透视表
- **melting**：宽表转长表
- **pivoting**：长表转宽表
- **stacking**：列索引压栈（转为行索引层级）
- **unstacking**：行索引展开（转为列索引层级）

### 索引操作

- **resetting index**：重置索引
- **setting index**：设置索引


## 关联实体

- Pandas

---
> 📎 **物理文献**：[[raw/playbooks/超强图解 Pandas，建议收藏.md]]