---
type: source
tags:
- AI-Agent/deep-research
- Infra/platform
- RAG/retrieval
summary: 深度剖析 Agent 时代 Web Search 供应链解耦与商业逻辑：底层全网抓取与索引重活未变，搜索需求从人看网页转为模型吞吐 Token，催生出代理层、定向语义索引、上下文精炼与云端基础设施四层可售服务。
sources:
- raw/articles/搜索没有变便宜，但 Agent 把它拆成了新的供应链.md
updated: '2026-08-20'
---

# 来源摘要：搜索没有变便宜，但 Agent 把它拆成了新的供应链

## 1. 来源信息
- **标题**：搜索没有变便宜，但 Agent 把它拆成了新的供应链
- **作者**：[[entities/实体_鸭哥|鸭哥]]
- **发布日期**：2026-08-10
- **原文链接**：[yage.ai/share/agentic-web-search-supply-chain-20260810.html](https://yage.ai/share/agentic-web-search-supply-chain-20260810.html)

## 2. 核心要点
1. **全网搜索难度未减，改变的是交付契约与供应链拆分**：做全网搜索引擎依然需要面对高频抓取、防爬对抗、反垃圾网页与秒级新鲜度等高昂硬件与工程沉没成本。Agent 时代到处出现 Web Search API，并非全网搜索变便宜了，而是调用主体从人类变成了大模型，交付契约从“带广告样式的网页列表”变为“模型吞吐的干净 Token 和权威引用”，原本一体化大包干的抓取、召回、解析、压缩被解耦为可单独购买的模块。
2. **搜索 Stack 的四层解耦与商业化模式**：
   - **透传大厂结果的代理层**（如 Serper）：不上网抓取、不自建物理索引，仅通过 API 包装透传 Google 等巨头的原始排序结果；
   - **定向语义索引层**（如 [[entities/实体_Exa|Exa]]）：放弃对抗全网海量垃圾网页，优先抓取 GitHub、ArXiv、Wikipedia 与高质量技术博客等高密度站点建立定向语义索引；
   - **上下文精炼与混合检索层**（如 [[entities/实体_Tavily|Tavily]]）：专注于针对 LLM 的 RAG 需求进行网页降噪、正文抽取与文本压缩，输出高信息密度的片段；
   - **云原生基础设施层**（如 AWS AgentCore Web Search Tool 与 Amazon Bedrock Web Search）：将检索能力直接内嵌在云端模型运行时与 MCP 连接器中。
3. **AWS 进场的两大深层逻辑**：
   - **内部基础设施的二次 B2B 商业化**：包装支撑内部 Alexa+、Amazon Quick、Kiro 的 Amzn-SearchBot 抓取基建，对外输出以分摊固定成本（`[Agent 推断]`：后端共用比例和单位经济为合理战略推断，AWS 官方未公开披露）；
   - **搜索分发渠道向云端模型 API 运行时迁移**：流量入口从 C 端浏览器地址栏（Google 曾年付 260 亿美元买断分发）转移至 Bedrock/SageMaker 的运行时。开发者直接在云端复用 IAM 鉴权与云账单，使得原生 Web Search 成为合规摩擦最小的默认选项。
4. **护城河与数据反馈闭环的重构**：
   - 被绕过的是传统 SERP 页面排版、广告竞价系统与浏览器默认位买断；
   - 依然存在且无法绕过的硬骨头是物理工程约束（抓取带宽与 IP 资源、防爬对抗、版权许可谈判、新鲜度索引与垃圾网站权威度计算）；
   - **新护城河**：分发入口变成了模型 SDK、MCP 协议标准与云 API 运行时；校准排序质量的信号从人类点击停留转变为 Agent 任务的代码运行成功率、工具重试率和引用打开率。
5. **架构师选型方法论**：面对 Agent 联网需求，不可被“人人都能做搜索”的表象误导。纯透传 SERP 代理层面对自建索引与云巨头长期存在确定性劣势；架构师应根据系统对延迟、隐私、COGS 和证据深度的需求，组合采购上下文精炼或独立索引服务。

## 3. 关键架构与机制解析

### 3.1 传统搜索一体化黑盒 vs Agent 时代分层可售
- **旧搜索闭环**：默认入口买断（如 2021 年 Google 分发商 revenue-share 超过 260 亿美元） $\rightarrow$ 获取海量查询 $\rightarrow$ NavBoost 系统利用点击行为反馈持续校准排序 $\rightarrow$ 精准排序变现广告 $\rightarrow$ 支撑庞大抓取团队与硬件基建。垂直一体化导致任何单一步骤都无法独立收回成本。
- **Agent 时代供应链拆分**：大模型无需展示广告与 HTML 渲染，仅需结构化文本与引用源。底层公共 Crawl（Common Crawl）、开源搜索基础设施与云账单直接变现的成熟，促成了抓取、索引、降噪抽取和运行时分发四层的商业解耦。

### 3.2 护城河迁移矩阵
| 维度 | 传统 C 端搜索时代 | Agent 时代 |
| :--- | :--- | :--- |
| **主要分发渠道** | 操作系统与浏览器默认搜索位（Safari/Android） | 模型 SDK、MCP 协议连接器、云模型 API 运行时（Bedrock/SageMaker） |
| **交付物** | 包含广告和样式的 SERP 网页列表 | 干净正文片段、压缩 Token 与权威 URL 引用 |
| **排序优化信号** | 用户查询与点击/停留（NavBoost 反馈机制） | Agent 代码运行成功率、工具重试率、引用链接有效性 |
| **商业变现方式** | 广告展示与竞价点击变现 | API Token 吞吐计费、云服务订阅与 B2B 基础设施用量 |
| **硬核工程壁垒** | 全网爬虫、防爬对抗、反垃圾、广告引擎 | 全网爬虫、防爬对抗、版权谈判、新鲜度、RAG 降噪与抽取深度 |

## 4. 关联实体与概念
- **作者实体**：[[entities/实体_鸭哥|鸭哥]]
- **代表性搜索供应商实体**：[[entities/实体_Exa|Exa]]、[[entities/实体_Tavily|Tavily]]
- **核心概念**：[[concepts/概念_Agentic_Web_Search_智能体网络搜索|Agentic Web Search（Agent 网络搜索供应链）]]
- **相关工程概念**：[[concepts/概念_Harness_Engineering_宿主编排工程|Harness Engineering]]、[[concepts/概念_上下文工程|上下文工程]]、[[concepts/概念_Agent_Skills元工具架构|Agent Skills 元工具架构]]

> 📎 **物理文献**：[[raw/articles/搜索没有变便宜，但 Agent 把它拆成了新的供应链.md]]
