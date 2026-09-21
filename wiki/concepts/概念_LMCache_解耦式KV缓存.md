---
type: concept
tags:
- Infra/serving
- LLM/inference
summary: 解耦式 KV 缓存（Disaggregated KV Caching）将缓存管理从推理引擎主进程剥离为旁路独立进程，结合 CacheBlend 算法的选择性重计算，突破传统前缀缓存（Prefix
  Caching）的严格限制，解决资源抢占，大幅提速智能体与 RAG 推理。
sources:
- wiki/sources/2026-07-07_Rethinking-KV-caching-for-production-inference_19f3d7.md
updated: '2026-09-21'
aliases:
- LMCache
- 解耦式KV缓存
- KV缓存解耦
- 概念_解耦式KV缓存与LMCache
---

# 概念：解耦式 KV 缓存与 LMCache

## 定义
**解耦式 KV 缓存（Disaggregated KV Caching）**是一种新型的 LLM 推理缓存管理架构。其核心思想是将 KV 缓存的物理管理（存储、传输、量化等 I/O 密集型任务）从推理引擎（如 vLLM、SGLang、TensorRT-LLM，执行计算密集型的矩阵乘法）主进程中剥离出来，作为单独的旁路进程运行。这使得推理引擎仅处理推理计算，而复杂的缓存生命周期与跨设备流转由专门的缓存管理系统（如 LMCache）处理。

## 传统前缀缓存的物理瓶颈
传统**前缀缓存（Prefix Caching / Prompt Caching）**要求两次请求的输入 Token 序列在字节级上必须存在完全相同的“公共前缀”。一旦前缀发生任何改变，就会发生 100% 的缓存失效（Cache Miss）。这导致其在以下实际生产场景中面临物理瓶颈：
- **多文档 RAG（检索增强生成）**：若缓存了文档 $A$ 和文档 $B$ 的独立 KV 缓存，当查询需要同时检索 $A$ 和 $B$ 时，由于 $B$ 的 KV 缓存是在没有 $A$ 语境的情况下计算的，前缀不匹配导致无法直接拼接复用。
- **文档顺序发生颠倒**：同一批文档如果以不同顺序输入（例如：$A, B, C$ 变为 $B, A, C$），前缀哈希全部失效。
- **动态增长的会话历史**：在 Agent 多轮对话或工具调用中，随着对话历史的膨胀和系统提示词的变动，除最开头的固定 prompt 外，后续的所有缓存都会因前缀被破坏而彻底报废。

## LMCache 的解耦架构与核心机制
LMCache 是一套开源的解耦式 KV 缓存系统，其核心物理机制包括：

### 1. 旁路独立进程设计
LMCache 作为一个旁路守护进程（Sidecar Process）运行，通过极轻量的共享 GPU 内存（Shared GPU Memory）与推理引擎进程进行 IPC 通信。推理引擎只需要发送极小的 Block ID 列表通知 LMCache，其余的所有 KV 缓存数据的转移、换入换出全由 LMCache 进程异步完成。由于缓存管理（I/O 密集型）与模型计算（计算密集型）资源解耦，消除了进程内缓存处理带来的资源抢占（Contention），避免了传统缓存量化与存储导致的推理吞吐下降。

### 2. 多 GPU 零拷贝共享（Zero-copy Sharing）
在多 GPU 推理集群中，传统方法在 GPU 间共享缓存需要多次显存到内存的复制。LMCache 允许不同的 GPU 实例直接读取和写入同一片共享显存区域，省去了数据拷贝的 CPU-GPU 物理总线带宽开销，实现多 GPU 间的零拷贝共享。

### 3. 多层级并行异步加载（Multi-tier Parallel Loading）
KV 缓存可以保存在 GPU 显存、CPU 内存、本地 SSD 以及远端云存储中。LMCache 摒弃了传统逐级线性查找的低效模式，采用多层级并行查询与异步流式加载。当在某一介质中匹配成功时，即刻流式传输数据，从而最大化利用系统带宽，将首字延迟（TTFT）加速高达 14 倍，冷启动时间由分钟级降至秒级。

## CacheBlend 算法原理
为解决前缀缓存中“多文档拼接失效”的本质痛点，LMCache 引入了 **CacheBlend** 算法（EuroSys 2025 最佳论文）。
- **核心观测**：在现代 Transformer 架构中，绝大部分 Token 在计算自注意力时，其注意力权重主要局限在自身内部（局部上下文），只有极少数 Token 会跨越文档边界产生强烈的交互。
- **选择性重计算（Selective Recomputation）**：
  CacheBlend 并不在文档拼接时重新计算所有 Token 的 KV 缓存，而是识别出那些跨文档边界、对全局上下文有强注意力联系的极少数 Token 集合，仅对这部分 Token 进行重新计算。
- **缓存复用与加速**：
  除了极少数边界 Token 被重新计算外，其余的大部分 Token 均直接复用先前独立计算并缓存的 KV 块。这样在保证输出质量与原始全量计算一致的前提下，多文档拼接查询的处理速度提升了 **2~4 倍**。

## 关联
- [[概念_KV_Cache_键值缓存]]（基础理论）
- [[wiki/sources/2026-07-07_Rethinking-KV-caching-for-production-inference_19f3d7]]（直接来源）