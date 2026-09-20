# /// script
# requires-python = ">=3.12"
# dependencies = ["beautifulsoup4>=4.12", "html2text>=2024.2.26", "PySocks>=1.7.1"]
# ///

"""Daily Dose of DS 邮件解析器与 Ghost 官网长文探测增强。

支持：
1. Ghost Content API 官方只读接口全量拉取；
2. Jina Reader 免渲染次级降级 (Level 1 Fallback)；
3. 邮件原生 HTML 保底降级 (Level 2 Fallback)；
4. <video> 嵌入、多图画廊、表格防断裂、Bookmark 与 Callout 卡片高保真转换。
"""

from __future__ import annotations

import base64
import copy
import email
import json
import logging
import re
import urllib.error
import urllib.parse
import urllib.request
from email import policy
from email.utils import parsedate_to_datetime
from typing import Any

import html2text
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

GHOST_API_BASE: str = "https://daily-dose-of-data-science-1.ghost.io/ghost/api/content"
GHOST_CONTENT_KEY: str = "59065599b5c21100e85d179b92"

IGNORED_HEADINGS = [
    r"In today's newsletter", r"Together with", r"TODAY's Daily dose", r"ADVERTISE TO",
    r"SPONSOR US", r"THAT'S A WRAP", r"Today’s email was brought to you", r"Looking for more",
    r"In case you missed it", r"Update your profile", r"Unsubscribe",
]


def slugify(text: str | None) -> str:
    """将文章标题规范化为 Ghost 标准 URL Slug。

    兼顾各种特殊标点（冒号、破折号、引号、数学符号）与 Unicode 破折号。
    """
    if not text or not isinstance(text, str):
        return ""
    # 移除各类引号（避免 "Claude Code's" -> "claude-code-s"）
    cleaned = re.sub(r"['’‘\"“”`]", "", text)
    # 将各类破折号 (em-dash, en-dash) 转为空格
    cleaned = re.sub(r"[—–―]", " ", cleaned)
    # 将除字母、数字、连字符以外的特殊符号（包括数学公式符号、冒号等）转为空格
    cleaned = re.sub(r"[^\w\s-]", " ", cleaned)
    # 将空白字符与下划线替换为单个连字符
    cleaned = re.sub(r"[\s_]+", "-", cleaned)
    # 折叠多重连字符，去除首尾连字符并转小写
    return re.sub(r"-+", "-", cleaned).strip("-").lower()


def is_public_article_url(url: str | None) -> bool:
    """校验 URL 是否符合官方公开长文 pattern: https://www.dailydoseofds.com/p/{article-title}/。

    规则：以 /p/ 开头为公开长文；非 /p/ 开头为付费 course 或其它非公开页面。
    """
    if not url or not isinstance(url, str):
        return False
    try:
        parsed = urllib.parse.urlparse(url)
    except Exception:
        return False
    host = parsed.netloc.casefold()
    if "dailydoseofds.com" not in host and "ghost.io" not in host:
        return False
    path = parsed.path.strip("/")
    parts = path.split("/")
    return len(parts) == 2 and parts[0] == "p" and bool(parts[1])


def extract_slug_from_url(url: str | None) -> str | None:
    """从给定的完整 URL 中提取 Ghost 官网文章 Slug。仅匹配 /p/{article-title}/ 格式。"""
    if not is_public_article_url(url):
        return None
    parsed = urllib.parse.urlparse(url)
    parts = parsed.path.strip("/").split("/")
    return parts[1]


