#!/usr/bin/env python3
"""Dependency-free static site server backed by Git-tracked Markdown."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

LEARNING_SLUG = re.compile(r"^\d{6}-[A-Za-z][A-Za-z0-9]*-[A-Za-z0-9][A-Za-z0-9-]{0,95}$")
RESEARCH_DOCUMENT = ("研究记录.md", "研究记录")


def safe_learning_slug(raw: str) -> str:
    slug = unquote(raw).strip()
    if not LEARNING_SLUG.fullmatch(slug):
        raise ValueError("invalid daily learning slug")
    return slug


def learning_metadata(slug: str, markdown: str, modified: str) -> dict:
    title_match = re.search(r"^#\s+(.+)$", markdown, re.M)
    paper_match = re.search(r"^>\s*论文：\*?(.+?)\*?\s{0,2}$", markdown, re.M)
    doi_match = re.search(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", markdown)
    match = paper_match or title_match
    return {"slug": slug, "date": f"20{slug[:2]}-{slug[2:4]}-{slug[4:6]}",
            "author": slug.split("-", 2)[1], "shortName": slug.split("-", 2)[2],
            "title": match.group(1).strip("* ") if match else slug,
            "doi": doi_match.group(0).rstrip(").,") if doi_match else "", "modified": modified}


def file_modified(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()


class SiteHandler(SimpleHTTPRequestHandler):
    server_version = "Keblog/3.0"

    @property
    def content_dir(self) -> Path:
        return self.server.content_dir

    @property
    def learning_dir(self) -> Path:
        return self.content_dir / "daily-learning"

    @property
    def research_document_path(self) -> Path:
        default = self.content_dir / "research" / RESEARCH_DOCUMENT[0]
        return Path(os.environ.get("RESEARCH_DOCUMENT_FILE", default)).resolve()

    def end_headers(self) -> None:
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, HEAD, OPTIONS")
        super().end_headers()

    def log_message(self, fmt: str, *args) -> None:
        print(f"{self.address_string()} - {fmt % args}", flush=True)

    def send_json(self, status: int, payload: dict, headers: dict | None = None) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        for key, value in (headers or {}).items(): self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body)

    def send_markdown_json(self, path: Path, name: str | None = None) -> None:
        if not path.is_file():
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "document not found"})
            return
        raw = path.read_bytes()
        etag = hashlib.sha256(raw).hexdigest()
        self.send_json(HTTPStatus.OK, {"name": name or path.name, "content": raw.decode("utf-8"),
            "modified": file_modified(path), "etag": etag}, {"ETag": f'"{etag}"'})

    def learning_entries(self) -> list[dict]:
        entries = []
        if self.learning_dir.is_dir():
            for directory in self.learning_dir.iterdir():
                if not directory.is_dir() or not LEARNING_SLUG.fullmatch(directory.name): continue
                path = directory / "README.md"
                if path.is_file():
                    entries.append(learning_metadata(directory.name, path.read_text("utf-8"), file_modified(path)))
        return sorted(entries, key=lambda item: (item["date"], item["slug"]), reverse=True)

    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self) -> None:
        route = unquote(urlparse(self.path).path)
        if route == "/api/health":
            self.send_json(200, {"status": "ok", "service": "keblog", "version": "3.0", "source": "git"}); return
        if route == "/api/research/document":
            self.send_markdown_json(self.research_document_path, RESEARCH_DOCUMENT[1]); return
        if route in {"/api/documents/paperpool.md", "/api/v1/paper-pool"}:
            self.send_markdown_json(self.content_dir / "documents" / "paperpool.md"); return
        if route in {"/api/v1/prompt", "/api/documents/daily-task-prompt.md"}:
            self.send_markdown_json(self.content_dir / "support" / "prompt.txt", "daily-task-prompt.md"); return
        if route == "/api/daily-learning":
            self.send_json(200, {"entries": self.learning_entries()}); return
        if route.startswith("/api/daily-learning/"):
            item = route.removeprefix("/api/daily-learning/")
            if item == "index": path = self.learning_dir / "README.md"
            elif item == "plan": path = self.learning_dir / "PLAN.md"
            else:
                try: path = self.learning_dir / safe_learning_slug(item) / "README.md"
                except ValueError as error:
                    self.send_json(400, {"error": str(error)}); return
            self.send_markdown_json(path); return
        if route == "/api/v1/bootstrap":
            pool, plan, prompt = self.content_dir / "documents" / "paperpool.md", self.learning_dir / "PLAN.md", self.content_dir / "support" / "prompt.txt"
            self.send_json(200, {"sourceOfTruth": "Git repository content",
                "paperPool": pool.read_text("utf-8") if pool.is_file() else "",
                "dailyPlan": plan.read_text("utf-8") if plan.is_file() else "",
                "prompt": prompt.read_text("utf-8") if prompt.is_file() else "",
                "completed": self.learning_entries()}); return
        if route.startswith("/api/"):
            self.send_json(404, {"error": "read-only endpoint not found"}); return
        super().do_GET()

    def reject_write(self) -> None:
        self.send_json(405, {"error": "keblog content is maintained through GitHub; commit content changes to the repository"}, {"Allow": "GET, HEAD, OPTIONS"})

    do_POST = reject_write
    do_PUT = reject_write
    do_PATCH = reject_write
    do_DELETE = reject_write


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--dev", action="store_true"); args = parser.parse_args()
    project = Path(__file__).resolve().parents[1]
    static_root = Path(os.environ.get("SITE_STATIC_DIR", project / ("src-static" if args.dev else "dist"))).resolve()
    content_root = Path(os.environ.get("SITE_CONTENT_DIR", project / "content")).resolve()
    os.chdir(static_root)
    host, port = os.environ.get("SITE_HOST", "127.0.0.1"), int(os.environ.get("SITE_PORT", "8080"))
    print(f"Serving {static_root} with content from {content_root} on http://{host}:{port}", flush=True)
    server = ThreadingHTTPServer((host, port), SiteHandler); server.content_dir = content_root; server.serve_forever()


if __name__ == "__main__": main()
