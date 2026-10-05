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
- wiki/sources/Context Engineering 完整指南：为什么管理上下文比堆大窗口更重要.md
updated: '2026-10-05'
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

## 影响因素与收益递减（Chroma 实证研究）

- **上下文长度与分布**：上下文长度超过训练时的常见长度，且信息密度不均匀分布；
- **收益递减的有限资源（Chroma 研究）**：Chroma 技术报告揭示，Context 是一种具有显著**收益递减（Diminishing Returns）**特性的有限资源。单纯用海量信息填满上下文窗口不仅无法带来线性能力增益，反而会导致显著的性能滑坡；
- **上下文膨胀退化**：随着 Token 数量持续增加，模型的输出可靠性快速下降，在触及硬性上下文限制之前就已经发生推理退化；
- **自然语言的模糊性**：冗余信息稀释关键信号，导致模型注意力被分散，难以捕捉关键线索。

## 预腐化阈值

Manus 实践中通常在 **128K-200K token** 之间，通过大量评估确定。当模型出现重复、推理变慢、质量下降等现象时即接近此阈值。

触发后依次执行：压缩（Compaction）→ 若增益不足再总结（Summarization）

## 解决策略

- 见 [[概念_上下文工程]] 核心操作（Write/Select/Compress/Isolate 与 Offload/Retrieve/Reduce/Isolate）
- 结合 [[概念_Long_Text_Reorder_长文本位置重排序]] 缓解长文本“迷失在中间（Lost in the Middle）”现象
- 采用 MIT 提出的 [[概念_RLM递归语言模型]] 架构，通过在外部 REPL 环境缓存上下文数据，并用工具进行 Peek/Grep/Partition 分治与递归调用，使模型在 10M+ 极端超长文本下避免上下文腐化。

## 来源

- [[Context_Engineering_LangChain_Manus_NotebookLM]]
- [[也许当前最好的上下文工程讲解_LangChain联合Manus]]
- [[浅谈上下文工程_Claude_Code_Manus_Kiro]]
- [[2026-06-24_Recursive-language-models_19ef72]]
- [[sources/Context Engineering 完整指南：为什么管理上下文比堆大窗口更重要]]