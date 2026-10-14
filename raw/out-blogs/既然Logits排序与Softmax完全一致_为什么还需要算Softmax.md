---
title: 既然 Logits 排序与 Softmax 完全一致，为什么我们还需要算 Softmax？
author:
  - "[[Hugo Yang]]"
published: 2026-09-23
created: 2026-09-23
draft: true
description: 揭示深度学习体系中数学直觉与工程实践的反差，从严格单调性出发，拆解模型训练、大模型采样生成、工业推理优化与现实决策对 Softmax 的底层依赖。
tags:
  - LLM/inference
  - LLM/arch
---
# 既然 Logits 排序与 Softmax 完全一致，为什么我们还需要算 Softmax？

> **草稿定位**：面向算法工程师、大模型推理/系统优化从业者、深度学习进阶学习者的深度技术博客草稿。  
> **核心命题**：揭示深度学习体系中“数学直觉”与“工程实践”之间的反差——从严格单调性出发，拆解模型训练、大模型采样生成、工业推理优化与现实决策对 Softmax 的底层依赖。  
> **备选标题**：
> 1. 《既然 Logits 排序与 Softmax 一模一样，为什么我们还要算 Softmax？》
> 2. 《破除理所当然：为什么深度学习死磕 Softmax，而不是直接拿 Logits 排序？》
> 3. 《Logits 是内心独白，Softmax 是外交辞令：一次关于概率、梯度与大模型采样的深度复盘》

---

## 0. 写作灵感与核心洞察（Core Insight）

在构建分类模型或大模型解码时，有一个几乎所有人都见过、却很少停下来深究的数学事实：

假设最后一层线性头输出的未归一化分值向量（Logits）为 $z = [z_1, z_2, \dots, z_K]$，经过 Softmax 变换后得到的概率向量为 $p = [p_1, p_2, \dots, p_K]$：

$$p_i = \text{Softmax}(z)_i = \frac{e^{z_i}}{\sum_{j=1}^K e^{z_j}}$$

因为指数函数 $f(x) = e^x$ 在整个实数域上都是**严格单调递增**的，而分母 $\sum_{j=1}^K e^{z_j}$ 是一个对所有类别共享的正数常量，因此必然有：

$$z_i > z_j \iff p_i > p_j$$

**这意味着：未归一化的 Logits 的大小排序，与经过 Softmax 计算后的概率分布排序在数学上完全等价！**

如果你只是想知道模型认为“哪个类别最可能”，或者想把所有候选类别按可能性从大到小排个序，Logits 提供的排序结果和 Softmax 没有一丁点差别。

那么问题来了：
**计算 Softmax 既需要做昂贵的指数运算（`exp`），还要面临浮点数上溢/下溢（Overflow/Underflow）的风险，在大词表（如 128k/150k）下甚至会占用大量显存与访存带宽——既然排序完全一致，为什么深度学习体系还要大费周章地去算 Softmax？直接用 Logits 不香吗？**

---

## 1. 结构大纲与叙事节奏（Narrative Arc）

本文采用“**认知反转 $\to$ 工程揭秘 $\to$ 数学本质 $\to$ 生成哲学 $\to$ 现实落地**”的层层递进结构：

1. **破除盲从：工业界什么时候“坚决不算”Softmax？**
   - 贪婪解码（Greedy Decoding）与 Argmax 直通
   - 推理引擎（vLLM / TensorRT-LLM / llama.cpp）的 Top-K 剪枝优化（先截断再局部归一化）
   - 训练期的算子融合（`nn.CrossEntropyLoss` 为什么禁止你先传 Softmax）
2. **训练之核：为什么反向传播非 Softmax 不可？**
   - 如果直接在 Logits 上做排序约束（Ranking Loss / Margin Loss），梯度动力学会发生什么崩溃？
   - Softmax + 交叉熵损失的极简数学美：$\frac{\partial \mathcal{L}}{\partial z_i} = p_i - y_i$ 的动态自适应与曲面凸性
3. **生成之魂：大模型不是“选最大”，而是“掷骰子”**
   - 贪婪搜索的死穴：文本退化、复读机与多样性丧失
   - 为什么不能对 Logits 掷骰子？（柯尔莫哥洛夫公理、负数与概率单纯形）
   - 温度（Temperature）的几何本质：为什么只有指数结构才能调节信息熵？
   - Top-p（核采样 / Nucleus Sampling）的硬约束：无量纲数值无法定义“置信区间”
