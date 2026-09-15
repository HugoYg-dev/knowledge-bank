---
type: "entity"
tags:
- "LLM/inference"
summary: "EAGLE 是一个基于目标模型倒数第二层隐状态特征预测的 LLM 推测解码推理加速框架。"
sources:
- "wiki/sources/2026-09-12_4-speculative-decoding-variants_1a09737e364224e2.md"
updated: "2026-09-15"
---

# 实体：EAGLE

## 概述

EAGLE（Extrapolation Algorithm for Greater Language-model Efficiency）是一个高效的大语言模型推测解码（Speculative Decoding）加速框架。与传统的双模型架构（需运行一个独立的自回归小语言模型）不同，EAGLE 通过在目标模型内部表征层进行轻量级特征外推，实现高接受率与低显存开销的推测解码。

## 核心机制

1. **倒数第二层特征预测（Feature-Level Drafting）**：
   - 传统推测解码通常在 Token 空间进行自回归预测，而 EAGLE 在隐状态空间（Hidden States）操作。
   - EAGLE 训练一个轻量级前向预测模块，直接预测目标大模型倒数第二层（second-to-top layer）的特征向量，再将预测出的特征隐状态映射为候选 Token。
2. **解决特征多义性（Disambiguation via Shifted Input）**：
   - 在特征空间中，不同 Token 序列可能产生非常相近的隐藏状态。
   - 为了消除这种特征多义性（Feature Ambiguity），EAGLE 将当前 Token 序列向前平移一位（shifted forward by one position）联合输入草稿模块，为特征预测提供充分的上下文约束，从而大幅提升预测准确度与 Token 接受率。

## 性能与工程特点

- **加速性能**：论文在 LLaMA2-Chat 70B 上的测试结果表明，EAGLE 可实现 **2.7x 至 3.5x** 的端到端延迟加速比，在典型部署配置下服务吞吐量接近翻倍。
- **显存占用低**：无需在显存中同时常驻另一个独立的小语言模型权重及庞大的二级 KV Cache，仅需加载参数量极小的专用特征预测模块。
- **部署边界与权衡**：EAGLE 的轻量草稿模块是针对特定目标模型训练的，因此最适合模型权重与推理引擎可协同维护的专用服务场景，需引入针对性的部署支持。

## 关联

- [[概念_推测解码]] — 所属的推理加速核心范式
- [[实体_Medusa]] — 同为参数内生/外挂头类的自推测解码代表框架
- [[实体_vLLM]] — 主流高性能推理引擎，已集成推测解码相关优化
- [[2026-09-12_4-speculative-decoding-variants_1a09737e364224e2]] — 4 种推测解码变体横向对比来源
