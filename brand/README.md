# `brand/` — Arjuna Badger Press brand kit

The consumer brand for the publishing & editorial studio built on this repo's tooling.

| File | What it is |
|---|---|
| **[BRAND.md](BRAND.md)** | The guidelines. Logo rules, colour, type, voice, do/don'ts. **Start here.** |
| [STRATEGY.md](STRATEGY.md) | Go-to-market: the offer (3 tiers), positioning, GTM, decisions. |
| [MARKET_ANALYSIS.md](MARKET_ANALYSIS.md) | The evidence: competitors, ACX model, the African-voices wedge. |
| [PRODUCTION_STRATEGY.md](PRODUCTION_STRATEGY.md) | The recording-quality line: business case + the booth/rental/app model. |
| `tokens.json` | Design tokens (colour + type) as JSON — for build tools / JS. |
| `tokens.css` | The same tokens as CSS custom properties — `@import` once, use the vars. |
| `assets/` | Logo variants, favicons, social card, brand sheet (see below). |

> The artist-facing recording **knowledge base** (the production ladder + DIY build
> plans) lives at [`docs/RECORDING_STUDIO_GUIDE.md`](../docs/RECORDING_STUDIO_GUIDE.md).

### `assets/`
| File | Use |
|---|---|
| `logo-master.png` | Source art (archive). |
| `logo-transparent.png` | Default logo, transparent bg. |
| `mark-only.png` | Brand mark alone — icons, avatars, watermark. |
| `logo-on-dark.png` / `logo-on-light.png` | Pre-padded on brand-ink / white. |
| `favicon.ico`, `favicon-{16,32,180,512}.png` | Browser / Apple-touch / PWA. |
| `social-og-1200x630.png` | Open Graph share card. |
| `brand-sheet.png` | One-page visual reference (palette + type + mark). |

### Quick start (web)
```html
<link rel="stylesheet" href="/brand/tokens.css">
<link rel="icon" href="/brand/assets/favicon.ico">
<meta property="og:image" content="/brand/assets/social-og-1200x630.png">
```
```css
.cta { background: var(--abp-ochre); color: var(--abp-black); }
```

### Regenerating assets
The PNG assets are derived from `assets/logo-master.png` with Pillow. The generation
snippets live in this commit's history; re-run them if the master art changes. Colour
tokens were **sampled** from the master — re-sample (don't guess) if the art is replaced.

> **Scope note:** this is the *brand* only. The website, the productized multi-tenant
> tooling, and the go-to-market plan are separate, not-yet-built deliverables.
