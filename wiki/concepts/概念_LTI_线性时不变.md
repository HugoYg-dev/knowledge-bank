---
type: concept
tags:
- LLM/arch/Mamba
summary: Linear Time Invariance，传统 SSM（包括 S4）的一个核心属性，也是其主要局限所在。
sources:
- wiki/sources/A_Visual_Guide_to_Mamba_and_SSM.md
- wiki/sources/Mamba2_SSD_大一统.md
- wiki/sources/一文读懂Mamba_知乎.md
updated: '2026-09-21'
aliases:
- LTI
- Linear Time-Invariant
- 线性时不变
- 线性时不变系统
- 概念_线性时不变LTI
---

# 线性时不变 LTI

Linear Time Invariance，传统 SSM（包括 S4）的一个核心属性，也是其主要局限所在。

## 定义

SSM 参数 A、B、C 对所有时间步固定不变——无论输入序列是什么，可学习参数的值随着新 token 传入都保持不变。

## 局限

LTI 导致 SSM **无内容感知能力**（not content-aware），具体体现在两类失败任务：

1. **选择性复制（Selective Copying）**：要求模型从输入中复制特定 token 并按顺序输出——LTI SSM 无法区分哪些 token 需要复制
2. **归纳头（Induction Heads）**：模式重复识别，如 few-shot 提示中的 Q-A 对应——LTI SSM 无法选择性地从历史中回忆特定 token

## 根本原因

以矩阵 B 为例：无论输入 x 是什么，B 保持不变，独立于 x。A 和 C 同理。这使得模型对每个 token 的处理方式完全相同，如"流水线工厂"。

## 对比 Transformer

Transformer 通过注意力机制动态改变对不同 token 的关注权重，天然具备内容感知能力。LTI SSM 缺少这一特性。

## 解决方案

Mamba 的选择机制：让 B、C、Δ 依赖输入，打破 LTI 约束，见 [[概念_Mamba选择机制]]

## 来源

- [[A_Visual_Guide_to_Mamba_and_SSM]]
- [[Mamba2_SSD_大一统]]