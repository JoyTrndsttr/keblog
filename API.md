# Cloud Paper Pool API

Base URL: your deployment URL (for example `https://example.com`), configured through `SITE_PUBLIC_URL`. Local development uses `http://127.0.0.1:8080`. The server is the only source of truth for the daily task; clients must not depend on Zotero, local files, automation memory, or a device-local Paper Pool. Every write request requires `Authorization: Bearer <token>` configured as a private Action secret.

## Bootstrap a ChatGPT daily task

`GET /api/v1/bootstrap` returns the canonical task prompt, daily plan, complete cloud Paper Pool, completed-note metadata, and the write contract in one request.

`GET /api/openapi.json` returns the OpenAPI description for a ChatGPT Action or another API client.

`GET /api/v1/prompt` and `GET /api/v1/paper-pool` return the two documents separately.

## Read daily learning

`GET /api/daily-learning` lists every completed reading note, newest first.

`GET /api/daily-learning/<YYMMDD-FirstAuthor-ShortName>` returns the Markdown note, modified time, and ETag. `GET /api/daily-learning/index` returns the reading schedule and completion index; `GET /api/daily-learning/plan` returns the canonical daily execution plan.

## Maintain daily learning

`PUT /api/daily-learning/<YYMMDD-FirstAuthor-ShortName>` creates or replaces a UTF-8 Markdown note. `PUT /api/daily-learning/index` maintains the schedule and `PUT /api/daily-learning/plan` maintains the execution plan. These endpoints require a Bearer Token, accept either a UTF-8 body or `{ "content": "..." }`, honor `If-Match`, and create a backup before replacing an existing file.

`POST /api/v1/completions` is the preferred completion endpoint. It validates the note slug and Paper Pool fields, rejects duplicate slugs, titles, and DOI values, writes the Markdown note, and updates the cloud Paper Pool in one request. Required JSON fields are `slug`, `content`, `date`, `title`, `authors`, `venue`, `link`, `topics`, and `value`; `status` is optional.

## Read the paper pool

`GET /api/documents/paperpool.md`

The response includes `content`, `modified`, and `etag`. Use the returned ETag in `If-Match` when replacing a document.

## Add a read paper

`POST /api/paperpool/entries` with JSON fields: `date`, `title`, `authors`, `venue`, `link`, `topics`, `value`, and optional `status`.

The endpoint rejects duplicate titles and DOI values and creates a backup before changing the Markdown file.

## Replace a text document

`PUT /api/documents/<name>.md` with either a UTF-8 body or `{ "content": "..." }`. Send `If-Match: <etag>` to prevent overwriting a concurrent edit.

## Store or retrieve a file

`PUT /api/files/<name>` accepts up to 20 MiB. `GET /api/files/<name>` is authenticated. Allowed types are Markdown, text, PDF, CSV, JSON, BibTeX, PNG, JPEG, and WebP.
