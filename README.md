# Arjuna Badger Press — the library

> The single, consolidated home for all the **prose**: every book, its canon, its prompts, its
> design notes, and its finished EPUB/PDF artifacts. One repo, on its own, decoupled from the engine.
>
> *The archer's eye. The badger's nerve.*

This repo is **content, not code**. The autonomous manuscript engine (StoryGraph · NovelBench ·
the editorial pipeline) stays private in [`africangold`](../africangold) and consumes this library
through its `AFRICANGOLD_WORKSPACES` seam — so the prose can live here, public-ready, while the
proprietary tooling stays where it belongs. Brand assets and the venture map live alongside the
books so the press has one front door.

## Layout

```
books/        all book content (canon · prompts · design · build/chapters · build/export)
  resonance/ revelation/ relic/        The African Gold Trilogy
  history-before-time/books/*          History Before Time (the Jakobus constellation)
  the-unheard/books/*                  The Unheard (living displaced peoples; shared Jakobus)
  the-why-files/books/*                The Why Files (anomalous sites; the "maybe" kept open)
  the-sheltering-desert/ the-north-forge/ the-loneliest/   Standalones
  registry.py                          the catalogue (titles · status · order — single source of truth)
brand/        Arjuna Badger Press brand kit (crest, variants, favicons, OG, tokens, guidelines)
docs/         the venture map + the Verification Gate spec
site/         ajgreyling.online — the showcase library (built from this content)
```

## The catalogue

- **The African Gold Trilogy** — *RESONANCE* → *REVELATION* → *RELIC* (the live, scored trilogy).
- **History Before Time** — the grounded ancient-engineering series; Jakobus Swart is the binding
  thread. Africa · India ×3 · Egypt · Australia (*Songlines*) · *Project Stargate*, plus the
  Jakobus-thread books (*The Silver Thread*, *The Recitation*) and *The Field of Doors*.
- **The Unheard** — the living-people mirror: displaced and land-rooted peoples, told in their own
  ground. (Japan/Ainu and Mongolia drafted; the rest scaffolded.)
- **The Why Files** — the anomalous-sites line that plays the official story straight, finds the one
  real hole, and leaves the *maybe* open.
- **Standalones** — *The Sheltering Desert*, *The North Forge*, *The Loneliest*.

## What is deliberately NOT here

- **No audio renders** (`*.mp3` etc.) — those belong with the audio pipeline.
- **No copyrighted third-party reference material** (`ingest/`) — never vendored into this repo.
- **No engine code** — the pipeline, gate, and scorers stay in `africangold`.

## Rights & licensing

All works © Andries J. Greyling. **All rights reserved unless a per-book LICENSE says otherwise.**
Published under **Arjuna Badger Press**; the author retains every right and routes the proceeds to
the artist. Reference material used during research is excluded from this repository by design.

## Non-negotiable: accuracy + both sides

Per the venture's binding rule, the pipeline fact-checks against live sources and presents **both
sides of a contested story** — Weir / Crichton / Brown-grade historical and factual accuracy is
*core*, not a nice-to-have. See [`docs/VERIFICATION_GATE.md`](docs/VERIFICATION_GATE.md).
