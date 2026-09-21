---
type: source
tags:
- AI-Agent/AI-BI
summary: 矩阵起源实践：NL2SQL 生产落地需要 AI-ready data（M-Schema+约束池）+ 小模型（Qwen2.5-Coder 3B/7B
  LoRA）+ 两级 Schema Linking，结构幻觉率从7.9%降至1.3%
sources:
- raw/articles/企业落地 NL2SQL，需要的是 AI-ready data 和 小模型.md
updated: '2026-07-01'
---
# 企业落地 NL2SQL，需要的是 AI-ready data 和 小模型

## 来源信息

- 原文标题：企业落地 NL2SQL，需要的是 AI-ready data 和 小模型
- 作者：矩阵起源（InfoQ）
- URL：https://mp.weixin.qq.com/s/m-y-ZvTMQw88uJseYpMyEA

## 核心要点

### 核心观点：四个关键判断

1. **先数据、后模型**：把元数据/业务语义/权限/样例 SQL 做成"AI-ready data"，是可靠落地第一性问题
2. **小模型足够用**：3B-7B 代码/SQL 友好模型 + LoRA 微调 + 语法约束解码 + 执行校验，效果很好
3. **落地成本低**：相比 100B+ 通用大模型，小模型算力支撑企业更容易投入
4. **评估换维度**：Execution Accuracy（执行一致性）比 Exact Match 更接近真实可用性

### "大模型+开箱即用"失灵的四大原因

- **业务语义缺席**：字段名（amt/dt/no）在不同库含义不同，缺少别名词典/指标口径/实体映射
- **治理与合规割裂**：多租户/行列权限/审计等导致"能生成 ≠ 能执行"
- **评估口径失真**：只看 Exact Match，忽略结果等价与实际可执行性
- **成本/延迟不可控**：超长上下文 → Context-Rot + Lost in the middle 问题

### NL2SQL 任务属性：受限代码生成

- 输出是形式语言（SQL）：语法强约束、词表小、可执行可验证
- 输入可结构化：Schema/主外键/候选列/样例值可作为外部信号
- 所需推理是"结构性推理"：列/表选择/聚合/条件/时间窗，非开放域常识

### 为什么选小模型：三类理论支持

1. **语法/AST 约束降低搜索熵**：PICARD/CFG/XGrammar 屏蔽不合法 token，小模型+约束=大增益
2. **外部结构信息替代"内生常识"**：schema linking 将隐式知识外显，模型无需承载过多通用知识
3. **规模-性能-成本最优点**：Chinchilla（70B）在 closed-book QA 超越 GPT-3（128B）；phi 系列验证小模型可行性

### 技术架构总览

**两步式推理：**
- 第一步：Schema Linking（筛表/列/外键）→ 精简 Schema
- 第二步：在精简 Schema 上生成 SQL

**数据侧增强（AI-ready data）：**
- **M-Schema**：在传统表/列清单上补充类型/主键/中文释义/真实值示例
- **约束池**：自动识别查询语义类型，注入去重/精度/排序/限制等约束

**两级 Schema Linking：**
- BM25 粗排：表+列+注释拼文档，BM25 打分，Top-k 表，<5ms 延迟
- SIC 精排（Schema Item Classifier）：Encoder+交互层，逐项相关性打分，<2GB 显存

**小模型路线：**
- 基座：Qwen2.5-Coder-3B/7B
- 训练：LoRA 轻量精调，DeepSpeed 显存/吞吐优化
- 推理：低温度/束搜索，固定输出前缀

**统一数据底座：**
- MatrixOne（HTAP 数据库）+ Matrix Intelligence 平台
- 统一纳管 Schema/元数据/业务词典/权限
- 向量引擎辅助发现同义词/影子字段

### 关键实测结果

- 结构幻觉率：**7.9% → 1.3%**
- 语义误配：约 **-18%**
- Spider-S4 内部集 Execution Accuracy：**+6.4%**

## 关键引文

> 没有 AI-ready data，就没有可落地的 NL2SQL。 [重点]

> 当 NL2SQL 从 Demo 走向生产，关键不在"更大的模型"，而是"更干净的数据底座 + 更小的专用模型 + 更可控的工程化流程"。 [高亮]

> 在可强约束、可外接结构信息的 NL2SQL 上，最优点通常落在 3B-7B 代码向模型，而不是一味做大。 [重点]

## 关联

- [[概念_Text2SQL_自然语言转SQL]]
- [[概念_AI_Ready_Data_AI就绪数据]]
- [[概念_Schema_Linking_数据库模式联接]]
- [[概念_M_Schema_增强元数据模式]]
- AST约束解码
- [[实体_Qwen2.5-Coder]]
- MatrixOne

---
> 📎 **物理文献**：[[raw/articles/企业落地 NL2SQL，需要的是 AI-ready data 和 小模型.md]]