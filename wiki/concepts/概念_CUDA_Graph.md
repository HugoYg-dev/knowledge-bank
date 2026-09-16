---
type: concept
tags:
- Infra/serving
- LLM/inference
summary: CUDA Graph 将多个 GPU 操作（内核启动、内存拷贝、计算）转化为有向无环图（DAG）一次性提交给 GPU 执行，由 GPU 自身管理依赖和执行顺序，减少
  CPU-GPU 交互开销，降低模型推理延时。
sources:
- wiki/sources/入局AI_Infra系统设计与挑战.md
updated: '2026-06-29'
---


# 概念：CUDA Graph

## 定义

在 GPU 编程中，CPU 通过 CUDA API 向 GPU 提交任务存在内核启动、通信和调度等非核心开销。模型推理需执行大量重复 GPU 操作，这些开销成倍放大。CUDA Graph 技术将多个 GPU 操作转化为一个有向无环图（DAG），一次性提交整个图到 GPU 执行，由 GPU 管理操作间依赖和执行顺序，从而减少交互开销。

## 类比

传统后台服务中 Redis Lua 脚本封装多个 Redis 操作一次提交减少网络开销。

## 关联

- [[入局AI_Infra系统设计与挑战]]（来源）