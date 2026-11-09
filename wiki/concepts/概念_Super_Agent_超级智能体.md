---
type: "concept"
tags: ["AI-Agent/multi-agent", "AI-Agent/UI"]
summary: "常驻 Router 协调分派与独立 Worker 执行解耦、跨入口跨工作环境且能代表用户持续推进复杂长程任务的智能体架构形态与产品范式"
aliases:
  - "Super Agent"
  - "超级智能体"
  - "概念_Super_Agent"
sources:
  - "wiki/sources/从OpenClaw，怎么走到了Super Agent？.md"
  - "wiki/sources/便宜的模型越来越多，怎么判断它能不能胜任我的 Agent 工作.md"
  - "wiki/sources/Super-agent 设计探索：迈向更自主的 Agent 系统.md"
updated: "2026-11-09"
---

# 概念：Super Agent（超级智能体）

## 1. 核心定义与演化脉络

**Super Agent（超级智能体）** 是一种打破 Agent 与单次手动会话（Session）绑定，将**常驻全局协调路由层（Resident Router）**与**上下文隔离执行层（Isolated Worker）**解耦，能够跨交互信道保持上下文连续、同时高并发推进多项复杂任务且互不干扰的连续自主智能体架构形态与产品范式。

### 1.1 四大基础特征（DeepSeek Harness 架构定义）
根据 DeepSeek Harness 团队提出的系统设计约束，Super-agent 具备以下四大基础特征：
- **连续（Continuous）**：用户直接在 IM 聊天、GitHub 评论等熟悉的工作界面与它交互，感觉始终只存在一个统一 Agent，无需记忆“Session X 的上下文中是否有 Y 信息”；
- **高效（Efficient）**：交互响应迅速，同时能并行、高质量完成多个复杂任务；无需等待上一个命令或任务完成，就能接收下一条新指令；
- **主动（Proactive）**：无需等待用户逐条下达指令，持续观察环境事件流（Trigger），在无人 @ 的情况下主动推进值得处理的事项（如群聊静默复现缺陷并提交修复 PR），不需要介入时则保持安静；
- **持久（Persistent）**：始终在线、直接接入用户真实的重状态物理工作环境，并在长期运行中遇到异常时自动恢复。

### 1.2 演化驱动力：从 Bot 到 Working Agent 的“双向奔赴”
1. **第一阶段：以 Bot 为入口的初始探索（易用与泛在触达）**：
   - 早期形态以 OpenClaw 等聊天机器人（Bot）为主，依赖即时通讯（IM）等极低门槛的聊天窗口，人无需一直守在电脑前即可随时随地唤起。
   - **痛点**：缺乏深层业务工作区，难以感知本地代码仓库结构、口径变动历史及未言明的业务背景，停留在“能找到但干不好复杂任务”的浅层阶段。
2. **第二阶段：以 IDE/桌面端为阵地的 Working Agent（贴近真实工作环境）**：
   - 随着对交付质量要求的提高，WorkBuddy 等工作台类、IDE 类 Working Agent 兴起。其核心优势在于深度嵌入真实工作现场（左侧资料、中间编辑、右侧对话、底部执行），使得任务上下文、历史否决方案和调试反馈能自然沉淀。
   - **痛点**：局限于单一设备和特定桌面环境，离开电脑便产生交互断层，外部即时产生的灵感与会议结论无法即时回流。
3. **第三阶段：双向融合催生 Super Agent 范式**：
   - 近期 Bot 类产品积极补齐底层工作台、本地连接器与工具链，而 Working Agent 则反向拓展移动端、群聊等常驻入口；
   - 驱动该收敛的是两个根本诉求：**Agent 要干好活必须贴近真实物理环境**；**Agent 越好用、磨合越深，人越希望能随时触达它并向他人复用其能力**。两者的最终收敛形态即为 Super Agent。

---

## 2. 核心架构与运行机制

Super Agent 在系统工程上打破了“单会话大包大揽”的传统模式，将“维护全局连续性”与“高并发执行”分拆到两个不同层级，构建了五大核心支撑模块：

