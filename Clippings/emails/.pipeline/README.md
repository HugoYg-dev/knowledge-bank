# 多来源邮件暂存管线

`Clippings/emails/` 是 Gmail 订阅邮件的暂存根目录。共享管线发现所有星标邮件、记录差异并按发件人路由；每个来源的解析器只负责把自己的邮件拆分为待审 Markdown。

```text
Gmail is:starred
  -> sync（发现、元数据、差异账本）
  -> route（已注册来源解析；未知来源仅待路由）
  -> Clippings/emails/<source_key>/*.md（用户人工逐篇 Review）
  -> 用户明确指令后，Agent 执行 AGENTS.md Ingest SOP
  -> raw/articles + wiki/sources + 图谱/索引/日志
```

## 目录与状态

- `manifest.json`：机器事实账本。邮件是容器，`articles` 数组中的文章是状态管理和 Ingest 的原子要素；记录每篇文章的 `status`、`content_tier`（`email_fallback` 或 `web_canonical`）与 `canonical_url`。
- `SYNC_STATUS.md`：自动生成的人工可读状态表，列出待路由邮件和待审文章。
- `ARCHIVE_INDEX.md`：已归档至 `raw/articles/` 的邮件订阅文章索引。
- `../<source_key>/*.md`：来源解析器生成的待审文章；当前已注册来源为 `dailydoseofds`。

未注册发件人仅保存 ID、发件人、主题和日期，并标记为 `unhandled`；不会拉取正文或生成文件。新增解析器后，登记发件人规则并执行 `route` 即可处理。

## 使用方法

### 1. 基础同步与路由

```bash
# 同步全部 Gmail 星标邮件，登记元数据与差异
uv run scripts/mail_pipeline.py sync

# 解析已注册来源，生成待审 Markdown；未知来源保持 unhandled
uv run scripts/mail_pipeline.py route

# 路由同时探测并拉取官网全量长文（若支持）
uv run scripts/mail_pipeline.py route --fetch-web

# 日常组合命令：逐篇对账 -> 同步 -> 路由
uv run scripts/mail_pipeline.py run

# 日常组合命令（同时启用官网长文增强）
uv run scripts/mail_pipeline.py run --fetch-web

# 查看共享状态
uv run scripts/mail_pipeline.py status
```

### 2. 官网长文增强与存量升级

针对邮件内容为删节导读（Teaser）、官网提供完整长文的订阅源（如 `dailydoseofds`），管线提供了单篇比对、Diff 预览、增量检测与安全替换工具：

```bash
# 1. 直接抓取单篇官网长文并生成待审文档（支持完整 URL 或 Slug）
uv run scripts/mail_pipeline.py fetch-web 'https://www.dailydoseofds.com/p/how-a-gpu-actually-works/'
uv run scripts/mail_pipeline.py fetch-web 'how-a-gpu-actually-works'

# 2. 单篇或批量升级比对报告（对比字数与代码块）
# 全量扫描存量文章
uv run scripts/mail_pipeline.py check-web-upgrades
# 增量扫描：跳过已是 web_canonical 的文章（大幅优化网络开销）
uv run scripts/mail_pipeline.py check-web-upgrades --pending-only
# 靶向单篇文章比对
uv run scripts/mail_pipeline.py check-web-upgrades 'raw/articles/2026-03-26_Breathing-KMeans_123.md'

# 3. 深度对比单篇差异 (Diff & Heading Tree)
# 针对归档库或暂存区文章输出章节目录对比与 Unified Diff
uv run scripts/mail_pipeline.py diff-web 'raw/articles/2026-03-26_Breathing-KMeans_123.md'
uv run scripts/mail_pipeline.py diff-web 'Clippings/emails/dailydoseofds/2026-09-18_xxx.md'

# 4. 安全升级与覆盖替换
# 预览升级差异（Dry-run 模式，不写盘）
uv run scripts/mail_pipeline.py upgrade-article 'raw/articles/xxx.md' --dry-run --diff
# 物理覆盖升级并打印差异
uv run scripts/mail_pipeline.py upgrade-article 'raw/articles/xxx.md' --diff
# 指定通道抓取 (auto: 默认4级容灾链路 / ghost: 纯Ghost API / jina: 直连Jina Reader)
uv run scripts/mail_pipeline.py upgrade-article 'raw/articles/xxx.md' --channel jina
```

## 筛选与入库约束

一封邮件可拆分为多篇独立文章。`route` 只生成待审 Markdown，**绝不表示同封邮件中的所有文章都应入库**。

