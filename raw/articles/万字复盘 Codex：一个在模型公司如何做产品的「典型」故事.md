---
title: "万字复盘 Codex：一个在模型公司如何做产品的「典型」故事"
source: "https://mp.weixin.qq.com/s/U1he1wBWS2PKIaTD1LtRlQ"
author:
  - "[[Founder Park]]"
published:
created: 2026-10-25
description: "从边角料产品到今天 ChatGPT 的基座"
tags:
  - "clippings"
---
Founder Park Founder Park *2026年10月21日 19:14*

![图片](https://mmbiz.qpic.cn/sz_mmbiz_gif/5icxfcvT9Umj7xQFlVRNLVdicYzwKh4W3eaKCopIyU3gzLxhELh1qyS8CwlNlgpOmPia1SlAMOXSju1HmQ8kdQzB8QGpflkgVxtA82AoIVJBbk/640?wx_fmt=gif&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

半年前，很少有人相信 Codex 能追上 Claude Code。

那时，开发者几乎一边倒地沉浸在 Claude Code 里。到了 2026 年夏天，风向变了，很多团队把主力工具切到 Codex，桌面端周活很快突破 500 万。7 月，OpenAI 干脆把 Codex 桌面 App 改造成了新的 ChatGPT 桌面 App。当初 ChatGPT 里一个标签页的边缘项目，反过来成了 ChatGPT 的底座。

但在这个爆款背后，过去一年 OpenAI 内部经历了剧烈的方向摇摆。

Claude Code 在本地跑起来时，Codex 在做云端的 Codex Cloud。结果迟迟找不到 PMF，工程负责人还跳槽去了 Cursor。退回本地后，面对 Claude Code 的领跑，接手团队的 Tibo 顶着「CLI 不够好用」的压力，把底层 Agent 彻底重写了一遍。

准备做原生桌面端的时候，又开始纠结要不要内置代码编辑器，因为其他家都在做。结果得到新的更强的模型发布后，这个问题，又不是个问题了。

Codex 几乎把今天做 AI 产品要回答的问题都踩了一遍：

- 模型能力每隔一两个月就变一次，产品形态到底该怎么选？
- 明明看清了 Agent 的终局，为什么一步到位，反而会死在半路？
- 在一家公司里，产品、工程和模型团队该怎么配合，才能把一个产品救活？

文章作者，是硅谷 AI 机构 Every 的 CEO Dan Shipper。从觉得 OpenAI 要失去「天命」，到半年后全团队切回 Codex、感叹「OpenAI 又回来了」，他深入采访了 Tibo、Alexander Embiricos、Mia Glaese 等 Codex 核心成员，还原了这款产品几次转向背后的完整故事。

以下是全文编译，经 Founder Park 编辑整理。

原文：https://every.to/p/how-codex-happened

⬆️关注 Founder Park，最及时最干货的创业分享

---

Founder Park 正在持续寻找值得被看见的 AI 团队与项目。

我们将通过「AI 产品市集」、内容报道、社群分发等方式，帮你触达早期用户、获得真实反馈，以及建立关键连接。

如果你正在做 AI 相关的事，欢迎和我们聊聊。 ![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/5icxfcvT9UmgOh5XmERHvv2VVoORvdnbvh4ibIxMDRSuiaxqCJibx4xuQczqhRaswaqZnlibib6b0cAI877gQcVzDJJIk5fSE0oxhOAf4bVh9SdS8/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=1)

---

**01**

## OpenAI 内部赛马，

## Codex 是好几条路线合起来的

打造一名 AI 程序员，是 OpenAI 追逐了太久的目标。以至于 Codex 有过很多个起点，就连这个名字本身，也已经不是第一次出现。

第一代 Codex 发布于 2021 年。它是一个在公开代码上微调过的 GPT-3 版本，后来为初代 GitHub Copilot 提供了底层能力。

真正让编程重新成为 OpenAI 重点方向的，是推理模型。

第一代大语言模型只能一个词接一个词地推演答案，既没机会提前规划，也无法在完成后回头修改。推理模型不同，它在回复前，会先在一个叫作「推理轨迹」的草稿区里工作。它可以从不同角度切入问题，发现走进死胡同时退回来，再选择一条更可能成功的路径。

OpenAI 将首个此类模型命名为 o1，并于 2024 年 9 月发布预览版。在此之前，模型进步主要靠扩大规模、延长训练时间。到了 o1，OpenAI 发现，同一个模型只要在难题上多花一点时间，答案就能变得更好。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/5icxfcvT9UmjAJXQbT3iaNtpaL7mvqUSwMnDmYXQwmsNu4ZomtkknIf0icNF7xLlXgXQMvWEYvMGdt0BiaYfryVI71zzo6qPUlkq06b53ib2Zd7I/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=2)

有一类工作从中获益的程度远超其他所有领域，那就是编程。编程尤其适合推理模型，因为它存在一个闭环。模型可以修改代码、运行代码，并在几秒内看到改动是否生效。它可以自行测试、修正，不需要每一步都由人来检查。理论上，只要给足思考时间，推理模型可以独立完成任何编程任务。

**在 o1 预览版展现出推理模型的潜力之后的几周里，编程重新成为 OpenAI 最高层级的目标。** 来自管理层的一道指令，让 OpenAI 内部的好几个团队再次从不同方向出发，探索编程 Agent。

