---
type: entity
tags:
- Infra/AI
- LLM/inference
summary: vLLM 是开源 LLM 推理框架，支持 KV Cache、连续批处理（Continuous Batching）、PagedAttention 等核心优化，是当前主流高吞吐低延时推理引擎。
sources:
- wiki/sources/LLM后训练技术全景解读.md
- wiki/sources/MiniMax_vs_Kimi_注意力路线之争.md
- wiki/sources/R1复现认知与误区.md
- wiki/sources/Tongyi DeepResearch的技术报告探秘.md
- wiki/sources/入局AI_Infra系统设计与挑战.md
- wiki/sources/推测解码Speculative_Decoding综述.md
- wiki/sources/淘宝直播数字人_TTS语音合成技术.md
- wiki/sources/2026-08-05_How-to-serve-5-models-on-one-GPU_19fd38.md
- wiki/sources/2026-08-07_8-LLM-precision-formats_19fddf.md
updated: '2026-08-10'
---

# 实体：vLLM

## 简介

vLLM 是一个开源 LLM 推理框架（UC Berkeley），以高吞吐量和低延时为目标。在全文中被多次提及作为 KV Cache 和连续批处理的代表实现。

## 在本文语境中的角色

- 几乎所有 LLM 推理框架都支持 KV Cache，vLLM 为典型代表
- vLLM 的 Continuous Batching 实现连续批处理
- [原文陈述] 在 2026-08-05 的多模型服务来源中，vLLM 被作为独立服务进程的代表；该文指出其 `--gpu-memory-utilization` 默认值为 0.9，多进程共用单卡时需要外部协调显存与调度。
- [原文陈述] 2026-08-07 的精度格式来源将 vLLM 列为 4-bit 格式在本地/推理生态中常见的使用场景之一。

## 关联

- [[入局AI_Infra系统设计与挑战]]（来源）
- [[概念_KV_Cache]]
- [[概念_连续批处理]]
