# arjunabadger.press — the showcase site

A self-contained **static** site for **arjunabadger.press**: the library of finished books as
"completed projects" any visitor can browse, read online, and download (EPUB/PDF). Pure stdlib
generator — no build dependencies, no framework, no JS bundler.

> **The book deliverables under `../books/` are GENERATED** — synced in from the private
> `africangold` platform repo by its `publish-library` workflow. Do not hand-edit them; edit a
> book's prose in africangold and let the pipeline rebuild. The `CURATED` list in
> [`build.py`](build.py) is the single catalogue contract the sync reads. Site chrome
> (this generator, templates, covers, `_comingsoon/` placeholders) IS owned here.

## Build

```bash
python3 site/build.py        # scans books/, emits site/public/
```

What it does:

- Curates the catalogue into series (`build.py` → `CURATED`), pulling **real synopses** from each
  book's `SYNOPSIS.md` (curated fallbacks where a book has none).
- Uses real cover art where it exists (`design/cover.png|jpg`, or `build/export/cover.png`).
  **No typographic SVG fallback** — books without a rich cover (≥ 500 KB) are withheld from the
  shelf until art ships; stale procedural stubs are deleted on build.
- Copies EPUB/PDF into `public/downloads/<id>/` and links them.
- Generates a **Read-online** page from each book's merged `build/BOOK.md` where present.
- Emits `index.html`, `book/<id>.html`, `read/<id>.html`, and the brand assets.

`site/public/` is a **generated artifact** (git-ignored). Rebuild it; never hand-edit it.

## Navigation (do not regress)

Site nav is **drawer-only at all breakpoints**: brand + hamburger; links grouped in the left `#navdrawer`.

**Information architecture**

| Zone | Where |
|---|---|
| **Front door** | `index.html` — hero, available library, compact mission, explore grid |
| **Everything else about the house** | `press.html` — platform, pipeline, studio |
| **Personal annex** | `safari/` — CV, letters, heraldry, writing desk, [How it started](https://arjunabadger.press/safari/how-it-started.html) (Misogi scorecard) |

- Source of truth: `nav_drawer_links()` + `safari_nav_drawer_links()` + CSS in [`build.py`](build.py)
- `assert_nav_drawer_contract()` runs on every build and **exits non-zero** if inline nav returns
- Do not add `@media (min-width:…)` rules that show `.navinline` or hide `.hamburger`
- Homepage shows **available** titles only; pipeline titles live on `press.html#pipeline`

## Preview locally

```bash
cd site/public && python3 -m http.server 8765
# open http://localhost:8765/
```

## Deploy (Render — live origin)

**`https://arjunabadger.press` is served by Render**, not GitHub Pages. GitHub Pages CI
(`.github/workflows/pages.yml`) rebuilds this site on every `master` push as a parallel artifact;
the custom domain hits Render via Namecheap DNS → Cloudflare → FastAPI/Uvicorn serving
`arjuna-badger-platform/saas/web/public/`.

Full runbook: `arjuna-badger-platform/.claude/skills/deploy/SKILL.md`

```
0. (platform) ./tools/sync_library.sh     engine → books/ here
1. python3 site/build.py                  → site/public/
2. rsync site/public/ → platform/saas/web/public/
3. git push master (this repo) + git push main (platform)
4. Render redeploy — RENDER_DEPLOY_HOOK_URL or Manual Deploy on Render dashboard
5. Verify: curl -sL https://arjunabadger.press/ | grep <book-id>
```

### Infrastructure

| Layer | Role |
|---|---|
| Namecheap | DNS registrar |
| Cloudflare | CDN + TLS in front of Render |
| Render | Live library + SaaS API |
| Neon | Postgres (platform workshop) |
| R2 | Workshop blobs only — shelf EPUB/PDF on Render disk |
| GitHub Pages | CI mirror on push to `master` |

## Notes

- **Privacy:** the source repo is private. The *site* is public, but it serves only finished,
  rights-clean books — no canon, no prompts, no engine, no reference material.
- **Analytics:** Plausible is wired into the generated pages. Event names, launch KPIs, and optional
  `plausible-cli` commands live in `docs/PLAUSIBLE_ANALYTICS.md`.
- **Public contact:** `info@arjunabadger.press` — site mailto buttons, footer, and README. Wire the
  mailbox in Namecheap (Private Email or forwarding) before launch.
- **WHOIS:** set all four Domain Contact emails to `info@arjunabadger.press`; enable **Domain
  Privacy / Withheld for Privacy** on the domain so street address and personal phone are not public.
- Re-run `build.py` whenever a book's chapters, synopsis, cover, or export changes.
