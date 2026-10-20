import json
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from functools import partial
from http.server import ThreadingHTTPServer
from http.cookiejar import CookieJar
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "server"))
from community import CommunityStore
from content_server import SiteHandler


class QuietHandler(SiteHandler):
    def log_message(self, *_args):
        pass


class CommunityHTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        root = Path(cls.temp.name)
        static = root / "static"; static.mkdir(); (static / "index.html").write_text("home")
        content = root / "content"; (content / "daily-learning" / "260910-Test-Paper").mkdir(parents=True)
        (content / "daily-learning" / "260910-Test-Paper" / "README.md").write_text("# Test\n\nA paragraph for notes.\n")
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=static))
        cls.server.content_dir = content
        cls.server.community_store = CommunityStore(root / "community.sqlite3")
        cls.server.cookie_secure = False
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True); cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"
        cls.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CookieJar()))

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.temp.cleanup()

    def request(self, path, method="GET", payload=None):
        data = None
        headers = {}
        if payload is not None:
            data = json.dumps(payload).encode()
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(self.base + path, data=data, headers=headers, method=method)
        try:
            with self.opener.open(request) as response:
                return response.status, response.headers, json.loads(response.read())
        except urllib.error.HTTPError as error:
            return error.code, error.headers, json.loads(error.read())

    def test_public_reading_and_login_gate(self):
        status, _, payload = self.request("/api/articles/260910-Test-Paper/community")
        self.assertEqual(status, 200)
        self.assertIsNone(payload["user"])
        self.assertIsNone(payload["status"])
        status, _, payload = self.request("/api/articles/statuses?slugs=260910-Test-Paper")
        self.assertEqual((status, payload["statuses"]), (200, {"260910-Test-Paper": None}))
        self.assertEqual(self.request("/api/articles/260910-Test-Paper/comments", "POST", {"content": "blocked"})[0], 401)

    def test_register_status_note_comment_and_logout(self):
        status, headers, payload = self.request(
            "/api/auth/register", "POST", {"username": "reader_one", "password": "a-secure-pass", "displayName": "Reader One"}
        )
        self.assertEqual(status, 200)
        self.assertIn("keblog_session", headers.get("Set-Cookie", ""))
        self.assertEqual(payload["user"]["displayName"], "Reader One")

        status, _, payload = self.request("/api/articles/260910-Test-Paper/community")
        self.assertEqual((status, payload["status"]), (200, "unread"))
        self.assertEqual(self.request("/api/articles/260910-Test-Paper/status", "POST", {"status": "read"})[0], 200)
        status, _, payload = self.request("/api/articles/statuses?slugs=260910-Test-Paper")
        self.assertEqual((status, payload["statuses"]), (200, {"260910-Test-Paper": "read"}))
        note = self.request(
            "/api/articles/260910-Test-Paper/notes", "POST",
            {"quote": "A paragraph", "start": 9, "end": 21, "content": "记下证据。"},
        )
        self.assertEqual(note[0], 201)
        comment = self.request("/api/articles/260910-Test-Paper/comments", "POST", {"content": "我的评论"})
        self.assertEqual(comment[0], 201)

        status, _, payload = self.request("/api/articles/260910-Test-Paper/community")
        self.assertEqual(payload["status"], "read")
        self.assertEqual(payload["notes"][0]["content"], "记下证据。")
        self.assertEqual(payload["comments"][0]["content"], "我的评论")

        self.assertEqual(self.request("/api/auth/logout", "POST")[0], 200)
        self.assertEqual(self.request("/api/articles/260910-Test-Paper/status", "POST", {"status": "deeper"})[0], 401)
        status, _, payload = self.request("/api/articles/260910-Test-Paper/community")
        self.assertEqual(status, 200)
        self.assertIsNone(payload["user"])
        self.assertEqual(len(payload["notes"]), 1)

    def test_validation_and_duplicate_username(self):
        status, _, _ = self.request("/api/auth/register", "POST", {"username": "bad", "password": "short"})
        self.assertEqual(status, 400)
        status, _, _ = self.request(
            "/api/auth/register", "POST", {"username": "reader_two", "password": "a-secure-pass", "displayName": "Two"}
        )
        self.assertEqual(status, 200)
        status, _, payload = self.request(
            "/api/auth/register", "POST", {"username": "READER_TWO", "password": "a-secure-pass", "displayName": "Duplicate"}
        )
        self.assertEqual(status, 409)
        self.assertEqual(payload["error"], "username_taken")


if __name__ == "__main__":
    unittest.main()
