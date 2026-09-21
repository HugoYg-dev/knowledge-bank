---
type: entity
tags:
- LLM/training/post-train
summary: HuggingFace 开源的参数高效微调库，集成多种 PEFT 方法。
sources:
- wiki/sources/LoRA微调实战_Qwen2.5全流程.md
updated: '2026-07-06'
---

# 实体：PEFT 库（HuggingFace Parameter-Efficient Fine-Tuning）

HuggingFace 开源的参数高效微调库，集成多种 PEFT 方法。

## 基本信息

- GitHub：https://github.com/huggingface/peft
- 与 Transformers / datasets / TRL 深度集成

## 支持的方法

- **LoRA**：低秩适应，q/k/v 等矩阵注入低秩分解
- **QLoRA**：量化 + LoRA，NF4 量化 + 双量化
- **Adapter Tuning**：在层间插入小型适配器
- **Prefix Tuning / P-Tuning / Prompt Tuning**：软提示

## 核心 API

```python
from peft import LoraConfig, get_peft_model, TaskType
config = LoraConfig(task_type=TaskType.CAUSAL_LM, r=8, lora_alpha=32, lora_dropout=0.1)
model = get_peft_model(model, config)
# 训练后合并
model = model.merge_and_unload()
```

## 相关资源

- [[LoRA微调实战_Qwen2.5全流程]] — 完整实战代码
- [[概念_LoRA_低秩适应微调]] — LoRA 原理
- [[概念_LoRA与QLoRA显存]] — 显存估算