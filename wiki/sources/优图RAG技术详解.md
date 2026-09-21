---
type: source
tags:
- RAG/retrieval
summary: 腾讯优图RAG全栈技术：2B级Embedding多阶段训练、Reranker分层蒸馏、Text2SQL多智能体框架MAC-SQL、自研GraphRAG（知识树+S2Dual社区检测+AgenticGraphQ）
sources:
- raw/articles/万字长文详解优图RAG技术.md
updated: '2026-07-01'
---
# 优图RAG技术详解

## 摘要

腾讯优图实验室 RAG 全栈解决方案：覆盖语义检索（Embedding+Reranker）、结构化表检索（Text2SQL）、图检索（GraphRAG）三大模块。自研 apd-embedding-2b 模型在 C-MTEB 中文 IR/STS 任务达 SOTA；Reranker 升级为 LLM 并引入分层知识蒸馏；Text2SQL 采用 MAC-SQL 多智能体框架；GraphRAG 知识树结构融合图与树优点，构图成本降至百万级 token。

## [重点/高亮] Embedding模型任务定制损失

用户高亮内容：

> 具体到编码模型最主要的两类应用场景——文本语义相似性（STS）及信息检索（IR）。STS任务采用Spearman相关系数作为根本指标，该指标通过计算样本的预测排位与真实排位之差来衡量顺序一致性。IR任务的核心指标nDCG同样是list-wise式的，但它更强调高位优先性。鉴于在大部分IR任务中，与给定query相关的文档其实非常稀少，因此将这些正样本有效突出出来是提升模型表现的关键。

## 语义检索

### Embedding模型（apd-embedding-2b）

#### 多阶段训练管线
1. 弱监督对比学习：批次内+跨设备负样本共享，每查询对应6万负样本
2. 有监督对比学习：跨设备共享负样本来自同一子数据集；加入任务指令进行指令感知对比学习

#### 精细化数据工程
- 数据构造：开源问答对 + LLM合成问题；两千万规模语料库挖掘难负样本
- 质量控制：Reranker筛选（剔除伪正例、过滤简单负例、识别潜在正样本替换）
- Reranker评分实现label层面知识蒸馏

#### 多任务均衡配置
- 数据统一化：IR和STS两大类统一格式混合加载
- 动态采样器：一次iteration中多GPU严格出自同一数据集，支持差异化batch size
- 任务特定指令及损失：STS和IR不同损失函数+个性化指令
- 模型融合策略：ModelSoups权重融合

#### 任务定制损失
- STS：顺序性损失（逆序对、分数差异性），捕获细粒度语义区别
- IR：扩大query与所有正样本相似度分数，增强判别能力

#### 效果
- C-MTEB中文IR和STS任务SOTA
- 2B参数量超越竞品4B、8B模型

### Reranker模型

#### LLM化升级
- 传统Reranker（BERT/RoBERTa，110M~400M，512 token）→ LLM Reranker（8k+ token）
- 支持特殊任务指令适配不同场景

#### 分层知识蒸馏损失（Layerwise）
- 多个层级Transformer输出添加约束
- 强化模型在不同深度层给出一致的查询-文档相似度分数
- 无教师分数时用最后一层输出约束前层（自蒸馏）
- 允许用户选择不同层输出，在性能和推理速度间权衡

#### 高质量业务训练数据构造
- 流程：Query预处理→实体识别→文档实体召回→文档初筛→文档精评分→分数校准→自适应正负例筛选
- 实体召回粗筛降低精评分文档量；实体分数校准缓解LLM幻觉
- 正例：高分突出时固定≤10个，高分均衡时最大分均为正例
- 负例：按正例数量固定比例，高到低补齐保留难负例

## 结构化信息检索（Text2SQL）

### 多源数据检索
- 支持DB数据库表和表格文件
- 文本切片RAG + Text2SQL融合→阅读理解模型综合生成

### Text2SQL核心技术

#### 自动化数据合成
- 自动生成多语言数据库表结构+自然语言问题+带推理过程SQL答案
- 适配不同数据库方言（SQLite/MySQL等）

#### MAC-SQL多智能体框架（COLING 2025）
- Selector（筛选器）：选择相关表和列
- Decomposer（分解器）：复杂问题分解为子问题逐步解决
- Refiner（优化器）：执行SQL获取反馈，优化错误SQL
- 自研7B模型执行准确率超ChatGPT-3.5；配合GPT-4达SOTA

### 技术实践

#### 表格文件场景
- 高精度结构化解析（非标准表格→结构化，精度90%+）
- 灵活语义窗口切分：表头+表内容组合多粒度切分
- 双引擎SQL查询：ES + MySQL
  - AST语法校验与自动校正
  - ES泛化查询提升模糊匹配召回

#### 通用DB场景
- DDL/SimpleDDL两种schema提示词范式
- Schema Linking + Value Linking（引入语义向量）
- 改写信号拆解与融合：编辑矩阵融入self-attention（EMNLP 2022, PRICAI 2023）

## GraphRAG

### 自研GraphRAG-Benchmark
- 四维度评价：构图成本/检索效率/回复准确率/推理能力
- 评测9种方法：RAPTOR向量检索最快；GFM-RAG/GraphRAG/HippoRAG准确率领先

### 自研GraphRAG框架

#### 知识树结构
- 融合图（细粒度知识推理）和树（层次化汇总摘要）
- 四级知识粒度：属性/知识图(三元组)/关键词/社区
- 节点类型：实体和关系（连接语义单元）、属性（实体特征）、社区（核心信息总结）

#### S2Dual-perception社区检测
- 解决Leiden算法问题（强制连接性划分、全图遍历效率低）
- Structure感知：稀疏邻接矩阵Jaccard相似度量化拓扑重合度
- Semantics感知：编码锚节点与候选社区子图文本相似度
- 效率提升近100%（对比Leiden）

#### AgenticGraphQ复杂Query理解
- 首次将图Schema应用到Query理解和子任务解耦
- 挖掘Query中Entity/Relation/Attribute隐式关系和依存句法
- 多跳→单跳简化，降低对推理模型依赖

#### 高效多路检索
- 主题词/关键词检索
- Query-Triple三元组向量匹配+相关性剪枝
- DFS邻居检索

#### 效果
- 构图token：微软GraphRAG亿级/LightRAG千万级/优图GraphRAG百万级
- 准确率：对比微软GraphRAG提升200%+，对比LightRAG提升20%-100%

## 未来展望

1. Agentic RAG：复杂问题自动分解+多步骤推理
2. 精细化与低成本：动态增量更新、轻量化建模
3. 发展为"规划-决策-检索-验证-推理"一体化闭环

## 关联

- 相关概念：[[概念_Dense_Embedding_稠密向量嵌入]]、[[概念_Rerank_重排序]]、[[概念_分层知识蒸馏]]、[[概念_Embedding训练管线]]、[[概念_Text2SQL_自然语言转SQL]]、[[概念_Graph_RAG_知识图谱增强检索]]、[[概念_Agentic_RAG_智能体检索增强生成]]、[[概念_知识树结构]]
- 实体：[[实体_优图实验室]]、[[实体_MAC-SQL]]

---
> 📎 **物理文献**：[[raw/articles/万字长文详解优图RAG技术.md]]