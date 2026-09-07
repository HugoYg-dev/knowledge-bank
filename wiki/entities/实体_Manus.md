---
type: entity
tags:
- AI-Agent/context-engineering
- AI-Agent/deep-research
summary: '- 类型：通用 AI Agent 产品'
sources:
- wiki/sources/100家顶尖AI初创公司的7个真相.md
- wiki/sources/AI应用实战_搞定复杂指令和工具膨胀.md
- wiki/sources/AI时代如何做独立开发.md
- wiki/sources/Context_Engineering_LangChain_Manus_NotebookLM.md
- wiki/sources/Manus团队测模型一点微小的经验.md
- wiki/sources/Manus创始人手把手拆解上下文工程.md
- wiki/sources/九大主流AI_PPT横测.md
- wiki/sources/也许当前最好的上下文工程讲解_LangChain联合Manus.md
- wiki/sources/浅谈上下文工程_Claude_Code_Manus_Kiro.md
updated: '2026-09-07'
---
# 实体：Manus

## 基本信息

- 类型：通用 AI Agent 产品
- 联合创始人：Peak Ji 季逸超
- 发布：2025年3月
- 特点：运行在VM沙盒中，典型任务约50次工具调用，输入/输出 token 比约100:1

## 架构特点

- 基于上下文工程而非微调，与底层模型保持正交
- 分层行动空间：函数调用 / 沙盒工具集 / 软件包与API 三层
- KV缓存优化：前缀稳定、追加式上下文、显式缓存断点
- 工具掩码（非移除）：上下文感知状态机 + logits掩码
- 文件系统作为外化记忆
- todo.md 复述注意力机制
- 保留错误路径作为负面样本

## 演进历史

- 已四次重构Agent框架（"随机梯度下降"式探索）
- MCP发布后从紧凑静态行动空间转变为可无限扩展系统
- 每次重构后发现最大飞跃来自简化而非增加复杂层

## AIGC：PPT 生成能力

[[九大主流AI_PPT横测]] 评测：Manus 能生成 PPT，遵循标准「大纲优先」模式（先生成大纲再创建完整演示文稿）。但暴露通用型工具的「最后一公里」短板——二次编辑和格式兼容性（导出到 PowerPoint/WPS）存在问题，现阶段更像快速产出内容框架的「玩具」而非可靠生产力工具。

## 深度研究评估与 Research Bench

在通用研究报告场景中，Manus 团队构建了内部评测基准 **Research Bench**（覆盖 9 个主流厂商模型与 36 个跨行业深度研究题目），用于评测 Agent 产出的 Research 质量并指导 Harness 迭代：
- **评估维度与信号**：将报告拆解为「包含哪些信息」（事实密度）与「信息如何组织」（理解成本/文风）两大维度，分别构建了基于 LLM 事实抽取的「信息量」指标与量化生硬用词的「隐喻率」指标。
- **过程笔记驱动 Harness 调优**：发现底层模型（如 GPT 旗舰）在搜索次数更多的情况下最终报告信息量反而低于 Claude，根因在于中间过程研究笔记格式（Claude 采用保真的 Bullet points，GPT 倾向长文本总结造成信息折损）。Manus 据此在 Harness 提示工程中规范笔记行为，实现了最终报告信息密度的显著提升。

## 出现文章

- [[Context_Engineering_LangChain_Manus_NotebookLM]]
- [[Manus创始人手把手拆解上下文工程]]
- [[Manus团队测模型一点微小的经验]]
- [[也许当前最好的上下文工程讲解_LangChain联合Manus]]
- [[浅谈上下文工程_Claude_Code_Manus_Kiro]]
- [[九大主流AI_PPT横测]]（AIGC）