---
type: concept
tags:
- AI-Agent/context-engineering
summary: Post-Compact Rehydration（压缩后状态回水）是智能体长会话上下文压缩后，通过外挂 Hook 或系统附件将真实历史请求、源码切片与活跃技能等关键 Ground Truth 自动回填至上下文的工程机制。
sources:
- wiki/sources/Antigravity CLI 压缩后无损回水（Post-Compact Rehydration）与跨 fork 溯源方案.md
updated: '2026-11-16'
aliases:
- Post-Compact Rehydration
- Post-Compact State Rehydration
- 压缩后状态回水
- 上下文回水
- 状态回水
- 无损回水
- 概念_Post_Compact_Rehydration
---

# 概念：Post-Compact Rehydration（压缩后状态回水）

## 定义

**Post-Compact Rehydration（压缩后状态回水）** 是在长程 AI Agent 交互中，针对长会话触发自动或手动上下文压缩（Compaction）后造成的上下文“断忆”问题，通过运行时 Hook 或框架内建附件，在压缩后的第一轮调用前将未被总结污染的真实源码、关键指令与历史轨迹等“客观事实（Ground Truth）”按预算自动重新注入模型的工程机制。

## 核心设计哲学

> **“`<CONTEXT_SUMMARY>` 是有损的，但本地磁盘上的会话流水和工作区源码是 100% 无损的 Ground Truth。”**

传统的上下文压缩仅依赖单一摘要模型生成全局总结，极易导致：
1. **全局红线丢失**：跨轮次历史中的环境规范、排版约定或接口约束被模糊概括；
2. **源码与轨迹清空**：前期耗费大量工具调用读取的文件和执行轨迹彻底消失，迫使模型凭印象猜测；
3. **分支断代**：在支持 `/fork` 等分叉会话的 Agent CLI 中，子会话往往丢失父分支的上下文支撑。

## 工业实现方案对比

| 机制维度 | [[entities/实体_Claude_Code|Claude Code]] (v2.1.322+) | [[entities/实体_Antigravity|Antigravity CLI]] (PreInvocation 方案) |
|---|---|---|
| **接入层级** | 官方 Harness 内核原生事件 | 零侵入用户级全局 Hook（`PreInvocation`） |
| **触发时机** | 压缩边界后追加合成记录 | 检测到新增 `CHECKPOINT` 后的首轮对话 |
| **摘要形态** | 9 段结构化摘要（`isCompactSummary: true`） | 原生 `<CONTEXT_SUMMARY>` + 外部注入 |
| **回水载体** | `type: "attachment"` 结构化系统附件 | `injectSteps -> systemMessage` 动态系统消息 |
| **文件恢复** | `compact_file_reference` 挂载活跃文件 | Top 3 修改 + Top 3 读取文件（头部 68% + 尾部） |
| **技能与规范** | 自动恢复 `invoked_skills` 与 `plan_file_reference` | 实时重读接触过的 `SKILL.md` 及 SPEC/PLAN 文档 |
| **分叉会话溯源** | 框架原生分支树 | 向上递归 8 层遍历同级 `brain/*` 多维消歧还原祖先链 |

## 四层回水结构与 Token 预算配额

为了在无损恢复核心上下文的同时不挤占后续推理空间，状态回水通常实施严格的分层预算分配（以 256K 上下文为例，回水控制在 28K–38K tokens，仅占窗口约 12%–15%）：

1. **Header 溯源路标**：标注当前压缩点步号与跨 fork 会话分支谱系（Lineage）；
2. **全量用户需求时间线（User Request Timeline）**：从底层持久化流水中逐字提取全量真实 `USER_INPUT`，超限时保留最早 5 条立项红线与最近提问；
3. **压缩前逐字对话滑窗（Pre-Compaction Dialogue）**：倒推保留最近数轮 User/Assistant 完整对话，并将中间连续工具调用紧凑折叠为单行 `(Tools run: read -> edit)`；
4. **活跃技能与规范文档（Active Skills & Spec Docs）**：从工作区磁盘实时读取最新自定义 `SKILL.md` 及含有 SPEC / PLAN / HANDOFF 的文档；
5. **活跃工作区源码（Active Workspace Files）**：从磁盘读取最后触碰的 Top-K 关键源码文件，超限文件实施两端保留并标注中间截断字符。

## 工程防护纪律

- **快速短路（Early Exit）**：通过字节偏移增量扫描，无压缩轮次耗时控制在毫秒级（~1ms），杜绝引入额外延迟；
- **老会话守卫**：设置新近压缩点距离步数上限（如最大间隔 8 步），防止冷启动老会话误触重放陈旧压缩点；
- **Fail-Open 熔断机制**：任何解析异常均放行原始调用，绝不阻塞开发者的终端交互流程。

## 关联

- [[concepts/概念_上下文工程|概念_上下文工程]]
- [[concepts/概念_Context_Rot_上下文衰退|概念_Context_Rot_上下文衰退]]
- [[entities/实体_Antigravity|实体_Antigravity]]
- [[entities/实体_Claude_Code|实体_Claude_Code]]
- [[sources/Antigravity CLI 压缩后无损回水（Post-Compact Rehydration）与跨 fork 溯源方案|Antigravity CLI 压缩后无损回水（Post-Compact Rehydration）与跨 fork 溯源方案]]
