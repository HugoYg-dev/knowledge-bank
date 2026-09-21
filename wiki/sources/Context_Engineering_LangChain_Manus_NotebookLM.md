---
type: source
tags:
- AI-Agent/context-engineering
summary: LangChain 和 Manus 专家对话提炼的4条上下文工程反直觉原则：战略边界、可逆压缩、工具分层卸载、简化优先
sources:
- raw/articles/AI 代理的上下文工程：LangChain 和 Manas - Notebook....md
updated: '2026-07-01'
---
Context Engineering for AI
  Agents- LangChain and Mana.md
--- Context Engineering for AI
  Agents- LangChain and Mana.md
created: '2026-06-29'
updated: '2026-07-01'
confidence: high
---
## 来源信息

- 标题：Context Engineering for AI Agents: LangChain and Manas（AI 代理的上下文工程：LangChain 和 Manas）
- 来源：NotebookLM 对 LangChain × Manus 专家对话的提炼
- 关键人物：Lance Martin（LangChain 创始工程师）、Peak Ji 季逸超（Manus 联合创始人）

## 核心要点

### 定义
上下文工程 = "一种精妙的艺术和科学，用恰到好处的信息填充上下文窗口，以供下一步使用"（Karpathy 定义）

### 要点1：上下文工程是战略边界，不只是技术修复
- Peak 早期创业曾从零训练模型，一次训练+评估周期耗时1-2周，产品创新速度被模型迭代速度卡死
- 核心论点：上下文工程是应用层和模型层之间最清晰、最实用的分界线
- 选择上下文工程而非微调，让产品迭代速度独立于模型训练周期
- "be firm about where you draw the line right now context engineering is the clearest and most practical boundary between application and model"

### 要点2：并非所有上下文压缩都相同——可逆性至关重要
- Manus 定义"context rot（上下文腐化）"：模型在达到硬性上下文限制前就开始性能下降
- 设定"预腐化阈值"：通常 128K-200K token，作为触发上下文压缩的时机

**压缩（Compaction）— 可逆**
- 移除可从外部状态重建的信息（如文件内容只保留路径）
- 只压缩最旧的50%工具调用，保留最新的完整格式作为 few-shot 示例
- 可逆性关键："你永远不知道哪个过去的行动会在10步后突然变得极其重要"

**总结（Summarization）— 不可逆，最后手段**
- 总结前将完整上下文转储到文件备份，后续可用 glob/grep 检索
- 关键规则：总结时始终使用完整版数据，而非压缩版，防止信息累积损失

### 要点3：卸载工具，不只是数据——分层行动空间
解决"上下文混淆"（工具过多导致模型调错工具）：

- **第一层 Function Calling**：小而固定的原子函数集（读写文件、执行shell、搜索），缓存友好
- **第二层 Sandbox Utilities**：VM沙盒内预装命令行工具，通过 execute_shell 调用，适合大输出，无需改变函数调用空间
- **第三层 Packages & APIs**：Agent编写脚本调用外部API，只将最终结果返回上下文，适合内存密集型计算

### 要点4：更智能的Agent来自构建更少
- Manus 自发布以来重构了5次
- 最大的性能飞跃不是来自增加更多复杂的上下文管理层，而是来自简化和移除不必要的技巧
- "the biggest leap we've ever seen didn't came from like adding more fancy context management layers... they all came from simplifying"
- 核心建议：**"build less and understand more"**

## 关键引文

> "the delicate art and science of filling the context window with just the right information needed for the next step" [重点/高亮]

> "be firm about where you draw the line right now context engineering is the clearest and most practical boundary between application and model so trust your choice" [重点/高亮]

> "you never know like which past action will suddenly become super important like 10 steps later" [高亮]

> "the biggest leap we've ever seen didn't came from like adding more fancy context management layers or clever retrieval hacks they all came from simplifying or from like removing unnecessary tricks and trusting the model a little more" [重点/高亮]

> "if you like take one thing from today I think it should be build less and understand more" [重点/高亮]

## 关联

- [[也许当前最好的上下文工程讲解_LangChain联合Manus]] — 同一场对话的更详细中文解析
- [[Manus创始人手把手拆解上下文工程]] — Peak 亲写的 Manus 官方上下文工程总结
- [[浅谈上下文工程_Claude_Code_Manus_Kiro]] — 三产品实践对比
- [[概念_上下文工程]] 
- [[概念_Context_Rot_上下文衰退]]
- [[概念_分层行动空间]]
- [[实体_Peak_Ji_季逸超]]
- [[实体_LangChain]]

---
> 📎 **物理文献**：[[raw/articles/AI 代理的上下文工程：LangChain 和 Manas - Notebook....md]]