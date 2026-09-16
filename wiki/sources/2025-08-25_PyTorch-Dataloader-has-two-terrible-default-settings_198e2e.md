---
type: source
tags:
- DeepLearning
- Skill/python
- Infra/training
summary: 介绍 PyTorch 中 DataLoader 的默认设置问题（导致 CPU 和 GPU 串行等待），并阐述如何通过启用固定内存 (pin_memory=True)、多进程加载以及非阻塞传输
  (non_blocking=True) 来实现 CPU-GPU 的异步流水线优化，在 MNIST 数据集上实现 4.7 倍的加速。
sources:
- raw/articles/2025-08-25_PyTorch-Dataloader-has-two-terrible-default-settings_198e2e.md
updated: 2026-08-03
---

# PyTorch Dataloader has two terrible default settings

本文讨论了 PyTorch `DataLoader` 在默认设置下的效率缺陷，并提供了通过固定内存与非阻塞数据传输实现训练加速的具体方案。

## 来源信息
- **邮件主题**: 4 Layers of Agentic AI Systems
- **发送人**: Daily Dose of DS (avi@dailydoseofds.com)
- **日期**: 2025-08-25
- **链接**: [Daily Dose of DS Blog](https://www.dailydoseofds.com/15-ways-to-optimize-neural-network-training-with-implementation/)

## 核心要点
1. **CPU/GPU 串行等待瓶颈**：在默认的 PyTorch 训练循环中，数据从 CPU 传输到 GPU 是同步阻塞的。当 GPU 进行计算时，CPU 处于闲置状态；当 CPU 进行数据加载时，GPU 处于闲置状态，这导致了严重的计算资源浪费。
2. **异步流水线优化**：通过让 CPU 在 GPU 训练当前 Batch（如 Batch 1）的同时，提前将下一个 Batch（如 Batch 2）传输到 GPU，可以极大消除上述串行等待。
3. **两步实现优化**：
   - 在定义 `DataLoader` 时，设置 `pin_memory=True` 并指定 `num_workers` 以启用锁页内存和多线程数据加载。
   - 在数据传输至 GPU 的 `to()` 步骤中，设置 `non_blocking=True`，允许数据传输与 GPU 计算任务异步并行。
4. **性能对比**：在 MNIST 数据集上进行 5 个 epoch 的模型训练对比：
   - 默认设置：耗时 **43 秒**。
   - 优化后设置：耗时 **9 秒**，实现约 **4.7 倍 (4.7x)** 的加速。

## 关键引文
> "This means when the GPU is working, the CPU is idle, and when the CPU is working, the GPU is idle..."
> 
> "Ideally, you can transfer batch 2 when the GPU is training the model on batch 1. Enabling this is quite simple in PyTorch."

## 联动概念
- [[wiki/concepts/概念_固定内存_Memory_Pinning]]
- [[wiki/concepts/概念_神经网络训练优化综述]]

---
> 📎 **物理文献**：[[raw/articles/2025-08-25_PyTorch-Dataloader-has-two-terrible-default-settings_198e2e.md]]
