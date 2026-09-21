---
type: source
tags:
- RAG/embedding
- RAG/retrieval
summary: Qwen3 Embedding 与 Rerank 原理剖析：三层嵌入流程、[CLS] vs [EOS] 池化、Instruct 指令机制、Reranker
  的 LLM 化 yes/no 打分
sources:
- raw/articles/为什么用Qwen3 embedding和rerank.md
updated: '2026-07-01'
---
# 为什么用Qwen3_embedding和rerank

## 核心内容

### 背景

Qwen3 Embedding 在 MTEB 排行榜上开源闭源现在都是第一，Rerank 同样领先（4B 除 8B 外也基本第一）。

### Embedding 三层流程

**第一层：词元嵌入（Token Embedding）——查字典阶段**
- 分词后查 Embedding Layer 得到每个 token 的初始向量
- 这层向量是**上下文无关**的（如 "bank" 在 river bank 和 investment bank 中向量相同）

**第二层：上下文感知（Contextualization）——Transformer**
- 将初始向量序列送入 Transformer 多层自注意力机制（QKV）深加工
- 每个 token 向量吸收整句话上下文信息后更新
- 此后 "bank" 在不同上下文中向量不再相同
- 仍是词元序列对应一串向量（每 token 一个）

**第三层：句子嵌入（Sentence Embedding）——从一串到一个**
- 通过聚合/池化（Pooling）策略浓缩成代表整句的整体向量
- 这里 BGE 代表的 BERT 派和 Qwen3 代表的 LLM 派有区别

### [CLS] vs [EOS] 池化策略

**传统 BERT（[CLS] 策略）**：
- 输入最前面加 [CLS] 标记，训练使该标记最终向量代表整句含义
- 格式：`[CLS] 句子A [SEP] 句子B [SEP]`

**Qwen3（[EOS] 策略）**：
- 因为是 causal LLM（单向，看不到前面），在序列末尾加 [EOS] 标记
- 整个语义被压缩到最后一个 special token（EOS），其 hidden state 等价于 CLS

### Qwen3 Embedding 为何效果好 10 几个百分点

1. **模型够大**：维度大隐空间表征丰富，泛化性更好
2. **基础模型太强**（核心）：Qwen3 语义理解远超 BERT，也强于早期用 mistral 训练的方案
3. **训练方法**：
   - 前两阶段对比学习，第 3 阶段加 Slerp
   - 合成数据用 Qwen32 刷，约 1.5 亿对弱监督训练文本对
   - 精确控制任务类型、语言、文本长度、难度等多样性维度；两阶段生成流程先配置文档"角色"再生成查询
   - FT 阶段约 700 万对人工标注 + 1200 万对高质量合成数据
   - Slerp 融合多个 step 的 checkpoint

### Instruct 新玩法

- Qwen3 支持 `prompt_name="query"` 即 instruct 机制
- 默认 instruct：`Given a web search query, retrieve relevant passages that answer the query`
- 查询连同 instruct 一起进入问题塔 encoder，相当于给查询加了控制
- 应用示例：
  - FAQ 问题→问题相似匹配：`For the given user question, find the most similar question from the FAQ list`
  - 相关推荐（主题/风格）：`Find other articles with a similar topic` / `similar narrative style`
  - 代码功能性搜索：`Find code snippets that perform a similar function`（Qwen3 代码检索强项）
  - 细粒度评论情感分析：检索关于电池续航的负面评价
- 注意：现有大部分 RAG 系统不支持该能力，需改进工具来 fit

### Qwen3 Reranker

- 与传统 rerank 不同（传统单塔最后一层 linear 输出 logit）
- 用 system prompt 让模型生成 yes/no，输出 yes 的概率得分
- 评分公式：`score = P("yes") / (P("yes") + P("no"))`，取值 0~1
- 需做 padding 左移以兼容
- 输入采用类聊天模板（结构化对话）：
  - System Prompt：设定角色，规定答案只能是 yes/no（排序转为二元分类）
  - User Block：`<Instruct>` + `<Query>` + `<Document>`
  - Assistant Prompt 结尾让模型思考生成判断
- Qwen3 基础模型有 0.6B/4B/8B 规模，支持 32K 长上下文
- 通过将排序任务"LLM 化"/"对话化"释放基础模型潜力

## 关联

- 相关概念：[[概念_Embedding与向量检索]]、[[概念_Instruct_Embedding_指令增强向量嵌入]]、[[概念_Sentence_BERT_孪生网络句向量]]、[[概念_Rerank_重排序]]
- 实体：[[实体_Qwen3_Embedding]]、[[实体_Sentence_Transformers]]

---
> 📎 **物理文献**：[[raw/articles/为什么用Qwen3 embedding和rerank.md]]