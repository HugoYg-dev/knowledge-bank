---
type: concept
tags:
- LLM/reasoning
- AI-Agent/prompt-engineering
summary: '- 来源：DeepMind Brain 团队 2022 年论文'
sources:
- wiki/sources/375篇文献_推理大模型后训练技术综述.md
- wiki/sources/DeepSeek-R1工作原理.md
- wiki/sources/自适应快慢思考推理模型.md
updated: '2026-09-07'
---
# 概念：思维链 CoT 高级方法

## 基础 CoT

- 来源：DeepMind Brain 团队 2022 年论文
- 做法：Zero-shot（"让我们一步步思考"）或 Few-shot（提供推理示例）
- 效果：在数学和复杂推理任务上显著提升，简单任务改善有限

## CoT-SC（Self-Consistency with CoT）

- 生成多条推理路径，选取最一致答案
- DeepMind 报告算术推理提升 1%~8%

## Decoding CoT（Chain-of-Thought Reasoning Without Prompting）

- 无需提示词；启动 k 个初始 top token，各自生成不同推理路径
- 根据各路径 token logits 计算置信度分，返回最高概率答案
- 来源：DeepMind 2024，arXiv 2402.10200

## Tree of Thoughts（ToT）+ MCTS

- 普林斯顿+DeepMind 2023 提出
- 多路径动态评估，边生成边剪枝无效路径（与 CoT-SC 事后评估不同）
- MCTS 扩展：引入外部奖励（UCB 统计），支持回溯改进早期决策

## 成本与适用性

- CoT 链每问题成本可高出约 8 倍
- 《To CoT or not to CoT?》（2409.12183）：改进主要在数学/复杂推理，简单任务不适用
- 实践：根据问题难度自适应选择是否使用 CoT（→ 自适应快慢思考）

## CoT 三条发展路径（上交综述）

### Prompt 模式
- 手动指令：Zero-Shot CoT（"Let's think step by step"）、Plan-and-Solve（先制定计划再执行）
- 自动指令：APE（自动 Prompt 工程）、OPRO（LLM 自动优化 Prompt）
- 范例生成：Few-Shot-CoT → ActivePrompt（不确定性采样）→ Auto-CoT（聚类+代表性问题）

### 推理结构
- **PoT**：程序化思维，将计算问题交给代码解释器
- **Tab-CoT**：表格结构推理（步数/子问题/过程/结果）
- **ToT**：树状推理，多路探索+回溯纠正
- **GoT**：图状推理，控制器管理图操作（GoO）和图状态推理（GRS）
- **Self-consistency**：多路采样+多数投票选最一致路径
- **Self-Verification**：多候选采样+后向验证打分排序
- **CRITIC**：外部工具验证+循环修改（检索/计算器/代码）

### 应用场景
- 多模态 CoT（MM-CoT 输入多模态；VCoT 输出多模态）
- 领域应用：摘要（SumCoT）、机器翻译（MAPS）、化学（ChemCrow）、医学（Med-PaLM）

## CoT 与 Agent 的关系
- Agent 三能力：感知（逐步理解输入/反馈/多模态）、记忆（短期上下文链+长期树搜索/矢量检索）、推理（计划+行动+观察循环）
- CoT 弥合推理与行动的差距；工具使用扩展 Agent 能力边界

## 关联

- [[概念_Prompt工程方法]]
- [[概念_自适应长短CoT]]
- Decoding_CoT
- ToT树状推理
- Agent推理规划