1. `sync`、`route` 与 `run` 是可自动执行的**邮件同步阶段**：仅更新账本、读取已支持来源的邮件并生成待审 Markdown，绝不 Ingest。
2. 用户在 `SYNC_STATUS.md` 或来源目录中逐篇完成 Review，决定保留或删除；未选文章继续保持 `review`，或执行 `uv run scripts/mail_pipeline.py reject '<文章 ID>' --reason '<原因>'` 显式拒绝。
3. 即使文章状态为 `review`，Agent 也不得自行判断其应保留或执行 Ingest。只有用户完成 Review 后明确要求 Agent 入库指定文章，才可对该单篇文章执行 `AGENTS.md` 的完整 Ingest SOP。
4. Ingest 完成并将该文章归档至 `raw/articles/` 后，执行 `uv run scripts/mail_pipeline.py reconcile`；该命令只会逐篇回写已存在于 `raw/articles/` 的文章状态。

`run` 不会自动移动、Ingest 或写入 `wiki/`。

## 官网全量长文增强 (Web Canonical Enhancement)

### 1. 设计动机与分层定位

订阅邮件（如 Daily Dose of Data Science）正文往往只提供前置导读（Newsletter Teaser），截断了后续的核心算法推导、可运行 Python 代码块与高清示意图；而官方发布站点（如 Ghost CMS）则公开挂载了无删节的完整长文。

为了在自动化同步阶段直接沉淀高保真事实底座，管线在保留邮件元数据的前提下引入了**官网长文探测与拉取引擎**：
- **`web_canonical`（官网标准层）**：包含完整代码、公式、高清图集与分级标题的高质量长文。
- **`email_fallback`（邮件兜底层）**：邮件原生截断版，作为外部网络受限时的可靠保底。

### 2. 四级容灾与决议链路

抓取过程严格遵循四级防故障决议链，保证 100% 容灾，绝不因官网改版或网络波动阻断邮件主流程：

```text
1. Ghost API Slug 查询   -> 提取邮件内官方外链或将标题转为 Slug 进行精准探测
       ↓ (未命中)
2. Ghost NQL 模糊检索    -> 按标题核心词进行 Ghost Content API 过滤搜索
       ↓ (未命中/异常)
3. Jina Reader 降级      -> 通过 r.jina.ai 免渲染公开代理拉取长文 Markdown
       ↓ (仍失败)
4. 邮件原生 HTML 兜底     -> 降级为邮件解析正文，标记 content_tier: email_fallback
```

### 3. 富媒体与排版转换能力

Ghost 官方 HTML 解析器内置了专属的富媒体转换适配：
- **代码块与公式**：精准保留 `<pre><code>` 语言标记与缩进，不截断长代码。
- **图片与画廊**：支持单个 `<figure class="kg-image-card">` 与 `<figure class="kg-gallery-card">` 多图画廊排版。
- **视频嵌入**：自动将 Ghost `<video>` 嵌入标签解析为 Markdown 视频预览卡片。
- **表格保护**：自动净化表格单元格内的 `<br>` 与换行，防止破坏 Markdown 表格结构。

### 4. 存量文章无损升级与差异审查 SOP

对于早期已归档至 `raw/articles/` 或仍停留在待审区中的删节版邮件文章，推荐按以下四步精细化 SOP 完成对比、审查与无损升级：

1. **快速扫描与增量排查**：
   ```bash
   # 全量增量扫描：跳过已是 web_canonical 的文章（大幅优化网络开销与速度）
   uv run scripts/mail_pipeline.py check-web-upgrades --pending-only

   # 或针对单篇文章快速比对指标
   uv run scripts/mail_pipeline.py check-web-upgrades 'raw/articles/2026-03-26_Breathing-KMeans_123.md'
   ```
   输出对比指标（本地 vs 官网的字数、代码块数），给出 `强烈建议升级`、`已是官网长文` 或 `保持现状` 的明确建议。

2. **单篇深度差异审查 (Heading Tree & Diff)**：
   ```bash
   # 深度对比单篇差异：输出章节目录树对比与行级 Unified Diff 片段
   uv run scripts/mail_pipeline.py diff-web 'raw/articles/2026-03-26_Breathing-KMeans_123.md'
   ```
   直观比对新增的推导章节、算法步骤、公式图表与代码增补行，杜绝“盲盒式覆盖”。

3. **安全预览 (Dry-run 模式)**：
   ```bash
   # 模拟升级，在控制台高亮预览变更 Diff，绝不物理修改磁盘或账本
   uv run scripts/mail_pipeline.py upgrade-article 'raw/articles/2026-03-26_Breathing-KMeans_123.md' --dry-run --diff
   ```

