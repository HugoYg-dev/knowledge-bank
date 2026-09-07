---
type: entity
tags:
- Skill/python
- DeepLearning
- Infra/AI
summary: PyTorch 是深度学习框架的事实标准，核心特性为动态计算图、自动微分和丰富 Tensor 操作算子，设计哲学 Python 优先。
sources:
- wiki/sources/PyTorch图像增强方法总结.md
- wiki/sources/PyTorch常用代码段合集.md
- wiki/sources/PyTorch训练代码模板.md
- wiki/sources/Transformer大模型3D可视化_NanoGPT.md
- wiki/sources/Transformer被挑战_Mamba解析与PyTorch复现.md
- wiki/sources/入局AI_Infra系统设计与挑战.md
- wiki/sources/大模型显存计算公式与优化.md
- wiki/sources/手把手教你实现稀疏MoE语言模型.md
updated: '2026-09-07'
---
# 实体：PyTorch

## 简介

PyTorch 是当前 AI 模型训练、推理的深度学习框架事实标准（Meta 开源），开源模型和代码一边倒地使用 PyTorch。

## 核心特性

- **动态计算图**：灵活定义与执行计算逻辑
- **自动微分**：自动计算梯度，无需手写反向传播
- **丰富 Tensor 操作算子**：支持 GPU 加速
- **Python 优先**设计哲学

## 在本文语境中的角色

- 入局 AI Infra 文：类比传统后台的 tRPC/Spring，为 AI 应用屏蔽底层细节；与 Megatron 配合实现模型并行
- PyTorch 常用代码段合集：涵盖基本配置、张量处理、模型定义、数据处理、训练测试的全面 cheat sheet

## 关联

- [[入局AI_Infra系统设计与挑战]]（来源）
- [[PyTorch常用代码段合集]]（来源）
- [[PyTorch训练代码模板]]（来源）
- [[实体_Megatron]]