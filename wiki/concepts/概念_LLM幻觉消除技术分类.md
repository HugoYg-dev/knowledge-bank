---
type: concept
tags:
- LLM/hallucination
summary: 基于论文 "A Comprehensive Survey of Hallucination Mitigation Techniques in Large
  Language Models"（arxiv 2401.01313）的系统分类框架。
sources:
- wiki/sources/LLM_32种消除幻觉技术综述.md
- wiki/sources/大模型幻觉陷阱_AGI之路04期.md
updated: '2026-09-07'
---


# 概念：LLM 幻觉消除技术分类（32 种）

基于论文 "A Comprehensive Survey of Hallucination Mitigation Techniques in Large Language Models"（arxiv 2401.01313）的系统分类框架。

## 两大类别

```
幻觉消除技术
├── 提示工程（Prompt Engineering）
│   ├── 检索增强生成（RAG）——生成前/中/后/端到端
│   ├── 通过反馈自我完善
│   └── 提示微调（软提示学习）
└── 开发新模型
    ├── 新的解码策略
    ├── 利用知识图谱
    ├── 基于忠诚度的损失函数
    └── 有监督微调
```

## 提示工程——RAG 按时间维度分类

| 时机 | 代表方法 | 核心思想 |
|------|---------|---------|
| 生成前 | LLM-Augmenter | 迭代检索+验证候选响应 |
| 生成前 | FreshPrompt | 搜索引擎整合最新信息 |
| 生成中 | 知识检索 | logit 识别幻觉并实时纠正 |
| 生成中 | EVER | 实时三阶段生成-验证-纠正 |
| 生成后 | RARR | 研究+后期编辑对齐证据 |
| 生成后 | 高熵词汇替换 | 替换高熵词降低幻觉 |
| 端到端 | Seq2Seq+DPR | 生成时以检索文档为条件 |

## 提示工程——反馈自我完善关键方法

- **CoVe**：验证链，初始→验证问题→独立回答→精练输出
- **CoNLI**：NLI 链幻觉检测 + 后期编辑，无需调整模型
- **Mind's Mirror**：将 LLM 自我评估能力蒸馏进 SLM
- **DRESS**：条件 RL 处理视觉语言模型
- **MixAlign**：不确定时请用户澄清

## 模型开发——解码策略

- **CAD（上下文感知解码）**：对比有/无上下文分布差异，无需额外训练
- **DoLa（对比层解码）**：对比 Transformer 前后层 logit，利用知识局部化
- **ITI（推理时介入）**：识别真实性相关注意力头，推理时调整激活方向

## 模型开发——监督微调关键方法

- **R-Tuning**：构建拒绝训练数据，教模型对超能力问题保持沉默
- **TWEAK**：假设验证模型对候选排名，不重训生成模型

## 相关资源

- [[LLM_32种消除幻觉技术综述]] — 详细 source 页
- [[概念_抗幻觉方法]] — 主要方法详解
- [[概念_幻觉检测方法]] — 检测方法体系
- [[概念_LLM外在幻觉与上下文内幻觉]] — 幻觉定义