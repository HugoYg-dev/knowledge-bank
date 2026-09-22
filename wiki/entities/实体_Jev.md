---
type: "entity"
tags: ["LLM/inference", "AI-Agent/tool-calling"]
summary: "TypeSafe 推出的无生成文本概率分布输出接口，将分类判断从通用大模型生成中解耦，主打百毫秒级确定性选择与 Agent 状态路由。"
sources: 
  - "wiki/sources/更好的替代品早已存在，Jev 留给研究的只剩时机.md"
  - "wiki/sources/Laya开源_421M参数33毫秒System1决策.md"
updated: "2026-09-22"
---

# 实体：Jev

## 概述

**Jev** 是由 TypeSafe 推出的专用模型接口，官方定义为“面向前沿智能的函数调用接口”（System 1 Model）。它不同于通用的对话型大语言模型，其核心职责收敛于在给定输入和一组预定义候选项中输出选项的概率分布与置信度，完全不生成自然语言文本。该接口旨在解决智能体（AI Agent）在高频状态机跳转、工具调用安全拦截及多分支路由中的高延迟与高推理成本问题。

## 核心技术特性与接口形态

1. **概率分布而非单一硬标签**：
   - Jev 输出包含所有选项的归一化概率分布（和为 1.0），并在后续附带整体把握置信度（Margin / Confidence）。
   - 下游系统可消费该分布构建多层路由逻辑（例如第一层置信度不足转人工；第二层按胜者派发任务；第三层若第二名概率超过阈值则触发抄送或复核）。
2. **前向提取与无自回归生成**：
   - 底层机制通过单次前向传播直接提取选项对应 Token 的 Logits 并做归一化，消除了自回归生成（Autoregressive Generation）带来的逐 Token 延迟与思考冗余。
3. **生态与分发整合**：
   - 团队创始人具有 InstructGPT 核心论文共同作者背景；
   - 发布后迅速接入 Vercel AI Gateway、Cloudflare 与 OpenRouter 等云平台，主打百毫秒级的确定性云端决策能力。

## 工程评测与开源替代方案对比

根据社区与独立机构（如 sgnt.ai、truestandard.ai）的对照基准评测：

- **质量表现**：在重构官方评测材料的 102 个判断任务中，SemIf（基于冻结的 Qwen3.5-4B 基座，零微调）与标准答案一致率为 84.5%，Jev 为 88.3%，差距仅 3.8 个百分点；在依赖记忆的边缘任务（MMLU-Pro，Jev 83% vs 27B 开源 60%）中，一旦缺少必要背景，Jev 亦会在 0.90 高置信度下给出典型的错误事实；
- **推理延迟**：Browser Use 实际航旅查询实测中 Jev 云端 API 中位延迟为 178 毫秒；而本地开源方案（如 jev-fire 在浏览器 WebGPU 运行 0.8B Qwen）在马里奥游戏中单步仅需 71.26 毫秒且省去网络往返；
- **输出一致性**：Jev 在云端生产 API 上重复测试 15 次，部分问题概率在 0.43 到 0.53 之间摆动横穿 0.5 决策临界点（Bud-ro 迷宫测试中求解率甚至直接归零）；而本地直接提取 Logits 在数学上具备完全确定性；
- **校准曲线**：truestandard.ai 跨 6 领域 108 命题测试显示 Jev 的 ECE 为 0.066，与通用模型 Gemini 3.1 Flash Lite (0.061)、Claude Haiku 4.5 (0.067) 水平相当，通过合理提示词或两三百条样本的 Platt/温度缩放即可在本地拉平；仅在第 4 级对抗小样本（108 条）中以 91.7%（vs 83.3% / 80.6%）领先，但该测试曾反转三次，属于未独立复现的孤证。
- **与完全开源方案 Laya 的正面对比**：Convai Innovations 开源的 421M 端到端决策模型 [[entities/实体_Laya|Laya]]（基于 ModernBERT-large 与 RLCD 训练）实测单问题 P50 延迟仅 38.4 ms，较 Jev 最佳 150 ms 快 4 倍、较平均 400 ms 快 10.4 倍；在 23,024 任务内问题宏平均准确率达 83.8%（Jev 为 67.8%），且提供 100% 本地自托管与 Apache 2.0 协议支持。

## 关联页面

- **归属机构/产品**：TypeSafe
- **开源对标实体**：[[entities/实体_Laya|实体_Laya]]（421M 开源端到端非自回归决策模型）
- **核心概念**：[[concepts/概念_Decision_Model_专用判断模型|Decision Model (专用判断模型)]]、[[concepts/概念_RLCD校准决策强化学习|RLCD校准决策强化学习]]、[[concepts/概念_分类模型校准|分类模型校准]]、[[concepts/概念_LLM模型路由|LLM 模型路由]]
- **应用场景**：[[entities/实体_Claude_Code|Claude Code]] 与 [[entities/实体_Codex|Codex]] 工具执行前置拦截、[[entities/实体_LangChain|LangChain]] 路由中间件

## 来源与参考

- [[sources/更好的替代品早已存在，Jev 留给研究的只剩时机|更好的替代品早已存在，Jev 留给研究的只剩时机]]
