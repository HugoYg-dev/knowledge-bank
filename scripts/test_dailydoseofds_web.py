# /// script
# requires-python = ">=3.12"
# dependencies = ["beautifulsoup4>=4.12", "html2text>=2024.2.26", "PySocks>=1.7.1", "pyyaml>=6.0"]
# ///

"""Daily Dose of Data Science (dailydoseofds) 官网长文增强测试套件。

涵盖：
1. URL Slug 规范化与提取单元测试 (test_slugify & test_extract_slug_from_url，包含极端字符、破折号与数学符号)
2. Ghost HTML 转 Markdown 格式转换测试 (代码块、<video> 嵌入、多图画廊、表格防断裂、Bookmark、Callout)
3. Ghost API 客户端 Mock 单元测试 (HTTP 200, 404, 429 Rate Limit, 500 Server Error, Timeout, NQL Filter 特殊字符清洗)
4. Jina Reader 免渲染次级降级测试 (Level 1 Fallback)
5. 全量长文探测决议链测试 (优先级：候选 URL -> Slug -> NQL -> Jina -> Email)
6. 邮件解析器 parse() 与官网增强集成测试 (web_canonical vs email_fallback)
7. mail_pipeline CLI 子命令测试 (fetch-web, check-web-upgrades, upgrade-article, route --fetch-web, reconcile 元数据同步)
8. 真实 Ghost Content API 连通性健全性测试 (Live Sanity Test)
"""

from __future__ import annotations

import base64
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
import urllib.error
from unittest.mock import MagicMock, patch

# 确保可以直接导入同目录下的模块
TEST_DIR = Path(__file__).resolve().parent
if str(TEST_DIR) not in sys.path:
    sys.path.insert(0, str(TEST_DIR))

import mail_pipeline
from mail_sources import dailydoseofds