4. **现实接口：无界无量纲 vs. 跨样本置信度与拒答**
   - Logits 的尺度无关性缺陷（Scale Invariance Defect）：样本间数值不可比
   - 模型校准（Calibration）与置信度门禁：企业级 Agent 何时该“拒答并转人工”？
5. **统计学底层：最大熵原理与玻尔兹曼分布**
   - 广义线性模型（GLM）与自然参数的规范链接函数（Canonical Link Function）
6. **升华总结**：Logits 是内心独白，Softmax 是外交辞令。

---

## 2. 章节草稿与核心论据展开

### 第一幕：工业界的“偷懒”——什么时候我们确实坚决不算 Softmax？

写技术博客最怕教条主义。在解释为什么需要 Softmax 之前，先给读者来一个**认知反转**：很多时候，大家确实不用它！

#### 1. 贪婪推理（Greedy Decoding）与 Top-1 预测
在传统的图像分类、意图识别，或者大模型的 Greedy Search 阶段，我们只需要概率最大的那一项：

$$\arg\max_i (p_i) = \arg\max_i (\text{Softmax}(z)_i) = \arg\max_i (z_i)$$

因为单调性，任何成熟的推理引擎（ONNX Runtime、TensorRT、vLLM）在执行 Greedy Decoding 时，代码直接走的是 `argmax(logits)`。
在这里，算 Softmax 纯粹是浪费 FLOPs 和显存读写带宽。

#### 2. 大模型 Top-K 采样的“偷梁换柱”
现代大模型的词表动辄 128,000 到 150,000。如果在每一步解码生成时，都对 15 万维的浮点向量做一次全局 Softmax：
- 需要计算 15 万次 $\exp$；
- 需要做一次跨线程块的规约求和（Reduction Sum）；
- 需要写回显存。

实际上，vLLM 和 llama.cpp 的经典优化做法是：
1. **直接在 Logits 上跑 Top-K 算子**（通过快速选择算法 QuickSelect 或 GPU 局部堆，在 Logits 阶段直接把候选集砍到前 50 个）；
2. **只对这 50 个候选值做局部 Softmax 归一化**：
   $$\tilde{p}_k = \frac{e^{z_k}}{\sum_{j=1}^{50} e^{z_j}}, \quad k \in \text{Top-}K$$
全量 Softmax 在推理层被彻底规避了。

#### 3. 训练时的算子融合与数值稳定
即便在训练阶段，工程师也极力避免“先算 Softmax，再求对数”。
PyTorch 的 `nn.CrossEntropyLoss` 在文档里反复强调：**输入必须是未归一化的 Logits，严禁手动传入经过 Softmax 的结果。**

原因在于经典的 **Log-Sum-Exp 技巧与算子融合**：

$$\log p_i = z_i - \log \sum_j e^{z_j} = z_i - \left( c + \log \sum_j e^{z_j - c} \right), \quad \text{其中 } c = \max_j(z_j)$$

如果先算 Softmax，大数值会发生上溢（变成 `inf`），小数值会下溢（变成 `0`），再取 $\log$ 就会产生大量的 `NaN`。而在底层 CUDA kernel 中，`LogSoftmax` 和 `NLLLoss` 是融合成一个算子执行的，既防止数值溢出，又减少了一次昂贵的中间显存读写（HBM 往返）。

---

### 第二幕：训练之核——为什么反向传播非 Softmax 不可？

既然推理时能省则省，那为什么整个深度学习的训练基石仍然牢牢锁死在 Softmax 之上？

答案在于：**为了那一行在数学上近乎奇迹的梯度。**

#### 1. 如果直接在 Logits 上做排序（Ranking / Margin Loss）会怎样？
有人可能会问：既然我们只要正确的类别排序靠前，为什么不直接在 Logits 上用类似 SVM 的 Hinge Loss，或者排序学习（Learning to Rank）的损失函数？比如：

$$\mathcal{L}_{\text{hinge}} = \max(0, \max_{j \neq y}(z_j) - z_y + \Delta)$$

