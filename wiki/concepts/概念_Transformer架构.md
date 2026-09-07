---
type: concept
tags:
- LLM/arch
- DeepLearning
summary: Google 2017 提出的深度学习模型，通过自注意力机制捕捉序列中各元素之间关系。当前大语言模型的主流架构。
sources:
- wiki/sources/Discrete_Tokenization多模态综述.md
- wiki/sources/Transformer大模型3D可视化_NanoGPT.md
- wiki/sources/向量数据库原理与应用全解析.md
- wiki/sources/大模型幻觉陷阱_AGI之路04期.md
- wiki/sources/大模型显存计算公式与优化.md
updated: '2026-09-07'
---

# 概念：Transformer 架构


## 定义

Google 2017 提出的深度学习模型，通过自注意力机制捕捉序列中各元素之间关系。当前大语言模型的主流架构。

## 5 步流程（全文描述）

1. **Tokenization**：文字转 token（最小处理单位），token list 提前人工设置，各模型不同
2. **Input Layer（Embedding）**：
   - token 转向量（高维映射到低维空间），训练获得的参数，使用时查表
   - 接近的 Embedding 其 token 意思相近
   - 还需位置信息（同字不同位置含义差别大）
3. **Attention（理解上下文）**：
   - Attention Weight：token 间相关性得分
   - Attention Matrix：所有 token 两两计算
   - Causal Attention：只考虑左边 token
   - Multi-head Attention：多角度（多投影平面）计算相关性，保留更多原始信息
4. **Feed Forward（整合思考）**：前馈网络提供非线性变换，整合多维信息提取复杂特征
   - Attention + Feed Forward = Transformer Block，实际多层堆叠
5. **Output Layer**：Linear Transform 映射到词汇表大小 → Softmax 归一化为概率分布

## 关键特性

- 输出是归一化概率分布词汇表 → 每次输出结果不同（概率采样）
- 文字接龙：用分类策略解决生成式问题

## 来源
