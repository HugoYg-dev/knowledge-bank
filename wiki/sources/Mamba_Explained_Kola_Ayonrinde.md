---
type: source
tags:
- LLM/arch/Mamba
summary: 从直觉出发解释 Mamba：效率/有效性 Pareto 前沿、选择机制类比、状态即压缩、State Swapping 新推理范式及可解释性分析
sources:
- raw/articles/Mamba Explained _ Kola Ayonrinde.md
updated: '2026-07-01'
---
## 来源信息

- **标题**：Mamba Explained
- **作者**：Kola Ayonrinde
- **URL**：https://www.kolaayonrinde.com/blog/2024/02/11/mamba.html

## 核心要点

- Transformer 核心问题：KV cache 存储全部历史，前向传播 O(n²) 时间、O(n) 空间；长上下文时延迟和内存双双爆炸
- 好的序列模型需要两类操作：token 间 Communication（Transformer 用 Attention，Mamba 用 SSM）和 token 内 Computation（两者都用 MLP 式投影）
- SSM 来自控制论：h'(t)=Ah(t)+Bx(t)，y(t)=Ch(t)+Dx(t)；A 是遗忘矩阵，B 是输入编码，C 是输出解码，Δ 是"停留时间"（linger time）
- 效率/有效性权衡：RNN 高效但不有效（遗忘太多）；Transformer 有效但不高效（存全部历史）；Mamba 用选择机制推进 Pareto 前沿
- 选择机制（Selectivity）：让 A、B、C 成为输入 x 的函数（A=Aθ(x)），使模型可以在"记忆生成时"而非"回忆时"过滤信息——与人类记忆类似
- 非选择性 SSM 可以写成卷积形式（FFT 加速），但选择机制打破卷积形式，需要硬件感知算法补偿效率损失
- 状态是压缩（state is compression）：state size 越小越高效；越大越有效；关键是用选择机制动态压缩
- 类比政治经济学：RNN 无政府主义（最小状态）；Transformer 共产主义（最大状态，全缓存）；Mamba 精简有效政府（小但精准的状态）
- Mamba-3B 在预训练和下游任务上超过同参数量 Transformer，并与 2× 参数量 Transformer 相当
- 推理速度：最高 5× 快于同等 Transformer
- State Swapping 新范式：预先对专业数据集运行推理生成 state，可直接复用（无需 backprop，无 few-shot 例子）；类似 LoRA 插件
- 可解释性：Mamba 的 token 通信通过隐状态而非 Attention 矩阵；IOI（间接宾语识别）任务中信息经隐状态路径传递已有实验验证
- 未来场景：超长上下文（DNA、视频、小说）、长期记忆 Agent；混合 Mamba+Transformer 架构（短程用 Attention，长程用 SSM）

## 关键引文

- "For the first time, Mamba promises similar performance (and crucially similar scaling laws) as the Transformer whilst being feasible at long sequence lengths (say 1 million tokens)."
- "The efficiency vs. effectiveness tradeoff of sequence models is characterized by how well they compress their state: efficient models must have a small state, while effective models must have a state that contains all necessary information from the context."
- "Transformers decide what's relevant at recall time. The innovation of Mamba is allowing the model better ways of forgetting earlier — focusing by choosing what to discard using Selectivity, throwing away less relevant information at memory-making time."

## 关联

- [[概念_Mamba选择机制]] — Selectivity 核心原理
- [[概念_状态空间模型SSM]] — SSM 数学基础
- [[概念_SSM离散化]] — ZOH 离散化与步长 Δ
- [[概念_Mamba硬件感知算法]] — 弥补选择机制丧失卷积加速的效率损失
- State_Swapping — Mamba 特有的新推理范式
- [[实体_Mamba]] — Mamba 模型

---
> 📎 **物理文献**：[[raw/articles/Mamba Explained _ Kola Ayonrinde.md]]