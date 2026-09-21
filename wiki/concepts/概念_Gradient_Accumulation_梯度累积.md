---
type: concept
tags:
- DeepLearning
- Skill/python
- Skill/data-analysis
- LLM/training
summary: 梯度累积（Gradient Accumulation）是一种在硬件显存受限时，通过多次前向和反向传播累积梯度，再统一执行一次参数更新，从而在逻辑上等效实现大
  Batch Size 训练的优化技术。
sources:
- wiki/sources/2025-06-27_15-techniques-to-optimize-neural-network-training_197b30.md
updated: '2026-09-21'
aliases:
- Gradient Accumulation
- 梯度累积
- 概念_梯度累积_Gradient_Accumulation
---

# 梯度累积 (Gradient Accumulation)

## 定义
梯度累积（Gradient Accumulation）是在深度学习训练中，当物理显存不足以容纳所需的大 Batch Size 时，通过将大 Batch 拆分为多个较小的 Micro-batch 运行，并将多次前向与反向传播计算得到的梯度进行累加，最后在累积到设定步数时统一调用优化器更新参数的一种“时间换空间”的技术。

## 解决的瓶颈
1. **物理显存限制（VRAM Bottleneck）**：大模型的参数量巨大，若使用大 Batch Size 会导致显存溢出（OOM）。
2. **训练稳定性和收敛速度**：某些任务（如对比学习、大语言模型预训练）需要极大的 Batch Size 才能稳定梯度并加快收敛，而单卡显存无法直接承载。梯度累积能够在不增加显存的情况下，逻辑上达到与大 Batch Size 完全一致的更新效果。

## 算法机制
在正常的训练流程中，每个 mini-batch 都会执行：
`前向传播 -> 计算 Loss -> 反向传播计算梯度 -> 优化器更新参数 -> 梯度清零`

而在梯度累积机制下（假设累积步数为 $N$）：
1. 循环 $N$ 次小 mini-batch（Micro-batch）：
   - 执行前向传播计算 Loss，并对 Loss 进行缩放（除以 $N$ 避免梯度过大）。
   - 执行反向传播计算当前 Micro-batch 的梯度，这些梯度会自动累加在 PyTorch 内部张量的 `.grad` 属性中（即不执行 `optimizer.zero_grad()`）。
2. 在第 $N$ 步：
   - 调用 `optimizer.step()`，使用累积的总梯度更新权重参数。
   - 调用 `optimizer.zero_grad()` 将累积梯度清零。

### PyTorch 代码实现
```python
accumulation_steps = 4  # 累积4步，等效于 Batch Size 扩大4倍
optimizer.zero_grad()

for i, (inputs, targets) in enumerate(train_loader):
    outputs = model(inputs)
    loss = criterion(outputs, targets)
    
    # 缩放 loss
    loss = loss / accumulation_steps
    loss.backward()  # 累积梯度
    
    if (i + 1) % accumulation_steps == 0:
        optimizer.step()       # 更新参数
        optimizer.zero_grad()  # 梯度清零
```

## 适用场景
- **大模型微调与预训练**（如 Transformer/LLM 训练）：这些模型通常需要几百万甚至几千万的 tokens 作为一个 batch，必须通过梯度累积实现。
- **高分辨率图像任务**（如 3D 医疗影像分割、目标检测）：由于单张图像尺寸极大，Batch Size 只能设为 1 或 2，梯度累积能够模拟更大的有效 batch。
- **单卡或低配硬件环境**：在消费级显卡上训练大网络时的首选折中方案。

## 关联
- [[wiki/concepts/概念_神经网络训练优化综述]]
- 来源：[[wiki/sources/2025-06-27_15-techniques-to-optimize-neural-network-training_197b30]]