---
type: source
tags:
- AI-Agent/coding
summary: Anthropic 为 Claude Agent SDK 开发双 Agent 架构（初始化 Agent + 编码 Agent）解决长程 Coding
  任务的跨会话状态管理难题。
sources:
- raw/articles/Anthropic再发Agent神文：像人类工程师一样思考，解决「长程任务」难题.md
updated: '2026-07-01'
---
## 来源信息

- 原文：Anthropic 工程博客《Effective harnesses for long-running agents》
- 转载：AI寒武纪 微信公众号
- Cubox ID：7393599330126398303

## 核心要点

### 长程 Agent 面临的核心挑战

长程任务（跨越数小时甚至数天）的 Agent 需要分"会话"（Session）工作，每个新会话开始时就像没有过往记忆的新工程师接班。

仅靠**上下文压缩**不够——Claude 表现出两种失败模式：
1. **试图一次性完成所有工作**：中途耗尽上下文，留下半成品且缺乏文档
2. **过早宣布完工**：新 Agent 实例看到已有功能就误以为整体已完成

### 解决方案：双 Agent 架构

**初始化 Agent（Initializer Agent）**：第一个会话专用，负责：
- 生成 `init.sh` 脚本
- 创建 `claude-progress.txt` 进度文件
- 建立展示文件添加情况的初始 Git 提交

**编码 Agent（Coding Agent）**：后续每个会话致力于取得增量进展并留下结构化更新。

快速上手流程（每次会话开始时）：
1. `pwd` 查看工作目录
2. 读取 Git 日志和进度文件
3. 读取功能列表选择最高优先级未完成功能
4. 运行 `init.sh` 启动开发服务器
5. 运行基本端到端测试确认应用未损坏

### 环境管理三大支柱

**1. 功能列表（Feature List）**
- 初始化 Agent 创建包含所有功能需求的详细 JSON 文件（一个 claude.ai 克隆案例包含 200+ 功能点）
- 所有功能初始标记为 `"passes": false`
- 使用 JSON 格式优于 Markdown（模型不易错误修改 JSON）[重点/高亮]
- Prompt 需包含强硬指令：禁止删除或编辑测试，只允许改 `passes` 字段

**2. 增量进展（Incremental Progress）**
- 编码 Agent 每次只做一个功能
- 每次代码变更后：Git 提交（带描述性信息）+ 进度文件摘要
- 模型可利用 Git 回滚错误代码，恢复到工作状态

**3. 端到端测试**
- 明确提示 Claude 使用浏览器自动化工具（如 Puppeteer MCP server）进行测试
- 让 Claude 看到截图，识别并修复代码中不明显的 Bug

### 故障模式与对应方案

| 问题 | 初始化 Agent | 编码 Agent |
|------|-------------|-----------|
| 过早宣布完成 | 建立包含详细功能描述的 JSON 文件 | 读取功能列表，只选一个功能工作 |
| 环境遗留 Bug | 建立初始 Git 仓库和进度文件 | 读取进度和 Git 日志；运行基础测试；结束时提交 |
| 过早标记完成 | 建立功能列表文件 | 仔细测试后才标记通过 |
| 浪费时间研究启动方式 | 编写 init.sh 脚本 | 直接读取并运行 init.sh |

### 未解决问题

- **单 Agent vs 多 Agent**：通用编码 Agent vs 测试 Agent/QA Agent/代码清理 Agent 多专业分工，尚无定论
- **领域泛化**：当前针对全栈 Web 开发，未来可推广至科学研究、金融建模等

## 关键引文

> 实验发现，使用 JSON 格式优于 Markdown，因为模型不太容易错误地更改或覆盖 JSON 文件。同时，提示词需包含强硬指令，禁止删除或编辑测试，只允许更改 passes 字段的状态 [重点/高亮]

## 关联

- [[概念_Orchestrator_Worker_编排工模式]]
- [[概念_Agent感知记忆推理三能力]]
- [[实体_Anthropic_Research系统]]
- [[概念_MCP代码执行模式]]
- [[概念_上下文工程]]

---
> 📎 **物理文献**：[[raw/articles/Anthropic再发Agent神文：像人类工程师一样思考，解决「长程任务」难题.md]]