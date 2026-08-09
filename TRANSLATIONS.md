# Translations — Arjuna Badger Press

The catalog ships **full parallel editions** in translation. This file is the binding
spec for *which* languages each book gets and *why*. The pipeline (`tools/translate_book.sh`,
`tools/translate_real.sh`) reads a per-book `LANGUAGES.json` that must conform to the rules below.

## The rule

> Translate each book into **the languages of the cultures it actually touches**, plus a
> catalog-wide market pair. "Cultures touched" is read at the level of the **specific**
> culture a book honours — never a national monolith. The Deccan book is *Marathi*, the
> Mahabalipuram book is *Tamil*; they are not interchangeably "Indian."

Concretely, a book's edition set =

1. **Regional languages** — the dominant language(s) of the book's setting/culture.
2. **Afrikaans** — for any book set in **South Africa or Namibia**.
3. **Market pair** — **Spanish + French**, added to *every* book for reach *(temporarily deferred during the corpus-first SA regional pass — see below)*.

### Hard exclusions (decided)

- **Indigenous / endangered / sacred-adjacent languages are OUT of scope for AI translation.**
  Books that carry a `sensitivity_read: REQUIRED` flag for an Indigenous people (the Aboriginal,
  Khalkha, Ainu, Topnaar/ǂAonin material) are translated only into the **dominant national /
  contact language** of their setting — never into the Indigenous language itself. AI translation
  into those languages risks exactly the harm the sensitivity reads exist to prevent. This is a
  dignity-first decision, consistent with the project's own stance.
- **Placeless / invented-world books** (`The Loneliest People…`, the Salt-Veil / Dust-Throne
  fantasy with their invented tongues) have no real culture to map. They take the **market pair
  only** (Spanish + French) — a *reach* rationale, explicitly NOT a "cultures touched" one.

### Faithfulness rules (apply to every edition)

- Words the source leaves **deliberately untranslated** (e.g. isiZulu phrases in *Resonance*)
  stay **verbatim in every edition**, including the regional and market ones. Foreignness is content.
- **Proper names and invented entities are never translated** (characters, places, Guardian, SAGE…).
- **No translator's notes / footnotes / glosses** the source doesn't already have.
- Front-/back-matter **structure** is preserved; only its prose is translated.
- Each book's `GLOSSARY_PRESERVE.json` (produced by `tools/extract_glossary.py`) is the
  machine-checkable preserve-list.

### QA scan of shipped editions (Buabantu scan, 2026-06-21)

A mechanical faithfulness scan over the 4 live *RESONANCE* editions (af · fr · es · zu):

- **Proper names preserved** — Priya · Arin · Jakobus · Ellis · Ndlela intact in all 4 ✅
- **No translator's-note leakage** in any edition ✅
- **Chapter alignment** — all 4 have the full 24 chapters, correctly translated headings; nothing dropped ✅
- **Length ratios:** af 1.07 · fr 1.15 · es 1.05 (all healthy). **isiZulu 0.66** — a flat ~0.66 across
  *every* chapter (not localized), which is **expected, not a defect**: isiZulu is agglutinative and packs
  articles/prepositions/pronouns into single inflected words, so a faithful zu translation genuinely has
  ~30–35% fewer whitespace words than its English source.

> ⚠️ **Engine lesson (do not re-raise this false alarm):** raw word-count length-ratio QA is calibrated
> for European languages (≈0.9–1.15). It is **wrong for agglutinative Bantu languages** (Zulu/Xhosa/Sotho/
> Tswana), which legitimately run ~0.6–0.7. Any Buabantu/translation length check needs **per-language-family
> baselines**, or it cries wolf on every Nguni/Sotho edition. (This is a real Buabantu design requirement —
> see `arjuna-badger-platform/docs/MISOGI.md`, Buabantu section.)

## People's Language (in progress)

