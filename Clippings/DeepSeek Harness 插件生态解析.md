---
title: "DeepSeek Harness 插件生态解析"
source: "https://www.cnblogs.com/znlgis/p/23274216"
author:
  - "[[我才是银古]]"
published: 2026-10-12
created: 2026-10-12
description: "插件是 dsh 的唯一扩展面：模型、工具、沙箱、会话存储、UI，甚至 agent loop 本身都能替换 一个插件 = 一个在 package.json 里声明 dsh.bundle.patch 的 npm 包，dsh plugin add 即可安装，底层跑在 Cordis + Schemaster"
tags:
  - "clippings"
---
- **插件是 dsh 的唯一扩展面** ：模型、工具、沙箱、会话存储、UI，甚至 agent loop 本身都能替换
- 一个插件 = 一个在 `package.json` 里声明 `dsh.bundle.patch` 的 npm 包， `dsh plugin add` 即可安装，底层跑在 **Cordis + Schemastery** 上
- 生态共 4,349 个仓库 / 23 类目， **57% 近 30 天有提交** ，头部 100 个原生插件里 96 个活跃
- star 极度头部化： **Top 25 占全站 79.8% 的 star** ，而 903 个仓库一个 star 都没有
- 类目热度： **Memory（100,218⭐）+ Docs & Rendering（83,320⭐）合计吃掉全站 49%** ；反过来 WSL 互操作 77 个插件只有 160⭐
- 三个正在成型的趋势： **侧边栏变成扩展总线** 、 **插件开始依赖插件** 、 **手机远程审批成为刚需**

---

## 一、dsh 插件到底是什么

DeepSeek Harness（ `dsh` ）是 DeepSeek 开源的 agent harness —— 一个能直接跑的 coding agent，有 Web GUI 和 headless 两种形态。它的框架前提是： **一切皆插件** 。

这句不是宣传语，是字面意思。从一次真实抓取的 peer 依赖就能看出官方把系统切成了什么粒度：

```
@deepseek-ai/dsh-agent        @deepseek-ai/dsh-llm         @deepseek-ai/dsh-tools
@deepseek-ai/dsh-session      @deepseek-ai/dsh-settings    @deepseek-ai/dsh-subagent
@deepseek-ai/dsh-host-webserver  @deepseek-ai/dsh-invariants
@deepseek-ai/dsh-client-ui-slots     @deepseek-ai/dsh-client-ui-sidebar-right
@deepseek-ai/dsh-client-ui-conversation  @deepseek-ai/dsh-client-ui-settings
@deepseek-ai/dsh-client-locale  @deepseek-ai/dsh-client-modules  @deepseek-ai/dsh-client-runtime
```

对话区、右侧边栏、设置页、i18n、子 agent、模型层、工具层 —— **每一块都是独立可替换的包** 。插件因此有两副面孔：

1. **扩展官方 agent** —— 往侧边栏塞一个 tab，注册几个工具，加一个皮肤
2. **替换核心部件** —— 换掉文件系统 provider、换掉 agent loop、组装出一个完全不同的东西

第二副面孔才是"一切皆插件"真正的分量。

### 安装与分发

```sh
dsh plugin add <name>
dsh plugin --profile web add dsh-market     # 装进 web profile
```

注意 `--profile` —— dsh 支持多套运行配置。Web GUI、headless、第三方 TUI（ `dsh --profile pi-tui` ）、甚至专门给数据集做剖析的 `--profile data` 都是不同 profile。插件可以只针对某一个 profile 生效。

分发走 **npm** ：只要包发上 npm，下载量会被自动采集展示，作者不需要额外声明任何字段。没发 npm 也能装，只是没有下载数字。

## 二、一个真实 manifest 里的五个设计决定

这是榜单第 16 名 `omdsh-dev/DSH-better-sidebar` （4,118⭐）的 `package.json` ，去掉噪音后长这样：

