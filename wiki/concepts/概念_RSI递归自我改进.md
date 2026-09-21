---
type: concept
tags:
- RSI
summary: Recursive Self-Improvement（递归自我改进），AI 系统自我迭代优化的机制。在现代 Agent 工程中涵盖从提示词、驾具代码自修改到元研究闭环的多层阶梯。
sources:
- wiki/sources/OpenAI前VP_Lilian_Weng_AI自我改进的近路不是改权重.md
- wiki/sources/这是一篇把RSI讲明白的科普级综述.md
updated: '2026-09-20'
---

# 概念：RSI递归自我改进

## 定义

**RSI（Recursive Self-Improvement，递归自我改进）** 指 AI 系统能够反身分析自身性能并改进自身架构、运行逻辑或认知机制，且改进后的系统更擅长进行下一轮改进，从而形成指数级增益正反馈闭环的理论与工程范式。

## 四层梯度分界标准

根据现代 RSI 工程评测框架，自我改进被严格区分为四个可观察的递进层级：
1. **持久改进（Persistent Improvement）**：改动写入权重、情景记忆、工具链或驾具代码，跨任务持久生效而非单次上下文临时效果；
2. **自主闭环（Autonomous Loop / 有界 RSI）**：系统在人类限定的安全沙盒内能够自主完成“识别缺陷 $\to$ 提出变体 $\to$ 实验验证 $\to$ 评估接纳”的完整闭环；
3. **递归增益（Recursive Gain / 点火 Ignition）**：系统不仅在特定任务基准上提升分数，更**显著提升了自身产生下一次有效改进的能力**，正式跨入复利加速区间；
4. **稳健与可控（Robustness & Open-ended RSI）**：增益在固定资源与分布外隐藏评测下保持稳健泛化，且不发生奖励作弊（Reward Hacking）、系统复杂度膨胀或对齐失控。

## 历史演进的五次边界推进

1. **推理与记忆反思（2022-2023）**：以 Reflexion 为代表，模型参数冻结，通过自然语言事后复盘构建外部情景记忆（错题本）；
2. **自生成数据与参数微调（2022-2024）**：以 STaR（推理链自举）与 SPIN（与历史策略自博弈微调）为代表，将改进信号固化写入模型权重；
3. **评判权移交与元评判（2022-2025）**：从 Constitutional AI 到 Self-Rewarding 与 Meta-Rewarding，逐步将打分权交由模型自身，但伴随严重的“尺子变弯”与评判标准漂移挑战；
4. **驾具代码自修改（2023-2026）**：通过 [[concepts/概念_Harness_Engineering_宿主编排工程|Harness Engineering]] 与代码生成，以 [[concepts/概念_Self_Harness_自主进化宿主系统|Self-Harness]]、达尔文哥德尔机（DGM）及工业级 AgentX 为代表，让智能体在固定底座模型上搜索优化运行代码与工具编排；
5. **学习与研究过程闭环（2025-2026）**：涵盖自适应学习（SEAL）、环境沙盘（WebEvolver）、真实物理控制（Motus2）乃至双层元研究架构（Bilevel Autoresearch、AIDE²），使科研流程本身成为优化对象。

## 核心挑战与四道安全门禁

当前工程实践表明，有界净正闭环已在部分场景中实现，但尚未跨过第三层递归“点火”门槛。通往开放式 RSI 存在四道关键制约：
- **外部验证锚（External Verifier Anchor）**：评估器、编译器及安全权限必须独立于可进化系统之外，严禁系统篡改自身裁判标准；
- **防分布坍缩（Anti-Collapse）**：防止自生成数据循环迭代导致的表征多样性衰减与自我确认偏见；
- **深层算法突破难度**：当前智能体在工作流工程优化上表现突出，但在重写核心机器学习训练算法上仍显薄弱（如 AI4AI-Bench 仅 0.250）；
- **对齐与复杂度治理**：伴随自进化出现的死代码累积、逻辑膨胀以及由于缺乏元认知循环导致的不可审计风险。

## 来源与参考

- [[wiki/sources/OpenAI前VP_Lilian_Weng_AI自我改进的近路不是改权重]]
- [[wiki/sources/这是一篇把RSI讲明白的科普级综述]]
- [[concepts/概念_Harness_Engineering_宿主编排工程]]
- [[concepts/概念_Self_Harness_自主进化宿主系统]]
