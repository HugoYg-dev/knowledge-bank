---
type: "source"
tags: ["LLM/inference", "Infra/serving"]
summary: "Manifest 团队反思并废弃其 LLM 模型路由器的实践经验：复杂度无法单凭 Prompt 判断、前缀缓存收益远高于路由分流，且不可预测性增加了 Agent 系统的维护代价"
sources: ["raw/articles/Everyone is building LLM routers, we deprecated ours.md"]
updated: "2026-09-21"
---

# 来源摘要：Everyone is building LLM routers, we deprecated ours

## 来源信息

- **标题**：Everyone is building LLM routers, we deprecated ours
- **作者**：Bruno Perez (Manifest)
- **发布日期**：2026-07-31
- **原文链接**：https://manifest.build/blog/why-we-deprecated-our-llm-router/

## 核心要点

1. **废弃背景与初衷反差**：Manifest 作为 LLM 网关平台，曾于 3 月推出基于任务复杂度（simple、standard、complex、reasoning 四层）的 [[concepts/概念_LLM模型路由]]，旨在降低推理开销。但在 7000 名云端用户实际运行 4 个月后，最终于 6 月宣布废弃并在 9 月 1 日彻底下线。
2. **任务复杂度无法单凭 Prompt 判定**：Prompt 仅是任务的触发器（Trigger），很多决定复杂度的关键上下文是在后续的工具调用（Tool Calls）、网络检索等交互执行过程中才浮现出来的，仅根据初始提示词无法准确评估真实复杂度。
3. **缓存效益优于路由分流**：前缀缓存（Prefix Cache / [[concepts/概念_KV_Cache_键值缓存]]）的读取成本比无缓存输入便宜 75% 至 90%。System Prompt 和多轮对话历史构成了核心 Token 开销；若路由考虑缓存粘性则无法分流，若频繁分流则破坏缓存击穿，使得路由在成本优化上得不偿失。
4. **破坏行为一致性与工程师工具熟练度**：不同模型的细微差异要求工程师像工匠挑选画笔一样精细理解并固定选择模型与参数。在工作会话中频繁跳变模型会导致整体输出质量下降，并削弱工程师对工具特性的掌控力。
5. **智能体工作流中不可预测性的隐性代价**：在自动化 Agent 工作流中，管理多模型带来的不确定性成本（Evals 评测、System Prompt 适配、可观测性等运维负担）远大于分流节省的边际推理费用；固定配置经过验证的模型反而更具确定性与性价比。

## 关联概念与实体

- [[concepts/概念_LLM模型路由]]
- [[concepts/概念_KV_Cache_键值缓存]]

---

> 📎 **物理文献**：[[raw/articles/Everyone is building LLM routers, we deprecated ours.md]]
