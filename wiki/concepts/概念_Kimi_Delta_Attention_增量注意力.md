---
type: concept
tags:
- LLM/arch/attention
- LLM/inference
summary: 月之暗面（Kimi）Delta Attention 增量注意力体系：涵盖 Kimi Linear 的通道级门控 KDA（效率比 DPLR 提升 100%）与 Kimi K3 的固定矩阵增量缓存（Delta Rule 先读后写只写差值，实现 O(1) 空间与 O(N) 计算）。
sources:
- wiki/sources/MiniMax_vs_Kimi_注意力路线之争.md
- wiki/sources/2026-07-24_Delta-attention-in-Kimi-K3-to-fix-growing-KV-cache_19f962.md
updated: '2026-11-16'
aliases:
- Kimi Delta Attention
- Delta Attention
- 增量注意力
- 增量矩阵缓存
- 概念_Kimi_Delta_Attention
- 概念_Delta_Attention与增量矩阵缓存
---

# 概念_Kimi_Delta_Attention_增量注意力

## 基本信息

- **来源**：月之暗面，Kimi Linear 技术报告
- **基础**：Gated DeltaNet（GDN）

## 核心改进

| 维度 | 标准 Gate | KDA |
|------|----------|-----|
| 门控粒度 | scalar gate（标量，一个开关） | **channel-wise gate（通道级，每维独立）** |
| 遗忘因子 | 全局统一 | 每特征维度独立 |
| 计算效率 | DPLR 基准 | 约 **+100%** |

## 验证实验

在三个合成任务上测试（对比 GDN 和 Mamba2）：
- **Palindrome**（回文）：KDA 100% 准确
- **MQAR**（多查询关联回忆）：KDA 100% 准确
- **Stack**（栈追踪）：KDA 100% 准确
- GDN 和 Mamba2 在长序列上失败

## 工程化

- KDA 算子已整合进 vLLM 官方主代码库

## 演进与机制：Delta Attention 与增量矩阵缓存（Kimi K3）

Kimi K3 进一步阐述了基于 **Delta Rule（先读后写、只写差值）** 的固定大小矩阵缓存机制，旨在消除传统自回归解码中随序列长度线性增长的 [[concepts/概念_KV_Cache_键值缓存|KV Cache]] 存储开销：

| 维度 | 传统 KV Cache 机制 | Delta Attention 机制 |
| :--- | :--- | :--- |
| **存储介质** | 动态增长的 KV 向量列表 | 固定大小的关联矩阵（Fixed-size matrix） |
| **空间复杂度** | $O(N)$（随序列长度增长） | **$O(1)$**（显存占用固定） |
| **计算复杂度** | $O(N^2)$（每步扫描历史列表） | **$O(N)$**（每步对固定矩阵做常数次乘法） |
| **检索特征** | 精确检索（Exact Lookup） | 近似检索（Approximate Lookup，有损压缩） |

- **Delta Rule 两步写入逻辑**：
  1. **先读后写（Read-before-write）**：将新 Token 的 Key 输入当前关联矩阵，读取矩阵对该键的旧有关联预测值；
  2. **只写差值（Write the delta）**：计算预测值与当前真实 Value 之间的差值（Delta），仅将差值增量写入矩阵进行纠错覆盖，并允许老旧关联随时间自然淡出，防止固定矩阵信息过载。
- **生产混合交替方案（Interleaving）**：由于近似检索无法像全注意力一样确保单 Token 100% 精确召回，生产模型将少数全注意力层（Exact Lookup）与多数 Delta Attention 线性层交叉交替编织，以兼顾显存压缩与大海捞针等高精度召回场景。

## 参见

- [[实体_Kimi_Linear]]
- [[MiniMax_vs_Kimi_注意力路线之争]]
- [[wiki/sources/2026-07-24_Delta-attention-in-Kimi-K3-to-fix-growing-KV-cache_19f962.md]]
- [[概念_线性注意力与混合注意力]]
- [[concepts/概念_KV_Cache_键值缓存]]