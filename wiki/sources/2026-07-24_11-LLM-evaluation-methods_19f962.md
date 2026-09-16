---
type: source
tags:
- LLM/reasoning
- Infra/platform
summary: 本文详细整理了 11 种必知的大模型（LLM）评估方法，深入探讨了不同评估指标的定义、使用局限以及在实际应用（如翻译、摘要、智能体、多轮对话等）中的最佳实践要点。
sources:
- raw/articles/2026-07-24_11-LLM-evaluation-methods_19f962.md
updated: '2026-08-04'
---

# 来源摘要：11 LLM Evaluation Methods

## 来源信息
- **标题**: 11 LLM Evaluation Methods
- **作者/发布者**: Daily Dose of DS (Avi)
- **发布日期**: 2026-07-24
- **原始链接**: [Daily Dose of DS - LLMOps Course Part 1](https://www.dailydoseofds.com/llmops-crash-course-part-1/)
- **关联概念**: [[概念_LLM应用评估体系]]

## 核心要点
- **评估局限与方法分化**：传统的 n-gram 重合度指标（如 BLEU）在面对表达相同语义但用词不同的“干净改写（Paraphrase）”时会失效，这是导致 LLM 评估方法分化为 11 种的主要原因。
- **基于字面与嵌入的评估（BLEU, ROUGE, BERTScore）**：
  - **BLEU** 适合翻译和受限生成，但对语义改写极度不友好。
  - **ROUGE** 以召回为主，是摘要和信息提取的默认选择，但易被冗长文字刷分，需结合精确度指标。
  - **BERTScore** 利用语义嵌入计算相似度，解决了语义改写的问题，但其绝对分值高且集中，适合做系统间横向对比。
- **基于大模型的评估（G-Eval, LLM-as-Judge, LLM Juries）**：
  - **G-Eval** 通过 CoT 步骤及 Token 概率权重打分，对主观指标更具稳定性。
  - **LLM-as-Judge** 通常采用成对比较（Pairwise）来比对两个模型配置，需随机化顺序消除位置偏见，并需严控文本长度偏见。
  - **LLM Juries（陪审团）** 利用多个不同模型家族消除单一模型的家族偏见（如倾向于给同家族模型打高分），性价比通常优于单一巨型模型。
- **人工评估（Human Eval）**：是校准大模型裁判（LLM-as-Judge）以及上线前的终极关卡。必须提前制定好细则，若标注者一致性低通常说明评判细则不够明确。
- **结构化与场景化评估（DAG, Trajectory, Multi-turn）**：
  - **DAG（有向无环图/决策树）** 适合做确定性的格式/硬性限制检查，成本低且结果完全一致。
  - **Trajectory Accuracy（轨迹准确率）** 专注于 Agent 中间思考和工具调用步骤的精确度，以防止模型通过错误路径“侥幸”得到正确答案。
  - **Multi-turn Eval（多轮评估）** 将整个对话视为评测单元，考察随时间推移下的角色依从性和长文本约束保持，建议基于生产日志而非合成的二轮对话进行评估。
- **安全红线一票否决**：安全评估（Safety Eval）如隐私、偏见、有害性检测等应作为独立闸口（Gate），直接实行“一票否决制”，严禁将其折算到综合平均分中以防严重漏洞被均值掩盖。

## 关键引文
> A model can answer a question correctly and still score close to zero on BLEU. That happens whenever the model says the right thing in different words than the reference.

> Criteria written as a concrete checklist score far more consistently than criteria written as adjectives.

> Several small models in a jury often beat one large judge at a lower cost.

> A single PII leak matters regardless of how good the mean quality score looks, which is how folding safety into an aggregate ends up shipping violations.

---
> 📎 **物理文献**：[[raw/articles/2026-07-24_11-LLM-evaluation-methods_19f962.md]]