### 2.1 双层架构（Router 层 + Worker 层）解耦连续性与吞吐量
- **常驻 Router 层（协调与全局序点）**：
  - 作为全局序点（Sequence Point）、协调点与记忆，统一承接所有入口的人类交互。
  - **职责约束**：Router 层不直接执行具体任务，甚至不配备 Bash 工具，避免中心节点成为计算瓶颈；
  - **自动批处理机制（Batching）**：突发事件密集涌入时，上一轮推理期间积压的多条 Trigger 会在下一次 LLM 调用中一并注入，在 Prefill 阶段并行计算。压力测试表明到达速率从 1条/分 提升到 40条/分 时，单决策分摊推理时间从 6.4s 骤降至 1.6s；超限时可水平切分（Sharding）。
- **隔离 Worker 层（并发任务执行）**：
  - 各个 Worker 上下文彼此物理隔离，挂载完整执行工具链与主力模型，在独立上下文中专注单一任务，彻底消除多任务交叉污染与上下文腐化（Context Rot）；
  - **状态聚合回复**：Worker 不直接向外部信道输出推理与工具细节，其状态向 Router 汇报并由 Router 统一对外部输出，消除多会话争抢回复的混乱。

### 2.2 事件驱动与 Thread 订阅直通（Fast Path / Slow Path）
- **Trigger 与两级过滤**：
  - 针对环境事件“高噪音、低触发率”特征，先通过程序层白名单与规则进行快速准入检查（Fast Path），仅将候选事件交由语义层 LLM 提示词判断（Slow Path）；
- **Thread 订阅与直通（Direct-pass Routing）**：
  - 同一话题或 Pull Request 的连续事件构成 **Thread**。Router 分派任务后 Worker 直接订阅该 Thread；
  - 同一 Thread 的后续事件由程序**直接直通（Fast Path）**发往已订阅的 Worker，无需 Router 中转；消融实证直通机制减少了 Router 30% 决策负担并节省 37% 读缓存 Token。多 Worker 订阅同 Thread 时可自动感知彼此操作并协同。

### 2.3 上下文组织：Inline & Spill 与链式召回（Chain of Recall）
- **上下文 Cache 化管理**：
  - **Inline**：将近期高频使用的关联信息（当前对象 ID、前 50 字摘要、前后相邻消息/评论）直接内联入窗口，减少工具往返；
  - **Spill**：超出预算的长内容截断并溢出到窗口外，保留按需读取入口；
- **链式召回（Chain of Recall）**：
  - 系统为 Trigger、Thread、Worker 赋予唯一 ID 并相互内联构成引用图。模型可从当前事件出发，顺着引用链多跳按需展开历史上下文（`Trigger -> Thread -> Worker -> 相关代码评审`），解决长程记忆丢失。

### 2.4 全双工交互与投机执行
- **异步 ReAct Loop（全双工）**：
  - 将耗时命令改为异步的 `start()` 和 `stop()`。调用后立即返回 Started，后台任务运行期间前台仍可随时响应用户新输入；后台执行完毕作为新事件投递进会话，且模型可主动 `stop()` 超时任务；
- **投机执行（Speculative Execution）**：
  - Agent 在不确定是否被采纳时，根据环境信号后台提前尝试（如群聊讨论时后台静默复现缺陷并准备 PR），以廉价后台算力换取人类时间成本。

### 2.5 存算分离与执行环境解耦（BYOM）
- **计算与状态分离**：Agent Loop 放入云端无状态弹性计算容器，会话与任务状态存入持久数据库，打破单机生命周期；
- **计算与执行环境分离（Bring Your Own Machine）**：不强求将含有私有凭据、未提交修改和本地依赖的重状态环境迁移上云；云端常驻无状态 Agent Loop（脑），本地端侧仅部署轻量无状态 daemon（手）执行命令并回传结果，支持日常开发机与间歇在线设备跨端接入。

### 2.6 外部控制回路（Watchdog Session）与人机共建
- **Watchdog 语义监控与自愈**：
  - 在主系统外配置独立的 Watchdog Session 充当外部 Control Loop，既监控基础设施，又监控 Worker 是否取得实质进展或偏离目标；具备完整工具能力，支持自然语言排查故障并在线热修规则；
- **成熟 Agent 辅导机制（Mature Agent Coach）与环境共建**：
  - 成熟主 Agent 辅导新 Worker，审查轨迹、对齐业务口径；人与 Agent 借助微内核插件机制（如 DeepSeek Harness Creator mode）共建执行环境。

