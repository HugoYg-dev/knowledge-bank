---
type: "concept"
tags:
  - Infra/gpu
  - Infra/AI
  - LLM/inference
summary: "Roofline 模型是量化评估硬件算力峰值与内存带宽瓶颈的经典性能模型。通过算力强度（FLOPs/Byte）与芯片硬件平衡阈值的对比，划分计算密集与内存带宽受限区域，为大模型 Prefill 与 Decode 阶段的系统优化提供统一指导"
sources:
  - wiki/sources/How_a_GPU_Actually_Works.md
updated: "2026-09-15"
---

# 概念：Roofline 模型与算力强度

## 定义与数学模型

Roofline 模型是由加州大学伯克利分校提出的经典计算机体系结构性能评估与性能调优模型。该模型将计算应用在给定硬件平台上的可达性能（Attainable Performance）直观绑定于两个物理上限：**芯片峰值算力（Peak Compute Performance）** 与 **内存访问带宽（Peak Memory Bandwidth）**。

### 核心公式

1. **算力强度（Arithmetic Intensity / Work per Byte）**：
   衡量程序在执行过程中对内存数据的复用效率，定义为执行的浮点运算总次数与从主存（如 GPU HBM/VRAM）搬运的字节总数之比：
   $$I = \frac{\text{Total Floating Point Operations (FLOPs)}}{\text{Total Memory Traffic (Bytes)}} \quad (\text{ops/byte})$$

2. **硬件平衡阈值（Machine Balance / Break-even Point）**：
   由硬件物理极限决定的临界算力强度，即芯片最大算力与最大访存带宽的商：
   $$I^* = \frac{P_{\text{peak}} \text{ (FLOP/s)}}{B_{\text{peak}} \text{ (Bytes/s)}} \quad (\text{ops/byte})$$

3. **可达性能理论上限（Attainable Performance Roofline）**：
   $$P = \min\left(P_{\text{peak}}, \; I \times B_{\text{peak}}\right)$$

---

## 性能区域划分与瓶颈诊断

```text
 可达性能 (FLOP/s)
    ^
P_peak |-------------------\========================= (算力峰值天花板 Compute-bound)
       |                  / :
       |                 /  :
       |                /   :
       |               /    :
       |              /     :
       |             /      :
       |            /       :
       |           /        :
       |          /         :
       +---------/----------+-------------------------> 算力强度 I (ops/byte)
             Memory-bound   I* (平衡拐点)  Compute-bound
```

### 1. 内存带宽受限区（Memory-Bound Region，当 $I < I^*$ 时）
- **物理表现**：程序的算力强度低于芯片的硬件平衡阈值。计算单元在大部分时钟周期内处于等待数据从主存搬运的状态（Stall），实际算力受制于倾斜的“屋檐”：$P = I \times B_{\text{peak}} < P_{\text{peak}}$。
- **优化对策**：增加计算核心或升级浮点单元不会带来任何性能提升。必须通过**提升算力强度**（如增大 Batch Size、分块 Tiling）或**减少数据搬运量**（如算子融合、低精度量化）来逼近或越过平衡线。

### 2. 计算峰值受限区（Compute-Bound Region，当 $I \ge I^*$ 时）
- **物理表现**：算力强度高于平衡点，主存带宽已能充分满足计算流水线需求，性能触达水平的“天花板”：$P = P_{\text{peak}}$。
- **优化对策**：进一步提升访存带宽已无收益，性能优化只能依靠算法逻辑精简、指令级并行优化或采用更高效的专用矩阵计算单元（如 Tensor Core）。

### 3. 硬件演进中的算存鸿沟加剧
在现代 AI 加速芯片演进中，浮点算力的扩张速度远高于内存总线带宽的物理扩张速度：
- 以 [[entities/实体_NVIDIA|NVIDIA]] **H100 SXM5** 为例：Dense BF16 峰值约 989 TFLOPS，HBM3 显存带宽约 3.35 TB/s，平衡阈值约为 **295 ops/byte**；
- 针对显存瓶颈升级的 **H200**：保持 989 TFLOPS 算力不变，将显存升级为 HBM3e（带宽增至 4.8 TB/s），将平衡阈值主动拉低至 **206 ops/byte**。降低平衡阈值使得更多中等复杂度的计算能够脱离 Memory-bound 泥潭，直接享受更高的硬件算力释放。

