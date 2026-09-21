---
type: source
tags:
- CV/detection
summary: 系统介绍 Meta AI 的 Segment Anything Model（SAM）：架构（ViT 图像编码器 + Prompt 编码器 + 轻量
  Mask 解码器）、训练方法（Focal Loss + Dice Loss、SA-1B 数据集三阶段标注）、多模态 CLIP 集成、交互/自动分割模式。
sources:
- raw/articles/分割一切(Segment Anything)不是梦，SAM模型引领图像分割新时代....md
updated: '2026-07-01'
---
# SAM：Segment Anything Model

## 来源信息

- 标题：分割一切(Segment Anything)不是梦，SAM模型引领图像分割新时代
- 平台：知乎专栏
- URL：https://zhuanlan.zhihu.com/p/619659530
- 基于全文 ingest

## 核心要点

1. **[重点/高亮] SAM 架构**：由 3 个主要部分组成——提示词编码器（Prompt Encoder）、图像编码器（Image Encoder）和轻量级掩码解码器（Mask Decoder）。图像通过图像编码器处理，提示（点、框、掩码、文本）通过提示编码器转换。掩码解码器接收两者表征并产出掩码。图像编码器是计算量最大的部分。

2. **图像编码器**：基于 ViT-H/16 + MAE 预训练。输入 1024×1024 RGB，输出 64×64×256 embedding。处理时间 ~0.2-0.3s/GPU。三种模型规模：ViT-B(86M)、ViT-L(308M)、ViT-H(636M)。

3. **Prompt 编码器**：
   - 点（Point）：位置编码 + 学习嵌入（前景/背景区分）
   - 框（Box）：角点对编码
   - 掩码（Mask）：卷积编码为 4×64×64
   - 文本：通过 CLIP 集成

4. **Mask 解码器**：轻量 Transformer，双向注意力（prompt→image, image→prompt）。对模糊 prompt 生成 3 个候选 mask + 置信度分数。IoU 预测头评估 mask 质量。

5. **训练**：
   - 损失函数：20×Focal Loss + Dice Loss
   - Focal Loss（RetinaNet）：解决类别不平衡，FL(pt)=-αt(1-pt)^γ log(pt)，下调简单样本权重
   - Dice Loss：衡量预测与 GT mask 重合度，1-2|X∩Y|/(|X|+|Y|)

6. **SA-1B 数据集**：11M 张图像，1.1B mask，平均每张 100 个 mask。三阶段收集：人工标注 → 半自动（SAM 预生成+人工修正）→ 全自动。

7. **自动分割模式（Segment Everything）**：32×32 点网格覆盖图像，每点生成 mask，NMS 去重。

8. **局限性**：细节结构（发丝、线缆）困难、边界精度有限、最小 prompt 下歧义、图像编码器计算开销大、文本 prompt 需额外 CLIP。

## 关联概念

- [[概念_图像分割]]
- [[概念_Prompt驱动分割]]
- [[概念_Focal_Loss_焦点损失]]
- [[概念_Vision_Transformer_视觉Transformer]]

## 关联实体

- [[实体_SAM]]
- [[实体_CLIP]]
- [[实体_ViT]]

---
> 📎 **物理文献**：[[raw/articles/分割一切(Segment Anything)不是梦，SAM模型引领图像分割新时代....md]]