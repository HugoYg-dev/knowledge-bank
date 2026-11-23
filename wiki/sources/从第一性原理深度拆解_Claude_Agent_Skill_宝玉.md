---
type: source
tags:
- AI-Agent/skill
- AI-Agent/context-engineering
summary: 宝玉翻译 Han Lee 深度文章：从源码层面解构 Claude Agent Skill 元工具架构，含双消息注入机制与执行上下文修改全生命周期
sources:
- raw/articles/从第一性原理深度拆解 Claude Agent Skill _ 宝玉的分享.md
updated: '2026-07-01'
---
## 来源信息

- 原文：Han Lee，翻译：宝玉 baoyu.io
- 原始链接：https://baoyu.io/translations/claude-skills-deep-dive
- 英文原文：https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/

## 核心要点

### Skills 的本质定义

Skills = 提示词模板 + 对话上下文注入 + 执行上下文修改 + 可选数据文件和 Python 脚本

技能不是可执行代码，不运行任何程序，不在系统提示词中。它们存在于 API 请求的 `tools` 数组中，作为 `Skill` 元工具的描述字段。

### [[concepts/概念_渐进式披露|渐进式披露（Progressive Disclosure）]]

构建技能最重要的概念：
1. 首次披露 Frontmatter（最少信息：name/description/license）
2. 选中技能后加载完整 SKILL.md
3. 执行时按需加载辅助资源、参考资料和脚本

### SKILL.md Frontmatter 字段详解

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 必填 | 用作 Skill Tool 的 command 参数 |
| `description` | 必填 | Claude 判断何时调用的主要信号；系统自动附加来源信息 |
| `when_to_use` | 未文档化 | 附加到 description 后，建议不用于生产 |
| `allowed-tools` | 可选 | 支持通配符限定权限范围；常见错误是列出所有工具 |
| `model` | 可选 | 默认 inherit 继承会话模型 |
| `disable-model-invocation` | 可选 | true 时仅支持用户手动 `/skill-name` 调用 |
| `mode` | 可选 | true 时显示在技能列表顶部"模式命令"区域 |

### Skill 元工具内部架构

`Skill` 工具与 Read/Bash/Write 并列在 tools 数组中。关键特征：`prompt` 字段是动态生成器，运行时聚合所有可用技能名称和描述，默认 15,000 字符的 Token 预算限制。

普通工具 vs Skill 工具对比：
- Token 开销：普通工具 ~100 tokens；Skill ~1,500+ tokens 每轮
- 执行复杂度：普通工具 3-4 条消息；Skill 5-10+ 条消息
- 上下文：普通工具静态；Skill 动态（每轮修改）

### 双消息注入机制（核心设计）

技能执行时注入两条独立用户消息：

**消息1（`isMeta: false`，用户可见）**：极简 XML 状态指示器（50-200字符）
```xml
<command-message>The "pdf" skill is loading</command-message>
<command-name>pdf</command-name>
```

**消息2（`isMeta: true`，用户隐藏，发送给 API）**：完整 SKILL.md 内容（500-5000词）

为什么要分两条？单条消息设计面临不可能的选择：要么把数千字 AI 指令暴露给用户，要么完全隐藏失去透明度。双消息分离通过 `isMeta` 标志实现：透明度（消息1）+ 详细指令（消息2）。

### 执行上下文修改

技能通过 `contextModifier` 函数修改执行上下文：
1. **工具权限**：将 `allowed-tools` 中的工具加入 `alwaysAllowRules`，预批准无需用户确认
2. **模型覆盖**：如果 Frontmatter 指定了 model，覆盖会话模型

### 完整执行生命周期（pdf 技能案例）

1. 启动扫描：并行加载用户/项目/插件/内置技能
2. 用户请求 → Claude 阅读 `<available_skills>` → LLM 推理匹配 → 调用 Skill(command="pdf")
3. 验证（5种错误码）→ 权限检查（允许/拒绝/询问）→ 加载 SKILL.md
4. 注入双消息 + 生成 contextModifier → 发送 API
5. Claude 在增强上下文中执行 Bash(pdftotext) + Read → 返回结果

### 技能 vs 传统工具设计哲学

> 通过将专业知识视为"修改对话上下文的提示词"和"修改执行上下文的权限"，而不是"执行的代码"，Claude Code 实现了传统函数调用难以企及的灵活性、安全性和可组合性。

与 ChatGPT 不同，Claude 的 skills 不在系统提示词中（ChatGPT 工具占系统提示词约 90% Token），而是用临时 `isMeta: true` 消息实现有作用域的行为修改，技能结束后恢复正常上下文。

## 关键引文

> "技能不是执行离散动作并返回结果，而是注入全面的指令集，修改 Claude 对任务的推理和处理方式。" [高亮]

> "代码层面没有算法路由或意图分类。Claude Code 不使用嵌入（Embeddings）、分类器或模式匹配来决定调用哪个技能...这是纯粹的 LLM 推理...决策发生在 Claude 在 Transformer 模型的前向传播（Forward Pass）中。" [重点]

> "通过将专业知识视为修改对话上下文的提示词和修改执行上下文的权限，而不是执行的代码，Claude Code 实现了传统函数调用难以企及的灵活性、安全性和可组合性。" [重点]

## 关联

- [[Claude_Agent_Skills_从第一性原理深入剖析]]
- [[概念_MCP代码执行模式]]
- [[概念_上下文工程]]
- [[概念_渐进式披露]]
- [[概念_Agent思考工具]]
- [[实体_David_Soria_Parra]]

---
> 📎 **物理文献**：[[raw/articles/从第一性原理深度拆解 Claude Agent Skill _ 宝玉的分享.md]]