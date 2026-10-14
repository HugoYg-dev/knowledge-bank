---
title: "既然 Logits 排序与 Softmax 完全一致，为什么我们还需要算 Softmax？"
author:
  - "[[Hugo Yang]]"
published: 2026-09-23
created: 2026-09-23
draft: false
description: "揭示深度学习体系中数学直觉与工程实践的反差，从严格单调性出发，拆解模型训练、大模型采样生成、工业推理优化与现实决策对 Softmax 的工程依赖。"
tags:
  - "LLM/inference"
  - "LLM/arch"
---

# 既然 Logits 排序与 Softmax 完全一致，为什么我们还需要算 Softmax？

在很多深度学习推理引擎的底层实现里，只要开启的是贪婪解码（Greedy Decoding），代码通常直接对最后一层的未归一化分值向量（Logits）执行一次 `argmax`，把最大值对应的索引捞出来就交差了，中间根本不跑 Softmax。

原因可以用一条简单的数学性质说清楚。

假设最后一层线性变换输出的分值向量为 $z = [z_1, z_2, \dots, z_K]$，经过 Softmax 计算后得到的概率向量为 $p = [p_1, p_2, \dots, p_K]$，数学形式定义如下

$$p_i = \text{Softmax}(z)_i = \frac{e^{z_i}}{\sum_{j=1}^K e^{z_j}}$$

指数函数 $f(x) = e^x$ 在整个实数域上严格单调递增，分母 $\sum_{j=1}^K e^{z_j}$ 又是所有候选类别共享的正数常量，所以在实数域内必然满足

$$z_i > z_j \iff p_i > p_j$$

未归一化的 Logits 大小排序，与经过 Softmax 计算后的概率分布排序在实数域内完全等价。

如果系统只关心哪一个类别概率最大，或者想按可能性从大到小排个名次，Logits 提供的排序结果和 Softmax 分毫不差。在 IEEE-754 浮点数计算中，这个等价性在极小概率的长尾处甚至更具优势。当两个负数 Logits 极低（例如 -90 和 -120）时，在单精度浮点数下计算 Safe Softmax 会因为指数下溢将二者都变为硬零，抹平原有的微弱大小关系。未归一化的 Logits 反而在精度范围内保留了长尾相对序。

但算一次 Softmax 的代价并不低。它不仅要跑昂贵的指数运算，在 GPU 上还要做跨线程块的规约求和，词表一旦扩到十几万，还要提防数值溢出。既然排出来的名次完全没区别，为什么现代深度学习体系没有扔掉 Softmax，反而把它作为训练、采样和大模型决策的关键组成？

## 能不算的地方，引擎确实坚决不算

在回答系统为什么需要 Softmax 之前，可以先看工业界在哪些场景里主动把它省掉。

最直接的场景是单选预测与贪婪解码。在图像分类、意图识别，或者大语言模型关闭采样直接贪婪生成的路径上，系统只关心第一名是谁。既然 $\arg\max_i (p_i)$ 恒等于 $\arg\max_i (z_i)$，ONNX Runtime、TensorRT 还是 vLLM 的执行流里，走的就是纯粹的 `argmax(logits)`。在这里计算 Softmax 只会凭空浪费算力与显存读写带宽。

到了大模型做 Top-K 采样的时候，词表往往有 128,000 到 150,000 维。如果每解一个 token 都在完整的词表上算一遍全局 Softmax，光是十几万次指数运算、跨线程块的规约求和以及显存读写往返，就会吃掉不少访存带宽。

像 vLLM 或 llama.cpp 这类推理引擎，常见的做法是把步骤调换。引擎先直接在未归一化的 Logits 上跑截断算子，llama.cpp 在 CPU 或 Metal 上使用局部堆排序或部分排序截出候选集，vLLM 在 GPU 上则基于 Radix 选择或无排序拒绝采样，把候选集直接砍到前 50 个。

随后，计算流只针对这 50 个候选值做局部 Softmax 归一化