class TestDailydoseofdsSlugAndUrl(unittest.TestCase):
    """测试 URL Slug 规范化算法与 URL 提取功能。"""

    def test_slugify(self) -> None:
        """测试基础转换、标点引号、特殊符号与多连字符修剪。"""
        # 1. 基础字母数字转换
        self.assertEqual(
            dailydoseofds.slugify("KV Cache Engineering for LLM Serving"),
            "kv-cache-engineering-for-llm-serving",
        )
        self.assertEqual(
            dailydoseofds.slugify("How a GPU Actually Works"),
            "how-a-gpu-actually-works",
        )
        self.assertEqual(
            dailydoseofds.slugify("72 techniques to optimize LLMs in production"),
            "72-techniques-to-optimize-llms-in-production",
        )

        # 2. 标点、单双引号及智能引号处理（智能单引号 ’ 必须直接剔除而非转为连字符）
        self.assertEqual(
            dailydoseofds.slugify("Claude Code’s architecture, explained visually!"),
            "claude-codes-architecture-explained-visually",
        )
        self.assertEqual(
            dailydoseofds.slugify("What's the difference between \"A\" and 'B'?"),
            "whats-the-difference-between-a-and-b",
        )
        self.assertEqual(
            dailydoseofds.slugify("The “Secret” of In-Context Learning: A Deep Dive"),
            "the-secret-of-in-context-learning-a-deep-dive",
        )

        # 3. 符号与多连字符修剪
        self.assertEqual(
            dailydoseofds.slugify("Prompt, context, harness & loop engineering"),
            "prompt-context-harness-loop-engineering",
        )
        self.assertEqual(
            dailydoseofds.slugify("KV vs. Prefix vs. Prompt vs. Semantic Caching..."),
            "kv-vs-prefix-vs-prompt-vs-semantic-caching",
        )
        self.assertEqual(
            dailydoseofds.slugify("   ---Whitespace   and___underscores---   "),
            "whitespace-and-underscores",
        )

        # 4. 边界与空值情况
        self.assertEqual(dailydoseofds.slugify(""), "")
        self.assertEqual(dailydoseofds.slugify(None), "")  # type: ignore[arg-type]
        self.assertEqual(dailydoseofds.slugify("---"), "")

    def test_slugify_extreme_titles(self) -> None:
        """测试极端字符：Unicode 破折号 (em-dash, en-dash)、冒号、数学公式符号与纯符号。"""
        # Unicode 破折号转换为空格并折叠为连字符
        self.assertEqual(
            dailydoseofds.slugify("KV Cache — The Complete Guide"),
            "kv-cache-the-complete-guide",
        )
        self.assertEqual(
            dailydoseofds.slugify("Part 1 – Foundation vs. Part 2 — Advanced"),
            "part-1-foundation-vs-part-2-advanced",
        )

        # 复杂标点与冒号
        self.assertEqual(
            dailydoseofds.slugify("Model Serving: A 10-Minute Deep Dive (v2.0)"),
            "model-serving-a-10-minute-deep-dive-v2-0",
        )

        # 数学符号与公式字符
        self.assertEqual(
            dailydoseofds.slugify("Is O(N) > O(1)? Matrix Multiplication: A × B ÷ C = D"),
            "is-o-n-o-1-matrix-multiplication-a-b-c-d",
        )

        # 纯标点、纯数学符号及空格应安全返回空字符串
        self.assertEqual(dailydoseofds.slugify("::: --- ???"), "")
        self.assertEqual(dailydoseofds.slugify("+=<>*&^%$#@!"), "")
        self.assertEqual(dailydoseofds.slugify("    "), "")

    def test_extract_slug_from_url(self) -> None:
        """测试从完整 URL 提取官网 Slug。"""
        self.assertEqual(
            dailydoseofds.extract_slug_from_url("https://www.dailydoseofds.com/p/how-a-gpu-actually-works/"),
            "how-a-gpu-actually-works",
        )
        self.assertEqual(
            dailydoseofds.extract_slug_from_url("https://dailydoseofds.com/p/kv-cache-engineering-for-llm-serving"),
            "kv-cache-engineering-for-llm-serving",
        )
        self.assertEqual(
            dailydoseofds.extract_slug_from_url("http://daily-dose-of-data-science-1.ghost.io/p/test-article/"),
            "test-article",
        )

        # 带 query 参数与 hash 锚点的 URL 提取
        self.assertEqual(
            dailydoseofds.extract_slug_from_url(
                "https://www.dailydoseofds.com/p/how-a-gpu-actually-works/?ref=daily-dose-of-data-science&source=email#section-2"
            ),
            "how-a-gpu-actually-works",
        )

        # 非匹配或无效 URL 返回 None
        self.assertIsNone(dailydoseofds.extract_slug_from_url("https://example.com/other-page"))
        self.assertIsNone(dailydoseofds.extract_slug_from_url("https://www.dailydoseofds.com/membership"))
        self.assertIsNone(dailydoseofds.extract_slug_from_url("https://www.dailydoseofds.com/archive"))
        self.assertIsNone(dailydoseofds.extract_slug_from_url("https://www.dailydoseofds.com/p/"))
        self.assertIsNone(dailydoseofds.extract_slug_from_url(""))
        self.assertIsNone(dailydoseofds.extract_slug_from_url(None))  # type: ignore[arg-type]

    def test_decode_tracking_url(self) -> None:
        """测试 ConvertKit 追踪链接还原。"""
        original = "https://www.dailydoseofds.com/p/how-a-gpu-actually-works/"
        encoded = base64.urlsafe_b64encode(original.encode("utf-8")).decode("utf-8").rstrip("=")
        tracking_url = f"https://click.kit-mail3.com/redirect/{encoded}"
        self.assertEqual(dailydoseofds.decode_tracking_url(tracking_url), original)
        self.assertEqual(dailydoseofds.decode_tracking_url(original), original)

    def test_is_public_article_url(self) -> None:
        """测试 URL 筛选规则：仅匹配 /p/{article-title}/ 格式为公开文章，非 /p/ 为付费 course 或非文章。"""
        # 公开文章格式 -> True
        self.assertTrue(dailydoseofds.is_public_article_url("https://www.dailydoseofds.com/p/how-a-gpu-actually-works/"))
        self.assertTrue(dailydoseofds.is_public_article_url("https://www.dailydoseofds.com/p/kv-cache-engineering-for-llm-serving"))
        self.assertTrue(dailydoseofds.is_public_article_url("http://daily-dose-of-data-science-1.ghost.io/p/continuous-batching-in-llms/"))

        # 非 /p/ 的付费 Course 或非公开页面 -> False
        self.assertFalse(dailydoseofds.is_public_article_url("https://www.dailydoseofds.com/ai-agents-with-langgraph-course-part-1-with-implementation/"))
        self.assertFalse(dailydoseofds.is_public_article_url("https://www.dailydoseofds.com/building-rag-systems-course-part-15-with-implementation/"))
        self.assertFalse(dailydoseofds.is_public_article_url("https://www.dailydoseofds.com/what-is-mcp/"))
        self.assertFalse(dailydoseofds.is_public_article_url("https://www.dailydoseofds.com/archive/"))
        self.assertFalse(dailydoseofds.is_public_article_url("https://www.dailydoseofds.com/p/"))
        self.assertFalse(dailydoseofds.is_public_article_url("https://example.com/p/test/"))
        self.assertFalse(dailydoseofds.is_public_article_url(""))
        self.assertFalse(dailydoseofds.is_public_article_url(None))  # type: ignore[arg-type]


