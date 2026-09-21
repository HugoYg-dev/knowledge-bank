---
type: source
tags:
- LLM/hallucination
summary: 翁荔 Blog：LLM 外在幻觉定义、产生原因（预训练/微调新知识）、检测方法（FActScore/SAFE/SelfCheckGPT）、抵抗方法（RAG/CoVe/FLAME）
sources:
- raw/articles/OpenAI 翁荔提出大模型「外在幻觉」：万字 blog 详解抵抗办法、产幻原因....md
updated: '2026-07-01'
---
## 来源信息

- **标题**：OpenAI 翁荔提出大模型「外在幻觉」：万字 blog 详解抵抗办法、产幻原因和检测方式
- **作者**：翁荔（Lilian Weng），OpenAI；量子位编译
- **URL**：https://lilianweng.github.io/posts/2024-07-07-hallucination/（原文），https://www.ithome.com/0/781/633.htm（IT之家）

## 核心要点

### 幻觉定义与分类

- **上下文内幻觉**：输出应与源内容一致，出现时与源内容不一致
- **外在幻觉（extrinsic hallucination）**：输出应基于预训练数据（世界知识），但内容虚构且无法通过外部世界知识验证；当模型不了解某个事实时应明确表示不知道

### 产生幻觉的原因

- **预训练数据问题**：从公共互联网爬取数据可能包含过时、缺失或错误信息；模型通过最大化对数似然可能错误记忆这些信息
- **微调新知识**：SFT 引入新知识的风险——LLM 学习带有新知识的微调示例比学习与已有知识一致的示例学得更慢；一旦学习了大多数 Unknown 示例后，模型幻觉倾向增加（Gekhman et al.）

### 幻觉检测方法

- **FactualityPrompt**（Lee et al. 2022）：NE 错误率 + 蕴含比率，较大模型表现更好
- **FActScore**（Min et al. 2023）：将长文分解为原子事实，逐个对照维基百科验证；检索增强比无上下文 LLM 一致性更好
- **SAFE**（Wei et al. 2024）：LLM 作为 Agent 多步骤迭代 Google 搜索验证事实；成本比人类低 20 倍，与人类一致率 72%，意见不一致时胜过人类 76%；指标 F1@K 同时衡量精确率（事实性）和召回率（长篇覆盖）
- **SelfCheckGPT**（Manakul et al. 2023）：黑盒访问，多次采样检查一致性，无需外部知识库；使用 BERTScore/NLI/提示等度量一致性
- **TruthfulQA**：对抗性构建，最佳 LLM 准确率 58%，人类 94%；较大模型反而因常见误解更不真实
- **校准置信度**：RLHF 微调使模型校准变差；较高采样温度带来更好校准

### 抵抗幻觉的方法

- **RARR**（Gao et al. 2022）：研究→修订两阶段，搜索+编辑归因框架，无需训练
- **FAVA**（Mishra et al. 2024）：检索器+编辑器，编辑器需微调，通过合成插入错误的训练数据学习纠正
- **Self-RAG**（Asai et al. 2024）：四种反思 Token（Retrieve/IsRel/IsSup/IsUse），端到端训练，蒸馏自 GPT-4 监督数据
- **Chain-of-Verification（CoVe）**（Dhuliawala et al. 2023）：基线响应→规划验证→独立执行验证→最终输出；分解验证效果优于联合验证；LLM 自由生成验证问题优于启发式
- **WebGPT**：Web 搜索 + 微调 GPT，引用网页帮助判断事实；RL 效果有限，Best-of-n 效果较好
- **FLAME**（Lin et al. 2024）：事实性感知 SFT + DPO，用 FActScore 作为事实性奖励；避免 RAG 数据中未知知识蒸馏问题

## 关键引文（Cubox 高亮）

> LLM 学习带有新知识的微调示例，要比学习与模型预先存在的知识一致的示例，学得更慢；一旦学习了这些带有新知识的示例，模型产生幻觉的倾向就会增加。 [重点/高亮]

> 回顾一组提升 LLM 响应真实性的方法，这些方法包括从外部知识库检索、特殊的采样方法、对齐微调。在这里暂不讨论一些通过神经元编辑来减少幻觉的可解释性方法。 [重点/高亮]

## 关联

- [[概念_LLM外在幻觉与上下文内幻觉]] — 外在幻觉定义与两种类型
- [[概念_幻觉检测方法]] — FActScore/SAFE/SelfCheckGPT 检测框架
- 幻觉产生原因 — 预训练数据/微调新知识两大根因
- [[概念_抗幻觉方法]] — RAG/CoVe/FLAME/Self-RAG 抵抗方案
- [[实体_翁荔_Lilian_Weng]] — OpenAI 科学家，Agent 公式 / 幻觉 Blog 作者
- [[概念_Self_RAG_自省式检索增强生成]] — 自我反思 RAG，同时也是幻觉抵抗方法

---
> 📎 **物理文献**：[[raw/articles/OpenAI 翁荔提出大模型「外在幻觉」：万字 blog 详解抵抗办法、产幻原因....md]]