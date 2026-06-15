# arjunabadger.press — the showcase site

A self-contained **static** site for **arjunabadger.press**: the library of finished books as
"completed projects" any visitor can browse, read online, and download (EPUB/PDF). Pure stdlib
generator — no build dependencies, no framework, no JS bundler.

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

## Deploy (Caddy on the webdock container)

1. Build, then copy `site/public/` to the server:

   ```bash
   python3 site/build.py
   rsync -az --delete site/public/ user@server:/var/www/arjunabadger.press/public/
   ```

2. `Caddyfile` (auto-HTTPS via Let's Encrypt):

   ```caddy
   arjunabadger.press, www.arjunabadger.press {
       root * /var/www/arjunabadger.press/public
       encode zstd gzip
       try_files {path} {path}/ {path}.html
       file_server
       header /assets/*    Cache-Control "public, max-age=31536000, immutable"
       header /downloads/* Cache-Control "public, max-age=86400"
   }
   ```

3. Point the DNS **A/AAAA** records for `arjunabadger.press` (and `www`) at the container's IP, then:

   ```bash
   caddy reload --config /etc/caddy/Caddyfile
   ```

Caddy provisions and renews the TLS certificate automatically on first request.

## Notes

- **Privacy:** the source repo is private. The *site* is public, but it serves only finished,
  rights-clean books — no canon, no prompts, no engine, no reference material.
- **Public contact:** `info@arjunabadger.press` — site mailto buttons, footer, and README. Wire the
  mailbox in Namecheap (Private Email or forwarding) before launch.
- **WHOIS:** set all four Domain Contact emails to `info@arjunabadger.press`; enable **Domain
  Privacy / Withheld for Privacy** on the domain so street address and personal phone are not public.
- Re-run `build.py` whenever a book's chapters, synopsis, cover, or export changes.
