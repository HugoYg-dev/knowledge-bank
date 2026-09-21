---
type: source
tags:
- RAG/retrieval
- RAG/chunking
summary: 文本切分系列第1篇，提出五层级切分框架并介绍最基础的字符切分（Level 1），涵盖 LangChain 和 LlamaIndex 实现。
sources:
- raw/articles/RAG文本切分的五个层次1：字符切分基础(实战).md
updated: '2026-07-01'
---
# RAG文本切分的五个层次1：字符切分基础

> URL：https://mp.weixin.qq.com/s/SnfhuQyRmjQxDP3n5n3Upw
> Cubox 高亮：无

## 摘要

文本切分系列第 1 篇。提出将文本切分划分为五个层级，并介绍最基础的字符切分（Character Splitting）概念与实战。字符切分简单容易但非常死板，不考虑文本结构，不建议实际使用，仅作为理解基础。

## 五个层级框架

- **Level 1: Character Splitting** — 简单的字符长度切分
- **Level 2: Recursive Character Text Splitting** — 通过分隔符切分，然后递归合并
- **Level 3: Document Specific Splitting** — 针对不同文档格式切分（PDF、Python、Markdown）
- **Level 4: Semantic Splitting** — 语义切分
- **Level 5: Agentic Splitting** — 使用代理实现自动切分

## 核心内容

### 字符切分概念
- 将文本简单分成 n 个字符大小的块，不考虑内容或形式
- 优点：简单容易；缺点：死板，未考虑文本结构
- **Chunk Size（块大小）**：块中包含的字符数量
- **Chunk Overlap（块重叠）**：为避免重要信息被切开，连续块之间重叠的字符大小

### LangChain 实现
- `CharacterTextSplitter`，参数：`chunk_size`、`chunk_overlap`、`separator`、`strip_whitespace`
- 加入 overlap 后，重叠部分会在相邻片段中重复出现
- 加入 separator 后，先用分隔符切分成小块，再用长度切割

### LLama-Index 实现
- `SentenceSplitter`（参数 `chunk_size`、`chunk_overlap`）+ `SimpleDirectoryReader` 加载文档
- `get_nodes_from_documents` 得到 nodes，包含切分文本及额外相关内容

## 关联

- 概念：[[概念_文本切分五层级]]、[[概念_字符切分]]、[[概念_Chunk_Size_分块大小与重叠]]
- 实体：[[实体_LangChain]]、[[实体_LlamaIndex]]
- 系列下一篇：[[RAG文本切分_递归字符切分]]

---
> 📎 **物理文献**：[[raw/articles/RAG文本切分的五个层次1：字符切分基础(实战).md]]