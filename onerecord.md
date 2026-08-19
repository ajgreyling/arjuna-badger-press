# ONE RECORD — handover

> African science-thriller duology. **Book I *The Record*** (2031) · **Book II *The Forward Cone***
> (2033–34). Canon locked 2026-08-19 and **merged to `master`**. **Zero prose written.**
>
> This file is the cold-start briefing: what exists, what is decided, what is not, what to do next,
> and what will silently break the book if you get it wrong. Everything below points at
> `books/the-record/`.

---

## 1 · What it is, in one breath

An African research consortium proves that actualised events leave dispersed, recoverable physical
consequences, and builds a machine that reconstructs the past by solving backward under constraint.
It is not a recording, not a simulation and not time travel: it eliminates every past configuration
incompatible with surviving residue until one remains. Book I proves the past is readable and costs
the world the mercy of forgetting. Book II points the same machine forward and discovers that
prediction has made everybody behave alike, which is the actual catastrophe.

> The universe is the archive. The 420 Code is the codec. The machine is the reader.

**Series thesis, one line:** *you cannot forget for free.*

## 2 · Where things stand

| Layer | State |
|---|---|
| Series canon | **Locked** — `canon/CANON_LOCKS.md`, L-01…L-27 |
| Book I blueprint | Complete — 24 sequences, `books/book1-the-record/canon/PLOT.md` |
| Book II blueprint | Complete — 27 sequences, `books/book2-the-forward-cone/canon/PLOT.md` |
| **Beat ledger (live)** | **63 beats** — `books/book1-the-record/BEAT_LEDGER.md`, full Book I spine |
| Consent instrument | Drafted with its five designed flaws — `books/book1-the-record/canon/CONSENT_INSTRUMENT.md` |
| Chapter ledger | Not built. Blocked on human review, not on decisions |
| Prose | **None** |
| Site | Not listed in `site/build.py`. Nothing ships until an id is added to `PUBLISHED` |

## 3 · Authority order

Read in this order; when two disagree, the higher one wins.

1. **`canon/CANON_LOCKS.md`** — binding. L-01…L-27.
2. **`canon/SERIES_BIBLE.md`** — the source document (`The_Record_Series_Bible.docx` v0.1),
   transcribed. Boundary map, dramatic engine, ethics, anti-tropes.
3. **`canon/`** — `WORLD_SYSTEM` (nodes + the seven machine rules) · `CHARACTERS` · `CHRONOLOGY` ·
   `OBJECTS` · `PHYSICS_ANCHORS` · `CRAFT` · `PLANT_PAYOFF` · `TERMINOLOGY` · `SOURCES`.
4. **Per-book `canon/`** — blueprint, reveal ladder, style guide, and (Book I)
   **`CONSENT_INSTRUMENT.md`**, whose wording is *not* locked but whose flaws are deliberate.
5. **`BEAT_LEDGER.md`** — living. Names and ordering may still move here; it is where riffs go.

Also: **`canon/RETIRED_IDEAS.md`** — cut ideas *with their reasons*, so they are not rediscovered and
re-argued. Read it before proposing anything that feels brilliant and obvious.

## 4 · The locks that actually constrain drafting

Twenty-seven exist; these are the ones you will hit on page one.

- **Five nodes, five POVs.** Karoo (ear) · Technopark (brain) · Accra–Kumasi (memory) · Nairobi
  (conscience) · Antarctic station (clock). Dries Venter is primary POV; rotating close third
  otherwise. Each principal owns one indispensable layer and **is wrong outside it**.
- **Never cinema.** Reconstructions are sparse, gap-marked, slow and usually ugly. **The smooth
  version is always the fake.**
- **Cost is always visible.** Compute, grid, queue position, custody, a night nobody slept. A free
  query is a continuity error.
- **The machine proves a fall and cannot prove a hand.** Intention is not in the residue.
  Concealment is — and concealment is where the moral weight sits.
