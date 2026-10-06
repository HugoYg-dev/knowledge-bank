---
type: "entity"
tags:
  - "LLM/arch"
  - "AI-Agent/UI"
summary: "全球科技巨头与 AI 核心创新机构，主导 LLaMA 开源大模型家族、PyTorch 深度学习框架、FAISS 向量检索库、REFRAG 向量压缩架构与 Muse 个人智能体生态。"
sources:
  - "wiki/sources/Meta复盘Muse_Agent怎么才能像一个人长期存在.md"
  - "wiki/sources/2026-03-24_RAG-vs-MetaAI's-REFRAG_19d21b.md"
updated: "2026-10-06"
---

# 实体：Meta

## 机构概述

**Meta**（原 Facebook，旗下涵盖 Meta AI 与 FAIR 实验室）是全球人工智能与开源基础设施的核心领导者之一。创始人兼首席执行官为马克·扎克伯格（Mark Zuckerberg）。公司在 AI 领域的战略鲜明：一方面通过开放开源大模型权重（LLaMA 家族）与基础算力工具（PyTorch、FAISS）构建全球开发者生态，另一方面将前沿 AI 技术与社交网络、即时通信（WhatsApp、Messenger）及个人智能体（Muse）深度结合。

## 核心开源贡献与技术创新

1. **LLaMA 系列开源大语言模型**：
   - 从 LLaMA-1 到 LLaMA-3.x 系列，奠定了全球开源大语言模型的基准架构，催生了整个开源大模型微调与量化繁荣生态。
2. **AI Infra 与深度学习底座**：
   - **PyTorch**：全球事实标准的深度学习框架；
   - **[[entities/实体_Faiss|Faiss]]**：业界使用最广泛的海量向量高维近似最近邻（ANN）检索库。
3. **视觉与多模态基础模型**：
   - **[[entities/实体_SAM|SAM]] (Segment Anything Model)**：计算机视觉领域开创性的通用图像分割基础模型。
4. **高效检索与 RAG 架构革新**：
   - **REFRAG 架构**：在 [[wiki/sources/2026-03-24_RAG-vs-MetaAI's-REFRAG_19d21b.md|REFRAG]] 中，Meta AI 提出在向量层面直接压缩与过滤 Chunks 的新思路，实现 30x 首字生成提速（TTFT）与 16x 上下文扩展。

## 智能体战略与端到端隐私

在个人智能体（Personal Agent）领域，Meta 推出旗舰产品 [[entities/实体_Muse|Muse]]，探索“长程在线、替用户自主办事”的系统工程：
- **双安全域隔离**：在专属虚拟机中划定 Agent 运行单元与宿主哨兵（Sentinel）两个互不信任域；
- **机密虚拟机与隐私安全**：引入 Signal 创始人 Moxie Marlinspike 领衔机密虚拟机研发，延续 WhatsApp 端到端加密原则，确保连云端平台本身也无法接触用户私密数据。

## 关联页面

- **核心产品/项目**：[[entities/实体_Muse|实体_Muse]]、[[entities/实体_Faiss|实体_Faiss]]、[[entities/实体_SAM|实体_SAM]]
- **核心概念**：[[concepts/概念_Personal_Agent_个人智能体|概念_Personal_Agent_个人智能体]]、[[concepts/概念_REFRAG_RAG压缩与过滤|概念_REFRAG_RAG压缩与过滤]]

## 来源与参考

- [[wiki/sources/Meta复盘Muse_Agent怎么才能像一个人长期存在.md]]
- [[wiki/sources/2026-03-24_RAG-vs-MetaAI's-REFRAG_19d21b.md]]
