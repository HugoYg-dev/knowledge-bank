---
type: concept
tags:
- RAG/retrieval
summary: '长文本重排序（Long-text Reorder / Lost in the Middle Reorder）是一种检索后处理策略。基于论文 "Lost
  in the Middle: How Language Models Use Long Contexts" 的发现：大模型更容易记忆开头和结尾的文档...'
sources:
- wiki/sources/RAG_12痛点与解决方案.md
- wiki/sources/RAG高级优化_检索后处理.md
updated: '2026-09-21'
aliases:
- Long-text Reorder
- Lost in the Middle Reorder
- 长文本重排序
- 位置重排序
- 概念_Long-text_Reorder
---

# 概念_Long_Text_Reorder_长文本位置重排序


## 定义

长文本重排序（Long-text Reorder / Lost in the Middle Reorder）是一种检索后处理策略。基于论文 "Lost in the Middle: How Language Models Use Long Contexts" 的发现：大模型更容易记忆开头和结尾的文档，对中间部分记忆能力不强。

## 策略

将召回文档按相关性重排序：更相关的文档放在开头和结尾，不太相关的放在中间位置。

## 实现

LangChain `_litm_reordering` 算法：
1. 反转文档列表（使原排名靠后的文档在前）
2. 遍历：奇数索引追加到末尾，偶数索引插入开头
3. 结果：最相关文档交替分布在序列两端

## 关联

- 相关概念：[[概念_检索后处理]]、[[概念_Contextual_Compression_上下文压缩]]、[[概念_Prompt_Compression_提示词压缩]]
- 来源：[[RAG高级优化_检索后处理]]、[[RAG_12痛点与解决方案]]