---
type: entity
tags:
- LLM/arch/attention
summary: 月之暗面开源的 48B 混合注意力模型，采用 KDA（线性）+ MLA（全注意力）3:1 混合，KV Cache 减少 75%，吞吐量提升 6.3×
sources:
- wiki/sources/MiniMax_vs_Kimi_注意力路线之争.md
updated: '2026-06-29'
---

# 实体：Kimi Linear

## 基本信息

- **机构**：月之暗面（Moonshot AI）
- **发布时间**：2025年10月30日
- **参数**：48B 总参数，3B 激活参数（MoE）
- **训练数据**：5.7T tokens
- **上下文**：1M tokens
- **开源**：是（权重 + 代码 + 技术报告）

## 核心架构

### 混合比例：KDA:MLA = 3:1
- 每 3 层 KDA（线性注意力）配 1 层 MLA（全注意力）
- 通过 ablation study 确定最优比例（Validation PPL 5.65，最优）
- MoE 通道混合层接在每个 token 混合层后

### Kimi Delta Attention（KDA）
- 基于 Gated DeltaNet
- 升级：scalar gate → **channel-wise gate（通道级门控）**
- 每个特征维度独立控制遗忘因子
- 相比标准 DPLR 实现，计算效率提升约 100%

### NoPE（No Position Encoding）
- MLA 层不使用 RoPE，位置信息由 KDA 层负责
- 好处：MLA 可转为更高效的 MQA，训练更简单，长上下文泛化更好

## 性能

| 指标 | 数值 |
|------|------|
| KV Cache 减少 | 75%（4× 内存降低）|
| 1M tokens 解码吞吐提升 | 6.3× vs MLA |
| TPOT（1M tokens）| 11.48ms → 1.84ms |
| RULER（128k）| 84.3，速度 3.98× vs MLA |
| Scaling 效率 | ≈1.16× 优于 Full Attention |

## 工程化

- KDA 算子已整合进 **vLLM 官方主代码库**

## 参见

- [[MiniMax_vs_Kimi_注意力路线之争]]
- [[concepts/概念_Kimi_Delta_Attention|Kimi Delta Attention]]
- [[概念_线性注意力与混合注意力]]
- [[概念_MLA低秩KV压缩]]
- [[实体_MiniMax_M2]]