---

## 3. 代表系统与工程落地

| 系统 / 方案 | 架构角色与落地实现 | 关键工程特性 |
| :--- | :--- | :--- |
| **DeepSeek Super-agent 原型 (`dsh-superagent-prototype`)** | DeepSeek Harness 团队官方研究原型与落地实践：双层架构（常驻 Router + 隔离 Worker）与事件驱动系统 | 基于 [[entities/实体_DeepSeek_Harness|DeepSeek Harness]] 微内核；支持 IM 与 GitHub 跨信道连续推进、群聊无人 @ 主动识别缺陷提 PR、Thread 订阅直通（节省 37% 读缓存 Token）、异步 ReAct Loop 全双工交互、BYOM 存算分离与外部 Watchdog 自愈 |
| **[[entities/实体_HiRoute|HiRoute]] + Hermes/OpenCode** | 阿里云开源本地任务路由（Task Routing）与动态调度工程实践 | 通过 `hiroute worker exec` 绑定预设场景计划（如 Pi、Qoder CLI、Codex CLI），实现非阻塞并行执行、单轮锁定 90% 前缀缓存保护与后台唤醒回传 |
| **WorkBuddy / OpenClaw 演化** | 腾讯内部 iMate 平台与微信生态连接实践 | Working Agent 接入移动端与企业微信群，实现“群聊提出 → 唤起 Agent 补充背景 → 异步执行 → 交付结果”闭环 |

---

## 4. 选型与工程权衡（Trade-offs）

1. **状态一致性 vs 上下文隔离**：
   - 解耦 Worker 可以大幅降低单步 Token 成本并规避模型幻觉，但跨 Worker 的知识同步、数据共享与最终一致性需要依赖严格的元数据总线或共享账本，避免信息孤岛。
2. **多端入口同步复杂度**：
   - 用户在移动端轻量追加的需求与桌面端正在跑的深度执行流之间需要建立优雅的上下文注入队列（Steering），防止执行冲突或打断关键锁区。
3. **权限与隐私隔离边界（云端 Loop 与端侧 Daemon）**：
   - 存算分离让 Agent Loop 常驻云端并通过 daemon 接入本地开发机（BYOM），但外部不可信事件（提示词注入）若与本地未提交敏感代码/凭证相连，存在越权风险；必须在完全不接触凭据本身的情况下使用凭据。
4. **长程记忆扩展瓶颈与 A2A 边界**：
   - 链式召回主要解决近期任务与会话历史的按需检索，跨月运行的长程记忆仍是制约扩展的瓶颈；多实例在不同权限边界间协同需要安全的 Agent-to-Agent（A2A）协议支持。

---

## 5. 关联概念与实体

- **核心概念**：
  - [[concepts/概念_Personal_Agent_个人智能体]]：聚焦个人生活、长程在线与主动陪伴的同类范式
  - [[concepts/概念_Harness_Engineering_宿主编排工程]]：支撑 Worker 执行、存算分离与自进化的底层环境体系
  - [[concepts/概念_上下文工程]]：Inline & Spill 缓存化管理与链式召回多跳检索治理
  - [[concepts/概念_LLM模型路由]]：在任务执行底层根据复杂度与缓存策略进行模型选型的配套基础设施
  - [[concepts/概念_Loop_Engineering循环工程]]：全双工异步 ReAct Loop 与外部 Watchdog Control Loop
- **核心系统与实体**：
  - [[entities/实体_HiRoute]]：支持 Super Agent 式任务路由与本地模型动态调度的开源项目
  - [[entities/实体_DeepSeek_Harness]]：提供命令式插件化、Creator mode 与自进化环境支持的智能体底座
  - [[entities/实体_DeepSeek]]：Super-agent 架构与 DeepSeek Harness 开源研发机构

---

## 6. 支撑来源

- [[wiki/sources/Super-agent 设计探索：迈向更自主的 Agent 系统.md]]
- [[wiki/sources/从OpenClaw，怎么走到了Super Agent？.md]]
- [[wiki/sources/便宜的模型越来越多，怎么判断它能不能胜任我的 Agent 工作.md]]
