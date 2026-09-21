---
type: concept
tags:
- RAG/retrieval
summary: S2Dual-perception 是优图 GraphRAG 提出的社区检测算法，同时利用拓扑结构（Structure）和子图语义信息（Semantics）双重感知，生成更高质量的社区总结和发现，克服传统社区检测算法的局限性。
sources:
- wiki/sources/优图RAG技术详解.md
updated: '2026-07-06'
---

# 概念_S2Dual社区检测


## 定义

S2Dual-perception 是优图 GraphRAG 提出的社区检测算法，同时利用拓扑结构（Structure）和子图语义信息（Semantics）双重感知，生成更高质量的社区总结和发现，克服传统社区检测算法的局限性。

## 解决的问题（Leiden 算法缺陷）

- 强制按连接性划分社区，过分依赖图构建质量，限制推理发现和补全能力
- 效率低下：全图遍历单个节点不断计算合并后的质量函数，不适用大规模图

## 双重感知

- **Structure 感知**：通过稀疏邻接矩阵计算 Jaccard 相似度，量化锚节点与社区子图间的拓扑重合度，反映连接强度
- **Semantics 感知**：编码锚节点特征与候选社区子图特征，捕捉语义重合度，反映文本相似度

## 效果

- 相比社区检测 SOTA 算法 Leiden，效率提升近 100%

## 关联

- 相关概念：[[概念_Graph_RAG_知识图谱增强检索]]、[[概念_知识树结构]]
- 来源：[[优图RAG技术详解]]