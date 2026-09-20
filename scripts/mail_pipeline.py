# /// script
# requires-python = ">=3.12"
# dependencies = ["beautifulsoup4>=4.12", "html2text>=2024.2.26", "PySocks>=1.7.1", "pyyaml>=6.0"]
# ///

"""多来源 Gmail 星标邮件同步、路由与文章状态对账（基于原生 IMAP + App Password）。

支持：
- Gmail IMAP 星标邮件拉取与账本同步
- 来源解析与待审文章生成（支持 --fetch-web 官网长文增强）
- fetch-web: 独立从官网抓取单篇全量长文
- check-web-upgrades: 扫描库内存量文章，比对官网长文版本
- upgrade-article: 拉取官网版本覆盖升级指定文章
- 逐篇对账与状态统计
"""

from __future__ import annotations

import argparse
import base64
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
import difflib
import email
from email.header import decode_header
from email.utils import parseaddr
import imaplib
import inspect
import json
import os
from pathlib import Path
import re
import shutil
import socket
import subprocess
import sys
import time
from typing import Any, Callable
import urllib.parse

try:
    import socks
except ImportError:
    socks = None
from mail_sources import dailydoseofds


ROOT = Path(__file__).resolve().parents[1]
EMAILS_DIR = ROOT / "Clippings" / "emails"
PIPELINE_DIR = EMAILS_DIR / ".pipeline"
MANIFEST_PATH = PIPELINE_DIR / "manifest.json"
STATUS_PATH = PIPELINE_DIR / "SYNC_STATUS.md"
INDEX_PATH = PIPELINE_DIR / "ARCHIVE_INDEX.md"
ARCHIVE_DIR = ROOT / "raw" / "articles"
LEGACY_STAGE = ROOT / "Clippings" / "DailyDoseOfDS"
CREDENTIALS_PATH = Path.home() / ".config" / "knowledge-bank" / "imap_credentials.json"
SCHEMA_VERSION = 2
IMAP_TIMEOUT_SECONDS = max(int(os.environ.get("IMAP_TIMEOUT_SECONDS", "30")), 1)


class PipelineError(RuntimeError):
    pass


@dataclass(frozen=True)
class Source:
    key: str
    addresses: tuple[str, ...]
    domains: tuple[str, ...]
    parser: Callable[..., tuple[dict[str, str], list[dict[str, Any]]]]


SOURCES = (
    Source(
        key="dailydoseofds",
        addresses=("avi@dailydoseofds.com",),
        domains=("dailydoseofds.com",),
        parser=dailydoseofds.parse,
    ),
)
SOURCES_BY_KEY = {source.key: source for source in SOURCES}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def log_line(message: str, *, error: bool = False) -> None:
    """Write a readable line inside the current launchd log block."""
    stream = sys.stderr if error else sys.stdout
    normalized = " | ".join(str(message).splitlines())
    print(normalized, file=stream, flush=True)


def log_block(command: str, event: str, *, error: bool = False) -> None:
    """Mark one complete pipeline invocation in launchd's append-only logs."""
    stream = sys.stderr if error else sys.stdout
    marker = "=" * 72
    print(f"\n{marker}", file=stream, flush=True)
    print(f"[{now_iso()}] mail_pipeline command={command} event={event}", file=stream, flush=True)
    print(marker, file=stream, flush=True)


def empty_manifest() -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "updated_at": now_iso(),
        "last_sync_at": None,
        "emails": {},
    }


def load_manifest(path: Path | None = None) -> dict[str, Any]:
    if path is None:
        path = MANIFEST_PATH
    if not path.exists():
        return empty_manifest()
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != SCHEMA_VERSION or not isinstance(data.get("emails"), dict):
        raise PipelineError(f"不支持的共享 manifest 格式: {path}")
    return data


def save_manifest(data: dict[str, Any], path: Path | None = None) -> None:
    if path is None:
        path = MANIFEST_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = now_iso()
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def new_email_record(message_id: str) -> dict[str, Any]:
    return {
        "id": message_id,
        "lifecycle": "discovered",
        "routing": "pending",
        "source_key": None,
        "remote_starred": None,
        "first_seen_at": None,
        "last_seen_at": None,
        "sender": "",
        "subject": "",
        "date": "",
        "attempts": 0,
        "last_error": None,
        "reason": None,
        "articles": [],
    }


def decode_mime_header(header_value: str) -> str:
    """Safely decode RFC 2047 MIME-encoded headers."""
    if not header_value:
        return ""
    try:
        parts = decode_header(header_value)
        decoded: list[str] = []
        for content, encoding in parts:
            if isinstance(content, bytes):
                decoded.append(content.decode(encoding or "utf-8", errors="replace"))
            else:
                decoded.append(str(content))
        return "".join(decoded).strip()
    except Exception:
        return str(header_value).strip()


def load_imap_credentials() -> dict[str, Any]:
    """优先使用环境变量，其次读取 ~/.config/knowledge-bank/imap_credentials.json。"""
    env_user = os.environ.get("GMAIL_USER")
    env_pwd = os.environ.get("GMAIL_APP_PASSWORD")
    if env_user and env_pwd:
        return {
            "email": env_user,
            "app_password": env_pwd,
            "imap_server": os.environ.get("IMAP_SERVER", "imap.gmail.com"),
            "imap_port": int(os.environ.get("IMAP_PORT", "993")),
        }
    if CREDENTIALS_PATH.exists():
        try:
            data = json.loads(CREDENTIALS_PATH.read_text(encoding="utf-8"))
            if data.get("email") and data.get("app_password"):
                return {
                    "email": data["email"],
                    "app_password": data["app_password"],
                    "imap_server": data.get("imap_server", "imap.gmail.com"),
                    "imap_port": int(data.get("imap_port", 993)),
                }
        except Exception as exc:
            raise PipelineError(f"读取 IMAP 凭证文件失败: {exc}") from exc
    raise PipelineError(
        f"未找到有效 Gmail IMAP 凭据。请在 {CREDENTIALS_PATH} 中配置或设置环境变量 GMAIL_USER 和 GMAIL_APP_PASSWORD。"
    )


