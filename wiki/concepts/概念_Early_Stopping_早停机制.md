---
type: concept
tags:
- LLM/arch
- DeepLearning
summary: 训练中监控验证集 loss，当其连续多次不再下降时提前停止训练，避免过拟合并保存最优模型。
sources:
- wiki/sources/Agent Loop使用语义早停比max_iterations硬截断节省38% Token 且质量不降.md
- wiki/sources/PyTorch常用代码段合集.md
- wiki/sources/PyTorch训练代码模板.md
- wiki/sources/从提示员到系统架构师：Loop Engineering 的范式跃迁.md
updated: '2026-09-21'
aliases:
- Early Stopping
- EarlyStopping
- 早停
- 早停机制
- 概念_早停EarlyStopping
---

# 概念：早停（EarlyStopping）


## 定义

训练中监控验证集 loss，当其连续多次不再下降时提前停止训练，避免过拟合并保存最优模型。

## 要点（全文实现）

### 1. 深度学习模型训练早停
- 关键参数：patience（容忍次数）、delta（最小改善量）、verbose
- 监控 val_loss：score = -val_loss
- 逻辑：
  - 若 score 优于 best_score：更新 best_score，保存 checkpoint，counter 归零
  - 若不优于：counter += 1，达到 patience 则 early_stop = True
- save_checkpoint：当验证 loss 下降时用 `torch.save(model.state_dict(), path)` 保存模型
- 训练循环中每个 epoch 结束调用，early_stop 为真则 break

### 2. Agent Loop 语义早停 (Semantic Early-Stopping)
- 在大模型智能体迭代循环中（如 Writer→Critic），监控生成草稿在本地 Embedding 向量空间相邻两轮的余弦距离 $d_t = 1 - \cos(e_t, e_{t-1})$。
- 当连续 $k$ 轮距离低于阈值（如 $\epsilon=0.06$）时触发停止，避免简单任务硬跑满 `max_iterations` 浪费 Token。实测节省 38% Token 且质量不降。

## 来源

- [[PyTorch训练代码模板]]
- [[Agent Loop使用语义早停比max_iterations硬截断节省38% Token 且质量不降]]
- [[从提示员到系统架构师：Loop Engineering 的范式跃迁]]