---
type: source
tags:
- RAG/retrieval
- RAG/chunking
summary: 文本切分五层级中针对 Markdown 的第三层级（Document Specific Splitting）实践，介绍如何借助 LangChain
  MarkdownHeaderTextSplitter 按标题进行有效切分。
sources:
- raw/articles/RAG文本切分LV3：轻松定制Markdown切分.md
updated: '2026-07-01'
url: https://mp.weixin.qq.com/s?__biz=Mzk0NTcyNTMzNw==&mid=2247484120&idx=1&sn=51fdd215151fe9be2d0ab8290eed6a1e
---
# RAG文本切分 LV3：轻松定制 Markdown 切分

## 摘要

文本切分五层级中 Level 3（Document Specific Splitting）的 Markdown 实践。介绍如何借助 LangChain `MarkdownHeaderTextSplitter` 按标题对 Markdown 文档进行有效切分。

## 核心内容

### 文本切分五层级回顾

- Level 1: Character Splitting — 简单字符长度切分
- Level 2: Recursive Character Text Splitting — 分隔符切分后递归合并
- **Level 3: Document Specific Splitting — 针对不同文档格式切分（PDF、Python、Markdown）** ← 本文
- Level 4: Semantic Splitting — 语义切分
- Level 5: Agentic Splitting — 使用代理实现自动切分

### 基本思路

分块旨在将共同上下文的文本放在一起，应尊重文档自身结构。Markdown 文件按标题组织，在特定标题组中创建块是直观想法。使用 `MarkdownHeaderTextSplitter` 按指定的标题集拆分。

安装：`pip install langchain-text-splitters`

### 切分实现

**指定要拆分的标题：**
```python
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on)
md_header_splits = markdown_splitter.split_text(markdown_document)
```
切分后内容按标题分组，标题信息存入每个 Document 的 metadata。

**保留标题：** 默认从输出块内容中剥离被分割的标头；设置 `strip_headers=False` 可将标题保留到内容中。

**按行返回：** 默认按 `headers_to_split_on` 聚合行；设置 `return_each_line=True` 使一行成为一条独立 Document。

### 限制块大小

在每个 Markdown 标题组中再应用任意文本分割器（如 `RecursiveCharacterTextSplitter`）进一步控制块大小：
```python
# 先按标题切
md_header_splits = MarkdownHeaderTextSplitter(headers_to_split_on, strip_headers=False).split_text(...)
# 再按字符级切（chunk_size=250, chunk_overlap=30）
splits = RecursiveCharacterTextSplitter(chunk_size, chunk_overlap).split_documents(md_header_splits)
```

## 关联

- 概念：[[概念_文档结构切分]]、Markdown标题切分、[[概念_文本切分五层级]]、[[概念_递归字符切分]]
- 实体：[[实体_LangChain]]
- 同系列：[[RAG文本切分_JSON文档切分]]、[[RAG文本切分_语义切分]]

---
> 📎 **物理文献**：[[raw/articles/RAG文本切分LV3：轻松定制Markdown切分.md]]