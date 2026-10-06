---
type: "source"
tags:
  - "LLM/inference"
  - "AI-Agent/tool-calling"
summary: "解析 100% 本地复现 Jev 确定性决策推理路径：利用 SGLang /v1/score 直接提取首 Token Logits 进行受限 Softmax 归一化，对比结构化输出与自回归生成"
sources:
  - "raw/articles/2026-09-22_Build-your-own-Jev-(100%-local)_1a0ca86e233289fe.md"
updated: "2026-10-06"
---

# Source: Build your own Jev (100% local)

## 来源信息

- **标题**：Build your own Jev (100% local)
- **作者**：Avi Chawla (Daily Dose of DS)
- **原始链接**：https://www.dailydoseofds.com/ai-agents-with-langgraph-course-part-1-with-implementation/
- **发布日期**：2026-09-22
- **邮件元数据**：邮件主题 `Build your own Jev (100% local)` | 发送人 `Daily Dose of DS <avi@dailydoseofds.com>` | 邮件 ID `1a0ca86e233289fe` | 文章 ID `1a0ca86e233289fe:2`
- **原始归档**：[[raw/articles/2026-09-22_Build-your-own-Jev-(100%-local)_1a0ca86e233289fe.md]]

## 核心要点

1. **固定候选项打分（Fixed-answer Scoring）与决策解耦**：许多大模型调用并不需要生成新的自然语言文本，应用侧已知全部合规选项（如工单路由分类），只需模型做出单一裁决。将此类请求建模为概率打分而非文本生成，可在单次前向请求中直接获得各候选项的概率分布，避免了自回归生成中的语法包装与解析开销。
2. **区别于结构化输出（Structured Output）的底层机制**：结构化输出（如 JSON Schema 约束）虽然限制了最终返回的数据格式，但在推理引擎底层仍然以逐 Token 方式自回归生成左大括号、字段名、取值和右大括号；而固定候选项打分完全不生成任何 Token，直接在第一步前向计算中提取候选 Token 的 Logits 并做归一化，大幅消除计算冗余与解码延迟。
3. **单 Token 标签对齐与 Chat Template 陷阱防范**：为了避免词汇跨多 Token 切分（如短语 `technical support` 跨多个位置）导致序列打分的不公，系统将语义候选项映射为单字符标签（如 `A`、`B`、`C`）。同时必须通过 `/tokenize` 严格校验标签在特定分词器与 Chat Template（注意前置空格与控制符）下确属单 Token，防止分词错位。
4. **受限 Softmax（Restricted Softmax）与概率消费**：推理服务端从完整词表中仅提取候选标签对应的 Logits，忽略其余词表项并应用 Softmax 归一化。应用层代码可消费完整的分布形状（Shape）与胜出裕度（Margin），例如要求最高项概率超过 0.80 且领先第二名 0.20 以上方可自动放行，贴近阈值则流转人工复核。
5. **非穷尽选项的逃逸通道（Escape Route）**：当预定义候选项无法完全覆盖所有现实场景时（例如安全警报误入工单路由），受限 Softmax 仍会将 100% 概率强行分摊给错误选项。因此必须在候选项中显式设置 `OTHER` 或 `ESCALATE` 作为逃逸保底分支。
6. **基于 SGLang `/v1/score` 的本地极简工程落地**：通过 SGLang 加载开源模型（如 Qwen2.5-0.5B/Qwen3-4B），利用原生 `/v1/score` 接口传入 prompt、空 `items` 与 `label_token_ids`，配合 `apply_softmax=true` 实现零额外模型修改的端到端单次前向打分，并映射回语义选项。
7. **延迟基准测试与连续批处理并发**：在 100 例真实分类测试集（工单路由、候选人筛选、报销审核）上，通过并发屏障（Barrier）公平对比 Jev 式打分泳道与常规自回归生成泳道（max_tokens=32）。在同机共享 GPU 与连续批处理调度下，打分泳道速度显著领先，且直接避免了输出格式解析失败的脆弱性。

## 三种 LLM 输出范式横向对比

| 评估维度 | 常规自回归生成 (Generation) | 结构化输出 (Structured Output) | 固定候选项打分 (Jev-style Scoring) |
| :--- | :--- | :--- | :--- |
| **底层推理行为** | 逐 Token 自回归解码完整句子 | 逐 Token 自回归解码 JSON 字段与括号 | **单次前向传播**提取指定 Token Logits，**零生成** |
| **首字/首包时间** | 受限解码速度，需等完整文本生成 | 受限解码速度，需等 JSON 闭合 | **仅单次 Prefill 前向耗时**，百毫秒内完成 |
| **输出信息形式** | 自由文本字符串（需正则解析） | 强类型单一选项（如 `{"team": "billing"}`） | **全候选项归一化概率分布 + 置信度裕度** |
| **下游决策控制** | 难以量化模型确信程度与边界摇摆 | 仅获得单一 Argmax 标签，无法获知次选概率 | **代码级设定置信度阈值**，支持自动放行与人工复核分流 |
| **适用场景** | 答案内容在推理前未知、开放生成 | 字段结构已知但取值开放不可穷举 | **合规选项在推理前完全已知且有限**（状态路由/拦截） |

## 关键引文

> “Many LLM calls do not need newly written text. The application already knows the possible answers, and it only needs the model to choose one.” `[核心洞见]`
>
> “Structured output generates a valid object. Fixed-answer scoring returns a distribution over answers the application already knows.” `[范式区别]`
>
> “Generate when the output content is unknown before inference. Score when the output set is known, and selection is sufficient.” `[选型黄金法则]`

## 关联

- [[entities/实体_Jev]] — TypeSafe 推出的商业化无生成概率分布判断接口
- [[concepts/概念_Decision_Model_专用判断模型]] — 将分类选择从自回归文本生成中解耦的核心概念
- [[entities/实体_Laya]] — 开源端到端 421M 非自回归 System 1 决策模型
- [[concepts/概念_分类模型校准]] — 原始 Logits 与概率分布的校准技术
- [[concepts/概念_连续批处理]] — SGLang 与推理引擎底层的并发调度机制

---
> 📎 **物理文献**：[[raw/articles/2026-09-22_Build-your-own-Jev-(100%-local)_1a0ca86e233289fe.md]]
