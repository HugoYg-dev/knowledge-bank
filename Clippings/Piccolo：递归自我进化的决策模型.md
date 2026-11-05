---
title: "Piccolo：递归自我进化的决策模型"
source: "https://mp.weixin.qq.com/s/g5RyquIct8gK1mX8_6n3OQ"
author:
published:
created: 2026-11-05
description: "Piccolo是一款基于递归自改进（RSI）框架的决策模型，在JevBench等基准测试中多项指标排名第一，能为智能体工作流、数据处理及游戏操控提供快速精准的长程决策支持。"
tags:
  - "clippings"
---
在实际应用中，Piccolo 可以作为决策组件，接入需要快速判断的任务流程。从智能体的工具审核与上下文筛选，到数据处理中的关键决策，再到游戏中的连续判断，Piccolo **迅速理解当前状态、比较候选项** ，返回程序可以直接使用的结果与概率。

为持续提升这些判断能力，团队设计了一套基于 **递归自改进（RSI）** 的研发框架：研究 Agent 根据模型错误与训练反馈选择数据、检验改动，并将实验结果用于下一轮优化。

**01**

**从游戏到工作流，看 Piccolo 如何决策**

### Game｜在连续动作中作出选择

Piccolo 具有优秀且迅速的长程决策能力。团队选取了《绝区零》的战斗场景， **Piccolo 根据当前游戏的实时局面，动态为角色的移动、攻击和闪避提供动作指导** 。下方实录同步展示了游戏画面与按键决策， **Piccolo 在高帧率下流畅地击败了敌人** 。

《绝区零》战斗实录：Piccolo 根据游戏截图提供动作指导，执行端落实为按键操作。

除了瞬息变化的动作游戏，Piccolo 也支持益智与棋盘游戏中的策略判断。Mario 需要关注移动与跳跃时机，2048 需要规划合并方向，推箱子关注箱子与目标的合理分配，黑白棋则需要根据博弈局面选择落子位置。

**Mario** 移动与跳跃时机

黑白棋棋盘状态下的落子选择

### Harness｜让判断覆盖 Agent 工作流的关键环节

从选择工具到确认任务完成，Agent 的每一步都需要结合任务、证据与约束作出判断。Piccolo 可以嵌入 Harness，在 **工具选择、模型路由、上下文与记忆、权限与信任、完成验收、失败恢复** 等子场景中，为下一步动作提供决策。

