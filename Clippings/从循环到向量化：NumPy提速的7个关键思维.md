---
title: "从循环到向量化：NumPy提速的7个关键思维"
source: "https://www.cnblogs.com/wang_yb/p/23291209"
author:
  - "[[wang_yb]]"
published: 2026-10-13
created: 2026-10-14
description: "用 NumPy 写代码的人很多，但很多人写出来的代码还是慢。 原因通常只有一个：虽然用了 NumPy 的数组，但逻辑上还是在一行一行地 for 循环。 NumPy 快的根源在于底层调用的是 C 和 Fortran 的优化库，能一次性处理整个数组——前提是你得把循环改成向量化操作。 这需要的不是背 A"
tags:
  - "clippings"
---
[合集 - numpy(11)](https://www.cnblogs.com/wang_yb/collections/8152)

[1.【numpy基础】--基础操作](https://www.cnblogs.com/wang_yb/p/17493320.html) [2.【numpy基础】--通用计算](https://www.cnblogs.com/wang_yb/p/17495983.html) [3.【numpy基础】--聚合计算](https://www.cnblogs.com/wang_yb/p/17505273.html) [4.【numpy基础】--广播计算](https://www.cnblogs.com/wang_yb/p/17511013.html) [5.【numpy基础】--数组过滤](https://www.cnblogs.com/wang_yb/p/17515408.html) [6.【numpy基础】--数组索引](https://www.cnblogs.com/wang_yb/p/17520930.html) [7.【numpy基础】--数组排序](https://www.cnblogs.com/wang_yb/p/17522409.html) [8.【numpy基础】--结构化](https://www.cnblogs.com/wang_yb/p/17532130.html) [9.【numpy基础】--数组简介](https://www.cnblogs.com/wang_yb/p/17489127.html) [10.什么是范数？用 NumPy 动手算一遍就明白了](https://www.cnblogs.com/wang_yb/p/23222493)

11.从循环到向量化：NumPy提速的7个关键思维

用 NumPy 写代码的人很多，但很多人写出来的代码还是慢。

原因通常只有一个：虽然用了 NumPy 的数组，但逻辑上还是在一行一行地 for 循环。

NumPy 快的根源在于底层调用的是 C 和 Fortran 的优化库，能一次性处理整个数组——前提是你得把循环改成向量化操作。

这需要的不是背 API，而是换一种思维方式：从 **"逐个遍历判断"** 变成 **"描述对数据做什么变换，让底层去批量执行"** 。

本文列举 7 个具体场景，演示从循环到向量化的改写过程，每个场景都带模拟数据，你可以直接跑起来看效果。

先看下面这张图，感受一下两种思维方式的不同：

![](https://img2024.cnblogs.com/blog/83005/202610/83005-20261013213259574-1947276060.png)

## 1\. 布尔索引：条件筛选不用 if

做数据分析时，经常遇到"满足条件的元素做一种处理，不满足的做另一种"的需求。

比如一份销售数据，正数是实际销售额、负数是退货金额，现在要把所有实际销售额翻倍，退货金额保持不变。

先造一批模拟数据：

```python
import numpy as np

np.random.seed(42)
sales = np.random.normal(loc=50, scale=30, size=100_000)
# 大致是均值为50、标准差为30的正态分布，会有不少负数
```

循环写法是这样的——逐个判断，正的翻倍，负的保留：

```python
result_loop = np.empty_like(sales)
for i in range(len(sales)):
    if sales[i] > 0:
        result_loop[i] = sales[i] * 2
    else:
        result_loop[i] = sales[i]
```

向量化写法只需要两行：

```python
result_vec = sales.copy()
result_vec[sales > 0] *= 2
```

`sales > 0` 生成一个与 `sales` 等长的布尔数组， `True` 表示该位置满足条件。

用这个布尔数组做索引，NumPy 只选中 `True` 对应的元素，然后对它们执行 `*= 2` 。

不需要循环，不需要 `if` ，一行搞定筛选加修改。

思维转变的关键点： **不再逐个问"你是不是正数"，而是直接生成一个"谁是正数"的掩码，然后对掩码选中的区域操作** 。

## 2\. 广播：不同形状的数组直接运算

数据标准化是常见操作：每行数据减去该行的均值。

假设有一个 1000 行 × 500 列的特征矩阵，每行代表一个样本，每列是一个特征。

```python
np.random.seed(42)
features = np.random.rand(1000, 500)
```

循环写法：逐行减去该行均值：

```python
row_means = np.mean(features, axis=1)  # shape: (1000,)
centered_loop = np.zeros_like(features)
for i in range(features.shape[0]):
    centered_loop[i] = features[i] - row_means[i]
```

这里有个坑： `row_means` 的形状是 `(1000,)` ，而 `features` 是 `(1000, 500)` ，直接相减会报维度不匹配的错。循环里没问题，因为每次取出一行来减一个标量。

向量化写法的关键在于 `keepdims=True` ：

```python
row_means = np.mean(features, axis=1, keepdims=True)  # shape: (1000, 1)
centered_vec = features - row_means
```

`keepdims=True` 让 `row_means` 保持为 `(1000, 1)` 而不是 `(1000,)` 。当 `(1000, 500)` 减 `(1000, 1)` 时，NumPy 的广播机制自动把第二维的 1 "虚拟展开"为 500，相当于把每行的均值复制到该行所有列上，然后逐元素相减。

这个展开是虚拟的，不会真的分配内存复制数据。

![](https://img2024.cnblogs.com/blog/83005/202610/83005-20261013213259556-1130638858.png)

广播的兼容规则很简单： **两个数组在每个维度上要么相等，要么其中一个为 1** 。为 1 的维度会被虚拟扩展。

掌握这个规则，很多"需要逐行/逐列处理"的场景都能一行搞定。

## 3\. np.where / np.select：分支逻辑的向量化

温度传感器采集了一天的数据，需要把温度分类：0°C 以下为"冰冻"，0~20°C 为"凉爽"，20°C 以上为"温暖"。

```python
np.random.seed(42)
temps = np.random.uniform(-10, 40, size=100_000)
```

循环写法里，分支逻辑是绕不开的：

```python
labels_loop = []
for t in temps:
    if t < 0:
        labels_loop.append('freezing')
    elif t < 20:
        labels_loop.append('cool')
    else:
        labels_loop.append('warm')
labels_loop = np.array(labels_loop)
```

向量化写法用 `np.select()` ，把所有条件和对应的值列出来：

```python
labels_vec = np.select(
    [temps < 0, temps < 20, temps >= 20],
    ['freezing', 'cool', 'warm'],
    default='unknown'
)
```

`np.select()` 按顺序检查每个条件，返回第一个为 `True` 的条件对应的值。

如果有多个条件同时为 `True` ，先到先得。

如果是简单的二分支， `np.where()` 更简洁：

```python
scores = np.random.randint(0, 100, size=50_000)
results = np.where(scores >= 60, 'pass', 'fail')
```

`np.where(condition, x, y)` 就是一个向量化的三元表达式：条件为 `True` 取 `x` ，否则取 `y` 。

## 4\. 花式索引：批量查表一步到位

假设有一个编码表，索引 0~4 分别对应 5 种商品类别。

现在有一批订单，每条记录了商品类别编号，需要查出对应的类别名称。

```python
category_table = np.array(['食品', '服装', '电子', '家居', '图书'])
orders = np.random.randint(0, 5, size=100_000)
```

循环写法是逐个查表：

```python
cats_loop = []
for idx in orders:
    cats_loop.append(category_table[idx])
cats_loop = np.array(cats_loop)
```

向量化写法只需要一行：直接用整数数组做索引：

```python
cats_vec = category_table[orders]
```

`category_table[orders]` 会一次性从 `category_table` 中取出 `orders` 每个位置指定的元素，拼成新数组。

这在多维场景下同样适用：

```python
# 二维花式索引：同时指定行和列
matrix = np.arange(20).reshape(4, 5)
row_idx = np.array([0, 2, 3])
col_idx = np.array([1, 3, 4])
values = matrix[row_idx, col_idx]  # 取出 matrix[0,1], matrix[2,3], matrix[3,4]
# 结果: array([ 1, 13, 19])
```

花式索引在实现类别编码、构建直方图、从大表中抽取子集等场景下非常实用。

## 5\. np.vectorize：让标量函数接受数组

有些函数逻辑复杂，一时难以用纯 NumPy 操作重写，但又希望能接受数组输入。

比如一个非线性变换：负数取负平方根，非负数取平方。

```python
def nonlinear(x):
    if x < 0:
        return -np.sqrt(abs(x))
    else:
        return x ** 2
```

循环写法：

```python
data = np.random.randn(10_000)
result_loop = np.array([nonlinear(x) for x in data])
```

`np.vectorize()` 可以把标量函数包装成能接受数组的形式：

```python
vec_nonlinear = np.vectorize(nonlinear)
result_vec = vec_nonlinear(data)
```

代码确实简洁了，但这里要强调一点： `np.vectorize()` \*\* 不会提速\*\*。

它底层仍然是逐个调用原函数的 Python 循环，只是帮你省去了手写循环的麻烦。

真正想提速，还是得用 NumPy 原生操作重写：

```python
result_fast = np.where(data < 0, -np.sqrt(np.abs(data)), data ** 2)
```

所以 `np.vectorize()` 的定位是"代码可读性的过渡方案"，而不是性能方案。

能用布尔索引、 `np.where` 等原生操作替代时，优先用原生操作。

## 6\. np.einsum：复杂张量运算的统一表达

深度学习里经常遇到批量矩阵乘法：32 组 (10×20) 和 (20×15) 的矩阵对，每组各自相乘。

```python
np.random.seed(42)
batch_A = np.random.rand(32, 10, 20)
batch_B = np.random.rand(32, 20, 15)
```

循环写法：逐组调用 `np.dot`:

```python
result_loop = np.zeros((32, 10, 15))
for i in range(32):
    result_loop[i] = np.dot(batch_A[i], batch_B[i])
```

用 `np.einsum()` 一行搞定：

```python
result_vec = np.einsum('bij,bjk->bik', batch_A, batch_B)
```

`einsum` 使用 `Einstein` 求和约定，通过下标字符串描述运算。

规则是： **输入里出现但输出里没有的下标，会被求和消除** 。上面 `'bij,bjk->bik'` 中， `j` 在输入出现了两次但不在输出中，所以对 `j` 做求和——恰好就是矩阵乘法的定义。

![](https://img2024.cnblogs.com/blog/83005/202610/83005-20261013213259595-1267857942.png)

`einsum` 不只能做矩阵乘法，很多常见操作都能用下标约定统一表达：

```python
# 矩阵的迹（对角线求和）
trace = np.einsum('ii->', matrix)

# 转置
transposed = np.einsum('ij->ji', matrix)

# 逐元素相乘后求和（即内积）
result = np.einsum('ij,ij->', A, B)  # 等价于 np.sum(A * B)
```

学习曲线有点陡，但一旦习惯，复杂张量运算的代码会大幅简化，而且不容易出错。

## 7\. np.apply\_along\_axis：逐行/列应用函数

假设需要计算每个样本的变异系数（CV = 标准差 / 均值），这个统计量没有直接的 NumPy 函数。

```python
data = np.random.rand(1000, 50) + 0.1  # 加0.1避免均值接近0
```

循环写法：

```python
cv_loop = []
for i in range(data.shape[0]):
    row = data[i]
    cv_loop.append(np.std(row) / np.mean(row))
cv_loop = np.array(cv_loop)
```

向量化写法用 `np.apply_along_axis()` ：

```python
def cv(row):
    return np.std(row) / np.mean(row)

cv_vec = np.apply_along_axis(cv, axis=1, arr=data)
```

`axis=1` 表示按行应用函数（把每一行当作 1D 数组传入 `cv` ）， `axis=0` 则按列。

和 `np.vectorize()` 类似，这个函数主要提升的是代码可读性——底层仍然是 Python 层的逐行调用。

如果你的逐行逻辑可以用纯 NumPy 操作表达，那直接用 NumPy 操作更快：

```python
# 更快的纯向量化写法
cv_fast = np.std(data, axis=1) / np.mean(data, axis=1)
```

所以使用顺序是： **纯 NumPy 操作 > apply\_along\_axis > 手写循环** 。能用纯 NumPy 搞定的优先用，不行再用 `apply_along_axis` 兜底。

## 8\. 回到本质：描述变换，而不是描述遍历

7 个技巧看下来，它们共享同一个核心： **告诉 NumPy 你要对数据做什么变换，而不是怎样遍历数据** 。

| 场景 | 循环思维 | 向量化思维 |
| --- | --- | --- |
| 条件筛选 | 逐个 if 判断 | 布尔掩码 + 索引 |
| 不同形状运算 | 逐行取出来减 | 广播自动对齐 |
| 分支逻辑 | if-elif-else | np.where / np.select |
| 查表映射 | 逐个取值 | 花式索引 |
| 标量函数扩展 | 列表推导 | np.vectorize（过渡方案） |
| 张量运算 | 逐组 dot | np.einsum 下标约定 |
| 逐行/列统计 | 循环切片 | apply\_along\_axis 或纯 NumPy |

向量化代码不仅快，往往也更短、更易读。

循环版需要读者在脑子里模拟迭代过程才能理解，而向量化版一眼就能看出"对满足某条件的元素做了什么"。这种可读性的提升在代码维护时同样重要。