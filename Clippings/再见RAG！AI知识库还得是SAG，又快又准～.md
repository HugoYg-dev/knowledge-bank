---
title: "再见RAG！AI知识库还得是SAG，又快又准～"
source: "https://mp.weixin.qq.com/s/lSjeOxFs7NAJ0NIOsqDW8Q"
author:
  - "[[袋鼠帝]]"
published: 2026-06-22
created: 2026-09-15
description: "一个真实需求的AI知识库方案拆解，有需要的朋友非常值得一看。"
tags:
  - "clippings"
---
袋鼠帝 袋鼠帝AI客栈 *2026年6月22日 17:02*

你好，我是袋鼠帝。

上周有客户找我聊了个需求，大意是想做一个本地「小秘书」：

会议纪要、立项材料、批复文件，这些都要能通过Agent对话直接查询，项目金额、开始时间这类确定信息也要能查，而且准确率要高，可用性要强，他自己有本地服务器和大模型，数据量大概不超过1500个文档。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/PF8icWqEe2PRgTTrnPZKtb56ibIvmvBiaiaEGAGqnpvKprGXMNaDbcMicYvbusl4ibZCR8NnErOEzY4L1vGrDk9Sw9wJcZj4VlNNx4S3znWDnccso/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

我当时第一反应是用FastGPT来上传文档，打造知识库。

24年的时候我接过不少类似需求，基本都是用fastgpt快速搭建的。

然后我拉了一位好朋友来一起看，仔细分析过后，感觉这个事儿没那么简单。

