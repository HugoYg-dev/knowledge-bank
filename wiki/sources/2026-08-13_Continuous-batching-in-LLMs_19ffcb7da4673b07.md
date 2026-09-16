---
type: "source"
tags:
  - Infra/serving
  - LLM/inference
summary: "解构 LLM 连续批处理（Continuous Batching）的核心调度机理：迭代级调度（Iteration-level Scheduling）、选择性批处理（Selective Batching）、vLLM V1 调度器四步预算算法与抢占重算（Preemption Recompute）治理"
sources:
  - "raw/articles/2026-08-13_Continuous-batching-in-LLMs_19ffcb7da4673b07.md"
updated: "2026-09-09"
---

# 来源摘要：Continuous batching in LLMs

## 来源信息

- **原文标题**：Continuous batching in LLMs
- **通讯来源**：Daily Dose of DS
- **原邮件主题**：Continuous Batching in LLMs
- **发送作者**：Daily Dose of DS (Avi Chawla) `<avi@dailydoseofds.com>`
- **发布日期**：2026-08-13
- **邮件/文章标识**：`19ffcb7da4673b07:2`

---

## 核心要点（Executive Summary）

1. [原文陈述] **传统 ML 静态批处理在 LLM 解码中的失效**：传统推理将 Batch 视为固定维度的矩阵，所有样本填充或截断至等长，一次前向传播同时完成；但在 LLM 解码阶段，每次前向传播仅产出一个 Token，且每个请求所需迭代轮次必须等到其生成终止符（Stop Token）才能知晓。固定 Batch 会导致短请求完成后占位等待长请求，GPU 持续全额读取权重显存但产生极低有效吞吐。
2. [原文陈述] **迭代级调度（Iteration-level Scheduling）核心哲学**：服务引擎不等待整个 Batch 全部完成，而是在每次前向传播迭代边界重新决策批次成员。已完成的请求在当前迭代结束时立即离队释放资源，等待中的请求在同一步边界进入填补空位，Batch 每步动态重构。
3. [原文陈述] **选择性批处理（Selective Batching）化解张量异构**：当 Prefill 请求（如 4096 Tokens）与 Decode 请求（如第 900 步的 1 Token）混合在同一步时，系统将所有 Token 展平成一维长序列 `(total_tokens, hidden_size)`。无上下文依赖的 LayerNorm、QKV 线性投影与 FFN 模块在扁平流上单次高效批量运行；在自注意力边界处将张量拆分，各请求对其各自长度不同的 KV Cache 执行注意力运算后，再合并回扁平流进入后续模块。
4. [原文陈述] **vLLM V1 调度器四步算法**：
   - **确定预算**：以 `max_num_batched_tokens` 设定每步 Token 总上限，`max_num_seqs` 设定并发序列上限；
   - **运行中请求优先分配**：运行中请求优先消费预算（Prefill 申请其剩余 Prompt Token 数，Decode 申请 1 个 Token，两者在代码层面统一计算 `target - computed`）；
   - **分配并锁定 KV Cache 块**：在做出调度决策时就地预留显存块；
   - **剩余预算让渡给等待队列**：未启动的等待请求仅分发剩余 Token 预算。
5. [原文陈述] **抢占与重算成本（Preemption and Recompute）**：显存不足分配失败时，调度器强制释放运行中请求的 KV 块，将其标记为 Preempted 并将已计算 Token 计数置零重回等待队列头部。重算（Recompute）已成为 vLLM V1 默认策略（淘汰了 Swap 换入换出）；Prometheus 指标 `total_cumulative_preemption_cnt` 是排查长尾延迟（p99）异常飙升的第一核心指标。
6. [原文陈述] **端到端性能提升量级**：在 OPT-13B 实测基准下，随着输出长度差异拉大，静态批处理吞吐降至 81 tokens/s，而连续批处理引擎达到标准 Hugging Face 朴素服务架构的 23 倍吞吐。

---

## 关联概念与实体

- **关联概念**：
  - [[concepts/概念_连续批处理|概念_连续批处理]]：动态拼车式推理调度核心范式。
  - [[concepts/概念_KV_Cache|概念_KV_Cache]]：自回归自注意力缓存与显存块分配底座。
  - [[concepts/概念_LLM推理两阶段|概念_LLM推理两阶段]]：Prefill 与 Decode 阶段特征及其在调度预算中的统一处理。
- **关联实体**：
  - [[entities/实体_vLLM|实体_vLLM]]：连续批处理与 V1 迭代调度器的行业标杆实现。

---

> 📎 **物理文献**：[[raw/articles/2026-08-13_Continuous-batching-in-LLMs_19ffcb7da4673b07.md]]