class TestGhostHtmlToMarkdown(unittest.TestCase):
    """测试 Ghost 原生 HTML 到无损 Markdown 的转换规范（含富媒体与格式保护）。"""

    def test_convert_html_to_markdown_basic(self) -> None:
        """测试核心结构转换：标题层级、代码块、Ghost 图片与链接保护。"""
        html = """
        <h2>Introduction to GPU Memory</h2>
        <p>Understanding GPU latency requires examining its memory hierarchy.</p>
        <h3>HBM vs SRAM</h3>
        <p>HBM is large but slower; SRAM is tiny but blazingly fast.</p>
        <pre><code class="language-python">import torch

def allocate_kv_cache(seq_len: int, num_heads: int, head_dim: int):
    # Allocate empty cache tensor
    return torch.empty((seq_len, num_heads, head_dim), dtype=torch.float16)
</code></pre>
        <figure class="kg-card kg-image-card kg-width-wide">
            <img src="https://storage.ghost.io/content/images/2026/08/gpu-memory.png" alt="GPU Memory Hierarchy">
            <figcaption>Detailed memory hierarchy layout</figcaption>
        </figure>
        <p>For more details, see <a href="https://www.dailydoseofds.com/p/flash-attention">FlashAttention Deep Dive</a>.</p>
        """

        markdown = dailydoseofds.convert_html_to_markdown(html)

        self.assertIn("## Introduction to GPU Memory", markdown)
        self.assertIn("### HBM vs SRAM", markdown)
        self.assertIn("```python", markdown)
        self.assertIn("def allocate_kv_cache(seq_len: int, num_heads: int, head_dim: int):", markdown)
        self.assertIn("![GPU Memory Hierarchy](https://storage.ghost.io/content/images/2026/08/gpu-memory.png)", markdown)
        self.assertIn("*Detailed memory hierarchy layout*", markdown)
        self.assertIn("[FlashAttention Deep Dive](<https://www.dailydoseofds.com/p/flash-attention>)", markdown)

    def test_convert_html_video_embed(self) -> None:
        """测试 Ghost 原生 <video> 嵌入卡片与独立 video 标签的无损转换。"""
        html = """
        <h2>Dynamic Attention Visualization</h2>
        <figure class="kg-card kg-video-card">
            <video src="https://storage.ghost.io/videos/attention-flow.mp4" poster="https://storage.ghost.io/poster.jpg" loop autoplay muted></video>
            <figcaption>Attention weights calculation animation</figcaption>
        </figure>
        <p>Below is a standalone video:</p>
        <video src="https://storage.ghost.io/videos/standalone.mp4" controls></video>
        """
        markdown = dailydoseofds.convert_html_to_markdown(html)

        # 验证包含 Obsidian 原生可播放的 <video> 标签与说明
        self.assertIn('<video src="https://storage.ghost.io/videos/attention-flow.mp4" controls="controls" poster="https://storage.ghost.io/poster.jpg"></video>', markdown)
        self.assertIn("*Attention weights calculation animation*", markdown)
        self.assertIn("[▶ 视频演示: Attention weights calculation animation](https://storage.ghost.io/videos/attention-flow.mp4)", markdown)

        # 验证独立 video
        self.assertIn('<video src="https://storage.ghost.io/videos/standalone.mp4" controls="controls"></video>', markdown)
        self.assertIn("[▶ 视频演示: 点击播放/下载](https://storage.ghost.io/videos/standalone.mp4)", markdown)

    def test_convert_html_gallery_and_multiple_images(self) -> None:
        """测试画廊卡片 (kg-gallery-card) 内包含多张图片的完整提取。"""
        html = """
        <figure class="kg-card kg-gallery-card">
            <img src="https://storage.ghost.io/pic1.png" alt="Pic 1">
            <img src="https://storage.ghost.io/pic2.png" alt="Pic 2">
            <figcaption>Comparison of two architectures</figcaption>
        </figure>
        """
        markdown = dailydoseofds.convert_html_to_markdown(html)
        self.assertIn("![Pic 1](https://storage.ghost.io/pic1.png)", markdown)
        self.assertIn("![Pic 2](https://storage.ghost.io/pic2.png)", markdown)
        self.assertIn("*Comparison of two architectures*", markdown)

    def test_convert_html_bookmark_and_callout(self) -> None:
        """测试 Ghost 书签卡片 (kg-bookmark-card) 与 Callout 提示框 (kg-callout-card) 的排版转换。"""
        html = """
        <figure class="kg-card kg-bookmark-card">
            <a class="kg-bookmark-container" href="https://vllm.ai">
                <div class="kg-bookmark-content">
                    <div class="kg-bookmark-title">vLLM: High-throughput Serving</div>
                    <div class="kg-bookmark-description">Easy, fast, and cheap LLM serving.</div>
                </div>
            </a>
        </figure>
        <div class="kg-card kg-callout-card kg-callout-card-grey">
            <div class="kg-callout-emoji">💡</div>
            <div class="kg-callout-text">KV cache compression can achieve 4x throughput improvement.</div>
        </div>
        """
        markdown = dailydoseofds.convert_html_to_markdown(html)
        self.assertIn("> 🔗 **[vLLM: High-throughput Serving](https://vllm.ai)**", markdown)
        self.assertIn("> Easy, fast, and cheap LLM serving.", markdown)
        self.assertIn("> [!note] 💡", markdown)
        self.assertIn("KV cache compression can achieve 4x throughput improvement.", markdown)

    def test_convert_html_table_br_protection(self) -> None:
        """测试表格 <table> 中单元格内带有 <br> 时的防断裂保护。"""
        html = """
        <table>
            <thead>
                <tr><th>Method</th><th>Pros</th><th>Cons</th></tr>
            </thead>
            <tbody>
                <tr>
                    <td>PagedAttention</td>
                    <td>Near-zero memory waste<br>Dynamic allocation</td>
                    <td>Complex kernel<br>CUDA dependency</td>
                </tr>
            </tbody>
        </table>
        """
        markdown = dailydoseofds.convert_html_to_markdown(html)
        # 表格应该保持为一行一记录，且单元格内不会因字面换行导致表格破碎
        lines = [line for line in markdown.splitlines() if "PagedAttention" in line]
        self.assertEqual(len(lines), 1, "PagedAttention 记录必须在一行内输出")
        self.assertIn("Near-zero memory waste", lines[0])
        self.assertIn("Dynamic allocation", lines[0])

    def test_convert_empty_html(self) -> None:
        """测试空输入边界。"""
        self.assertEqual(dailydoseofds.convert_html_to_markdown(""), "")
        self.assertEqual(dailydoseofds.convert_html_to_markdown(None), "")  # type: ignore[arg-type]


