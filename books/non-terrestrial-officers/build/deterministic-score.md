# NovelBench — deterministic scorecard

**NULL HORIZON** · ~12,179 words · no LLM calls

## Prose Quality (deterministic dimension)

| Metric | Score (0–10) |
|---|---:|
| Sentence variety | **7.1** |
| Lexical diversity (MATTR) | **5.6** |
| Repetition (inverse) | **7.1** |
| Passive voice (inverse) | **8.0** |
| Exposition / filter words | **6.0** |
| Register evenness (burstiness) | **10.0** |
| Scene cadence (mic-drop inverse) | **8.7** |

**Book prose_quality (det mean): 7.5/10** (chapter-weighted: 6.0/10)

Quality bar reference: prose_quality ≥ **7.5** → **PASS**

## Machine tells (scaled targets from RELIC × word ratio)

**5** tell(s) over scaled target

| Tell | Count | Target | |
|---|---:|---:|---|
| spaced em-dash ` — ` (typographic machine fingerpr | 79 | 1 | OVER |
| tight em-dash `word—word` (density — the dash doin | 39 | 28 | OVER |
| "the way…" (the single most over-used construction | 19 | 18 | OVER |
| "Not X. Y." reframe-fragment (the trilogy's #1 ove | 9 | 3 | OVER |
| "something in his face / something moved" (placeho | 2 | 1 | OVER |
| hedge "seemed/appeared to · perhaps · somewhat · s | 5 | 6 | ok |
| "very/really [word]" intensifier-padding (a weak w | 4 | 5 | ok |
| caption density "which meant / that was / the diff | 3 | 4 | ok |
| sentence-initial reframe "It wasn't X / It was not | 1 | 1 | ok |
| stacked trailing "which" clauses (your most identi | 1 | 1 | ok |
| superlative-inflation "the only/most/truest X" (ev | 1 | 1 | ok |
| weasel "obviously/clearly/literally/basically/actu | 1 | 2 | ok |
| wordy connective "the fact that / in order to / in | 1 | 1 | ok |
| "almost [emotion]" (almost smiled/laughed/gentle) | 0 | 1 | ok |
| same-sentence reframe "X, it was/but Y" (the manuf | 0 | 1 | ok |
| prophecy / stone-tablet foreshadowing ("the land w | 0 | 1 | ok |
| "Not a question." + fragment family (authorial thr | 0 | 1 | ok |
| "which from [Name] meant/was …" (the in-group-tran | 0 | 1 | ok |
| "filed it / filed it under …" (Priya's cognition-v | 0 | 1 | ok |
| the "set it down / put it down" thesis-refrain (th | 0 | 2 | ok |
| "(exact/negative) shape of [a person/thing]" (one  | 0 | 1 | ok |
| "two [facts/impossibilities] of the same shape" (p | 0 | 1 | ok |
| "the string, not the gong" / violin-string metapho | 0 | 1 | ok |
| the AI's self-narrating meta-commentary ("I want y | 0 | 1 | ok |
| "the cold went up her neck/spine" (pre-fab thrille | 0 | 1 | ok |
| RELIC: Arin's "buried alive → under-dramatic" temp | 0 | 1 | ok |
| inline prebuttal reframe "that's not X, that's Y"  | 0 | 1 | ok |
| the withhold/cognition template "she didn't say X  | 0 | 2 | ok |
| RELIC: the watcher-at-every-node scene-opening bea | 0 | 1 | ok |
| classic cliché (proselint list) — REGRESSION GUARD | 0 | 1 | ok |

Reframe density: **0** / 49 pages ≥ 2 moves (max 1 on one page)

## Chapter prose (deterministic)

| Chapter | Words | prose_quality |
|---|---:|---:|
| ch-01 | 732 | 5.26 |
| ch-02 | 478 | 5.89 |
| ch-03 | 487 | 7.04 |
| ch-04 | 543 | 6.16 |
| ch-05 | 507 | 6.17 |
| ch-06 | 434 | 5.57 |
| ch-07 | 502 | 5.6 |
| ch-08 | 465 | 7.36 |
| ch-09 | 607 | 7.16 |
| ch-10 | 423 | 6.69 |
| ch-11 | 593 | 5.0 |
| ch-12 | 523 | 4.69 |
| ch-13 | 492 | 6.06 |
| ch-14 | 583 | 4.34 |
| ch-15 | 473 | 6.93 |
| ch-16 | 376 | 5.84 |
| ch-17 | 528 | 4.7 |
| ch-18 | 509 | 5.79 |
| ch-19 | 500 | 6.46 |
| ch-20 | 557 | 6.51 |
| ch-21 | 423 | 7.06 |
| ch-22 | 312 | 7.07 |

## Weakest / strongest (deterministic prose)

Weakest: ch-14 (4.34), ch-12 (4.69), ch-17 (4.7), ch-11 (5.0), ch-01 (5.26)

Strongest: ch-08 (7.36), ch-09 (7.16), ch-22 (7.07), ch-21 (7.06), ch-03 (7.04)

---

*LLM-judged dimensions (reader experience, emotional impact, character, story mechanics, canon integrity, place magnetism) require `./run.sh --book <id> bench score` after registry wiring. This report is the free deterministic layer only.*
