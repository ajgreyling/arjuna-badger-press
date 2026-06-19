# Translations — Arjuna Badger Press

The catalog ships **full parallel editions** in translation. This file is the binding
spec for *which* languages each book gets and *why*. The pipeline (`tools/translate_book.sh`)
reads a per-book `LANGUAGES.json` that must conform to the rules below.

## The rule

> Translate each book into **the languages of the cultures it actually touches**, plus a
> catalog-wide market pair. "Cultures touched" is read at the level of the **specific**
> culture a book honours — never a national monolith. The Deccan book is *Marathi*, the
> Mahabalipuram book is *Tamil*; they are not interchangeably "Indian."

Concretely, a book's edition set =

1. **Regional languages** — the dominant language(s) of the book's setting/culture.
2. **Afrikaans** — for any book set in **South Africa or Namibia**.
3. **Market pair** — **Spanish + French**, added to *every* book for reach.

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

## Per-book edition map

`★` = pilot (built first). `RR` = regional. `AF` = Afrikaans (SA/Namibia rule). `MK` = market pair (es+fr).
Languages in *italics* are **candidates pending the author's confirmation** (marked `?` below).

| Book | Setting / culture | Regional | Afrikaans | Market | Notes |
|---|---|---|---|---|---|
| **Resonance** ★ | Near-future SA · KZN/Zulu | isiZulu | ✅ | es · fr | pilot; canon: don't over-translate isiZulu |
| Revelation | Ethiopia · Lalibela/Addis | Amharic | — | es · fr | trilogy sibling but NOT SA → no Afrikaans |
| Relic | Witwatersrand · Mpumalanga | isiZulu | ✅ | es · fr | |
| Calendar of Stone (HBT 1) | Cape → up Africa | isiZulu · *Swahili?* | ✅ (partial — Cape open) | es · fr | |
| The Indian One (HBT 2) | India · diaspora→North | Hindi | — | es · fr | |
| The Temple in the Rock (HBT 3) | Deccan · **Marathi** | Marathi | — | es · fr | canon refuses the "Indian" monolith |
| The Shore That Remembers (HBT 4) | Mahabalipuram · **Tamil** | Tamil | — | es · fr | |
| The Engineer of the Gods (HBT 5) | Egypt · Nile | Arabic | *? (SA engineer lead)* | es · fr | Afrikaans only if SA-set scenes warrant |
| The Silver Thread (Jakobus) | San / Border War · SA–SWA | — *(San excluded: Indigenous)* | ✅ | es · fr | |
| The Recitation (Jakobus) | Sahara · Quran/Arabic | Arabic | — | es · fr | |
| The Rose in the Rock (Jakobus) | Petra · Jordan | Arabic | — | es · fr | |
| The Straight Darkness (Jakobus) | Longyou · China | Mandarin | — | es · fr | |
| The Broken Crescent (Jakobus) | Iraq·Afghanistan·Syria | Arabic · *Persian/Dari?* | — | es · fr | seed stage |
| The Long Dark (Jakobus) | SA load-shedding collapse | isiZulu | ✅ | es · fr | bible stage |
| The Felt and the Sky (Unheard) | Mongolia · Khalkha | Mongolian (Khalkha) | — | es · fr | sensitivity read; no sacred content |
| The Songlines of Stone (Unheard) | Australia · Aboriginal | — *(Aboriginal langs excluded)* | — | es · fr | English-native + market only |
| (Japan / Ainu) (Unheard) | Japan · Ainu | Japanese *(Ainu excluded)* | — | es · fr | sensitivity read |
| The Indifferent Desert | Namib 1940–42 | German | ✅ | es · fr | sensitivity read; Topnaar excluded |
| The Loneliest People… | Invented / unnamed | — | — | es · fr | market-only (reach rationale) |
| The Salt Veil · Dust Throne | Secondary-world fantasy | — *(invented tongue)* | — | es · fr | market-only |
| The Men Who Opened the Door | US · remote-viewing | — (English-native) | — | es · fr | market-only |
| Modern Sherlock (Reichenbach) | England | — (English-native) | — | es · fr | public-domain derivation |

> Books in `books/_comingsoon/` inherit the same rules once they reach draft; add their
> `LANGUAGES.json` at that point.

## Pipeline

```
tools/extract_glossary.py books/<book>            # → <book>/GLOSSARY_PRESERVE.json
edit books/<book>/LANGUAGES.json                  # declare targets + directives
tools/translate_book.sh books/<book>              # → build/BOOK.<code>.md per language
tools/render_book.sh build/BOOK.<code>.md  "<out>"  "<Title>"  "<Author>"   # → EPUB + PDF
```

Body prose in every edition still renders in **Atkinson Hyperlegible** through the binding
render gate. Translation never bypasses the gate.

## Status

- **Pilot:** Resonance → `af`, `zu`, `es`, `fr` (in progress).
- Rollout to the rest of the catalog follows once the pilot editions are reviewed.
