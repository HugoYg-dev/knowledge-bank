---
type: source
tags:
- LLM/arch
- LLM/inference
- Skill/data-analysis
summary: 探讨大模型量化技术（Quantization）及其面临的离群值（Outliers）挑战，并详细对比五种主流的量化方法（RTN、GPTQ、AWQ、LLM.int8()、QAT）的实现机制与应用场景。
sources:
- raw/articles/2026-07-21_5-LLM-Quantization-Techniques_19f86b.md
updated: 2026-08-04
---

# 5 LLM Quantization Techniques (Source 摘要)

## 来源信息
- **来源**: Daily Dose of DS
- **作者**: Avi
- **日期**: 2026-07-21
- **原始物理文献**: [[raw/articles/2026-07-21_5-LLM-Quantization-Techniques_19f86b.md]]
- **关联概念**: [[concepts/概念_量化|量化]]

## 核心要点
1. **量化的必要性与数值折算**：在 FP16 精度下，一个 70B 参数的模型仅权重就需要 140GB 显存，超出了单张显卡（如 H100 80GB, RTX 4090 24GB）的容量，导致必须使用多卡和张量并行。通过量化将权重映射到低比特（如 4-bit），显存占用可降低 4 倍（70B 模型缩减至 35GB），从而可在单张 40GB 或 48GB 显卡上运行。
2. **离群值（Outliers）的挑战**：在大于 6.7B 参数的 Transformer 模型中，约有 0.1% 的特征维度存在比正常值大 20x 至 100x 的极端离群值。简单的 Round-to-Nearest（RTN）由于需要覆盖这些离群值的范围，会导致网格划分过大（Scale Factor 变大），从而将正常范围内的其余 99.9% 权重压塌合并进极少数几个量化级别中，严重损毁精度。
3. **五大主流技术对比**：
   - **RTN (Round to Nearest)**：最基础、廉价的无校准量化，低 bit 下由于舍入误差累积导致精度极差。
   - **GPTQ**：通过校准集逐层量化，量化过程中计算并利用二阶误差补偿来微调未量化的权重。速度快，但在低比特下可能对校准集过拟合。
   - **AWQ (Activation-aware Weight Quantization)**：通过校准集观测激活，对乘以较大激活值的核心权重（约 1% 的通道）应用缩放因子放大保护，从而保留精度，随后整体量化为 INT4。此方法不依赖复杂的二阶计算，泛化性好，已成为 vLLM 等推理引擎的主流生产标准。
   - **LLM.int8()**：在推理时动态分离极少数离群维度（使用 FP16 运行）与其余 99.9% 正常维度（使用 INT8 运行），再行合并。无须预先计算，是 `bitsandbytes` (如 `load_in_8bit`) 的基础，但由于矩阵乘法的分割与合并，推理并发性能较差，常用于本地开发与 QLoRA 微调。
   - **QAT (Quantization-Aware Training)**：在训练/微调期间的前向传播中模拟量化舍入，在反向传播中仍以全精度更新权重，使模型适应量化带来的损耗。例如 Google Gemma 3 QAT 经过约 5000 步的微调，让 INT4 量化版本逼近全精度质量。

## 关键引文
> Beyond roughly 6.7B parameters, every transformer layer develops a handful of hidden dimensions carrying values 20x to 100x larger than the rest. These dimensions make up about 0.1% of the model’s features, but zeroing them out nearly destroys the model’s ability to predict text.
> They differ in where the outlier problem gets addressed, at rounding time, after rounding, before rounding, at inference, or during training itself.

---

> 📎 **物理文献**：[[raw/articles/2026-07-21_5-LLM-Quantization-Techniques_19f86b.md]]
