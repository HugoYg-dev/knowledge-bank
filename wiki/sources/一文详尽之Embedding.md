---
type: source
tags:
- RAG/embedding
summary: Embedding 全景综述：从独热编码/词袋/主题模型/Word2Vec 到 BERT 各向异性问题及优化方法（SBERT/Bert-flow/Bert-whitening/SimCSE）
sources:
- raw/articles/一文详尽之Embedding（向量表示）！.md
updated: '2026-07-01'
---
# 一文详尽之Embedding

## 用户高亮 [重点/高亮]

> 句向量（Sentence Embedding）是将整个句子转换为固定长度的向量表示的方法。最简单的句向量获取方式是基于平均词向量的方法：将句子中的每个词转换为词向量，然后对这些词向量取平均得到句子向量。

用户批注：WordEmbedding -> SentenceEmbedding，此时的SentenceEmb还不是Bert时代的Embedding

> 大模型时代的展望

用户批注：https://aws.amazon.com/cn/blogs/china/practice-of-knowledge-question-answering-application-based-on-llm-knowledge-base-construction-part-4/

## 核心内容

### 1. 文本表示模型演进

#### 1.1 独热编码（One-Hot Encoding）
- 每个词转为高维稀疏向量，只有一个位置为 1
- 缺点：高维稀疏性；无法捕捉词语之间的关系

#### 1.2 词袋模型与 N-gram 模型
- 词袋模型（BoW）：文档表示为词频向量，不考虑词序
- N-gram：通过连续 n 个词序列捕捉局部上下文

#### 1.3 主题模型
- 代表：pLSA、LDA
- 解决词袋模型无法识别相同主题的词/词组的问题
- 将文档表示为主题概率分布，维度较低（等于主题数），降低稀疏性

#### 1.4 词向量（Word Embedding）
- 将词映射到低维稠密向量空间
- Word2Vec：CBOW 和 Skip-gram 两种结构，通过最大化上下文词出现概率优化
- 其他方法：GloVe、FastText
- 相似度度量：余弦相似度、欧氏距离
- 问题：上下文无关（一词多义）；OOV 问题；语法语义信息捕捉不足

#### 1.5 句向量（Sentence Embedding）
- 最简单方式：词向量取平均
- SIF/USIF 加权算法：考虑词重要性差异，使用随机游走推算句子生成概率
- Doc2vec：基于 Word2Vec 扩展，增加 Paragraph vector；PV-DM 和 PV-DBOW 两种训练方式

### 2. 基于 BERT 的文本向量

#### 2.1 BERT 向量的各向异性问题
- 通常使用最后一层 [CLS] 向量或最后一层 MeanPooling 获取文本向量
- **各向异性**：词向量在向量空间中占据一个狭窄的圆锥形体
- 高频词靠近原点，低频词远离原点；高频词分布紧凑，低频词分布稀疏
- 导致余弦相似度计算不准确——向量都挤在一起，彼此相似度都很高
- 不只 BERT，大多数 Transformer 架构预训练模型（包括 GPT-2）都有类似问题
- 好的向量表示应满足 alignment（相似向量距离相近）和 uniformity（向量空间均匀分布）

#### 2.2 有监督优化：Sentence-BERT（SBERT）
- 修改预训练 BERT 结构，通过有监督任务微调优化向量相似度计算
- 孪生(Siamese)网络 + 三级(Triplet)网络
- 三种目标函数：
  1. Classification Objective：交叉熵损失
  2. Regression Objective：余弦相似度 + MSE
  3. Triplet Objective：欧式距离，边距为 1
- 使用 NLI 标注数据集（SNLI/MNLI）训练，展现较好的语义扩展性和鲁棒性

#### 2.3 无监督优化

**Bert-flow**：
- 基于流式生成模型，将 BERT 表示可逆映射到标准高斯分布
- BERT 参数不参与训练，只优化 flow 模型参数
- 训练目标：最大化从高斯分布中产生 BERT 表示的概率

**Bert-whitening**（苏剑林）：
- 分析余弦相似度仅在标准正交基下成立
- 将 BERT 向量均值变换为 0、协方差矩阵变换为单位阵（白化操作）
- 比 Bert-flow 更简单

**SimCSE**：
- 利用预训练模型中的 Dropout mask 作为增广手段
- 对每个样例进行两次前向传播得到两个不同 embeddings 作为正样本对
- 同 batch 其他样例的 embeddings 作为负样本
- 有监督版本：利用 NLI 数据，entailment 作正样本，contradiction 作 hard negative

### 3. 大模型时代展望

- LLM 时代向量模型训练范式尚在探索：自动编码 or 对比学习

## 关联

- 相关概念：[[概念_Embedding与向量检索]]、[[概念_词向量]]、[[概念_BERT各向异性]]、[[概念_Sentence_BERT_孪生网络句向量]]、[[概念_SimCSE_简单对比学习句向量]]
- 实体：[[实体_Sentence_Transformers]]

---
> 📎 **物理文献**：[[raw/articles/一文详尽之Embedding（向量表示）！.md]]