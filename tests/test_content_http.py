import json
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from functools import partial
from http.server import ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "server"))
from content_server import SiteHandler


class QuietHandler(SiteHandler):
    def log_message(self, *_args): pass


class ContentHTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        root = Path(cls.temp.name)
        static = root / "static"; static.mkdir(); (static / "index.html").write_text("home")
        content = root / "content"; (content / "documents").mkdir(parents=True); (content / "daily-learning" / "260910-Test-Paper").mkdir(parents=True); (content / "support").mkdir()
        (content / "documents" / "paperpool.md").write_text("# Paper Pool\n")
        (content / "daily-learning" / "README.md").write_text("# Index\n")
        (content / "daily-learning" / "PLAN.md").write_text("# Plan\n")
        (content / "daily-learning" / "260910-Test-Paper" / "README.md").write_text("# Reading\n\n> 论文：*Test Paper*  \n")
        (content / "support" / "prompt.txt").write_text("task prompt")
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=static))
        cls.server.content_dir = content
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True); cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.temp.cleanup()

    def request(self, path, method="GET"):
        try:
            with urllib.request.urlopen(urllib.request.Request(self.base + path, method=method)) as response:
                return response.status, json.loads(response.read())
        except urllib.error.HTTPError as error:
            return error.code, json.loads(error.read())

    def test_git_content_routes(self):
        self.assertEqual(self.request("/api/health")[1]["source"], "git")
        self.assertIn("Paper Pool", self.request("/api/documents/paperpool.md")[1]["content"])
        entries = self.request("/api/daily-learning")[1]["entries"]
        self.assertEqual([entry["slug"] for entry in entries], ["260910-Test-Paper"])
        self.assertIn("Test Paper", self.request("/api/daily-learning/260910-Test-Paper")[1]["content"])
        self.assertEqual(self.request("/api/v1/bootstrap")[1]["sourceOfTruth"], "Git repository content")

    def test_writes_and_old_v2_are_unavailable(self):
        self.assertEqual(self.request("/api/daily-learning/260910-Test-Paper", "PUT")[0], 405)
        self.assertEqual(self.request("/api/v2/context")[0], 404)


if __name__ == "__main__": unittest.main()
