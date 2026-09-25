---
type: "source"
tags:
  - "RAG/retrieval"
  - "RAG/eval"
  - "AI-Agent/context-engineering"
summary: "系统梳理面向 Agent 的 RAG 技术选型指南：解构 Naive/Advanced/Modular 演进脉络，对比 GraphRAG、Agentic RAG、LLM Wiki 与上下文压缩，并建立检索与生成解耦的评估闭环及非 RAG 适用边界。"
sources:
  - "raw/articles/Agent时代，RAG怎么选？这份指南一次讲清！.md"
updated: "2026-09-25"
---

# Agent时代，RAG怎么选？这份指南一次讲清！

## 来源信息
- **标题**：Agent时代，RAG怎么选？这份指南一次讲清！
- **作者**：卞一岚（Datawhale、百度ACG实习生、河海大学研究生）
- **发布日期**：2026-09-22
- **原文链接**：https://mp.weixin.qq.com/s/4XGijn-_H1KH05op--1kBg

## 核心要点
1. **RAG 核心本质转变（Context Construction over Retrieval）**：在 Agent 语境下，RAG 不再是简单的相似片段检索（retrieval），而是为了补全模型此刻需要却未知信息的上下文构建系统（context construction）。检索只是手段，目标是让模型看到足够相关、完整且有结构的上下文。
2. **经典 RAG 演进三代（Naive → Advanced → Modular）**：
   - **Naive RAG**：遵循离线 `Load -> Split -> Embed -> Store` 与在线 `Query -> Retrieve -> Rerank -> Generate` 线性闭环，易受分块破碎与语义丢失困扰；
   - **Advanced RAG**：在各环节精细化补强，引入 [[concepts/概念_文本切分五层级|Late Chunking]]（长上下文先整篇编码再切分）、[[concepts/概念_HyDE_假设文档嵌入|HyDE]]/Multi-Query 查询改写、[[concepts/概念_混合检索|混合检索]]（Dense + BM25）与 Cross-Encoder [[concepts/概念_Rerank_重排序|Rerank]]；
   - **[[concepts/概念_Modular_RAG_模块化检索增强生成|Modular RAG]]**：打破线性 retrieve-then-generate 流程，将 RAG 解构为可替换、可路由、可组合的独立模块，支持条件分支、多跳路由与反馈循环。
3. **关系密集与结构化场景的选型权衡（GraphRAG vs LightRAG）**：
   - 当答案散落在跨文档实体关系中时，[[concepts/概念_Graph_RAG_知识图谱增强检索|GraphRAG]] 通过实体/关系抽取与社区摘要构建全局语义网，但面临极高 LLM Token 构建成本与增量更新困难；
   - **LightRAG** 保留实体-关系主线，采用图结构与向量双层检索并强化局部图增量合并，是兼顾秒级响应与可控成本的实用折中。
4. **[[concepts/概念_Agentic_RAG_智能体检索增强生成|Agentic RAG]] 与循环决策机制**：
   - 将检索包装为智能体工具（Tool over Function），由 Agent 循环进行“决策 -> 检索 -> 反思 -> 再检索”；
   - 引入 Sufficient Context Agent 评估上下文充沛度，利用 session 级 `consumed_ids` 过滤与记忆图（如 VimRAG）避免重复检索，并通过 Citation Resolver 进行语法、哈希及语义蕴含三层引用真实性核查；
   - 明确其能力边界为“路径走完”，对全局统计与量词验证（如“是否全部满足”）仍需依赖 Evergreen 等语义查询引擎。
5. **稳定知识预编译与上下文压缩**：
   - **[[concepts/概念_LLM_Wiki范式|LLM Wiki]] / 知识预编译**：稳定、高频、跨文档综合的知识应预编译为 Markdown 知识库（Raw sources -> Wiki -> Schema），避免每次临场从头煮生水；
   - **[[concepts/概念_Contextual_Compression_上下文压缩|上下文压缩]]**：区分自然语言符号空间的硬压缩（如 LLMLingua-2 抽取式压缩，具任务无关性与复用性）与连续向量/KV 空间的软压缩，权衡模型绑定风险与 token 收益。
6. **RAG 评估第一原则（检索层与生成层解耦诊断）**：
   - 必须通过 [[concepts/概念_RAGAS_RAG评估框架|RAGAS]] 等框架拆分评估维度：检索层关注 Context Precision（相关度排序）与 Context Recall（关键证据召回）；生成层关注 Faithfulness（证据忠实度）与 Answer Relevancy（切题度）；
   - 引入 **Noise Sensitivity（噪声敏感度）** 监控抗冗余干扰能力；
   - 测试集必须覆盖单跳具体、单跳抽象、多跳具体、多跳抽象四象限，实现“指标异常 -> 对应模块定向优化”。
7. **什么时候不该用 RAG（五大非 RAG 适用边界）**：
   - ① **MB 级本地代码库**：优先使用 `grep`/`glob`/`read`/`git` 等 CLI 原语精准定位，无需过早引入向量检索开销；
   - ② **全局量词与聚合统计**：使用 UQE/Evergreen 等语义查询引擎而非局部样本检索；
   - ③ **个人助手外部状态**：应构建严肃的 Memory 架构（Raw Ledger、Derived Views、Policy）而非松散向量检索；
   - ④ **持续事件监控**：应采用 Continuous RAG 流式管道计算；
   - ⑤ **复杂业务长链路**：采用 Plan-and-Execute + ReAct 状态机推进，避免单次召回误差击穿执行流。

## 关联概念与实体
- **关联概念**：
  - [[concepts/概念_Modular_RAG_模块化检索增强生成]]
  - [[concepts/概念_RAG基础流程]]
  - [[concepts/概念_Agentic_RAG_智能体检索增强生成]]
  - [[concepts/概念_Graph_RAG_知识图谱增强检索]]
  - [[concepts/概念_LLM_Wiki范式]]
  - [[concepts/概念_Contextual_Compression_上下文压缩]]
  - [[concepts/概念_Prompt_Compression_提示词压缩]]
  - [[concepts/概念_RAGAS_RAG评估框架]]
  - [[concepts/概念_混合检索]]
  - [[concepts/概念_Rerank_重排序]]
  - [[concepts/概念_HyDE_假设文档嵌入]]
  - [[concepts/概念_BM25_最佳匹配25算法]]
  - [[concepts/概念_RRF_互易秩融合]]
  - [[concepts/概念_文本切分五层级]]
  - [[concepts/概念_上下文工程]]
- **关联实体**：
  - [[entities/实体_Claude_Code]]
  - [[entities/实体_Andrej_Karpathy]]
  - [[entities/实体_Anthropic]]
  - [[entities/实体_RAGAS]]

> 📎 **物理文献**：[[raw/articles/Agent时代，RAG怎么选？这份指南一次讲清！.md]]
