---
id: "7389934316072996414"
cubox_url: https://cubox.pro/web/card/7389934316072996414
url: https://baoyu.io/translations/rl-envs-real-world
tags:
  - LLM/training/RL
  - Infra/rl
published: 2025-11-13
---
# RL 环境与智能体能力金字塔 | 宝玉的分享

2025 年是“智能体之年”，AI 已经走出聊天框，开始迈入现实世界。但我们真的快要有通用的智能体了吗？还是说这仍是十年后的梦想？那个价值万亿美金的问题是：**这些 AI 智能体 (AI Agent) 到底能完成多少有经济价值的工作？**

[Read in Cubox](https://cubox.pro/web/card/7389934316072996414)  
[Read Original](https://baoyu.io/translations/rl-envs-real-world)  

---


---

\## 📖 正文全文

# RL 环境与智能体能力金字塔

[baoyu.io](https://baoyu.io/translations/rl-envs-real-world)

2025 年是"智能体之年"，AI 已经走出聊天框，开始迈入现实世界。但我们真的快要有通用的智能体了吗？还是说这仍是十年后的梦想？那个价值万亿美金的问题是：**这些 AI 智能体 (AI Agent) 到底能完成多少有经济价值的工作？**

为了回答这个问题，我们对模型的训练和评估方式已经变了：不再是给单个回复打分，而是评估它使用工具执行多步骤任务的能力。对于参与测试和后期训练的人来说，2025 年是 **RL 环境 (RL environments) 之年** ：这是一个个虚拟世界，模型可以在其中行动、实验，并通过逼真的多步骤任务进行学习。**(RL 指的是强化学习 Reinforcement Learning，这是一种让 AI 通过试错和获得"奖励"来学习的训练方法)**。

我们"雇佣"了 9 个 AI 模型，在我们的一个 RL 环境中执行了 150 项任务。结果如下：

![](https://cubox.pro/c/filters:no_upscale()?imageUrl=https%3A%2F%2Fbaoyu.io%2Fuploads%2F2025-11-13-690939dbf8147ed73bf3b6e2_5f38d8a3.png&valid=false)

即使是 GPT-5 和 Claude Sonnet 4.5，在我们的 RL 环境中，也失败了超过 40% 的智能体任务。

两件事显而易见：

* GPT-5 和 Claude Sonnet 4.5 遥遥领先，独一档。

* 但即便是它们，失败率也超过了 40%。

原始分数告诉了我们谁赢了，但没有告诉我们 *为什么*，以及我们该如何进步。要理解这些结果对现实世界智能体的真正启示，我们得先看看一个逼真的 RL 环境是如何被构建------或者更准确地说，是如何被"培育"出来的。

\## "培育"一个 RL 环境

每个 RL 环境都需要三样东西：

* **一个连贯的世界模型：** 定义了环境背景的宏观框架。

* **一套实体 (entities)：** 世界中的物体以及它们之间的关系。

* **一个工具系统：** 智能体与这些实体互动的接口。

要想把模型训练成合格的"虚拟同事"，这些环境需要植根于真实打工人的经验，而不是抽象的模拟。并且，现实世界的复杂系统不是自上而下设计出来的，它们是逐渐演化出来的。

RL 环境的一大优点是，它们天然就体现了这一思想。一旦框架搭建好，一个由专家贡献者组成的多元化社区就可以有机地"培育"它。

我们的环境就是这么来的：在一个确保关系和属性连贯的框架内，拥有专业领域知识的"Surgers"**(指本文作者公司 Surge AI 的贡献者)** 会根据他们自己的经验，往这个世界里填充逼真的实体和任务，从而"培育"这个世界。

换句话说，这些智能体所训练的环境，正是由那些它们未来要辅助的人类同事亲手塑造的。

\## 走进 Corecraft 公司

我们的 RL 环境之一是 Corecraft 公司，这是一家在线零售商，专卖高性能 PC 零件和定制电脑。这个"世界模型"就是公司本身，它的"实体"包括客户、订单、支持工单，以及所有维持运营的记录。

这次测试结果中，智能体扮演的角色是"客服专员"，帮助客户和员工处理任务。这些任务五花八门，从简单的产品查询、政策提问，到需要理解不同系统如何交互的、多步骤的操作流程。

一个非常简单的任务可能是： *2025 年 7 月有多少笔退款？*

而一个更复杂的任务是： *一位客户下单一台游戏电脑，但我在最后审核时收到了兼容性警告。他们订购了 ZentriCore Storm 6600X CPU 和 SkyForge B550M Micro 主板，还有 32GB 的 HyperVolt DDR5-5600 内存。系统提示不兼容。你能帮我找出问题所在，并给出最便宜的解决方案吗？*

为什么选择客服？因为尽管最耀眼的 AI 应用大多在高级研发领域，但 AI 的巨大经济价值很可能来自解决日常工作。此外，由于这个角色涵盖了各种难度和类型的任务，它是一个完美的试验场，能帮我们理解在现实世界中，一个智能体（无论什么角色）到底需要具备哪些基石能力。

\## 智能体能力金字塔

当我们分析模型们在这个岗位上的工作轨迹时，我们注意到同样的失败模式一再出现，但并非随机。每个模型的"翻车点"都倾向于集中在某个能力水平上，这揭示了一个自然的能力层级（或称金字"塔"）：AI 智能体必须先熟练掌握前一层，才能在开放环境中连贯地运作。

我们称这个框架为 **智能体能力金字塔 (Hierarchy of Agentic Capabilities)**，如下图所示（图中也标出了我们认为当前模型处于金字塔的哪个位置）。

![](https://image.cubox.pro/cardImg/52vz5cl9e6j15sy5tzre8u786hpefomhlkcwb8vjeuiad7if6f.png?imageMogr2/quality/90/ignore-error/1)

智能体能力金字塔，从工具使用到常识推理，以及 AI 模型目前所处的位置。

位于金字塔底座的是**基础能力：工具使用、目标设定和基础规划** 。往上是**更高阶的能力，如适应性和"接地气" (groundedness)：** 这些技能让模型能在不可预测的、混乱的现实环境中，保持对上下文的把握并随时调整。只有当模型高度熟练掌握了这些基础能力后，它才能开始展现出类似**常识推理 (common-sense reasoning)** 的东西：即能对从未见过的情况做出合理推断的能力，这是通用智能的核心组成部分。

当然，这个金字塔只是一个初步的划分。在实践中，模型的发展并非如此线性。这些能力相互重叠、相互促进，并持续并行进化。而且，达到"高度熟练"不等于"完美"：GPT-5 和 Claude Sonnet 4.5 偶尔也会在基础的工具使用上"翻车"，就像最优秀的高尔夫球手有时也会推丢一个简单的球。重要的是，它们已经足够稳定，让我们的关注点可以转移到更高阶的技能上。

从这个角度来看，划分这些层次的目的不是要强制一个僵化的顺序，而是为了诊断：我们在哪些方面取得了扎实的进展，哪些基础工作仍需努力。

\## 第一步：基础工具使用、规划与目标设定

这个金字塔最底层的地基，是判断一个模型是否能可靠地使用工具来实现特定目标。再往上一步，是它能否将一个任务分解为有意义的目标，并制定一个多步骤计划来完成它们。

做不到这一点的模型，不能叫"智能体"；它们顶多是"能用工具的聊天机器人"。

我们看到 GPT-4o、Mistral Medium 和 Nova Pro 就停留在这个层次。

要想成功完成最基础的智能体任务，模型需要能持续做到几件事：

1. 拿到一个多步骤任务，并将其分解为多个"小目标"。

2. 为每个小目标找到合适的工具，并排好使用顺序。

3. 把手头的信息准确地填入工具的参数中。

4. 一步步执行计划，不跑偏、不遗漏。

我们发现，那些较弱的模型无法可靠地完成这四点，这意味着即使是简单的智能体任务，对它们来说也像是在"掷骰子"------全凭运气。

**在一个任务中，这三个模型都犯了基础的工具使用错误** ，它们没能把提示里的信息合理地填入工具参数，或者干脆没能正确遵循 MCP 模式 **(MCP schema，可以理解为模型调用工具时必须遵守的"技术格式规范")**。

任务： *找出所有"黄金"或"白金"忠诚度等级的客户，条件是他们还有"未解决的"且"高优先级的"支持工单。*

以下是 Nova Pro 的尝试：

![](https://cubox.pro/c/filters:no_upscale()?imageUrl=https%3A%2F%2Fbaoyu.io%2Fuploads%2F2025-11-13-69096358dc70396c3951b173_860345cc.png&valid=false)

*"gold" (黄金) 显然不是客户 ID！*

GPT-4o 倒是先正确搜索了"黄金"和"白金"等级的客户，但在搜索"高优先级"工单时犯了一个基础的工具错误：

![](https://cubox.pro/c/filters:no_upscale()?imageUrl=https%3A%2F%2Fbaoyu.io%2Fuploads%2F2025-11-13-69096385d08b57dfaa27e513_f790744c.png&valid=false)

它试图把 "high" (高) 传给 "status" (状态) 参数，想以此找到高优先级的工单...... 这么做也许勉强能原谅，但问题是，明明有另一个参数就叫 "priority" (优先级)。

Mistral Medium 在搜索客户时就失败了，它把一个数组（array）传给了 "customer_id"：

![](https://cubox.pro/c/filters:no_upscale()?imageUrl=https%3A%2F%2Fbaoyu.io%2Fuploads%2F2025-11-13-6909639b2db60fff33d305da_ea4c0069.png&valid=false)

这纯粹是没遵守 MCP 模式，那个规范里清楚地定义了：这个参数需要的是一个字符串 (string)。

**在另一个例子中，这三个模型都在"制定和执行计划"上栽了跟头。**

任务提示： *SkyForge X670E Pro 这款产品被召回了。请给我一个列表，列出在 2025 年 8 月订购了该产品、且订单状态为"已履行"(fulfilled)、"已支付"(paid) 或"待处理"(pending) 的客户姓名。*

正确的工作流程是：

1. 使用 `searchProducts` (搜索产品) 工具，找到该产品的 ID。这个工具允许在产品记录中搜索文本并返回完整的产品信息。

2. 使用 `searchOrders` (搜索订单) 工具，找到包含该产品 ID 的相关订单。

   * 确保同时检查"已履行"、"已支付"和"待处理"三种状态。

3. 返回所有相关客户的列表。

Nova Pro 和 Mistral Medium 都在第一步就失败了；它们直接跳到了第二步，把产品名称（一个字符串）直接传给了 "product_id" (产品ID) 参数：

![](https://cubox.pro/c/filters:no_upscale()?imageUrl=https%3A%2F%2Fbaoyu.io%2Fuploads%2F2025-11-13-690963b15f45a96a85104914_e2131148.png&valid=false)

这表明它们没有正确推理"提示中给的信息"和"工具参数想要的信息"之间的关系。虽然我们无法确知模型到底在"想"什么，但它们的行为表明：它们似乎是选中了它们认为能一步到位的那个工具，然后把手头的数据硬塞进了***那个工具***看起来最 plausible (最像) 的参数里。

事实上，它们本应考虑所有可用的工具，确定哪些参数与它们 *实际拥有* 的信息相匹配，并规划如何 *组合* 这些工具来得出正确结果。

GPT-4o 做得稍好一点。它正确地找到了产品 ID：

![](https://cubox.pro/c/filters:no_upscale()?imageUrl=https%3A%2F%2Fbaoyu.io%2Fuploads%2F2025-11-13-690963c7b398885e36c56844_905f7129.png&valid=false)

然后去搜索订单：

![](https://cubox.pro/c/filters:no_upscale()?imageUrl=https%3A%2F%2Fbaoyu.io%2Fuploads%2F2025-11-13-690963c7b398885e36c56847_ae395338.png&valid=false)

然而，它只搜索了 "fulfilled" (已履行) 的订单，完全忘记了还有 "paid" (已支付) 和 "pending" (待处理) 的订单。

这又是一个简单的规划失败，遗漏了关键的"小目标"。

当然，这只是几个例子。错误使用工具或无法制定执行计划的方式有无数种。但这类基础错误，是那些没有针对"智能体行为"进行过训练的模型的典型表现。在模型能够可靠地推理工具、并将简单任务分解为小目标之前，去评估它们在智能体环境下的通用推理能力，是毫无意义的。

这就引出了下一步，当模型学会了制定计划和使用工具之后。

\## 适应性：当计划遭遇现实

恭喜，模型会做计划了。但现在，世界拒绝合作。欢迎来到"适应性"层：当现实打脸时，你得会更新计划。

即使模型能正确推理工具了，也不代表万事大吉。有时工具的文档可能写得不对，或者存在歧义，又或者模型需要更多信息才能制定完整的计划。当遇到意外结果时，能够及时调整、中途修改计划，是必须掌握的下一个技能。

目前的 Gemini 2.5 和 Qwen3 (通义千问3) 模型经常在这里出问题。它们执行了一系列合理的工具调用，但当某个步骤出错时，它们往往毫无反应。

**举个例子：** *"你好，我是 Penny Whitcomb。我想升级我的显卡，我通常用 Vortex Labs 这个牌子。你能帮我查查 RX820L 或 RX780 和我上一单的零件是否兼容吗？顺便告诉我一下这两款各需要多少钱？"*

正确的工作流程是：

1. 使用 `searchCustomers` (搜索客户) 工具找到 Penny 的忠诚度等级（用于确定价格）和客户 ID（用于搜索历史订单）。

2. 使用 `searchOrders` (搜索订单) 工具找到 Penny 上一单购买的产品。

3. 使用 `searchProducts` (搜索产品) 工具找到 Vortex Labs 显卡的产品 ID。

4. 使用 `validateBuildCompatibility` (验证装机兼容性) 工具检查新显卡与 Penny 之前购买的零件是否兼容。

当接到这个任务时，Gemini 2.5 Flash、Gemini 2.5 Pro 和 Qwen3 Max 都执行了正确的工具调用顺序。然而，当它们进行到第 3 步时，全都遇到了同一个问题：

![](https://cubox.pro/c/filters:no_upscale()?imageUrl=https%3A%2F%2Fbaoyu.io%2Fuploads%2F2025-11-13-690963e62a66d7331c7dfe46_55fe27df.png&valid=false)![](https://cubox.pro/c/filters:no_upscale()?imageUrl=https%3A%2F%2Fbaoyu.io%2Fuploads%2F2025-11-13-690963e62a66d7331c7dfe49_ff0d6638.png&valid=false)

它们在搜索这两款显卡时，什么也没搜到。原因很简单。它们在 "brand" (品牌) 参数里填的是 "Vortex Labs" (中间有空格)。而实际上，系统里存的品牌名是 "VortexLabs" (没有空格)。

![](https://cubox.pro/c/filters:no_upscale()?imageUrl=https%3A%2F%2Fbaoyu.io%2Fuploads%2F2025-11-13-690939dbf8147ed73bf3b6fd_355ba2af.png&valid=false)

我们应该期望模型提前知道这一点吗？当然不。问题在于 *接下来* 发生的事情。这三个模型都没有意识到出了问题，也没有尝试别的策略，而是把"空结果"当成了事实，然后回复客户说 Corecraft 公司不卖这些显卡。

相比之下，看看 Claude Sonnet 4.5 遇到同样问题时的表现，它 *适应* 了情况，并当场尝试了不同的搜索方法：

![](https://cubox.pro/c/filters:no_upscale()?imageUrl=https%3A%2F%2Fbaoyu.io%2Fuploads%2F2025-11-13-690963ffb93325a018ca6f11_928b3455.png&valid=false)![](https://cubox.pro/c/filters:no_upscale()?imageUrl=https%3A%2F%2Fbaoyu.io%2Fuploads%2F2025-11-13-690963ffb93325a018ca6f14_efc6b736.png&valid=false)![](https://cubox.pro/c/filters:no_upscale()?imageUrl=https%3A%2F%2Fbaoyu.io%2Fuploads%2F2025-11-13-690963ffb93325a018ca6f17_baa23bfe.png&valid=false)

我们可以看到 Claude 在**主动适应**情况，尝试不同的搜索参数。这正是人类会做的事。

那些较弱的模型虽然计划是对的，但它们"一条道走到黑"，遇到问题时不知道变通。在现实世界的任务中，适应和尝试不同方法是至关重要的，因为事情很少会第一次就完全按计划进行。

\## "接地气"：时刻紧贴现实

"接地气" (Groundedness) 是下一类失败------即模型始终"紧贴"当前上下文的能力：不"幻觉"**(即凭空捏造)** 出 ID，不"跑题"，不捏造脱离现实的"事实"。

尽管 Kimi K2 Turbo **(Kimi 智能助手的 K2 Turbo 模型)** 在规划和适应性上比 Qwen3 Max 和 Gemini 模型要强，但它在"接地气"、保持上下文一致性方面存在严重问题。

**例如，系统提示的第一行明确写着：**

![](https://cubox.pro/c/filters:no_upscale()?imageUrl=https%3A%2F%2Fbaoyu.io%2Fuploads%2F2025-11-13-690939dbf8147ed73bf3b71c_58246c80.png&valid=false)

尽管如此，Kimi 在调用工具时还是经常搞错年份。当被要求查找 8 月 25 日至 31 日的订单时，Kimi 搜索的是 2024 年的订单：

![](https://cubox.pro/c/filters:no_upscale()?imageUrl=https%3A%2F%2Fbaoyu.io%2Fuploads%2F2025-11-13-690964150f0e3d59aa4e9b7d_d698045d.png&valid=false)

然后，在给出最终回复时，Kimi 又切换回了 2025 年！

![](https://cubox.pro/c/filters:no_upscale()?imageUrl=https%3A%2F%2Fbaoyu.io%2Fuploads%2F2025-11-13-690939dbf8147ed73bf3b70f_fa6aa6ad.png&valid=false)

此外，虽然 Claude Sonnet 4.5 总体表现惊艳，但它在"接地气"方面仍然存在一些明显的问题，这也是它与 GPT-5 之间的一个主要差距。

**在一个例子中，Claude 明显"游离"了上下文，但它随后又设法"自我纠正"了**。Claude 需要查找在 9 月 30 日之前订购了产品、但尚未发货的客户的详细信息。在正确找到了一个相关订单后：

![](https://cubox.pro/c/filters:no_upscale()?imageUrl=https%3A%2F%2Fbaoyu.io%2Fuploads%2F2025-11-13-6909642e1f6e1428d1c48a06_c539d271.png&valid=false)

Claude 接着试图用一个明显是 *捏造* 出来的电子邮件地址去搜索客户详情：

![](https://cubox.pro/c/filters:no_upscale()?imageUrl=https%3A%2F%2Fbaoyu.io%2Fuploads%2F2025-11-13-6909642e1f6e1428d1c48a0a_106d622e.png&valid=false)

然而，当这次尝试失败后，Claude 确实设法自我纠正了，再次显示了它强大的适应性：

![](https://cubox.pro/c/filters:no_upscale()?imageUrl=https%3A%2F%2Fbaoyu.io%2Fuploads%2F2025-11-13-6909642e1f6e1428d1c48a0d_99b7df09.png&valid=false)

虽然 Claude 这种适应和修复错误的能力令人印象深刻，但它难以"锚定"在当前上下文中的问题，对于任何期望在现实中运作的智能体来说，都是一个隐患。

**另一个例子表明，更微妙的"不接地气"问题更难被发现**，并且在某些情况下，会悄悄溜进最终答案。

Claude 被要求查找支持工单并报告它们的优先级。它正确地调用了工具来查找所有"普通"(normal) 优先级的工单：

![](https://cubox.pro/c/filters:no_upscale()?imageUrl=https%3A%2F%2Fbaoyu.io%2Fuploads%2F2025-11-13-6909645b3528625fc6ea9d14_4b0306b4.png&valid=false)

在工单列表中，有以下两条：

![](https://cubox.pro/c/filters:no_upscale()?imageUrl=https%3A%2F%2Fbaoyu.io%2Fuploads%2F2025-11-13-6909645b3528625fc6ea9d17_60ba79bd.png&valid=false)

两条都清楚地标着 "normal" (普通) 优先级。但这并没有反映在 Claude 的最终回复中：

![](https://cubox.pro/c/filters:no_upscale()?imageUrl=https%3A%2F%2Fbaoyu.io%2Fuploads%2F2025-11-13-690939dbf8147ed73bf3b74a_0fd5870f.png&valid=false)

它不仅错误地将它们列为"高优先级"(high priority)，还在"普通优先级"(normal priority) 部分重复了它们，但又说它们"已在高优先级中列出"。这个回复不仅脱离了上下文（不接地气），它甚至连内部逻辑都不自洽。

\## 常识推理：最后的边疆

当一个模型能够可靠地使用工具、有效规划、随时调整计划，并且始终"接地气"之后，还剩下最后一道屏障，将即便是最强的模型与"人类水平"的表现区分开来：**常识推理 (Common Sense Reasoning)**。

我们现在正进入更模糊的"AGI"**(通用人工智能)** 领域。常识推理不是一个定义清晰的概念，但对于通用智能体来说，它至关重要。它就是"通用智能"里的那个"通用"------那些你无法明确训练的东西：当它们面对一个陌生情况时，它们表现得到底好不好。到了这个阶段，模型已经能可靠地作为智能体行事并保持连贯。现在的问题是，它到底有多 *聪明*？

在这次测试中，常识推理问题是导致 GPT-5 的表现与人类水平产生差距的主要原因。

**这里有一个 GPT-5 失败的例子，不是因为规划或工作流程出了问题，而是一个简单的常识推理问题。**

任务： *请识别出当前分类为"其他"(other) 的支持工单中，有哪些应该被重新分类为"退货"(returns)。*

GPT-5 正确地调用工具找到了相关的工单，包括这一条：

![](https://cubox.pro/c/filters:no_upscale()?imageUrl=https%3A%2F%2Fbaoyu.io%2Fuploads%2F2025-11-13-69139ba2f4833167a03c7eda_6e0a5d74.png&valid=false)

这个工单应该被重新分类，但需要一点常识推理才能明白为什么：

* 首先，客户要求退款 (refund)，所以这可能是一个 *退货* (return) 或 *取消订单* (cancellation)。

* 但"包裹几小时前刚到"(the package showed up a few hours ago) 这句话提供了关键线索：他们已经 *收到* 货了。

* 这个细节明确无误地表明，这应该是一个"退货"。

GPT-5 没能做出这个推断。它收集了所有正确的信息，但没有把这些点联系起来，最终的回复中漏掉了这个工单。

**另一个 GPT-5 因推理问题而失败的例子**，是识别哪些客户可能是"游戏玩家"(gamers)。任务建议去查找那些"购买了 GPU、带 GPU 的预装整机，以及提到'游戏'(gaming) 字样的产品"的客户。

使用建议的启发式方法 (heuristics) 是明智的，即：1. 识别游戏相关类别的产品（如 GPU）；2. 识别产品描述中包含"游戏"字样的产品；3. 然后搜索 8 月份包含这些产品的订单。所有这些都可以用现有工具实现。

但 GPT-5 偏不。它费力地 *一天一天* 地搜索 8 月份的所有订单，以避免超出搜索结果的最大数量限制。

![](https://cubox.pro/c/filters:no_upscale()?imageUrl=https%3A%2F%2Fbaoyu.io%2Fuploads%2F2025-11-13-690964828dd7a566ec24d5c4_065af631.png&valid=false)![](https://cubox.pro/c/filters:no_upscale()?imageUrl=https%3A%2F%2Fbaoyu.io%2Fuploads%2F2025-11-13-690964828dd7a566ec24d5d4_322541b7.png&valid=false)

...如此往复，整整 31 天。

然后，它对这些订单中的特定产品使用 `getProduct` (获取产品) 工具，以获取更多详细信息，并判断其是否与游戏相关。然而，它试图根据产品 *名称* 来猜测是否与游戏相关，因为它没有搜索出现的每一件商品，只搜索了那些产品 ID 中包含 "graph" (图形) 或 "gaming" (游戏) 的商品。Claude 也用了完全相同的方法，问题也一模一样。

GPT-5 的行为是连贯的，也执行了一个计划，但这个计划并*不聪明*。

**最后，这个案例中 GPT-5 误解了任务**，这本是可以通过一点常识推理来避免的。

任务提示： *"我玩游戏时一直掉帧，所以想升级 GPU。900 美元以下我能买到的最高端 GPU 是什么？请提供价格和所有规格。我账户上的名字应该是 Sarah Kim。"*

GPT-5 正确检索了产品信息，但 *忘记* 了去检查"Sarah Kim"的客户记录，以查找她的忠诚度等级和个性化定价。相反，它回复了一段通用的政策信息：

![](https://cubox.pro/c/filters:no_upscale()?imageUrl=https%3A%2F%2Fbaoyu.io%2Fuploads%2F2025-11-13-690939dbf8147ed73bf3b753_c299e15a.png&valid=false)

根本原因很简单：它没能推断出 *客户就是 Sarah Kim* 。它把"我账户上的名字应该是 Sarah Kim" (My name under my account should be set to Sarah Kim) 这句话，理解成了一条 *更改账户名称* 的指令，而不是一个关于 *请求者身份* 的线索：

![](https://cubox.pro/c/filters:no_upscale()?imageUrl=https%3A%2F%2Fbaoyu.io%2Fuploads%2F2025-11-13-690939dbf8147ed73bf3b757_a54a0e4f.png&valid=false)

这句话本身单独看确实有歧义，但在上下文中，含义是清晰的，而且模型本可以用可用的工具来消除这种歧义。让我们来运用一下常识推理：

* 客户没有提供任何其他信息来查询她的客户记录。

* 使用 `searchCustomers` (搜索客户) 工具本可以发现一个名叫 "Sarah Kim" 的现有客户。

* "更改账户名"这个操作与任务的其余部分（查显卡、查价格）完全无关；而"查询她的忠诚度等级"则与她要求的"价格信息"密切相关。

所有这些本应让正确的意图变得清晰明了。再次强调，这不是一个策略或执行上的错误，这只是在当前环境和任务上下文中，没能进行一次聪明的、合乎情理的推理。

\## 那么，这是否意味着 GPT-5 已接近"人类水平"？

好吧，也许第一张（金字塔）图不完全准确。真相可能更像这样：

![](https://cubox.pro/c/filters:no_upscale()?imageUrl=https%3A%2F%2Fbaoyu.io%2Fuploads%2F2025-11-13-690939dbf8147ed73bf3b75a_6775098a.png&valid=false)

换句话说，精通了前四个层面（工具、规划、适应性、接地气），并不意味着模型就达到了"人类水平"，可以胜任现实世界的工作。它们仅仅代表了任何智能体 *必须* 掌握的基础能力，只有掌握了这些，我们才能 *开始* 讨论它在真实环境中的常识推理表现如何。

常识推理目前还不是一个可以被清晰定义的东西，但当它缺失时，你一眼就能看出来。它最终是会被证明为一组可识别、可训练的子技能，还是大规模真实世界训练后的一种"涌现"属性？这还有待观察。找出答案，将塑造 AI 发展的下一个阶段。

2025 年是"智能体之年"，但这并不意味着这是我们实现通用强智能体的那一年。相反，这是"智能体们终于能足够连贯地行动，以至于我们可以开始分析和讨论它们的常识推理能力"的元年。

摆在我们面前的挑战，是训练和分析这些正迅速接近我们自己（人类）的智能。至于需要多长时间才能最终弥合这一差距，还是一个悬而未决的问题。

*** ** * ** ***

来源： <https://surgehq.ai/blog/rl-envs-real-world>

[Read in Cubox](https://cubox.pro/web/card/7389934316072996414)
