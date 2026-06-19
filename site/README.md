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
- Uses real cover art where it exists (`design/cover.png|jpg`); otherwise renders an elegant
  **typographic cover** (gold-on-black, in the house style) so every book looks intentional.
- Copies EPUB/PDF into `public/downloads/<id>/` and links them.
- Generates a **Read-online** page from each book's merged `build/BOOK.md` where present.
- Emits `index.html`, `book/<id>.html`, `read/<id>.html`, and the brand assets.

`site/public/` is a **generated artifact** (git-ignored). Rebuild it; never hand-edit it.

## Preview locally

```bash
cd site/public && python3 -m http.server 8765
# open http://localhost:8765/
```

## Deploy (GitHub Pages first)

### Cheapest production shape

Keep the public static site on **GitHub Pages** for as long as possible. It is the cheapest host for
the catalogue, free downloads, generated book pages, and the installable PWA shell. Use Webdock only
for the parts GitHub Pages cannot do:

- `arjunabadger.press` — GitHub Pages static site and PWA shell.
- `api.arjunabadger.press` — Webdock containers for authoring chat, uploads, payments, royalties,
  audiobook delivery, and print-order workflows.
- `files.arjunabadger.press` or object storage later — large/private audio, print PDFs, and paid
  downloads if GitHub bandwidth or repo size becomes the constraint.

This keeps the expensive moving parts off the static host, but avoids paying a VPS to serve files
GitHub can serve for free.

### Webdock is not the static origin

Do not use the Webdock VPS/container as the public origin for this static catalogue while GitHub
Pages can carry the traffic and CDN edge. Webdock is reserved for backend surfaces GitHub Pages
cannot provide, such as API workers, uploads, account sync, payments, royalty ledgers, and print or
audio workflows.

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
