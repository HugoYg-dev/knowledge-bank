---
type: "source"
tags: ["AI-Agent/tool-calling", "LLM/inference"]
summary: "TypeSafe AI 推出首个非自回归概率决策模型 Jev，通过 RLCD 训练范式与契约原语实现无文本生成、零解析幻觉与极低延迟的 Agent 结构化决策"
sources: ["raw/articles/新模型Jev 爆红一周：不生成文字、只输出概率，却被玩出了花.md"]
updated: "2026-09-20"
---

# 来源摘要：新模型Jev 爆红一周：不生成文字、只输出概率，却被玩出了花

- **来源信息**：微信公众号“代码的使命” / 何码先生（2026-09-19）
- **核心定位**：专用于决策判断（不生成自由文本、只输出校准概率）的非自回归轻量模型，解决 AI Agent 循环中过度依赖重型生成模型做分类、路由与工具选择的延迟与可靠性问题。

## 核心要点

1. **Agent 核心负载是判断而非生成**：在经典的 Plan-Act-Observe-Adjust 循环中，绝大多数节点是分类、安全审核、工具挑选和条件跳转等判断任务。用大语言模型生成文字再用正则/JSON 提取不仅慢（数秒延迟），还存在编造非法工具名的幻觉风险。
2. **三类基础原语（Primitives）契约**：Jev 仅接受 `state`（上下文）与 `questions`（问题定义），仅提供三种原子类型：
   - `Noul`：是非命题判断（输出 0 到 1 概率）；
   - `Choice`：从预设有限选项中单选（输出选中项、概率分布与置信度）；
   - `Score`：序数分级打分（2 到 10 档，带置信度与 legend）。
3. **“不会幻觉”的本质是 Schema Matching 约束**：由于输出空间在先验上被约束在定义好的候选集内，Jev 无法产生未定义的格式或非法字段（0% schema error），但这不等于“判断事实 100% 正确”。
4. **[[concepts/概念_RLCD校准决策强化学习|RLCD]] 训练范式**：采用 Reinforcement Learning for Calibrated Decisions，使用 Proper Scoring Rules（如 cross-entropy、Brier score）优化预测概率与真实频率的统计一致性（校准），使得置信度成为可信的程序路由门控量。
5. **性能与成本断崖式优化**：端到端延迟在 70-500ms（典型约 100ms），输入价格 0.042 美元 / 百万 token，输出免计费；使得在 Agent 的每一次中间动作（逐步安全检查、工具选择、路由重试）进行实时验证成为可行。
6. **生态落地实践**：一周内社区涌现出基于 Jev 的 Browser Agent 元素选择（jev-ultrafast）、Vercel 命令安全审查、代码审查矩阵（jev-review）、SQL 模糊条件过滤（pg-jev）等探索。
7. **客观局限与黑盒审计**：当前模型权重与架构未开源，基准主要基于强模型答案聚合而非纯客观 Ground Truth；在复杂多跳推理、长文本（64k 限制）及含语义噪声输入下仍有准确率折损，适合作为快速路由层而非复杂认知中枢。

## 关联实体与概念

- 机构与人物：TypeSafe_AI
- 关联概念：[[concepts/概念_RLCD校准决策强化学习]]、[[concepts/概念_Harness_Engineering]]

> 📎 **物理文献**：[[raw/articles/新模型Jev 爆红一周：不生成文字、只输出概率，却被玩出了花.md]]
