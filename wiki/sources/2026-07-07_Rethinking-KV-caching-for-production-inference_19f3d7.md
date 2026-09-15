---
type: source
tags:
- Infra/AI
- LLM/inference
summary: 针对 AI 智能体应用中 62% 的重复 Token 浪费问题，介绍解耦式 KV 缓存架构 LMCache，该架构实现缓存管理与推理引擎进程解耦，并引入
  CacheBlend 算法提速多文档 RAG 场景。
sources:
- raw/articles/Rethinking KV Caching For Production Inference.md
updated: '2026-09-15'
---

# 来源摘要：Rethinking KV caching for production inference

## 来源信息
- **标题**: Rethinking KV caching for production inference
- **来源**: Daily Dose of DS (Avi Chawla)
- **日期**: 2026-07-07
- **原文链接**: [Daily Dose of DS 专栏原文](https://www.dailydoseofds.com/p/rethinking-kv-caching-for-production-inference/) | [LMCache GitHub](https://github.com/lmcache/lmcache)
- **物理文献**: [[raw/articles/Rethinking KV Caching For Production Inference.md]]

## 核心要点
1. **智能体 Token 浪费背景**：斯坦福大学调研表明，AI 智能体在多轮交互中，每次调用发送给模型的 Token 有约 **62%** 是重复的系统 Prompt、工具定义和历史文档。由于 Agent 的每一步交互都是从头输入，即使仅发生微小变化，也需要重新计算所有上下文，导致推理成本暴增。
2. **前缀缓存（Prefix Caching）的物理瓶颈**：传统前缀缓存要求必须是完全一致的字节级前缀匹配。在以下三个实际场景中会导致 100% 缓存失效（Cache Miss）：
   - 多文档 RAG 场景下混合使用已缓存的单文档。
   - 多个文档的排列顺序发生颠倒或更改。
   - 随对话轮数增加，动态增长的会话历史破坏了原有前缀。
3. **解耦式缓存架构（LMCache）**：将 KV 缓存管理工作从推理引擎主进程中彻底剥离出来，作为独立的旁路进程运行。两进程通过共享 GPU 内存进行轻量级 Block ID 通信，从而消除缓存 I/O（I/O 密集型）与模型推理（计算密集型）之间的资源抢占（Contention），避免了传统在进程内压缩缓存导致的 20%+ 推理吞吐降低。
4. **多 GPU 零拷贝与多级并行加载**：LMCache 实现了多 GPU 间对同一内存区域的直接读写（零拷贝共享），并支持 GPU 显存、CPU 内存、本地 SSD 以及云端远程存储的并行多层级异步加载，首字延迟（TTFT）最高可缩短 14 倍，冷启动时间由 3 分钟以上压缩到 30 秒。
5. **CacheBlend 算法突破前缀限制**：LMCache 团队荣获 EuroSys 2025 最佳论文奖的 **CacheBlend** 算法发现，Transformer 模型中绝大部分 Token 主要与其局部上下文相关，仅极少数跨文档边界的 Token 存在强交叉注意力。CacheBlend 通过识别并仅对这些边界 Token 进行**选择性重计算（Selective Recomputation）**，其余大部分 Token 直接复用各自独立的 KV 缓存，在无精度损失前提下为多文档 RAG 查询带来 2~4 倍的加速。

## 关键引文
- > "Making tokens cheaper doesn’t help if most of those tokens shouldn’t exist in the first place."
- > "All the heavy work of actually moving KV tensors between GPU, CPU, and storage happens inside LMCache’s own process. The inference engine doesn’t even notice it’s happening."
- > "CacheBlend exploits this by identifying just those few tokens and selectively recomputing only them. Everything else gets reused as-is from the independent caches."

## 相关实体与概念
- [[wiki/concepts/概念_KV_Cache]]
- [[wiki/concepts/概念_解耦式KV缓存与LMCache]]

---
> 📎 **物理文献**：[[raw/articles/Rethinking KV Caching For Production Inference.md]]
