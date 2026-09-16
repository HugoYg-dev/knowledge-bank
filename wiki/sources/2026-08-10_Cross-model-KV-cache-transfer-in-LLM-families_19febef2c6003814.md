---
type: source
tags:
- LLM/inference
- Infra/serving
summary: 同一模型家族内的 KV Cache 可通过无训练的跨层线性映射转换到目标模型，实验报告转换速度为重新 Prefill 的 3-25 倍，但跨家族与不匹配 KV 头配置尚未验证。
sources:
- raw/articles/2026-08-10_Cross-model-KV-cache-transfer-in-LLM-families_19febef2c6003814.md
updated: '2026-08-11'
---

# 来源摘要：Cross-model KV cache transfer in LLM families

## 来源信息
- **标题**：Cross-model KV cache transfer in LLM families
- **来源**：Daily Dose of DS
- **日期**：2026-08-10
- **原文链接**：[Daily Dose of DS 邮件文章](https://www.dailydoseofds.com/building-rag-systems-course-part-12-with-implementation/)
- **文中引用论文**：[arXiv:2608.03893](https://arxiv.org/abs/2608.03893)

## 核心要点
- [原文陈述] 常规 KV Cache 只能由生成它的模型读取；当路由切换到另一模型时，既有缓存会失效并需要重新 Prefill。
- [原文陈述] 该工作将跨模型复用表述为表示转换问题：为每个目标层与注意力头拟合独立线性映射，并以闭式解求解，不依赖梯度训练。
- [原文陈述] 对每个目标层，方法按预测能力挑选多个源层；文中从单源层重建目标 Key 方差的 56% 提升到使用前 8 个源层的 79%。
- [原文陈述] 映射前先移除 Key 中由 RoPE 引入的位置旋转，在与位置无关的空间拟合，推理时再施加目标模型的旋转。
- [原文陈述] 在 Qwen3、Llama 3.1 与 Ministral 3 的 6 组同家族模型配对中，文中称有 4 组保留接收模型独立准确率的 73%-98%，转换速度为重新处理上下文的 3-25 倍。
- [待验证] 文中仅覆盖同家族的稠密全注意力模型；跨家族迁移、KV 头数量或单头维度不匹配、滑动窗口与注意力递归混合架构仍未测试。

## 关联概念
- [[concepts/概念_KV_Cache]]
- [[concepts/概念_跨模型KV缓存转换]]
- [[concepts/概念_LLM推理两阶段]]

> 📎 **物理文献**：[[raw/articles/2026-08-10_Cross-model-KV-cache-transfer-in-LLM-families_19febef2c6003814.md]]
