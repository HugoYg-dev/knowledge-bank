---
type: concept
tags:
- AI-Agent/tool-calling
- AI-Agent/prompt-engineering
summary: 将'思考'封装为 MCP 工具强制模型在每次工具调用前结构化规划，比纯 Prompt 指令遵循更稳定
sources:
- wiki/sources/HumanInTheLoop用MCP实现.md
- wiki/sources/从第一性原理深度拆解_Claude_Agent_Skill_宝玉.md
updated: '2026-06-29'
---


# 概念_Agent思考工具

将"规划与思考"封装为一个 MCP/Function Call 工具，强制 Agent 在每次调用业务工具前先调用该工具，输出结构化的思考、计划和行动。

## 动机

- 纯 Prompt 指令（"你必须进行充分规划"）对未经后训练的开源模型效果打折
- 工具调用有固定格式约束（参数名、类型），比"请你做规划"这类模糊指令遵循效果更好
- 推理模型的思维链历史会被 chat template 截断，思考工具的内容保留在上下文中，对多轮工具调用更有益

## 两种实现

**Anthropic 版（think 工具）**：
```json
{
  "name": "think",
  "description": "用于思考，不获取新信息，只将思考附加到日志",
  "input_schema": { "thought": "string" }
}
```

**蚂蚁集团扩展版（思考和规划工具）**：
```json
{
  "name": "think_and_plan",
  "input_schema": {
    "thought": "当前分析/假设/洞见",
    "plan": "任务分解为可执行步骤",
    "action": "下一步具体行动（含工具名）",
    "thoughtNumber": "步骤编号"
  }
}
```

## 使用规则（System Prompt 核心）

> 在每次调用其他任务工具之前，你**必须首先**调用思考和规划工具；思考完成后可继续并行调用多个任务工具；工具结果返回后，必须再次调用思考工具，如此循环。

## 效果数据（τ-bench 评测，Claude 3.7）

| 场景 | 基线 | 优化后 think 工具 | 提升 |
|------|------|-----------------|------|
| 航空客服 | 0.370 | 0.570 | +54% |
| 零售客服 | 0.783 | 0.812 | +3.7% |

SWE-bench：OpenAI Prompt 引导规划提升 4%。

## 与推理模型的关系

- claude-sonnet-3.7 非推理模式 + think 工具，效果优于纯推理模式
- 可能原因：推理模式思维链不受 Prompt 干预；think 工具可提供 few-shot 示例指导领域特定思考

## 相关概念

- [[概念_MCP协议]]
- [[概念_CoT_高级思维链方法]]

## 来源

- [[HumanInTheLoop用MCP实现]]