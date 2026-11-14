---
title: 既然 Logits 排序与 Softmax 完全一致，为什么我们还需要算 Softmax？
author:
- '[[Hugo Yang]]'
published: 2026-09-23
created: 2026-09-23
draft: false
description: 揭示深度学习体系中数学直觉与工程实践的反差，从严格单调性出发，拆解模型训练、大模型采样生成、工业推理优化与现实决策对 Softmax 的工程依赖。
tags:
- LLM/inference
- LLM/arch
---

# 既然 Logits 排序与 Softmax 完全一致，为什么我们还需要算 Softmax？

在深度学习推理引擎里，只要开启的是贪婪解码（greedy decoding），底层代码通常只对最后一层的未归一化分值向量（logits）跑一次 `argmax`，直接把最大值对应的索引捞出来交差，中间根本不计算 Softmax。

原因可以用一条简单的数学性质说清楚。假设最后一层线性变换输出的分值向量为 $z = [z_1, z_2, \dots, z_K]$，经过 Softmax 计算后得到的概率向量为 $p = [p_1, p_2, \dots, p_K]$，其数学定义可以写成下面这个比值。

$$p_i = \text{Softmax}(z)_i = \frac{e^{z_i}}{\sum_{j=1}^K e^{z_j}}$$

指数函数 $f(x) = e^x$ 在整个实数域上严格单调递增，分母 $\sum_{j=1}^K e^{z_j}$ 又是所有候选类别共享的正数常量，所以在实数域内必然满足下面的等价关系。

$$z_i > z_j \iff p_i > p_j$$

**未归一化的 logits 大小排序，与经过 Softmax 计算后的概率分布排序在实数域内完全等价。**

如果系统只关心哪一个类别概率最大，或者只按可能性从大到小排个名次，logits 提供的排序结果和 Softmax 分毫不差。在 IEEE-754 浮点数计算中，直接保留未归一化 logits 在极小概率的长尾处有时还更保真。假如词表里存在较大正值，使两个极低负数 logits（例如 `-90` 和 `-120`）减去全局最大值 $c = \max_j(z_j)$ 后双双跌破单精度下溢临界（约 `-103.3`），Safe Softmax 在算指数时会把二者同时压成硬零，抹平原本的微弱大小关系。未归一化的 logits 反而在精度范围内保留了相对序。

既然排出来的名次毫无区别，算一次 Softmax 还要跑昂贵的指数运算、在 GPU 上做跨线程块规约求和、并提防词表扩到十几万之后的数值溢出，为什么现代深度学习体系反而把它当成训练、采样与风控决策的基础组件？

## 能不算的地方，引擎确实坚决不算

在看系统为什么离不开 Softmax 之前，先看工业界已经成功省掉它的地方。

最直接的场景是单选预测与贪婪解码。在图像分类、意图识别或大语言模型关闭采样做贪婪生成时，系统只关心第一名是谁。既然 $\arg\max_i (p_i)$ 恒等于 $\arg\max_i (z_i)$，无论在 ONNX Runtime、TensorRT 还是 vLLM 的执行流里，底层走的都是纯粹的 `argmax(logits)`。在这里计算 Softmax 只会白白浪费算力与显存带宽。

到了大模型做 Top-K 采样时，词表往往达到 128,000 到 150,000 维。如果每解一个 token 都在完整词表上跑一遍全局 Softmax，光是十几万次指数运算、跨线程块规约和显存读写往返，就会吃掉大量访存带宽。

像 vLLM 或 llama.cpp 这类推理引擎会把步骤调换。llama.cpp 在 CPU 或 Metal 上使用部分排序截出前 $K$ 个候选；vLLM 在 GPU 上也提供两类优化思路，一类是基于 Radix 选择先截出前 $K$ 个（例如前 50 个）候选值，再只对这 50 个候选做局部 Softmax 归一化，另一类则是直接采用无排序拒绝采样绕过显式排序。对于先截断后归一化的路径，局部 Softmax 满足如下公式。

