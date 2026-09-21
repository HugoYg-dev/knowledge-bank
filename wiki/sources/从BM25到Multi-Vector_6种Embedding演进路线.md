---
type: source
tags:
- RAG/embedding
- RAG/retrieval
summary: 从 BM25 到 Multi-Vector 的 6 种 Embedding 演进路线：Sparse/Dense/Quantized/Binary/Matryoshka/Multi-Vector
  对比选型
sources:
- raw/articles/从BM25到Multi-Vector：6种Embedding演进路线.md
updated: '2026-07-01'
---
# 从BM25到Multi-Vector_6种Embedding演进路线

## 核心内容

### 一、Sparse Embedding（关键词式稀疏向量）

- 典型实现：TF-IDF、BM25、SPLADE
- 向量形态：50000+ 维，>95% 位置为 0
- 相似度计算：余弦或点积，仅激活维度参与运算
- 优点：关键词命中时精度极高，可解释性强
- 痛点：只做精确关键词匹配，同义词/句式变化即失效；高维稀疏导致存储索引膨胀
- 案例：新闻版权去重，BM25 检索准确率达 98%，10ms 内返回

### 二、Dense Embedding（语义级稠密向量）

- 典型模型：text-embedding-3-large、BGE、E5-mistral
- 向量形态：256~1536 维，全部非零
- 相似度计算：余弦距离
- 优点：捕捉同义、上下位、跨语言语义
- 痛点：需要 GPU/CPU 做推理，单条 10~100ms；维度越低信息越"挤"
- 案例：SaaS 客服 FAQ 检索，TOP1 命中率从 62% 提升到 89%

### 三、Quantized Embedding（压缩版稠密）

- 压缩手段：float32 → int8/uint8
- 压缩率：75% 体积下降，召回下降 <1%
- 效果：内存×4↓，磁盘×4↓，向量检索 QPS×2↑
- 痛点：必须重新训练或做 Post-Training Quantization；极低比特（4bit）有明显"值域截断"误差
- 案例：电商 2 亿商品向量 2.4TB → 600GB，P99 延迟 18ms → 9ms

### 四、Binary Embedding（极致 0/1 压缩）

- 编码方式：对 float 向量做 sign() 或 ITQ 旋转二值化
- 存储：1bit × dim，比 float32 省 32×
- 效果：计算改 XOR + popcount，CPU 单核可过 1 亿次/秒
- 痛点：汉明距离只能排序，无法得到真实相似度分值；精度平均下降 5~15%
- 案例：安卓相册重复照片清理，3 万张照片 80ms

### 五、Matryoshka (Variable Dimension) 嵌入

- 训练技巧：把 1024 维向量分层加权，前 64 维已含 80% 信息
- 调用方式：同一模型按需截断 dim=64/128/256...
- 效果：一套存储支持"性能↔精度"滑杆；低维阶段 QPS 提升 3~5 倍
- 痛点：必须选用官方 MRL 训练模型，普通模型硬截断会崩；早期维数太短时不同语义容易"挤"在一起
- 案例：初创公司先用 64 维跑 Demo，客户签约后秒切 512 维上线

### 六、Multi-Vector（ColBERT 式后期交互）

- 表征方式：一段文本 → 128 个 128 维向量（每 token 一个）
- 相似度计算：先求每 query token 与 doc token 最大余弦（MaxSim），再求和
- 效果：实现词-词细粒度匹配，长文档召回提升 10~20%；可解释（能高亮哪一句被命中）
- 痛点：索引体积×100↑，需专用压缩（ColBERTv2 残差+量化）；检索阶段计算量远高于单向量
- 案例：律所 50 万判决文书检索，文书阅读时间 15 分钟 → 3 分钟

### 七、选型指南

| 场景关键词 | 首选方案 | 备选 |
|---|---|---|
| 关键词精确匹配 | Sparse | — |
| 通用语义搜索 | Dense | Matryoshka |
| 内存/磁盘告急 | Quantized | Binary |
| 设备端离线快搜 | Binary | — |
| 长文档段落定位 | Multi-Vector | — |

### 八、方案选择步骤

1. 先用 Dense 打 baseline，再决定要不要更复杂
2. 量化/二值化前务必在业务数据上测"召回@K 下降"曲线
3. Multi-Vector 用 ColBERTv2 残差+量化可把 100GB 压到 8GB，保持 95% 精度
4. 最终上线把 Sparse + Dense 做 Hybrid Ranking 往往最稳妥

## 关联

- 相关概念：[[概念_Sparse_Embedding_稀疏向量嵌入]]、[[概念_Dense_Embedding_稠密向量嵌入]]、[[概念_Quantized_Embedding_量化向量嵌入]]、[[概念_Binary_Embedding_二进制向量嵌入]]、[[概念_Matryoshka表示学习]]、[[概念_ColBERT_多向量延迟交互检索]]、[[概念_BM25_最佳匹配25算法]]、[[概念_Embedding与向量检索]]
- 实体：[[实体_ColBERT]]

---
> 📎 **物理文献**：[[raw/articles/从BM25到Multi-Vector：6种Embedding演进路线.md]]