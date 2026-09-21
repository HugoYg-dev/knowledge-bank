---
type: concept
tags:
- AI-Agent/deep-research
- Infra/platform
- RAG/retrieval
summary: 面向大模型智能体的网络搜索架构与供应链解耦范式，将一体化搜索引擎解构为代理层、定向语义索引、上下文精炼与云端运行时四层，并以代码运行成功率等 Agent
  任务信号替代人类点击。
sources:
- wiki/sources/搜索没有变便宜，但 Agent 把它拆成了新的供应链.md
updated: '2026-09-21'
aliases:
- Agentic Web Search
- 智能体网页搜索
- 智能体网络搜索
- 概念_Agentic_Web_Search
---

# 概念：Agentic Web Search（Agent 网络搜索架构）

## 定义

**Agentic Web Search（面向智能体的网络搜索架构）** 是指在 AI Agent / Deep Research 时代，针对大语言模型（LLM）吞吐 Token 与上下文窗口需求重构的网络检索供应链与技术架构体系。

在传统互联网时代，通用搜索引擎（如 Google、Bing）采用“全网抓取 + 相关性排序 + SERP 广告展示”的垂直一体化黑盒飞轮。而在 Agent 时代，调用主体从人类转变为大模型，交付契约转变为**结构化干净正文、抽样片段与权威 URL 引用**，促使传统搜索 Stack 解耦为可独立采购的模块化层级。

---

## 搜索供应链解耦的四大层级

在 Agentic Web Search 体系中，各供应商通过解耦搜索 Stack 的不同层级形成差异化商业模式：

```
┌────────────────────────────────────────────────────────┐
│  4. 云原生基础设施层 (AWS Bedrock / AgentCore Search)  │ ──> 云端模型运行时与 MCP 连接器
├────────────────────────────────────────────────────────┤
│  3. 上下文精炼与混合检索层 (Tavily)                     │ ──> 网页降噪、正文抽取与 RAG 片段压缩
├────────────────────────────────────────────────────────┤
│  2. 定向语义索引层 (Exa)                               │ ──> GitHub/ArXiv/Wiki 垂类高质量语义检索
├────────────────────────────────────────────────────────┤
│  1. 透传大厂结果的代理层 (Serper)                       │ ──> 包装 Google SERP 原始排序列表
└────────────────────────────────────────────────────────┘
```

1. **代理透传层（SERP Proxy Layer）**：
   - 代表厂商：Serper。
   - 机制：不自建爬虫，不上网抓网页，不构建物理索引，仅以轻量 API 代理透传 Google 等巨头的原始搜索结果列表。
   - 局限：工程实现轻量，但受制于上游巨头接口与策略，长期缺乏自控壁垒。
2. **定向语义索引层（Focused Semantic Indexing Layer）**：
   - 代表厂商：[[entities/实体_Exa|Exa]]。
   - 机制：放弃对抗全网海量低质/垃圾网页的巨大工程开销，优先抓取 GitHub、ArXiv、Wikipedia 与高质量技术博客等高信息密度站点，构建专用语义向量与倒排索引。
   - 特点：在学术、技术与垂类领域检索精度极高，但无法覆盖全网长尾生活通用搜索。
3. **上下文精炼与混合检索层（Context Refinement & RAG Layer）**：
   - 代表厂商：[[entities/实体_Tavily|Tavily]]。
   - 机制：核心卖点在于面向大模型 RAG 需求进行网页降噪、正文抽取、HTML 清洗与文本压缩，直接输出可填入 Context Window 的高密度 Token 片段。
4. **云原生基础设施层（Cloud-Native Runtime Layer）**：
   - 代表厂商：AWS（AgentCore Web Search Tool、Amazon Bedrock Web Search）。
   - 机制：将检索工具直接内嵌在云端大模型 API 运行时（Runtime）与 MCP（Model Context Protocol）连接器中，统一接入云端 IAM 鉴权与计费体系。

---

## 分发渠道与数据闭环的迁移

Agent 时代的搜索不仅是技术 Stack 的解耦，更带来了分发入口与数据反馈飞轮的结构性重构：

### 1. 分发入口重构
- **传统搜索**：由操作系统和浏览器厂商掌控地址栏与默认搜索位（如 Google 每年向分发商支付数百亿美元买断 Safari / Android 默认入口）；
- **Agentic 搜索**：搜索变为 B2B 开发者产品，流量入口迁移至云端模型 API 运行时（Bedrock/SageMaker）、模型 SDK 与 MCP 协议标准，成为开箱即用的默认基础设施组件。

### 2. 排序反馈信号重构
- **传统 NavBoost 系统**：依赖数十亿人类用户的聚合查询、点击（Click）与页面停留时间（Dwell Time）持续校准排序；
- **Agentic 反馈闭环**：依赖智能体在执行多步推理与长程任务时的自动化行为信号——**代码运行成功率、工具调用重试率（Retry Rate）以及引用链接有效性**。

---

## 架构选型与权衡准则

在为智能体系统（如 Deep Research Agent、编码 Agent）选型网络检索方案时，架构师应依据以下维度权衡：

| 选型维度 | 考量重点 | 推荐技术路线 |
| :--- | :--- | :--- |
| **时延与计算成本（COGS）** | 尽量减少中间代理转发与多次 HTML 请求开销 | 云原生内置检索（Bedrock Search）或轻量代理层 |
| **Token 预算与抗噪声** | 避免大段无效 HTML/导航栏挤占上下文窗口 | 上下文精炼层（[[entities/实体_Tavily|Tavily]]） |
| **学术/技术垂类深度** | 需要精准代码片段、论文与专业文档引用 | 定向语义索引层（[[entities/实体_Exa|Exa]]） |
| **隐私合规与数据主权** | 企业内网合规、权限审计与零第三方泄露 | 云原生私有化部署连接器 |

---

## 关联实体与概念
- **代表性实体**：[[entities/实体_Exa|Exa]]、[[entities/实体_Tavily|Tavily]]、[[entities/实体_鸭哥|鸭哥]]
- **核心关联概念**：[[concepts/概念_Harness_Engineering_宿主编排工程|Harness Engineering]]、[[concepts/概念_上下文工程|上下文工程]]、[[concepts/概念_Agent_Skills元工具架构|Agent Skills 元工具架构]]、[[concepts/概念_Agentic_RAG_智能体检索增强生成|Agentic RAG]]

---

## 来源与参考
- [[sources/搜索没有变便宜，但 Agent 把它拆成了新的供应链|搜索没有变便宜，但 Agent 把它拆成了新的供应链]]