def convert_html_to_markdown(html_content: str | None) -> str:
    """将 Ghost 文章 HTML 正文转换为保留代码块、图片、视频、表格与卡片的干净 Markdown。"""
    if not html_content or not isinstance(html_content, str):
        return ""
    soup = BeautifulSoup(html_content, "html.parser")

    placeholders: dict[str, str] = {}

    # 1. 代码块 <pre><code> 围栏保护
    for i, pre in enumerate(soup.find_all("pre")):
        code = pre.find("code")
        lang = ""
        if code and code.get("class"):
            for cls in code.get("class"):
                if cls.startswith("language-"):
                    lang = cls[len("language-"):]
                    break
        raw_code = code.get_text() if code else pre.get_text()
        token = f"___FENCED_CODE_BLOCK_{i}___"
        placeholders[token] = f"```{lang}\n{raw_code.rstrip()}\n```"
        pre.replace_with(soup.new_string(token))

    # 2. 富媒体：处理 Ghost <figure>（含 <video> 视频卡片、画廊与图片卡片）
    for figure in soup.find_all("figure"):
        caption_tag = figure.find("figcaption")
        caption_text = caption_tag.get_text(strip=True) if caption_tag else ""

        # 2.1 视频卡片 (Ghost kg-video-card 或普通 figure 内的 video)
        video = figure.find("video")
        if video:
            src = video.get("src")
            if not src:
                source_tag = video.find("source")
                if source_tag and source_tag.get("src"):
                    src = source_tag.get("src")
            if src:
                poster = video.get("poster")
                poster_attr = f' poster="{poster}"' if poster else ""
                token = f"___MEDIA_BLOCK_{len(placeholders)}___"
                cap_line = f"\n*{caption_text}*\n" if caption_text else ""
                video_html = (
                    f"\n\n<video src=\"{src}\" controls=\"controls\"{poster_attr}></video>"
                    f"{cap_line}\n"
                    f"[▶ 视频演示: {caption_text or '点击播放/下载'}]({src})\n\n"
                )
                placeholders[token] = video_html
                figure.replace_with(soup.new_string(token))
                continue

        # 2.2 图片卡片与多图画廊 (Ghost kg-image-card / kg-gallery-card)
        imgs = figure.find_all("img")
        if imgs:
            img_lines: list[str] = []
            for img in imgs:
                src = img.get("src")
                if src:
                    alt = img.get("alt", "") or caption_text
                    img_lines.append(f"![{alt}]({src})")
            if img_lines:
                token = f"___MEDIA_BLOCK_{len(placeholders)}___"
                cap_line = f"\n*{caption_text}*\n" if caption_text else ""
                placeholders[token] = f"\n\n" + "\n".join(img_lines) + f"{cap_line}\n\n"
                figure.replace_with(soup.new_string(token))
                continue

    # 3. 独立 <video> 标签处理（未被 figure 包裹的独立视频）
    for video in soup.find_all("video"):
        src = video.get("src")
        if not src:
            source_tag = video.find("source")
            if source_tag and source_tag.get("src"):
                src = source_tag.get("src")
        if src:
            poster = video.get("poster")
            poster_attr = f' poster="{poster}"' if poster else ""
            token = f"___MEDIA_BLOCK_{len(placeholders)}___"
            video_html = (
                f"\n\n<video src=\"{src}\" controls=\"controls\"{poster_attr}></video>\n"
                f"[▶ 视频演示: 点击播放/下载]({src})\n\n"
            )
            placeholders[token] = video_html
            video.replace_with(soup.new_string(token))

    # 4. Ghost 书签卡片 (kg-bookmark-card)
    for bookmark in soup.find_all(class_=lambda c: c and "kg-bookmark-card" in c):
        a_tag = bookmark.find("a", href=True)
        if a_tag:
            title_div = bookmark.find(class_=lambda c: c and "kg-bookmark-title" in c)
            desc_div = bookmark.find(class_=lambda c: c and "kg-bookmark-description" in c)
            b_title = title_div.get_text(strip=True) if title_div else a_tag.get_text(strip=True)
            b_desc = desc_div.get_text(strip=True) if desc_div else ""
            href = a_tag["href"]
            token = f"___MEDIA_BLOCK_{len(placeholders)}___"
            block = f"\n\n> 🔗 **[{b_title}]({href})**"
            if b_desc:
                block += f"\n> {b_desc}\n\n"
            else:
                block += "\n\n"
            placeholders[token] = block
            bookmark.replace_with(soup.new_string(token))

    # 5. Ghost Callout 提示框 (kg-callout-card) -> Obsidian Callout 语法
    for callout in soup.find_all(class_=lambda c: c and "kg-callout-card" in c):
        emoji_div = callout.find(class_=lambda c: c and "kg-callout-emoji" in c)
        text_div = callout.find(class_=lambda c: c and "kg-callout-text" in c)
        emoji_text = f"{emoji_div.get_text(strip=True)} " if emoji_div else ""
        content = text_div.get_text(strip=True) if text_div else callout.get_text(strip=True)
        token = f"___MEDIA_BLOCK_{len(placeholders)}___"
        placeholders[token] = f"\n\n> [!note] {emoji_text}\n> {content}\n\n"
        callout.replace_with(soup.new_string(token))

    # 6. 表格 <table> 防断裂优化：将单元格内换行转换为空格，防止破坏 Markdown 单行结构
    for cell in soup.find_all(["th", "td"]):
        for br in cell.find_all("br"):
            br.replace_with(soup.new_string(" "))

    converter = html2text.HTML2Text()
    converter.body_width = 0
    converter.ignore_links = False
    converter.ignore_images = False
    converter.protect_links = True
    converter.unicode_snob = True

    markdown = converter.handle(str(soup))
    for token, replacement in placeholders.items():
        markdown = markdown.replace(token, replacement)

    return re.sub(r"\n{3,}", "\n\n", markdown).strip()


