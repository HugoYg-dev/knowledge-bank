---
type: source
tags:
- LLM/arch/Mamba
summary: 知乎中文解析 Mamba 论文：选择机制动机、硬件感知算法、选择性复制与归纳头任务，作者背景（Albert Gu / Tri Dao）
sources:
- raw/articles/一文读懂Mamba：具有选择状态空间的线性时间序列建模 - 知乎.md
updated: '2026-07-01'
---
## 来源信息

- **标题**：一文读懂 Mamba：具有选择状态空间的线性时间序列建模
- **作者**：SakuraK（知乎）
- **URL**：https://zhuanlan.zhihu.com/p/680846351
- **原论文**：Mamba: Linear-Time Sequence Modeling with Selective State Spaces（arXiv:2312.00752）
- **代码**：https://github.com/state-spaces/mamba

## 核心要点

- 论文作者：Albert Gu（CMU 助理教授、Cartesia AI 联合创始人）和 Tri Dao（普林斯顿助理教授、Together AI 首席科学家）；均毕业于斯坦福，导师 Christopher Ré
- Transformer 两大根本缺陷：① 无法对有限窗口外内容建模；② 序列长度的二次缩放问题（O(L²) 计算复杂度）
- 现有亚二次架构（线性注意力/门控卷积/SSM）的共同弱点：无法进行基于内容的推理
- SSM 本质：RNN 与 CNN 的结合，灵感来自经典状态空间模型（Kalman 1960）；在离散/信息密集数据（文本）上效果不佳
- Mamba 三大改进：① 选择机制（让 SSM 参数成为输入的函数）；② 硬件感知算法；③ 简化架构（去掉注意力和 MLP，仅用 SSM）
- 选择机制：设计简单——对 SSM 参数用输入进行参数化，使模型能过滤无关信息、无限期记住相关信息
- 注：全文因 Cubox 截断，硬件感知算法部分未完整保存，confidence 仍为 high（核心贡献部分完整）

## 关联

- [[概念_Mamba选择机制]] — 选择机制原理
- [[概念_SSM_状态空间模型]] — SSM 基础
- [[概念_LTI_线性时不变]] — LTI 局限，motivates 选择机制
- [[实体_Mamba]] — Mamba 模型
- [[实体_Albert_Gu]] — Mamba 第一作者
- [[实体_Tri_Dao]] — Mamba 第二作者，FlashAttention 作者

---
> 📎 **物理文献**：[[raw/articles/一文读懂Mamba：具有选择状态空间的线性时间序列建模 - 知乎.md]]