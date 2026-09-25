---
title: "Agent时代，RAG怎么选？这份指南一次讲清！"
source: "https://mp.weixin.qq.com/s/4XGijn-_H1KH05op--1kBg"
author:
  - "[[Datawhale]]"
published:
created: 2026-09-24
description:
tags:
  - "clippings"
---
卞一岚 Datawhale *2026年9月22日 19:04*

Datawhale干货

******作者：卞一岚，百度ACG实习生、河海大学研究生  
******

## 一、引言：Agent 靠什么补上信息缺口

## 给 Agent 的输入，常常只有几句话：“这是我领导的要求 xxxx，你帮我做好一下”“这是报错信息 xxxx，你帮我修一下”。但很显然，距离真正做好，Agent 需要的上下文远不止这几句话。

至少，它需要知道具体目标：最后要做成什么样子；需要知道验收标准：做到什么程度才算完成，Agent 应该怎么自查；还需要知道代码库之外的必要信息：那些停留在人脑、会议记录、聊天记录、历史决策里的背景。用户一句话只是任务入口，不是完成任务所需的全部上下文。

这也是为什么现在的 Agent 越来越不像“一个大模型加一句 prompt”，而更像一个围绕模型搭起来的上下文系统。以 Claude Code 为例，Anthropic 官方把 Claude Code 的可控入口拆成了 CLAUDE.md、rules、skills、subagents、hooks、output styles、append system prompt 等多种机制\[1\]。

这些机制的共同点不是“把提示词写长”，而是把不同类型的信息放到合适的位置：有些规则常驻，有些知识按需加载，有些流程用 hook 保证执行，有些复杂任务交给隔离的 subagent。

RAG 要解决的，正是这条链路里最常见的一类问题：用户的话太短，模型参数里的知识又不够新、不够私有、不够贴合当前任务，于是系统需要在推理时临时补上下文。

一句话讲，RAG 就是在 LLM / Agent 推理时，把它“此刻需要但自己不知道”的信息找出来，整理成上下文，再交给模型完成回答或行动。

这里有两个关键词：一个是“此刻需要”，一个是“整理成上下文”。RAG 不是把所有资料都塞给模型，也不是一搜到相似 chunk 就万事大吉。用户问“上线后白屏怎么办”，系统真正需要的可能不是“白屏”这个词附近的几段文档，而是线上/本地环境差异、构建配置、资源加载、容器渲染、监控日志这些排查链路。

淘宝答疑系统用 CoT 做意图拆解，再并行生成多组查询，本质上就是先规划信息需求，再去填充上下文。

因此，RAG 的核心不是 retrieval，而是 context construction。检索只是手段，目标是让模型看到足够相关、足够完整、足够有结构的信息。

VimRAG / MMG 这类多轮检索记忆方案进一步说明了这一点：多轮对话里，检索系统如果没有“自己查过什么”的记忆，就会反复召回同一批内容；用图结构记录检索路径，或者工程上用 session 级 consumed\_ids 去重，都是在让上下文构建变得更有状态\[2\]。

所以这篇文章不把 RAG 当成一个固定架构来讲。更准确地说，RAG 是一组给 LLM / Agent 补信息缺口的技术：有时候是经典向量检索，有时候是 GraphRAG / LightRAG 这样的知识组织方式，有时候是 Agentic RAG 让 Agent 自己决定要不要再查一次，有时候甚至不该用 RAG，而该用 grep、LLM Wiki、Memory、上下文压缩或结构化查询。

