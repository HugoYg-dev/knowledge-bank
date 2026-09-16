---
type: source
tags:
- Infra/serving
summary: 本文探讨了在模型训练与生产伺服部署之间存在的分歧，分析了开放神经网络交换（ONNX）作为跨框架的中间表示的优势，详述了 ONNX Runtime（ORT）的各种执行引擎加速和图优化机制，并客观归纳了在使用
  ONNX 时面临的算子转换不全、混合精度漂移等挑战。
sources:
- raw/articles/2026-05-25_Build-portable-ML-models-with-ONNX_19e60c.md
updated: '2026-08-04'
---

# Build portable ML models with ONNX

## 来源信息
- **来源**: Daily Dose of DS
- **作者**: Avi Chawla
- **原始链接**: [Build portable ML models with ONNX](https://www.dailydoseofds.com/mlops-crash-course-part-10/)
- **归档物理文献**: [[raw/articles/2026-05-25_Build-portable-ML-models-with-ONNX_19e60c.md]]

## 核心要点
1. **训练与伺服部署的脱节**：大多数团队使用 PyTorch 或 TensorFlow 训练模型，但生产环境注重速度、可移植性与稳定性。不同的运行目标（C++ 服务、移动端、GPU 优化运行环境、CPU 独占生产环境）导致每次部署都变成高度定制且复杂的工程问题。
2. **ONNX 作为中立中间表示**：ONNX（Open Neural Network Exchange，开放神经网络交换）提供了一种与框架无关的、通用的计算图表征标准。它包含了标准化算子（Operators）、显式张量形状、元数据，并把所有权重参数烘焙（Baked）在内。
3. **算子标准化（Operator Standardization）的重要性**：不同的框架对同一个数学算子有自己的底层实现。ONNX 定义了通用的算子集合（Opset），这使得导出器能够将各种特定框架的算子映射到统一的标准词汇表中。
4. **ONNX Runtime (ORT) 加速执行**：ONNX 只是描述图的静态格式，而 ORT 是实际的执行引擎。ORT 加载静态图，并在运行时自动应用图级别优化（如算子融合）、根据硬件条件将子图切分并分发到不同的执行提供商（Execution Providers，如 CUDA、TensorRT），实现高效执行。
5. **实际限制与痛点挑战**：ONNX 也不是万灵药。实际部署上面临算子覆盖不完全、硬件目标上的执行提供商覆盖差异、混合精度计算带来的微小数值漂移，以及对自定义算子需要额外定制工程支持等限制。

## 关键引文
- "Most ML teams train models in PyTorch or TensorFlow, but production systems don’t care about it. They care about speed, portability, and stability. This disconnect between training and serving is where most deployment headaches begin."
- "ONNX acts as a framework-agnostic intermediate representation that sits between training and deployment. An ONNX model is essentially a saved computation graph with standardized operators, explicit tensor shapes, metadata, and all weights baked in."
- "ONNX Runtime (ORT) is the execution engine that turns that format into fast inference. Under the hood, ORT loads the ONNX graph, applies graph-level optimizations, partitions the graph across hardware backends, and executes each subgraph efficiently."
- "ONNX simplifies deployment significantly, but it doesn’t remove the need for careful validation before going to production."

## 联动概念
- [[wiki/concepts/概念_ONNX模型跨平台部署]]

> 📎 **物理文献**：[[raw/articles/2026-05-25_Build-portable-ML-models-with-ONNX_19e60c.md]]
