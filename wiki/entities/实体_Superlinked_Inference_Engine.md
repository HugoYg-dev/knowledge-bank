---
type: "entity"
tags: ["Infra/serving", "LLM/inference"]
summary: "Superlinked Inference Engine（SIE）是面向多模型流水线的 Apache 2.0 开源推理服务引擎，通过单进程共享 GPU、LRU 模型置换与统一 API 将自托管推理成本降低约 4 倍。"
sources:
  - "wiki/sources/2026-08-05_How-to-serve-5-models-on-one-GPU_19fd38.md"
  - "wiki/sources/2026-08-31_Researchers-built-a-new-AI-inference-engine_1a0580f9aa7f67f1.md"
updated: "2026-09-09"
---

# 实体：Superlinked Inference Engine (SIE)

## 简介

Superlinked Inference Engine（SIE）是由 Superlinked 团队开源的统一 AI 推理服务引擎（遵循 Apache 2.0 协议，仓库：`superlinked/sie`）。针对典型 AI Agent 链路中同时串联嵌入（Embedder）、重排（Reranker）、实体抽取（Extractor）与生成（LLM）等 4-5 个模型的异构协同痛点，SIE 通过单进程统一管理与显存时分复用，将完整 Agentic Pipeline 整合至单张 GPU 上运行，使自托管服务成本降低约 4 倍。

## 核心架构与功能机制

- **四大统一调用原语**：提供兼容 OpenAI API 的统一服务接口：
  - `encode()`：多模态向量与文本 Embedding 抽取
  - `score()`：相关性评分与 Cross-Encoder Rerank
  - `extract()`：实体抽取与信息结构化 Span 解析
  - `generate()`：开源小规模 LLM 的文本生成推理
- **动态按需加载与 LRU 显存置换**：模型在首次收到请求时才按需载入显存；当 GPU 显存饱和时，按照最近最少使用（LRU）策略自动淘汰冷模型，解决传统架构每个服务独立独占静态显存 Slice 导致的空转浪费。
- **跨负载感知与调度优化**：支持共享队列与基于预估计算成本的多请求批处理，调度层拥有跨模型全局显存与计算负载视图。
- **生态集成与部署弹性**：支持从单机笔记本到多节点 Kubernetes 集群的弹性部署，开箱即用支持 85+ 种模型架构，并原生集成 Qdrant、Weaviate、Chroma、LanceDB、LangChain 与 LlamaIndex 等向量库及 Agent 编排框架。

## 关联

- [[entities/实体_vLLM|实体_vLLM]]：单大模型高性能 Serving 引擎与多小模型协调服务层的对比选型。
- [[concepts/概念_连续批处理|概念_连续批处理]]：推理服务中的动态调度与请求批处理机制。
- [[concepts/概念_KV_Cache|概念_KV_Cache]]：大模型推理时的显存占用与管理。

## 来源

- [[wiki/sources/2026-08-05_How-to-serve-5-models-on-one-GPU_19fd38|wiki/sources/2026-08-05_How-to-serve-5-models-on-one-GPU_19fd38]]
- [[wiki/sources/2026-08-31_Researchers-built-a-new-AI-inference-engine_1a0580f9aa7f67f1|wiki/sources/2026-08-31_Researchers-built-a-new-AI-inference-engine_1a0580f9aa7f67f1]]
