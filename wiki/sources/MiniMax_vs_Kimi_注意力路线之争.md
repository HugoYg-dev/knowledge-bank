---
type: source
tags:
- LLM/arch/attention
summary: MiniMax M2 回归 Full Attention，Kimi 发布开源混合注意力模型 Kimi Linear（KDA+MLA 3:1），两条技术路线的工程视角对比
sources:
- raw/articles/MiniMax和Kimi为了“注意力”，隔空交手.md
updated: '2026-07-01'
---
## 来源信息

- **标题**：MiniMax和Kimi为了"注意力"，隔空交手
- **作者**：周一笑
- **URL**：https://mp.weixin.qq.com/s?__biz=MzkyNjU2ODM2NQ==&mid=2247619925&idx=1&sn=375f3d4c9dfae099424769ecd31c9ddf
- **发布平台**：硅星人Pro

## 核心要点

### 事件背景

- 2025年10月29日，MiniMax 预训练负责人孙浩海（Haohai Sun）发布技术博客《为什么M2是Full Attention》，罕见公开说明放弃 efficient attention 的原因
- 72小时后（10月30日），月之暗面发布 **Kimi Linear**，开源 48B 参数混合注意力模型，正面回应技术路线之争

### MiniMax M2：回归 Full Attention

- M2 定位 Agent 和代码生成，强调"大巧若拙"，定价仅为 Claude Sonnet 4.5 的 8%（每百万 Token 输入 0.3 美元），TPS 约 100
- Haohai 阐述放弃 efficient attention 的三个核心困难：
  1. **工程链路复杂性爆炸**：需同时支持 code/math、agent、多模态、Long CoT、RL、低精度、缓存、speculative decoding 等场景，每增加一种 attention 机制就要全面验证，工程复杂度指数增长
  2. **评测体系局限**：小规模实验结论无法外推，复杂多跳推理（KorBench、BBEH、BBH dyck language）的缺陷只在大规模时暴露
  3. **基建不完善**：Linear Attention 训练是访存 bound，推理需解决低精度存储、Prefix Cache、投机解码等问题，尚无成熟方案
- 对于 GPU 进步预期："目前只有成本问题，没有时延问题"，策略是等待硬件解决成本

### Kimi Linear：混合注意力反击

- **规模**：48B 总参数，3B 激活参数（MoE），训练数据 5.7T tokens，支持 1M tokens 上下文，全部开源
- **Kimi Delta Attention (KDA)**：基于 Gated DeltaNet，将 scalar gate 升级为 **channel-wise gate（通道级门控）**，每个特征维度独立控制遗忘因子；相比标准 DPLR 实现，计算效率提升约 100%
- **混合比例 3:1**：通过 ablation study 确定，每 3 层 KDA 配 1 层 MLA（DeepSeek V2/V3 技术）
  - Validation PPL：纯 MLA=5.77，3:1=**5.65**（最优），1:1=5.66，7:1=5.70，15:1=5.82
- **NoPE（No Position Encoding）**：MLA 层不使用 RoPE，位置信息完全由 KDA 层处理，好处是 MLA 可转为更高效的 MQA，训练更简单，长上下文泛化更好
- **性能数据**：
  - KV Cache 减少 75%（内存占用降低 4 倍）
  - 1M tokens 场景下解码吞吐量比 MLA 快 **6.3 倍**（TPOT：11.48ms → 1.84ms）
  - RULER 基准（128k context）达 84.3，速度是 MLA 的 3.98 倍
- **Scaling Law 验证**：1.4T tokens 训练中，Kimi Linear 约 1.16× 计算效率优于 Full Attention
- **vLLM 集成**：KDA 算子已被 vLLM 官方整合进主代码库

### 两条路线分析

| 维度 | MiniMax（Full Attention） | Kimi（KDA+MLA） |
|------|--------------------------|----------------|
| 策略 | 时间换空间，赌 GPU 进步 | 空间换时间，主动降成本 |
| 优势 | 验证充分，无隐藏弱点 | 效率高，长期竞争力强 |
| 风险 | 成本高 | 工程挑战大，多场景稳定性待验证 |

- 行业背景：DeepSeek 用 MLA 压缩 KV Cache，Mistral 用滑动窗口稀疏注意力，OpenAI/Anthropic 以 Full Attention 工程加速为主

## 关键引文

> Haohai：需要同时满足 code/math、agent、多模态、Long CoT、RL、低精度运算、缓存、speculative decoding 等众多场景，工程复杂度呈指数级增长 [重点/高亮]

> 第二个困难是评测体系局限。"小规模实验的结论无法外推，复杂多跳推理任务的缺陷只在大规模时暴露。" [重点/高亮]

> 第三个困难是基建不完善。"Linear Attention的训练是访存bound，推理需要解决低精度存储、Prefix Cache、投机解码等问题。" [重点/高亮]

## 关联

- [[概念_线性注意力与混合注意力]] — Linear Attention、Hybrid Attention 架构原理
- [[概念_MLA低秩KV压缩]] — DeepSeek MLA 技术
- [[概念_KV_Cache_键值缓存]] — KV Cache 原理与内存占用
- [[实体_MiniMax_M2]] — MiniMax 回归 Full Attention 的 Agent 模型
- [[实体_Kimi_Linear]] — 月之暗面开源混合注意力模型
- [[concepts/概念_Kimi_Delta_Attention_增量注意力|Kimi Delta Attention]] — KDA：channel-wise gate 线性注意力
- [[Attention复杂度解析与改进方向]]

---
> 📎 **物理文献**：[[raw/articles/MiniMax和Kimi为了“注意力”，隔空交手.md]]