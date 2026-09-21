---
type: source
tags:
- AI-Agent/multi-agent
- AI-Agent/deep-research
summary: 深入解析 Anthropic 构建 Claude 生产级多智能体研究系统（Research feature）的工程挑战与经验，涵盖编排器-工作者架构、提示词工程、并行推理及长时间跨度状态管理。
sources:
- raw/articles/How we built our multi-agent research system.md
updated: '2026-07-06'
---
# Anthropic 多智能体研究系统构建实践

> URL：https://www.anthropic.com/engineering/built-multi-agent-research-system

## 摘要

探讨 Anthropic 在将 Claude 的多智能体研究功能（Research）从原型推向大规模生产过程中，所遇到的系统架构设计、工具接口定义、提示词策略以及评估机制等核心工程挑战与实战经验。

## 核心要点

### 1. 多智能体系统的价值与核心动力
- **动态探索与路径依赖**：研究工作通常是开放性且高度动态的，无法硬编码固定流程。多个子智能体可以在独立的上下文窗口中并行探索不同路径。
- **搜索即压缩（Compression）**：子智能体作为智能过滤器，先在各自的海量文档中提取要点，再精简关键 Token 给主研究智能体（Lead Researcher）。
- **性能倍增与 Token 经济学**：多智能体研究系统在广度优先查询上表现卓越；内部评测显示，以 Claude Opus 4 为主智能体、Claude Sonnet 4 为子智能体的系统，在研究评估中比单智能体 Opus 4 高出 90.2%。
- **代价**：多智能体系统的 Token 消耗速度极快（约为普通对话的 15 倍），仅适用于高价值、高度可并行化且依赖大量复杂工具的任务。

### 2. 核心架构：编排器-工作者模式（Orchestrator-Worker）
- **职责划分**：主智能体（Lead Researcher）负责整体规划与协调，将其拆解为子任务；并行的专职子智能体（Subagents）通过迭代调用搜索工具收集信息并筛选。
- **动态检索对比静态 RAG**：不同于传统的静态检索增强生成（[[概念_RAG基础流程|Naive RAG]]），该架构能够实时评估搜索结果、动态调整方向并综合推理生成高质量答案（即 [[概念_Agentic_RAG_智能体检索增强生成|Agentic RAG]]）。
- **引文归因（CitationAgent）**：在完成研究循环后，由专门的引文智能体对报告和原始文档进行比对，精确标注来源。

### 3. 提示词工程与系统治理八大原则
1. **像智能体一样思考**：利用控制台（Console）模拟工具调用轨迹，直观发现“过度搜索”或“选错工具”等死循环。
2. **教编排器如何高效委派**：为子智能体提供详尽的目标、输出格式及明确的任务边界，避免多个子智能体重复做同样的搜索。
3. **根据任务复杂度动态扩缩投入**：在提示词中嵌入明确规则，例如简单事实查询仅启动 1 个智能体（3-10次工具调用），复杂研究则启动 10+ 子智能体。
4. **工具设计与描述优化**：MCP（Model Context Protocol）工具描述的优劣直接决定智能体成败。利用 Claude 4 作为“工具测试智能体”自动执行重写，将任务完成时间缩短 40%。
5. **引导思考过程**：结合扩展思考（Extended Thinking）规划策略；子智能体在使用工具后通过交错思考（Interleaved Thinking）评估质量并查漏补缺。
6. **并行化工具调用**：主智能体并行启动 3-5 个子智能体，每个子智能体同时并发调用 3+ 个工具，使复杂查询耗时缩短达 90%。

### 4. 生产级评估（Evals）与稳定性挑战
- **评估框架**：采用 LLM-as-a-Judge 针对事实准确性、引文正确性、来源质量与工具效率进行多维度打分；结合人工测试捕获边缘情况。
- **状态管理与长周期容错**：长时间运行的智能体面临状态累积错误，需要依赖外部记忆（[[概念_Memory_RAG_显式记忆增强检索|Memory RAG]]）保存研究计划（Plan）及断点恢复机制。
- **异步与文件系统落地**：为了减少经过主智能体中转带来的“传话筒效应（Game of telephone）”，子智能体直接将结构化报告和代码写入外部文件系统，仅回传轻量级引用。

## 关联概念与实体

- **概念**：[[概念_Orchestrator_Worker_编排工模式|orchestrator-worker模式]]、[[概念_Agentic_RAG_智能体检索增强生成|Agentic RAG]]、[[概念_Memory_RAG_显式记忆增强检索|Memory RAG]]、[[概念_LLM_as_a_Judge校准|LLM-as-a-Judge]]
- **实体**：[[实体_Anthropic_Research系统|Anthropic]]、[[实体_Claude_Code|Claude]]

---
> 📎 **物理文献**：[[raw/articles/How we built our multi-agent research system.md]]