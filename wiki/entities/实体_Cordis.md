---
type: entity
tags:
- AI-Agent/coding
summary: 支持时空可组合性（Spatiotemporal Composability）的轻量级微内核框架，通过副作用跟踪、撤销条（Disposer）、依赖变动通知与事务性
  HMR 为 DeepSeek Harness 等系统提供进程内带状态组件的生命周期与热替换管理。
sources:
- wiki/sources/刚刚，DeepSeek Harness震撼开源：一切皆插件.md
- wiki/sources/深度剖析 DeepSeek 最新的 Harness DSH：为了自进化这盘醋包了一整盘饺子.md
- wiki/sources/DeepSeek_Harness_插件生态解析.md
updated: '2026-10-13'
---

# 实体：Cordis

## 简介
**Cordis** 是一个支持“时空可组合性（Spatiotemporal Composability）”的现代微内核框架与插件系统。它通过 Context（上下文）、Effect（副作用）与 Fiber 机制，管理服务的生命周期、依赖注入、撤销清场与能力注册，是 [[entities/实体_DeepSeek_Harness|DeepSeek Harness（DSH）]] 等大型复杂智能体系统的底层内核架构。

## 核心机制与设计哲学

1. **命令式插件微内核**：
   - 区别于声明式配置加载模型，Cordis 允许插件直接运行在 Harness 进程内，携带内部状态并通过 Context 注册服务能力，支持跨插件直接函数调用与依赖注入。
2. **副作用跟踪与撤销条管理（Disposers）**：
   - 框架自动记录插件装载时对环境造成的全部改动（事件监听、连接占用、后台任务），在插件卸载或热替换时按序调用撤销函数（Disposer），彻底清理残留，避免悬空引用。
3. **依赖变动响应机制**：
   - 实时监控插件间的依赖拓扑图：当依赖的服务上线时通知启动，服务下线时通知挂起，提供者热替换时通知重新加载与重连。
4. **事务性热模块替换（HMR）与回滚容错**：
   - 在热更新与插件动态替换过程中提供事务性保护。若新插件代码执行报错或依赖解析失败，框架自动回滚至上一个稳定版本，防止系统卡在半加载的中间崩溃态。
5. **Fiber 状态机与工程健壮性**：
   - 核心调度机制（如 `fiber.ts`）系统性处理了并发卸载时的竞态条件、依赖链传播的终止边界以及回滚容错逻辑，为进程内复杂状态的动态替换提供坚实的下限保障。
30	6. **时空可组合性与自指扩展（Self-Referential Extensibility）**：
31	   - 允许上层程序或具备自进化能力的 AI Agent 在受控边界内读取自身插件树与 TypeScript 接口定义，动态装配新工具或动态替换 Agent Loop 控制流。
32	7. **声明式 Patch 与包级生态装配**：
33	   - 在工程落地中（如 DSH），Cordis 支持通过 `cordis.patch.yml` 描述能力注入与依赖边界，与 npm 包管理模型紧密结合，使宿主扩展以声明式补丁织入而非侵入式代码篡改的方式完成装配。
34	
35	## 关联页面
36	- **典型应用**：[[entities/实体_DeepSeek_Harness|DeepSeek Harness]]
37	- **相关概念**：[[concepts/概念_Harness_Engineering_宿主编排工程|Harness Engineering]]、[[concepts/概念_Self_Harness_自主进化宿主系统|Self-Harness]]、[[concepts/概念_Loop_Engineering循环工程|Loop Engineering 循环工程]]
38	- **支撑来源**：
39	  - [[sources/刚刚，DeepSeek Harness震撼开源：一切皆插件|刚刚，DeepSeek Harness震撼开源：一切皆插件]]
40	  - [[sources/深度剖析 DeepSeek 最新的 Harness DSH：为了自进化这盘醋包了一整盘饺子|深度剖析 DeepSeek 最新的 Harness DSH：为了自进化这盘醋包了一整盘饺子]]
41	  - [[sources/DeepSeek_Harness_插件生态解析|DeepSeek Harness 插件生态解析]]
