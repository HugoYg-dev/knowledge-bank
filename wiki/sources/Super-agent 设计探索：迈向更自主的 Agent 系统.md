---
type: "source"
tags: ["AI-Agent/multi-agent", "AI-Agent/context-engineering", "AI-Agent/coding"]
summary: "DeepSeek Harness 团队系统阐述 Super-agent 架构：以双层架构（Router/Worker）兼顾连续交互与高效并发，事件驱动两级过滤与 Thread 直通，Inline & Spill 与链式召回，全双工异步 ReAct，存算分离（BYOM）与外部 Watchdog 自愈回路"
sources: ["raw/articles/Super-agent 设计探索：迈向更自主的 Agent 系统.md"]
updated: "2026-11-09"
---

# 来源摘要：Super-agent 设计探索：迈向更自主的 Agent 系统

## 来源元信息
- **标题**：Super-agent 设计探索：迈向更自主的 Agent 系统（Towards a More Autonomous Agent System）
- **作者 / 团队**：Yujia Qiao 等 / DeepSeek Harness 团队（DeepSeek-AI）
- **发布渠道**：微信公众号 / GitHub 开源原型（`deepseek-ai/dsh-superagent-prototype`）
- **发布日期**：2026-11-02
- **原文链接**：https://mp.weixin.qq.com/s/zoS7GlReWPhfCjENGxXCdg
- **开源原型**：https://github.com/deepseek-ai/dsh-superagent-prototype
- **物理文献**：[[raw/articles/Super-agent 设计探索：迈向更自主的 Agent 系统.md]]

---

## 核心要点

1. **突破单会话局限与 Super-agent 四大基础特征**：
   - 当前单会话 Agent 受制于同步阻塞、多任务上下文混乱及本地离线停运等局限；人类通常只能同时跟进 3 到 5 个活跃会话。单任务上限取决于模型能力，多任务上限取决于人的注意力。
   - **Super-agent 定位**：打破 Agent 与单次手动会话的绑定，成为跨会话保持上下文、多任务并发且互不干扰的连续自主协作者。具备四大基础特征：
     - **连续（Continuous）**：跨 IM、GitHub 等多界面交互，用户感知始终只有一个统一 Agent，无需记忆 Session 上下文边界；
     - **高效（Efficient）**：并发推进多任务且交互响应迅速，无需等待上个命令完成即可接受新指令；
     - **主动（Proactive）**：持续监听环境半结构化事件（Trigger），在无人 @ 情况下主动识别缺陷并提 PR（不需介入时保持安静）；
     - **持久（Persistent）**：始终在线、接入真实工作环境，在长期运行中遇到异常自动恢复。

2. **双层架构（Router 层 + Worker 层）解耦连续性与吞吐量**：
   - **核心权衡**：单会话太慢且上下文混杂，全独立会话缺乏全局上下文且回复割裂。将职责划分为两个层级：
   - **Router 层（常驻协调与人机界面）**：作为全局序点（Sequence Point）、协调点与记忆，统一承接所有入口的人类交互；不直接执行具体任务（甚至不配备 Bash 工具），仅负责分派；外部事件突发时触发自动**批处理（Batching）**（Prefill 并行计算，将单决策分摊推理时间从 6.4s 骤降至 1.6s）；超限时可水平切分（Sharding）。
   - **Worker 层（隔离并发执行）**：各个 Worker 上下文相互隔离，配置最强模型与完整工具链，专注单任务交付；不直接输出至外部信道，统一向 Router 汇报状态，避免多个会话各自回复造成交互混乱；内部可再嵌套 Subagent 或 Agent Team。

3. **事件驱动与四阶生命周期治理（Trigger、两级过滤、订阅直通、Inline & Spill）**：
   - **Trigger 与两级过滤**：面对环境高噪音、低触发率特征，采用程序层白名单准入（Fast Path）与语义层 LLM 提示词判断（Slow Path）相结合；
   - **Thread 订阅与直通（Fast Path 路由）**：同一话题或 PR 的连续事件构成 Thread；初始事件由 Router 创建 Worker 并建立多对多订阅，后续同 Thread 事件由程序**直接直通 Worker（Fast Path）**，绕过 Router 避免全局拥堵；消融实证直通机制为 Router 节省了 30% 决策量与 37% 读缓存 Token；
   - **Inline & Spill 与链式召回（Chain of Recall）**：将上下文视作 Cache。高频相邻内容（对象 ID、前 50 字摘要、前后相邻评论）执行 **Inline**，长内容超限部分 **Spill** 到窗口外；通过引用图赋予唯一 ID，支持沿 `Trigger -> Thread -> Worker` 关系按需逐跳多步展开上下文；
   - **投机执行（Speculative Execution）**：根据环境信号在后台提前行动（如群聊讨论时后台静默尝试复现并准备修复草稿），以廉价后台算力置换人类等待与介入成本。

