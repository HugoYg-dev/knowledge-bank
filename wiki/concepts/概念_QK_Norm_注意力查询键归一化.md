---
type: concept
tags:
- LLM/arch
summary: QK-Norm 是在多头注意力模块内部对 Query 和 Key 向量做归一化的技术，用于提升训练稳定性。
sources:
- wiki/sources/2025年七大顶流大模型架构.md
- wiki/sources/从DeepSeek-V3到Kimi_K2_八种现代LLM架构大比较.md
- wiki/sources/近6年的大模型架构，我挨个试了个遍.md
updated: '2026-11-04'
aliases:
- QK-Norm
- QK Norm
- QK归一化
- 概念_QK_Norm
---

# 概念_QK_Norm_注意力查询键归一化

QK-Norm 是在多头注意力模块内部对 Query 和 Key 向量做归一化的技术，用于提升训练稳定性。

## 实现方式

在应用 RoPE 位置编码之前，对 Q 和 K 各施加一层 RMSNorm：

```python
if self.q_norm:
    queries = self.q_norm(queries)   # RMSNorm on Q
if self.k_norm:
    keys = self.k_norm(keys)         # RMSNorm on K
# 然后再应用 RoPE
queries = apply_rope(queries, cos, sin)
keys = apply_rope(keys, cos, sin)
```

## 作用

- 防止 Q/K 向量数值过大导致注意力分数 Softmax 饱和（梯度消失）
- 与 Post-Norm 组合使用（OLMo 2）可显著稳定训练损失曲线
- 即使不使用精心设计的学习率预热，也能保持稳定训练
- **自适应注意力熵调节（1000+ 消融实验实证）**：Nikita Pavlichenko 在 6 年架构超级消融中指出，在所有归一化变体中，QK-norm 是**唯一在大尺寸模型上仍能稳定提升约 1% 效果**的改动。其更深层的物理机制是赋予模型自主学会“注意力该多集中”的自适应能力，而不仅是单纯防止数值溢出。

## 应用模型

- **OLMo 2**（Allen AI）：QK-Norm + Post-Norm 组合
- **Qwen3**：同样使用 QK-Norm
- **2026 混合基准模型**：将其作为必备标准件与细粒度 MoE 搭配使用

## 相关来源

- [[从DeepSeek-V3到Kimi_K2_八种现代LLM架构大比较]]
- [[2025年七大顶流大模型架构]]
- [[近6年的大模型架构，我挨个试了个遍]]

## 关联概念

- [[概念_Normalization方法对比]] — BN/LN/RMSNorm 整体对比
- [[概念_自注意力复杂度]] — 注意力机制基础