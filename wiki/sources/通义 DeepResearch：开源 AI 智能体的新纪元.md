---
type: source
tags:
- AI-Agent/deep-research
summary: 通义官方博客：通义 DeepResearch 全开源 Web Agent 的技术全貌——Agentic CPT+SFT+RL 训练、IterResearch
  范式、数据合成与基础设施
sources:
- raw/articles/通义 DeepResearch：开源 AI 智能体的新纪元 _ Tongyi D....md
updated: '2026-07-01'
---
# 通义 DeepResearch：开源 AI 智能体的新纪元

## 来源信息

- 作者：Tongyi Lab DeepResearch Team
- 原文：https://tongyi-agent.github.io/zh/blog/introducing-tongyi-deep-research/
- GitHub：https://github.com/Alibaba-NLP/DeepResearch
- HuggingFace/ModelScope：Tongyi-DeepResearch-30B-A3B
- Cubox 高亮：2 处，已标注 [重点/高亮]

## 核心要点

### SOTA 性能

- Humanity's Last Exam (HLE)：32.9
- BrowseComp-EN：43.4
- BrowseComp-ZH：46.7
- xBench-DeepSearch：75.0

全面超越所有闭源及开源 Deep Research 智能体。

### 增量预训练数据（Agentic CPT）

提出 **AgentFounder** 数据合成方案，构建支持大规模持续扩展的智能体预训练数据。

**数据重组和问题构建**：基于知识文档/爬虫数据/知识图谱/轨迹数据，构建以实体为锚定的开放世界知识记忆，生成多风格（问题，答案）对。

**动作合成**：构建三种类型动作数据：
- 单步规划动作
- 单步推理动作
- 多步决策动作合成

离线环境下大规模探索推理-动作空间，无需额外商业工具 API 调用。

### 后训练数据（High-quality QA）

历史演进路线：WebWalker → WebSailor/WebSailor-V2 → WebShaper，确保数据质量和可扩展性。

**WebFrontier（WebShaper）核心流程**：
- 知识图谱随机游走 + 表格数据融合，整合真实网站数据
- 采样子图/子表生成初始问题答案，策略性混淆信息增加问题难度
- "原子操作"正式建模 QA 难度，系统性增加复杂性
- 自动化学术数据构建：生成种子QA对 → 配备工具的 Agent 进行迭代复杂度升级循环

### Rollout 模式

**ReAct 模式**：
- 遵循"思考-行动-观察"循环
- 模型上下文长度 128K
- 受"The Bitter Lesson"影响，利用可扩展计算的通用方法

**IterResearch（深度模式）**：

> [重点/高亮] IterResearch 范式的创建是为了解决Agent将所有信息堆积在一个不断扩展的单一上下文窗口中时出现的认知瓶颈和噪音污染。针对多步研究任务，IterResearch 将其解构为一系列研究回合。
>
> 在每一轮中，Agent仅使用上一轮中最重要的输出来重建一个精简的工作空间。在这个专注的工作空间中，Agent会分析问题，将关键发现整合成一个不断演变的核心报告，然后决定下一步行动——是收集更多信息还是提供最终答案。这种"综合与重构"的迭代过程使Agent能够在执行长期任务时保持清晰的认知焦点和高质量的推理能力。
>
> 在此基础上，我们提出了Research‑Synthesis框架。并行使用多个IterResearch Agent探索同一个问题。并最终整合它们完善的报告和结论，从而得出更准确的最终答案。

### 端到端 Agent 训练流程

三阶段串联：Agentic CPT → Agentic SFT → Agentic RL

**基于 On-Policy 策略的 RL**：

基础算法：基于 GRPO 定制优化。关键设计：
- 严格遵循 on-policy 训练范式
- token 级别策略梯度损失函数
- 留一法（leave-one-out）策略降低优势估计方差
- 选择性排除负样本（过长而未能生成最终答案的样本），缓解"格式崩溃"现象
- 批次（batch size）和组规模（group size）大化，维持小方差

> [重点/高亮] 我们认为，算法固然重要，但并非 Agentic RL 成功的唯一决定因素。在尝试了多种算法和优化技巧后我们发现，数据质量和训练环境的稳定性，可能是决定强化学习项目成败的更关键一环。一个有趣的现象是，我们曾尝试直接在 BrowseComp 测试集上训练，但其表现远不如使用我们合成数据的结果。

**基础设施四要素**：
1. **仿真训练环境**：离线维基百科数据库 + 自定义工具套件构成模拟环境，SailorFog-QA-V2 生成专属数据
2. **稳定高效工具沙盒**：缓存结果/重试失败调用/饱和式响应，防止工具错误响应破坏学习轨迹
3. **自动数据管理**：实时优化数据，全自动数据合成+数据漏斗动态调整训练集，形成数据-训练正向循环
4. **异步 on-policy 框架**：基于 rLLM 实现异步 RL 训练推理框架，多个 Agent 实例并行与环境交互

### 应用落地

- **高德地图**：复杂查询助手「小高老师」，纯 Agentic + ReAct 执行复杂推理，通义提供模型 + 高德提供工具和 Agent 链路
- **通义法睿**：法律 Deep Research，司法多步查询与复杂推理，Iterative Planning 技术

### 未来工作

1. 扩展上下文窗口（当前 128k 在极端复杂任务时不足）
2. 更大规模模型（超 30B）上验证训练流程可扩展性
3. 引入 partial rollouts 提升 RL 框架效率，攻克离线训练分布偏移问题

## 关联

- [[概念_IterResearch范式]]
- [[概念_WebFrontier数据合成]]
- [[概念_Deep_Research_Agent_定义与分类]]
- [[实体_通义DeepResearch]]

---
> 📎 **物理文献**：[[raw/articles/通义 DeepResearch：开源 AI 智能体的新纪元 _ Tongyi D....md]]