---
type: "source"
tags: ["Infra/gpu", "Infra/serving", "LLM/inference"]
summary: "深入剖析现代 GPU 底层硬件架构（SIMT、Warp 调度、多级存储阶梯）与算力强度/Roofline 性能模型，揭示 LLM 自回归生成受限于内存带宽的根本原因，并将批处理、算子融合、SRAM 分块及量化等优化统一归纳为算存比移动法则"
sources: ["raw/articles/How a GPU Actually Works.md"]
updated: "2026-09-15"
---

# 来源摘要：How a GPU Actually Works

## 来源元信息
- **标题**：How a GPU Actually Works
- **作者**：Avi Chawla (Daily Dose of Data Science)
- **发布日期**：2026-08-18
- **原文链接**：https://www.dailydoseofds.com/p/how-a-gpu-actually-works/
- **上游物理归档**：`raw/articles/How a GPU Actually Works.md`

---

## 核心要点提炼

1. **核心不对称性与算力-带宽鸿沟（The Fundamental Asymmetry）**：
   - 现代硬件体系中，“执行算术运算极其廉价，而搬运参与运算的数据极其昂贵”。
   - 过去几代硬件加速器中，浮点算力峰值的增长速度数倍于内存带宽增长。每一代新芯片都能执行多得多的计算，但获取数据的通道拓宽十分有限，导致算存失衡随硬件演进持续加剧。
   - 任何系统级优化技术的本质，都是为了在每次遍历内存总线时榨取更多的有效计算。

2. **SIMT 架构与零成本 Warp 延迟掩盖机制（Latency Hiding）**：
   - 与 CPU 耗费大量晶体管用于单线程乱序执行、复杂分支预测及深层缓存不同，GPU 针对“数百万数据元素执行相同指令”的图形与张量特征，大幅削减控制逻辑，将芯片面积全力投入算术逻辑单元（ALU），构成 [[concepts/概念_AI硬件加速芯片架构|SIMT（单指令多线程）架构]]。
   - 硬件以 32 个线程组成的 **Warp** 为不可分割的调度原子，共享单一指令发射器。若 Warp 内部存在数据驱动的分支分歧（Warp Divergence），不同路径必须串行执行并让非活动线程空转，产生执行惩罚。
   - **GPU 并不缩短访存等待，而是通过调度使等待隐形**：GPU 在片上常驻远超并发执行容量的数十个 Warp，当当前执行的 Warp 发起访存请求进入等待（Stall）时，硬件调度器零延迟（单周期）切换至已就绪的其他 Warp 执行。

3. **存储金字塔阶梯与 SM 物理隔离设计（The Memory Ladder）**：
   - GPU 存储体系由近及远、由快到慢分为四层：
     1. **线程级私有寄存器（Register File）**：容量异常庞大（全芯片总和接近 L2 Cache），专门用于停放数万个半完成线程的状态，实现无开销上下文切换；
     2. **片上暂存/共享内存（Shared Memory / L1 Cache）**：位于每个流式多处理器（SM）内部，低延迟且由开发者显式控制生命周期；
     3. **全芯片共享 L2 缓存**：位于所有 SM 下方，由硬件自动管理；
     4. **全局主存（HBM / VRAM）**：位于芯片物理封装外部，通过总线连接，容量达数十至上百 GB，但访存延迟最高且带宽成为全局硬上限。
   - 数据留在 SM 片上则成本低廉；一旦需要跨 SM 共享或回写 HBM，数据传输开销呈数量级上升。

4. **算力强度与 Roofline 性能模型平衡点（Arithmetic Intensity & Roofline Model）**：
   - 算力强度（Arithmetic Intensity）定义为每从主存读取 1 字节所执行的浮点运算次数（FLOPs / Byte）。
   - 硬件平衡分界点由 $\text{Peak FLOPS} / \text{Memory Bandwidth}$ 决定。以 [[entities/实体_NVIDIA|NVIDIA]] H100 SXM5（密集 BF16 989 TFLOPS，3.35 TB/s 显存带宽）为例，平衡阈值约为 **295 ops/byte**；H200 在算力不变的情况下将带宽增至 4.8 TB/s，平衡阈值降至 **206 ops/byte**。
   - 在 [[concepts/概念_Roofline模型与算力强度|Roofline 模型]] 中，低于平衡点即为**内存带宽受限（Memory-bound）**，增加算力无济于事；高于平衡点才为**计算受限（Compute-bound）**。

