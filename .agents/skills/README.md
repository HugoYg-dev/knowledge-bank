# .agents/skills/ — Agent 专业能力与技能扩展库

本目录存放 AI Agent 在特定领域或格式下的扩展能力定义（Agent Skills）。每个技能为独立子目录，遵循标准化规范，包含专属指令 `SKILL.md` 及支撑素材。

---

## 已注册技能清单

| 技能目录 | 定位与核心作用 | 规范入口 |
| :--- | :--- | :--- |
| [`human-writing/`](human-writing/) | **自然中文活人感创作技能**：用于知乎回答、长文博客、技术复盘与深度评测，规避 AI 腔、陈词滥调与机械转折，保持自然生动的活人表达。 | [`human-writing/SKILL.md`](human-writing/SKILL.md) |
| [`obsidian-markdown/`](obsidian-markdown/) | **Obsidian Flavored Markdown 规范技能**：指导 Agent 编写合规的 Obsidian 专有语法，包括双向链接 `[[]]`、嵌入 Embeds `![[]]`、Callouts 标注块及 YAML Frontmatter 属性。 | [`obsidian-markdown/SKILL.md`](obsidian-markdown/SKILL.md) |
| [`obsidian-bases/`](obsidian-bases/) | **Obsidian Bases 数据库视图技能**：用于创建与编辑 `.base` 文件，提供类数据库的多维表格、卡片看板、动态过滤与公式聚合能力。 | [`obsidian-bases/SKILL.md`](obsidian-bases/SKILL.md) |
| [`json-canvas/`](json-canvas/) | **JSON Canvas 可视化画板技能**：用于解析、创建与维护 `.canvas` 画板文件，管理思维导图节点、文本块、分组及关联连线。 | [`json-canvas/SKILL.md`](json-canvas/SKILL.md) |

---

## 技能开发与使用规范

1. **结构标准**：每个新技能必须拥有独立的目录与 `SKILL.md` 顶层指令文件，必要时配备 `references/` 详细参考或 `scripts/` 工具。
2. **能力边界**：Skill 仅提供特定场景的专业方法论与辅助工具，**不得覆盖或违反根目录 `AGENTS.md` 的架构分层、来源约束与安全纪律**。
