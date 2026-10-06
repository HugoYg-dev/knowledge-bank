# scripts/ — 知识库自动化运维与工程治理工具集

本目录存放面向 **LLM Wiki Repository** 自动化治理、健康诊断与管线运维的 Python 脚本工具集。所有脚本均采用 PEP 723 单文件依赖声明，统一使用 `uv run scripts/<script>.py` 执行。

---

## 核心运维工具清单

| 文件 | 功能定位 | 核心用法与说明 |
| :--- | :--- | :--- |
| [`vault_lint.py`](vault_lint.py) | **全库图谱健康诊断与级联清理核心** | `uv run scripts/vault_lint.py lint` 审计 YAML Schema、总索引漏登与死链；支持 `prune` 级联垃圾回收与 `prune-low-freq-entities`。 |
| [`tag_manager.py`](tag_manager.py) | **标签白名单权威治理工具** | `uv run scripts/tag_manager.py list/check/add/rename/delete`，维护全库 `tags.json` 白名单与标签级联变更。 |
| [`mail_pipeline.py`](mail_pipeline.py) | **多来源邮件暂存管线 CLI** | `uv run scripts/mail_pipeline.py sync/route/run/reconcile`，实现 Gmail 星标同步、发件人路由、官网长文比对升级与入库对账。 |
| [`concept_source_lint.py`](concept_source_lint.py) | **概念与来源双向链审计** | 校验末端概念页的 `sources:` 字段是否合法指向 `wiki/sources/`，防止出现断链或越级直连。 |
| [`audit_upstream_sources.py`](audit_upstream_sources.py) | **上游溯源链深度审计** | 审计 `raw/` -> `wiki/sources/` -> 末端产物的单向推导链完整性。 |
| [`daily_scan.py`](daily_scan.py) | **每日例行健康扫描** | 扫描 `Clippings/` 待审堆积、未归档文件与异常出链，输出巡检报告。 |
| [`migrate_concept_names.py`](migrate_concept_names.py) | **概念命名规范迁移工具** | 支撑概念命名三分层规范（缩写/专名+中文）历史存量页面的平滑重命名与全库双链替换。 |
| [`normalize_tags.py`](normalize_tags.py) | **标签规范化清洗工具** | 批量扫描并纠正全库 Frontmatter 中的非标 Tag。 |
| [`vault_utils.py`](vault_utils.py) | **底层通用函数库** | 提供全库 Markdown 文件解析、Frontmatter 读取回写、双链提取等公共底层能力。 |

---

## 支撑目录与子模块

- [`mail_sources/`](mail_sources/)：各个邮件订阅源的具体解析插件目录（如 `dailydoseofds.py`），负责将原始 HTML 邮件结构化拆解为待审 Markdown。
- [`launchd/`](launchd/)：macOS 自动化定时任务配置 plist 模版，用于部署定时巡检与邮件同步。

---

## 自动化测试套件

本工具集配备了完整的 pytest 单元测试，保证重构与变更的安全性：
- `test_vault_lint.py`：测试 `vault_lint` 的死链检测、YAML 校验与 prune 逻辑。
- `test_tag_manager.py`：测试标签白名单 CRUD 与级联重命名。
- `test_mail_pipeline.py` & `test_dailydoseofds_web.py`：测试邮件同步路由与官网长文升级逻辑。
- `test_vault_utils.py` & `test_normalize_tags.py`：测试底层工具函数与标签清洗。

运行测试：
```bash
uv run pytest scripts/
```
