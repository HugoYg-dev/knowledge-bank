---
type: source
tags:
- Skill/data-analysis
summary: '`matplotlib` 是 Python 生态中最流行的数据可视化框架，功能强大但默认样式简陋，想做出简洁商务风格图表往往需要编写大量代码调整参数。本文介绍
  dufte 库——通过简短代码自动改造默认 matplotlib 图表样式。`pip install dufte` 安装后，将'
sources:
- raw/playbooks/一行代码让 matplotlib 图表变高大上.md
updated: '2026-07-01'
cubox_url: https://cubox.pro/web/card/7128377660480160628
date_collected: 2023-11-26
---
# 一行代码让 matplotlib 图表变高大上

## 来源信息

- **标题**：一行代码让 matplotlib 图表变高大上
- **作者**：费弗里（程序员的那些事）
- **URL**：https://mp.weixin.qq.com/s/6TrDtLHqBBYEfCwJobZeAg



## 概述

`matplotlib` 是 Python 生态中最流行的数据可视化框架，功能强大但默认样式简陋，想做出简洁商务风格图表往往需要编写大量代码调整参数。本文介绍 dufte 库——通过简短代码自动改造默认 matplotlib 图表样式。`pip install dufte` 安装后，将 dufte 的几个关键 API 穿插进常规 matplotlib 绘图流程即可。

## dufte 的四个主要功能

### 1. 主题设置
dufte 最重要的功能是自带的主题风格。matplotlib 有两种设置主题的方式：
- `plt.style.use(主题)` 全局设置——一般不建议。
- `with plt.style.context(主题):` 在 `with` 作用范围内局部使用主题——文中推荐方式。

用法是 `with plt.style.context(dufte.style):` 包裹绘图代码。文中以折线图、柱状图为例演示。dufte 自带一套简洁绘图风格，主张去除多余的轴线，只保留必要的参考线，适用于日常工作的通用出图需求。

### 2. 自动图例美化
dufte 自带一套图例风格化策略，只需在绘图过程中用 `dufte.legend()` 代替 matplotlib 原有的 `legend()`。对于多系列图表，一行 `dufte.legend()` 就能自动添加别致的图例说明。

### 3. 柱状图自动标注
通过 `dufte.show_bar_values()`，只要之前的绘图流程设置了 `xticks`，它就会自动往柱体上标注对应的 y 值信息。

## 配套细节
- 中文显示：从本地注册思源宋体 `font_manager.FontProperties(fname='NotoSerifSC-Regular.otf')`，绘图时通过 `fontproperties=` 参数应用。
- 文中评价 dufte 是处于开发初期的库，未来会加入更多实用功能。

## 关联
- 概念：[[概念_matplotlib样式美化]]
- 实体：dufte、[[实体_Pandas]]（同属 data-analysis 可视化工具链）
- 相关来源：[[Pandas一行代码绘制25种美图]]

---
> 📎 **物理文献**：[[raw/playbooks/一行代码让 matplotlib 图表变高大上.md]]