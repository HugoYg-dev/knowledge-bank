---
type: source
tags:
- AI-Agent/skill
- AI-Agent/coding
summary: 基于 Karpathy 的 LLM Wiki 理念，结合 Claude Code（大脑）、Obsidian（可视化图谱眼睛）与飞书机器人（移动端手），实现自动化知识入库与复利积累。
sources:
- raw/articles/Claude Code + Obsidian + 飞书，我搭了一套会自己长大的知识库.md
updated: '2026-07-06'
published: '2026-04-14'
---
## 来源信息

- 原文：[Claude Code + Obsidian + 飞书，我搭了一套会自己长大的知识库](https://mp.weixin.qq.com/s/QTSqMJm4rXKHHzPLae5xKw)
- 作者：翻斗花园二蛋 / 2026-04-14
- 物理文献：`raw/articles/Claude Code + Obsidian + 飞书，我搭了一套会自己长大的知识库.md`

## 核心要点与关键引文

### 1. 痛点：RAG 缺乏复利，只是“临时抱佛脚”
- **传统 RAG 缺陷**：每次查询时去向量数据库检索零散片段并拼接回答，查询完后毫无沉淀。系统无法理解概念间的深入展开与逻辑冲突，导致“每次翻课本但从不做笔记”，没有知识复利。
- **复利效应（Compounding）**：知识管理应像投资，今天存入的概念能与新概念产生引用与补充。时间越长、节点与连接越密，价值呈指数级增长。

### 2. 核心理念：LLM Wiki 范式转变（由 Andrej Karpathy 提出）
- **根本翻转**：**不要在查询时才去处理知识，要在摄入（Ingest）时就完成结构化与编译**。
- **三层架构比喻**：
  - **[[实体_Obsidian]] 是 IDE**（直接查看 Markdown 与可视化图谱 Graph View）。
  - **LLM 是程序员**（不是搜索引擎，而是知识库管理员，负责整理、维护交叉引用、更新摘要与检查矛盾）。
  - **Wiki 是代码库**（结构化的中间层知识）。
- **规则指引**：通过配置文件 `CLAUDE.md` 作为“员工手册”与 [[概念_系统提示词四层架构]]，指导 AI 理解知识体系结构、处理规范与操作流程。

### 3. 三件套实践落地：Claude Code + Obsidian + 飞书
- **[[实体_Claude_Code]]（大脑）**：执行抓取、提炼知识点、生成/更新 wiki 页面、维护双向引用（通常一篇文章触发更新 3~10 个页面），并自动同步 `INDEX.md` 与 `LOG.md`。针对微信反爬自动调用 Playwright 浏览器。
- **[[实体_Obsidian]]（眼睛）**：本地文件夹作为 Vault，实现零基建依赖的纯 Markdown 存储与图谱可视化。
- **飞书机器人（手）**：通过 `Claude-to-IM` 打通移动端 IM 与本地 Claude Code，把“回家再整理”变成“随时随地发送即入库”。

### 4. 从“信息存储”到“知识编译”
- 过去十年的笔记工具只解决了“存”的问题，而整理成本随规模指数增长导致人类放弃。
- 现在的 AI Agent 将整理成本降至近乎零，实现**渐进式披露**（Workspace -> App -> Context 层级快速定位），在摄入端预先完成编译，查询时直接输出结构化全局全景。

## 涉及主题与概念

- 核心思想：[[概念_LLM_Wiki范式]]、知识编译与复利、[[概念_渐进式披露]]
- 对比分析：[[概念_RAG与LLM_Wiki对比]]
- 工具链：[[实体_Claude_Code]]、[[实体_Obsidian]]、[[实体_Andrej_Karpathy]]

> 📎 **物理文献**：[[raw/articles/Claude Code + Obsidian + 飞书，我搭了一套会自己长大的知识库.md]]