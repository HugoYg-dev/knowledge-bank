---
type: concept
tags:
- AI-Agent/tool-calling
summary: MCP（Model Context Protocol）是 Anthropic 制定的模型无关可互操作 AI 应用工程协议，标准化工具调用格式，将工具层从
  Agent 解耦
sources:
- wiki/sources/AI时代如何做独立开发.md
- wiki/sources/HumanInTheLoop用MCP实现.md
- wiki/sources/MCP五大原语与Web化.md
- wiki/sources/MCP遇上代码执行.md
- wiki/sources/别再误会MCP了辟谣指南.md
- wiki/sources/2026-08-31_WebMCP-by-Google,-clearly-explained!_1a0580f9aa7f67f1.md
updated: '2026-09-09'
---


## 定义

MCP（Model Context Protocol）是一套模型无关的、用于构建可互操作 AI 应用的工程协议，由 Anthropic 制定并开源。其核心目标是通过标准化的工具调用格式，将工具提供方（MCP Server）与 Agent 开发者解耦，让开发者一次开发可对接所有兼容 MCP 的模型。

MCP 本质是建立在 JSON-RPC 2.0 之上的 RPC 协议，支持双向通信和工具可发现性（capability discovery），而不仅是工具调用。

## 诞生背景

前 MCP 时代的三大工程痛点：

1. **开发耦合度高** — 工具代码与 Agent 代码紧耦合，难以复用
2. **工具复用性差** — 同一工具需为不同模型编写不同调用规则
3. **生态碎片化** — 各模型厂商 Function Calling 格式不统一

MCP 以"前后端分离"类比解决上述问题：MCP Server 类比后端 API，Agent（Host）类比前端，两者通过标准协议通信，互不感知对方内部实现。

## 架构：CHS 三组件

MCP 架构是 Client-Host-Server（CHS）三层，而非常见误读的 CS 两层：

| 组件 | 角色 | 是否含 AI 逻辑 |
|------|------|--------------|
| **Host** | AI 智能唯一承载者，管理对话上下文、构建 Prompt、解析 LLM 响应 | 是（核心） |
| **Client** | 无状态协议中间件，处理协议握手/会话管理/心跳，将 Host 意图转为 JSON-RPC 请求 | 否 |
| **Server** | 确定性能力执行器，声明暴露能力，接收标准化请求返回确定结果 | 否 |

**关键结论**：应用的智能水平完全由 Host 的实现质量决定——MCP Server 和 Client 是模型无关的 RPC 管道，不含任何推理或决策逻辑。

## 五大原语

MCP 协议定义了五类原语（Primitive），绝大多数用户只用到 Tool，其余四类鲜被利用：

- **Tool**（模型主动）：最常见的工具调用，由模型决定何时触发确定性动作
- **Prompt**（用户主动）：服务器预设的交互模板，用户主动触发，支持参数补全
- **Resource**（应用主动）：暴露原始内容/数据，客户端可基于此构建 Embedding 做 RAG
- **Sampling**：Server 向 Client 发起"请求补全"调用，实现链式 MCP Server 调用
- **Roots**：MCP 服务向客户端询问当前环境信息，限定操作范围

## 传输方式

| 方式 | 场景 |
|------|------|
| **Stdio** | 本地子进程，同机通信 |
| **SSE（Server-Sent Events）** | 远端 HTTP，单向流式推送 |
| **Streamable HTTP** | Web 化未来方向，可同步返回 JSON 或开启流式通道 |
| **WebMCP（浏览器原生）** | 浏览器客户端原生声明，直接在 DOM/页面会话中暴露 Tools 与 JSON Schema（参见 [[concepts/概念_WebMCP|概念_WebMCP]]） |

## 与 Function Calling 的关系

MCP 不是"更高级的 Function Calling"，两者定位不同：

- **Function Call** — JSON Schema 静态函数调用，适合单一静态场景，与特定模型绑定
- **MCP** — JSON-RPC 动态协议，支持双向通信和能力发现，模型无关，适合复杂多工具场景

从演进视角：Function Call → MCP 解决了协议碎片化和生态孤立问题。

## 生态与工具链

- **代表性 Host**：Claude Desktop、Cursor、VS Code+Cline、CherryStudio
- **远端托管平台**：Cloudflare、Composio、Zapier（通过 SSE 托管 MCP Server）
- **部署模式**：本地 Stdio、远端 SSE、Sidecar（与 Agent 同跑 Docker 容器）

## 工程层关键变量

1. **System Prompt 约束力**：角色定义、禁止规则、工具调用格式规约
2. **工具 description 信息熵**：太宽泛（如"Handles files"）→模型滥用；太狭隘→模型无法关联用户意图
3. **Token 消耗**：20 个工具单次请求可突破 60K Token；数千工具时工具定义本身可占几十万 Token

## 参考来源

- [[别再误会MCP了辟谣指南]] — CHS 架构深度解析（SDK 源码法证）
- [[MCP五大原语与Web化]] — 五大原语权威解读（MCP 联合创建者）
- [[MCP遇上代码执行]] — Token 消耗问题与代码执行模式
- [[wiki/sources/2026-08-31_WebMCP-by-Google,-clearly-explained!_1a0580f9aa7f67f1|WebMCP by Google, clearly explained!]] — 浏览器端原生 WebMCP 标准与六种交互范式对比