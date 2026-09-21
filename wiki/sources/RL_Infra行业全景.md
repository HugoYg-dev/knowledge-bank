---
type: source
tags:
- LLM/training/RL
- Infra/rl
summary: 海外独角兽 Cage 梳理 RL Infra 行业全景：RL 环境（应用沙盒/浏览器环境/世界模型）、RLaaS（Palantir 模式深度定制）、数据/评估三大模块；论证
  RL Scaling 将把 AI 从"人类数据时代"推向"Agent 体验时代"，迎来 RL 的 GPT-3 时刻。Cubox 高亮重点：Mechanize 复制训练（Replication
  Training）范式。
sources:
- raw/insights/RL Infra 行业全景：环境和 RLaaS 如何加速 RL 的 GPT-3 ....md
updated: '2026-07-01'
---
# RL Infra 行业全景：环境和 RLaaS 如何加速 RL 的 GPT-3 时刻

## 来源信息

- 标题：RL Infra 行业全景：环境和 RLaaS 如何加速 RL 的 GPT-3 时刻
- 作者：Cage / 海外独角兽（公众号）
- URL：https://mp.weixin.qq.com/s/-5lMX9oVHn6x0NI6QEZrrA
- 基于全文 ingest

## [重点/高亮] Mechanize 复制训练（Replication Training）

> Mechanize 提出复制训练的新范式：让 AI Agent 去完整复现现有软件产品或其中的特定功能，作为训练任务。任务成功与否可通过自动化方式验证（如 agent 生成的代码是否通过原始仓库所有单元测试）。巧妙地将开放、模糊的创造性任务转化为有明确、可验证奖励信号的 RL 问题，解决了长周期复杂任务设计奖励函数的难题。

- 利用人类已开发的大量软件作为蓝本，源源不断生成训练任务（类比预训练用互联网语料）
- 锻炼 AI 核心技能：精确阅读并理解长规格说明、严格 instruction following、发现并纠正自身错误、在长达数万行代码项目中保持连贯
- Founder 来自 Stripe 和 Epoch AI，获 Nat Fridman 和 Daniel Gross 天使支持

## 核心要点

### 1. 为什么需要 RL Infra

**Era of Experience**：Foundation Model 仅依赖静态人类数据性能提升边际递减（Richard Sutton & David Silver）。通过模拟环境试错，模型可学到长链条推理、复杂决策等 pretrain+SFT 难以获得的能力。

**当前规模差距**：DeepSeek-R1 RL 仅约 60 万道数学题（相当人类连续工作 6 年）；GPT-3 训练语料 3000 亿 token（数万年人类写作）。RL Scaling 需做到与 Pretrain 同量级计算量。

**现有 Infra 不足**：
- 训练环境稀缺受限（不能开 VM/Docker/Slack，无法多人协作）
- 生产环境悖论：真实环境学习高效但有安全/合规风险
- 奖励设计难题：reward hacking 问题

### 2. RL Infra Mapping 框架

三大模块：

**RL 环境类公司**：模拟环境搭建者，面向 AI Lab/中小团队，提供模拟训练环境+任务平台+基准测试。类比"游戏引擎服务游戏开发"。规模效应强但 research bet 属性浓。

**RLaaS 公司**：Palantir 模式，深入企业垂直领域。服务环节：奖励建模→自动化评分→模型定制与 RFT。高度定制化，单合同数千万美金级。

**数据/评估类公司**：提供高质量反馈数据和评测基准，充当"数据军火商"。

### 3. RL 环境详解

核心三要素：状态管理系统、任务场景、奖励/评估系统。

主要形态：
- **应用级沙盒**：CRM/ERP/客服票务系统模拟器（如 Salesforce CRMArena-Pro）
- **通用浏览器/桌面环境**：虚拟浏览器/OS/办公软件（computer use agent 路线）
- **环境世界模型**：用 AI 合成数据驱动生成新环境，摆脱手工搭建依赖

代表公司：
- **Mechanize**：复制训练平台（见高亮）
- **Veris AI**：Mirror Your Stack，企业数字孪生训练场（850万美元种子轮）
- **Halluminate**：computer use 环境平台，真实感沙盒+专有数据集评估

### 4. RLaaS 详解

服务环节：
1. **奖励建模**：将抽象业务 KPI 转化为可计算奖励函数
2. **自动化评分**：搭建自动评分管道对 rollout 严格打分
3. **模型定制与 RFT**：选取基础模型进行定制化强化微调

代表公司：
- **Fireworks AI**：从 Inference Infra 到 RFT，用户只需提供评分函数，其他全平台处理；与 Vercel 合作 RFT 训练代码修复模型媲美 GPT-4 且快 10-40x
- **Applied Compute**：OpenAI 前研究人员，pre-launch 1 亿估值/2000 万种子轮（Benchmark 领投），项目制深度绑定大企业
- **RunRL**：YC 出身，$80/node-hour 透明定价，民主化方向

### 5. 未来展望

- **RL 环境 vs RL 数据**：在线学习（on-policy）精确但昂贵缓慢；离线学习（off-policy）快但泛化差。可能是两者结合。投资上构成对冲组合。
- **RLaaS Palantir 模式**：嵌入专家→解决核心问题→构建专有数据飞轮→形成护城河。极可能在垂直行业催生"赢家通吃"，由一系列"小 Palantir"构成。

## 关联概念

- [[概念_RL环境]]
- [[概念_RLaaS_强化学习即服务]]
- [[概念_复制训练]]
- [[概念_RLVR_可验证奖励强化学习]]

## 关联实体

- [[实体_Mechanize]]
- [[实体_Fireworks_AI]]

---
> 📎 **物理文献**：[[raw/insights/RL Infra 行业全景：环境和 RLaaS 如何加速 RL 的 GPT-3 ....md]]