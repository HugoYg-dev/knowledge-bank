---
type: concept
tags:
- LLM/arch
summary: Fine-tuning（微调）通过在特定领域/任务数据上继续训练大模型，增强 LLM 本身的能力，使其在目标场景上产出更准确/更符合格式的输出。
sources:
- wiki/sources/375篇文献_推理大模型后训练技术综述.md
- wiki/sources/LoRA微调实战_Qwen2.5全流程.md
- wiki/sources/OpenAI_LLM应用最佳实践.md
updated: '2026-09-21'
aliases:
- Fine-tuning
- Fine Tuning
- 微调
- 模型微调
- 概念_Fine-tuning
---

# 概念_Fine_Tuning_模型微调


## 定义

Fine-tuning（微调）通过在特定领域/任务数据上继续训练大模型，增强 LLM 本身的能力，使其在目标场景上产出更准确/更符合格式的输出。

## 主要好处

1. 提升模型在特定领域/任务上的性能
2. 降低 Token 数量提升效率（避免 Prompt 中加入大量指令和示例）
3. 可通过蒸馏将大模型能力蒸馏到小模型（如 70B → 13B）

## 适用场景

- **适合**：激发模型已有知识、自定义结构/语气、教会复杂指令
- **不适合**：向 base 模型注入新知识、快速在新场景验证
- 注意：如果 Prompt Engineering 没有效果，Fine-tuning 可能不是正确选择

## 最佳实践

1. 从 Prompt Engineering + Few-shot Learning 开始快速验证
2. 建立 baseline，了解核心问题
3. 从小的高质量数据集开始，验证方向正确
4. 结合主动学习（Active Learning）不断迭代构建高质量数据

## 微调流程

1. **Data Preparation**：收集、验证、标注高质量数据，按要求格式化
2. **Training**：选择超参，理解损失函数
3. **Evaluation**：评估指标 + 任务测试集 + GPT-4 评估
4. **Inference**：进一步收集数据标注，用于后续迭代

## 失败案例教训

- 用 140K Slack 聊天记录微调 GPT-3.5 想生成个人风格博文 → 产出变成聊天场景
- 教训：数据集偏离需求导致"种瓜得瓜"，数据集质量和相关性至关重要

## Fine-tuning + RAG 结合

- Fine-tuning 使模型遵循格式/风格、降低 Prompt 复杂度 → 为 RAG 留更大空间
- RAG 注入相关知识增强短期记忆
- Text-to-SQL 案例：PE 69% → RAG 80% → FT+Reduced Schema 81.7% → FT+RAG 83.5%

## 关联

- 相关概念：[[概念_LLM应用优化两轴]]、[[概念_RAG基础流程]]、[[概念_Prompt工程方法]]
- 来源：[[OpenAI_LLM应用最佳实践]]