![Harness 六类子场景：工具选择、模型路由、上下文与记忆、权限与信任、完成验收、失败恢复](https://mmbiz.qpic.cn/sz_mmbiz_gif/ia2awwZLWFZS7Qicv9A4ZBBoL3hlh7CHWkDogAprPlmibaZTh5YbPl5EIplCQdBQwtSlIV4EsmasZqZMjhaWeaceKpffj32R2DCSJ5Nr5B8iabk/640?wx_fmt=gif&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

Harness 六类子场景：工具选择、模型路由、上下文与记忆、权限与信任、完成验收、失败恢复

例如，查询交付日期时选择订单系统；多个模型都能完成任务时，结合预算选择执行资源。为晚餐规划筛选上下文时，保留用户的食物过敏信息，过滤过期天气等无关内容；当 Agent 仅获准保存草稿时，选择保存草稿，而不直接发送或发布。证据不足就继续核验，遇到临时故障则判断是否重试。

Piccolo 根据任务进展，为工作流的下一步提供判断： **Harness 提供当前状态与候选动作，Piccolo 给出判断，再由工作流执行。** 这些决策帮助工作流调用工具、保留信息、请求确认，或调整执行路径。

### Data｜从数据进入流程，到产物校验与交付

数据处理同样需要大量结合语义、规则与证据的判断。Piccolo 可支持 **数据过滤、处理方案选择、产物质量评估、信息充分性判断、证据与隐私审查、工作流控制** 等子场景，帮助流程决定保留什么、怎样处理，以及结果能否继续使用。

![Data 六类子场景：数据过滤、处理方案、产物质量、信息充分性、证据与隐私、工作流控制](https://mmbiz.qpic.cn/mmbiz_gif/ia2awwZLWFZSluzTrWsTDTe68f05iazaib4t7ow3u2MVjXuD1IBmOfQWNDHQWKG3IQSyFlrAGic8U78SCTsDPFT0rt3rmPTdLD64Lh0yTgjqaa0/640?wx_fmt=gif&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=1)

Data 六类子场景：数据过滤、处理方案、产物质量、信息充分性、证据与隐私、工作流控制

例如，判断清洗与去重的先后顺序，选择忠于来源的摘要；计算税后利润时，缺少税额就先请求补充信息；对外分享包含邮箱的记录前，先将邮箱脱敏。模型接收原始材料、处理要求和当前结果，比较候选动作，再由数据工作流落实选择。

这些子场景覆盖数据进入、处理、审核与交付的多个环节。面对不同任务，可以调整问题与候选项，让 **同一种决策接口支持工作流中的多种判断** 。

**02**

**四项基准，检验 Piccolo 的决策能力**

AgentScope团队在 **JevBench Public、Decision Index、HarnessJevBench Hard 和 DataJevBench** 上评测 Piccolo，分别观察通用决策、文本判断、Agent 运行控制及数据工作流中的能力。

在网站 11 月 2 日更新的 11 模型对比中，Piccolo-27B 的 JevBench Public 准确率为 92.21%，HarnessJevBench Hard 为 84.41%，DataJevBench 为 82.60%，三项均排名第一。其文本 Decision Index Public 成绩为 68.59。 多模态 Decision Index Public 成绩为 77.75。

![图片](https://mmbiz.qpic.cn/mmbiz_png/ia2awwZLWFZQWGNI0Idhw88Pg5KYuSHo5D7kfH4OTFO0u6dVnUktczZy31RWPLgicaFGlGjKPRQibE3TkqtEbQ1ccBnA9lKCJYibsicKMsdiaYMx0/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=2 "undefined") ![图片](https://mmbiz.qpic.cn/mmbiz_png/ia2awwZLWFZRMXUUgpE0zmQTiaibECnFkyh7DF7ibJQWOQ8eT6tcPiacJVIm7zBwKTiaO9WuMTp0pKnibUiaqXmQibor9PMf6mdeCKNpJlxAQBMfToT8/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=4 "undefined") ![图片](https://mmbiz.qpic.cn/mmbiz_png/ia2awwZLWFZSnEibYGzQy6XlKia6ovaw9XyAnsyXUAo8IsBIibGD0yibVhxfSe8QYSmbYQqglQtaspdbQxkrCnGs7b4Jtn8W61ESicgoDhBGF9Kus/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=6 "undefined")

左右滑动查看更多

通用成绩之外，团队还希望检验模型能否处理前面展示的工作流判断。因此，团队构建并开源了两个场景基准： **HarnessJevBench（https://github.com/agentscope-ai/HarnessJevBench）** 检验工具与资源选择、上下文管理、权限边界、完成验收和失败恢复； **DataJevBench（https://github.com/datajuicer/DataJevBench）** 检验数据收录、处理方案、产物质量、信息充分性、结论判断和工作流控制。

两个基准的任务定义与评测方法均可在仓库中查看，欢迎社区使用及贡献。

**03**

**Piccolo 如何持续进化**

为持续提升 Piccolo 的决策能力，团队设计了一套基于 **递归自改进（RSI）** 的研发框架。研究 Agent 选择或构造训练材料，执行训练与评测，再根据模型错误与训练反馈调整下一轮实验。数据来源、语义标签、逐题学习记录和模型表现被关联起来，让每次改动都有据可查，也为后续探索提供起点。

，时长00:20

<video src="https://mpvideo.qpic.cn/0bc3oaaceaaaquapgbxkyzvfa4gdejyaaiqa.f10002.mp4?dis_k=d52d7c152cce61cb287599cc0a68d948&amp;dis_t=1793852188&amp;play_scene=10120&amp;auth_info=FNPFnrQCEC5IkumdvFkNEURddzwTDkhzdj0XZkIXdFMkL25HGCwLYz9/bhU3NgAxUFc=&amp;auth_key=c310cb28cf88b96c9277447a661a9183&amp;vid=wxv_4767779417022791685&amp;format_id=10002&amp;support_redirect=0&amp;mmversion=false" controls="">您的浏览器不支持 video 标签</video>

**Piccolo 演化轨迹：** 在 Agent 驱动的迭代闭环中，10+ 轮、150+ 探索实验沿着反馈持续演进。全部探索实验合计使用 6,300 GPU hours（PPU-真武810E），并非仅用于训练最优模型。

### ① 把多源数据，变成模型能学的判断题

团队从开源社区收集了 **665 万条数据** ，覆盖分类、检索、数理推理、偏好判断与工具使用等任务，并定向合成决策环境，从中整理训练材料。不同来源统一为 **“状态、问题、候选项、目标分布”** ：硬标签给出确定选择，软标签保留评分与偏好的分布，两者使用同一个训练接口。

要选择训练材料，先要知道每条样本训练什么判断。基于 Data-Juicer，团队建立了包含 **13 个标注维度、551 个预定义取值** 的标签体系，记录领域、能力、任务形式、难度和质量等信息。图一按领域、能力和任务形式展示训练数据画像。在这些大类下，团队进一步标注具体的判断能力，例如约束推理、工具适用性，并结合领域等标签筛选训练材料。

所有数据入池前统一去重，并检查、排除与 Benchmark 的重叠，保持训练与评测隔离。主要监督阶段让模型直接学习候选项上的目标概率分布，为不同任务提供统一的决策训练接口。

![数据来源治理、语义标注与训练数据画像](https://mmbiz.qpic.cn/sz_mmbiz_png/ia2awwZLWFZTp8icq4O0pYddqhvf9MnYo8JITY6U67wNRc880iaKwz0vu9jicWZbIfAkZp6aTcKrpuR8d6SQ0yn67y5OaBnOpLoY11yXnQfn34E/640?wx_fmt=png&from=appmsg#imgIndex=7)

数据来源治理、语义标注与训练数据画像

### ② 从模型的错误中，找到下一轮改进方向

数据整理好之后，研究 Agent 需要决定 **下一轮训练什么，以及怎样使用这些数据** 。团队观测逐题 KL 损失，即模型预测与目标分布的差异，再按语义标签汇总，观察不同领域、能力和任务类型的学习状态。

对偏差持续较高的数据切片，先复核题目条件与答案，再检索相近材料或定向合成更多条件组合；对已充分学习、偏差低位稳定的同质样本，则减少重复曝光，保留有代表性的回放。筛选与配比、审计与改写、定向合成、删除与降采样，可以组合成不同的实验方案。

![训练反馈、能力诊断与数据操作](https://mmbiz.qpic.cn/mmbiz_png/ia2awwZLWFZR9hTebHRiaupGBscqEbKYrAgQfxUAkBq3HGKKLibY4ic2KBKKKlyRRUFQ7WTMPwELPNtm2B9XHdI74tlrqd1Q6po8fB4pTL12Hrg/640?wx_fmt=png&from=appmsg#imgIndex=8)

训练反馈、能力诊断与数据操作

自研的 Agentic Data Engineering(https://github.com/datajuicer/agentic-data-engineering) 组织多个研究 Agent，按 **“方案设计 → 构建与实验 → 结果反馈 → 诊断与更新”** 推进。DataJuicer-Sandbox(https://github.com/datajuicer/data-juicer-sandbox) 将数据处理、训练和评测组织成可执行工作流。人类设定目标、资源预算与数据范围，Agent 在约定范围内提出方案、完成实验并分析结果。

这个 **反馈 LOOP** 将上一轮结果转化为下一轮选择：比较总体与分项变化，决定哪些分支继续探索、哪些需要调整，并将模型检查点、数据版本、配方和实验记录关联保存。表现较好的模型成为后续起点，有效经验供下一轮复用。

### ③ 协同优化数据、训练与推理，持续提升决策能力

Piccolo 的演进从数据整理与配比入手，逐步细化到具体判断能力，再结合实验结果调整训练与推理方式。27B 基座的研发全集文本 Decision Index 为 **48.91** ，初步整理数据并训练后达到 **56.68** ；随后按标签调整背景与定向材料的比例，从表现较好的模型继续探索。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ia2awwZLWFZR5gY7Yup5OZZ0rBOxEspPR2yib8IY5HC3pyg5xmbe9Hkogxax4w3scSBNnf4BwavYXiau5cPicgUpzCJTLb5pApQbh5PiavUxnoLM/640?wx_fmt=png&from=appmsg#imgIndex=9)

图三：数据配方、训练经验与模型合并连接不同实验分支。文本主线采用研发全集 DI，多模态分支采用相应图文评测

团队同时探索模型如何使用这些材料：双向注意力让题面信息相互参考，候选监督对齐决策输出，分阶段安排广泛覆盖和定向加强，并依据分项表现合并互补模型。问题与上下文的排列、问题前置和重复阅读等输入组织策略，也被纳入搜索，形成 Context evolving。在一组同权重复测中，仅调整输入与推理设置，全集文本 DI 从 65.05 提升到 66.19。

继续匹配数据、训练和输入设置，并结合逐题学习反馈筛选与补充数据后，27B 的全集文本 DI 达到 **68.59** ，最优模型累计训练 **35 万条样本** 。上述总体提升来自多轮探索；单项改动的收益通过对应实验检验。

同一套数据工程方法也用于 9B 和 4B。如图三所示，在采用 Context evolving 与双向推理的设置下，9B 从 **46.78 提升到 60.86** ，4B 从 **39.94 提升到 58.29** 。图文分支进一步探索了视觉能力训练与图文、文本模型合并，为后续跨模态判断提供基础。

**04**

**后续发展**

从游戏中的连续动作，到 Agent 执行控制与数据处理，Piccolo 将当前状态转化为工作流可以使用的判断。接下来，AgentScope团队将继续提高 **反馈闭环的探索效率** ，让有限的训练与评测预算更多用于有效改进；同时强化 **跨模态判断** ，提升长程、实时场景中的 **连续决策能力** 。

点击阅读原文，即可跳转模型链接~

---

```
👇点击关注ModelScope公众号获取更多技术信息~
 魔搭ModelScope社区  模型开源社区魔搭社区ModelScope官方账号 184篇原创内容  
          公众号
```