其中一个起点，来自 2024 年末的 Alexander Embiricos，后来的 Codex 产品负责人。

Alexander Embiricos 是在 2024 年早些时候加入 OpenAI 的，当时 OpenAI 收购了他联合创办的程序员多人屏幕共享工具 Multi。加入 OpenAI 后，他继续推进一个相关构想，让人类和 Agent 在日常使用的应用里共同工作。他先是在 ChatGPT 桌面应用上尝试，后来又参与 AI 浏览器 Atlas，但当时的模型读取用户屏幕既慢又笨，很难真正派上用场。

「我第一次真正产生那种强烈的『AGI 降临感』，是看到有人把推理模型接进终端运行。」他对我说。「我知道这放到现在已经不稀奇了，」但看着它读取文件、执行命令、自己处理错误，「真的酷毙了。」

在终端里，模型不需要去「看」屏幕，它们可以直接在文本和代码里干活。看到早期推理模型在终端里的表现，Alexander Embiricos 确信它们完全可以驱动一款真正的编程产品。当时编程还不是他的全职工作，但他立刻开始画产品草图。他认为，要让这款产品行得通，用户必须每 30 秒、或者最多每分钟就能看到模型正在做什么。

问题又回到了速度。当时，大多数 AI 编程产品都围绕 VS Code 生长。GitHub Copilot 通过扩展提供 AI 自动补全，Cursor 和 Windsurf 则基于 VS Code 的开源代码构建自己的编辑器，在程序员工作的界面旁加入 AI 对话。

这些工具依赖紧密的反馈循环。Copilot 补全你正在输入的那一行代码，Cursor 和 Windsurf 会在几秒内回答问题。 **没有哪款产品会让模型独自工作很久，因为模型做不到。**

OpenAI 的早期推理模型正好相反，一旦思考时间被掐断，它们就会变得既慢又弱。他开始思考，能不能把模型得出响应需要漫长时间这个缺陷，转化成一种优势？

与此同时，在 OpenAI 的另一边，大家称作 Tibo 的 Thibault Sottiaux，正试图让推理模型反过来作用于模型自身。用它的能力，帮助研究员打造下一代模型。

「我大概是从 2024 年 12 月开始参与编程 Agent 的。」他对我说，目标「是帮助我们更快地编写基础设施，更快地做研究」。

Tibo 职业生涯的大部分时间，都在为研究员搭建基础设施，先是在 DeepMind，后来是 OpenAI。在 AI 的世界里，研究基础设施，也就是 AI 研究员用来运行、评估、复现实验并部署实验结果的共享代码，恰恰是无数核心突破发生的地方。如果你能缩短跑一次实验所需的时间，就能跑更多实验，从而更快地拿到更好的模型。

Tibo 的团队并不是要面向大众做一款模型，是在 OpenAI 的 Monorepo（统一代码仓库，OpenAI 整个组织的代码都存放在这里）上训练内部使用的编程 Agent。这些 Agent 负责编写 Python 代码，帮助研究员运行和改进那些用于训练新模型的系统。研究员每天都在使用这些 Agent，也因此为团队提供了紧密的反馈循环。

「我们看到编程能力进步得非常快。」Tibo 说。他的团队频繁训练模型，使用的技术和公司大范围训练公众模型的方法并不相同。甚至在相当长一段时间里，两边很难调和到一起。

这套方法很快奏效了，他们成功地让模型反过来参与创造模型的研究过程，研究员也正在用这些模型打造下一代模型。

工程师把这叫作「自举」（bootstrapping）。先做出一个擅长帮研究员跑实验的模型，研究员就能用它造出一个更强大的模型，接着跑出更好的实验，再催生出更强的模型，如此循环往复。

当我问 Tibo 他们是在哪个时间点决定把 Codex 独立模型线从 ChatGPT 中拆分出来时，Tibo 语气平淡地说道：「从来没有什么拆分模型线的决定。在最开始，这只是一次研究探索，以及对我们研发速度的一次优化。」

这项工作提供了后来 Codex 的一半，一个 **能够改进新模型研发基础设施的 Agent** 。但要成为一款公司其他人也能使用、最终还能走出 OpenAI 的产品，它还缺少另一半，Alexander Embiricos 关于人类应当如何与这些 Agent 协作的构想。

如果现在回看 2024 年末至 2025 年初的 OpenAI，OpenAI 总裁兼联合创始人 Greg Brockman 告诉我，当时悬而未决的问题是找到正确的「产品形态」。

Agent 究竟应该待在开发者执行命令的终端里、写代码的编辑器里，还是在云端拥有一台属于自己的电脑、独立工作？有些路径最终被证明是死胡同，但在当时，没有人知道究竟是哪一条。

「从某种意义上说，OpenAI 是在押注一系列创业公司，只不过它们全都在公司内部。」OpenAI CEO Sam Altman 在 2025 年接受 Ben Thompson 采访时说道。

这种内部并行探索的做法，在几位内部人士看来有时显得混乱且浪费，谁愿意待在那个「做出 OpenAI 内部第三好用的 Agent 产品」的团队里？为探索留出空间，与制造彻底的混乱之间，只有一线之隔。

但在技术前沿不断移动时，这种做法是必经之路。借用已故哈佛大学教授 Clayton Christensen 的术语来说，模型层面快速的「延续性」进步，会让全新的应用形态成为可能，并不断颠覆前一代应用。