class TestGhostApiClientMock(unittest.TestCase):
    """测试 Ghost Content API 客户端函数（通过 Mock HTTP 模拟各类网络与错误状态）。"""

    def test_fetch_ghost_post_by_slug_success(self) -> None:
        """Mock HTTP 200 正常响应获取文章全量数据。"""
        mock_post_payload = {
            "posts": [
                {
                    "id": "post-gpu-123",
                    "title": "How a GPU Actually Works",
                    "slug": "how-a-gpu-actually-works",
                    "html": "<h2>GPU Deep Dive</h2><p>Full content here.</p>",
                    "url": "https://www.dailydoseofds.com/p/how-a-gpu-actually-works/",
                    "published_at": "2026-08-18T01:58:58.000Z",
                }
            ]
        }
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mock_post_payload).encode("utf-8")
        mock_response.__enter__.return_value = mock_response

        with patch("urllib.request.urlopen", return_value=mock_response) as mock_urlopen:
            post = dailydoseofds.fetch_ghost_post_by_slug("how-a-gpu-actually-works")
            self.assertIsNotNone(post)
            self.assertEqual(post["title"], "How a GPU Actually Works")  # type: ignore[index]
            self.assertEqual(post["slug"], "how-a-gpu-actually-works")  # type: ignore[index]

            mock_urlopen.assert_called_once()
            call_arg = mock_urlopen.call_args[0][0]
            request_url = call_arg.full_url if isinstance(call_arg, urllib.request.Request) else str(call_arg)
            self.assertIn("/posts/slug/how-a-gpu-actually-works/", request_url)
            self.assertIn(f"key={dailydoseofds.GHOST_CONTENT_KEY}", request_url)

    def test_fetch_ghost_post_by_slug_not_found(self) -> None:
        """Mock HTTP 404 返回 None 而不抛出未捕获异常。"""
        http_error = urllib.error.HTTPError(
            url="http://mock-ghost/posts/slug/not-found/",
            code=404,
            msg="Not Found",
            hdrs={},  # type: ignore[arg-type]
            fp=io.BytesIO(b'{"errors":[{"message":"Post not found."}]}'),
        )
        with patch("urllib.request.urlopen", side_effect=http_error):
            post = dailydoseofds.fetch_ghost_post_by_slug("non-existent-slug")
            self.assertIsNone(post)

    def test_fetch_ghost_post_rate_limit_and_500(self) -> None:
        """Mock HTTP 429 与 HTTP 500 返回 None 并记录 warning，绝不抛错。"""
        for code in (429, 500, 502):
            err = urllib.error.HTTPError(
                url="http://mock-ghost/",
                code=code,
                msg="Error",
                hdrs={},  # type: ignore[arg-type]
                fp=io.BytesIO(b"Error"),
            )
            with self.assertLogs("mail_sources.dailydoseofds", level="WARNING"):
                with patch("urllib.request.urlopen", side_effect=err):
                    post = dailydoseofds.fetch_ghost_post_by_slug("error-slug")
                    self.assertIsNone(post)

    def test_fetch_ghost_post_by_slug_timeout_and_network_error(self) -> None:
        """Mock 网络超时及 DNS 异常返回 None 并记录警告。"""
        with self.assertLogs("mail_sources.dailydoseofds", level="WARNING"):
            with patch("urllib.request.urlopen", side_effect=TimeoutError("Request timed out")):
                post = dailydoseofds.fetch_ghost_post_by_slug("timeout-slug")
                self.assertIsNone(post)

        with self.assertLogs("mail_sources.dailydoseofds", level="WARNING"):
            with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("DNS resolution failed")):
                post = dailydoseofds.fetch_ghost_post_by_slug("dns-fail-slug")
                self.assertIsNone(post)

    def test_search_ghost_post_by_title_sanitization(self) -> None:
        """验证 NQL 检索在遇到特殊字符（冒号、方括号、数学符号）时被严格清洗。"""
        mock_search_payload = {
            "posts": [
                {
                    "id": "post-special",
                    "title": "Attention: All You Need [Deep Dive]",
                    "slug": "attention-all-you-need-deep-dive",
                    "html": "<h2>Attention</h2>",
                }
            ]
        }
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mock_search_payload).encode("utf-8")
        mock_response.__enter__.return_value = mock_response

        with patch("urllib.request.urlopen", return_value=mock_response) as mock_urlopen:
            # 输入带有容易引发 NQL 报错的字符
            post = dailydoseofds.search_ghost_post_by_title("Attention: All You Need [Deep Dive] + v2.0")
            self.assertIsNotNone(post)

            call_arg = mock_urlopen.call_args[0][0]
            request_url = call_arg.full_url if isinstance(call_arg, urllib.request.Request) else str(call_arg)
            # 确认保留的是清洗后的安全单词，未直接将方括号和冒号裸传给 NQL
            self.assertIn("title%3A~", request_url)

    def test_search_ghost_post_empty_on_pure_symbols(self) -> None:
        """当传入纯符号标题时，直接安全返回 None，不发起无效请求。"""
        with patch("urllib.request.urlopen") as mock_urlopen:
            self.assertIsNone(dailydoseofds.search_ghost_post_by_title("::: --- ???"))
            self.assertIsNone(dailydoseofds.search_ghost_post_by_title(""))
            mock_urlopen.assert_not_called()

    def test_fetch_ghost_post_rejects_paid_course_or_non_p_url(self) -> None:
        """测试当 Ghost API 返回的文章是非 /p/ 格式（付费课程）或 visibility=paid/access=False 时，严格拒绝返回 None。"""
        paid_course_payload = {
            "posts": [
                {
                    "title": "AI Agents with LangGraph Course",
                    "slug": "ai-agents-with-langgraph-course-part-1-with-implementation",
                    "url": "https://www.dailydoseofds.com/ai-agents-with-langgraph-course-part-1-with-implementation/",
                    "visibility": "paid",
                    "access": False,
                    "html": "<p>Preview excerpt only...</p>",
                }
            ]
        }
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(paid_course_payload).encode("utf-8")
        mock_response.__enter__.return_value = mock_response

        with patch("urllib.request.urlopen", return_value=mock_response):
            post = dailydoseofds.fetch_ghost_post_by_slug("ai-agents-with-langgraph-course-part-1-with-implementation")
            self.assertIsNone(post, "非 /p/ 开头的付费课程应被拒绝")