这在深度神经网络中会遇到严重的训练动力学问题：
- **梯度稀疏与断崖**：一旦正确类别的 logit 比其他类别高出阈值 $\Delta$，损失瞬间变为 0，梯度直接归零。网络停止在该样本上继续学习，无法进一步拉大置信度差距，难以学到深层的泛化表征。
- **极端错误时缺乏自适应放大**：当预测严重错误时，Hinge Loss 的梯度通常是常数（$\pm 1$），无法像指数函数那样在面对离谱错误时产生强烈的回传动力。

#### 2. Softmax + 交叉熵：梯度动力学的极致优雅
当我们使用 Softmax 配合负对数似然（交叉熵损失）时：

$$\mathcal{L} = -\log p_y = -\log \frac{e^{z_y}}{\sum_j e^{z_j}} = -z_y + \log \sum_j e^{z_j}$$

对未归一化的输入分值 $z_i$ 求偏导：

$$\frac{\partial \mathcal{L}}{\partial z_i} = - \mathbb{I}(i = y) + \frac{\frac{\partial}{\partial z_i} \left( \sum_j e^{z_j} \right)}{\sum_j e^{z_j}} = - \mathbb{I}(i = y) + \frac{e^{z_i}}{\sum_j e^{z_j}} = p_i - y_i$$

这里的导数形式简练到了极致：
$$\nabla_z \mathcal{L} = \mathbf{p} - \mathbf{y}$$

这个公式的物理意义极其优美：**回传给第 $i$ 个神经元的梯度，恰好就是“预测概率与真实标签的直接残差”！**

- **动态平滑自适应**：
  - 如果模型预测正确且非常自信（$p_y \approx 0.99$），残差 $0.99 - 1 = -0.01$，梯度微乎其微，平稳收敛；
  - 如果模型错得很离谱（比如真实类别概率 $p_y \approx 0.001$，而错误类别 $p_k \approx 0.95$），残差迅速放大，产生极强的推力拉回权重。
- **全局竞争机制**：
  分母上的 $\sum e^{z_j}$ 使得所有类别处于零和博弈中。提高某一个类别的 logit，不仅自身概率增加，还会自然压低其他所有负样本的概率。这种全局竞争是仅靠单类独立排序无法达到的。

---

### 第三幕：生成之魂——大模型不是“选最大”，而是“掷骰子”

如果模型只做 Top-1 确定性预测（比如传统二分类），我们可能真的能把 Softmax 边缘化。
但在生成式大语言模型（LLM）的时代，**Softmax 构成了整个自回归生成的“灵魂”**。

#### 1. 为什么不能永远选最大？（破除 Greedy）
如果大模型在生成每句话时都选择当前概率最大的词（Greedy Search）：
- 文本会迅速陷入**死循环与机械重复**（例如反复打印同一句口头禅）；
- 输出缺乏任何创造性和文学色彩。

大模型的灵动感，来自于**随机采样（Sampling）**。生成的过程，本质上是在词表空间上不断掷骰子。

#### 2. 无法对 Logits 掷骰子：柯尔莫哥洛夫公理系统的硬约束
为什么不能直接基于 Logits 掷骰子？
- **取值范围**：Logits 是无界的实数，范围在 $(-\infty, +\infty)$。它可能是负数，甚至全为负数（例如 $[-12.5, -8.3, -20.1]$）。
- **概率测度**：根据现代概率论的柯尔莫哥洛夫公理，一个合法的离散概率分布必须满足两条铁律：
  1. **非负性**：$p_i \ge 0$
  2. **归一性**：$\sum_i p_i = 1$
Logits 无法直接作为多项式分布（Multinomial Distribution）的采样权重。而 Softmax 中的 $\exp(z_i)$ 强制保证了非负性，分母归一化强制保证了总和为 1，将无边界的欧氏空间完美映射到了**标准概率单纯形（Standard Probability Simplex）**上。

#### 3. 温度系数（Temperature）的几何变形记
在大模型调参中，最重要的参数莫过于 Temperature（$T$）：

$$p_i = \frac{e^{z_i / T}}{\sum_j e^{z_j / T}}$$

为什么除以一个标量 $T$ 就能调节模型是“严谨求实”还是“天马行空”？
- **物理原型**：这直接脱胎于统计力学中的玻尔兹曼分布（Boltzmann Distribution），其中能量态占据概率为 $P(E) \propto e^{-E / k_B T}$。
- **当 $T \to 0$**：任何微小的 logit 差异在指数放大后都会变成悬殊的天堑，分布极度尖锐化，退化为确定性的 Dirac $\delta$ 函数（即 Argmax）；
- **当 $T \to \infty$**：所有的 $z_i / T \to 0$，$e^0 = 1$，分布被彻底抹平成均匀分布（Uniform Distribution），模型在词表中完全盲目瞎选；
- **当 $T = 1$**：保持标准模型内在信息熵。

