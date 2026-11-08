---
title: "yetone 的魔法：magpie 是怎么让 AI 自己维护项目的"
source: "https://x.com/wquguru/status/2109650264601117141"
author:
  - "[[@wquguru]]"
published: 2026-10-12
created: 2026-11-08
description: "关于全 AI 自动化构建软件该不该存在的问题，最近终于爆发了。起因是 @yetone 维护的 magpie，被同行喷“快餐式服务”、“不太敢用”。相信大部分朋友已经有共识，AI 自动化构建软件是大势所趋，那么 magpie 是怎么实践的呢？我把 magpie 拉下来，分析了过去十..."
tags:
  - "clippings"
---
![图像](https://pbs.twimg.com/media/HUb0sJGbwAAxeXV?format=jpg&name=large)

> 关于全 AI 自动化构建软件该不该存在的问题，最近终于爆发了。起因是 [@yetone](https://x.com/@yetone) 维护的 magpie，被同行喷“快餐式服务”、“不太敢用”。

相信大部分朋友已经有共识，AI 自动化构建软件是大势所趋，那么 magpie 是怎么实践的呢？我把 magpie 拉下来，分析了过去十来天的 2,862 个 commit，顺手拿 OpenClaw 做个对照。

> 10月12日
> 
> 关于全 AI 自动化构建软件该不该存在的问题，最近终于爆发了。 这次事件的主角是 @yetone 的 magpie： 从 9 月 23 日建仓开始算，短短 19 天积累了 9200 星 版本号已经到 v0.1.1203，过去 24 小时发了 25 版

## 19 天 1204 个版本

magpie 是个本地 LLM 网关，能把 Claude Code、Codex、Gemini CLI 这些编程 agent 接到任意模型和订阅上。9 月 22 日第一个 commit，到今天 19 天，9,474 星。2,862 个 commit 里 yetone 账号占 85%，合并了 383 个社区 PR。

tag 数（等同版本） 19 天高达 1,204 个，一天平均 60 多个版本，人手可发不出这个频率。对比之下，OpenClaw 头 19 天是 1,423 个 commit，99% 是 Peter Steinberger 自己提的，tag 大概 10 个。

magpie 的 commit 多了一倍，版本多了一百多倍。

**我想搞清楚的就一件事：AI 在这个项目里到底是怎么闭环的。**

## 一张路由表，一本错题本

magpie 的 CLAUDE.md 只引用了两个文件，AGENTS.md 和 LESSONS.md。

AGENTS.md 是张路由表，自己不写规则，只告诉 agent 干什么活之前翻哪份文档：改子系统先看 docs/subsystems/，写代码、审代码照 docs/code-standards.md，审社区 PR 看 docs/contributors.md。

LESSONS.md 第一句就回答了最开始的问题：

> magpie's code is written, reviewed, merged and released by agents. （magpie 的代码由 agent 编写、审查、合并和发布）

![图像](https://pbs.twimg.com/media/HUb01bUbAAA08m8?format=jpg&name=large)

写、审、合、发，全是 agent。那没人盯着，它凭什么不翻车？答案就在这个文件里。479 行，说白了是一本错题本，而且是 agent 自己每晚写的。

每天夜里，agent 把当天的 commit 全过一遍，关注三个场景：

1. 哪些修完又返工了
2. 哪些压根不该合
3. 哪些验证做得太糙

每揪出一个就记一条，一句规则，一段原因，后面挂上 commit 和 issue 号当证据。比如这条：

> **Reproduce the reporter's exact case, on the surface they use, before you call it fixed.** 834 came back 4 times (v0.1.920 → .925 → .931 → .938). Each round fixed only the agent in the screenshot. Seen 1× (2026-10-05).

834 来回返工了 4 次，每次都只修了截图里那一个 agent。所以规矩是，说修好之前，先在报告人用的那个界面上把问题原样复现一遍。

关键是最后那行 Seen 1×。**同一条教训，如果在 3 个不同日子的复盘里都出现了，就从 LESSONS.md 挪进 code-standards.md，从经验变成硬规则。** 之后每个 PR 审查都要逐条对。

已经有 8 条这么转正了。比如同类的 bug 要一起修掉（10-05、10-06、10-07 各抓到一次）；main 上挂掉的测试就是马上要修的 bug；合并前要写清楚跑了什么、在哪个 commit 上跑的。

当然错题本也记录做对的事情，标成 Done right，agent 读到的除了别这样，还有照这个来。

![图像](https://pbs.twimg.com/media/HUb08bXa0AAkh5M?format=jpg&name=large)

## 错题本是 10 月 6 日凌晨才引入

这套东西是一开始就设计好的吗？翻 LESSONS.md 的提交记录，第一版是 commit 303819c5，10 月 6 日凌晨 3:10。

再往前一天，10 月 5 日，magpie 发了 168 个版本。

LESSONS.md 第一版里就记着这天。220 个 commit，大约 170 次发版，其中 40 来个是在修当天或前一天刚发出去的版本。CI 几乎每一轮都被下一次 push 取消，有个只在 Linux 上挂的测试，从 v0.1.877 一路红到 v0.1.892，愣是没人发现。

> 294 tags in 51 hours left no run to finish. （51 小时 294 个 tag，没有一轮 CI 能跑完）

于是第一版里就多了一条：**打 tag 前，这个 commit 的 CI 必须跑完、全绿，被下一次 push 取消的不算。**

![图像](https://pbs.twimg.com/media/HUb1AI4aQAA9Cjx?format=jpg&name=large)

168，第二天 42，第三天 15，之后一直在 15 到 26 之间。

中间没人开会，也没人发通知。夜审翻出问题，往错题本里加了一条，后面干活的 agent 读到了，发版就慢下来了。

这样看来，昨晚被拿来说事的一天二十几版，其实已经是踩过刹车之后的速度。

## PR 验收标准

接着看看真实的 PR：

code-standards.md 里一共 6 条验收标准，全过才能合并或发版。三平台编译、沙箱跑测试这些常规的就不说了，有三条是一般项目里少见的：

1. 回退测试 把旧代码放回去，新写的测试必须真挂，而且挂得明明白白，指出是哪个行为错了；编译不过、测试被跳过都不算
2. 真实使用 改了哪家厂商的接入，就得拿真账号、真配置、真接口返回去验。没实测过的功能，不许在上面接着开发，也不许跟用户说能用
3. 没跑的要写出来：

> A check that wasn't run is listed as not run, never left out. （没跑的检查要列为没跑，不能省略不写）

然后我随手挑了 #1339，看它合并前留的那条评论：

![图像](https://pbs.twimg.com/media/HUb1CjLaIAEn__a?format=jpg&name=large)

Red check 就是回退测试，Break check 是故意改坏看测试能不能抓到，最后一行写着 Not run，真机没测就是没测。

合并命令还带着 --match-head-commit <审过的 sha>，审的过程中要是有人又 push 了，合并直接失败，确保没审过的代码进不来。

## Human in the Loop

当然，人总归是要参与一些工作的，至少有这几样：

- 拍过板的产品决定：“Don't reverse deliberate decisions”，滚动行为、按钮光标这种，PR 不能改
- 安全闸门：风险检查一旦命中，等 maintainer 放行
- 社区建议：474 个 commit 标题里写着报告人来自 X 或 Discord，比如 JonahFu on X、Jeremy.Zhou on Discord

说到底，人管方向、守闸门，写、审、合、发都交给 agent。

## yetone 是不是还藏了一手？

写到这儿肯定有人问：yetone 是不是还藏了一手？我也好奇，又专门翻了一遍。

确实有几样东西仓库里找不到：

- 夜审怎么触发的没写，4 个 workflow 没一个是定时的
- 我把 7 次更新 LESSONS.md 的时间拉出来，03:10、03:49、00:23、23:46、03:48、14:24、05:26，东一个西一个，不像定时任务，更像本地手动跑或者自己写的脚本
- 夜审用的提示词也没有，用的哪个 agent、开几个会话并行，同样没写

顺带挖到两样前面没提到的东西：

**一是这套方法里有社区的功劳** 子系统文档和语义变更审查，是社区成员 Junjie Zhou 的 PR #889 带进来的。code-standards.md 开头那两张表，commit 926bcaa3 的说明里写得明明白白，是 Junjie Zhou 在 Discord 上提的六条审查规则。

**二是 yetone 平时怎么跟 agent 说话，commit 里都留着** 有 52 个 commit 标题，括号里原封不动放着 yetone 的原话：

```text
(the owner: 这个太丑了)
(the owner: 这里为啥是原生的 selector 而不是我们抽象的 ComboBox？)
(the owner: 这个为什么又加回来了啊？不是说 hover 的时候才出现吗？一直出现太丑了)
(owner: pr-preview 的时候有时候没有数据压根儿测不了，能否帮忙造一些假数据)
```

基本都是一句话的吐槽，剩下的 agent 自己补齐，一个 commit 正文动不动几百字。上面那句造一些假数据，后来就成了 CI 录屏用的那套假数据。

人说哪里不对，agent 把它变成能验证的改动。这几十条 commit 标题，比方法论文档讲得还清楚。

## 想自己搭一套的话

路由表谁都会写，真正要抄的是错题本这一套。一条 LESSONS 大概长这样：

```text
**<一句话规则>**
- <哪个 commit / issue 出的事，后果是什么>
- <修复的 commit>
- Done right: <做对的例子>
- Seen N× (YYYY-MM-DD, YYYY-MM-DD).
```

每天让 agent 复盘一次当天的 commit，只找返工的、不该合的、验证太弱的。同一条在 3 个不同日子出现，就挪进代码规范。验收时把回退测试、真实使用、没跑的项目都写进 commit 正文和 PR 评论。

翻完整个仓库，我印象最深的是那个 Seen 3× 的门槛。犯过的错写下来，agent 下次启动一定会读到，同一个错犯满三天就升成硬规则，正好印证了“事不过三”的约定俗成。

## 说在最后...

如果放在一年前，甚至半年前，模型能力几乎很难达到生产级别的自动化程度，而当前，尤其是 Opus 5.5 出来之后，我们能看到——未来已来。

此时，我也想起来 [@yuanhao](https://x.com/@yuanhao) 的 Yoyo，一只已经自我迭代 200+天的 Agent：[https://yoyo-gasp.yolog.dev/](https://yoyo-gasp.yolog.dev/)，也很值得看看。