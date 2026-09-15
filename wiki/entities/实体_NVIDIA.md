---
type: entity
tags:
- Infra/gpu
- DeepLearning
summary: 全球人工智能算力与 GPU 硬件基础架构的领导企业，构建了以 CUDA、TensorRT 和 Megatron 为核心的软硬件加速生态。
sources:
- wiki/sources/PyTorch常用代码段合集.md
- wiki/sources/入局AI_Infra系统设计与挑战.md
- wiki/sources/大模型显存计算公式与优化.md
- wiki/sources/How_a_GPU_Actually_Works.md
updated: '2026-09-15'
---
# 实体_NVIDIA

全球领先的加速计算与 GPU 半导体企业，现代深度学习、大语言模型与人工智能软硬件基础设施的基石提供商。

## 核心贡献与技术生态
- **GPU 算力硬件平台**：推出 V100/A100/H100/H200/Blackwell 等专为深度学习矩阵计算与 AI 训练推理优化的硬件架构，提供海量算力与高带宽显存（HBM）。
  - [原文陈述] 在 2026-08-18 的 GPU 工作原理来源中，NVIDIA **H100 SXM5**（Dense BF16 989 TFLOPS，3.35 TB/s 显存带宽）被用作主流算力基准，其硬件平衡阈值约为 **295 ops/byte**；而 **H200** 在保持算力不变的前提下将显存带宽提升至 4.8 TB/s，主动将平衡阈值压降至 **206 ops/byte**，以显著缓解大模型自回归解码阶段严重的内存带宽受限（Memory-bound）瓶颈。
- **CUDA 编程开发生态**：建立统治级的并行计算架构与 CUDA 库生态，使开发人员能够在 GPU 上高效执行各类深度学习与高性能计算任务。
- **分布式与加速推理**：研发 Megatron-LM 分布式大模型训练框架（支持 TP/PP/EP 等多维并行）、TensorRT 推理加速引擎及 Triton 推理服务架构。

## 关联

- [[sources/大模型显存计算公式与优化]]（来源）
- [[sources/How_a_GPU_Actually_Works]]（来源）
- [[concepts/概念_AI硬件加速芯片架构|概念_AI硬件加速芯片架构]]
- [[concepts/概念_Roofline模型与算力强度|概念_Roofline模型与算力强度]]
- [[concepts/概念_LLM推理两阶段|概念_LLM推理两阶段]]