![图片](https://mmbiz.qpic.cn/mmbiz_png/PF8icWqEe2PSIzl7r1qx7G8frdTzPM98mmb0KZLHyKHGa6fJibubicZibZBBgtNq5FtIsNMCibczDUKt1xiaXBHgRZSic0oTQCykpibOYoM15b6rYfU/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=2)

知识库最难的从来不是「搭建」，是调优。。

之前跟这位好朋友交流过知识库调优这块，她说她们公司本来想外采一个知识库系统，但是大厂开价有点高。

然后就自己组了个六人团队做知识库，搞了整整半年，才把回复准确率调到一个相对满意的状态。。

![图片](https://mmbiz.qpic.cn/mmbiz_png/PF8icWqEe2PTTjrul0CnNTRj38hc8Ja4A11rka1FibAZt7NXZuSFLND1fmg9vKsfYX7rZpicrt3DPic0apDNmDOdc5cZLFsPicQQ5uSk6kia72oJk/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=3)

我觉得不是他们能力的问题，而是传统 RAG 的调优本来就是这样，是黑盒的，比较模糊的，你不知道改了哪里会造成「按下葫芦浮起瓢」。

有可能你调低个过滤的score，获取的信息范围是增大了，但是可能又回出现很多噪音。

更要命的是，这个客户的需求里肯定还有一种场景，普通RAG方案搭建的知识库遇上基本都会GG。

就是 多跳推理。

举个例子。假设他的知识库里有三份独立文档：

> **文档 1："2023年，A公司全资收购了B公司。"**  
> 文档 2："张三被任命为A公司的CTO。"
> 
> 文档 3："2024年，张三离职，加入了盘古大模型项目。"

用户问："收购了B公司的企业，其CTO后来加入了哪个项目？"

传统向量检索或混合检索（全文+向量+重排）拿着问题里的关键词去库里搜，能找到文档1和文档2，但绝对找不到文档3。

原因很简单：文档3里根本没出现「收购」「B公司」「CTO」这几个词，字面和语义都毫不沾边，线索在这里断了。

最后只能给出：「抱歉，资料中未找到相关内容。。。。」

会议纪要这种场景，这类多跳检索需求一定是非常多的。

这中途我也想过用 GraphRAG，但我一直都觉得 GraphRAG 太重了：

![图片](https://mmbiz.qpic.cn/mmbiz_png/PF8icWqEe2PTKfqib8hribu9v4qhKw6sDJHibAPrJTobTCnVqwwnGvibUmlrgMIt5yNKaxomgUQqaSA78wgodfIlCdxb3H7Mp4cibDJwfNfic4UGlo/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=4)

它需要在文件入库之前，大量调用 LLM 去提取三元组（谁-做了什么-对谁），然后把整个语料库的知识图谱在离线状态下全部构建好。

光是索引成本，据我了解一个中等规模的数据集就能烧好几万块钱。对于这个客户的项目，有点杀鸡用牛刀，而且图谱构建好之后，只要有新文件进来，就可能要重新算一遍关系，维护成本贼高。

所以我找了一圈，发现了一个前几天刚开源新东西：SAG。已经在Github斩获1.3K Star了。

https://github.com/Zleap-AI/SAG

![图片](https://mmbiz.qpic.cn/mmbiz_png/PF8icWqEe2PSwpMWWl0bKia0QmYr2Ea4M8VATKR3w1XmBoK1So4dPEJP9LcWOWLq42eYlbj8EticIKBWn3uaqyxxCArB7aicRss0LdeZBMLD0As/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=5)

我打开论文一看标题：

"SQL-Retrieval Augmented Generation with Query-Time Dynamic Hyperedges"--基于查询时动态超边的 SQL 检索增强生成

好家伙，SQL我特别熟悉，看到这个思路我一下子就来精神了🤔

**SAG 到底是什么？**

SAG 是 广州智跃深空人工智能科技有限公司 Zleap 提出的一套开源检索架构。

它的核心思路，简单来说就是把文档转成「事项（event）-实体（entity）」索引存进 SQL 关系型数据库，查询时用 SQL 动态组装关联关系，代替GraphRAG的那种离线预构建的静态知识图谱。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/PF8icWqEe2PRCibu7zCmhIFAqZsVOicJiaB2kQM7ZJOtbNKtu3UmOqyAgIRL0ODtRuTlf2mNibnyoSTJaBquXpY4jRiapKcftSB2U3gfUCXl4fhUQ/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=6)

这句话你可能没搞懂，我换个更简单的解释，就好理解了。

你可以把传统 RAG 想象成一个图书馆管理员：每次你问问题，比如，你想要医学相关的书，他就拿着你的关键词在书架上找相关的医学书籍，找到了递给你。

这个方式在大多数情况下够用，但如果你问的问题需要从三本书里各抽一段看似没有关联的内容才能拼出答案，他就挠头了，因为他是靠「字面意思匹配」找书的，没有能力自动把三本书的线索串起来。

*传统RAG工作流程图  
*

![图片](https://mmbiz.qpic.cn/mmbiz_png/PF8icWqEe2PS9py7UuycuNM0zfHTJXIib6cicAIWfqMfCIdVwET8wHUZIdBKiceiaE0eicR1T26zLNQs1DQJ3DibtPLicjYAax6wJA0MxIlDnnia6wicM/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=7)

GraphRAG 的做法是在你把书放进图书馆之前，先花大量时间把整个图书馆的所有人名、公司名、事件，提前画一张巨大的关系图挂在墙上。

查询的时候顺着关系图谱找，效果确实很好。但问题是画这张图非常耗时耗钱，而且每进来一本新书，就得重新画。

SAG 走了第三条路：它不画全局关系图，而是在你上传文档的时候，用 AI 把每个文档片段提炼成一张「事项卡片」（记录发生了什么事），同时提取出这件事涉及的「实体」（公司名、人名、项目名等），把这些存进一个普通的 SQL 数据库和向量库里。

查询时，用 SQL 的 JOIN 语句动态把有共同实体的事项拎出来，组成局部关系网，实时串联多跳线索。

![图片](https://mmbiz.qpic.cn/mmbiz_png/PF8icWqEe2PTpuhPrb1YjmXJNrNbmfyeZic6Gmvv9Fe4CCdEzgQRhjYUqWr6uaibgtsiccTP7sOvjDGDu0DMr46UCYeus9qem3nb9PiaF2c7yelo/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=8)

比如，用刚才那个例子跑一遍：

知识库里有三份文件：文档1说「A公司全资收购了B公司」，文档2说「张三被任命为A公司的CTO」，文档3说「张三离职，加入了盘古大模型项目」。

用户问：「收购了B公司的企业，其CTO后来加入了哪个项目？」

SAG 拿到问题，两件事同时在跑：

一边用普通 RAG 一样做向量语义搜索，找意思最相关的段落；

另一边从问题里提取实体「B公司」「CTO」，去数据库里用SQL查哪些事项涉及了这两个实体，最后命中文档1和文档2。

到这里，SAG 做到了普通 RAG 很难做到的一步：扫描已命中的文档1和文档2，从里面发现了一个新实体「张三」。

这个名字在用户原始问题里根本没出现过，但它是两份文档之间的连接点。

于是数据库自动触发第二轮查询：「哪些事项涉及了张三」命中文档3。

三份文档全部到位，加上向量搜索的结果，一起交给大模型拼出最终答案。

普通 RAG 做完向量搜索就停了，因为找到了文档1和文档2，但不会从里面挖出「张三」这个新线索继续追，文档3对它来说可能是永远的盲区。

SAG 在向量搜索的基础上多了实体关联这条链，从已经找到的内容里挖出新线索、接着往下查，让多跳推理变成一件确定的事，而不是靠运气。

**和 FastGPT 混合检索有什么区别？**

其实我看完论文之后还有一个疑问，就是SAG和Fastgpt自带的混合检索有啥区别？

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/PF8icWqEe2PQhhNTLz40FDEicSLCfRUpGRGSBQwib2bU8esvcia7icluUZlfkSOrNg6iadOHjEoMfIfaYbvGeqLccDOMzLVSBj0SWWXwaibzjSeQfA/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=9)

FastGPT 里的「全文检索+向量检索+重排序」，其实就是目前最成熟的工业标准 RAG 方案，它本身并没有什么问题，对绝大多数日常知识库问答足够好。

SAG 和它的区别，主要也是在SQL部分，对应具体的能力就是SAG「多跳推理」更强。

日常的单文档问答，FastGPT 完全够用，速度也快。

但涉及需要跨多个文档逻辑串联的问题，FastGPT（本质上是扁平的相似度匹配）就触到了物理上限，而 SAG 靠 SQL 结构兜底。

除此之外，SAG 还有几个让我觉得有意思的地方：

可解释性： 传统 RAG 检索问题排查是黑盒，你可能只知道「相似度不够」，要不是分块没弄好，要不是Score设置的有问题，大部分时候是去调试，但不知道具体是哪个环节出了问题。

SAG 的检索链条是完全可追溯的 SQL 调用记录：大模型提取了什么实体 -> 同义词扩展命中了哪些 -> SQL 走通了哪条路径。

哪里断了，工程师一眼就能定位去修。

这一条对调优来说是革命性的。传统 RAG 调优有点像「炼丹」，你改切块大小、改向量模型、改重排阈值，改完一个，可能又会出现另一个问题，永远不知道瓶颈在哪。

SAG 的调优更像程序员们熟悉的「找 Bug 和修 Bug」，有问题，看日志，找具体的问题点，只能砍掉团队80%像无头苍蝇一样瞎摸索的时间。

入库逻辑的转变：传统 RAG 的调优大量时间花在切块、参数上：按500字切还是1000字一块切？重叠的部分要不要？如果切块切坏了，把「张三负责A项目」和「500万预算」切成两段，线索就断了。

SAG 把这个问题前移了：在文档入库之前，用 AI 把内容提炼成完整的「事项卡片」，一件事就是一张卡，不用关心切块的问题。入库的数据是完整的，后续检索准确率自然就会更高。

SAG不挑模型，论文里有一个很有意思的消融实验：

研究员故意把 SAG 底层的向量模型换成了一个很普通的开源弱模型，结果其他高级 RAG 方案的准确率暴跌了将近10%，SAG 几乎没什么变化（依然稳定在80%左右）。

原因就在于：SAG 找线索的主干力量是确定的 SQL 实体关联，不是模糊的向量距离，换个弱模型不太能影响 SQL 找东西。

这对有行业黑话的企业场景更加重要：因为通常向量模型不认识你们公司内部的一些"黑话"，但只要 SQL 里存了这个实体，就能查出来，不需要专门微调向量模型～

**SAG到底行不行？**

Zleap在三个多跳推理标准数据集（HotpotQA、2WikiMultiHop、MuSiQue）上跑了评测。

其中在 MuSiQue 上的 Recall@5 达到 80.04%，比 HippoRAG 2 的 65.13% 高出约 15 个百分点。

MuSiQue 是这三个测试集里最难的，要求最多4跳的组合推理，且不允许跳过中间步骤，是公认的RAG里面的「地狱难度」测试集。

![图片](https://mmbiz.qpic.cn/mmbiz_png/PF8icWqEe2PQolSI9syuAqlNUbCJoKltrozyPSMobcOzbmqiau3JVctSugmROH5mZrjeQqK0k9XFIAHhmdbKqG6eOQpWCR5zLdoqIhvdCE5bI/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=10)

而HippoRAG 2，是目前比较推崇的方案之一，灵感来自神经科学里的「海马体索引理论」，原理是把知识图谱和 Personalized PageRank 算法结合起来做多跳推理。简单来说就是一种模仿 **人脑海马体** 的AI检索技术。

跟 SAG 相比，HippoRAG 2 在构建阶段也需要离线预先建好知识图谱，依赖图结构的静态全局关系；而 SAG 把图的构建时机后推到查询时，会用 SQL 动态激活，避开了全局图重建和维护的开销。

*PS：SQL动态激活就是 SAG 把图的构建时机后推到了查询时。也就是你提问的那一刻，SAG 才通过 SQL 把事项之间的关联关系查询出来，不是提前把全图建好等着你来用。  
*

另外，目前SAG 已经在约5亿条数据规模的生产环境里完成了部署，在线检索延迟保持在秒级以内。而一般的RAG在数据量上了百万就 OOM（内存溢出）或者速度拉跨。这次，SAG直接刷新了SOTA。

目前SAG有在线 demo 可以直接体验：

https://wiki.zleap.com/search

*拿的是 Wikipedia 的数据  
*

![图片](https://mmbiz.qpic.cn/mmbiz_png/PF8icWqEe2PRdOOUB1XHSCezh1tu6n4alymnRcwwKSdKIDRDMiazR5fOVobPtELDddcia3pqQoIBmiad199I8ILibHy4G1nC6keRZJRevicyncicmY/640?wx_fmt=png&from=appmsg#imgIndex=11)

也可以本地docker-compose部署（我用codex帮我一键完成了部署）：

![图片](https://mmbiz.qpic.cn/mmbiz_png/PF8icWqEe2PSIHwmD1AvRoYuY3J4jf7ufMcwI9BEOHSwqCfoAAQiaq6tUy0PdoW2lM5QJAIWzy3ldlkQZBrSbUTrIbkIK6Ibn5ej3mU9xVnOo/640?wx_fmt=png&from=appmsg#imgIndex=12)

我让codex帮我造了一些数据丢进去，测试了一些问题，命中率比我预期的高～

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/PF8icWqEe2PSR3xWewJW3zpkfI6KyfMZtFOXG4VSI8oCXwlKlN6weWDM156rE8CRLGojyxn3YlQzNKhl9TzvpdySWLhUu6s1IeDntnK6O5c4/640?wx_fmt=png&from=appmsg#imgIndex=13)

**回到这个客户的需求：落地方案怎么搞？**

我觉得 SAG 目前主要还是一套检索架构。

如果你想纯按 SAG 的思路从零做一个完整的知识库产品，还是需要自己搭前端、做权限管理、写文档解析引擎、搞部署运维，工程量很大，对一个预算有限的项目来说，烂尾风险很高。

而 FastGPT，对话界面完善、权限管理成熟、接微信/飞书都很快，能瞬间满足客户对「可用性」的要求。

所以对于这个客户的项目，可以两者结合：

在成熟的系统（如 FastGPT）之上，使用 SAG 作为知识库的实现方案。

既能复用 FastGPT 的工程成熟度，同时用 SAG 的思想解决了「切块破碎」和「结构化检索」的问题。后续的调优也更加的方便快捷。

目前最简单的方式应该是把SAG作为MCP工具，丝滑的接入Fastgpt

![图片](https://mmbiz.qpic.cn/mmbiz_png/PF8icWqEe2PTEM46DtFt0lbPX590Zz5JJ7e0nP8e8909RayDQMeO0vy9HvCITTibA1FwNxtTHUibST7Qg68l8I5L9icfdNppgnZKKicIBsXt6S4A/640?wx_fmt=png&from=appmsg#imgIndex=14)

当然，如果 FastGPT 或其他主流知识库系统哪天把 SAG 的架构思想丝滑地融进官方工作流，那更好，拿来即用就行。

*PS：也可以通过MCP，丝滑接入Codex、Claude code等本地Agent使用～  
*

**「最后」**

RAG 这几年的演化路径从最早的纯向量检索，到混合检索，到 GraphRAG 引入知识图谱，再到现在 SAG 把知识图谱的构建时机从「离线」挪到「查询时」，用 SQL 关系型数据库作为动态组织层。

每一步看起来都是在加复杂度，但感觉 SAG 这一步有点返璞归真的意思。

SQL 关系型数据库大家用了几十年，稳定、可解释、可维护，把它拉进检索架构，工程落地的难度反而降低了不少。

而且对于很多企业来说，开发团队可能会天天写 SQL，贼熟，接起来也比较丝滑。

创新不一定是发明全新的东西，有时候是把已经被验证过的工具，重新组合用在对的地方（站在巨人的肩膀上）。

然后我觉得SAG将成为 Agent 的数据底座：

因为 Agent 很多时候就是在完成多跳推理工作，先查 A，用 A 的结论决定去查 B，每一步输出都是下一步的输入。这正好也是 SAG 解决的问题。

传统 RAG 给 Agent 的是「大概相关的几段内容」，SAG 给的是更确定的结构化的事项和实体，拿到就能直接推理，不用再从相似的文本里自己挖掘，出幻觉的概率也低很多。

并且有了精确且高效的查询，能更好的发挥本地小模型的优势。

这种私有知识库的数据底座设计好了，本地Agent 的能力也会更上一层楼。

我是袋鼠帝，一个致力于帮你把AI变成生产力的博主。我们下期见～

能看到这里的都是凤毛麟角的存在！

如果觉得不错，随手点个赞、在看、转发三连吧~

如果想第一时间收到推送，也可以给我个星标⭐

谢谢你耐心看完我的文章~

袋鼠帝AI客栈

邀请你前往腾讯公益一起捐

滇苗助学

170人捐赠

知识库 · 目录

作者提示: 个人观点，仅供参考

闪记

复制 LaTeX 公式