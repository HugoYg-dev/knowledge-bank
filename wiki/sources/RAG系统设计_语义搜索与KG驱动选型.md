---
type: source
tags:
- RAG/embedding
- RAG/retrieval
summary: RAG 的本质是提示工程（Prompt Engineering）：通过改变条件调整概率分布，不改变模型参数 θ
sources:
- raw/articles/RAG系统设计：揭秘语义搜索被低估的核心价值与KG驱动的架构选型策略.md
updated: '2026-07-01'
---
# RAG系统设计_语义搜索与KG驱动选型

## 来源信息

- **标题**：RAG系统设计_语义搜索与KG驱动选型
- **作者**：尹一峰 / Hugging Face
- **发布时间**：2025-05-19
- **URL**：https://mp.weixin.qq.com/s?__biz=MzU1NDA4NjU2MA==&mid=2247639036&idx=2&sn=374549b625d449cf9d137783ae038dd0


> AICon 演讲实录，深入探讨语义搜索在 RAG 中的核心价值、系统设计权衡，以及 KG-RAG 的适用场景。

## 主要内容

### RAG 本质

- RAG 的本质是提示工程（Prompt Engineering）：通过改变条件调整概率分布，不改变模型参数 θ
- 解决两个问题：分布偏移（新知识对抗）+ 幻觉（相关文件减少）
- 任何形式的搜索（SQL/Google/数据库）都可以作为 RAG 输入

### Semantic Search 本质

- 核心：metric embedding，将文件映射到高维测度空间
- 本质是"document as index"——文件本身作为索引
- 灵活性：没有内在数据结构，反而可赋予任何合适的数据结构（"无为而无不为"）
- Multi-Vector Retrieval：用自然语言（注释/README）索引代码、用摘要索引长文本
- 多模态检索：图像/表格/文本分别生成标签，通过自然语言统一检索

### 系统设计——Loss Function 选择

- Contrastive Loss：形成相距 m 距离的紧密聚类，适合方差较小的数据
- Triplet Loss：关注 positive/negative 与 anchor 的相对距离差，同类内方差较大；适合类内方差大的数据（如人脸识别）
- 选择前提：必须充分了解数据特性

### 系统设计——Distance Function 选择

- 余弦距离：不满足度量空间（非负性、三角不等式），但计算简单只考虑方向，适合推荐系统
- 欧几里得距离（L2）：满足度量空间，适合复杂场景（电商推荐），可利用三角不等式实现跨模态传递

### 系统设计——Embedding 模型选择

- LLM vs Encoder 权衡：Encoder 归纳偏差更适合嵌入任务，小模型可接近大模型效果
- NV embed-2（7B, 72.31分）vs Stella（435M, 70.11分）——性能差距小但参数差数倍
- 优先级：性能/成本 > 数据领域 > 损失函数 > 距离度量

### 系统设计——Vector Database 选择

- 索引类型：哈希（快但准确度一般）、树（低维好）、图/HNSW（高维友好、省内存）、倒排索引IVF（需乘积量化加速）
- 考虑因素：开源/闭源、实现语言、On-premise/云端、嵌入式模式

### 给 Semantic Search 一个结构

- 分层结构：教科书→章节→小节；代码→文件→片段
- Context Enrichment：句子级定位后添加上下文信息
- Parent-child chunk retrieve：片段关联到完整文件

### Query Transformation

- Step back prompting：退一步思考背后原理
- 宽泛查询拆分为具体子查询
- 反馈+反思（Reflection）逐步优化

### KG-RAG

- 适用场景：实体+关系明确的数据（面向全局查询和聚焦总结）
- 成本：约为简单向量 RAG 的 1000 倍
- Lazy Graph RAG：语义搜索+知识图谱结合，索引成本降至上一代的 0.1%
- 设计原则：KG-RAG 用于全局/实体关系查询，Semantic Search 用于无结构数据快速检索

### 未来趋势

- 端设备 RAG（手机端存储+快速 RAG）
- 非 Transformer 架构（RWKV/Mamba/TTT/Hyena）：嵌入和生成可由同一模型完成
- 核心原则：尽量避免使用 ML，传统方法（SQL/ES/正则）能解决就不用 LLM

## 关联

- 相关概念：[[概念_Embedding与向量检索]]、[[概念_Graph_RAG_知识图谱增强检索]]、[[概念_Graph_RAG_知识图谱增强检索]]、[[概念_向量数据库]]、[[概念_向量索引方法]]、[[概念_向量相似度度量]]、[[概念_ColBERT_多向量延迟交互检索]]、[[概念_Multi_Representation_Indexing_多表征索引]]、[[概念_Step_Back_回退提示]]、[[概念_父页面检索]]
- 实体：[[实体_HNSW]]

---
> 📎 **物理文献**：[[raw/articles/RAG系统设计：揭秘语义搜索被低估的核心价值与KG驱动的架构选型策略.md]]