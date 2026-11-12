---
title: "Claude 的记忆怎么维护：Anthropic dreaming 机制与实现"
source: "https://mp.weixin.qq.com/s/ZjvQiukT30PyM48djsMFVA"
author:
  - "[[oldpan博客]]"
published:
created: 2026-11-10
description: "Anthropic 的 dreaming 如何把历史经历整理为可复用的记忆？从四层记忆结构到 Dreams、动态工作流与知识 Wiki，梳理实现路径、评测证据和工程边界。"
tags:
  - "clippings"
---
老潘 oldpan博客 *2026年11月7日 16:29*

Dream 机制其实已经不新鲜了，我也不知道我什么时候听到这个术语的，之前在尝试搭建自己 agent 的时候好像也是从 Claude 官方了解到的。

《The components of agent memory》是 Anthropic 工程团队的 Lance Martin 在 2026 年 11 月 6 日发的一篇研究文章，讲 agent 怎么把过去的经历变成下一次能用上的记忆。 **核心机制叫 dreaming：一个在后台运行的离线过程，回看 session 日志和已有笔记，修掉写错的内容，再整理成更容易读取的结构。** <sup>[1]</sup>

做法上，文章把记忆拆成原始记录、笔记、wiki 这类组织结构和每次注入的上下文四层，dreaming 可以往每一层写。官方同时给了两套能跑的实现：Managed Agents 里的 Dreams（research preview），以及用 dynamic workflow 自己搭的 dreaming cookbook。后者的流程是一份 transcript 交给一个 analyzer，最后由一个 organizer 收尾。 <sup>[2]</sup> <sup>[6]</sup>

效果上，CL-Bench 数据库任务里 Opus 5.5 有了记忆目录后，mean reward 从 0.655 提到 0.838。在 Stainless 约 4.2 亿 token 的内部语料上， **dreaming 建出来的 wiki 加搜索做到 61%，单用搜索是 53%，每题还省了约 2 万 token。** 这些变化都发生在模型下一次读取的上下文里，模型权重不变。 <sup>[1]</sup>

比较关注这里的工程问题：哪些经历应该留下，已有结论错了怎么改，整理出来的内容又能不能被下一次任务找到。

我们一起看看吧。

## 1 记忆放在哪里

==文章对 agent memory 的定义比较窄：Claude 从经历里获得、跨 session 保留、之后还能读到的知识。== 权重更新、单次对话里的 in-context learning、把旧轮次替换成摘要的 compaction，都不算在内。 <sup>[1]</sup>

在这个定义下，记忆从下到上分四层。下表前两列按原文整理，最后一列是对工程用途的归纳。

| 层次 | 保存的内容 | 主要用途 |
| --- | --- | --- |
| Transcripts | 用户请求、工具调用、工具结果等可搜索的事件日志 | 回查发生了什么 |
| Memory notes | session 中或结束后写下的关键观察，比如 memory store 里的文件 | 减少重复探索 |
| Memory representations | wiki 这类结构，按主题组织、页面之间互相链接 | 跨任务查找与关联 |
| Injected context | 每个 session 一开始就加载的少量内容 | 新 session 一开始就知道去哪里找 |

