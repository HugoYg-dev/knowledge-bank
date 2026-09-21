---
type: concept
tags:
- DeepLearning
- Skill/python
- Infra/gpu
- Infra/training
summary: 固定内存配合非阻塞传输，使 CPU 在 GPU 训练当前批次时异步传送下一批数据，从而减少 GPU 等待，但会占用额外 RAM 且对小张量收益有限。
sources:
- wiki/sources/2025-05-07_Memory-Pinning-to-accelerate-model-training_196ac3.md
- wiki/sources/2025-06-27_15-techniques-to-optimize-neural-network-training_197b30.md
- wiki/sources/2025-08-25_PyTorch-Dataloader-has-two-terrible-default-settings_198e2e.md
updated: '2026-09-21'
aliases:
- Memory Pinning
- Pinned Memory
- 固定内存
- 锁页内存
- 概念_固定内存_Memory_Pinning
---

# 固定内存 (Memory Pinning)

固定内存（Memory Pinning），也称为锁页内存（Pinned Memory / Page-locked Memory），是 GPU 训练中用于加速 CPU 到 GPU 数据传输的一种硬件级优化技术。

## 1. 核心原理与异步流水线 (Pipelining)
在默认情况下，CPU 内存分配是**可分页的 (Pageable)**，这意味着操作系统可以根据需要将物理主存中的数据交换到磁盘的虚拟内存中。
当要将数据从可分页内存拷贝到 GPU 时，CUDA 驱动不得不：
1. 先在系统内存中临时申请一块**锁页内存 (Pinned Memory)**；
2. 将可分页内存的数据拷贝到该临时锁页内存中；
3. 通过 DMA (Direct Memory Access) 将数据从锁页内存发送到 GPU 显存。

如果直接把数据存放在锁页内存 (Pinned Memory) 中，就可以**跳过中间拷贝步骤**，直接由 DMA 传输。这样可以使数据传输速率大幅提高，并且允许传输操作与 GPU 计算任务**异步进行 (Overlap)**。

### 异步流水线优化机制
在典型的神经网络训练流程中，默认的同步加载会导致 CPU 与 GPU 串行等待：当 GPU 在前向/反向计算时 CPU 处于闲置状态，而当 CPU 进行数据加载与预处理时 GPU 则被迫处于饥饿和等待状态。

通过在数据加载时结合固定内存，可以实现高效的异步流水线（Pipelining）：
- 当 GPU 在训练第 $N$ 个 Mini-batch 时，CPU 可以并行地将第 $N+1$ 个 Mini-batch 的数据通过 DMA 提前搬运至 GPU。
- 这保证了 GPU 在算完当前 batch 后能够无缝读取下一个 batch 的数据，极大程度地消除了 GPU 饥饿，提高了计算卡在训练过程中的吞吐和利用率。

```mermaid
graph TD
    subgraph 可分页内存 (Pageable Memory)
        A[CPU 内存数据] -->|1. 复制| B[驱动临时锁页内存 Pinned]
        B -->|2. DMA| C[GPU 显存]
    end
    
    subgraph 固定内存 (Memory Pinning)
        D[CPU 锁页内存 Pinned] -->|直接 DMA| E[GPU 显存]
    end
```

## 2. PyTorch 配置实现
在 PyTorch 中，实现 CPU-GPU 异步数据传输需要两步配置：

### 第一步：DataLoader 阶段固定内存与多线程设置
在创建 `DataLoader` 时，设置 `pin_memory=True` 且合理配置 `num_workers > 0`（即 `max_workers`）。这会让数据在 CPU 加载时直接放入锁页内存中，并开启多进程异步加载数据。
```python
train_loader = DataLoader(
    dataset, 
    batch_size=64, 
    shuffle=True, 
    num_workers=4, 
    pin_memory=True  # 启用固定内存
)
```

### 第二步：数据 Transfer 阶段启用非阻塞
在将张量移至 GPU 时，设置 `non_blocking=True`。这使得 CPU 不会等待数据拷贝完成，而是继续执行后续的非 GPU 依赖代码，实现 CPU-GPU 的异步并行。
```python
for inputs, targets in train_loader:
    # 异步传输到 GPU
    inputs = inputs.to('cuda', non_blocking=True)
    targets = targets.to('cuda', non_blocking=True)
    
    # 后续的前向传播与计算
    outputs = model(inputs)
    loss = criterion(outputs, targets)
    ...
```

## 3. 适用场景与显存/内存影响
- **适用场景**：
  - **大 Batch Size / 大张量**：当数据拷贝时间是训练的明显瓶颈时（例如处理高分辨率图像或大文本批次），优化效果非常显著。
  - **I/O 绑定型任务**：当 GPU 计算速度极快，需要 CPU 连续高频传输数据时。
  - 对于极小的张量，数据拷贝时间微不足道，内存固定的开销可能得不偿失。
- **系统内存影响**：
  - 锁页内存无法被操作系统换出（Swap）到磁盘。如果过度使用（比如设置过大的 Batch Size 或过多的 Workers），会**强行霸占大量系统物理主存 (RAM)**，导致系统其他进程由于可用内存不足而运行缓慢，甚至触发系统的 OOM (Out of Memory) 机制。
  - **显存影响**：Memory Pinning 占用的是主机系统内存（RAM），不占用 GPU 显存（VRAM），但它可以大幅提高显存的利用效率（避免 GPU 闲置等待）。

## 4. 实验与性能数据对比
根据实际对比测试（以 MNIST 数据集上训练 5 个 Epoch 为例）：
- **默认设置**（未固定内存，串行等待）：训练总耗时 **43 秒**。
- **优化设置**（启用 `pin_memory=True` 与 `non_blocking=True` 异步流水线）：训练总耗时 **9 秒**，实现约 **4.7x** 的加速。