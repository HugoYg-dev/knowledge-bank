---
type: source
tags:
- MachineLearning
- DeepLearning
summary: 介绍机器学习与深度学习中的双下降（Double Descent）现象，该现象对传统的偏差-方差折中理论提出了挑战，指出在模型复杂度跨越临界插值界限后测试误差可能会二次下降。
sources:
- raw/articles/2026-08-01_Double-Descent-vs.-Bias-Variance-Trade-off_19fbed_part3.md
updated: '2026-08-04'
---

# 来源信息
- **邮件主题**：Build a Stock Market Research Agentic Workflow
- **发送人**：Daily Dose of DS <avi@dailydoseofds.com>
- **发布日期**：2026-08-01
- **原始 ID**：19fbed5d2cd155dd

# 核心要点
- 传统的机器学习理论认为，随着模型参数数量的增加，模型会逐渐过拟合，测试误差会呈 U 型曲线（偏差-方差折中）。
- 双下降现象（Double Descent）表明，当进一步增加模型复杂度以跨越“插值临界界限”（即参数量等于样本量）并进入过度参数化区域时，测试误差不仅不会无限上升，反而会开始下降，从而改善泛化性能。
- 目前其根本原因仍是开放式科学问题，但部分理论指出，过度参数化区域中模型的“隐式正则化”帮助其聚焦于适量参数的特征，从而提升了泛化能力。
- 可以通过使用不同阶数 $m$（从 $1$ 到大于样本量 $n$）的多项式回归在一维虚拟数据集上重现这一双下降曲线。

# 关键引文
- "It depicts that increasing the model complexity beyond the point of interpolation can improve generalization performance."
- "And it’s hard to fathom since it challenges the traditional bias-variance trade-off"
- "Some theories suggest that the model applies an implicit regularization that allows it to precisely focus on an apt number of parameters for generalization."

# 联动概念与实体
- [[wiki/concepts/概念_机器学习双下降现象|概念_机器学习双下降现象]]
- [[wiki/concepts/概念_机器学习诊断分析图表|概念_机器学习诊断分析图表]]

---
> 📎 **物理文献**：[[raw/articles/2026-08-01_Double-Descent-vs.-Bias-Variance-Trade-off_19fbed_part3.md]]
