---
type: source
tags:
- LLM/arch
- RAG/retrieval
- AI-Agent/prompt-engineering
summary: OpenAI DevDay 2023 演讲总结：LLM 应用性能优化路线——Prompt Engineering → RAG → Fine-tuning，两轴(Context
  Optimization / LLM Optimization)思考框架，附 RAG 45%→98% 案例与 Fine-tuning+RAG 结合 Text-to-SQL
  案例
sources:
- raw/articles/Prompt Engineering, Finetune, RAG？：OpenA....md
updated: '2026-07-01'
---
# OpenAI_LLM应用最佳实践

## 摘要

基于 OpenAI DevDay 2023 演讲（John Allard & Colin Jarvis），总结 LLM 应用从 Demo 到生产的优化路线。核心观点：不是 Prompt Engineering → RAG → Fine-tuning 的线性流程，而是沿两个轴并行迭代。

## 两轴优化框架

- **Context Optimization（上下文优化）**：模型缺知识时，用 RAG 注入外部知识
- **LLM Optimization（模型优化）**：模型输出不正确时，用 Fine-tuning 改善格式/风格/遵循指令

## Prompt Engineering

- 清晰指令、任务拆分、给 LLM 思考时间（think step by step）、参考文本、外部工具
- 适合：早期测试、确定 baseline
- 不适合：引入新信息、可靠复制复杂样式、最小化 Token 使用

## RAG

- 集成外部知识库（私有数据、特定领域数据）通过 ICL 解决幻觉/知识不足
- 适合：注入/更新知识、通过控制内容减少幻觉
- 不适合：嵌入大范围领域理解、教模型新语言/格式、减少 Token
- **RAG 优化案例（45% → 98% Accuracy）**：
  - 45% Baseline（简单 Cosine 相似度）
  - 65%：Chunking 方案（实验选择最优 Chunk 大小）
  - 85%：Re-Ranking + Classification（领域分类缩小检索范围）
  - 98%：Prompt Engineering + 工具使用 + Query 扩展
  - HyDE 尝试无效未采用；微调 Embedding 代价高放弃

## Fine-tuning

- 提升特定领域/任务性能、降低 Token 数量（蒸馏大模型到小模型）
- 适合：激发模型已有知识、自定义结构/语气、教复杂指令
- 不适合：注入新知识到 base 模型、快速在新场景验证
- **失败案例**：140K Slack 聊天记录微调 GPT-3.5，数据集偏离需求，产出偏向聊天场景
- **最佳实践**：从 Prompt Engineering 开始 → 建立 baseline → 小高质量数据集 → Active Learning 迭代

## Fine-tuning + RAG 结合

- Fine-tuning 使模型遵循格式/风格，降低 Prompt 复杂度，为 RAG 留更大空间
- RAG 注入知识，增强短期记忆
- **Text-to-SQL 案例**：
  - Baseline 69%（Prompt Engineering）
  - RAG 优化 → 80%
  - Fine-tuning + Reduced Schema → 81.7%
  - Fine-tuning + RAG → 83.5%（达标 84%）

## 评估体系

- 自动评估：F1/召回/精确率、模型评委（GPT-4/3.5）、A/B Test
- 人工评估：流畅度、相关性、新颖性
- RAG 专项评估（[[实体_RAGAS|Ragas]]）：忠诚度、答案相关性、上下文精度、上下文召回

## 短期 vs 长期记忆

- 短期记忆：模型处理单一输入时的临时信息 → RAG 增强
- 长期记忆：训练数据学到的知识 → Fine-tuning 增强

## 关联

- 相关概念：[[概念_RAG基础流程]]、[[概念_HyDE]]、[[概念_查询重写]]、[[概念_重排序Rerank]]、[[概念_Prompt工程方法]]、[[概念_RAG评估框架RAGAS]]、[[概念_LLM应用优化两轴]]
- 相关实体：[[实体_RAGAS]]

---
> 📎 **物理文献**：[[raw/articles/Prompt Engineering, Finetune, RAG？：OpenA....md]]

- 关联实体：[[entities/实体_OpenAI|OpenAI]]
