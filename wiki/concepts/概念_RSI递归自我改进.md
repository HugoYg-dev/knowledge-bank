---
type: concept
tags:
- RSI
summary: Recursive Self-Improvement（递归自我改进），AI 系统自我迭代优化的机制。在现代 Agent 工程中涵盖从提示词、驾具代码自修改（Self-Harness）到元研究闭环的多层阶梯。
aliases:
- RSI
- Recursive Self-Improvement
- 递归自我改进
- 递归自进化
- 自进化
- 概念_RSI递归自我改进
- Self-Harness
- Self Harness
- 自主进化宿主
- 自进化工程闭环
- 概念_Self_Harness_自主进化宿主系统
- 概念_Self-Harness
sources:
- wiki/sources/OpenAI前VP_Lilian_Weng_AI自我改进的近路不是改权重.md
- wiki/sources/这是一篇把RSI讲明白的科普级综述.md
- wiki/sources/万字复盘Codex_模型公司如何做产品的典型故事.md
- wiki/sources/一文读懂_RSI_大模型递归自进化五大技术路线全景解析.md
- wiki/sources/刚刚，DeepSeek Harness震撼开源：一切皆插件.md
- wiki/sources/深度剖析 DeepSeek 最新的 Harness DSH：为了自进化这盘醋包了一整盘饺子.md
- wiki/sources/从 LOOP 到图探索 —— 算法模型的 AutoResearch 自进化系统架构演进之路  美团 · 技术团队.md
- wiki/sources/Piccolo：递归自我进化的决策模型.md
updated: '2026-11-06'
---

# 概念：RSI递归自我改进

## 定义

**RSI（Recursive Self-Improvement，递归自我改进）** 指 AI 系统能够反身分析自身性能并改进自身架构、运行逻辑或认知机制，且改进后的系统更擅长进行下一轮改进，从而形成指数级增益正反馈闭环的理论与工程范式。

## 四层梯度分界标准

根据现代 RSI 工程评测框架，自我改进被严格区分为四个可观察的递进层级：
1. **持久改进（Persistent Improvement）**：改动写入权重、情景记忆、工具链或驾具代码，跨任务持久生效而非单次上下文临时效果；
2. **自主闭环（Autonomous Loop / 有界 RSI）**：系统在人类限定的安全沙盒内能够自主完成“识别缺陷 $\to$ 提出变体 $\to$ 实验验证 $\to$ 评估接纳”的完整闭环；
3. **递归增益（Recursive Gain / 点火 Ignition）**：系统不仅在特定任务基准上提升分数，更**显著提升了自身产生下一次有效改进的能力**，正式跨入复利加速区间；
4. **稳健与可控（Robustness & Open-ended RSI）**：增益在固定资源与分布外隐藏评测下保持稳健泛化，且不发生奖励作弊（Reward Hacking）、系统复杂度膨胀或对齐失控。

## 历史演进的五次边界推进

1. **推理与记忆反思（2022-2023）**：以 Reflexion 为代表，模型参数冻结，通过自然语言事后复盘构建外部情景记忆（错题本）；
2. **自生成数据与参数微调（2022-2024）**：以 STaR（推理链自举）与 SPIN（与历史策略自博弈微调）为代表，将改进信号固化写入模型权重；
3. **评判权移交与元评判（2022-2025）**：从 Constitutional AI 到 Self-Rewarding 与 Meta-Rewarding，逐步将打分权交由模型自身，但伴随严重的“尺子变弯”与评判标准漂移挑战；
4. **驾具代码自修改（2023-2026）**：通过 [[concepts/概念_Harness_Engineering_宿主编排工程|Harness Engineering]] 与代码生成，以 Self-Harness（自主外壳进化闭环）、达尔文哥德尔机（DGM）及工业级 AgentX 为代表，让智能体在固定底座模型上搜索优化运行代码与工具编排；
5. **学习与研究过程闭环（2025-2026）**：涵盖自适应学习（SEAL）、环境沙盘（WebEvolver）、真实物理控制（Motus2）乃至双层元研究架构（Bilevel Autoresearch、AIDE²），使科研流程本身成为优化对象。