$$\tilde{p}_k = \frac{e^{z_k}}{\sum_{j \in \text{Top-}K} e^{z_j}}, \quad k \in \text{Top-}K$$

根据条件概率展开，全词表的配分函数 $\sum_{m=1}^V e^{z_m}$ 在分子与分母中完全约分抵消，局部 Softmax 在数学上严密无损。全量 Softmax 在推理阶段被完全规避了。

```python
import torch

# 假设 1 个样本，5 个类别的 Logits
logits = torch.tensor([[2.3, -1.2, 5.8, 0.4, 5.799]])

# 方式 A，直接在 Logits 上取 Top-1
top1_logit_idx = torch.argmax(logits, dim=-1)

# 方式 B，经过 Softmax 之后再取 Top-1
probs = torch.softmax(logits, dim=-1)
top1_prob_idx = torch.argmax(probs, dim=-1)

# 方式 C，Top-K 排序
topk_logits_idx = torch.topk(logits, k=3, dim=-1).indices
topk_probs_idx = torch.topk(probs, k=3, dim=-1).indices

assert torch.equal(top1_logit_idx, top1_prob_idx)
assert torch.equal(topk_logits_idx, topk_probs_idx)
print("数学验证成功，Logits 排序与 Softmax 排序完全一致")
```

在模型训练阶段，工程师也极力避免在 Python 层手动写 `softmax`。PyTorch 的 `nn.CrossEntropyLoss` 要求直接传入未归一化的 Logits，底层使用经典的 Log-Sum-Exp 技巧完成算子融合

$$\log p_i = z_i - \log \sum_j e^{z_j} = z_i - \left( c + \log \sum_j e^{z_j - c} \right), \quad c = \max_j(z_j)$$

底层 CUDA kernel 把 LogSoftmax 和 NLLLoss 融合成一个算子执行，既防止了浮点数溢出，又减少了一次昂贵的中间显存读写。在超大词表训练中，像 Megatron-LM 与 Liger-Kernel 还会进一步采用融合线性交叉熵（Fused Linear Cross-Entropy），在 GPU 片上共享内存（SRAM）中分块计算矩阵乘法并在线更新 Log-Sum-Exp，算完即丢弃 Logits，不再把巨大的未归一化张量写回显存。

在所有只需要极值、或者底层能直接融合吸收的地方，工程实现都在尽可能绕开显式的 Softmax。

## 训练需要残差，而不是硬排序

既然推理时能省就省，为什么整个深度学习的训练基石仍然建立在 Softmax 之上？

一个自然的疑问是，既然分类任务只要正确的类别排在第一，为什么不直接在 Logits 上使用类似支持向量机（SVM）的铰链损失（Hinge Loss）或者排序损失？

例如设定目标类分值比其他类别高出固定间隔 $\Delta$ 时损失为零

$$\mathcal{L}_{\text{hinge}} = \max(0, \max_{j \neq y}(z_j) - z_y + \Delta)$$

这种设计在深度神经网络里很难训练出稳定的表征，根本原因在于梯度的动力学特征。

Hinge Loss 存在明显的梯度死区。一旦目标类别的分值高出阈值，损失直接变为 0，梯度立刻归零。网络随即停止在这个样本上更新参数，不会继续拉大正负样本的区分度，难以建立鲁棒的泛化特征。此外，Hinge Loss 每次只对单个最大负样本计算固定斜率（$\pm 1$）的惩罚，忽略其余全部类别，缺乏全局视野。

Softmax 配合交叉熵（负对数似然）损失的表现完全不同。设真实标签为独热向量 $y$，其中目标类别分量 $y_i = 1$，其余分量为 0。损失函数为

$$\mathcal{L} = -\log p_y = -z_y + \log \sum_j e^{z_j}$$

对未归一化的输入分值 $z_i$ 求偏导，推导如下