一个能补全一行代码的模型，很适合做成自动补全工具。一个能思考 30 秒的模型，可以在聊天侧边栏里回答问题。一个能连续工作一小时的模型，需要的则是完全不同的另一种形态。

围绕上一代模型做出成功的产品，并不意味着你就知道下一代该长什么样。你需要让好几个团队去尝试不同的点子，等看清什么东西真正有用之后，再把大家的工作汇聚到一起。

到 2025 年初，OpenAI 准备这么干了。「最终，我们觉得应该与另一个叫 Scientist Assistant 的项目合并。」Tibo 告诉我。正是这次合并，让他与 Alexander Embiricos 走到了一起。Greg Brockman 回忆 OpenAI 内部的多条编程探索路线时说：「我们最后先合并了两个，然后又合并了另外两个。」

新团队规模不大，却横跨多个领域。有 Alexander Embiricos 这样的技术型产品思考者，有 Tibo 这样的基础设施与工程高手，还有来自 DeepMind、曾参与 Gemini 和模型对齐工作的研究员 Mia Glaese。在 OpenAI，Mia Glaese 负责模型训练与对齐所需的数据，专门研究如何获取并利用数据来塑造模型的特定行为。

这种让产品人员与研究员并肩工作的跨学科团队，在 AI 领域并不常见。从历史上看，AI 一直是个由研究驱动的领域，顶尖研究员能拿到堪比勒布朗·詹姆斯的数百万美元天价合同，其他人拿的则是行业标准的工程师薪水。

与产品团队一起工作，让 Mia Glaese 和其他研究员有机会亲眼看到自己的模型是如何被使用的，也能听见人们接下来希望模型做什么。产品人员可以问：「如果模型能完成这件事，不是很棒吗？」接着研究员就能把它变成现实。

这又是 Tibo 的「自举」飞轮，只不过这一次，它是在模型与基于模型构建的产品之间运转。

OpenAI 终于有了一支完整的 Codex 团队，产品、设计与研究共同协作。现在，他们只需要决定，到底要造什么。

## 02

## 2025 年，

## OpenAI 过早押注了云端 Agent

在 Anthropic，一条很有希望的路线已经开始起飞。

2025 年 2 月 24 日，Anthropic 发布 Claude 3.7 Sonnet，并同步推出 Claude Code 的研究预览版。与 Cursor 等工具不同，Claude Code 没有内置代码编辑器。它运行在终端里，直接操作你本地电脑上的文件。你告诉它你想要什么，它就会读取代码、作出修改并运行测试。

因为运行在用户自己的电脑上，它的工作会直接落进你原本就在使用的文件里，沿用已经安装好的工具，也继承此前共同工作的全部上下文。任务进行到一半时，你可以打断它，还可以把一次会话学到的经验带进下一次，让整个系统随着时间持续改进、不断复利。

开发者很快接受了 Claude Code。比如在 Every，Edmar Ferreira 在 2025 年 3 月的 Vibe Check 中写道：「在 Agent 这件事上，Claude Code 比我用过的任何东西都好。」

