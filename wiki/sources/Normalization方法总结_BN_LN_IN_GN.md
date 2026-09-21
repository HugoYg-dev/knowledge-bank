---
type: source
tags:
- DeepLearning
- 面试
summary: 总结四种 Normalization 方法 BN/LN/IN/GN 的区别——基于 [N,C,H,W] 特征图在不同维度做归一化（"一摞书"比喻）；BN
  的动机/作用/问题、LN 适配 RNN、IN 用于风格迁移、GN 解决小 batch 问题。
sources:
- raw/playbooks/常用 Normalization 方法的总结与思考：BN、LN、IN、GN.md
updated: '2026-07-01'
---
# 常用 Normalization 方法总结：BN、LN、IN、GN

## 来源信息

- 标题：常用 Normalization 方法的总结与思考：BN、LN、IN、GN
- 作者：G-kdom（知乎 https://zhuanlan.zhihu.com/p/72589565）
- URL：https://mp.weixin.qq.com/s/_o0Wa_1KVSa98bYDFA_bQA
- 基于全文 ingest

## 核心要点

特征图记为 [N, C, H, W]（N=batch，C=通道，H/W=高宽）。四者都对激活函数的输入做归一化，区别在归一化维度：

| 方法 | 年份 | 归一化维度 | 保留维度 | 主要用途 |
|------|------|-----------|---------|---------|
| **BN** Batch Norm | 2015 | N、H、W | C | CNN 等固定深度前向网络 |
| **LN** Layer Norm | 2016 | C、H、W | N | RNN / 变长序列 |
| **IN** Instance Norm | 2017 | H、W | N、C | 图像风格迁移 |
| **GN** Group Norm | 2018 | 分组后组内 | N | 小 batch（如图像分割）|

### "一摞书"比喻（N 本书、每本 C 页、每页 H 行、每行 W 字符）

- **BN**：按页码对应相加再除 N×H×W（求"平均书"，每页只有一个字）
- **LN**：每本书所有字相加除 C×H×W（求整本书"平均字"）
- **IN**：一页所有字相加除 H×W（求每页"平均字"）
- **GN**：把 C 页平均分 G 份，每份 C/G 页的小册子单独求"平均字"

### Batch Normalization 详解

- **动机**：解决 mini-batch 分布不一致、Internal Covariate Shift（ICS）；缓解梯度消失、加快收敛
- **思想**：进入激活函数前沿通道计算 batch 均值/方差，强迫数据保持均值 0、方差 1 的正态分布（除以 N×H×W）
- **算法**：沿通道算均值→算方差→归一化→加缩放平移变量 γ、β（可学习，保留原有特征）
- **使用位置**：全连接/卷积之后，激活函数之前
- **作用**：允许较大学习率、减弱初始化依赖、数值更稳定、轻微正则化（类似 Dropout）
- **问题**：batch 太小则均值方差不具代表性；batch 太大超内存、训练时间长、梯度方向固定难更新

### LN / IN / GN 要点

- **LN**：同层神经元输入共享均值方差，不依赖 batch size 和序列长度，可用于 batch=1 和 RNN；CNN 上效果不如 BN
- **IN**：针对图像像素，最初用于风格迁移；feature map 各 channel 均值方差影响生成风格，保持图像实例独立
- **GN**：解决 BN 小 batch 差的问题，是 LN 和 IN 的折中；channel 分 G 组组内归一化，与 batch size 无关；适合占显存大的任务（如图像分割）

### 参数差异

- BN、IN、GN：γ、β 都是维度等于通道数 C 的向量
- LN：γ、β 是维度等于 normalized_shape 的矩阵
- BN、IN 可设 momentum / track_running_stats 获得整体数据更准的均值方差；LN、GN 只能算当前 batch 内真实均值方差

## 关联概念

- [[概念_Normalization方法对比]]
- [[概念_Batch_Normalization_批归一化]]

---
> 📎 **物理文献**：[[raw/playbooks/常用 Normalization 方法的总结与思考：BN、LN、IN、GN.md]]