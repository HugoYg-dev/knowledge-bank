---
type: source
tags:
- LLM/arch
summary: 软件工程师Brendan Bycroft制作的LLM 3D可视化网站，逐层展示GPT-3/NanoGPT的Embedding/LN/Self-Attention/MLP/Softmax工作原理
sources:
- raw/articles/矩阵模拟！Transformer大模型3D可视化，GPT-3、Nano-GPT每....md
updated: '2026-07-01'
---
# 矩阵模拟！Transformer大模型3D可视化，GPT-3、Nano-GPT每一层清晰可见

## 来源信息

- **标题**：矩阵模拟！Transformer大模型3D可视化，GPT-3、Nano-GPT每一层清晰可见
- **来源平台**：微信公众号 新智元
- **URL**：https://mp.weixin.qq.com/s/UtNLpJc0SlIowuHGbJ8SRg
- **原始项目**：https://bbycroft.net/llm
- **作者**：Brendan Bycroft（软件工程师，受 Andrej Karpathy minGPT 和 Neural Networks Zero to Hero 启发）

## 核心要点

- **可视化项目概述**：网站 bbycroft.net/llm 提供 GPT-3（175B）、GPT-2 各规格（XL 15B / Small 1.24B）、NanoGPT（85584参数）的完整3D可视化，每个绿色单元格为正在处理的数字，蓝色单元格为权重
- **演示任务**：NanoGPT 对六字母序列「CBABBC」排序为「ABBBCC」，逐步展示推理（非训练）过程

### Embedding（嵌入层）
- token index 通过查表选取 token 嵌入矩阵对应列（C=48维向量）
- 同一 token 的位置嵌入与 token 嵌入相加，得到输入嵌入矩阵（TxC），T为序列长度

### Layer Norm
- 对输入嵌入矩阵每列独立归一化：均值为0、标准差为1；再乘以学习权重γ加偏置β
- 目的：提升深层网络训练稳定性

### Self-Attention（自注意力）
- 每列生成 Q（查询）、K（键）、V（值）三个向量（矩阵-向量乘法加偏置）
- Q与前序各列K做点积，结果除以 sqrt(A) 防止大值主导 softmax；softmax归一化后得注意力权重
- 因果掩码：只能查找过去的K，不预见未来（causal self-attention）
- 输出向量 = 注意力权重加权的V向量之和；多头输出堆叠后投影

### MLP（前馈网络）
- LayerNorm → 线性变换扩展到 4×C → GELU激活 → 线性变换回C → 残差连接
- GELU比ReLU平滑，适合神经网络引入非线性

### Softmax 输出
- 最后一个Transformer块输出经LayerNorm → 线性变换到nvocab维度（logits）
- Softmax将logits转化为概率分布；softmax数值稳定处理：减去最大值再指数化
- 温度参数控制分布平滑度：高温更均匀，低温更集中在概率最高token
- 从最后一列概率分布采样得到下一个token，追加回输入循环

### 规模对比
- NanoGPT: 85,584 参数；GPT-2 Small: 1.24亿参数；GPT-2 XL: 150亿参数；GPT-3: 1750亿参数（96层，8列密密麻麻）

## 关联

### 概念
- [[概念_Transformer架构]] — Transformer 5步流程与本文逐层拆解直接对应
- [[概念_自注意力复杂度]] — 自注意力计算复杂度原理
- [[概念_FlashAttention_快速注意力]] — 自注意力的I/O优化
- [[概念_KV_Cache_键值缓存]] — K/V缓存推理加速机制
- [[概念_Normalization方法对比]] — LayerNorm在Transformer中的位置
- [[概念_梯度下降优化器]] — 模型训练所用优化器

### 实体
- [[实体_PyTorch]] — NanoGPT / minGPT 的实现框架

---
> 📎 **物理文献**：[[raw/articles/矩阵模拟！Transformer大模型3D可视化，GPT-3、Nano-GPT每....md]]