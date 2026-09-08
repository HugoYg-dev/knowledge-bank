---
title: "阿里高德 LongHorizon-Harness 框架：使用审计状态机重构Agent执行流程"
source: "https://mp.weixin.qq.com/s/hPR4uXPs_5sD9-2i3lG_eQ"
author:
  - "Coggle数据科学"
published: 2026-08-26
created: 2026-09-08
description:
tags:
  - "clippings"
---
Coggle数据科学 *2026年8月26日 16:20*

传统 Agent Harness 通常把执行过程、任务记忆和完成判断放在同一个不断增长的会话中，模型一边行动，一边依据自己的历史描述维护状态，最后再由同一个执行主体判断是否成功。

![图片](https://mmbiz.qpic.cn/mmbiz_png/U2KthBqSEeib1B3hlr8vCLF2PYOkzJHm045o0XPAZCia1Q1ibPSlO5H6WjdJAw8GmJicLs5d2gES47FC0wOthqTBVqSLOjjLVMbXqviaQXGO6bl0/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

阿里高德团队提出的 LongHorizon-Harness 将这个问题重新定义为 **任务状态管理问题** ，而不是简单的长上下文问题。通过 Manage-Execute-Audit（MEA）循环，把长期协调、局部执行和独立验证拆成三个结构上隔离的角色。

> https://lh-harness.pages.dev/

本文会把LongHorizon-Harness与当前 Claude Code、Codex 的会话、记忆、子代理、代码审查、权限和并行机制逐项比较，从而说明 LongHorizon-Harness 增加的是哪一层能力，以及什么时候原生 Coding Agent 已经足够使用。

### LongHorizon-Harness 安装与方式

```
uv tool install lh-harness

lh-harness doctor

cd /path/to/project
lh-harness init

lh-harness run \
  --task @task.md \
  --agent codex \
  --dashboard
```

如果希望在浏览器中创建任务、选择每个角色的后端与模型、响应授权请求并在运行中追加指令，可以直接启动：

```
lh-harness web --workspace-root .
```

### 为什么长任务不是“把 Context Window 调大”就能解决

短任务里，Agent 可以把目标、工具调用、观察结果和中间推理全部保留在同一个上下文中。即使其中存在冗余，模型通常仍能找到当前问题的关键信息。然而在长任务中，系统要同时记住原始目标、硬性约束、已完成步骤、失败尝试、文件路径、界面状态、外部依赖、交付物和验收标准，工具还会不断返回日志、截图、网页、代码和报错。 **上下文即使没有达到物理上限，也会因为有效信息密度下降而出现检索和推理退化。**

![Two panels side by side. Left: a single growing session coils back on itself, judging its own progress, and drifts. Right: a manager re-plans the next subtask from audited facts, a fresh-context executor performs it, and a read-only auditor certifies what actually changed.](https://mmbiz.qpic.cn/sz_mmbiz_png/U2KthBqSEeicFU1iaXIVdtQb2krohF3ePN7tOB5boBAVt3giccnbe0Eyh4SMLeLQG3bApIMD3c6AYe57clLCfZFW5WhFTWURbVmmlHr1roodAw/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=1)

Two panels side by side. Left: a single growing session coils back on itself, judging its own progress, and drifts. Right: a manager re-plans the next subtask from audited facts, a fresh-context executor performs it, and a read-only auditor certifies what actually changed.

LongHorizon-Harness把这类失败归纳为三个相互强化的问题：

- Compounding Errors 与 Goal Drift，早期错误一旦被当作事实，后续计划会在错误前提上继续展开；
- Context Rot 交互历史越长，关键约束越容易埋在大量局部观察之中；最后是 Task-State Loss，Agent 无法稳定回答“哪些要求已经满足、哪些产物已经产生、环境当前到底是什么状态、还有什么必须完成”。

传统单会话 Harness 的隐含数据流可以概括为：模型执行操作，随后把自己的总结写入历史，再根据同一份历史决定下一步，并最终判断自己是否完成。这里至少存在两个结构性耦合：执行与状态维护共享上下文，执行与完成判断共享主体。只要一次错误总结进入历史，LongHorizon-Harness 在形式上就与真实证据没有区别；只要模型认为界面“看起来已经正确”，系统就可能提前结束，而没有人重新读取文件、运行测试或检查真实应用状态。

**LongHorizon-Harness 的处理方式不是让单个会话记得更多，而是让局部会话忘得更彻底，同时让系统状态记得更可靠。** Executor 的原始轨迹在每轮之后不再进入后续执行上下文，跨轮保留的是压缩后的任务状态与审计报告。这里的“忘记”并不意味着运行日志被物理删除，当前开源实现仍会将角色输入输出、事件和轨迹保存到运行目录，便于观察和恢复；它真正丢弃的是这些高噪声轨迹作为下一轮推理上下文的资格。

### 从轨迹中心转向状态转换中心

普通 Agent 往往把一次任务理解为一条逐渐变长的轨迹：

其中 是动作， 是环境观察。系统是否继续、如何继续以及是否完成，主要从整条轨迹中推断。 **LongHorizon-Harness 则把任务理解为一系列经过审计的环境状态转换。每一轮不要求保留此前所有动作，而是要求回答三个问题：当前有哪些可信事实，这一轮允许改变什么，改变之后环境是否真的满足验收条件。**

```
flowchart TD
    T["原始任务与可信状态"] --> M["Manager 生成子任务契约"]
    M --> E["Executor 在新上下文中执行"]
    E --> A["Auditor 只读检查真实环境"]
    A --> D{"证据是否满足契约"}
    D -->|满足| S["写入可信进度"]
    D -->|不满足| G["记录缺口或完整性问题"]
    S --> M
    G --> M
```

### MEA 循环的三个角色

#### Manager：管理可信状态，不直接操作环境

Manager 拥有原始任务、当前任务状态和累计审计报告，但没有直接访问计算机环境的接口。它不能点击界面、读取工作区、运行 Shell，也不能修改文件。

任务状态在LongHorizon-Harness中被定义为三类记录的集合：

- Requirement 表示从原始任务提取的目标或约束
- Artifact 表示执行过程中创建或修改的交付物
- Fact 表示后续轮次需要使用的环境事实

每条记录都带有 `completed` 、 `pending` 、 `blocked` 或 `untrusted` 状态，并保留支持当前状态的审计证据。Manager 每轮先将新审计结果应用到状态，再比较状态与原始任务，选择一个当前可推进的未解决目标，并为其生成依赖、边界和验收标准。

#### Executor：唯一有意改变环境的角色

Executor 是唯一被允许主动改变任务环境的角色。它接收原始任务、Manager 维护的状态、本轮子任务契约，以及契约明确引用的少量历史审计报告，然后在一个全新的、受预算限制的上下文中执行。

系统还区分 GUI 与 CLI 两类主要状态转换。GUI Executor 负责屏幕、应用界面和交互状态，CLI Executor 负责文件、进程、程序、脚本、测试与工作区状态。

#### Auditor：读验证结果

Auditor 接收原始任务、当前状态、本轮契约、Executor 报告和相关历史审计，但不会获得 Executor 的原始推理与工具轨迹。

Auditor 可以改变观察视角，例如打开文件、查看界面或执行非修改性命令，但不能创建、编辑、移动、覆盖或删除受保护产物，也不能执行会改变被审对象的操作。

审计报告同时给出三种判断维度，而不是一个模糊的“通过/不通过”。当前源码要求报告前三条控制行分别表达任务状态、完整性状态与契约审计状态；任务状态为 `complete` 、 `incomplete` 或 `blocked` ，完整性为 `clean` 、 `suspect` 或 `violation` ，契约审计为 `aligned` 、 `unknown` 、 `needs_revision` 或 `invalid` 。

| 维度 | 可选状态 | 回答的问题 |
| --- | --- | --- |
| Completion Status | `complete`  / `incomplete` / `blocked` | 本轮子任务的验收条件是否已经满足 |
| Integrity Status | `clean`  / `suspect` / `violation` | 证据与产物是否可信，审计过程是否污染环境 |
| Contract Audit | `aligned`  / `unknown` / `needs_revision` / `invalid` | 本轮合同是否仍忠实覆盖原始任务与硬约束 |

### 子任务契约如何约束执行

MEA 循环不是把一句“继续做”传给下一个 Agent，而是要求 Manager 产生 Subtask Contract。一个有效合同至少包含立即目标、验收标准、边界约束、依赖条件，以及本轮执行和审计所需的历史证据引用。

**契约也是长任务动态分解与固定计划之间的中间层。预先生成完整 DAG 的问题在于，真实环境经常产生未知错误，后续步骤依赖本轮实际结果** ，任务无法一次性拆完；完全反应式执行的问题则是缺乏全局约束，容易被当前界面和局部报错牵着走。LongHorizon-Harness 每轮只承诺一个可审计的局部转换，同时始终把它放在原始任务和稳定合同下解释，因此允许动态改道，但不允许动态降低目标。

### LongHorizon-Harness 不是 Claude Code 或 Codex 的替代品

把 LongHorizon-Harness、Claude Code 和 Codex 放在同一个平面上比较，很容易得出错误结论，因为它们并不完全处在同一层。

![图片](https://mmbiz.qpic.cn/mmbiz_png/U2KthBqSEeicJosw1sNwbQEOI1uAxXzjpibibenQk7aLXib361sicrXeic8f5b2lE2m6Nr9nnqUS6QXGMply40OK0t7UjSDPGzg3OHtuem1k20cRQ/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=3)

Claude Code 与 Codex 首先是可以独立工作的 Coding Agent Harness：它们把模型、文件读写、Shell、搜索、测试、版本控制、权限与交互界面组合成一个原生 Agent Loop，用户给出目标后，Agent 会自行观察、行动、读取反馈并继续调整。

**LongHorizon-Harness 则更像这些 Harness 外面的“事务协调层”，它没有试图重新实现代码搜索、编辑器、Shell 或模型的内部 Tool Loop，而是通过 `AgentAdapter` 把 Claude Code、Codex 等现有 Agent 作为某一轮的执行引擎，再额外规定这一轮怎样获得输入、谁可以改变环境、谁负责验收，以及哪些结论可以进入下一轮。**

```
flowchart TD
    U["用户的长期目标"] --> H["LongHorizon-Harness：MEA 外层循环"]
    H --> M["Manager：选择下一项状态转换"]
    M --> C["Claude Code / Codex：原生 Agent Loop"]
    C --> E["代码库、终端、桌面与外部环境"]
    E --> A["Auditor：重新取证并决定是否提交状态"]
    A --> H
```

### LongHorizon-Harness 与 Claude Code 的区别

Claude Code 已经远不只是一个“单 Agent、单上下文”的终端工具。它的原生循环能够读取和编辑文件、执行命令、运行测试、使用 Git、搜索网页，并通过 Skills、MCP、Hooks 和 Subagents 扩展工作流；复杂任务可以被拆成步骤，工具结果会继续反馈给模型。每个新会话虽然从新的上下文窗口开始，但用户可以恢复或分叉会话，Claude Code 也会自动压缩接近上限的历史，并使用 `CLAUDE.md` 与 Auto Memory 在会话之间保留项目规则、偏好和经验。

Claude Code 的 Subagent 同样已经覆盖了“隔离上下文”这一重要思路。每个 Subagent 可以拥有独立上下文、专用系统提示、不同工具权限与模型，适合把搜索日志、测试输出或专项审查留在侧线程中，只把摘要返回主会话；当前版本还支持前台或后台运行、恢复 Subagent，以及更高层的并行会话与 Agent Team。换言之，“多角色”“新上下文”和“把噪声移出主线程”本身都不是 LongHorizon-Harness 独有的发明

Claude Code 的主线仍然是会话中心模型：对话历史、压缩摘要、 `CLAUDE.md` 、Auto Memory 和 Subagent 返回的摘要共同构成后续推理上下文，这些机制的目标是让 Agent 记得规则、经验和正在做的事情。官方文档也明确指出， `CLAUDE.md` 与 Auto Memory 属于提供给模型的 Context，而不是强制执行的配置；如果某个动作必须被阻断，应使用 `PreToolUse` Hook。

LongHorizon-Harness 的 `task_state` 则不是一般意义上的项目知识，而是当前任务的提交账本，Executor 对完成情况的描述没有直接写入权，只有 Auditor 从环境重新获得的证据才有资格改变 Requirement、Artifact 或 Fact 的状态。这使它关注的不是“下一轮模型还记不记得”，而是“下一轮模型拿到的进度是否已经过验收”。

Claude Code 的 Hooks 使两者的边界比表面看起来更接近。Hooks 可以在会话、每轮提示、每次工具调用、Subagent 生命周期、任务创建与完成、Context Compaction 等节点执行 Shell、HTTP 或 LLM 检查，也能阻止某个工具调用；有经验的团队完全可以用 `TaskCompleted` 、 `Stop` 、 `PreToolUse` 和 `PostToolUse` Hooks 自行搭建测试门禁、策略检查和证据采集。然而这些 Hooks 是可编程扩展点，并不会默认把整个任务重构成 Manager—Executor—Auditor 状态机。LongHorizon-Harness 的贡献正是提供一套现成的外层协议，使“每轮新 Executor、执行与验收分权、审计结果成为跨轮状态、失败后从可信进度恢复”成为默认路径，而不是依赖用户自行拼装 Hooks 与 Prompt。

Claude Code 当前的 `/code-review` 会在独立上下文的后台 Subagent 中检查分支提交和未提交 Diff，返回正确性、复用、简化与效率方面的发现，因而它已经能够避免“让刚写代码的同一上下文随手自评”。但这个 Review 的默认对象仍然是代码差异，它通常是用户调用或工作流触发的一项能力；MEA Auditor 则是每个状态转换后的必经环节，其验收对象由本轮合同确定，可以是文件内容、测试结果、服务状态、GUI 画面、文档内部结构或跨应用副作用，而且 Auditor 的结论会直接决定 Manager 能否把某项要求标记为完成。二者都有独立审查者，却服务于不同粒度：前者偏向工程质量审查，后者偏向长期任务的状态提交。

Claude Code 的 Checkpoint 会在用户提示前捕获由文件编辑工具造成的代码状态，允许回退代码或对话；它非常适合交互式试错，但官方文档说明 Bash 命令造成的文件变化、外部系统变化以及多数后台 Subagent 的编辑并不都在恢复范围内，Checkpoint 也不替代 Git。 LongHorizon-Harness 的运行账本不承诺把世界回滚到旧状态，而是记录失败以后哪些事实仍然可信、哪些要求需要重做，并从最后可信状态继续。一个解决“回到过去”，另一个解决“在无法完整回到过去时怎样继续向前”，这正是桌面应用、服务进程和外部 SaaS 长任务中非常现实的差别。

## LongHorizon-Harness 与 Codex 的区别

Codex 的原生定位同样是完整的工程 Agent，而不只是一个模型调用器。它通过 `AGENTS.md` 分层加载全局、仓库和目录级指令，通过 Memories、Skills 与 MCP 保存项目经验或连接外部系统，并通过 Subagents 把代码探索、测试、日志分析和实现工作分给独立线程。当前 Codex 客户端还允许把多个聊天放到 Git Worktree 中并行运行，使不同分支上的写操作互不干扰；在适合并行的代码库探索和功能开发中，这种机制可以直接提升吞吐量。

`AGENTS.md` 、Skills 和 Memories 让团队无需在每次任务中重复解释构建命令、代码规范、审查要求和领域流程，Subagents 与 Worktrees 则把相对独立的工作并行化，并把大量中间日志隔离在各自线程中。LongHorizon-Harness 不会取代这些机制，因为它维护的 `task_state` 不是一套长期项目规范，也不适合承载所有领域知识；它提供的是某一次长期任务的动态完成状态，其中每一项状态都应该能够追溯到某轮合同与审计证据。 `AGENTS.md` 回答“在这个仓库里永远应该怎样工作”，MEA 状态回答“在这次任务里，哪些要求已经被证明完成”。

Codex 的 Sandbox 与 Approval Policy 也不能和 Auditor 混为一谈。Sandbox 规定 Agent 在技术上可以读取或写入哪些路径、能否访问网络，Approval Policy 规定越过边界或调用有副作用的工具时是否必须停下来请求授权；它们保护的是执行前的能力边界与风险边界。Auditor 处理的是执行后的事实边界：即使某条命令完全在 Sandbox 内合法运行，也不代表它达到了任务目标；相反，即使 Auditor 确认结果正确，它也没有权力扩大 Executor 的写权限。把 Codex 放进 LongHorizon-Harness 后，两层控制是正交叠加的：内层 Sandbox 决定“能不能做”，外层 Audit 决定“做完以后能不能记为完成”。

Codex 也提供了专用 `/review` 流程，由独立 Reviewer 读取选定 Diff 并以只读方式报告优先级明确的发现，因此同样不能说 Codex 缺乏独立审查。区别仍然在于审查是否构成默认提交协议。原生 Review 面向代码改动，可以按分支、提交、工作区或上一轮选择范围；LongHorizon Auditor 面向本轮任务合同，即使代码 Diff 没有明显问题，它仍可能因为服务未启动、文件没有保存到指定位置、GUI 证据缺失或原始硬约束未满足而拒绝完成。只有把测试、Review、Artifact 检查和外部状态共同连接到一个任务账本，审查结果才会从“建议”变成长期编排的控制信号。

Codex Subagents 和 Worktrees 擅长把相对独立的读任务或分支开发并行推进，官方文档也提醒写密集型并行任务会产生冲突与协调成本；LongHorizon-Harness 的核心循环则更偏向串行提交可信状态，每一轮根据上一轮审计结果决定下一项环境转换。它牺牲一部分吞吐量，换取依赖清晰和较低的状态冲突概率。因此，一个大型仓库内三个彼此独立的模块改造更适合先用 Codex Worktrees 或 Subagents 并行，而一个必须“先保存原始证据，再修改生产配置，再验证服务，最后生成报告”的有序任务更适合用 MEA 外层循环。两者可以组合：Codex 在某个边界清楚的 Executor 回合内并行调查，LongHorizon-Harness 仍只在 Auditor 验收后提交该回合的结果。

### 三者的核心能力对比

| 维度 | Claude Code | Codex | LongHorizon-Harness |
| --- | --- | --- | --- |
| 核心定位 | Claude 驱动的通用 Coding Agent 与可扩展 Agent Loop | 面向代码库、终端、云端与本地环境的工程 Agent 平台 | 包裹现有 Agent 的长时任务编排与验证层 |
| 默认工作单元 | 一个可恢复、可分叉的会话或后台任务 | 一个 Chat、Task、Subagent 线程或 Worktree | 一个带合同的 MEA 状态转换轮次 |
| 后续推理的主要依据 | 会话历史、Compaction、 `CLAUDE.md` 、Auto Memory、Subagent 摘要 | 会话上下文、 `AGENTS.md` 、Memories、Skills、Subagent 结果 | 原始任务、可信 `task_state` 、当前合同与相关审计报告 |
| 项目级持久规则 | `CLAUDE.md`  、Rules、Skills、Hooks | `AGENTS.md`  、Skills、Rules、MCP | 通常复用底层 Agent；自身重点不是项目知识管理 |
| 长期任务状态 | 会话、任务列表与记忆可以表达进度 | 会话、Plan、Tasks、Memories 可以表达进度 | 显式 Requirement、Artifact、Fact 与审计状态 |
| 上下文隔离 | Subagent、Fork、后台会话与自动压缩 | Subagents、独立线程、Worktrees | 每个 Executor 与 Auditor 回合默认使用新上下文 |
| 并行能力 | 后台 Subagents、并行会话、Agent Teams | Subagents 与 Git Worktrees | 主要强调跨轮串行验证；可复用底层 Agent 的局部并行 |
| 原生验证 | 测试循环、Hooks、独立 `/code-review` | 测试循环、独立 `/review` 、GitHub Review | 每轮强制只读 Audit，验证范围由合同而不是仅由 Diff 决定 |
| 谁能宣布完成 | 当前会话或被调用的审查流程，具体取决于用户工作流 | 当前线程或 Review 工作流，具体取决于用户工作流 | Executor 只能提出声明，Auditor 与 Harness 完成守卫决定是否提交 |
| 权限与安全 | Permission Modes、Rules、Hooks、Checkpoint | OS/云 Sandbox、Approval Policy、网络与工具权限 | 通过角色权限限制 Manager、Executor、Auditor，并继承底层 Agent 安全边界 |
| 恢复重点 | 恢复/分叉会话与回退可跟踪的文件编辑 | 恢复线程、检查 Diff、借助 Git/Worktree 隔离变更 | 从已审计进度继续，即使整个外部环境无法完全回滚 |
| 主要代价 | 长会话上下文、Subagent 与 Review 的额外 Token | 多线程、Worktree、Review 与环境配置成本 | 每轮 Manager 与 Auditor 带来的延迟、Token 和编排成本 |
| 最适合的任务 | 交互式编码、调试、重构、带 Hooks 的团队流程 | 代码库改造、并行工程任务、隔离环境和结构化 Review | 数小时、多界面、强证据依赖、容易错误宣布完成的任务 |

### 如何选择框架？

**如果任务主要发生在一个代码库中，预计几十分钟到一两个小时内完成，验收条件可以用测试、Lint、类型检查和 Diff Review 表达，那么优先直接使用 Claude Code 或 Codex 通常更合理。**

Claude Code 适合重视连续对话、可编程 Hooks、Checkpoint 与 Claude 生态的工作流；Codex 适合重视 Sandbox、Approval、代码审查、Subagents、Worktrees 以及本地与云端工程协同的场景。两者都可以通过项目指令和 Skills 把团队规范固化下来，没有必要为了形式上的“多 Agent”额外引入外层 Harness。

**如果任务会持续许多轮，跨越 GUI、CLI、文档与服务状态，包含不可逆的先后约束，或者历史上经常出现“Agent 说完成但 Benchmark、用户或外部系统并不认可”的问题，那么 LongHorizon-Harness 才开始显示出独特价值。**

此时可以继续选择最合适的 Claude Code 或 Codex 作为 Executor，同时把任务分解、证据准入、失败恢复和完成判定交给 MEA。判断是否值得增加这一层的一个实用标准是：如果你最担心的是 Agent 不会做，应该优先升级模型、工具和项目指令；如果你最担心的是它做了一半却忘了、重复做、破坏前置证据或过早宣布成功，应该优先考虑 LongHorizon-Harness。

对于部署、数据库迁移、财务操作、消息发送或其他高风险外部动作，三者都不应被当作完整的安全证明。MEA 的 LLM Auditor 可能误判，Claude Code 与 Codex 的 Review 也可能漏掉问题；生产系统仍需要确定性测试、策略引擎、最小权限凭证、幂等设计、不可变日志和人工批准。比较三者时，最准确的结论不是“谁更强”，而是它们分别控制不同的失败面：Claude Code 与 Codex 提高单轮执行质量并提供原生安全边界，LongHorizon-Harness 降低跨轮状态腐化与错误完成的概率，确定性验证器和人类则处理不能交给概率模型的最后一道风险。

### LongHorizon-Harness 框架总结

LongHorizon-Harness 提出的不是一个更长的 Prompt，也不是一个新的基础模型，而是一种面向长时 Agent 的 Loop Engineering：把原始目标固定下来，把执行拆成有界的环境状态转换，把局部轨迹限制在当前轮次，把经过独立验证的事实写入持久状态，再从该状态生成下一步。

与 Claude Code、Codex 相比，LongHorizon-Harness 不是另一套更强的代码编辑器或 Tool Loop，而是可以包裹这些原生 Coding Agent 的外层提交协议；Claude Code 和 Codex 负责把局部工作做出来，MEA 负责判断哪些局部结果能够累积为长期可信进度。

\# *学习大模型 & 讨论Kaggle* #

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/uoTGEibAZUEgGtr0ib3fibjtZGGiawJxeZb8NEPR0DibUlaMhD1mD7NiajMfbiaBiarSpbLMkrct2I5dsSVoOnCFD7zElg/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1&tp=webp#imgIndex=5)

△长按添加竞赛小助手

每天大模型、算法竞赛、干货资讯

与 36000+来自竞赛爱好者一起交流~ ![图片](https://mmbiz.qpic.cn/mmbiz_png/uoTGEibAZUEgjVMpibbLcunLvNOo6YlvekSTegqBSKoMSyrUbWVDkq5jNG5Hf3uwt71tAq11staN0STb2VPxa1CA/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1&tp=webp#imgIndex=6)

闪记

复制 LaTeX 公式