---
type: "source"
tags: ["Infra/serving", "LLM/inference", "AI-Agent/coding"]
summary: "以 Superlinked Inference Engine 为例，说明多模型智能体流水线通过共享 GPU 池、按需加载和统一调度降低专用 GPU 闲置成本的服务方式。"
sources: ["raw/articles/2026-08-05_How-to-serve-5-models-on-one-GPU_19fd38.md"]
updated: "2026-08-10"
---

# 多模型共享 GPU 服务：Superlinked Inference Engine

## 来源信息

- 标题：How to serve 5 models on one GPU
- 作者：Avi Chawla / Daily Dose of Data Science
- 日期：2026-08-05
- URL：https://github.com/superlinked/sie

## 核心要点

- [原文陈述] 多模型流水线会组合文档解析、字段抽取、重排序、视觉识别和生成等不同模型；若每个服务栈独占 GPU，顺序执行的阶段会造成设备在等待期间仍被占用。
- [原文陈述] 把多个独立服务进程塞进同一 GPU 时，进程之间并不天然共享显存与负载视图；文章以 `vLLM` 默认允许使用 90% GPU 显存为例，指出静态配额会带来 OOM 风险或闲置显存。
- [原文陈述] [[实体_Superlinked_Inference_Engine]]（SIE）将多类模型置于统一 API 与共享 GPU 池中，按请求加载模型；显存紧张时按最近最少使用策略逐出模型。
- [原文陈述] SIE 使用共享请求队列，并按预估计算成本而非固定请求数量分批，以减少不同长度请求同批时的填充计算。
- [原文陈述] 文章的保险理赔示例以 `extract`、`score`、`generate` 三个原语串联 Docling 文档解析、GLiNER 字段提取、重排序、Grounding DINO 检测与 Qwen3.5 生成。
- [原文陈述] SIE 提供网关与 worker 层以按需求伸缩，也以模型目录保存支持模型的服务配置；文中称其目录当时覆盖 112 个模型。

## 关联实体与概念

- [[实体_Superlinked_Inference_Engine]]：本文的多模型服务引擎。
- [[实体_vLLM]]：作为单模型推理运行时与显存配置问题的对照。
- [[概念_连续批处理]]：共享服务层通过队列和成本感知分批提高资源利用率。
- [[概念_量化]]：模型精度与显存占用是多模型共用 GPU 时的相关约束，但并非本文的主要方案。

> 📎 **物理文献**：[[raw/articles/2026-08-05_How-to-serve-5-models-on-one-GPU_19fd38.md]]
