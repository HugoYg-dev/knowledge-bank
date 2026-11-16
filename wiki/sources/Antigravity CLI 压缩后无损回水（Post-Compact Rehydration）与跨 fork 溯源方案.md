---
type: "source"
tags: ["AI-Agent/context-engineering"]
summary: "面向 Antigravity CLI 的零侵入 PreInvocation Hook 方案，实现长会话压缩后无损状态回水（Rehydration）与跨 /fork 分支祖先历史溯源"
sources: ["raw/articles/Antigravity CLI 压缩后无损回水（Post-Compact Rehydration）与跨 fork 溯源方案.md"]
updated: "2026-11-16"
---

# 来源摘要：Antigravity CLI 压缩后无损回水（Post-Compact Rehydration）与跨 fork 溯源方案

## 来源信息

- **来源标题**：Antigravity CLI 压缩后无损回水（Post-Compact Rehydration）与跨 /fork 溯源方案
- **发布平台**：agy-rehydrate.pages.dev
- **发布时间**：2026-11-14
- **原文链接**：https://agy-rehydrate.pages.dev/

## 核心要点

1. **原生压缩失忆根因与 Claude Code 对标**：[[entities/实体_Antigravity|Antigravity CLI]] 在单轮上下文累计跨过约 256K tokens（262,144）或用户手动执行 `/compact` 时，会写入 `CHECKPOINT` 记录并生成 `<CONTEXT_SUMMARY>` 替换早期历史。原生机制存在三项结构性损耗：
   - 仅保留概括摘要与最近 10 条提问，早期全局约束被弱化或遗漏；
   - 源码上下文与工具轨迹彻底清空，导致模型压缩后容易凭印象猜测接口或重复排查；
   - `/fork` 分支历史断代（新目录从 `step K > 0` 起步且不复制父会话 JSONL，`parent_conversation_id` 为空）。
   对比 [[entities/实体_Claude_Code|Claude Code]]（v2.1.322+）的 9 段结构化摘要与 `attachment` 状态恢复附件（重挂最近源码、活跃技能与计划引用），该方案确立了核心设计原则：**`<CONTEXT_SUMMARY>` 是有损的，但本地磁盘上的 `transcript_full.jsonl` 和工作区源码是 100% 无损的 Ground Truth**。
2. **零侵入全局 Hook 部署与快速短路**：方案部署于用户级全局配置（`~/.gemini/config/hooks.json` 与 `hooks/rehydrate_after_compact.py`），通过 `PreInvocation` 钩子在每次模型推理前介入。采用字节偏移增量扫描（`seek(prev_offset)`），平时无压缩普通对话耗时约 1ms 立即短路；设置 `FRESH_CHECKPOINT_MAX_GAP = 8` 避免在老会话半途误触重放陈旧压缩点，并具备状态文件与特征标记的双重幂等保护。
3. **跨 `/fork` 祖先会话链自动溯源与分叉隔离（resolve_fork_ancestors）**：针对子分支首步 $K > 0$ 的断代问题，算法在同级 `brain/*` 目录递归向上寻亲最多 8 层，结合步号范围、尾部 64KB 快速过滤、时间因果律校验（$T_{prev} \le T_{child} + 5s$）以及 `history.jsonl` 中的 `/fork` 命令记录进行多维消歧打分；每段祖先严格按 $[min\_step, K-1]$ 切片，实现父分支后续并发消息的分叉隔离，并在上下文拼接处插入路标注释。
4. **四层无损回水内容与严格 Token 预算控制**：回水总字符数控制在 85K–130K 字符（折合约 28K–38K tokens，仅占 256K 窗口的 12%–15%）：
   - **Header 溯源头**：标明 checkpoint 步号与 fork 祖先链条；
   - **Complete User Request Timeline（预算 24,000 字符）**：提取全链路所有非空 `USER_INPUT`，超限时保留最早 5 条红线原话与最近全部提问；
   - **Recent Pre-Compaction Verbatim Dialogue（预算 42,000 字符）**：倒推保留 User/Assistant 逐字对话，工具调用折叠为单行；
   - **Restored Active Skills & Spec Docs（预算 20,000 字符）**：从磁盘实时重读触碰过的 `SKILL.md` 及 SPEC/PLAN/TEMPLATE/HANDOFF 文档；
   - **Restored Active Workspace Files（预算 48,000 字符，单文件上限 12,000 字符）**：选取 Top 3 最近修改与 Top 3 最近读取文件，超限保留头部 68% + 尾部并标注中间省略字数。
5. **工程踩坑与 Fail-Open 安全边界**：
   - 规避 `hookcaller.go` 的 `protojson` 反序列化崩溃（`StepMetadata.user_markdown` 为 Protobuf Message，直接传 string 会报错，必须保持最小纯净返回结构 `injectSteps -> systemMessage`）；
   - 文件过滤黑名单自动跳过多媒体、大文件（>2MB）和内部临时日志目录，确保槽位留给真实源码；
   - 纯 Python 3.10+ 标准库零外部依赖，任何异常均 Fail-Open 放行（`exit 0`），绝不阻塞 CLI。

## 关键引文

> “`<CONTEXT_SUMMARY>` 是有损的，但本地磁盘上的 `transcript_full.jsonl` 和工作区源码是 100% 无损的 Ground Truth；只要在压缩后的第一轮调用前把关键状态自动‘回水（Rehydrate）’进 `<SYSTEM_MESSAGE>` ，即可消除压缩断忆。”

## 关联

- [[entities/实体_Antigravity|实体_Antigravity]]
- [[entities/实体_Claude_Code|实体_Claude_Code]]
- [[concepts/概念_上下文工程|概念_上下文工程]]
- [[concepts/概念_Context_Rot_上下文衰退|概念_Context_Rot_上下文衰退]]
- [[concepts/概念_Post_Compact_Rehydration_压缩后状态回水|概念_Post_Compact_Rehydration_压缩后状态回水]]

---

> 📎 **物理文献**：[[raw/articles/Antigravity CLI 压缩后无损回水（Post-Compact Rehydration）与跨 fork 溯源方案.md]]
