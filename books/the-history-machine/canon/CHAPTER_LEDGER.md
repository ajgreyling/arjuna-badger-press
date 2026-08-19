# Chapter Ledger — *The History Machine*

> Binding map. **K** Karoo · **T** Technopark · **A** Accra · **N** Nairobi · **I** Ice (Antarctica).
> Target ~95k · 24 chapters · four parts named for the Code's principles.

| # | Part | Tag | Working title | Beat |
|---|---|---|---|---|
| 00 | — | — | Note on the reading | The consortium's four principles; whose reading this is |
| 01 | I · SYMMETRY | **K** | The Quiet Is the Instrument | Karoo; engineered silence; first clean residue |
| 02 | I | **T** | Tolerances | Technopark workshop; sensors survive the world; the last ship loads |
| 03 | I | **I** | Bara | Yusuf goes south; the borehole; ice memory; the season closes |
| 04 | I | **A** | Unmixing the Choir | Accra; separation on a busy coordinate for the first time |
| 05 | I | **N** | Before It Is Needed | Nairobi; the custody standard written in advance |
| 06 | I | **K** | Four Small Answers | The first cases land; unambiguous good; the queue is born |
| 07 | II · BREAK | **N** | Admissible | First courtroom; physical record as evidence |
| 08 | II | **K** | The List | The asks arrive; the queue becomes the instrument of power |
| 09 | II | **A** | What They Actually Want | Services; rooms, then conversations; the shape of the next request |
| 10 | II | **N** | Protected Is a Word | First experiential request; the chair's veto used and held |
| 11 | II | **I** | Two Numbers | The first deliberate historical reconstruction; the second timestamp |
| 12 | II | **T** | The Ice Closes | Midpoint; unreachable instrument, impossible number, contamination assumed |
| 13 | III · RECORD | **A** | Through the Column | Accra proves the signal is everywhere in the ice; contamination dies |
| 14 | III | **I** | Eight Months | Suspicion lands on the man before the physics; the data budget |
| 15 | III | **N** | Chain Intact | Provenance verified end to end; fraud dies |
| 16 | III | **T** | From Raw | Re-inversion from unprocessed residue; pipeline error dies |
| 17 | III | **K** | What Record Was For | The Code, not the machine, is what has broken |
| 18 | III | **N** | The Inside of an Afternoon | Experiential reading demonstrated; the veto routed around (O-06) |
| 19 | III | **T** | The Second Machine | The north proposes an instrument with no seal on its Reader (O-08) |
| 20 | IV · CONSTRAINT | **A** | Read-Residue | The pre-echo identified as the trace a reading leaves |
| 21 | IV | **K** | Introduced | What it means that the archive now contains us |
| 22 | IV | **N** | The Binding | The document; argued line by line; everyone loses something |
| 23 | IV | **I** | The Ice Opens | The ship; the winter's arithmetic; someone gets off |
| 24 | IV | **K** | Still Listening | Close; no victory, no shutdown; the instrument hums |

## Act gates

- **Part I — SYMMETRY:** ch 01–06 (a project that has not yet broken anything)
- **Part II — BREAK:** ch 07–12 (midpoint at 12: the ice closes)
- **Part III — RECORD:** ch 13–19 (elimination in binding order)
- **Part IV — CONSTRAINT:** ch 20–24

## Draft status

| Status | Chapters |
|---|---|
| Scaffolded | 00–24 (canon only — no prose) |
| Words | 0 / 95,000 |
| Cover | none |
| EPUB/PDF | none |
| Site | **not listed** in `site/build.py` — nothing ships until the id is added to PUBLISHED |
| Canon locks | C-01…C-24 · open: O-01…O-08 (O-03/O-04 block drafting ch 11 and ch 06) |

## Parallel draft protocol

1. Read `prompts/draft-chapter.md` + your card in `build/chapter_briefs.md`
2. Draft only your assigned `build/chapters/ch-NN.md`
3. Do not contradict `canon/CANON_CHOICES.md` or `canon/MACHINE.md`
4. Reassemble with blank lines between chapters (required for pandoc chapter splits)
5. Render via `../../tools/render_book.sh` with cover
