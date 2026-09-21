---
type: concept
tags:
- LLM/arch/Mamba
summary: Mamba 的基本构建单元，类比 Transformer 的 decoder block，可堆叠多层。
sources:
- wiki/sources/A_Visual_Guide_to_Mamba_and_SSM.md
- wiki/sources/Mamba2_SSD_大一统.md
- wiki/sources/Transformer被挑战_Mamba解析与PyTorch复现.md
updated: '2026-06-29'
---


# Mamba Block 架构

Mamba 的基本构建单元，类比 Transformer 的 decoder block，可堆叠多层。

## Mamba1 Block 结构

```
输入 x
 ├── 线性投影（d → 2d，扩展嵌入）
 │    ├── 分支 A：1D Conv（kernel=3）→ SiLU → Selective SSM（S6）→ SiLU
 │    └── 分支 B：线性层 → SiLU（残差门控）
 ├── 分支 A × 分支 B（逐元素乘，引入非线性）
 └── 输出线性投影（2d → d）
```

Selective SSM（S6）包含：
- 离散化（ZOH，步长 Δ）
- HiPPO 初始化的矩阵 A
- 选择扫描算法（parallel scan）
- 硬件感知算法（kernel fusion + recomputation）

1D Conv 的作用：防止 token 独立计算（SSM 之前做局部混合）

## Mamba2 Block 改进

- **并行参数投影**：A、B、C、X 通过单次投影并行产生（类比 QKV 一起投影），减少参数量，支持 Megatron 张量并行
- **额外归一化层**：在输出投影前加 LayerNorm / GroupNorm / RMSNorm，防止大模型训练不稳定
- SSD 层（状态空间对偶）替代 S6，见 [[概念_SSD_状态空间对偶]]

## PyTorch 实现要点（Mamba1）

```python
# MambaBlock 核心流程
x_proj = self.inp_proj(x)          # d → 2d
x_conv = self.conv(x_proj)         # 1D conv, kernel=3
x_conv_act = F.silu(x_conv)
x_ssm = self.S6(x_conv_act)        # Selective SSM
x_act = F.silu(x_ssm)
x_residual = F.silu(self.D(x))     # 残差分支
x_out = self.out_proj(x_act * x_residual)
```

## 来源

- [[A_Visual_Guide_to_Mamba_and_SSM]]
- [[Transformer被挑战_Mamba解析与PyTorch复现]]
- [[Mamba2_SSD_大一统]]