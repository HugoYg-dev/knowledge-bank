---
type: entity
tags:
- Infra/AI
- LLM/arch
summary: 专注于通用人工智能（AGI）研发的中国 AI 创新机构，代表作包括 DeepSeek-V3/R1 系列大模型及基于 Cordis 微内核的 DeepSeek-Harness 智能体生态。
sources:
- wiki/sources/DeepSeek AI Infra 一面，面爽了！！！.md
- wiki/sources/DeepSeek Agent开发岗三面，再面一轮就offer啦！！！.md
- wiki/sources/刚刚，DeepSeek Harness震撼开源：一切皆插件.md
- wiki/sources/深度剖析 DeepSeek 最新的 Harness DSH：为了自进化这盘醋包了一整盘饺子.md
updated: "2026-09-07"
---

# 实体：DeepSeek

## 简介

**DeepSeek（深度求索）** 是一家专注于通用人工智能（AGI）底层技术研发与创新的中国 AI 机构。团队坚持长期主义，在基础模型架构创新（如 MLA 多头潜在注意力、DeepSeekMoE、多 Token 预测 MTP）、大规模强化学习（RL）、低成本训练推理工程及智能体基础设施（Agent Infra）等方向取得了行业突破性成果。

## 核心技术栈与代表性成果

### 1. 基础大模型矩阵
- **DeepSeek-V2 / V3**：提出 MLA（Multi-Head Latent Attention）与细粒度专家路由（DeepSeekMoE），显著压缩 KV Cache 并保持极限算力效率，见 [[entities/实体_DeepSeek-V3|DeepSeek-V3]] 与 [[entities/实体_DeepSeek_V2|DeepSeek-V2]]。
- **DeepSeek-R1**：通过大规模强化学习与纯 RL 激励涌现长思维链（Chain of Thought, CoT）推理能力，打破传统过度依赖高成本监督微调（SFT）的路径依赖，见 [[entities/实体_DeepSeek-R1|DeepSeek-R1]]。

### 2. 智能体基础设施（Agent Infra）
- **微内核插件生态**：开源了基于 [[entities/实体_Cordis|Cordis]] 的生产级智能体运行时 [[entities/实体_DeepSeek_Harness|DeepSeek-Harness]]，践行“组合优先（Composition-first）”哲学，将模型适配器、工具注册表、事件流与 Agent Loop 自身完全插件化解耦。
- **分布式协同（Meta-Harness）**：在单实例 Harness 之外，提出 Meta-Harness 概念，负责多智能体实例间的资源调度、负载均衡与跨实例任务编排。
- **模型原生 Agent 化路线**：主张通过后训练（SFT/RL）在模型权重内部原生沉淀工具调用、分层早停、主动追问与边界反思能力，使智能体从“能做事”迈向具备分寸感与自我判断力的“会做人”境界。

### 3. 工程系统设计与安全准则
- **闭环可解释与沙箱控制**：提倡工作区隔离、网络白名单与 cgroup 资源配额的三层工具沙箱；采用 `FailureMemory` 记录操作哈希遏制路径震荡；通过无人值守分级权限与熔断机制构筑安全底盘。
- **小模型与大模型协同**：坚持“小模型筛选信息，大模型处理信息”原则，用 7B 小模型承担上下文压缩与记忆检索重排，大模型聚焦高阶推理。

## 关联实体与概念

- **旗下模型与框架**：
  - [[entities/实体_DeepSeek-V3|DeepSeek-V3]]
  - [[entities/实体_DeepSeek-R1|DeepSeek-R1]]
  - [[entities/实体_DeepSeek_V2|DeepSeek-V2]]
  - [[entities/实体_DeepSeek_Harness|DeepSeek Harness]]
  - [[entities/实体_Cordis|Cordis]]
- **核心概念**：
  - [[concepts/概念_Harness_Engineering|Harness Engineering]]
  - [[concepts/概念_AI-Native_Infra|AI-Native Infra]]
  - [[concepts/概念_Agent工具调用沙箱|Agent工具调用沙箱]]
  - [[concepts/概念_Agent三层记忆体系|Agent三层记忆体系]]
  - [[concepts/概念_Agent完整轨迹评估|Agent完整轨迹评估]]
