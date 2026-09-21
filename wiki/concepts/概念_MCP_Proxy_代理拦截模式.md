---
type: concept
tags:
- AI-Agent/tool-calling
summary: MCP 代理模式：在每个 tool/call 前植入人类确认逻辑，现有 MCP Server 无需改动，接入 Proxy URL 即可
sources:
- wiki/sources/HumanInTheLoop用MCP实现.md
updated: '2026-09-21'
aliases:
- MCP Proxy
- MCP代理
- MCP代理拦截
- 概念_MCP_Proxy
---

# 概念_MCP_Proxy_代理拦截模式

MCP Proxy 是一种设计模式，在 Agent 调用真实 MCP Server 之前插入一层代理逻辑，实现操作确认（Human-in-the-Loop）而无需修改原有 MCP Server。

## 工作方式

Proxy MCP Server 对外暴露与 Upstream MCP Server 完全相同的工具列表（透传 tools/list），但拦截所有 tool/call 请求：

1. 收到 tool/call → 触发 [[概念_HITL_MCP_人机协同协议架构]] 的确认流程，向人类发送确认请求
2. 人类回答"是/继续" → 转发 tool/call 给 Upstream MCP Server，返回执行结果
3. 人类回答"否" → 直接返回 TextContent "人类拒绝执行"，不调用 Upstream

## 类比

设计模式中的**代理模式（Proxy Pattern）**：被代理方前植入代理逻辑，满足条件则调用被代理方，否则断路。

## 优点

- 现有 MCP Server 零改动
- Agent 无需感知 Proxy 存在，只需替换连接 URL
- 可对部分工具选择性代理（高危操作才确认）

## 局限

- YOLO 模式下无法完全绕过（Proxy 层始终存在）
- 拒绝回答的 TextContent 需要 Agent Prompt 做对应处理

## 来源

- [[HumanInTheLoop用MCP实现]]