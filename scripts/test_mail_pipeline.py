import base64
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import mail_pipeline
from mail_sources import dailydoseofds


class FakeClient:
    def __init__(self, messages=None, raw_map=None):
        self.messages = messages or []
        self.raw_map = raw_map or {}
        self.closed = False

    def connect(self):
        pass

    def list_starred_messages(self):
        return self.messages

    def fetch_raw_message(self, message_id):
        return self.raw_map.get(message_id, {"raw": ""})

    def close(self):
        self.closed = True


class MailPipelineTest(unittest.TestCase):
    def test_remote_list_follows_all_pages(self):
        client = mail_pipeline.GmailImapClient(
            {"email": "test@example.com", "app_password": "pwd", "imap_server": "imap.example.com", "imap_port": 993}
        )
        client.mail = unittest.mock.MagicMock()
        client.get_starred_mailbox = unittest.mock.MagicMock(return_value="[Gmail]/Starred")
        client.mail.select.return_value = ("OK", [b"100"])
        # Mock 60 UIDs to trigger batching (> 50)
        uids = [str(i).encode() for i in range(1, 61)]
        client.mail.uid.side_effect = [
            ("OK", [b" ".join(uids)]),  # SEARCH
            ("OK", [(b'1 (X-GM-MSGID 12345 BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)] {20}', b"From: a@b.com\r\n\r\n")]),  # batch 1
            ("OK", [(b'2 (X-GM-MSGID 67890 BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)] {20}', b"From: c@d.com\r\n\r\n")]),  # batch 2
        ]
        results = client.list_starred_messages()
        self.assertEqual(len(results), 2)
        self.assertEqual([r["id"] for r in results], [f"{12345:x}", f"{67890:x}"])
        self.assertEqual(client.mail.uid.call_count, 3)

    def test_sync_marks_unknown_sender_without_raw_fetch(self):
        data = mail_pipeline.empty_manifest()
        client = FakeClient(
            messages=[{
                "id": "unknown",
                "sender": "Other <news@example.com>",
                "subject": "Other",
                "date": "Mon, 10 Aug 2026 10:00:00 +0000",
            }]
        )

        self.assertEqual(mail_pipeline.sync(data, client), (1, 1))
        record = data["emails"]["unknown"]
        self.assertEqual(record["lifecycle"], "unhandled")
        self.assertIsNone(record["source_key"])

    def test_ddods_parser_filters_membership_footer(self):
        membership = base64.urlsafe_b64encode(b"https://www.dailydoseofds.com/membership").decode().rstrip("=")
        raw = (
            "Subject: Weekly\nFrom: avi@dailydoseofds.com\nDate: Mon, 10 Aug 2026 10:00:00 +0000\n"
            "MIME-Version: 1.0\nContent-Type: text/html; charset=utf-8\n\n"
            "<html><body><h2>First</h2><p>A</p><h2>Second</h2><p>B</p>"
            f'<h2><a href="https://click.kit-mail3.com/x/{membership}">Succeed in AI Engineering roles</a></h2>'
            "<p>Master full-stack AI engineering</p></body></html>"
        ).encode()
        metadata, articles = dailydoseofds.parse("abcdef123456", {"raw": base64.urlsafe_b64encode(raw).decode().rstrip("=")})
        self.assertEqual(metadata["formatted_date"], "2026-08-10")
        self.assertEqual([article["title"] for article in articles], ["First", "Second"])

    def test_article_filename_excludes_source_key(self):
        self.assertEqual(
            mail_pipeline.article_filename(
                "2026-08-10",
                " How to query billion+ rows on postgres without overhead ",
                "19febef2c6003814",
            ),
            "2026-08-10_How-to-query-billion+-rows-on-postgres-without-overhead_19febef2c6003814.md",
        )

    def test_reconcile_updates_only_archived_article(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / "raw" / "articles"
            archive.mkdir(parents=True)
            record = mail_pipeline.new_email_record("mail")
            record["source_key"] = "dailydoseofds"
            record["articles"] = [
                {"id": "mail:1", "file": "kept.md", "status": "review", "title": "Kept"},
                {"id": "mail:2", "file": "skip.md", "status": "review", "title": "Skip"},
            ]
            data = mail_pipeline.empty_manifest()
            data["emails"]["mail"] = record
            (archive / "kept.md").write_text("# Kept\n", encoding="utf-8")
            staging = root / "Clippings" / "emails"
            (staging / "dailydoseofds").mkdir(parents=True)
            (staging / "dailydoseofds" / "skip.md").write_text("# Skip\n", encoding="utf-8")
            record["articles"][0]["staging_file"] = "dailydoseofds/kept.md"
            record["articles"][1]["staging_file"] = "dailydoseofds/skip.md"
            with patch.object(mail_pipeline, "ARCHIVE_DIR", archive), patch.object(mail_pipeline, "EMAILS_DIR", staging):
                self.assertEqual(mail_pipeline.reconcile(data), 1)
            self.assertEqual(record["articles"][0]["status"], "ingested")
            self.assertEqual(record["articles"][1]["status"], "review")
            self.assertEqual(record["lifecycle"], "review")

            (staging / "dailydoseofds" / "skip.md").unlink()
            with patch.object(mail_pipeline, "ARCHIVE_DIR", archive), patch.object(mail_pipeline, "EMAILS_DIR", staging):
                self.assertEqual(mail_pipeline.reconcile(data), 0)
            self.assertEqual(record["articles"][1]["status"], "rejected")
            self.assertEqual(record["articles"][1]["reason"], "manual_delete")

    def test_reconcile_preserves_routing_failure_for_retry(self):
        data = mail_pipeline.empty_manifest()
        record = mail_pipeline.new_email_record("mail")
        record.update({
            "source_key": "dailydoseofds",
            "lifecycle": "failed",
            "routing": "failed",
            "last_error": "temporary network error",
        })
        data["emails"]["mail"] = record

        self.assertEqual(mail_pipeline.reconcile(data), 0)
        self.assertEqual(record["lifecycle"], "failed")
        self.assertEqual(record["routing"], "failed")

    def test_route_retries_a_failed_message(self):
        data = mail_pipeline.empty_manifest()
        record = mail_pipeline.new_email_record("mail")
        record.update({
            "source_key": "test",
            "lifecycle": "failed",
            "routing": "failed",
            "attempts": 1,
            "last_error": "temporary network error",
        })
        data["emails"]["mail"] = record

        source = mail_pipeline.Source(
            key="test",
            addresses=(),
            domains=(),
            parser=lambda _message_id, _response: (
                {"sender": "test@example.com", "subject": "Test", "date": "Mon", "formatted_date": "2026-08-11"},
                [],
            ),
        )
        with patch.object(mail_pipeline, "SOURCES_BY_KEY", {"test": source}):
            self.assertEqual(mail_pipeline.route(data, FakeClient(raw_map={"mail": {"raw": ""}})), (1, 0))

        self.assertEqual(record["attempts"], 2)
        self.assertEqual(record["routing"], "parsed")
        self.assertEqual(record["lifecycle"], "ignored")
        self.assertIsNone(record["last_error"])


if __name__ == "__main__":
    unittest.main()
