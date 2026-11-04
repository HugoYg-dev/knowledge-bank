---
type: "source"
tags: ["DeepLearning", "LLM/training"]
summary: "Daily Dose of DS 系统拆解神经网络训练的 12 种主流优化器（SGD、AdaGrad、RMSprop、Adam、AdamW、Adafactor、Lion、AdEMAMix、Shampoo、SOAP、Muon、Sophia），对比梯度平滑、步长自适应、正则化解耦、显存占用、矩阵结构与曲率估计维度的工程权衡，指出步数减少 20% 但单步慢 30% 反致更慢的性能陷阱"
sources: ["raw/articles/2026-11-02_12-optimizers-for-training-neural-networks_1a19e2c67284daff.md"]
updated: "2026-11-04"
---

# 来源摘要：12 optimizers for training neural networks

## 来源信息

- **原文标题**：12 optimizers for training neural networks
- **通讯来源**：Daily Dose of DS (Avi Chawla) `<avi@dailydoseofds.com>`
- **原文主题**：12 Optimizers for Training Neural Networks, clearly explained!
- **发布日期**：2026-11-02
- **邮件 ID**：`1a19e2c67284daff`
- **文章 ID**：`1a19e2c67284daff:2`
- **内容层级**：`email_fallback`
- **物理文献**：[[raw/articles/2026-11-02_12-optimizers-for-training-neural-networks_1a19e2c67284daff.md]]

---

## 核心要点（Executive Summary）

1. [原文陈述] **12 种主流优化器演化谱系与工程权衡核心**：
   - 优化器选择的关键不仅是“收敛所需步数”，而是每一次参数更新的计算复杂度与显存状态开销。
   - 12 种优化器（SGD、AdaGrad、RMSprop、Adam、AdamW、Adafactor、Lion、AdEMAMix、Shampoo、SOAP、Muon、Sophia）通过改变梯度历史保存方式、步长自适应机制、显存压缩程度以及矩阵几何与曲率利用，形成了不同的工程取舍。
2. [原文陈述] **梯度平滑与步长自适应演进（SGD $\to$ AdaGrad $\to$ RMSprop $\to$ Adam）**：
   - **SGD with Momentum**：维护梯度一阶矩（累积滑动平均），平抑横向振荡并积累纵向速度，但所有参数共享同一标量学习率；
   - **AdaGrad**：累积历史所有梯度平方和，频繁更新的参数步长自动衰减，适合稀疏特征，但分母单调递增导致训练后期步长过早收敛至零；
   - **RMSprop**：改用指数移动平均（EMA）追踪二阶矩，历史观测平滑衰退，保持自适应调节活力；
   - **Adam**：融合一阶动量与二阶矩缩放，但其二阶统计量追踪的是梯度方差统计量，而非真实的 Hessian 二阶曲率。
3. [原文陈述] **正则化解耦、显存状态优化与动量增强（AdamW、Adafactor、Lion、AdEMAMix）**：
   - **AdamW**：将权重衰减（Weight Decay）从自适应梯度更新中解耦，直接作用于权重本身，避免 L2 正则项被二阶矩尺度 $\sqrt{v}$ 扭曲；
   - **Adafactor**：针对 2D 矩阵参数将 $n \times m$ 的二阶矩分解为行与列的低维因子统计量 $n+m$（以 1B 参数为例，标准 Adam FP32 状态需 8GB 显存），大幅缓解大模型训练显存压力；
   - **Lion**：完全移除二阶矩缓冲，仅保留动量与梯度的线性混合并取符号（Sign），使每个坐标更新步长绝对值一致，显著减少显存占用但需适配更小学习率；
   - **AdEMAMix**：引入快慢双重动量 EMA，快 EMA 紧跟最新梯度，慢 EMA 长期保留历史方向信息，以额外状态换取更佳泛化。
4. [原文陈述] **矩阵结构正交化与二阶曲率估计（Shampoo、SOAP、Muon、Sophia）**：
   - **Shampoo**：利用矩阵值统计量构造左右双侧预条件子（Preconditioner），捕捉参数跨维度相关性；
   - **SOAP**：将梯度旋转到 Shampoo 预条件子的特征基（Eigenbasis）中应用 Adam，再旋转回原坐标系；
   - **Muon**：利用 Newton-Schulz 多项式迭代对 2D 矩阵动量进行正交化，均衡奇异值谱范数，使参数更新流形更加稳定；其参数覆盖具有明确选择性，通常应用于隐藏层二维权重矩阵，而 Embedding、Output 输出层与向量参数仍维持使用 AdamW；
   - **Sophia**：定期轻量估计对角二阶曲率缩放动量并执行元素级截断，以较低均摊开销引入曲率感知。
5. [原文陈述] **实验基准测试规范与“步数减少 vs 单步变慢”性能陷阱**：
   - **选型基线推荐**：以 AdamW 为基线；显存受限评估 Adafactor / Lion；二维矩阵架构评估 Muon、Shampoo 或 SOAP；
   - **工程耗时陷阱**：步数减少 20% 但单步耗时增加 30% 反致总时间增加（如 80 步 $\times$ 1.3 秒 = 104 秒，劣于基线的 100 步 $\times$ 1.0 秒 = 100 秒）；
   - **评估闭环**：必须固定计算预算比较验证集质量，且务必端到端同时度量显存峰值与单步耗时（Step Time）。

---

## 关键引文

> "An optimizer can reduce the number of training steps and still make your run slower. Each update has its own compute and memory cost, which becomes part of the training budget."
>
> "Muon approximately orthogonalizes momentum updates for matrix parameters using Newton–Schulz iterations. It changes the matrix update’s singular-value structure rather than scaling every coordinate independently. Parameter selection matters here. Muon is typically applied to hidden weight matrices, with another optimizer handling embeddings, output layers, and vector parameters."
>
> "Also measure peak memory and step time. An optimizer that reaches the target in 20% fewer steps but makes each step 30% slower takes about 4% longer overall."

---

## 关联概念与实体

- **关联概念**：
  - [[concepts/概念_梯度下降优化器|概念_梯度下降优化器]]：Vanilla GD、Momentum、AdaGrad、RMSprop 与 Adam 一阶/二阶矩机制。
  - [[concepts/概念_Muon优化器|概念_Muon优化器]]：Newton-Schulz 迭代矩阵正交化与参数覆盖选择（隐藏层 vs 嵌入/输出层）。
  - [[concepts/概念_神经网络训练优化综述|概念_神经网络训练优化综述]]：现代神经网络训练超参、优化器选型与显存分析。
  - [[concepts/概念_混合精度训练|概念_混合精度训练]]：FP16/BF16/FP32 状态张量与显存开销。
  - [[concepts/概念_学习率调度|概念_学习率调度]]：自适应学习率与学习率搜索调优。
- **关联实体**：
  - [[entities/实体_Adam优化器|实体_Adam优化器]]：主流深度学习自适应优化器基线。

---

> 📎 **物理文献**：[[raw/articles/2026-11-02_12-optimizers-for-training-neural-networks_1a19e2c67284daff.md]]
