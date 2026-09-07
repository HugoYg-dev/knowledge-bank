---
type: concept
tags:
- AI-Agent/tool-calling
summary: 利用 MCP Notification 机制实现服务端 Human-in-the-Loop：send_inquiry 工具挂起等待人类答复，HTTP
  接口接收回复，支持多端协同
sources:
- wiki/sources/HumanInTheLoop用MCP实现.md
- wiki/sources/OpenAI_构建AI智能体实用指南.md
- wiki/sources/腾讯ABI工程架构探索与实践.md
updated: '2026-09-07'
---


# 概念_HITL_MCP

Human-in-the-Loop（HITL）通过 MCP 协议实现，使 Agent 在服务端执行时也能向人类发起询问或获取操作授权。

## 核心设计

**send_inquiry 工具**：专用 MCP 工具，接受 prompt 参数（疑问文本）。调用后**同步挂起**，直到人类通过 HTTP 接口回答才返回。此设计保持 MCP 同步调用语义不变。

**ID 传递（凭条机制）**：工具挂起期间，通过 **MCP Notification 帧**将 inquiryId 和问题文本一起发送给调用方；调用方（Agent 平台）将 Notification 帧透传进 ChatCompletions SSE 流；端侧解析后渲染 UI，等待人类输入。

**HTTP 回答接口**：与 MCP Server 同进程提供 HTTP 接口，接受 response 参数；端侧人类作答后调用该接口，send_inquiry 解除挂起，将人类答复作为 tool/call 响应返回给模型。

## 三种人类回答模式

- **直接回答**：多轮单问题（逐步澄清，轮次难控制）或单轮多问题（结构化或 Markdown 富文本编辑器）
- **拒绝回答**：端侧发送固定文本如"人类选择不作答，请自主决策"
- **超时未作答**：端侧计时器触发，发送超时消息；MCP Client 超时 > HITL 服务超时 > 端侧超时

## YOLO 模式

当 HITL 开启但人类无需干预时：
- 客户端代为决策（随机/YOLO/请求外援）
- 另一个"决策 Agent"作为 MCP Server 兜底代替人类作答
- Prompt 约束模型绕过 HITL Server

## 应用场景

- Agent 意图不清晰时主动向用户澄清（替代直接"打在公屏上"）
- 执行危险操作前获取人类授权（配合 [[概念_MCP_Proxy]]）
- 多端协同：任意端作答后其他端自动关闭问询 UI

## 来源

- [[HumanInTheLoop用MCP实现]]
