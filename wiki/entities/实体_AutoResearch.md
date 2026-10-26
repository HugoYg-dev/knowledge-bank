---
type: "entity"
tags:
  - "AI-Agent/coding"
  - "AI-Agent/multi-agent"
summary: "Andrej Karpathy 于 2025 年底开源的算法研究自进化实验原型系统，以 program.md + train.py + prepare.py 三文件和 keep/reset 棘轮机制为核心，后被美团等工业界团队演进为图探索自进化系统"
sources:
  - "wiki/sources/从 LOOP 到图探索 —— 算法模型的 AutoResearch 自进化系统架构演进之路  美团 · 技术团队.md"
updated: "2026-10-26"
---

# 实体：AutoResearch

## 简介

**AutoResearch** 是由知名 AI 科学家 [[entities/实体_Andrej_Karpathy|Andrej Karpathy]] 于 2025 年底开源的算法研究自进化实验原型系统（GitHub: `karpathy/autoresearch`）。该项目旨在探索通过大语言模型驱动自主实验循环，在夜间和周末无人值守环境下自动进行模型训练与超参/架构改进。

---

## 核心架构与机制设计

Karpathy 的开源原型以极简的三文件结构和刻意的“信任机制”著称：

1. **三文件极简组合**：
   - `program.md`：用自然语言明确描述研究规则、实验约束与目标；
   - `train.py`：智能体（Agent）**唯一被允许自主修改**的模型训练与算法代码；
   - `prepare.py`：负责基线评估与验证集指标计算（如 `val_bpb`）。
2. **冻结裁判与防篡改信任设计**：
   - 负责评估指标的 `prepare.py` 被物理冻结为不可修改文件，Agent 只能修改训练代码而无法更改评估逻辑，从机制上杜绝了模型“篡改裁判”的作弊可能。
3. **Git 棘轮机制（Keep / Reset Ratchet）**：
   - 单步训练完成后提取评估指标，若效果改善则执行 `git commit`（keep 保留），若指标退化则执行 `git reset`（回滚）；每一步改进均物理可审计、可回滚。
   - 在单张 H100 训练 5000 万参数教学级 GPT 的实测中，该系统在约 2 天内自主运行了约 700 次实验，产出约 20 个正向提交。

---

## 工业界落地挑战与演进

当将 Karpathy 的 AutoResearch 原型引入企业级真实业务场景时，暴露出三大底层瓶颈：
- **可信度问题**：规则纯靠自然语言 Prompt 声明，长程无人值守时模型认知幻觉会导致不可信决策；
- **环境差异**：本地单机同步极速训练 vs 企业云端训练平台的异步长周期（数小时）训练，指标体系具备复杂业务差异；
- **单线程 LOOP 的根本局限**：keep/reset 机制本质上是单线程串行状态机，同一时刻只能探索单条时间线，容易陷入局部最优。

针对上述瓶颈，[[entities/实体_美团|美团技术团队]] 在真实工业建模项目中对其进行了三次架构重构（V1 云端 LOOP → V2 异步状态机 → V3 CyclicGraph Engine），通过 **Spawn-Converge** 图探索架构实现正交并行验证，将探索速度提升 18 倍，并在真实业务线上推全取得收益。

---

## 关联实体与概念

- **创始人与核心实践者**：
  - [[entities/实体_Andrej_Karpathy|Andrej Karpathy]] — 开源原型作者
  - [[entities/实体_美团|美团技术团队]] — 企业级演进与 CyclicGraph Engine 实践
- **核心概念**：
  - [[concepts/概念_Harness_Engineering_宿主编排工程|Harness Engineering]]
  - [[concepts/概念_Loop_Engineering循环工程|Loop Engineering]]
  - [[concepts/概念_Self_Harness_自主进化宿主系统|Self-Harness]]
  - [[concepts/概念_Orchestrator_Worker_编排工模式|Orchestrator-Worker 编排模式]]
