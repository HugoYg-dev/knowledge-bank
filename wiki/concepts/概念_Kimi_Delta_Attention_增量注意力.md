---
type: concept
tags:
- LLM/arch/attention
summary: Kimi Linear 的核心注意力机制，基于 Gated DeltaNet 改进，将 scalar gate 升级为 channel-wise
  gate，计算效率比 DPLR 提升约 100%
sources:
- wiki/sources/MiniMax_vs_Kimi_注意力路线之争.md
updated: '2026-09-21'
aliases:
- Kimi Delta Attention
- Delta Attention
- 增量注意力
- 概念_Kimi_Delta_Attention
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

## 参见

- [[实体_Kimi_Linear]]
- [[MiniMax_vs_Kimi_注意力路线之争]]
- [[概念_线性注意力与混合注意力]]