The SA regional pass and Real Language API are being branded **People's Language** (working title):
translation into everyday, register-aware speech, corpus-first. Taglines per language and engineering
notes: [`docs/PEOPLES_LANGUAGE.md`](docs/PEOPLES_LANGUAGE.md).

## Corpus-first SA regional pass (2026)

**Active scope:** `af`, `zu`, `xh`, `st`, `tn`, `sw` (where setting warrants).

**Deferred for this pass:**
- **Spanish + French** — market pair returns after SA regional editions are reviewed.
- **Revelation** — Ethiopia setting; Amharic deferred; no SA langs apply.

Human-curated urban slang in [`docs/corpus/`](docs/corpus/) (weight 100, cited sources) **outranks AI**
via the same [`correction_corpus.py`](../arjuna-badger-platform/saas/correction_corpus.py) router as
the `/api/real-language` endpoint. Batch translation uses:

```
tools/translate_real.sh books/<book>     # split → Aya + corpus → verify → render
./tools/run_translate_ab.sh books/<book> --provider aya --codes zu,af,xh,st,tn
```

Each target in `LANGUAGES.json` carries a `"temp"` register (default 0.75 for SA urban langs; 0.5 for literary-neutral Swahili).

## Per-book edition map

`★` = pilot (built first). `RR` = regional. `AF` = Afrikaans (SA/Namibia rule). `MK` = market pair (es+fr, deferred this pass).
Languages in *italics* are **candidates pending the author's confirmation** (marked `?` below).

| Book | Setting / culture | Regional | Afrikaans | Market | Notes |
|---|---|---|---|---|---|
| **Resonance** ★ | Near-future SA · KZN/Zulu | zu · xh · st · tn | ✅ af | ~~es · fr~~ deferred | corpus-first pilot; 5 SA langs |
| Revelation | Ethiopia · Lalibela/Addis | Amharic | — | es · fr | **deferred** — not SA |
| Relic | Witwatersrand · Mpumalanga | zu · xh · st · tn | ✅ af | ~~es · fr~~ deferred | corpus-first; 5 SA langs |
| Calendar of Stone (HBT 1) | Cape → up Africa | zu · xh · st · tn · sw | ✅ af | ~~es · fr~~ deferred | sw for up-Africa leg |
| The Indian One (HBT 2) | India · diaspora→North | Hindi | — | es · fr | outside SA pass |
| The Temple in the Rock (HBT 3) | Deccan · **Marathi** | Marathi | — | es · fr | outside SA pass |
| The Shore That Remembers (HBT 4) | Mahabalipuram · **Tamil** | Tamil | — | es · fr | outside SA pass |
| The Engineer of the Gods (HBT 5) | Egypt · Nile | Arabic | *? (SA engineer lead)* | es · fr | outside SA pass |
| The Silver Thread (Jakobus) | San / Border War · SA–SWA | — *(San excluded: Indigenous)* | ✅ af | ~~es · fr~~ deferred | af only this pass |
| The Recitation (Jakobus) | Sahara · Quran/Arabic | Arabic | — | es · fr | outside SA pass |
| The Rose in the Rock (Jakobus) | Petra · Jordan | Arabic | — | es · fr | outside SA pass |
| The Straight Darkness (Jakobus) | Longyou · China | Mandarin | — | es · fr | outside SA pass |
| The Broken Crescent (Jakobus) | Iraq·Afghanistan·Syria | Arabic · *Persian/Dari?* | — | es · fr | seed stage |
| The Long Dark (Jakobus) | SA load-shedding collapse | isiZulu | ✅ | es · fr | bible stage; af+zu when ready |
| **Southern Coast** (Jakobus) | Namib/SA coast | — | ✅ af | ~~es · fr~~ deferred | af only this pass |
| The Felt and the Sky (Unheard) | Mongolia · Khalkha | Mongolian (Khalkha) | — | es · fr | sensitivity read |
| The Songlines of Stone (Unheard) | Australia · Aboriginal | — *(Aboriginal langs excluded)* | — | es · fr | English-native + market only |
| (Japan / Ainu) (Unheard) | Japan · Ainu | Japanese *(Ainu excluded)* | — | es · fr | sensitivity read |
| The Indifferent Desert | Namib 1940–42 | German | ✅ | es · fr | sensitivity read; Topnaar excluded |
| The Loneliest People… | Invented / unnamed | — | — | es · fr | market-only |
| The Salt Veil · Dust Throne | Secondary-world fantasy | — *(invented tongue)* | — | es · fr | market-only |
| The Men Who Opened the Door | US · remote-viewing | — (English-native) | — | es · fr | market-only |
| Modern Sherlock (Reichenbach) | England | — (English-native) | — | es · fr | public-domain derivation |
| **Palindrome** | Chamber piece · SA names (Grahamstown, Loubser ’81) | — | ✅ af *(prose)* | — | Full Afrikaans prose translation → `Palindrome.af`; Emma audiobook from `BOOK.af.md` |
| **Palindroom Toneelstuk** | Stage adaptation of Palindrome | — | — *(standalone AF play)* | — | Separate shelf title; same cover plate as Palindrome |

