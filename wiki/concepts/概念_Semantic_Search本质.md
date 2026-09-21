---
type: concept
tags:
- RAG/retrieval
- RAG/embedding
summary: 语义搜索（Semantic Search）的核心是 metric embedding——将文件映射到一个高维测度空间（metric space），使向量间距离能有意义地反映文件之间的语义关系。其本质是"document
  as index"（文件本身作为索引）。
sources:
- wiki/sources/RAG系统设计_语义搜索与KG驱动选型.md
updated: '2026-07-06'
---

# 概念_Semantic_Search本质


## 定义

语义搜索（Semantic Search）的核心是 metric embedding——将文件映射到一个高维测度空间（metric space），使向量间距离能有意义地反映文件之间的语义关系。其本质是"document as index"（文件本身作为索引）。

## 与传统检索的区别

- 传统检索依赖预设索引，前提是用户明确知道自己需要什么
- 语义搜索直接将文件作为索引，通过 embedding 与查询对比，在不知道具体需要哪个文件的情况下仍能找到最相关文件

## 关键特性：无结构即灵活

- Semantic Search 本身缺乏明确数据结构，只是一堆向量的集合（"无为而无不为"）
- 正因没有内在数据结构，反而可以为其赋予任何合适的数据结构
- RAG 系统设计的关键之一：为 Semantic Search 提供贴近数据天然结构的结构（树状/分层/Context Enrichment 等）

## 测度空间条件

度量距离函数需满足四个条件：自身距离为0、不同点距离大于0、对称性、三角不等式。现代语义搜索不一定局限于测度空间（如常用的余弦距离即非测度距离）。

## 关联

- 相关概念：[[概念_Embedding与向量检索]]、[[概念_Multi_Vector_多向量检索]]、距离函数选择、[[概念_向量相似度度量]]
- 来源：[[RAG系统设计_语义搜索与KG驱动选型]]