def fetch_ghost_post_by_slug(
    slug: str,
    api_key: str = GHOST_CONTENT_KEY,
    base_url: str = GHOST_API_BASE,
    timeout: float = 10.0,
) -> dict[str, Any] | None:
    """根据 Slug 查询 Ghost Content API 获取文章全量数据。"""
    if not slug:
        return None
    endpoint = f"{base_url.rstrip('/')}/posts/slug/{urllib.parse.quote(slug)}/?key={urllib.parse.quote(api_key)}"
    req = urllib.request.Request(endpoint, headers={"User-Agent": "KnowledgeBank-Sync/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            posts = data.get("posts", [])
            if not posts:
                return None
            post = posts[0]
            # 严格校验：必须是公开长文（url 含 /p/ 且 access 为 True 且 visibility 为 public）
            post_slug = post.get("slug") or slug
            post_url = post.get("url") or f"https://www.dailydoseofds.com/p/{post_slug}/"
            if not is_public_article_url(post_url):
                logger.info(
                    "Ghost post '%s' URL '%s' does not match /p/ pattern (paid course or non-article), skipped",
                    slug,
                    post_url,
                )
                return None
            if post.get("access") is False or post.get("visibility") == "paid":
                logger.info("Ghost post '%s' is member-gated (access=False/paid), skipped", slug)
                return None
            return post
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        logger.warning("Ghost API HTTP %s for slug '%s': %s", e.code, slug, e.reason)
        return None
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        logger.warning("Ghost API network error for slug '%s': %s", slug, e)
        return None
    except Exception as e:
        logger.warning("Ghost API unexpected error for slug '%s': %s", slug, e)
        return None


def search_ghost_post_by_title(
    title: str,
    api_key: str = GHOST_CONTENT_KEY,
    base_url: str = GHOST_API_BASE,
    timeout: float = 10.0,
    limit: int = 5,
) -> dict[str, Any] | None:
    """通过 Ghost NQL 语法按标题前缀模糊检索文章。"""
    if not title:
        return None
    # 提取纯字母数字有效单词（去除标点、连字符和下划线）
    words = [w for w in re.findall(r"[A-Za-z0-9]+", title) if w]
    if not words:
        return None
    search_term = " ".join(words[:5])
    if len(search_term) < 2:
        return None

    params = {
        "key": api_key,
        "filter": f"title:~'{search_term}'",
        "limit": str(limit),
    }
    endpoint = f"{base_url.rstrip('/')}/posts/?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(endpoint, headers={"User-Agent": "KnowledgeBank-Sync/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            posts = data.get("posts", [])
            if not posts:
                return None
            # 严格过滤：仅保留符合 /p/ pattern 且具有完整访问权限的公开长文，排除非 /p/ 的付费 course
            valid_posts = [
                p
                for p in posts
                if is_public_article_url(p.get("url") or f"https://www.dailydoseofds.com/p/{p.get('slug', '')}/")
                and p.get("access") is not False
                and p.get("visibility", "public") == "public"
            ]
            if not valid_posts:
                return None
            target_slug = slugify(title)
            for post in valid_posts:
                if post.get("slug") == target_slug:
                    return post
                if post.get("title", "").casefold() == title.casefold():
                    return post
            return valid_posts[0]
    except urllib.error.HTTPError as e:
        logger.warning("Ghost API search HTTP %s for title '%s': %s", e.code, title, e.reason)
        return None
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        logger.warning("Ghost API search network error for title '%s': %s", title, e)
        return None
    except Exception as e:
        logger.warning("Ghost API search unexpected error for title '%s': %s", title, e)
        return None


def fetch_jina_reader_post(
    slug_or_url: str,
    timeout: float = 8.0,
) -> dict[str, Any] | None:
    """当 Ghost API 异常时，通过 Jina Reader (免渲染公开抓取) 获取官方文章内容作为 Level 1 降级。"""
    if not slug_or_url:
        return None
    target_url = (
        slug_or_url
        if slug_or_url.startswith("http")
        else f"https://www.dailydoseofds.com/p/{slug_or_url.strip('/')}/"
    )
    # 严格校验：URL 必须符合 /p/ 公开长文 pattern
    if not is_public_article_url(target_url):
        return None

    jina_endpoint = f"https://r.jina.ai/{target_url}"
    req = urllib.request.Request(
        jina_endpoint,
        headers={
            "User-Agent": "KnowledgeBank-Sync/1.0",
            "X-Timeout": str(int(timeout)),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw_text = resp.read().decode("utf-8")
            if not raw_text or len(raw_text.strip()) < 80:
                return None
            # 过滤 404 错误页及站点通用模版
            if (
                "Page not found" in raw_text
                or "404:" in raw_text
                or "sx-main" in raw_text
            ):
                return None

            title_match = re.search(r"^Title:\s*(.+)$", raw_text, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else ""
            if not title or title.casefold() in {"daily dose of data science", "page not found"}:
                return None

            body = raw_text
            if "Markdown Content:" in raw_text:
                body = raw_text.split("Markdown Content:", 1)[-1].strip()
            slug = extract_slug_from_url(target_url) or slugify(title)
            return {
                "title": title or slug,
                "slug": slug,
                "canonical_url": target_url,
                "content_tier": "web_canonical",
                "body": body,
                "published_at": "",
            }
    except Exception as exc:
        logger.warning("Jina Reader fallback failed for '%s': %s", target_url, exc)
        return None


def fetch_canonical_article(
    title: str,
    candidate_urls: list[str] | None = None,
    api_key: str = GHOST_CONTENT_KEY,
    base_url: str = GHOST_API_BASE,
    timeout: float = 10.0,
    channel: str = "auto",
) -> dict[str, Any] | None:
    """探测并拉取 Ghost 官网标准长文版本。

    参数：
    - channel: 抓取通道决议策略 ("auto", "ghost", "jina")。
      - "auto": 默认 4 级容灾决议链 (Ghost Slug -> Ghost 标题搜索 -> Jina Reader -> 失败兜底)；
      - "ghost": 仅尝试 Ghost API，不触发 Jina 降级；
      - "jina": 跳过 Ghost API，直接走 Jina Reader 抓取。
    """
    try:
        channel_norm = channel.lower() if isinstance(channel, str) else "auto"
        post = None
        target_slug: str | None = None

        # 若指定纯 Jina 通道，直接解析 slug 并抓取
        if channel_norm == "jina":
            if candidate_urls:
                for url in candidate_urls:
                    if is_public_article_url(url):
                        target_slug = extract_slug_from_url(url)
                        if target_slug:
                            break
            if not target_slug and title:
                target_slug = slugify(title)
            if target_slug:
                return fetch_jina_reader_post(target_slug, timeout=timeout)
            return None

        # 1. 候选 URL 优先级最高（必须先经过 is_public_article_url 校验）
        if candidate_urls:
            for url in candidate_urls:
                if not is_public_article_url(url):
                    continue
                slug = extract_slug_from_url(url)
                if slug:
                    target_slug = slug
                    post = fetch_ghost_post_by_slug(slug, api_key=api_key, base_url=base_url, timeout=timeout)
                    if post:
                        break

        # 2. 标题 Slug 次优匹配
        if not post and title:
            slug = slugify(title)
            if slug:
                target_slug = target_slug or slug
                post = fetch_ghost_post_by_slug(slug, api_key=api_key, base_url=base_url, timeout=timeout)

        # 3. 标题 NQL 模糊检索保底
        if not post and title:
            post = search_ghost_post_by_title(title, api_key=api_key, base_url=base_url, timeout=timeout)
            if post:
                target_slug = post.get("slug")

        # 4. 若 Ghost API 命中，解析组装并最终校验 URL
        if post:
            post_slug = post.get("slug") or slugify(post.get("title", ""))
            canonical_url = post.get("url") or f"https://www.dailydoseofds.com/p/{post_slug}/"
            if not is_public_article_url(canonical_url):
                logger.info("Canonical URL '%s' is not /p/ public article, skipped", canonical_url)
                return None
            raw_html = post.get("html", "")
            markdown_body = convert_html_to_markdown(raw_html)
            return {
                "title": post.get("title") or title,
                "slug": post_slug,
                "canonical_url": canonical_url,
                "content_tier": "web_canonical",
                "body": markdown_body,
                "published_at": post.get("published_at", ""),
            }

        # 5. Level 1 降级：尝试 Jina Reader (若 channel=="ghost" 则跳过)
        if channel_norm != "ghost" and target_slug:
            jina_post = fetch_jina_reader_post(target_slug, timeout=timeout)
            if jina_post:
                logger.info("Jina Reader fallback succeeded for slug '%s'", target_slug)
                return jina_post

        return None
    except Exception as exc:
        logger.warning("fetch_canonical_article unexpected error for title '%s': %s", title, exc)
        return None


def decode_tracking_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc.casefold()
    if "convertkit" not in host and "kit-mail" not in host:
        return url
    encoded = parsed.path.strip("/").split("/")[-1]
    if len(encoded) <= 20:
        return url
    try:
        encoded += "=" * (-len(encoded) % 4)
        decoded = base64.urlsafe_b64decode(encoded).decode("utf-8", errors="ignore")
        return decoded if decoded.startswith("http") else url
    except (ValueError, UnicodeDecodeError):
        return url


def extract_html(raw_message: str) -> tuple[email.message.EmailMessage, BeautifulSoup]:
    padded = raw_message + "=" * (-len(raw_message) % 4)
    message = email.message_from_bytes(base64.urlsafe_b64decode(padded), policy=policy.default)
    html_body = ""
    plain_body = ""
    for part in message.walk() if message.is_multipart() else [message]:
        if "attachment" in str(part.get("Content-Disposition", "")):
            continue
        payload = part.get_payload(decode=True) or b""
        charset = part.get_content_charset() or "utf-8"
        if part.get_content_type() == "text/html" and not html_body:
            html_body = payload.decode(charset, errors="ignore")
        elif part.get_content_type() == "text/plain" and not plain_body:
            plain_body = payload.decode(charset, errors="ignore")
    if not html_body:
        html_body = f"<pre>{plain_body}</pre>" if plain_body else "<p>无可用邮件内容</p>"
    return message, BeautifulSoup(html_body, "html.parser")


def ignored_heading(heading: Any) -> bool:
    text = heading.get_text(" ", strip=True)
    if any(re.search(pattern, text, re.IGNORECASE) for pattern in IGNORED_HEADINGS):
        return True
    return any(
        urllib.parse.urlparse(anchor["href"]).path.rstrip("/").casefold() == "/membership"
        for anchor in heading.find_all("a", href=True)
    )


def parse(
    message_id: str,
    response: dict[str, Any],
    fetch_web: bool = False,
) -> tuple[dict[str, str], list[dict[str, Any]]]:
    """解析邮件并根据开关探测 Ghost 官网全量长文。"""
    if "raw" not in response:
        raise ValueError("邮件响应缺少 raw 字段")
    message, soup = extract_html(response["raw"])
    subject = str(message.get("Subject", f"untitled_{message_id}"))
    sender = str(message.get("From", "未知发送者"))
    date = str(message.get("Date", ""))
    formatted_date = "0000-00-00"
    if date:
        try:
            formatted_date = parsedate_to_datetime(date).strftime("%Y-%m-%d")
        except (TypeError, ValueError, OverflowError):
            pass

    for anchor in soup.find_all("a", href=True):
        anchor["href"] = decode_tracking_url(anchor["href"])
    for image in soup.find_all("img", src=True):
        if "open.convertkit-mail" in image["src"] or "pixel" in image["src"]:
            image.decompose()

    converter = html2text.HTML2Text()
    converter.body_width = 0
    converter.ignore_links = False
    converter.ignore_images = False
    converter.protect_links = True
    converter.unicode_snob = True

    headings = soup.find_all("h2")
    valid_headings = [heading for heading in headings if not ignored_heading(heading)]
    articles: list[dict[str, Any]] = []

    def _process_article(
        title: str,
        article_soup_or_full: BeautifulSoup,
        position: str,
    ) -> dict[str, Any]:
        email_body = re.sub(r"\n{3,}", "\n\n", converter.handle(str(article_soup_or_full))).replace("\u200b", "")
        article_entry: dict[str, Any] = {
            "title": title,
            "body": email_body,
            "part": position,
            "content_tier": "email_fallback",
            "canonical_url": None,
        }

        if fetch_web:
            try:
                candidate_urls = [a["href"] for a in article_soup_or_full.find_all("a", href=True)]
                canonical = fetch_canonical_article(title, candidate_urls=candidate_urls)
                if canonical:
                    article_entry["body"] = canonical["body"]
                    article_entry["content_tier"] = canonical["content_tier"]
                    article_entry["canonical_url"] = canonical["canonical_url"]
                    article_entry["slug"] = canonical["slug"]
            except Exception as exc:
                logger.warning("Failed web enrichment for article '%s': %s", title, exc)

        return article_entry

    if valid_headings:
        for position, heading in enumerate(valid_headings, 1):
            article_soup = BeautifulSoup("", "html.parser")
            article_soup.append(copy.copy(heading))
            node = heading.next_sibling
            while node and getattr(node, "name", None) != "h2":
                article_soup.append(copy.copy(node))
                node = node.next_sibling

            title = heading.get_text(" ", strip=True).replace("\u200b", "")
            articles.append(_process_article(title, article_soup, str(position)))
    elif not headings:
        title = subject.replace("\u200b", "")
        articles.append(_process_article(title, soup, "1"))

    return {"subject": subject, "sender": sender, "date": date, "formatted_date": formatted_date}, articles