$$\frac{\partial \mathcal{L}}{\partial z_i} = - y_i + \frac{\frac{\partial}{\partial z_i} \left( \sum_j e^{z_j} \right)}{\sum_j e^{z_j}} = - y_i + \frac{e^{z_i}}{\sum_j e^{z_j}} = p_i - y_i$$

整理成向量形式，梯度正好是预测概率与真实标签的直接残差

$$\nabla_z \mathcal{L} = \mathbf{p} - \mathbf{y}$$

这个简洁的梯度形式具备三条优秀的动力学性质。

第一，梯度幅度平滑自适应且严格有界。回传给目标神经元的梯度范围落在 $[-1, 0]$，回传给错误类别的梯度落在 $[0, 1]$。即便模型产生严重偏离，单样本梯度模长也始终有界，杜绝了梯度爆炸；当模型预测正确且置信度极高（如 $p_y = 0.99$）时，残差仅为 $-0.01$，梯度自动衰减，网络平稳收敛。

第二，无梯度死区。只要输入分值有限，预测概率 $p_y$ 就永远小于 1，残差永远不为 0。即使分类完全正确，网络依然会产生微弱推力继续拉大正负类别的差距。Soudry 等人在 2018 年的研究证明，正是这种持续推力让交叉熵损失在线性可分数据上具备隐式最大边距正则化效应。

第三，全局概率博弈。分母中的指数求和项将所有类别绑定在同一约束下。推高目标类别分值的同时，负梯度会按照各自的预测概率 $p_j$ 分摊给每一个错误类别，形成平滑的全局压制。这种协作机制是单类排序无法实现的。

## 大模型采样生成与概率空间约束

如果模型永远只做 Argmax，我们确实可以在推理中跳过 Softmax。但在生成式大语言模型中，自回归生成无法单纯依靠选择最大分值。

贪婪搜索会导致生成文本很快陷入机械重复与模式坍塌。大语言模型输出流畅自然文本的基础，是在词表空间进行多项式采样（Multinomial Sampling）。

采样计算必须依赖合法的离散概率分布。未归一化的 Logits 取值落在整个实数域，既无界，又常出现负数（例如一组分值为 $[-12.5, -8.3, -20.1]$）。离散概率分布必须满足非负性（$p_i \ge 0$）与归一性（$\sum_i p_i = 1$）。计算机无法将负数和无边界分值直接当作多项式采样的权重。Softmax 通过指数运算将任意实数映射为正数，再通过分母归一化将总和约束为 1，将无边界的欧氏空间映射到了标准概率单纯形（Standard Probability Simplex）上。

更为关键的是对生成多样性的调节。大模型常用的温度系数（Temperature），定义如下

$$p_i = \frac{e^{z_i / T}}{\sum_j e^{z_j / T}}$$

这个结构对应统计物理中的玻尔兹曼分布。通过指数的非线性放缩，$T$ 承担着调节分布信息熵的作用。

当 $T \to 0$ 时，高分值与其他分值之间的差距被指数级拉大，分布呈现极端的尖锐脉冲，退化为确定性的贪婪选择。

当 $T \to \infty$ 时，所有 $z_i / T$ 均趋于 0，每个词的概率都接近 $1/V$，分布被强行拉成平坦的均匀分布。

在 $T = 1$ 时，保持模型原本学习到的概率偏好。

如果脱离指数结构直接在原始 Logits 上除以标量 $T$，所有类别的相对比例依然保持线性，排序和差值比例丝毫不变，无法调节分布的信息熵。

同样，Top-p（核采样）要在累积概率达到阈值 $p$（通常为 0.9）的区间截断候选集

$$\sum_{i \in V^{(p)}} p_i \ge p$$

因为 Logits 没有基准和量纲，无法在原始分值空间中定义置信区间，这种累积截断只能在归一化后的概率测度空间中完成。

下面的实现展示了温度调节、单调性预排序、Top-p 掩码映射与多项式采样的完整流程。针对多批次场景，代码使用 `scatter` 规避了多维布尔索引展平导致的跨样本掩码污染。

