---
type: concept
tags:
- LLM/arch/attention
- LLM/inference
summary: MLA（Multi-head Latent Attention）：DeepSeek V2/V3 提出的低秩 KV 压缩方案，通过矩阵吸收使注意力计算时
  K/V 不含头信息，兼具 MQA 效率和 MHA 表达能力
sources:
- wiki/sources/DeepSeek_MLA矩阵吸收原理.md
- wiki/sources/KV_Cache原理图解.md
- wiki/sources/MiniMax_vs_Kimi_注意力路线之争.md
updated: '2026-06-29'
---


# 概念：MLA 低秩 KV 压缩

MLA（Multi-head Latent Attention）是 DeepSeek V2/V3 提出的注意力机制，通过**低秩压缩 + 矩阵吸收**，在减少 KV Cache 显存的同时保留 MHA 的表达能力。

## 核心机制

### 低秩投影
- KV 不直接展开，而是先降秩投影得到 `compressed_kv`（低维潜在向量）
- 升维矩阵（`k_up`、`v_up`）通过矩阵吸收延迟处理

### 矩阵吸收
核心优化：将 K/V 的升维矩阵**吸收进 Q**，使注意力计算时 K/V 不含头维度，退化为广播计算（减少内存访问）

三处广播优化：
1. Q_rope @ K_rope^T：k_rope 头维度=1
2. Q_nope @ compressed_kv^T：compressed_kv 无头信息
3. attn_weights @ compressed_kv：同上

### RoPE 解耦
- 输入拆分为需要位置编码（rope）和不需要（nope）两部分
- KDA/NoPE 等方案在此基础上进一步简化

## 与其他 KV 共享方案对比

| 方案 | KV Cache 大小 | 信息损失 | 多头 |
|------|-------------|---------|------|
| MHA | 全量 | 无 | 是 |
| GQA | 1/G | 有 | 分组 |
| MQA | 最小 | 较大 | 否 |
| MLA | 低秩 | 极小 | 是（升维矩阵多头） |

## 显存效益

MLA 继承了 MQA 的 KV 共享优势，KV Cache 仅存 `compressed_kv`（低秩），但通过多头升维矩阵极大保留了信息表达。

## 参见

- [[概念_KV_Cache_键值缓存]]
- [[DeepSeek_MLA矩阵吸收原理]]
- [[MiniMax_vs_Kimi_注意力路线之争]] — Kimi Linear 中 MLA 作为混合架构组件
- [[实体_DeepSeek_V2]]