---

## 大模型推理两阶段在 Roofline 上的极端对立

大语言模型（LLM）推理天然具备 Prefill 与 Decode 两个迥异的阶段（参见 [[concepts/概念_LLM推理两阶段|概念_LLM推理两阶段]]），两者在 Roofline 模型上处于完全相反的区间：

| 阶段 | 典型算力强度 | 瓶颈归属 | 物理极限成因 |
| :--- | :--- | :--- | :--- |
| **自回归解码（Decode，Batch=1）** | **~1 op/byte** | **极端 Memory-bound** | 每产生 1 个 token 需完整加载全模型权重（以 70B 模型 16-bit 为例需加载 140GB），每个权重仅执行 1 次乘法与 1 次加法（2 次运算），总运算 140 GFLOPs。算力强度比 H100 平衡点低约 300 倍，理论单 token 耗时下限被锁死在 $140\text{GB} / 3.3\text{TB/s} \approx 42\text{ms}$（~24 tok/s）。 |
| **预填充阶段（Prefill）** | **$\gg 300$ ops/byte** | **Compute-bound** | 一次性并行处理 Prompt 内的 $N$ 个 tokens，单次加载的模型权重被 $N$ 个向量并行复用，算力强度随序列长度线性倍增，直接跨过硬件平衡线进入算力饱和区。 |

---

## 统一系统优化技术的 Roofline 投影

现代 AI 推理工程的所有性能技巧，在 Roofline 视角下均可归为两大类矢量移动：

1. **水平右移（提升 $I$，将应用从 Memory-bound 推向 Compute-bound）**：
   - **连续批处理（[[concepts/概念_连续批处理|Continuous Batching]]）**：单次权重搬运为 $B$ 个并发请求共同使用，将 Decode 的算力强度提升 $B$ 倍。在 16-bit 精度下，需达约 300 并发才能使 70B 模型的自回归生成触达计算边界；
   - **分块复用（SRAM Tiling）**：将矩阵分块载入片上 Shared Memory 进行高阶交叉运算。

2. **垂直抬升 / 削减分母（直接减少从 HBM 传输的 Bytes）**：
   - **低精度量化（Quantization）**：将模型权重从 FP16（2 字节）压缩为 INT8（1 字节）或 INT4（0.5 字节），直接将分母 Memory Traffic 削减 50%–75%，使单请求生成延迟理论下限直接压缩至 $21\text{ms}$（~48 tok/s）或更快；
   - **算子融合（Operator Fusion）**：将连续 Element-wise 算子串联执行，中间变量驻留在片上寄存器，避免往返写入与读取全局显存；
   - **[[concepts/概念_FlashAttention|FlashAttention]]**：利用在线 Softmax 与 SRAM Tiling，避免在全局显存 HBM 中物化庞大的 $N \times N$ 注意力矩阵；
   - **连续合并访存（Memory Coalescing）**：对齐 Warp 线程访问的物理地址，避免非对齐访存造成的有效带宽折损。

---

## 关联页面

- [[sources/How_a_GPU_Actually_Works|How_a_GPU_Actually_Works]]（来源）
- [[concepts/概念_AI硬件加速芯片架构|概念_AI硬件加速芯片架构]]
- [[concepts/概念_LLM推理两阶段|概念_LLM推理两阶段]]
- [[concepts/概念_连续批处理|概念_连续批处理]]
- [[concepts/概念_FlashAttention|概念_FlashAttention]]
- [[concepts/概念_KV_Cache|概念_KV_Cache]]
- [[entities/实体_NVIDIA|实体_NVIDIA]]
