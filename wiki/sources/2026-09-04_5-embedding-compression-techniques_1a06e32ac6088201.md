---
type: "source"
tags:
  - "RAG/embedding"
summary: "系统梳理 5 种 Embedding 向量压缩技术：PCA 投影、MRL 前缀截断、SQ 标量量化、BQ 二值量化与 PQ 乘积量化，以及 Over-fetch 粗排配合 Rescoring 精排的两阶段检索范式"
sources:
  - "raw/articles/2026-09-04_5-embedding-compression-techniques_1a06e32ac6088201.md"
updated: "2026-09-15"
---

# 5 embedding compression techniques

- **来源**: Daily Dose of DS
- **作者**: Avi Chawla (`avi@dailydoseofds.com`)
- **原文链接**: [Daily Dose of DS - Building RAG Systems Crash Course](https://www.dailydoseofds.com/a-crash-course-on-building-rag-systems-part-1-with-implementations/)
- **发布日期**: 2026-09-04
- **邮件/文章标识**: `1a06e32ac6088201:2`

---

## 核心要点

1. **向量检索的真实显存与容量瓶颈**：
   - 工业级海量检索中，以 1,000 万个（10M）1536 维向量为例，不同数值精度的裸向量载荷差异悬殊：
     - Float32：62 GB
     - Int8：15 GB（约 4x 缩减）
     - Packed Bits（二值量化）：2 GB（约 32x 缩减）
   - 除裸向量外，基于内存的向量系统还必须承载 ANN 索引结构（如 HNSW 图拓扑）、字段元数据（Metadata）与系统分配器碎片，实际内存膨胀率远高于纯向量载荷。
2. **向量压缩的两大正交优化维度**：
   - **降低存储维度（Dimensions stored）**：直接减少向量的特征分量数量（如 PCA、MRL）。
   - **降低单维位宽（Bits used per dimension）**：降低表示每个特征值的比特数（如 SQ、BQ）。
3. **5 大核心向量压缩技术机制**：
   - **[[concepts/概念_PCA_主成分分析|PCA（主成分分析）]]**：训练后降维投影。基于代表性样本集拟合方差最大的前 $k$ 个主成分方向，将原向量映射到低维空间；要求对库内向量与查询 query 应用完全一致的投影变换矩阵。
   - **[[concepts/概念_MRL套娃表示学习|MRL（Matryoshka Representation Learning）]]**：训练期前置优化目标。在模型训练阶段强制前缀维度（如前 $n$ 维）独立保持高区分度，推理时无需二次微调即可任意按需截断维度（例如 OpenAI `text-embedding-3-large` 截断至 256 维在 MTEB 评测中仍超越 1536 维的 `text-embedding-ada-002`）。
   - **[[concepts/概念_Quantized_Embedding_量化向量嵌入|SQ（标量量化，Scalar Quantization）]]**：保持维度不变，将 Float32 线性离散化映射为 Int8，取得 4x 显存缩减，仅需附加极小量的 scale 与 offset 比例元数据。
   - **[[concepts/概念_Binary_Embedding_二进制向量嵌入|BQ（二值量化，Binary Quantization）]]**：保持维度不变，将连续数值按符号二值化为 1 个 bit（正为 1，负为 0），实现 32x 极致显存压缩；向量点积相似度退化为硬件级极速指令（按位异或 XOR + 汉明权重 popcount）。核心代价是丢失向量幅度（magnitude）信息。
   - **PQ（乘积量化，Product Quantization）**：子空间切分聚类编码。将高维向量切分为若干子向量，每个子向量用其所属的最近聚类中心（Centroid）ID 进行紧凑编码；检索时通过预计算的距离查找表（Lookup Table）进行快速近似距离评估。
4. **两阶段检索范式（Over-fetch 粗召回 + Rescoring 精排）**：
   - 压缩向量无需直接决定最终精确排序。工程上普遍采用两阶段架构：在压缩索引中超额检索候选集（Over-fetch，如粗排召回 Top 100），随后使用完整未压缩的高精度向量进行重打分（Rescore，精排输出 Top 10）。
   - 该范式不仅消除了低位宽量化（特别是 BQ）带来的精度损失，同时享有海量向量下的极低显存与极高吞吐；但需注意，粗排漏检的文档无法被精排重排召回。
5. **正交技术串联组合**：
   - 维度压缩与位宽压缩属于两个正交阶段，可协同生效。例如先通过 MRL 将 1536 维截断至 256 维，再进行 Int8 标量量化或二值量化，实现复合级存储与延迟优化。

---

## 5 种 Embedding 压缩技术对比矩阵

| 技术分类 | 代表方法 | 介入阶段 | 压缩倍率 (典型) | 核心计算特征 | 适用场景与主要权衡 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **减少维度** | **[[concepts/概念_PCA_主成分分析|PCA]]** | 训练后 (Post-train) | 2x–8x | 矩阵正交变换投影，计算线性内积 | 普适性好，但对非线性语义流形有损，Query 必须同步投影 |
| **减少维度** | **[[concepts/概念_MRL套娃表示学习|MRL]]** | 训练期 (Pre-train/FT) | 2x–6x | 原生支持前缀截断，无额外推理开销 | 必须在训练目标中显式定义，代表模型为 OpenAI `text-embedding-3` |
| **减少位宽** | **[[concepts/概念_Quantized_Embedding_量化向量嵌入|SQ (标量量化)]]** | 索引构建期 | 4x (FP32 → Int8) | 线性量化映射 + 比例还原 | 精度损失极小（通常 <1%），广泛支持（Milvus/Qdrant/Faiss） |
| **减少位宽** | **[[concepts/概念_Binary_Embedding_二进制向量嵌入|BQ (二值量化)]]** | 索引构建期 | 32x (FP32 → 1bit) | 极速硬件位运算（XOR + popcount） | 丢失幅度信息，必须配合两阶段 Over-fetch + Rescore |
| **码本量化** | **PQ (乘积量化)** | 索引构建期 | 8x–32x | 子空间切分 + 聚类 ID 编码 + 查表距离 | 适合千万至亿级海量向量，聚类训练开销高，有近似误差 |

---

## 关联

- **相关概念**: [[concepts/概念_PCA_主成分分析|概念_主成分分析_PCA]]、[[concepts/概念_MRL套娃表示学习|概念_MRL套娃表示学习]]、[[concepts/概念_Quantized_Embedding_量化向量嵌入|概念_Quantized_Embedding]]、[[concepts/概念_Binary_Embedding_二进制向量嵌入|概念_Binary_Embedding]]、[[concepts/概念_向量量化|概念_向量量化]]
- **相关来源**: [[wiki/sources/从BM25到Multi-Vector_6种Embedding演进路线.md]]、[[wiki/sources/ES企业AI搜索实践.md]]、[[wiki/sources/向量数据库原理与应用全解析.md]]

---
> 📎 **物理文献**：[[raw/articles/2026-09-04_5-embedding-compression-techniques_1a06e32ac6088201.md]]
