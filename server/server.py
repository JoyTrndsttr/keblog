#!/usr/bin/env python3
"""Small, dependency-free web server for the personal site and document API."""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import mimetypes
import os
import re
import shutil
import tempfile
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse, parse_qs
from pool import Pool, APIError
from pool_schema import schema

MAX_DOCUMENT_BYTES = 2 * 1024 * 1024
MAX_FILE_BYTES = 20 * 1024 * 1024
ALLOWED_DOCUMENT_SUFFIXES = {'.md', '.txt'}
ALLOWED_FILE_SUFFIXES = {'.md', '.txt', '.pdf', '.csv', '.json', '.bib', '.png', '.jpg', '.jpeg', '.webp'}
PUBLIC_DOCUMENTS = {'paperpool.md', 'daily-brief.md', 'daily-task-prompt.md'}
LEARNING_SLUG = re.compile(r'^\d{6}-[A-Za-z][A-Za-z0-9]*-[A-Za-z0-9][A-Za-z0-9-]{0,95}$')


def safe_name(raw: str, suffixes: set[str]) -> str:
    name = unquote(raw).strip().lower()
    if not name or name.startswith('.') or name != Path(name).name:
        raise ValueError('invalid filename')
    if not re.fullmatch(r'[a-z0-9][a-z0-9._-]{0,127}', name):
        raise ValueError('invalid filename')
    if Path(name).suffix not in suffixes:
        raise ValueError('unsupported file type')
    return name


def safe_learning_slug(raw: str) -> str:
    slug = unquote(raw).strip()
    if not LEARNING_SLUG.fullmatch(slug):
        raise ValueError('invalid daily learning slug')
    return slug


