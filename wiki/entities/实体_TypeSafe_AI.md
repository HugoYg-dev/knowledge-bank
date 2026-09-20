---
type: "entity"
tags: ["AI-Agent/tool-calling", "LLM/inference"]
summary: "由前 OpenAI 核心成员 Diogo Almeida 于 2024 年创立的 AI 研发机构，主打非自回归决策模型 Jev 与校准决策强化学习（RLCD）"
sources: ["wiki/sources/新模型Jev_爆红一周_不生成文字只输出概率却被玩出了花.md"]
updated: "2026-09-20"
timeline:
  - field: "funding"
    value: "4000万美元种子轮融资"
    valid_from: "2026-09-15"
    valid_to: null
    observed_at: "2026-09-20"
    sources:
      - "wiki/sources/新模型Jev_爆红一周_不生成文字只输出概率却被玩出了花.md"
  - field: "product"
    value: "发布首个概率决策模型 Jev (jev-1.13.0)"
    valid_from: "2026-09-15"
    valid_to: null
    observed_at: "2026-09-20"
    sources:
      - "wiki/sources/新模型Jev_爆红一周_不生成文字只输出概率却被玩出了花.md"
---

# 实体：TypeSafe AI

## 基本信息

- **创始人**：Diogo Almeida（前 OpenAI 团队成员，曾参与构建 ChatGPT 早期基础架构）。
- **成立时间**：2024 年创办，隐身开发两年后于 2026 年 9 月公开。
- **融资情况**：2026 年 9 月宣布完成 4000 万美元种子轮融资。
- **核心产品**：Jev 系列决策模型（首发版本 `jev-1.13.0`）。

## 技术路线与核心特征

1. **非自回归判别架构**：放弃 LLM 逐 token 串行生成文字的范式，转向基于输入状态（state）并行计算预定义问题（questions）概率分布的架构。
2. **RLCD 训练机制**：主打 [[concepts/概念_RLCD校准决策强化学习|RLCD（Reinforcement Learning for Calibrated Decisions）]]，专注于概率校准而非自然语言连贯性。
3. **定位软件基础路由层**：主张将模糊语境的自然语言条件转化为可被传统控制流（if/else、路由状态机）直接消费的确定性概率，充当 Agent 系统与大模型之间的轻量级分流中枢。

## 支撑来源

- [[wiki/sources/新模型Jev_爆红一周_不生成文字只输出概率却被玩出了花]]
