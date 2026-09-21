---
type: source
tags:
- AI-Agent/deep-research
summary: 魔搭社区深度解读通义 DeepResearch：三阶段训练流程、IterResearch 范式、WebFrontier 数据合成与六大研发问题
sources:
- raw/articles/Tongyi DeepResearch的技术报告探秘.md
updated: '2026-07-01'
---
# Tongyi DeepResearch的技术报告探秘

## 来源信息

- 作者：罗智凌（浙江大学），魔搭 ModelScope 社区
- 原文：https://mp.weixin.qq.com/s?__biz=Mzk3NTc1NTU0Mw==&mid=2247501232
- 项目 GitHub：https://github.com/Alibaba-NLP/DeepResearch
- 开源模型：Tongyi-DeepResearch-30B-A3B（ModelScope）
- Cubox 高亮：1 处，已标注 [重点/高亮]

## 核心要点

### 项目定位

Tongyi DeepResearch（2025年9月16日发布）是开源高性能 Web Agent，在多项评测中取得 SOTA：
- Humanity's Last Exam (HLE)：32.9
- BrowseComp：45.3
- xbench-DeepSearch：75.0

超越 OpenAI Deep Research 等闭源模型。

模型为 30B MoE 架构，每次激活 3B 参数（Qwen3MoeForCausalLM），支持 PC/Mac 本地部署。

### 三大产品组件

1. **模型**：DeepResearch-30B-A3B
2. **推理代码**：兼容 Qwen3 系列部署方式（vLLM/ollama），ModelScope 提供开箱即用服务
3. **评测代码**：采用字节跳动 Sandbox_fusion 作为评测沙盒，包含 ReAct AgentUse 模式
4. **Agent 推理代码**：项目未直接开源（截止 2025-09-23），IterResearch 模式未随开源发布，兼容 Qwen-Agent 框架

### 三阶段训练流程

**阶段一：增量预训练（Agentic CPT）**

数据包含两大类：
1. 常见高质量 CPT 数据（爬虫数据、知识图谱等）
2. 后训练轨迹数据（合成轨迹）

轨迹合成方式：对原始轨迹按步骤展开，分别探索多个候选分支（步骤级 rollout），拆分为三类动作数据：单步规划、推理动作、多步决策动作。问题：构造样本采纳率不高，轨迹采样成本昂贵（项目作者："一条轨迹的价格远比想象中昂贵"）。

**阶段二：监督微调（SFT，冷启动）**

引入 **WebFrontier** 数据合成方法，三个要点：
1. **种子数据生成**：基于网页、文档、电子书生成种子 QA 对
2. **迭代式复杂度升级**：由装备四个工具（通用搜索/学术搜索/网页浏览/代码执行）的 Agent 迭代改进问题和答案
3. **质量控制**：去除过简单样本（无工具 Agent 可解），保留工具 Agent 可解的样本，未解样本经人工审核回收

潜在问题：深度绑定评测数据和固定工具集，动态工具集合（如 MCP 生态）下有效性存疑。

**阶段三：强化学习（RL）**

基础算法：报告提 GRPO，论文提 GSPO（不完全一致）。

关键设计：
- 将每条轨迹分解为多个轮次样本（传统：G 个样本；改进：G×T 个样本），提高数据利用率
- **组级别优势归一化**：所有轮次样本在同一标准下评估，防止模型只学"开头"或"结尾"
- 加入最小损失下采样，解决轨迹长度差异问题
- **双环境策略**：先在模拟环境快速迭代，再应用到真实环境

**IterResearch 范式**（关键创新）

相比 ReAct，IterResearch 有两个关键点：
1. **良好维护的核心报告**：保存关键分析思路
2. **动态维护的工作空间**：动态压缩工具调用结果，避免上下文被 10k+ 的网页内容占满

效果数据（推测）：在 HLE 中比 ReAct 高 7.9pt，在 BrowserComp 上高 14pt。

## 关键引文

> [重点/高亮] 首先，从21年开始，大家都认可数据制作上花的每一分钱（和时间）都是值得的，大量研究指出高质量的数据对模型训练的效果是至关重要的。……第三个是冷启动+强化学习的必要性，随着Deepseek的报告，和大量类似研究的披露，从业者使用一些精心设计的冷启动数据和一个良好设计的RL环境，用于最后一个训练阶段，这一点也接近了共识。此外在Websailor的工作中，作者提到在工具场景中，纯RL无法使工具调用次数有效提升，而这一提升可以靠冷启动SFT阶段完成。

### 六大研发问题讨论

- **RQ1**：Deep Research Agent 适合 AI 搜索和分析报告生成，但速度慢（单次查询数分钟）
- **RQ2**：专用 Agent 模型 vs 通用大模型仍处于欠共识状态；专用模型当前 SOTA 但通用模型支持者认为可覆盖
- **RQ3**：数据质量的必要性相对可观，轨迹多样性是关键难点
- **RQ4**：CPT 并非必选，蚂蚁集团 Atom-Searcher 跳过 CPT 也可行
- **RQ5**：最低成本方案是接入大模型 + 精心设计 Prompt（OpenManus/OWL 等框架）
- **RQ6**：数据合成+多阶段训练方式可参考；WebFrontier 对其他工具/Agent 的迁移性未被证明；封闭工具集有利于模型训练稳定性

## 关联

- [[概念_IterResearch范式]]
- [[概念_WebFrontier数据合成]]
- [[概念_Deep_Research_Agent_定义与分类]]
- [[实体_通义DeepResearch]]

---
> 📎 **物理文献**：[[raw/articles/Tongyi DeepResearch的技术报告探秘.md]]