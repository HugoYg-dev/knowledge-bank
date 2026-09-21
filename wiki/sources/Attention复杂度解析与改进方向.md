---
type: source
tags:
- DeepLearning
- LLM/arch/attention
summary: 系统分析标准自注意力 O(N²d) 时间 / O(N²) 空间复杂度来源与内存 I/O 瓶颈；详解 FlashAttention 1/2/3 的分块计算、在线
  Softmax、异步调度、FP8 低精度优化；简介 Hyena、线性注意力、S2-Attention 等替代方案。
sources:
- raw/articles/Attention复杂度解析与改进方向 - GRITJW - 博客园.md
updated: '2026-07-01'
---
# Attention 复杂度解析与改进方向

## 来源信息

- 标题：Attention复杂度解析与改进方向
- 作者：GRITJW（博客园）
- URL：https://www.cnblogs.com/GlenTt/p/19109565
- 基于全文 ingest

## 核心要点

### 1. 标准自注意力复杂度瓶颈

- **公式**：Attention(Q,K,V) = softmax(QK^T / √d_k) V
- **时间复杂度 O(N²·d)**：
  - Q,K,V 生成：O(Nd²)（3 次矩阵乘法，共 3Nd²）
  - 注意力得分 S = QK^T：O(N²d)——主导项
  - Softmax 归一化：O(N²)
  - 加权求和 P·V：O(N²d)
  - N >> d 时，N² 项主导
- **空间复杂度 O(N²)**：必须存储 N×N 的 S 矩阵和 P 矩阵；反向传播需复用。N=65536 时 FP16 矩阵占 >8GB
- **真正瓶颈是内存 I/O**：GPU 计算快但显存带宽增长慢；标准实现需 S→HBM→读回做 Softmax→P→HBM→读回做 PV，大量"写入-读出"往返导致算力利用率低

### 2. FlashAttention 系列

**FlashAttention-1（2022, Tri Dao）**：
- 核融合（Kernel Fusion）：将所有操作融合为单个 CUDA Kernel，不在 HBM 显式生成 N×N 矩阵
- 分块计算（Tiling）：Q/K/V 按序列长度分块，外层加载 K/V 块到 SRAM，内层加载 Q 块，逐块执行矩阵乘 + Softmax 并累加
- 在线 Softmax（Online Softmax）：维护当前行最大值和归一化累积值，逐块更新，无需完整行
- 效果：空间复杂度从 O(N²) 降至线性；加速 2-4 倍；无近似，精度不变

**FlashAttention-2**：
- 更合理线程块布局和工作划分，充分利用多头并行性
- 在序列维度分片，降低同步开销
- A100 FP16 前向达约 70% 理论峰值；H100 上 540-570 TFLOPs（比初代快近一倍）

**FlashAttention-3（2024）**：
- **异步重叠（Asynchrony）**：Warp 粒度上并行 GEMM 与 Softmax，"乒乓调度"（Ping-Pong Scheduling）；FP16 前向 570→620→640-660 TFLOPs
- **FP8 低精度**：H100 FP8 峰值 1978 TFLOPs vs FP16 989；采用"非相干处理"（incoherent processing）——Q/K 乘随机正交矩阵抑制异常值，量化误差降 2.6 倍；峰值接近 1.2 PFLOPs
- 综合：FP16 达 740 TFLOPs（H100 理论峰值 75%），比前代 1.5-2.0 倍加速

### 3. 其他高效注意力机制

- **Hyena（Hazy Research）**：基于长卷积替代注意力，亚二次复杂度；序列 10 万时比 FlashAttention 快 100 倍；4K 序列时略慢于 FlashAttention
- **线性注意力（Linear Attention）**：如 Performer，用随机特征（Random Fourier Features）将 Softmax 线性化，O(N²)→O(N)；以一定偏差为代价
- **S2-Attention**：硬件感知上下文分片+稀疏注意力；不同头关注不同子集（跨头分片）；128K 长度下比 FlashAttention-2 快 8.79x/15.87x/25.3x；7B 模型推理约 4.5x 加速

### 4. 总结

FlashAttention 不改变模型结构，通过算法与硬件协同（分块、内存复用、Kernel 融合）消除 N×N 矩阵全局读写，将注意力从内存密集型转为计算密集型。其他方法则通过近似/稀疏/替代机制降低理论复杂度。

## 关联概念

- [[概念_自注意力复杂度]]
- [[概念_FlashAttention_快速注意力]]

## 关联实体

- [[实体_FlashAttention]]

---
> 📎 **物理文献**：[[raw/articles/Attention复杂度解析与改进方向 - GRITJW - 博客园.md]]