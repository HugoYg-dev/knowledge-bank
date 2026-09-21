---
sources:
- wiki/sources/LLM后训练技术全景解读.md
- wiki/sources/LoRA微调实战_Qwen2.5全流程.md
- wiki/sources/淘宝直播数字人_LLM文案生成技术.md
- wiki/sources/2026-04-23_LoRAQLoRA-explained-from-a-business-lens_19dbca.md
summary: Low-Rank Adaptation（LoRA）与 QLoRA 是主流参数高效微调方法。通过冻结预训练权重并注入低秩分解矩阵，极大降低算力开销；在工程多租户服务中，单个
  Adapter 仅 20-25MB，支持多客户共享单物理底座与动态热插拔。
tags:
- LLM/training/post-train
type: concept
updated: '2026-09-21'
---
# 概念：LoRA 低秩适应微调

Low-Rank Adaptation（LoRA）是一种参数高效微调（PEFT）方法，通过在预训练权重旁注入低秩分解矩阵，只训练极少量参数即可实现领域适配。

## 核心原理

- 对目标权重矩阵 W（d×d），引入低秩分解 ΔW = BA，其中 B（d×r）和 A（r×d），r << d
- 训练时冻结原始权重 W，只训练 A 和 B；推理时可合并为 W' = W + BA
- 可训练参数量约为原来的 2r/d，r=8 时通常极低（< 1% 参数）

## 关键超参

- **r（秩）**：低秩矩阵的秩，控制适配器容量；r=8 是常用起点
- **lora_alpha**：缩放因子，ΔW = (lora_alpha/r) × BA；通常设为 r 的 4 倍（r=8 则 alpha=32）
- **lora_dropout**：Dropout 比例，防止过拟合；通常 0.1
- **target_modules**：应用 LoRA 的模块；推荐覆盖 q/k/v/o_proj 和 gate/up/down_proj

## QLoRA 变体

- QLoRA = 量化 + LoRA：将基础模型量化为 4-bit（NF4），在量化模型上添加 LoRA 适配器
- 显存进一步降至约 0.5Φ bytes/参数（相比 LoRA 的 2Φ）
- 适合更大模型（30B+）的单卡微调

## 适用场景

- 领域适配（垂直领域知识注入）
- 指令遵循（特定任务格式学习）
- 端侧部署（小参数模型降低延迟）
- 成本考量：微调 0.5B 模型在 CPU 上约 50 分钟

## 相关资源

- [[LoRA微调实战_Qwen2.5全流程]] — 完整 PEFT 实战代码
- [[概念_Fine-tuning]] — 微调方法全览对比
- [[概念_LoRA与QLoRA显存]] — LoRA/QLoRA 显存估算
- [[实体_PEFT库]] — HuggingFace PEFT 实现

---

## 多租户服务（Multi-tenant Serving）与工业落地价值

在平台级模型服务架构中，LoRA 呈现出全参数微调无法比拟的工程与商业优势：

1. **存储极致压缩**：每个微调用户仅需保存低秩适配层权重（通常仅 20~25MB），对比全参数模型单副本几十至数百 GB，实现千倍存储节省。
2. **显存多租户时分复用**：多个业务租户共享同一块 GPU 上长驻的物理基座大模型（Base Model），仅需在显存中按需动态挂载活跃用户的轻量 LoRA 权重，彻底解决模型切换的冷启动延迟与显存瓶颈。
