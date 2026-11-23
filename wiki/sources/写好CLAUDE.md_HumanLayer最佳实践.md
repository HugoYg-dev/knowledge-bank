---
type: source
tags:
- Skill/claude-code
summary: HumanLayer 团队发布的 CLAUDE.md 编写最佳实践指南，基于上下文工程原则，从 LLM 无状态特性出发，提出"少即是多"、渐进式披露等核心方法论，帮助开发者写出高质量的
  [[概念_CLAUDE.md最佳实践|CLAUDE.md]] 文件。
sources:
- raw/articles/写好 CLAUDE.md _ HumanLayer 博客.md
updated: '2026-07-01'
---
# 写好 CLAUDE.md — HumanLayer 博客

## 来源信息

- **标题**：写好CLAUDE.md_HumanLayer最佳实践
- **作者**：HumanLayer
- **URL**：https://www.humanlayer.dev/blog/writing-a-good-claude-md


## 概述

HumanLayer 团队发布的 CLAUDE.md 编写最佳实践指南，基于上下文工程原则，从 LLM 无状态特性出发，提出"少即是多"、渐进式披露等核心方法论，帮助开发者写出高质量的 [[概念_CLAUDE.md最佳实践|CLAUDE.md]] 文件。

## 核心要点

### 核心原则：LLM 是无状态的
- LLM 权重推理时已固定，不会随时间学习
- 编码代理每次会话开始对代码库完全一无所知
- CLAUDE.md 是默认写入每次对话的唯一文件
- 因此必须将重要信息通过 CLAUDE.md 告知代理

### CLAUDE.md 应包含的三要素
- **What（内容）**：技术栈、项目结构、架构，给 Claude 一份代码库地图；单体仓库尤为重要
- **Why（原因）**：项目的目的，各部分的功能和用途
- **How（方法）**：项目中的工作方式，包工具偏好（如 bun 而非 node）、验证方式、测试/类型检查/编译命令

### Claude 会忽略 CLAUDE.md 的原因
- Claude Code 注入 system-reminder：`"this context may or may not be relevant to your tasks"`
- 若 Claude 认为内容与当前任务无关，会忽略该文件
- 文件中不适用于所有任务的信息越多，整体被忽略的概率越高

### 少即是多（核心建议）
- 研究表明前沿思维 LLM 能可靠执行约 150-200 条指令
- Claude Code 系统提示已包含约 50 条独立指令，占三分之一配额
- 随指令数量增加，执行质量**均匀下降**（非只忽略新指令）
- 较小模型性能指数衰减，前沿思维模型线性衰减
- LLM 倾向处理提示信息**边缘**的指令（开头和结尾）
- 建议：300 行以内最佳，越短越好；HumanLayer 自己的根 CLAUDE.md 不到 60 行

### [[concepts/概念_渐进式披露|渐进式披露（Progressive Disclosure）]]
- 将特定任务指令保存在单独 Markdown 文件中，自描述性命名
- 示例目录结构：`agent_docs/building_the_project.md`、`running_tests.md`、`code_conventions.md` 等
- CLAUDE.md 中列出文件+简要描述，指示 Claude 按需阅读
- 使用指向原始文件的指针，避免复制代码片段（易过时）
- 概念上类似 [[概念_Agent_Skills元工具架构|Claude Skills]] 的渐进加载机制

### 不要用 Claude 代替确定性工具
- 代码风格指南不应放在 CLAUDE.md 中
- LLM 成本更高、速度更慢，不适合替代 linter/formatter
- 推荐：用 Stop hook 运行 linter，将错误呈现给 Claude 修复
- 推荐工具：Biome（支持自动修复）
- LLM 是情境学习者——会从代码库现有模式中学习

### 不要使用 /init 自动生成
- CLAUDE.md 进入每个会话，是**杠杆作用最大的点**
- 一行糟糕的 CLAUDE.md 影响所有后续工作流产物
- 应精心手写，仔细考虑每一行

## 总结六条规则
1. 定义项目的 Why/What/How
2. 少即是多，减少指令数量
3. 内容简洁且具有普遍适用性
4. [[concepts/概念_渐进式披露|渐进式披露]]——告诉 Claude 如何找到信息而非全部展示
5. 用确定性工具处理代码格式
6. CLAUDE.md 是最高杠杆点，不要自动生成

## 关联概念

- [[概念_CLAUDE.md最佳实践]]
- [[概念_上下文工程]]
- [[concepts/概念_渐进式披露]]
- [[概念_Agent_Skills元工具架构]]
- Claude_Code工作流

---
> 📎 **物理文献**：[[raw/articles/写好 CLAUDE.md _ HumanLayer 博客.md]]