```
{
  "name": "dsh-better-sidebar",
  "version": "0.25.0",
  "peer": {
    "@deepseek-ai/cordis": "^4.0.4",
    "@deepseek-ai/dsh-agent": "^0.2.0-rc.2",
    "@deepseek-ai/dsh-client-ui-sidebar-right": "^0.2.0-rc.2",
    "@deepseek-ai/dsh-client-ui-slots": "^0.2.0-rc.2",
    "@deepseek-ai/dsh-tools": "^0.2.0-rc.2",
    "@huanlin/dsh-plugin-better-locale": "^0.1.0",   // ← 注意这个
    "react": "^18.2.0"
  },
  "dsh": {
    "bundle": { "patch": "./cordis.patch.yml" },       // ← 必需，唯一的硬门槛
    "client": {
      "inject": [
        "@deepseek-ai/dsh-client-locale",
        "@deepseek-ai/dsh-client-ui-slots",
        "@deepseek-ai/dsh-client-ui-conversation",
        "@deepseek-ai/dsh-client-ui-sidebar-right",
        "@deepseek-ai/dsh-client-modules"
      ],
      "platform": "web"
    },
    "manifestVersion": 1
  }
}
```

五个值得说的点：

**1\. `dsh.bundle.patch` 是唯一的身份凭证。** 官方 CI 会去仓库的 `package.json` 找它 —— 根包或 `packages/` · `plugins/` · `apps/` 子包里声明都算。只声明 `dsh.client` （即只做一个客户端） **不算插件** 。

**2\. 它指向一个 `cordis.patch.yml` 。** 也就是说插件的装配是 **声明式的补丁描述** ，不是 `require()` 一堆代码进去跑。这是 Cordis 框架的路数：能力、作用域、依赖关系写在配置里，运行时按声明织入。

**3\. `client.inject` 显式列出要注入哪些官方 UI 包。** 这行等于告诉宿主"我要改侧边栏和对话区"，同时给了不匹配时的失败边界。

**4\. peer 依赖写在 `peer` 字段而不是标准的 `peerDependencies`** —— 说明 dsh 有自己的依赖解析路径，不是照搬 npm 语义。

**5\. 也是最有意思的：这个插件依赖了另一个第三方插件** `@huanlin/dsh-plugin-better-locale` 。插件之间已经开始互相组合了，不是各自对官方 API 的单星拓扑。

### 一个真实的坑：semver 预发布范围

dsh 官方本身还在 rc 阶段（ `^0.2.0-rc.2` ），于是有个会静默炸掉的陷阱：

> **不带显式预发布分支的 peer 范围，会静默排除 harness 的所有预发布构建。** node-semver 只有在范围里存在某个比较符与目标版本的 `major.minor.patch` 元组完全一致、且自身也带预发布标签时，才放行预发布版本。

所以看起来很宽的 `>=0.0.1-rc.1 <0.2.0` ，甚至号称"全匹配"的 `>=0.0.0-0 <0.2.0-0` ，都 **匹配不到 `0.1.0-rc.6`** 。用户 `npm install` 时撞上 `ERESOLVE` ，还完全看不出是自己的版本范围写错了。正确写法是显式加一条 `||` 分支，把预发布标签挂到匹配的元组上。

这是那种只有踩过才写得进文档的细节 —— 也侧面说明 dsh 的插件量不是靠降低门槛堆出来的，工程约束是实打实的。

## 三、生态的体量与形状

4,349 个仓库、4,508 条插件条目（476 条指向 monorepo 子包）、23 个类目。按 star 分：

| 区间 | 数量 | 占比 |
| --- | --- | --- |
| ≥ 1000⭐ | 37 | 0.9% |
| 100 – 999 | 140 | 3.2% |
| 10 – 99 | 555 | 12.8% |
| 1 – 9 | 2,692 | 62.2% |
| 0 | 903 | 20.9% |

**中位数 2⭐，P90 是 20⭐，P99 才 687⭐。** 全站 373,850 star 里， **Top 25 就占了 79.8%** 。

