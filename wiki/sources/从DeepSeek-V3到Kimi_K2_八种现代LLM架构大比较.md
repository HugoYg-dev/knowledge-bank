---
type: source
tags:
- LLM/arch
- LLM/arch/MoE
summary: Sebastian Raschka 对比 8 种 2024-2025 年现代 LLM 架构的创新点：MLA/MoE/滑动窗口/Post-Norm/NoPE/Muon
sources:
- raw/articles/从DeepSeek-V3到Kimi K2：八种现代 LLM 架构大比较.md
updated: '2026-07-01'
---
## 来源信息

- **标题**：从DeepSeek-V3到Kimi K2：八种现代 LLM 架构大比较
- **作者**：Sebastian Raschka（编译：PaperAgent，Datawhale）
- **URL**：https://sebastianraschka.com/blog/2025/the-big-llm-architecture-comparison.html

## 核心要点

### DeepSeek V3/R1
- **MLA（多头潜在注意力）**：将 K/V 张量压缩到低维空间存入 KV Cache，推理时再投影回原尺寸；内存占用低于 GQA，建模性能优于 MHA（见 DeepSeek-V2 消融研究）
- **MoE**：256 个专家，推理时仅激活 9 个（1 个共享 + 8 个路由选择），总参数 671B，激活参数 37B；共享专家对每个 Token 始终激活

### OLMo 2
- **Post-Norm（后归一化）**：RMSNorm 放在 Attention/FFN 之后（残差内部），非残差外；有助训练稳定性
- **QK-Norm**：在 MHA 内部、RoPE 之前对 Q 和 K 各加一层 RMSNorm，减少数值不稳定；两者结合显著稳定训练 Loss
- 仍使用 MHA（非 GQA）

### Gemma 3
- **滑动窗口注意力（Local Attention）**：局部窗口大小 1024，全局:局部比例 1:5，大幅降低 KV Cache 内存；消融研究显示对 perplexity 几乎无影响
- 注意力模块前后均有 RMSNorm（Pre+Post Norm 结合）
- **Gemma 3n**：Per-Layer Embedding（PLE）+ MatFormer，适配手机端设备

### Mistral Small 3.1
- 放弃滑动窗口注意力，转用标准 GQA + FlashAttention；优化推理延迟而非内存
- 更小 KV Cache、更少层数、定制分词器

### Llama 4
- 与 DeepSeek-V3 架构相似，使用 MoE，但使用 GQA（非 MLA）
- 专家较少但较大（每次激活 2 个，隐藏层 8192），交替使用 MoE 层和密集层

### Qwen3
- Dense：更深（更多 Transformer Block）、更窄架构，vs Llama 3 更宽
- MoE（235B-A22B）：无共享专家（与 DeepSeek-V3 不同）

### SmolLM3
- **NoPE（无位置嵌入）**：不使用绝对/RoPE 位置编码，依赖因果 Attention Mask 隐式学习位置；长度泛化更好

### Kimi K2
- 基于 DeepSeek-V3 架构扩展至 1 万亿参数
- **Muon 优化器**（非 AdamW）：首次在生产级大模型规模使用，训练 Loss 曲线极平滑

## 关键引文

无有效 Cubox 高亮内容。

## 关联

- [[概念_MLA_多头潜在注意力]] — DeepSeek MLA 压缩 KV Cache
- [[概念_MoE混合专家]] — MoE 架构原理
- [[概念_滑动窗口注意力]] — Gemma 3 局部注意力
- [[概念_QK_Norm_注意力查询键归一化]] — OLMo 2 训练稳定化
- [[概念_NoPE无位置嵌入]] — SmolLM3 位置编码缺失实验
- [[概念_Muon优化器]] — Kimi K2 训练创新
- [[实体_DeepSeek-V3]] — DeepSeek 模型实体
- [[实体_Kimi_K2]] — Kimi K2 模型实体
- Llama4 — Meta Llama 4 模型实体
- [[2025年七大顶流大模型架构]] — 同主题互补文章
- [[腾讯混元TurboS技术报告]] — Mamba+MoE 混合架构

---
> 📎 **物理文献**：[[raw/articles/从DeepSeek-V3到Kimi K2：八种现代 LLM 架构大比较.md]]