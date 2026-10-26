---
type: "source"
tags:
  - "LLM/arch/attention"
  - "LLM/inference"
summary: "从 PyTorch 代码实现视角手撕 DeepSeek MLA 算法：详解 Q/KV 低秩投影与维度拆分、RoPE 位置编码解耦、张量组织与打分计算全流程"
sources:
  - "raw/articles/MLA(1)：从代码角度学习和彻底理解 DeepSeek MLA 算法.md"
updated: "2026-10-26"
---

# MLA(1)：从代码角度学习和彻底理解 DeepSeek MLA 算法

- **来源**: 个人博客（yuanchaofa.com）
- **作者**: 袁朝发（Chaofa Yuan）
- **发布日期**: 2025-02-05
- **原始链接**: [https://yuanchaofa.com/post/hands-on-deepseek-mla](https://yuanchaofa.com/post/hands-on-deepseek-mla)

---

## 核心要点

1. **MLA 的核心目标定位**：MLA（Multi-head Latent Attention）的核心目标是节约大语言模型自回归生成期间的 KV Cache，其本质上可以理解为建模表达力更强、显存效率更高的升级版 Grouped-Query Attention。
2. **维度分离实现 RoPE 兼容**：
   - 传统低秩投影无法与 RoPE 旋转位置编码直接融合，因为旋转矩阵打乱了线性投影吸收的可能性；
   - MLA 通过维度显式切分实现兼容：将 Query 和 Key 各自拆解为参与 RoPE 计算的子向量（$q_{pe}, k_{pe}$）与不参与 RoPE 的非位置子向量（$q_{nope}, k_{nope}$）；
   - 在注意力矩阵计算前，将两组特征拼合为全头尺寸：$q = \text{concat}(q_{nope}, q_{pe})$，$k = \text{concat}(k_{nope}, k_{pe})$。
3. **PyTorch 前向计算张量流动拆解**：
   - **Query 投影**：`hidden_states` ➔ 降维线性层（`q_down_proj`，大小 $d'_c$）➔ RMSNorm ➔ 升维线性层（`q_up_proj`，输出多头维度）➔ 拆分为 `q_nope` 与 `q_pe`；
   - **KV 投影**：`hidden_states` ➔ 降维线性层（`kv_down_proj`，大小 $d_c + d_h^R$）➔ 拆分为压缩潜在向量 `compressed_kv` 与位置特征 `k_pe`；
   - **KV 展开**：`compressed_kv` 经过 RMSNorm 与 `kv_up_proj` 升维，拆分为 `k_nope` 与 `value_states`。
4. **注意力得分与输出合成**：
   - 对 `q_pe` 与 `k_pe` 分别应用旋转矩阵 `apply_rotary_pos_emb` 后，拼装出 `query_states` 与 `key_states`；
   - 执行矩阵乘法 `torch.matmul(query_states, key_states.transpose(2, 3))` 并缩放，结合 Causal Mask 与 Softmax 计算权重，加权聚合 `value_states` 并经由 `o_proj` 映射回隐藏层维度。
5. **官方开源实现与矩阵吸收边界**：
   - 论文与开源基础实现（如 HuggingFace 模型权重定义）通常展示未经矩阵吸收的标准前向逻辑，适合算法学习与训练期理解；
   - 而生产部署场景必须引入矩阵吸收技术，将 Key/Value 升维矩阵融合至 Query 侧投影中，从而避免在自回归推理期间展开多头 KV。

---

## 关联概念与实体

- **关联概念**: [[concepts/概念_MLA_多头潜在注意力|概念_MLA_多头潜在注意力]]、[[concepts/概念_KV_Cache_键值缓存|概念_KV_Cache]]、[[concepts/概念_GQA_分组查询注意力|概念_GQA_分组查询注意力]]
- **关联实体**: [[entities/实体_DeepSeek|实体_DeepSeek]]、[[entities/实体_DeepSeek-V3|实体_DeepSeek-V3]]、[[entities/实体_DeepSeek_V2|实体_DeepSeek_V2]]

---
> 📎 **物理文献**：[[raw/articles/MLA(1)：从代码角度学习和彻底理解 DeepSeek MLA 算法.md]]
