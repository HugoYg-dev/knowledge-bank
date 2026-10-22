---
type: "source"
tags: ["面试"]
summary: "Daily Dose of DS 经典 LLM 面试题：更换更快 GPU 后 Kernel 执行变快但 Token 生成延迟几乎不变的根因，以及 CUDA Graphs 如何消除 CPU 算子发射开销与权衡"
sources: ["raw/articles/2026-10-15_A-tricky-LLM-interview-question_1a141d112851aa57.md"]
updated: "2026-10-22"
---

# A tricky LLM interview question: GPU Kernel 加速与 Token 延迟瓶颈

## 来源信息

- **来源/主题**：Daily Dose of DS（原邮件主题：A Full Walkthrough on Multimodal Jev）
- **发件人**：Daily Dose of DS <avi@dailydoseofds.com>
- **日期**：2026-10-15（Thu, 15 Oct 2026 23:06:22 +0000）
- **邮件 ID**：1a141d112851aa57（文章 ID: 1a141d112851aa57:3）
- **原文链接**：https://www.dailydoseofds.com/llmops-crash-course-part-1/

## 核心要点

- **反直觉面试谜题**：在模型架构、精度与 Batch Size 均保持一致的前提下，将大语言模型迁移到算力更强的新 GPU 上，虽然 Profiler 显示单个算子 Kernel 的物理执行时间明显缩短，但端到端 Token 逐字生成的生成延迟（Inter-Token Latency）却几乎没有改善。
- **根因剖析——CPU 算子发射开销（Launch Overhead）**：LLM 的前向传播由数十甚至上百个细粒度算子（如 Attention、Matmul、LayerNorm、Softmax/Sampling、数据搬运等）链式构成。在没有 CUDA Graphs 的情况下，CPU 必须依次向 GPU 准备并逐个提交这些 Kernel。
- **Decoding 阶段的空闲间隙（Idle Gaps）**：自回归解码（Token-by-Token Decoding）阶段，每一步仅处理一个新生成的 Token，产生大量微秒级（Microseconds）的极小 Kernel。GPU 往往在几十微秒内就已经执行完毕当前 Kernel，而 CPU 尚未完成下一个 Kernel 的指令封装与发射，导致 GPU 在 Profiler Trace 上暴露出大量等待 CPU 发射指令的空白闲置间隙。
- **CUDA Graphs 破局机制**：CUDA Graphs 在运行时捕获一段可复现的算子执行序列与其拓扑依赖关系。在后续推理重放时，整个调用图作为单一工作单元发射至 GPU（One Graph Launch），彻底消除了算子间 CPU 频繁介入的调度发射延迟。
- **Prefill 与 Decode 阶段的差异特征**：Prefill 阶段由于 Prompt 长度通常较长，计算并行度高，单个 Kernel 的执行时间足够长，GPU 始终处于满负荷状态，CPU 发射开销占比微乎其微；而 Decode 阶段计算极轻且重复高频，CPU 发射开销成为端到端延迟的主要瓶颈。
- **CUDA Graphs 的工程代价与权衡**：CUDA Graphs 并非“无代价的加速开关”。它严格依赖固定的内存地址、算子序列与执行拓扑。由于在线推理服务面临动态 Batch Size 以及混合请求，无法用一张静态图覆盖全部执行路径。主流引擎（如 vLLM、TensorRT-LLM）必须针对常用 Batch Size 捕获多张图（或将未命中尺寸 Padding 补齐），这显著增加了 GPU 显存开销与服务初始冷启动/预热耗时。

## 关键引文

> “Without CUDA Graphs, the CPU prepares and submits these operations individually. Some kernels finish in only a few microseconds. The GPU can complete one kernel before the CPU has submitted the next one. That leaves empty spaces in a profiler trace showing the GPU waiting for its next operation.”

> “CUDA Graphs are not a universal inference speed switch. They trade flexibility and setup cost for lower steady-state launch overhead.”

---
> 📎 **物理文献**：[[raw/articles/2026-10-15_A-tricky-LLM-interview-question_1a141d112851aa57.md]]
