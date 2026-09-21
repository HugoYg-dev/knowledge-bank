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
updated: '2026-09-07'
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

## 关联

- 相关概念：[[概念_Embedding与向量检索]]、[[概念_向量数据库]]、RAG四大基础范式、RAG五类提升方法、[[概念_LLM应用优化两轴]]
- 进阶技巧：[[概念_Query_Translation_查询改写与翻译]]、[[概念_RAG_Routing_检索智能路由]]、[[概念_Query_Construction_查询构建]]、[[概念_Multi_Representation_Indexing_多表征索引]]
- 来源：[[RAG基础_索引检索生成]]、RAG综述_北大AIGC2024、[[OpenAI_LLM应用最佳实践]]