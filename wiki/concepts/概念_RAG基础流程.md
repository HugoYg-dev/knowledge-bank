---
type: concept
tags:
- RAG/retrieval
summary: RAG（Retrieval Augmented Generation，检索增强生成）是一种将 LLM 与外部数据源（私有数据或最新数据）连接的通用方法，允许
  LLM 使用外部数据生成输出。解决 LLM 训练数据不含任务相关数据或非最新数据的问题。
sources:
- wiki/sources/Anthropic多智能体研究系统构建.md
- wiki/sources/OpenAI_LLM应用最佳实践.md
- wiki/sources/RAG_12痛点与解决方案.md
- wiki/sources/RAG基础_索引检索生成.md
- wiki/sources/RAG挑战赛冠军方案.md
- wiki/sources/TableRAG_文本表格异构问答.md
- wiki/sources/斯坦福RAG新基线_DOS_RAG.md
- wiki/sources/淘宝直播数字人_LLM文案生成技术.md
- wiki/sources/Agent时代，RAG怎么选？这份指南一次讲清！.md
updated: '2026-09-25'
---

# 概念_RAG基础流程


## 定义

RAG（Retrieval Augmented Generation，检索增强生成）是一种将 LLM 与外部数据源（私有数据或最新数据）连接的通用方法，允许 LLM 使用外部数据生成输出。解决 LLM 训练数据不含任务相关数据或非最新数据的问题。

## 三步流程

1. **Indexing（索引）**：对外部文档建立索引
2. **Retrieval（检索）**：根据用户问题检索相关文档
3. **Generation（生成）**：将问题 + 相关文档输入 LLM 生成最终答案

## 补充：通用架构（来源：北大 AIGC 综述）

北大 PKU-DAIR 综述给出通用 RAG 流程：面对输入查询，检索器定位并提取相关数据源，检索结果与生成器交互提升生成质量。用户查询和生成结果均可为多种模态（文本/代码/音频/图像/视频/3D）。

## 补充：OpenAI 视角（来源：OpenAI 最佳实践）

OpenAI DevDay 将 RAG 定位为 **Context Optimization** 手段：集成外部知识库（私有/特定领域数据）通过 ICL（In-Context Learning）解决模型幻觉和知识不足。适合注入/更新知识、减少幻觉；不适合教模型新语言/格式、减少 Token 使用。

## Agent 时代的本质跃迁与演进三代

- **核心本质跃迁（Context Construction over Retrieval）**：传统 RAG 将焦点置于检索（Retrieval）环节；而在智能体（Agent）工程语境下，RAG 本质是一套围绕模型搭建的**上下文构建系统（Context Construction System）**。检索仅为手段，最终目标是根据模型推理瞬时所需，动态装配具备高度相关性、完整性与结构化的上下文。
- **经典三代演进脉络**：
  1. **Naive RAG**：遵循离线索引（Load -> Split -> Embed -> Store）与在线查询（Query -> Retrieve -> Generate）的简单线性链条；
  2. **Advanced RAG**：在线性骨架关键环节定向补强，引入查询改写（[[concepts/概念_HyDE_假设文档嵌入|HyDE]]/Multi-Query）、长上下文分块（Late Chunking）、[[concepts/概念_混合检索|混合检索]]（Dense + BM25）与精排（Cross-Encoder [[concepts/概念_Rerank_重排序|Rerank]]）；
  3. **[[concepts/概念_Modular_RAG_模块化检索增强生成|Modular RAG]]**：打破线性流程，将各环节解构为可独立编排、路由与反馈循环的模块化计算图。

## 什么时候不该用 RAG（适用边界与反模式）

RAG 仅为“在推理阶段填补一小段外部上下文”的特定手段，当面临以下场景时不应默认套用向量检索：
1. **MB 级本地代码库**：精确标识符与文件路径搜索（`grep`/`rg`/`glob`/`read`）配合语法树探索，由于保留了路径结构与执行反馈信号，工程表现远优于语义切块向量检索；
2. **全局量词与聚合统计**：面对“所有实体是否满足条件”、“比例是否超半数”等全局验证问题，局部切块检索极易导致局部以偏概全，应采用语义查询引擎（如 UQE、Evergreen）进行查询编译与验证；
3. **个人助手外部状态（Memory）**：长期状态不能退化为松散的“召回几段旧话”，而需包含原始事件账本（Raw Ledger）、派生视图（Derived Views）与读写策略（Policy）的完整状态体系；
4. **持续事件流监控**：舆情或风险监控属于流式连续语义管道，应采用 Continuous RAG 流处理算子而非单次孤立问答；
5. **复杂业务长链路**：多步骤高耦合流程中，一次检索错误将击穿执行流，应通过 Plan-and-Execute + ReAct 状态推进，将知识沉淀为确定性脚本。

## 关联

- 相关概念：[[概念_Embedding与向量检索]]、[[概念_向量数据库]]、[[concepts/概念_Modular_RAG_模块化检索增强生成]]、[[concepts/概念_Agentic_RAG_智能体检索增强生成]]、[[concepts/概念_Graph_RAG_知识图谱增强检索]]、[[概念_LLM应用优化两轴]]
- 进阶技巧：[[概念_Query_Translation_查询改写与翻译]]、[[概念_RAG_Routing_检索智能路由]]、[[概念_Query_Construction_查询构建]]、[[概念_Multi_Representation_Indexing_多表征索引]]
- 来源：[[RAG基础_索引检索生成]]、RAG综述_北大AIGC2024、[[OpenAI_LLM应用最佳实践]]、[[wiki/sources/Agent时代，RAG怎么选？这份指南一次讲清！.md]]