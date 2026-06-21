# Fix a translation — community corrections

*How first-language speakers help fix AI colloquialisms on translated editions. Internal planning
doc; the public surface is `/fix-translation.html`.*

## People's Language (in progress)

Accepted fixes from this programme feed the **People's Language** corpus (working title for Real
Language + SA regional translation). See [`PEOPLES_LANGUAGE.md`](PEOPLES_LANGUAGE.md) for taglines,
status, and links to the API doc and evaluation fixture.

## Why

Parallel editions are machine-translated under the faithfulness rules in [`TRANSLATIONS.md`](../TRANSLATIONS.md).
Idiom, register, and colloquial speech still need a human ear — especially from someone who lives
inside the language. This programme invites that help without pretending every suggestion will land.

## The constraint (same as feedback)

The public site is static. Submissions resolve to:

1. **A hosted form** (Google Forms / Tally) whose responses land in a sheet the press reads. *Primary.*
2. **`mailto:j@`** with a pre-filled subject — always works, zero setup. *Fallback.*

Configure with `ABP_TRANSLATION_FIX_FORM_URL`. Optional field ids:

| Env | Default | Pre-fills |
|---|---|---|
| `ABP_TRANSLATION_FIX_BOOK_PARAM` | `entry.book` | Which book |
| `ABP_TRANSLATION_FIX_LANG_PARAM` | `entry.lang` | Language (code or name) |
| `ABP_TRANSLATION_FIX_LIVE` | `1` | Toggle page + nav + per-book links |

## What gets built

- `/fix-translation.html` — programme page: submit, terms, accepted log, top contributors
- Nav link **Fix a translation** (when live)
- Per-book **Other languages** note + respond link when the book has translated editions
- `/feedback.html` branch pointing here (distinct from general feedback and the bounty)
- `docs/translation_fixes.json` — SSOT for accepted fixes + top contributors (edited by hand, rendered on rebuild)

## Acceptance & credit

When a fix is accepted:

1. Add an entry to `translation_fixes.json` → `accepted[]` with `weight: 100` (human default — always outranks AI)
2. Rebuild the site — the fix appears on `/fix-translation.html`
3. **Real Language API** picks it up automatically (corpus mtime reload) — exact matches skip LLM entirely
4. Fold the correction into the next edition re-export; credit the contributor in the book's translation acknowledgements

### Corpus entry fields

| Field | Required | Notes |
|---|---|---|
| `original` | yes | Wrong phrase as published or sent |
| `fix` | yes | Human-approved replacement — **binding** in Real Language |
| `lang` | yes | Target language code (`af`, `zu`, …) |
| `source_lang` | for translate | Source language; omit for register-only fixes |
| `kind` | no | `translate` or `register` |
| `temp_min` / `temp_max` | no | Register band (default 0–1) |
| `weight` | no | Default **100** — outweighs any AI response |
| `contributor` | no | Credit name |

Top contributors per language (`top_contributors`) are named on the page. The leading voices in each
language receive a **printed copy of any Arjuna Badger Press book they choose, in the language they
helped fix**, sent free — one per calendar year per language, at the press's discretion.

## Terms (shown on the public page)

By submitting, contributors agree that:

- Their suggested wording may be **published in the book and on the site**, with credit, if accepted
- Accepted wording may be **licensed for income** (sales, print, audio) like any other part of the edition
- **Not every submission will be accepted** — editorial judgement applies; silence is not rejection of the person

Entry is free. We never ask for money.

## Shipped

- **2026-06-20** — `/fix-translation.html`, nav link, per-book + feedback funnel links, `translation_fixes.json` log in `site/build.py`

## Local Ollama RAG (optional)

SA urban corpus files in [`docs/corpus/`](corpus/) (`sa_urban_*.json`) use the same `corrections[]` /
`accepted[]` schema as `translation_fixes.json`. For local Ollama ingestion, chunk each entry as
`original → fix` with metadata (`lang`, `kind`, `temp_min`, `temp_max`, `weight`, `source_url`) and
embed for retrieval alongside the Real Language API path (`REAL_LANGUAGE_CORPUS_DIR`). Weight 100
entries remain binding overrides; lower-weight or retrieved chunks guide generation only.

## Corpus expansion (2026-06-20)

Phase order for SA languages + Swahili corpus scale-up (target 150–250+ entries each, modelled on Afrikaans ~308):

| Phase | Language | File | Before | After |
|---|---|---|---|---|
| 0 (done) | Afrikaans (`af`) | `sa_urban_af.json` | 308 | 308 |
| 1 | isiZulu (`zu`) | `sa_urban_zu.json` | 37 | 290 |
| 2 | isiXhosa (`xh`) | `sa_urban_xh.json` | 32 | 284 |
| 3 | Setswana (`tn`) | `sa_urban_tn.json` | 32 | 282 |
| 4 | Sesotho (`st`) | `sa_urban_st.json` | 11 | 282 |
| 5 | Swahili (`sw`) | `sa_urban_sw.json` | 20 | 302 |

Rebuild with `python3 tools/build_sa_urban_corpus.py` after editing `tools/sa_corpus_lang_tables.py`.
Categories per language: automotive/garage/taxi culture, urban street register, register anti-patterns (overlay pass), handbook section headings at temp ≥ 0.75.

## Literary sources (corpus expansion)

PD and openly licensed fiction/word-list research lives in [`corpus/LITERARY_SOURCES.md`](corpus/LITERARY_SOURCES.md) (78 named sources, ingestion plan, license flags). Mine candidates with `tools/mine_literary_vocab.py --dry-run`; human review before any merge into `sa_urban_*.json`.
