---
type: source
tags:
- LLM/arch/attention
summary: 通过逐步图解说明 DeepSeek MLA 矩阵吸收的工程优化原理：将 K/V 升维矩阵吸收进 Q，使注意力计算时 K/V 不含头信息，利用广播减少内存访问
sources:
- raw/articles/deepseek MLA 矩阵吸收浅谈 - 知乎.md
updated: '2026-07-01'
---
## 来源信息

- **标题**：deepseek MLA 矩阵吸收浅谈
- **作者**：大猫咪与小狮子
- **URL**：https://zhuanlan.zhihu.com/p/1888290264377976190
- **发布平台**：知乎

## 核心要点

### 矩阵吸收的工程动机

- 核心洞察：张量广播计算（broadcast）远快于等维度矩阵乘法，本质在于**减少内存访问**
  - 实验对比（4080 GPU）：两个 `[1000, 500, 1000]` × `[1000, 1000, 2000]` = 0.47s；利用广播的 `[1000, 500, 1000]` × `[1, 1000, 2000]` = 0.12s（约 4× 加速）
- MLA 矩阵吸收的目标：在注意力计算时让 K、V **不含头维度（H）**，使计算退化为广播，降低内存访问开销

### MLA 计算流程（以 B=2, S_Q=1, S_KV=12, C=7168 为例）

1. **Q 矩阵处理**：输入 → 低秩投影（降维）→ 升维 → 拆分为 `q_rope`（需位置编码）和 `q_nope`（不需位置编码）
2. **KV 矩阵处理**：输入 → 降秩投影得到 `compressed_kv` 和 `k_rope`；**升维矩阵此时不执行**，留待后续吸收
3. **编码部分注意力权重**：`q_rope` 和 `k_rope` 各做位置编码后计算注意力权重；此时 `k_rope` 的头维度为 **H=1**（广播优化点1）
4. **拆分 KV 升维矩阵**：`W_kv_up`（Linear，in=512, out=16×(128+128)=4096）拆为 `k_up`（K 升维）和 `v_up`（V 升维）
5. **K 升维矩阵吸收**：`q_nope @ k_up` → k_up 被吸收进 q_nope，此步含多头信息
6. **注意力分数计算**：吸收后的 `q_nope` @ `compressed_kv^T`；`compressed_kv` **不含头信息**（广播优化点2）；两部分权重相加后 softmax
7. **V 升维矩阵吸收**：`attn_weights @ compressed_kv`（广播优化点3）→ 再 @ `v_up^T` 吸收 V 升维矩阵 → 合并头 → 线性投影输出

### 三处广播优化

| 位置 | 操作 | 优化方式 |
|------|------|---------|
| 注意力权重1 | Q_rope @ K_rope^T | k_rope 头维度=1，广播 |
| 注意力权重2 | Q_nope @ compressed_kv^T | compressed_kv 无头信息，广播 |
| 注意力分数 | attn_weights @ compressed_kv | compressed_kv 无头信息，广播 |

### 小结

- MLA 矩阵吸收**继承了 MQA 的 KV 共享优势**（减少 KV Cache 显存），同时通过多头升维矩阵**极大保留了信息表达能力**
- DeepSeek 的多头数为 128，广播优化收益巨大
- 每张流程图对应一个独立的代码实现单元，提高了代码可读性

## 关联

- [[概念_MLA低秩KV压缩]] — MLA 完整原理：低秩压缩 + 矩阵吸收
- [[概念_KV_Cache_键值缓存]] — MLA 矩阵吸收减少 KV Cache 显存的机制
- 多头注意力变体 — MHA/MQA/GQA/MLA 对比
- [[实体_DeepSeek_V2]] — MLA 首次提出的模型
- [[MiniMax_vs_Kimi_注意力路线之争]]
- [[Attention复杂度解析与改进方向]]

---
> 📎 **物理文献**：[[raw/articles/deepseek MLA 矩阵吸收浅谈 - 知乎.md]]