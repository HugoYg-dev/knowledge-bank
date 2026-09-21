---
type: source
tags:
- AI-Agent/context-engineering
summary: 介绍由MIT提出的递归语言模型（RLM，Recursive Language Models）架构，该架构通过在Python REPL环境中缓存上下文数据，并让模型使用工具进行Peek、Regex过滤和Partition分治，实现自上而下的递归子调用，从而有效解决Context
  Rot问题，保证超长文本性能不衰减。
sources:
- raw/articles/2026-06-24_Recursive-language-models_19ef72.md
updated: '2026-08-04'
---

# 来源：Recursive language models

## 来源信息
- **主题**：Loop Engineering, Clearly Explained!
- **作者**：Daily Dose of DS (avi@dailydoseofds.com)
- **日期**：2026-06-24
- **原始文献**：[[raw/articles/2026-06-24_Recursive-language-models_19ef72.md]]

## 核心要点
1. **Context Rot（上下文衰减）问题**：即便在模型的最大上下文窗口内，随着对话或上下文长度的增长，LLM 召回和推理的能力也会显著下降，这就是 [[concepts/概念_Context_Rot_上下文衰退|Context Rot]] 现象。
2. **RLM（递归语言模型）架构**：MIT 研究者提出将数据与指令解耦。Context 不直接输入 LLM，而是缓存在 Python REPL 变量中。
3. **工具化上下文探索**：LLM 无法直接看到全部 Context，但可以通过工具在 Python 沙箱中执行 `Peek`（预览）、`Grep`（正则/关键词过滤，例如将 5000 级降为 50 级）和 `Partition`（切分）操作。
4. **自上而下的分治（Recursive Calls）**：模型对切分后的子块发起递归子调用，解决子问题后将结果返回给父 LLM，使其自身的上下文始终保持在极小规模。
5. **性价比与长文本优势**：在 10M+ 的超长文本测试中，RLM 的性能没有衰减，且使用小模型（如 GPT-5-mini）的 RLM 能在长文本基准上超越大模型（如 GPT-5），成本更低。
6. **工程共鸣**：这种将上下文视为可编程探索数据的方法，与现代 agentic 编码工具（如 Claude Code）按需读取 and 过滤代码库的运作方式高度一致。

## 关键引文
> "In an RLM, the context is stored separately as a variable in a Python REPL environment. The model never sees all of it directly."
> "Traditional LLMs treat context as a black box to process all at once. RLMs treat context as data to be programmatically explored."

## 联动概念
- [[concepts/概念_RLM递归语言模型|概念：RLM递归语言模型]]
- [[concepts/概念_Context_Rot_上下文衰退|概念：Context Rot]]

---
> 📎 **物理文献**：[[raw/articles/2026-06-24_Recursive-language-models_19ef72.md]]
