---
type: source
tags:
- AI-Agent/context-engineering
summary: LangChain Lance Martin × Manus Peak Ji 对话详细实录：上下文压缩两种模式、Agent上下文隔离两种模式、三层行动空间、避免过度工程化等实战策略
sources:
- raw/articles/也许当前最好的「上下文工程」讲解_LangChain联合Manus季逸超最新分享....md
updated: '2026-07-01'
---
## 来源信息

- 标题：LangChain联合Manus季逸超最新分享！也许当前最好的「上下文工程」讲解
- 来源：AI寒武纪（作者：花不玩）
- 原始内容：LangChain 创始工程师 Lance Martin × Manus 联合创始人 Peak Ji（季逸超）视频对话
- Peak 背景：《麻省理工科技评论》2025年35岁以下创新者

## 核心要点

### 上下文工程兴起背景
- Agents 核心特征：循环调用工具，每次工具调用结果追加到对话历史
- 规模问题：Manus典型任务约50次工具调用；生产Agent可达数百轮
- 性能悖论：功能依赖大量上下文，但上下文过长导致性能下降（Context Rot）
- Chroma 团队报告证实：随上下文长度增加，模型性能显著下降

**五大策略**：Offloading / Reduction / Retrieval / Isolation / Caching

### 战略选择：优先上下文工程而非过早模型专业化
- 过早构建专用模型的风险：
  1. 扼杀创新速度（产品迭代被模型迭代周期卡死）
  2. 优化目标错位（训练好的模型可能一夜之间被MCP等变化颠覆）
  3. 重复造轮子（变相成为LLM公司）
- Peak核心论点：**上下文工程是应用层和模型层之间最清晰、最实用的边界**

### 上下文精简：压缩 vs 总结

**压缩（Compaction）— 可逆信息外化**
- 将可重建信息移出上下文（如文件内容只保留路径）
- 只压缩最旧50%的工具调用，保留最新完整格式（为了few-shot效果）
- 可逆性是关键：无法预知哪条历史在10步后会变关键

**总结（Summarization）— 不可逆，最后手段**
- 总结前将完整上下文转储到文件备份
- 总结时使用未经压缩的完整版数据
- **使用结构化schema而非自由格式**：字段如"修改了哪些文件"/"用户目标"/"上次进行到哪"
- 始终保留最后几次工具调用的完整细节（保证行为连续性）

**基于阈值的工作流程**：
1. 确定预腐烂阈值（128K-200K，通过大量评估确定）
2. 接近阈值时触发压缩（选择性，不全量）
3. 压缩多轮增益变微时触发总结
4. 总结使用完整版数据，保留最后几次完整记录

### 上下文隔离两种模式（借鉴 Go 语言哲学）
"Do not communicate by sharing memory; instead, share memory by communicating."

**模式一：通过通信（By Communicating）**
- 工作流：主Agent封装清晰指令 → 发送给子Agent → 子Agent干净上下文独立完成 → 返回结果
- 适用：指令简短、主Agent只关心最终产出
- 例子：代码库搜索（Claude Code 的 task 工具就是此模式）

**模式二：通过共享上下文（By Sharing Context）**
- 子Agent能看到主Agent的完整历史，但拥有自己的系统提示和行动空间
- 适用：最终产出质量依赖大量中间历史（如深度研究报告）
- 成本：预填充成本高 + KV缓存失效（每个子Agent系统提示不同）
- Manus实现：共享VM沙箱作为媒介，Schema作为合约（submit_result + 约束解码）

### 三层分层行动空间（超越数据卸载工具本身）
工具过多导致"上下文混淆"；动态RAG工具有两个弊端：破坏KV缓存 + 误导模型

**第一层：函数调用（Function Calling）**
- 固定小集合（约10-20个）原子函数：读写文件、执行shell、搜索、浏览器操作
- 缓存友好，约束解码保证格式安全

**第二层：沙盒工具集（Sandbox Utilities）**
- VM中预装命令行工具：格式转换器、语音识别、MCP CLI等
- 通过execute_shell调用，无需改变函数调用空间
- 无限扩展；符合模型Linux直觉；处理大数据输出（grep/cat/less）

**第三层：软件包与API（Packages & APIs）**
- Agent编写Python脚本调用外部API
- 通过write_file + execute_shell执行
- 适合内存密集型计算，只将最终总结返回上下文

### 核心设计哲学：避免过度工程化
- Manus最大性能飞跃来自**简化和移除不必要的技巧**，而非增加复杂层
- 核心：**"Build less, understand more（构建得更少，理解得更多）"**

### Q&A 实战洞见

**评测**
- 最重要指标：用户会话结束后的1-5星评分
- 公开学术基准（GAIA等）可能与真实用户需求严重脱节
- 涉及"品味"的任务（网站生成、数据可视化）必须人类评估

**模型选择**
- Agent任务输入远长于输出，旗舰模型KV缓存基础设施更成熟，规模化时可能更具成本效益
- 不同模型路由：Claude擅长编码，Gemini擅长多模态
- 架构"未来兼容性"测试：从弱模型切换强模型时性能有显著提升

**Agent设计**
- **避免角色拟人化**：人类的设计师/程序员/经理分工是人类上下文限制的产物，不要照搬
- Manus多代理按**功能**划分：执行者(Executor)/规划者(Planner)/知识管理器(Knowledge Manager)
- todo.md升级为独立规划者Agent（"Agent as Tool"范式），减少文件反复读写的token浪费

**强化学习**
- 支持开放可扩展行动空间（如MCP）的通用Agent很难做RL，相当于在自己构建基础模型
- 当前阶段交给模型公司，应用层专注上下文工程

## 关键引文

> "随着 AI Agents 执行日益复杂的长期任务，其上下文窗口会因大量的工具调用而急剧膨胀，导致性能下降。" [重点/高亮]

> "上下文工程，即将恰到好处的信息填入上下文窗口，是构建高效、稳定和智能代理的决定性因素。" [重点/高亮]

> "Don not communicate by sharing memory; instead, share memory by communicating." [高亮]

> "优秀的上下文工程不仅是技术组合，更是一种'少即是多'的哲学，即通过简化架构、信任模型，而非过度工程化，才能实现代理性能的最大飞跃。" [重点/高亮]

> "避免角色拟人化：不要强行将人类的组织架构套用在Agent设计上。这种分工是人类上下文限制的产物。" [高亮]

## 关联

- [[Context_Engineering_LangChain_Manus_NotebookLM]] — 同一对话的 NotebookLM 提炼版
- [[Manus创始人手把手拆解上下文工程]] — Peak 官网亲写版
- [[浅谈上下文工程_Claude_Code_Manus_Kiro]] — 外部综合分析
- [[概念_上下文工程]]
- [[概念_Context_Rot_上下文衰退]]
- [[概念_分层行动空间]]
- 上下文隔离两种模式
- [[实体_Peak_Ji_季逸超]]
- [[实体_Manus]]
- [[实体_LangChain]]

---
> 📎 **物理文献**：[[raw/articles/也许当前最好的「上下文工程」讲解_LangChain联合Manus季逸超最新分享....md]]