---
type: source
tags:
- AI-Agent/deep-research
summary: 浙大研究：4维分类法分析80+个Deep Research系统，提出单体/流水线/多智能体/混合四种实现架构
sources:
- raw/articles/一篇95页最新80种Deep Research系统全面综述.md
updated: '2026-07-01'
---
# 一篇95页最新80种Deep Research系统全面综述

## 来源信息

- 作者：浙大 PaperAgent
- 原文：https://mp.weixin.qq.com/s/U5iEFpEAjqWwhCPrfvnZQQ
- 综述论文：https://arxiv.org/pdf/2506.12594（A Comprehensive Survey of Deep Research: Systems, Methodologies, and Applications）
- GitHub：https://github.com/scienceaix/deepresearch
- Cubox 高亮：无（stub，仅有摘要性文字）

## 核心要点

### 研究范围

分析自 2023 年以来出现的 80+ 个商业和非商业 Deep Research 系统实现，包括 OpenAI、Gemini、Perplexity、以及众多开源替代方案。

### 4 维度分层分类法

**维度一：基础模型与推理引擎**
- 上下文理解和记忆机制：现代实现采用情景缓冲区、层次化压缩和基于注意力的检索机制，Grok 3 和 Gemini 2.5 Pro 拥有百万级上下文窗口
- 推理能力增强：链式推理、树状推理、基于图的推理架构；OpenAI o3 通过自我批评、不确定性估计和递归推理改进增强复杂研究任务处理能力

**维度二：工具利用与环境交互**
- 内容处理：OpenAI o3 能从非结构化内容提取语义结构、识别关键信息、跨模态整合见解
- 专用工具集成：通过工具集成框架掌握超过 16,000 个真实世界 API；AssistGPT 展示了如何通过多模态交互框架规划/执行/检查/学习跨多样环境任务

**维度三：任务规划与执行控制**
- 研究任务规划：OpenAI Agents SDK 提供目标分解/执行跟踪/自适应细化框架
- 多智能体协作：明确的协调机制和信息共享协议，smolagents/open_deep_research 通过模块化智能体架构实现有效多智能体协作

**维度四：知识综合与输出生成**
- 报告生成：mshumer/OpenDeepResearcher 通过结构化输出框架和证据整合机制生成高质量研究报告
- 交互式呈现：HKUDS/Auto-Deep-Research 通过动态界面实现交互式结果探索

### 四种实现架构

**单体架构**
- 所有深度研究功能集成在统一框架中，以中心推理引擎为核心
- 特点：集中式控制流、紧密耦合组件、共享内存系统
- 优点：推理一致性、实现简单
- 缺点：扩展性和并行化能力有限
- 代表：OpenAI/DeepResearch、grapeot/deep_research_agent

**流水线架构**
- 研究流程分解为一系列专门处理阶段，每阶段负责特定数据转换
- 特点：顺序组件组织、标准化接口、可重用性
- 适合：需要定制化工作流的场景
- 缺点：复杂推理任务表现不佳
- 代表：n8n、dzhng/deep-research

**多智能体架构**
- 多个专门智能体协作，每个负责特定角色和任务
- 特点：分布式功能分解、明确协调机制、自主决策逻辑
- 优点：多样化专业能力和并行处理
- 缺点：整体一致性和推理透明性问题
- 代表：smolagents/open_deep_research、TARS

**混合架构**
- 结合上述多种架构优点，适应不同研究需求
- 特点：分层组织、领域特定优化、灵活集成机制
- 优点：最大灵活性
- 缺点：实现复杂性增加
- 代表：Perplexity/DeepResearch、Camel-AI/OWL

## 关联

- [[概念_Deep_Research_四类实现架构]]
- [[概念_Deep_Research_Agent_定义与分类]]

---
> 📎 **物理文献**：[[raw/articles/一篇95页最新80种Deep Research系统全面综述.md]]