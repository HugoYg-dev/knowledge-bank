---
type: entity
tags:
- LLM/arch/Mamba
- LLM/arch/MoE
summary: 腾讯混元旗舰大语言模型，业界首个大规模部署的 Hybrid Transformer-Mamba MoE 模型。
sources:
- wiki/sources/实测腾讯开源的 BrowserSkill：让 AI 直接用你登录好的浏览器.md
- wiki/sources/腾讯混元TurboS技术报告.md
updated: '2026-06-29'
---
# 实体_腾讯混元TurboS

腾讯混元旗舰大语言模型，业界首个大规模部署的 Hybrid Transformer-Mamba MoE 模型。

## 基本信息

- **机构**：腾讯混元团队
- **论文**：Hunyuan-TurboS，https://arxiv.org/abs/2505.15431
- **发布时间**：2025 年 5 月（技术报告公开）

## 规格

- 总参数：560B；激活参数：56B
- 总层数：128 层（Attention 5.5% + Mamba2 44.5% + FFN-MoE 50%）
- 上下文窗口：256K Token
- 预训练数据：16 万亿 Token

## 架构创新

- **Hybrid Transformer-Mamba**：AMF/MF 模块交错，Mamba2 实现 O(n) 长序列处理
- **MoE FFN**：1 共享 + 32 专门专家，每次激活 1+2
- **自适应长短 CoT**：根据问题复杂度自动切换"快速/深度"推理模式

## 性能

- LMSYS Chatbot Arena：1356 分，全球第 7（5 月 2025），国内仅次于 DeepSeek
- 中文、法语、西班牙语并列全球第一；韩文全球第二
- Token 效率：与 DeepSeek-R1 性能相当，Token 消耗仅 52.8%

## 相关文件

- [[腾讯混元TurboS技术报告]]
- [[概念_Mamba_混合架构]]
- [[概念_CoT_自适应长短思考]]
- [[实体_Mamba2]]