$$\tilde{p}_k = \frac{e^{z_k}}{\sum_{j \in \text{Top-}K} e^{z_j}}, \quad k \in \text{Top-}K$$

按照条件概率展开，全词表的配分函数 $\sum_{m=1}^V e^{z_m}$（其中 $V$ 为全词表大小）在分子与分母里刚好约分抵消，**局部 Softmax 在数学上严密无损，全量 Softmax 在推理阶段被完全绕开。**

```python
import torch

# 假设 1 个样本，5 个类别的 logits
logits = torch.tensor([2.3, -1.2, 5.8, 0.4, 5.799])

# 方式 A，直接在 logits 上取 Top-1
top1_logit_idx = torch.argmax(logits, dim=-1)

# 方式 B，经过 Softmax 之后再取 Top-1
probs = torch.softmax(logits, dim=-1)
top1_prob_idx = torch.argmax(probs, dim=-1)

# 方式 C，Top-K 排序
topk_logits_idx = torch.topk(logits, k=3, dim=-1).indices
topk_probs_idx = torch.topk(probs, k=3, dim=-1).indices

assert torch.equal(top1_logit_idx, top1_prob_idx)
assert torch.equal(topk_logits_idx, topk_probs_idx)
print("数学验证成功，logits 排序与 Softmax 排序完全一致")
```

到了模型训练阶段，工程师同样会避免在 Python 层手动调用显式 `softmax`。PyTorch 的 `nn.CrossEntropyLoss` 要求直接传入未归一化的 logits，底层使用 Log-Sum-Exp 技巧完成算子融合。

$$\log p_i = z_i - \log \sum_j e^{z_j} = z_i - \left( c + \log \sum_j e^{z_j - c} \right), \quad c = \max_j(z_j)$$

底层 CUDA kernel 把 LogSoftmax 和 NLLLoss 融合成单个算子，既防止浮点数溢出，又少了一次中间显存读写。在超大词表训练中，Megatron-LM 与 Liger-Kernel 还会采用融合线性交叉熵（Fused Linear Cross-Entropy），在 GPU 片上共享内存（SRAM）里分块计算矩阵乘法并在线更新 Log-Sum-Exp，算完直接丢弃 logits，不再把庞大的未归一化张量写回全局显存。

在所有只求极值、或者底层能直接融合吸收的环节，工程实现都在绕开显式的 Softmax。

## 训练需要平滑残差，不能只靠硬排序

既然推理时能省就省，为什么深度学习的训练基础依然建立在 Softmax 之上？一个自然的问题是，分类任务只要正确类别排第一，为什么不直接在 logits 上用支持向量机（SVM）的铰链损失（Hinge Loss）或排序损失？

比如设定目标类分值比其他类别高出固定间隔 $\Delta$ 时损失就归零，写出来就是下面这个式子。

$$\mathcal{L}_{\text{hinge}} = \max(0, \max_{j \neq y}(z_j) - z_y + \Delta)$$

这种设计在深度神经网络里很难训出稳定的表征，根源在梯度动力学。Hinge Loss 存在梯度死区，一旦目标类别分值高出间隔阈值，损失直接变成 0，梯度立刻归零。网络随后停止在这个样本上更新参数，不再继续拉开正负样本的区分度；而且它每次只惩罚最大的那一个负样本，斜率固定为 $\pm 1$，忽略其余全部类别。

Softmax 配合交叉熵（负对数似然）的表现完全不同。设真实标签为独热向量 $y$，其中目标类别分量 $y_i = 1$，其余分量为 0，交叉熵损失写出来如下。

$$\mathcal{L} = -\log p_y = -z_y + \log \sum_j e^{z_j}$$

对未归一化的输入分值 $z_i$ 求偏导，可以化简出非常干净的结果。

