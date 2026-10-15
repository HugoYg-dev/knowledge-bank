---
type: concept
tags:
- Skill/python
summary: 通过选择正确的数据结构、内置函数和编程范式，将 Python for 循环的性能提升 1.3x 到 970x；并依托 NumPy 向量化实现从逐个遍历到批量变换的思维演进。
aliases:
  - "Python循环优化技巧"
  - "Python循环优化"
  - "NumPy向量化优化"
sources:
- wiki/sources/加速Python循环的12种方法.md
- wiki/sources/从循环到向量化_NumPy提速的7个关键思维.md
updated: '2026-10-15'
---


# 概念_Python循环优化技巧

## 定义

通过选择正确的数据结构、内置函数和编程范式，将 Python for 循环的性能提升 1.3x 到 970x。

## 12 种方法速览

| # | 方法 | 提速 | 核心原理 |
|---|------|------|----------|
| 1 | 列表推导式 | 2x | Python 内部优化的单表达式循环 |
| 2 | 外部计算 len() | 1.6x | 避免每次迭代重新调用 len |
| 3 | Set 集合操作 | 498x | 查找 O(1) 替代嵌套 O(n) |
| 4 | 跳过不相关迭代 | 1.9x | 减少冗余计算 |
| 5 | 内联代码 | 1.35x | 消除函数调用栈开销 |
| 6 | 预计算 | 1.5x | 提前算好重复用到的值 |
| 7 | Generator 生成器 | 22x | 延迟求值 / 省内存 |
| 8 | map() | 970x | C 语言实现的内部循环 |
| 9 | lru_cache | 57x | 缓存重复计算结果 |
| 10 | NumPy 向量化 | 28x | SIMD / C 底层 |
| 11 | itertools.filterfalse | 131x | 避免创建中间列表 |
| 12 | str.join() | 1.5x | O(n) 替代 += 的 O(n²) |

## 关键原理归纳

- **函数调用开销**：循环内频繁调用函数 → 推栈/弹栈/参数传递累积开销 → 内联可消除
- **数据结构选择**：set 查找 O(1) vs list 查找 O(n)
- **C 扩展**：map / numpy 底层 C 实现绕过 Python 解释器
- **缓存**：functools.lru_cache 装饰器，LRU 策略，maxsize=None 无限增长
- **字符串**：`+=` 每次创建新对象 O(n²)，`join` 一次性分配 O(n)

## NumPy 向量化进阶思维（从遍历到变换）

NumPy 高性能源于调用底层 C/Fortran 优化库，能借助 SIMD 并行指令与连续内存一次性处理整个数组。改写循环的核心是从“逐个遍历判断”转向“描述对数据做批量变换”：

1. **布尔索引替代条件分支**：直接生成布尔掩码就地筛选赋值（如 `arr[arr > 0] *= 2`），彻底消除 `if` 分支与循环。
2. **广播机制（Broadcasting）自动对齐**：数组维度要么相等，要么其中一个为 1。在行/列标准化中，配合 `keepdims=True` 维持虚拟维度，实现零内存复制的向量化相减。
3. **分支逻辑向量化**：二分支用 `np.where(condition, x, y)`；多分支复杂区间分类使用 `np.select(condlist, choicelist, default)`，避免链式循环。
4. **花式索引（Fancy Indexing）一步查表**：用整数数组索引（如 `table[indices]`）实现批量查表映射与多维抽取。
5. **张量运算统合（np.einsum）**：利用爱因斯坦求和约定描述批量矩阵乘法（`'bij,bjk->bik'`）、转置与内积，消除多层嵌套循环。
6. **伪向量化陷阱与选型优先级**：`np.vectorize` 与 `np.apply_along_axis` 仅是代码可读性层面的语法糖包装，底层仍为 Python 逐行循环，无法提速。工程选型优先级：**纯 NumPy 原生操作 > apply_along_axis > 手写 Python 循环**。

## 来源

- [[加速Python循环的12种方法]]
- [[从循环到向量化_NumPy提速的7个关键思维]]

## 关联

- [[概念_Python函数式工具]]