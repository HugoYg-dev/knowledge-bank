# HANDOFF: Gmail 同步管线与 gws 方案交接

## 1. 目标与结论 (Goal & Status)
为本知识库（knowledge-bank）的 Gmail 邮件暂存管线（`Clippings/emails/`）提供长期稳定、免维护的自动化拉取能力。
**已全面完成改造：彻底摒弃依赖 7 天硬过期的 Google OAuth 2.0 Testing 模式及外部 `gws` CLI，切换至 Gmail 原生 IMAP 协议 +「应用专用密码 (App Password)」方案。**

---

## 2. 核心成果与技术落地 (Delivered Results)

### 2.1 鉴权与配置规范
- **凭据路径**：存储于本地受保护目录 `~/.config/knowledge-bank/imap_credentials.json`（权限 `600`，独立于 Git 仓库，确保密钥安全）；
- **永久有效**：只要不在 Google 账号中主动删除该应用专用密码，授权永久有效，彻底免去每 7 天手动重授权与弹窗打扰；
- **环境变量支持**：同时支持 `GMAIL_USER` 与 `GMAIL_APP_PASSWORD` 覆盖。

### 2.2 核心代码重构 (`scripts/mail_pipeline.py`)
- **解耦外部 CLI**：完全移除对系统 `gws` (Node.js CLI) 的调用，改用 Python 原生 `imaplib` + `PySocks`；
- **透明代理适配**：自动识别 `ALL_PROXY`（如 `socks5://127.0.0.1:7897`）、`HTTPS_PROXY` 和 `HTTP_PROXY`，无缝穿透本地代理连接 `imap.gmail.com:993`；
- **全链路账本兼容（X-GM-MSGID）**：
  - Gmail IMAP 的 `X-GM-MSGID` 扩展返回 64 位整型 ID，转换为十六进制（`f"{int(id):x}"`）后与原 Gmail REST API 的 Message ID **100% 一致**；
  - 既有 `manifest.json` 账本历史记录零损坏、零重复，实现无缝平滑切换；
- **上游解析器零修改**：通过 `BODY.PEEK[]` 获取 RFC822 原始字节流并以 base64url 编码塞入 `response["raw"]`，`scripts/mail_sources/dailydoseofds.py` 保持原样工作。

### 2.3 运维服务简化与瘦身
- **退役保活任务**：因不再存在 7 天过期限制，原每 4 小时轮询的 `gws_token_keepalive.sh` 脚本和 `com.parsonlee.knowledge-bank.token-keepalive.plist` 已被从 macOS `LaunchAgents` 中彻底卸载并清理；
- **保留主同步定时任务**：`com.parsonlee.knowledge-bank.mail-sync.plist` 保持原设定，每天 09:00 与 21:00 自动执行 `uv run scripts/mail_pipeline.py run`。

---

## 3. 验证情况 (Verification)

经端到端真实测试，全部命令均通过验证：
1. **IMAP 握手与鉴权**：连接 `imap.gmail.com:993` 成功，登录测试通过；
2. **星标拉取与账本比对 (`sync`)**：成功检索 69 封远端星标邮件，与本地 71 条账本记录正确对齐，耗时仅 2 秒；
3. **全流程执行 (`run`)**：`reconcile -> sync -> route` 单连接复用运行流畅，状态返回 `ok`；
4. **LaunchAgent 状态**：确认后台仅保留 `mail-sync` 任务，系统轮询与弹窗彻底归零。

---

## 4. 后续维护速查 (Cheat Sheet)

- **手动触发同步**：
  ```bash
  uv run scripts/mail_pipeline.py run
  ```
- **查看管线与文章状态**：
  ```bash
  uv run scripts/mail_pipeline.py status
  ```
- **配置文件位置**：
  `~/.config/knowledge-bank/imap_credentials.json`
