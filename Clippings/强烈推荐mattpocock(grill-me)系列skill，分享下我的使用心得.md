---
title: "强烈推荐mattpocock(grill-me)系列skill，分享下我的使用心得"
source: "https://linux.do/t/topic/2952622"
author:
  - "[[zerosoul]]"
published: 2026-09-25
created: 2026-10-19
description: "grill-me/grill-with-docs 这个热度极高的Skill很多人应该都用过，但是我发现大多数人也仅限于此，只会用这两个，而我在实践过程中发现，grill-me/grill-with-docs仅仅是mattpocock的skill体系中的一环，matt做的这套ski"
tags:
  - "clippings"
---
grill-me/grill-with-docs 这个热度极高的Skill很多人应该都用过，但是我发现大多数人也仅限于此，只会用这两个，而我在实践过程中发现，grill-me/grill-with-docs仅仅是mattpocock的skill体系中的一环，matt做的这套skill需要成套相互配合使用才会发挥最大的效果，我现在已经极为依赖这套skill。

我以前比较依赖Superpowers，但Superpowers有点太重了，而且遇到比较大的项目有时候容易走偏，太小的项目触发Superpowers又完全是白白多浪费时间和token。  
而matt的这套skill使用起来就灵活了很多，各种大小的项目都可以适应，并且以前用Superpowers容易走偏的项目用matt这套能稳步推进，效率比以前高了很多。

只是matt的这套skill数量有点多，学起来需要一定时间，我把我在实践过程中对他的这套skill的配合用法总结一下，尽量给大家一个直观印象，相当于脑中建立一个基础索引，然后需要的佬可以再针对性的学习对自己有用的具体skill。

**注意：这套Skill需要用户学会之后主动按需调用，而不是Superpowers那样自动触发并一干到底，如果没按正确用法使用很难达到预期效果**

## 核心设计

首先，按matt的想法，常规项目工程化的路径有一个大致的顺序（非常重要），这个顺序每一步分别对应一个skill：

1. **对齐想法** - /grill-with-docs: 跟用户对齐想法，并沉淀共识文档
2. **落实文档** - /to-spec: 把想法落实成设计文档（上一步的文档只是共识想法，这一步才是Spec）
3. **拆分任务** - /to-ticket: 把设计文档拆分成可以独立完成的多个任务(ticket)
4. **完成任务** - /implement: 新开session调用它实现拆分好的指定ticket，比如/implement 01
5. **审核代码** - /code-review: 审核代码有没有按设计完成，是否符合规范(/implement会自动调用)

我认为这是matt系列skill最核心的设计，非常重要，一定要理解这个工程化路径步骤，其它很多skill也都是围绕这个工程化路径做辅助

工程化核心步骤有了，但是要实现这套步骤，必须要通过一套流程化的文档让Agent能遵守，前面的每一步骤都应该能遵守不跑偏，因此在这5步真正开始之前，还应该先设计好一套大家都要遵守的标准，因此就有了/setup-matt-pocock-skills这个skill，我把它称作工程化路径的步骤0，**这一步应该在项目刚刚建立，新建了文件夹后的第一步就执行**

0. **设置标准** - /setup-matt-pocock-skills: 初始化每个步骤都应遵守的标准文档，确定术语，配置issue tracker、文档布局等

## 使用细节

上面是matt这套skill的最核心设计，记住上面几个skill，已经能应付大多数的项目了。  
但上面的skill也有一些灵活用法和注意事项，所以下面我稍微深入说一下

