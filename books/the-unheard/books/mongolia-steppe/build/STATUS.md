# Build status — *The Felt and the Sky* (unheard-mongolia)

**DRAFT COMPLETE — 2026-06-14.** Full first draft of all 23 narrative chapters + `ch-99` backmatter (~44k prose; ~53k merged with dedication + front matter + expanded *What Is Real*).

## What exists
- **Canon (bible v1.0):** `PLACE_RESEARCH.md` (sourced, 3-vote adversarially verified) + `STORY_BIBLE`,
  `WORLD`, `CHARACTERS`, `MYTHOS_RULES`, `THEMES`, `PLOT`, `JAKOBUS_SPINOFF`, `EPIGRAPHS`, `SEED_STORY`.
- **Dedication:** `canon/DEDICATION_BOOK.md` (wired into merge front matter).
- **Outline:** `build/outline.json` (24 ch plan incl. backmatter; narrative ends ch-23).
- **Manuscript:** `build/chapters/ch-01..23.md` + `ch-99.md` → merged `build/BOOK.md` + `BOOK.novelcrafter.md`
  (DERIVED, gitignored — commit only `chapters/` + `canon/`).
- **Export:** `build/export/The Felt and the Sky.epub` + `.pdf` (cover: `design/cover.jpg`).

## Verified
- **Continuity:** all character names consistent across 24 ch; zero stray/wrong-book names; the relay
  nodes and act structure follow PLOT.md.
- **The 4 Jakobus payoffs**, in locked placement: tea (ch-04) · wrestling humbling, SSOT line verbatim
  (ch-08) · the horse / machine creed + the generous flip side (ch-09) · the long-song dance grace-note
  (ch-14); + a completed Sawubona/Sikhona pair (ch-23, Otgon → Jakobus).
- **Keel held:** the herders lead, decide, own the win; Jakobus is the road (never POV, never the hero,
  drives the voice to town and stays in the van); the win is honest-partial (route kept open, spring
  watched-not-saved, animals die, Sukh leaves) per §7a; sacred withheld (ovoo at threshold, fictional
  long-song); Khalkha ≠ Kazakh stated in the back matter.
- **De-LLM (self-scan on the real BOOK.md):** spaced em-dash 0 · "it wasn't X it was Y" 0 ·
  sentence-initial "Not X." 0 · "something moved in" 0 · "filed it under" 0 · "almost [emotion]" 3
  (earned band) · "the way" 117 (under the ≤130 plateau; reflexive doubles cut by reading). Clean at the
  earned-residual plateau.

> NB the unified **trilogy** continuity gate (`./run.sh gate`) PASSES (0 errors) but does **not** ingest
> this book — the Unheard series lives in `the-unheard/` outside the StoryGraph trilogy ingest. Continuity
> for this book was verified manually (names/relay/payoffs) + the prose-tic scanner (which DOES resolve
> the book, though it labels output "RELIC" via the inherited tic config and conflates RELIC's BOOK.md
> counts — the real per-book numbers above were taken directly from this book's BOOK.md).

## Known gaps (next passes — author's call)
1. **Length: ~44k vs 88k target.** The draft is tight. An **expand pass** (`./run.sh --book
   unheard-mongolia expand` or hand-expansion against the outline) could grow set-pieces, the herder
   community texture, and Act II breathing room toward novel length — without padding.
2. **SENSITIVITY READ — the hard gate before publication (MYTHOS Rule 7).** In-culture Mongolian
   consultants (herders, long-song/wrestling tradition-holders, scholars) with a real veto. ALL names +
   depictions provisional until then. Lived-experience consultants (Tourette's, autism, Deaf) for the
   crew. This is "drafted," NOT "publication-final."
3. **Front matter:** wired via engine merge (`series_title: The Unheard`, `DEDICATION_BOOK.md`, `ch-99` backmatter). EPUB + PDF exported 2026-06-14.
4. **A full cold-read / craft-audit** pass (the metered Opus reads) once length + sensitivity are settled.

## Provenance
Claude single-shot prose per the MASTER_PLAN operating model (the prose engine); the repo tooling
(merge, prose-tic scanner) measured & alarmed; no metered generation. Research via the deep-research
workflow (recovered from a killed run's verified claims). Goal: "/goal full send. finish the novel."
