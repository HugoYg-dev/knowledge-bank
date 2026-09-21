---
type: source
tags:
- MachineLearning
summary: 探讨如何通过绘制学习曲线（Learning Curve）来评估是否需要收集更多训练数据。介绍了将数据集划分为多个等分并累加训练来测定模型表现的方法，并详细阐述了未饱和曲线与已饱和曲线的物理意义。
sources:
- raw/articles/2025-11-20_Should-you-gather-more-data_19aa2d.md
updated: 2026-08-03
---

# 来源信息
- **标题**: Should you gather more data?
- **来源**: Daily Dose of DS
- **日期**: 2025-11-20
- **链接**: [Daily Dose of DS](https://www.dailydoseofds.com/object-oriented-programming-with-python-for-data-scientists/)

# 关联概念与实体
- 学习曲线

# 核心要点
1. **模型性能瓶颈的诊断**: 当特征工程和更换模型仅带来微小提升时，通常意味着数据量不足。但由于收集新数据成本高，需要科学的方法来决策。
2. **学习曲线的测定方法**:
   - 将数据集等分成 $K$ 个子集（推荐 $7 \sim 12$ 份）。
   - 采用累加合并的方式逐步增加训练集数据量：第一次只用第 1 个子集，第二次用前 2 个子集，以此类推。
   - 测量每次训练后模型在固定验证集（Validation Set）上的表现。
3. **关键演进路线解析**:
   - **未饱和曲线（Line A）**: 验证集性能随着数据量增加而持续上升。说明模型仍处于高方差（High Variance）阶段，收集更多数据可以有效提高泛化能力。
   - **已饱和曲线（Line B）**: 验证集性能在大约一半或更少的数据量时就已经趋于平缓。说明模型进入了高偏差（High Bias）阶段，即性能已经饱和，追加更多数据收效甚微，此时应转向特征工程或更换更复杂的模型。

# 关键引文
> "This is usually an indicator that we don’t have enough data to work with. But since gathering new data can be a time-consuming and tedious process... here's a technique to determine whether more data will help."
> "Line A conveys that adding more data will likely increase the model's performance. Line B conveys that the model's performance has already saturated. Adding more data will most likely not result in any considerable gains."

---
> 📎 **物理文献**：[[raw/articles/2025-11-20_Should-you-gather-more-data_19aa2d.md]]
