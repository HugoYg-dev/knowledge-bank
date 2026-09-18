# 🧠 Knowledge Bank — AI Agent 驱动的个人知识库系统

[![Obsidian Vault](https://img.shields.io/badge/Obsidian-Knowledge%20Vault-7057ff?logo=obsidian&logoColor=white)](https://obsidian.md)
[![Python Lint Tool](https://img.shields.io/badge/Scripts-Vault%20Lint-blue?logo=python&logoColor=white)](file:///Users/ZHao/WorkSpace/knowledge-bank/scripts/vault_lint.py)
[![Git Sync](https://img.shields.io/badge/Sync-Obsidian%20Git-green?logo=git&logoColor=white)](file:///Users/ZHao/WorkSpace/knowledge-bank/setup-config.md)

基于 **Obsidian** 与 **Git** 的个人知识库 (Vault)，专为 **AI Agent / LLM 协同治理** 与 **结构化知识复利** 打造。通过严密的单向数据推导管线与自动化脚本治理，将分散的网页剪藏、技术文章与随想提炼为高内聚、网状联动的 Wiki 知识图谱。

---

## 📐 1. 系统架构与分层设计

知识库严格遵循 **三层数据架构与单向推导管线**（Derivation Chain）：

```
raw/ & Clippings/ (零级底座·绝对只读)
       │
       ▼  Ingest 提炼
wiki/sources/ (一级摘要·1:1 物理映射)
       │
       ▼  实体/概念图谱提取
wiki/{entities, concepts, comparisons, overview} (末端知识产物)
```

### 🗂️ 目录划分说明

| 目录/文件 | 角色定位 | 说明与规范 |
| :--- | :--- | :--- |
| **`raw/`** | **零级物理底座** | 外部原始资料归档（包含 `articles/`, `insights/`, `papers/`, `playbooks/`, `transcripts/`），**绝对只读不改**。 |
| **`Clippings/`** | **外部资料暂存区** | 网页剪藏由官方插件暂存；邮件订阅暂存于 `emails/<来源>/`，由共享邮件管线发现、路由和拆分。两者均须在完成 Ingest 提炼后归档至 `raw/` 对应子目录。 |
| **`wiki/sources/`** | **一级摘要层** | 单个文献的结构化摘要页，Frontmatter `sources:` 字段 100% 精确指向 `raw/` 物理文件。 |
| **`wiki/entities/`** | **实体图谱页** | 人物、机构、开源项目等实体（如 `实体_xxx.md`），基于 `sources/` 提炼。 |
| **`wiki/concepts/`** | **概念图谱页** | 算法、理论、模型架构等核心概念（如 `概念_xxx.md`），基于 `sources/` 提炼。 |
| **`wiki/comparisons/`** | **对比分析页** | 横向技术选型与框架对比分析（`xxx_vs_yyy.md`）。 |
| **`wiki/overview/`** | **专题综述页** | 体系化专题总结与全景框架（`综述_xxx.md`）。 |
| **`wiki/index.md`** | **全库总索引** | 知识库所有 Wiki 页面分类挂载的根索引。 |
| **`wiki/log.md`** | **运维日志** | AI Agent 与人工对知识库进行变更与精简的操作流水账。 |
| **`assets/`** | **静态资源库** | 存储本地原创图片/PDF等资源。网页抓取文章保持公网 URL，严禁膨胀 Git 体积。 |
| **`workdocs/`** | **业务工作文档** | 存放业务交付物、调研报告及 Word 原始文档。 |
| **`scripts/`** | **自动化工程脚本** | 知识库健康诊断、死链/漏登审查、级联清理与标签白名单治理核心工具库（含 `vault_lint.py`, `tag_manager.py`, `vault_utils.py` 等）。 |

---

## ⚖️ 2. 单向推导与 Agent 治理纪律

为了杜绝幻觉生成与图谱断链，全库严格遵守以下规则（详见 [AGENTS.md](file:///Users/ZHao/WorkSpace/knowledge-bank/AGENTS.md)）：

1. **唯一上游溯源**：
   - `wiki/sources/` 唯一上游必须是 `raw/` 物理文件。
   - 末端产物（`entities/`, `concepts/`, `comparisons/`, `overview/`）的唯一上游必须是 `wiki/sources/`，**严禁绕过摘要层直接链接 `raw/`**。
2. **严禁无源虚假生成**：
   - 任何没有 `sources/` 支撑的末端页面均被视为“虚假生成”，将在 Lint 审计中物理清除。
3. **入度门槛与级联清理 (Pruning SOP)**：
   - **实体/概念创建门槛**：非核心讨论或仅提及一次的次要对象不单独建页。
   - **级联精简**：删除最上游 `raw/` 资料时，自动清理对应 `sources/`，并重新计算关联实体/概念的全库引用度（In-degree），引用度 $\le 1$ 时自动触发垃圾回收。

---

## 🛠️ 3. 自动化工程与工具脚本

项目内置专有 Python 工具集（位于 [`scripts/`](file:///Users/ZHao/WorkSpace/knowledge-bank/scripts)），为 Agent 和开发者提供自动化治理能力：

### 常用治理命令

```bash
# 1. 全库健康度诊断（包含索引挂载率、死链、漏登、Sources 映射审计）
python3 scripts/vault_lint.py lint

# 2. 原始资料只读净化视图派生（派生过滤了 HTML 污染的安全临时视图到 tmp/sanitized/）
python3 scripts/vault_lint.py sanitize-view raw/articles/xxx.md

# 3. 级联精简与清理预览 (Dry-run)
python3 scripts/vault_lint.py prune raw/articles/xxx.md

# 4. 执行物理级联精简 (确认影响页面 < 5 时使用)
python3 scripts/vault_lint.py prune raw/articles/xxx.md --apply

# 5. 低频无效果孤立实体/概念专项清理 (支持 entities 与 concepts)
python3 scripts/vault_lint.py prune-low-freq-entities
python3 scripts/vault_lint.py prune-low-freq-concepts

# 6. 标签治理与权威白名单审查 (基于 tags.json)
python3 scripts/tag_manager.py list
python3 scripts/tag_manager.py validate
```

---

## ⚙️ 4. Obsidian 环境配置与同步

知识库配合 Obsidian 客户端使用效果最佳。配置细节请参阅 [setup-config.md](file:///Users/ZHao/WorkSpace/knowledge-bank/setup-config.md)。

### 推荐插件配置

- **Obsidian Git**：每 10 分钟自动 Commit & Push/Pull，实现多端无缝同步。
- **Dataview**：基于 YAML Frontmatter 进行动态汇总与表格查询。
- **Templater**：快速套用标准模板。
- **Local REST API with MCP**：提供本地 HTTP/MCP 接口，方便 AI Agent 直接进行图谱交互与检索。

---

## 📜 5. 相关核心文档指针

- 📖 **[AGENTS.md](file:///Users/ZHao/WorkSpace/knowledge-bank/AGENTS.md)** — AI Agent 核心宪法、图谱规范与 SOP 操作指南。
- 📋 **[TODO.md](file:///Users/ZHao/WorkSpace/knowledge-bank/TODO.md)** — 知识库演化路线与待办任务清单。
- ⚙️ **[setup-config.md](file:///Users/ZHao/WorkSpace/knowledge-bank/setup-config.md)** — Obsidian 客户端安装与插件配置指南。
- 🗂️ **[wiki/index.md](file:///Users/ZHao/WorkSpace/knowledge-bank/wiki/index.md)** — Wiki 图谱分类总索引。
- 📝 **[wiki/log.md](file:///Users/ZHao/WorkSpace/knowledge-bank/wiki/log.md)** — 知识库演进操作日志。

---

*Powered by Obsidian, Python Engineering Tools & AI Agents.*
