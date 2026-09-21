---
type: source
tags:
- RAG/retrieval
summary: 12 个 RAG 痛点及对应解决方案：涵盖内容缺失、排名遗漏、上下文不足、未提取、格式错误、粒度不当、不完整、数据摄取扩展性、结构化数据QA、复杂PDF提取、后备模型、LLM安全
sources:
- raw/articles/12 RAG 痛点和拟议解决方案.md
updated: '2026-07-01'
---
# RAG_12痛点与解决方案

## 摘要

基于论文 "Seven Failure Points When Engineering a RAG System" 扩展而来，列出 12 个 RAG 开发痛点及对应解决方案。前 7 个源自论文（内容缺失、排名遗漏、上下文不足、未提取、格式错误、粒度不当、不完整），后 5 个为作者实践补充（数据摄取扩展性、结构化数据 QA、复杂 PDF 提取、后备模型、LLM 安全）。

## 痛点与解决方案

### Pain Point 1：内容缺失（Missing Content）

- 问题：知识库中无答案时 RAG 给出似是而非的错误回答
- 方案：
  - 清洗数据（Garbage in, garbage out）
  - 改进 Prompt（如"不确定就说不知道"）

### Pain Point 2：排名遗漏（Missed Top Ranked）

- 问题：正确文档未进入 top-k 返回结果
- 方案：
  - 超参调优：chunk_size 和 similarity_top_k（LlamaIndex ParamTuner）
  - [[概念_Rerank_重排序|重排序]]：先检索 top-10 再用 CohereRerank 返回 top-2

### Pain Point 3：上下文不足（Not in Context）

- 问题：有答案的文档被检索到但未进入生成上下文（合并策略限制）
- 方案：
  - 调整检索策略（LlamaIndex 多种 retriever）
  - 微调嵌入模型（SentenceTransformers finetune）

### Pain Point 4：未提取（Not Extracted）

- 问题：上下文信息过多/噪声/矛盾导致无法提取正确答案
- 方案：
  - 清洗数据
  - Prompt 压缩（LongLLMLingua）
  - LongContextReorder（将重要文档置于首尾）

### Pain Point 5：格式错误（Wrong Format）

- 问题：LLM 忽略格式化指令
- 方案：
  - 改进 Prompt（明确格式、给例子）
  - Output Parsing（Guardrails / LangChain）
  - Pydantic Programs（LLM Text Completion / Function Calling）
  - OpenAI JSON Mode

### Pain Point 6：粒度不当（Incorrect Specificity）

- 问题：回答太笼统，缺乏细节
- 方案：
  - 高级检索策略：small-to-big retrieval、sentence window retrieval、recursive retrieval

### Pain Point 7：不完整（Incomplete）

- 问题：部分回答正确但遗漏细节，尤其比较类问题
- 方案：
  - 查询转换（Query Transformations）：Routing / Query-Rewriting / Sub-Questions / ReAct Agent Tool Selection
  - [[概念_HyDE_假设文档嵌入|HyDE]]：生成假设文档再检索

### Pain Point 8：数据摄取扩展性（Data Ingestion Scalability）

- 问题：大量数据导致性能瓶颈
- 方案：并行化摄取管道（IngestionPipeline num_workers）

### Pain Point 9：结构化数据 QA

- 问题：复杂/模糊查询下 text-to-SQL 不够灵活
- 方案：
  - Chain-of-Table Pack：链式表格操作逐步切片数据
  - Mix-Self-Consistency：文本推理 + 符号推理 + 多数投票

### Pain Point 10：复杂 PDF 提取

- 问题：嵌入式表格无法通过简单检索获取
- 方案：EmbeddedTablesUnstructuredRetrieverPack（Unstructured.io 解析 HTML 中嵌入表格 + 递归检索）

### Pain Point 11：后备模型（Fallback Models）

- 问题：主模型故障（如 rate limit）
- 方案：
  - Neutrino Router：预测模型路由到最佳 LLM
  - OpenRouter：统一 API + 自动 fallback

### Pain Point 12：LLM 安全

- 问题：prompt 注入、不安全输出、敏感信息泄露
- 方案：Llama Guard（基于 Llama 2-7B 的内容分类，输入+输出双重审核）

## 关联

- 相关概念：[[概念_Rerank_重排序]]、[[概念_HyDE_假设文档嵌入]]、[[概念_检索后处理]]、[[概念_Long_Text_Reorder_长文本位置重排序]]、[[概念_Contextual_Compression_上下文压缩]]、[[概念_Query_Translation_查询改写与翻译]]、[[概念_RAG基础流程]]、[[概念_Prompt_Compression_提示词压缩]]、[[概念_LLM重排序]]、[[概念_RAG_Routing_检索智能路由]]
- 实体：[[实体_LlamaIndex]]、[[实体_LangChain]]、[[实体_Cohere_Rerank]]
- 相关来源：[[RAG高级优化_检索后处理]]、[[RAG查询翻译_Query_Translation]]

---
> 📎 **物理文献**：[[raw/articles/12 RAG 痛点和拟议解决方案.md]]