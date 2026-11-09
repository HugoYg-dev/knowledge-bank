---
type: "source"
tags:
  - "面试"
  - "Skill/python"
summary: "通过中位数计算考察候选人编程基础、排序副作用、边界条件与快速选择进阶维度的软件工程面试题设计"
sources:
  - "raw/articles/A software engineering interview question I like-computing the median.md"
updated: "2026-11-09"
---

# 来源：A software engineering interview question I like: computing the median

## 来源信息
- **标题**：a software engineering interview question I like: computing the median
- **作者**：Kris Shamloo
- **日期**：2026-11-08
- **原文链接**：https://krisshamloo.com/blog/007
- **物理文献**：[[raw/articles/A software engineering interview question I like-computing the median.md]]

## 核心要点
- **拒绝脑筋急转弯（No Puzzle Questions）**：作者倾向于在技术面试中避开脑筋急转弯类低价值题目，转而选择表象简单但拥有多维度纵深、可层层展开深入讨论的问题。
- **基本功检验（Fizz-Buzz 级信号）**：计算中位数要求对数组进行规约与统计，能快速验证候选人是否具备基本的代码编写与防御性编程能力（如空数组异常处理）。
- **API 设计与可变性权衡（Mutation vs Performance）**：输入数组需要排序，引申出由函数自身排序还是由调用者预先排序的 API 设计权衡；在 Python 等按引用传递对象的语言中，讨论原地修改 `numbers.sort()` 与返回副本 `sorted(numbers)` 对外部状态和性能的影响。
- **边界条件与调试排错（Off-by-one Trap）**：计算中位数天然存在分支（偶数长度求中间两数均值、奇数长度直接取中位值），容易暴露经典的差一错误（Off-by-one），为观察候选人的现场排错与调试能力提供契机。
- **标准库与进阶算法延展**：
  - 候选人可借此展现对语言标准库（如 Python statistics.median）的熟稔程度；
  - 进阶探讨可延伸至统计学中中位数相比均值在抗离群值方面的鲁棒性；
  - 算法深度上可探讨从常规排序的 $O(n \log n)$ 优化为快速选择算法（Quickselect）实现 $O(n)$ 平均时间复杂度的进阶技巧。

## 关联讨论（普通纯文本）
- 软件工程技术面试题设计
- Python 引用传递与可变性副作用
- 快速选择算法（Quickselect）与中位数复杂度优化
- 防御性异常处理与边界测试

---
> 📎 **物理文献**：[[raw/articles/A software engineering interview question I like-computing the median.md]]
