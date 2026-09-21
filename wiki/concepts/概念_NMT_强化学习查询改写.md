---
type: concept
tags:
- RAG/query
summary: 强化学习优化的 NMT（Neural Machine Translation，神经网络翻译模型）查询改写是一种端到端生成式改写方法，通过将搜索系统作为环境（Environment）、NMT改写模型作为智能体（Agent），用搜索曝光和点击作为奖励（Reward）来指导模型优化，解决长尾Query覆盖...
sources:
- wiki/sources/美团搜索查询改写实践.md
updated: '2026-09-21'
aliases:
- NMT
- Neural Machine Translation
- 强化学习NMT改写
- 概念_强化学习NMT改写
---

# 概念_NMT_强化学习查询改写


## 定义

强化学习优化的 NMT（Neural Machine Translation，神经网络翻译模型）查询改写是一种端到端生成式改写方法，通过将搜索系统作为环境（Environment）、NMT改写模型作为智能体（Agent），用搜索曝光和点击作为奖励（Reward）来指导模型优化，解决长尾Query覆盖不足问题。

## 解决的问题

- 分词粒度限制：单字维度改写易造成Case且无法穷举
- 语义相近不能对齐的复杂Query（如"哪里有便宜的手机卖"→"手机优惠"）
- NMT原生问题：生成不符合语义（生僻/不通顺）、语义漂移

## 框架设计（美团实践）

### 预训练NMT生成器
- 经典Seq2Seq + 字切分Embedding + Attention机制（替代SMT对齐）
- BERT初始化Encoder（引入语义信息，快速收敛）
- Coverage机制解决过翻；编辑距离解决漏翻

### 环境（Environment）
- 离线搜索日志模拟搜索系统：原词和改写词的召回商户ID列表、点击商户ID列表重合度
- BERT模拟语义判别系统：避免商户多服务、热门词等导致的点击偏差

### 奖励（Reward）
- 加权打分器：搜索、用户行为、语义判别、字面匹配度不同权重，归一化到0-1
- Reward叠加到NMT Fine-Tuning的Loss（Google式batch平均句长归一化效果最好）

## 效果

- 离线评估准确率 69%→87%
- 解决语义改写（挑筋→拨筋）、生僻简写（法甜店→法式甜点）、输入错误（瑜教练→瑜伽教练）、自然语言去词（染发剂哪里买→染发剂）

## 关联

- 相关概念：[[概念_SMT查询改写]]、[[概念_查询重写]]、[[概念_向量化召回改写]]
- 来源：[[美团搜索查询改写实践]]