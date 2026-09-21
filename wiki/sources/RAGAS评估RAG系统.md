---
type: source
tags:
- RAG/eval
summary: BLEU：n-gram 匹配 + 简短惩罚，仅关注词语匹配忽略语义，无法评估检索质量和事实一致性
sources:
- raw/articles/用 RAGAS 精准定位 RAG 系统短板.md
updated: '2026-07-01'
---
# RAGAS评估RAG系统

## 来源信息

- **标题**：RAGAS评估RAG系统
- **作者**：筱可 / 筱可AI
- **发布时间**：2025-09-26
- **URL**：https://mp.weixin.qq.com/s?__biz=MzkwNjcxNTc2Ng==&mid=2247484810&idx=1&sn=8a4180ab552ce9305ab5bbaead771396


> 介绍 RAGAS 评估框架的核心指标、计算原理和实战用法，用于科学评估 RAG 系统性能。

## 主要内容

### 传统评估指标的局限

- BLEU：n-gram 匹配 + 简短惩罚，仅关注词语匹配忽略语义，无法评估检索质量和事实一致性
- ROUGE：召回率导向（ROUGE-N/L/S），依赖表面文本匹配，可能给冗长低质量输出高分

### RAGAS 核心评估指标

#### 1. 上下文召回率（Context Recall）

- 衡量检索是否找全了回答问题需要的关键内容
- 公式：Context Recall = 上下文支持的关键点数 / 标准答案总关键点数
- 用 LLM 提取标准答案关键要点，判断检索上下文能支持多少个

#### 2. 上下文精确度（Context Precision）

- 衡量检索结果中有多少与问题真正相关
- 考虑排序的加权精确度：Precision@K 加权，排名靠前的更重要
- 公式带 Precision@k × v_k 求和除以相关项总数

#### 3. 上下文实体召回率（Context Entity Recall）

- 检查关键实体（人名/地名/时间）的覆盖率
- 公式：|E_reference ∩ E_context| / |E_reference|

#### 4. 答案相似度（Answer Similarity）

- 用嵌入模型提取答案和标准答案的语义向量，计算余弦相似度
- 需要标准答案（Reference），适合有明确参考的场景

#### 5. 回答相关性（Answer Relevance）

- 无需标准答案：LLM 根据回答反推可能的问题，与实际问题计算相似度
- 公式：平均 sim(原问题, 各反推问题)

### 各指标输入需求

| 指标 | Question | Answer | Reference | Contexts | 需标注 |
|------|----------|--------|-----------|----------|--------|
| Context Recall | Yes | No | Yes | Yes | 否 |
| Context Precision | Yes | No | No | Yes | 否 |
| Answer Similarity | No | Yes | Yes | No | 是 |
| Answer Relevance | Yes | Yes | No | No | 否 |
| Faithfulness | Yes | Yes | No | Yes | 否 |
| Answer Correctness | Yes | Yes | Yes | No | 是 |

### 实战代码

- 依赖：ragas + langchain-openai + datasets
- LLM：DeepSeek-V3（通过硅基流动 API）
- Embedding：BAAI/bge-m3
- 评估流程：构建数据集 → 定义指标 → evaluate() → 分析结果

### 优化指导

- 上下文召回率低 → 增加检索结果数量/更先进检索算法
- 上下文精确度低 → 优化检索排序/过滤无关文档
- 答案正确性低 → 改进提示词/微调生成模型
- 响应相关性低 → 检查提示词是否引导模型聚焦问题

## 关联

- 相关概念：[[概念_RAGAS_RAG评估框架]]、[[概念_Embedding与向量检索]]、[[概念_BM25_最佳匹配25算法]]、[[概念_混合检索]]
- 实体：[[实体_BGE-M3]]

---
> 📎 **物理文献**：[[raw/articles/用 RAGAS 精准定位 RAG 系统短板.md]]