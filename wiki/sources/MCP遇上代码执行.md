---
type: source
tags:
- AI-Agent/tool-calling
summary: Anthropic 工程博客：将 MCP 工具以代码 API 方式调用，Token 消耗减少 98.7%，并获得隐私保护与状态持久化能力
sources:
- raw/articles/MCP 遇上代码执行：构建更高效率的 AI 智能体 _ 宝玉的分享.md
updated: '2026-07-01'
---
## 来源信息

- **标题**：MCP 遇上代码执行：构建更高效率的 AI 智能体
- **作者**：Adam Jones、Conor Kelly（Anthropic）；译者：宝玉
- **URL**：https://baoyu.io/blog/code-execution-with-mcp（原文：https://www.anthropic.com/engineering/code-execution-with-mcp）

## 核心要点

- 随着 Agent 连接工具数量激增，两大 Token 消耗问题出现：①工具定义撑爆上下文窗口（数千工具 = 几十万 Token 的工具描述）；②中间结果反复"过一遍"模型（如 2h 会议纪要被来回处理两次 = 额外 50,000 Token）
- 核心方案：把 MCP Server 当"代码 API"而非"直接工具"调用——LLM 通过写代码来调用 MCP，而非直接 TOOL CALL
- 实现方式：将所有 MCP Server 的工具生成"文件树"（servers/google-drive/getDocument.ts 等），Agent 通过浏览文件系统按需加载工具定义，而非一次性全量加载
- 效果：Google Drive→Salesforce 示例的 Token 使用量从 150,000 锐减到 2,000，节省 98.7%
- 过滤数据：代码执行环境中可在返回结果前先过滤（如 10,000 行电子表格只返回 5 行 pending 订单），彻底避免中间结果撑爆上下文
- 隐私保护：中间结果默认只停留在执行环境，模型只看到 print/return 的内容；Host 可自动对 PII 进行 Token 化脱敏，真实数据从 Google Sheets 流向 Salesforce 全程不经过模型
- 状态持久化：代码执行可将中间结果写入文件，支持断点续作；Agent 可将有效代码沉淀为可复用"技能"函数（Skills），配合 SKILL.md 描述文件逐步建立高级能力工具箱
- 两种工具发现方式：①文件系统浏览（列出 ./servers/ 目录）；②在 Server 上添加 search_tools 工具，支持按名称搜索并可选择信息详细程度
- 代价：需要安全的代码执行环境（沙盒/资源限制/监控），增加运营开销和安全考量
- Cloudflare 也发布了类似发现，称之为"Code Mode"

## 关键引文

> 简述：以 CodeAgent 的方式，通过代码来调用 tool (MCP tools) [重点/高亮]

## 关联

- [[概念_MCP协议]] — MCP 基础
- [[概念_MCP代码执行模式]] — 本文核心模式
- Agent技能沉淀 — Skills 概念
- [[概念_KV_Cache_键值缓存]] — Token 消耗背景
- [[实体_Anthropic_Research系统]] — 本文作者所在公司
- Cloudflare — 独立发现相同方法

---
> 📎 **物理文献**：[[raw/articles/MCP 遇上代码执行：构建更高效率的 AI 智能体 _ 宝玉的分享.md]]