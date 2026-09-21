---
type: source
tags:
- LLM/training/RL
- LLM/reasoning
summary: Unsloth 出品 RL 入门指南：从 RLHF/PPO 到 GRPO/RLVR，原理+奖励函数设计+实战技巧
sources:
- raw/articles/新手必看！强化学习入门指南 _ 从RLHF、PPO、GRPO到RLVR，最后到训....md
updated: '2026-07-01'
---
## 来源信息

- **标题**：新手必看！强化学习入门指南 | 从RLHF、PPO、GRPO到RLVR，最后到训练推理模型
- **作者**：Daniel Han & Michael Han（Unsloth 团队）；整理：ShuCP（AINLPer）
- **URL**：https://mp.weixin.qq.com/s/F4fediyP2in_CWW-ERMoUg
- **原始文档**：https://docs.unsloth.ai/basics/reinforcement-learning-guide

## 核心要点

### 强化学习基本概念

- RL 目标：增加获得「好」结果的几率，降低「坏」结果的几率
- 三要素：环境（游戏世界）、动作（可选操作）、奖励（好/坏信号）
- RL 本质：通过积累「坏信号」引导模型主动减少坏输出，逐渐修剪输出分布向正确答案靠拢；只要正确答案概率不为零，极限情况下一定能收敛

### RLHF → PPO → GRPO 演进

- **RLHF**（基于人类反馈的强化学习）：用人类偏好（👍/👎）训练 agent，OpenAI 让其普及
- **PPO**（近端策略优化）：agent = 生成策略（当前模型）+ 参考策略（原始模型）+ 价值模型；需要奖励模型估算当前奖励；公式复杂但稳定
- **GRPO**（组相对策略优化，DeepSeek 开发）：
  - 移除价值模型，改用多次采样统计计算平均奖励（Z 分数标准化 → 优势 A）
  - 移除神经网络奖励模型，改用自定义奖励函数
  - 结果：显著节省显存，训练更高效
- **RLVR**（可验证奖励的强化学习）：用易于自动验证的任务（数学等式/代码执行结果）设计奖励函数；适用范围不限于代码/数学，电子邮件、数据库检索、法律医学等均可，关键是把奖励分解为一系列较小的可验证子奖励

### 奖励函数 vs 验证器

- **验证器（Verifier）**：只判断对错，不给分
- **奖励函数（Reward Function）**：将验证结果（和其他标准）转为数值分数；可惩罚长度过长、可读性差等
- GRPO 的目标：最大化奖励，学习答案推导方式，而非记忆训练数据

### Unsloth GRPO 实战技巧

- 至少等待 300 步奖励才真正增加，实际可能需要 1000 步以上
- 至少 500 行数据，更多更好
- GRPO 建议用于 ≥1.5B 模型，小模型可能无法正确生成 thinking token
- QLoRA 4-bit 的显存规则：模型参数量 ≈ 所需显存 GB 数；上下文越长显存越多
- 使用基础模型时需确保有聊天模板
- GSM8K 是目前 R1 风格训练最流行的数据集选择
- 训练时间越长越好，GRPO 不需要大量数据，但需要优秀的奖励函数

### 典型奖励函数示例（GSM8K）

- `correctness_reward_func`：完全匹配标签
- `int_reward_func`：鼓励整数答案
- `soft_format_reward_func`：允许少量换行不匹配的结构检查
- `strict_format_reward_func`：严格匹配响应结构
- `xmlcount_reward_func`：XML 标签精确一一对应

## 关键引文

> GRPO 完全移除了价值模型，但我们仍然需要根据当前状态估算「平均奖励」。诀窍在于对 LLM 进行采样！然后，我们通过统计多个不同问题的采样过程来计算平均奖励。 `[重点/高亮]`

## 关联

- [[概念_GRPO_群组相对策略优化]] — GRPO 算法原理
- [[概念_RLVR_可验证奖励强化学习]] — 可验证奖励 RL
- [[概念_大模型训练三阶段]] — 后训练阶段
- [[实体_DeepSeek-R1]] — GRPO 的应用案例
- [[实体_Unsloth]] — 本文出品方，开源微调框架

---
> 📎 **物理文献**：[[raw/articles/新手必看！强化学习入门指南 _ 从RLHF、PPO、GRPO到RLVR，最后到训....md]]