def configure_proxy() -> None:
    """若存在 ALL_PROXY / HTTPS_PROXY / HTTP_PROXY，设置全局 socket 走 SOCKS 或 HTTP 代理。"""
    proxy_url = os.environ.get("ALL_PROXY") or os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY")
    if not proxy_url or socks is None:
        return
    parsed = urllib.parse.urlsplit(proxy_url)
    scheme = parsed.scheme.casefold()
    if "socks5" in scheme:
        proxy_type = socks.SOCKS5
    elif "socks4" in scheme:
        proxy_type = socks.SOCKS4
    elif "http" in scheme:
        proxy_type = socks.HTTP
    else:
        return
    host = parsed.hostname
    port = parsed.port or (1080 if proxy_type == socks.SOCKS5 else 8080)
    socks.set_default_proxy(proxy_type, host, port, username=parsed.username, password=parsed.password)
    socket.socket = socks.socksocket


class GmailImapClient:
    """封装 Gmail 原生 IMAP 连接、星标邮件发现与基于 X-GM-MSGID 的邮件提取。"""

    def __init__(self, credentials: dict[str, Any] | None = None) -> None:
        self.credentials = credentials or load_imap_credentials()
        self.mail: imaplib.IMAP4_SSL | None = None
        self._starred_box: str | None = None
        self._all_box: str | None = None

    def connect(self) -> None:
        if self.mail is not None:
            return
        configure_proxy()
        try:
            self.mail = imaplib.IMAP4_SSL(
                self.credentials["imap_server"],
                self.credentials["imap_port"],
            )
            if self.mail.sock:
                self.mail.sock.settimeout(IMAP_TIMEOUT_SECONDS)
            self.mail.login(self.credentials["email"], self.credentials["app_password"])
        except imaplib.IMAP4.error as exc:
            try:
                subprocess.run(
                    [
                        "osascript",
                        "-e",
                        'display notification "Gmail IMAP 登录失败，请检查应用专用密码"'
                        ' with title "⚠️ 邮件同步" subtitle "knowledge-bank"',
                    ],
                    timeout=5,
                    capture_output=True,
                )
            except Exception:
                pass
            raise PipelineError(f"Gmail IMAP 登录失败: {exc}") from exc
        except Exception as exc:
            raise PipelineError(f"连接 Gmail IMAP 失败: {exc}") from exc

    def close(self) -> None:
        if self.mail is not None:
            try:
                self.mail.logout()
            except Exception:
                pass
            self.mail = None

    def __enter__(self) -> GmailImapClient:
        self.connect()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    def _get_special_mailbox(self, flag: str, fallback_candidates: tuple[str, ...]) -> str:
        self.connect()
        assert self.mail is not None
        typ, mailboxes = self.mail.list()
        if typ == "OK" and mailboxes:
            for b in mailboxes:
                name_str = b.decode("utf-8", errors="ignore")
                if flag.casefold() in name_str.casefold():
                    return name_str.split(' "/" ')[-1].strip('"')
                for candidate in fallback_candidates:
                    if candidate.casefold() in name_str.casefold():
                        return name_str.split(' "/" ')[-1].strip('"')
        return fallback_candidates[0]

    def get_starred_mailbox(self) -> str:
        if not self._starred_box:
            self._starred_box = self._get_special_mailbox(r"\Flagged", ('"[Gmail]/Starred"', '"[Gmail]/&XfJSoGYfaAc-"'))
        return self._starred_box

    def get_all_mail_mailbox(self) -> str:
        if not self._all_box:
            self._all_box = self._get_special_mailbox(r"\All", ('"[Gmail]/All Mail"', '"[Gmail]/&YkBnCZCuTvY-"'))
        return self._all_box

    def list_starred_messages(self) -> list[dict[str, str]]:
        """获取星标邮箱中的全部邮件，通过 X-GM-MSGID 映射为 16 进制 Message ID。"""
        self.connect()
        assert self.mail is not None
        box = self.get_starred_mailbox()
        status, _ = self.mail.select(box, readonly=True)
        if status != "OK":
            raise PipelineError(f"选择星标邮箱失败: {box}")

        typ, search_res = self.mail.uid("SEARCH", "ALL")
        if typ != "OK" or not search_res or not search_res[0]:
            return []

        uids = search_res[0].split()
        results: list[dict[str, str]] = []

        batch_size = 50
        for i in range(0, len(uids), batch_size):
            batch = uids[i : i + batch_size]
            uid_set = b",".join(batch)
            fetch_typ, fetch_res = self.mail.uid(
                "FETCH", uid_set, "(X-GM-MSGID BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])"
            )
            if fetch_typ != "OK":
                continue

            for part in fetch_res:
                if not isinstance(part, tuple) or len(part) < 2:
                    continue
                header_meta = part[0].decode("utf-8", errors="ignore")
                m = re.search(r"X-GM-MSGID\s+(\d+)", header_meta)
                if not m:
                    continue
                msgid_dec = int(m.group(1))
                hex_id = f"{msgid_dec:x}"

                raw_header = part[1]
                msg = email.message_from_bytes(raw_header)
                sender = decode_mime_header(msg.get("From", ""))
                subject = decode_mime_header(msg.get("Subject", ""))
                date_str = decode_mime_header(msg.get("Date", ""))

                results.append(
                    {
                        "id": hex_id,
                        "sender": sender,
                        "subject": subject,
                        "date": date_str,
                    }
                )
        return results

    def fetch_raw_message(self, message_id: str) -> dict[str, Any]:
        """按 message_id (hex) 提取完整 RFC822 邮件内容，并以 base64url 格式返回包装字典。"""
        self.connect()
        assert self.mail is not None
        dec_id = int(message_id, 16)

        all_box = self.get_all_mail_mailbox()
        self.mail.select(all_box, readonly=True)
        typ, data = self.mail.uid("SEARCH", "X-GM-MSGID", str(dec_id))
        uids = data[0].split() if (typ == "OK" and data and data[0]) else []

        if not uids:
            star_box = self.get_starred_mailbox()
            self.mail.select(star_box, readonly=True)
            typ, data = self.mail.uid("SEARCH", "X-GM-MSGID", str(dec_id))
            uids = data[0].split() if (typ == "OK" and data and data[0]) else []

        if not uids:
            raise PipelineError(f"未在邮箱中找到对应邮件: message_id={message_id}")

        uid = uids[0]
        fetch_typ, fetch_res = self.mail.uid("FETCH", uid, "(BODY.PEEK[])")
        if fetch_typ != "OK":
            raise PipelineError(f"提取邮件内容失败: message_id={message_id}, uid={uid}")

        raw_bytes = b""
        for part in fetch_res:
            if isinstance(part, tuple) and len(part) >= 2:
                raw_bytes = part[1]
                break

        if not raw_bytes:
            raise PipelineError(f"提取的邮件内容为空: message_id={message_id}")

        raw_b64 = base64.urlsafe_b64encode(raw_bytes).decode("ascii")
        return {"raw": raw_b64}


