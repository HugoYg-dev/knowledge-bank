---
type: "source"
tags:
  - "AI-Agent/coding"
summary: "分析 yetone 维护的本地 LLM 网关 magpie 如何通过路由表、错题本、Seen 3× 硬规则晋升与严格 PR 验收实现全 AI 自动化研发闭环"
sources:
  - "raw/articles/yetone 的魔法：magpie 是怎么让 AI 自己维护项目的.md"
updated: "2026-11-09"
---

# 来源：yetone 的魔法：magpie 是怎么让 AI 自己维护项目的

## 来源信息
- **标题**：yetone 的魔法：magpie 是怎么让 AI 自己维护项目的
- **作者**：@wquguru (X: @wquguru)
- **日期**：2026-10-12
- **原文链接**：https://x.com/wquguru/status/2109650264601117141
- **物理文献**：[[raw/articles/yetone 的魔法：magpie 是怎么让 AI 自己维护项目的.md]]

## 核心要点
- **全 AI 自动化研发的高频产出实证**：[[entities/实体_magpie|magpie]] 作为连接 [[entities/实体_Claude_Code|Claude Code]]、[[entities/实体_Codex|Codex]]、Gemini CLI 等编程 Agent 至任意模型的本地 LLM 网关，在建仓 19 天内产出 2,862 个 commit、合并 383 个社区 PR 并发布 1,204 个版本，证明纯靠 AI 编写、审查、合并和发布的可行性。
- **路由表与错题本双核架构（AGENTS.md + LESSONS.md）**：
  - `AGENTS.md` 充当路由表，不堆砌繁琐规则，只告诉 Agent 面对不同任务时查阅哪份规范文档；
  - `LESSONS.md` 充当错题本（479 行），由 Agent 每晚自动复盘当天 commit 并产出，记录返工、不该合与验证粗糙的教训及具体 commit/issue 凭据。
- **经验沉淀与硬规则晋升机制（Seen 3× 门槛）**：
  - 错题本中每条教训附带出现频次标记（如 `Seen 1×`）；
  - **经验升级纪律**：同一条教训若在 3 个不同日子的复盘中重复出现（Seen 3×），即自动从 `LESSONS.md` 移入 `docs/code-standards.md`，由软性经验升级为每个 PR 审查必须逐条对照的硬规则。
- **自动刹车与收敛治理**：早期 51 小时狂发 294 个 tag 导致 CI 跑不完且 Linux 单测红测被淹没；夜审复盘后确立“打 tag 前 commit 的 CI 必须全绿完，被下一次 push 取消的不算”规则，发版节奏从单日 168 版迅速降速收敛至单日 15~26 版的稳定节奏。
- **三大严苛 PR 验收标准**：
  1. **回退测试（Red check）**：还原旧代码时新写的测试必须确凿挂掉，验证测试真实捕捉了缺陷；
  2. **真实环境实测**：修改厂商接口必须使用真实账号、真实配置与真接口返回实测，未实测不许宣称可用；
  3. **显式声明未跑项（Not run）**：未跑检查必须显式列出而非隐式省略；
  4. **合并防并发**：合并指令携带 `--match-head-commit <sha>`，杜绝审查后并发 push 绕过检查。
- **人机协同分工（Human in the Loop）**：人类守住高价值战略防线（不可推翻既定产品决策、安全拦截闸门、社区诉求倾听）；日常编码、单测、CR、分支合并与版本发布全权由 Agent 自主闭环。人类只需在 commit 中提供一两句原话吐槽，Agent 自主补齐测试用例与实现代码。

## 关联实体与概念
- **关联实体**：[[entities/实体_magpie]]、[[entities/实体_Claude_Code]]、[[entities/实体_Codex]]
- **关联概念**：[[concepts/概念_Loop_Engineering循环工程]]、[[concepts/概念_Harness_Engineering_宿主编排工程]]

---
> 📎 **物理文献**：[[raw/articles/yetone 的魔法：magpie 是怎么让 AI 自己维护项目的.md]]
