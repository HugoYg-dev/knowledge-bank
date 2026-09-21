---
type: concept
tags:
- RAG/retrieval
- RAG/chunking
summary: 在递归字符切分基础上，将长度计算从字符个数改为 token 个数，使切分结果与语言模型实际处理方式对齐。
sources:
- wiki/sources/RAG文本切分_token优化.md
updated: '2026-07-06'
---

# 概念_Token切分优化


## 定义

在递归字符切分基础上，将长度计算从字符个数改为 token 个数，使切分结果与语言模型实际处理方式对齐。

## 优势

1. 保证切分后文本片段不超过模型最大长度
2. 保证送入模型的 token 数相当，并行节约资源
3. 有效预估送入大模型的片段长度，便于系统内资源调整

## 实现方式

- **tiktoken（OpenAI）**：`from_tiktoken_encoder(encoding_name/model_name, chunk_size, chunk_overlap)`
  - 发现：OpenAI tokenizer 中一个中文汉字消耗多个 token，成本高
- **SentenceTransformers**：`SentenceTransformersTokenTextSplitter(tokens_per_chunk, chunk_overlap, model_name)`
  - 对中文支持好的模型（如 bge-m3），token 压缩比例显著提升
- **自定义 HuggingFace tokenizer**：`RecursiveCharacterTextSplitter.from_huggingface_tokenizer(tokenizer, chunk_size, chunk_overlap, separators, keep_separator)`
  - 使用自己的向量模型时，切分也用对应的 tokenizer

## 关联

- 上层框架：[[概念_文本切分五层级]]
- 相关概念：[[概念_递归字符切分]]、[[概念_Chunk_Size_分块大小与重叠]]
- 来源：[[RAG文本切分_token优化]]