def source_key_for_sender(sender: str) -> str | None:
    address = parseaddr(sender)[1].casefold()
    domain = address.rsplit("@", 1)[-1] if "@" in address else ""
    for source in SOURCES:
        if address in source.addresses or domain in source.domains:
            return source.key
    return None


def sync(data: dict[str, Any], client: GmailImapClient | None = None) -> tuple[int, int]:
    should_close = False
    if client is None:
        client = GmailImapClient()
        client.connect()
        should_close = True

    try:
        remote = client.list_starred_messages()
        timestamp = now_iso()
        remote_ids = {item["id"] for item in remote}
        remote_by_id = {item["id"]: item for item in remote}
        new_count = 0
        for message_id in remote_ids:
            record = data["emails"].get(message_id)
            if record is None:
                record = new_email_record(message_id)
                record["first_seen_at"] = timestamp
                data["emails"][message_id] = record
                new_count += 1
            record["remote_starred"] = True
            record["last_seen_at"] = timestamp

            meta = remote_by_id[message_id]
            if not record.get("sender") and meta.get("sender"):
                record["sender"] = meta["sender"]
            if not record.get("subject") and meta.get("subject"):
                record["subject"] = meta["subject"]
            if not record.get("date") and meta.get("date"):
                record["date"] = meta["date"]

            if record.get("source_key") is None:
                record["source_key"] = source_key_for_sender(record.get("sender", ""))
            if record["source_key"] is None and record["lifecycle"] == "discovered":
                record["routing"] = "unhandled"
                record["lifecycle"] = "unhandled"
                record["reason"] = "no_registered_parser"

        for message_id, record in data["emails"].items():
            if message_id not in remote_ids:
                record["remote_starred"] = False
        data["last_sync_at"] = timestamp
        return len(remote_ids), new_count
    finally:
        if should_close:
            client.close()


def clean_filename(title: str) -> str:
    title = re.sub(r'[\\/*?:"<>|]', "", title).strip()
    return re.sub(r"\s+", "-", title) or "untitled"


def article_filename(formatted_date: str, title: str, message_id: str) -> str:
    return f"{formatted_date}_{clean_filename(title)}_{message_id}.md"


def update_email_lifecycle(record: dict[str, Any]) -> None:
    if record.get("routing") == "failed":
        record["lifecycle"] = "failed"
        return

    articles = record.get("articles", [])
    if any(article.get("status") == "review" for article in articles):
        record["lifecycle"] = "review"
    elif any(article.get("status") == "ingested" for article in articles):
        record["lifecycle"] = "ingested"
    elif articles:
        record["lifecycle"] = "ignored"
    elif record.get("routing") == "unhandled":
        record["lifecycle"] = "unhandled"
    else:
        record["lifecycle"] = "ignored"


def route(
    data: dict[str, Any],
    client: GmailImapClient | None = None,
    fetch_web: bool = False,
) -> tuple[int, int]:
    processed = article_count = 0
    candidates = [
        record
        for record in data["emails"].values()
        if record.get("source_key") in SOURCES_BY_KEY
        and record["lifecycle"] in {"discovered", "failed"}
        and record.get("remote_starred") is not False
    ]
    if not candidates:
        return 0, 0

    should_close = False
    if client is None:
        client = GmailImapClient()
        client.connect()
        should_close = True

    try:
        for record in sorted(candidates, key=lambda item: item["id"]):
            source = SOURCES_BY_KEY[record["source_key"]]
            record["attempts"] += 1
            try:
                response = client.fetch_raw_message(record["id"])
                sig = inspect.signature(source.parser)
                if "fetch_web" in sig.parameters:
                    metadata, parsed_articles = source.parser(record["id"], response, fetch_web=fetch_web)
                else:
                    metadata, parsed_articles = source.parser(record["id"], response)

                record.update({key: metadata[key] for key in ("sender", "subject", "date")})
                record["articles"] = []
                source_dir = EMAILS_DIR / source.key
                source_dir.mkdir(parents=True, exist_ok=True)
                for index, article in enumerate(parsed_articles, 1):
                    article_id = f"{record['id']}:{index}"
                    filename = article_filename(metadata["formatted_date"], article["title"], record["id"])
                    staging_path = source_dir / filename
                    if staging_path.exists():
                        raise PipelineError(f"待审文章文件已存在: {staging_path}")
                    safe_title = article["title"].replace('"', '\\"')
                    safe_subject = metadata["subject"].replace('"', '\\"')
                    safe_sender = metadata["sender"].replace('"', '\\"')
                    canonical_url = article.get("canonical_url")
                    content_tier = article.get("content_tier", "email_fallback")
                    canonical_frontmatter = f'canonical_url: "{canonical_url}"\n' if canonical_url else ""
                    canonical_line = f"- **官网长文**: {canonical_url}\n" if canonical_url else ""

                    header = (
                        "---\n"
                        f'title: "{safe_title}"\n'
                        f'source_key: "{source.key}"\n'
                        f'email_subject: "{safe_subject}"\n'
                        f'email_sender: "{safe_sender}"\n'
                        f'email_date: "{metadata["date"]}"\n'
                        f'email_id: "{record["id"]}"\n'
                        f'article_id: "{article_id}"\n'
                        f'published: "{metadata["formatted_date"]}"\n'
                        f'content_tier: "{content_tier}"\n'
                        f"{canonical_frontmatter}"
                        "tags: []\n"
                        "---\n\n"
                        f"# {article['title']}\n\n"
                        f"- **邮件来源**: {source.key}\n"
                        f"- **原邮件主题**: {metadata['subject']}\n"
                        f"- **发送人**: {metadata['sender']}\n"
                        f"- **日期**: {metadata['date']}\n"
                        f"- **邮件 ID**: {record['id']}\n"
                        f"- **文章 ID**: {article_id}\n"
                        f"- **内容层级**: {content_tier}\n"
                        f"{canonical_line}\n---\n\n"
                    )
                    staging_path.write_text(header + article["body"], encoding="utf-8")
                    record["articles"].append(
                        {
                            "id": article_id,
                            "title": article["title"],
                            "source_key": source.key,
                            "file": filename,
                            "staging_file": f"{source.key}/{filename}",
                            "canonical_url": canonical_url,
                            "content_tier": content_tier,
                            "status": "review",
                            "reason": None,
                        }
                    )
                    article_count += 1
                record["routing"] = "parsed"
                record["last_error"] = None
                record["reason"] = None if parsed_articles else "parser_returned_no_articles"
                update_email_lifecycle(record)
                processed += 1
            except Exception as exc:
                record["lifecycle"] = "failed"
                record["routing"] = "failed"
                record["last_error"] = str(exc)
        return processed, article_count
    finally:
        if should_close:
            client.close()


