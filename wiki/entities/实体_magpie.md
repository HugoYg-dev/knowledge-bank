---
type: "entity"
tags:
  - "AI-Agent/coding"
summary: "由 yetone 发起的开源本地 LLM 网关，以全 AI Agent 编写、审查、合并与发版闭环及错题本硬规则晋升机制为核心特征"
sources:
  - "wiki/sources/yetone 的魔法：magpie 是怎么让 AI 自己维护项目的.md"
updated: "2026-11-09"
---

# 实体：magpie

## 简介
**magpie** 是由开发者 yetone 发起的开源本地大语言模型网关，旨在将 [[entities/实体_Claude_Code|Claude Code]]、[[entities/实体_Codex|Codex]]、Gemini CLI 等主流编程智能体（Coding Agent）无缝接入任意模型与订阅端点。在开源初期 19 天内迅速积累 9,400+ GitHub Stars，并因由 AI Agent 完全自主闭环进行代码编写、审查、合并与高频发版而成为智能体软件工程领域备受关注的标志性项目。

## 全 AI 自动化研发闭环架构

magpie 的工程实践展现了高度自收敛的 [[concepts/概念_Loop_Engineering循环工程|Loop Engineering（循环工程）]] 落地范式：

1. **路由表与错题本双核规范（AGENTS.md + LESSONS.md）**：
   - **路由表（AGENTS.md）**：作为顶层索引，自身不堆砌规则，仅指引 Agent 在执行不同子系统任务、代码编写或 PR 审查时查阅对应的独立规范文档（如 `docs/code-standards.md`）；
   - **错题本（LESSONS.md）**：由 Agent 每日夜审自动生成，聚焦返工、误合与弱验证三类问题，记录具体规则、原因及关联 commit/issue 凭据。
2. **Seen 3× 经验晋升硬规则机制**：
   - 错题本中每条教训附带历史出现频次；
   - 设定“事不过三”阈值：同一条教训在 3 个不同日期的复盘中出现（Seen 3×），即自动从经验层（`LESSONS.md`）迁入规范层（`code-standards.md`），成为所有 PR 审查强制核验的硬门禁。
3. **严苛确定性 PR 验收门禁**：
   - **回退测试（Red check）**：代码还原后新测试必须切实失败，避免无意义的虚假测试；
   - **真实环境实测**：多厂商接口必须绑定真实账号和配置完成真机验证；
   - **显式声明未测项（Not run）**：禁止隐式忽略未跑测试；
   - **防并发破坏**：合并指令强绑定 `--match-head-commit`，防止审查后并发提交穿透检查。
4. **人机边界切分（Human in the Loop）**：
   - **人类责任面**：负责高阶战略与不可违背的产品决策（如交互逻辑）、安全放行闸门与外部社区反馈；
   - **Agent 责任面**：负责长程具体实现、代码重构、测试编写、相互审查、分支合并与版本发版。人类只需给出简短的自然语言吐槽，Agent 自主补齐工程闭环。

## 关联页面
- **宿主与工具生态**：[[entities/实体_Claude_Code|Claude Code]]、[[entities/实体_Codex|Codex]]
- **核心概念**：[[concepts/概念_Loop_Engineering循环工程|Loop Engineering 循环工程]]、[[concepts/概念_Harness_Engineering_宿主编排工程|Harness Engineering 宿主编排工程]]
- **支撑来源**：[[wiki/sources/yetone 的魔法：magpie 是怎么让 AI 自己维护项目的.md|yetone 的魔法：magpie 是怎么让 AI 自己维护项目的 (Source 摘要)]]
