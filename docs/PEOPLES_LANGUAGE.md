# People's Language — die mense se taal

**Status:** **in progress** — `car-handbook-test` fixture validated; press rollout pending human corpus
sign-off (AJ review + native-speaker lock on taglines).

AI translation into **everyday speech**: not textbook flatness, not machine gloss. This name folds the
**Real Language** API, corpus-first routing, register `temp`, and the SA regional batch pass under one
product label.

## What it is

| Layer | Role |
|---|---|
| **Corpus** | Human fixes (weight 100) outrank any model. Exact match skips LLM. |
| **Register temp** | 0 (formal) → 1 (street). Set per language in each book's `LANGUAGES.json`; same dial on the API. |
| **Post-AI overlay** | `correction_corpus.overlay_all()` binds human `fix` over wrong model output. |
| **Real Language API** | `POST /api/real-language` — live at [arjunabadger.press/real-language](https://arjunabadger.press/real-language). |
| **Batch pipeline** | `tools/translate_real.sh` / `run_translate_ab.sh` share the same router as the API. |
| **Fix a translation** | Community submissions feed `translation_fixes.json` and `docs/corpus/sa_urban_*.json`. |

Target languages for the current pass: `af`, `zu`, `xh`, `st`, `tn`, `sw`.

## Taglines

The feature is branded as translation into **the people's language**:

| Code | Language | Phrase |
|---|---|---|
| `af` | Afrikaans | die mense se taal |
| `zu` | isiZulu | ulimi lwabantu |
| `xh` | isiXhosa | ulwimi lwabantu |
| `tn` | Setswana | puo ya batho |
| `st` | Sesotho | puo ea batho |
| `sw` | Swahili | lugha ya watu |

Machine-readable copy: [`peoples_language_taglines.json`](peoples_language_taglines.json).

Afrikaans confirmed by editorial. Bantu-language phrases are attested equivalents of "language/tongue
of the people". Native-speaker sign-off still binding before public marketing lock.

## Receipts

| Receipt | Path |
|---|---|
| Binding brief (Misogi) | [`../../arjuna-badger-platform/docs/MISOGI.md`](../../arjuna-badger-platform/docs/MISOGI.md) § People's Language |
| Real Language API & routing | [`../../arjuna-badger-platform/docs/REAL_LANGUAGE.md`](../../arjuna-badger-platform/docs/REAL_LANGUAGE.md) |
| Fix a translation programme | [`FIX_TRANSLATION_PLAN.md`](FIX_TRANSLATION_PLAN.md) |
| Corpus router | [`../../arjuna-badger-platform/saas/correction_corpus.py`](../../arjuna-badger-platform/saas/correction_corpus.py) |
| SA urban corpus (~1,748 entries) | [`corpus/sa_urban_*.json`](corpus/) |
| English top-1000 frequency seed | [`corpus/FREQUENCY_SEED.md`](corpus/FREQUENCY_SEED.md) · [`corpus/en_frequency_1000.txt`](corpus/en_frequency_1000.txt) |
| Car handbook A/B fixture | [`../../../car-handbook-test/`](../../../car-handbook-test/) · [`../tools/test_translate_corpus_offline.py`](../tools/test_translate_corpus_offline.py) |
| Edition map & faithfulness rules | [`../TRANSLATIONS.md`](../TRANSLATIONS.md) |

## Evaluation

[`car-handbook-test/`](../../../car-handbook-test/) holds the car owner's handbook passage used to stress-test
register (headings, garage/taxi vocabulary, brake-pedal guards) across all six languages. Corpus entries
sourced from that fixture are tagged `car handbook` in `sa_urban_*.json`. Offline gate:
`python3 tools/test_translate_corpus_offline.py`.

## LLM gateway

All People's Language LLM calls (API, batch A/B, car-handbook fixture) route through
**OpenRouter** when `OPENROUTER_API_KEY` is set in `arjuna-badger-platform/.env`.
Logical provider names (`anthropic`, `openai`, `perplexity`) are unchanged at CLI and
API call sites; OpenRouter model slugs are configured per role:

| Logical provider | Env override | Default slug |
|---|---|---|
| `anthropic` | `OPENROUTER_MODEL_ANTHROPIC` | `anthropic/claude-opus-4` |
| `openai` | `OPENROUTER_MODEL_OPENAI` | `openai/gpt-4.1` |
| `perplexity` | `OPENROUTER_MODEL_PERPLEXITY` | `perplexity/sonar-pro` |

Set `LLM_BACKEND=direct` to use legacy vendor keys (`ANTHROPIC_API_KEY`, etc.) instead (local / batch only).

**Render (live API):** `OPENROUTER_API_KEY` only — see `arjuna-badger-platform/render.yaml`. No vendor keys on Render.

## Web UI

Live demo: [arjunabadger.press/real-language](https://arjunabadger.press/real-language) (Real Language page;
People's Language branding on that surface still in progress).
