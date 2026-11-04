---
type: "entity"
tags: ["LLM/inference", "AI-Agent/tool-calling"]
summary: "阿里云开源的运行在本地的 Agent 智能路由器，支持多场景路由计划、System One 三问决策、缓存感知与自适应信任度调整"
sources:
  - "wiki/sources/便宜的模型越来越多，怎么判断它能不能胜任我的 Agent 工作.md"
updated: "2026-11-04"
---

# 实体：HiRoute

## 基本信息

- **项目定位**：运行在开发者本地的 Agent 智能路由器与任务调度器
- **主导团队**：阿里云 AgentCore 团队（澄潭等发起）
- **开源代码库**：[higress-group/HiRoute](https://github.com/higress-group/HiRoute)
- **官网**：[hiroute.ai](https://hiroute.ai/)
- **平台支持**：支持 macOS（桌面 App）、Windows（免管理员权限、无需 Python 环境安装）、Linux（x86_64 / ARM64，Web 控制台网络监听）

---

## 核心架构与功能特性

### 1. 场景化路由计划（Routing Plans）
- 允许用户为不同工作场景（如工程开发、调研搜集、架构决策）创建独立路由计划；
- 每份计划独立配置经济模型组（如 Qwen Flash）、主力模型组（如 Qwen Max）、思考档位、信任度与专用决策模型（可直连阿里云百炼等服务）；
- Agent 客户端无需修改模型名或配置，统一请求本地 HiRoute 网关，实现无缝透明接入。

### 2. 轮内模型锁定与前缀缓存协同（Cache-Friendly Scheduling）
- 针对 Agent 任务连续多次调用模型的特征，严格落实**“一轮任务内锁定模型不变”**的工程纪律；
- 仅在用户发送新消息、上下文发生压缩或重构时重新进行模型选择，确保单轮内的连续交互能够高度命中服务商的前缀缓存（Prefix Cache），实测缓存命中率接近 90%，大幅降低 Token 总花销。

### 3. System One 三问拆解与程序化裁决
- 彻底摒弃由单一大模型主观做出复合选组决定的不稳定做法，提出“让模型回答问题，让程序做决定”的架构范式；
- 将单次路由请求拆解为三个正交的轻量问题：
  1. **上一步做得怎么样？**（评估胜任度评分）；
  2. **这一步有多难？**（输出步骤难度与简单概率）；
  3. **上一步的问题会不会带到这一步？**（评估已知错误在当前步的延续性）；
- 本地程序根据预设阈值（信任度指标）进行硬逻辑裁决，消除了模型本身的激进或保守偏差，决策耗时仅 0.5–1 秒，准确率达到 88%–100%。

### 4. 表现可观测性与统计驱动的自适应放手
- 持续收集用户反馈（以用户下一条输入的肯定/否定作为真实证据）并生成模型表现报告；
- 设定非对称调整策略：
  - **建议多放手**：至少累积 30 个评分步、覆盖 ≥3 个会话、打分步骤占比 ≥60% 且胜任率 ≥85%；
  - **建议收回**：至少 30 个步骤中达标率低于 70% 时及时告警收回；
- 支持利用本地历史真实会话日志执行离线回放（Offline Replay），预演阈值变更带来的换模影响。

### 5. Super Agent 式任务路由（Task Routing）
- 深度融合 Super Agent 架构思想，除底层模型路由外，扩展出顶层任务级调度：
- 将日常使用的 Agent（如 Hermes、OpenCode、OpenClaw）作为常驻 Router 负责任务分派，通过 CLI 指令 `hiroute worker exec --plan <PLAN_ID> --cwd <DIR> --no-wait` 分发给已绑定的专用 Worker（如 Pi、Qoder CLI、Codex CLI）；
- 结合后台异步轮询与 `notify_on_complete` 回调机制，在任务完成后自动唤醒 Router 汇报结果，实现多任务并行与场景解耦。

---

## 关联页面与概念

- **核心概念**：
  - [[concepts/概念_LLM模型路由]]：HiRoute 是模型动态路由与缓存协同工程的典型实践
  - [[concepts/概念_Decision_Model_专用判断模型]]：三问拆解决策依赖轻量专用判断模型
  - [[concepts/概念_Super_Agent_超级智能体]]：支持常驻 Router 与独立 Worker 任务编排
- **同类/关联系统**：
  - [[entities/实体_Jev]]：商业化轻量判断接口
  - [[entities/实体_Codex]] / [[entities/实体_DeepSeek_Harness]]：可被 HiRoute 编排调度的执行宿主
- **来源文献**：
  - [[wiki/sources/便宜的模型越来越多，怎么判断它能不能胜任我的 Agent 工作.md]]
