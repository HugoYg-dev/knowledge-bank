---
type: source
tags:
- LLM/inference
summary: 推测解码（Speculative Decoding）综述：Draft-then-Verify 范式通过并行推测+验证实现无损推理加速
sources:
- raw/articles/LLM推理加速新范式！推测解码（Speculative Decoding）最新综....md
updated: '2026-07-01'
---
## 来源信息

- 标题：LLM推理加速新范式！推测解码（Speculative Decoding）最新综述
- 作者：hemingkx（香港理工大学、北京大学、微软亚洲研究院、阿里巴巴）
- URL：https://blog.csdn.net/qq_27590277/article/details/135812738
- 论文：Unlocking Efficiency in Large Language Model Inference: A Comprehensive Survey of Speculative Decoding（arXiv 2401.07851）

## 核心要点

- LLM 推理是 memory-bandwidth bound：大部分时间消耗在将参数从 HBM 搬运到 cache，而非实际计算；GPU 利用率低下
- 自回归解码每步只生成一个 token，序列生成时间随长度线性增加
- 推测解码定义：**Draft-then-Verify**——每个解码步先高效"推测"未来多步 token，再用 target LLM 并行验证，通过的 token 作为解码结果
- 关键性质：理论上保证解码结果与 target LLM 自回归解码完全一致（无损加速）
- 实现加速的三个要素：①并行验证引入的额外 latency 极小；②推测的高效性和准确性；③验证策略的选择
- 两类推测（Drafting）策略：
  - **Independent Drafting**：使用同系列小模型推测（如 OPT-125M 推测 OPT-70B）；Google 和 DeepMind 同时提出；支持 greedy decoding 和 nucleus sampling 的无损加速；可通过知识蒸馏增强小模型与 target LLM 的行为对齐
  - **Self-Drafting**：用 target LLM 自身推测，如 Medusa/Blockwise Decoding 在最后一层之上添加多个额外 FFN Head 并行预测多 token；还有 Early-Exiting、Layer-Skipping、插入 [PAD] token 等方式
- 验证（Verification）策略：
  - 贪婪解码验证：第一个不匹配 token 后的所有推测 token 被丢弃
  - 可放松验证要求（accept-relaxed），让更多高质量推测 token 通过
  - 支持并行验证多条推测序列（token tree verification，如 SpecInfer）
- 推测精度与推测耗时之间存在权衡，如何选择合适策略是核心问题

## 关键引文

> 推测解码是一种"先推测后验证" (Draft-then-Verify) 的解码算法：在每个解码步，该算法首先高效地"推测"target LLM未来多个解码步的结果，然后用target LLM同时进行验证，以加速推理。 `[重点/高亮]`

## 关联

- [[概念_推测解码]] — Draft-then-Verify 推理加速范式
- 自回归解码 — 推测解码的加速对象
- [[概念_KV_Cache_键值缓存]] — 推理显存优化的互补技术
- [[概念_FlashAttention_快速注意力]] — 推理加速另一关键方向
- [[实体_Medusa]] — Self-Drafting 代表工作，多 FFN Head 并行解码
- [[实体_vLLM]] — 工业界推理框架，集成推测解码等加速手段

---
> 📎 **物理文献**：[[raw/articles/LLM推理加速新范式！推测解码（Speculative Decoding）最新综....md]]