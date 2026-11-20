---
type: "concept"
tags:
  - "LLM/inference"
  - "Infra/serving"
summary: "将计算密集的 Prefill 预填充阶段与显存带宽密集的 Decode 解码阶段物理解耦至不同硬件节点运行的分布式大模型推理架构，消除资源争抢并优化端到端吞吐与时延"
aliases:
  - "PD分离"
  - "PD 分离"
  - "Prefill-Decode Disaggregation"
  - "PD Disaggregation"
  - "预填充解码分离"
  - "预填充解码解耦"
sources:
  - "wiki/sources/非算法工程师也能看懂_推理框架的来龙去脉.md"
  - "wiki/sources/腾讯15年资深后台工程师_转战大模型推理的抉择.md"
updated: "2026-11-20"
---

# 概念：PD 预填充解码分离 (Prefill-Decode Disaggregation)

## 1. 定义与设计背景

**PD 分离（Prefill-Decode Disaggregation，预填充解码解耦）** 是一种面向大模型服务集群的分布式推理架构范式。其核心思想是将整个大模型推理生命周期中计算特性迥异的两个阶段——**Prefill（预填充/读题阶段）** 与 **Decode（自回归解码/作答阶段）** 物理拆分到独立的 GPU 节点或实例集群中运行，通过高速互联网络传递中间 [[concepts/概念_KV_Cache_键值缓存|KV Cache]]。

### 1.1 传统同机混合部署的物理冲突
在单机引擎或传统混合批处理（Mixed Batching）架构中，Prefill 与 Decode 请求共享同一批 GPU：
- **资源瓶颈相悖**：Prefill 阶段一次性并行计算 Prompt 所有输入 Token，GPU 算力利用充分，属于**计算受限（Compute-bound）**；Decode 阶段逐字自回归生成，每步必须将数十 GB 模型权重从显存读取一次却只产生 1 个 Token 的计算量，属于**显存带宽受限（Memory-bound）**；
- **长尾时延冲击与卡顿（Interference & Head-of-line Blocking）**：当新请求携带数千甚至数万 Token 的超长 Prompt 进入系统执行 Prefill 时，巨大的矩阵乘法算力占用会导致同批次内正在以几十毫秒步长平稳 Decode 的请求发生瞬时停顿（Jank），造成 P99 词间延迟（TBT/TPOT）严重恶化。

---

## 2. 核心架构与工作机理

```
[客户端请求] ──> [LLM 智能网关 / 负载均衡]
                       │
                       ▼
       ┌───────────────────────────────┐
       │     Prefill 专用实例集群      │
       │  (计算密集型优化：高算力 GPU)  │
       │   - 适合大张量并行 (TP)       │
       │   - 优先保障首字时延 (TTFT)   │
       └──────────────┬────────────────┘
                      │ 高速网络传输 (RDMA/PCIe)
                      │ KV Cache 跨机搬运
                      ▼
       ┌───────────────────────────────┐
       │      Decode 专用实例集群      │
       │  (访存密集型优化：高带宽显存) │
       │   - 适合高并发批处理/EP/DP    │
       │   - 优先保障高吞吐与稳定 TBT   │
       └──────────────┬────────────────┘
                      │
                      ▼
                 [流式返回客户端]
```

### 2.1 阶段解耦与异构并行配置
- **Prefill 节点**：专门处理输入上下文。并行度设计以降低首字延迟（TTFT）为目标，通常采用更高维度的张量并行（TP，如 8 卡 TP）将大矩阵切分并压满 Tensor Core；
- **Decode 节点**：承接 Prefill 节点生成的初始 KV Cache，负责后续的长程逐 Token 生成。并行度设计以最大化系统吞吐量为目标，通常采用数据并行（DP）结合专家并行（EP，针对 MoE 架构，如 8 路 EP + 8 路 DP），并配合大批次连续批处理；
- **KV Cache 高速跨机传输**：Prefill 计算完成后，节点利用高效的通信协议（如基于 RDMA 的专用数据传输引擎）将生成的 Key-Value 张量直接推送到被调度的 Decode 节点显存池中，Decode 机器即刻启动自回归解码。

---

## 3. 选型权衡与优势局限

| 维度 | 传统混合推理 (Unified Colocation) | PD 分离架构 (Disaggregated Serving) |
| :--- | :--- | :--- |\n| **资源竞争** | Prefill 与 Decode 争抢 GPU 算力与显存，互为干扰 | 物理隔离，消除突发长 Prompt 对 Decode 的卡顿冲击 |
| **首字与词间时延** | 相互牵制，难以兼顾低 TTFT 与稳定低 TBT | Prefill 节点独享算力优化 TTFT，Decode 节点保障极低 TBT 抖动 |
| **硬件配比灵活性** | 所有节点硬件规格必须对称统一 | 可采用异构芯片/机型（如 Prefill 用强算力卡，Decode 用大显存高带宽卡） |
| **网络通信开销** | 仅机内通信，无跨机传输 KV Cache 开销 | **高度依赖节点间高带宽低时延网络**（需 RDMA 支持），避免网络拷贝抵消加速红利 |
| **调度复杂度** | 单层调度器即可完成批次调度 | 需引入分布式全局调度器，兼顾 KV Cache 路由亲和性、网络拥塞与双端水位负载均衡 |

---

## 4. 工业界落地与代表项目

- **Mooncake（月之暗面 Kimi）**：以 KV Cache 为中心的 PD 分离架构，解构长上下文场景下存储与计算边界，荣获 FAST 2025 最佳论文；
- **英伟达 Dynamo**：跨引擎的分布式集群编排框架，原生支持 PD 分离、感知 KV Cache 分布的智能路由与跨机快速传输，兼容 vLLM、SGLang、TensorRT-LLM；
- **阿里云 PAI-EAS**：提供 MoE 模型 PD 分离部署模板，支持 Prefill（如 8 卡 TP）与 Decode（如 8 路 EP + 8 路 DP）动态配比推荐；
- **学术奠基工作**：DistServe（OSDI 2024）、Splitwise（ISCA 2024）开创了将 LLM 两阶段解耦并分配至异构资源池的理论基础。

---

## 5. 关联概念与实体

- **核心理论基础**：
  - [[concepts/概念_LLM推理两阶段|概念_LLM推理两阶段]]：Prefill 与 Decode 的计算与访存瓶颈物理根源；
  - [[concepts/概念_KV_Cache_键值缓存|概念_KV_Cache_键值缓存]]：跨节点流转与存储的核心状态载体；
  - [[concepts/概念_Roofline模型与算力强度|概念_Roofline模型与算力强度]]：量化评估算力受限与带宽受限的分析模型。
- **协同服务技术**：
  - [[concepts/概念_连续批处理|概念_连续批处理]]：Decode 节点维持高吞吐的基础调度机制；
  - [[concepts/概念_PagedAttention_分页注意力|概念_PagedAttention_分页注意力]]：节点内部显存块离散管理；
  - [[concepts/概念_LMCache_解耦式KV缓存|概念_LMCache_解耦式KV缓存]]：旁路分布式 KV 缓存池与流式传输。
- **代表性落地实体**：
  - [[entities/实体_vLLM|实体_vLLM]] / [[entities/实体_SGLang|实体_SGLang]]：通用推理引擎后端；
  - [[entities/实体_DeepSeek|实体_DeepSeek]]：大规模 MoE 推理工程实践。