![图 1：跨 session 的记忆分层，dreaming 从 transcript 往上写到各层（from Anthropic）](https://mmbiz.qpic.cn/sz_mmbiz_png/ezjZug0fpibx97PEicsDrl20KZrs3QfVPSb27pPmP3AZ2YNctTI6CXAIRgibKqHSSPZ4JzNGQvKo1qP0XGhD7Xd0GBozjZ1pO87djXpWQap3Nk/640?from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

图 1：跨 session 的记忆分层，dreaming 从 transcript 往上写到各层（from Anthropic）

图 1：跨 session 的记忆分层，dreaming 从 transcript 往上写到各层（from Anthropic）

Dreaming 读的是最底层的 transcript，可以往每一层写，也可以在相邻的上层之间搬运内容。比如把一条经常用到的笔记提升到注入层，每个 session 一开始就能看到。

不过注入层要克制。文章提醒，注入的内容每次都占 token，写错一条会扩散到所有 session，指令文件太长还会降低遵循度。Claude Code 的文档也建议单个

```
CLAUDE.md
```
控制在 200 行以内。 <sup>[1]</sup> <sup>[4]</sup>

这几层不需要每次完整走一遍。比如当前任务只需要一个编译命令，读相关笔记就够了，遇到矛盾再回到原始日志核实。短索引的作用是让模型知道有哪些信息，细节留在可以按需读取的位置。

Managed Agents 的 memory store 是一组按路径寻址的文本文件，单个文件上限 100 kB，一个 store 最多 1 万个文件。store 只能在创建 session 时挂上，每个 session 最多挂 8 个。挂载后 store 出现在

```
/mnt/memory/
```
下，agent 用普通文件工具读写。 <sup>[3]</sup>

**挂载时注入 system prompt 的只是每个 store 的名称、挂载路径、读写模式、描述和使用说明，整份知识库并不会进入 prompt。** <sup>[3]</sup>

Claude Code 的 auto memory 也是这个思路：启动时只加载

```
MEMORY.md
```
的 **前 200 行或前 25 KB，以先达到的限制为准** ，细节放在主题文件里按需读取。写入后如果接近上限，Claude Code 会提醒 Claude 精简索引。这个限制只针对
```
MEMORY.md
```
，和前面
```
CLAUDE.md
```
的 200 行建议是两回事。 <sup>[4]</sup>

**==这里最容易做错的，是把长期目录当成第二份聊天记录。==** ==一个命令已经失效，原样保存得再完整，下一次还是会把 agent 带到旧路径上。更稳妥的做法是优先保留可复用结论，同时留下来源和适用版本。==

## 2 有记忆目录，模型还得会用

Anthropic 用 CL-Bench 1.0 中的数据库任务比较了不同模型。每道题启动新 session，答题后给出正确解答，只有 memory 目录跨题保留。 **图中数值是该任务的 mean reward，不能当成完整 CL-Bench 的总成绩。** <sup>[1]</sup>

![图 2：CL-Bench 数据库任务，各模型有无记忆的 mean reward（from Anthropic）](https://mmbiz.qpic.cn/sz_mmbiz_png/ezjZug0fpibyXfj6bLMdicUCfrOExaBKQDejHNJ9weIJrrlpVIGl286ayUaWBHZK25esWP7ib7Y527kYBWmPOhxPwPHnNyAERO2UZz3WGjMaEQ/640?from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=1)

图 2：CL-Bench 数据库任务，各模型有无记忆的 mean reward（from Anthropic）

图 2：CL-Bench 数据库任务，各模型有无记忆的 mean reward（from Anthropic）

| 模型 | 无记忆 | 有记忆 |
| --- | --- | --- |
| Opus 5.5 | 0.655 | 0.838 |
| Sonnet 5.5 | 0.644 | 0.833 |
| Opus 5 | 0.564 | 0.828 |
| Opus 4.7 | 0.383 | 0.700 |
| Sonnet 5 | 0.306 | 0.610 |
| Sonnet 4.6 | 0.330 | 0.364 |

**同样一个目录，Sonnet 4.6 几乎没吃到收益。** 它常常不读记忆，写下的猜测也没有验证。加上先读记忆、再验证假设的提示后，它到了 0.641。Sonnet 5 答题前 10 次里有 9 次会先读记忆，Sonnet 4.6 不到一半。 <sup>[1]</sup>

再往上看，Opus 4.7 会把笔记合并成参考文档，并标出哪些事实已核实。Opus 5 开始把规则、验证方式和容易踩的坑一起记下来，原文称之为第一次把学习闭环跑通。Opus 5.5 和 Sonnet 5.5 也做到了。

反过来，硬性的写入规则会拖累强模型。要求只记录失败时，Opus 5 的记忆收益少了 0.234，Opus 4.7 少了 0.150，Sonnet 4.6 只少了 0.020。所以文章给前沿模型的建议是简单引导，什么值得记交给模型判断。 <sup>[1]</sup>

个人还没复现实验。这里可以得到的工程启发是， **==评测 memory 时要同时看读和写== ==：==** ==模型有没有读取相关文件，笔记里的规则有没有经过验证，后续题目有没有真正用到它。只统计生成了多少文件，很难回答记忆是否有效。==

例如，一次安装失败之后，记录“这个项目不能使用版本 A”，和记录“版本 A 在环境 B 下因依赖 C 冲突失败，环境 D 尚未验证”，对下一次任务的影响差别很大。后一种写法给出了使用条件，也给后续修正留下了位置。

原文还用 Pokémon Red 比较了记什么。Sonnet 3.7 跑了约 1 万步，写了 225 个文件夹里的 413 个文件，每场战斗、每个 NPC 各一个文件。这些内容很快过时，最后只拿到 1 个徽章。

Fable 5 只写了 10 个文件，记当前目标、道馆计划和路线这些屏幕上看不到的东西，拿到 4 个徽章。Opus 5.5 只维护一个很小的目标文件夹，最后通关。 <sup>[1]</sup>

这些对比里模型和轨迹同时在变，适合用来理解失败机制，不足以单独证明某种目录组织必然更强。

## 3 Dreaming 的两条实现路径

==Dreaming 可以理解为单独运行的一次记忆维护任务。它拿到历史材料和现有记忆，输出更新后的可读内容。至于多久运行一次、由谁触发、结果直接生效还是先审阅，属于 harness 的设计。==

原文举了一个纠错的例子。Pokémon 里 Claude 把 Mt. Moon 附近宝可梦中心的位置记错了，又因为一段单向台阶掉回之前的路线，误以为“Mt Moon DONE”。一次 dreaming 拿笔记和 transcript 对照，找出错误并改写。

用修正后的记忆，Claude 在第 1,935 个动作到达 Cerulean City。用没修正的记忆，它从台阶上掉了三次，最后停在 Pewter City。没有记忆时则一直没有到达。 <sup>[1]</sup>

![图 3：前往 Cerulean City 的进度，dreaming 修正后的记忆、未修正的记忆和无记忆三组对比（from Anthropic）](https://mmbiz.qpic.cn/sz_mmbiz_png/ezjZug0fpibwKJDeqPgKDe3KDicqLicjrO6eUD7cMJH8FZiab4sRdslnTUic1HCRCWQPh2JgppudUkYREy8WSGlhcFaWsxKSEwqzTpAwvf459W00/640?from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=2)

图 3：前往 Cerulean City 的进度，dreaming 修正后的记忆、未修正的记忆和无记忆三组对比（from Anthropic）

图 3：前往 Cerulean City 的进度，dreaming 修正后的记忆、未修正的记忆和无记忆三组对比（from Anthropic）

这和 Letta、UC Berkeley 的 sleep-time compute 有共同思路： ==在用户提出下一次问题之前，先围绕已有上下文做准备工作。== 收益依赖后续问题是否会复用这些准备，离线计算也要计入总成本。 <sup>[5]</sup>

### 3.1 官方 Dreams

Managed Agents 已提供 Dreams，截至 2026 年 11 月 7 日仍是 research preview。目前只在 Claude API 上可用，需要申请访问资格，请求要带

```
dreaming-2026-04-21
```
beta header。一次任务读取一个已有 memory store 和 1–100 个历史 session， **生成独立的新 store，输入 store 保持不变。** <sup>[6]</sup>

```
instructions
```
用来说明关注什么、保留什么、输出约定。这些说明作用于一次整体综合，粒度比逐行编辑粗。一次运行一般几分钟到几小时，计费按所选模型的标准 token 价格，成本大致随输入 session 的数量和长度线性增长。

输出 store 的 ID 在任务进入

```
running
```
后不久就会出现，所以集成时要检查任务是否
```
completed
```
。 **失败或取消后也可能留下部分结果，不能只看见 ID 就切给线上 agent。** 官方的用法是检查输出，再把它挂到后续 session，替换或者和原 store 并用都可以。 <sup>[6]</sup>

下面按官方文档的接口写了一个最小流程，验收那一步是额外补上的建议：

py

dream = client.beta.dreams.create(  
inputs=\[  
{"type": "memory\_store", "memory\_store\_id": store\_id},  
{"type": "sessions", "session\_ids": session\_ids}, # 1–100 个  
\],  
model="claude-opus-5-5",  
instructions="Focus on coding-style preferences; ignore one-off debugging notes.",  
)  
  
while dream.status in ("pending", "running"):  
time.sleep(10)  
dream = client.beta.dreams.retrieve(dream.id)  
  
if dream.status == "completed":  
new\_store\_id = next(  
o.memory\_store\_id for o in dream.outputs if o.type == "memory\_store"  
)  
\# 建议：先在固定任务上做回归，通过后再挂给线上 session

验收可以先简单到检查关键事实是否丢失，再逐渐加入固定任务回归。新旧 store 分开，至少让这一步有一个明确的比较对象。

### 3.2 自建 dynamic workflow

官方 cookbook 给了另一种做法：开发者导出已结束 session 的 transcript，每个 session 一个文件。在一个 session 里，这些文件以只读方式挂载，memory store 以读写方式挂载。lead agent 写出 workflow 并启动，每份 transcript 交给一个 analyzer，全部处理完再由一个 organizer 整理一次。默认 lead 是 Sonnet 5.5，analyzer 和 organizer 是 Haiku 5.5。 <sup>[2]</sup>

![图 4：cookbook 的 dreaming 流程，导出 session、一个 workflow 跑 analyzer 和 organizer、后续 session 只读挂载（from Claude Cookbooks）](https://mmbiz.qpic.cn/mmbiz_png/ezjZug0fpibxL0lcHfvoIZ3qEedZJcGS8pgB6Js8uHiaI43QUXAN47dm6A92elO2Y8PtuR1MS5vOa5fLG7TxuBXw5G7RmQKQN24PIPLXDIy8w/640?from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=3)

图 4：cookbook 的 dreaming 流程，导出 session、一个 workflow 跑 analyzer 和 organizer、后续 session 只读挂载（from Claude Cookbooks）

图 4：cookbook 的 dreaming 流程，导出 session、一个 workflow 跑 analyzer 和 organizer、后续 session 只读挂载（from Claude Cookbooks）

产出是一组小的链接文件，入口是

```
_index.md
```
。 **这条路径第一次运行新建 store，之后每次运行原地更新同一个 store** 。运行前会先保存一份文件副本，每次写入也都留有 memory version。后续工作 session 以只读方式挂载它。 <sup>[2]</sup>

成本上，示例的 11 份 transcript（283 KB）跑完约 2.5 分钟、0.36 美元。50 份长 transcript（约 12 MB）大约 8 美元、10 分钟。notebook 默认预算上限 40 美元，transcript 按每组约 20 份顺序处理。一个 session 最多挂 500 个文件。配套的

```
dreaming_nightly.py
```
可以用 cron 每晚 1 点处理上次运行以来的新 session。

多个 analyzer 会改同一批文件，cookbook 在 prompt 里做了处理：改文件前先重读，写完读回确认，发现被别人覆盖就合并两边的事实再写。organizer 等所有 analyzer 结束后单独运行。

transcript 一律当作不可信输入，analyzer 没有 shell 和网络工具。运行需要 Python 3.11+、

```
anthropic
```
SDK 2.x 和 API 凭据。

Managed Agents 当前仍属 beta，quickstart 文档说明已对 API organizations 默认启用。原生 Dreams 另处于需要申请访问资格的 research preview，两者的开放状态要分开看。 <sup>[7]</sup> <sup>[6]</sup>

| 实现 | 写到哪里 | 需要开发者决定什么 |
| --- | --- | --- |
| Dreams research preview | 新 memory store | 输入、整理目标、验收和切换 |
| Dynamic workflow cookbook | 首次新建，之后原地更新同一个 store | prompt、模型分工、调度和发布流程 |

先参考哪条，取决于需要控制的部分。如果主要想验证记忆整理有没有收益，保持输入和输出分离，前后对比会更容易。如果要研究具体的抽取和合并策略，cookbook 更方便改动。

## 4 Wiki 与搜索怎么配合

原文的 Stainless 实验用了约 35 万份文件、4.2 亿 token 和 25 个评测问题，由 Opus 5 agent 通过共享日志协作建 wiki。随着离线构建从 2 个 session 推进到 128 个，wiki 单独使用从 13% 涨到 48%，wiki 加搜索从 54% 涨到 61%，单用搜索是 53%。 **这些百分比表示评分标准满足情况，不能换算成答对了多少道题。** <sup>[1]</sup>

![图 5：Stainless 实验，随 dreaming 推进 wiki、搜索与组合的得分（from Anthropic）](https://mmbiz.qpic.cn/mmbiz_jpg/ezjZug0fpibzgaBGNOjLzXfTmx8kPLFWSyKft3ibtQzM7m2c5CNIasrpk7nmIVibjbf6Uy5Q0Yzba3TEWasRickGymceicCJhGOFQNUPZffnhQ6Y/640?from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=4)

图 5：Stainless 实验，随 dreaming 推进 wiki、搜索与组合的得分（from Anthropic）

图 5：Stainless 实验，随 dreaming 推进 wiki、搜索与组合的得分（from Anthropic）

同期 wiki 从 103 页、766 条链接长到 222 页、12,893 条链接。这个结果可以这样理解： **wiki 适合提前整理主题关系，原始搜索负责补全细节和核验来源。** 比如查一个项目的迁移历史，索引先帮 agent 找到相关决策，再从当时的原始文档中确认版本和限制。

wiki 也不是总有用。原文在 Harvey 的 LAB 法律基准上试过：24 道跨多份文件、要判断或计算的并购问题上，wiki 是 87%，单用搜索是 73%。另一个任务的 57 条评分标准大多只依赖一份交易概要，wiki 就没有明显优势。还有一个任务，10 份文档 115 KB，建出来的 wiki 有 68 页、203 KB，是原始语料的 1.77 倍。 <sup>[1]</sup>

所以如果问题本来只需要检索一份文件中的明确字段，维护复杂 wiki 的收益就要重新评估。多加一层表示，会增加一个需要保持正确的地方，也会增加上下文消耗。

原文提到 wiki 加搜索每题约节省 2 万 token， **但没有因此证明整个系统的总成本下降。** 离线构建和维护也会消耗计算。 <sup>[1]</sup>

可以用一个简单的成本关系估算是否值得做。下面的公式是个人的分析，并非官方实验结论：

N·(C <sub>search</sub> -C <sub>wiki+search</sub>)>C <sub>build</sub> +C <sub>maintenance</sub>

```
N
```
是这段时间内能复用记忆的查询次数，
```
C
```
全部采用同一成本单位。左侧表示在线查询节省，右侧是构建和维护开销。不同模型的 input、output、cache 价格不同，只看 token 总数还不够。

官方 knowledge-wiki quickstart 给了一组可以代入的数：用 8 份 SEC 文件建 wiki，录制的那次花了约 16 美元、23 分钟。有了 wiki，小模型的回答和大模型直接搜原始文档只差 1 分左右，单题价格约为后者的 1/15。按基准平均约 19 美元的构建成本算，大约 240 个问题后回本。 <sup>[7]</sup>

![图 6：knowledge-wiki quickstart 的流程，先建 wiki，再一题一个只读 session 查询（from claude-quickstarts）](https://mmbiz.qpic.cn/mmbiz_png/ezjZug0fpibyJwPEa2iaFXAv8vkwjCtZpQ8uUuecCNQVatCOdY8pgicqWZiaTqUCBnBfHW5SlG7uByEFARmdtRGF3j2ecvZcxapFicozUlz01Nw4/640?from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=5)

图 6：knowledge-wiki quickstart 的流程，先建 wiki，再一题一个只读 session 查询（from claude-quickstarts）

图 6：knowledge-wiki quickstart 的流程，先建 wiki，再一题一个只读 session 查询（from claude-quickstarts）

同一批材料被反复问，且问题经常涉及多份文件，比较容易摊薄离线成本。材料只用一次，或者很快失效，直接搜索可能更合适。具体还要在自己的查询分布上比一下。

## 5 多 agent 写记忆的并发问题

Anthropic 的一个合同任务中，最初多个 agent 写同一张条款表，互相覆盖，wiki 只保留了 57 条关键事实中的 41 条（72%）。随后让 Claude 回看失败、提出指令修改再重建。新做法改成每份合同单独一页、一个 agent 负责写入，并逐字保留关键条款， **57 条事实全部保留，简报评分标准的满足率从 72% 提到 100%** 。 <sup>[1]</sup>

![图 7：合同任务，共享表格和每份合同一页两种写法下保留下来的事实（from Anthropic）](https://mmbiz.qpic.cn/mmbiz_png/ezjZug0fpibxnhib7VyakGUAxbG4v2eiaayU5Yw1yjquaeGDJuDUp4An6nEyvYu81cgCs1EyAP5uR8XBRO1ow9M0tsnz47miaqlLehiaSS3o9ESo/640?from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=6)

图 7：合同任务，共享表格和每份合同一页两种写法下保留下来的事实（from Anthropic）

图 7：合同任务，共享表格和每份合同一页两种写法下保留下来的事实（from Anthropic）

这里同时改了写入分工和内容保留方式， **不能把提升全部归给消除并发覆盖** 。57/57 也只对应该任务的评分项。

这个例子放到实际系统里也成立。多个 agent 都在改共享文件时，一次写入成功返回之后，稍后仍可能被另一个写入覆盖。模型把文件读回来确认一次，也只能观察那个时刻的状态。

公开的 knowledge-wiki quickstart 也保留了共享页面写入的设计。README 披露，在该示例最繁忙的实体页上，约 5% 的已写入行会丢失内容，作者接受这个代价，换来不同文档的数字汇到同一页、方便标出分歧。这个数字来自单个样例，并非平台固定的丢失率，不过也说明并发合并仍需要处理。 <sup>[7]</sup>

比较稳妥的做法是先让 analyzer 写自己的候选页，再由一个合并任务更新共享索引。如果业务确实需要多人同时修改同一实体，就 **在存储层解决版本冲突，不能只靠 prompt 提醒大家小心** 。

Managed Agents 的 memory store 本身提供了这个能力：

```
update()
```
可以带
```
content_sha256
```
前置条件，如果存储里的内容已经被别人改过，就拒绝写入，需要重新读取再试。
```
create()
```
也不会覆盖已有文件。自托管 sandbox 上的 store 是本地副本，默认最多每 15 秒同步一次，不同 session 之间看到的内容会有延迟。 <sup>[3]</sup>

每次修改还会生成不可变的 memory version，默认保留 30 天，便于追踪和恢复。版本历史提供的是审计依据，业务仍然要判断哪条内容成立、哪些改动应该合并。 <sup>[3]</sup>

## 6 自己接入时，先做一个可验收的版本

个人会从原始日志、少量笔记和短索引开始。先让下一次任务能查到正确的历史结论，再决定是否需要更复杂的 wiki。下面是参考这些公开实现后的一种工程建议，并非 Anthropic 的固定协议。

![图 8：带证据状态的记忆更新流程（工程建议，自绘示意）](https://mmbiz.qpic.cn/mmbiz_png/ezjZug0fpibxKDSj3G9QlrtFdCTyGfhnOXFdQVSsMXdDfMgosxaiaqk1enPibnDcwv1wlia5licxUQoXiap7VU9nokSCcsRSVWfFzPgaqVgRE2yDs/640?from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=7)

图 8：带证据状态的记忆更新流程（工程建议，自绘示意）

图 8：带证据状态的记忆更新流程（工程建议，自绘示意）

==笔记里最有价值的几个字段是== **==结论、来源、验证时间和适用条件==** ==。比如“某个参数必须设置”要能追溯到实际命令和结果，同时说明对应版本。来源中的 agent 自述只能说明它当时怎么判断，工具结果也要结合时间和环境理解。==

后台维护先处理新增材料，遇到相关条目再核实。证据支持的内容可以合入，明确矛盾的内容标注或替换旧结论，仍未验证的猜测保留为候选。 **没有在这一份 transcript 找到支持，不能直接等同于这条记忆是假的** 。

上线前，固定同一批历史数据、同一模型和同一组后续任务做对照。可以先比较下面几组，避免一次把所有组件加上，最后分不清改善来自哪里。

| 对照组 | 想确认的问题 |
| --- | --- |
| 只搜索原始记录 | 原始材料已经能解决多少问题 |
| 搜索 + 会话内笔记 | 即时记录是否有帮助 |
| 搜索 + 离线整理笔记 | 校验和合并是否进一步改善 |
| 搜索 + 笔记 + wiki | 更复杂的组织结构是否值得维护 |

评测除了任务得分，还应记录错误记忆被采用的次数、关键事实遗漏、在线 token 和延迟，以及离线维护成本。新数据按时间切开， **后续评测问题和答案不要提前交给整理阶段** ，否则测到的就混入了提前知道题目的收益。

实现里还有三件事值得先处理：

- 原始日志作为数据读取，保留工具结果和时间。外部网页或工具输出中的指令被写成笔记后仍然只是数据，要避免它自动变成后续 agent 的规则。官方文档也提醒，处理不可信输入的
	```
	read_write
	```
	store 可能被 prompt injection 污染，之后会被当成可信内容读回来。 <sup>[3]</sup>
- 对共享参考记忆显式配置只读。Managed Agents 的挂载默认是
	```
	read_write
	```
	，
	```
	read_only
	```
	会在文件系统层面拒绝写入。读写权限要按用途配置。 <sup>[3]</sup>
- 增量任务要保存成功处理到哪里，并能补跑跨越时间窗口的 session。cookbook 的 nightly 脚本在失败的那晚会保留时间窗口重试，但当时还在运行的 session 会被跳过，之后也不再补。所以调度器跑过一次，历史材料也可能没有全部纳入记忆。 <sup>[2]</sup>

需要上手的可以先看 dreaming cookbook，再看官方 knowledge-wiki quickstart。它们提供了不同起点：前者围绕历史 session 维护记忆，后者围绕文档集合构建可查询的 wiki。这些示例不是 Stainless 内部语料实验的完整复现包，文中也还没有实际运行过它们。 <sup>[2]</sup> <sup>[7]</sup>

## 7 最终结论

==全文梳理下来，核心就是这几点：==

- ==记忆分四层：transcript 是底座，往上是笔记、wiki 这类组织结构和每次注入的上下文，dreaming 在后台回看日志、纠正笔记、整理结构，模型权重不动；==
- ==有记忆目录不等于有收益，CL-Bench 上 Opus 5.5 从 0.655 到 0.838，Sonnet 4.6 却几乎没变，关键在模型会不会读、会不会验证；==
- ==官方给了两条路，原生 Dreams 输出独立的新 store，cookbook 用 dynamic workflow 在同一个 store 上持续更新；==
- ==wiki 加搜索在跨文档问题上更强，单文档问题上收益不明显，离线构建的成本要靠反复查询来摊薄；==
- ==多个 agent 写同一份记忆会互相覆盖，要靠单写入路径和存储层的版本检查来解决。==

Dreaming 本身并不神秘，它最有价值的地方是 **把记忆维护做成一个可以单独调度、检查和评测的任务** 。真正的难点在验收和成本，整理这一步反而是最容易的。

想接入的话，建议从原始日志、少量笔记和短索引开始，用固定任务做对照，先确认它能否减少重复失败，以及离线开销能否被后续任务所消化。共享的参考记忆挂只读，并发写入在存储层防覆盖。 **先把简单版本测清楚，再增加 wiki 和更多后台 agent** 。

权重不动，agent 也能靠整理好的经验一次比一次做得好，有点像人睡一觉把白天的事想清楚。往后 agent 之间的差距，可能会越来越多地体现在它怎么管理自己的经验上。

我是老潘，我们下期见~  
关注「oldpan博客」，持续酝酿深度质量文。

## 参考来源

\[1\] Anthropic：The components of agent memory，2026-11-06

https://www.anthropic.com/research/components-of-agent-memory

\[2\] Claude Cookbook：Dreaming with a dynamic workflow

https://platform.claude.com/cookbook/managed-agents-cma-dreaming-with-a-dynamic-workflow

\[3\] Claude Platform：Using agent memory

https://platform.claude.com/docs/en/managed-agents/memory

\[4\] Claude Code：How Claude remembers your project

https://code.claude.com/docs/en/memory

\[5\] Sleep-time Compute: Beyond Inference Scaling at Test-time

https://arxiv.org/abs/2504.13171

\[6\] Claude Platform：Dreams

https://platform.claude.com/docs/en/managed-agents/dreams

\[7\] Anthropic quickstarts：Knowledge Wiki，README 与运行入口

https://github.com/anthropics/claude-quickstarts/blob/main/managed-agents/knowledge-wiki/README.md

复制 LaTeX 公式