---
type: concept
tags:
- LLM/inference
- Infra/gpu
summary: ZeRO 的三种策略（Zero1/2/3）通过在多卡间切分优化器状态、梯度、模型参数来降低单卡显存的方法及计算公式。
sources:
- wiki/sources/大模型显存计算公式与优化.md
updated: '2026-09-07'
---


# 概念：Zero 显存优化

## 定义

Zero（ZeRO）方法最早出现在 [[实体_DeepSpeed]] 中，包含三种策略，对显存降低效果不同。原理参考论文《ZeRO: Memory Optimizations Toward Training Trillion Parameter Models》(arXiv:1910.02054)。

## 三种策略计算公式

假设不考虑 3D 并行和重计算，N 为 GPU 数量：

- **Zero1**：`TotalMemory = Model + Optimizer/N + Activation + Gradient`
  （切分优化器状态）
- **Zero2**：`TotalMemory = Model + Activation + (Optimizer + Gradient)/N`
  （切分优化器状态 + 梯度）
- **Zero3**：`TotalMemory = Activation + (Model + Optimizer + Gradient)/N + LiveParams`
  （切分优化器状态 + 梯度 + 模型参数）

## LiveParams

LiveParams 是 Zero3 引入的参数，用于控制模型中哪些参数需要加载在 GPU 中，其本身的显存占用不可忽视。

## 关联

- [[概念_训练并行策略]]
- [[实体_DeepSpeed]]