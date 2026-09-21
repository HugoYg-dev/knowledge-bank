---
type: concept
tags:
- AI-Agent/deep-research
summary: WebFrontier 是通义 DeepResearch 提出的端到端合成数据生成方案，用于为 Agent SFT 冷启动阶段构建高质量 Web
  问答数据。核心思路是"种子—扩展—评估"经典套路与 Deep Research 工具集深度绑定。
sources:
- wiki/sources/Tongyi DeepResearch的技术报告探秘.md
- wiki/sources/通义 DeepResearch：开源 AI 智能体的新纪元.md
updated: '2026-06-29'
---


# 概念：WebFrontier 数据合成

## 定义

WebFrontier 是通义 DeepResearch 提出的端到端合成数据生成方案，用于为 Agent SFT 冷启动阶段构建高质量 Web 问答数据。核心思路是"种子—扩展—评估"经典套路与 Deep Research 工具集深度绑定。

## 三步流程

### 第一步：种子数据生成
- 以网页数据、文档、电子书为基础
- 清洗处理成 chunk 后，用模型生成种子 QA 对

### 第二步：迭代式复杂度升级
- 一个装备完整工具集的 Agent（通用搜索/学术搜索/网页浏览/代码执行）迭代改进问题和答案
- 目的：增加数据与 DeepResearch 场景契合度，尽可能用上工具
- 此阶段不直接评估数据质量，侧重工具使用覆盖

### 第三步：质量控制（掐头去尾）
- 去除过简单样本：无工具 Agent 可解 → 过滤
- 保留样本：强力工具 Agent 可解 → 保留
- 未解样本：经人工审核，回收部分

## 数据构建深层方法（官方技术报告补充）

**知识图谱路线**：
- 知识图谱随机游走 + 表格数据融合整合真实网站数据
- 采样子图/子表生成初始 QA，策略性混淆信息增加难度
- "原子操作"正式建模 QA 难度（如合并具有相似属性的实体），系统性增加复杂性
- 集合论信息搜索问题形式化建模，最小化推理捷径和结构冗余

**学术数据路线**：
- 多学科知识库生成"种子"QA 对
- 种子进入自我引导"迭代复杂性升级"循环：问题构建 Agent 配备网络搜索/学术检索/Python 执行
- 每次迭代扩展知识边界、深化概念抽象、甚至构建计算任务

## 历史演进

WebWalker → WebSailor/WebSailor-V2 → WebShaper → WebFrontier

每一代都在数据质量、可扩展性和任务难度建模上持续改进。

## 优势与局限

**优势**：
- 保证训练数据与模型推理时见到的工具一致性
- 全自动流程，无需人工干预，可构建超越人类质量的数据集

**局限**：
- 深度绑定固定工具集（四个工具），对动态工具集合（如 MCP 生态）有效性存疑
- 场景深度绑定带来潜在的跨场景效果下降风险
- 训练数据使用合成数据比人工标注数据（如 BrowseComp）训练效果更好（模型方更一致分布）

## 关联

- [[概念_IterResearch范式]]
- [[概念_Deep_Research_Agent_定义与分类]]
- [[实体_通义DeepResearch]]

## 来源

- [[通义 DeepResearch：开源 AI 智能体的新纪元]]
- [[Tongyi DeepResearch的技术报告探秘]]