---
type: concept
tags:
- AI-Agent/deep-research
summary: 来源：浙大综述《A Comprehensive Survey of Deep Research》（arxiv:2506.12594），分析 80+
  个 DR 系统后归纳的四种架构模式。
sources:
- wiki/sources/一篇95页最新80种Deep Research系统全面综述.md
updated: '2026-09-21'
aliases:
- Deep-Research
- Deep Research
- 深度研究实现架构
- 概念_Deep-Research实现架构四类
---

# 概念：Deep Research 实现架构四类

来源：浙大综述《A Comprehensive Survey of Deep Research》（arxiv:2506.12594），分析 80+ 个 DR 系统后归纳的四种架构模式。

## 四种架构

### 单体架构（Monolithic）

- **定义**：所有深度研究功能集成在统一框架中，以中心推理引擎为核心
- **特点**：集中式控制流、紧密耦合组件、共享内存系统
- **优点**：推理一致性高、实现简单
- **缺点**：扩展性和并行化能力有限
- **代表**：OpenAI/DeepResearch、grapeot/deep_research_agent

### 流水线架构（Pipeline）

- **定义**：研究流程分解为一系列专门处理阶段，每阶段负责特定数据转换
- **特点**：顺序组件组织、标准化接口、高可重用性
- **优点**：适合需要定制化工作流的场景
- **缺点**：复杂推理任务表现不佳
- **代表**：n8n、dzhng/deep-research

### 多智能体架构（Multi-Agent）

- **定义**：多个专门智能体协作，每个负责特定角色和任务
- **特点**：分布式功能分解、明确协调机制、自主决策逻辑
- **优点**：多样化专业能力和并行处理，处理复杂研究任务出色
- **缺点**：整体一致性和推理透明性问题
- **代表**：smolagents/open_deep_research、TARS

### 混合架构（Hybrid）

- **定义**：结合上述多种架构优点，分层组织以适应不同研究需求
- **特点**：分层组织、领域特定优化、灵活集成机制
- **优点**：最大灵活性
- **缺点**：实现复杂性最高
- **代表**：Perplexity/DeepResearch、Camel-AI/OWL

## 选型建议

- 简单场景/快速原型：单体架构
- 定制化工作流：流水线架构
- 复杂并行研究任务：多智能体架构
- 生产级复杂系统：混合架构

## 关联

- [[概念_Deep_Research_Agent_定义与分类]]
- [[概念_Orchestrator_Worker_编排工模式]]

## 来源

- [[一篇95页最新80种Deep Research系统全面综述]]