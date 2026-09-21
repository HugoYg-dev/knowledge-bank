---
type: concept
tags:
- AI-Agent/skill
- AI-Agent/coding
summary: LLM Wiki 是由 Andrej Karpathy 提出的一种全新知识管理范式，旨在颠覆传统 RAG “临时抱佛脚”模式，强调在知识摄入（Ingest）阶段即完成信息的结构化与编译。
sources:
- wiki/sources/Claude Code与Obsidian飞书知识库搭建实践.md
- wiki/sources/Karpathy推文引发的LLM_Wiki知识库搭建实践.md
updated: '2026-07-22'
---

# 概念：LLM Wiki 范式

## 定义

**LLM Wiki** 是由 [[entities/实体_Andrej_Karpathy|Andrej Karpathy]] 提出的一种全新知识管理范式，旨在颠覆传统 RAG（检索增强生成）“临时抱佛脚”的模式，强调**在知识摄入（Ingest）阶段即完成信息的结构化与编译**。

## 与传统 RAG 的深度对比

| 维度 | 传统 RAG | LLM Wiki |
|------|----------|----------|
| **核心思维** | “我有一堆文档，AI 现场帮我搜” | “AI 平时帮我编译好知识库，我随时用” |
| **处理时机** | **查询时（Query-time）** 临时检索与拼接 | **摄入时（Ingestion-time）** 预先结构化与关联 |
| **知识复利** | **无积累**：每次查询从零开始，搜完即散 | **高复利（Compounding）**：新知识在图谱中交叉引用与补充 |
| **存储形态** | 向量数据库（高维度，人类不可读） | 纯 Markdown（零基建依赖，[[entities/实体_Obsidian|Obsidian]] 可读与图谱可视化） |
| **冲突处理** | 检索到矛盾碎片易引发幻觉或逻辑断裂 | 在 Ingest 阶段主动发现、标注矛盾与维护一致性 |

## 三层经典架构（Karpathy 比喻）

1. **底层原始资料（Raw Sources）**：由笔记、剪藏、PDF 构成的只读层，保持绝对原貌（只读不改）。
2. **中间层维基（Wiki Layer - 编译产物）**：AI 提取要点、编写词条、建立概念间双向引用的结构化网络（由 LLM 维护）。
3. **顶层规则配置（Schema Layer - 构建配置）**：如 `CLAUDE.md`、`AGENTS.md` 与 [[concepts/概念_系统提示词四层架构|系统提示词四层架构]]，指导 AI 理解知识体系结构、格式与处理 SOP。

> **核心名言**：**"Obsidian 是 IDE，LLM 是程序员，Wiki 是代码库。"** AI 不是搜索引擎，而是知识库管理员。

## 四大核心闭环操作

1. **[[concepts/概念_Ingest入库闭环|Ingest（摄入）]]**：往 `raw/` 放入新文档，LLM 阅读全文、提炼要点、生成摘要、联动实体与概念，检查矛盾并同步索引与日志。
2. **Query（查询）**：阅读已编译 Wiki 输出解答，优质探究结果可回填为 Wiki 新页面。
3. **Index（索引）**：`index.md` 提供内容导向总目录，`log.md` 提供追加式流水。
4. **Lint（健康检查）**：定期体检矛盾、孤立节点、过时内容与占位符页面。

## 80 年知识管理思想谱系

- **1945 年**：[[entities/实体_Vannevar_Bush|Vannevar Bush]] 提出 [[concepts/概念_Memex_个人机电知识扩展系统|Memex]] 构想，开创“关联性路径”与个人知识设备视角。
- **1950 年代**：[[entities/实体_Niklas_Luhmann|Niklas Luhmann]] 打造 [[concepts/概念_卡片盒笔记法|卡片盒笔记法 (Zettelkasten)]]，通过 9 万张索引卡建立“对话伙伴”。
- **2026 年**：[[entities/实体_Andrej_Karpathy|Andrej Karpathy]] 引入 LLM 自动化维护，使知识库的记账与维基编织成本接近于零。

## 来源与参考

- [[Karpathy推文引发的LLM_Wiki知识库搭建实践]]
- [[Claude Code与Obsidian飞书知识库搭建实践]]
- [[concepts/概念_RAG与LLM_Wiki对比]]