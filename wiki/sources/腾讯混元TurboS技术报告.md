---
type: source
tags:
- LLM/arch/Mamba
- LLM/arch/MoE
summary: 腾讯混元 TurboS：560B 参数 Hybrid Transformer-Mamba MoE 模型，业界首个大规模部署的 Mamba 架构，自适应长短
  CoT 融合
sources:
- raw/articles/腾讯混元TurboS技术报告首次全公开：560B参数混合Mamba架构，自适应长....md
updated: '2026-07-01'
---
## 来源信息

- **标题**：腾讯混元TurboS技术报告首次全公开：560B参数混合Mamba架构，自适应长短链融合
- **作者**：腾讯混元 AI前线
- **URL**：https://mp.weixin.qq.com/s/AsdREeEoqkY4XnEJkrZEFg
- **论文**：https://arxiv.org/abs/2505.15431

## 核心要点

- 混元 TurboS 是业界首个大规模部署的 Hybrid Transformer-Mamba MoE 模型，总参数 560B，激活参数 56B
- 架构共 128 层：Attention 层占 5.5%，Mamba2 层占 44.5%，FFN (MoE) 层占 50%
- 核心模块模式为 "AMF"（Attention→Mamba2→FFN）和 "MF"（Mamba2→FFN）交错排列
- FFN 层采用 MoE 结构：1 个共享专家 + 32 个专门专家，每次前向激活 1+2 个专家
- Mamba2 层实现序列长度线性复杂度 O(n)，相比纯 Transformer MoE 实现 1.8x 推理加速
- 自适应长短 CoT（Adaptive Long-short CoT）：根据问题复杂度自动切换"无思考"与"思考"模式
- 在 Chatbot Arena 获得 1356 分（5月排名全球第7），23 个自动化基准平均 77.9%
- 自适应 CoT 使 Token 消耗仅为 DeepSeek-R1 的 52.8%，数学/编程推理 Token 降低 35%-45%
- 预训练数据规模：16 万亿 Token；上下文窗口：4K → 32K → 256K（课程学习扩展）
- 后训练四阶段：SFT → 自适应长短 CoT 融合 → 多轮推敲学习（Deliberation Learning）→ 两阶段 GRPO RL
- GRPO 两阶段：阶段一聚焦推理（代码/数学/逻辑），阶段二扩展到通用指令遵循
- 推理框架 AngelHCF：Mamba Kernel 优化 + MoE 优化 + fp32 精度 Mamba 状态（长文本质量达全 Attention 水平）
- 训练框架 Angel-RL 支持 TP/PP/EP/CP 并行，ZeroCache 技术降低多模型 GPU 显存压力

## 关键引文

无有效 Cubox 高亮内容。

## 关联

- [[概念_Mamba_混合架构]] — Hybrid Transformer-Mamba 架构设计
- [[概念_MoE混合专家]] — FFN 层替换为 MoE
- [[概念_CoT_自适应长短思考]] — 动态切换推理深度的机制
- [[概念_GRPO_群组相对策略优化]] — Group Relative Policy Optimization
- [[实体_腾讯混元TurboS]] — 混元 TurboS 模型实体
- [[实体_Mamba2]] — Mamba2 SSM 架构组件
- [[A_Visual_Guide_to_Mamba_and_SSM]] — Mamba 架构基础
- [[Mamba2_SSD_大一统]] — Mamba2 SSD 框架

---
> 📎 **物理文献**：[[raw/articles/腾讯混元TurboS技术报告首次全公开：560B参数混合Mamba架构，自适应长....md]]