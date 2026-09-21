---
type: source
tags:
- DeepLearning
- Skill/python
- Infra/training
summary: 介绍了在 PyTorch 中使用固定内存（Memory Pinning）技术来加速 CPU-GPU 数据传输的原理和配置方法，通过 pin_memory=True
  和 non_blocking=True 实现 CPU 和 GPU 的异步并行工作。
sources:
- raw/articles/2025-05-07_Memory-Pinning-to-accelerate-model-training_196ac3.md
updated: 2026-08-03
---

# Memory Pinning to accelerate model training

## 来源信息
- **主题**: Memory Pinning to Accelerate Model Training
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Wed, 07 May 2025
- **原始物理文件**: [[raw/articles/2025-05-07_Memory-Pinning-to-accelerate-model-training_196ac3.md]]

## 核心要点
- **串行瓶颈**：传统的 PyTorch 训练中，CPU 传输数据和 GPU 计算是串行的，即 CPU 传输数据时 GPU 闲置，GPU 训练时 CPU 闲置。
- **固定内存异步传输**：通过将 CPU 内存中的数据锁在物理内存中（不进行虚拟内存交换），可以通过 GPU 的 DMA（Direct Memory Access）通道实现更快速且与计算并行的异步数据拷贝。在训练第 N 个 mini-batch 时，CPU 同时将第 N+1 个 mini-batch 拷贝到 GPU。
- **PyTorch 配置实现**：
  - 在创建 `DataLoader` 时设置 `pin_memory=True`，并配置合理的 `num_workers`；
  - 在将数据 transfer 到 GPU 时（如 `.to(device)` 或 `.cuda()`），配置 `non_blocking=True`。
- **显存与硬件限制**：
  - 锁页内存（Pinned Memory）会强行占用主存（RAM）且无法被换出，如果锁定过多张量会严重挤占系统可用内存。
  - 对于小张量，数据拷贝耗时极短，固定内存优化的效果几乎可以忽略不计。

## 关联知识
- 核心概念：[[concepts/概念_Memory_Pinning_固定内存]]

## 关键引文
> "Memory pinning is used to speed up the data transfer from the CPU to the GPU by making the training workflow asynchronous."
> "If several tensors are allocated to the pinned memory, it will block a substantial portion of RAM. This impacts the memory available to other operations."
> "Also, if the tensors are small, memory pinning has a negligible effect since the data transfer from the CPU to the GPU does not take that time anyway."

> 📎 **物理文献**：[[raw/articles/2025-05-07_Memory-Pinning-to-accelerate-model-training_196ac3.md]]
