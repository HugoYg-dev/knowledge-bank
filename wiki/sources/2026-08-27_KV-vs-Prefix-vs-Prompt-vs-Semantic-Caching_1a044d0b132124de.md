---
type: "source"
tags:
  - "Infra/AI"
  - "LLM/inference"
summary: "系统横向解构 LLM 技术栈四种常被混淆的缓存机制（KV Cache、Prefix Caching、Prompt Caching、Semantic Caching）所存储的底层对象、正确性影响、Prefix Caching 链式哈希原理与常见失效陷阱"
sources:
  - "raw/articles/2026-08-27_KV-vs-Prefix-vs-Prompt-vs-Semantic-Caching_1a044d0b132124de.md"
updated: "2026-09-09"
---

# 来源摘要：KV vs Prefix vs Prompt vs Semantic Caching

## 来源信息

- **原文标题**：KV vs Prefix vs Prompt vs Semantic Caching
- **通讯来源**：Daily Dose of DS
- **原邮件主题**：KV vs Prefix vs Prompt vs Semantic Caching
- **发送作者**：Daily Dose of DS (Avi Chawla) `<avi@dailydoseofds.com>`
- **发布日期**：2026-08-27
- **邮件/文章标识**：`1a044d0b132124de:2`

---

## 核心要点（Executive Summary）

1. [原文陈述] **四种缓存存储对象的本质区别**：
   - **KV Cache**：单个请求内部为每个 Prompt/生成 Token 存储的多层注意力 Key/Value 张量；
   - **Prefix Caching**：服务引擎端（如 vLLM）跨请求复用的 KV 张量块，以 Token ID 构成的父子哈希链（Hash Chain）为键；
   - **Prompt Caching**：云服务商（如 Anthropic、OpenAI）提供的托管计费版前缀复用，采用差异化费率（如读取 0.1x 基础输入价，写入 1.25x 基础输入价）；
   - **Semantic Caching**：应用层对外置存储的完整回答文本字符串，以 Prompt Embedding 的余弦相似度（Cosine Similarity）为键。
2. [原文陈述] **正确性中立（Correctness-Neutral）vs 模糊匹配置信风险**：前三者属于精确匹配（Exact-match），完全保证输出正确性，Cache Miss 仅带来成本和延迟开销；而语义缓存（Semantic Caching）属于模糊近似匹配（Fuzzy-match），一旦误中可能以 HTTP 200 返回完全错误的过时或违背意图的回答。
3. [原文陈述] **Prefix Caching 块哈希链机制**：以 vLLM 默认 16 Tokens 块为例，当前块哈希 = Hash(父块哈希 + 当前块内 Token IDs)。查询沿哈希链遍历直至遇到首个 Miss，未命中之后的所有 Tokens 全部重新 Prefill。因此块大小是关键权衡：大块减少查找开销并改善内存局部性，小块减少尾部丢弃浪费并提升细粒度共享率。
4. [原文陈述] **RAG 场景下的 Prefix Caching 失效痛点**：RAG Prompt 结构通常为 `System -> Retrieved Chunks -> User Query`。检索返回的文档块在不同请求之间顺序变动，即使检索到的内容完全一致，因出现顺序不同会导致整条哈希链彻底失效。
5. [原文陈述] **语义缓存的固有缺陷**：在向量空间中，否定句与肯定句的 Embedding 距离极近；或者共享相同句子模板仅修改单项数值的两个 Prompt 也会得出接近 1.0 的相似度，极易引发严重业务事故。
6. [原文陈述] **生产环境五大隐蔽失效模式（Silent Cache Invalidation）**：
   - **前缀插入动态变量**：在 System Prompt 头部注入时间戳、用户 ID 或 Request ID 会导致后续所有块缓存彻底作废；
   - **Tool Schema 重排序**：工具定义通常位于上下文前部，重新排序会导致全量缓存报废；
   - **渲染配置切换**：开关 Web Search、Citations、思考模式配置（Thinking Config）或更改 `tool_choice` 会改写渲染提示词导致下游断裂；
   - **历史文本压缩重写**：修改历史摘要会导致前缀哈希断裂全额按 Cold Token 计费；
   - **跨模型路由**：切换到更便宜的模型会导致缓存无法跨模型复用，被迫全量冷启动。

---

## 关联概念与实体

- **关联概念**：
  - [[concepts/概念_KV_Cache|概念_KV_Cache]]：自回归自注意力张量缓存核心原理与显存特征。
  - [[concepts/概念_上下文工程|概念_上下文工程]]：前缀稳定、追加式交互与断点设计规范。
  - [[concepts/概念_解耦式KV缓存与LMCache|概念_解耦式KV缓存与LMCache]]：跨请求跨位置的缓存块解耦复用。
- **关联实体**：
  - [[entities/实体_vLLM|实体_vLLM]]：Prefix Caching 块哈希链与内存淘汰算法的开源参考实现。
  - [[entities/实体_Anthropic|实体_Anthropic]]：Prompt Caching 差异化计费规范与 20 块回溯窗口设计者。

---

> 📎 **物理文献**：[[raw/articles/2026-08-27_KV-vs-Prefix-vs-Prompt-vs-Semantic-Caching_1a044d0b132124de.md]]
