---
type: source
tags:
- AI-Agent/coding
- Infra/platform
summary: 本文详细探讨了 Agent Harness（智能体宿主/外壳）的概念。指出在多步骤任务中，Agent 系统的瓶颈往往在于围绕 LLM 的外壳基础设施。文章定义了
  Harness 的 11 个生产级核心组件，并梳理了单步 TAO 循环以及长周期两阶段协作的 Ralph Loop 模式，最后给出了架构设计中的七个关键抉择。
sources:
- raw/articles/2026-04-06_The-Anatomy-of-an-Agent-Harness_19d64a.md
updated: '2026-08-04'
---

# Source: The Anatomy of an Agent Harness

## 来源信息
- **标题**: The Anatomy of an Agent Harness
- **来源**: Daily Dose of DS (avi@dailydoseofds.com)
- **日期**: 2026-04-06
- **原始物理文件**: [[raw/articles/2026-04-06_The-Anatomy-of-an-Agent-Harness_19d64a.md]]

## 核心要点
- **宿主定位（Harness Definition）**：Vivek Trivedy 指出：“如果你不是模型，你就是 Harness”。Harness 是围绕 Raw LLM 的完整软件基础设施，决定了智能体的表现上限。LangChain 通过优化 Harness（模型和权重不变）便在 TerminalBench 2.0 上排名显著上升。
- **硬件系统类比**：Beren Millidge 将其类比为硬件系统：Raw LLM 是无 RAM/Disk/IO 的 CPU，Context window 是 RAM，外部数据库是 Disk，工具集成是驱动程序，而 Harness 则是操作系统（OS）。
- **工程层次划分**：智能体开发包含 Prompt Engineering（提示词工程）、Context Engineering（上下文工程）与 Harness Engineering（宿主工程）。Harness Engineering 统管整体执行、记忆持久化、错误恢复、校验回路、安全策略和生命周期。
- **11 大核心组件**：
  1. **Orchestration Loop**：Thought-Action-Observation (TAO) 的 ReAct 心跳循环。
  2. **Tools**：工具 Schema 注入、参数检验与沙箱化执行。
  3. **Memory**：跨会话的多尺度记忆（如 Claude Code 中的 `CLAUDE.md` 与 `MEMORY.md` 索引）。
  4. **Context Management**：解决上下文退化（Context rot），采用压缩、掩码、懒加载及子代理精简总结。
  5. **Prompt Construction**：具有严格优先级的系统和会话 Prompt 分层堆叠。
  6. **Output Parsing**：原生工具调用与 Schema 强约束解析。
  7. **State Management**：以图节点/状态字典流及 Checkpoint 机制支持中断恢复。
  8. **Error Handling**：错误分级处理，区分瞬时错误、LLM 可恢复错误、用户修复错误与非预期错误。
  9. **Guardrails & Safety**：多级（输入/输出/工具）安全策略与 tripwire 阻断机制。
  10. **Verification Loops**：代码与推理校验，给模型自我验证机会，可大幅度提升任务质量。
  11. **Subagent Orchestration**：子代理的派生、隔离分支（Worktree）及邮箱式通信。
- **长生命周期 Ralph Loop 模式**：针对复杂长周期任务，采用 Initializer Agent（搭建环境、进度文件、初始提交）+ Coding Agent（读取提交与进度，增量开发并提交）的双阶段工程设计模式。
- **架构设计的七大抉择**：
  1. 单代理 vs 多代理
  2. ReAct 循环 vs 规划-执行（Plan-and-execute）
  3. 上下文窗口管理策略
  4. 校验回路设计（计算验证 vs 推理验证）
  5. 权限与安全架构（宽容 vs 限制）
  6. 工具范围控制（Tool Scoping）
  7. Harness 厚度（逻辑下沉到 Harness 还是交给 Model 自行处理）

## 关键引文
- > "If you’re not the model, you’re the harness." (Vivek Trivedy)
- > "A raw LLM is a CPU with no RAM, no disk, and no I/O... The harness is the operating system." (Beren Millidge)
- > "Giving the model a way to verify its work improves quality by 2 to 3x." (Boris Cherny)
- > "The scaffold is removed when the building is complete. As models improve, harness complexity should decrease."

---
> 📎 **物理文献**：[[raw/articles/2026-04-06_The-Anatomy-of-an-Agent-Harness_19d64a.md]]
