---
type: source
tags:
- AI-Agent/coding
- AI-Agent/skill
summary: DeepSeek Harness (dsh) 插件生态全景解析：基于 Cordis 微内核的声明式插件装配、4,349 个仓库生态数据、Top 25 头部效应与四大演化趋势。
sources:
- raw/articles/DeepSeek Harness 插件生态解析.md
updated: '2026-10-13'
---

# 来源摘要：DeepSeek Harness 插件生态解析

## 来源元信息
- **标题**：DeepSeek Harness 插件生态解析
- **作者**：我才是银古
- **发布日期**：2026-10-12
- **原文链接**：https://www.cnblogs.com/znlgis/p/23274216
- **数据来源**：https://github.com/awesome-dsh-plugin/awesome-dsh-plugin

## 核心要点 (Key Takeaways)
1. **“一切皆插件”的微内核工程落地**：[[entities/实体_DeepSeek_Harness|DeepSeek Harness（dsh）]] 将对话区、右侧边栏、设置页、i18n、子 Agent、模型层、工具层全量解耦为独立包。插件具备两副面孔：既能外挂 UI 与工具，也能替换 Agent Loop 与文件系统 Provider 等核心部件。
2. **声明式补丁与 Manifest 设计**：插件通过 npm 包分发，`package.json` 中的 `dsh.bundle.patch`（指向 `cordis.patch.yml`）是唯一的官方身份凭据；依赖 [[entities/实体_Cordis|Cordis]] 框架的能力作用域与运行时声明织入模型；支持多 profile（web GUI、headless、pi-tui、data）按需生效。
3. **生态规模与活跃度画像**：全网累计 4,349 个仓库、4,508 条插件条目、23 个类目。生态处于“供给过剩但活跃度极高”阶段：57% 仓库近 30 天内有提交，头部 100 原生插件 96 个活跃；但呈现极端头部效应，Top 25 占据全网 79.8% 的 Star，中位数仅 2⭐。
4. **真实痛点分布与“借船出海”现象**：Memory（100,218⭐）与 Docs & Rendering（83,320⭐）合计占全站 49% 热度。成熟产品（如 archify、hindsight、OpenViking、WeKnora、BrowserSkill 等）纷纷为 dsh 提供适配子包；在剔除上游集成后，原生插件榜首为 `dsh-web`（8,650⭐）与单包 `dsh-routing-suite`（7,019⭐）。
5. **记忆（Memory）三大分化路线**：零模型本地派（如 `dsh-deja` 基于 BM25，`memsearch` 共享 Markdown）、平台派（hindsight 自动召回学习、OpenViking、ReMe）与上下文工程派（`dsh-context`、`graph-memory`）。
6. **四大演进趋势**：① 右侧边栏演进为二级扩展总线（如 `DSH-better-sidebar` 支持多插件注册 Tab）；② 插件出现横向组合依赖网络；③ 移动端远程审批（飞书/微信卡片推送）成为无人值守后台运行的刚需；④ 娱乐化与轻量化插件大量涌现。
7. **安全与权限边界警示**：安装插件等同于在本地以本机权限运行第三方代码，**工具审批（Tool Approval）机制并不等于插件沙箱隔离**；社区正衍生出 `dsh-plugin-guard`（静态审计/能力锁）与 `dsh-permgate`（细粒度权限网关）等可插拔防御机制。

## 关键技术与机制解析

### 1. DSH 插件规范与 Manifest 核心结构
插件的定义依赖于 `package.json` 中的专属字段：
- `dsh.bundle.patch`：必需字段，指向 `cordis.patch.yml`，声明能力与注入规则；
- `dsh.client.inject`：显式声明要拦截或注入的官方客户端包（如 UI 侧边栏与对话区），定义失败隔离边界；
- `peer` 字段：自定义依赖解析机制，非传统 `peerDependencies`。

> ⚠️ **Semver 预发布版本陷阱**：Node-semver 范围若无显式预发布标签，会静默排除形如 `^0.2.0-rc.2` 的 Harness 预发布版本，导致 `npm install` 报错 `ERESOLVE`，需要通过显式 `||` 分支挂载元组标签解决。

### 2. 插件生态热度结构与上游分层
生态按仓库形态分为两类：
- **原生插件（Native Plugins）**：4,009 个，纯粹为 dsh 设计；
- **上游集成包（Upstream Integrations）**：313 个，成熟产品将 dsh 作为 Agent 生态标配分发渠道之一（如 WeKnora 检索工具、BrowserSkill 浏览器控制）。

## 关联实体与概念
- **关联实体**：[[entities/实体_DeepSeek_Harness|DeepSeek Harness]]、[[entities/实体_Cordis|Cordis]]
- **关联概念**：[[concepts/概念_Harness_Engineering_宿主编排工程|Harness Engineering]]

> 📎 **物理文献**：[[raw/articles/DeepSeek Harness 插件生态解析.md]]
