# CROSS-BOOK WEAVE — the three-way trilogy braid

> **Trilogy-wide binding canon** (not one book's). The single source of truth for how *RESONANCE*,
> *REVELATION*, and *RELIC* interlock. Gate-enforced by `storygraph/crumbs.py` over the **unified**
> StoryGraph. Lives in RELIC's canon because RELIC is the capstone that closes the weave, but it
> governs all three.
>
> **The model is three-way, not pairwise.** A *crumb* is one motif with **appearances across the
> books** — each appearance is a `seed` (a subtle plant) or a `landing` (where it pays off / is
> recognised). A crumb is **woven-complete only when a reader has read all three books**; no single
> book completes it. Seeding is **mutual**: RESONANCE may seed something RELIC lands, *and* RELIC
> seeds something that retroactively illuminates RESONANCE. The braid weaves all three together so
> that the trilogy-as-a-whole is more than the sum, while **each book stays standalone-intact.**

Books: **R** = *RESONANCE* (1) · **REV** = *REVELATION* (2) · **REL** = *RELIC* (3).

## The two invariants the gate enforces

1. **STANDALONE-INTACT** — each book reads complete on its own. **No appearance may be load-bearing
   for its own book's plot.** A first-time reader of any one book never needs another to follow it.
   (Hard error if violated.)
2. **WEAVE-INTACT** — every crumb's declared appearances exist across the set, and the crumb
   **closes when all three are read**. A crumb that names an appearance in a book where it is never
   anchored is a dangling weave (warning → error once that book is drafted). A crumb with only one
   appearance is not a weave — it's a single-book thread (belongs in that book's thread ledger).

## Appearance grammar

Each crumb lists **appearances**, one per book it touches:

> `<BOOK>: <seed|landing|mutual> — <the anchoring detail> [@ where, when known]`

- **seed** — a subtle plant; means little on first read, loads later.
- **landing** — where the motif pays off / is recognised / reframed.
- **mutual** — both at once: it seeds forward *and* lands something seeded elsewhere (the
  bidirectional case).

**Reading-order independence:** the weave must reward *any* order. A reader who starts with REL and
then reads R must find R's seed loaded; a reader who starts with R and reaches REL must find the
landing. So most crumbs carry a `seed` in the earlier-written book and a `landing` in the later,
**plus** — where it deepens the braid — a faint **back-seed** in the later book that a re-reader of
the earlier one catches. State the intended effect per direction; never make either direction
required.

## RESONANCE's gold-site seeding (the "frozen except" — sanctioned light edits)

RESONANCE is frozen **except** for: the vitrified-tunnel plant, the Priya setup, and — sanctioned
here — **light references to real ancient-gold-mining and gold-trading sites** that weave R into the
trilogy. Arin is a KwaZulu-Natal engineer who works in deep mines, so these touches are *native to
his world* — invisible-as-plot to a book-1-only reader, loaded for the trilogy reader. They give R
more `seed` appearances (esp. `crumb:resonance-gold`, `crumb:gold-was-never-wealth`,
`crumb:builders-deep-history`).

**Sanctioned R touch-points (subtle, standalone-invisible — applied via the RESONANCE change-set,
not this session):**
- **Mapungubwe** — the real SA gold-kingdom (the gold rhinoceros; 9th–13th c.). A passing mention —
  a museum reference, a colleague's aside, a line about SA's deep gold heritage — seeds RELIC's
  gold-as-deep-root thread. (WONDER_OF_PLACE.)
- **The Witwatersrand's deep antiquity** — Arin's mines already sit on Archean gold; a single line
  noting the *age* of the gold (older than anything human) back-seeds the Builders.
- **Great Zimbabwe / the gold-trade routes** — a passing cultural/historical reference (the dry-
  stone kingdoms, the gold that moved north) seeds the inheritance trail RELIC walks.
- **Vredefort** — already canon-adjacent to R's setting; a faint note that the oldest scar and the
  gold are connected back-seeds RELIC's waveguide.
- **Gold "rings"/tone** — the keystone back-seed: one otherwise-throwaway R line about a
  resonance/tone in the deep rock that "shouldn't carry," which only RELIC explains.

**Rules:** each touch is **one line / one image**, never a scene; never load-bearing for R's plot;
never contradicts R's frozen canon; reads as natural texture in Arin's engineering world. These are
**weave seeds**, logged as R appearances in the matrix above, realised when the RESONANCE
change-set is applied.

---

## THE WOVEN CRUMBS

### `crumb:resonance-gold` — gold is the thing that resonates (the keystone)
The trilogy's title-level hinge. Gold's function is acoustic/resonant (GOLD.md): it is the medium
that makes the ancient machines *resonate*. This binds REL's MacGuffin to R's very title.
- **Appearances:**
  - **REL: landing** — the worked gold "rings"; "the string, not the gong"; the waveguide. The
    mechanism is shown in full (grounded).
  - **R: mutual** — R's title and its hidden-mind resonance are, in hindsight, the *same physics* a
    re-reader now sees; **back-seed**: a faint, otherwise-throwaway line in R about a resonance/tone
    that "shouldn't carry" gains meaning only after REL.
  - **REV: seed** — REV's gold economy (the untraceable bullion) sits on top of this without knowing
    it; a single REV image (gold that is valued for something *other* than money) faintly prefigures.
