---
type: "source"
tags: ["RSI", "LLM/training/RL"]
summary: "探讨 RSI 时代下模型自验证（Self-Verification）与多轮验证闭环（Verification Loop）的必要性及 RL 训练方法，解析生成与验证分离实验及 ReVeal、SCoRe、RepExp 三类奖励机制。"
sources: ["raw/articles/RSI，先会verify的模型先享受.md"]
updated: "2026-11-17"
---

# RSI，先会 verify 的模型先享受

- **作者**：李rumor
- **发布时间**：2026-11-16
- **原文链接**：https://mp.weixin.qq.com/s/ptXWGpxyO_gQhL7zAuYPnQ

## 核心要点

1. **验证能力是开放任务 [[concepts/概念_RSI递归自我改进|RSI]] 的关键瓶颈**：现有 RSI 工作多依赖客观可验证任务，而真实世界任务大多难以直接打分；[[entities/实体_DeepSeek|DeepSeek]]（DeepSeek-V4.1-Flash-1017 自反馈强化学习）与 [[entities/实体_Gemini|Gemini]]（Gemini 4 Carbon 的 Extended Verification Loops）均将多轮发现问题并自我改进的验证闭环视为核心能力。
2. **生成能力不等于验证能力（生成 != 验证）**：ICML 2026 论文 *Learning to Self-Verify Makes Language Models Better Reasoners* 的 1,000 步 Math RL 对比实验表明，只练做题不一定提升判题能力；而只练判题的模型不仅判题更强，做题准确率也接近只练做题的模型，且平均输出更短。
3. **验证训练能增强从错误路径恢复的能力**：在 1,545 道数学题（Qwen2.5-7B-Instruct 解题 + GPT-4.1 改写为带错 thinking prefix）的续写实验中，判题模型最终答对率高于做题模型与 Base 模型，证明 [[concepts/概念_Self_Verification_模型自验证|Self-Verification]] 训练赋予了模型更强的纠错与路径修正能力。
4. **ReVeal（奖励验证行为，ICLR 2026）**：面向代码生成场景，让模型交替写代码与写单元测试；训练期利用参考实现过滤无效测试，并将后一轮代码通过率差值同时归功于前一轮写测试行为（三类奖励：测试通过参考实现比例、代码修改前后通过率差值、最终版本测试通过率 $\times 5$ + 格式分）。
5. **SCoRe（奖励有效修改，ICLR 2025）**：[[entities/实体_DeepMind|Google DeepMind]] 针对两轮自纠错提出两阶段 RL 训练——第一阶段对第一轮施加较强 KL 约束以保留原始错误样本供第二轮练习纠错；第二阶段同时奖励两轮正确性，并叠加「第二轮得分 - 第一轮得分」的差值权重，避免模型通过提高首轮准确率而逃避修改。
6. **RepExp（奖励多样探索，ICLR 2026）**：普林斯顿大学与 Microsoft Research 在 [[concepts/概念_GRPO_群组相对策略优化|GRPO]] 正确性奖励之外，基于模型隐藏表示计算同批采样的表征差异度作为探索奖励（答错的解答也可获得探索分），提升原题多采样命中率。
7. **从单轮 Judge 走向多轮 Trajectory 优化**：相较 2023 年侧重单轮生成的 [[concepts/概念_LLM_as_a_Judge校准|LLM-as-a-Judge]] 与 Self-Rewarding，Agent 时代优化目标转向多轮轨迹；只要验证反馈能驱动下一步改得更好，即便单步验证不完美也有价值，且验证正确性需随环境与用户交互的上下文动态提升。

## 关联实体与概念

- **核心概念**：[[concepts/概念_RSI递归自我改进]]、[[concepts/概念_Self_Verification_模型自验证]]、[[concepts/概念_GRPO_群组相对策略优化]]、[[concepts/概念_LLM_as_a_Judge校准]]
- **相关实体**：[[entities/实体_DeepSeek]]、[[entities/实体_Gemini]]、[[entities/实体_DeepMind]]

## 参考资料

- DeepSeek-V4.1-Flash-1017: https://api-docs.deepseek.com/zh-cn/news/news261017/
- Gemini 4 Carbon: https://deepmind.google/models/model-cards/gemini-4-carbon/
- *Learning to Self-Verify Makes Language Models Better Reasoners* (ICML 2026): https://proceedings.mlr.press/v306/chen26es.html
- *ReVeal: Self-Evolving Code Agents via Reliable Self-Verification* (ICLR 2026): https://arxiv.org/html/2506.11442
- *Training Language Models to Self-Correct via Reinforcement Learning* (SCoRe, ICLR 2025): https://arxiv.org/html/2409.12917v2
- *Representation-Based Exploration for Language Models: From Test-Time to Post-Training* (RepExp, ICLR 2026): https://arxiv.org/html/2510.11686

> 📎 **物理文献**：[[raw/articles/RSI，先会verify的模型先享受.md]]
