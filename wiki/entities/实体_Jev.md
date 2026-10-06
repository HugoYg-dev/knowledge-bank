---
type: "entity"
tags: ["LLM/inference", "AI-Agent/tool-calling"]
summary: "TypeSafe 推出的无生成文本概率分布输出接口，将分类判断从通用大模型生成中解耦，主打百毫秒级确定性选择与 Agent 状态路由。"
sources: 
  - "wiki/sources/更好的替代品早已存在，Jev 留给研究的只剩时机.md"
  - "wiki/sources/Laya开源_421M参数33毫秒System1决策.md"
  - "wiki/sources/2026-09-22_Build-your-own-Jev-(100%-local)_1a0ca86e233289fe.md"
updated: "2026-10-06"
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
4. **100% 本地确定性打分复现（SGLang /v1/score 机制）**：
   - Daily Dose of DS 验证了在本地环境中 100% 复现 Jev 推理机制的可行性：利用 SGLang 原生 `/v1/score` 接口搭配开源基座（如 Qwen2.5/Qwen3），将候选选项映射为经 `/tokenize` 校验的单 Token 标签（A/B/C），直接读取首个 Next-token 向量对应 Logits 并应用受限 Softmax 归一化；
   - 彻底消除逐 Token 解码开销，与结构化输出（Structured Output，底层仍自回归生成 JSON 键值字符）形成本质计算层解耦；
   - 设立 `OTHER` 或 `ESCALATE` 逃逸通道，防范非穷尽选项下概率强行归一化的误判风险；
   - 在 100 例分类任务的连续批处理（Continuous Batching）基准实测中，打分泳道较自回归生成泳道展现出显著的吞吐与延迟优势。

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
- **核心概念**：[[concepts/概念_Decision_Model_专用判断模型|Decision Model (专用判断模型)]]、[[concepts/概念_RLCD校准决策强化学习|RLCD校准决策强化学习]]、[[concepts/概念_分类模型校准|分类模型校准]]、[[concepts/概念_LLM模型路由|LLM 模型路由]]、[[concepts/概念_连续批处理|概念_连续批处理]]
- **应用场景**：[[entities/实体_Claude_Code|Claude Code]] 与 [[entities/实体_Codex|Codex]] 工具执行前置拦截、[[entities/实体_LangChain|LangChain]] 路由中间件

## 来源与参考

- [[wiki/sources/更好的替代品早已存在，Jev 留给研究的只剩时机.md|更好的替代品早已存在，Jev 留给研究的只剩时机]]
- [[wiki/sources/Laya开源_421M参数33毫秒System1决策.md|Laya 开源：比Jev快4倍！421M 参数，33 毫秒完成 System 1 决策]]
- [[wiki/sources/2026-09-22_Build-your-own-Jev-(100%-local)_1a0ca86e233289fe.md|Build your own Jev (100% local)]]
