---
type: concept
tags:
- LLM/training/post-train
summary: 大模型 SFT 数据清洗的三个核心维度，用于系统性筛选高价值训练数据。
sources:
- wiki/sources/SFT数据挑选方法_质量多样性必要性.md
updated: '2026-06-29'
---


# 概念：SFT 数据三维度

## 定义

大模型 SFT 数据清洗的三个核心维度，用于系统性筛选高价值训练数据。

## 三维度

### 1. 数据质量（Quality）

- 目标：去除低质量、有问题的数据
- 方法：奖励模型打分（OpenAssistant/自训练）、ChatGPT 多维度打分（准确性/指令遵循/表达）、长度过滤、困惑度过滤

### 2. 数据多样性（Diversity）

- 目标：覆盖更大范围的指令类型和回答风格
- 方法：K-Center-Greedy（最大化最小距离）、聚类（K-Means）后每簇采样、向量相似度过滤（DEITA）

### 3. 数据必要性（Necessity）

- 目标：只保留模型当前无法很好处理的数据，避免训练模型已掌握的内容
- 方法：IFD 指标（指令跟随难度）、奖励模型验证（MoDS）

## 代表方法对比

| 方法 | 质量 | 多样性 | 必要性 |
|-----|------|-------|-------|
| MoDS | 奖励模型（阈值 α） | K-Center-Greedy | 奖励值低于 β |
| DEITA | 复杂性×质量综合评分 | 向量相似度过滤（阈值 t） | IFD |
| CaR | Sentence BERT 分类 | K-Means 聚类+topn | — |

## 关联

- [[SFT数据挑选方法_质量多样性必要性]]
- [[概念_IFD指令跟随难度]]
- [[概念_K_Center_Greedy_中心贪婪算法]]