## 核心挑战与四道安全门禁

当前工程实践表明，有界净正闭环已在部分场景中实现，但尚未跨过第三层递归“点火”门槛。通往开放式 RSI 存在四道关键制约：
- **外部验证锚（External Verifier Anchor）**：评估器、编译器及安全权限必须独立于可进化系统之外，严禁系统篡改自身裁判标准；
- **防分布坍缩（Anti-Collapse）**：防止自生成数据循环迭代导致的表征多样性衰减与自我确认偏见；
- **深层算法突破难度**：当前智能体在工作流工程优化上表现突出，但在重写核心机器学习训练算法上仍显薄弱（如 AI4AI-Bench 仅 0.250）；
- **对齐与复杂度治理**：伴随自进化出现的死代码累积、逻辑膨胀以及由于缺乏元认知循环导致的不可审计风险。

## 工业级实践注记

- **OpenAI Codex 的「自举」飞轮（2024-12 起）** `[原文陈述]`：据 [2026-10-21 来源] 的 Codex 万字复盘，Tibo 团队在 OpenAI Monorepo 上训练内部编程 Agent，让研究员用它更快编写基础设施、运行与改进下一代模型的训练系统——「先做出一个擅长帮研究员跑实验的模型，研究员用它造出更强的模型，再跑出更好的实验，如此循环往复」；后期进一步演化为「用 Codex 开发 Codex」，几个人几周即可做出新产品入口，改变了产品研发的物理规律。

## 五大技术路线分类架构

现代大模型 RSI 衍生出五种截然不同的实现范式，在修改对象、算力门槛与工程形态上呈现出明确的分工：

1. **模型权重与训练层自进化（Model-Level RSI）**：
   - **核心逻辑**：模型自己出题、自己答题、自己打分，通过 SFT/DPO/RL 微调自身权重，脱离对人类新增标注数据的依赖。
   - **代表工作**：Meta *Self-Rewarding LMs*（兼任考生与裁判）、UCLA *SPIN*（与旧版本策略自对弈微调）、Stanford *Quiet-STaR*（在任意文本预测时内化思维链独白）、MIT *SEAL*（生成自编辑指令直接更新自身参数）。
   - **特征与门槛**：需大量 GPU 算力，迭代周期长，存在表征漂移与坍缩风险。
2. **提示词与脚手架程序自进化（Prompt & Scaffold RSI）**：
   - **核心逻辑**：冻结基座权重（将 LLM 视作 CPU），将外围调用编排代码（Harness/Scaffold）与 Prompt 抽象为可优化目标，通过文本反馈梯度或进化搜索自修改。
   - **代表工作**：Microsoft *STOP*（自授优化器重写脚手架）、*ADAS*（Meta Agent Search 搜索图灵完备代码空间）、Stanford *TextGrad*（用自然语言批评模拟 PyTorch 自动反向传播）、Stanford *DSPy*（声明式流水线编译与示范样本优化）。
   - **特征与门槛**：仅需推理 API，门槛极低，适合闭源商业模型。
3. **上下文、记忆与技能库自进化（Context, Memory & Skill RSI）**：
   - **核心逻辑**：构建外挂的自演化记忆网络与可执行技能代码库。做错则写入反思错题本，做对则将逻辑封装为可复用函数工具。
   - **代表工作**：*Voyager*（Minecraft 终身自主技能库）、*Reflexion*（语言强化反思机制）、*A-MEM*（基于卡片盒笔记法的互联演化记忆网络）、*ACE*（模块化演化上下文剧本）、*MemEvolve*（连同记忆架构与学习机制一同进化的元进化）、*Letta*（原 MemGPT，状态化自维护 Agent）。
   - **特征与门槛**：随日常任务运行自然沉淀，零额外微调成本，天然具备高可解释性与抗遗忘性。
