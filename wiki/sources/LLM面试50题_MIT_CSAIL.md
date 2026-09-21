---
type: source
tags:
- LLM/arch
- 面试
summary: MIT CSAIL 工程师整理的 50 个 LLM 核心面试题，覆盖架构、训练微调、推理、数学原理、高级系统设计五大主题
sources:
- raw/articles/信息过载时代，如何真正「懂」LLM？从MIT分享的50个面试题开始 ｜ 机器之心.md
updated: '2026-07-01'
---
## 来源信息

- **标题**：信息过载时代，如何真正「懂」LLM？从MIT分享的50个面试题开始
- **作者**：机器之心原创
- **URL**：https://www.jiqizhixin.com/articles/2025-06-18-9
- **LLM 指南来源**：MIT CSAIL 工程师 Hao Hoang 编写
- **文档链接**：https://drive.google.com/file/d/1wolNOcHzi7-sKhj5Hdh9awC9Z9dWuWMC/view

## 核心要点

### 一、核心架构与基本概念（问题 1–12）

- **Tokenization**：将文本分解为 token（单词/子词/字符），LLM 处理数值化 token 而非原始文本；BPE 处理 OOV 词汇
- **注意力机制**：通过 Q/K/V 向量相似性分数分配不同 token 的重要性；多头注意力允许同时关注输入的不同方面
- **上下文窗口**：LLM 能同时处理的 token 数（如 32K），定义模型短期记忆，更大窗口=更高计算成本
- **Seq2Seq 模型**：编码器（处理输入）+ 解码器（生成输出），用于翻译/摘要/聊天机器人
- **Embedding**：表征 token 语义的连续向量，初始化为随机或 GloVe 预训练值，训练中调整
- **Transformer 改进 Seq2Seq**：并行处理（自注意力代替序列 RNN）、长距离依赖捕获、位置编码维持顺序
- **位置编码**：正弦函数或可学习向量，向 Transformer 输入添加序列顺序信息
- **梯度消失解决方案**：自注意力（避免序列依赖）+ 残差连接（梯度直接路径）+ 层归一化

### 二、模型训练与微调（问题 13–18）

- **LoRA vs QLoRA**：LoRA 在层中插入低秩矩阵极少内存微调；QLoRA 在此基础上 4-bit 量化，可单 GPU 微调 70B 模型
- **灾难性遗忘预防**：重播（混合新旧数据）、弹性权重整合（EWC，保护重要权重）、模块化架构
- **PEFT**：只更新少量参数（如 LoRA），冻结其余以保留预训练知识
- **模型蒸馏**：小"学生"模型学习大"教师"模型的软概率输出，实现移动端部署
- **过拟合缓解**：L1/L2 正则化、Dropout、Early Stopping

### 三、推理与高级技术（问题 19–24）

- **温度参数**：控制输出随机性；高温=创造性多样，低温=确定性保守
- **Top-k/Top-p 采样**：Top-k 限制词汇表候选数量；Top-p（Nucleus Sampling）按累积概率截断
- **贪婪搜索 vs 束搜索**：贪婪每步选最高概率 token；束搜索保留 k 个候选路径
- **RAG**：检索→排序→生成，用外部文档提高事实准确性
- **CoT（思维链）提示**：引导 LLM 逐步推理，提升复杂任务准确性

### 四、训练范式（问题 25–31）

- **MLM（掩码语言建模）**：BERT 预训练方法，预测被掩盖 token，实现双向上下文理解
- **自回归模型 vs 掩码模型**：GPT 系列逐 token 生成（生成任务强）；BERT 双向理解（分类任务强）
- **零样本/少样本学习**：利用预训练通用知识，无需/仅需少量样本完成新任务

### 五、数学原理（问题 32–42）

- **Softmax 在注意力中**：将 Q·K^T 点积分数转为概率分布权重
- **注意力分数计算**：Attention(Q,K,V) = Softmax(QK^T/√d_k)V；O(N²) 二次复杂度
- **交叉熵损失**：衡量预测 token 概率与真实概率差异，惩罚错误预测
- **KL 散度**：度量两分布差异，用于微调过程指导对齐
- **自适应 Softmax**：按词汇频率分组减少不常见词汇计算

### 六、高级系统设计（问题 43–50）

- **GPT-4 vs GPT-3**：多模态输入（文本+图像）、25K token 上下文（vs 4096）、更少事实错误
- **MoE（专家混合）**：门控函数路由每个输入到特定子网络，激活约 10% 参数，高效大规模扩展
- **知识图谱集成**：验证事实减少幻觉、利用实体关系改善推理、提供结构化上下文
- **基础模型分类**：语言（BERT/GPT-4）、视觉（ResNet）、生成（DALL-E）、多模态（CLIP）
- **LLM 部署挑战**：资源密集、偏见延续、可解释性差、隐私安全

## 关联论文清单（文章提供）

- Attention Is All You Need（Transformer 基础）
- LoRA: Low-Rank Adaptation of Large Language Models
- BERT: Pre-training of Deep Bidirectional Transformers
- Language Models are Few-Shot Learners（GPT-3）
- Outrageously Large Neural Networks: Sparsely-Gated MoE
- Chain-of-Thought Prompting Elicits Reasoning in LLMs
- Retrieval-Augmented Generation for Knowledge-Intensive NLP

## 关联

- [[概念_Transformer架构]]
- [[概念_自注意力复杂度]]
- [[概念_FlashAttention_快速注意力]]
- [[概念_KV_Cache_键值缓存]]
- [[概念_LoRA_低秩适应微调]]
- [[概念_大模型训练三阶段]]
- [[概念_RLHF_基于人类反馈的强化学习]]
- [[概念_RAG基础流程]]
- [[概念_CoT_高级思维链方法]]
- [[概念_MoE混合专家]]
- [[概念_Fine_Tuning_模型微调]]
- [[实体_DeepSeek-R1]]
- [[实体_Qwen3]]

---
> 📎 **物理文献**：[[raw/articles/信息过载时代，如何真正「懂」LLM？从MIT分享的50个面试题开始 ｜ 机器之心.md]]