- **Woven effect:** read all three and gold = value (REV) = medium (REL) = the resonance R was named
  for. **Standalone:** each book's gold reads complete on its own terms.

### `crumb:vitrified-tunnel` — the smooth-to-the-touch bore
- **Appearances:**
  - **R: seed** — Arin crawls a tunnel *smooth to the touch like vitrified glass*; in R it is an
    unexplained, eerie detail (and stays standalone-fine as atmosphere).
  - **REL: landing** — it's a **waveguide**, made smooth on purpose by the Builders (Node 3,
    Vredefort); Arin re-enters because it now means something.
  - **REL: back-seed** — a line in REL that only a returning R reader catches (Arin references the
    *first* tunnel without REL ever explaining R's plot).
- **Woven effect:** R's creepy detail becomes REL's engineering. **Standalone:** R never needs REL;
  REL introduces the bore fresh.

### `crumb:the-court` — the machine-mind across time (and its threshold)
- **Appearances:**
  - **R: landing** — the Court / SAGE is *born* and proven a person (R's whole arc).
  - **REL: mutual** — the Court returns in a new form, having *studied* the ancient instrument; it
    carries memory of R (a re-reader feels the lineage) and **back-seeds** a recognition that ties
    the made-mind to the Builders' work. **At RELIC's climax the Court steps aside** — the one
    intelligence that cannot operate a consciousness-keyed machine (MYTHOS_RULES Rule 7-T) —
    completing R's "can a made mind be a person?" with *…and even a person-mind has a threshold it
    can't cross.*
  - **REV: seed** — REV's "AI re-translating the texts" is a *different* machine-intelligence, but
    the trilogy reader clocks the rhyme: minds made to read what humans altered or forgot.
- **Woven effect:** three machine-intelligences, one question — and RELIC's answer is the limit of
  mind-as-computation. **Standalone:** each book's AI is self-contained.
- **Woven effect:** three machine-intelligences, one question (what do we owe a mind that sees what
  we hid?). **Standalone:** each book's AI is self-contained.

### `crumb:priya` — the engineer who signs her name to the failure
- **Appearances:**
  - **R: seed** — Priya Ellis appears as the neural-feedback engineer who reads telemetry and owns
    her calibration failure (a strong supporting beat; standalone-complete in R).
  - **REL: landing** — she is the lead; her R wound and exit from AugmenTech are her backstory,
    shown not lectured.
- **Woven effect:** the reader who met her in R feels her growth into the lead. **Standalone:** REL
  teaches the newcomer exactly enough; R needs nothing from REL.

### `crumb:gold-was-never-wealth` — the untraceable gold flips
- **Appearances:**
  - **REV: seed** — the Brotherhood banks/moves untraceable physical gold / Krugerrands (the
    John-Wick economy; REV deck item #9). In REV it reads as secret *money* (standalone-complete).
  - **REL: landing** — the flip: it was **never wealth, it was a key** (GOLD.md Layer A/B). The
    Brotherhood coin's hidden resonance geometry is the real reason they never spent it.
  - **REV: back-seed** — one REV line about *why* the order never converts the last of it ("some of
    it is not for spending") that a REL reader retroactively understands.
  - **R: seed (⏳ pending — see docs/RESONANCE_CHANGESET.md item 4)** — *if applied:* Arin uses gold
    in the Guardian for its real physical properties (making the suit work but ~100× too costly to
    sell). In R it reads as impractical genius / why the Guardian stays a one-off; REL reveals he
    stumbled onto the resonance principle — gold's value was never monetary, and Arin *proved* it by
    ignoring the money. Awaiting the author's depth + mechanism decision before this R appearance is
    realised.
- **Woven effect:** REV's secret money + (pending) Arin's "too-expensive" Guardian both become REL's
  machine key — gold's value was never wealth. **Standalone:** every read holds on its own.

### `crumb:brotherhood` — the keepers, transformed
- **Appearances:**
  - **REV: landing** — the Brotherhood of Abraham as keepers of altered-text truth (REV's order).
  - **REL: mutual** — transformed into keepers of the *key*; Leila carries her REV evidence-
    discipline forward; **back-seed** ties REL's custody back to REV's stewardship.
- **Woven effect:** one order, two custodies (truth, then the machine). **Standalone:** each holds.

### `crumb:the-fixer` — the man who is the road, never the destination
The recurring South African fixer the keepers trust — soft-bellied, unbothered, pale eyes doing
their slow total reading; he keeps the party alive and supplies *nothing* of the insight or the win
(the white-saviour firewall, binding: the locals lead, break the case, own it). His full series
sheet is the SSOT at `books/history-before-time/canon/characters/JAKOBUS_SWART.md`; in the trilogy
he is **iceberg only** — present, never explained.
- **Appearances:**
  - **R: seed** — operates in the SA deep-mining world under the cover-alias *Jakobus Gerber / "Jan"
    Venter*; the deeper biography (Border War, the relay Order) is never exposed.
  - **REV: mutual** — the dust-coloured Land Cruiser fixer who extracts Leila off the mountain after
    the safe-house betrayal and defers to the keeper Tewodros; **back-seed** — a re-reader of R now
    reads "Jan Venter" as the same man.
  - **REL: landing** — the unnamed pilot who flies Priya's party out of the Aksum firefight to the
    drowned-temple reservoir in Egypt (ch-15); he answers to Leila (of the line), never opens the
    bag, and is gone. Priya never gets the name.
- **Woven effect:** a returning reader recognises the fixer (the Cruiser, the bare-eyed read, the
  refusal to claim) and is rewarded; the debt-and-favour economy that places him reads as one quiet
  tissue across all three. **Standalone (binding):** in REL he is a nameless pilot the Order sent —
  **never load-bearing**; a first-time RELIC reader needs none of the other books to follow the
  scene. (Crumb rule: reward, never require — his name is never given in REL.)

### `crumb:stewardship` — who gets to mediate / decide
The trilogy's spine-question, threaded as a crumb because it *evolves* across the three.
- **Appearances:**
  - **R: seed** — what do we owe a made mind? (a person we can switch off).
  - **REV: mutual** — who gets to mediate destabilising truth? (stewardship without ownership).
  - **REL: landing** — who decides what humanity switches on? (technological consent). REL's climax
    answers the question R and REV each asked a facet of.
- **Woven effect:** three facets of one moral question, resolved in REL. **Standalone:** each book's
  theme is whole on its own.

### `crumb:all-the-same` — one light, refracted (deep)
- **Appearances:**
  - **REV: seed** — "all the same"; the anti-dogmatic, consciousness-adjacent substrate.
  - **R: mutual** — the made mind as another facet of the one light.
  - **REL: landing** — the Builders, the inheritors, the faiths, the machine: partial views of one
    thing; lands in REL's epilogue as benediction (theme only — never mechanism; MYTHOS_RULES R7).
- **Woven effect:** the trilogy's soul-line, completed across all three. **Standalone:** carried as
  meaning in each.

### `crumb:builders-deep-history` — the shared ancient layer (deep)
- **Appearances:**
  - **R: seed** — R's resonance was a *partial view* of the Builders' physics (a re-reader sees it).
  - **REV: seed** — REV's ancient gold/Ophir/Aksum history was a *partial view* of the Builders'
    inheritance (a re-reader sees it).
  - **REL: landing** — the ancient layer (TIMELINE Layer A) is revealed as the shared deep-history
    both prior books half-saw; the weave closes here.
- **Woven effect:** R's physics + REV's history were two windows on the same lost civilisation, seen
  whole only in REL. **Standalone:** neither prior book needs REL to stand.

---

## THE WEAVE, AT A GLANCE

```
                R (RESONANCE)         REV (REVELATION)        REL (RELIC)
resonance-gold   mutual(back-seed) ·· seed ·············· landing      ← title hinge
vitrified-tunnel seed ·························· landing+back-seed
the-court        landing ··········· seed ·············· mutual(back-seed)
priya            seed ······························· landing
gold-was-never…              ······· seed+back-seed ··· landing
brotherhood                  ······· landing ·········· mutual(back-seed)
stewardship      seed ······ mutual ················· landing          ← spine question
all-the-same     mutual ···· seed ·················· landing
builders-deep…   seed ······ seed ·················· landing           ← closes the weave
```

Every row touches **≥2 books**; the four spine rows (`resonance-gold`, `the-court`, `stewardship`,
`builders-deep-history`, `all-the-same`) touch **all three** and are the load that makes the
trilogy whole. **No cell is required for its own book.** The weave closes when all three are read,
in any order.

---

## Gate checks (`storygraph/crumbs.py`, over the unified graph)

| Check | Severity | Flags |
|---|---|---|
| `crumb_load_bearing` | **error** | an appearance a newcomer of *that book* must follow to understand its plot (breaks standalone-intact) |
| `crumb_single_book` | warning | a "crumb" with appearances in only one book (it's a thread, not a weave) |
| `crumb_unanchored` | warning→error | a declared appearance never anchored in that book's manuscript (error once that book is drafted) |
| `crumb_unwoven` | warning | a crumb whose appearances don't yet span its declared books in the graph |
| `weave_incomplete` | info | crumbs that won't fully close until a not-yet-drafted book lands its appearance (expected mid-build) |

> **Design law:** the weave **rewards** reading all three and **requires** none. Each book is a
> whole; the trilogy is a greater whole; the gate keeps both true at once.
