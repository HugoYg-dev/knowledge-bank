---
type: source
tags:
- CV/arch
summary: 详解 DiT（Diffusion Transformers）：用 Transformer 替换扩散模型中的 U-Net，在 Latent Space
  上对 patches 操作；探索 Patchify、4 种条件注入方式（adaLN-Zero 最优）、模型缩放性（GFLOPs 与 FID 强相关）；DiT-XL/2
  在 ImageNet 256x256 达到 SOTA FID 2.27。
sources:
- raw/articles/Sora的幕后功臣？详解大火的DiT：拥抱Transformer的扩散模型.md
updated: '2026-07-01'
---
# DiT：Transformer 构建扩散模型

## 来源信息

- 标题：Sora的幕后功臣？详解大火的DiT：拥抱Transformer的扩散模型
- 论文：Scalable Diffusion Models with Transformers (ICCV 2023, Oral)
- 作者：William Peebles, Saining Xie（UCB, NYU）
- URL：https://mp.weixin.qq.com/s/ScHjSd_JtcZKD2cJxWuavg
- 基于全文 ingest

## 核心要点

1. **动机**：Diffusion Models 一直使用 U-Net（继承自 PixelCNN++）作为骨干；本文证明 U-Net 架构设计对扩散模型性能并不关键，可被 Transformer 替换，从而受益于其可扩展性和鲁棒性。

2. **Latent Diffusion 框架**：先学 AutoEncoder 将图像压缩为小空间表征 z，再在 z 上训练扩散模型（VAE Encoder 下采样率 8），生成时采样 z 再解码。使用 Stable Diffusion 预训练 VAE。

3. **Patchify**：将 latent z 类似 ViT 切分为 patches，经 Linear Embedding + sine-cosine 位置编码变为 token 序列。Patch size p 与 token 数 T 满足 T = (I/p)^2 关系，p 减半则计算量 4 倍。

4. **DiT Block 设计（4 种条件注入方式）**：
   - In-Context Conditioning：时间步 t、类标签 c 作为额外 token 附加，额外 GFLOPs 微不足道
   - Cross-Attention Block：t/c embedding 作为独立序列做 Cross-Attention，额外约 15% GFLOPs
   - Adaptive Layer Norm (adaLN)：用 t/c 生成归一化的缩放/移位参数 γ/β
   - **adaLN-Zero**：额外回归缩放系数 α，初始化为 0 使 Block 初始为恒等映射；FID 最优且计算最高效

5. **模型缩放**：4 种尺寸 DiT-S/B/L/XL（0.3~118.6 GFLOPs），从深度 N、hidden dim d、head 数维度缩放。

6. **关键发现——GFLOPs 决定性能**：
   - 增大模型或减小 Patch Size 均可显著改善 FID
   - 参数量相似但 GFLOPs 不同时，FID 差异显著；GFLOPs 相似时 FID 相似（如 DiT-S/2 ≈ DiT-B/4）
   - GFLOPs 与 FID 存在强负相关

7. **大模型更计算高效**：小模型即使训练更久，计算效率最终低于大模型少训几步。同规模下小 Patch Size 更高效。

8. **缩放模型 vs 增加采样步骤**：DiT-XL/2 用 128 步（15.2 TFLOPs/图）优于 DiT-L/2 用 1000 步（80.7 TFLOPs/图），说明增加采样计算无法弥补模型本身计算量不足。

9. **实验结果**：
   - ImageNet 256×256：DiT-XL/2 FID 2.27（SOTA），118.6 GFLOPs 远低于 ADM 1120 GFLOPs
   - ImageNet 512×512：FID 3.04（优于 ADM 的 3.85），524.6 GFLOPs vs ADM 1983 GFLOPs

10. **训练配置**：AdamW 固定 lr=1e-4，batch 256，无 weight decay，数据增强仅 horizontal flip，EMA 0.9999，无 warmup。

## 关联概念

- [[概念_扩散模型]]
- [[概念_Latent_Diffusion]]
- Patchify
- adaLN_Zero
- [[概念_Vision_Transformer]]

## 关联实体

- [[concepts/概念_DiT|DiT]]
- [[实体_ViT]]

---
> 📎 **物理文献**：[[raw/articles/Sora的幕后功臣？详解大火的DiT：拥抱Transformer的扩散模型.md]]