- **The family's three questions** are the ethical spine: present? left alive? anyone accountable?
  Consent does not extend to his fear, pain or final thoughts, and Lucid enforces that as a query
  boundary.
- **Lucid computes, cites, conflicts or refuses.** Never a POV, never a voice, never cute. It refuses
  **G** on the page in Book I.
- **G is living and difficult** — not offstage, not posthumous, not a mentor.

## 5 · Decisions already made — do not re-open without dating the change

| Decision | Why |
|---|---|
| Duology, 2031 / 2033–34 | Keeps Lucid's extrapolation ladder honest; 2038 needed a bigger fictional leap |
| African Record Consortium, not a world-universities body | North Star: the world arrives *after* the work succeeds |
| Second Antarctic timestamp = the Anchor's later movement through an evidence store | Layered material history. **No time loop.** The pre-echo idea is retired — `RETIRED_IDEAS.md` |
| ARIADNE keeps the instrument name; BARA joke cut | In SA, *Bara* is Baragwanath — wrong collision in this book |
| Nairobi carries the whole conscience load | A separate ethical chair duplicates Kiki and wins arguments she should lose herself |
| Series **ONE RECORD**, Book I *The Record* | Series and Book I previously shared a title; and *One Record* is already shelf continuity (L-27) |

## 6 · Five traps

1. **Composite drift.** The apartheid-era case is composite **by construction, permanently** (L-09).
   Nothing adapts or keys to a real disappearance. Drift accumulates quietly during drafting and is
   the single thing most likely to make the book unpublishable. Figures are written by role and
   marked `[COMPOSITE]` until the historian and legal review names them.
2. **One Record ≠ Lucid World (L-27).** *One Record* is the ingested corpus — it survives Book II and
   is what *Afrika 2035* means a year later. *Lucid World* is history joined to live telemetry as one
   global causal graph — that is what Book II destroys the ability to recombine. A character who says
   "they deleted the One Record" is wrong and should be corrected on the page.
3. **Vopson is fringe and stays fringe** (`PHYSICS_ANCHORS.md`). Landauer (1961, real, measured 2012:
   k<sub>B</sub>T ln 2, 2.87 zJ at 300 K) is foundation. The mass-per-bit extension
   (3.19 × 10⁻³⁸ kg) is unconfirmed: the press, the believers and the forgers reach for it; **the
   consortium never claims it**, and G refuses it because no measurement currently kills it.
4. **Writing a reconstruction as footage.** If a scene has a face, sound and no gaps, you have written
   the forgery. That is a plot object, not a rendering style.
5. **Letting a node lose its voice.** Ghana names things and defends the names; Nairobi speaks in the
   conditional and will not be charmed; Antarctica reads colder in sentence length, not just content.
   The node voice sheet is at the foot of the beat ledger.

## 7 · What is genuinely open

**Human review only** — `canon/OPEN_DECISIONS.md`. None of it blocks drafting; all of it blocks
publication: historian + legal on the composite case · victim-family sensitivity read · Ghanaian and
Kenyan technical/cultural readers (every ensemble name is provisional until this clears) · SANAP
operational review · G on 420 terminology and the Landauer/Vopson boundary · Lucid architecture
(AJ/G) · quant read on Book II · cryptography review of the valid-signature paradox.

## 8 · Next actions, in order

**Done since the first handover:** the consent instrument (Beat 23a + its own canon file), G's spine
(Beats 3 · 36a · 39a · 52a), Naledi from inside her office (Beats 33a · 48a).

1. **Two pages of real prose — Beat 1 and Beat 16.** Do this first, before anything else on this
   list. The canon is now tightly specified and has never met a sentence. If the voice fights the
   architecture, discover it at 800 words, not at 40,000.
2. **Ensemble names.** Highest-leverage unlock. All 63 beats use provisional names pending Ghanaian,
   Kenyan and South African readers. A late rename is not find-and-replace — names carry rhythm and
   register in dialogue, and every 10k words raises the cost.