![图片](https://mmbiz.qpic.cn/mmbiz_png/zW6S9vt0cSicQRJzt1CxyWIyVMbBg8Ajs5LMvM5nKtb0JDZdOqoa1G7DoZia3F7QoB9juBKb3PicqGgEe6icEK4qxgDZhphWS77icWEgx1UnoGPc/640?wx_fmt=png&from=appmsg#imgIndex=0)

图1：Agent 为什么需要 Context System

## 二、五类 RAG 场景选型

### 1\. 经典 RAG：Naive -> Advanced -> Modular

经典 RAG 最适合从“我有一堆文档，想让大模型别瞎编”这个朴素需求开始。比如文档问答、客服助手、内部知识库、产品答疑，第一版通常都长得差不多：把文档切成 chunk，做 embedding，塞进向量库；用户提问时召回几个相似片段，再拼进 prompt 让 LLM 回答。这就是 Naive RAG。

它的好处是便宜、快、工程闭环短，能把“模型不知道内部知识”这个问题先救回来；RAG 最早的核心思想也是把参数化记忆和外部非参数化记忆结合起来，让模型在生成时访问外部知识\[3\]。

如果把 Naive RAG 拆开看，它其实就是两条链路。离线索引阶段是 Load -> Split -> Embed -> Store：先把 PDF、Word、Markdown、HTML、JSON、Excel、语雀、钉钉文档等来源解析成干净文本，顺手保留文件名、页码、章节、标题、作者、创建时间等 metadata；再把长文档切成适合检索的 chunk；然后用 embedding 模型转成向量；最后把向量和 metadata 存进向量库。

在线查询阶段是 Query -> Retrieve -> Rerank -> Generate：先处理用户问题，再召回 Top-K chunk，必要时精排，最后把问题和证据一起交给 LLM 生成答案。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/zW6S9vt0cSibdNibIr1hGuOPV3AbwjN1bsKhyF3icU0byNXXVC7nXa7cpnWM9BfvPg68xSnicFHGe3GxYAWLbo9gjibGAmzgjOlWWCFGoQdHcs68/640?wx_fmt=png&from=appmsg#imgIndex=1)

图2：经典 RAG 全链路：从文档到答案

离线索引阶段，这套流程听起来简单，但每一步都有坑。文档加载阶段，PDF 文字层、扫描件 OCR、HTML 正文抽取、表格结构保留，都会影响后面能不能搜到正确内容。

metadata 也不是装饰品，它决定了后面能不能做权限过滤、章节过滤、时间过滤、引用溯源。很多“RAG 答错”的根因不是模型差，而是文档入口就把正文、页码、标题层级或者表格语义弄丢了。

切分是 Naive RAG 里最容易被低估的环节。固定长度切分最便宜，适合快速 baseline；递归切分按标题、段落、句子逐层切，通常是通用文档的稳健起点；语义切分根据相邻句子的 embedding 相似度找边界，听起来更聪明，但研究显示它的计算成本不一定能换来同比例收益\[19\]。

实践里常见的起步方案反而很朴素：递归切分 + 10%-20% overlap + 保留章节 metadata，然后用 Context Precision / Recall 看 bad case。

进阶切分主要解决一个问题：chunk 不能太小，否则答案被切碎；chunk 不能太大，否则噪声太多。Late Chunking 的思路是“先编码整篇文档，再切 chunk”，利用长上下文 embedding 模型让每个 chunk 的向量带上全局上下文\[20\]。

Intent-Driven Dynamic Chunking 则更进一步：切分边界不只看文档结构，而是预测用户可能的信息需求，让 chunk 更贴近未来查询\[21\]。Small-to-Big 是工程上很实用的折中：检索时用小 chunk 精确命中，生成时扩展到相邻段落、章节或父节点，避免答案缺上下文。

Embedding 和索引阶段要做的选择也不少。稠密检索适合语义改写、同义表达和开放式问题；稀疏检索，比如 BM25，适合专有名词、编号、错误码、型号、法规条款这类精确匹配；混合检索把两者结合起来，通常比任何单一路线更稳。融合可以用 Reciprocal Rank Fusion，也可以在验证集上调加权系数。这里不要迷信“最强 embedding 模型”，要看语种、领域、文档长度、成本、延迟，以及它是否真的提高了端到端答案质量。

在线查询阶段，第一件事是别把用户原话直接扔进向量库。用户问题往往短、口语化、上下文缺失，还可能有错别字、指代词和非专业表达。Query rewriting 可以做指代消解、纠错、术语对齐和结构简化；Multi-Query 可以从多个角度生成 3-5 个变体问题，提升召回率；

HyDE 则先让 LLM 写一个“假设性答案”，再用这个答案向量去搜真实文档，本质是把“问题-文档匹配”转换成“文档-文档匹配”\[22\]。反向 HyDE / Doc2Query 则把工作前置到离线阶段：给每个 chunk 生成它可能回答的问题，用问题倒排到 chunk，降低在线延迟。

查询增强也不是越多越好。多查询会扩大覆盖面，也会放大 rerank 成本；HyDE 对开放式问题有帮助，但如果 LLM 写出的假设答案偏了，检索方向也会偏。EAR 提醒我们：查询扩展本身也需要被重排，不是贪婪生成出来的第一个扩展就最好\[23\]。比较稳的做法是按问题类型路由：事实型问题先走 BM25 + Dense，模糊开放问题再走 HyDE / Multi-Query，强业务约束问题先做 metadata filter。

Rerank 是经典 RAG 里性价比很高的一步。向量检索通常是 Bi-Encoder：query 和 document 分别编码，速度快，但交互少，只能说明“看起来相关”。Reranker 通常是 Cross-Encoder：把 query 和候选文档拼在一起，让模型逐 token 判断匹配程度。

典型流程是先召回 Top-50 或 Top-100，再 rerank 到 Top-3 或 Top-5 交给 LLM。它能显著缓解“搜回来的资料看着像，但就是答非所问”的问题，也能统一 BM25、Dense、多路召回的排序标准。代价是延迟和算力，所以 Top-K 不要无限放大。

最后是生成。RAG 的生成阶段更多是在“基于证据组织答案”，不是让模型自由发挥。prompt 里要清楚地区分用户问题、检索材料、回答规则和引用格式；事实型问题降低 temperature；

资料不足时要求拒答；知识冲突时要求指出冲突来源；关键结论要带引用。若提示词优化到极限仍然不稳，才考虑 SFT，用“问题-参考资料-标准答案”训练模型学会根据材料回答，以及在材料不足时拒绝回答。

所以，Advanced RAG 本质上不是完全换一套东西，而是在 Naive RAG 的每个环节补强：切分更聪明，检索更混合，query 更贴近知识库，rerank 更精确，生成更受约束。

淘宝答疑里用 CoT 做意图识别，再按排查步骤生成多组查询并行召回，就是一个很实用的版本：用户问“小程序上线后白屏”，系统不是只搜“白屏原因”，而是拆成环境差异、资源加载、渲染链路、监控日志几条线同时找证据。

Advanced RAG 适合知识库规模已经起来、用户问法很飘、领域术语很多、召回质量不稳定的场景。比如企业内部文档、工单系统、研发答疑、售后知识库，通常都要混合检索和重排。

这里最值得落地的不是“上最贵的 embedding”，而是先做最小评测集：十几条 golden queries 覆盖精确词、多跳、长尾、不可回答问题；每次改 chunk、embedding、rerank、rewrite，都看 Recall@k、Context Precision、Faithfulness、Relevance 有没有变好。

RAG survey 也把 Naive、Advanced、Modular 看成一条演进线：问题不是“要不要 RAG”，而是 retrieval、generation、augmentation 三个环节分别怎么增强\[4\]。

不过 Advanced RAG 也有边界。它仍然主要是在“更好地找片段”，不是在“真正理解整个知识系统”。如果问题需要全局统计、复杂实体关系、跨文档结构推理，单纯 query rewriting + rerank 可能只是把更多碎片塞给模型，最后让模型在一堆看似相关的文本里自由发挥。

另一个常见误区是把所有优化都堆进一条 pipeline：每次查询都 rewrite、multi-query、hybrid、rerank、compress、judge，最后准确率可能没涨多少，延迟和 token 成本先爆了。

所以再往后就会走到 Modular RAG。Modular RAG 的关键不是某个单点算法，而是把 RAG 拆成可替换、可路由、可组合的模块：loader、splitter、embedder、retriever、reranker、query rewriter、fusion、compressor、generator、evaluator。

它不再默认所有问题都走同一条“retrieve-then-generate”直线，而是允许 conditional、branching、looping：简单事实题走 dense retrieval；包含精确术语的走 BM25；多跳问题走 hybrid RRF；召回不足时触发 query rewrite；证据冲突时再检索一次。Modular RAG 论文把这种变化描述为从线性流程走向带路由、调度和融合机制的可重构框架\[5\]。

代表实践可以看三类。AutoRAG 试图自动搜索不同 chunk 策略、embedding、retriever、reranker 的组合，帮团队找到更适合特定数据集的 pipeline\[24\]。QuIM-RAG 把“Query-Document 匹配”改成“Query-Query 匹配”，通过问题倒排索引提升 QA 召回精度\[25\]。

OpenViking 则把上下文数据库做成文件系统范式，让记忆、资源、技能、检索链路更可解释、更可调试\[26\]。Experience-RAG Skill 也是同一类思路：把“选择检索策略”从业务代码里抽出来，让系统根据任务场景在 BM25、Rewrite-BM25、Dense、Hybrid RRF 等检索器里选择策略。

选型上可以很直接：刚起步、文档少、问题简单，用 Naive RAG，先跑通“有据可查”；召回不稳、用户问法复杂、术语多，上 Advanced RAG，把 query、chunk、hybrid、rerank、评测补齐；

如果业务里已经出现多知识库、多检索器、多任务类型、多轮调用，就该考虑 Modular RAG，把策略路由和证据打包做成独立层。不要一上来就建宇宙飞船，RAG 的第一原则还是：先证明文档能被找对，再讨论模型能不能答好。

![图片](https://mmbiz.qpic.cn/mmbiz_png/zW6S9vt0cSibjaO9FntIPRLnrqAZBr6VybXicpdLXibibfqeCU9p5yvu40NyMnwEZp32kCiajTYsVCUhHapTzBMHLTe9cp8MVY9I0U7XiancYxNps/640?wx_fmt=png&from=appmsg#imgIndex=2)

图3：从 Naive RAG 到 Advanced RAG

### 2.2 GraphRAG / LightRAG：当知识不再是一堆孤立 chunk

经典 RAG 最怕一种问题：答案不在某一个 chunk 里，而散落在一堆文档的关系里。比如“这个系统的核心设计模式是什么？”“A 组件和 B 组件为什么耦合？”“上线白屏可能涉及哪些链路？”

向量检索能把相似片段捞出来，但它不知道这些片段之间谁依赖谁、谁解释谁、谁只是同名路人。最后模型拿到一盘散沙，只能硬拼，拼得好叫推理，拼不好就是一本正经地猜。

GraphRAG 的思路是：别只把知识库看成 chunk 仓库，而是先抽实体、关系，构建一张知识图谱，再在图上做检索和摘要。微软 GraphRAG 的代表做法是先从语料里抽取实体图谱，再对相互关联的实体做社区发现，并为社区生成摘要；查询时既可以围绕某个实体做 Local Search，也可以用社区摘要回答“整个语料在讲什么”这类全局问题\[6\]。它真正解决的不是“召回更多文本”，而是“让知识之间的结构先显形”。

但 GraphRAG 不是免费午餐。它的构建成本高，实体/关系抽取要大量 LLM 调用；社区发现和社区摘要会继续吃 token；更麻烦的是增量更新不友好。对于合同库、代码库、业务文档这种经常变的资料，如果每次改一点都要全量重建，那工程团队很快会从“知识图谱真高级”变成“今晚谁来守重建任务”。

所以 GraphRAG 更适合离线分析、全局综述、研究型知识库、低频更新但要求综合理解的场景，不适合高频更新、强实时、成本敏感的在线问答系统。

LightRAG 的实用点就在这里：它保留“实体-关系”这条主线，但尽量砍掉 GraphRAG 里最贵的部分。LightRAG 用图结构和向量表示共同做索引，支持低层事实和高层关系的双层检索，并强调增量更新能力：新数据先形成局部图，再合并进已有图，而不是动不动重建全局索引\[7\]。从工程视角看，它不是要把 GraphRAG 做得更玄，而是把“知识有关联”这件事做得更便宜、更快、更能上线。

选型可以粗暴一点：如果你要问的是“这 500 篇文档体现了哪些主题”“这个领域的关键矛盾是什么”“跨文档有哪些隐含关系”，GraphRAG 值得考虑；如果你要做企业答疑、技术支持、产品文档助手，用户 80% 的问题都是具体事实或局部排障，LightRAG 通常更务实。

淘宝 AI 答疑的笔记里就有一个很典型的判断：GraphRAG 在复杂问答和全局理解上更强，但在线答疑更在意秒级响应、频繁更新和可控成本，于是 LightRAG 成了更接近生产的折中方案。

还有一个容易混淆的方向是 Graphify。Graphify 更像给 Agent 准备的“项目导航图”：它可以把代码、SQL、文档、论文、图片等资料映射成可查询知识图谱，并输出 graph.html、GRAPH\_REPORT.md、graph.json 这类人和 Agent 都能消费的产物\[8\]。

它不一定是直接回答用户问题的 RAG 后端，更像是让 Agent 不必每次从原始文件开始瞎逛。对代码库、系统设计文档、复杂项目交接来说，这种“先有结构化地图，再决定读哪里”的体验，比单纯 embedding 检索更接近真实工程师的工作方式。

一句话总结：GraphRAG / LightRAG 适合知识之间存在强关系的问题。它们不是为了替代所有向量检索，而是当 chunk 已经装不下“关系”时，把知识从一堆碎片重新组织成网络。别一上来就建图，先看问题是不是需要跨文档关联、全局摘要、实体关系推理；如果只是查一个接口参数、找一条制度原文，Naive/Advanced RAG 加重排可能更便宜、更稳。

![图片](https://mmbiz.qpic.cn/mmbiz_png/zW6S9vt0cS8ZicyxMnkxsiaaMicA3kMsDerAJOCurUc9UgTD0DTza5c2RB6CGrWibrdCDQicmOosI51HqgibZWpgCVtUCoY67GMcSmPIylIbdAFFc/640?wx_fmt=png&from=appmsg#imgIndex=3)

图4：从文本检索到知识关系网络

### 2.3 Agentic RAG：让 Agent 决定要不要再查一次

传统 RAG 像一个“只准搜一次的实习生”：拿到问题，查一把，拼上下文，开始回答。问题是，很多真实业务问题根本不是一跳能解决的。比如你问“项目 X 用的服务器规格是什么”，第一次检索可能只找到项目文档里的服务器 ID，真正的规格藏在另一套资产库里。

普通 RAG 到这里就容易尴尬：要么回答“不知道”，要么开始脑补。Agentic RAG 的核心价值，就是让 Agent 在发现信息不够时，自己决定：拆问题、换 query、换数据源、再查一次，直到上下文足够或明确不可答。

Google 的 Agentic RAG 方案可以理解成把检索拆进 Agent workflow：Orchestrator 判断任务是不是一跳能做，Planner 规划信息路径，Query Rewriter 改写多个可检索问题，Search Fanout Agent 分发到不同语料或系统，最后再综合回答。

它真正有意思的地方不只是“多 Agent”，而是引入了 sufficient context agent：先看召回片段、草稿答案和原始问题，判断“现在的信息够不够回答”。如果缺了某个关键信息，就别急着生成答案，而是带着明确缺口回去搜更具体的线索\[9\]。

这类方案特别适合多跳、跨源、信息分散的场景。企业内部最常见：合同在法务库，付款在财务库，项目状态在 Jira，客户沟通在 CRM。用户一句“这个客户为什么还没续约”，背后可能需要查历史工单、报价、合同条款、最近会议纪要。

Agentic RAG 的选型逻辑很简单：如果答案路径需要“查到 A 后才能知道去哪里查 B”，就该考虑它；如果只是固定知识库 FAQ，一次混合检索加 rerank 就够了，别把小问题装修成指挥中心。

再检索会带来一个副作用：重复查。多轮对话里，用户经常追问、改问、绕着同一个主题问，如果检索系统没有记忆，就会一遍遍召回同一批 chunk。

工程上有两个层级的解法：轻量做法是按 session 维护 consumed\_ids，每轮检索后记录已经用过的 doc/chunk，下轮过滤；同时在单次检索内按 doc 去重，避免同一篇文档的三个相似 chunk 挤满 Top-K。

更重的做法是 VimRAG 这类多模态记忆图，把推理过程建成 DAG，记录每一步 action、query、证据节点和路径，让模型知道哪些分支已经走过，哪些是新线索\[2\]。

但 VimRAG 这类方案不是拿来就能用的插件。它的 Multimodal Memory Graph、图调制视觉记忆编码、Graph-Guided Policy Optimization 都是围绕训练后的多模态 agentic RAG 体系设计的，适合多图片、多视频、长链路推理。普通团队更现实的起步方式，是先把 retrieval 做成 tool，而不是普通 function：function 适合“输入确定、输出可预期”的逻辑，retrieval 的结果不确定，更适合交给 Agent loop 做“决策 -> 检索 -> 反思 -> 再检索”。这也是 Agentic RAG 的工程最小闭环。

还有一个坑：Agent 查得更多，不代表引用更可信。Deep research 类 RAG 系统最容易出现“引用标签看起来很正规，点进去完全不支持原句”的情况。引用存在和引用正确是两回事。

靠谱做法是在生成后加 Citation Resolver：先做 citation ID 是否存在的规则校验，再做 chunk hash 校验，确认引用内容没有因索引重建或文档更新而漂移，最后对高风险 claim 做 NLI 或 LLM-as-Judge 的语义蕴含校验。普通场景可以抽样做第三层，高风险场景就别省这点钱。

Agentic RAG 也有边界。它擅长找证据，不擅长验证全局量词。比如“所有门店都没有差评吗”“超过 50% 的评论是否提到了服务慢”“哪个 group 排名第一”，这些不是多搜几次就能稳的，而是语义聚合与全局验证问题。

Evergreen 的思路是把自然语言 claim 编译成可执行的 semantic verification query，再用 query plan 和执行优化来降低成本，并返回支撑 verdict 的 citations\[10\]。

所以选型时要记住：Agentic RAG 解决“路径没走完”，不解决“全局统计不可靠”。前者让 Agent 再查一次，后者需要查询计划、采样、聚合和验证。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/zW6S9vt0cS9ty0gMrPiayCYpojKtFQicsrib4SDcPGjcbSztuGBG7MkW9vZwxAEvda3E35Zbj40Voa8EvoGAUS5GBPfcE82HX4SogzyCFOVgMY/640?wx_fmt=png&from=appmsg#imgIndex=4)

图5：Agentic RAG：让 AI 主动寻找缺失信息

### 2.4 知识预编译 / LLM Wiki：稳定知识不要每次从头检索

经典 RAG 像“开卷考试”：问题来了，先去翻书，翻到几个相似片段，再临场组织答案。这个模式适合事实查询，但遇到稳定、长期、反复使用的知识，就会显得有点浪费。

比如一个团队的项目文档、合同资料、研究论文、个人知识库，每次问一个跨文档问题，都让模型重新检索、重新拼接、重新综合，等于每次都把同一锅汤从生水开始煮。真正缺的不是再多一个向量库，而是把已经读过的材料沉淀成可复用的中间层。

LLM Wiki 的思路就是“知识预编译”：原始资料进来以后，不只是切 chunk 入库，而是让 LLM 把它整理成结构化、互相链接、可持续维护的 Markdown Wiki。

Karpathy 的 LLM Wiki 设计里有三层：Raw sources 是只读原始材料，Wiki 是 LLM 维护的摘要页、实体页、主题页、综合页，Schema 则规定目录结构、引用规则、更新流程和校验方式\[11\]。这和编译型语言有点像：RAG 是运行时解释，LLM Wiki 是先把常用知识编译成更适合模型读取的形态。

它适合“知识稳定、问题会反复来、跨文档综合很多”的场景。个人知识库、团队 onboarding、研究选题、产品资料库、竞品分析、项目复盘，都很适合。你不是只想回答“某个条款在哪里”，而是想知道“这些资料共同说明了什么”“不同版本哪里矛盾”“新人应该先读哪些页面”。

这时预编译比检索更合适，因为高价值工作不是找一个 chunk，而是维护一张越来越厚的知识地图。新的 LLM-Wiki 研究也把它描述成一种 agent-native retrieval：外部知识不是扁平 chunk，而是可搜索、可阅读、可沿链接遍历、可自我修正的结构\[12\]。

它不适合强实时、强审计、强权限隔离但工程底座没准备好的生产问答。Wiki 页毕竟是二级知识，哪怕保留来源，也不是严格的原文 chunk 级引用。企业合同、金融合规、医疗法规这类场景，如果答案必须逐字追溯到原文，LLM Wiki 不能替代引用链、权限系统和评测闭环。

更现实的落地方式，是把它当作 RAG 的预处理层：先用 Wiki 做主题组织、实体归档、矛盾发现和问题路由，最后回答仍然回到原文证据。

代表实践上，Karpathy 的原始 LLM Wiki 更像一个通用模式：人负责堆资料和提问题，LLM 负责摘要、交叉引用、维护 `index.md` 和 `log.md` 。Obsidian-Wiki、GBrain 这类实践进一步加入 delta 追踪、来源可信度、热缓存、可见性标签等工程机制。

这里最重要的判断标准不是“有没有向量库”，而是“上次查询产生的洞察有没有留下来”。如果每次问完都只剩聊天记录，那就是一次性消费；如果好答案能回写成页面、被后续问题复用，知识库才真的开始复利。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/zW6S9vt0cS8gJPiaQNTWiaMxvtUnic6NLCQibMUuibUQQYPL8aCr1RWl7Wliaz9vRUFaKIv6RCX7Oxl8sfQ8ynkia56DUys79iaL9TDuSuVmEWYzRl8/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=5)

图6：Raw Sources -> Wiki -> Schema 三层架构图

### 2.5 上下文压缩：不是所有上下文都值得原样塞进去

上下文压缩解决的是另一个问题：不是所有上下文都值得原样塞进模型。长文档、长对话、RAG 召回结果、Agent 执行轨迹，常见毛病都是“内容很多，信息密度很低”。

模型窗口变长以后，这个问题没有消失，只是变贵了：输入越长，延迟越高，注意力计算越重，模型越容易被无关细节带偏。压缩的目标不是把文本变短这么简单，而是在 token 预算、答案质量、延迟和可复用性之间做交易。

第一类是硬压缩，也就是还在人类可读的符号空间里做删减、抽取、改写。SelectiveContext、LLMLingua、LLMLingua-2 这类方法会判断哪些 token、短语或句子更值得保留。

好处是工程友好：压缩后仍然是自然语言，可以直接喂给闭源 API，跨模型迁移也容易。坏处也明显：删错一个约束，答案就会偏；压得太碎，语法和语义分布会变怪；如果每个 query 都重新压一遍，压缩器本身也会变成新的延迟来源。

第二类是软压缩，也就是把长上下文压成连续向量、特殊 token、KV 状态或前缀表示。Prompt Compression Survey 把相关方法梳理成 hard prompt 和 soft prompt 两大路线，并在 soft prompt 中继续区分 decoder-only、encoder-decoder 等方案\[13\]。

其中 encoder-decoder 路线又可以粗略分成四派：COCOM / LLOCO 这类前后模型都微调，ICAE / 500xCompressor / QGC 这类冻结解码大模型只训练编码器，xRAG 这类借用 embedding encoder，UniICL 这类冻结两端只训练 projector。它们的想象空间很大：像图片模型把百万像素压成少量视觉 token 一样，把长文本压成 LLM 能读懂的高密度前缀。

但工程上要冷静。软压缩最大的麻烦是“绑定模型”。你在某个开源模型 embedding 空间里训练出来的连续向量，换到另一个模型可能就是随机噪声；如果业务依赖 GPT、Claude 这类闭源 API，你甚至不能直接注入自定义 soft prompt。

它适合做模型内核可控、调用量足够大、愿意长期维护压缩器的系统；不适合今天换模型、明天换供应商、后天还要接多个 API 的轻量应用。对大多数工程团队来说，自然语言硬压缩虽然不酷，但更稳、更通用。

LLMLingua-2 是一个很实用的方向：它把提示词压缩建模成 token 二分类任务，用 GPT-4 蒸馏出抽取式压缩数据，再用 XLM-RoBERTa-large 或 mBERT 这类双向编码器学习“保留还是丢弃”\[14\]。

它的关键点不是单次压得多狠，而是 task-agnostic：一份长文档可以先压成高信息密度版本，再被多个 RAG 查询或多轮对话复用。相比 LongLLMLingua 这类更 query-aware 的方案，它牺牲了一部分针对性，换来更好的复用性和系统吞吐。

所以选型时可以问三个问题。第一，压缩对象会不会复用？如果是同一份说明书被反复问，先离线压缩很划算；如果每次都是临时网页，压缩成本可能抵不过收益。

第二，错误代价高不高？合同、财报、代码补丁这类任务，压缩必须保留引用、数字、否定词、条件边界，宁可少压一点。

第三，瓶颈到底是 token 费、延迟，还是模型注意力被噪音污染？如果只是贵，硬压缩和摘要就够；如果是长任务状态管理，可能要像 Agent Memory 那样做逐级折叠：完整材料留在外部，当前上下文只保留任务状态、关键证据和可回溯索引。

## 三、RAG 的评估：没有指标，就没有优化方向

前面讲了很多 RAG 技术：切 chunk、做 embedding、query rewriting、HyDE、Doc2Query、标签过滤、rerank、GraphRAG、Agentic RAG、上下文压缩。但真正落地时，团队最容易掉进一个坑：系统答错了，第一反应是“再调一下 prompt”。

这很危险，因为 RAG 的错误不一定发生在生成端。很多时候模型不是不会答，而是检索阶段根本没有把正确材料召回；也有时候材料召回对了，但模型没有忠实使用；还有时候答案看起来相关，但夹杂了冗余和幻觉。

所以 RAG 评估的第一原则是：把问题拆开看。至少要拆成两层：检索层和生成层。检索层问的是“有没有把正确上下文找回来，以及相关内容有没有排在前面”；生成层问的是“模型有没有基于这些上下文回答，回答是否贴合用户问题”。只有拆开以后，优化才有方向。

Context Recall 低，就先别调 prompt，应该看切分、索引、query 改写、召回策略；Faithfulness 低，说明模型拿到了材料但没有忠实使用，才该看提示词、引用约束、生成参数或模型能力。

Ragas 是一个常用的 RAG 自动化评估框架，它的核心思路是用 LLM-as-a-Judge 近似人工评测，把 RAG 输出拆成可量化指标\[17\]。

它不是要取代人工验收，而是让团队在每次改 chunk、换 embedding、加 rerank、改 prompt 之后，都能跑同一套测试集，看指标到底变好还是变坏。没有这个闭环，RAG 优化就很容易变成“我感觉这版更好了”。

==检索层最重要的两个指标是 Context Precision 和 Context Recall。Context Precision 关注“排在前面的上下文是不是相关”：如果 Top-K 里前几个 chunk 都是噪音，模型就会被带偏，后面即使有正确材料也可能被淹没。==

==Context Recall 关注“参考答案需要的事实有没有被召回”：Ragas 会把参考答案拆成若干事实点，再判断这些事实点是否能从 retrieved contexts 中找到支持。简单说，Precision 解决“捞上来的东西干不干净”，Recall 解决“关键证据有没有漏”。==

生成层常看 Faithfulness 和 Answer Relevancy。Faithfulness 衡量回答中的 claim 是否能被检索上下文支撑，它回答的是“有没有根据材料说话”。这对 RAG 很关键，因为带引用不等于引用正确，模型完全可能拿着 A 文档说 B 结论。

Answer Relevancy 衡量回答是否真正回应用户问题，它不直接判断事实对错，而是看回答有没有跑题、有没有缺失用户真正关心的信息、有没有塞入无关细节。

==还有一个很实用但容易被忽略的指标是 Noise Sensitivity。它看系统在面对相关但冗余、或者完全不相关的上下文时，会不会被噪声带偏。实际 RAG 系统里，召回结果很少是纯净的：一个 chunk 可能同时包含答案、背景和过期信息；Top-K 里也可能混入几个“语义很像但事实不对”的片段。==

噪声敏感度高，说明模型看到材料就想用，不会筛选。这时优化方向可能不是扩大召回，而是收紧 rerank、加 metadata filter、调整 prompt 让模型只使用能直接支撑答案的证据。

![图片](https://mmbiz.qpic.cn/mmbiz_png/zW6S9vt0cS9AwASxkO5hI1iakQ8ribXWibN336Ve624j5OKRUKomcI4RUlwDibQAW3ptf9vVH1Sia3NQicteTKu0Lfp6fwRQiciaLZtHUOX5eibAtSicY/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=6)

图7：RAG Evaluation：从检索质量到生成质量

指标之外，还需要测试集。没有测试集，指标就没有稳定参照。Ragas 的测试集生成思路很值得借鉴：先把文档切分成节点，再通过信息提取器和关系构建器形成知识图谱，然后按场景生成问题。

场景可以包含节点、查询长度、查询风格和用户 persona。这样生成的问题不只是“从一个 chunk 抽一个事实”，还可以覆盖不同表达方式、不同角色、不同复杂度。

测试集至少要覆盖四类问题：单跳具体问题、单跳抽象问题、多跳具体问题、多跳抽象问题。单跳具体问题检验基础事实召回，比如“某条规则是什么”；单跳抽象问题检验总结解释能力，比如“这个规则背后的原则是什么”；

多跳具体问题检验跨文档串联，比如“A 的导师的导师是谁”；多跳抽象问题检验跨来源综合，比如“某个理论从提出到现在如何演变”。如果测试集只包含简单事实题，系统很可能在评测里很好看，一上线遇到复杂问法就崩。

这套评估方法还有一个工程价值：它能把优化动作和指标变化对应起来。Context Recall 低，可以尝试 query rewriting、多查询生成、HyDE、Doc2Query、chunk 策略调整；

Context Precision 低，可以尝试 metadata filter、标签过滤、rerank、缩小 Top-K；Faithfulness 低，可以强化引用约束、降低 temperature、要求 evidence-only、增加 Citation Resolver；

Answer Relevancy 低，可以按问题类型切 prompt 模板；Noise Sensitivity 高，则要减少无关上下文，或者训练模型学会拒绝使用噪声。

所以，RAG 工程化的关键不是“技术栈堆得多”，而是“可测、可调、可信赖”。可测，意味着每次改动都有指标；可调，意味着指标能指向具体模块；可信赖，意味着系统不仅会回答，还能说明答案来自哪里、哪些证据支撑了它、哪些场景下应该拒绝回答。没有评估闭环的 RAG，只是一个看起来会检索的聊天机器人；有评估闭环的 RAG，才是可以持续优化的工程系统。

## 四、什么时候不该用 RAG

最容易被忽略的一点是：RAG 不是“让模型知道更多”的唯一方式，它只是“在推理时找一小段上下文”的方式。只要问题的关键不在“找几段相关证据”，RAG 就可能变成错误抽象：多一套向量库、多一套索引更新、多一层召回误差，最后还要靠 prompt 去修补检索没有拿到的东西。真正的选型问题不是“要不要接 RAG”，而是“当前信息缺口到底适合被检索成 chunk 吗”。

==第一个不该默认用 RAG 的场景，是 MB 级本地代码库。代码库不是一堆语义相似的段落，而是有文件名、符号名、调用关系、提交历史和测试反馈的工程对象。==

Claude Code、Codex 这类 CLI Agent 的思路更接近“让模型驱动 grep/glob/read/git 逐步探索”：先用文件名定位，再用 `rg` 找匹配行，再按需读取局部代码，必要时开子 Agent 隔离搜索上下文。

这样做的优势不是“更原始”，而是它保留了代码世界里最强的信号：精确字符串、路径结构、局部上下文和可执行验证。对于几 MB、几十 MB 的项目，预先 embedding 往往是在给一个本来可以动态搜索的问题制造同步、切块和召回问题。

==当然，代码库变到 GB 级、跨仓库、用户查询经常是“哪里实现了某个概念”而不是“这个函数在哪”，索引就重新有价值。Cursor 这类方案会做 tree-sitter 切块、Merkle Tree 增量同步、embedding 与倒排索引结合。==

==这里的判断标准不是“代码能不能 RAG”，而是：关键词搜索和结构化工具是否已经足够覆盖主要工作流。如果已经够，RAG 是复杂化；如果跨语言、跨仓库、概念召回成为瓶颈，索引才是合理成本。==

第二个边界是聚合查询和全局量词验证。RAG 很擅长回答“有没有证据支持这句话”，但不擅长回答“所有 tuple 是否都满足条件”“满足比例是否超过 50%”“哪个 group 排第一”。

这些问题的核心不是 evidence retrieval，而是 global verification。Evergreen 把语义聚合后的自然语言 claim 拆成可执行的 semantic verification query，再结合执行计划和优化来验证\[10\]。

UQE 也把非结构化数据分析转成 query engine 问题，用 UQL、采样和优化来处理条件聚合、语义检索、抽象聚合\[15\]。这类任务如果硬用 RAG，最危险的是模型可能召回几个看似相关的样本，然后把局部证据误读成全局结论。

第三个场景是个人助手。个人助手需要的不是“每次问答从记忆库里召回几段最相似文本”，而是长期可用、可审计、可更新的个人状态。Memory 和 RAG 的差别在这里非常关键：RAG 的输出通常是上下文片段，Memory 则是可被决策利用的 external state。

一个严肃的 Memory 系统至少要有 Raw Ledger、Derived Views 和 Policy：原始事件可追溯，派生视图面向使用，读写策略可记录、可回放。否则所谓“长期记忆”很容易退化成一个越存越乱的向量库，模型每次从里面捞几段相似旧话，再把偶然相似误认为用户偏好。

这也是为什么个人助手里经常会出现“grep beats RAG”的现象。像 nanobot 这类小型个人助手，核心代码和知识规模都不大，直接用文件系统管理 prompt、技能和上下文，懒加载详细内容，比上来搭一套向量检索更稳。

个人资料天然有目录、日期、项目、联系人、任务这些结构信号，很多时候 Markdown、Wiki、配置文件、事件日志和显式工具调用，比“切块 embedding 后召回”更贴近真实需求。RAG 可以作为读取 Derived Views 的一种方式，但不该冒充整个 Memory 系统。

第四个场景是持续监控。传统 RAG 是 episodic 的：用户问一次，系统检索一次，回答一次。但告警、舆情、股票新闻、客服风险、数据质量监控这类任务不是一次性问答，而是长时间运行的语义管道。

Continuous Prompts / Continuous RAG 的思路是把 LLM 放进流处理系统：Semantic Filter、Map、Aggregate、Top-k、Join、Window、Group-By 持续运行，并用 batching、operator fusion、shadow runs、优化器在吞吐和准确率之间选 plan\[16\]。在这类场景里，把每次新事件都包装成一次 RAG 问答，会丢掉系统状态、窗口语义和增量优化空间。

第五个边界来自复杂业务流程。小红书服务端端到端测试的案例里，团队面对跨域、长链路、组合爆炸的问题，并没有把 RAG 当主解法，而是使用 Plan-and-Execute + ReAct，让 Agent 逆向推导依赖链、渐进式加载知识库、Debug-first 调通接口，再把成功链路沉淀为脚本。

这里 RAG 召回不准的代价太高，因为一次错误召回可能直接让 Agent 调错接口、造错数据、污染后续步骤。复杂流程里，知识库可以存在，但更关键的是计划、工具、验证和经验沉淀，而不是一次检索命中率。

所以，“什么时候不该用 RAG”的简化判断可以这样说：当问题需要精确定位，用 grep/glob/read；当问题需要全局统计，用 query engine / semantic operator；当问题需要长期个性化，用 Memory / LLM Wiki

当问题需要持续运行，用 Continuous RAG；当问题需要可控执行，用 Workflow / Agent loop / Harness。RAG 仍然重要，但它不应该是默认答案。它适合补一段证据，不适合替代搜索工具、数据库、记忆系统、流处理系统和工程闭环。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/zW6S9vt0cSicZwxAGDFRC12ZQdNET5RzbeMQVW8NHwgmkRVyZDRCdTbS0ygla2hmNesng5JIWBnZOtkCLQZRnDib0bxibf0TyruUj6L4bOYwk4/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=7)

图8：什么时候应该用 RAG？信息缺口驱动的技术选型

## 写在最后：按信息缺口选技术

RAG 不是一把万能锤子，而是一组补上下文的工具箱。问题简单、文档规模小、关键词明确时，Naive RAG 或 grep/glob 可能已经够用；问题表达模糊、召回不稳定时，需要 query rewriting、混合检索、重排和评测闭环。

系统上线后答错时，要先用 Context Precision、Context Recall、Faithfulness、Answer Relevancy 等指标定位问题发生在检索层还是生成层；知识跨文档关联很强时，可以考虑 GraphRAG 或 LightRAG。

任务需要多跳搜索、反复确认、跨数据源联动时，Agentic RAG 更合适；知识稳定且会被反复使用时，LLM Wiki / GBrain 这类预编译方案可能比每次从头检索更划算；上下文太长、成本太高时，又要考虑压缩和路由。

选型时不要先问“我要\`不要上 RAG”，而要先问三个更具体的问题：模型缺的是什么信息？这些信息是稳定的、实时的、结构化的，还是分散在文档和工具里？补上这些信息的最低成本方式是什么？

答案可能是向量检索，也可能是知识图谱、Agent 工具调用、文件系统搜索、Memory、Wiki、SQL-like 语义查询，或者只是一个更清楚的业务流程。

最终，RAG 的价值不在于“让模型多看点资料”，而在于把用户的一句话，扩展成模型完成任务真正需要的上下文。工程上真正要优化的，也不是某个单点算法，而是从问题理解、信息获取、上下文组织、回答生成到评测反馈的整条链路。

```swift
参考资料[1] Anthropic: Steering Claude Code: CLAUDE.md files, skills, hooks, rules, subagents and more.https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more[2] VimRAG: Navigating Massive Visual Context in Retrieval-Augmented Generation via Multimodal Memory Graph. https://arxiv.org/pdf/2602.12735[3] Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. https://arxiv.org/abs/2005.11401[4] Retrieval-Augmented Generation for Large Language Models: A Survey. https://arxiv.org/abs/2312.10997[5] Modular RAG: Transforming RAG Systems into LEGO-like Reconfigurable Frameworks. https://arxiv.org/abs/2407.21059[6] From Local to Global: A Graph RAG Approach to Query-Focused Summarization. https://arxiv.org/abs/2404.16130[7] LightRAG: Simple and Fast Retrieval-Augmented Generation. https://arxiv.org/abs/2410.05779[8] Graphify. https://github.com/safishamsi/graphify[9] Google Research: Unlocking dependable responses with Gemini Enterprise Agent Platform's Agentic RAG.https://research.google/blog/unlocking-dependable-responses-with-gemini-enterprise-agent-platforms-agentic-rag/[10] Evergreen: Efficient Claim Verification for Semantic Aggregates. https://arxiv.org/abs/2604.26180[11] Andrej Karpathy: LLM Wiki. https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f[12] Retrieval as Reasoning: Self-Evolving Agent-Native Retrieval via LLM-Wiki. https://arxiv.org/abs/2605.25480[13] Prompt Compression for Large Language Models: A Survey. https://arxiv.org/abs/2410.12388[14] LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression. https://arxiv.org/abs/2403.12968[15] UQE: A Query Engine for Unstructured Databases. https://arxiv.org/abs/2407.09522[16] Continuous Prompts: LLM-Augmented Pipeline Processing over Unstructured Streams. https://arxiv.org/abs/2512.03389[17] Ragas Documentation. https://docs.ragas.io/en/latest/getstarted/[18] Traversal-as-Policy: Log-Distilled Gated Behavior Trees as Externalized, Verifiable Policies for Safe, Robust, and Efficient Agents. https://arxiv.org/abs/2603.05517[19] Is Semantic Chunking Worth the Computational Cost?  https://arxiv.org/abs/2410.13070[20] Late Chunking: Contextual Chunk Embeddings Using Long-Context Embedding Models.https://arxiv.org/abs/2409.04701[21] Intent-Driven Dynamic Chunking: Segmenting Documents to Reflect Predicted Information Needs.https://arxiv.org/abs/2602.14784[22] Precise Zero-Shot Dense Retrieval without Relevance Labels. https://arxiv.org/abs/2212.10496[23] Expand, Rerank, and Retrieve: Query Reranking for Open-Domain Question Answering. https://arxiv.org/abs/2305.17080[24] AutoRAG: Automated Framework for optimization of Retrieval Augmented Generation Pipeline.https://arxiv.org/abs/2410.20878[25] QuIM-RAG: Advancing Retrieval-Augmented Generation with Inverted Question Matching for Enhanced QA Performance. https://arxiv.org/abs/2501.02702[26] OpenViking. https://github.com/volcengine/OpenViking
```

![图片](https://mmbiz.qpic.cn/mmbiz_png/vI9nYe94fsGxu3P5YibTO899okS0X9WaLmQCtia4U8Eu1xWCz9t8Qtq9PH6T1bTcxibiaCIkGzAxpeRkRFYqibVmwSw/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1&tp=webp#imgIndex=20)

**一起“ **点** **赞”** **三连** ↓**

闪记

复制 LaTeX 公式