![图片](https://mmbiz.qpic.cn/mmbiz_png/5icxfcvT9Umj9jeTZQBFvAAibd9Aa02L5quscMSMazhIGMYukykYmEyhIptGBF06ibsfGoQUx8TojybarDXkwXjkUianTibBS2Qzm4pgRPZ2XibmA/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=3)

但到了 2025 年春天，合并后的 Codex 团队，却把目光投向了另一种软件工程未来，Codex Cloud。

他们设想了一个运行在云端、拥有自己电脑的 Agent，专门处理异步工作，用户可以从电脑或手机把编程任务交给它。他们给自己定了大约七周的时间来开发并上线这款产品。

在 Codex Cloud 里，用户可以点击 ChatGPT 侧边栏里的 Codex，打开一个工作区，在里面描述任务并点击「Code」。这项任务就会被剥离并放入队列，同时清空输入框以便你输入下一个任务。Codex 会把你的代码库复制到一台隔离的云端机器上，自动修改文件，并运行测试和代码检查工具。完成后，它会返回一份摘要、一份改动 diff，以及一个用于发起 pull request 的按钮。

Codex Cloud 于 2025 年 5 月 16 日发布。Tibo 告诉我，它在 OpenAI 内部「非常成功」。但走出 OpenAI 后，发布虽然引发了兴趣，真正持续使用的人却很少。

![图片](https://mmbiz.qpic.cn/mmbiz_png/5icxfcvT9Umg1ywEX5RRwKAnMp9s2mmocQNCC17F7zafQ998VuLShF2CEdQbwkyeCKNfEaZ0M8kKNHdJf3L7t1SSvcgGfLAGNMLB89zmZT8A/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=4)

**问题出在实际使用门槛上。** 为了让它跑起来，开发者需要在云端重建自己笔记本电脑上的软件、权限和设置。这个过程可能要花上好几个小时，因为你得把各种凭证复制过去，并安装关键的软件包。一旦配置妥当，它确实能完成定义明确的任务。但在任务执行过程中，你没法随时打断它以纠正方向，甚至连追问一句提示词都会重新启动一台全新的云端电脑。

「如果你是一名技术负责人，要在现有代码库里加功能或修 bug，那它是你会顺手拿起来用的工具。但如果你想靠 vibe coding 做出一家单人十亿美元 SaaS 公司，还是另寻他处吧。」我在发布当天的 Vibe Check 里写道。

阻碍 Codex Cloud 的也不只是产品。「它发布得太早了，当时的模型还不够聪明。」Alexander Embiricos 说。

内部的成功，恰恰误导了团队。在 OpenAI 内部，标准化的开发环境让配置过程实现了全自动，研究员交出去的任务也都有清晰定义。团队自身的工作条件，掩盖了外部用户需要承担的配置成本有多高。

「我们当时是带着一种更偏未来的愿景去切入的。」Mia Glaese 对我说，「没有想着『先去用户已经在的地方找他们』，而用户所在的地方，就是他们自己的笔记本电脑上。」

既然如此，为什么 OpenAI 跳过了已经在 Anthropic 那里奏效的终端形态？

「我们没有跳过。」Tibo 告诉我。他指的是一个从未对外发布的内部原型。「我们做过一个终端版本，但一个月后就把它废弃了，转而全力投入全云端版本。」

「为什么？」我问。

「因为当时我们优化的目标是，如果愿意在前期配置上投入巨大精力，哪种形态能让我们获益最大，」他说。

这背后，是我在 OpenAI 内部反复听到的一种信念。在他们看来， **AI Agent 最理想的形态，一直是在云端自主为你工作。** 即使你合上电脑，它也不会停止。Greg Brockman 在采访中也说过同样的话：「如果把时间拉到未来，正确的产品形态应该是一个待在云端、拥有自己笔记本电脑的 AI。所以我们真的把它造出来了。」

这一选择也是对当时模型局限性的妥协。当时的模型更适合花较长时间独自处理任务，做不到每时每刻实时响应程序员，团队干脆顺着这个特点做出了第一代 Cloud 产品。

事实上，OpenAI 确实在 4 月 16 日，Codex Cloud 发布前整整一个月，推出过一个酷似 Claude Code 的小型开源 Codex 命令行界面（CLI）。这又是 Codex 众多起点中的一个。

Alexander Embiricos 把这个公开 CLI 形容为一个独立的支线项目，由「大概两个人像孤胆英雄一样做出来的」。但 OpenAI 的大部分资源，以及为 Codex Cloud 专门训练的模型，都没有投入 CLI。「你甚至没法在那个 CLI 里使用 Codex 模型。」他说。

在用户的电脑上直接运行 Agent 还引发了安全顾虑，因为它可以直接修改用户电脑上的文件并执行命令。「作为一家公司，我们对安全的态度非常保守。」Alexander Embiricos 说，「我们实际上不得不做了大量工作，去摸索怎样才能放心地部署这种级别的能力。」

因此，早期用户只能在 CLI 里运行通用模型，默认是 o4-mini，它本来就不是作为编程 Agent 打造的。CLI 虽然存在，但团队的注意力与最好的模型都放在了 Cloud 上。

结果，Cloud 这条路没走通，产品没能找到 PMF。团队的工程负责人离开去了当时估值高达 90 亿美元的 AI 编程领头羊 Cursor。大约在同一时期，据报道 OpenAI 曾达成一项 30 亿美元的协议，准备收购 Cursor 最接近的竞争对手 Windsurf，但这笔交易在 7 月份告吹了。

「最难熬的时候，是我们觉得自己不知道该做什么。或者说，我们知道该做什么，却很难看到进展真正发生。」Alexander Embiricos 对我说。

Codex 团队，乃至在一定程度上 OpenAI 更大的编程野心，第一次迷失在荒野里。云端是他们相信的长期方向，但无论模型还是产品，当时都还没有准备好。

## 03

## 转向本地，

## 开始追赶 Claude Code

在 Cloud 发布后的余波中，2025 年暮春与整个夏天，Codex 团队准备好尝试另一条道路了。

当时，用刚加入团队不久的设计师 Ed Bayes 的话来说，这个项目处在 OpenAI 的「偏远死水区」。「如果你想当那种光鲜亮丽的设计师，」他告诉我，「你会去做 ChatGPT。」

就在这个被忽视的角落里，Tibo 接手成为团队的工程经理。「我接管团队后，大幅改变了方向，」他告诉我，「我们转向了本地。」

「本地」意味着像 Claude Code 一样，让 Agent 运行在开发者自己的电脑上，而不是云端。他们重新捡起了此前由两个人开发出来的本地 Codex CLI。如果在它上面直接增加新功能，本可以迅速拉起声势，但 Tibo 没有急着为 CLI 堆功能，他决定重写整个 Agent。

「很长一段时间里，我们的 CLI 功能确实不够好，」他对我说，「因为我们忙着开发底下的 Agent。」

CLI 只是用户交互的界面，但 Tibo 优先改造的是底层能力，那个负责读取文件、执行命令等工作的 Agent。他希望把它做得更好，并把 Agent 与终端界面拆开，好让同一套 Agent 以后可以进入 CLI、代码编辑器、桌面或移动 App、云端，乃至 ChatGPT 本身。

![图片](https://mmbiz.qpic.cn/mmbiz_png/5icxfcvT9UmgCC3jkribYWyEAwqEiaaH0ayQ2hovbibAeQVYjvgeiaia15VvGOQJjElic3uuZLnnq3jLpJxQXjXwLgFZnic6eN8CBMB8X5VyXsiaAfx0/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=5)

团队用 Rust 重新构建了整个 Agent，这门语言专为对速度和安全性要求极高的系统而设计。如此一来，同一套底层引擎既能驱动终端 CLI，也能在后来驱动编辑器扩展。

但他们仍然缺少一个足够强、能真正驱动它的模型。

就在 Codex 团队在 Tibo 带领下重建 Agent 的同时，Michelle Pokrass 正努力让 GPT-5 更擅长真实世界的编程工作。

Michelle Pokrass 此前负责 GPT-4.1 的研究，这一次领导后训练工作，也就是对已经完成训练的模型继续调整行为，使其能够应付真实的编程任务，重点服务那些希望获得更好交互式编程体验的客户。

OpenAI 的模型在各类编程竞赛中表现优异，但这些成绩并没能转化为处理真实代码库的能力。Greg Brockman 将其形容为一个 SAT 考了满分、却从来没有工作过的学生：「它们从来没见过乱糟糟的真实代码库，也没见过程序员是如何在任务进行到一半时打断它的。」

为了让这些只会死读书的模型获得实战经验，Michelle Pokrass 和团队坐在程序员身边观察他们工作，找出模型在哪里崩溃，再把这些失败转化为可重复的训练任务。

此前，Codex Cloud 试图一步跨进完全自主，结果遭遇失败。客户又明确要求一个更好的交互式搭档，于是 OpenAI 训练出来的 GPT-5 形成了更谨慎的编程风格。它能理解大型代码库里的各个模块如何咬合、能解释自己的计划、调查 Bug，并且在越过沙盒权限边界前，会停下来先询问人类。

2025 年夏天，OpenAI 在 GPT-5 发布前大约一个月向我们开放了内测权限，让我们帮助了解模型的长处与短板。GPT-5 用在日常任务上让我们印象不错，放进 Codex 后，反应却平平。

在 Codex 里，GPT-5 很快，看起来也很聪明。我们技术能力最强的工程师之一 Naveen Naidu，用它定位了语音听写应用 Monologue 中一个困扰自己多日的诡异卡死问题。但它总是停得太早，生怕越过权限边界，用起来更像是一个谨小慎微的结对编程搭档（Pair Programmer）。

而我们的团队，已经不再满足于与 AI 模型一步一步协作。Kieran Klaassen 带着一群人使用 Claude Code，开始把整项任务交给 Opus 4，然后直接离开，直到它交回一个完成的功能，有时甚至是一款完整的应用。团队作者 Katie Parrott 只获得了工程师很少的帮助，就在几天内搭建并部署了自己的 AI 内容管理系统。

为了分享我们的测试感受，在 GPT-5 发布前夜，我来到 OpenAI 位于 Mission Bay 的办公室，与 Alexander Embiricos 和传播团队的 Lindsay McCallum 见面。

「用 Claude Code 的时候，你可以直接放手让它干。」我对 Alexander Embiricos 说，「GPT-5 显得有点胆小，像是被沙箱束缚住了，不敢真正用出自己的能力。」

**「我们现在甚至已经不怎么看代码了。」** 我开口说。但说出这句话时，我脸都红了。向他解释如何把任务交给 Agent，实在显得荒唐，他的工作本来就是打造自主编程 Agent。况且在当时，我也不确定我们这套工程方法离开这个小团队后是否还能奏效。

一声 Slack 提示音让 Alexander Embiricos 的屏幕亮了起来，也打破了会议室里突如其来的安静。他把电脑静音，将笔记本屏幕合上了四分之三，只留下一条窄缝，让他在本地运行的 Codex Agent 继续思考。

与 Claude Code 相比，Every 团队仍觉得 Codex CLI 里的 GPT-5 落后了一步。Kieran Klaassen 写道：「GPT-5 可以干掉 Sonnet 3.5，但它并没有跃进未来。」那天晚上离开 Mission Bay 时，我忍不住想，OpenAI 会不会正在为一种日渐消亡的工作流，打造一款完美工具？

不过，对当时绝大多数软件工程师来说，他们想要的恰恰是一个谨慎的协作者。习惯了每一行代码都自己写的程序员，依然普遍对把生产代码交给自主 Agent 嗤之以鼻。

「我不会让它替我掌控代码。」Ruby on Rails 的创造者、工程师社群中极具影响力的 DHH 在 GPT-5 发布前后说，「作为程序员，我的乐趣就是亲手敲代码。」

到了 2026 年 1 月，DHH 又写道，AI Agent「完全有能力为真实代码库贡献生产级代码」。在 9 月的 Rails World 大会上，他更宣布，自己的公司将不再手写代码。

在荒野中徘徊数月之后，重做后的本地 Agent 终于等到了能驱动它的模型。8 月底 GPT-5 发布后，Codex 团队紧接着推出了面向 VS Code 和 Cursor 的扩展，开发者们蜂拥而至。到 2025 年 10 月，使用量增长超过十倍，编辑器扩展很快超过终端，成为 Codex 使用最多的入口。

Alexander Embiricos 说，在改版后的 CLI 里发布 GPT-5 后，「一个开始自行运转的飞轮形成了」。

他记得自己当时的感觉是：「终于，我们可以开打了。」

## 04

## Coding Agent 要不要取消代码编辑器？

随着 Codex CLI 和 VS Code 扩展的人气爆发，换作大多数公司，正常的选择自然是继续对这两者加大投入。当时编辑器扩展增长很快，而 Claude Code 又在终端里领先，团队完全可以一边强化编辑器扩展，一边在终端里追赶。

但 Codex 团队做了一件出人意料的事。

「我们决定继续维护 CLI，但下一个最重要、最紧迫的投入，应该是一款原生桌面应用。」Tibo 对我说。

在 OpenAI 内部，他已经看到模型能完成越来越长的任务，也能调用代码库以外的信息，语音和图像能力也在路上。人们很快会同时运行多个 Agent，并长时间与它们一起工作。「如果你要把所有时间都花在里面，它就必须是一种非常丰富的界面。」他说。

在他看来，试图在一个诞生于 20 世纪 70 年代、只能显示文本的窗口里，同时调度六七个通过文本、图像、语音和视频交流的 Agent，根本难以承载这种工作方式。

对 Alexander Embiricos 而言，本地桌面 App 也指向了他们在 Codex Cloud 上未能实现的理想工作流。在 Cloud 里，用户无法在任务中途打断 Agent。有了运行在自己电脑上的桌面应用，人们可以先与 Agent 紧密协作，再像带一名新同事那样，逐渐弄清哪些任务可以放心交给它。最终，同一个界面还能把 Codex 带出开发者圈子，交到那些永远不会打开终端的人手里。

为了帮助设计和开发这款 App，Tibo 找来了 Andrew Ambrosino，一名设计师、程序员，也是前创业者。

Andrew Ambrosino 加入这个开发 App 的小团队时，他们知道自己想做桌面应用，却不知道它最后会长成什么样。团队唯一确定的，是把这款应用做成自己日常工作的主力工具。「我们知道，自己需要一个能够每天使用的入口，但它必须比传统 IDE 更轻。」他说。

随着 Claude Code 走红，市面上已有少数应用开始尝试在终端之外为编程 Agent 打造入口。ChatGPT 提供了另一个参照，一侧是历史会话，中间是当前对话线程。

Andrew Ambrosino 在谈到设计过程时说， **Codex App「从聊天产品获得的灵感，比从 VS Code 获得的更多」。**

团队很快敲定了基本布局，侧边栏按照项目组织任务，每项任务都有一段与 Agent 的独立对话。

紧接着，一个更棘手的问题摆在了面前。当 Agent 做错时，用户能不能直接在 Codex 里手动修改代码？团队做出了一个冒险的决定，不内置代码编辑器。如果你想要对代码做任何修改，必须继续交给 Agent 去改。

「我们就是想让它成为一种和代码编辑器不同的东西。」Andrew Ambrosino 对我说。一旦允许开发者在 App 里亲手敲代码，他们就会期待编辑器该具备的其他一切功能，撤销、搜索、快捷键，进而处处注意到 Codex 的缺失。

要满足、甚至超越这些预期，对于一个只有四个人的团队来说，会是一项庞大工程。更重要的是，他们不想做一款功能不完整的 VS Code。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/5icxfcvT9UmjTjmABowBYsQAfiaPQic3LwialvPMUCgETK1QrVEJPEbibYGCWvU2rhk7tANLDCI8JbbJX12Dlor9CAf5YIDZR3qibibYGqQRb9Urbg/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=6)

Codex 不可能靠做一个蹩脚的代码编辑器赢下比赛。 **用 Agent 写代码的体验必须足够好，好到开发者不会想念编辑器。**

唯一的问题是，当时他们自己都还在用 VS Code，来开发一个要取代 VS Code 的产品。

「每天 Alexander Embiricos 走进来都会问：『我们来挨个过一圈。你把这款应用当主力了吗？你把它当主力了吗？』」Andrew Ambrosino 回忆道。

一开始，所有人的答案都是「没有」，没有人把 Codex 当成自己的主力编程工具。没有代码编辑器，哪怕只是很小的修正，也得和 Agent 对话。负责开发者体验的 Dominik Kundel 在一条早期 Slack 消息里写道，这「感觉太繁琐了」。

就连 Andrew Ambrosino 自己也有怀疑。11 月，他在发给团队的消息里写道：「『不能编辑文件』可能是整个首发功能范围里，最让我犹豫的一点。」

外部市场的发展，让不做代码编辑器的决定显得更加冒险。2025 年 11 月，Google 发布另一款基于 VS Code 构建的编程工具 Antigravity，把 AI Agent 与完整编辑器结合在一起。

「我们就那么面面相觑。」Andrew Ambrosino 回忆，「没有基于 VS Code 二次开发，是不是犯了一个天大的错误？我们非常纠结，我觉得团队内部甚至都没有达成共识。」

更严峻的是，当时驱动这款应用的模型质量也不够。OpenAI 虽然在 9 月份推出了专属的 Codex 模型线，但到了 11 月，它的水平依然撑不起他们正在打造的桌面产品。Andrew Ambrosino 告诉我，以当时模型的质量，桌面 App 即使功能完整也是「根本没法拿出去发布的」。

## 05

## 模型足够强，

## 很多问题就不是问题了

接下来的几周，情况开始发生转机。

2025 年 11 月 19 日，OpenAI 发布 GPT-5.1 Codex Max，可以一次连续写几个小时代码。12 月 18 日，GPT-5.2 Codex 紧随其后，进一步提升了在大型代码库中跨文件修改的能力。

因为 Codex 模型线与 ChatGPT 主模型分开，团队可以更快地调整迭代，不需要担心每次改动都会影响正在使用 ChatGPT 的 8 亿用户。

与此同时，Mia Glaese 与 Codex 团队其他成员直接协作，进一步缩短了从开发者反馈到模型改进之间的循环。产品团队直接告诉研究团队，真实用户希望模型下一步做什么。研究团队专注于改进模型在真实工作中的表现，不再只是追求热门 Benchmark 上的跑分。

到了 12 月，团队里越来越多人开始用 Codex App 取代代码编辑器。

「我最开始很想要一个代码编辑器，」Dominik Kundel 在 Slack 里写道，「但现在我的大部分修改只需要留下一条行内评论，处理速度快得惊人。」

Andrew Ambrosino 发现，自己虽然仍然需要引导模型的方向，但已经不用再手动去改它的代码了。

Mia Glaese 也将 GPT-5.2 视为一个转折点：「当时我就觉得：『哇，我对它能帮我做的事情感到很兴奋。』」

放眼整个行业，那个圣诞假期成了一个分水岭，开发者们用 Anthropic 的 Opus 4.5 和 OpenAI 的 GPT-5.2 端到端地构建出了完整的应用，全程没有手写一行代码。

到 2026 年 1 月初，整个 Codex 团队都在使用 Codex App。接下来，他们需要验证 OpenAI 内部的其他人会不会也用它。Andrew Ambrosino 说，如果大家不用，那就只能「推倒重来」。

到了 2 月，Codex 桌面 App 在 OpenAI 的工程与研究团队中获得广泛采用。OpenAI 研究员 Noam Brown 表示自己已经「完全切换」到了 Codex。长期使用终端和 Emacs 编辑器的 Greg Brockman 也切换了过来，他说回到自己以前的工作流「感觉就像穿越回了过去」。Sam Altman 后来更是称它是 OpenAI 内部「有史以来最受喜爱的产品」。

Codex 团队造出了一个让内部开发者爱不释手的产品。但当年的 Codex Cloud 在 OpenAI 内部同样很受欢迎，推向外部后却遭遇了失败。这一次，会有什么不同？

## 06

## 从大厂内部的边角项目，

## 到 ChatGPT 的底座

2026 年 2 月 2 日，Codex macOS 桌面 App 正式面向公众发布。它看起来更像一款聊天应用，不是代码编辑器。侧边栏里放着正在进行和历史上的任务，点击其中一个，就能看到 Agent 已经完成了哪些工作，也可以继续向它发送指令。

你可以让一个 Agent 修 bug，让另一个去开发新功能，再在它们之间切换，回答问题或审查改动。每个 Agent 都能在自己的一份代码副本上工作，不会覆盖其他 Agent 的成果。你既可以随时介入把控方向，也可以让几项任务在后台同时运行，等它们需要你的时候再回来处理。

在当时，这些功能并不算特别突破。比如 Claude 桌面应用，好几个月前已经允许技术与非技术用户做同样的事。但 Claude 桌面端是先有 Chat，再逐步加入 Code 和 Cowork，多个入口拼在一起，让界面显得混乱且生硬拼凑。用户很难判断不同任务该进入哪个标签页，也弄不清每个页面究竟有哪些功能和权限。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/5icxfcvT9UmjJeoPvvqrhc3AYfCu8iccAKaxof9zlGby9UeYkddPq2E6vBzKNgXUVgCYqR661WOjH4Kz07OVhhavlLEpvgNZdkuQq4qT1rf5A/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=7)

Codex App 没有这些历史伤痕，作为后来者，Codex 团队看清了这条已被验证的演进轨迹。第一次使用它时，我搭配了几天后发布的新模型 GPT-5.3 Codex。它快速、简单，而且完全是为 Agent 原生设计的。整个体验有一种流动感，只有产品每个细节都做对时，才会出现这种感觉。

正因为团队坚持不内置代码编辑器，他们必须确保，Codex Agent 能在 App 里完成用户几乎所有能做的事。比如想连接一个新工具时，用户不再需要去菜单里翻找，直接告诉 Agent 就行。

几天后发布的 GPT-5.3 Codex，让 Codex 开始走出编程。据 Mia Glaese 介绍，这是模型训练第一次不再只围绕编程展开，团队开始考虑，一个编程 Agent 还需要具备什么能力，才能服务各类知识工作？

这对我的工作流立刻产生了影响。此前我几乎只用 Claude，之后却把大部分工作切到了 Codex。3 月初 GPT-5.4 到来后，Codex 正式成为我的日常主力工具，Every 团队里的许多人也开始每天使用 OpenAI 的工具和模型。正如我们在 GPT-5.4 的 Vibe Check 中所写：OpenAI 回来了。

同样的变化也发生在 Every 之外。到 3 月 19 日，OpenAI 表示 Codex 周用户已经超过 200 万，整体使用量自年初以来增长了五倍。

4 月，Codex 加入应用内浏览器，让 Agent 可以搜索信息，并在真实网页上检查自己的工作。它还能跨其他 Mac 应用操作，展示文档、幻灯片和电子表格的预览。即使从未写过代码，一个人也可以要求它制作演示文稿或预算报告，并且不离开 App 就能看到结果。

到 6 月，Codex 周用户超过 500 万，其中大约五分之一是知识工作者。

7 月 9 日，Codex 桌面 App 正式并入 ChatGPT，成为新的 ChatGPT 桌面 App，把聊天功能装进了它里面。在底层代码里，新版 ChatGPT 的应用名称仍然是 com.openai.codex。

![图片](https://mmbiz.qpic.cn/mmbiz_png/5icxfcvT9UmjYZjCzvvHzMmXBia7ysS1Qjxp8T21IZIBIVx3Noq2ZWgqwHRRHucdiccbx0znOfMEvgcZ8t8Xuph53V9vziaNbGQUVu7vpgH7mFs/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=8)

Codex Cloud 当初是 ChatGPT 里的一个标签页。现在，ChatGPT 运行在 Codex 之上。

Ed Bayes 记得，宣布合并的全员大会结束后，他走出会场，脑海里想的是团队究竟走了多远。起初只是「角落里的几个人」，如今却已经成了「ChatGPT 的未来」。

「这简直是美国公司史的一部分。」他对我说。

在合并前一个月，2026 年 6 月初，我再次与 Alexander Embiricos 坐进一间会议室。他的职位刚从 Codex Agent 产品负责人变成了 OpenAI 企业产品负责人。

我问他，他的团队如何从 Codex Cloud 的失败，一路造出后来成为 ChatGPT 底座的产品？又是怎样避开我担心的那个「结对编程陷阱」？大多数团队都会沿着已经奏效的东西继续建设，Codex 团队却没有。是什么让他们能够持续向前？

Alexander Embiricos 拿起一支黑色马克笔，在身后的白板上画出 Codex 的增长曲线。首先是 Codex Cloud，短暂冲高后迅速躺平。第二条是 GPT-5 发布后陡峭爬升的 CLI。第三条是更高的编辑器扩展。最后一条是 GPT-5.3 Codex 与桌面 App，这条曲线让前面所有的曲线都相形见绌。最开始画下的第一道痕迹，看起来就像白板底部的一道微小划痕。

他画在白板上的曲线，很像已故哈佛教授 Clayton Christensen 在《创新者的窘境》中描绘的图。底层技术的每一次跃迁，都会催生更简单的产品形态，撬动规模更大、技术门槛更低的市场，并超越上一代产品。

传统计算时代需要历经半个世纪、在一家又一家新老交替的公司之间演完的规律，在 OpenAI 内部仅凭几个人的小团队，就在 10 个月内走完了全程。每一次模型能力变化，都撑破了原有的交互界面，催生出不同的产品形态。

在《创新者的窘境》里，乘着上一条制胜曲线的团队，几乎从来没能站上下一条曲线，现有产品的成功会扼杀掉后面的新事物。

Codex 团队之所以能避开这个命运，一方面是因为 OpenAI 允许内部多个团队像创业公司组合一样并行探索，再把有效路线合并。Codex 团队也获得了空间，可以在 ChatGPT 的庞大体量所带来的束缚之外，独立迭代自己的产品和模型线。

另一方面，用 AI 开发 AI，也改变了产品研发的物理规律。在传统公司，启动一个新产品需要开几个月的会，去争抢预算与工程师，现有爆款几乎总是赢家。而在 OpenAI，因为团队用 Codex 开发 Codex，几个人就能在几周内做出一个新的产品入口。「现在要说服别人，已经不需要讲那么多了。」Tibo 此前对我说。

望着白板，Alexander Embiricos 还有一条新曲线要画。既然已经有数百万人在自己的本地电脑上信任了这个 Agent，下一步，是重新回到去年春天失败的那个愿景：让 Agent 在人离开之后，仍然长时间持续工作。

「我们会转向异步，」他说，「这意味着，我们必须重新把它托管到云端。」

这一次，我注意到，他放在会议桌上的那台笔记本电脑，屏幕盖子已经完全合上了。

![图片](https://mmbiz.qpic.cn/mmbiz_png/UrL1kkHON7Kcz8Or5brWBwzqAYIlYKibyEbpPpNkVwSABfH4YXdCWaLlDdicEyZicYTMbVsPqiatsWtgyIlVsfbemF4pOsJA6npibOGqoicSNSRo8/640?wx_fmt=other&from=appmsg&wxfrom=5&wx_lazy=1&tp=webp#imgIndex=3)

**更多阅读**

[独家对话 Karpo：Personal AI 的终局，是用户意图的「竞争」，但这还不是行业共识](https://mp.weixin.qq.com/s?__biz=MzY5ODQwMTkxNA==&mid=2247517294&idx=1&sn=4fc5c9ae9c4f4dd8cde7129b5c2a85b9&scene=21#wechat_redirect)

[人人都想当你的 Personal Agent，却没人知道它应该长什么样](https://mp.weixin.qq.com/s?__biz=MzY5ODQwMTkxNA==&mid=2247517258&idx=1&sn=fec86dc55a9be81dac3441ee2d587f92&scene=21#wechat_redirect)

[Lovart 2.0 发布个人设计 Agent Arti：Personal Agent 在设计赛道先落地了](https://mp.weixin.qq.com/s?__biz=MzY5ODQwMTkxNA==&mid=2247517324&idx=1&sn=4939b4b57340578f45ce48058b7bbe84&scene=21#wechat_redirect)

[a16z AI 应用 Top 100：只有 4.5% 的用户愿意付费订阅，AI 产品该换种方式收钱了](https://mp.weixin.qq.com/s?__biz=MzY5ODQwMTkxNA==&mid=2247517225&idx=1&sn=e641d2d5c090f736b36efe76cb1e2a85&scene=21#wechat_redirect)

转载原创文章请添加微信：founderparker

闪记

复制 LaTeX 公式