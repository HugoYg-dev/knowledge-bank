# HANDOFF: Gmail 同步管线与 gws 方案交接

## 1. 目标 (Goal)
为本知识库（knowledge-bank）的 Gmail 邮件暂存管线（`Clippings/emails/`）提供长期稳定、无人值守的自动化拉取能力，彻底解决 Google OAuth Testing 模式下 7 天 Refresh Token 硬过期导致的同步中断问题。

---

## 2. 当前进展 (Current Progress)

### 已完成工作
1. **深度排查技术根因**：
   - 明确了 Google OAuth 2.0 在 External + Testing 模式下的策略限制：服务端对 `refresh_token` 施加严格的 7 天生命周期（7-day TTL），任何纯客户端 API 轮询或临时 `access_token` 刷新均无法延长该生命周期。
   - 查证了先前 `scripts/gws_token_keepalive.sh` 脚本失效的原因：
     - `gws auth status` 输出了变化后的 JSON 结构，不再包含 `"token_valid": true` 字段，导致脚本误判或未能真实探测 API；
     - 轮询间隔设置过长（5 天 / 432000s），无法在 7 天窗口到期前有效捕获并预警；
     - 依赖简单的后台轮询无法突破服务端 7 天硬性吊销。
2. **优化现有 gws 机制**：
   - **重构健康探测脚本** (`scripts/gws_token_keepalive.sh`)：
     - 改为直接通过轻量 API (`getProfile`) 探测真实连通性与鉴权有效性；
     - 结合 `auth_state.json` 跟踪授权账期时间戳，当处于第 6 天（剩余时间不足 36 小时）时，主动推送 macOS 原生预警通知，提醒提前续期；
     - 当检测到过期（`invalid_grant` / `Token expired or revoked`）时，立即发送 macOS 桌面通知提醒重新授权。
   - **新增一键授权脚本** (`scripts/gws_reauth.sh`)：
     - 封装了代理环境变量配置与 `gws auth login -s gmail` 流程；
     - 授权成功后自动写入 `auth_state.json` 并触发一次邮件同步测试。
   - **优化 launchd 调度** (`com.parsonlee.knowledge-bank.token-keepalive.plist`)：
     - 将探测周期从 5 天缩短至 4 小时（14400s），确保及时捕获过期与预警；
     - 已重新加载至本机的 `~/Library/LaunchAgents/`。

---

## 3. 经验沉淀：有效与无效的方案对比

### ❌ 无效方案（请勿重复尝试）
- **客户端定时调用 API 保活 (Keepalive API ping)**：
  - 在 Google Cloud External + Testing 状态下，定时调用 API 只能刷新 1 小时有效期的 `access_token`，无法刷新 `refresh_token` 本身。
  - 到达 7 天绝对时间后，Google 服务端仍会强制将 `refresh_token` 吊销。
- **依赖 `gws auth status` 的字符串匹配**：
  - `gws` 的 JSON 结构会随版本迭代调整（例如当前已无 `token_valid`），必须以直接调用 Gmail API 探测结果作为判断真凭实据。

### ⚠️ 过渡优化方案（当前在用）
- **保留 `gws` + 主动健康探测 + 到期预警通知**：
  - 优点：无需改动现有的 `mail_pipeline.py` 代码。
  - 局限性：每 7 天仍需用户在浏览器中手动确认一次登录授权（通过运行 `bash scripts/gws_reauth.sh`）。

---

## 4. 一劳永逸的根本方案：Gmail IMAP + 应用专用密码 (App Password)

为了彻底摆脱 Google Cloud GCP、OAuth 2.0 刷新限制、Keyring 依赖以及 7 天过期的困扰，**最彻底、免维护的终极方案是改用 Gmail 原生 IMAP 协议配合「应用专用密码」**。

### 4.1 核心优势
1. **永久有效**：应用专用密码只要不在 Google 账号中主动删除，永不过期，不受 7 天、测试模式、OAuth 审核等任何政策影响。
2. **原生支持**：Python 标准库内置 `imaplib` 和 `email` 模块，无需额外依赖外部 CLI（如 `gws`）或 Node 运行时环境。
3. **隔离安全**：专用密码仅限邮件收发，独立于 Google 主密码，且仅对本机特定任务授权。

### 4.2 前置配置步骤（用户手动操作一次）
1. 打开 [Google 账号安全性页面](https://myaccount.google.com/security)。
2. 确认已开启「两步验证 (2-Step Verification)」。
3. 在搜索栏输入并进入 **「应用专用密码」(App Passwords)**（直接访问链接：`https://myaccount.google.com/apppasswords`）。
4. 创建一个新密码：
   - 应用名称填写：`knowledge-bank-mail`
   - 生成 16 位密码（形如 `abcd efgh ijkl mnop`）。
5. 在本地保存配置（例如以环境变量或存储于受保护的本地文件 `~/.config/knowledge-bank/imap_credentials.json`，切勿提交至 Git）：
   ```json
   {
     "email": "hugoyang1229@gmail.com",
     "app_password": "abcdefghijklmnop",
     "imap_server": "imap.gmail.com",
     "imap_port": 993
   }
   ```

### 4.3 迁移实现蓝图 (`scripts/mail_pipeline.py` 改造)

在 `scripts/mail_pipeline.py` 中，目前通过 `gws gmail users messages list` 拉取邮件：
```python
# 现状：依赖 gws CLI 子进程
subprocess.run(["gws", "gmail", "users", "messages", "list", "--params", json.dumps({"q": "is:starred"})], ...)
```

#### 替换为原生 IMAP 提取（伪代码与核心结构）：
```python
import imaplib
import email
from email.header import decode_header

def fetch_starred_emails_imap(account: str, app_password: str) -> list[dict]:
    """使用 IMAP 原生拉取所有星标邮件"""
    # 若有本地代理，可使用 socks 包装或设置代理环境变量
    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    mail.login(account, app_password)
    mail.select("INBOX")
    
    # 检索星标邮件（Gmail IMAP 对应 FLAGGED 标示）
    status, messages = mail.search(None, "FLAGGED")
    if status != "OK":
        return []
    
    email_ids = messages[0].split()
    results = []
    
    for eid in email_ids:
        # 获取邮件头部与正文
        res, msg_data = mail.fetch(eid, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                # 解析 Subject, From, Date, Body 并映射到现有 manifest 格式
                # ...
                
    mail.logout()
    return results
```

#### 保持管线后续阶段 100% 兼容：
- `manifest.json` 的存储格式（`id`、`sender`、`subject`、`date`、`remote_starred`）保持不变；
- 来源解析器（如 `mail_sources/dailydoseofds.py`）无需任何修改，输入仍然是标准的 HTML/Text 正文和元数据字典；
- 状态机（`unhandled`、`review`、`ingested`、`rejected`）和人工 Review SOP 完全不变。

---

## 5. 下一步行动建议 (Next Steps)

1. **日常维护（当前方案）**：
   - 留意 macOS 桌面通知。当弹出“Gmail 同步即将到期”时，终端运行：
     ```bash
     bash scripts/gws_reauth.sh
     ```
   - 按照弹出的浏览器提示完成一键重新授权即可续期 7 天。
2. **彻底改造（切换至一劳永逸方案）**：
   - 生成 Google 应用专用密码；
   - 派发任务给 Agent，参考本文档 §4 的设计，将 `scripts/mail_pipeline.py` 中的 `gws` 同步后端平滑重构为 `imaplib` 原生后端；
   - 卸载已无需要的 `token-keepalive` 定时任务。