def learning_metadata(slug: str, markdown: str, modified: str) -> dict:
    title_match = re.search(r'^#\s+(.+)$', markdown, re.M)
    paper_match = re.search(r'^>\s*论文：\*?(.+?)\*?\s{0,2}$', markdown, re.M)
    doi_match = re.search(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', markdown)
    date = f'20{slug[:2]}-{slug[2:4]}-{slug[4:6]}'
    match = paper_match or title_match
    return {
        'slug': slug,
        'date': date,
        'author': slug.split('-', 2)[1],
        'shortName': slug.split('-', 2)[2],
        'title': match.group(1).strip('* ') if match else slug,
        'doi': doi_match.group(0).rstrip(').,') if doi_match else '',
        'modified': modified,
    }


def atomic_write(path: Path, payload: bytes, backup_dir: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    backup_dir.mkdir(parents=True, exist_ok=True)
    if path.exists():
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        digest = hashlib.sha256(path.read_bytes()).hexdigest()[:10]
        shutil.copy2(path, backup_dir / f'{path.name}.{stamp}.{digest}.bak')
    fd, temporary = tempfile.mkstemp(prefix=f'.{path.name}.', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def append_paper_entry(markdown: str, entry: dict) -> str:
    required = ['date', 'title', 'authors', 'venue', 'link', 'topics', 'value']
    missing = [field for field in required if not str(entry.get(field, '')).strip()]
    if missing:
        raise ValueError(f"missing fields: {', '.join(missing)}")
    title = str(entry['title']).strip()
    link = str(entry['link']).strip()
    if title.casefold() in markdown.casefold():
        raise FileExistsError('title already exists')
    doi_match = re.search(r'10\.\d{4,9}/[-._;()/:a-z0-9]+', link, re.I)
    if doi_match and doi_match.group(0).casefold() in markdown.casefold():
        raise FileExistsError('DOI already exists')

    def cell(field: str, default: str = '') -> str:
        return str(entry.get(field, default)).replace('|', '\\|').replace('\r', ' ').replace('\n', ' ').strip()

    section = '## Codex 维护记录'
    header = (
        f'\n\n{section}\n\n'
        '| 精读日期 | 论文 | 作者 | Venue / 年份 | DOI / 原文 | 主题 | 一句话价值 | 状态 |\n'
        '|---|---|---|---|---|---|---|---|\n'
    )
    row = f"| {cell('date')} | {cell('title')} | {cell('authors')} | {cell('venue')} | {cell('link')} | {cell('topics')} | {cell('value')} | {cell('status', '已精读')} |"
    if section not in markdown:
        return markdown.rstrip() + header + row + '\n'
    return markdown.rstrip() + '\n' + row + '\n'


class SiteHandler(SimpleHTTPRequestHandler):
    server_version = 'Keblog/2.0'

    @property
    def data_dir(self) -> Path:
        return Path(os.environ.get('SITE_DATA_DIR', '/var/lib/wangke-site')).resolve()

    @property
    def learning_dir(self) -> Path:
        return Path(os.environ.get('SITE_LEARNING_DIR', self.data_dir / 'daily-learning')).resolve()

    @property
    def token(self) -> str:
        return os.environ.get('SITE_API_TOKEN', '')

    @property
    def task_prompt_path(self) -> Path:
        return Path(os.environ.get('SITE_TASK_PROMPT_FILE', self.data_dir / 'documents' / 'daily-task-prompt.md')).resolve()

    def end_headers(self) -> None:
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('Referrer-Policy', 'strict-origin-when-cross-origin')
        self.send_header('Permissions-Policy', 'camera=(), microphone=(), geolocation=()')
        self.send_header('Content-Security-Policy', "default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Authorization, Content-Type, If-Match, Idempotency-Key')
        self.send_header('Access-Control-Allow-Methods', 'GET, PUT, POST, PATCH, DELETE, OPTIONS')
        super().end_headers()

    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header('Content-Length', '0')
        self.end_headers()

    def log_message(self, fmt: str, *args) -> None:
        print(f'{self.address_string()} - {fmt % args}', flush=True)

    def send_json(self, status: int, payload: dict, headers: dict | None = None) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        for key, value in (headers or {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body)

    def authorized(self) -> bool:
        supplied = self.headers.get('Authorization', '')
        expected = f'Bearer {self.token}'
        return bool(self.token) and hmac.compare_digest(supplied, expected)

    def require_auth(self) -> bool:
        if self.authorized():
            return True
        self.send_json(HTTPStatus.UNAUTHORIZED, {'error': 'valid bearer token required'}, {'WWW-Authenticate': 'Bearer'})
        return False

    def read_body(self, limit: int) -> bytes:
        try:
            length = int(self.headers.get('Content-Length', '0'))
        except ValueError as exc:
            raise ValueError('invalid content length') from exc
        if length < 1 or length > limit:
            raise ValueError(f'body must be between 1 and {limit} bytes')
        return self.rfile.read(length)

    def document_path(self, raw_name: str) -> Path:
        return self.data_dir / 'documents' / safe_name(raw_name, ALLOWED_DOCUMENT_SUFFIXES)

    def file_path(self, raw_name: str) -> Path:
        return self.data_dir / 'files' / safe_name(raw_name, ALLOWED_FILE_SUFFIXES)

    def learning_path(self, raw_slug: str) -> Path:
        if raw_slug == 'index':
            return self.learning_dir / 'README.md'
        if raw_slug == 'plan':
            return self.learning_dir / 'PLAN.md'
        return self.learning_dir / safe_learning_slug(raw_slug) / 'README.md'

    def learning_entries(self) -> list[dict]:
        entries = []
        if self.learning_dir.exists():
            for directory in self.learning_dir.iterdir():
                if not directory.is_dir() or not LEARNING_SLUG.fullmatch(directory.name):
                    continue
                path = directory / 'README.md'
                if not path.exists():
                    continue
                modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()
                entries.append(learning_metadata(directory.name, path.read_text('utf-8'), modified))
        entries.sort(key=lambda entry: (entry['date'], entry['slug']), reverse=True)
        return entries

    @staticmethod
    def read_text(path: Path, fallback: str = '') -> str:
        return path.read_text('utf-8') if path.exists() else fallback

    def handle_structured(self):
        route = unquote(urlparse(self.path).path)
        method = self.command
        pool = self.server.pool
        if route == '/api/openapi.json' and method == 'GET':
            self.send_json(200, schema(os.environ.get('SITE_PUBLIC_URL', 'http://127.0.0.1:8080')))
            return True
        if route.startswith('/api/v2/'):
            if (method != 'GET' or route.startswith('/api/v2/briefs/')) and not self.require_auth():
                return True
            try:
                body = json.loads(self.read_body(MAX_DOCUMENT_BYTES)) if method not in ['GET','DELETE'] else {}
                query = {k:v[-1] for k,v in parse_qs(urlparse(self.path).query).items()}
                status, result = pool.dispatch(method,route,query,body,self.headers.get('Idempotency-Key') if method!='GET' else None)
                if method == 'GET' and route.endswith('/markdown'):
                    raw = result['content'].encode('utf-8')
                    self.send_response(200)
                    self.send_header('Content-Type','text/markdown; charset=utf-8')
                    self.send_header('Content-Disposition',f'attachment; filename="{result["slug"]}.md"')
                    self.send_header('Content-Length',str(len(raw)))
                    self.end_headers()
                    self.wfile.write(raw)
                else:
                    self.send_json(status,result)
            except APIError as exc:
                self.send_json(exc.status,exc.payload)
            except (ValueError,UnicodeDecodeError) as exc:
                self.send_json(400,{'error':str(exc)})
            return True
        pool_routes = ['/api/documents/paperpool.md','/api/v1/paper-pool','/api/v1/bootstrap','/api/v1/completions','/api/paperpool/entries','/api/v1/paper-pool/entries','/api/v1/prompt','/api/documents/daily-task-prompt.md']
        if route not in pool_routes and not route.startswith('/api/daily-learning'):
            return False
        if method != 'GET':
            if self.require_auth():
                self.send_json(410,{'error':'Use structured v2 API; legacy Markdown writes are disabled','schema':'/api/openapi.json'})
            return True
        with pool.connect() as db:
            config = json.loads(db.execute("SELECT body FROM settings WHERE key='task-config'").fetchone()[0])
            if route == '/api/v1/bootstrap':
                self.send_json(200,pool.context(db))
                return True
            if route == '/api/daily-learning':
                self.send_json(200,{'entries':[pool.metadata(db,r) for r in pool.reading_list(db)]})
                return True
            if route in ['/api/documents/paperpool.md','/api/v1/paper-pool']:
                content=pool.markdown(db)
            elif route in ['/api/v1/prompt','/api/documents/daily-task-prompt.md']:
                content=config['instructions']
            elif route.endswith('/plan'):
                content=config['plan']
            elif route.endswith('/index'):
                content=pool.index(db)
            else:
                row=db.execute('SELECT body FROM readings WHERE slug=?',(route.rsplit('/',1)[-1],)).fetchone()
                if not row:
                    self.send_json(404,{'error':'reading not found'})
                    return True
                r=json.loads(row[0]);content=r['content']
            etag=hashlib.sha256(content.encode()).hexdigest()
            self.send_json(200,{'content':content,'etag':etag,'modified':datetime.now(timezone.utc).isoformat()}, {'ETag':f'"{etag}"'})
        return True

    def do_PATCH(self):
        if not self.handle_structured():
            self.send_json(404,{'error':'endpoint not found'})

    def do_DELETE(self):
        if not self.handle_structured():
            self.send_json(404,{'error':'endpoint not found'})

    def do_GET(self) -> None:
        if self.handle_structured():
            return
        route = urlparse(self.path).path
        if route == '/api/health':
            self.send_json(HTTPStatus.OK, {'status': 'ok', 'service': 'wangke-cloud-paper-pool', 'version': '2.0'})
            return
        if route == '/api/documents':
            documents = []
            for name in sorted(PUBLIC_DOCUMENTS):
                path = self.data_dir / 'documents' / name
                if path.exists():
                    documents.append({'name': name, 'size': path.stat().st_size, 'modified': datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()})
            self.send_json(HTTPStatus.OK, {'documents': documents})
            return
        if route.startswith('/api/documents/'):
            try:
                path = self.document_path(route[len('/api/documents/'):])
            except ValueError as exc:
                self.send_json(HTTPStatus.BAD_REQUEST, {'error': str(exc)})
                return
            if path.name not in PUBLIC_DOCUMENTS and not self.authorized():
                self.send_json(HTTPStatus.NOT_FOUND, {'error': 'document not found'})
                return
            if not path.exists():
                self.send_json(HTTPStatus.NOT_FOUND, {'error': 'document not found'})
                return
            raw = path.read_bytes()
            etag = hashlib.sha256(raw).hexdigest()
            self.send_json(HTTPStatus.OK, {'name': path.name, 'content': raw.decode('utf-8'), 'modified': datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(), 'etag': etag}, {'ETag': f'"{etag}"'})
            return
        if route.startswith('/api/files/'):
            if not self.require_auth():
                return
            try:
                path = self.file_path(route[len('/api/files/'):])
            except ValueError as exc:
                self.send_json(HTTPStatus.BAD_REQUEST, {'error': str(exc)})
                return
            if not path.exists():
                self.send_json(HTTPStatus.NOT_FOUND, {'error': 'file not found'})
                return
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-Type', mimetypes.guess_type(path.name)[0] or 'application/octet-stream')
            self.send_header('Content-Length', str(path.stat().st_size))
            self.send_header('Content-Disposition', f'attachment; filename="{path.name}"')
            self.end_headers()
            with path.open('rb') as stream:
                shutil.copyfileobj(stream, self.wfile)
            return
        super().do_GET()

    def do_PUT(self) -> None:
        if self.handle_structured():
            return
        if not self.require_auth():
            return
        route = urlparse(self.path).path
        try:
            if route.startswith('/api/daily-learning/'):
                path = self.learning_path(route[len('/api/daily-learning/'):])
                body = self.read_body(MAX_DOCUMENT_BYTES)
                if self.headers.get('Content-Type', '').startswith('application/json'):
                    content = json.loads(body).get('content')
                    if not isinstance(content, str):
                        raise ValueError('JSON content must be a string')
                    body = content.encode('utf-8')
                body.decode('utf-8')
            elif route.startswith('/api/documents/'):
                path = self.document_path(route[len('/api/documents/'):])
                body = self.read_body(MAX_DOCUMENT_BYTES)
                if self.headers.get('Content-Type', '').startswith('application/json'):
                    content = json.loads(body).get('content')
                    if not isinstance(content, str):
                        raise ValueError('JSON content must be a string')
                    body = content.encode('utf-8')
                body.decode('utf-8')
            elif route.startswith('/api/files/'):
                path = self.file_path(route[len('/api/files/'):])
                body = self.read_body(MAX_FILE_BYTES)
            else:
                self.send_json(HTTPStatus.NOT_FOUND, {'error': 'endpoint not found'})
                return
            current = path.read_bytes() if path.exists() else b''
            if_match = self.headers.get('If-Match')
            if if_match and if_match.strip('"') != hashlib.sha256(current).hexdigest():
                self.send_json(HTTPStatus.PRECONDITION_FAILED, {'error': 'document changed; read it again before writing'})
                return
            backup_dir = self.data_dir / 'backups'
            if route.startswith('/api/daily-learning/'):
                backup_dir = backup_dir / ('system' if path.parent == self.learning_dir else path.parent.name)
            atomic_write(path, body, backup_dir)
            self.send_json(HTTPStatus.OK, {'ok': True, 'name': path.name, 'etag': hashlib.sha256(body).hexdigest()})
        except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            self.send_json(HTTPStatus.BAD_REQUEST, {'error': str(exc)})

    def do_POST(self) -> None:
        if not self.handle_structured():
            self.send_json(404, {'error': 'endpoint not found'})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--dev', action='store_true')
    args = parser.parse_args()
    root = Path(os.environ.get('SITE_STATIC_DIR', Path(__file__).resolve().parents[1] / ('src-static' if args.dev else 'dist'))).resolve()
    # Resolve data paths before changing into the static document root.
    project = Path(__file__).resolve().parents[1]
    default_data = project / 'content' if args.dev else Path('/var/lib/wangke-site')
    os.environ['SITE_DATA_DIR'] = str(Path(os.environ.get('SITE_DATA_DIR', default_data)).resolve())
    for name in ('SITE_LEARNING_DIR', 'SITE_TASK_PROMPT_FILE'):
        if os.environ.get(name):
            os.environ[name] = str(Path(os.environ[name]).resolve())
    os.chdir(root)
    host = os.environ.get('SITE_HOST', '127.0.0.1')
    port = int(os.environ.get('SITE_PORT', '8080'))
    print(f'Serving {root} on http://{host}:{port}', flush=True)
    server = ThreadingHTTPServer((host, port), SiteHandler)
    server.pool = Pool(os.environ['SITE_DATA_DIR'], os.environ.get('SITE_LEARNING_DIR'))
    server.serve_forever()


if __name__ == '__main__':
    main()
