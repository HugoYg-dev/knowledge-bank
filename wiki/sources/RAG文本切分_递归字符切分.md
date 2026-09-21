---
type: source
tags:
- RAG/retrieval
- RAG/chunking
summary: 文本切分系列第2篇，介绍 Level 2 递归字符文本分割（RecursiveCharacterTextSplitter）：先按分隔符切分再合并至指定长度，是实践中最常用的基础切分方案。
sources:
- raw/articles/RAG文本切分的五个层次2：递归字符分割(实战).md
updated: '2026-07-01'
---
# RAG文本切分_递归字符切分

> URL：https://mp.weixin.qq.com/s?__biz=Mzk0NTcyNTMzNw==&mid=2247483959&idx=1&sn=8805bfc48c02cc396042eed5ad5f440a
> Cubox 高亮：无

## 摘要

文本切分系列第 2 篇。介绍 Level 2 递归字符文本分割（Recursive Character Text Splitting），日常实践中最常采用的切分方案，也是其它高级方案的基础。

## 核心内容

### 为什么需要递归字符切分
- 按字符长度切分的问题：没有考虑文档结构，按固定数量字符分割，容易将文档随意切开
- 递归字符文本分割器：先指定一系列分隔符用于分割文档，然后将分割好的小块合并，达到指定长度
- 如果不知道选哪个切分器，这是一个不错的默认选择

### 默认分隔符
- LangChain 中默认分隔符列表：`["\n\n", "\n", " ", ""]`
- 拆分器首先寻找 `\n\n`（段落断行），段落被分割后查看块大小，太大则用下一个分隔符分割，依此类推

### 实现
- `RecursiveCharacterTextSplitter(chunk_size=65, chunk_overlap=0)`
- chunk_size 太小（如 65 个字符）切出来太零碎
- 放大 chunk_size（如 450）可以得到按段落自然切分的预期效果

### 关键发现
- 仅使用字符个数作为块内切分依据不理想
- 相同语义下中英文、数字等字符个数差别太大
- 需要进一步优化块内的切分和计数方案（引出 token 优化）

## 关联

- 概念：[[概念_文本切分五层级]]、[[概念_递归字符切分]]、[[概念_Chunk_Size_分块大小与重叠]]
- 实体：[[实体_LangChain]]
- 系列上一篇：[[RAG文本切分_字符切分]]
- 系列下一篇：[[RAG文本切分_token优化]]

---
> 📎 **物理文献**：[[raw/articles/RAG文本切分的五个层次2：递归字符分割(实战).md]]