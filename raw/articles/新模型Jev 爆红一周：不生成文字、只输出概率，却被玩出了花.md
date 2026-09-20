---
title: 新模型Jev 爆红一周：不生成文字、只输出概率，却被玩出了花
source: https://mp.weixin.qq.com/s/Ra3NBisCf95zFhlCbXZDZA
author:
  - "[[何码先生]]"
published: 2026-09-20
created: 2026-09-20
description: 先说结论大语言模型在聊天上超过人类，已经好几年了。可自动化到底在哪？这个问题 Diogo Almeida 追了四年。
tags:
  - clippings
  - LLM
---
何码先生 代码的使命 *2026年9月19日 16:56*

先说结论

大语言模型在聊天上超过人类，已经好几年了。可自动化到底在哪？

这个问题 Diogo Almeida 追了四年。他在 OpenAI 参与搭出的那套方法，后来成了 ChatGPT 的地基。2024 年他离开，创办 TypeSafe AI，隐身开发两年，2026 年 9 月 15 日带着 4000 万美元种子轮和第一个模型走了出来。

模型叫 Jev。它最扎眼的设定是： **它不生成文字** 。你没法跟它聊天，它不写解释、不写代码、不总结文档。你给它一段状态，再给它一组提前定义好的问题，它还你一组带概率的选择。

发布帖在 X 上两天拿到大约 3300 万次浏览。接下来这一周，我大概读了一百来个围绕它的帖子和仓库，发现一个挺说明问题的现象：官方的宣传材料全在讲「快 193.6 倍、便宜 444.6 倍」，而 X 上的开发者基本没人在意这两个数。他们在干的事是，把 Jev 塞进 Agent 的每一个判断点、塞进浏览器、塞进交易机器人、塞进 PostgreSQL，甚至有人为它写了一门编程语言。

所以这篇分四块。前五节把原理讲透：接口是怎么设计的、为什么「不会幻觉」这句话要拆开听、它换了什么训练目标、快和便宜从哪来。中间五节看这一周真实长出来的东西。然后是审计，把能信的和不能信的分开。最后落到架构上，说它该待在软件的哪一层。

下面出现的截图和动图都来自项目自己的仓库，不是示意图，来源我一条条标在图注里。也许大家早看过其他博主的介绍文章，但本文除了Jev模型的介绍还有一些Jev有关的落地应用介绍（从第六章开始），文章比较长，大家可以挑感兴趣的部分看。

01.

先看看一个 Agent 一天到晚在忙什么

Anthropic 讲 Agent 时用过 self-directed loop 这个说法：计划、行动、观察、调整，反复循环，直到达成目标。

如果你真去读一遍生产环境里跑着的 Agent 的调用日志，会发现这个循环里塞满了判断点：