$$\frac{\partial \mathcal{L}}{\partial z_i} = - y_i + \frac{\frac{\partial}{\partial z_i} \left( \sum_j e^{z_j} \right)}{\sum_j e^{z_j}} = - y_i + \frac{e^{z_i}}{\sum_j e^{z_j}} = p_i - y_i$$

整理成向量形式，梯度恰好就是预测概率与真实标签的残差。

$$\nabla_z \mathcal{L} = \mathbf{p} - \mathbf{y}$$

**这个残差梯度同时具备有界自适应、无梯度死区与全局博弈三条关键性质。** 第一，回传给目标神经元的梯度落在 $[-1, 0]$，错误类别落在 $[0, 1]$，单样本梯度模长始终有界，既防住了梯度爆炸，又能在高置信度（如 $p_y = 0.99$）时自动把残差缩到 $-0.01$ 平稳收敛。第二，只要输入分值有限，预测概率 $p_y$ 就永远小于 1，残差不会归零；Soudry 等人在 2018 年证明，正是这股微弱推力让交叉熵损失在线性可分数据上具备隐式最大边距正则化效应。第三，分母的指数求和项把所有类别绑在同一个约束里，推高目标分值时，负梯度会按预测概率 $p_j$ 比例分摊给每个错误类别，形成平滑的全局压制。

## 大模型采样生成与概率空间约束

如果模型永远只做 `argmax`，推理时确实用不上 Softmax。但在生成式大语言模型里，贪婪搜索很快会让文本陷入机械重复与模式坍塌，输出自然文本依赖的是在词表空间做多项分布采样（在 PyTorch 接口中对应 `torch.multinomial`）。

合法的离散概率分布必须满足非负性（$p_i \ge 0$）与归一性（$\sum_i p_i = 1$）。未归一化的 logits 取值落满整个实数域，既没有上下界，也常出现负数（比如一组分值 $[-12.5, -8.3, -20.1]$），计算机没法拿负数和无边界分值直接充当采样权重。Softmax 通过指数运算把任意实数映射为正数，再用分母归一化把总和固定成 1，从而把无边界的欧氏空间收进标准概率单纯形（Standard Probability Simplex）。

更重要的是温度系数（Temperature，$T > 0$）对生成多样性的非线性调节，对应如下公式。

$$p_i = \frac{e^{z_i / T}}{\sum_j e^{z_j / T}}$$

这个形式对应统计物理中的玻尔兹曼分布，$T$ 用来调节分布的信息熵。当 $T \to 0$ 时，分值差距被指数级拉大，分布收尖成脉冲，退化为确定贪婪选择；当 $T \to \infty$ 时，所有 $z_i / T$ 都趋向 0，每个词的概率趋近 $1/V$（其中 $V$ 为词表大小），分布被拉平为均匀分布；而在 $T = 1$ 时，则完整保留模型原本学到的概率偏好。如果脱离指数结构直接在原始 logits 上除以标量 $T$，所有类别的差值比例只做线性放缩，相对结构丝毫不变，调节不了分布的信息熵。

同样，Top-p（核采样）要求在累积概率达到阈值 $p$（通常取 0.9）时截断候选集，满足如下不等式。

$$\sum_{i \in V^{(p)}} p_i \ge p$$

因为 logits 缺少基准和量纲，没法在原始分值空间里定义概率质量区间，累积截断也只能在归一化后的概率空间里完成。下面这段实现展示了温度调节（`temperature > 0`）、单调性预排序、排序空间掩码截断与多项分布采样的完整流程，全程直接在排序空间完成掩码与重归一化，再通过 `gather` 将采样索引映回原词表。

