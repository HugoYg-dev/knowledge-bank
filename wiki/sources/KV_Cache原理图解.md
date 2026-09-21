---
type: source
tags:
- LLM/inference
summary: 图解 KV Cache 原理：Decoder 自回归推理中 K/V 可缓存复用，避免重复计算，但长序列下显存开销巨大
sources:
- raw/articles/大模型推理加速：看图学KV Cache - 知乎.md
updated: '2026-07-01'
---
## 来源信息

- **标题**：大模型推理加速：看图学KV Cache
- **作者**：看图学（知乎，前百度资深算法工程师）
- **URL**：https://zhuanlan.zhihu.com/p/662498827
- **发布平台**：知乎

## 核心要点

### KV Cache 的适用条件

- KV Cache 是 Transformer 推理的**标配加速功能**，`use_cache` 默认 True
- **仅适用于 Decoder 架构**：因 Decoder 有 Causal Mask，已生成的 token 不与后续 token 产生 attention，使得已计算的 K/V 可以缓存复用

### 无 KV Cache 时的冗余分析

- 逐步推导（生成"遥遥领先"4字）：
  - 生成第 k 个 token 时，`Att_k` 只与 `Q_k` 有关
  - `Q_1` 在第2步参与的计算与第1步完全相同（重复计算）
  - `V_2` 的计算仅依赖 `Q_2`，与 `Q_1` 无关
- 结论：当前方式**存在大量冗余计算**

### KV Cache 工作原理

- 每步推理只需输入上一个 token（`x_{k-1}`），计算新的 `Q_k` 得到 `Att_k`
- K 和 V 全程参与计算，因此将每步的 K/V 缓存起来（concat 操作）
- 作者注：称之为"KV Cache"不太准确，"**增量KV计算**"更贴切，因为 K/V 本来就需要全程计算

### 代码实现（GPT-2）

```python
if layer_past is not None:
    past_key, past_value = layer_past
    key = torch.cat((past_key, key), dim=-2)
    value = torch.cat((past_value, value), dim=-2)
```

核心就是一个 `torch.cat` concat 操作。

### 显存代价

- 序列较长时 KV Cache 是"Memory 刺客"
- 估算示例：batch_size=32, head=32, layer=32, dim=4096, seq=2048, float32 → **KV Cache 约占 64GB 显存**
- 公式：`2 × layers × heads × dim × seq_len × batch_size × dtype_bytes`

## 关联

- [[概念_KV_Cache_键值缓存]] — KV Cache 原理、显存估算、适用条件
- [[概念_MLA低秩KV压缩]] — MLA 通过低秩压缩减少 KV Cache 显存
- [[概念_线性注意力与混合注意力]] — Linear Attention 无需 KV Cache 的方案
- [[大模型显存计算公式与优化]]
- [[DeepSeek_MLA矩阵吸收原理]]
- [[MiniMax_vs_Kimi_注意力路线之争]]

---
> 📎 **物理文献**：[[raw/articles/大模型推理加速：看图学KV Cache - 知乎.md]]