class TestJinaReaderFallback(unittest.TestCase):
    """测试 Jina Reader 免渲染次级降级 (Level 1 Fallback)。"""

    def test_fetch_jina_reader_success(self) -> None:
        mock_jina_text = (
            "Title: KV Cache Engineering for LLM Serving\n\n"
            "Markdown Content:\n"
            "## Deep Dive into DynamicCache\n\n"
            "Full content from Jina reader."
        )
        mock_response = MagicMock()
        mock_response.read.return_value = mock_jina_text.encode("utf-8")
        mock_response.__enter__.return_value = mock_response

        with patch("urllib.request.urlopen", return_value=mock_response):
            post = dailydoseofds.fetch_jina_reader_post("kv-cache-engineering-for-llm-serving")
            self.assertIsNotNone(post)
            self.assertEqual(post["title"], "KV Cache Engineering for LLM Serving")  # type: ignore[index]
            self.assertIn("DynamicCache", post["body"])  # type: ignore[index]
            self.assertEqual(post["content_tier"], "web_canonical")  # type: ignore[index]

    def test_fetch_jina_reader_rejects_404_error_page(self) -> None:
        """测试 Jina Reader 抓到 404 错误页及站点通用首页导航模版时被安全拦截，不作为文章返回。"""
        mock_404_text = (
            "Title: Daily Dose of Data Science\n\n"
            "URL Source: https://www.dailydoseofds.com/p/non-existent-slug/\n\n"
            "Markdown Content:\n"
            "[Skip to main content](https://www.dailydoseofds.com/p/non-existent-slug/#sx-main)\n\n"
            "404: Page Not Found. Here are some other articles..."
        )
        mock_response = MagicMock()
        mock_response.read.return_value = mock_404_text.encode("utf-8")
        mock_response.__enter__.return_value = mock_response

        with patch("urllib.request.urlopen", return_value=mock_response):
            post = dailydoseofds.fetch_jina_reader_post("non-existent-slug")
            self.assertIsNone(post, "404 模版页必须被拦截")

    def test_fetch_jina_reader_failure_returns_none(self) -> None:
        with patch("urllib.request.urlopen", side_effect=TimeoutError("Jina timed out")):
            post = dailydoseofds.fetch_jina_reader_post("any-slug")
            self.assertIsNone(post)


class TestFetchCanonicalArticleChain(unittest.TestCase):
    """测试官网长文探测决议链与逐级降级机制。"""

    def test_ghost_api_slug_hit(self) -> None:
        fake_post = {
            "title": "How a GPU Actually Works",
            "slug": "how-a-gpu-actually-works",
            "html": "<h2>GPU Architecture</h2>",
            "url": "https://www.dailydoseofds.com/p/how-a-gpu-actually-works/",
        }
        with patch("mail_sources.dailydoseofds.fetch_ghost_post_by_slug", return_value=fake_post):
            article = dailydoseofds.fetch_canonical_article("How a GPU Actually Works")
            self.assertIsNotNone(article)
            self.assertEqual(article["content_tier"], "web_canonical")  # type: ignore[index]
            self.assertEqual(article["slug"], "how-a-gpu-actually-works")  # type: ignore[index]

    def test_ghost_api_fails_then_jina_reader_succeeds(self) -> None:
        """Ghost API 失败时，无缝降级到 Jina Reader (Level 1)。"""
        fake_jina = {
            "title": "How a GPU Actually Works",
            "slug": "how-a-gpu-actually-works",
            "canonical_url": "https://www.dailydoseofds.com/p/how-a-gpu-actually-works/",
            "content_tier": "web_canonical",
            "body": "## Full Content from Jina Fallback",
            "published_at": "",
        }
        with patch("mail_sources.dailydoseofds.fetch_ghost_post_by_slug", return_value=None), \
             patch("mail_sources.dailydoseofds.search_ghost_post_by_title", return_value=None), \
             patch("mail_sources.dailydoseofds.fetch_jina_reader_post", return_value=fake_jina):
            article = dailydoseofds.fetch_canonical_article("How a GPU Actually Works")
            self.assertIsNotNone(article)
            self.assertEqual(article["body"], "## Full Content from Jina Fallback")  # type: ignore[index]

    def test_all_web_fails_returns_none(self) -> None:
        """当 Ghost API 与 Jina Reader 均失败时返回 None，平滑触发 Level 2 邮件降级。"""
        with patch("mail_sources.dailydoseofds.fetch_ghost_post_by_slug", return_value=None), \
             patch("mail_sources.dailydoseofds.search_ghost_post_by_title", return_value=None), \
             patch("mail_sources.dailydoseofds.fetch_jina_reader_post", return_value=None):
            article = dailydoseofds.fetch_canonical_article("Unknown Article")
            self.assertIsNone(article)


