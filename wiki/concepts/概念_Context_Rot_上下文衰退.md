---
type: concept
tags:
- AI-Agent/context-engineering
summary: 随着Agent运行过程中上下文长度持续增长，模型性能在达到硬性上下文限制之前就已显著下降的现象。
sources:
- wiki/sources/Context_Engineering_LangChain_Manus_NotebookLM.md
- wiki/sources/Manus创始人手把手拆解上下文工程.md
- wiki/sources/也许当前最好的上下文工程讲解_LangChain联合Manus.md
- wiki/sources/浅谈上下文工程_Claude_Code_Manus_Kiro.md
- wiki/sources/2026-06-24_Recursive-language-models_19ef72.md
updated: '2026-09-21'
aliases:
- Context Rot
- 上下文衰退
- 上下文腐烂
- 概念_Context_Rot
---

# 概念：Context Rot（上下文腐化）

## 定义

随着Agent运行过程中上下文长度持续增长，模型性能在达到硬性上下文限制**之前**就已显著下降的现象。

## 表现

- 产生幻觉后被持续带偏
- 模糊性导致信息冲突，模型行为不可预测
- 关键信息被稀释，注意力被分散
- 大量重复文本导致"行动瘫痪"

## 影响因素

- 上下文长度超过训练时的常见长度
- 信息密度不均匀分布
- 自然语言的模糊性

## 预腐化阈值

Manus 实践中通常在 **128K-200K token** 之间，通过大量评估确定。当模型出现重复、推理变慢、质量下降等现象时即接近此阈值。

触发后依次执行：压缩（Compaction）→ 若增益不足再总结（Summarization）

## 解决策略

- 见 [[概念_上下文工程]] 四类操作（Offload/Retrieve/Reduce/Isolate）
- 采用 MIT 提出的 [[概念_RLM递归语言模型]] 架构，通过在外部 REPL 环境缓存上下文数据，并用工具进行 Peek/Grep/Partition 分治与递归调用，使模型在 10M+ 极端超长文本下避免上下文腐化。

## 来源

- [[Context_Engineering_LangChain_Manus_NotebookLM]]
- [[也许当前最好的上下文工程讲解_LangChain联合Manus]]
- [[浅谈上下文工程_Claude_Code_Manus_Kiro]]
- [[2026-06-24_Recursive-language-models_19ef72]]