#!/usr/bin/env python3
"""Small SQLite-backed account and article-community store for keblog."""
from __future__ import annotations

import hashlib
import hmac
import re
import secrets
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path

USERNAME_RE = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_.-]{2,31}$")
STATUSES = {"unread", "read", "deeper"}
PBKDF2_ITERATIONS = 310_000
SESSION_TTL_SECONDS = 30 * 24 * 60 * 60


class CommunityError(Exception):
    def __init__(self, status: int, code: str, message: str):
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def public_user(row: sqlite3.Row | None) -> dict | None:
    if row is None:
        return None
    return {"id": row["id"], "username": row["username"], "displayName": row["display_name"]}


class CommunityStore:
    def __init__(self, path: str | Path):
        self.path = Path(path).expanduser().resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 10000")
        connection.execute("PRAGMA journal_mode = WAL")
        return connection

    def _initialize(self) -> None:
        with self._connect() as db:
            db.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE COLLATE NOCASE,
                    password_hash TEXT NOT NULL,
                    display_name TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS sessions (
                    token_hash TEXT PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    expires_at INTEGER NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS sessions_expiry_idx ON sessions(expires_at);
                CREATE TABLE IF NOT EXISTS reading_status (
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    slug TEXT NOT NULL,
                    status TEXT NOT NULL CHECK(status IN ('unread', 'read', 'deeper')),
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY(user_id, slug)
                );
                CREATE TABLE IF NOT EXISTS comments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    slug TEXT NOT NULL,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS comments_slug_idx ON comments(slug, created_at, id);
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    slug TEXT NOT NULL,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    quote TEXT NOT NULL,
                    start_offset INTEGER NOT NULL,
                    end_offset INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS notes_slug_idx ON notes(slug, created_at, id);
                """
            )
            db.execute("DELETE FROM sessions WHERE expires_at <= ?", (int(time.time()),))

    @staticmethod
    def _password_hash(password: str) -> str:
        salt = secrets.token_bytes(16)
        digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
        return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt.hex()}${digest.hex()}"

    @staticmethod
    def _password_matches(password: str, encoded: str) -> bool:
        try:
            algorithm, iterations, salt_hex, digest_hex = encoded.split("$", 3)
            if algorithm != "pbkdf2_sha256":
                return False
            digest = hashlib.pbkdf2_hmac(
                "sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), int(iterations)
            )
            return hmac.compare_digest(digest.hex(), digest_hex)
        except (ValueError, TypeError):
            return False

    @staticmethod
    def _validate_credentials(username: str, password: str, display_name: str | None = None) -> tuple[str, str, str]:
        username = str(username or "").strip()
        password = str(password or "")
        display_name = str(display_name or username).strip()
        if not USERNAME_RE.fullmatch(username):
            raise CommunityError(400, "invalid_username", "用户名需为 3—32 位字母、数字、下划线或短横线。")
        if len(password) < 8 or len(password) > 256:
            raise CommunityError(400, "invalid_password", "密码长度需为 8—256 位。")
        if not display_name or len(display_name) > 48:
            raise CommunityError(400, "invalid_display_name", "显示名称不能为空且不能超过 48 个字符。")
        return username, password, display_name

    @staticmethod
    def _token_hash(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def _new_session(self, db: sqlite3.Connection, user_id: int) -> tuple[str, int]:
        token = secrets.token_urlsafe(32)
        expires_at = int(time.time()) + SESSION_TTL_SECONDS
        db.execute(
            "INSERT INTO sessions(token_hash, user_id, expires_at, created_at) VALUES (?, ?, ?, ?)",
            (self._token_hash(token), user_id, expires_at, now_iso()),
        )
        return token, expires_at

    def register(self, username: str, password: str, display_name: str | None = None) -> tuple[dict, str, int]:
        username, password, display_name = self._validate_credentials(username, password, display_name)
        try:
            with self._connect() as db:
                cursor = db.execute(
                    "INSERT INTO users(username, password_hash, display_name, created_at) VALUES (?, ?, ?, ?)",
                    (username, self._password_hash(password), display_name, now_iso()),
                )
                user_id = cursor.lastrowid
                row = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
                token, expires_at = self._new_session(db, user_id)
        except sqlite3.IntegrityError as error:
            if "users.username" in str(error) or "UNIQUE" in str(error):
                raise CommunityError(409, "username_taken", "这个用户名已经注册。") from error
            raise
        return public_user(row), token, expires_at

    def login(self, username: str, password: str) -> tuple[dict, str, int]:
        username = str(username or "").strip()
        password = str(password or "")
        with self._connect() as db:
            row = db.execute("SELECT * FROM users WHERE username = ? COLLATE NOCASE", (username,)).fetchone()
            if row is None or not self._password_matches(password, row["password_hash"]):
                raise CommunityError(401, "invalid_credentials", "用户名或密码不正确。")
            token, expires_at = self._new_session(db, row["id"])
        return public_user(row), token, expires_at

    def user_for_session(self, token: str | None) -> dict | None:
        if not token:
            return None
        with self._connect() as db:
            row = db.execute(
                "SELECT users.* FROM sessions JOIN users ON users.id = sessions.user_id "
                "WHERE sessions.token_hash = ? AND sessions.expires_at > ?",
                (self._token_hash(token), int(time.time())),
            ).fetchone()
            if row is None:
                db.execute("DELETE FROM sessions WHERE token_hash = ?", (self._token_hash(token),))
            return public_user(row)

    def logout(self, token: str | None) -> None:
        if token:
            with self._connect() as db:
                db.execute("DELETE FROM sessions WHERE token_hash = ?", (self._token_hash(token),))

    def set_status(self, user_id: int, slug: str, status: str) -> str:
        if status not in STATUSES:
            raise CommunityError(400, "invalid_status", "阅读状态只能是待阅读、已阅读或待深入。")
        updated_at = now_iso()
        with self._connect() as db:
            db.execute(
                "INSERT INTO reading_status(user_id, slug, status, updated_at) VALUES (?, ?, ?, ?) "
                "ON CONFLICT(user_id, slug) DO UPDATE SET status=excluded.status, updated_at=excluded.updated_at",
                (user_id, slug, status, updated_at),
            )
        return updated_at

    def add_comment(self, user_id: int, slug: str, content: str) -> dict:
        content = str(content or "").strip()
        if not content or len(content) > 5000:
            raise CommunityError(400, "invalid_comment", "评论不能为空且不能超过 5000 个字符。")
        created_at = now_iso()
        with self._connect() as db:
            cursor = db.execute(
                "INSERT INTO comments(slug, user_id, content, created_at) VALUES (?, ?, ?, ?)",
                (slug, user_id, content, created_at),
            )
            comment_id = cursor.lastrowid
            row = db.execute(
                "SELECT comments.*, users.username, users.display_name FROM comments "
                "JOIN users ON users.id = comments.user_id WHERE comments.id = ?",
                (comment_id,),
            ).fetchone()
        return self._comment_payload(row)

    def add_note(self, user_id: int, slug: str, quote: str, start_offset: int, end_offset: int, content: str) -> dict:
        quote = str(quote or "").strip()
        content = str(content or "").strip()
        try:
            start_offset = int(start_offset)
            end_offset = int(end_offset)
        except (TypeError, ValueError) as error:
            raise CommunityError(400, "invalid_note_range", "笔记缺少有效的划线位置。") from error
        if not quote or len(quote) > 2000:
            raise CommunityError(400, "invalid_note_quote", "划线内容不能为空且不能超过 2000 个字符。")
        if start_offset < 0 or end_offset <= start_offset or end_offset - start_offset > 5000:
            raise CommunityError(400, "invalid_note_range", "划线范围无效。")
        if not content or len(content) > 5000:
            raise CommunityError(400, "invalid_note", "笔记不能为空且不能超过 5000 个字符。")
        created_at = now_iso()
        with self._connect() as db:
            cursor = db.execute(
                "INSERT INTO notes(slug, user_id, quote, start_offset, end_offset, content, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (slug, user_id, quote, start_offset, end_offset, content, created_at),
            )
            note_id = cursor.lastrowid
            row = db.execute(
                "SELECT notes.*, users.username, users.display_name FROM notes "
                "JOIN users ON users.id = notes.user_id WHERE notes.id = ?",
                (note_id,),
            ).fetchone()
        return self._note_payload(row)

    @staticmethod
    def _comment_payload(row: sqlite3.Row) -> dict:
        return {
            "id": row["id"],
            "user": {"username": row["username"], "displayName": row["display_name"]},
            "content": row["content"],
            "createdAt": row["created_at"],
        }

    @staticmethod
    def _note_payload(row: sqlite3.Row) -> dict:
        return {
            "id": row["id"],
            "user": {"username": row["username"], "displayName": row["display_name"]},
            "quote": row["quote"],
            "start": row["start_offset"],
            "end": row["end_offset"],
            "content": row["content"],
            "createdAt": row["created_at"],
        }

    def article_community(self, slug: str, user_id: int | None = None) -> dict:
        with self._connect() as db:
            comments = db.execute(
                "SELECT comments.*, users.username, users.display_name FROM comments "
                "JOIN users ON users.id = comments.user_id WHERE comments.slug = ? "
                "ORDER BY comments.created_at ASC, comments.id ASC LIMIT 200",
                (slug,),
            ).fetchall()
            notes = db.execute(
                "SELECT notes.*, users.username, users.display_name FROM notes "
                "JOIN users ON users.id = notes.user_id WHERE notes.slug = ? "
                "ORDER BY notes.created_at ASC, notes.id ASC LIMIT 300",
                (slug,),
            ).fetchall()
            status = None
            if user_id is not None:
                row = db.execute(
                    "SELECT status FROM reading_status WHERE user_id = ? AND slug = ?", (user_id, slug)
                ).fetchone()
                status = row["status"] if row else "unread"
        return {
            "slug": slug,
            "status": status,
            "comments": [self._comment_payload(row) for row in comments],
            "notes": [self._note_payload(row) for row in notes],
        }