```python
import torch


def sample_next_token(logits: torch.Tensor, temperature: float = 0.8, top_p: float = 0.9):
    if temperature <= 0:
        raise ValueError("temperature 必须大于 0；贪婪解码请直接调用 argmax")

    # 1. 调节温度
    scaled_logits = logits / temperature

    # 2. 直接对 logits 降序排序，单调性保证排序结果与概率排序一致
    sorted_logits, sorted_indices = torch.sort(scaled_logits, descending=True, dim=-1)

    # 3. 在排序空间计算 Softmax 与累积概率
    sorted_probs = torch.softmax(sorted_logits, dim=-1)
    cumulative_probs = torch.cumsum(sorted_probs, dim=-1)

    # 4. 计算截断掩码，右移一位以保留刚好达到阈值的临界词
    sorted_indices_to_remove = cumulative_probs > top_p
    sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
    sorted_indices_to_remove[..., 0] = False

    # 5. 直接在排序空间掩码清零并重新归一化（全流程仅执行一次 Softmax）
    masked_probs = sorted_probs.masked_fill(sorted_indices_to_remove, 0.0)
    final_probs = masked_probs / masked_probs.sum(dim=-1, keepdim=True)

    # 6. 兼容任意前导维度（1D/2D/3D）做多项分布采样，并映回原始词表索引
    orig_prefix = final_probs.shape[:-1]
    flat_probs = final_probs.reshape(-1, final_probs.shape[-1])
    sampled_sorted = torch.multinomial(flat_probs, num_samples=1).reshape(*orig_prefix, 1)
    next_token = sorted_indices.gather(dim=-1, index=sampled_sorted)
    return next_token
```

## Logits 没有绝对尺度，定不了拒答门槛

在工程系统里，除了采样，安全拒答与置信度门控也离不开概率尺度。

logits 缺乏跨样本比较的绝对基准。神经网络最后一层通常是线性映射 $z = W h + b$。如果训练时权重矩阵 $W$ 整体放大 10 倍，logits 之间的差值就会从 2 变成 20；缩小到 0.1 倍，差值就会缩成 0.2。网络内部没有约束 logits 绝对尺度的机制。

举个例子，模型在请求 A 输出的最高两项分值为 `[12.0, 10.0]`，差值为 `2.0`；在请求 B 输出的分值为 `[2.0, 0.0]`，差值同样是 `2.0`。单看数值差根本没法判断模型在两个请求上的把握是否一样。跨样本之间，或者模型迭代的不同检查点之间，直接对比 logits 的绝对数值缺少统计意义。

在金融风控、医疗辅助或企业级 Agent 任务中，业务规则经常要求在模型最高类别置信度低于 0.85 时触发「拒答」并转人工审核。要让硬阈值在跨请求场景下含义稳定，传入的数值必须同时满足两个条件，**其一是落进 $[0, 1]$ 区间内的有界性，其二是频率一致性**（即预测置信度为 0.9 的样本里，确实大约有 90% 是正确的）。未归一化的 logits 做不到这两点，只有先经过 Softmax 归一化，再配合 Platt Scaling 或 Temperature Scaling 针对期望校准误差（ECE）做后处理校准，无界分值才能变成下游服务可以信赖的置信度指标。

## 统计学渊源与指数归一化

如果只是为了凑出非负且和为 1 的向量，平方归一化（$\tilde{p}_i = z_i^2 / \sum z_j^2$）或者截断归一化（$\tilde{p}_i = \text{ReLU}(z_i) / \sum \text{ReLU}(z_j)$）也能做到。深度学习几乎全面采用指数归一化，根源在广义线性模型（GLM）与最大熵原理。

多类别分类的统计本质是对多项分布（Multinomial Distribution）建模，而多项分布属于经典的指数族分布。将其写成指数族的标准形式如下。

$$P(y=i \mid \eta) = \exp \left( \eta_i - A(\eta) \right)$$

这里的自然参数（natural parameters）$\eta = [z_1, z_2, \dots, z_K]$ 对应的正是 logits，而对数配分函数（log-partition function）恰好是 Log-Sum-Exp 形式。

$$A(\eta) = \log \sum_{j=1}^K e^{\eta_j}$$

