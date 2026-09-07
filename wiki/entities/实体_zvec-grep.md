---
type: "entity"
tags:
  - "AI-Agent/coding"
  - "AI-Agent/tool-calling"
  - "RAG/retrieval"
summary: "zvec-grep（zg）是由阿里 Zvec 团队开源的 local-first 代码搜索基础设施，结合 BM25 词法检索、向量语义检索与 RRF 排名融合，为人类开发者和 AI Coding Agent 提供高效的上下文获取层"
sources:
  - "wiki/sources/阿里千问 zvec-grep：让代码搜索变成 AI Agent 基础设施.md"
updated: "2026-09-07"
---

# 实体：zvec-grep (zg)

## 概述

**zvec-grep**（CLI 命令为 `zg`）是由阿里 Zvec 团队开源的本地优先（Local-First）代码与文档检索基础设施。其官方定位为 *“local-first search infrastructure for humans and agents”*。

zg 旨在解决 Coding Agent 在进入大型代码库后面临的 **上下文获取（Context Acquisition）** 瓶颈：当任务输入由确定性的函数名和 Symbol 转向自然语言业务意图、实现意图或系统行为时，传统的精确文本扫描（如 `grep`、`ripgrep`）由于缺乏词汇重叠（Lexical Overlap）容易引发高成本的试探死循环。zg 在保留底层精确搜索能力的同时，在前端构建了结合 BM25、向量语义检索与 RRF 融合的统一检索层。

---

## 核心架构与技术特性

### 1. 本地优先与轻量运行时（Local-First Architecture）
- **数据隐私与持久化**：代码文件、Query 与检索索引全程保留在本地 Workspace，底层基于嵌入式 Zvec 向量检索引擎，不依赖外部独立向量数据库服务。
- **多模型运行时支持**：
  - **Model2Vec（无 GPU 依赖）**：推荐采用 `local/potion-code-16m-v2` 等轻量静态查找表模型（最大 1024 Token，输出 256 维向量），极速构建索引，无需深度网络推理。
  - **ONNX Runtime**：支持 Jina-code、MiniLM、E5 等模型，支持 CPU、Metal、CUDA 加速。
  - **GGUF Runtime**：支持本地运行更强语义能力的 `qwen3-embedding-0.6b`（最大 8192 Token，输出 1024 维向量）。
  - **远程 Embedding 支持**：支持云端模型接入，但对 Provider 凭证与代码数据外发进行严格权限隔离。

### 2. 细粒度结构化抽取（Extraction Path）
- 向量化作用于局部抽取的 Fragment，而非对整个文件或整个仓库整体编码。
- 对能够结构化解析的代码，抽取并保留 Symbol、函数签名（Signature）、路径面包屑（Breadcrumb）与源码定位（Source Location）；对 Markdown 按章节层级组织，最大化提升局域信息检索纯度。

### 3. 双路召回与 RRF 混合检索（Hybrid Retrieval）
代码具有“自然语言意图”与“精确标识符”并存的特质：
- **BM25 词法检索**：提供带有词频（TF-IDF）相关性排序的精确文本匹配，对真实类名（如 `AuthService`）提供强保真度。
- **Vector 语义检索**：基于 Cosine Similarity 计算 Query 与局部 Fragment 的空间几何相似度，召回同义异构的业务实现（如由“恢复偏好”命中 `hydratePreferences`）。
- **RRF 排序融合**：通过 Reciprocal Rank Fusion 从排名维度无量纲合并两套结果列表，使同时具备语义相关性与精准符号匹配的代码段脱颖而出。

### 4. 源码反向映射与 Agent 工具协同
- 检索命中的 Fragment 包含完整的文件路径与行列坐标。
- Agent 在通过语义发现（Semantic Discovery）锁定候选符号后，即可无缝调用 `ripgrep` 扫描定义与调用链，切换回确定性验证与阅读，大幅缩短 Tool Calls 轮次并降低 Token 消耗。

### 5. 统一生态接口（CLI & MCP）
- 提供终端交互命令 `zg` 供开发者直接使用。
- 提供符合 MCP（Model Context Protocol）规范的接口，便于 [[entities/实体_Claude_Code|Claude Code]]、Codex、Cursor、Qwen Code、Qoder 等主流 Agent 环境作为基础设施接入。

---

## 来源

- [[wiki/sources/阿里千问 zvec-grep：让代码搜索变成 AI Agent 基础设施.md]]
