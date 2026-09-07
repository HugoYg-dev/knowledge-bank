---
type: concept
tags:
- AI-Agent/skill
summary: Agent Skills 元工具架构（Agent Skills Meta-Tool Architecture）是 Claude Code 中扩展
  Agent 能力的一种设计模式：通过一个名为 Skill 的元工具（meta-tool）作为容器，动态加载和调度各个具体技能（skills），技能本质是领...
sources:
- wiki/sources/Claude_Agent_Skills_从第一性原理深入剖析.md
- wiki/sources/Firecrawl 新工具开源，anydoc，将各种输入转换为md.md
- wiki/sources/从第一性原理深度拆解_Claude_Agent_Skill_宝玉.md
- wiki/sources/写好CLAUDE.md_HumanLayer最佳实践.md
- wiki/sources/如何系统评价一个_Agent_Skill.md
- wiki/sources/搜索没有变便宜，但 Agent 把它拆成了新的供应链.md
updated: '2026-09-07'
---
# 概念：Agent Skills 元工具架构

## 定义

Agent Skills 元工具架构（Agent Skills Meta-Tool Architecture）是 Claude Code 中扩展 Agent 能力的一种设计模式：通过一个名为 `Skill` 的**元工具**（meta-tool）作为容器，动态加载和调度各个具体技能（skills），技能本质是**领域专属提示词模板**，通过注入对话上下文和修改执行上下文来改变 LLM 行为，而不执行任何代码。

## 核心公式

**Skill = 提示词模板 + 对话上下文注入 + 执行上下文修改 + 可选数据文件和 Python 脚本**

## 与传统工具的根本区别

| 维度 | 传统工具（Read/Bash/Write） | Skills |
|------|--------------------------|--------|
| 执行模式 | 同步直接执行 | 提示词扩展 |
| 目的 | 执行具体操作 | 引导复杂工作流 |
| 返回值 | 即时结果 | 上下文变化 |
| Token 开销 | ~100 tokens | ~1500+ tokens/轮 |

## 技能选择机制

**纯 LLM 推理，无任何算法路由**。系统将所有可用技能格式化为文本描述，嵌入 Skill 工具的 description 字段，由 Claude 在 Transformer 前向传播中自主决定是否匹配。没有嵌入/分类器/正则/关键词匹配。

## 渐进式披露（Progressive Disclosure）

三级信息逐步展开：
1. 元工具仅暴露 Frontmatter（name/description），供 Claude 决策
2. 选中技能后加载完整 SKILL.md 指令
3. 执行时按需加载 scripts/references/assets

## 双消息注入机制

技能调用时向对话历史注入两条用户消息：

- **消息1**（`isMeta: false`，用户可见）：50-200字符 XML 状态标签，提供透明度
- **消息2**（`isMeta: true`，用户隐藏）：完整 SKILL.md 内容（500-5000词），给 Claude 的指令

设计意图：透明度（用户知道哪个技能在运行）vs 干净（不用详细指令污染用户视图）。

## Frontmatter 关键字段

- `name`（必填）：技能名，作为 command 参数
- `description`（必填）：Claude 匹配用户意图的主要信号
- `allowed-tools`（可选）：预批准工具列表，支持通配符限定范围
- `model`（可选）：覆盖会话模型（默认 inherit）
- `disable-model-invocation`（可选）：仅允许用户手动 `/skill-name` 调用

## 技能资源三目录

```
my-skill/
├── SKILL.md              # 核心指令（<5000词）
├── scripts/              # Python/Bash 可执行脚本
├── references/           # 按需 Read 加载的文档
└── assets/               # 通过路径引用的模板/二进制
```

references 与 assets 的区别：references 通过 Read 工具加载到 Claude 上下文（消耗 Token）；assets 仅通过路径引用，不加载（不消耗 Token）。

## 四种常见模式

1. **脚本自动化**：将确定性逻辑卸载到 scripts/ 脚本
2. **读取-处理-写入**：文件转换数据处理
3. **搜索-分析-报告**：代码库分析模式检测
4. **命令链执行**：CI/CD 类多步骤工作流

## 大规模 Skill 路由与 MCP 协议分层

随着智能体接入能力规模化，工具系统面临上下文膨胀与协议互通的双重挑战：

### 1. 百级 Skill 分层路由选择器（Hierarchical Tool Selector）
当 Skill 数量突破 100 个时，若全量加载工具描述将导致上下文窗口严重退化。工程上采用三层路由架构：
- **类别粗排**：用轻量级规则匹配或小模型意图分类器，将全量工具池收敛到特定业务大类（如数据库、搜索、文件系统）；
- **向量精排**：在命中类别内，利用 Query 与各工具语义描述的 Embedding 计算余弦相似度，动态筛选 Top-5 注入当前 Prompt；
- **描述缓存**：对高频复用的工具元数据进行 Token 级缓存，大幅削减预处理延迟。

### 2. MCP 协议标准与 Skill 的架构定位区别
- **MCP（Model Context Protocol）**：标准化**通信契约与交互协议**。统一不同客户端与服务端间的工具发现、参数规范、通信格式与错误代码，解决跨系统复用与中立性问题；
- **Skill**：具体的**领域业务实现**。承载复杂的领域业务流、上下文注入模板与私有脚本。二者结合构成了“通用标准底座（MCP）+ 业务定制引擎（Skill）”的现代智能体扩展范式。

## 来源

- [[Claude_Agent_Skills_从第一性原理深入剖析]]
- [[从第一性原理深度拆解_Claude_Agent_Skill_宝玉]]