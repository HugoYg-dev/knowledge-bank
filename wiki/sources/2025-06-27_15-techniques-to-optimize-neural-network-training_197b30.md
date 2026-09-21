---
type: source
tags:
- DeepLearning
- Skill/data-analysis
- LLM/training
summary: 本文总结了15种神经网络训练优化技术，包括使用高效优化器、最大化Batch Size、贝叶斯超参搜索、混合精度训练、He/Xavier初始化、多GPU并行训练、大模型专用库、
  activation checkpointing（激活值重计算）、在GPU上进行数据归一化、梯度累积以及DataLoader优化（max_workers和pin_memory）等。
sources:
- raw/articles/2025-06-27_15-techniques-to-optimize-neural-network-training_197b30.md
updated: '2026-08-03'
---

# 15 techniques to optimize neural network training

## 来源信息
- **来源**: Daily Dose of DS
- **作者**: Avi Chawla
- **原始链接**: [15 ways to optimize neural network training with implementation](https://www.dailydoseofds.com/15-ways-to-optimize-neural-network-training-with-implementation/)
- **归档物理文献**: [[raw/articles/2025-06-27_15-techniques-to-optimize-neural-network-training_197b30.md]]

## 核心要点
1. **基础硬件与批大小优化**：使用高效优化器（如 AdamW、Adam 等）；利用硬件加速器（GPU/TPU）；并在显存允许的条件下尽量增大 Batch Size。
2. **超参搜索与初始化**：当超参数搜索空间较大时，使用贝叶斯优化（Bayesian Optimization）来根据历史配置表现指导搜索，从而以更少的迭代次数和时间找到最佳配置；使用 He 或 Xavier 初始化来加快模型收敛。
3. **混合精度训练 (Mixed precision training)**：在卷积和矩阵乘法等可行环节混合使用 `float16`（半精度）与 `float32`（单精度），以显著降低显存开销并加快计算速度。
4. **分布式与并行计算**：利用 Model/Data/Pipeline/Tensor parallelism 进行多 GPU 训练；对大型模型使用 DeepSpeed、FSDP、YaFSDP 等框架；即便不进行分布式训练，在 PyTorch DataLoader 中也推荐使用 `DistributedDataParallel` (DDP) 代替 `DataParallel` (DP)。
5. **显存与计算权衡（激活值重计算）**：利用激活值重计算（Activation Checkpointing / Gradient Checkpointing）来避免在内存中存储所有中间激活值，而是保留部分关键激活值并在反向传播时重新计算其余部分。这可将显存消耗降低至未采用时的 $\sqrt{M}$，但会由于重复计算增加计算耗时。
6. **数据搬运与归一化优化**：先将低精度数据（如8位整型像素值图像）传输到 GPU，再在 GPU 上进行归一化和类型转换为32位浮点数，这能节省主机到设备的传输带宽；避免使用 `torch.rand(2,2).cuda()` 这种先在 CPU 创建再移至 GPU 的做法，而是直接用 `torch.rand(2, 2, device=...)` 在 GPU 上直接创建。
7. **数据加载管道优化（梯度累积与异步加载）**：显存受限时可使用**梯度累积 (Gradient Accumulation)**，即通过小 batch 运行多次前向/反向传播后才执行一次 `optimizer.step()` 更新权重，实现等效的大 Batch Size 训练；在 DataLoader 中设置合理数量 of `max_workers` 并启用 `pin_memory`（固定内存），使 CPU 在 GPU 计算当前 Batch 时预先将下一个 Batch 的数据搬运到 GPU（异步流水线），避免 GPU 处于饥饿等待状态。

## 关键引文
- "We don’t need to store all the intermediate activations in memory. Instead, storing a few of them and recomputing the rest when needed can significantly reduce the memory requirement. This can reduce memory usage by a factor of `sqrt(M)`... But due to recomputations, it increases run-time."
- "Despite that, there’s a technique called **gradient accumulation** , which lets us (logically) increase batch size without explicitly increasing the batch size."
- "When the model is being trained on the 1st mini-batch, the CPU can transfer the 2nd mini-batch to the GPU... This ensures that the GPU does not have to wait for the next mini-batch of data..."

## 联动概念
- [[wiki/concepts/概念_神经网络训练优化综述]]
- [[wiki/concepts/概念_Gradient_Accumulation_梯度累积]]
- [[wiki/concepts/概念_Memory_Pinning_固定内存]]
- [[wiki/concepts/概念_激活值重计算]]

> 📎 **物理文献**：[[raw/articles/2025-06-27_15-techniques-to-optimize-neural-network-training_197b30.md]]
