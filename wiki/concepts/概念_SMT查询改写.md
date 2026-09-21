---
type: concept
tags:
- RAG/query
summary: SMT（Statistical Machine Translation，统计翻译模型）查询改写将查询改写任务抽象为机器翻译任务，将用户搜索词f翻译为目标改写词e，基于噪声信道模型和贝叶斯公式求解。
sources:
- wiki/sources/美团搜索查询改写实践.md
updated: '2026-07-06'
---

# 概念_SMT查询改写


## 定义

SMT（Statistical Machine Translation，统计翻译模型）查询改写将查询改写任务抽象为机器翻译任务，将用户搜索词f翻译为目标改写词e，基于噪声信道模型和贝叶斯公式求解。

## 核心组件（美团实践）

1. **对齐字典过滤**：用BERT语义判别模型+规则（类目交叉熵、是否互相包含）对对齐词表过滤
2. **结构化Decode**：BeamSearch算法，参数包括映射概率（对齐score+Term相似度特征）和转移概率（语言模型+Term结合度）
3. **排序模型**：XGBoost排序，特征同时考虑语义相关性和改写词召回结果有效性
   - 语义：文本编辑距离、语义相似度、Session转移次数
   - 有效性：地域和流行性（Document维度的曝光/点击/下单共现）

## 效果

- 线上有改写流量覆盖提升约12%
- 整体框架类似业界经典 Learning to Rewriting 框架

## 与NMT的对比

- SMT 基于短Term候选的翻译，依赖分词粒度和候选
- NMT 端到端生成，不依赖候选，覆盖长尾Query

## 关联

- 相关概念：[[概念_查询重写]]、[[概念_NMT_强化学习查询改写]]
- 来源：[[美团搜索查询改写实践]]