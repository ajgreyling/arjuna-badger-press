# Homo Credens — state of the working copy

> Written 2026-08-13. Measured, not remembered — every number below came from the files.

## Current state: single source of truth

**`chapters/` is canonical. `BOOK.md` is generated from it and must never be authored in.**

| | `chapters/` (22 files) | `BOOK.md` |
|---|---|---|
| Prose | canonical | generated — 0 of 1,094 paragraphs stale |
| `[PLATE: …]` art briefs | **all 107** | generated |

Regenerate with `./assemble-book.sh`. Verify with `./assemble-book.sh --check`, which exits
non-zero if `BOOK.md` has fallen behind. The script is idempotent — re-running is byte-identical.

## What was wrong, and why the check exists

Until 2026-08-13 the two files had drifted **in opposite directions**, and neither was a superset
of the other:

- `chapters/` held the post-factcheck corrections and **zero** plate briefs.
- `BOOK.md` held **all 107** plate briefs and prose that was stale in 23 paragraphs across 11
  chapters — still "402 CE" for Kumārajīva, "twenty-seven months" for Xavier, "the first
  unambiguously monotheist text in human history" for Second Isaiah, no Spencer and Gillen.

So the obvious repair — regenerating `BOOK.md` from `chapters/` — would have destroyed the book's
entire illustration programme, and the equally obvious one — treating `BOOK.md` as the manuscript —
would have shipped uncorrected prose. This was confirmed to be upstream's state too
(`lucid-religion`, branch `claude/study-bible-multiagent-adventure-1phsom`, path `book/`), so it
was never a local hydration artifact.

**Fixed** by porting all 107 briefs into `chapters/` at anchor-matched positions, verified as a
plate-only diff (0 lines removed, 0 non-plate additions, prose byte-identical), then generating
`BOOK.md`. Distribution is unchanged: 4–6 plates per chapter, 107 total.

## How art actually reaches the book

Two different things, easily confused:

1. **`[PLATE: …]` briefs** — prose descriptions of what an image should depict. Now in
   `chapters/`. These are the *specification*, used to commission or generate the plates. They are
   not rendered into the EPUB.
2. **Rendered images** — `art/ch-NN-vignette.png` (one per chapter, inlined under the heading by
   `build-epub.sh`), `art/endpaper-armillary.png`, `art/symbology.png`,
   `art/timeline-rivers-of-faith.png`, and the PD photo gallery under `art/pd/part-*/`.

**The rendered images are not here.** `art/` is 24K in this copy — the `CREDITS.md` files only.
The PNGs are LFS blobs skipped when this tree was hydrated with `GIT_LFS_SKIP_SMUDGE=1`.

> ⚠️ **`build-epub.sh` degrades silently.** A missing vignette is skipped, not raised. Building in
> this tree produces a **text-only EPUB with no art** and exits 0. It will look like it worked.
> Hydrate `art/` before trusting any build from here.

## Already-built artifacts upstream

`book/` upstream holds `Homo Credens.epub` (22.9 MB) and `Homo Credens (print).pdf` (102 MB). The
build scripts read `chapters/`, so those files are only as current as the moment they were built —
and if they predate the correction pass they carry the uncorrected prose. **Their build date has
not been established. Do not treat them as print-ready until it has.**

## Build inputs, for reference

`build-epub.sh` and `build-print.sh` both read `chapters/` directly. Neither reads `BOOK.md`, so
`BOOK.md` is for reading, quoting, and word counts — not for the print path.
