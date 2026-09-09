# Repository instructions

- Active frontend: `src-static/`; backend: `server/server.py` (Python standard library).
- Build: `node scripts/build.mjs` with Node.js 22.13+.
- Test: `python3 -m unittest discover -s tests -v` with Python 3.10+.
- Local dev: `python3 server/server.py --dev`; data lives in ignored `runtime-data/`.
- Keep source paths free of spaces. Keep personal notes, PDFs, chat exports, credentials and runtime data out of Git.
- Preserve existing API routes and VPS data paths unless migration is part of the task.
- Update API/deployment docs when changing configuration or behavior.
- Do not deploy to a live server unless the user requests deployment.