class TestMailPipelineWebEnhancement(unittest.TestCase):
    """测试 mail_pipeline.py 中的 --fetch-web 参数与扩展 CLI 子命令。"""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_root = Path(self.temp_dir.name)
        self.archive_dir = self.test_root / "raw" / "articles"
        self.emails_dir = self.test_root / "Clippings" / "emails"
        self.pipeline_dir = self.emails_dir / ".pipeline"
        self.manifest_path = self.pipeline_dir / "manifest.json"
        self.status_path = self.pipeline_dir / "SYNC_STATUS.md"
        self.index_path = self.pipeline_dir / "ARCHIVE_INDEX.md"
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        self.emails_dir.mkdir(parents=True, exist_ok=True)
        self.pipeline_dir.mkdir(parents=True, exist_ok=True)

        # 打补丁将管线路径重定向到临时目录
        self.patchers = [
            patch.object(mail_pipeline, "ROOT", self.test_root),
            patch.object(mail_pipeline, "ARCHIVE_DIR", self.archive_dir),
            patch.object(mail_pipeline, "EMAILS_DIR", self.emails_dir),
            patch.object(mail_pipeline, "PIPELINE_DIR", self.pipeline_dir),
            patch.object(mail_pipeline, "MANIFEST_PATH", self.manifest_path),
            patch.object(mail_pipeline, "STATUS_PATH", self.status_path),
            patch.object(mail_pipeline, "INDEX_PATH", self.index_path),
        ]
        for p in self.patchers:
            p.start()

    def tearDown(self) -> None:
        for p in reversed(self.patchers):
            p.stop()
        self.temp_dir.cleanup()

    def _build_mock_email(self, title: str, link: str) -> str:
        content = (
            f"Subject: Daily DS Update\nFrom: avi@dailydoseofds.com\nDate: Mon, 10 Aug 2026 10:00:00 +0000\n"
            f"MIME-Version: 1.0\nContent-Type: text/html; charset=utf-8\n\n"
            f"<html><body><h2>{title}</h2>"
            f"<p>Teaser text from email. <a href=\"{link}\">Read full article online</a></p>"
            f"</body></html>"
        ).encode("utf-8")
        return base64.urlsafe_b64encode(content).decode("utf-8").rstrip("=")

    def test_pipeline_route_with_fetch_web_flag(self) -> None:
        """测试 mail_pipeline.route() 传递 fetch_web=True 生成带 web_canonical 的待审文章。"""
        raw_b64 = self._build_mock_email(
            "How a GPU Actually Works",
            "https://www.dailydoseofds.com/p/how-a-gpu-actually-works/",
        )
        fake_client = MagicMock()
        fake_client.fetch_raw_message.return_value = {"raw": raw_b64}

        data = {
            "schema_version": 2,
            "updated_at": "2026-09-15T00:00:00Z",
            "emails": {
                "msg001": {
                    "id": "msg001",
                    "lifecycle": "discovered",
                    "routing": "pending",
                    "source_key": "dailydoseofds",
                    "remote_starred": True,
                    "attempts": 0,
                    "articles": [],
                }
            },
        }

        fake_canonical = {
            "title": "How a GPU Actually Works",
            "slug": "how-a-gpu-actually-works",
            "canonical_url": "https://www.dailydoseofds.com/p/how-a-gpu-actually-works/",
            "content_tier": "web_canonical",
            "body": "## Full Web Article with CUDA Details",
            "published_at": "2026-08-18T00:00:00.000Z",
        }

        with patch("mail_sources.dailydoseofds.fetch_canonical_article", return_value=fake_canonical):
            processed, art_count = mail_pipeline.route(data, client=fake_client, fetch_web=True)
            self.assertEqual(processed, 1)
            self.assertEqual(art_count, 1)

            rec = data["emails"]["msg001"]
            self.assertEqual(rec["lifecycle"], "review")
            art = rec["articles"][0]
            self.assertEqual(art["content_tier"], "web_canonical")
            self.assertEqual(art["canonical_url"], "https://www.dailydoseofds.com/p/how-a-gpu-actually-works/")

            # 校验待审 Markdown 文件写入的内容
            staging_file = self.emails_dir / art["staging_file"]
            self.assertTrue(staging_file.exists())
            file_content = staging_file.read_text(encoding="utf-8")
            self.assertIn('content_tier: "web_canonical"', file_content)
            self.assertIn('canonical_url: "https://www.dailydoseofds.com/p/how-a-gpu-actually-works/"', file_content)
            self.assertIn("Full Web Article with CUDA Details", file_content)

    def test_pipeline_fetch_web_subcommand(self) -> None:
        """测试 fetch_web_article 单篇抓取生成标准规范文件。"""
        fake_canonical = {
            "title": "KV Cache Engineering",
            "slug": "kv-cache-engineering",
            "canonical_url": "https://www.dailydoseofds.com/p/kv-cache-engineering/",
            "content_tier": "web_canonical",
            "body": "## Python DynamicCache Implementation",
            "published_at": "2026-08-20T00:00:00.000Z",
        }
        with patch("mail_sources.dailydoseofds.fetch_canonical_article", return_value=fake_canonical):
            out_file = mail_pipeline.fetch_web_article("https://www.dailydoseofds.com/p/kv-cache-engineering/")
            self.assertTrue(out_file.exists())
            content = out_file.read_text(encoding="utf-8")
            self.assertIn('content_tier: "web_canonical"', content)
            self.assertIn('canonical_url: "https://www.dailydoseofds.com/p/kv-cache-engineering/"', content)
            self.assertIn("Python DynamicCache Implementation", content)

    def test_pipeline_check_web_upgrades(self) -> None:
        """测试 check_web_upgrades 正确比对存量文章并提出升级建议。"""
        # 创建一篇存量简短文章（无代码块，字数较少）
        sample_file = self.archive_dir / "2026-03-26_Breathing-KMeans_123.md"
        sample_file.write_text(
            "---\ntitle: Breathing KMeans\nsource_key: dailydoseofds\ncontent_tier: email_fallback\n---\n\n"
            "# Breathing KMeans\nShort summary in email without code.\n",
            encoding="utf-8",
        )

        fake_web = {
            "title": "Breathing KMeans",
            "slug": "breathing-kmeans",
            "canonical_url": "https://www.dailydoseofds.com/p/breathing-kmeans/",
            "content_tier": "web_canonical",
            "body": "## Full Algorithm\n```python\nimport bkmeans\nbk = bkmeans.BKMeans()\n```\n" + ("Extensive analysis text " * 50),
        }
        with patch("mail_sources.dailydoseofds.fetch_canonical_article", return_value=fake_web):
            report = mail_pipeline.check_web_upgrades(source_key="dailydoseofds")
            self.assertEqual(len(report), 1)
            item = report[0]
            self.assertEqual(item["status"], "upgrade_available")
            self.assertIn("强烈建议升级", item["recommendation"])
            self.assertGreater(item["web_chars"], item["local_chars"])
            self.assertGreater(item["web_codes"], item["local_codes"])

    def test_pipeline_upgrade_article(self) -> None:
        """测试 upgrade_article 覆盖更新文件并同步 Frontmatter 与 manifest。"""
        sample_file = self.archive_dir / "2026-03-26_Breathing-KMeans_123.md"
        sample_file.write_text(
            "---\n"
            "title: Breathing KMeans\n"
            "source_key: dailydoseofds\n"
            "email_id: msg-bk-01\n"
            "article_id: msg-bk-01:1\n"
            "content_tier: email_fallback\n"
            "tags: [Skill/data-analysis]\n"
            "---\n\n"
            "# Breathing KMeans\n\n- **邮件来源**: dailydoseofds\n- **发送人**: avi@dailydoseofds.com\n\n---\n\n"
            "Old brief content.\n",
            encoding="utf-8",
        )

        data = {
            "schema_version": 2,
            "updated_at": "2026-09-15T00:00:00Z",
            "emails": {
                "msg-bk-01": {
                    "id": "msg-bk-01",
                    "articles": [
                        {
                            "id": "msg-bk-01:1",
                            "file": sample_file.name,
                            "content_tier": "email_fallback",
                            "status": "ingested",
                        }
                    ],
                }
            },
        }

        fake_web = {
            "title": "Breathing KMeans",
            "slug": "breathing-kmeans",
            "canonical_url": "https://www.dailydoseofds.com/p/breathing-kmeans/",
            "content_tier": "web_canonical",
            "body": "## Full Algorithm Implementation\n\n```python\n# Full Code\n```",
        }

        with patch("mail_sources.dailydoseofds.fetch_canonical_article", return_value=fake_web):
            mail_pipeline.upgrade_article(data, str(sample_file))
            new_text = sample_file.read_text(encoding="utf-8")
            self.assertIn('content_tier: "web_canonical"', new_text)
            self.assertIn('canonical_url: "https://www.dailydoseofds.com/p/breathing-kmeans/"', new_text)
            self.assertIn("Skill/data-analysis", new_text, "原有 tags 应被完整保留")
            self.assertIn("Full Algorithm Implementation", new_text)

            # 校验 manifest 同步更新
            art = data["emails"]["msg-bk-01"]["articles"][0]
            self.assertEqual(art["content_tier"], "web_canonical")
            self.assertEqual(art["canonical_url"], "https://www.dailydoseofds.com/p/breathing-kmeans/")

    def test_pipeline_reconcile_syncs_metadata(self) -> None:
        """测试 reconcile() 对账时同步已归档文献的 content_tier 与 canonical_url。"""
        archived = self.archive_dir / "2026-08-18_How-a-GPU-Actually-Works_abc.md"
        archived.write_text(
            "---\ntitle: GPU\ncontent_tier: web_canonical\ncanonical_url: https://www.dailydoseofds.com/p/gpu/\n---\n",
            encoding="utf-8",
        )
        data = {
            "schema_version": 2,
            "updated_at": "2026-09-15T00:00:00Z",
            "emails": {
                "msg_rec": {
                    "id": "msg_rec",
                    "lifecycle": "review",
                    "articles": [
                        {
                            "id": "msg_rec:1",
                            "file": archived.name,
                            "staging_file": f"dailydoseofds/{archived.name}",
                            "status": "review",
                            "content_tier": "email_fallback",
                        }
                    ],
                }
            },
        }
        reconciled = mail_pipeline.reconcile(data)
        self.assertEqual(reconciled, 1)
        art = data["emails"]["msg_rec"]["articles"][0]
        self.assertEqual(art["status"], "ingested")
        self.assertEqual(art["content_tier"], "web_canonical")
        self.assertEqual(art["canonical_url"], "https://www.dailydoseofds.com/p/gpu/")

    def test_check_web_upgrades_single_target_and_pending_only(self) -> None:
        """测试 check_web_upgrades 支持单篇 target 与 pending_only 增量跳过。"""
        # 创建两篇归档文章：一篇已是 web_canonical，另一篇是 email_fallback
        f1 = self.archive_dir / "2026-08-01_Article-One_111.md"
        f1.write_text(
            '---\nsource_key: "dailydoseofds"\ntitle: "Article One"\ncontent_tier: "web_canonical"\ncanonical_url: "https://www.dailydoseofds.com/p/article-one/"\n---\n\n## Section 1\nSome body\n',
            encoding="utf-8",
        )
        f2 = self.archive_dir / "2026-08-02_Article-Two_222.md"
        f2.write_text(
            '---\nsource_key: "dailydoseofds"\ntitle: "Article Two"\ncontent_tier: "email_fallback"\n---\n\nShort email body\n',
            encoding="utf-8",
        )

        with unittest.mock.patch.object(mail_pipeline.dailydoseofds, "fetch_canonical_article") as mock_fetch:
            mock_fetch.return_value = {
                "title": "Article Two",
                "slug": "article-two",
                "canonical_url": "https://www.dailydoseofds.com/p/article-two/",
                "body": "## Section 1\nExpanded body with code:\n```python\nprint(1)\n```\n",
                "content_tier": "web_canonical",
            }

            # 1. 测试 pending_only: f1 已是 web_canonical，应跳过 mock_fetch 调用
            results = mail_pipeline.check_web_upgrades(pending_only=True)
            self.assertEqual(len(results), 2)
            res1 = next(r for r in results if r["file"] == f1.name)
            self.assertEqual(res1["status"], "up_to_date")
            self.assertIn("已跳过网络检测", res1["recommendation"])

            # mock_fetch 只应针对 f2 触发 1 次，而不是 2 次
            self.assertEqual(mock_fetch.call_count, 1)

            # 2. 测试单篇 target 过滤
            mock_fetch.reset_mock()
            single_res = mail_pipeline.check_web_upgrades(target=f2.name)
            self.assertEqual(len(single_res), 1)
            self.assertEqual(single_res[0]["file"], f2.name)
            self.assertEqual(single_res[0]["status"], "upgrade_available")
            self.assertEqual(mock_fetch.call_count, 1)

    def test_diff_web_article_headings_and_diff(self) -> None:
        """测试 diff_web_article 正确提取章节目录结构及 Unified Diff。"""
        f = self.archive_dir / "2026-08-03_Diff-Test_333.md"
        f.write_text(
            '---\nsource_key: "dailydoseofds"\ntitle: "Diff Test"\ncontent_tier: "email_fallback"\n---\n\n## Local Section 1\nOld content\n',
            encoding="utf-8",
        )

        with unittest.mock.patch.object(mail_pipeline.dailydoseofds, "fetch_canonical_article") as mock_fetch:
            mock_fetch.return_value = {
                "title": "Diff Test",
                "slug": "diff-test",
                "canonical_url": "https://www.dailydoseofds.com/p/diff-test/",
                "body": "## Web Section 1\nNew content\n\n### Web Subsection\nDetail",
                "content_tier": "web_canonical",
            }

            diff_data = mail_pipeline.diff_web_article(target=str(f))
            self.assertEqual(diff_data["file"], f.name)
            self.assertEqual(diff_data["local_headings"], ["## Local Section 1"])
            self.assertEqual(diff_data["web_headings"], ["## Web Section 1", "### Web Subsection"])
            self.assertGreater(len(diff_data["diff_lines"]), 0)
            diff_text = "".join(diff_data["diff_lines"])
            self.assertIn("-Old content", diff_text)
            self.assertIn("+New content", diff_text)

    def test_upgrade_article_dry_run_and_diff(self) -> None:
        """测试 upgrade_article 的 --dry-run 预览机制不修改文件。"""
        f = self.archive_dir / "2026-08-04_Dryrun-Test_444.md"
        original_content = (
            '---\nsource_key: "dailydoseofds"\ntitle: "Dryrun Test"\ncontent_tier: "email_fallback"\n---\n\nOriginal body\n'
        )
        f.write_text(original_content, encoding="utf-8")
        data = {"schema_version": 2, "emails": {}}

        with unittest.mock.patch.object(mail_pipeline.dailydoseofds, "fetch_canonical_article") as mock_fetch:
            mock_fetch.return_value = {
                "title": "Dryrun Test",
                "slug": "dryrun-test",
                "canonical_url": "https://www.dailydoseofds.com/p/dryrun-test/",
                "body": "New full web body",
                "content_tier": "web_canonical",
            }

            # 执行 dry_run
            mail_pipeline.upgrade_article(data, target=str(f), dry_run=True, show_diff=True)
            # 验证文件并未被物理覆盖
            self.assertEqual(f.read_text(encoding="utf-8"), original_content)

            # 执行物理升级
            mail_pipeline.upgrade_article(data, target=str(f), dry_run=False)
            self.assertIn("content_tier: \"web_canonical\"", f.read_text(encoding="utf-8"))
            self.assertIn("New full web body", f.read_text(encoding="utf-8"))