```python
import torch

def sample_next_token(logits: torch.Tensor, temperature: float = 0.8, top_p: float = 0.9):
    # 1. 调节温度
    scaled_logits = logits / temperature
    
    # 2. 直接对 Logits 降序排序，单调性保证排序结果与概率排序一致
    sorted_logits, sorted_indices = torch.sort(scaled_logits, descending=True, dim=-1)
    
    # 3. 在排序空间计算 Softmax 与累积概率
    sorted_probs = torch.softmax(sorted_logits, dim=-1)
    cumulative_probs = torch.cumsum(sorted_probs, dim=-1)
    
    # 4. 计算截断掩码，右移一位以保留刚好达到阈值的临界词
    sorted_indices_to_remove = cumulative_probs > top_p
    sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
    sorted_indices_to_remove[..., 0] = 0
    
    # 5. 将排序空间的掩码精确映射回原始词表索引，防止多批次掩码展平冲突
    indices_to_remove = sorted_indices_to_remove.scatter(
        dim=-1, index=sorted_indices, src=sorted_indices_to_remove
    )
    masked_logits = scaled_logits.masked_fill(indices_to_remove, -float('Inf'))
    
    # 6. 对截断后的 Logits 执行单次 Softmax 归一化并进行多项式采样
    final_probs = torch.softmax(masked_logits, dim=-1)
    next_token = torch.multinomial(final_probs, num_samples=1)
    return next_token
```

## Logits 没有绝对尺度，定不了拒答门槛

在工程落地中，不仅采样需要概率，系统控制与安全拒答同样需要概率。

Logits 缺乏跨样本比较的绝对基准。神经网络的最后一层通常是线性映射 $z = W h + b$。如果模型在训练中把权重矩阵 $W$ 整体放大 10 倍，Logits 之间的数值差就会从 2 变成 20；如果缩小到 0.1 倍，差值就会缩到 0.2。网络内部没有强制约束 Logits 绝对尺度的机制。

例如一个模型在请求 A 输出的最高两项分值为 `[12.0, 10.0]`，差值为 `2.0`；在请求 B 输出的分值为 `[2.0, 0.0]`，差值同样是 `2.0`。单看数值差无法判断模型在这两个请求上的把握程度是否一致。在不同样本之间，或者在模型迭代的不同检查点之间，直接对比 Logits 的绝对大小缺乏现实意义。

在金融风控、医疗辅助或企业级 Agent 任务中，系统经常需要设立确定性的业务规则。例如当模型最高类别的置信度低于 0.85 时，系统触发拒答流程并转交人工审核。

要让这样一个硬阈值在跨请求场景下具备一致的业务含义，传入的数值必须满足两项条件。

其一是具备固定在 $[0, 1]$ 区间内的有界性。

其二是具备统计学上的频率一致性，即预测置信度为 0.9 的样本集合里，大约有 90% 是真实正确的样本。

未归一化的 Logits 无法满足这些条件。通过 Softmax，再配合 Platt Scaling 或 Temperature Scaling 针对期望校准误差（ECE）进行后处理校准，网络内部的无界分值才能转化为下游服务可以稳定解析的置信度。

## 统计学渊源与指数归一化

如果只是为了实现非负与归一化，使用平方归一化（$\tilde{p}_i = z_i^2 / \sum z_j^2$）或者截断归一化（$\tilde{p}_i = \text{ReLU}(z_i) / \sum \text{ReLU}(z_j)$）也可以得到总和为 1 的非负向量。为什么深度学习几乎全面采用了指数归一化？

这源于统计学中广义线性模型（GLM）与最大熵原理的内在要求。

多类别分类任务的数学本质是对多项分布（Multinomial Distribution）进行建模。多项分布属于经典的指数族分布。将多项分布表示为指数族的标准形式

$$P(y=i \mid \eta) = \exp \left( \eta_i - A(\eta) \right)$$

