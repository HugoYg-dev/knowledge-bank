---
type: source
tags:
- LLM/arch/MoE
- Skill/python
summary: 从零 PyTorch 实现稀疏 MoE 语言模型：Top-k 门控、噪声 Top-k、SparseMoE 模块到完整训练循环
sources:
- raw/playbooks/手把手教你，从零开始实现一个稀疏混合专家架构语言模型（MoE）.md
updated: '2026-07-01'
---
## 来源信息

- **标题**：手把手教你，从零开始实现一个稀疏混合专家架构语言模型（MoE）
- **来源**：机器之心，极市平台
- **URL**：https://mp.weixin.qq.com/s/zyZndz65GKUydmwBgdlSZw
- **代码仓库**：https://github.com/AviSoori1x/makeMoE/tree/main

## 核心要点

- 在 Andrej Karpathy 的 makemore 基础上改造，用稀疏 MoE 替换单一 FFN，基于莎士比亚文本语言建模
- 自注意力层与普通 Transformer 相同，差异仅在 FFN 位置替换为多个稀疏激活的专家网络
- **Expert 模块**：每个 Expert 是 MLP（Linear→ReLU→Linear→Dropout），是 FFN 的直接替代
- **TopkRouter**：Linear 层投影到 Expert 数量维度，取 top-k logits，其余填 -inf，Softmax 得稀疏权重
- **NoisyTopkRouter**：在 logits 上叠加标准正态噪声（Softplus 缩放），实现负载均衡探索；论文认为噪声门控对 MoE 训练稳定性至关重要
- **SparseMoE 模块**：遍历每个 Expert，只对 top-k 选中它的 Token 执行前向传播，避免不必要的矩阵乘法，保证稀疏性
- **Block 整合**：MultiHeadAttention + SparseMoE + LayerNorm + 残差，形成完整 MoE Transformer Block
- 参数初始化使用 Kaiming He（因 Expert 含 ReLU），对比选项有 Xavier/Glorot
- 完整训练循环：AdamW 优化，MLFlow 跟踪指标，共 5000 步，最终 val loss 约 1.75
- 关键设计细节：SparseMoE 的索引操作 `final_output[expert_mask] += weighted_output`，确保加权求和正确

## 关键引文

无有效 Cubox 高亮内容。

## 关联

- [[概念_MoE混合专家]] — MoE 架构原理
- [[概念_MoE_Router_专家路由门控网络]] — Top-k Router 门控机制
- [[概念_MoE负载均衡]] — 噪声门控与负载均衡
- [[大模型面试面经_简单透彻理解MoE]] — MoE 理论基础
- [[概念_PyTorch训练循环]] — 训练循环模板

---
> 📎 **物理文献**：[[raw/playbooks/手把手教你，从零开始实现一个稀疏混合专家架构语言模型（MoE）.md]]