5. **大模型自回归生成的极端访存瓶颈（The 1 Op/Byte Dilemma）**：
   - 在 [[concepts/概念_LLM推理两阶段|自回归解码（Decode）]] 阶段，每生成 1 个 token 必须对全模型权重进行一次完整的前向加载。
   - 以 70B 参数模型在 16-bit（BF16）精度为例：模型权重占用 140 GB；产生 1 个 token 时每个参数执行 1 次乘法与 1 次加法（共 2 次运算），总计算量约为 1400 亿次浮点运算（140 GFLOPs）。
   - 运算量与访存量之比为 $140\text{ GFLOPs} / 140\text{ GB} = 1\text{ op/byte}$，比硬件平衡线（~300 ops/byte）**低整整 300 倍**。
   - 理论生成延迟下限仅取决于权重加载时间：$140\text{ GB} / 3300\text{ GB/s} \approx 42\text{ ms/token}$（即吞吐硬上限约 24 tokens/s）。相反，Prefill 阶段一次性并行计算 Prompt 所有 tokens，权重在序列长度上完全复用，天然落在计算受限区。

6. **优化技术的统一归类（算存比移动的两大途径）**：
   - **提升每次读取的计算收益（Increase Work per Fetch）**：
     - **批处理（[[concepts/概念_连续批处理|Batching / Continuous Batching]]）**：并发处理多个请求共享单次权重加载，需约 300 个并发序列才能将自回归解码推入计算受限区；
     - **分块计算（Tiling）**：将数据切块加载至片上 Shared Memory 进行高阶复用。
   - **直接减少访存搬运字节（Decrease Bytes Fetched）**：
     - **算子融合（Operator Fusion）**：将连续 Element-wise 操作串联，中间激活值留在寄存器中，避免多次往返 HBM；
     - **[[concepts/概念_FlashAttention|FlashAttention]]**：利用 SRAM Tiling 和在线 Softmax，避免将 $N \times N$ 注意力矩阵写入和重读 HBM；
     - **低精度量化（Quantization）**：将权重从 16-bit 降至 8-bit 或 4-bit，直接将每次生成需搬运的显存字节削减 50%–75%，使 70B 模型的单序列生成上限从 24 tok/s 提升至 48 tok/s 甚至更高；
     - **连续合并访存（Memory Coalescing）**：保证 Warp 内 32 个线程访问连续内存地址，避免非对齐或跨步访问造成高达 8x 的无谓带宽放大浪费。

7. **三态性能诊断法则（Diagnostic Triad）与调度开销**：
   - **Memory-bound**：显存带宽打满，计算单元空闲。优化手段为增大 Batch Size、量化、算子融合与紧凑数据排布；
   - **Compute-bound**：计算单元接近峰值，带宽充足。优化方向为更低精度算术单元（如 FP8 Tensor Core）、优化算法或升级硬件；
   - **Overhead-bound**：算力与带宽利用率均极低。通常由于 CPU 发射小算子（Kernel Launch）的调度开销超过了 GPU 执行时间，需通过 CUDA Graph 或算子合并解决。

---

## 关键引文

> "Doing arithmetic is cheap. Fetching the numbers to do arithmetic on is expensive."

> "A GPU does not make waiting shorter. It makes waiting invisible."

> "140 billion operations funded by 140 GB of traffic, which is 1 operation per byte. The break-even threshold was around 300. Serving a single request puts you roughly three hundred times below it."

> "Divide the chip's peak arithmetic rate by its peak memory bandwidth. For a current data center GPU running 16-bit precision, that number is around 300 operations per byte."

---

## 关联页面与实体图谱

- **核心概念**：
  - [[concepts/概念_AI硬件加速芯片架构|概念_AI硬件加速芯片架构]]（GPU SIMT 结构与存储阶梯体系）
  - [[concepts/概念_Roofline模型与算力强度|概念_Roofline模型与算力强度]]（算力强度定义与平衡分界点）
  - [[concepts/概念_LLM推理两阶段|概念_LLM推理两阶段]]（Prefill 计算受限 vs Decode 显存带宽受限机制）
  - [[concepts/概念_连续批处理|概念_连续批处理]]（通过高并发请求重叠提升 Work per Byte）
  - [[concepts/概念_FlashAttention|概念_FlashAttention]]（片上 SRAM Tiling 避免中间注意力矩阵回写 HBM）
  - [[concepts/概念_KV_Cache|概念_KV_Cache]]（推理阶段显存与访存的主要动态来源）
- **核心实体**：
  - [[entities/实体_NVIDIA|实体_NVIDIA]]（H100 SXM5 与 H200 硬件性能规格与算存平衡点演进）

---

> 📎 **物理文献**：[[raw/articles/How a GPU Actually Works.md]]
