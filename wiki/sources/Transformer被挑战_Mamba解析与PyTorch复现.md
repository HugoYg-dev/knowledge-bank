---
type: source
tags:
- LLM/arch/Mamba
summary: Mamba 架构解析 + 完整 PyTorch 复现代码：S6 模块、MambaBlock、RMSNorm、SRAM/HBM 内存优化、enwiki8
  训练流程
sources:
- raw/playbooks/Transformer被挑战？新架构Mamba解析以及Pytorch复现.md
updated: '2026-07-01'
---
## 来源信息

- **标题**：Transformer被挑战？新架构Mamba解析以及Pytorch复现
- **作者**：机器学习杂货店（微信公众号）
- **URL**：https://mp.weixin.qq.com/s/BdT1qI4lXrA7JsFDoq5dQA

## 核心要点

- 现有模型对比：Transformer（O(L²) 计算/内存）、RNN（恒定内存但长程依赖弱）、S4（捕获远程依赖且内存高效）
- Mamba 核心：选择性状态空间，兼具 RNN 的推理效率和 Transformer 的训练并行性；训练时像 Transformer 同时处理全序列，推理时像 RNN 按步骤处理
- 固定主干 + 输入相关转换：A 矩阵（固定）控制状态转移，B 矩阵（依赖当前输入）控制输入影响隐状态的方式
- 硬件优化：GPU 有 HBM（大但慢）和 SRAM（小但快）；Mamba 将离散化和递归计算直接在 SRAM 中执行，减少 HBM↔SRAM 数据搬运；融合选择扫描层使内存需求与 FlashAttention 优化的 Transformer 相当
- PyTorch 实现关键组件：
  - `S6` 模块：包含 fc1/fc2/fc3 线性层，A 参数初始化为 Xavier uniform；`discretization()` 计算 dA=exp(Δ⊗A)、dB=Δ⊗B；`forward()` 支持两种隐状态更新机制
  - `MambaBlock`：inp_proj（d→2d）→ Conv1d（kernel=3, padding=1）→ SiLU → S6 → SiLU → 残差（D 线性层 + SiLU）→ out_proj（2d→d）；包含 RMSNorm
  - `Mamba`：3 个 MambaBlock 串联
  - `RMSNorm`：x * rsqrt(mean(x²) + eps) * weight
- 训练流程：bert-base-uncased tokenizer → enwiki8 数据集 → Embedding（d_model=8）→ AdamW（lr=5e-6）→ 25 epochs → perplexity 评估
- 超参数示例：d_model=8, state_size=128, seq_len=100, batch_size=256

## 关联

- [[概念_Mamba选择机制]] — 选择性状态空间原理
- [[概念_SSM_状态空间模型]] — SSM 数学基础
- [[概念_Mamba硬件感知算法]] — SRAM/HBM 优化细节
- [[概念_MambaBlock架构]] — Block 结构：投影+卷积+S6+残差
- [[实体_Mamba]] — Mamba 模型
- [[实体_S4]] — S4 前置架构

---
> 📎 **物理文献**：[[raw/playbooks/Transformer被挑战？新架构Mamba解析以及Pytorch复现.md]]