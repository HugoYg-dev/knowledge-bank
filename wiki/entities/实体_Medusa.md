---
type: entity
tags:
- LLM/inference
summary: Medusa 是一个 LLM 推理加速框架，属于推测解码（Speculative Decoding）的多头并行树状验证方案。
sources:
- wiki/sources/推测解码Speculative_Decoding综述.md
- wiki/sources/2026-09-12_4-speculative-decoding-variants_1a09737e364224e2.md
updated: '2026-09-15'
---

# 实体：Medusa

## 概述

Medusa 是一个开源的 LLM 推理加速框架，属于推测解码（Speculative Decoding）体系下的单模型自推测（Self-Drafting）方案。它通过在目标模型顶层附加多个轻量级预测头并结合树状注意力（Tree Attention）验证，规避了传统推测解码维护第二套独立小模型的显存开销。

## 核心机制

1. **并行多头预测（Medusa Heads）**：
   - 在目标大模型（Target Backbone）最后一层 Decoder 之上添加多个额外的前馈预测头（FFN Heads）。
   - 每个 Head 针对同一模型隐状态并行预测未来不同位置的 Token（例如 Head 1 预测 $+1$ 位置，Head 2 预测 $+2$ 位置，依此类推）。
2. **树状注意力验证（Tree Attention Verification）**：
   - **挑战**：由于所有 Heads 均基于同一个隐层状态并行输出，彼此之间缺乏自回归条件依赖（Conditioning），单纯按贪婪序列拼接容易产生语义不连贯。
   - **解决**：Medusa 将各个 Head 预测出的 Top-k 候选 Token 组合构建为候选树（Candidate Tree）。利用定制的树状注意力掩码（Tree Attention Mask），使目标模型在单次前向验证（Forward Pass）中同时校验多条可能的分支路径，最终接受匹配长度最长的一致分支。

## 训练范式与性能

Medusa 提供了两种训练与调优路径：
- **Medusa-1（仅训练预测头）**：
  - 冻结目标模型主干骨干参数，仅训练外挂的多个 Medusa Heads。
  - 训练成本极低，在完全不改变主干生成质量的前提下，论文汇报实现 **>2.2x** 的推理加速比。
- **Medusa-2（主干与多头联合微调）**：
  - 将主干模型与 Medusa Heads 进行联合微调（Joint Tuning）。
  - 加速比进一步提升至 **2.3x 至 3.6x**，但对训练配方和算力要求更高。

## 工程部署与权衡

- **显存占用极小**：相比双模型推测解码，无需额外加载小模型的数十亿参数及二级独立 KV Cache，仅需常驻极少量的 Head 权重。
- **树宽超参调控（Tree Width Tradeoff）**：候选树的宽度与深度是服务端调控的核心杠杆。增加树宽可提高候选分支覆盖率与 Token 接受率，但单次验证的矩阵计算量与瞬时显存峰值也会相应增长。
- **开源生态**：代码开源于 GitHub（`FasterDecoding/Medusa`），并已被 vLLM、TGI 等多个主流推理引擎集成或支持。

## 关联

- [[概念_推测解码]] — 所属的推理加速核心范式
- [[实体_EAGLE]] — 同属于优化草稿阶段的高效推测解码方案
- [[实体_vLLM]] — 工业级推理引擎，支持 Medusa 推测解码加速
- [[推测解码Speculative_Decoding综述]] — 早期推测解码体系性综述
- [[2026-09-12_4-speculative-decoding-variants_1a09737e364224e2]] — 4 种推测解码变体横向机制对比来源