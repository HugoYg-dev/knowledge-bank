---
type: "concept"
tags:
  - "RAG/retrieval"
summary: "将 RAG 拆解为可替换、可路由、可组合独立功能模块的架构范式，突破线性流程，支持条件分支、动态调度与循环迭代。"
aliases:
  - "Modular RAG"
  - "Modular Retrieval-Augmented Generation"
  - "模块化RAG"
  - "模块化检索增强生成"
  - "概念_Modular_RAG"
sources:
  - "wiki/sources/Agent时代，RAG怎么选？这份指南一次讲清！.md"
updated: "2026-09-25"
---

# 概念_Modular_RAG_模块化检索增强生成

## 定义

**模块化检索增强生成（Modular RAG）** 是将传统 RAG 系统解构为独立、可替换、可自由编排与路由的功能组件的架构范式。与 Naive RAG 的单一固定管道以及 Advanced RAG 的单点补强不同，Modular RAG 突破了“检索-生成（Retrieve-then-Generate）”的线性枷锁，引入条件分支（Conditional）、多路路由（Branching）与反馈循环（Looping）机制，形成乐高积木式的高度可重构框架。

## 演进背景与核心思想

RAG 架构经历了三代演进：
1. **Naive RAG**：遵循离线索引（Load -> Split -> Embed -> Store）与在线查询（Query -> Retrieve -> Generate）的简单线性链条。易受切块碎片化、词义鸿沟与幻觉困扰；
2. **Advanced RAG**：在线性骨架的特定阶段加入增强算子（如前置 Query Rewrite、混合检索、后置 Rerank、提示词约束），但本质仍是将所有请求送入同一套重型流水线；
3. **Modular RAG**：将 RAG 从固定管道升级为计算图或工作流。其核心思想是根据查询的类型、难度与上下文完备度，动态调度最优的模块路径。

## 核心功能模块划分

Modular RAG 将整个检索增强体系解构为十个核心可热插拔模块：
- **Loader（加载器）**：解析 PDF、Word、HTML、表格等多源异构数据并提取元数据；
- **Splitter（切分器）**：执行固定字符、递归切分、文档结构切分、语义切分或 Late Chunking；
- **Embedder（嵌入器）**：针对稠密向量、稀疏向量或多向量（如 ColBERT）进行特征编码；
- **Retriever（检索器）**：执行 Dense 检索、BM25 稀疏检索或图数据库查询；
- **Reranker（重排序器）**：使用 Cross-Encoder 对多路候选进行精细化语义对齐重排；
- **Query Rewriter（查询改写器）**：进行指代消解、多查询扩展（Multi-Query）或假设文档生成（HyDE）；
- **Fusion（融合器）**：采用互易秩融合（RRF）或加权评分归一化多路召回结果；
- **Compressor（压缩器）**：通过抽取式硬压缩（如 LLMLingua-2）或语义剪枝减少冗余 token；
- **Generator（生成器）**：在受限提示词或约束解码下生成忠于证据的回答；
- **Evaluator（评估器）**：在线实时评测召回相关度、忠实性与置信度，决定是否触发回退或二次检索。

## 编排机制与典型模式

- **条件路由（Conditional Routing）**：简单事实题路由至单一 Dense/BM25 检索；复杂分析题路由至混合检索或知识图谱；
- **动态分支（Branching / Multi-source Fanout）**：跨领域问题同时并发分发至法务、技术、财务等多个独立垂直知识库，再经 Fusion 层汇总；
- **反馈闭环（Looping / Iterative Retrieval）**：当 Evaluator 判定当前上下文不足或证据冲突时，自动触发 Query 改写并重新检索，形成自我纠错闭环。

## 代表实践与实现

- **AutoRAG**：自动搜索并评测不同分块策略、Embedding 模型、检索器与重排序器的组合，寻找特定数据集上的全局最优 Pipeline；
- **QuIM-RAG**：将“Query-Document 匹配”转换为“Query-Query 匹配”，通过问题倒排索引大幅提升问答召回精度；
- **OpenViking**：采用类文件系统范式管理记忆、技能与检索资源，使检索链路高度可解释、可单步调试；
- **Experience-RAG Skill**：将检索策略选择从业务硬编码中剥离，由系统根据运行时任务特征在 BM25、Rewrite-BM25、Dense 与 Hybrid 之间动态切换。

## 选型原则与权衡边界

- **适用场景**：多知识库、多检索器、跨业务任务类型、要求严密控制延迟与成本的生产级智能体系统；
- **防过度工程化第一原则**：**先证明文档能被找对，再讨论模型能不能答好**。初创小规模场景优先验证 Naive/Advanced RAG 基线；只有当业务出现多样化问法、不同成本预算与跨模态数据源时，才需引入 Modular RAG 的策略路由层，避免盲目堆砌模块导致延迟与调试成本暴增。

## 关联

- 相关概念：[[concepts/概念_RAG基础流程]]、[[concepts/概念_Agentic_RAG_智能体检索增强生成]]、[[concepts/概念_Graph_RAG_知识图谱增强检索]]、[[concepts/概念_混合检索]]、[[concepts/概念_Rerank_重排序]]、[[concepts/概念_RAG_Routing_检索智能路由]]、[[concepts/概念_RAGAS_RAG评估框架]]
- 来源：[[wiki/sources/Agent时代，RAG怎么选？这份指南一次讲清！.md]]
