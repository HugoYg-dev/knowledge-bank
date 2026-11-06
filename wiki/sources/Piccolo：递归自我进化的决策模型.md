---
type: "source"
tags: ["RSI", "AI-Agent/tool-calling"]
summary: "Piccolo 决策模型原理解析：基于 RSI 自进化框架与 Agentic Data Engineering，覆盖 Game、Harness 六类子场景与 Data 流水线的高性能长程连续决策模型"
sources: ["raw/articles/Piccolo：递归自我进化的决策模型.md"]
updated: "2026-11-06"
---

# Piccolo：递归自我进化的决策模型

## 来源信息

- **来源标题**：Piccolo：递归自我进化的决策模型
- **作者 / 团队**：AgentScope & Data-Juicer 团队 / 魔搭 ModelScope 社区
- **发布时间**：2026-11-05
- **原文链接**：https://mp.weixin.qq.com/s/g5RyquIct8gK1mX8_6n3OQ

## 核心要点

1. **专用决策模型定位与统一接口**：[[entities/实体_Piccolo|Piccolo]] 作为专用决策组件接入高频判断流程，迅速理解当前状态并比较候选项，输出程序可直接消费的确定性结果与概率分布。其训练与推理接口统一抽象为“状态、问题、候选项、目标分布”，用一套接口承载从离散硬标签选择到连续软标签评分的多样化判断需求。
2. **三大应用业务场景落地**：
   - **Game（游戏连续动作选择）**：支持毫秒级长程连续决策，在《绝区零》实时战斗中根据高帧率截图动态指导角色移动、攻击与闪避；同时支持 Mario（时机判断）、2048、推箱子与黑白棋等博弈与规划任务；
   - **Harness（智能体编排决策）**：嵌入 [[concepts/概念_Harness_Engineering_宿主编排工程|Harness Engineering]]，覆盖**工具选择、模型路由、上下文与记忆、权限与信任、完成验收、失败恢复**六类子场景；
   - **Data（数据处理流控）**：覆盖**数据过滤、处理方案、产物质量、信息充分性、证据与隐私审查、工作流控制**六类子场景，实现语义、规则与证据驱动的数据工程流闭环。
3. **四项基准评测领跑**：在 2026 年 11 月 2 日更新的 11 款决策模型评测中，Piccolo-27B 在 **JevBench Public**（92.21%）、**HarnessJevBench Hard**（84.41%）与 **DataJevBench**（82.60%）三项场景中准确率均位列全行业第一；文本 Decision Index Public 达到 68.59，多模态 Decision Index Public 达到 77.75。团队同步开源了 HarnessJevBench 与 DataJevBench 两个面向 Agent 与数据流的真实场景基准。
4. **基于 RSI 的自主研发演化闭环**：团队设计了一套基于 [[concepts/概念_RSI递归自我改进|RSI（递归自我改进）]] 的模型研发架构。研究 Agent 利用自研的 Agentic Data Engineering 与 DataJuicer-Sandbox 调度 10+ 轮、150+ 项探索实验（耗费 6,300 GPU hours，PPU-真武810E），按照“方案设计 $\to$ 构建与实验 $\to$ 结果反馈 $\to$ 诊断与更新”的反馈 LOOP 驱动数据与模型持续演化。
5. **精细化数据治理与能力画像**：从开源社区清洗整理 665 万条数据，基于 Data-Juicer 建立包含 13 个标注维度、551 个预定义取值的语义标签体系；通过逐题 KL 损失（预测分布与目标分布偏差）在语义切片上进行精准能力诊断，对高偏差切片定向合成条件，对低偏差样本去重降采样。
6. **协同优化与 Context Evolving**：采用双向注意力与候选监督机制，分阶段安排广泛覆盖与定向加强；结合分项表现执行互补模型合并；进一步引入 **Context Evolving** 搜索输入组织策略（问题前置、上下文重排与重复阅读），在相同模型权重下单靠输入与推理设置将全集文本 DI 从 65.05 提升至 66.19；最终 27B 最优模型累计训练 35 万条样本，在 9B（46.78 $\to$ 60.86）与 4B（39.94 $\to$ 58.29）上展现一致的 Scaling 收益。

## 关联实体与概念

- **关联实体**：[[entities/实体_Piccolo]]、[[entities/实体_Jev]]
- **关联概念**：[[concepts/概念_RSI递归自我改进]]、[[concepts/概念_Harness_Engineering_宿主编排工程]]、[[concepts/概念_Decision_Model_专用判断模型]]

> 📎 **物理文献**：[[raw/articles/Piccolo：递归自我进化的决策模型.md]]
