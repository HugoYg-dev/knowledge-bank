---
type: concept
tags:
- AI-Agent/skill
- AI-Agent/coding
summary: Skill 触发评价必须同时评估漏触发（False Negative）与误触发（False Positive），引入 Description 负样本反例机制、L0 核心用例过滤与 Pass@k / Pass^k 严密分级。
sources:
- wiki/sources/如何系统评价一个_Agent_Skill.md
- wiki/sources/智能体 Skill 调优“焚诀”——业务逻辑之外的胜负手.md
updated: '2026-11-16'
---

# 概念：Skill 误触发与漏触发评价

## 定义

**Skill 误触发与漏触发评价** 是针对 Agent Skill 路由与选择阶段的量化测试规范。Skill 的第一道防线是准确被 Agent 识别并加载。评价需兼顾“该用未用”与“不该用而误用”两类偏差。

## 两类误区与评估指标

1. **漏触发（False Negative）**：原本需要 Skill 支持的复杂任务，Agent 未能感知并加载 Skill。
2. **误触发（False Positive）**：简单或无关指令误触发了高开销/强约束 Skill，引入额外的 Token 延迟与行为干扰。

## 指标权衡与业务分级

$$\text{Precision} = \frac{\text{正确触发次数}}{\text{所有触发次数}}$$
$$\text{Recall} = \frac{\text{正确触发次数}}{\text{所有应该触发的次数}}$$

- **高风险/高成本 Skill**：提升 Precision，严防误触发带来的越权或昂贵 Token 开销。
- **关键核心业务 Skill**：提升 Recall，防止漏触发导致模型自由幻觉。

## 负样本机制与路由调优实证（阿里千问实践）

在工业级投研平台评测实证中，近义 Skill 之间的路由错误绝大多数集中在边界模糊地带：
- **负样本反例的判别杠杆**：Description 缺少反例（不适用场景）声明时，路由准确率从基准 73% 骤跌至 53%；补足反例后跃升至 85%，响应时间降低 18.1%。证明负样本是划定技能边界最直接有效的手段；
- **意图黑洞防范**：按“话题”切分（如“公司基本面”）会导致周边意图被大面积吸入（Precision 仅 0.641）；改按“分析范式”切分后，系统性混淆消除，残留错误单向收敛；
- **Pass@k 与 Pass^k 严谨区分**：探索能力上限使用 Pass@k（$k$ 次至少一次正确），而生产上线回归必须强制使用 **Pass^k**（核心 L0 业务用例每次变更必须 $100\%$ 全对才能发布）。

## 关联

- [[concepts/概念_Agent_Skill系统化评价框架|概念_Agent_Skill系统化评价框架]]
- [[concepts/概念_Agent_Skills元工具架构|概念_Agent_Skills元工具架构]]
- [[sources/如何系统评价一个_Agent_Skill|如何系统评价一个_Agent_Skill]]
- [[wiki/sources/智能体 Skill 调优“焚诀”——业务逻辑之外的胜负手.md|智能体 Skill 调优“焚诀”——业务逻辑之外的胜负手]]
