---
type: source
tags:
- LLM/training/post-train
summary: 普林斯顿陈丹琦团队发现 RL 抗遗忘优于 SFT，根源在于 on-policy 数据分布，而非算法形式
sources:
- raw/insights/后训练认知：SFT vs RL—关于记忆和遗忘机制.md
updated: '2026-07-01'
---
## 来源信息

- 标题：RL记得更牢，SFT更健忘？普林斯顿陈丹琦团队改写后训练认知
- 作者/来源：PaperWeekly
- URL：https://mp.weixin.qq.com/s/Vg0HUgIgOujLBClDXSDslQ
- 论文：Retaining by Doing: The Role of On-Policy Data in Mitigating Forgetting（arxiv 2510.18874）

## 核心要点

- 后训练（SFT/RL）带来的副作用是**灾难性遗忘**（alignment tax）：对齐越彻底，旧能力下降越明显
- 直觉认为 RL（reverse KL）更激进、更容易遗忘，但实验结果相反：**RL 在长期训练后保留更多原有能力**
- 实验设置：Llama-3 与 Qwen-2.5 系列，相同算力与数据预算，覆盖 IFEval（指令遵循）、MMLU（通识推理）、Countdown（算术推理）三类任务
- **核心发现：遗忘的根源不在算法，而在数据分布与模型行为之间的错位**
  - SFT 使用离线静态数据（off-policy），始终在"过时数据"上更新
  - RL 基于当前策略（on-policy）采样，训练数据贴近模型当前行为
- KL 视角：SFT 最小化 forward KL（覆盖全部目标分布区域），RL 最小化 reverse KL（选择最可能的部分）
  - 多峰分布下，SFT 的 forward KL 为"覆盖"新目标会拉扯旧峰概率质量；RL 的 reverse KL 直接"平移新峰"，不动旧峰
- 消融分析：去掉 KL 正则项（β=0）或替换为 REINFORCE，RL 抗遗忘性能几乎不变，证明关键是 on-policy 采样机制本身
- 定量结果：SFT 非目标任务 Drop ≈ -3~-7，REINFORCE 与 GRPO 的 Drop 几乎为 0
- SFT 学习率与遗忘呈跷跷板关系：高 LR 提升目标任务但加重遗忘，低 LR 缓解遗忘但目标任务停滞
- **Iterative-SFT**（每个 epoch 用当前模型重新生成训练样本）可复现 RL 的抗遗忘特性，性能与 GRPO 相当

## 关键引文

> 模型能否记得更牢，不取决于算法聪不聪明，而在于它学的是"谁的数据"。[重点/高亮]

## 关联

- [[概念_on-policy与off-policy数据]]
- [[概念_灾难性遗忘]]
- alignment_tax
- Forward_KL与Reverse_KL
- [[概念_GRPO强化学习]]
- Llama-3
- [[实体_Qwen2.5-Coder]]

---
> 📎 **物理文献**：[[raw/insights/后训练认知：SFT vs RL—关于记忆和遗忘机制.md]]