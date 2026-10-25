---
type: "source"
tags:
  - "AI-Agent/coding"
  - "AI-Agent/UI"
  - "CaseStudy"
  - "创业"
summary: "Every CEO Dan Shipper 深度复盘 OpenAI Codex 产品演化史：从内部多线赛马、Codex Cloud 过早押注云端折戟、本地 Rust 重写 Agent、桌面 App 取消代码编辑器的冒险决定，到成为 ChatGPT 桌面端底座的完整产品故事与模型公司做产品方法论"
sources:
  - "raw/articles/万字复盘 Codex：一个在模型公司如何做产品的「典型」故事.md"
updated: "2026-10-25"
---

# Source: 万字复盘 Codex：一个在模型公司如何做产品的「典型」故事

## 来源信息

- **标题**：万字复盘 Codex：一个在模型公司如何做产品的「典型」故事
- **作者/编译**：Dan Shipper（硅谷 AI 机构 Every 的 CEO）原著，Founder Park 编译整理（基于对 Tibo、Alexander Embiricos、Mia Glaese 等 Codex 核心成员的深入采访）
- **原始链接**：https://mp.weixin.qq.com/s/U1he1wBWS2PKIaTD1LtRlQ ；原文 https://every.to/p/how-codex-happened
- **发布日期**：2026-10-21
- **原始归档**：[[raw/articles/万字复盘 Codex：一个在模型公司如何做产品的「典型」故事.md]]

## 核心要点

1. **内部赛马与多起点合流**：打造 AI 程序员是 [[entities/实体_OpenAI|OpenAI]] 的长期目标——第一代 Codex 发布于 2021 年（在公开代码上微调的 GPT-3，曾为初代 GitHub Copilot 供能），而真正让编程重回最高优先级的是 o1 推理模型（2024-09 预览）：编程存在「改代码—跑代码—秒级验证」闭环，是推理模型获益最大的领域。管理层随后让多个团队并行探索编程 Agent，2025 年初这些路线（含 Alexander Embiricos 的人机协作构想、Tibo（Thibault Sottiaux）在 OpenAI Monorepo 上训练内部编程 Agent 的「自举」（bootstrapping）实践——让 Agent 反哺研究员搭下一代模型的研发基础设施）与 Scientist Assistant 项目合并，形成产品（Embiricos）+ 工程（Tibo，前 [[entities/实体_DeepMind|DeepMind]]）+ 研究（Mia Glaese，曾参与 [[entities/实体_Gemini|Gemini]] 与对齐）的跨学科完整团队。
2. **2025 年过早押注云端 Agent 的失败**：2025-02-24 [[entities/实体_Anthropic|Anthropic]] 发布 Claude 3.7 Sonnet 并同步推出 [[entities/实体_Claude_Code|Claude Code]] 研究预览（终端、本地、无内置编辑器），开发者迅速接受；而 Codex 团队却用约七周开发并于 2025-05-16 发布云端异步产品 **Codex Cloud**（ChatGPT 侧边栏发起任务，代码库复制到隔离云机执行，返回摘要+diff+PR 按钮）。它在 OpenAI 内部「非常成功」，外部却找不到 PMF：开发者需花数小时在云端重建本机的软件/凭证/权限配置、无法中途打断纠正、追问一句提示词都会重启全新云机，且「发布得太早了，当时的模型还不够聪明」。内部标准化的开发环境掩盖了外部配置成本，恰恰误导了团队；工程负责人随后跳槽当时估值 90 亿美元的 [[entities/实体_Cursor|Cursor]]，据报道 OpenAI 曾达成的 30 亿美元收购 Windsurf 协议也在 7 月告吹。值得注意的是，OpenAI 曾在 2025-04-16 发布过酷似 Claude Code 的开源 Codex CLI，但那只是两人支线项目，早期只能跑 o4-mini 通用模型，最好的模型与团队注意力都在云端。
3. **转向本地与底层 Agent 重写**：2025 年暮春起，Tibo 接手工程经理并「大幅改变方向」转向本地。他没有急着给 CLI 堆功能，而是用 Rust 彻底重写底层 Agent，并将其与终端界面解耦——同一套 Agent 引擎此后可进入 CLI、编辑器扩展、桌面/移动 App、云端乃至 ChatGPT 本身。与此同时 Michelle Pokrass（曾负责 GPT-4.1 研究）主导 GPT-5 后训练：团队坐在程序员身边观察工作、把模型崩溃点转化为可重复训练任务，使 GPT-5（2025-08 底发布）形成理解大型代码库模块咬合、能解释计划、越权前先询问的谨慎编程风格。GPT-5 发布后 Codex 推出面向 VS Code 与 Cursor 的扩展，到 2025-10 使用量增长超十倍，编辑器扩展超过终端成为最主要入口，「一个开始自行运转的飞轮形成了」。
4. **桌面 App 取消代码编辑器的冒险决定**：团队判断人们很快会同时运行多个 Agent 并长时间沉浸其中，诞生于 1970 年代的纯文本终端难以承载，于是投入原生桌面 App。设计师 Andrew Ambrosino 称 Codex App「从聊天产品获得的灵感，比从 VS Code 获得的更多」：侧边栏按项目组织任务、每项任务对应一段与 Agent 的独立对话、多个 Agent 各自在独立代码副本上并行工作互不覆盖。最冒险的决定是**不内置代码编辑器**——所有代码修改必须交给 Agent，以避免做成功能不完整的 VS Code：「用 Agent 写代码的体验必须足够好，好到开发者不会想念编辑器」。2025-11 Google 发布基于 VS Code 的 Antigravity（Agent+完整编辑器）一度让团队动摇，且当时专属 Codex 模型（2025-09 推出）到 11 月仍撑不起桌面产品。
5. **模型足够强，很多问题就不是问题了**：Codex 专属模型线与 ChatGPT 主模型分开，使团队可以快速迭代而不必担心影响 8 亿 ChatGPT 用户——2025-11-19 GPT-5.1 Codex Max 可一次连续写几小时代码；2025-12-18 GPT-5.2 Codex 提升大型代码库跨文件修改能力；Mia Glaese 与产品团队直接协作，把开发者反馈到模型改进的循环缩到最短，研究专注真实工作表现而非 Benchmark 跑分。到 2025-12 越来越多团队成员用 Codex App 取代编辑器；那个圣诞假期成为行业分水岭——开发者用 Anthropic Opus 4.5 与 OpenAI GPT-5.2 端到端构建完整应用、全程零手写代码。2026-02 Codex 桌面 App 在 OpenAI 内部广泛采用（Noam Brown「完全切换」、Greg Brockman 弃用旧工作流、Sam Altman 称其为内部「有史以来最受喜爱的产品」）。
6. **从边角项目到 ChatGPT 底座**：2026-02-02 Codex macOS 桌面 App 公开发布（更像聊天应用而非 IDE），几天后 GPT-5.3 Codex 发布——模型训练第一次不再只围绕编程，开始思考编程 Agent 服务各类知识工作；2026-03-19 Codex 周用户超 200 万（年初以来使用量增五倍），2026-04 加入应用内浏览器与跨 Mac 应用操作，2026-06 周用户超 500 万（约五分之一为知识工作者），2026-07-09 桌面 App 正式并入成为新的 ChatGPT 桌面 App（底层 bundle id 仍是 com.openai.codex）。「Codex Cloud 当初是 ChatGPT 里的一个标签页。现在，ChatGPT 运行在 Codex 之上。」下一步团队将转向异步、重新托管到云端——回到 2025 年春天失败的那个愿景。
7. **模型公司做产品的方法论沉淀（Christensen 创新者窘境视角）**：Alexander Embiricos 白板上的四条增长曲线（Cloud 短暂冲高躺平 → GPT-5 后的 CLI 陡峭爬升 → 更高的编辑器扩展 → GPT-5.3 Codex+桌面 App 让前者相形见绌）复刻了《创新者的窘境》的图景：模型能力每一次跃迁都撑破原有交互界面、催生全新产品形态，而乘上一条制胜曲线的团队几乎从没能站上下一条。Codex 团队避开该命运的两个原因：一是 OpenAI 允许内部多团队像「创业公司组合」一样并行探索再合并，且 Codex 获准在 ChatGPT 主线体量束缚之外独立迭代产品与模型线；二是「用 AI 开发 AI」改变了研发物理规律——团队用 Codex 开发 Codex，几个人几周内就能做出新产品入口。此外，开发者态度的迁移同样剧烈：DHH 从 2025 年 GPT-5 发布前后的「我不会让它替我掌控代码」，到 2026-01 承认 AI Agent「完全有能力为真实代码库贡献生产级代码」，再到 2026-09 Rails World 宣布自己的公司将不再手写代码。