**关键在于**：只有在指数函数架构下，给 Logits 除以标量 $T$，才能在保留排序顺序的同时，非线性地调节分布的信息熵（Entropy）与方差。如果直接在线性 Logits 上做除法，排序和相对比例丝毫不变，根本无法实现温度调节的效果。

#### 4. Top-p（核采样 / Nucleus Sampling）的依赖
目前业界最流行的采样策略是 Top-p（截取累积概率达到阈值 $p$ 的最小候选集合，通常 $p=0.9$）：

$$\sum_{i \in V^{(p)}} p_i \ge p$$

因为 Logits 是没有量纲和基准的抽象分值，**根本不存在“前 90% 置信区间”的概念**。你无法在 Logits 空间里回答“累加到多少算涵盖了绝大部分可能性”，这一操作只能在概率测度空间中完成。

---

### 第四幕：现实接口——无界无量纲 vs. 跨样本置信度与拒答

在工程落地中，不仅“选词”需要概率，“决策”更需要概率。

#### 1. Logits 的尺度无关性缺陷（Scale Invariance Defect）
Logits 是一个没有绝对基准的无量纲数值。
看一个直观的反例：

- **场景 A**：模型输出的 Top-2 Logits 为 `[12.0, 10.0]`，差值为 `2.0`。
- **场景 B**：模型输出的 Top-2 Logits 为 `[2.0, 0.0]`，差值也是 `2.0`。

请问：模型在场景 A 的第一名上，和在场景 B 的第一名上，置信度是一样的吗？

**完全无法判断！**
因为神经网络的最后一层是线性映射 $z = W h + b$。如果模型把权重矩阵 $W$ 整体缩放 10 倍，Logits 的差值就会从 2 变成 20；如果缩放 0.1 倍，差值就会变成 0.2。
神经网络内部没有任何机制去强制约束 Logits 的绝对尺度。在不同输入样本之间，或者在模型微调迭代的不同 checkpoint 之间，**直接比较 Logits 的绝对大小毫无意义**。

#### 2. 模型校准（Calibration）与风控拒答
在医疗诊断、金融风控或企业级 Agent 任务中，我们必须回答一个现实问题：**“模型到底有多确信自己的回答？”**

企业级落地常见的业务规则是：
> “如果模型预测的最高类别置信度低于 0.85，系统必须判定为低置信度，触发拒答机制（Abstention）并转交人工审核。”

如果要设定这样一个跨请求全局生效的硬阈值，输入值必须满足：
1. **有界性**（固定在 $[0, 1]$ 之间）；
2. **频率学意义的可比性**（即预测置信度为 0.9 的样本中，确实有约 90% 是真实的正确样本）。

通过 Softmax，结合后处理校准技术（如 Platt Scaling 或 Temperature Scaling 针对 ECE 期望校准误差进行优化），我们才能把网络内部那堆狂野的浮点数，转化成业务系统能够理解并制定契约的“置信度”。

---

### 第五幕：统计学的深层归宿——为什么偏偏是 Softmax？

很多人可能会追问最后一个底牌：
既然我们要非负、要归一化、要能采样，为什么非得用 $e^x$？用其他单调非负函数不行吗？比如：

$$\tilde{p}_i = \frac{z_i^2}{\sum_j z_j^2} \quad \text{或者} \quad \tilde{p}_i = \frac{\text{ReLU}(z_i)}{\sum_j \text{ReLU}(z_j)}$$

为什么在整个机器学习史上，Softmax 几乎占据了绝对统治地位？

#### 1. 广义线性模型（GLM）的自然选择
在统计学中，分类任务面对的是**多项分布（Multinomial Distribution）**。
多项分布属于指数族分布（Exponential Family）。当我们将多项分布写成指数族的标准形式时：

$$P(y=i \mid \eta) = \exp \left( \eta_i - A(\eta) \right)$$

我们会发现，其**自然参数（Natural Parameters）** $\eta_i$ 与分类概率 $p_i$ 之间的映射关系，其**规范链接函数（Canonical Link Function）的逆函数正是 Softmax！**
换句话说，Logits 本质上就是多项分布的自然参数 $\eta$。从信息几何的角度看，Softmax 不是人为生造的凑巧方案，而是指数族分布固有的代数结构。