3. **The composite case → historian and legal review.** Same logic: drift toward a real
   disappearance accumulates *in prose*, quietly, and it is the one failure that makes the book
   unpublishable rather than merely worse.
4. **Book II at beat level.** Nearly every Book II payoff is planted in Book I. Drafting Book I with
   Book II only at sequence resolution means planting approximately, and plants are the one thing
   revision cannot fix without re-cutting scenes.
5. **Chapter ledger and a target length.** Book I's `target_words` is unset. 63 beats against a
   45–55 chapter target means **merging, not splitting** — the lettered beats (5a, 12a, 23a, 30a,
   33a, 34a, 36a, 39a, 48a, 52a) are mostly single scenes belonging inside a neighbouring chapter.
   Treat 63 as the scene count.
6. **POV distribution.** "Dries primary, rotating ensemble" is not a ratio. Decide chapters per node
   before drafting order is set.

Further riff targets are kept live at the foot of the beat ledger — currently the intermediary behind
the queue exception, Book II's Movement One, Ama's interiority, the family's attorney, and Sanna's
winter as a continuous thread.

## 9 · What stands between here and full send

Nothing blocks drafting. In order of what actually gates publication:

1. **~95k words that do not exist.** Everything else on this list is small next to it.
2. Items 2–3 above (names, composite case) — they gate *quality of drafting*, not drafting itself.
3. The remaining review gates in `canon/OPEN_DECISIONS.md`: SANAP operational, G on terminology,
   Lucid architecture, quant on Book II, cryptography on the valid-signature paradox, family
   sensitivity read.
4. Cover and `design/`; exports; then site wiring — a `PUBLISHED` id, a `CURATED` row, and, because
   L-03 puts this on its own line, a new **ONE RECORD** shelf plus its `SHELF_TAGLINE` entry.
   `site/build.py` already handles nested series roots (`history-before-time/books/bookN-*`), so
   `the-record/books/book1-the-record` needs no code change.
5. The full deploy loop: `build.py` → rsync into the platform repo → push both repos → Render
   redeploy. Live `arjunabadger.press` does not change until Render redeploys.

**Known inconsistency to resolve before this book has exports:** `CLAUDE.md` contradicts itself.
The repo-layout section says `build/export/` holds "EPUB + PDF (committed — these are the
downloads)"; the commit-discipline section says never commit heavy binaries, R2 via
`assets.manifest.json`, explicitly reversing the old commit-exports rule. The layout section looks
stale.

## 10 · Repo mechanics

- Merged to **`master`** 2026-08-19 as `de3787e` (rebase merge, eight commits kept distinct so the
  security-doctrine change stayed visible). PR **#1** closed. Branch
  `claude/420-code-history-machine-t436ve` still exists on the remote and can be deleted.
- **CI:** `gate` (asset gate — never commit binaries; R2 + `assets.manifest.json` instead) and `scan`
  (`scripts/leak_scan.py`). Both green at merge.
- `scan` carries a **consent register**: protected identifiers stay listed, and `CONSENTED` maps an
  identifier to the paths its consent actually covers. One identifier is currently consented, scoped
  to a single book and attested 2026-08-19; see `scripts/leak_scan.py` and `SECURITY.md` for who and
  when. **Adding a row asserts that a real human said yes.** Never add one to make CI green.
  *(This file is outside that scope, which is why it does not name him — the register fired on an
  earlier draft of this handover, which is the mechanism working.)*
- Nothing in `site/build.py`. The id is the gate.

## 11 · Provenance

Source: `The_Record_Series_Bible.docx` **v0.1**, prepared for AJ Greyling — transcribed to repo canon
2026-08-19, plus AJ's beat ledger pass (beats 1–25) landed verbatim and extended (26–53, four
lettered Landauer beats, and six more for the consent instrument, G and Naledi). Upstream shelf continuity: *Afrika 2035*. Downstream: *AFRIKA 2100*, not
binding, no winks. Public references and the legal/editorial note: `canon/SOURCES.md`.
