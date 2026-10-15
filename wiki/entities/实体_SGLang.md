---
type: entity
tags:
  - Infra/serving
  - LLM/inference
summary: "SGLang 是由 LMSYS 团队开源的高性能大语言模型推理和服务引擎，以 RadixAttention 树状前缀缓存、高效的调度运行时与灵活的结构化生成见长。"
sources:
  - wiki/sources/腾讯15年资深后台工程师_转战大模型推理的抉择.md
updated: "2026-10-15"
---

# 实体：SGLang

## 简介

SGLang 是一个开源的高性能大语言模型（LLM）推理和服务框架（由 LMSYS 组织与 UC Berkeley 等团队主导开发）。其通过编程语言层面的前端控制流优化与运行时（Runtime）的高性能后端协同，为大模型推理提供超高吞吐与低延迟支持。

与 [[entities/实体_vLLM|vLLM]] 类似，SGLang 是当前工业界与开源社区最主流的 LLM 推理加速引擎之一。

## 核心技术特性

- **RadixAttention（基数树前缀缓存）**：通过 Radix Tree（基数树）在运行时动态管理 KV Cache，实现跨请求、跨会话以及多轮对话/多分支生成中的前缀缓存自动化命中与复用，显著减少 Prefill 阶段的冗余计算。
- **高效的调度与执行架构**：具备原生 Overlap Scheduler（重叠调度器）、Chunked Prefill、连续批处理（Continuous Batching）以及张量并行（TP）等多种并行调度能力。
- **结构化生成（Structured Output）**：在前端编译期与后端解码期深度结合语法约束（Regex / BNF），极大降低了结构化 JSON 输出和特定格式约束时的解码开销。

## 在本库来源中的角色与实践

- [原文陈述] 在《[[wiki/sources/腾讯15年资深后台工程师_转战大模型推理的抉择|腾讯15年资深后台工程师，转战大模型推理的抉择]]》中，作者吴银光（腾讯资深搜索后台工程师）在转战大模型推理工程时深入研读 SGLang 源码，并指出 `mini-sglang` 是深入理解大模型推理关键底层机制的优秀入门项目。
- [原文陈述] 作者在 SGLang 框架上针对搜广推场景落地了高性能的 **Beam Search（束搜索）** 实现，突破了多路径 KV Cache 复用、大 Beam 宽度大词表的高并发剪枝、业务合规 DocID 约束解码等技术瓶颈，取得了业界 SOTA 性能；该分支经过 SGLang 官方开发者重构后，最终成功合入官方主分支并在 **SGLang v0.5.19** 版本中发布。

## 关联概念

- [[concepts/概念_LLM推理两阶段]]
- [[concepts/概念_KV_Cache_键值缓存]]
- [[concepts/概念_连续批处理]]
- [[concepts/概念_FlashAttention_快速注意力]]

## 关联实体

- [[entities/实体_vLLM]]