class TestLiveGhostApi(unittest.TestCase):
    """实网连通性健全性测试 (Live Sanity Test)。"""

    def test_live_ghost_api_query(self) -> None:
        """测试对真实 Ghost Content API 的连通性与数据完整性。"""
        target_slug = "how-a-gpu-actually-works"
        try:
            post = dailydoseofds.fetch_ghost_post_by_slug(target_slug, timeout=10.0)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            self.skipTest(f"实网连接不可用，跳过实网健全性测试: {exc}")
            return

        if post is None:
            self.skipTest(f"无法从线上 Ghost API 获取 '{target_slug}'（可能因网络代理或环境受限），跳过实网测试。")
            return

        self.assertEqual(post.get("slug"), target_slug)
        self.assertIn("GPU", str(post.get("title")))
        self.assertTrue(str(post.get("url", "")).startswith("https://www.dailydoseofds.com/p/"))

        html_content = post.get("html", "")
        self.assertGreater(len(html_content), 5000, "官网全量长文 HTML 长度应显著大于 5KB")

        markdown = dailydoseofds.convert_html_to_markdown(html_content)
        self.assertIn("##", markdown, "长文 Markdown 应包含至少一个二级标题")
        self.assertGreater(len(markdown), 3000, "转换后 Markdown 长度应大于 3000 字符")


if __name__ == "__main__":
    unittest.main()
