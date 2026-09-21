---
type: source
tags:
- RAG/retrieval
summary: 阿里云开发者文章：用 Python 基础库从零手撕 RAG 内核，含 10 大实战技巧——naive RAG/语义分块/上下文检索增强/块标题CCH/问题生成/Query改写/重排序/相关段落提取RSE/上下文压缩/反馈机制
sources:
- raw/playbooks/RAG技巧与底层代码剖析.md
updated: '2026-07-01'
---
# RAG技巧与底层代码剖析

## 摘要

阿里云开发者文章，仅用 numpy 等 Python 基础库从零实现 RAG 系统，逐步解剖 10 大实战技巧的底层逻辑和代码实现。涵盖从基础到高级的 RAG 优化全链路。

## 技巧一览（10 个）

1. **Naive RAG**：基础实现——PDF提取→固定长度分块→Embedding→余弦相似度检索→LLM生成
2. **语义分块（Semantic Chunking）**：百分位法/标准差法/四分位距法判断切分点
3. **上下文增强检索（Context-Enriched Retrieval）**：返回最相关块+前后相邻块
4. **块标题（Contextual Chunk Headers, CCH）**：LLM 为每块生成标题，标题+正文联合 Embedding 检索
5. **问题生成 RAG（Question Generation）**：为每块生成问题，问题也入向量库增强匹配
6. **Query 改写**：三种转换——查询重写/回退提问(Step-back)/子查询拆解
7. **重排序（Reranking）**：LLM 评分重排 + 关键词匹配重排
8. **相关段落提取（RSE, Relevant Segment Extraction）**：识别并重建连续文本段落，chunk_value 评分+最佳段落选择
9. **上下文压缩（Context Compression）**：三种模式(selective/summary/extraction)，LLM 过滤仅保留相关句子
10. **反馈机制（Feedback Loop）**：收集用户反馈→调整相关性评分→高质量QA对回注知识库→索引微调

## 一、Naive RAG 基础实现

- PDF 文本提取（PyMuPDF/fitz）
- 固定长度分块（chunk_size=1000, overlap=100）
- Embedding 生成（阿里云 text-embedding-v3）
- 余弦相似度语义搜索（top-k）
- LLM 基于检索块生成回答（qwen-max）
- 评估：LLM 评分（0/0.5/1）

## 二、语义分块

- 按句子切分 → 逐句 Embedding → 计算相邻句子余弦相似度
- 三种切分点判定方法：
  - **百分位法**：差异超过第X百分位阈值处切分
  - **标准差法**：差异超过均值-X*标准差处切分
  - **四分位距法**：Q1-1.5*IQR 识别异常变化点
- 生成语义完整的 chunks

## 三、上下文增强检索

- 核心思想：不只返回最相关块，同时返回前一个和后一个块
- context_window_size 控制上下文范围
- 解决孤立文本块缺乏上下文的问题

## 四、块标题（CCH）

- 用 LLM 为每个 chunk 生成描述性标题
- 检索时同时计算 query 与标题、正文的相似度取平均
- 标题提供高层上下文信息，提高检索相关性

## 五、问题生成 RAG

- LLM 为每个 chunk 自动生成 N 个相关问题
- 问题 Embedding 也存入向量库，metadata 指向原 chunk
- 检索时 query 既匹配原始 chunk 也匹配生成问题
- 提高召回率，尤其当 query 表述与原文不同时

## 六、Query 改写

### 查询重写（Query Rewriting）
- 让查询更具体、详细，提高检索精准度

### 回退提问（Step-back Prompting）
- 生成更广泛高层次问题获取背景信息

### 子查询拆解（Sub-query Decomposition）
- 复杂问题拆为多个简单子问题分别检索

## 七、重排序

### LLM 重排序
- LLM 对每个检索文档打 0-10 相关性评分
- 按评分重新排序取 top-n

### 关键词重排序
- 基础分(相似度*0.5) + 关键词匹配得分 + 位置加分 + 频率加分
- 轻量无需额外 LLM 调用

## 八、相关段落提取（RSE）

- 核心：识别连续文本块组合为连贯段落
- chunk_value = 相关性得分 - irrelevant_chunk_penalty
- find_best_segments：遍历可能的起止位置，找累加 value 最高的连续段落
- 限制最大段落长度和总长度
- 保留原文结构和语义连贯性

## 九、上下文压缩

- 三种压缩模式：
  - **selective**：保留原文中与 query 相关的句子（原始措辞不变）
  - **summary**：生成面向 query 的简洁摘要
  - **extraction**：仅提取直接相关的原句
- 计算压缩比例，过滤空内容，回退机制

## 十、反馈机制

- 收集用户反馈（相关性评分 1-5、质量评分 1-5、评论）
- 存储为 JSON 反馈日志
- assess_feedback_relevance：LLM 判断历史反馈是否与当前查询相关
- adjust_relevance_scores：根据历史反馈动态调整检索评分
- fine_tune_index：高质量 QA 对回注向量库（relevance_score=1.2 加权）
- 系统越用越准

## 关联

- 相关概念：[[概念_语义切分]]、[[概念_问题生成检索增强]]、[[概念_查询重写]]、[[概念_Step_Back_回退提示]]、[[概念_子查询分解]]、[[概念_Rerank_重排序]]、[[概念_LLM重排序]]、[[概念_Contextual_Compression_上下文压缩]]、[[概念_RSE相关段落提取]]、RAG反馈机制、CCH块标题、[[概念_上下文增强检索]]
- 参考文献：arXiv:2407.01219, arXiv:2410.12837

---
> 📎 **物理文献**：[[raw/playbooks/RAG技巧与底层代码剖析.md]]