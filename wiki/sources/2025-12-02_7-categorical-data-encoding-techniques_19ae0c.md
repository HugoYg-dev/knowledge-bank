---
type: source
tags:
- MachineLearning
summary: 介绍了 7 种常见的类别型数据编码技术（One-Hot、Dummy、Effect、Label、Ordinal、Count、Binary）的基本原理、特征输出维度及其适用场景。
sources:
- raw/articles/2025-12-02_7-categorical-data-encoding-techniques_19ae0c.md
updated: 2026-08-03
---

# 7 categorical data encoding techniques

## 来源信息
- **主题**: 7 Categorical Data Encoding Techniques
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Tue, 02 Dec 2025
- **原始物理文件**: [[raw/articles/2025-12-02_7-categorical-data-encoding-techniques_19ae0c.md]]

## 核心要点
- **One-Hot 编码与 Dummy 编码**：One-Hot 将每个类别映射为包含单个 1 的二值向量，产出与类别数相同的特征数；Dummy 编码通过随机舍弃一个类别列（产出 $n-1$ 个特征）来规避哑变量陷阱（多重共线性）。
- **Effect 编码**：与 Dummy 编码类似，但将参考类（全 0 向量行）的所有元素修改为 -1，从而能够对比其他类别与参考类的基准差异。
- **Label 编码与 Ordinal 编码**：Label 编码将类别直接赋予随机整数，容易引入假性顺序偏差；Ordinal 编码则赋予具有实际大小意义的等级数值，适用于本身就具备逻辑顺序的特征。
- **Count 编码（频数编码）**：直接以类别在数据集中出现的绝对频数/频率作为特征值。
- **Binary 编码**：结合了序数和二进制转换，先赋予序数，再将其转换为二进制，并按位拆分为单独特征。能大幅降低高基数特征的特征空间维度（输出维度为 $\lceil \log_2(n) \rceil$）。
- **扩展实现**：推荐使用 Python 的 `category-encoders` 库以方便地在工程中实践各种编码策略。

## 关联知识
- 核心概念：类别特征编码技术

## 关键引文
> "Label encoding introduces an inherent ordering between categories, which may not be the case."
> "Binary encoding is a combination of one-hot encoding and ordinal encoding. It represents categories as binary code... Useful when dealing with high-cardinality categorical features."
> "You can try plenty of techniques with the category-encoders library."

> 📎 **物理文献**：[[raw/articles/2025-12-02_7-categorical-data-encoding-techniques_19ae0c.md]]
