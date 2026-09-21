---
type: source
tags:
- LLM/training/post-train
summary: 使用 LoRA 在 CPU 老笔记本上对 Qwen2.5-0.5B-Instruct 进行领域微调的完整实战流程
sources:
- raw/articles/【有手就行】LoRA：用你自己的数据来微调大模型，让大模型真正懂你 - 程序员老....md
updated: '2026-07-01'
---
## 来源信息

- **标题**：【有手就行】LoRA：用你自己的数据来微调大模型，让大模型真正懂你
- **作者**：程序员老奥
- **URL**：https://www.cnblogs.com/oddmeta/p/19350019

## 核心要点

- 微调方法横向对比：全参数微调（极高成本）、Adapter Tuning（低成本）、LoRA/QLoRA（极低成本）、指令微调（中高成本）、领域适配微调（中成本），普通人首选 LoRA/QLoRA
- 实验配置：i7-8850H CPU + 16G 内存老笔记本，无 GPU，微调 Qwen2.5-0.5B-Instruct，耗时约 49 分钟
- 数据集构造：通过其他大模型为每个意图生成 50 条数据，格式为 instruct + input + output（工具名称+参数），省去人工标注
- LoRA 关键超参：r=8（秩），lora_alpha=32（缩放因子），lora_dropout=0.1，target_modules 覆盖 q/k/v/o_proj 及 gate/up/down_proj
- 训练参数：batch_size=4，gradient_accumulation_steps=4（实际 bs=16），epochs=8，lr=1e-4，启用 gradient_checkpointing 节省显存
- 训练完成后用 `merge_and_unload()` 将 LoRA 适配器合并回基础模型后保存
- 实测效果：Qwen2.5-0.5B 微调后意图识别准确率 96.47%；Qwen3-4B 同数据可达 100% 但参数量过大无法端侧部署
- 核心洞察：数据是决定微调效果和产品成败的真正价值，技术本身门槛低

## 关联

- [[概念_LoRA_低秩适应微调]] — LoRA 低秩分解原理
- [[概念_Fine_Tuning_模型微调]] — 微调方法对比
- [[概念_大模型训练三阶段]] — 训练阶段概述
- Qwen系列模型 — Qwen2.5/Qwen3 系列
- [[实体_PEFT库]] — HuggingFace PEFT，LoRA 实现库

---
> 📎 **物理文献**：[[raw/articles/【有手就行】LoRA：用你自己的数据来微调大模型，让大模型真正懂你 - 程序员老....md]]