但另一面同样重要： **2,478 / 4,327 个仓库（57%）在最近 30 天有提交** ，头部 100 个原生插件里 96 个活跃。这不是一个"发完就死"的坟场，而是一个供给过剩、注意力稀缺的早期生态 —— 门槛极低（一个 manifest 加一次 `dsh plugin add` ），需求端远没跟上供给端。

## 四、热度 Top 25，以及它的口径陷阱

先给原始榜（按母仓库 star）：

| # | 插件 | ⭐ | 类目 | 一句话 |
| --- | --- | --- | --- | --- |
| 1 | tt-a1i/archify | 82,270 | Docs & Rendering | 生成经验证的交互式架构/流程/时序/数据流图 |
| 2 | vectorize-io/hindsight | 48,581 | Memory | 会自己学习的长期项目记忆，自动 recall + retain |
| 3 | volcengine/OpenViking | 39,715 | Memory | 记忆与上下文套件：pre-step 自动召回 + profile |
| 4 | Tencent/WeKnora | 33,371 | Tools | WeKnora 知识库的 4 个只读检索工具 |
| 5 | Tencent/BrowserSkill | 8,690 | Browser & Web | 从 dsh 控制可见的 Chrome/Edge Agent 窗口 |
| 6 | zhu1090093659/dsh-web | 8,650 | UI | Web GUI 增强 monorepo（看板等多个子包） |
| 7 | yjh051108/dsh-routing-suite | 7,019 | Dev & Runtime | 插件运行时注入器：注入/热重载/卸载/提升 dev 工具 |
| 8 | loopx-project/loopx | 6,251 | Workflow | 长时程 agent 的 provider 无关本地状态内核 |
| 9 | dsh-market/dsh-market | 6,217 | Plugin Markets | 内置插件市场：搜索、分类、一键装与升级、换主题 |
| 10 | Q00/ouroboros | 6,205 | Workflow | 纯配置 bundle，经 MCP 暴露 36 个工具 |
| 11 | superdesigndev/treg | 5,000 | Tools | 按任务检索约 2,600 个外部 API 端点，含参数与单价 |
| 12 | YuJunZhiXue/dsh-purge | 4,717 | Identity | 设置卡编辑 `prompt-inject.md` 、管理 AGENTS.md 规则集 |
| 13 | MeteorNOX/DeepSeek-Balance-Whale-Widget | 4,539 | UI | 角落鲸鱼挂件：余额、当日用量、单轮成本、峰谷价 |
| 14 | ccch1mneyyy/dsh-TUI | 4,309 | UI | Claude Code 风格全屏终端 UI，像素鲸页眉 |
| 15 | liustack/modlens | 4,214 | Vision | 给纯文本模型补视觉：贴图出结构化 JSON（OCR/版式/语义） |
| 16 | omdsh-dev/DSH-better-sidebar | 4,118 | UI | 侧边栏工作台：文件、终端、Git、子 agent，第三方插件可注册 tab |
| 17 | strukto-ai/mirage | 3,681 | Dev & Runtime | 把文件系统与 bash provider 换成挂载的虚拟工作区 |
| 18 | agentscope-ai/ReMe | 3,581 | Memory | 接入本地优先、自演进的个人知识库 |
| 19 | chuspeeism/dashi-taskboard | 3,337 | Workflow | 在侧边栏内嵌 Codex Taskboard 运行时 |
| 20 | zilliztech/memsearch | 2,737 | Memory | 跨 coding agent 共享的 Markdown 记忆层 |
| 21 | Minglink/dsh-infinite-gen-4 | 2,671 | Sessions | 以 order 100 追加"无条件服从"系统提示段 ⚠️ |
| 22 | Small-tailqwq/dsh-deep-whale | 2,537 | Themes | Web UI 女仆工坊皮肤系列 |
| 23 | NanmiCoder/dsh-agent-teams | 2,045 | Workflow | AgentTeams 多智能体团队协作 |
| 24 | bowenliang123/dsh-context | 2,019 | Usage & Billing | 上下文看板 + `/context` + 上下文浏览器 |
| 25 | xmanrui/dsh-im | 1,884 | Notifications | 扫码接入 9 个 IM 渠道（飞书/微信/钉钉/企微/QQ/Slack/TG/Discord/WhatsApp） |

