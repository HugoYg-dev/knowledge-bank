---
type: source
tags:
- Infra/platform
summary: 腾讯 QQ 基础架构团队从传统后台工程师视角系统拆解 AI Infra 硬件（GPU 中心化/AI 大型机）、软件（PyTorch/GPU 编程/Python）、训练挑战（显存/模型并行/通信计算重叠）和推理挑战（CUDA
  Graph/KV Cache/流式响应/连续批处理），强调传统 Infra 方法论可无缝迁移到 AI Infra。
sources:
- raw/articles/入局AI Infra：程序员必须了解的AI系统设计与挑战知识.md
updated: '2026-07-01'
---
# 入局AI Infra：程序员必须了解的AI系统设计与挑战知识

## 来源信息

- 标题：入局AI Infra：程序员必须了解的AI系统设计与挑战知识
- 作者：rayrphuang / 腾讯技术工程（公众号）
- URL：https://mp.weixin.qq.com/s?__biz=MjM5ODYwMjI2MA==&mid=2649794657
- 基于全文 ingest

## 核心要点

### 一、硬件演进

#### 1.1 从 CPU 为中心到 GPU 为中心

- 传统 Infra：CPU 核心，多线程+微服务处理高并发逻辑事务，瓶颈在网络 I/O 和 CPU 核心数
- AI Infra：GPU 核心，设计目标从逻辑事务转向高吞吐浮点计算；CPU 多线程被 GPU 并行计算替代，内存被显存替代
- H20 单卡：96GB 显存，44TFlops 单精度，算力和访存带宽是主流 CPU 数十倍甚至数百倍
- 原因：LLM 每次生成一个 token 需读取全量模型参数；DeepSeek-R1-671B-A37B-FP8 生成一个 token：H20 = 37B×1byte÷4000GB/s = 9ms，CPU = 37B×1byte÷64GB/s = 578ms

#### 1.2 从"去IOE"到"AI大型机"

- GPU 算力是 CPU 数百倍，微秒级延时等待造成大量算力损耗，需硬件高度集成
- DeepSeek-R1/QWen3-235B 千亿参数训练需千卡 GPU 集群协同，专用网络互联构建"AI超算"
- 传统 Infra 追求横向扩展（去 IOE），AI Infra 呈现纵向集成（AI 大型机）
- 长期（5年）看必然出现"AI 去 NVIDIA 化"

### 二、软件演进

#### 2.1 深度学习框架

- PyTorch 是事实标准：动态计算图、自动微分、丰富 Tensor 操作算子
- 类比传统后台的 tRPC/Spring 微服务框架

#### 2.2 GPU 编程

- GPU SIMT 架构与传统 CPU 串行思维根本性冲突
- 推荐使用 Triton 编程语言（Python 语法，无需深入 GPU 硬件细节）
- 例：Meta HSTU 模型 hstu_attn 用 PyTorch 组合实现 O(N³)，自定义内核优化到 O(N²)

#### 2.3 Python 编程

- PyTorch 设计哲学 Python 优先
- 随着 KV Cache/MoE/模型并行/自定义 Triton 算子等，模型越来越难脱离 Python 部署

### 三、模型训练的挑战

#### 3.1 存得下

- 显存刺客：中间激活。LLM 中间激活空间复杂度 O(N²)（正比输入长度平方）
- 模型并行：将单个大模型拆分为多个子模块分布到不同 GPU；有按模块划分、按张量划分、混合策略（PyTorch/Megatron）

#### 3.2 算得快

- 通信计算重叠：GPU stream 概念，不同流并行执行，令计算与通信在时间上重叠（类比传统 Infra 的多线程/异步 IO）
- 例：TorchRec 训练流水线

### 四、模型推理的挑战

#### 4.1 降低延时

- CUDA Graph：将多个 GPU 操作转化为 DAG 一次性提交，减少 CPU-GPU 交互开销（类比 Redis Lua 脚本封装多操作）
- KV Cache：缓存 X@W_K 和 X@W_V 已计算结果，空间换时间减少重复计算（几乎所有 LLM 推理框架支持，如 vLLM）
- 流式响应：首 token/首音频帧即返回，改善用户等待体验

#### 4.2 提高吞吐量

- 传统批处理：多输入打包 batch，N 次轻量推理合并为 1 次重量计算（类比 Redis MGet）
- 连续批处理：类似"随时拼车的顺风车"，短请求完成立即释放资源，新请求随时加入（解决长短请求不一致导致 GPU 空闲问题；类比 work stealing 算法）

### 五、结语

AI Infra 面对的工程挑战（计算/存储/通信）大部分是新时代的老问题，传统后台工程师积累的方法论可无缝衔接。

## 关联概念

- [[概念_AI_Native_Infra_AI原生基建]]
- [[概念_KV_Cache_键值缓存]]
- CUDA_Graph
- [[概念_模型并行]]
- [[概念_连续批处理]]
- 通信计算重叠

## 关联实体

- [[实体_vLLM]]
- [[实体_PyTorch]]
- [[实体_Megatron]]

---
> 📎 **物理文献**：[[raw/articles/入局AI Infra：程序员必须了解的AI系统设计与挑战知识.md]]