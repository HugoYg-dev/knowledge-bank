---
type: "source"
tags: ["Infra/serving", "LLM/inference"]
summary: "系统科普大模型推理引擎 vLLM 的核心架构与性能优化机制：剖析 KV Cache 显存占用根因，详解 PagedAttention 虚拟内存分页与块表寻址、前缀缓存复用、连续批处理与 Chunked Prefill 动态调度、FP8 权重量化与多卡切分（TP/PP/DP），以及线上推理瓶颈指标、常用参数速查与针对性调优排错策略"
sources: ["raw/articles/大模型推理引擎 vLLM 是什么？.md"]
updated: "2026-11-10"
---

# 来源摘要：大模型推理引擎 vLLM 是什么？

- **文章原题**：大模型推理引擎 vLLM 是什么？（副标：vLLM 如何让同一批 GPU 服务更多请求 —— 从 KV Cache、请求调度到多卡执行）
- **发布渠道/UP 主**：Bilibili / 小白debug（《Vibe知识大赏 | 大模型推理引擎vLLM 是什么？》）
- **视频与参考链接**：[Bilibili 视频](https://www.bilibili.com/video/BV1Q8HP69EEB/?p=1) ｜ 报告精读：vreport.tri4t.xyz
- **入库时间**：2026-11-10

---

## 核心要点

1. **自回归生成与 KV Cache 显存瓶颈**：大模型逐 token 生成时，自注意力机制需参考前文所有 token 的 Key/Value 向量。缓存 KV 虽避免了每步 $O(N)$ 重复计算，但显存随序列线性膨胀（如 LLaMA-13B 在 2048 token 下单请求需占用 1.6 GB 显存）。传统预分配机制因无法预测真实输出长度，导致严重的**内部预留浪费**与显存**外部碎片无法分配**。
2. **PagedAttention 分页管理与块表寻址**：[[entities/实体_vLLM|vLLM]] 借鉴操作系统虚拟内存页表思想，提出 [[concepts/概念_PagedAttention_分页注意力|PagedAttention]]。将逻辑连续的 [[concepts/概念_KV_Cache_键值缓存|KV Cache]] 切分为固定大小的物理块（Block），离散存放于显存池中，由块表（Block Table）维护映射关系。每个请求最多仅浪费最后一个未满块的尾部空间，彻底消除了显存碎片并实现显存块按需申领与归还。
3. **前缀缓存（Prefix Caching）复用**：针对多用户请求共享系统提示词（如“你是一个专业设计师...”）的高频场景，系统为写满的物理块计算上下文哈希指纹。新请求命中相同前缀块时，直接复用既有 KV 块，免除重复计算与存储开销。工程上建议**固定提示词前置、动态内容后置**以最大化命中率。
4. **[[concepts/概念_连续批处理|连续批处理]]与分块预填充（Chunked Prefill）**：静态批处理受制于木桶效应，短请求无法提前离场；vLLM 采用迭代级（Iteration-level）连续批处理，每个 token 生成步重新调度，已完成请求立即离场释放显存，新请求无缝插入。针对超长 Prompt 在预填充（Prefill）阶段长时霸占 GPU 算力导致解码停顿的问题，引入分块预填充（Chunked Prefill）将长输入切段分批推进，在首字延迟（TTFT）、吞吐量与输出流畅度之间取得灵活权衡。
5. **模型超限应对：量化、卸载与多卡切分**：显存不足时，采用 [[concepts/概念_量化|FP8 权重量化]]与 FP8 KV Cache 可使参数和缓存显存减半、并发承载翻倍；CPU 内存卸载因受限于 PCIe 带宽仅适合个人尝鲜；企业生产环境主要依赖多卡并行——高速互联（NVLink）下单机首选张量并行（Tensor Parallelism），跨机或带宽受限环境采用流水线并行（Pipeline Parallelism）。
6. **三层执行架构与指标驱动调优**：系统由 API Server（协议兼容）、Engine Core（调度、显存池、块表与抢占管理）与 GPU Worker（算子执行）分层协作。当监控指标出现 KV Cache 使用率逼近 1.0、请求持续排队或频繁触发抢占时，应针对性调整 `gpu_memory_utilization`、`max_model_len`、`kv_cache_dtype`，或优化提示词结构与 Chunked Prefill 预算。
7. **生产落地参数速查与运维避坑**：标准化启动 `vllm serve` 时需注意：① 单卡放得下且纯并发高时使用数据并行（`--data-parallel-size`）起多副本分摊；② 对外暴露（`--host 0.0.0.0`）务必加上 `--api-key` 鉴权；③ 启动显存不足报错时看末尾预估数字直接限定 `--max-model-len`；④ CUDA Graphs 录图提速但多占显存，显存极端紧张可开 `--enforce-eager`；⑤ 老旧显卡不支持 bfloat16 时 `--dtype auto` 自动安全退回 float16；⑥ 通过 `/metrics` 监控 `vllm:kv_cache_usage_perc`，并计算前缀命中率 `prefix_cache_hits_total / prefix_cache_queries_total`。

---

## 关键引文

> “操作系统的虚拟内存提供了一个思路：程序看到连续地址，数据可以分散在物理内存中，由页表记录对应关系。PagedAttention 将这个思路用于 KV cache：逻辑顺序由块表维护，物理显存可以分散存放。注意力计算按块表找到并读取各块。”
> 
> “这些优化各自针对不同开销：缓存复用减少重复计算，分块管理提高显存利用率，连续批处理利用 GPU 并行能力，量化降低数据占用。调优从实际出现的排队、抢占和命中率入手，才能把参数调整对应到具体瓶颈。”

---

## 关联实体与概念

- **所属系统实体**：[[entities/实体_vLLM|实体_vLLM]]
- **核心支撑概念**：
  - [[concepts/概念_PagedAttention_分页注意力|概念_PagedAttention_分页注意力]]
  - [[concepts/概念_KV_Cache_键值缓存|概念_KV_Cache_键值缓存]]
  - [[concepts/概念_连续批处理|概念_连续批处理]]
  - [[concepts/概念_量化|概念_量化]]

---

> 📎 **物理文献**：[[raw/articles/大模型推理引擎 vLLM 是什么？.md]]
