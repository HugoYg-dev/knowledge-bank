---
type: concept
tags:
- LLM/arch
summary: QK-Norm 是在多头注意力模块内部对 Query 和 Key 向量做归一化的技术，用于提升训练稳定性。
sources:
- wiki/sources/2025年七大顶流大模型架构.md
- wiki/sources/从DeepSeek-V3到Kimi_K2_八种现代LLM架构大比较.md
updated: '2026-09-21'
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

## 应用模型

- **OLMo 2**（Allen AI）：QK-Norm + Post-Norm 组合
- **Qwen3**：同样使用 QK-Norm

## 相关来源

- [[从DeepSeek-V3到Kimi_K2_八种现代LLM架构大比较]]
- [[2025年七大顶流大模型架构]]

## 关联概念

- [[概念_Normalization方法对比]] — BN/LN/RMSNorm 整体对比
- [[概念_自注意力复杂度]] — 注意力机制基础