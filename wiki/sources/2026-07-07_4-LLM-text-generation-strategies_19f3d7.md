---
type: source
tags:
- LLM/arch
- LLM/inference
- DeepLearning
summary: 介绍了 LLM 文本生成中的四种核心解码策略（贪婪搜索、多项式采样、束搜索与对比搜索），分析了它们的工作机制以及在流畅度、多样性与重复度等方面的权衡。
sources:
- raw/articles/2026-07-07_4-LLM-text-generation-strategies_19f3d7.md
updated: '2026-08-04'
---

# 来源：4 LLM text generation strategies

## 来源信息
- **原邮件主题**: Rethinking KV Caching For Production Inference
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Tue, 07 Jul 2026 16:52:26 +0000
- **ID**: 19f3d7ecdb9a83ee
- **原始链接**: [Daily Dose of DS Substack](https://www.dailydoseofds.com/p/what-is-temperature-in-llms/)

## 核心要点
1. **生成即预测下一步**：大模型并不在生成句子的开头就预知整句话，而是逐个 token 进行概率预测。为了将预测概率转化为最终单词，必须采用解码策略（Decoding Strategy）。
2. **四大解码策略**（参见 [[concepts/概念_LLM文本生成解码策略]]）：
   - **贪婪搜索 (Greedy Search)**：单步最优化。每次都选择概率最高的 token。容易导致生成的句子重复、死板。
   - **多项式采样 (Multinomial Sampling)**：在概率向量上进行随机采样。常结合 Temperature/Top-p 参数使用，能显著增强输出的多样性与创意度。
   - **束搜索 (Beam Search)**：近似全局概率最大化。每次保留前 $k$ 个局部序列（Beam），探索概率树的更多分支，非常适合机器翻译与代码生成等准确性要求高、不需要太高创造力的任务。
   - **对比搜索 (Contrastive Search)**：结合概率与多样性惩罚。在候选 token 中考虑其与已生成序列表示向量之间的相似度，引入退化惩罚项（Degeneration Penalty）来阻断文本生成陷入死循环，极其适用于长文本生成（如写故事）。
3. **策略的选择权衡**：不同的解码策略直接影响了模型生成的流畅度、多样性与重复度。机器翻译更依赖束搜索，而长文故事生成更适合使用对比搜索或多项式采样。

## 关键引文
- "Every time you prompt an LLM, it doesn’t 'know' the whole sentence in advance. Instead, it predicts the next token step by step."
- "Beam search tries to approximate the true global maximization... by keeping alternatives alive, beam search explores more of the probability tree."
- "Essentially, [Contrastive Search] penalizes repetitive continuations by checking how similar a candidate token is to what’s already been generated to have more diversity in the output."

## 关联概念
- [[concepts/概念_LLM文本生成解码策略]]

> 📎 **物理文献**：[[raw/articles/2026-07-07_4-LLM-text-generation-strategies_19f3d7.md]]