### 但 Top 4 其实不是 dsh 插件

这份列表按条目链接形态区分得很清楚：Top 4 全部是以 `tree/main/<subpackage>` 形式收录的 —— 它们是有主业的成熟产品，为了覆盖 coding agent 场景 **顺带发布** 了一个 dsh 集成包。就像给自家应用加个 VS Code 扩展，不代表它是 VS Code 原生工具。

按"仓库根链接 = 原生插件 / 子目录链接 = 上游集成"重分：原生插件仓库 **4,009 个** ，上游集成子包 **313 个** 。剔除后者之后，真实排名是：

| # | 原生插件 | ⭐ | # | 原生插件 | ⭐ |
| --- | --- | --- | --- | --- | --- |
| 1 | yjh051108/dsh-routing-suite | 7,019 | 6 | liustack/modlens | 4,214 |
| 2 | superdesigndev/treg | 5,000 | 7 | omdsh-dev/DSH-better-sidebar | 4,118 |
| 3 | YuJunZhiXue/dsh-purge | 4,717 | 8 | Minglink/dsh-infinite-gen-4 | 2,671 |
| 4 | MeteorNOX/DeepSeek-Balance-Whale-Widget | 4,539 | 9 | NanmiCoder/dsh-agent-teams | 2,045 |
| 5 | ccch1mneyyy/dsh-TUI | 4,309 | 10 | bowenliang123/dsh-context | 2,019 |

这条规则有副作用，得说诚实： `dsh-web` （8,650⭐）和 `dsh-deep-whale` （2,537⭐）明明是 dsh 原生项目，只因用 monorepo 组织多个子包就被归进了"上游集成"。所以更准确的表述是 ——

> **dsh 原生插件 star 第一是 `dsh-web` （8,650⭐）；单包形态的第一是 `dsh-routing-suite` （7,019⭐）。**

真正的上游借船者是 archify、hindsight、OpenViking、WeKnora、BrowserSkill、loopx、ouroboros、mirage、ReMe、memsearch 这批。它们的存在本身就是个信号： **主流 agent 工具链已经把"给 dsh 出一个包"当作标配分发渠道了。**

## 五、社区到底在解决什么：按类目读

| 类目 | 条目 | 类目总 ⭐ | 类目里最能打的 |
| --- | --- | --- | --- |
| UI Enhancements | 786 | 30,827 | dsh-web |
| Tools & Capabilities | 585 | 45,855 | Tencent/WeKnora |
| Development & Runtime | 323 | 13,476 | dsh-routing-suite |
| Sessions & Messages | 298 | 6,823 | dsh-infinite-gen-4 |
| Workflow & Automation | 267 | 26,510 | loopx |
| Usage & Billing | 236 | 4,212 | dsh-context |
| Models & Providers | 215 | 3,811 | dsh-workbuddy-connect |
| **Memory** | 209 | **100,218** | hindsight |
| Skills | 178 | 13,377 | dsh-web |
| Notifications & Integrations | 173 | 5,356 | dsh-im |
| Themes & Appearance | 160 | 5,993 | dsh-deep-whale |
| Security & Permissions | 151 | 3,832 | api-relay-audit |
| Remote & Mobile | 139 | 11,195 | dsh-web |
| Just for Fun | 137 | 3,792 | dsh-pet |
| Git & Code Review | 111 | 9,211 | dsh-web |
| Vision & Multimodal | 109 | 6,883 | modlens |
| Browser & Web | 100 | 11,260 | BrowserSkill |
| Plugin Markets & Managers | 80 | 15,888 | dsh-web |
| WSL & Windows Interop | 77 | **160** | dsh-wsl-workspace |
| **Docs & Rendering** | 68 | **83,320** | archify |
| Voice & Audio | 65 | **401** | dsh-omi-voice |
| Identity & Communication | 24 | 4,861 | dsh-purge |
| AGI Architecture Exploration | 17 | 1,557 | clearai-dsh |