![图 1 ｜ Agent 循环里真正的负载是判断，不是写作](https://mmbiz.qpic.cn/sz_mmbiz_png/9uWm17ydXxkzBiaKV4MAiawEmW9pgGaq5SBKTeWOicKp7AjswwKfERc4IKLlqFmNpiaeGSm1Nx9ptpjqAibplPiasX9SgX1ShnlxI6npeLl3vVicicQ/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

图 1 ｜ Agent 循环里真正的负载是判断，不是写

这一串问题里，没有一个需要「写」。全都要「选」。

但过去两年，我们把它们统统交给了同一个生成模型。分类问它，审核问它，工具选择问它，不知道下一步干什么还是问它。理由很充分：一个模型解决所有问题，不用为每个环节单独训模型。

这笔账的另一面是隐性的。你等 8 秒拿到一段话，再用正则或解析器从话里抠出一个标签。更麻烦的是抠不出来的时候。

Beam AI 复盘自家 Agent 的失败案例时发现，影响最大的单一失败模式是工具选择错误：Agent 挑错了工具，或者干脆挑了一个不存在的工具。它排第一的原因是它会安静地毁掉整条链路，不读 trace 根本发现不了。

顺着往下想一层就够了：让一个生成模型回答「我该调用哪个工具」，理论上它可以编出一个不存在的工具名。因为它在生成 token，任何 token 都合法。下游程序拿着 analyze\_sentiment 去工具注册表里查，查不到，流程断在这里。

于是问题变成：这套下判断的活，真的需要一个以生成为核心能力的模型来干吗？

02.

Jev 的接口长什么样

比你想的简单。一次请求就两部分。

**state** ，要判断的原料。字符串、JSON 对象、JSON 文本数组都行。比如一条客服消息加上订单历史。

**questions** ，你要它做的判断。每个问题有个自己定的 ID、一个类型、一段 instructions，Choice 和 Score 还要给 criteria。

![图 2 ｜ Jev 的输入输出契约](https://mmbiz.qpic.cn/mmbiz_png/9uWm17ydXxnBoxw2KOMQQQiag76ffLd1mtIENSVxeicHquHLyNF26oD5VIcfL5bLfMcH14ibat7ybLmAHRe8NFibQZIOBs0P1iaxqaVLvCawVIPQ/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=1)

图 2 ｜ Jev 的输入输出契约

问题只有三种类型，官方管它们叫 primitives。

| 原语 | 问的是什么 | 返回什么 |
| --- | --- | --- |
| Noul | 一句是非命题成不成立 | 0 到 1 的概率 |
| Choice | 从预设选项里选一个（最多 255 个） | 选中项 + 完整概率分布 + confidence |
| Score | 落在有顺序的量表哪一档（2 到 10 层） | 分数 + 概率分布 + confidence + legend |

看个真实的返回长什么样。

请求 · Choice

{ "department": { "type": "choice", "instructions": "这条消息该由哪个团队处理？", "criteria": { "billing": "账单、发票、退款、订阅", "technical": "故障、报错、集成问题", "sales": "报价、升级、新开户", "other": "以上都不是" } } }

返回

{ "department": { "type": "choice", "choice": "billing", "probabilities": { "billing": 0.84, "technical": 0.15, "sales": 0.0, "other": 0.01 }, "confidence": 0.6 } }

看完返回，再看一眼它在代码里是什么样子，差别更直观。

写法上的差别，一眼就能看懂

\# 传统写法：确定性条件 if transaction.amount > 10000: review() # Jev 写法：概率条件 if jev("这笔行为看起来可疑吗？") > 0.95: review()

这段对比比任何 benchmark 图都好懂。大部分软件本来就是一个巨大的 if 树，我们只是过去没有一种便宜办法，让 if 的条件读懂模糊的人类语境。

X 上 @paarangatrai 有句话概括得挺好：LLM 生成答案，Jev 做决定。听着差别很小，但它改变的是一类软件的写法。

剩下三个细节值得单独拎出来。

问题之间互不成为上下文

所有问题共享同一份 state，但独立并行求值。第 3 个问题的答案不会进入第 4 个问题的上下文。官方说他们测过批量提问的影响，除了模型自身的采样噪声，没发现额外偏差。这一点和 LLM 里「上下文越长越容易被前面的话带偏」的直觉正好相反。

你起的 ID，模型看不到

上面那个 department 只是给代码用的 key，不会发给模型。所以别指望一个「看起来自解释」的 key 能省下那句完整提问，instructions 该写清楚还得写清楚。

窗口不大，这个限制是真的

state 加所有问题共享大约 64k token 的预算，而 state 加最长的那一个单独问题必须能塞进 32k，大概 15 万英文字符。放在长上下文模型动辄几十万上百万 token 的今天，这个数字显得很小。它也只读文本，没有图像、音频、视频。

03.

「不会幻觉」是真的吗？

这是宣传里最容易被误读的一句。TypeSafe 在结构化输出和工具调用的测试中把错误率标成了 0%。但他们自己在注脚里写得很直白：这个 0% 不是跑出来的经验数据，是 schema matching 的机制保证。

所以准确的说法是： **Jev 无法输出你没定义过的东西** 。

你在 Choice 里给了 billing、technical、sales、other 四个选项，它就吐不出第五个。合约说这里要数字，它就写不出诗。错误被围在一个你预先划定的空间里。

但围在笼子里的错还是错。如果正确答案是 B，它照样可能很自信地选 A。「不会幻觉」跟「判断正确」是两件不同的事。官方文档自己也写了：类型化不等于正确。

我的判断

这个承诺被过度包装了，但它的内核是有价值的。真正毁掉一条无人值守链路的，常常是输出根本没法解析，判断差那么一点反倒没那么致命。把这一类失败彻底消掉，在工程上是实打实的进步，只不过它跟「模型不会说假话」是两码事。

要理解这个结构性保证值多少钱，得先想清楚 LLM 为什么会跑偏。

LLM 的本职工作是预测下一个词。它估计的是「这个 token 跟前文搭不搭」，而不是「这句话跟现实符不符合」。一旦它编出一家看着挺合理的公司名，后面接 Inc. 的概率就高得离谱。语言上一切正常，企业注册处未必同意。

更关键的一点：模型内部本来是有概率的，但接口只把成品文字递给你。概率帮着模型继续往下说，却没帮着程序决定该不该动手。

工程界的反应是加约束。别让它写作文，让它填表。于是有了 JSON mode、Structured Outputs、各种 schema。LLM 终于穿上西装，看着像能上生产了。

可 JSON 只管格式，管不了判断。你的程序知道结果是 billing，但它不知道模型是以 95% 的把握选的，还是在 billing 和 technical 之间抛了一枚读过很多书的硬币。

换个角度更明显。你直接问 LLM「你有多自信」，它回你一个 0.9，那个 0.9 同样是生成出来的字符串。JSON 能保证 0.9 是个数字，保证不了这个数字配得上 0.9。

![图 3 ｜ 输出契约决定了错误被围在哪](https://mmbiz.qpic.cn/sz_mmbiz_png/9uWm17ydXxnbybYwQoqthdcepQpWnVJxEibNeCRM7lLhYviauep9g5TOq9uWesd9zAQr0A8uEia6D4TYQBykRB63vibA1nlSYmaoRZibbDSFSbhE/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=2)

图 3 ｜ 输出契约决定了错误被围在哪

接口和「不会幻觉」这两件事讲到这儿就完了。围绕它们最常见的五个误解，X 上 @paarangatrai 那篇长帖拆得比官方材料诚实，我转述一下要点。

五个常见误解，逐个拆

**它不是分类器。** 输入可以是混乱的真实上下文，而且你可以在同一份输入上一次问多个问题：是不是欺诈、会不会流失、要不要升级、够不够格、优先级多高。  
  
**它也不替代 GPT 和 Claude。** 比较合理的架构是：Jev 决定该发生什么，Claude 和 GPT 在需要更深思考时出手，普通代码执行确定性的部分。Jev 变成路由层。  
  
**「不会幻觉」要加限定。** 如果允许的答案是低 / 中 / 高，Jev 不会突然发明一个「超高」。但如果正确答案是「中」，它给你一个 92% 置信的「高」，那还是错的。  
  
**「为什么不直接让 LLM 返回 JSON」。** 你可以，而且我们到处都在这么干。但你还是要处理生成延迟、schema 校验、重试、奇怪输出、置信度估计和一堆胶水代码。  
  
**为什么该在意。** 因为大部分软件本来就是一个巨大的 if 树。Jev 问的其实是：如果这些 if 的条件能读懂模糊的人类语境，会怎样。

04.

换个训练目标，让概率诚实

Jev 用的训练方法叫 RLCD，Reinforcement Learning for Calibrated Decisions，校准决策强化学习。

理解它最好的办法，是把三条路线并排看。

![图 4 ｜ 三条训练路线的优化目标](https://mmbiz.qpic.cn/mmbiz_png/9uWm17ydXxkVU9WwRUQI3DicnRXCur0eM4JXicPOKyJOtsdNsHxe8kPStphwoE01R0rCSMFzyAJhSOfR5XCt8OeUsk8ZAPzMo5EDyUsWjo3Ck/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=3)

图 4 ｜ 三条训练路线的优化目标

说得更准一点： **校准是对一组预测的统计承诺，它管平均值，不管单次** 。一次标着 0.95 的判断完全可能错。但如果模型在一千次标着 0.9 的判断里错了三百次，那个 0.9 就是装饰品。

训练出这种性质用的数学工具并不新，而且相当老派：proper scoring rules，严格适当评分规则，常用的有 cross-entropy 和 Brier score。评估指标里常提的还有 Expected Calibration Error（ECE）和 reliability diagram。映射到 Jev 的三种原语上也不复杂，Noul 本质是个二元概率，Choice 是候选上做 softmax，Score 是个序数分类问题。

东西不新，新的是把它当成一个前沿实验室的主线目标，并且配上一套非自回归的架构和解法。TypeSafe 想赌的是，这条路能通到「前沿智能」那一档，而不是停在「小分类器」那一档。

校准能拿来干什么？想想你的路由逻辑。

python · 置信度门控

ROUTE\_CONFIDENCE = { "deterministic\_code": 0.90, "fast\_llm": 0.80, "reasoning\_llm": 0.75, "human\_review": 0.00, } route = response.answers\["route"\] if route.confidence < ROUTE\_CONFIDENCE\[route.choice\]: return "human\_review" return route.choice

这段代码的价值不在于模型多聪明，而在于它把「模型有多确定」变成了程序可以比较的量。你可以给不同的路由设不同的门槛，让不确定的案例自己走到人工那一支。

不过有个坑得说清楚： **confidence 不是授权** 。一个 0.97 不能用来批准一笔付款、绕过一条风控规则。它只是一个路由信号。官方文档也写了，Choice 和 Score 的 confidence 是从概率分布的形状推出来的，它不构成「选中项正确」的证明。

05.

快和便宜是怎么来的

先摆数字。

| 指标 | 官方公布值 |
| --- | --- |
| 端到端延迟 | 70 至 500 毫秒，典型约 100 毫秒 |
| 输入价格 | 0.042 美元 / 百万 token |
| 输出价格 | 免费。官方原话是 too cheap to meter |
| 宣传倍速 | 快 193.6 倍，便宜 444.6 倍 |
| 当前模型 | jev-1.13.0，仅文本，64k 总预算 |

那两组倍速数字来自他们自己的四项工作流评估，官方同时标注了它们代表现实收益的上限。来路的问题我后面专门说。

算笔账会有感觉。一条 300 token 左右的工单，判断一次大约 0.0000126 美元。十万张工单，一块二毛六。

官方演示里更极端的一个：一个玩《毁灭战士》的 bot，每秒约 10 次判断，跑一小时大约 7 美元。还有个维基百科竞速的 bot，每一步要从几百个链接里挑一个，它永远不会选到不存在的链接，因为它只能从候选集里选。

速度快在哪？LLM 逐个 token 预测，天然串行，一句话说完才能说下一句。Jev 则把同一状态上的所有问题一次性并行求解，真正省掉的是整条等待链，单步算力倒在其次。Almeida 的比方是用 transformer 替掉 RNN 式的串行计算。

![图 5 ｜ 省下的是等待链，不是单步算力](https://mmbiz.qpic.cn/mmbiz_png/9uWm17ydXxlRstMmBtM78m3iby6CTYS70kU6vsoyMglhsBkumN2xico2h2iaBWnAtQzhxVY8e71lvEFhxmkeSOPSIoz6aPk9Gz2cNA0831l2YI/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=4)

图 5 ｜ 省下的是等待链，不是单步算力

把这两件事放一起，会得出一个反直觉的结论。Jev 的卖点压根不在它比前沿模型聪明，它不比。卖点是 **便宜到你可以把它塞进每一次判断里** 。

这引出一个以前不成立的场景。逐轮校验 Agent 的每一步：这次工具调用跟上一次矛盾吗？这个输出跟用户说的意图一致吗？这里该不该亮个黄灯？这些事用前沿模型早就能做，只是规模上贵得荒唐。当单价掉到 0.042 美元一百万个 token，它从成本决策变成了默认动作。

06.

这一周，X 上的人把 Agent 的零件换了一遍

原理说到这儿就够了。接下来看真实发生的事。发布之后一周，X 上最扎堆的一类项目是给 Agent 换零件：把一个 Agent 跑一轮中间那些要拍板的地方，一个个替换掉。

![图 6 ｜ Jev 在 Agent 里的六个真实落点](https://mmbiz.qpic.cn/mmbiz_png/9uWm17ydXxk4gechMs8eTLiaib9T9icYLUnnEHkicdiamVQywFc1Z5PUxGAgM2glj2yuBBSoIibpjHiav9iaXJCF6bYQo82icc8sAwyQ0h7K4ickBhvh0/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=5)

图 6 ｜ Jev 在 Agent 里的六个真实落点

工具选择

这是最热的一个。开发者 Mohit Karekar 在做一个浏览器里跑本地模型的 Agent：用 WebLLM 加载 Qwen3 8B，工具来自用户配置的 MCP 服务。麻烦在于模型太小，Qwen3 8B 在 WebLLM 里不支持直接的工具调用，他只能把工具列表整个塞给模型让它选，很慢。

接上 Jev 之后流程变成：Agent 循环问 Jev 两个问题，选哪个工具、参数该用哪个候选值，Jev 秒回，执行工具，再把工具结果和原始消息交给 Qwen3 生成回答。他贴出的返回里，Jev 对 get\_me 这个工具给了 0.91 的置信度。

我的判断

这个案例的价值在于它点出一种新分工：本地小模型负责写，云端 Jev 负责选。小模型不擅长的事，不一定要换个更大的模型来解决。

命令安全审查

Vercel 的 CEO Guillermo Rauch（@rauchg）发了条帖子：他们那个 fx 的默认模式是 auto，每条命令都要过一个安全审查器。审查器原来跑在 GPT Luna 上，换成 Jev 之后 p95 快了 18 倍，而且更准。他还说 Jev 要进 Vercel AI Gateway，很可能成为新的默认。

这条信息的分量比大多数 demo 重，因为它说的是一个有人在真实流量上跑过、并且打算改成默认配置的位置。事实上 Vercel 的 AI Gateway 已经上了 typesafe-ai/jev 这个模型标识，AI SDK 7 里可以用 evaluate 直接调。

模型路由

给 Claude Code、Codex 这类工具决定每一次请求该走便宜模型还是贵模型。有人做了 jev-router，有人在给多 Agent 系统做「值班调度」：Jev 读任务，决定该叫醒哪个子 Agent、给它配哪个模型。思路是一致的，路由本身就是一个判断，没必要用推理模型来推理该不该用推理模型。

上下文压缩

tamaratran 做了 fast-jev-compaction，思路是不再用「总结」来做压缩，而是让 Jev 给每一次历史工具调用打分，把不相关的丢掉、保留有用原文。Alex Volkov 实测：一个 Claude 会话从近 100 万 token 压到 86K，耗时 1 秒。

细节值得记一下。压缩质量的关键不在于能不能总结，而在于能不能判断哪些东西以后还用得上。后者本来就是个判断，用生成模型去做属于降维打击。

行动前自查

DevMortimer 的 pi-warden 放在 Agent 和工具之间，执行前让 Jev 评估这件事是否不可逆、是否偏离原计划、有没有外部后果、是不是陷入了重复循环。他说自己在 17000 次工具调用上跑过这套检查。OpeOginni 的 OpenCode 权限插件是在允许访问某个域名之前先检查 Agent 的意图。Ian Nuttall 做了个叫 jev-review 的 MCP 插件，让 coding agent 边干活边被评分、然后迭代。

同一个名字底下还有个完全不同的项目。Dev Agrawal（@devagrawal09）的 Jev Review 走的是分阶段审查：先让 Jev 用 Noul 给每个文件在正确性、安全性、可靠性、兼容性、测试缺口五个维度上各打一个概率，形成一张矩阵；再从矩阵里最强的信号决定往下看哪几个文件的哪几段 diff；选中证据之后才分类问题机制、打严重程度分、路由给对应的审查角色。整条编排链写在代码里，Jev 只承担其中每一次有界判断。

![Jev Review 仪表盘](https://mmbiz.qpic.cn/mmbiz_jpg/9uWm17ydXxlqVxaobr33jULicVojRmLIiaWGMf338Oakb6sltfKlpfp9ooNuea6TkrMmXC00o2AiabibxLD7olFstiaT9QoHK4cEaWD1XLCPia4uM/640?wx_fmt=jpeg&from=appmsg&watermark=1#imgIndex=6)

图 7 ｜ Jev Review 的本地仪表盘

上半部分是工作流漏斗：65 个格子筛出 4 个信号，逐级收敛到 1 处问题。下半部分就是 Noul 矩阵，五个维度各一格概率，最深的那两格是 server.ts 的 0.83 和 api.ts 的 0.81  
素材来源：github.com/devagrawal09/jev-review

这张图值得多看两眼的地方是下半部分。它把「这个文件有没有问题」这种没法直接回答的问题，拆成了五个维度上的独立概率，再让代码去决定用哪个维度作为往下走的线索。这就是前面说的「有界判断」。模型只负责在定义好的格子里给出数字，剩下的事都是普通程序干的。

这一类的共同点很清楚：把那些「肯定要做的判断」从生成模型里剥出来。它们不改变 Agent 能做什么，只是让它更快、更便宜、更少跑偏。

07.

浏览器和电脑操作，这一周最出圈

最热的是 Browser Use 团队（@gregpr07）的 jev-ultrafast。它把网页变成一个编号的元素表，然后让 Jev 选「做什么操作、操作哪个元素」。操作集是预定义好的：点击、输入、滚动、选择、等待、完成、被挡住。只有需要打自由文本的时候，才叫一个小模型来生成。

![jev-ultrafast 航班搜索演示](https://mmbiz.qpic.cn/mmbiz_gif/9uWm17ydXxleKk8CNOWkUjZIPxZuQY023NHicLTsTQZvCtAiarMpAsC3gicIzUGxZIiayK7MpweUOXu1ibZJmQhvNibX6apDwmYzmvwu3YicDiaYu1Q/640?wx_fmt=gif&from=appmsg#imgIndex=7)

图 8 ｜ 真实 Google Flights 上跑一次机票搜索（动图，1 倍速）

右边计时器是原始时间戳，不是后期配的。截图这一帧停在 3.77 秒，正在选 9 月 20 日。底部那行小字写着操作由 Jev 选择、文本由 mercury-2.5 生成、计时包含等待  
素材来源：github.com/browser-use/jev-ultrafast

他们演示了在真实 Google Flights 上找苏黎世到伦敦的航班：7.1 秒，0.0039 美元。Gregor Zunic 的帖子里把「7 秒」和「不到半美分」放在最显眼的位置，两天内被转了很多次。

![图 9 ｜ jev-ultrafast 的单循环结构](https://mmbiz.qpic.cn/mmbiz_png/9uWm17ydXxlYiaPMFvvV8KzSljxmXLcuUsym2Wn9kjFLFMw9mASdkYUtj4Qsef3OxQebdP6SOMfgNNgfWQEFCSZrKUqZxiaKBk5Aich87yXo6Q/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=8)

图 9 ｜ jev-ultrafast 的单循环结构

这个数字值得拆一下，拆完你会发现它没那么神。项目仓库里的测量文件写得很细：整个流程 7073 毫秒，其中 Jev 请求 17 次共占 3.72 秒（约 53%），两次自由文本生成 927 毫秒，其余时间花在页面快照、DOM 执行和客户端环境上。计时从初始观察之后、第一次模型调用之前开始，到 DONE 被接受为止，不含浏览器启动和初始导航。

项目自带的 inspector 把每一次决策都摊开了，这也是我觉得它比多数 demo 有用的地方。

![jev-ultrafast inspector](https://mmbiz.qpic.cn/mmbiz_jpg/9uWm17ydXxkocESVphyE19pzELic3uFfAEzIpwEJE13YsREeiaVwCibpue6PhqibnEevNRAuNcQw9dicyENIkiaOGpWiaa7rWawSCaOu5Dp0xubmzI/640?wx_fmt=jpeg&from=appmsg&watermark=1#imgIndex=9)

图 10 ｜ inspector 里的单步决策

右侧这一栏是本篇最值得看的一张图。这次决策花了 351 毫秒，目标置信度 91%，操作层的分布是 CLICK 76%、TYPE\_TEXT 23%、BLOCKED 1%。下面按概率排好序的元素表里，19 号元素 93% 领先，22 号 6%，23 号 1%  
素材来源：github.com/browser-use/jev-ultrafast

看到这张图应该能明白「概率条件」到底长什么样了。一个答案加一个信心指数，那是另一回事。它交出来的是一整条从高到低排好序的候选链。你的代码可以自己决定在 93% 处停下，也可以退到 76% 处取更保守的策略，这个开关在程序手里，不在模型手里。

而且 DONE 是由同一个策略模型选的，「任务成功」由计时器之外的独立路线检查来确认。仓库里那张收尾截图把五项检查都打上了勾：单程、苏黎世、伦敦、9 月 20 日、结果已可见。他们确实做了这个检查，比不少 demo 严谨，但流程上仍然有自己给自己阅卷的成分。

![7.07 秒完成的结果](https://mmbiz.qpic.cn/sz_mmbiz_jpg/9uWm17ydXxkc8WFshT9RcJmh6EgT4kHcLPO5Reumsk2u7yTgg9obg1qf7j2En13YmmabqLskxUlOLthMXkAtO6aQPOnqibmta4sL5Ap8WnN8/640?wx_fmt=jpeg&from=appmsg&watermark=1#imgIndex=10)

图 11 ｜ 收尾一帧：07.07 秒，五项检查全绿

注意右下角那个数：178 毫秒的中位决策延迟。这一趟一共做了 17 次判断，每一次都得在两百毫秒上下交卷，这才是「7 秒」真正依赖的东西  
素材来源：github.com/browser-use/jev-ultrafast

成本上还有个反直觉的地方：总共 0.0039 美元里 98% 花在 Jev 上，因为每一步都要把整份 state 重发一遍，比那两次短文本生成贵得多。第三方做过一次对比，同样的浏览器任务，Jev 版配置快了 31% 到 43%，但也贵了 38% 到 51%。

同一类里还有几个挺有意思的。

jkudish 的 jev-browser 走的是另一个极端，它没有网页界面，只把每一步判断直接打成一行日志：这一步是点击还是输入、选中了哪个元素、置信度多少、有没有偏离目标、有没有卡住。

![jev-browser 判断轨迹](https://mmbiz.qpic.cn/sz_mmbiz_gif/9uWm17ydXxmE2bn8HCar6uIeGO1mcaA0MyWT6roMbuxWlQiabbWXib0lD7aOxuN2F16xUvvaMtFophLSf2h4iadjGS4DHvCoyJA2HEnwic0n8Mo/640?wx_fmt=gif&from=appmsg#imgIndex=11)

图 12 ｜ jev-browser 的判断轨迹（动图）

左边是它在操作的 GitHub 页面，右边是每一步的返回。第一步 click\_e8 的置信度是 0.99，第二步 type\_e1 多出了 goal 和 stuck 两个概率头，分别表示「有没有在朝目标走」和「是不是卡住了」。底部一行写着 provider cloudflare、model jev-1.13.0、总耗时 7.0 秒  
素材来源：github.com/jkudish/jev-browser

多出来的这两个头挺关键。LLM 版的 Agent 最麻烦的地方就是它卡住的时候自己不知道，你得在外面加一层检测超时和重复的启发式规则。Jev 把它变成同一个请求里的另一个问题，一次网络往返一起拿回来。

Kyle Jeong（@kylejeong）用 Jev 加 Stagehand 做计算机操作，一个任务 0.001 美元。Zachi（@iam\_zachi）做了一套更极端的版本：不传截图、不调 LLM。本地 CoreML 模型分割屏幕上的按钮和 UI 元素，端上 OCR 读标签，只把文字给 Jev，Jev 返回点哪个的概率。他说大约 90 毫秒一次决策，比他用过的任何 LLM 计算机操作都快，而且像素永远不出本机。

droidrun 的 mobile-jev 把这套逻辑搬到安卓，演示里 9 个动作、约 21 秒下完一单 Uber。Oskar（@o\_kwasniewski）在做用 Agent 跑端到端测试的开源框架，Web 和移动端都要覆盖，移动端恰好是过去最难做的部分。

Zachi 那个方案方向上最有意思，因为它把「看屏幕」和「做决定」彻底拆开了。像素留在本地，只有文本出去，这在隐私敏感的场合是天然优势。

08.

流水线上的批量判断

这类没有浏览器代理那么好看，但可能是商业价值最大的一类。

1018 篇论文，分类花了 8 美分

Hassan El Mghari（@nutlope）做了 1kpapers.com。流程分两段：先用 DeepSeek V4 Flash 给 1018 篇论文生成摘要，花了 3.99 美元；再把每篇的标题和摘要加上 24 个候选主题交给 Jev 做一次 Choice 分类，总共 0.08 美元，中位延迟 256 毫秒。

![1kpapers 项目说明图](https://mmbiz.qpic.cn/sz_mmbiz_jpg/9uWm17ydXxlY2HjHSNDLeg8AVL88DGbHkzev6FqIibAxiaq2PzRDF6JCs2fOrNic3K0p35BT0icg59bLOAeCJoGE7gU3iciboCdMXGe76J4BiamnOA/640?wx_fmt=jpeg&from=appmsg&watermark=1#imgIndex=12)

图 13 ｜ 1kpapers 的封面图，把两个数字并排放在了最显眼的位置

底下那行小字是这批数据的规模：30681 页、1.027 亿字符。3.99 美元是摘要那半段的账单，Jev 负责的分类那半段是 0.08 美元  
素材来源：github.com/Nutlope/1kpapers

摘要花 3.99，分类花 0.08，差不多 50 比 1。他自己总结成一句话：不同模型做工作流的不同部分。一年前这个分类环节要么写成脆弱的正则，要么用同一个贵模型顺手做掉，两种都不划算。

给 PostgreSQL 加一个自然语言条件

Zachi 又出现了，这次做了 pg-jev 扩展，让 SQL 里能直接写这种条件。

sql · 模糊条件不需要 embedding 索引

SELECT \* FROM people WHERE jev(people, 'could work from home'); SELECT \* FROM people WHERE jev(people, 'name sounds european');

他给的数字是：129 行约 1 秒判完，成本 0.0009 美元，第二次跑命中缓存 6 毫秒返回。不建索引，不做 embedding。这个案例的意义在于它把「模糊条件」变成了数据库能用的东西。

还有一堆散在各处的

Search1API 团队做了 jev-search，把搜索这条链路整个拆给 Jev。第一步是你的这句话想找什么、该去哪些源搜、时间范围多大，全都由 Jev 判断；第二步十几个引擎并发去搜，Google、DuckDuckGo、Yandex 之外，Hacker News、Reddit、GitHub、arXiv、YouTube、维基百科各走各的通道；第三步让 Jev 给每一条结果打相关性分，再按分数和引擎一致性排序。

![Jev Search 首页](https://mmbiz.qpic.cn/sz_mmbiz_jpg/9uWm17ydXxmGxMkyQB4tiaqlyZwNickiaYicZHibfL0IOWe3r0CK2DvdG2gjyyibEI7qRayO2JvPR3iaJLia4ffBBvCcVcsa7hPYsxQgOL9ibMjTrtm0/640?wx_fmt=jpeg&from=appmsg&watermark=1#imgIndex=13)

图 14 ｜ Jev Search：选源、理解查询、给结果排序，三段都交给 Jev

它不生成答案，只给链接和摘要，相关性分数是露出给用户看的。整个请求以逐行 JSON 流式返回，分 intent、found、lane、done 四种事件  
素材来源：github.com/superagents-lab/jev-search

Faadil Shaik（@faadilhshaik）拿 Jev 分析了自己 3282 条 X 帖子，累计一亿浏览。每条帖子问 8 个问题：什么主题、钩子是什么、什么语气、有没有教东西。425 万 token 花了 0.1282 美元，8 分半跑完。结论是 how-to 类帖子中位 150 赞，整体中位 44 赞；AI 和编程是 1.9 倍的主题加成。这种活以前只能靠灵感，现在可以算。

Tony Dinh（@tdinh\_me）做了个 Chrome 扩展，监听 YouTube 音频、识别赞助段落并自动跳过，约 0.005 美元一个视频。他顺手还做了个实时病毒度分析器，你停手 0.5 秒它就开始给草稿打分。有人做了 Discord 审核机器人，给垃圾、钓鱼、社工消息打分，再由程序把概率翻译成四级响应。有人做了实时广告拦截扩展，逐个 DOM 元素判断是不是广告。还有个叫 Jev Detector 的，自称最快的 AI 味检测器，一万词扫一遍 2 秒。有人做二手车搜索，每分钟读约 26 条，每条 406 毫秒决定要不要，合适的自动出价、缺信息自动给卖家发消息，整轮搜索 0.00085 美元。

09.

实时闭环：交易、无人机、游戏

这一类最能说明「快」到底意味着什么。

Jarrod Watts（@jarrodwatts）的 jev-trader 每 300 毫秒一个 Monad 区块，让 Jev 给 MON-USDC 这个交易对选买、卖还是等，模型延迟约 81 毫秒。仓库里确实有真实下单模式的代码，但默认跑 dry-run，作者没有公开交易记录和绩效。这一点要心里有数，回测都没看到的策略谈不上验证。

不过这一周最有价值的设计出现在无人机上。

![图 15 ｜ jev-drone 的分层设计，我觉得是这一周最值得抄的架构](https://mmbiz.qpic.cn/mmbiz_png/9uWm17ydXxm60Bfkibs6DsGWcQ2Gw0J6IxQyEcy6iaq87NYaYsicu51euSpdcF2Byl72mC7EJtLFHmKCYeUrxV8rJBibwicdZDcxeh9EB4kT96oY/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=14)

图 15 ｜ jev-drone 的分层设计，我觉得是这一周最值得抄的架构

游戏这一类大家其实是拿来测延迟包络的。Doom 每秒约 10 次判断，一小时约 7 美元。有人演示 Subway Surfers，除了「超人速度」之外还同时开了 50 局，一次运行花不到一美分。有人让 Jev 在 Smash Bros 里自己打自己，同时控制 4 个角色，用了 2200 万 token，花了大约几分钱。还有 Super Mario Bros，以及 phyous 用有限指令集做的星际争霸。

我自己看得最久的一个，是一个中文项目，叫弈瞬。它同时开九局五子棋，两个 Jev 玩家轮流执黑，每一步只问一个 Choice 问题：从代码预先筛出的候选里选最佳落点。它测的不是棋力，输入信息的影响。同一份棋盘，可以只给棋盘文本，也可以额外给出「这一手能不能立即取胜」「对手下一手有没有双胜点」这类战术事实，然后比较哪一种输入下的决策更靠谱。

![弈瞬 九宫格决策实验台](https://mmbiz.qpic.cn/mmbiz_jpg/9uWm17ydXxljBSPxWYibsDWV8eoLBExpylKB3D5gDpJQibbJBBP1srXX9gGG3aTQRjibCgSyZbG2k6CuCwspKBotd3kibxGpwqU4ZSjsOjkhA04/640?wx_fmt=jpeg&from=appmsg&watermark=1#imgIndex=15)

图 16 ｜ 弈瞬的九宫格擂台，一局一个棋盘

右侧是决策看板：这一手的 state、questions、答案、选项概率、耗时全部摊开。图里 F6 拿了 100%，F11 只有 40%，同一个模型在同一步上给出这么不一样的把握，正好说明为什么要带着置信度一起用。截图是作者本地真实跑完的九局，比分 2 比 7  
素材来源：github.com/XieChengYuan/jev-gomoku

作者的边界写得很老实：候选是代码预筛过的（本方前 8、对方前 4，加上所有立即取胜和直接防守的位置），所以这不构成无辅助的棋力测试；Choice 的概率不是胜率；九局的胜负受开局、执黑执白、模型版本和采样影响，不能用来证明哪种输入更好。仓库里还存了一轮 144 次真实决策的回放，不填 API Key 也能逐手翻。

Justin Schroeder（@jpschroeder）那条「一小时内用 Jev 重建特斯拉 FSD」传播很广，得打个折扣。他做的是 Three.js 里的可玩模拟器，项目叫 JevPilot，Jev 负责选轨迹和速度，几何、寻路、紧急刹车的判定都在普通代码里。仿真不是真车，但这个拆分方式本身跟上面无人机那套是一个思路。

![JevPilot 自动驾驶游乐场](https://mmbiz.qpic.cn/mmbiz_jpg/9uWm17ydXxlk0oYHvO9lnPsDl2MQdTmL1lXrNgeuEqMvcl0icwE8RMibOibMjw5WeibqFNJEiatq91eicGbjsJiaPHiaRI6DwgWChMFUiaic9MicT45obQ/640?wx_fmt=jpeg&from=appmsg&watermark=1#imgIndex=16)

图 17 ｜ JevPilot，一个可以自己开起来的自动驾驶游乐场

地上那几条彩色轨迹就是 Jev 给出的候选路线。哪条能走、哪条撞墙由几何计算决定，Jev 只在合法的那几条里选一条并给出速度  
素材来源：github.com/standardagents/jevpilot

10.

有人干脆把它做成了语言

Steve Faulkner（@southpolesteve）发了个叫 Probably 的编程语言，Jev 直接内建在里面：feels 用来提问，match 用来在若干描述之间路由。

他这条思路的来源是 X 上一句被转了很多遍的话：大家都说 Jev 是「AI if 语句」，那如果它真的变成 if 语句呢。

这个方向之所以值得单独提一句，是因为它把前面那条结论推到了极端：如果一次判断真的便宜到可以忽略，那它就没必要再以「一次 API 调用」的形式存在，它可以直接变成语言里的一种语法。当然，这离日常生产还很远，目前更多是个思维实验。

11.

理性思考

前面讲的都是 TypeSafe 希望世界相信的东西，加上这一周社区愿意相信的东西。现在换个视角，当审计看。

这一周的案例有个共同特征：绝大多数是作者自报，没有独立复现。按可信度分几档会清楚很多。

![图 18 ｜ 发布周案例的可信度分档](https://mmbiz.qpic.cn/mmbiz_png/9uWm17ydXxkRH6QtvJUOZ6d86JY175GQs2UPLclCcg0TGYkVcWZ10G76AkaiaPq73wibjBs0ZAl83GSYkK3Bdd1aMp8ou2lYb0uThghjPTpok/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=17)

图 18 ｜ 发布周案例的可信度分档

第一档里最实在的一条是 Vercel。Guillermo Rauch 说的是真实流量、真实配置、p95 延迟，而且他准备把它变成默认，这比任何演示都说明问题。Ian Nuttall 说他在 Cloudflare Workers 上跑 keep.md，搜索 rerank 比原来的混合方案快 7 倍，内容打标比 GLM 4.7 Flash 快 50 倍且没有失败。

第二档里 jev-ultrafast 的诚实程度值得一提。它把限制写得很清楚：动作空间截断到 250 项，可见文本截断 6000 字符，不支持 iframe、canvas、文件上传、新标签、深层滚动和 shadow DOM，有一份 81.62 秒的超时报告，而且没有通用的危险操作确认策略，也没有域名白名单。它缩小了错误范围，但不保证动作安全。

反向证据也得看。有人在 Banking77 上拿 Jev 和 GLiNER 2.5 做对比；@nikhilmudholkar 在 1565 封邮件分类上发现 Gemini 比 Jev 准；第三方对浏览器代理配置的对比显示 Jev 版更快但也更贵。更关键的是 TypeSafe 自己那份四工作流评测：Jev 准确率 67.8%，GPT-5.6 Sol 是 74.1%，Claude Opus 5 是 73.1%。它赢在相近准确率下的成本和延迟（0.4 秒对 10 到 78 秒），不是绝对准确率。还有第三方注意到，在发票处理这类任务上，Jev 的聚合得分其实落后于它的对比对象。

下面这三盆冷水加上那条前作提醒，是针对 TypeSafe 这边的。

第一盆：基准是自家设计的，参考答案是模型生成的

TypeSafe 用的是所谓 Workflow Evals。做法是把任务拆成决策图，然后把模型输出跟参考答案比对。参考答案从哪来？来自 GPT-6 Astra 和 Claude Fable 5.1 的答案聚合。

这个做法有两个后果。其一，它是一家公司的内部 benchmark，够不上独立审计。其二，它衡量的是「跟强模型的共识有多一致」，而不是「跟事实有多一致」。

这个指标本身有它的道理，很多语义判断本来就没有 ground truth。但它不能被读成「Jev 更准」。官方自己也承认那四套工作流是自家团队设计的，193.6 倍和 444.6 倍这两个数大概率落在真实收益的高端。架构、权重、训练数据、loss 都没公开。

第二盆：独立测试只有一份，里面藏着一个不太好看的数

目前唯一一份能算独立的测试来自 Every 的 Mike Taylor。他拿自己的文本做了个车辆测试：37 篇文档、21 个问题，Jev 在 0.7 秒内返回了 777 个判断，成本大约四分之一美分。中位数每次 0.35 秒，对比的前沿模型是 8.83 秒。

听着很漂亮。但同一个测试里还有另一个数字：他在文本里故意埋了 7 个缺陷，Jev 找出 6 个，对比模型 7 个全找到。

要算清楚的一笔账

约 25 倍快、约 580 倍便宜，代价是漏掉一个。这个取舍划不划算，完全取决于你漏掉的那一个有多贵。而且 6 比 7 这个样本量太小，它到底是噪声还是真实错误率，目前没人知道。  
  
这也提示了正确的评估姿势：别拿总准确率下结论，去测你这个业务里错一次要赔多少钱。

第三盆：模型本身基本是个黑盒

没有论文，没有架构细节，没有权重，没有训练数据，也没有 reward function 和 loss 的描述。TypeSafe 说用的是并行采样，「快」是已经发生的事实，「为什么快」目前还是个说法。

同样待验证的还有校准。整个产品的价值建立在「置信度可信」这个前提上，但公开材料里看不到完整的 ECE、Brier score 或 reliability diagram，也没有展示输入分布发生偏移之后置信度还稳不稳。第三方整理出的待办清单里排最前面的三条恰好是这些：公开架构论文或权重、第二份更大样本的独立评测、以及在真实脏数据上的校准审计。

还有一条得自己去看。TypeSafe 官方发布了一份叫「jaggedness」的页面，主动列了当前版本的弱点：读字面不读意图、数学能力不可靠、日期时间比较不稳、多跳推理会掉准、state 里塞太多无关内容会「上下文腐烂」、对抗性输入能偏移答案。厂商主动写这些，态度值得肯定，但你也该知道这份清单存在。

还有一条：这个方向不算横空出世，接口也不构成护城河

有位开发者在 dev.to 上写了篇文章，说他 2025 年 3 月就发过一篇非自回归决策模型的 arXiv 论文，9 月又发了第二篇讲 schema-based decision 加强化学习框架的文章，权重也开源了，只是做的是垂直的销售场景。他觉得 Jev 是同一个想法被包装成了横向的通用产品。

这个说法我没法独立核实细节。它提醒的事倒是实在的：用判别式模型做结构化决策这件事，之前就有分类器、reranker、reward model 一整条技术积累。Jev 真正的新意可能不在想法，而在于有人愿意拿一个前沿实验室的资源和工程能力，把它做成一个通用产品，并且赌它能保住前沿级的语义理解。

这一周里有人已经在开源小模型上复现了它的接口模式，直接从 logits 里读类型化选项的概率。

![SemIf 对照回放](https://mmbiz.qpic.cn/mmbiz_gif/9uWm17ydXxn3UpQO6ArVR6ugdsmQ0jrWCstrqia2qw119b872h9dXfTGZEw6Hh1PmbOxiba1IRMbX3JOibjVIzSjUfYbK2MAsibibnlgM6MGcR9k/640?wx_fmt=gif&from=appmsg#imgIndex=18)

图 19 ｜ SemIf 的对照回放：同一份 state，两条输出路线（动图）

这台实验台的问句就写在标题上：能不能在一张 3090 上跑出类似 Jev 的东西。条件是同一台机器、同一个冻结的 4B 模型、同一份 state、同样 21 个问题，只改输出方式。左边走直接读类型化 logits，产出 21 个分布、0 个输出 token；右边走生成 JSON，产出 1 个数组、111 个输出 token  
素材来源：github.com/TheoLeeCJ/SemIf

这个项目叫 SemIf，作者在 README 里明确声明与 TypeSafe 无关，就是一个独立复现。它证明的是接口层面的事可以照着做，证明不了 Jev 那套训练方法能照着做，RLCD 到目前为止只有描述、没有论文。这也是为什么右边那条路虽然多花 111 个 token，短期之内仍然会有人用，它不需要先把模型训出来。

还有人走得更远一点。vinnylarouge 的 jevlike 尝试在自己准备的数据上，把「候选选择」这件事单独训成一个模型，作者自己也说目前还不实用，但方向值得记一笔。

![jevlike 的候选选择架构](https://mmbiz.qpic.cn/mmbiz_jpg/9uWm17ydXxloib2nqev0Fiatnn0vEDUQKIU0X4JkHb55wyP9GfNibUic1zvY7zVypBdNSUVGX49nwibw4uejYJEABGq6HoIu35nfjI6u8LN4D5Zk/640?wx_fmt=jpeg&from=appmsg&watermark=1#imgIndex=19)

图 20 ｜ jevlike 的架构图：把「从候选里选一个」当成一个注意力问题来训

查询（Q）与候选（K、V）做一次加权聚合，再经输出层给出选择。整张图里没有生成式的解码器，这正是这类模型的共同形状。作者自己标注还在早期，目前不实用  
素材来源：github.com/vinnylarouge/jevlike

这件事反过来提示一个判断：接口本身不构成护城河，模型质量、校准和延迟才是。

12.

它应该待在架构的哪一层

这个问题比「Jev 好不好」重要得多。它的接口设计本身就在逼你做一次分工，而这一周的案例也把分工的样子演了一遍。

![图 21 ｜ 三层分工：各干各的活](https://mmbiz.qpic.cn/mmbiz_png/9uWm17ydXxkRicicA3EuuD2QB6eXEagibBmSOtoIuzNJo7bs1fqwfepkANicIuYFuvrqrd8HMn1c6vTMPmDxicqYxXjjbia3lQyOkYCicRr27ocicuo/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=20)

图 21 ｜ 三层分工：各干各的活

顺着这个分工能推出一个很实用的模式：两模型。Jev 在前，一轮一轮做判断；生成模型在后，只在需要写字的时候被叫醒。路由层的选项集大概长这样：deterministic\_code、fast\_llm、reasoning\_llm、human\_review。

适用边界其实很清楚

答案集已知、判断重复、能按置信度行动。 **三个条件缺一个，它就不是对的工具** 。

有意思的是，这一周冒出来的项目几乎全都满足这三条。大家在 X 上讨论的其实不是「Jev 能不能做 X」，而是「我自己的工作流里哪一步本来就是这三条」。

确定性要留在代码里

无人机那套分层是最好的例子：500 Hz 的飞控、50 Hz 的安全反射全在代码里，模型只在 2.5 Hz 上说一句「我觉着该往左」，而且还只是建议。

computer-use 那个项目里作者也提到一个代价，我觉得是这一周最该抄下来的一句话：前沿模型顺手就做完的推理，在这里必须重新写成确定性状态。他举的例子是 Jev 需要显式解析日期，而 LLM 能直接从像素里把日期读出来。

别忘了代价

便宜和快不是白来的。省下来的钱，有一部分会变成你要自己写的代码，以及你要自己维护的状态机。上面那些数字（90 毫秒、0.0002 美元一步）之所以成立，前提是有人先把页面结构和屏幕元素拆成了确定性的状态。  
  
如果那部分工作没人做，Jev 接上去也只会是个更便宜但不准的猜测器。

还有几个工程细节值得抄下来。

硬约束留在代码里。被禁止的数据类别、上下文长度、供应商可用性、预算上限，这些都不该交给概率模型。

选择题一定要留逃生口。真实世界总有落在你预设选项之外的东西，所以要显式加一个 unknown、other 或 human\_review。没有出口的封闭选项集，会把边缘案例强行塞进错误的格子里。

state 是攻击面。用户输入的文本或者检索回来的内容，都可能影响语义判断。可信策略和模型判断要隔离，对抗输入要专门测。

版本要钉住。jev-latest 背后的模型是会换的。如果你调好了置信度阈值，就固定到具体版本号，并把响应里返回的版本 ID 记进日志。

级联是这一周最主流的架构

前面用便宜的决策层筛一遍，确定的直接走掉，不确定的才交给贵模型。有人算过一笔账：一百万张工单的规模，级联方案大约 6480 美元，纯 LLM 方案大约 30400 美元，其中约 80 万条能在半秒内给出答复。

这个账的关键变量不是单价，是你能不能让「确定」的那部分真的走掉。如果置信度不可靠，级联就退化成一个更贵的单层方案。

关于这条路能走多远，Scott Williams 的推文我觉得是这一周最有想象力的一条，大意是：真正会出现的一批公司，是用这种「并行约束解码」的模型，去让企业已有的 Agent 流水线更省 token。他描述的场景是，公司里那些「每一条都要过一遍前沿模型」的环节（工单分流、发票放行、理赔标记），其实背后有多年的人工决策记录，把它训成一个便宜的决策层，只要它能在六成情况下给出高置信的判断，这一步的开销就能去掉一大半。

什么场景别用，也要说清楚。需要写回复、解释一起安全事件、生成代码、做开放式规划的，都不行。确定性规则已经能搞定的也别用，判断发票金额有没有超限，写在代码里就好，别去问模型。如果你已经有足够的标注数据、任务又很稳定，一个传统分类器或 reranker 可能更便宜、更好审计，还能跑在自己机器上。

13.

名字里的那个赌注

Jev 这个名字有两个来源，都挺值得琢磨。

一个来自卡尼曼。TypeSafe 把自家这条线叫 System One Models，System 1 是《思考，快与慢》里那个不费力、凭直觉做判断的系统。对应的 System 2 是慢而费力的推理，前沿模型追的 reasoning 能力就是它。Jev 赌的是前者。

另一个来自 19 世纪经济学家 William Stanley Jevons。他在《煤炭问题》里记录了一件反直觉的事：蒸汽机效率提高之后，英国的煤炭消耗没有下降，反而涨了。因为更便宜的能源催生了以前不存在的用法。这就是后来被称作 Jevons 悖论的东西。

![图 22 ｜ Jevons 悖论在 AI 上的翻版](https://mmbiz.qpic.cn/mmbiz_png/9uWm17ydXxnoX5zrQDY2YLS2V9dG6ufVBXesdJmfiaQtJSfhSiauFTINica7eCbgRWY8qZQfU2lzRkwrYFOicfVnK22d2XDV8WKicVAlbNKFst6k/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=21)

图 22 ｜ Jevons 悖论在 AI 上的翻版

这个赌注有风险吗？有。能源市场能承接 Jevons 悖论，是因为能源普适，几乎人人需要、人人用得掉。判断是不是也一样，现在没有答案。反面的理由也很实在：很多拿得到 AI 工具的人，其实并没有那么多用得上的地方。

不过我觉得更值得琢磨的，是它顺手指出来的一个工程习惯。

发散一下

过去两年，Agent 的设计一直有一个隐含约束：每一步推理都要花钱、都要等。所以工程师本能地合并步骤、把 prompt 塞满、尽量一次问完所有问题。这个约束悄悄塑造了很多现在看起来理所当然的架构。  
  
如果一次判断真能便宜到忽略不计，有些新的可能就打开了：每一步都做一次一致性校验；每次工具调用之前做一次风险判别；每一轮输出都过一遍安全闸；大批量文档用几百个并行判断去 map-reduce。这些以前也能做，只是不划算。  
  
再往远看一层。评估本身也是判断。今天很多 Agent 评估只能覆盖最后一个答案，因为逐步打分太贵。当判断便宜到一定程度，「测量任务中间过程」会从论文里的理想变成工程上的标配。

当然，上面这些推演都压在一个前提上：它的概率确实是校准的。这个前提目前还是一张待兑的支票。

14.

收尾

Jev 发布到现在不到一周。

官方那几张 benchmark 图我看了好几遍，说实话印象不深。印象深的是那些具体的东西：inspector 里那条从 93% 一路排到 1% 的元素表；一个 Claude 会话从 100 万 token 压到 86K 只用 1 秒；129 行数据库记录用自然语言条件筛完花 0.0009 美元；一架无人机的飞控跑在 500 Hz，而「我该往哪躲」这个问题每秒只问 2.5 次。

这些拼起来，指向一个挺朴素的判断：软件里本来就存在大量需要「看一眼再拍板」的地方，过去两年我们用一个会写字的模型去顶，是因为没有别的选择。

现在有了个别的选择。

至于 Jev 本身，我的判断是：接口设计值得学，架构解释权还在厂商手里，性能数字要等第三方，校准结论要等论文或者你自己的实测。

真要用的话，现在就做一件最朴素的事。挑一个你正在用 LLM 做的重复判断，用自己真实的数据建一个带标注的小集合，把 Jev 和你现在的方案放一起比。

比的时候别只看准确率，看这四个数：跟可信标签比的一致率、置信度的校准程度、p50 和 p95 延迟，以及每一次被接受的决策的总成本。

最后一个数最容易被人忘。它要把推理费用、重试、兜底调用、人工复核、工程时间，还有走错路的代价，全部加起来，再除以通过验收标准的决策数。

这一周的案例能告诉你该往哪儿看，替代不了你自己那一组数据。这个数算出来之前，所有的倍速和便宜都是别人的故事。

参考阅读

官方

TypeSafe 官方发布（System One Models & Jev）

https://typesafe.ai/blog/introducing-system-one-models-and-jev

官方站点与文档

https://typesafe.ai/

https://docs.typesafe.ai/

工作流评测 / Python 适配器

https://evals.typesafe.ai/

https://github.com/typesafe-ai/system-one-adapter-python

Diogo Almeida 发布帖（X）

https://x.com/CompleteSkeptic/status/2099925682726002904

第三方解读与评测

The Register：TypeSafe AI debuts model for machines that plays Doom

https://www.theregister.com/ai-and-ml/2026/09/16/typesafe-ai-debuts-model-for-machines-that-plays-doom/5296711

heise：AI model Jev to make machines decide faster

https://www.heise.de/en/news/AI-model-Jev-to-make-machines-decide-faster-11457071.html

Flavio Copes：A deep dive into Jev（含完整 API 字段与限制）

https://flaviocopes.com/jev

Wavect：架构评审与生产使用警告（Jev 1.13）

https://wavect.io/blog/jev-ai-decision-model-review

OrcaRouter：速度与成本拆解，以及三条待验证事项

https://www.orcarouter.ai/blog/jev-typesafe-system-one-what-we-know

Axentia：含 Every 独立测试的完整细节

https://axentia.in/blog/jev-ai-decision-model-built-for-software

Nexforce：校准决策与 LLM 路由

https://nexforce.ai/en/blog/typesafe-jev-calibrated-decisions-llm-routing

kingy.ai：第三方评测（指出聚合得分落后于对比对象）

https://kingy.ai/blog/typesafe-jev-review-the-ai-model-that-doesnt-generate-text

Every：拿自己的文章实测（777 个判断 / 0.7 秒 / 埋 7 个缺陷找出 6 个）

https://every.to/also-true-for-humans/mini-vibe-check-typesafe-s-jev-judged-everything-i-ve-written-in-0-7-seconds

dev.to：一位开发者的前作声明（非自回归决策模型，2025）

https://dev.to/nandakishor\_m\_6cc0adfde9f/i-built-non-autoregressive-decision-models-a-year-ago-then-a-frontier-lab-called-it-a-18me

文中截图与动图的出处

browser-use / jev-ultrafast（图 8、9、10、11）

https://github.com/browser-use/jev-ultrafast

devagrawal09 / jev-review（图 7）

https://github.com/devagrawal09/jev-review

jkudish / jev-browser（图 12）

https://github.com/jkudish/jev-browser

Nutlope / 1kpapers（图 13）

https://github.com/Nutlope/1kpapers

superagents-lab / jev-search（图 14）

https://github.com/superagents-lab/jev-search

XieChengYuan / jev-gomoku 弈瞬（图 16）

https://github.com/XieChengYuan/jev-gomoku

standardagents / jevpilot（图 17）

https://github.com/standardagents/jevpilot

TheoLeeCJ / SemIf（图 19）

https://github.com/TheoLeeCJ/SemIf

vinnylarouge / jevlike（图 20）

https://github.com/vinnylarouge/jevlike

社区项目

1kpapers.com（1018 篇论文分类 $0.08）

https://1kpapers.com

jev-trader（Monad 上每 300ms 决策）

https://github.com/jarrodwatts/jev-trader

pi-warden（Agent 行动前自查）

https://github.com/DevMortimer/pi-warden

fast-jev-compaction（1 秒压缩上下文）

https://github.com/tamaratran/fast-jev-compaction

pg-jev / mobile-jev / jev-router

https://github.com/realZachi/pg-jev

https://github.com/droidrun/mobile-jev

https://github.com/gargpratyush/jev-router

案例盘点与实测

15 个早期项目逐个拆（含 7 秒机票的计时边界）

https://gotacat.dev/en/blog/jev-decision-api-browser-agent

X 上社区项目汇总（含多条原帖）

https://wpnews.pro/news/what-people-built-with-jev-since-it-launched

浏览器本地 Agent 的工具选择实验（含完整返回）

https://mohitkarekar.com/posts/2026/probabilistic-decisions-with-system-one-model-jev大

代码的使命

邀请你前往腾讯公益一起捐

困弱群体关怀行动

闪记

复制 LaTeX 公式