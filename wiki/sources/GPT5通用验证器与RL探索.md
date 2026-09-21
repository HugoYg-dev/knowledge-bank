---
type: source
tags:
- LLM/arch
- LLM/training/RL
summary: 深度解析大语言模型从 RLVR 向开放主观领域进化的核心关键——“通用验证器”（Universal Verifier），详细剖析 RaR、Rubicon、Writing-Zero、VeriFree、INTUITOR
  及终极 OaK 架构六大技术路径。
sources:
- raw/articles/LLM output eval in RL.md
updated: '2026-07-06'
---
# GPT-5 通用验证器与强化学习范式革新

> URL：https://mp.weixin.qq.com/s?__biz=Mjc1NjM3MjY2MA==&mid=2691560834&idx=1

## 摘要

系统解读大语言模型如何在超越“对/错”二元判断的复杂主观领域（医疗、教育、创意写作等）进行强化学习（RL）。文章详细剖析了当前构建“通用验证器”（Universal Verifier）的两大主要流派及六项核心技术代表，并指出了通往终极智能的 OaK 架构愿景。

## 核心要点

### 1. 为什么需要通用验证器？
- **RLVR 的瓶颈**：可验证奖励强化学习（[[概念_RLVR_可验证奖励强化学习|RLVR]]）在数学和编程等具有绝对确定性答案的领域立竿见影；但在没有唯一答案、强调沟通与同理心的主观与开放领域中，容易出现优化失效甚至能力倒退。
- **核心目标**：构建能够对主观优劣进行精确评估的通用验证机制，将海量非结构化经验转化为有效的强化学习训练信号。

### 2. 第一条路：外挂“立法式”验证（AI 裁判与结构化细则）
- **RaR（Rubrics as Rewards，Scale AI）**：
  - “专家立法 + 模型释法 + AI 执法”三步法：专家定义评估元框架，模型针对具体问题自动扩展为 7~20 项精细化评分清单，裁判模型据此打分引导学生模型（如结合 [[概念_GRPO_群组相对策略优化|GRPO]]）。在医疗基准上表现大幅超越简单评分。
- **Rubicon（蚂蚁集团 & 浙大）**：
  - 构建超 10,000 个评分标准的庞大系统；引入**否决机制**（硬性过滤防 [[概念_Reward_Hacking_奖励攻陷与作弊|Reward Hacking]]）与**饱和度感知聚合**（边际效用递减防止单科刷分）。
  - **破解跷跷板效应（Seesaw Effect）**：采用分阶段强化学习，第一阶段夯实通用格式与基础逻辑，第二阶段引入专业评分细则，有效消除“AI味”，在开放任务中提升 5.2%。
- **Writing-Zero（阿里夸克）**：
  - 改进裁判模型本身，设计成对生成式奖励模型（GenRM）。强制裁判“先批判分析、后打分”（Critique-then-score），并通过 BRPO（引导相对策略优化）进行算法训练。

### 3. 第二条路：内观自评（无验证器与内在反馈）
- **VeriFree（SEALab）**：
  - 摒弃外部验证器，直接利用模型自身在生成推理链（CoT）后，预测出正确标准答案的“内在自信度”作为奖励信号。
- **INTUITOR / RLIF（UC Berkeley）**：
  - 完全无监督（无需标准答案或外部标注），引入**自确定性（Self-certainty）**指标：模型生成 Token 时的概率分布与均匀分布之间的平均 KL 散度。通过奖励高连贯性、高确定性的推理路径（RL from Internal Feedback），在通用和编程领域展现极佳泛化能力。

### 4. 终局蓝图：OaK 架构（Richard Sutton）
- 强化学习之父提出的基于“运行时经验”的智能体架构：完全摒弃人为设计时注入的静态知识，通过 8 个基础步骤（主策略学习 -> 特征生成排序 -> 构建子问题与选项 -> 学习知识模型 -> 规划管理）自主从环境中构建认知。
- 当前的 RaR 和 INTUITOR 分别是 OaK 架构中“子问题探索”与“内在价值函数”在早期阶段的雏形。

## 关联概念与实体

- **概念**：[[概念_LLM_as_a_Judge校准|LLM-as-a-Judge]]、[[概念_RLVR_可验证奖励强化学习|RLVR]]、[[概念_GRPO_群组相对策略优化|GRPO]]、[[概念_Reward_Hacking_奖励攻陷与作弊|Reward Hacking]]
- **实体**：[[实体_OpenAI|OpenAI]]、[[实体_DeepMind|DeepMind]]

---
> 📎 **物理文献**：[[raw/articles/LLM output eval in RL.md]]