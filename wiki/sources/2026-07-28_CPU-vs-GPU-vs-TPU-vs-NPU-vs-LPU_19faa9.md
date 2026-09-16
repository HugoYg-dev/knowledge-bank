---
type: source
tags:
- Infra/gpu
summary: 本文详细介绍了五种主流AI计算硬件架构（CPU、GPU、TPU、NPU和LPU）内部逻辑设计的物理差异与核心权衡，展现了AI计算芯片从通用灵活性向极致专用化的演进过程。
sources:
- raw/articles/2026-07-28_CPU-vs-GPU-vs-TPU-vs-NPU-vs-LPU_19faa9.md
updated: '2026-08-04'
---

# 来源摘要：CPU vs GPU vs TPU vs NPU vs LPU

## 来源信息
- **来源主题**: Serverless vs. On-prem vs. Edge Deployment (原邮件主题)
- **发送人**: Daily Dose of DS \<avi@dailydoseofds.com\>
- **日期**: Tue, 28 Jul 2026 21:23:05 +0000
- **原始物理文献**: [[raw/articles/2026-07-28_CPU-vs-GPU-vs-TPU-vs-NPU-vs-LPU_19faa9.md]]

## 核心要点
- **AI硬件架构的多样化**：目前有五种主要的AI硬件架构（CPU, GPU, TPU, NPU, LPU），它们在灵活性、并行度以及内存访问策略上做出了截然不同的物理折衷。
- **CPU与GPU的对比**：CPU适用于通用逻辑计算，依靠深层缓存和主存（DRAM）执行复杂的分支和任务；GPU则通过数千个小核心对多路数据并行执行相同指令（SIMT/SIMD），从而在AI训练上占据主导。
- **TPU的脉动阵列**：Google专为神经网络设计的TPU核心采用了MAC网格的脉动阵列。权重从一侧输入，激活值从另一侧输入，部分和在网格内部沿波浪式向相邻单元传导，大量节省了与主存交换的带宽需求。其整个执行过程完全由编译器进行静态时间编排，而非硬件动态调度。
- **NPU的边际低功耗**：NPU是针对边缘设备推理设计的架构，将MAC数组和SRAM集成在片上，但改用低功耗的系统内存（如 LPDDR），以在单位数瓦特的极低功耗下（如智能手机、可穿戴设备和物联网设备）运行推理。
- **LPU的片上超低延迟**：Groq推出的LPU架构移除了外部显存的限制，将所有模型权重和激活完全驻留在片上SRAM中。加上由编译器静态排期，实现了零 Cache Miss 和极致的推理延迟。其物理代价是单片内存容量极小，需要多片互联才能运行大模型。

## 关键引文
- "Each one makes a fundamentally different tradeoff between flexibility, parallelism, and memory access."
- "The core compute unit is a grid of multiply-accumulate (MAC) units where data flows through in a wave pattern."
- "The architecture removes off-chip memory from the critical path entirely. All weight storage lives in on-chip SRAM."

## 联动概念
- [[wiki/concepts/概念_AI硬件加速芯片架构|概念：AI硬件加速芯片架构]]

---
> 📎 **物理文献**：[[raw/articles/2026-07-28_CPU-vs-GPU-vs-TPU-vs-NPU-vs-LPU_19faa9.md]]
