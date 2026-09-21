---
type: "source"
tags: ["AI-Agent/coding", "AI-Agent/context-engineering", "AI-Agent/memory", "面试"]
summary: "一篇 Data Agent 一面复盘，从 miniclaude 项目延伸到工具、记忆、幻觉、ReAct、权限重试、死循环防护与 Subagent 设计。"
sources: ["raw/articles/快手data agent一面，我裂开了！！！.md"]
updated: "2026-08-03"
---

# 快手 Data Agent 一面复盘

## 来源信息

- 标题：快手data agent一面，我裂开了！！！
- 作者：AIGC小白入门记
- 发布时间：2026-07-14（正文署名时间为 2026-07-13 21:52）
- 原文：https://mp.weixin.qq.com/s/TAx39Oxk9BvV-ZWSqDZbGw

## 核心要点

- miniclaude 项目试图在不依赖闭源 API 的前提下，把大模型推理与操作系统级操作串联起来；项目实践暴露出的核心矛盾是权限过宽会带来风险，权限过窄又会限制行动能力。
- 文章将 Prompt Engineering 定位为任务表达层，将 Context Engineering 定位为动态组织系统指令、工具、外部数据与历史的信息层，将 Harness Engineering 定位为包含工具调用、状态、权限、重试、安全护栏和监控的系统层。
- 工具系统包含文件操作与命令行执行两类能力；工具描述决定模型能否正确选择工具和填写参数，错误处理则区分可重试的超时与不可重试的权限不足。
- 记忆分为当前会话上下文与可检索的长期记忆。长期记忆只保存关键决策、用户偏好和失败教训，并使用时间戳与相关性排序；文章指出当前实现为追加式写入，记忆合并与摘要仍是后续计划。
- 幻觉治理采用提示词约束、工具结果溯源和任务后反思三层措施，并明确承认无法完全消除幻觉，需要 Harness 校验与人工兜底。
- ReAct 通过“思考、行动、观察”循环动态调整计划；死循环防护包括最大步数、相同工具调用签名重复检测、状态停滞检测，以及提示模型在重复时改变策略。
- 权限设计遵循最小权限：读文件为基础权限，写文件需额外确认，Shell 执行需更高级别授权；重试只用于网络超时和限流等暂时性失败，并设置指数退避及最多三次的上限。

## 关联概念

- [[concepts/概念_上下文工程]]
- [[concepts/概念_Harness_Engineering_宿主编排工程]]
- [[concepts/概念_Agent三层记忆体系]]
- [[concepts/概念_多智能体协调]]

> 📎 **物理文献**：[[raw/articles/快手data agent一面，我裂开了！！！.md]]