4. **自我指向与代码自修改自进化（Self-Modifying Coding RSI）**：
   - **核心逻辑**：智能体具备自指涉权限（Self-Referential），直接读取、打补丁并重写自身运行底层源码，用新版本的自己继续修改下一代自己。
   - **代表工作**：*Gödel Agent*（哥德尔自指智能体框架）、*Darwin Gödel Machine (DGM)*（实证基准测试检验 + 达尔文智能体多样性档案树）、DeepMind *AlphaEvolve*（算法发现进化流水线）、Sakana AI *ShinkaEvolve*（引入代码新颖性拒绝采样的低开销演化）、Meta *Hyperagents*（将任务智能体与元智能体合二为一的可编程架构）。
   - **特征与门槛**：必须依赖强化沙箱环境（Docker/虚拟环境）与严密测试集，防范自锁死与越权。
5. **多智能体协同与全自动 AI 研发（Multi-Agent & Auto AI R&D）**：
   - **核心逻辑**：通过出题人 vs 解题人对抗博弈、或全自动“科研实验室”多角色分工，实现无人值守的持续演进。
   - **代表工作**：*R-Zero*（出题者动态逼近 50% 难度边界的零数据自博弈共进化）、*EvoAgentX*（自动化编排进化 MAS 拓扑）、Sakana AI *The AI Scientist (v1/v2)*（端到端提出假说、写代码跑实验、可视化并撰写论文）、Karpathy *autoresearch*（600 行代码单卡过夜全自动修改训练脚本与验证提交循环）。

## 工程落地判据与实施闭环

### 1. 适用与严禁场景
- **强烈推荐适用**：
  - **客观可验证反馈场景**：代码生成（单元测试通过率）、数学定理证明（形式化验证器）、算法性能（运行耗时优化）、模拟环境（环境奖励与得分）。
  - **人工设计提示词/工作流陷入瓶颈的复杂复合系统**。
  - **垂直领域高质量人工标注数据枯竭的场景**。
  - **开放式环境下的长期伴随式任务**（个人编程助手、桌面 OS Agent）。
- **严禁 / 避坑场景**：
  - **缺乏可靠评判标准的纯主观任务**：开放式文学创作、闲聊等，缺乏外部客观锚点时，极易陷入自我迎合（Reward Hacking）与模式坍缩。
  - **对单次响应延迟与 Token 成本极度敏感的实时生产业务**。
  - **无安全沙箱隔离的高危生产环境**。

### 2. RSI 落地标准五步法
1. **明确可修改边界**：遵循渐进暴露原则（Prompt/记忆 $\to$ 工具生成 $\to$ 源码/权重）；
2. **配置客观外部裁判**：优先使用编译器报错、单元测试、沙箱指标或多模型投票机制，防止“尺子变弯”；
3. **元智能体对症下药**：分析上一轮执行 Trace 与失败原因，精准生成代码/参数补丁；
4. **建立版本档案馆**：维护多样性变体树或帕累托前沿，避免早熟收敛至局部最优；
5. **设定安全死线与熔断**：资源、Token 与迭代轮数硬性封顶，异常时自动 Git 回滚。

## 核心工程范式：Self-Harness（自主外壳进化闭环）

**Self-Harness（自主外壳进化系统）** 是 RSI 在现代 Agent 体系中的核心工程落地范式。正如 Lilian Weng 在《Harness Engineering for Self-Improvement》中所指出的：自我改进近期的近路不是改模型权重，而是围绕模型搭建的外壳（Harness）。在模型权重冻结（视作通用 CPU）的前提下，通过对智能体长程任务弱点的自动化挖掘与代码重构，使系统持续进化且无性能回归。

### 1. 两种核心实现路径

#### 路径 A：离线/静态三步工程闭环（Standard Holdout Loop，Zhang et al. 2026）
1. **弱点挖掘（Weakness Mining）**：自动化聚合分析历史失败轨迹与报错日志，精准定位 Harness 宿主系统在机制、状态流与提示词上的缺陷；
2. **修改提议（Modification Proposal）**：由元智能体针对缺陷提出具有严格范围限制的 Harness 代码修改（diff 补丁）；
3. **保留集验证（Holdout Verification）**：在保留的独立验证集上运行严格测试——必须**既解决弱点模式，又不产生全局能力回归**，才允许通过 Git 棘轮机制自动合并进生产代码库。

