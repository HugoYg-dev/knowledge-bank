---
type: "entity"
tags: ["LLM/training/post-train", "Infra/training", "Skill/python"]
summary: "魔搭 ModelScope 团队开源的大模型微调与推理框架，提供轻量化模型训练、推理加速、决策模型专属损失函数及两级温度标定工程闭环。"
sources: ["wiki/sources/ms-swift倾情奉献_决策模型从原理到上手定制.md"]
updated: "2026-10-27"
---

# 实体：ms-swift

## 概述

**ms-swift** 是由阿里魔搭（ModelScope）开源社区团队主导研发的大模型（LLM/VLM）全生命周期轻量级微调与推理部署工程框架。代码仓库托管于 GitHub（`modelscope/ms-swift`）。框架全面覆盖主流开源大语言模型、多模态大模型的预训练、后训练（SFT/DPO/PPO/GRPO）与部署加速，并在业界率先针对[[concepts/概念_Decision_Model_专用判断模型|决策模型（Decision Model）]]提供了端到端专属训练、评估与校准工程支持。

## 核心特性

1. **广泛的模型与模态覆盖**：支持 Qwen、Llama、GLM、InternLM、Mistral 等前沿开源大语言模型与多模态模型（JEV-27B-VL、Clef、OmniJev、NanoJev 等）的微调与推理。
2. **轻量化微调技术集（PEFT）**：深度集成 [[concepts/概念_LoRA_低秩适应微调|LoRA]]、QLoRA、DoRA、AdaLoRA 等参数高效微调方法，支持 `all-linear` 快速全线性层适配。
3. **推理与部署生态联动**：无缝对接 vLLM、SGLang、LMDeploy 等高性能推理引擎，支持单卡与分布式多卡环境。
4. **决策模型模式（`--task_type decision`）**：在 SFT/后训练流程中将输出从自回归生成切换为固定候选项概率估计，实现 System 1 决策模型的闭环微调。

## 决策模型专项支持体系

针对新兴的决策模型范式，ms-swift 建立了完备的底层训练与工程管理支持：

1. **专属适当评分规则损失函数**：
   - `distill_rps`：结合教师蒸馏软目标与有序概率得分（RPS），专为 JEV-27B-VL 等多模态与分类模型设计；
   - `smooth_brier`：结合标签平滑交叉熵与 Brier 均方误差得分，专为多问题联合解码模型（如 Clef）设计；
   - `ce_rps`：结合无截断软交叉熵与 RPS，专为混合架构模型（如 OmniJev）设计；
   - `scoring`：不含校准惩罚项的纯对数评分基准模式。
2. **自动化训练与精度管理**：
   - **自动精度提升**：训练器自动激活评分头参数并将其提升至全精度训练，偏置（bias）与温度参数维持单精度，杜绝溢出；
   - **多维指标监控**：训练过程同时记录逐题准确率（Per-question Acc）与联合解码每记录全对准确率（Per-record Acc）；
   - **权重自动隔离与推理钩子**：评分头权重在保存时与底座主权重分离，推理阶段由框架自动挂载 Hook 动态加载。
3. **两级温度标定机制**：
   - 训练后回调自动注入校准流程，通过全局温度 $\tau_{global}$ 与题型相对温度 $\tau_{task\_relative}$ 的相乘微调，同时拉平模型宏观置信度偏差与特定题型（是非/多选/打分）的过度或欠自信；
   - 基于样本外两折交叉验证自动拟合温度；在保持预测答案与分类准确率完全不变的前提下，使 JEV 的期望校准误差（ECE）降低 46.7%。
4. **generic_decision 通用模型转换路径**：
   - 支持将普通生成式因果语言模型（如 Qwen3.5-4B）在不更换底座的前提下，通过轻量 LoRA 微调直接转换为 Jev 风格选项概率打分模型；
   - 实测通用对话模型经一轮训练即可从随机基线提升至 66.67% 的判断准确率。

## 使用范例

### 决策模型转换与微调训练（CLI）

```bash
swift sft \
    --model Qwen/Qwen3.5-4B \
    --model_type generic_decision \
    --task_type decision \
    --loss_type distill_rps \
    --tuner_type lora --target_modules all-linear \
    --dataset open_jev_jev:all \
    --output_dir output
```

### 决策推理与精度评估

```bash
swift infer \
    --model output \
    --task_type decision \
    --metric acc
```

## 关联概念与实体

- **关联概念**：
  - [[concepts/概念_Decision_Model_专用判断模型|概念_Decision_Model_专用判断模型]]：提供专项微调支持的目标模型架构。
  - [[concepts/概念_分类模型校准|概念_分类模型校准]]：框架内置的两级温度标定与 ECE 优化算法。
  - [[concepts/概念_LoRA_低秩适应微调|概念_LoRA_低秩适应微调]]：用于 generic_decision 参数高效转换的核心技术。
- **关联实体**：
  - [[entities/实体_Jev|实体_Jev]]：首个规模化决策模型产品与 benchmark 标杆。
  - [[entities/实体_OpenAI|实体_OpenAI]]：Decisions 接口的探索者。

## 支撑来源

- [[wiki/sources/ms-swift倾情奉献_决策模型从原理到上手定制.md|ms-swift倾情奉献：决策模型的从原理到上手定制]]