## 关键引文

> 「从某种意义上说，OpenAI 是在押注一系列创业公司，只不过它们全都在公司内部。」——Sam Altman（2025 年接受 Ben Thompson 采访）`[内部赛马机制]`
>
> 「如果把时间拉到未来，正确的产品形态应该是一个待在云端、拥有自己笔记本电脑的 AI。」——Greg Brockman `[云端终局信念]`
>
> Codex App「从聊天产品获得的灵感，比从 VS Code 获得的更多。」——Andrew Ambrosino `[界面形态选择]`
>
> 「用 Agent 写代码的体验必须足够好，好到开发者不会想念编辑器。」`[取消代码编辑器的原则]`
>
> 「Codex Cloud 当初是 ChatGPT 里的一个标签页。现在，ChatGPT 运行在 Codex 之上。」`[产品地位反转]`

## 关联

- [[entities/实体_Codex]] — 本文绝对主角，完整产品演化史（Cloud 折戟→本地重写→桌面 App→ChatGPT 底座）的记述对象
- [[entities/实体_Claude_Code]] — Codex 全程追赶与对标的产品基准，本地终端形态的先行者
- [[entities/实体_OpenAI]] — 内部多线赛马机制、跨学科团队组织与「用 AI 开发 AI」的母体公司
- [[entities/实体_GPT系列]] — GPT-5 后训练（真实编程实战化）与 GPT-5.1/5.2/5.3 Codex 专属模型线的演进
- [[entities/实体_Cursor]] — Codex Cloud 折戟后工程负责人的去向、编辑器扩展的分发平台之一
- [[concepts/概念_RSI递归自我改进]] — Tibo 团队「自举」实践（Agent 反哺模型研发基础设施）的工业级案例

---
> 📎 **物理文献**：[[raw/articles/万字复盘 Codex：一个在模型公司如何做产品的「典型」故事.md]]