其自然参数（Natural Parameters）$\eta = [z_1, z_2, \dots, z_K]$ 对应的就是 Logits。这里的对数配分函数（Log-Partition Function）正是 Log-Sum-Exp 形式

$$A(\eta) = \log \sum_{j=1}^K e^{\eta_j}$$

指数族分布的重要性质在于，均值参数等于对数配分函数的梯度

$$\mu = \mathbb{E}[y] = \nabla_\eta A(\eta) = \left[ \frac{e^{\eta_1}}{\sum e^{\eta_j}}, \dots, \frac{e^{\eta_K}}{\sum e^{\eta_j}} \right]^T = \text{Softmax}(\eta)$$

将均值映射到自然参数的函数称为规范链接函数（Canonical Link Function），其反函数正是 Softmax。从统计建模角度看，Logits 对应多项分布的自然参数，而 Softmax 是把自然参数还原为可观测均值概率的对应映射。

另一个支撑来自信息论中的最大熵原理（Maximum Entropy Principle）。当我们在已知部分特征期望约束的前提下推断未知概率分布时，先验假设最少、最客观的分布就是使香农信息熵最大化的分布。

求解该带约束优化问题，设拉格朗日函数如下

$$\mathcal{L}(p, \lambda_0, \boldsymbol{\lambda}) = -\sum_{i=1}^K p_i \log p_i - \lambda_0 \left(\sum_{i=1}^K p_i - 1\right) - \sum_m \lambda_m \left(\sum_{i=1}^K p_i f_m(i) - \bar{f}_m\right)$$

对每个概率分量 $p_i$ 求偏导并令其为 0，解出的解析形式必然是吉布斯分布，与 Softmax 完全一致。Softmax 是在给定一阶矩约束下对不确定性最平中无偏的数学形式。

## 硬件计算与算子分块演进

在硬件实现层面，Softmax 也曾被视为注意力机制的核心瓶颈。标准自注意力机制之所以产生 $O(N^2)$ 的显存占用，是因为 Softmax 的分母需要对整行全部元素求和，导致中间注意力矩阵必须完整写入显存。

现代注意力计算利用 Softmax 的分块结合律打破了这一瓶颈。Milakov、Gimelshein 与 Tri Dao 等人在 FlashAttention 中引入的在线安全 Softmax（Online Safe Softmax），能够在片上 SRAM 中分块处理局部数据。

当把两个数据块合并时，算法动态维护局部最大值 $m$ 与归一化分母 $d$

$$m_{\text{new}} = \max(m_A, m_B)$$

$$d_{\text{new}} = d_A e^{m_A - m_{\text{new}}} + d_B e^{m_B - m_{\text{new}}}$$

$$O_{\text{new}} = O_A e^{m_A - m_{\text{new}}} + O_B e^{m_B - m_{\text{new}}}$$

通过在寄存器中实时重缩放历史累加和，系统无需保留全局注意力矩阵即可准确完成计算。这种算法创新说明，工程界不仅没有抛弃 Softmax，还在不断重构芯片访存流水线，让指数归一化以更高的能效运行在硬件之上。

## 结语

回到最初的数学事实，未归一化的 Logits 排序与 Softmax 后的概率排序分毫不差。

这种单调等价性给工程推理留下了宝贵的优化空间。在贪婪解码的极值提取中，在 Top-K 的前置粗排中，以及底层算子的内核融合中，系统都在尽可能延后或跳过显式的全局 Softmax 计算，榨取显存带宽。

但只要脱离了静态取极值的场景，系统就必须依赖标准概率分布。反向传播依赖有界且动态自适应的残差梯度，大语言模型生成依赖能够非线性调节信息熵的采样空间，工程系统依赖具备统一尺度的置信度来卡控拒答。

数学上的等价发生在极值确定的瞬间，而动态系统的运转需要完整的概率上下文。Softmax 并不是多余的计算开销，它是维系模型训练、随机采样与系统决策平稳运转的基础纽带。
