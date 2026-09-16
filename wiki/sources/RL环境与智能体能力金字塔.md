---
type: source
tags:
- LLM/training/RL
- Infra/rl
summary: Surge AI 用 9 个模型在自建 RL 环境（Corecraft 客服场景）执行 150 项任务，提出「智能体能力金字塔」：工具使用→规划/目标设定→适应性→接地气（groundedness）→常识推理。GPT-5/Claude
  Sonnet 4.5 遥遥领先但仍失败超 40%；常识推理是 GPT-5 与人类水平的主要差距。
sources:
- raw/articles/RL 环境与智能体能力金字塔 _ 宝玉的分享.md
updated: '2026-07-01'
---
# RL 环境与智能体能力金字塔

## 来源信息

- 标题：RL 环境与智能体能力金字塔
- 译者：宝玉（baoyu.io 翻译）
- 原文：Surge AI, https://surgehq.ai/blog/rl-envs-real-world
- URL：https://baoyu.io/translations/rl-envs-real-world
- 基于全文 ingest

## 核心要点

### 测试设置

- "雇佣" 9 个 AI 模型，在 RL 环境中执行 150 项任务
- 结果：GPT-5 和 Claude Sonnet 4.5 遥遥领先独一档，但失败率仍超 40%

### "培育"一个 RL 环境

每个 RL 环境需三样东西：
- **连贯的世界模型**：定义环境背景宏观框架
- **一套实体（entities）**：世界中的物体及其关系
- **工具系统**：智能体与实体互动的接口

环境是逐渐"培育"演化出来的，由拥有专业领域知识的贡献者（Surgers）填充逼真实体和任务。

### Corecraft 公司（测试环境）

- 在线零售商，专卖高性能 PC 零件和定制电脑
- 世界模型=公司本身，实体=客户/订单/支持工单
- 智能体扮演"客服专员"，任务从简单查询到多步骤操作流程

### 智能体能力金字塔（Hierarchy of Agentic Capabilities）

由底向上五层（模型须先熟练前一层才能进入下一层）：

**1. 基础工具使用、规划与目标设定**
- 需持续做到：分解多步任务为小目标、为每个目标找合适工具并排序、准确填参数、不跑偏执行
- 停留此层：GPT-4o、Mistral Medium、Nova Pro
- 典型错误：把 "gold" 当客户 ID；把 "high" 传给 status 而非 priority 参数；把数组传给需要 string 的参数（违反 MCP schema）；跳过 searchProducts 直接把产品名传给 product_id

**2. 适应性（Adaptability）：当计划遭遇现实**
- 遇到意外结果时能及时调整、中途修改计划
- 常在此出问题：Gemini 2.5、Qwen3
- 例：品牌 "Vortex Labs"（有空格）vs 系统 "VortexLabs"（无空格），弱模型把空结果当事实直接回复"不卖"；Claude Sonnet 4.5 主动尝试不同搜索参数（适应）

**3. 接地气（Groundedness）：时刻紧贴现实**
- 不幻觉 ID、不跑题、不捏造脱离现实的事实
- 问题模型：Kimi K2 Turbo（规划适应强但接地气差，搞错年份 2024/2025）
- Claude Sonnet 4.5 也有此问题（捏造邮箱/工单优先级标错），是它与 GPT-5 的主要差距

**4. 常识推理（Common-Sense Reasoning）：最后的边疆**
- 进入"AGI"领域，无法明确训练的能力
- 是 GPT-5 与人类水平产生差距的主要原因
- GPT-5 失败例：未推断"包裹刚到"=已收货应归类"退货"；未用启发式而逐天搜索 31 天订单；把"我账户名应是 Sarah Kim"误解为改名指令而非身份线索

### 关键结论

- 精通前四层（工具/规划/适应性/接地气）≠ 达到人类水平，仅是基础能力
- 常识推理目前无法清晰定义，但缺失时一眼可见；是可训练子技能还是大规模训练的涌现属性尚待观察
- 2025 是"智能体们终于能足够连贯行动，以至于可以开始分析其常识推理能力"的元年

## 关联概念

- [[概念_智能体能力金字塔]]
- [[概念_RL环境]]
- [[概念_接地气Groundedness]]

---
> 📎 **物理文献**：[[raw/articles/RL 环境与智能体能力金字塔 _ 宝玉的分享.md]]