#### 2. 最大熵原理（Maximum Entropy Principle）
在信息论奠基人 Jaynes 提出的最大熵原理中：
> 当我们在只知道部分先验约束（例如一阶矩/期望值）的情况下对未知系统进行建模时，最客观、引入先验偏见最少的分布，就是**使香农信息熵最大化的分布**。

在离散多状态系统中，利用拉格朗日乘子法求解带有均值约束的最大熵优化问题，解出的解析形式必然是吉布斯分布（即 Softmax 的数学形式）。
**Softmax 是在给定特征约束下，对不确定性最诚实的表达。**

---

## 3. 典型代码示例与工程复现参考

在正文中可穿插以下清晰的最小工程验证代码，增加技术扎实度：

### 示例 1：验证单调性与贪婪解码的等价性
```python
import torch

# 假设 1 个样本，5 个类别的 Logits
logits = torch.tensor([[2.3, -1.2, 5.8, 0.4, 5.799]])

# 方式 A：直接在 Logits 上取 Top-1
top1_logit_idx = torch.argmax(logits, dim=-1)

# 方式 B：经过 Softmax 之后再取 Top-1
probs = torch.softmax(logits, dim=-1)
top1_prob_idx = torch.argmax(probs, dim=-1)

# 方式 C：Top-K 排序
topk_logits_idx = torch.topk(logits, k=3, dim=-1).indices
topk_probs_idx = torch.topk(probs, k=3, dim=-1).indices

assert top1_logit_idx == top1_prob_idx
assert torch.equal(topk_logits_idx, topk_probs_idx)
print("数学验证：Logits 排序与 Softmax 排序完全一致！")
```

### 示例 2：展示温度调节与核采样对概率空间的硬性依赖
```python
def sample_next_token(logits: torch.Tensor, temperature: float = 0.8, top_p: float = 0.9):
    # 1. 温度调节（改变相对熵）
    scaled_logits = logits / temperature
    
    # 2. 必须借助 Softmax 投影到概率测度空间
    probs = torch.softmax(scaled_logits, dim=-1)
    
    # 3. Top-p 必须在累积概率上计算截断
    sorted_probs, sorted_indices = torch.sort(probs, descending=True)
    cumulative_probs = torch.cumsum(sorted_probs, dim=-1)
    
    # 移除累积概率超过 top_p 的多余 token
    sorted_indices_to_remove = cumulative_probs > top_p
    # 保证至少保留一个候选词
    sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
    sorted_indices_to_remove[..., 0] = 0
    
    indices_to_remove = sorted_indices[sorted_indices_to_remove]
    scaled_logits[..., indices_to_remove] = -float('Inf')
    
    # 重新归一化并进行多项式采样（掷骰子）
    final_probs = torch.softmax(scaled_logits, dim=-1)
    next_token = torch.multinomial(final_probs, num_samples=1)
    return next_token
```

---

## 4. 金句与总结升华（Conclusion）

在文章末尾，可以用一段精辟的类比为整篇博客收尾：

> **“如果把神经网络看作一个正在思考的人：  
> 未经归一化的 Logits，是它脑海深处未经修饰的神经电信号与内心独白——嘈杂、无界、充满相对冲动；  
> 而 Softmax，则是它向人类的概率公理系统、梯度反传动力学以及现实业务决策所递交的一份标准‘外交辞令’。  
> 
> 在自己跟自己对话时（比如贪婪解码中只要最强的一个念头），它确实可以省掉外交辞令直接读取直觉；  
> 但只要涉及到与世界交互——无论是向梯度认错、在多选一里充满灵性地掷骰子，还是向人类汇报确定性置信度，它都必须跨过 Softmax 这座精妙的数学桥梁。”**

---

## 5. 后续扩展方向与延伸阅读

- **替代方案探讨**：
  - Sparsemax / Entmax：能否彻底将低概率直接置为硬零？
  - Taylor Softmax：在特定边缘芯片上如何规避昂贵的指数计算？
- **硬件与算子演进**：
  - FlashAttention 中对于 Softmax 的 Online Safe Softmax 重计算分块优化（Milakov & Gimelshein 技巧与 Tri Dao 的突破）。