- matt的这套skill依赖文档驱动，基本不依赖上下文，因此拆分的ticket都可以在新的session中实现，不用喂给它上下文，这点非常爽，换Agent实现完全无痛，但是matt建议**从/grill-with-docs到/to-ticket(步骤1-3)这个过程尽量在一个上下文中完成**
- grill-me/grill-with-docs有时候问的问题会非常多，你调用这个skill的时候可以告诉它有些优缺点十分分明的选项让它自作主张不用问你。让它提问之前你告诉它的信息也要足够并且有效，否则它没完没了的问，matt专门出视频讲过这个问题([https://www.bilibili.com/video/BV1zn396mEfz](https://www.bilibili.com/video/BV1zn396mEfz))
- 有些人可能会奇怪，/grill-with-docs和/to-spec都是把想法落实到文档，功能是不是重复了，实际上他们产生的文档类型不同，/grill-with-docs产生的是拷问用户达成的共识文档，比较零散，/to-spec是把所有共识文档整理总结后的真正设计文档
- 上面的项目**工程化0-6的步骤，并不是强制的**，可以根据项目大小等具体情况调整，比如，小项目可以/grill-with-docs之后直接直接跳到/implement开始实现，跳过/to-spec和/to-ticket，或者只跳过/to-ticket也行
- 为什么有了spec之后非要拆分成ticket，这个问题的答案也是matt的核心思想之一，现在的大模型虽然都有1M的上下文，但真正的smart zone仍然只有不到200K(因此命令GPT支持1M上下文但codex默认设置才不到300K), 上下问变大之后就会注意力下降流口水，因此通过拆分任务，可以把每个ticket实现需要的上下文都控制在smart zone以内(**每个ticket都推荐在新的session中实现**)。  
	并且拆分ticket也可以控制项目的模块化进展。
- /to-ticket拆分的ticket会包含依赖关系，有些ticket需要等前面某个ticket完成之后才能开始，无依赖的ticket可以多个session并行开始
- /code-review 会开两个subagent并行审查代码，一个审查代码规范，是否有bug等，一个审查是否偏离设计目标，很有用
- /implement跟你直接让它开始干的区别是，这个skill会自动调用/tdd来实现，并自动调用/code-review来审查代码，因此上面的0-6步骤，步骤6一般是自动完成的，但你也可以随时手动调用来审查刚写的代码
- /implement-spec可以自动按依赖关系和顺序用subagent实现一组spec拆分的ticket。这个skill是新出的，之前ticket只能用户自己开session实现，不能在一个session中自动化全部完成，我还特意自己写过一个skill解决这个问题，现在有了官方的版本了
- /ask-matt这个skill非常有用，它就是一个matt系列skill的帮助skill，实际上我上面说的内容，你用这个skill问都它都能给你给出更详细的解释，任何matt系列skill相关的问题都可以用它提问，包括使用方法、是否适用、推荐流程等

## 其它Skill

他的其它很多skill也非常有用，我说下我常用的几个

- /improve-codebase-architecture 架构优化，排查重复代码，提供代码模块化优化等建议，注意这个skill的结论大多数都需要进行一轮从grill-me/grill-with-docs开始的工程化1-5步骤，当然有些比较简单的整改你直接让AI自己改也可以。我一般/improve-codebase-architecture结束后我都会每个候选fork一个session，每个候选都在fork的session中走后续流程
- /wayfinder 这个skill对比较大的项目非常有用，有些项目你设计的时候自己可能都没想清楚有些地方具体要怎么实现，这时候grilling是从用户问不出足够有效信息的，直接上来grilling反而容易让设计文档走偏，这时候用这个skill让它引导走一遍规划过程，能现在就定下来的内容会生成可以直接实现的ticket，现在还无法定的内容会生成决策ticket，决策ticket是后续需要进一步探索的ticket，不是可以直接实现代码的ticket，这样整体项目的规划路径就可以先定下来，然后随着项目推进慢慢会把最开始看不清的迷雾慢慢吹散。决策/wayfinder生成的决策ticket可以用/wayfinder TICKET\_ID/TICKET\_PATH这样的方式完成
- /codebase-design这个skill推荐设计模块/接口时使用，实现ticket的时候也可能会按需自动调用它
- /prototype 先不真正写代码的情况下，根据你的描述快速做出几个备选原型让你选
- /writing-for-agents 把你想让Agent遵守的内容写到相关的文档，用这个skill比自己编辑文档要好很多，给Agent读的文档并不是越详细越好，它会按适合Agent读的方式组织语言，并且尽量节省token
- /handoff 顾名思义，交接用的，把当前session内容生成文档，别的session读了就可以直接继续干活，不过用了前面0-6步骤的项目几乎不需要这个skill
- /wait-what 把太啰唆的Agent回复简化，说人话。但是我实测，你直接让Agent用大白话重新讲，效果也很不错，有时候更容易看懂
- /research 启动subagent调研，不占用主session上下文。这个skill提示词内容很简单，最核心的思路就是查到的东西要刨根问底找来源，不要相信别人信口雌黄说的，所以调研结果准确度还不错
- /teach 让它教你理解项目，会生成一个网页，可以互动，还有问答题让你加深知识

## 表格总揽

| Skill | 功能 | 备注 |
| --- | --- | --- |
| /setup-matt-pocock-skills | 配置 issue tracker、文档布局 | mattpocock工程化步骤0/5，一切的开始 |
| /grill-with-docs | 对齐想法并沉淀文档 | mattpocock工程化步骤1/5 |
| /to-spec | 想法落实成设计文档 | mattpocock工程化步骤2/5 |
| /to-ticket | 拆分成较小的ticket，每个ticket可以单独完成 | mattpocock工程化步骤3/5 |
| /implement | 使用/tdd实现计划并用/code-review检查 | mattpocock工程化步骤4/5，可跳过spec和ticket直接实现 |
| /code-review | 检查是否按规范和设计文档来的，会调用2个subagent | mattpocock工程化步骤5/5 |
| /implement-spec | 对spec对应的所有ticket按依赖顺序在worktree自动实现 |  |
| /tdd | 用Test-Driven Development方法开发 |  |
| /codebase-design | 设计原则，规范代码形状，规范深度模块设计 | /tdd会自动调用，推荐设计模块/接口时主动调用 |
| /prototype | 做原型 |  |
| /research | 调用后台agent调研，不占用主session |  |
| /improve-codebase-architecture | 代码库健康巡检，空闲保养，HTML 可视化报告 | 它的下一步是对每个想做的候选进行grilling→spec→impl |
| /handoff | 把当前工作交给另一个Agent Session |  |
| /teach | 可以生成HTML引导课程教你想学的 | 学习开源仓库也可以用 |
| /wait-what | 把太啰唆的Agent回复简化，说人话 |  |
| /writing-for-agents | 用来写给Agent看的文档，会防止文档无效上下文占用 |  |
| /wayfinder | 为大项目规划决策ticket |  |
| /domain-modeling | 规范事物叫什么、指什么，沉淀在 CONTEXT.md |  |
| /triage | 面向工单的 AI 自动分诊与处理工作流，多人协作才需要 |  |
| /retro | 复盘Agent前面几个Session做的工作，看下次能不能做的更好 | 主要针对Agent的，而不是项目 |

## 视频推荐

这个视频覆盖了我写的很大一部分内容，推荐学习：

![](https://i0.hdslb.com/bfs/static/jinkela/long/images/favicon.ico) [哔哩哔哩](https://www.bilibili.com/video/BV1zUh56RE8k/?vd_source=32468b8f1b914911548382372c3e1778)

![](https://cdn3.ldstatic.com/optimized/4X/b/6/4/b644fe226dcd865a7241750c47c15ba209ed8b73_2_690x388.jpeg)

### [Matt Pocock：十分钟讲完 25 个 Skills | mattpocock/skills v1.2.3【中英字幕】\_哔哩哔哩\_bilibili](https://www.bilibili.com/video/BV1zUh56RE8k/?vd_source=32468b8f1b914911548382372c3e1778)

Matt Pocock：十分钟讲完 25 个 Skills | mattpocock/skills v1.2.3【中英字幕】共计2条视频，包括：【中英字幕】Matt Pocock：十分钟讲完 25 个 Skills | mattpocock/skills v1.2.3、【中配中字】Matt Pocock：十分钟讲完 25 个 Skills | mattpocock/skills v1.2.3等，UP主更多精彩视频，请关注UP账号。