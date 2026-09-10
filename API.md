# keblog Structured Paper API v2

Base URL: `https://keblog.lol`. Importable OpenAPI: `/api/openapi.json`.
SQLite (`SITE_DATA_DIR/paperpool.sqlite3`) is authoritative. Clients work with papers and readings, never edit the Paper Pool Markdown table. Existing website URLs remain readable through generated compatibility views.

## Daily workflow: two or three requests

1. `GET /api/v2/context`: task instructions and schedule metadata, counts, at most ten candidates and five recent readings. Full notes and the entire pool are not returned.
2. If discovering a new paper, `POST /api/v2/papers/lookup` checks up to 50 identities in one call. This step is optional because completion also checks duplicates.
3. `POST /api/v2/readings`: provide an existing `paperId` or inline `paper` metadata, a dated `slug`, and the complete Markdown `content`. The server creates the note and marks the paper read **in one SQLite transaction**.

This is an HTTP tool contract, not a ChatGPT scheduler integration. A ChatGPT scheduled task needs an available, authorized HTTP-capable connector; adding these URLs to a prompt alone does not grant write access. Schedule fields are metadata, not a server-side scheduler.

## Authentication and retries

All POST/PUT/PATCH/DELETE requests require `Authorization: Bearer <SITE_API_TOKEN>`. Daily briefs also require authentication for GET because a brief may include personal information. Other documented GET endpoints are public.

For retriable writes, send `Idempotency-Key: <unique-request-id>`. Repeat the **same path, method and JSON body** with the same key after a timeout. A successful replay returns `200` and `replayed: true`, without a second write. A different body with the same key returns `409`. Retain the key per logical operation; use a fresh key for a correction or a new reading. Keys are global across endpoints.

Updates to papers, readings, task configuration and briefs require the current `version` from GET. A stale version returns `409` with `currentVersion`. Refetch and merge before retrying. Revision history is retained in SQLite. Deletion is explicit, authenticated, and not part of normal daily publishing.

Request body limit: 2 MiB of encoded JSON including metadata and Markdown. Response errors use `{"error":"..."}`. Common status codes: `200` success, `201` created, `400` invalid data, `401` invalid/missing token, `404` missing resource, `409` duplicate/stale version, `410` retired legacy write endpoint.

## Papers

| Method | URL | Purpose |
|---|---|---|
| GET | `/api/v2/papers?status=candidate&limit=20&offset=0` | Paginated metadata, no Markdown bodies |
| GET | `/api/v2/papers?q=causal` | Search metadata |
| GET | `/api/v2/papers?doi=10.1145%2F3820059` | Exact normalized DOI lookup |
| POST | `/api/v2/papers/lookup` | Batch deduplication by title, DOI or arXiv |
| POST | `/api/v2/papers` | Add one candidate |
| GET | `/api/v2/papers/{id}` | Get one paper and version |
| PATCH | `/api/v2/papers/{id}` | Change selected metadata/status fields |
| DELETE | `/api/v2/papers/{id}` | Delete only if no reading references it |

List filters: `status`, `doi`, `arxiv`, `q`, `limit` (1–100), `offset` (non-negative). Response: `items`, `total`, `limit`, `offset`.

Paper input fields: `title` (required), `authors` (string array), `venue`, `url` (HTTP/HTTPS), `doi`, `arxiv`, `topics` (string array), `summary`, `reason`, `priority` (0–10), `date` (YYYY-MM-DD), `status` (`candidate`, `reading`, `read`, `skipped`; default `candidate`). Titles are normalized for case, punctuation and Unicode. DOI URLs are normalized; arXiv version suffixes are ignored. Matching an existing DOI, arXiv identifier or normalized title produces a duplicate match. Conflicting identities must be resolved explicitly.

Lookup body:

```json
{"papers":[{"doi":"10.1145/3820059"},{"title":"Example paper"}]}
```

Response has `results`, each containing the original `query` and matching paper objects. No matches means a new candidate; `status: read` means do not recommend it again unless explicitly asked to reread.

Patch example:

```json
{"version":1,"priority":8,"status":"reading"}
```

## Reading completion

```http
POST /api/v2/readings
Authorization: Bearer <secret>
Idempotency-Key: reading-260910-FirstAuthor-ShortName
Content-Type: application/json
```

```json
{
  "paper": {
    "title": "Actual paper title",
    "authors": ["First Author", "Second Author"],
    "venue": "Actual venue and year",
    "url": "https://example.org/paper",
    "topics": ["Code Review", "Causality"],
    "summary": "What this paper establishes",
    "reason": "Why it is relevant to the research question"
  },
  "slug": "260910-FirstAuthor-ShortName",
  "date": "2026-09-10",
  "content": "# Paper title\n\n## Motivation\n\nFull Markdown text…\n\n#### Experimental details\n\nEvidence and limitations…"
}
```

For an existing candidate, replace the entire `paper` object with `"paperId":"<id from GET>"`. Provide exactly one of these fields. For a matched inline paper the existing metadata is retained; use PATCH to correct it. The dated slug must match `date` and use `YYMMDD-FirstAuthor-ShortName` with ASCII letters/digits/hyphens.

The response includes `paper`, `reading` metadata and a website `url`. The list and Paper Pool view update automatically. Completed papers cannot be inadvertently returned to candidate status while notes exist. A reread needs `allowReread:true` and a different slug. It creates a second reading linked to the same paper.

| Method | URL | Purpose |
|---|---|---|
| GET | `/api/v2/readings?date=2026-09-10` | Paginated reading metadata |
| GET | `/api/v2/readings?paperId={id}` | Reading history for one paper |
| GET | `/api/v2/readings/{slug}` | Full Markdown, paperId and version |
| GET | `/api/v2/readings/{slug}/markdown` | Download a `.md` file |
| PUT | `/api/v2/readings/{slug}` | Replace one note with `version` and `content` |
| DELETE | `/api/v2/readings/{slug}` | Remove a note, retaining revision history |

After deleting a paper's last reading its status becomes `candidate`; explicitly PATCH it to `read` or `skipped` if that is desired. Original import files are historical copies and are not re-imported on restart.

## Task rules and daily brief

- `GET /api/v2/task-config`: `version`, `timezone`, `schedule` (HH:MM), `instructions`, `plan`.
- `PUT /api/v2/task-config`: current `version` plus only the fields to change.
- `PUT /api/v2/briefs/{YYYY-MM-DD}`: `{"version":0,"content":"# Daily briefing…"}` creates a brief; supply its current version to update it.
- `GET /api/v2/briefs/{YYYY-MM-DD}`: retrieve the brief (authenticated).
- `DELETE /api/v2/briefs/{YYYY-MM-DD}`: remove the brief (authenticated).

## Legacy compatibility and migration

On first startup, migrate the old `documents/paperpool.md`, all dated `daily-learning/*/README.md`, plan and prompt into SQLite in one transaction. Existing Markdown files are kept unchanged. A migration marker prevents repeated imports. Back up `paperpool.sqlite3` using SQLite's backup API or stop the service before copying it.

`/api/documents/paperpool.md`, `/api/v1/paper-pool`, `/api/daily-learning`, `/api/daily-learning/{slug}`, `/api/daily-learning/index`, `/api/daily-learning/plan` and `/api/v1/prompt` are generated read views. `/api/v1/bootstrap` now returns the compact v2 context. The legacy paper/reading write endpoints return `410`; use v2. Generic attachment/document endpoints remain available outside the structured resources.

Writing via v2 does not edit the historical Markdown files or update GitHub. Download current notes through `/markdown`; back up the SQLite database for the whole catalog, task configuration, notes and revisions.