def reconcile(data: dict[str, Any]) -> int:
    reconciled = 0
    for record in data["emails"].values():
        for article in record.get("articles", []):
            if not article.get("file"):
                continue
            archived_file = ARCHIVE_DIR / article["file"]
            if archived_file.exists():
                if article.get("status") != "ingested":
                    article["status"] = "ingested"
                    article["reason"] = None
                    reconciled += 1
                try:
                    raw_text = archived_file.read_text(encoding="utf-8")
                    if "content_tier:" in raw_text:
                        m = re.search(r'content_tier:\s*["\']?(.*?)["\']?$', raw_text, re.MULTILINE)
                        if m:
                            article["content_tier"] = m.group(1).strip()
                    if "canonical_url:" in raw_text:
                        m = re.search(r'canonical_url:\s*["\']?(.*?)["\']?$', raw_text, re.MULTILINE)
                        if m:
                            article["canonical_url"] = m.group(1).strip()
                except Exception:
                    pass
            elif article.get("status") == "review" and not (EMAILS_DIR / article.get("staging_file", "")).exists():
                article["status"] = "rejected"
                article["reason"] = "manual_delete"
        update_email_lifecycle(record)
    return reconciled


def reject_article(data: dict[str, Any], article_id: str, reason: str) -> None:
    for record in data["emails"].values():
        for article in record.get("articles", []):
            if article.get("id") != article_id:
                continue
            if article.get("status") != "review":
                raise PipelineError(f"文章不是待审状态: {article_id}")
            staging_file = article.get("staging_file")
            if staging_file:
                (EMAILS_DIR / staging_file).unlink(missing_ok=True)
            article["status"] = "rejected"
            article["reason"] = reason
            update_email_lifecycle(record)
            return
    raise PipelineError(f"未找到文章: {article_id}")


def fetch_web_article(target: str, source_key: str = "dailydoseofds") -> Path:
    """从官网直接抓取单篇全量长文并生成待审文档。"""
    if source_key != "dailydoseofds":
        raise PipelineError(f"目前仅 dailydoseofds 支持 fetch-web，未知来源: {source_key}")
    slug = dailydoseofds.extract_slug_from_url(target) or dailydoseofds.slugify(target)
    if not slug:
        raise PipelineError(f"无法从目标中提取有效 Slug: {target}")

    candidate_urls = [target] if target.startswith("http") else None
    post = dailydoseofds.fetch_canonical_article(title=slug, candidate_urls=candidate_urls)
    if not post:
        raise PipelineError(f"未能从官网成功获取文章: target={target}, slug={slug}")

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    pub_date = post.get("published_at", "")[:10] or today
    title = post.get("title") or slug
    filename = f"{pub_date}_{clean_filename(title)}_web.md"
    target_dir = EMAILS_DIR / source_key
    target_dir.mkdir(parents=True, exist_ok=True)
    out_path = target_dir / filename

    safe_title = title.replace('"', '\\"')
    header = (
        "---\n"
        f'title: "{safe_title}"\n'
        f'source_key: "{source_key}"\n'
        f'canonical_url: "{post["canonical_url"]}"\n'
        f'content_tier: "web_canonical"\n'
        f'published: "{pub_date}"\n'
        f'article_id: "web:{slug}"\n'
        "tags: []\n"
        "---\n\n"
        f"# {title}\n\n"
        f"- **来源**: {source_key} (官网直接抓取)\n"
        f"- **官网长文**: {post['canonical_url']}\n"
        f"- **抓取日期**: {today}\n"
        f"- **发布日期**: {pub_date}\n"
        f"- **内容层级**: web_canonical\n\n---\n\n"
    )
    out_path.write_text(header + post["body"] + "\n", encoding="utf-8")
    return out_path


def count_code_blocks(text: str) -> int:
    return len(re.findall(r"^```", text, re.MULTILINE)) // 2


def extract_headings(text: str) -> list[str]:
    """提取 Markdown 正文中的标题列表 (如 '# Title', '## Subheading')。"""
    return [
        line.strip()
        for line in text.splitlines()
        if re.match(r"^#{1,6}\s+", line.strip())
    ]


def resolve_target_article(target: str, data: dict[str, Any] | None = None) -> Path:
    """解析目标文件路径（支持绝对路径、相对路径、文件名或文章 ID）。"""
    target_path = Path(target)
    if not target_path.is_absolute():
        if (ROOT / target_path).exists():
            return ROOT / target_path
        elif (ARCHIVE_DIR / target_path.name).exists():
            return ARCHIVE_DIR / target_path.name
        elif (EMAILS_DIR / "dailydoseofds" / target_path.name).exists():
            return EMAILS_DIR / "dailydoseofds" / target_path.name
        elif data:
            for record in data.get("emails", {}).values():
                for art in record.get("articles", []):
                    if art.get("id") == target:
                        f_name = art.get("file")
                        if f_name and (ARCHIVE_DIR / f_name).exists():
                            return ARCHIVE_DIR / f_name
                        elif art.get("staging_file") and (EMAILS_DIR / art["staging_file"]).exists():
                            return EMAILS_DIR / art["staging_file"]
    if target_path.exists():
        return target_path
    raise PipelineError(f"未找到待处理文章文件或有效文章 ID: {target}")


