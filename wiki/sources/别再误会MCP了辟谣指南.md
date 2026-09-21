---
type: source
tags:
- AI-Agent/tool-calling
summary: 阿里云工程师以架构师视角从 SDK 源码和开源项目剖析 MCP 本质：CHS 三组件而非 CS，Server/Client 是模型无关 RPC 中间件，Host
  才是 AI 智能承载者
sources:
- raw/articles/别再误会MCP了！一篇写给AI工程师的硬核“辟谣”指南.md
updated: '2026-07-01'
---
## 来源信息

- **标题**：别再误会MCP了！一篇写给AI工程师的硬核"辟谣"指南
- **作者**：苗刀（阿里云开发者）
- **URL**：https://mp.weixin.qq.com/s?__biz=MzIzOTU0NTQ0MA==&mid=2247553063

## 核心要点

- 核心观点：MCP 是模型无关的可互操作 AI 应用工程协议，Server/Client 与 LLM 智能决策无直接关联
- **最常见误解**：将 MCP 视为"更高级的 Function Calling"，或将架构图误读为 CS（两组件）而非 CHS（三组件）
- **CHS 三组件精确界定**：
  - **Host**：AI 智能唯一承载者——唯一与 LLM 直接交互，负责管理对话上下文、构建 Prompt、解析 LLM 响应；应用的智能水平完全由 Host 的实现质量决定
  - **Server**：确定性能力的执行器——标准 RPC 服务，声明并暴露能力，接收标准化请求返回确定结果，不含任何 AI 逻辑
  - **Client**：无状态协议中间件——位于 Host 和 Server 之间，处理协议握手/会话管理/心跳，将 Host 意图转为 JSON-RPC 请求
- **SDK 源码法证**（基于 @modelcontextprotocol/sdk NodeJS 实现）：Server 构造函数只声明能力并注册请求处理器，初始化握手全程只处理协议元数据，不感知任何自然语言；整个"接收-校验-分发-执行"是机械的 JSON-RPC 路由，不进行任何推理或决策
- **Host 解剖**（CherryStudio 案例）：主进程 MCPService.ts 只做 MCP 通信代理；渲染进程 ApiService.ts 承担 Host 核心 AI 职责（Prompt 构建 + LLM 调用）
- **工程层关键变量**：System Prompt 的约束力（角色定义/禁止规则/工具调用格式规约）+ 工具 description 的信息熵（太宽泛→滥用，太狭隘→模型无法关联用户意图）
- **20个工具单次请求 Token 突破 60K** 是真实生产问题，根因是 Host 将所有工具定义一次性注入上下文
- MCP 的真实价值：解放开发者处理底层通信与工具适配的重复工作，让精力聚焦于提升 Host 的"智能"（提示词工程/模型选择/任务规划）

## 关键引文

> MCP 是一套模型无关的、用于构建可互操作 AI 应用的工程协议，其核心组件 Server/Client 与 LLM 的智能决策并无直接关联。[重点/高亮]

> MCP Server 是一个实现了 MCP 协议的、模型无关的 RPC 服务端……它们是连接 AI 智能（Host）与确定性能力（Server Tools）之间的标准化管道，而不是管道中流淌的"智能"本身。误以为它们与 LLM 有直接关联，就如同误以为 HTTP 协议本身能够理解网页内容一样。[重点/高亮]

> 一个 MCP 应用的最终效果本质上取决于其 Host 的实现水平，尤其是 Prompt 工程的质量和对 LLM 能力的驾驭。MCP 协议本身只提供了一个稳固的工程舞台，而 Host 才是舞台上真正的"主角"。[重点/高亮]

> 在依赖 Prompt 进行意图识别时，工具的 description 字段是 LLM 选择工具的核心依据。描述得太宽泛（如"Handles files"）会导致滥用；太狭隘或充满技术术语则可能导致模型无法将其与用户意图关联。[重点/高亮]

> 这种工程层面的价值，使得开发者能够从繁琐的、非标的底层通信和工具适配工作中解放出来，将全部精力聚焦于真正决定应用成败的核心——提升 Host 的"智能"。[重点/高亮]

## 关联

- [[概念_MCP协议]] — MCP 基础概念
- [[概念_MCP_CHS架构]] — 本文核心：Client-Host-Server 三组件
- MCP与Function_Call对比 — 概念边界
- CherryStudio — 文中解剖的开源 Host 实现案例

---
> 📎 **物理文献**：[[raw/articles/别再误会MCP了！一篇写给AI工程师的硬核“辟谣”指南.md]]