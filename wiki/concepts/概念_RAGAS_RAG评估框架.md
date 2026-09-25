---
type: concept
tags:
- RAG/eval
summary: RAGAS 是专为检索增强生成（RAG）系统设计的开源评估框架，提供一套全面的多维度指标，衡量 RAG 系统在检索准确性、生成内容与检索上下文一致性等方面的表现。
sources:
- wiki/sources/Agent Loop使用语义早停比max_iterations硬截断节省38% Token 且质量不降.md
- wiki/sources/OpenAI_LLM应用最佳实践.md
- wiki/sources/RAGAS评估RAG系统.md
- wiki/sources/Agent时代，RAG怎么选？这份指南一次讲清！.md
updated: '2026-09-25'
aliases:
- RAGAS
- Retrieval Augmented Generation Assessment
- RAG评估框架
- 概念_RAG评估框架RAGAS
---

# 概念_RAGAS_RAG评估框架


## 定义

RAGAS 是专为检索增强生成（RAG）系统设计的开源评估框架，提供一套全面的多维度指标，衡量 RAG 系统在检索准确性、生成内容与检索上下文一致性等方面的表现。

## 为何需要

传统指标（BLEU、ROUGE）依赖表面文本匹配，无法衡量检索质量、上下文利用、事实一致性和信息完整性。

## 核心评估指标

### 检索侧

- **上下文召回率（Context Recall）**：检索是否找全关键内容 = 上下文支持的关键点数 / 标准答案总关键点数
- **上下文精确度（Context Precision）**：检索结果有多准，按相关性排序的加权精确度（排名靠前更重要）
- **上下文实体召回率（Context Entity Recall）**：关键实体覆盖率 = |E_ref ∩ E_context| / |E_ref|

### 生成侧

- **答案相似度（Answer Similarity）**：答案与标准答案的语义余弦相似度（需标注）
- **回答相关性（Answer Relevance）**：LLM 根据回答反推问题，与实际问题计算平均相似度（无需标注）
- **忠实性（Faithfulness）**：回答是否基于检索上下文
- **答案正确性（Answer Correctness）**：需标注

### 系统鲁棒性侧

- **噪声敏感度（Noise Sensitivity）**：评估系统在面对相关但冗余、或完全不相关的噪声上下文时是否会被带偏。高敏感度表明模型缺乏证据筛选能力，需通过收紧重排阈值或强化 Prompt 证据约束加以治理。

## 评估驱动的定向调优映射表

RAG 评估的核心价值在于将指标异常转化为明确的工程优化动作：

| 指标异常表现 | 核心根因诊断 | 定向工程优化动作 |
| :--- | :--- | :--- |
| **Context Recall 偏低** | 关键证据未能在检索阶段召回 | 调整分块策略（Late Chunking）、丰富查询扩展（HyDE / Multi-Query）、引入混合检索（Dense+BM25） |
| **Context Precision 偏低** | 检索返回的 Top-K 存在较多噪音且排序靠后 | 引入前置元数据过滤、采用 Cross-Encoder 重排（Reranker）、精简 Top-K 截断窗口 |
| **Faithfulness 偏低** | 模型未忠实基于召回上下文，产生上下文内幻觉 | 降低生成温度（Temperature）、强约束证据引用规则、增加 Citation Resolver 校验 |
| **Answer Relevancy 偏低** | 回答内容跑题或未正面回应用户核心诉求 | 细化意图识别路由、针对具体问题类型定制专属 Prompt 模板 |
| **Noise Sensitivity 偏高** | 模型易受表面相似但事实无关的上下文干扰 | 强化精排分数门槛过滤、训练或提示模型主动识别并丢弃无支撑推断 |

## 测试集构建四象限

构建可靠基准测试集必须覆盖以下四类场景，防止系统在简单事实题上表现良好而在复杂真实问法中失效：
1. **单跳具体问题**：检验基础事实抽取的精确命中；
2. **单跳抽象问题**：检验单文档内的归纳概括与核心逻辑提炼；
3. **多跳具体问题**：检验跨文档、跨实体线索的链式检索与对齐；
4. **多跳抽象问题**：检验多源跨文档综合、发展演化脉络与全局结构性理解。

## 注意事项

- 自动化评估只能作为参考，仍脱离不了人工评估
- 指标设计可作为评估自己系统的灵感启发，可灵活选择

## 补充：OpenAI 实践中的 RAGAS 四指标

OpenAI DevDay 介绍在 RAG 阶段评估时引入 Ragas，给出四个指标（值均介于 0~1，越高越好）：
- **生成指标**：忠诚度（答案与上下文事实一致性）、答案相关性（答案与提示相关性，反推问题计算）
- **检索指标**：上下文精度（相关条目是否排名靠前）、上下文召回（检索上下文与标注答案一致程度）

## 关联

- 相关概念：[[概念_Embedding与向量检索]]、[[概念_BM25_最佳匹配25算法]]、[[概念_混合检索]]、[[概念_Rerank_重排序]]、[[概念_LLM应用优化两轴]]、[[concepts/概念_Modular_RAG_模块化检索增强生成]]
- 来源：[[RAGAS评估RAG系统]]、[[OpenAI_LLM应用最佳实践]]、[[wiki/sources/Agent时代，RAG怎么选？这份指南一次讲清！.md]]