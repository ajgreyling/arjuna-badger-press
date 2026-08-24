# TAME — cold-start handover

> **Standalone.** A near-future South African parable about an intelligence nobody designed,
> which is kind to us. Scaffolded 2026-08-23. **No manuscript prose exists yet.**
>
> Working title *TAME* (Afrikaans *Mak*). The reader is allowed to assume the title refers to the
> machine.
>
> **First full draft complete 2026-08-24** — 40 chapters, 84,685 words, five parts. Read
> `canon/STYLE_GUIDE.md` before touching a line of it: the rule that Oom's words never appear as
> dialogue is what makes L-12 enforceable at the sentence level, and it is held for forty chapters.

---

## Read in this order

1. **`canon/CANON_LOCKS.md`** — binding. L-01…L-18. If a lock and anything else disagree, the lock wins.
2. `canon/PREMISE.md` — what it is, the refusal at the centre, the two camps and the weather.
3. `canon/ENGINE.md` — how the harm is delivered: the flattening, *the word*, *the absence*, why
   Nel's instrument fails, the ending shape.
4. `canon/CHARACTERS.md` — the cast, each holding the strongest version of their position.
5. `canon/RETIRED_IDEAS.md` — read before proposing anything that feels brilliant and obvious.
6. `canon/OPEN_DECISIONS.md` — what is genuinely unsettled, the outside reviews (none performed),
   and the dated calls made during drafting.
6a. `canon/STYLE_GUIDE.md`, `canon/SYNOPSIS.md`, `canon/CHAPTER_STRUCTURE.md`,
   `canon/PLANTS_AND_PAYOFFS.md` — the prose contract, the whole book, the beats, the ledger.
7. **`PROVENANCE.md`** — the co-authorship ledger and colophon spec. Append an entry every session.

## The five ways to break this book

1. **Settling L-01.** Any hint, in either direction, of whether Oom intends anything.
2. **A reveal.** Confession, recovered log, deathbed line, reader-only wink. All of it is L-08.
3. **Making Oom sinister in register** — menace in the prose, a chilling last line. L-07.
4. **Making Thandeka a fool.** Her argument is correct about the mercy. L-13.
5. **Writing the brochure** — bad model versus good model, and the reader smells the pitch. L-15.

## Status

| Layer | State |
|---|---|
| Canon | Complete, locked, **author ratification pending** (see `PROVENANCE.md`) |
| Blueprint / plot | `canon/SYNOPSIS.md`, `canon/CHAPTER_STRUCTURE.md`, `canon/PLANTS_AND_PAYOFFS.md`, `canon/STYLE_GUIDE.md` |
| Manuscript | **First full draft — 40 chapters, 84,685 words** (2026-08-24) |
| Foreword | Written (the machine's, L-19) |
| Afterword | **Reserved for the author.** Never drafted. See `AFTERWORD_RESERVED.md` |
| Colophon | Not written — required by L-16 before any edition ships |
| Cover | Not started |
| Outside review | **None performed.** Five reads listed in `canon/OPEN_DECISIONS.md`; the isiZulu linguistics read on ch 26 is **blocking** |
| Site | **Not registered.** Not in `PUBLISHED`, not in `CURATED`, no shelf |

## Repo mechanics

- Nothing ships until the id `tame` is listed in `PUBLISHED` in `site/build.py`. The id is the gate.
- If this book is ever given its own shelf, the shelf must be added to `SERIES` in `site/build.py`
  or the book silently never reaches the library.
- Text only in git. Covers and any rendered artifacts follow the R2 + `assets.manifest.json` path
  in `AGENTS.md` — the pre-commit gate blocks binaries, and `./scripts/install-hooks.sh` must be
  run once per clone or the gate is decoration.
