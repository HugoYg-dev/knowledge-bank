---
type: source
tags:
- MachineLearning
summary: 本文详细介绍了机器学习中周期性特征（如时间、星期、季节等）的编码方法。传统的线性编码方法无法体现周期的邻近性，导致信息丢失。通过使用 sine 和
  cosine 三角函数，可以将周期性特征映射到单位圆上，从而在保留物理邻近性（例如 23点 和 0点 等距）的同时进行有效编码。
sources:
- raw/articles/2026-04-23_Cyclical-feature-encoding_19dbca.md
updated: 2026-08-04
---

# 来源信息
- **邮件主题**: Top AI Labs Share an Agent Memory Trick Most Miss
- **发送人**: Daily Dose of DS \<avi@dailydoseofds.com\>
- **日期**: 2026-04-23
- **原始文章链接**: [Cyclical feature encoding](https://www.dailydoseofds.com/11-powerful-techniques-to-supercharge-your-ml-models/)

# 关联概念与实体
- [[wiki/concepts/概念_周期性特征编码|概念: 周期性特征编码]]

# 核心要点
- **周期性特征的特点**：诸如一天中的小时（0-23）、星期几（周一到周日）、月份、风向和季节等特征具有周期性的循环规律，不同于传统的单向连续数值或普通的类别特征。
- **传统线性编码的缺陷**：如果直接使用 0-23 表示小时，模型无法学到“23点”与“0点”是相邻的。这导致：
  - 数值上的 23 与 0 距离最大，但它们在物理时间上只相差 1 小时。
  - 特征之间的几何距离不合理，限制了模型的表达和泛化能力。
- **三角函数双通道编码（Sine/Cosine Encoding）**：
  - 利用 $\sin$ 和 $\cos$ 的周期性、有界性和连续性，将周期变量投射到二维极坐标（单位圆）中。
  - 对于周期为 $T$ 的特征 $x$，其编码公式为：
    - $x_{sin} = \sin\left(\frac{2\pi \cdot x}{T}\right)$
    - $x_{cos} = \cos\left(\frac{2\pi \cdot x}{T}\right)$
  - 这种二维特征工程手段保证了“23点”与“0点”的几何距离与“0点”与“1点”完全相同。
- **扩展应用**：此方法同样适用于其他任何有循环规律的特征，例如风向（N, NE, E...）、月相以及一年中的四季。

# 关键引文
> "Unlike other features that progress continuously (or have no inherent order), cyclical features exhibit periodic behavior."
> 
> "One of the most common techniques to encode such a feature is using trigonometric functions, specifically, `sine` and `cosine`."
> 
> "This way, the engineered feature satisfies both the properties we discussed earlier. The value “23” is close to “0” [and] The distance between “0” and “1” is the same as that between “23” and “0”."

---
> 📎 **物理文献**：[[raw/articles/2026-04-23_Cyclical-feature-encoding_19dbca.md]]
