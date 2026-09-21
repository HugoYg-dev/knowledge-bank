---
type: source
tags:
- AI-Agent/tool-calling
- AI-Agent/multi-agent
summary: 阿里云 OpenLM 实践：利用 MCP Notification + HTTP 接口实现服务端 Human-in-the-Loop，含 send_inquiry
  工具、MCP Proxy 代理、YOLO 模式三方案
sources:
- raw/articles/Human In the Loop竟然可以是个MCP_.md
updated: '2026-07-01'
---
## 来源信息

- 标题：Human In the Loop竟然可以是个MCP?
- 作者：彭世昕、亚男、闫科忠（阿里巴巴智能引擎团队）
- URL：https://mp.weixin.qq.com/s/V5cb4HAufxvbNackr8aLVg

## 核心要点

- **HITL（Human-in-the-Loop）定义**：人类监督/参与 Agent 活动的方式，包括：输入、中断、答疑解惑（澄清歧义）、授权批准
- **服务端 HITL 的挑战**：Agent 在远端执行时面临并发、分布式、多端组合拳；LangGraph 类 HITL 节点需要图状态持久化存储与恢复，技术成本高
- **核心方案：send_inquiry MCP 工具**
  - 定义专用 `send_inquiry` MCP 工具，接受 prompt 参数
  - 调用后挂起（同步调用），直到人类通过 HTTP 接口回答才返回
  - 通过 MCP Notification 帧将 inquiry ID（凭条）发给调用方，端侧据此渲染 UI
  - HTTP 接口提供 response 参数实现人类回答
  - 关联机制：用 ID + 哈希表绑定不同 Agent 的疑问与人类答复
- **MCP Proxy 方案（操作确认）**：在每个 MCP Tool 调用前植入确认逻辑
  - 透传 tools/list 请求
  - 代理 tool/call，人类回答"是"则执行原工具，回答"否"则返回 TextContent "人类拒绝执行"
  - 现有 MCP Server 无需改动，接入 Proxy URL 即可
- **YOLO 模式三策略**：
  - 服务端决策：Prompt 约束大模型绕过或关闭 HITL Server
  - 客户端决策：瘦客户端可随机/YOLO（交给模型决策）/超时未回答/请求外援
  - Agent 决策：另一个"决策 Agent"暴露为 MCP Server，作为人类未回答时的兜底
- **超时配置层级**：MCP Client 超时 > HITL 服务超时 > 端侧"超时未作答"触发时间
- **多端协同**：主界面通过 SSE 帧收问询，其他已登录端通过服务端通知机制同步；任意端作答后其他端收到"撤回"通知关闭 UI
- **提示词设计**：需区分"意图澄清"（调用 send_inquiry）和"信息补充"（调用搜索工具），防止 Agent 把所有疑惑都向人类问询
- **工具 Description 动态干预**：QueryString 参数传入 description 实现多租户共享 MCP Server 的动态调整

## 关键引文

> 在普适化的Prompt作用下，当Agent发现需要澄清问题时，虽然会产生"疑问"，但是它会将疑问直接"打在公屏"上：在输出中阐述这个疑问。即使出现在"深度思考"的正文中，大模型也会试图通过既有知识尝试自主回答这个问题。
> 通过在提示词中加入一些轻微的引导，就可以将Agent的"疑问"交给MCP做工具调用。[重点/高亮]

> "人机回路"工具的Description需要事无巨细，且具有极强的普适性描述。这是通用工具的一个无法回避的选择。此类描述虽然可以覆盖大部分场景，但是一旦出现和Agent的主提示词冲突的描述，那么将无法调和：大模型将无法判断哪一个描述更加重要。[重点/高亮]

## 关联

- [[概念_MCP协议]]
- [[概念_MCP_CHS架构]]
- [[概念_MCP六大原语]]
- [[概念_MCP传输方式]]
- [[概念_HITL_MCP_人机协同协议架构]]
- [[概念_MCP_Proxy_代理拦截模式]]
- Agent_TARS
- [[别再误会MCP了辟谣指南]]
- [[MCP五大原语与Web化]]

---
> 📎 **物理文献**：[[raw/articles/Human In the Loop竟然可以是个MCP_.md]]