指数族分布有一条核心性质，均值参数等于对数配分函数的梯度，展开正好回到 Softmax。

$$\mu = \mathbb{E}[y] = \nabla_\eta A(\eta) = \left[ \frac{e^{\eta_1}}{\sum e^{\eta_j}}, \dots, \frac{e^{\eta_K}}{\sum e^{\eta_j}} \right]^T = \text{Softmax}(\eta)$$

把均值映射到自然参数的函数称为规范链接函数（canonical link function），它的反函数就是 Softmax。换句话说，logits 对应多项分布的自然参数，Softmax 则是把自然参数还原为可观测均值概率的映射。

另一个支撑来自信息论的最大熵原理（Maximum Entropy Principle）。当建模者在已知部分特征期望约束的前提下推断未知概率分布时，先验假设最少、最客观的分布就是使香农信息熵最大化的分布。列出该带约束优化问题的拉格朗日函数如下。

$$\mathcal{L}(p, \lambda_0, \boldsymbol{\lambda}) = -\sum_{i=1}^K p_i \log p_i - \lambda_0 \left(\sum_{i=1}^K p_i - 1\right) - \sum_m \lambda_m \left(\sum_{i=1}^K p_i f_m(i) - \bar{f}_m\right)$$

对每个概率分量 $p_i$ 求偏导并令其为 0，解出的解析形式必然是指数形式的吉布斯分布，与 Softmax 完全一致。Softmax 是在给定一阶矩约束下对不确定性最无偏的数学形式。

## 硬件计算与算子分块演进

即便在硬件实现层面，工程界也没有放弃 Softmax，而是反复重构访存流水线来迁就它。标准自注意力机制之所以产生 $O(N^2)$ 的显存占用，主要原因就是 Softmax 的分母需要对整行元素求和，迫使中间注意力矩阵必须完整写回显存。

转折点来自对 Softmax 分块结合律的挖掘。Milakov 与 Gimelshein 在 2018 年提出在线归一化计算方法（Online Softmax），随后 Tri Dao 等人在 2022 年的 FlashAttention 中将其与片上 SRAM 分块（tiling）及重计算结合，打破了这一瓶颈。当把两个数据块合并时，算法只需动态维护局部最大值 $m$ 与归一化分母 $d$。

$$m_{\text{new}} = \max(m_A, m_B)$$

$$d_{\text{new}} = d_A e^{m_A - m_{\text{new}}} + d_B e^{m_B - m_{\text{new}}}$$

$$O_{\text{new}} = O_A e^{m_A - m_{\text{new}}} + O_B e^{m_B - m_{\text{new}}}$$

按 FlashAttention-2 的写法，这里的 $O_A$、$O_B$ 表示尚未除以分母 $d$ 的局部加权累加矩阵，全部数据块合并完成后再在末尾统一除以最终的 $d_{\text{new}}$（若是 FlashAttention-1 先行归一化再重缩放的写法，则需乘以相应的 $d_A / d_{\text{new}}$ 权重系数）。通过在寄存器中实时重缩放历史累加和，系统不必物化全局注意力矩阵就能精确完成计算。

**只要离开单纯取极值的瞬间，整个深度学习系统从训练残差、随机采样、校准拒答到硬件算子分块，依然围绕完整的概率分布运转。** Logits 排序等价省下了推理解码阶段的冗余计算，而 Softmax 依然稳稳守在概率建模的核心位置。

## 参考来源

1. Maxim Milakov, Natalia Gimelshein (2018), *Online normalizer calculation for softmax*
2. Tri Dao et al. (2022), *FlashAttention, Fast and Memory-Efficient Exact Attention with IO-Awareness* 与 FlashAttention-2 (2023)
3. Daniel Soudry et al. (2018), *The Implicit Bias of Gradient Descent on Separable Data*
4. PyTorch 官方文档中关于 `torch.nn.CrossEntropyLoss` 与 `torch.multinomial` 的实现说明
