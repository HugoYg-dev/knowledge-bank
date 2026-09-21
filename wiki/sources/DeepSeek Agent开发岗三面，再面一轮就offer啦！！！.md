---
type: source
tags:
- AI-Agent/coding
- AI-Agent/memory
- 面试
summary: 一篇 Agent 开发岗面试复盘，覆盖私人助理架构、幻觉与代码安全、记忆分层、轨迹评测、Badcase 回流及 RAG 检索优化。
sources:
- raw/articles/DeepSeek Agent开发岗三面，再面一轮就offer啦！！！.md
updated: '2026-08-03'
---

# DeepSeek Agent 开发岗面试复盘

## 来源信息

- 标题：DeepSeek Agent开发岗三面，再面一轮就offer啦！！！
- 作者：AIGC小白入门记
- 发布时间：2026-08-02
- 原文：https://mp.weixin.qq.com/s/5jWTFwlMAr12q2y49KcCNw

## 核心要点

- 文中的 AI 私人助理采用用户交互、Agent 调度、工具执行和记忆四层架构，通过日历、邮件、待办与知识库工具，把自然语言请求转为可执行的个人事务管理流程。
- 高准确性场景的幻觉控制组合包括结构化输出约束、检索增强、引用溯源和生成后验证；文章强调时间、地点和数字必须来自工具结果。文中自述评测集上的幻觉率约为 3%-5%，引用错误率约为 2%，但未给出评测集规模与测量细节。
- 代码执行必须隔离于宿主环境：限制 CPU、内存、磁盘、网络和系统调用，并设置超时；文章明确反对直接使用 Python `exec`、`eval` 执行模型生成代码。
- Agent 的可恢复性与可观测性由任务调度、状态回退、Checkpoint 和 Trace 回放共同构成；记忆则分为内存中的短期会话、Redis 中的近期摘要，以及向量库与 MySQL 中的长期事实，并通过滚动窗口、摘要压缩和结构化抽取维护。
- Badcase 被区分为审核拒绝、用户不采纳和高质量样本，并通过“收集、人工修正、构造样本、SFT、离线评测、灰度上线、线上验证”形成回流闭环；评测覆盖检索、生成、端到端链路和线上行为四个维度。
- 文章把 Prompt Engineering、Context Engineering、Harness Engineering 与 Loop Engineering 视为逐层扩展的工程关注点，并区分面向流程编排的 Graph Engineering 与面向单 Agent 迭代控制的 Loop Engineering。
- RAG 部分建议以 Query Rewrite、BM25 与向量多路召回、RRF 融合及 Rerank 组成检索链路；效率侧使用 TopN 精排、上下文预算、模型路由、缓存、异步队列和批量推理进行权衡。

## 关联概念

- [[concepts/概念_上下文工程]]
- [[concepts/概念_Harness_Engineering_宿主编排工程]]
- [[concepts/概念_Agent三层记忆体系]]
- [[concepts/概念_Agent完整轨迹评估]]
- [[concepts/概念_多智能体协调]]
- [[concepts/概念_混合检索]]

> 📎 **物理文献**：[[raw/articles/DeepSeek Agent开发岗三面，再面一轮就offer啦！！！.md]]
