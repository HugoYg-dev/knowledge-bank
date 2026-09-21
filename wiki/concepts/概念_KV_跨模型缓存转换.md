---
type: concept
tags:
- LLM/inference
- Infra/serving
summary: 跨模型 KV 缓存转换通过学习源模型与目标模型的 KV 表示映射，尝试在模型切换时复用既有 Prefill 计算；当前证据仅覆盖同家族稠密全注意力模型。
sources:
- wiki/sources/2026-08-10_Cross-model-KV-cache-transfer-in-LLM-families_19febef2c6003814.md
updated: '2026-09-21'
aliases:
- Cross-Model KV
- 跨模型KV缓存
- KV缓存转换
- 概念_跨模型KV缓存转换
---

# 概念：跨模型 KV 缓存转换

## 定义

跨模型 KV 缓存转换是指将源模型生成的 Key/Value 缓存映射为目标模型可消费的表示，从而在模型路由切换时避免完整重新 Prefill。它不同于只在同一模型内复用的前缀缓存，核心前提是两个模型的内部表示存在可利用的对应关系。

## 文中方法

- 对每个目标层和注意力头分别拟合线性映射，使用闭式解而非梯度训练。
- 以目标层预测能力为依据选择多个源层，再联合用于转换；此举用于处理模型层数不同、没有天然一对一层对应的问题。
- 对 Key 先移除 RoPE 的位置相关旋转，在位置无关空间中拟合映射，完成转换后再施加目标模型的旋转。

## 适用边界

- [原文陈述] 已报告的实验对象限于 Qwen3、Llama 3.1、Ministral 3 等同家族模型的稠密全注意力配对。
- [待验证] 跨家族转换、KV 头数量或单头维度不匹配，以及滑动窗口或注意力递归混合模型均没有文中实验支撑。

## 关联

- [[concepts/概念_KV_Cache_键值缓存]]
- [[concepts/概念_LLM推理两阶段]]
- [[wiki/sources/2026-08-10_Cross-model-KV-cache-transfer-in-LLM-families_19febef2c6003814]]