---
type: entity
tags:
- AI-Agent/deep-research
summary: '- 发布方：阿里巴巴通义实验室（Tongyi Lab）'
sources:
- wiki/sources/Tongyi DeepResearch的技术报告探秘.md
- wiki/sources/通义 DeepResearch：开源 AI 智能体的新纪元.md
updated: '2026-06-29'
---

# 实体：通义 DeepResearch

## 基本信息

- **发布方**：阿里巴巴通义实验室（Tongyi Lab）
- **发布时间**：2025 年 9 月 16 日
- **类型**：全开源高性能 Web Agent
- **GitHub**：https://github.com/Alibaba-NLP/DeepResearch
- **模型**：Tongyi-DeepResearch-30B-A3B（HuggingFace / ModelScope）

## 模型规格

- 架构：30B MoE，每次激活 3B 参数（Qwen3MoeForCausalLM）
- 基座：Qwen3-30B-A3B
- 上下文长度：128K
- 部署：支持 PC/Mac 本地部署（M2 MacBook Pro 可运行），兼容 vLLM/ollama

## 性能指标（SOTA）

| 基准 | 得分 |
|------|------|
| Humanity's Last Exam (HLE) | 32.9 |
| BrowseComp-EN | 43.4 |
| BrowseComp-ZH | 46.7 |
| xBench-DeepSearch | 75.0 |

全面超越 OpenAI Deep Research 等闭源模型。

## 训练流程

三阶段端到端训练：
1. **Agentic CPT**：智能体增量预训练，AgentFounder 数据合成方案
2. **Agentic SFT**：有监督微调冷启动，[[概念_WebFrontier数据合成]] 方法
3. **Agentic RL**：基于 GRPO/GSPO 的 on-policy 强化学习

## 部署模式

- **ReAct 模式**：无需提示工程，128K 上下文，通用基准
- **深度模式（IterResearch）**：[[概念_IterResearch范式]]，处理极端复杂多步研究任务

## 配套工具生态

- 四个核心工具：通用搜索、学术搜索、网页浏览、代码执行
- 沙盒：字节跳动 Sandbox_fusion（评测代码执行环境）
- 训练框架：rLLM（异步 RL 训练推理框架）
- Agent 框架：兼容 Qwen-Agent

## 已落地应用

- **高德地图**：复杂查询助手「小高老师」，V16 暑期大版本功能
- **通义法睿**：法律 Deep Research，司法多步查询与复杂推理

## 系列工作

WebWalker → WebDancer → WebSailor → WebShaper → WebWatcher → WebResearch（通义 DeepResearch）

## 关联

- [[概念_IterResearch范式]]
- [[概念_WebFrontier数据合成]]
- [[概念_Deep_Research_Agent_定义与分类]]

## 来源

- [[通义 DeepResearch：开源 AI 智能体的新纪元]]
- [[Tongyi DeepResearch的技术报告探秘]]