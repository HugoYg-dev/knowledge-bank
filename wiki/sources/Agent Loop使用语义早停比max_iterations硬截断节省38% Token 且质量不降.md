---
type: source
tags:
- AI-Agent/coding
summary: 提出语义早停（Semantic Early-Stopping）方法，通过余弦距离收敛判断 Agent Loop 终止，替代硬迭代上限，实测节省 38%
  Token 且保证生成质量。
sources:
- raw/articles/Agent Loop使用语义早停比max_iterations硬截断节省38% Token 且质量不降.md
updated: '2026-07-02'
---

# Agent Loop使用语义早停比max_iterations硬截断节省38% Token 且质量不降

## 核心贡献与摘要

在传统的 Agentic 循环（如 Writer→Critic）中，终止条件通常硬编码为最大迭代次数（如 `max_iterations=6`）。这导致简单任务白白浪费 Token 跑满上限，而复杂任务过早被一刀切断。Sahil Shrivastava (arXiv:2606.27009) 提出了 **语义早停（Semantic Early-Stopping）** 方法：通过监控生成内容是否在语义空间收敛，来自主判断何时终止循环。

## 关键要点与引文

1. **几何信号与语义距离（零成本本地计算）**：
   每轮将 Writer 生成的草稿通过本地轻量化模型（如 [[实体_Sentence_Transformers]]）转换为向量，计算相邻两轮余弦距离：$d_t = 1 - \cos(e_t, e_{t-1})$。当连续 $k$ 轮距离小于阈值 $\epsilon$（默认 0.06）时，判断语义已收敛并触发早停。见 [[概念_Early_Stopping_早停机制]]。
2. **加质量信号反而血亏（极度反直觉）**：
   引入基于 [[实体_RAGAS]] 的 4 维评估作为质量信号（LLM Judge 打分），尽管减少了迭代轮数（降至 2.4 轮），但每轮频繁调用 Judge 消耗的 Token 远超循环本身，总体成本暴增 129%。
3. **最优性价比实践（Judge-Free 语义早停）**：
   仅依赖免费的本地几何信号（余弦距离收敛判断），实测在 HotpotQA 测试集上节省 **38% Token**，且生成质量与 Baseline 统计上无差异。
4. **震荡收敛与 Patience 机制**：
   文本生成迭代在语义空间的距离非严格单调递减，而是“震荡下降”。因此需设置耐心窗口（如 $k=2$），容忍单次迭代噪声。

## 关联实体与概念

- 概念关联：[[概念_Early_Stopping_早停机制]]、[[概念_RAGAS_RAG评估框架]]
- 实体关联：[[实体_Sentence_Transformers]]、[[实体_RAGAS]]

---
> 📎 **物理文献**：[[raw/articles/Agent Loop使用语义早停比max_iterations硬截断节省38% Token 且质量不降.md]]