> Books in `books/_comingsoon/` inherit the same rules once they reach draft; add their
> `LANGUAGES.json` at that point.

## Pipeline

```
tools/extract_glossary.py books/<book>            # → <book>/GLOSSARY_PRESERVE.json
edit books/<book>/LANGUAGES.json                  # declare targets + directives + temp
tools/translate_book.sh books/<book> split        # → build/.translate/segments/
./tools/run_translate_ab.sh books/<book> --provider aya --codes zu,af,xh,st,tn
tools/translate_book.sh books/<book> reassemble <code>   # each lang
tools/verify_translation.py books/<book>
tools/render_book.sh build/BOOK.<code>.md  "<out>"  "<Title>"  "<Author>"   # → EPUB + PDF

# Or the all-in-one corpus-first wrapper:
tools/translate_real.sh books/<book> [--codes zu] [--segments 0,1]
```

Body prose in every edition still renders in **Atkinson Hyperlegible** through the binding
render gate. Translation never bypasses the gate.

## Community corrections (`/fix-translation.html`)

AI editions are a first pass. **First-language speakers** can submit better colloquialisms, idioms,
and register fixes through the **Fix a translation** programme on [arjunabadger.press](https://arjunabadger.press/fix-translation.html).

| What | How |
|---|---|
| **Submit** | Hosted form (or `mailto:j@` fallback) — book, language, passage, your wording |
| **Accepted fixes** | Listed on the site; credited in the book; **fed into Real Language corpus** (weight 100, outranks AI) |
| **SA urban seed corpus** | [`docs/corpus/sa_urban_*.json`](docs/corpus/) — cited slang entries loaded via `REAL_LANGUAGE_CORPUS_DIR` |
| **Real Language API** | `/api/real-language` routes corpus-first — exact human match = no LLM call |
| **Top contributors** | Named per language; leading voices receive a **free printed copy** of any press book in the language they helped — their choice |
| **Terms** | By submitting you allow accepted wording to be published and licensed for income; not every suggestion is accepted |

Operational detail: [`docs/FIX_TRANSLATION_PLAN.md`](docs/FIX_TRANSLATION_PLAN.md) · data file:
[`docs/translation_fixes.json`](docs/translation_fixes.json) (rebuild to publish updates).

## Status

- **Corpus-first SA regional pass (active):** Resonance → Relic → HBT SA-set books.
- **Pilot targets:** Resonance `af`, `zu`, `xh`, `st`, `tn` via Aya + binding corpus.
- **Revelation:** deferred (Ethiopia; no SA langs).
- **es/fr:** temporarily deferred; return after regional editions reviewed.
- **Community fixes:** programme live; SA urban seed corpus in `docs/corpus/`; accepted log fills as first-language review lands.
