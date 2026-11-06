---
type: "source"
tags: ["AI-Agent/coding", "AI-Agent/memory", "AI-Agent/context-engineering"]
summary: "深度解析 Codex Harness 架构：118 个 Rust Crate 模块化解耦、Op/Event 双向事件驱动、三层循环、World State 补丁、SubAgent 协同及全新的 Token Budget 跨窗口上下文记忆体系"
sources: ["raw/articles/深度解析 Codex Harness 架构及其全新上下文压缩记忆体系的设计思路.md"]
updated: "2026-11-06"
---

# 深度解析 Codex Harness 架构及其全新上下文压缩记忆体系的设计思路

## 来源信息

- **来源标题**：深度解析 Codex Harness 架构及其全新上下文压缩记忆体系的设计思路
- **作者 / 平台**：飞樰 / 千问AI平台
- **发布时间**：2026-10-27
- **原文链接**：https://mp.weixin.qq.com/s/IM-zakQ9Bnog54NdYiJSqA

## 核心要点

1. **整体架构与 118 个 Rust Crate 模块化解耦**：Codex Harness 源码拆分为约 118 个独立的 Rust Crate，在 `AGENTS.md` 中严格贯彻“**Resist adding code to codex-core（禁止往 codex-core 里面写代码）**”的高内聚低耦合工程准则。改动单个 Crate 仅需局部重新编译，降低耦合与系统复杂度。关键 Crate 划分：
   - `codex-core`：Agent 运行核心（Session、主 Loop、工具执行、上下文管理）；
   - `codex-protocol`：底层数据协议层，定义用户操作 Op（TurnInput, Interrupt, Compact, Shutdown 等）与 Agent 响应 Event（TurnStarted, TurnComplete, AgentMessage, OutputDelta 等）；
   - `codex-api`：封装 OpenAI Response API（HTTP 与 WebSocket）；
   - `codex-app-server`：核心协议服务层，暴露标准 JSON-RPC 接口，统一驱动 TUI 终端与 Desktop 桌面端；
   - `codex-rollout`：会话持久化与 Agent Trace 层，支持文件或 SQLite 存储；
   - `codex-arg0`：利用可执行程序启动参数传入不同名称（如 `codex`、`codex-linux-sandbox`、`apply-patch`）动态识别并注入 Agent 角色与运行环境。
2. **三层嵌套循环（Task $\to$ Turn $\to$ Sampling）**：
   - **Task Loop**：外层处理用户任务流与消息等待（Pending）；
   - **Turn Loop（Run Turn）**：中层负责单轮对话与上下文压缩；
   - **Sampling Loop**：内层对应单次模型请求、工具调用或文本生成步骤（对标 DSH 的 Step）。
3. **工具并发与有序拼装（FuturesOrdered）**：当模型单次输出多个工具调用时，底层基于 `FuturesOrdered` 并发执行提升吞吐；但在将结果拼装回写模型上下文时，严格保持与模型调用一致的原始时序，消除时序错乱引发的模型理解混乱。
4. **World State 环境状态补丁**：将 Shell 权限、`AGENTS.md` 规则等环境划分为具备稳定 ID 与快照类型的带类型 Section；后续环境发生变动时，不重读全量上下文，仅注入 Diff 补丁语句，保护 Prefix KV Cache 不被打破并显著减少 Token 消耗。
5. **精细化 SubAgent 派生与 Mailbox 协同**：
   - **Fork Turns 三模式**：全部继承（影分身加速并行）、继承最近三轮（隔离历史同时保留近期上下文）、无上下文 None（彻底上下文隔离完成独立任务）；
   - **Mailbox 异步通信**：提供 Send Message（仅消息入信箱静默等待消费，不打断目标运行）与 Follow-up Task（发往信箱并在空闲时唤醒、运行中在步骤边界安全投递）两种模式。
6. **传统 Compaction 创新：交接文档（Handover Document）策略**：针对窗口达到 80% 阈值、模型切换或切至小窗口模型触发的上下文压缩，提示词不要求做干瘪的纯 Summary，而是要求压缩模型输出一份面向接手者的完整“**交接文档**”，使状态保留更完整、结构化；从最早消息开始压缩，使后续轮次能够快速重建并稳定利用 Prefix KV Cache。
7. **全新 Token Budget 跨窗口短期记忆体系**：8 月份更新的 Token Budget 机制彻底颠覆传统压缩思路——触发阈值后不再破坏性压缩上下文，而是**新起一个带自增 ID 的全新空白窗口**，通过三大机制实现跨窗口无缝衔接：
   - **Thread Hint**：后端抽取约 4000+ 字节便签注入新窗口的 Developer Message，提供上一窗口的任务进展背景；
   - **Notes 虚拟文件系统**：服务端托管的 Agent 私人笔记本，支持 List、Read、Search、Append、Write 等工具，供 Agent 渐进式读写当前任务状态、修改文件与踩坑记录；
   - **History 轨迹回溯**：保存完整的 Agent Trace 历史条目，支持按需检索与细节展开。
   - **正交分工**：跨 Session 的长期记忆（Memory，经 Rollout Extraction 提取与 Global Consolidation 引用频次 Top-N 筛选，含可遗忘机制）与单 Session 内跨 Window 的 Token Budget 任务状态衔接正交运行。

## 关联实体与概念

- **关联实体**：[[entities/实体_Codex]]
- **关联概念**：[[concepts/概念_Harness_Engineering_宿主编排工程]]、[[concepts/概念_上下文工程]]、[[concepts/概念_Agent三层记忆体系]]、[[concepts/概念_Context_Rot_上下文衰退]]

> 📎 **物理文献**：[[raw/articles/深度解析 Codex Harness 架构及其全新上下文压缩记忆体系的设计思路.md]]
