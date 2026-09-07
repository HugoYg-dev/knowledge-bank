---
type: concept
tags:
- AI-Agent/coding
summary: Agent 完整轨迹评估（Full Trajectory Evaluation） 是一种面向复杂大模型智能体的评估范式。对智能体从输入到输出的整个决策路径（包含
  Skill 加载、参考读取、工具选择、参数合规与环境清理）进行系统化评估。
sources:
- wiki/sources/Dropbox基于DSPy优化Dash Chat评估与提示词.md
- wiki/sources/如何系统评价一个_Agent_Skill.md
updated: '2026-09-07'
---
# 概念：Agent 完整轨迹评估

## 定义

**Agent 完整轨迹评估（Full Trajectory Evaluation）** 是一种面向复杂大模型智能体的评估范式。由于智能体完成一个任务通常涉及多步规划、工具调用、信息检索与多轮会话，不能像传统搜索评测那样仅依据**最终输出文本（Final Response）**打分，而必须**对智能体从输入到输出的整个决策路径与中间状态进行系统化评估**。

## 核心评估维度

1. **意图遵循（Intent Understanding）**：智能体是否准确识别了用户的根本目标与隐藏约束。
2. **上下文选择与 Skill 加载**：在海量记忆、检索结果或 Skill 库中，智能体是否挑选并加载了正确的技能包与参考文件。
3. **工具调用与参数合规**：调用搜索、读取、代码执行等工具的时机是否合理，工具参数与依赖顺序是否正确，是否有重复重试。
4. **归纳与真实性（Synthesis & Grounding）**：最终生成的内容是否严格基于收集到的证据，无额外捏造或幻觉。
5. **多轮对齐与环境清理**：在遇到歧义或错误反馈时能否自我修正，任务结束后是否正确清理临时文件并维持环境安全。

## 评估驱动工程闭环

- **程序化确定性检查（Deterministic Checks）**：优先使用代码检查（文件存在、JSON 合规、命令执行成功、单元测试通过）替代高成本且易波动的 LLM Judge。
- **细粒度人工监督与标注**：对抽样轨迹打分并标注**失败编码（Failure Codes）**与**推理理由（Reasoning Notes）**。
- **校准 LLM-as-a-Judge**：利用人工标注数据与 [[实体_DSPy]] 等工具，优化裁判模型的提示词，使得自动化评分与专家认知高度吻合。
- **反事实回放（Counterfactual Replay）**：在离线代表性数据集上对比测试 `With Skill` 与 `Without Skill`（或候选模版与 Baseline）的轨迹轨迹，定量评估边际增量。

## 长期规划能力 Benchmark 与客观综合评测

在生产级与高并发复杂场景下，轨迹评估进一步延伸至长期规划韧性、压力承受度与客观确定性度量：
1. **长期规划三维 Benchmark**：
   - **迷宫探索（Maze Exploration）**：考察有障碍与死路状态下的规划最短路径与回溯（Backtracking）收敛效率；
   - **项目分解（Project Decomposition）**：评测复杂宏观工程分解为 DAG 依赖子任务的完备性与合理度；
   - **动态调整（Dynamic Re-planning）**：考察在外界接口宕机、Schema 突变时，重规划的响应延迟与任务挽回率。
2. **逐步加压压力测试（Step-up Load Testing）**：
   - 线性加压观测系统的 QPS 拐点、P99 延迟突破 SLA（如 2 秒）阈值及错误率激增点，识别瓶颈并防范脉冲流量下的级联雪崩。
3. **消除主观偏差的综合验证体系**：
   - 建立由 **客观确定性验证（70%）**（工具返回有效性、JSON Schema、数值与字段断言）+ **用户显式反馈（20%）** + **专家人工抽检（10%）** 构成的加权完成率，解决单纯依靠用户点击主观“已解决”带来的严重评估偏差。

## 来源与参考

- [[sources/Dropbox基于DSPy优化Dash Chat评估与提示词]]
- [[sources/如何系统评价一个_Agent_Skill]]
- [[concepts/概念_LLM应用评估体系]]
