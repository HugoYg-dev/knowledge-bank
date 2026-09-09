---
type: "source"
tags: ["AI-Agent/tool-calling", "AI-Agent/UI"]
summary: "Google Chrome 与 Edge 团队推出的 WebMCP 协议解析：将网站能力以类型化工具直接暴露给 Agent，对比六种 Agent 应用交互范式"
sources: ["raw/articles/2026-08-31_WebMCP-by-Google,-clearly-explained!_1a0580f9aa7f67f1.md"]
updated: "2026-09-09"
---

# 来源摘要：WebMCP by Google, clearly explained!

## 来源信息

- **标题**: WebMCP by Google, clearly explained!
- **来源**: Daily Dose of DS (Avi Chawla)
- **原邮件主题**: WebMCP By Google, Clearly Explained!
- **日期**: 2026-08-31
- **邮件/文章 ID**: `1a0580f9aa7f67f1:2`
- **官方文档参考**: [https://developer.chrome.com/docs/ai/webmcp](https://developer.chrome.com/docs/ai/webmcp)

---

## 核心要点

1. **GUI 像素视觉交互的脆弱性**：传统 Computer Use 范式通过网页截图让多模态模型定位按钮并模拟点击，不仅运行缓慢、消耗大量 Token，且在网页改版或响应式布局调整时极易崩溃失效。本质原因是网页排版针对人类设计而非程序。
2. **WebMCP 浏览器原生工具暴露机制**：由 Google Chrome 与 Edge 团队主导的浏览器 API，允许前端网站在客户端通过 JavaScript 或标准 HTML 表单显式声明支持的动作、功能语义描述及参数 JSON Schema。
3. **Agent 触达应用的六种方式阶梯**：
   - 原始 API（Raw API）
   - 后端 MCP 服务器（Backend MCP Server）
   - 视觉屏幕操作（Computer Use）
   - 网页自动化（Browser Automation / DOM 解析）
   - WebMCP 浏览器原生声明
   - 站点内置专属助理（Site's Built-in Assistant）
4. **WebMCP 的三大核心权衡突破**：
   - **零配置与模型自主权（Bring Your Own Agent）**：用户无需配置 API Key 或部署本地中间代理服务，即可携带自己的 Agent 访问网页。
   - **天然用户会话绑定与免密执行**：工具在用户已打开的标签页会话上下文中运行，天然继承当前登录态 Cookie 与权限，无需向 Agent 暴露凭证。
   - **随状态动态暴露与界面可见性**：根据用户登录状态动态呈现工具（未登录仅暴露搜索，登录后追加购物车与结算），且所有动作在用户眼前 DOM 中实时响应呈现。
5. **两种声明接入形态**：
   - **JS 原生注册**：调用 `document.modelContext.registerTool({...})`，提供 tool name、description、inputSchema 以及执行回调 `execute()`。
   - **声明式 HTML 表单扩展**：仅需在现有 `<form>` 标签上添加 `toolname="..."` 与 `tooldescription="..."` 属性，浏览器即可自动反向解析构建参数 Schema。

---

## 关键技术对比：Agent 触达应用的六种范式

| 交互范式 | Agent 归属 | 用户前置配置要求 | 输入保真度与执行方式 | 核心局限与权衡代价 |
| :--- | :--- | :--- | :--- | :--- |
| **1. 原始 API (Raw API)** | 用户 Agent | 高（需申请并配置 API Key，人工梳理 Endpoint） | 结构化强类型请求 | 脱离网页交互界面，缺少实时上下文状态 |
| **2. 后端 MCP Server** | 用户 Agent | 中（需部署或挂载 MCP 进程与端点） | 规范化工具 Schema | 依然跳过前端 UI，难以复用当前浏览器已登录会话 |
| **3. Computer Use** | 用户 Agent | 无（开箱即用） | 纯像素截屏与坐标猜测 | 极慢、Token 开销巨大、UI 改版极易静默出错 |
| **4. 浏览器自动化** | 用户 Agent | 低/中（依赖 DOM 解析脚本） | 解析通用 HTML 节点树 | 面对混淆 class/div 需复杂语义猜测，容错率低 |
| **5. WebMCP** | 用户 Agent | **零配置**（浏览器级原生握手） | **强类型 JSON Schema + 原生会话执行** | 目前处于浏览器早期标准试用期（Chrome/Edge Canary） |
| **6. 站点内置助理** | 网站锁定 | 无（直接聊天） | 厂商内部集成 | 厂商锁定，用户无法携带私有 Agent，上下文无法跨站复利 |

---

## 关联实体与概念

- 关联概念：[[concepts/概念_WebMCP|概念_WebMCP]]、[[concepts/概念_MCP协议|概念_MCP协议]]、[[concepts/概念_Agent_Skills元工具架构|概念_Agent_Skills元工具架构]]、[[concepts/概念_MCP代码执行模式|概念_MCP代码执行模式]]

---

> 📎 **物理文献**：[[raw/articles/2026-08-31_WebMCP-by-Google,-clearly-explained!_1a0580f9aa7f67f1.md]]
