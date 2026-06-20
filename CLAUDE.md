# Arjuna Badger Press — Library & Site

This repo is the **public library and static site generator** for Arjuna Badger Press
(`arjunabadger.press`). It holds the published book catalog, EPUB/PDF exports, cover art,
and the Python static-site generator that builds the reader-facing site.

The companion repo `arjuna-badger-platform` holds the SaaS app (FastAPI/Uvicorn on Render),
the novel-generation engine, Neon Postgres, R2 workshop storage, and **`saas/web/public/`**
— the directory Render actually serves at the custom domain.

Monorepo layout: `~/code/arjuna-badger/arjuna-badger-press` + `arjuna-badger-platform`.

## Production infrastructure

| Layer | Role |
|---|---|
| **Namecheap** | DNS registrar for `arjunabadger.press` |
| **Cloudflare** | CDN + TLS in front of Render |
| **Render** | **Live site** — serves synced copy of `site/public/` from platform's `saas/web/public/` |
| **Neon** | Postgres for SaaS workshop (platform repo) |
| **R2** | Workshop generation blobs only — shelf EPUB/PDF are on Render disk |
| **GitHub Pages** | Parallel CI rebuild on `master` push — not the custom-domain origin |

## Repo layout

```
books/                 published book library (one dir per book-id)
  <book-id>/
    build/BOOK.md      merged manuscript (for read-online; synced from engine)
    build/export/      EPUB + PDF (committed — these are the downloads)
    design/            cover.json + cover.png
    canon/             story bible (where present)
site/
  build.py             static site generator (stdlib only — no dependencies)
  public/              GENERATED — never commit, CI rebuilds it
tools/                 generate_wiki.py, strip_forewords.py, etc.
.github/workflows/
  pages.yml            push to master → build.py → GitHub Pages artifact
```

Engine → library sync: `arjuna-badger-platform/tools/sync_library.sh` (run before deploy when
prose changed in the engine). Altas Resonance Engine books use `sync_are_book`.

## Deploying

Use `/deploy` in the **platform** repo (skill: `arjuna-badger-platform/.claude/skills/deploy/SKILL.md`).

```
0. (engine) ./tools/sync_library.sh
1. python3 site/build.py              → site/public/
2. rsync site/public/ → platform/saas/web/public/
3. Verify downloads in platform saas/web/public/downloads/
4. git push this repo (master)        → GitHub Pages CI
5. git push platform (main)           → render-deploy.yml
6. Render redeploy                    → hook secret OR Manual Deploy
```

**Both pushes are required.** Live `arjunabadger.press` only updates after **Render redeploys**
(`RENDER_DEPLOY_HOOK_URL` on platform repo, or Manual Deploy on Render dashboard).

## Publishing a new book

1. Sync from engine (or add book folder): `books/<book-id>/build/export/`, `build/BOOK.md`, `design/`
2. Add `PUBLISHED` + `CURATED` entries in `site/build.py`
3. Run full deploy loop (above)

The book id in `PUBLISHED` is the gate — nothing ships until listed there.
`WORKSHOP_HOLD` overrides PUBLISHED. `SERIAL` = read-online only, no downloads.

## site/build.py rules

- `PUBLISHED` — ids that may ship EPUB/PDF + read-online
- `WORKSHOP_HOLD` — overrides PUBLISHED; "In the workshop" badge
- `SERIAL` — read-online only, no downloads
- `HIDE_SERIES` / `HIDE_BOOKS` — drop from site entirely
- `CURATED` — master ordered list; shelf, subtitle, blurb fallback
- Cover gate: < 500 KB = procedural placeholder (hidden unless `PROCEDURAL_SHOW`)

## Translation editions

Translated EPUBs/PDFs: `build/export/<SLUG>.<lang>.epub`. See `TRANSLATIONS.md`.

## Commit discipline

- Commit EPUB/PDF exports and `build/BOOK.md` (read-online source)
- Never commit `site/public/` — CI rebuilds it
- Stage specifically; review before `git add -A`

## Branch

Default and deploy branch: **`master`**. Platform companion uses **`main`**.
