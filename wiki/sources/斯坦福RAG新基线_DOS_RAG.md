---
type: source
tags:
- RAG/retrieval
summary: 斯坦福 2025 新论文提出 DOS RAG（Document's Original Structure RAG）：检索后按原文顺序排列片段而非按相关性排序，在多个长文档
  QA 基准上持平或超越 ReadAgent/RAPTOR 等复杂方案
sources:
- raw/articles/2025来自斯坦福的RAG新基线.md
updated: '2026-07-01'
---
# 斯坦福RAG新基线_DOS_RAG

## 摘要

斯坦福论文 "Stronger Baselines for Retrieval-Augmented Generation with Long-Context Language Models" 提出 DOS RAG，挑战当前复杂 RAG 架构的必要性。核心发现：在长文档 QA 场景下，简单的"检索 + 按原文顺序排列"方案可持平甚至超越 ReadAgent、RAPTOR 等多阶段复杂方案。

## [重点/高亮] DOS RAG 流程

用户高亮内容：

> 什么是 DOS RAG？它的流程简单到令人发指：
> 1. 检索：和传统 RAG 完全一样，使用向量检索等技术，找出与问题最相关的文本片段（Chunks）。
> 2. 排序：这是唯一的、也是最关键的区别。它放弃了按相关性得分排序，而是将检索到的片段，按照它们在原始文档中出现的先后顺序进行重新排列。
> 3. 生成：将这些按原文顺序排列的片段连同问题一起，输入给 LLM。

## 对决选手

### 复杂派
- **ReadAgent**：多次与 LLM 互动来提炼问题、检索信息
- **RAPTOR**：通过对文档聚类和摘要构建信息金字塔（[[概念_RAPTOR_递归树状检索索引]]）

### 简约派
- **全文基线（Full-Document）**：将源文档全部内容直接输入 LLM，性能理论上限
- **朴素 RAG**：检索相关片段，按相关性得分从高到低排序
- **DOS RAG**：检索相关片段，按原文顺序排列

## 实验结果

- 评测数据集：∞Bench、NarrativeQA、QuALITY
- 结论：在几乎所有 Token 预算和评测场景下，DOS RAG 持平甚至超越 ReadAgent 和 RAPTOR
- RAPTOR 在这些任务中甚至不及朴素 RAG

## DOS RAG 成功原因

1. **保留叙事流与逻辑链**：按原文顺序保持上下文连贯性，减轻 LLM 理解负担
2. **信息保真度最大化**：直接从原文提取，避免摘要/重组带来的信息损失
3. **检索与阅读最佳平衡**：检索过滤无关信息（大海捞针），保留原始顺序让 LLM 在自然语境中推理（迷失在上下文）

## 启示

### 对开发者
- 将 DOS RAG 作为第一个最强基准（KISS 原则）
- 任何新功能上线需回答："比 DOS RAG 好多少？"
- 实现简单、计算开销小、延迟低

### 对研究者
- 提高了 RAG 领域创新门槛
- 未来研究方向应转向：提高第一步检索召回率、让 LLM 更好利用按原序排列的上下文、RAG 与纯长上下文的混合模式

## 关联

- 相关概念：[[概念_DOS_RAG_动态操作空间检索]]、[[概念_RAPTOR_递归树状检索索引]]、[[概念_RAG基础流程]]

---
> 📎 **物理文献**：[[raw/articles/2025来自斯坦福的RAG新基线.md]]