---
type: source
tags:
- LLM/training/post-train
summary: SFT 数据清洗三维度：质量（奖励模型打分）、多样性（K-Center-Greedy/聚类）、必要性（IFD 指标），梳理 MoDS/DEITA/CaR
  三类方法
sources:
- raw/articles/SFT数据挑选方法 - 知乎.md
updated: '2026-07-01'
---
## 来源信息

- 标题：SFT数据挑选方法
- 作者：深度人工dazed（知乎）
- URL：https://zhuanlan.zhihu.com/p/22529462474

## 核心要点

- SFT 数据清洗三个维度：**数据质量、数据多样性、数据必要性**

### 数据质量

- **MoDS**：使用 OpenAssistant reward-model-debertav3-large-v2，奖励分数高于阈值 α 则为高质量数据
- **DEITA**：
  - 指令复杂性：候选方法包括随机/长度/困惑度/ChatGPT 直接打分/语义树节点数/InstaTag/IFD；DEITA 方式是用 WizardLM 增强少量数据后训练 LLaMA 打分模型
  - 回答质量：类似方式，用 ChatGPT 改写高质量回复后训练 LLaMA 打分模型
- **CaR**：用 Sentence BERT 区分低质/高质量数据（基于 CoachLM 专家修改前后对比）

### 数据多样性

- **MoDS**：BERT 抽取特征 + K-Center-Greedy 算法，不断选出与已有中心点最远的样本
- **DEITA**：综合评分（复杂性×质量）排序 → LLaMA-13B 抽向量 → 逐个计算与保留池最小余弦相似度 → 保留相似度低于阈值 t 的数据
- **CaR**：sentence-transformers 抽向量 → PCA 降维 → K-Means 聚类（k=178）→ 每簇按分数取 top-n

### 数据必要性（IFD 指标）

- **IFD**：先用少量多样性数据（K-Means 100 簇各取 10 条，共 1000 条）微调基础模型，再计算：
  - `s(A|Q)`：给定问题时回答的困惑度（条件困惑度）
  - `s(A)`：单独回答的困惑度（无条件困惑度）
  - `IFD = s(A|Q) / s(A)`：IFD 高说明模型难以根据 Q 生成 A，即该数据对模型有训练价值
  - 注意：脏数据（Q 与 A 关联差）也可能得高 IFD，存在误选风险
- **MoDS 必要性过滤**：用多样性过滤后的数据微调模型 → 对高质量数据做推理 → 奖励值低于 β 则保留（模型无法很好回答的数据才有必要学）

## 关联

- [[概念_IFD指令跟随难度]]
- [[概念_K_Center_Greedy_中心贪婪算法]]
- [[概念_SFT数据三维度]]
- DEITA
- MoDS
- CaR

---
> 📎 **物理文献**：[[raw/articles/SFT数据挑选方法 - 知乎.md]]