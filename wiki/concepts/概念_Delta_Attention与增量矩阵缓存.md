---
type: concept
tags:
- Infra/serving
- LLM/inference
- LLM/arch/attention
summary: Delta Attention（增量注意力）是 Kimi K3 采用的注意力优化机制，将历史 Token 的键值对关联折叠压缩进一个固定大小的矩阵中，通过
  Delta 规则进行关联的“先读后写，只写差值”更新，实现 $O(1)$ 的空间复杂度和 $O(N)$ 的计算复杂度。
sources:
- wiki/sources/2026-07-24_Delta-attention-in-Kimi-K3-to-fix-growing-KV-cache_19f962.md
updated: '2026-08-04'
---

# 概念：Delta Attention 与增量矩阵缓存

## 定义

**Delta Attention（增量注意力）** 是 Kimi K3 模型采用的一种新型注意力与上下文检索优化机制。它通过将不断增长的历史 KV 信息压缩并折叠进一个固定大小的矩阵（Fixed-size matrix）中，从而消除传统自回归解码中随着序列无限增加的 `[[概念_KV_Cache]]` 存储，解决长文本推理中的内存膨胀和计算复杂度问题。

## 机制对比：Delta Attention vs 传统 KV Cache

在传统的自回归解码中，由于注意力扫描需要对比所有历史 Token，我们需要在内存中不断追加保存历史 Token 的 Key 和 Value 对。

| 维度 | 传统 KV Cache 机制 | Delta Attention 机制 |
| :--- | :--- | :--- |
| **存储介质** | 动态增长的 KV 向量列表 | 固定大小的关联矩阵 (Fixed-size matrix) |
| **空间复杂度** | $O(N)$（随序列长度 $N$ 呈线性增长，显存开销极大） | **$O(1)$**（显存占用固定，不随序列长度增长而膨胀） |
| **计算复杂度** | $O(N^2)$（每个新 Token 需要扫描整个列表） | **$O(N)$**（每次新 Token 仅需对固定矩阵进行常数次矩阵乘法） |
| **检索特征** | **精确检索**（Exact Lookup，可回溯任意具体 Token 的精准状态） | **近似检索**（Approximate Lookup，有损压缩，召回为混合状态） |

## Delta Rule 的两步写逻辑

Delta Attention 能够在固定大小的矩阵中高效存储大量长文本关联，得益于其遵循的 **Delta 写入规则 (Delta Rule)**。当一个新 Token 的信息需要被矩阵“吸收”时，执行以下两步逻辑：

1. **先读后写 (Read-before-write)**：
   - 提取新 Token 的键（Key）输入到当前的关联矩阵中。
   - 读取并获取矩阵在当前状态下对该 Key 的预测值（即旧关联的预测输出/现有猜想）。
2. **只写差值 (Write the delta)**：
   - 将该预测值与当前 Token 的实际期望值（Value）进行比对，计算它们之间的差距，即 **Delta（差值）**。
   - 仅仅将这个 **Delta（差值）** 增量写入并修正进关联矩阵的权重，而不是直接叠加完整值。这相当于对已有的关联知识库进行修正与纠错，避免新信息在固定矩阵中产生无序堆叠导致溢出或前序知识被瞬间覆盖。
   - 随着时间推移，该矩阵还支持让老旧数据自然淡出（Fade），从而保证最相关的关联被留存。

## 局限性与混合交替方案 (Interleaving)

### 1. 局限性：精确召回退化
由于 Delta Attention 将超长上下文强制压缩至固定大小的矩阵，它在本质上是有损压缩。因此，它无法确保像传统注意力机制那样对某一个特定 Token 实现 100% 的精确召回（Exact Recall），而是表现为**近似召回（Approximate Recall）**。

### 2. 生产混合方案：交替编织 (Interleaving)
为了克服近似召回对某些高精度长文本检索场景（如大海捞针、精准事实问答）的负面影响，Kimi K3 在生产落地中没有完全抛弃传统注意力机制，而是采用了一种 **“混合交替编织（Interleaving）”** 方案：
- **少数全注意力层 (Exact Lookup Layers)**：依然使用传统的自回归 Attention，维持少量关键的 KV Cache，用于保证高精度的信息对齐与召回。
- **多数 Delta Attention 层 (Linear Layers)**：绝大多数层级使用 Delta Attention 线性计算，维持 $O(1)$ 的矩阵存储。
- 通过这种“全注意力与增量注意力”的交叉交替设计，在保证极长上下文高召回率的同时，大幅降低了模型的显存消耗和推理延迟。

## 关联
- [[概念_KV_Cache]]（传统注意力缓存方案）
- [[2026-07-24_Delta-attention-in-Kimi-K3-to-fix-growing-KV-cache_19f962]]（来源摘要）
