---
type: "source"
tags:
- "LLM/inference"
summary: "解析推测解码（Speculative Decoding）四种主流变体：双模型独立草稿、EAGLE隐层特征预测、Medusa多头树状解码与LayerSkip浅层早退，对比其机制原理、加速性能与工程权衡"
sources:
- "raw/articles/2026-09-12_4-speculative-decoding-variants_1a09737e364224e2.md"
updated: "2026-09-15"
---

## 来源信息

- **标题**：4 speculative decoding variants
- **作者**：Avi Chawla (Daily Dose of DS)
- **原始链接**：https://www.dailydoseofds.com/p/speculative-decoding-in-llms/
- **发布日期**：2026-09-12
- **邮件元数据**：邮件主题 `4 Speculative Decoding Variants` | 邮件 ID `1a09737e364224e2` | 文章 ID `1a09737e364224e2:2`

## 核心要点

1. **访存受限与两阶段循环（Draft-then-Verify）**：大模型自回归生成受限于显存带宽（memory-bandwidth bound），每生成 1 个 token 需完整遍历模型参数。推测解码通过轻量级机制廉价生成多个连续候选 token（Drafting），再由目标大模型在单次前向传播中并行检验（Verification），实现一次模型运行推进多个 token。
2. **数学严谨的无损加速**：贪婪解码只需 token 序列完全匹配；采样（Sampling）基于两模型概率分布采用校正接受/拒绝机制，数学上严格保证最终输出分布与目标大模型独立自回归采样完全一致。
3. **双模型独立推测（Two-model Speculative Decoding）**：以小型独立草稿模型自回归生成、大模型并行验证。原论文在 T5-XXL 上汇报 2x–3x 无损加速。优势是目标大模型完全冻结无需二次训练，主流引擎原生支持；代价是需常驻第二套权重与独立 KV Cache，且要求两模型分词器和行为对齐。
4. **EAGLE 隐层特征预测（Drafting from Hidden States）**：摒弃独立语言模型，在目标模型顶层训练轻量模块直接预测倒数第二层特征隐藏状态，再转换为候选 token；将输入 token 序列前移一位联合输入消除特征多义性。在 LLaMA2-Chat 70B 上实现 2.7x–3.5x 延迟加速，吞吐量翻倍。
5. **Medusa 多头并行预测与树状注意力（Parallel Heads & Tree Attention）**：在目标模型顶层挂载多个并行预测头分别推测后续不同位置 token。为解决多头无自回归依赖导致的语义不连贯，引入候选树与树状注意力（Tree Attention）实现一次前向验证多分支。Medusa-1 冻结主干仅训头（>2.2x 加速）；Medusa-2 联合微调（2.3x–3.6x 加速）。
6. **LayerSkip 浅层早退推测（Early-Exit Self-Drafting）**：模型“自推测自验证”，浅层 Transformer 输出草稿、深层并行校正验证。共享权重、词表、KV Cache 与前向计算，实现零额外显存；但需在训练期引入层级 Dropout 与早期退出损失。论文汇报在文本摘要、代码生成与语义解析上分别达 2.16x、1.82x 与 2.0x 加速。
7. **工程选型决策标准**：核心度量是扣除草稿耗时与验证开销后每个目标模型 Pass 净接受的 token 数量（Accepted tokens per target pass）。任务越确定（如低温代码生成）接受率越高；大 Batch 饱和场景下边际收益收窄；全变体均依赖 KV Cache 避免重算。

## 4 种推测解码变体横向机制对比

| 变体名称 | 草稿生成源 (Drafter) | 目标模型改造要求 | 显存/内存额外开销 | 核心机制与创新点 | 典型加速比 (论文汇报) | 适用落地场景 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **双模型推测解码 (Two-Model)** | 独立同系列小语言模型 (Draft Model) | **零修改**（完全冻结） | 高（需承载独立模型权重与 KV 缓存） | 独立小模型自回归生成 + 大模型并行矩阵校验 | **2x – 3x** (T5-XXL) | 通用推理部署、无法修改目标模型权重 |
| **[[实体_EAGLE]]** | 目标模型倒数第二层特征预测模块 | 训练专用轻量前向预测模块 | 低（仅需加载轻量特征模块） | 倒数第二层隐状态特征预测 + 序列前移一位消除多义性 | **2.7x – 3.5x** (LLaMA2-Chat 70B) | 追求高接受率与极致吞吐的私有模型服务 |
| **[[实体_Medusa]]** | 顶层外挂的多个并行解码头 (Medusa Heads) | 训练额外 Heads（Medusa-1 仅训头；Medusa-2 联合微调） | 极低（仅增加若干 FFN 头权重） | 多头并行向前预测 + 树状注意力 (Tree Attention) 一次验证多分支 | **2.2x – 3.6x** (Vicuna / LLaMA) | 显存极度敏感、单模型体系内自推测加速 |
| **LayerSkip** | 目标模型早期浅层 Transformer (Early Exit) | **训练期前置干预**（Layer Dropout + 早期退出损失） | **零额外显存**（共享全部权重与 KV 缓存） | 浅层产生草稿、深层校验修正；计算、激活与缓存深度共享 | **1.8x – 2.16x** (代码/摘要/语义解析) | 自研模型从预训练阶段即规划推理加速的全生命周期管理 |

## 关键引文

> The number that matters is accepted tokens per target-model pass after accounting for drafting time and verification overhead. `[核心指标]`
>
> Speculative decoding tries to get several useful tokens from that run instead of just one... Draft tokens never reach the output without verification from the large model. `[基本原则]`

## 关联

- [[概念_推测解码]] — Draft-then-Verify 大模型推理加速核心范式
- [[实体_EAGLE]] — 基于倒数第二层隐状态特征预测的推测解码开源框架
- [[实体_Medusa]] — 基于多头并行预测与树状注意力的推测解码自加速框架
- [[实体_vLLM]] — 支持推测解码等多种加速算法的高性能推理框架
- [[概念_KV_Cache]] — 推测解码依赖的底层缓存优化基础

---
> 📎 **物理文献**：[[raw/articles/2026-09-12_4-speculative-decoding-variants_1a09737e364224e2.md]]