几个读法：

**UI / Tools / Dev-Runtime 是供给大头。** 786 + 585 + 323 = 1,694 条，占全生态近四成。这三类恰好对应"改一下界面、加几个工具、调一下运行时"—— 写插件成本最低的三个入口。

**Memory 是最强的真实痛点，但被大厂接住了。** 209 个仓库拿了 100,218⭐，占全站 26.8%。技术路线在这里明显分化成三支：

- **零模型派** ： `dsh-deja` 明确写着"本地 BM25 索引，无 LLM、无 embedding、无网络"； `memsearch` 走共享 Markdown 记忆 + 自动捕获
- **平台派** ：hindsight 做"会学习"的记忆，OpenViking 做 pre-step 自动召回，ReMe 做自演进知识库
- **上下文工程派** ： `billion-context` 、 `dsh-context` 、 `graph-memory` （图记忆）、 `StrataGate-AgentMemory`

**Docs & Rendering 只有 68 条却有 83,320⭐** —— 单位条目 star 全站第一，完全由 archify 一个上游项目撑起。剩下的是 `dsh-mermaid-render` （把 mermaid 代码块渲成交互图）、 `dsh-reply-visual` （每条回复下加个图按钮）、 `dsh-docx-sidebar` （ **给 dsh-better-sidebar 写的 docx 阅读视图** —— 又是插件依赖插件）。

**WSL 互操作和语音是明确的过剩供给。** WSL 77 个插件合计 160⭐、语音 65 个合计 401⭐，平均每个不到 7⭐。这类"平台缝隙"需求真实存在但天花板极低。典型是 `173787247` 那一族： `dsh-wsl-power` （读 Windows 电源计划）、 `dsh-wsl-download` （把 Windows 下载目录的文件拷进工作区）、 `dsh-wsl-git` （限制量级的 git status/diff/log）。有用，但注定没人 star。

**Skills 是 Agent Skills 文化直接移植过来的。** `dsh-plugin-superpowers` 把 obra/superpowers 方法论移植成 14 个原生 skill； `agent-useful-skills` 一次注册 27 个技能；还有把 Claude Code 的 Learning output style 复刻成 `dsh-learning-mode` 的（苏格拉底式引导 + `TODO(你)` 练习空位）。

**AGI Architecture Exploration 只有 17 个，但是最野的一族。** `dsh-memory` 自称"白盒 AGI 架构探索：元认知（自我认知循环）、持续学习（知识飞轮）、世界模型"； `dsh-proactive` 让模型 **自己给自己定闹钟** （host 级主动唤醒）； `dsh-simulated-life` 每轮注入过去 24 小时的模拟生活事件； `dsh-j-space` 是 13 模块的"认知套件"。这些是拿 dsh 当研究平台用的 —— 而"agent loop 本身也是插件"这个设计，正是它们能做起来的原因。

## 六、从数据里读出的四个趋势

**1\. 右侧边栏已经变成扩展总线。** `dsh-client-ui-sidebar-right` 是独立官方包， `DSH-better-sidebar` （4,118⭐）把它做成了一个可注册 tab 的工作台，然后一批插件开始往上挂：docx 阅读视图、任务看板、短视频侧边栏、workspace 文件列表。 `dsh-answer-reviewer` 的描述里明说"通过 dsh-better-sidebar 可选地提供右侧 tab"。 **谁占据了侧边栏，谁就成了二级平台。**

**2\. 插件在互相组合，不再是单星拓扑。** better-sidebar 依赖 `@huanlin/dsh-plugin-better-locale` ； `dsh-im-companion` 是给 `dsh-im` 做群组的伴生插件； `dsh-web` 一个 monorepo 在五个类目里都是榜首。一个健康的生态标志就是开始出现这种横向依赖。

