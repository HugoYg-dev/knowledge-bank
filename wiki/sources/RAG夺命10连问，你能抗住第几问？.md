---
type: "source"
tags: ["面试", "RAG/retrieval"]
summary: "全面总结大厂大模型应用方向高频考点：RAG核心原理、与SFT选型对比、切块与检索优化、评估指标体系、高阶纠错机制及Spring AI Alibaba工程落地方案"
sources: ["raw/articles/RAG夺命10连问，你能抗住第几问？.md"]
updated: "2026-09-19"
---

# RAG夺命10连问，你能抗住第几问？

## 来源信息
- **标题**：RAG夺命10连问，你能抗住第几问？
- **作者**：苏三说技术
- **发布时间**：2026-04-24
- **原始链接**：https://www.cnblogs.com/12lisu/p/19921242

## 核心要点
1. **RAG 核心定位与痛点解决**：通过外部知识库检索注入上下文，解决大模型知识时效性滞后、事实性幻觉以及企业私有数据安全隔离三大核心痛点。
2. **RAG 与微调（SFT）选型权衡**：
   - 知识频繁变动、重溯源、低成本优先采用 RAG；
   - 领域风格对齐、结构化格式约束、毫秒级推理优先采用 SFT；
   - 生产最佳实践为“SFT 对齐交互风格 + RAG 注入实时动态知识”。
3. **分块策略（Chunking）与召回优化**：
   - 推荐分块大小 512~1024 字符，重叠度 10%~20%（100~200 字符）；
   - 召回优化组合拳：混合检索（BM25 稀疏匹配 + 稠密向量语义）、Query 重写/HyDE 假设文档扩展、Cross-Encoder 二次重排序（Rerank）。
4. **评估指标体系（RAG Triad）**：
   - 检索侧考量 Recall@K、MRR、NDCG；
   - 生成侧基于 Ragas 体系评估忠实度（Faithfulness，防幻觉）、答案相关性（Answer Relevancy）与上下文召回率（Context Recall）。
5. **高阶反思与纠错机制**：
   - **Self-RAG**：通过输出反思 Token 自主裁决检索必要性与结果质量；
   - **CRAG（Corrective RAG）**：对低置信度检索触发网络搜索（Web Search Fallback）或图谱纠错；
   - **Graph RAG**：结合知识图谱实体关系三元组，突破传统 Chunk 向量检索在多跳关系推理上的局限。
6. **企业级工程落地**：结合 Spring AI Alibaba 框架，实现基于 Milvus / DashScope Embedding 的企业私有知识库高并发问答与监控流水线。

---
> 📎 **物理文献**：[[raw/articles/RAG夺命10连问，你能抗住第几问？.md]]
