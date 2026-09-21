---
type: concept
tags:
- DeepLearning
summary: 标签平滑（Label Smoothing）将硬标签（one-hot）软化，正确类概率设为 1-ε，其余类均分 ε/(C-1)，缓解模型过度自信、提升泛化。PyTorch
  中可用自定义 LSR 类或直接构造 smoothed_labels 实现。
sources:
- wiki/sources/PyTorch常用代码段合集.md
updated: '2026-09-21'
aliases:
- Label Smoothing
- 标签平滑
- 概念_Label_Smoothing
---

# 概念：标签平滑（Label Smoothing）

## 定义

标签平滑是一种正则化技巧，将训练用的硬标签（one-hot）软化：正确类的值设为 `1 - smooth_factor`，其余类均分 `smooth_factor / (length - 1)`，用平滑后的标签代替交叉熵中的硬标签。

> 注：全文以代码段形式给出（LSR 类实现 + 训练循环内直接实现两种方式），未展开理论原理，confidence 标 medium。

## 实现要点（全文代码）

- 自定义 `LSR(nn.Module)` 类：`_one_hot` 转换 + `_smooth_label` 平滑 + `log_softmax` 计算损失，支持 none/sum/mean reduction
- 或直接在训练循环内：`smoothed_labels = torch.full(size=(N,C), fill_value=0.1/(C-1))`，再 `scatter_` 把正确类设为 0.9，配合 `log_softmax` 计算损失

## 关联

- [[PyTorch常用代码段合集]]（来源）
- [[概念_Mixup训练]]