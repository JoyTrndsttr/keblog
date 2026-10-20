#!/usr/bin/env python3
"""Dependency-free static site server backed by Git-tracked Markdown."""
from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
import re
from datetime import datetime, timezone
from email.utils import format_datetime
from http import HTTPStatus
from http.cookies import CookieError, SimpleCookie
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from community import CommunityError, CommunityStore

LEARNING_SLUG = re.compile(r"^\d{6}-[A-Za-z][A-Za-z0-9]*-[A-Za-z0-9][A-Za-z0-9-]{0,95}$")
RESEARCH_DOCUMENT = ("研究记录.md", "研究记录")
SESSION_COOKIE = "keblog_session"
MAX_JSON_BYTES = 128 * 1024


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

    @property
    def research_workbench_dir(self) -> Path:
        default = self.content_dir / "research" / "workbench"
        return Path(os.environ.get("RESEARCH_WORKBENCH_DIR", default)).resolve()

    @property
    def community_store(self) -> CommunityStore:
        return self.server.community_store

    @property
    def cookie_secure(self) -> bool:
        return bool(getattr(self.server, "cookie_secure", False))

    def send_workbench_file(self, route: str) -> None:
        relative = route.removeprefix("/research/workbench/")
        root = self.research_workbench_dir
        candidate = (root / relative).resolve()
        try:
            candidate.relative_to(root)
        except ValueError:
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        if candidate.is_dir():
            candidate /= "index.html"
        if not candidate.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        body = candidate.read_bytes()
        content_type = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
        if content_type == "text/html":
            page = body.decode("utf-8")
            shell_style = '<link rel="stylesheet" href="/workbench-shell.css?v=20261002">'
            shell_link = ('<a class="keblog-return" href="/research/" aria-label="返回研究页">'
                          '<span aria-hidden="true">←</span><b>返回研究</b></a>')
            lower = page.lower()
            head_marker = lower.find("</head>")
            if head_marker >= 0:
                page = page[:head_marker] + shell_style + page[head_marker:]
            else:
                page = shell_style + page
            lower = page.lower()
            body_marker = lower.rfind("</body>")
            if body_marker >= 0:
                page = page[:body_marker] + shell_link + page[body_marker:]
            else:
                html_marker = lower.rfind("</html>")
                page = page[:html_marker] + shell_link + page[html_marker:] if html_marker >= 0 else page + shell_link
            body = page.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def end_headers(self) -> None:
        route = urlparse(self.path).path
        if route.endswith("/") or route.endswith(".html"):
            self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        if route.startswith("/research/workbench/"):
            # Workbench artifacts are self-contained exports whose CSS and
            # interaction code intentionally live in inline style/script tags.
            content_security_policy = "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
        else:
            content_security_policy = "default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
        self.send_header("Content-Security-Policy", content_security_policy)
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

    def _session_token(self) -> str | None:
        cookies = SimpleCookie()
        try:
            cookies.load(self.headers.get("Cookie", ""))
        except CookieError:
            return None
        morsel = cookies.get(SESSION_COOKIE)
        return morsel.value if morsel else None

    def _current_user(self) -> dict | None:
        return self.community_store.user_for_session(self._session_token())

    def _set_session_cookie(self, token: str, expires_at: int) -> str:
        cookie = SimpleCookie()
        cookie[SESSION_COOKIE] = token
        morsel = cookie[SESSION_COOKIE]
        morsel["path"] = "/"
        morsel["httponly"] = True
        morsel["samesite"] = "Lax"
        morsel["max-age"] = str(max(0, expires_at - int(datetime.now(timezone.utc).timestamp())))
        if self.cookie_secure:
            morsel["secure"] = True
        return morsel.OutputString()

    def _clear_session_cookie(self) -> str:
        cookie = SimpleCookie()
        cookie[SESSION_COOKIE] = ""
        morsel = cookie[SESSION_COOKIE]
        morsel["path"] = "/"
        morsel["httponly"] = True
        morsel["samesite"] = "Lax"
        morsel["max-age"] = "0"
        morsel["expires"] = format_datetime(datetime.now(timezone.utc), usegmt=True)
        if self.cookie_secure:
            morsel["secure"] = True
        return morsel.OutputString()

    def _read_json(self) -> dict:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as error:
            raise CommunityError(400, "invalid_body", "请求体长度无效。") from error
        if length <= 0 or length > MAX_JSON_BYTES:
            raise CommunityError(400, "invalid_body", "请求体为空或超过大小限制。")
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise CommunityError(400, "invalid_json", "请求体必须是有效 JSON。") from error
        if not isinstance(payload, dict):
            raise CommunityError(400, "invalid_json", "请求体必须是 JSON 对象。")
        return payload

    def _send_community_error(self, error: CommunityError) -> None:
        self.send_json(error.status, {"error": error.code, "message": error.message})

    def _require_user(self) -> dict | None:
        user = self._current_user()
        if user is None:
            self.send_json(HTTPStatus.UNAUTHORIZED, {"error": "login_required", "message": "请先登录后再进行此操作。"})
        return user

    def _article_slug(self, raw_slug: str) -> str | None:
        try:
            slug = safe_learning_slug(raw_slug)
        except ValueError:
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "article_not_found", "message": "文章不存在。"})
            return None
        if not (self.learning_dir / slug / "README.md").is_file():
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "article_not_found", "message": "文章不存在。"})
            return None
        return slug

    def _article_route(self, route: str) -> tuple[str, str] | None:
        parts = route.split("/")
        if len(parts) != 5 or parts[0] or parts[1] != "api" or parts[2] != "articles":
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
            return None
        return parts[3], parts[4]

    def _handle_auth_post(self, route: str) -> None:
        try:
            if route == "/api/auth/logout":
                self.community_store.logout(self._session_token())
                self.send_json(HTTPStatus.OK, {"user": None}, {"Set-Cookie": self._clear_session_cookie()})
                return
            payload = self._read_json()
            if route == "/api/auth/register":
                user, token, expires_at = self.community_store.register(
                    payload.get("username", ""), payload.get("password", ""), payload.get("displayName")
                )
            elif route == "/api/auth/login":
                user, token, expires_at = self.community_store.login(payload.get("username", ""), payload.get("password", ""))
            else:
                self.send_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
                return
            self.send_json(HTTPStatus.OK, {"user": user}, {"Set-Cookie": self._set_session_cookie(token, expires_at)})
        except CommunityError as error:
            self._send_community_error(error)

    def _handle_statuses_get(self, query: str) -> None:
        params = parse_qs(query, keep_blank_values=False)
        raw_slugs = params.get('slugs', [''])[0]
        requested = []
        for raw_slug in raw_slugs.split(','):
            if not raw_slug:
                continue
            try:
                slug = safe_learning_slug(raw_slug)
            except ValueError:
                continue
            if slug not in requested:
                requested.append(slug)
        if len(requested) > 100:
            self.send_json(HTTPStatus.BAD_REQUEST, {'error': 'too_many_articles', 'message': '一次最多查询 100 篇文章。'})
            return
        available = {entry['slug'] for entry in self.learning_entries()}
        slugs = [slug for slug in requested if slug in available]
        user = self._current_user()
        self.send_json(HTTPStatus.OK, {'statuses': self.community_store.reading_statuses(user['id'] if user else None, slugs)})

    def _handle_article_get(self, route: str) -> None:
        parsed = self._article_route(route)
        if parsed is None:
            return
        raw_slug, resource = parsed
        if resource != "community":
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
            return
        slug = self._article_slug(raw_slug)
        if slug is None:
            return
        user = self._current_user()
        payload = self.community_store.article_community(slug, user["id"] if user else None)
        payload["user"] = user
        self.send_json(HTTPStatus.OK, payload)

    def _handle_article_post(self, route: str) -> None:
        parsed = self._article_route(route)
        if parsed is None:
            return
        raw_slug, resource = parsed
        slug = self._article_slug(raw_slug)
        if slug is None:
            return
        user = self._require_user()
        if user is None:
            return
        try:
            payload = self._read_json()
            if resource == "status":
                updated_at = self.community_store.set_status(user["id"], slug, str(payload.get("status", "")))
                self.send_json(HTTPStatus.OK, {"status": payload.get("status"), "updatedAt": updated_at})
            elif resource == "comments":
                self.send_json(HTTPStatus.CREATED, {"comment": self.community_store.add_comment(user["id"], slug, payload.get("content", ""))})
            elif resource == "notes":
                self.send_json(
                    HTTPStatus.CREATED,
                    {"note": self.community_store.add_note(
                        user["id"], slug, payload.get("quote", ""), payload.get("start"), payload.get("end"), payload.get("content", "")
                    )},
                )
            else:
                self.send_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
        except CommunityError as error:
            self._send_community_error(error)

    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self) -> None:
        route = unquote(urlparse(self.path).path)
        if route == "/research/workbench":
            self.send_response(HTTPStatus.PERMANENT_REDIRECT)
            self.send_header("Location", "/research/workbench/")
            self.send_header("Content-Length", "0")
            self.end_headers(); return
        if route.startswith("/research/workbench/"):
            self.send_workbench_file(route); return
        if route == "/api/health":
            self.send_json(200, {"status": "ok", "service": "keblog", "version": "3.0", "source": "git"}); return
        if route == "/api/auth/me":
            self.send_json(HTTPStatus.OK, {"user": self._current_user()}); return
        if route == "/api/articles/statuses":
            self._handle_statuses_get(urlparse(self.path).query); return
        if route.startswith("/api/articles/"):
            self._handle_article_get(route); return
        if route == "/api/research/document":
            self.send_markdown_json(self.research_document_path, RESEARCH_DOCUMENT[1]); return
        if route in {"/api/documents/paperpool.md", "/api/v1/paper-pool"}:
            self.send_markdown_json(self.content_dir / "documents" / "paperpool.md"); return
        if route.startswith("/api/documents/paperpool_"):
            name = route.removeprefix("/api/documents/")
            if not re.fullmatch(r"paperpool_(?:\d{6}|short)\.md", name):
                self.send_json(HTTPStatus.NOT_FOUND, {"error": "document not found"}); return
            self.send_markdown_json(self.content_dir / "documents" / name); return
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

    def do_POST(self) -> None:
        route = unquote(urlparse(self.path).path)
        if route in {"/api/auth/register", "/api/auth/login", "/api/auth/logout"}:
            self._handle_auth_post(route); return
        if route.startswith("/api/articles/"):
            self._handle_article_post(route); return
        self.reject_write()

    def reject_write(self) -> None:
        self.send_json(405, {"error": "keblog content is maintained through GitHub; commit content changes to the repository"}, {"Allow": "GET, HEAD, OPTIONS"})
    do_PUT = reject_write
    do_PATCH = reject_write
    do_DELETE = reject_write


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--dev", action="store_true"); args = parser.parse_args()
    project = Path(__file__).resolve().parents[1]
    static_root = Path(os.environ.get("SITE_STATIC_DIR", project / ("src-static" if args.dev else "dist"))).resolve()
    content_root = Path(os.environ.get("SITE_CONTENT_DIR", project / "content")).resolve()
    database_path = Path(os.environ.get("KEBLOG_DB_PATH", project / "runtime-data" / "community.sqlite3"))
    os.chdir(static_root)
    host, port = os.environ.get("SITE_HOST", "127.0.0.1"), int(os.environ.get("SITE_PORT", "8080"))
    print(f"Serving {static_root} with content from {content_root} on http://{host}:{port}", flush=True)
    server = ThreadingHTTPServer((host, port), SiteHandler)
    server.content_dir = content_root
    server.community_store = CommunityStore(database_path)
    server.cookie_secure = os.environ.get("KEBLOG_COOKIE_SECURE", "0") == "1"
    server.serve_forever()


if __name__ == "__main__": main()