#### 路径 B：运行时动态插件热插拔范式（Runtime Self-Evolution）
- **微内核物理插槽**：以 [[entities/实体_DeepSeek_Harness|DeepSeek Harness (DSH)]] 为代表，依托 [[entities/实体_Cordis|Cordis]] 微内核将 Agent Loop 自身解耦为可插拔插件（`ctx.agentLoop`），对外声明依赖 `ctx.systemPrompt` 与 `ctx.tools`；
- **运行中自改装机制**：
  1. 智能体在执行任务时，可直接感知暴露在外的 TypeScript 插件接口与生命周期契约；
  2. 针对特定任务动态生成数十行工具插件，或自主重写数百行全新调度 Loop 代码；
  3. 框架利用撤销条（Disposer）管理副作用、依赖变动通知与事务性 HMR 进行进程内平滑热装载，若新代码出错则自动回滚至稳定版本，实现零停机、无残留的自适应演化。

### 2. 代表实践与系统
- **DeepSeek Harness DSH (2026)**：通过 Cordis 命令式微内核将 Agent Loop 本身作为插件解耦，提供事务性 HMR 与依赖响应，为 Agent 运行中自我演化提供底层基础设施。
- **美团 AutoResearch 自进化系统 (2026)**：在算法模型自进化场景中，通过“业务知识库 + 真实 A/B 大闭环 + 经验自动沉淀”实现系统越用越好用；踩坑经验自动提炼为 Skill 草稿，经“系统初筛 + 人工审核”两级校验后反哺系统工具集，形成高防幻觉的经验晋升链。
- **Piccolo 决策模型自进化研发框架 (2026)**：AgentScope 与 Data-Juicer 团队在专用决策模型领域实践了基于 RSI 的自动化研发演化闭环。通过研究 Agent 调度 Agentic Data Engineering 与 DataJuicer-Sandbox，构建“方案设计 $\to$ 构建与实验 $\to$ 结果反馈（逐题 KL 散度与 13 维语义画像切片诊断） $\to$ 诊断与更新”的反馈 LOOP。通过 10+ 轮、150+ 项探索实验（耗费 6,300 GPU hours）与 Context Evolving 输入演化搜索，驱动 [[entities/实体_Piccolo|Piccolo-27B]] 在 JevBench Public（92.21%）、HarnessJevBench Hard（84.41%）及 DataJevBench（82.60%）等基准上领跑第一，验证了在客观判断分布锚点支撑下的模型与数据协同 RSI 自进化路径。
- **Darwin Gödel Machine (2025)**：Agent 进化自身代码库，SWE-bench Verified 达 50%。
- **AlphaEvolve (2025)**：进化搜索 + 冻结 LLM 生成 diff，优化 GPU kernel 与矩阵乘法。

## 来源与参考

- [[wiki/sources/OpenAI前VP_Lilian_Weng_AI自我改进的近路不是改权重]]
- [[wiki/sources/这是一篇把RSI讲明白的科普级综述]]
- [[wiki/sources/万字复盘Codex_模型公司如何做产品的典型故事|万字复盘 Codex：一个在模型公司如何做产品的「典型」故事]]
- [[wiki/sources/一文读懂_RSI_大模型递归自进化五大技术路线全景解析]]
- [[wiki/sources/刚刚，DeepSeek Harness震撼开源：一切皆插件]]
- [[wiki/sources/深度剖析 DeepSeek 最新的 Harness DSH：为了自进化这盘醋包了一整盘饺子]]
- [[wiki/sources/从 LOOP 到图探索 —— 算法模型的 AutoResearch 自进化系统架构演进之路  美团 · 技术团队]]
- [[wiki/sources/Piccolo：递归自我进化的决策模型.md|Piccolo：递归自我进化的决策模型]]
- 关联概念：[[concepts/概念_Harness_Engineering_宿主编排工程]]、[[concepts/概念_Loop_Engineering循环工程]]、[[concepts/概念_Agent系统自动优化闭环]]
- 关联实体：[[entities/实体_DeepSeek_Harness]]、[[entities/实体_Cordis]]、[[entities/实体_AutoResearch]]、[[entities/实体_美团]]、[[entities/实体_Codex]]、[[entities/实体_Piccolo]]
