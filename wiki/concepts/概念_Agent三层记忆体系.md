---
type: concept
tags:
- AI-Agent/coding
summary: 来源：从代码生成到自主决策Coding驱动的自我编程Agent
sources:
- wiki/sources/AI智能体8种Memory策略与技术实现.md
- wiki/sources/LLM Agent记忆进化路径三阶段研究综述.md
- wiki/sources/A_guide_to_the_anatomy_of_effective_commerce_agents.md
updated: '2026-09-15'
---


# 概念：Agent 三层记忆体系

**来源**：从代码生成到自主决策_Coding驱动的自我编程Agent

基于 Atkinson-Shiffrin Memory Model（1968）将记忆分为感知/短期/长期三层，在 Agent 工程侧实现持久化、结构化、可检索的记忆能力。

## 感知记忆（Sensory Memory）

- **维度**：标签页级，最短期
- **内容**：通过悬浮球捕捉当前页面信息、URL 等环境感知数据
- **失效条件**：页面任意操作（打开抽屉/弹窗）即失效
- **典型场景**：答疑时 Agent "看到"用户当前页面，提前预输入上下文减少用户描述成本

## 短期记忆（Short-term Memory）

- **维度**：Session 级，基于 ES 存储
- **格式**：统一 Segment 格式，三类消息：
  - **段落记忆消息**：存储 Thought/Command/Evaluation 等推理段落（含 execId + parentExecId 支持执行链追溯）
  - **实体记忆消息**：工具调用结果、用户关键信息、环境状态快照
  - **基础消息**：uuid/sessionId/tags/timestamp/sortValue
- **流程**：对话 → 产生 Segment → 存储 → 下轮检索 → 提供上下文

## 长期记忆（Long-term Memory）

- **知识点（短知识）**：一句话配置化知识指引，如"重新部署是流水线概念，重启是诺曼底运维概念"；比知识库文档更轻量，直接作为思考 Prompt 指引
- **历史会话摘要**：长期上下文连续性
- **用户画像**：角色定位、技能标签、工作习惯
- **代码执行经验**：人工审核 + 大模型投票机制录入经验图谱（规划中），成功经验供后续任务借鉴

## 生产级长期记忆工程实践（Anthropic 商业智能体方案）

Anthropic 在《A guide to the anatomy of effective commerce agents》中进一步明确了跨会话长期记忆在企业级高并发与长程交互系统中的工业化实现准则：

1. **结构化存储（Typed Records in Database）**：
   - 弃用容易膨胀且难以维护一致性的扁平 Markdown 文件，将事实抽象为强类型记录（Key、Value、Category、SessionId）保存在既有关系数据库中，支持确定性业务逻辑联动与用户隐私删除（GDPR/CCPA）合规治理。
2. **异步后台写入（Asynchronous Fact Extraction）**：
   - 严禁让主智能体在交互轮次中调用保存工具（避免多占一轮交互时延并引发注意力争夺）；
   - 由独立后台线程在会话轮次结束后抽取对话，不仅避免前端延迟激增，还在评测中提升了 13% 的事实召回率；
   - 抽取器仅读取用户与智能体正文，完全隔离工具返回（Tool Results），防止将第三方商品描述或评论误作为用户特征录入。
3. **三层按需读取体系（Three-Tier Read Pattern）**：
   - **常驻上下文（Always in context）**：核心全局事实（如默认地址、严重过敏原、商户权限角色）每轮固定注入；
   - **按轮次预取（Pre-fetched per turn）**：依据本轮请求特征动态匹配预取（如搜鞋时预取鞋码与品牌偏好）；
   - **工具按需查询（Behind a lookup tool）**：低频冷数据保存在数据库中，由智能体在必要时通过工具精准检索。

## 与上下文窗口的关系

纯上下文拼接的局限：长度有固定 token 限制；无法有效组织检索历史；无法动态更新；计算成本高。三层记忆体系解决这些问题。

## 关联

- [[概念_Agent感知记忆推理三能力]]
- [[concepts/概念_电商智能体架构]]
- [[concepts/概念_上下文工程]]
- [[entities/实体_Anthropic]]
- [[概念_Context_Rot_上下文衰退]]

---

> 📎 **来源摘要**：
> - [[wiki/sources/AI智能体8种Memory策略与技术实现.md]]
> - [[wiki/sources/LLM Agent记忆进化路径三阶段研究综述.md]]
> - [[wiki/sources/A_guide_to_the_anatomy_of_effective_commerce_agents.md]]