def check_web_upgrades(
    source_key: str = "dailydoseofds",
    target: str | None = None,
    pending_only: bool = False,
    data: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """比对本地文章与官网长文版本并生成差异清单。

    支持：
    - target 指定单篇（文件路径或文章 ID）；
    - pending_only: 若已是 web_canonical 则跳过远端网络请求，大幅提升批量检查性能。
    """
    results: list[dict[str, Any]] = []

    candidate_files: list[Path] = []
    if target:
        candidate_files = [resolve_target_article(target, data)]
    elif ARCHIVE_DIR.exists():
        candidate_files = sorted(ARCHIVE_DIR.glob("*.md"))

    for file_path in candidate_files:
        content = file_path.read_text(encoding="utf-8")
        fm_match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        if not fm_match:
            continue
        fm_text = fm_match.group(1)
        if f'source_key: "{source_key}"' not in fm_text and f"source_key: {source_key}" not in fm_text:
            continue

        title_m = re.search(r'title:\s*["\']?(.*?)["\']?$', fm_text, re.MULTILINE)
        title = title_m.group(1) if title_m else file_path.stem
        tier_m = re.search(r'content_tier:\s*["\']?(.*?)["\']?$', fm_text, re.MULTILINE)
        current_tier = tier_m.group(1).strip() if tier_m else "email_fallback"
        url_m = re.search(r'canonical_url:\s*["\']?(.*?)["\']?$', fm_text, re.MULTILINE)
        canonical_url = url_m.group(1).strip() if url_m else None

        local_body = content[fm_match.end():]
        local_chars = len(local_body)
        local_codes = count_code_blocks(local_body)

        # 增量优化：若指定了 pending_only 且当前已是官网长文，则跳过耗时的网络探测
        if pending_only and current_tier == "web_canonical":
            results.append({
                "file": file_path.name,
                "title": title,
                "local_chars": local_chars,
                "local_codes": local_codes,
                "web_chars": local_chars,
                "web_codes": local_codes,
                "current_tier": current_tier,
                "status": "up_to_date",
                "recommendation": "已是官网长文 (已跳过网络检测)",
                "canonical_url": canonical_url,
            })
            continue

        target_urls = [canonical_url] if canonical_url else None
        web_post = dailydoseofds.fetch_canonical_article(title=title, candidate_urls=target_urls)
        if not web_post:
            results.append({
                "file": file_path.name,
                "title": title,
                "local_chars": local_chars,
                "local_codes": local_codes,
                "web_chars": 0,
                "web_codes": 0,
                "current_tier": current_tier,
                "status": "not_found_on_web",
                "recommendation": "保持现状 (官网未收录)",
            })
            continue

        web_body = web_post.get("body", "")
        web_chars = len(web_body)
        web_codes = count_code_blocks(web_body)

        is_upgrade_needed = False
        reason_parts = []
        if current_tier != "web_canonical":
            if web_codes > local_codes:
                is_upgrade_needed = True
                reason_parts.append(f"代码块({local_codes}->{web_codes})")
            if web_chars > local_chars * 1.3:
                is_upgrade_needed = True
                reason_parts.append(f"篇幅扩充({local_chars}->{web_chars})")

        if is_upgrade_needed:
            rec = f"强烈建议升级 ({', '.join(reason_parts)})"
            status = "upgrade_available"
        elif current_tier == "web_canonical":
            rec = "已是官网长文"
            status = "up_to_date"
        else:
            rec = "内容基本一致"
            status = "similar"

        results.append({
            "file": file_path.name,
            "title": title,
            "local_chars": local_chars,
            "local_codes": local_codes,
            "web_chars": web_chars,
            "web_codes": web_codes,
            "current_tier": current_tier,
            "status": status,
            "recommendation": rec,
            "canonical_url": web_post.get("canonical_url"),
        })

    return results


def diff_web_article(
    target: str,
    source_key: str = "dailydoseofds",
    channel: str = "auto",
    data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """比对单篇本地文章与官网长文版本，生成详细结构差异与 Diff。"""
    target_path = resolve_target_article(target, data)
    content = target_path.read_text(encoding="utf-8")
    fm_match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not fm_match:
        raise PipelineError(f"文件缺少有效 YAML Frontmatter: {target_path}")

    fm_text = fm_match.group(1)
    title_m = re.search(r'title:\s*["\']?(.*?)["\']?$', fm_text, re.MULTILINE)
    title = title_m.group(1) if title_m else target_path.stem
    tier_m = re.search(r'content_tier:\s*["\']?(.*?)["\']?$', fm_text, re.MULTILINE)
    current_tier = tier_m.group(1).strip() if tier_m else "email_fallback"
    url_m = re.search(r'canonical_url:\s*["\']?(.*?)["\']?$', fm_text, re.MULTILINE)
    canonical_url = url_m.group(1).strip() if url_m else None

    local_body = content[fm_match.end():]
    divider_m = re.search(r"\n---\n\n", local_body)
    pure_local_body = local_body[divider_m.end():] if divider_m else local_body

    candidate_urls = [canonical_url] if canonical_url else None
    web_post = dailydoseofds.fetch_canonical_article(
        title=title,
        candidate_urls=candidate_urls,
        channel=channel,
    )
    if not web_post:
        raise PipelineError(f"未能从官网拉取到对应长文: title='{title}'")

    web_body = web_post.get("body", "")
    local_headings = extract_headings(pure_local_body)
    web_headings = extract_headings(web_body)

    local_lines = pure_local_body.splitlines(keepends=True)
    web_lines = web_body.splitlines(keepends=True)
    diff = list(
        difflib.unified_diff(
            local_lines,
            web_lines,
            fromfile=f"local:{target_path.name}",
            tofile=f"web:{web_post.get('canonical_url', 'canonical')}",
            n=3,
        )
    )

    return {
        "file": target_path.name,
        "path": str(target_path),
        "title": title,
        "current_tier": current_tier,
        "canonical_url": web_post.get("canonical_url"),
        "local_chars": len(pure_local_body),
        "web_chars": len(web_body),
        "local_codes": count_code_blocks(pure_local_body),
        "web_codes": count_code_blocks(web_body),
        "local_headings": local_headings,
        "web_headings": web_headings,
        "diff_lines": diff,
    }


def upgrade_article(
    data: dict[str, Any],
    target: str,
    force: bool = False,
    dry_run: bool = False,
    show_diff: bool = False,
    channel: str = "auto",
) -> Path:
    """拉取官网全量版本覆盖升级指定文章文件。

    支持：
    - dry_run: 仅模拟计算，不写盘不改 manifest；
    - show_diff: 打印变更前后的 unified diff；
    - channel: 指定抓取策略通道 ("auto", "ghost", "jina")。
    """
    target_path = resolve_target_article(target, data)
    content = target_path.read_text(encoding="utf-8")
    fm_match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not fm_match:
        raise PipelineError(f"文件缺少有效 YAML Frontmatter: {target_path}")

    fm_text = fm_match.group(1)
    tier_m = re.search(r'content_tier:\s*["\']?(.*?)["\']?$', fm_text, re.MULTILINE)
    current_tier = tier_m.group(1).strip() if tier_m else "email_fallback"
    if current_tier == "web_canonical" and not force:
        log_line(f"文章已是 web_canonical 且未指定 --force，跳过升级: {target_path.name}")
        return target_path

    title_m = re.search(r'title:\s*["\']?(.*?)["\']?$', fm_text, re.MULTILINE)
    title = title_m.group(1) if title_m else target_path.stem
    url_m = re.search(r'canonical_url:\s*["\']?(.*?)["\']?$', fm_text, re.MULTILINE)
    candidate_urls = [url_m.group(1).strip()] if url_m and url_m.group(1) else None

    web_post = dailydoseofds.fetch_canonical_article(
        title=title,
        candidate_urls=candidate_urls,
        channel=channel,
    )
    if not web_post:
        raise PipelineError(f"未能从官网拉取到对应文章: title='{title}'")

    new_canonical_url = web_post["canonical_url"]
    if "content_tier:" in fm_text:
        new_fm_text = re.sub(r'content_tier:.*$', 'content_tier: "web_canonical"', fm_text, flags=re.MULTILINE)
    else:
        new_fm_text = fm_text + '\ncontent_tier: "web_canonical"'

    if "canonical_url:" in new_fm_text:
        new_fm_text = re.sub(r'canonical_url:.*$', f'canonical_url: "{new_canonical_url}"', new_fm_text, flags=re.MULTILINE)
    else:
        new_fm_text += f'\ncanonical_url: "{new_canonical_url}"'

    new_frontmatter = f"---\n{new_fm_text.strip()}\n---\n\n"

    # 保留原头部邮件信息（若有）
    body_tail = content[fm_match.end():]
    divider_m = re.search(r"\n---\n\n", body_tail)
    header_meta = body_tail[:divider_m.start()] if divider_m else ""

    # 若头部元信息中没有官网长文链接，则追加
    if header_meta and "官网长文" not in header_meta:
        header_meta = header_meta.rstrip() + f"\n- **官网长文**: {new_canonical_url}\n- **内容层级**: web_canonical"

    new_full_content = (
        new_frontmatter + (header_meta.strip() + "\n\n---\n\n" if header_meta else "") + web_post["body"] + "\n"
    )

    if show_diff or dry_run:
        diff = list(
            difflib.unified_diff(
                content.splitlines(keepends=True),
                new_full_content.splitlines(keepends=True),
                fromfile=f"before:{target_path.name}",
                tofile=f"after:{target_path.name}",
                n=3,
            )
        )
        print(f"\n--- Unified Diff for {target_path.name} ---")
        if diff:
            print("".join(diff[:60]))
            if len(diff) > 60:
                print(f"... [Diff 截断显示，总计 {len(diff)} 行] ...\n")
        else:
            print("内容完全一致，无差异。\n")

    if dry_run:
        log_line(f"[Dry-run] 升级预演完成，未物理写入: {target_path.name}")
        return target_path

    target_path.write_text(new_full_content, encoding="utf-8")

    # 同步更新 manifest
    updated_manifest = False
    for record in data.get("emails", {}).values():
        for article in record.get("articles", []):
            if (
                article.get("file") == target_path.name
                or article.get("staging_file") == f"dailydoseofds/{target_path.name}"
            ):
                article["content_tier"] = "web_canonical"
                article["canonical_url"] = new_canonical_url
                updated_manifest = True
    if updated_manifest:
        save_manifest(data)

    return target_path


def rebuild_index(data: dict[str, Any]) -> None:
    articles = [
        (record, article)
        for record in data["emails"].values()
        for article in record.get("articles", [])
        if article.get("status") == "ingested" and article.get("file") and (ARCHIVE_DIR / article["file"]).exists()
    ]
    articles.sort(key=lambda item: item[1]["file"], reverse=True)
    lines = [
        "# 邮件订阅文章索引\n\n",
        f"已进入 `raw/articles` 的邮件订阅文章共 **{len(articles)}** 篇。\n\n",
        "| 序号 | 来源 | 文章标题 | 发送人 | 日期 | 链接 |\n",
        "| --- | --- | --- | --- | --- | --- |\n",
    ]
    for index, (record, article) in enumerate(articles, 1):
        title = article["title"].replace("|", "\\|")
        sender = record.get("sender", "").replace("|", "\\|")
        lines.append(
            f"| {index} | {article.get('source_key', '')} | {title} | {sender} | {record.get('date', '')} | [查看文章](../../../raw/articles/{article['file']}) |\n"
        )
    INDEX_PATH.write_text("".join(lines), encoding="utf-8")


def rebuild_status(data: dict[str, Any]) -> None:
    records = list(data["emails"].values())
    lifecycle = Counter(record.get("lifecycle") for record in records)
    routing = Counter(record.get("routing") for record in records)
    articles = Counter(article.get("status") for record in records for article in record.get("articles", []))
    lines = [
        "# Gmail 星标邮件同步状态\n\n",
        f"> 此文件由 Pipeline 生成，请勿手工编辑。机器事实来源为 [`manifest.json`](./manifest.json)。更新时间：`{data['updated_at']}`。\n\n",
        "## 汇总\n\n| 维度 | 状态 | 数量 |\n| --- | --- | ---: |\n",
    ]
    for key in ("discovered", "failed", "review", "ingested", "ignored", "unhandled"):
        lines.append(f"| 邮件 | {key} | {lifecycle[key]} |\n")
    for key in ("pending", "parsed", "unhandled", "failed"):
        lines.append(f"| 路由 | {key} | {routing[key]} |\n")
    for key in ("review", "ingested", "rejected"):
        lines.append(f"| 文章 | {key} | {articles[key]} |\n")
    lines.extend(
        ["\n## 待处理邮件\n\n", "| Gmail ID | 来源 | 状态 | 主题 | 原因 |\n| --- | --- | --- | --- | --- |\n"]
    )
    pending = [
        record
        for record in records
        if record.get("lifecycle") in {"discovered", "failed", "review", "unhandled"}
    ]
    if pending:
        for record in sorted(pending, key=lambda item: item["id"]):
            subject = record.get("subject", "").replace("|", "\\|")
            detail = (record.get("last_error") or record.get("reason") or "").replace("|", "\\|")
            lines.append(
                f"| `{record['id']}` | {record.get('source_key') or '-'} | {record['lifecycle']} | {subject} | {detail} |\n"
            )
    else:
        lines.append("| - | - | - | 当前没有待处理邮件 | - |\n")
    lines.extend(["\n## 待审文章\n\n", "| 文章 ID | Gmail ID | 来源 | 标题 | 文件 |\n| --- | --- | --- | --- | --- |\n"])
    review = [
        (record, article)
        for record in records
        for article in record.get("articles", [])
        if article.get("status") == "review"
    ]
    if review:
        for record, article in review:
            title = article["title"].replace("|", "\\|")
            path = article.get("staging_file", "")
            lines.append(
                f"| `{article['id']}` | `{record['id']}` | {article.get('source_key', '')} | {title} | [`{article['file']}`](../{path}) |\n"
            )
    else:
        lines.append("| - | - | - | 当前没有待审文章 | - |\n")
    STATUS_PATH.write_text("".join(lines), encoding="utf-8")


def refresh_outputs(data: dict[str, Any]) -> None:
    save_manifest(data)
    rebuild_index(data)
    rebuild_status(data)


def migrate_ddods() -> dict[str, Any]:
    legacy_manifest = LEGACY_STAGE / ".pipeline" / "manifest.json"
    if not legacy_manifest.exists():
        raise PipelineError(f"未找到待迁移的 DDoDS manifest: {legacy_manifest}")
    old = json.loads(legacy_manifest.read_text(encoding="utf-8"))
    data = empty_manifest()
    data["last_sync_at"] = old.get("last_discovery_at")
    for message_id, old_record in old.get("emails", {}).items():
        record = new_email_record(message_id)
        record.update({key: old_record.get(key) for key in record if key in old_record})
        record["source_key"] = "dailydoseofds"
        record["routing"] = "parsed" if old_record.get("articles") else "pending"
        record["articles"] = []
        for article in old_record.get("articles", []):
            item = dict(article)
            item["source_key"] = "dailydoseofds"
            if item.get("file"):
                item["staging_file"] = f"dailydoseofds/{item['file']}"
            record["articles"].append(item)
        data["emails"][message_id] = record

    target_dir = EMAILS_DIR / "dailydoseofds"
    target_dir.mkdir(parents=True, exist_ok=True)
    for path in LEGACY_STAGE.glob("*.md"):
        shutil.move(str(path), str(target_dir / path.name))
    refresh_outputs(data)
    shutil.rmtree(LEGACY_STAGE)
    return data


def print_summary(data: dict[str, Any]) -> None:
    lifecycle = Counter(record.get("lifecycle") for record in data["emails"].values())
    articles = Counter(
        article.get("status") for record in data["emails"].values() for article in record.get("articles", [])
    )
    log_line(f"summary emails_total={len(data['emails'])}")
    log_line(
        "summary email_lifecycle "
        + " ".join(
            f"{key}={lifecycle[key]}"
            for key in ("discovered", "review", "ingested", "ignored", "unhandled", "failed")
        )
    )
    log_line(
        "summary article_status "
        + " ".join(f"{key}={articles[key]}" for key in ("review", "ingested", "rejected"))
    )
    log_line(f"summary last_sync_at={data.get('last_sync_at') or 'never'}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="多来源 Gmail 星标邮件同步、路由与官网长文增强")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("migrate-ddods", help="将旧 DailyDoseOfDS 管线迁移至共享邮件目录")
    commands.add_parser("sync", help="同步全部星标邮件并登记元数据和差异")

    route_cmd = commands.add_parser("route", help="路由已注册来源并生成待审文章")
    route_cmd.add_argument(
        "--fetch-web",
        action="store_true",
        default=False,
        help="探测并拉取来源官网长文版本（若支持）",
    )

    commands.add_parser("reconcile", help="按 raw/articles 逐篇对账已入库文章")
    commands.add_parser("status", help="刷新并显示共享账本状态")

    run_cmd = commands.add_parser("run", help="依次对账、同步和路由已注册来源")
    run_cmd.add_argument(
        "--fetch-web",
        action="store_true",
        default=False,
        help="探测并拉取来源官网长文版本（若支持）",
    )

    reject = commands.add_parser("reject", help="拒绝一篇待审文章")
    reject.add_argument("article_id")
    reject.add_argument("--reason", default="manual_reject")

    fetch_web_cmd = commands.add_parser("fetch-web", help="直接从官网抓取单篇全量长文并生成待审文档")
    fetch_web_cmd.add_argument(
        "target",
        help="官网文章完整 URL 或 Slug (如 https://www.dailydoseofds.com/p/how-a-gpu-actually-works/ 或 how-a-gpu-actually-works)",
    )
    fetch_web_cmd.add_argument("--source", default="dailydoseofds", help="指定来源标识，默认 dailydoseofds")

    diff_web_cmd = commands.add_parser("diff-web", help="针对单篇本地文章比对官网长文版本，输出章节树与统一 Diff")
    diff_web_cmd.add_argument(
        "target",
        help="本地文章文件路径 (例如 raw/articles/xxx.md 或 Clippings/emails/dailydoseofds/xxx.md) 或文章 ID",
    )
    diff_web_cmd.add_argument("--source", default="dailydoseofds", help="指定来源，默认 dailydoseofds")
    diff_web_cmd.add_argument(
        "--channel",
        choices=["auto", "ghost", "jina"],
        default="auto",
        help="抓取决议通道：auto (默认 4 级链路), ghost (仅 Ghost API), jina (直连 Jina Reader)",
    )

    check_upgrades_cmd = commands.add_parser("check-web-upgrades", help="扫描库内存量文献，比对官网长文版本并列出可升级清单")
    check_upgrades_cmd.add_argument(
        "target",
        nargs="?",
        default=None,
        help="可选：指定单篇文章路径或文章 ID。若未指定则全量扫描",
    )
    check_upgrades_cmd.add_argument("--source", default="dailydoseofds", help="指定来源，默认 dailydoseofds")
    check_upgrades_cmd.add_argument(
        "--pending-only",
        action="store_true",
        default=False,
        help="增量优化：若已是 web_canonical 则跳过外部网络检测，大幅提升批量扫描性能",
    )

    upgrade_cmd = commands.add_parser("upgrade-article", help="拉取官网长文版本覆盖升级指定文章")
    upgrade_cmd.add_argument(
        "target",
        help="本地待升级 Markdown 文件路径 (例如 raw/articles/xxx.md 或 Clippings/emails/dailydoseofds/xxx.md) 或文章 ID",
    )
    upgrade_cmd.add_argument("--force", action="store_true", default=False, help="若已是 web_canonical 是否强制重新抓取覆盖")
    upgrade_cmd.add_argument("--dry-run", action="store_true", default=False, help="仅模拟升级过程并预览差异，不物理写盘")
    upgrade_cmd.add_argument("--diff", action="store_true", default=False, help="打印前后正文的 Unified Diff")
    upgrade_cmd.add_argument(
        "--channel",
        choices=["auto", "ghost", "jina"],
        default="auto",
        help="抓取决议通道：auto (默认 4 级链路), ghost (仅 Ghost API), jina (直连 Jina Reader)",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        log_block(args.command, "START")
        if args.command == "migrate-ddods":
            data = migrate_ddods()
            log_line("result migration=dailydoseofds_complete")
        elif args.command == "fetch-web":
            out_file = fetch_web_article(args.target, source_key=args.source)
            log_line(f"result fetch_web_article={out_file}")
        elif args.command == "diff-web":
            data = load_manifest()
            diff_res = diff_web_article(args.target, source_key=args.source, channel=args.channel, data=data)
            log_line(f"result diff_article={diff_res['file']}")
            print(f"\n### 官网长文对比报告: `{diff_res['file']}`\n")
            print(f"- **文章标题**: {diff_res['title']}")
            print(f"- **当前层级**: {diff_res['current_tier']}")
            print(f"- **官网链接**: {diff_res['canonical_url']}")
            print(f"- **篇幅字数**: 本地 {diff_res['local_chars']} 字 vs 官网 {diff_res['web_chars']} 字")
            print(f"- **代码块数**: 本地 {diff_res['local_codes']} 块 vs 官网 {diff_res['web_codes']} 块")
            print("\n#### 章节目录结构对比 (Headings)")
            print("| 序号 | 本地章节 | 官网章节 |")
            print("| --- | --- | --- |")
            max_h = max(len(diff_res["local_headings"]), len(diff_res["web_headings"]))
            if max_h == 0:
                print("| - | 无章节标题 | 无章节标题 |")
            else:
                for idx in range(max_h):
                    loc_h = diff_res["local_headings"][idx] if idx < len(diff_res["local_headings"]) else "-"
                    web_h = diff_res["web_headings"][idx] if idx < len(diff_res["web_headings"]) else "-"
                    print(f"| {idx+1} | {loc_h} | {web_h} |")
            print("\n#### Unified Diff 差异片段 (前 80 行)")
            if diff_res["diff_lines"]:
                print("```diff")
                print("".join(diff_res["diff_lines"][:80]).rstrip())
                print("```")
                if len(diff_res["diff_lines"]) > 80:
                    print(f"\n*(Diff 截断显示，总计 {len(diff_res['diff_lines'])} 行差异)*\n")
            else:
                print("内容完全一致，无正文差异。\n")
        elif args.command == "check-web-upgrades":
            data = load_manifest()
            upgrades = check_web_upgrades(
                source_key=args.source,
                target=args.target,
                pending_only=args.pending_only,
                data=data,
            )
            log_line(f"result scanned_articles={len(upgrades)}")
            print("\n### 官网长文升级比对报告\n")
            print(
                "| 序号 | 本地文件名 | 本地字数/代码块 | 官网字数/代码块 | 当前状态 | 升级建议 |"
            )
            print("| --- | --- | ---: | ---: | --- | --- |")
            for idx, item in enumerate(upgrades, 1):
                loc = f"{item['local_chars']} 字 / {item['local_codes']} 块"
                web = f"{item['web_chars']} 字 / {item['web_codes']} 块" if item["web_chars"] else "-"
                print(
                    f"| {idx} | `{item['file']}` | {loc} | {web} | {item['current_tier']} | **{item['recommendation']}** |"
                )
            print("")
        elif args.command == "upgrade-article":
            data = load_manifest()
            upgraded_file = upgrade_article(
                data,
                args.target,
                force=args.force,
                dry_run=args.dry_run,
                show_diff=args.diff,
                channel=args.channel,
            )
            log_line(f"result upgraded_article={upgraded_file}")
            if not args.dry_run:
                refresh_outputs(data)
        else:
            data = load_manifest()
            if args.command == "sync":
                with GmailImapClient() as client:
                    total, added = sync(data, client=client)
                log_line(f"result remote_emails={total} newly_registered={added}")
            elif args.command == "route":
                with GmailImapClient() as client:
                    emails, articles = route(data, client=client, fetch_web=args.fetch_web)
                log_line(f"result routed_emails={emails} review_articles={articles}")
            elif args.command == "reconcile":
                log_line(f"result reconciled_articles={reconcile(data)}")
            elif args.command == "reject":
                reject_article(data, args.article_id, args.reason)
                log_line(f"result rejected_article={args.article_id}")
            elif args.command == "run":
                reconciled = reconcile(data)
                with GmailImapClient() as client:
                    total, added = sync(data, client=client)
                    emails, articles = route(data, client=client, fetch_web=args.fetch_web)
                log_line(
                    f"result reconciled_articles={reconciled} remote_emails={total} newly_registered={added} routed_emails={emails} review_articles={articles}"
                )
            refresh_outputs(data)
        if args.command not in {"fetch-web", "check-web-upgrades", "diff-web"} and not getattr(args, "dry_run", False):
            print_summary(data)
        log_block(args.command, "END status=ok")
        return 0
    except (PipelineError, OSError, json.JSONDecodeError, ValueError) as exc:
        log_block(args.command, "ERROR", error=True)
        log_line(f"error message={exc}", error=True)
        log_block(args.command, "END status=error")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