4. **精准覆盖升级与通道决议**：
   ```bash
   # 执行物理覆盖升级（并输出变更 diff）
   uv run scripts/mail_pipeline.py upgrade-article 'raw/articles/2026-03-26_Breathing-KMeans_123.md' --diff

   # 若遇到官网特定限制，可指定抓取通道 (auto / ghost / jina)
   uv run scripts/mail_pipeline.py upgrade-article 'raw/articles/2026-03-26_Breathing-KMeans_123.md' --channel jina
   ```
   升级操作会自动完成：
   - 更新 Frontmatter：标记 `content_tier: "web_canonical"` 并注入 `canonical_url`；
   - 完整保留用户既有手动打上的 `tags:` 与业务标注；
   - 保留原正文顶部的邮件元信息头（发件人、日期、邮件主题等）；
   - 同步更新机器账本 `manifest.json` 中该文章的状态记录。

## 自动同步到本地

推荐在保存此 Vault 且已配置 IMAP 凭据（`~/.config/knowledge-bank/imap_credentials.json`）的本机上，用 macOS `launchd` 定时执行邮件同步。调度器只运行 `run`，因此自动化边界始终停留在「拉取 -> 路由 -> 生成待审 Markdown」；它不会选择文章、删除文章、移动至 `raw/` 或写入 `wiki/`。

```text
Gmail 新邮件或星标变更
  -> launchd 定时唤醒本机任务
  -> uv run scripts/mail_pipeline.py run
  -> Clippings/emails/<source_key>/*.md
  -> 用户在本地逐篇 Review
```

### macOS launchd（推荐）

仓库提供模板 [`scripts/launchd/com.parsonlee.knowledge-bank.mail-sync.plist`](../../../scripts/launchd/com.parsonlee.knowledge-bank.mail-sync.plist)。先用本机的绝对路径替换模板中的以下占位符：

- `__VAULT_PATH__`：本仓库的绝对路径；
- `__UV_PATH__`：执行 `command -v uv` 得到的路径；
- `__HTTP_PROXY__` / `__HTTPS_PROXY__` / `__ALL_PROXY__`：本机代理地址；没有代理需求时，删除模板中的六个代理环境变量条目。`launchd` 只传递代理地址，不负责启动代理客户端。
- 若希望后台自动同步时一并拉取官方完整长文，可在 plist 模板的 `ProgramArguments` 中 `run` 之后追加 `<string>--fetch-web</string>`。

随后将文件复制到 `~/Library/LaunchAgents/`，并加载任务：

```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.parsonlee.knowledge-bank.mail-sync.plist
launchctl kickstart -k gui/$(id -u)/com.parsonlee.knowledge-bank.mail-sync
```

模板默认每 30 分钟运行一次，并在登录后立即补跑一次。日志写入 `.pipeline/logs/`，可用下列命令检查任务和最近输出：

```bash
launchctl print gui/$(id -u)/com.parsonlee.knowledge-bank.mail-sync
tail -n 100 Clippings/emails/.pipeline/logs/mail-sync.err.log
```

修改周期或模板后，先卸载再重新加载：

```bash
launchctl bootout gui/$(id -u)/com.parsonlee.knowledge-bank.mail-sync
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.parsonlee.knowledge-bank.mail-sync.plist
```

每次脚本运行均以 UTC ISO-8601 时间戳写入 `START` 与 `END` 区块边界；区块内的结果与汇总不重复标记时间。错误写入独立的 stderr 区块，便于按运行批次阅读和检索。

> [!warning] 前提与边界
> 电脑休眠或关机时不会即时拉取；下次登录/唤醒后的下一次调度会补拉，`sync` 的差异账本会去重。`launchd` 环境没有交互式 shell 的 `PATH`，所以模板必须使用 `uv` 的绝对路径。IMAP 凭据（应用专用密码）存储于 `~/.config/knowledge-bank/imap_credentials.json`（权限 `600`），严禁提交到仓库或复制到 GitHub Actions Secret。

### 事件触发的取舍

Gmail API 的 Push Notification 需要 Google Cloud Pub/Sub 端点和持续运行的 Web 服务，并且通知只表示「邮箱有变化」，仍需调用同步接口拉取并去重。对于个人 Vault，这比每 30 分钟轮询的运维成本高，收益很小；当前不建议实现。

若未来需要接近实时的同步，可部署一个仅触发本机 `run` 的受认证 Webhook/队列消费者，或将本机任务频率调整为 5 分钟。无论采用哪一种，处理范围都必须保持在本节的自动同步边界内，Ingest 仍需用户逐篇 Review 后明确指令。

### GitHub Actions 说明

`.github/workflows/sync-clippings.yml` 是旧的 Gemini/Google Drive 管线，指向已移除的 `Clippings/DailyDoseOfDS/`，不能同步本机 Gmail，也不应继续作为邮件同步方案。保留本地 `launchd` 作为唯一自动拉取入口。