4. **面向人的交互：异步 ReAct 全双工与信道定制**：
   - **全双工交互（异步 ReAct Loop）**：打破传统 `run()` 同步阻塞，引入异步 `start()` 与 `stop()`。调用后立即返回“已启动（Started）”，后台任务运行期间前台仍可实时响应人类输入；后台完成后作为新事件回流，模型亦可主动 `stop()` 超时任务；
   - **多信道交互规范**：IM 信道硬性约束低打扰、简短结论（单次回复 $\le 100$ 词）；GitHub/邮件/文档信道侧重高密度结构化交付。

5. **计算、状态与环境的分离（存算分离与 BYOM）**：
   - **计算与状态分离**：Agent Loop 计算放入云端无状态弹性容器，会话与任务状态持久化存入数据库，摆脱单机生命周期；
   - **计算与执行环境分离（Bring Your Own Machine）**：不强求将包含私有凭据、未提交修改和复杂工具链的重状态环境搬迁上云；云端常驻无状态 Agent Loop（脑），本地端侧仅部署不存状态的轻量 daemon（手）负责执行命令与回传结果；支持个人日常开发机接入，并支持间歇在线设备重连后自动唤醒任务。

6. **外部控制回路（Watchdog Session）与异常自愈**：
   - 传统进程存活监控无法捕获 Agent 陷入无效死循环或目标漂移；
   - 在主系统外部配置由定时消息驱动的独立 **Watchdog Session**，兼顾基础设施状态与任务语义进展监控；Watchdog 自身具备完整工具能力，支持维护者用自然语言排查故障并在线热修主系统规则与提示词。

7. **端到端消融实验与定量实证**：
   - 在 300 条消息（含 20 条工作请求）的模拟负载下，Super-agent 任务完成时间 p50 为 12.4 分钟，p95 为 15.7 分钟；
   - 相比之下，单 Session + Subagent 受提示词敏感性影响巨大：中性提示下 5 次测试中模型均未调用 Subagent，所有任务在主会话中串行阻塞且频繁被打断，p95 恶化至 29.5 分钟；优先委派提示下仍出现 1 次长尾；
   - 证明双层架构、事件驱动直通与存算分离能够从系统层面对多任务长程推进提供确定性保障。

---

## 关键引文

> “打破 Agent 与单次手动会话的绑定，使其成为一个能跨会话保持上下文、同时推进多项复杂任务且互不干扰的连续实体。我们把这种 Agent 形态及其系统架构称为 Super-agent。”

> “从这个角度看，让用户手动管理 Session，在很大程度上是从底层 LLM API 延续下来的设计惯性；Session 应当是系统的实现细节，而不应是用户的认知负担。”

> “把积压的多条 Trigger 合并进一次 LLM API 调用，会在 Prefill 阶段并行计算，单次请求耗时的增长远慢于批处理大小。因此在一定范围内，积压越多，单个决定分摊的推理时间越低。”

> “浪费上下文窗口，就是浪费模型的智能。将有限的上下文窗口当作 Cache 来管理……Inline 是指将近期很可能用到的信息直接内联进当前上下文窗口；Spill 则是将超出窗口预算或低频使用的完整信息留在上下文窗口之外。”

> “既然难以复制和同步的是环境本身，就不必让执行环境跟着 Agent Loop 上云。让 Agent Loop 在云端运行，而让重状态的执行环境留在原地，仅在端侧部署一个不保存会话状态的轻量 daemon……这种设计支持 BYOM（Bring Your Own Machine）。”

---

## 关联实体与概念

- **核心概念**：
  - [[concepts/概念_Super_Agent_超级智能体]]：常驻 Router 与独立 Worker 解耦、跨入口跨环境的连续自主智能体范式
  - [[concepts/概念_Harness_Engineering_宿主编排工程]]：微内核宿主、双层架构、存算分离与端侧 daemon 执行环境
  - [[concepts/概念_上下文工程]]：Inline & Spill 缓存化管理与基于引用图的链式召回（Chain of Recall）
  - [[concepts/概念_Personal_Agent_个人智能体]]：持续在线、事件驱动的同架构个人助理应用形态
  - [[concepts/概念_Loop_Engineering循环工程]]：全双工异步 ReAct Loop 与外部 Watchdog Control Loop
  - [[concepts/概念_Context_Rot_上下文衰退]]：Worker 隔离与链式召回避免长程会话上下文衰退
- **核心实体**：
  - [[entities/实体_DeepSeek_Harness]]：提供微内核架构支撑与开源原型验证的宿主工程底座
  - [[entities/实体_DeepSeek]]：Super-agent 架构与 DeepSeek Harness 开源研发机构

---
> 📎 **物理文献**：[[raw/articles/Super-agent 设计探索：迈向更自主的 Agent 系统.md]]
