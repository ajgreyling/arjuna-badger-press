# ONE RECORD — handover

> African science-thriller duology. **Book I *The Record*** (2031) · **Book II *The Forward Cone***
> (2033–34). Canon locked 2026-08-19 and **merged to `master`**. Book I was finished on 2026-08-20
> at **53 chapters · 45,399 source words** and authorised for publication by explicit author
> override after developmental and machine-polish passes. Book II was finished on 2026-08-20 at
> **27 chapters · 34,693 source words**; it remains outside-review and release-approval gated.
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
| Book I cut | **Finished; release authorised** — 53 chapters · 45,399 source words · final validation in release loop |
| Book II cut | **Finished; review pending** — 27 chapters · 34,693 source words · final cover · EPUBCheck clean · 165-page PDF inspected |
| Chapter ledgers | Complete through Book I Chapter 53 and Book II Chapter 27 |
| Prose audit | Both manuscripts completed developmental, continuity, exact/semantic deduplication, NovelBench and guarded local DE-LLM passes; admissions and rejections are recorded in each final ledger |
| Site | Book I approved for `PUBLISHED`/`CURATED`; Book II remains unlisted |

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

**Outside review register** — `canon/OPEN_DECISIONS.md`: historian + legal on the composite case ·
victim-family sensitivity read · Ghanaian and Kenyan technical/cultural readers · SANAP operational
review · G on 420 terminology and the Landauer/Vopson boundary · Lucid architecture (AJ/G) · quant
read on Book II · cryptography review of the valid-signature paradox. None was performed for Book I;
the author explicitly overrode that release gate on 2026-08-20. Book II's internal revision is now
complete; quant/market-structure, cryptography/provenance and SANAP review plus a separate release
decision remain outstanding.

## 8 · Next actions, in order

**Book I done:** 53-chapter developmental cut; P0 and relationship-bearing P1 revisions; continuity
and plant/payoff check; exact and semantic deduplication; guarded Ollama DE-LLM with no generated
rewrite admitted; NovelBench telemetry; final cover and gate-rendered artifacts.

1. **Book I release loop.** EPUBCheck and PDF inspection; update R2 manifests; add Book I to
   `PUBLISHED`/`CURATED` and the ONE RECORD shelf; run the two-repo deploy; verify Render and each
   reader/download route before calling it live.
2. **Book II human review and release decision.** The manuscript, cover and reading artifacts are
   finished. Obtain the quant/market-structure, cryptography/provenance and SANAP reviews, resolve
   material findings, then obtain explicit Book II release approval. Book I's override does not
   silently apply to Book II.
3. **Optional post-publication outside review.** If a historian, family-sensitivity reader or node
   specialist later identifies harm or error, revise the live edition and retain the disclosure trail.

## 9 · What stands between here and full send

For Book I: completion of the R2/site/Render release loop and live-route verification. For Book II:
the three named outside reviews, any resulting corrections and explicit release approval, followed
by its own R2/site/Render release loop. Book II is manuscript-complete but deliberately absent from
`PUBLISHED` and `CURATED`.

The current EPUB/PDF files are working build products and remain untracked. Do not commit them;
final heavy assets follow the R2 and `assets.manifest.json` path in `AGENTS.md`.

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