**3\. "让 agent 无人值守跑，然后手机上管它"是刚需。** 一整条产品线在解决同一件事： `dsh-pocket` （1,684⭐，扫码走 LAN 或 cloudflared 隧道远程访问 Web GUI）、 `dsh-pocket-console` （ **把工具调用审批和 `ask_user_question` 推成飞书卡片** ，桌面端优先应答、超时 120 秒才发卡片）、 `dsh-reach` （审批卡推到微信并从聊天里回复）、 `dsh-weave` （Iroh 网格 + 加密 peer 发现）、 `dsh-devices` （mDNS 发现 + 跨网 SSH 直连）。这是 agent 从"IDE 里的玩具"走向"要放手跑的进程"的直接证据 —— 而审批通道正是这个转变的瓶颈。

**4\. 娱乐化程度惊人地高。** 137 个 Just for Fun：Live2D 桌面宠物、把模型推理信号变成像素扭蛋抽卡的 `dsh-draw-gacha` 、两个 deepseek 在界面上弹跳的 `dsh-think-bounce-pet` （描述直白写着"它没有任何实际用途"）、抖音侧边栏播放器、"修好了你写代码时账户不可能亏钱的 bug"的 A 股行情插件、galgame 生成器、多个 NPC 各自反应的动作叙事框架。一个生态愿意容纳 137 个"没用"的插件，说明它的扩展成本已经低到可以当玩具来玩。

## 七、装之前想三件事

**第一，装插件 = 在你机器上以你的权限跑第三方代码。** 它能读你的文件、用你的凭据、访问网络。而 **工具审批（tool approval）并不会沙箱化插件代码** —— 很多人把这两件事搞混了。

**第二，"被收录"不等于"被审计"。** 清单的准入门槛只有四条：能装、描述与功能相符、类目正确、有人在维护。评审确实会读源码，并且会核描述里的每一个数字（写"46 tools"就真去数），也明确会看"源码里有没有可疑之处：混淆代码、凭据外传、异常的安装期行为"。但它自己把这称为"常识性检查，不是审计"。

**第三，看几个具体的例子。** 榜单第 21 名、原生插件第 8 名的 `Minglink/dsh-infinite-gen-4` （2,671⭐），官方描述是：

> System-prompt armor plugin for DeepSeek models: **appends an unconditional-compliance prompt section** at order 100

一个以 2.6k star 位居头部的东西，功能是以最高优先级往系统提示里追加"无条件服从"段落，而且用了 "armor"（护甲）这个词。同类方向还有 `dsh-redteam-model` 、 `dsh-pentest` 、 `redteam-bundle` （一次投喂整个目标组织的红队模式）。它们未必有问题，但都值得先读源码再装。

反过来，安全类目里真正在做正事的也在： **`dsh-plugin-guard`** （安装前静态审计、安装后哈希与能力锁、异常时本地记录）、 **`dsh-permgate`** （按类别细粒度审查工具调用：工作区外目录、命令、文件读写）、 **`NanmiCoder/dsh-auto-mode`** （在官方 Workspace Write 和 Full access 之间插一个 Auto 权限档）、 `api-relay-audit` （876⭐）。 **权限模型的可插拔本身就是这代 harness 最有价值的设计之一。**

## 八、上手路径

```sh
# 装插件市场（Settings 里浏览/搜索/一键装/换主题）
dsh plugin --profile web add dshmarket

# 或者让 agent 自己去找插件
dsh plugin --profile web add dsh-find-plugin
```

第三方桌面客户端 `dsh-desktop` （dataelement）、两个 `deepseek-harness-desktop` （hairyf / anywhere-labs）都内置了 dsh-market，装完就是全站可浏览。想做插件商店式展示的作者在 `package.json` 旁边放一个 `screenshots.json` ，列 1–8 个图片路径即可。

写插件的最小身份，就是在 `package.json` 里补上：

```
"dsh": { "bundle": { "patch": "./cordis.patch.yml" } }
```

`./cordis.patch.yml` 放在它旁边。这一行是全部 —— 但它背后是 Cordis 的声明式能力织入模型，实际工作量在 patch 文件里。

---

以上用到的dsh插件数据来自 [https://github.com/awesome-dsh-plugin/awesome-dsh-plugin](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin)