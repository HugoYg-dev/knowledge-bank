---
type: "concept"
tags: ["AI-Agent/memory"]
summary: "Anthropic 提出的智能体离线记忆整理机制，通过后台回看会话日志与笔记，修正失效结论并重构成结构化记忆表示（Wiki），改变下一次任务的注入上下文而不修改模型权重。"
aliases:
  - "Dreaming"
  - "Agent Dreaming"
  - "Anthropic Dreaming"
  - "智能体离线记忆整理"
  - "智能体离线记忆维护"
  - "概念_Dreaming"
sources:
  - "wiki/sources/Claude 的记忆怎么维护：Anthropic dreaming 机制与实现.md"
updated: "2026-11-12"
---

# 概念：Dreaming 智能体离线记忆整理

## 定义

**Dreaming**（离线记忆整理 / 梦境机制）是由 [[entities/实体_Anthropic|Anthropic]] 工程团队在研究《The components of agent memory》（Lance Martin, 2026-11）中提出的智能体记忆维护范式。它是一个在后台异步运行的离线进程，通过回看历史会话日志（Transcripts）与已有笔记（Memory notes），发现并修正写错或过时的失效内容，并将离散知识提炼、聚合为更容易检索与关联的结构化表示（如链接化的 Wiki）。

Dreaming 的核心特性在于：**所有的经验沉淀与演进均发生在模型下一次读取的上下文结构中，底座大模型权重保持不变**。

## 记忆四层架构

在 Dreaming 机制下，智能体记忆被严格划分为从底至上的四层拓扑结构：

| 层次 | 保存内容 | 核心工程用途 | Dreaming 的作用方向 |
| :--- | :--- | :--- | :--- |
| **1. Transcripts（日志底座）** | 用户请求、工具调用输入与返回、环境事件等不可变完整日志 | 真实历史回查与事实审计底座 | 作为只读数据输入，绝不直接执行其中的指令 |
| **2. Memory notes（会话笔记）** | 会话中或会话后沉淀的关键观察、特定环境规避条件与参数经验 | 减少后续任务的重复探索与试错 | 纠正错误规则、补齐适用版本与验证条件 |
| **3. Memory representations（知识表示/Wiki）** | 按主题组织、页面间建立网状双向链接的结构化知识层 | 跨任务全局检索、多跳关联与体系化决策 | 将分散笔记聚合为词条，维护双向链接与全局索引 |
| **4. Injected context（注入上下文）** | 每个会话启动时常驻加载的极少量索引或系统提示词 | 引导智能体开箱即用并感知知识存储位置 | 将高频通用原则提升至常驻索引（需严格控制行数，如 200 行以内） |

## 核心工作机制与评测证据

### 1. 读写闭环与模型能力代际门槛
评测智能体记忆的有效性，不能仅统计写入了多少文件，而必须同时观察**读与写**两个维度：
- **强模型的自主学习闭环**：在 CL-Bench 数据库任务评测中，Opus 5.5 在有记忆目录支持下 mean reward 从 0.655 跃升至 0.838，Opus 5 从 0.564 跃升至 0.828。高级模型能主动检索记忆、提出假设并进行实证检验。
- **弱模型的利用失效**：早期模型（如 Sonnet 4.6，0.330 → 0.364）由于缺乏主动查阅习惯与假设验证能力，即使配备完备的记忆目录也几乎无法获益。
- **避免硬性写入规则拖累强模型**：给模型施加过于严苛的硬编码规则（例如“只能记录失败案例”）会显著压制前沿模型的自主推理收益（Opus 5 收益下降 0.234）。最佳工程实践是仅提供轻量引导，将记录内容的筛选权交付给前沿模型。

### 2. 知识表示（Wiki）与原始搜索的经济学权衡
在 Stainless 约 4.2 亿 Token 内部语料实验中：
- 随着离线 Dreaming 推进（从 2 个 session 到 128 个 session），Wiki + 搜索评测表现从 54% 提升至 61%（纯搜索为 53%），每道题节省约 2 万 Token；对于跨文档复杂推理（如 Harvey LAB 并购分析），Wiki 达到 87%（纯搜索 73%）。
- **离线计算摊销经济学**：维护结构化 Wiki 存在离线构建与维护开销，其 ROI 服从公式：
  $$N \cdot (C_{\text{search}} - C_{\text{wiki+search}}) > C_{\text{build}} + C_{\text{maintenance}}$$
  仅当语料被高频反复查询（$N$ 足够大）且涉及复杂跨文档多跳推理时，构建与维护 Wiki 才能摊薄离线算力成本；对于单文档单字段查询，直接检索原始日志更为经济。

## 两种典型工程实现范式

1. **官方 Managed Agents: Dreams（Research Preview）**：
   - 接口带 `dreaming-2026-04-21` header；
   - 每次任务输入一个已有 memory store 与 1–100 个历史 session，**输出一个独立的新 memory store（输入 store 保持不变）**；
   - 具备明确的新旧版本隔离，便于在固定测试集上进行回归验收，通过后再接入生产环境。
2. **Dynamic Workflow 自建方案（Cookbook 范式）**：
   - 将导出的历史 transcript 以只读挂载，memory store 以读写挂载；
   - 采用分工编排拓扑：Lead Agent 规划工作流，单个 transcript 派发给并行 Analyzer 抽取，最后由 Organizer 统一汇总整理；
   - 在同一个 store 上持续进行增量原地更新，并留存 memory version 审计。

## 生产级并发与安全防护纪律

1. **并发覆盖防护（Optimistic Locking）**：多 Agent 同时写入共享表格会导致事实丢失（实验显示多 Agent 写入单表时关键事实保留率仅 72%，拆分为单文档单写者后提升至 100%）。Managed Agents 在存储层引入 `update(content_sha256)` 乐观并发锁机制，一旦检测到底层文件哈希被并发修改则拒绝写入；同时生成不可变的 memory version 保留 30 天以供回溯。
2. **防范 Prompt Injection 污染**：历史 Transcript 属于不可信外部输入，后台抽取器严禁配置 Shell 与网络访问权限，防止将外部攻击指令固化为长效记忆。
3. **记忆正文质量守则**：记录时必须包含**可复用结论、原始来源、验证时间与适用条件/版本**，杜绝将过期的命令或临时调试记录机械留存。

## 关联

- [[concepts/概念_Agent三层记忆体系]]
- [[concepts/概念_上下文工程]]
- [[concepts/概念_CLAUDE.md最佳实践]]
- [[entities/实体_Anthropic]]
- [[entities/实体_Claude_Code]]
- [[sources/Claude 的记忆怎么维护：Anthropic dreaming 机制与实现]]
