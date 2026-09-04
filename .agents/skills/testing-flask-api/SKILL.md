---
name: testing-flask-api
description: How to run and end-to-end test the devin-sandbox-api Flask todo API locally, including a before/after comparison against origin/main.
---

# Testing the Flask todo API locally

## Run the server
- Use the existing venv: `. .venv/bin/activate` (if missing: `python -m venv .venv && pip install -r requirements.txt`).
- `make run` / `python run.py` starts Flask in debug mode on port 5000. Debug mode means unhandled exceptions render as a Werkzeug HTML traceback (500) — useful for spotting leaked exceptions, but the tests should check `Content-Type: application/json`.
- The store is in-memory; restart the server to reset state (ids start at 1 each restart).

## Before/after comparison against main
- `git worktree add /tmp/main-wt origin/main`, then run the main version on another port without touching the working tree:
  `cd /tmp/main-wt && .venv-path/python -c "from app import create_app; create_app().run(debug=True, port=5001)"` (reuse the repo's `.venv/bin/python`).
- Clean up with `git worktree remove --force /tmp/main-wt && git worktree prune`. `pkill -f run.py` may kill the shell itself if the command line matches — prefer `ss -ltnp | grep :500` and `kill <pid>`.

## Checking responses
- Chrome renders JSON responses with a "Pretty-print" toggle; it does not show the HTTP status, so confirm status codes with `curl -s -i`.
- For POST endpoints in the browser, `fetch()` from the page's origin works (no auth) and the result can be written into `document.body` to show it on the recording.
- `<int:>` route converters yield Flask's default HTML 404 for non-integer ids — that is pre-existing behavior, not the JSON error handler.
- Chrome's omnibox autocompletes previously visited paths (typing `localhost:5000/items` can navigate to `/items/1`). Type the full `http://localhost:PORT/path`, press `Delete` to drop the inline completion, then `Return`.
- A good pattern for showing many API cases at once on a recording: loop the request matrix in one `fetch()` script and render `body -> status content-type body` lines into `document.body` as a `<pre>`. Confirm exact bytes/status separately with `curl -s -i` or a Python `urllib` snippet.
- Validation-style changes: assert the store side effects too (`GET /items` empty after rejects, and the next valid create keeping id 1) — that is what distinguishes "validated before mutating" from "validated after burning an id".

## Devin Secrets Needed
- none
