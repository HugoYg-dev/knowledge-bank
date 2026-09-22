---
type: "concept"
tags: ["LLM/training/RL", "AI-Agent/tool-calling"]
summary: "Reinforcement Learning for Calibrated Decisions，面向校准决策的强化学习。通过复合严格适当评分规则与策略梯度优化判别模型概率分布的真实统计一致性"
aliases:
  - "RLCD"
  - "Reinforcement Learning for Calibrated Decisions"
  - "校准决策强化学习"
  - "面向校准决策的强化学习"
sources:
  - "wiki/sources/新模型Jev_爆红一周_不生成文字只输出概率却被玩出了花.md"
  - "wiki/sources/Laya开源_421M参数33毫秒System1决策.md"
updated: "2026-09-22"
---

# 概念：RLCD校准决策强化学习

## 1. 定义与核心定位

**RLCD（Reinforcement Learning for Calibrated Decisions，面向校准决策的强化学习）** 是一种专门针对结构化判别、离散选择与分类决策任务的强化学习训练范式。

与旨在优化下一个 Token 困惑度（Perplexity）的自回归语言建模，或旨在优化开放生成质量与偏好胜率的 RLHF/DPO 不同，RLCD 的根本优化目标是**概率校准（Probability Calibration）**——确保模型输出的置信度在数理统计上严格对齐真实世界的后验经验频率，从训练目标层面杜绝“自信地犯错（Overconfident Hallucination）”。

---

## 2. 数学基础与核心机制

### 2.1 为什么交叉熵与二元强化学习会导致校准崩溃？
1. **交叉熵分类（Cross-Entropy）**：
   $$\mathcal{L}_{CE} = -\sum y_i \log p_i$$
   仅当正确类别的 Logit 趋近于 $+\infty$ 时损失才能被最小化，必然驱动 Softmax 输出极端的虚假高置信度（1.0 与 0.0 两极化）。
2. **朴素二元强化学习（Binary Reward RL）**：
   若以“答对 +1，答错 0”作为二元奖励，策略梯度的期望回报为：
   $$\mathbb{E}[R] = \sum p_i \cdot \mathbb{I}(y = i)$$
   策略梯度会迫使概率最高的一项趋向 1.0，其余项趋向 0.0，通过破坏分布的校准性来强行拉高账面准确率。

### 2.2 严格适当评分规则（Strictly Proper Scoring Rules）
在统计决策理论中，当且仅当模型报告的预测分布 $q$ 严格等于真实后验分布 $p$ 时，期望得分能唯一达到全局最大值，该评分规则 $S(q, y)$ 才是**严格适当（Strictly Proper）**的。

在工业级开源实现（如 [[entities/实体_Laya|Laya]]）中，RLCD 采用复合评分规则构建奖励函数：
1. **对数评分（Logarithmic Score, $S_{log}$）**：
   $$S_{log}(q, y) = \log q(y)$$
   针对将真实类别预测为低概率的情况施加重罚（工程上设置截断下限以保数值稳定，如 -9.21）。
2. **球面评分（Spherical Score, $S_{sph}$）**：
   $$S_{sph}(q, y) = \frac{q(y)}{\|q\|_2}$$
   有界归一化评分 $[0, 1]$，平滑纯对数损失带来的极端梯度尖峰。
3. **排序概率评分（Ranked Probability Score, $S_{rps}$）**：
   $$S_{rps}(q, y) = -\sum_{k=1}^K \left( \sum_{i=1}^k q_i - \sum_{i=1}^k \mathbb{I}(y \le i) \right)^2$$
   专门用于有序量表评分任务（如紧急程度 0～3 级），通过累积分布平方距离衡量有序偏差，惩罚“大跨度误判”。

### 2.3 策略梯度优化流水线（纯 RL，零交叉熵）
RLCD 放弃了有监督交叉熵预热与混合损失，采用纯策略梯度迭代：
1. **高斯探索采样**：在每个问题前向 Logits 处注入和为零的投影高斯噪声（$\epsilon - \text{mean}(\epsilon)$），生成 $G$ 组（如 $G=8$）带噪候选 Logits。
2. **组基线优势计算（GRPO 风格）**：
   $$A_g = R_g - \frac{1}{G} \sum_{j=1}^G R_j$$
   无须独立的 Value Critic 价值网络，直接通过组内候选得分均值消除方差。
3. **策略梯度反向传播**：利用高斯分布的对数概率执行 REINFORCE 更新。

### 2.4 多轮时序信用分配：$TD(\lambda = 1.0)$
针对多轮客服或销售场景的决策，为避免模型在早期对话轮次中通过全量上下文偷窥未来（Data Leakage），RLCD 采用**前缀递增切分（Prefix-slicing）**：
- 仅向模型提供截至第 $t$ 轮的历史上下文；
- 采用蒙特卡洛目标（$TD(\lambda = 1.0)$），让早期的反射式判断直接对齐最终真实的转化/流失终局结果，实现无偏的时序信用分配。

---

## 3. 在 Agent 基础设施中的工程价值

1. **确定性安全门控（Confidence Gating）**：
   结合归一化香农熵（Normalized Shannon Entropy）计算置信度：
   $$\text{Confidence} = 1 - \frac{H(p)}{\log K}$$
   在工单路由与工具调用中，下游系统只需配置阈值规则（如 $\ge 0.85$ 直接自动化执行，$< 0.85$ 升级人工审查），即可在极低 ECE（如 0.009）下安全拦截系统性风险。
2. **超低延迟与低成本**：
   RLCD 赋能的判别模型通常具备极小参数量（如 421M），在端侧或普通 GPU 上仅需 30 余毫秒前向计算，成本较 70B 生成式大模型下降两个数量级。

---

## 4. 落地代表模型与实体

- [[entities/实体_Laya|实体_Laya]]：421M Apache 2.0 开源 System 1 决策模型，完全基于 RLCD 数学框架与 ModernBERT-large 端到端训练。
- [[entities/实体_Jev|实体_Jev]]：商业闭源云端概率决策接口代表。

---

## 5. 支撑来源

- [[wiki/sources/新模型Jev_爆红一周_不生成文字只输出概率却被玩出了花|新模型Jev 爆红一周 不生成文字只输出概率却被玩出了花]]
- [[wiki/sources/Laya开源_421M参数33毫秒System1决策|Laya 开源：比Jev快4倍！421M 参数，33 毫秒完成 System 1 决策]]
