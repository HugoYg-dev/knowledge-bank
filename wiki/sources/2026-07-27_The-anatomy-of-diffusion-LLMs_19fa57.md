---
type: source
tags:
- LLM/arch
- LLM/inference
summary: 介绍了扩散语言模型（dLLMs）的基本原理、物理架构优势（从 memory-bound 转向 compute-bound），以及掩码扩散、Block
  Diffusion、注意力掩码退火与推理加速技术。
sources:
- raw/articles/2026-07-27_The-anatomy-of-diffusion-LLMs_19fa57.md
updated: 2026-08-04
---

# 来源信息
- **标题**: The anatomy of diffusion LLMs
- **作者**: Daily Dose of DS
- **日期**: 2026-07-27
- **原文链接**: [[raw/articles/2026-07-27_The-anatomy-of-diffusion-LLMs_19fa57.md]]
- **关联概念**:
  - [[concepts/概念_扩散模型]]
  - [[concepts/概念_LLM推理两阶段]]

# 核心要点
1. **内存带宽瓶颈（Memory-Bound）**：传统自回归模型（Autoregressive LLMs）逐个 token 生成，每次生成都需要将庞大的模型权重载入 GPU 内存，计算密度极低（在 A100 上约 1 FLOP/Byte），受限于内存带宽限制。
2. **计算受限瓶颈（Compute-Bound）**：扩散大语言模型（dLLMs）采用完全掩码（Full Mask）序列开始，使用双向注意力机制，在多步迭代中并行解码/解掩码。由于在每一步并行处理多个 token，这把推理过程从 Memory-Bound 转向 Compute-Bound，大幅提升了 GPU 计算效率。
3. **离散掩码扩散（Masked Diffusion）**：在离散 Token 空间中，高斯噪声不再适用，因此采用离散的 MASK 替换作为噪声机制，使用变分证据下界（ELBO）为导向的训练目标函数。
4. **模型无缝转换与兼容性**：通过注意力掩码退火（Attention Mask Annealing）技术，可将预训练好的自回归 LLaMA 等模型无缝转换为 dLLM；同时，Block Diffusion 技术使 dLLM 能兼容传统的 KV Cache。
5. **推理加速栈与吞吐优化**：包括 Fast-dLLM（块级 KV 缓存）、基于置信度感知（Confidence-Aware）的并行解码、LLaDA 2.1 级的 Token 编辑技术，并可在 SGLang 中进行生产级服务部署。

# 关键引文
> Each token requires loading the full model weights through GPU memory, performing a tiny computation, and then loading all the weights again for the next token. On an A100, this means roughly 1 FLOP per byte of data moved, while the GPU is designed for 100+ FLOPs per byte.

> They start with a fully masked sequence and iteratively unmask all tokens in parallel, using bidirectional attention at every step. This shifts inference from memory-bandwidth bound to compute-bound, which is exactly where modern GPUs are efficient.

---
> 📎 **物理文献**：[[raw/articles/2026-07-27_The-anatomy-of-diffusion-LLMs_19fa57.md]]
