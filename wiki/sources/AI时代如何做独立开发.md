---
type: source
tags:
- 创业
summary: 2011 武大核工程本科 → 自学平面设计+网页编程 → 取网名 idoubi 致敬 Adobe。
sources:
- raw/insights/一年上线超 10 款产品，AI 时代如何做独立开发.md
updated: '2026-07-01'
cubox_url: https://cubox.pro/web/card/7348601856957875896
ingested: 2026-06-30
---
# AI 时代如何做独立开发

## 来源信息

- **标题**：一年上线超 10 款产品，AI 时代如何做独立开发
- **作者**：艾逗笔（idoubi）
- **URL**：https://mp.weixin.qq.com/s?__biz=MjM5MDE0Mjc4MA==&mid=2651250699&idx=2&sn=5bbbaf6666be58fba2ce856a0fbf14df


> InfoQ/AICon 大会分享。ThinkAny & MCP.so 创始人艾逗笔（idoubi）讲述一年半独立开发经验：感悟、可复制经验和行业机会。

## 作者背景

- 2011 武大核工程本科 → 自学平面设计+网页编程 → 取网名 idoubi 致敬 Adobe。
- 2015 毕业（雷军毕业典礼演讲）→ 2018 入职腾讯 5 年 → 2023 裸辞自由职业 → 独立开发 AI 应用出海。
- 一年半做十来个项目，基本每月发布一款新产品。

## 代表产品

| 产品 | 上线时间 | 定位 | 成绩 |
|------|----------|------|------|
| ThinkAny | 2024.3 | AI 搜索引擎 | 月访问量大几十万，上过排行榜 |
| ShipAny | 2024 圣诞 | AI 应用开发框架 | 预售 4 小时销售额破 1 万美金 |
| MCP.so | 2024.11 | MCP 应用市场 | 月均百万访问，被 a16z 报告引用 |
| CopyWeb | 2025.2 | AI 网页复刻 | 已跑通 PMF |

## 独立开发感悟

### 1. 天下武功唯快不破
- AI 时代对独立开发者是利好——AI 帮助更快做出产品。基于 AI 热点做新产品时，快就是优势。
- 例：AI 红包封面生成器星巴克写 1 小时上线；AI 搜索引擎一个周末完成 V1。
- **策略：快速上线，先起飞再加油 → 验证用户需求 → 再决定是否继续投入。**

### 2. 快不如精，长期主义
- 兴趣过于广泛、浅尝辄止是最大教训。早期进入 chatbot 客户端/AI 知识库赛道但没坚持，用户口碑流失。
- **跑通 PMF 后应该坚持做下去**。

### 3. 梦想要大，切入要小
- AI 搜索引擎想对标 Perplexity 做通用 → 资源压力大/token 成本高/竞争激烈。
- 投资人建议做垂类（投资人看重竞争格局）。
- **独立开发者从垂直赛道切入**：竞争更小、效果更收敛、粘性更高、更易正反馈。先垂再通，"农村包围城市"。

### 4. 自己造血，打铁还需自身硬
- 资本看重团队和竞争格局，对个人英雄主义存疑。
- 能自己造血就不需资本杠杆，对资本祛魅。
- 晒 MRR 是曝光自己吸引资本注意力的策略之一。

### 5. 流量为王，持续构建影响力
- 社交平台输出内容积累影响力 → 推广/售卖产品的便利。
- **超级个体 / 一人公司**应积极经营社交账号、输出高质量利他内容。

### 6. 做产品最重要的是开心
- 作者 Coding Anywhere（咖啡馆、旅行途中）。

## AI 应用出海可复制经验

### AI 应用开发 SOP
- 技术栈：TypeScript / React / Next.js
- 登录：next-auth / Clerk
- 数据库：Supabase / Neon
- 多语言：i18n / next-intl
- 支付：Stripe / LemonSqueezy / Creem
- 文件存储：S3 / R2
- 部署：Cloudflare / Vercel
- 域名：GoDaddy / Namecheap

### 一小时快速上线
- 方式：熟悉的全栈框架（NextJS/Remix/Nuxt）+ 项目模板（OpenSaaS/saas-starter）或商业模板（ShipAny/ShipFast/MkSaaS）+ UI 组件库（Shadcn/MagicUI/HeroUI）。

### ProductHunt 打榜
- 产品冷启动最快方式。提前提交、设好定时发布、争取被 Featured（邮件或 Twitter 艾特官方）。
- 发布当天通过微信群/朋友圈/社交媒体号召投票，可选买量冲榜。
- 是有效的品牌 PR 手段。

### 程序化 SEO
- **SEO 是成本最低、见效最快的增长手段**。MCP.so 靠此拿到 Google MCP 关键词第一。
- SOP：数据采集清洗 → AI 摘要+结构化内容 → 服务端渲染+清晰网页结构 → 长尾关键词自动构建页面 → 定时更新 sitemap。
- SEO 是长期主义的事。

### AI Wrapper 指南
- "套壳追热点，打造现金流"——短平快适合独立开发者。
- SOP：发现热点（HF Space/Google Trends/GitHub Trending）→ 抢注域名 → Vibe Coding + 代码模板 + AI 能力（Replicate/Fal/OpenRouter）→ SEO+社媒宣传 → 付费订阅+谷歌广告。

## AI 大时代可 all in 的方向

### 1. AI Coding
- 四类产品：Coding Editor（Cursor/Windsurf）/ Coding Copilot（Cline/GitHub Copilot/Augment）/ Coding Agent（Bolt/Lovable/v0）/ Vertical Coding Agent（Same/Wegic/CopyWeb）。
- 独立开发者应避开主战场，从小场景切入。

### 2. Agent
- 最主流 AI 产品形态。Manus 开启新交互范式。
- 大公司做通用（Manus/Genspark/Minimax Agent/扣子空间），小团队做垂直（Lovart 设计/iMean 旅行/ClipClap 营销视频）。
- 用 Agent 形式改造原有 SaaS 产品。

### 3. Agent Infra
- "卖铲子永远是好方向"——Tools/Planning/Memory/Boilerplate/VM Container/Auth/Payment。
- 作者在做：MCP.so（工具）、ShipAny（模板）、K8S 基建（容器）。

### 4. MCP 生态
- **MCP 是 AI 三年来最大的平台型机会**。
- 方向：MCP 服务器（SaaS 以 MCP 形式开放）/ MCP 应用市场（"AI 时代豌豆荚"）/ MCP 服务路由平台（中间商赚差价）/ MCP 消费终端（chatbot/Agent，如 ChatWise/ChatBox/Cherry Studio/DeepChat/LobeChat）。

## 关联概念

- AI独立开发方法论
- [[概念_PMF引擎]]
- [[概念_MCP协议]]

---
> 📎 **物理文献**：[[raw/insights/一年上线超 10 款产品，AI 时代如何做独立开发.md]]