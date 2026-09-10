#!/usr/bin/env python3
"""Receive authenticated GitHub push events and queue a keblog update."""

import hashlib
import hmac
import json
import os
import subprocess
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


SECRET = os.environ["GITHUB_WEBHOOK_SECRET"].encode()
REPOSITORY = "JoyTrndsttr/keblog"
BRANCH = "refs/heads/master"
MAX_BODY_BYTES = 2 * 1024 * 1024


class Handler(BaseHTTPRequestHandler):
    def reply(self, status, message):
        body = message.encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/github-webhook":
            self.reply(HTTPStatus.NOT_FOUND, "not found")
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self.reply(HTTPStatus.BAD_REQUEST, "invalid content length")
            return
        if not 0 < length <= MAX_BODY_BYTES:
            self.reply(HTTPStatus.BAD_REQUEST, "invalid body size")
            return

        body = self.rfile.read(length)
        signature = self.headers.get("X-Hub-Signature-256", "")
        expected = "sha256=" + hmac.new(SECRET, body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected):
            self.reply(HTTPStatus.UNAUTHORIZED, "invalid signature")
            return

        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            self.reply(HTTPStatus.BAD_REQUEST, "invalid json")
            return

        if payload.get("repository", {}).get("full_name") != REPOSITORY:
            self.reply(HTTPStatus.FORBIDDEN, "wrong repository")
            return

        event = self.headers.get("X-GitHub-Event", "")
        if event == "ping":
            self.reply(HTTPStatus.OK, "pong")
            return
        if event != "push":
            self.reply(HTTPStatus.ACCEPTED, "ignored event")
            return
        if payload.get("ref") != BRANCH:
            self.reply(HTTPStatus.ACCEPTED, "ignored branch")
            return

        subprocess.Popen(
            ["/usr/bin/systemctl", "start", "--no-block", "keblog-update.service"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        self.reply(HTTPStatus.ACCEPTED, "deployment queued")

    def log_message(self, message, *args):
        print(f"{self.address_string()} {message % args}", flush=True)


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", 8090), Handler).serve_forever()
