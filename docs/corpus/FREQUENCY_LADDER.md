# Frequency ladder (People's Language corpus)

Per-language vocabulary tiers from open frequency lists (Wiktionary, wordfrequency.info, Leipzig CC BY-4.0, ACL research). Lists are **checked in** under [`frequency/`](frequency/); ingest via `tools/ingest_frequency_lists.py`.

**Human review gate:** all ingested rows use `weight: 20`, `contributor: frequency-ladder`. Do **not** promote to `weight: 100` until a native speaker spot-checks the row.

## Ladder table (lang × source × count)

| Lang | Tier | Source | URL | License | Available | Ingested (tier 2k) | Ingested (tier 10k) | Notes |
|------|------|--------|-----|---------|-----------|-------------------|---------------------|-------|
| **en** | 10 000 | Google / Wiktionary English | [Wiktionary EN Wikipedia 2016](https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/English/Wikipedia_(2016)) · [google-10000-english](https://github.com/first20hours/google-10000-english) | Open frequency list | 10 000 | 10 000 (reference file) | 10 000 (reference file) | `frequency/en_frequency.txt` |
| **af** | 5 050 | wordfrequency.info | [frekwencja af.txt](https://github.com/frekwencja/most-common-words-multilingual/blob/main/data/wordfrequency.info/af.txt) | See repo LICENSE | 5 050 | ~168 translate* | ~168 translate* | Native list; en gloss via curated/cache only |
| **af** | 2 532 | dohliam web corpus | [more-stoplists af](https://github.com/dohliam/more-stoplists/blob/master/af/af_frequency_list.txt) | Corpus-derived | 2 532 | merged* | merged* | Secondary native tier |
| **af** | 10 000 | en→af translate seed | (en ladder) | — | 10 000 | **1 987** | 1 987‡ | `frequency_translations.json` filled to tier 2k (2025-06-20) |
| **zu** | 5 050 | wordfrequency.info | [zu.txt](https://github.com/frekwencja/most-common-words-multilingual/blob/main/data/wordfrequency.info/zu.txt) | See repo | 5 050 | ~168 translate* | ~168 translate* | No Wiktionary zu frequency subpage |
| **zu** | 10 000 | en→zu | en ladder | — | 10 000 | **1 988** | 1 988‡ | |
| **xh** | 5 050 | wordfrequency.info | [xh.txt](https://github.com/frekwencja/most-common-words-multilingual/blob/main/data/wordfrequency.info/xh.txt) | See repo | 5 050 | ~116 translate* | ~116 translate* | |
| **xh** | 10 000 | en→xh | en ladder | — | 10 000 | **1 985** | 1 985‡ | |
| **tn** | 3 000 | Sibeko 2024 (target) | [ACL RAIL 2024](https://aclanthology.org/2024.rail-1.5/) | Research | 3 000 (paper) | **167 bootstrap** | **167 bootstrap** | Leipzig `tsn_web_2020_za` still times out; native list is en-rank bootstrap only |
| **tn** | 10 000 | en→tn | en ladder | — | 10 000 | **1 985** | 1 985‡ | **No open native 10k**; en-translate path is primary to 10k |
| **st** | 5 028 | wordfrequency.info (cleaned) | [st.txt](https://github.com/frekwencja/most-common-words-multilingual/blob/main/data/wordfrequency.info/st.txt) | See repo | 5 028 | ~116 translate* | ~116 translate* | English artifacts stripped |
| **st** | 975 | dohliam folktale | [st_frequency_list](https://github.com/dohliam/more-stoplists/blob/master/st/st_frequency_list.txt) | Folktale corpus | 975 | merged* | merged* | |
| **st** | 3 037 | Sibeko 2023 (target) | [ACL RAIL 2023](https://aclanthology.org/2023.rail-1.5/) · [SADiLaR](https://repo.sadilar.gov) | Research | 3 037 | not yet checked in | not yet checked in | Sesotho readability list |
| **st** | 10 000 | en→st | en ladder | — | 10 000 | **1 985** | 1 985‡ | |
| **sw** | 5 050 | wordfrequency.info | [sw.txt](https://github.com/frekwencja/most-common-words-multilingual/blob/main/data/wordfrequency.info/sw.txt) | See repo | 5 050 | ~112 translate* | ~112 translate* | |
| **sw** | 60 000 | Wiktionary sw.wikipedia 2011 | [Frequency lists/Swahili](https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Swahili) · [Wikipedia 2011](https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Swahili/Wikipedia_2011) | Leipzig CC BY-4.0 | 60 000 (Wiktionary) | 37 758† | 37 758† | Checked-in wiki wordlist is alphabetized, not ranked; ingest at `--tier 60000` only |
| **sw** | 10 000 | en→sw | en ladder | — | 10 000 | **1 980** | 1 980‡ | |

\*Before 2025-06-20 cache fill: ingested translate rows = curated/`frequency_translations.json` hits only (~168 af/zu, ~116 xh/tn/st, ~112 sw).

‡At tier 10 000 ingest, en→lang translate rows are capped by cache depth (~2 000 lemmas per lang as of 2025-06-20). Re-run `en_frequency_1000.py --write-cache --tier 10000` to extend.

†Reference file `sw_frequency_wiki.txt`; not ingested at default tier 10 000.

### Max native tier reached

| Lang | Max open native list | 10 000 native? |
|------|---------------------|----------------|
| af | 5 050 | No |
| zu | 5 050 | No |
| xh | 5 050 | No |
| tn | **167 bootstrap** (3 000 target from Sibeko 2024) | **No** |
| st | 5 028 (+ 3 037 research list pending) | No |
| sw | 5 050 (60 000 on Wiktionary; 37 758 wiki wordlist checked in) | No (ranked 60k not yet parsed) |

## Wiktionary index

- Master index: [Wiktionary:Frequency lists](https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists)
- English (10k+): [English/Wikipedia (2016)](https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/English/Wikipedia_(2016))
- Swahili (60k): [Frequency lists/Swahili](https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Swahili)
- Afrikaans: no dedicated Wiktionary frequency page; use [Leipzig Afrikaans](https://wortschatz.uni-leipzig.de/en/download/afr) (CC BY-4.0)
- Bantu SA langs: no Wiktionary frequency subpages; use wordfrequency.info + Leipzig + ACL/SADiLaR lists above

## Source files

| File | Format |
|------|--------|
| `frequency/en_frequency.txt` | `rank<TAB>word` or one word per line (10 000) |
| `frequency/{af,zu,xh,st,sw}_frequency.txt` | ranked native tokens |
| `frequency/tn_frequency.txt` | bootstrap until Leipzig/SADiLaR export |
| `frequency/ladder.json` | machine-readable tier metadata |
| `frequency_translations.json` | en→lang gloss cache (`languages.{lang}.{en_word}`); resume-safe |

## Translation cache (2025-06-20)

Anthropic batch fill via `tools/en_frequency_1000.py --write-cache --tier 2000` (everyday register, no Wiktionary by default). Cache depth:

| Lang | Cached lemmas | Corpus freq-ladder rows (tier 2k ingest) |
|------|---------------|------------------------------------------|
| af | 2 014 | 1 987 |
| zu | 2 000 | 1 988 |
| xh | 2 000 | 1 985 |
| tn | 2 000 | 1 985 |
| st | 2 000 | 1 985 |
| sw | 2 000 | 1 980 |

Corpus totals after ingest: ~2 269–2 295 entries per lang (base corpus + freq-ladder). Gap vs 2 000 en lemmas: non-alpha tokens skipped, dedupe against existing translate rows.

## Tooling

```bash
# Normalize raw downloads (_raw_*.txt) into ranked files
python3 tools/ingest_frequency_lists.py --prepare-sources

# Preview ingest
python3 tools/ingest_frequency_lists.py --lang zu --tier 1000 --dry-run

# Full merge (also invoked automatically at end of build_sa_urban_corpus.py)
python3 tools/ingest_frequency_lists.py --all --tier 10000

# Fill en→lang gaps (OPENROUTER_API_KEY or ANTHROPIC_API_KEY in arjuna-badger-platform/.env)
python3 tools/en_frequency_1000.py --write-cache --tier 2000
python3 tools/test_translate_corpus_offline.py
```

## Corpus row schema (frequency-ladder)

| Field | Value |
|-------|-------|
| `id` | `freq-{lang}-0001` … |
| `kind` | `translate` (en→lang or native with known en gloss) |
| `weight` | **20** |
| `contributor` | `frequency-ladder` |
| `temp_min` / `temp_max` | `0.0` / `0.64` (prompt seed; excluded from overlay at urban temps) |

Native tokens **without** an English gloss stay in `frequency/*.txt` only (not register overlays; short tokens break substring overlay).

## Build pipeline

```bash
python3 tools/build_sa_urban_corpus.py
python3 tools/test_translate_corpus_offline.py
```

`build_sa_urban_corpus.py` rebuilds base rows from lang tables, strips prior `freq-*` rows, then runs frequency-ladder ingest (`--all`, tier 10k) so one command restores ~2k ladder rows per lang.

## Moderation pipeline

LLM tri-judge moderation for the en→lang cache (`frequency_translations.json`). Three OpenRouter judges (same slots as `engine/llm_client.py`):

| Slot | Role | Default slug |
|------|------|--------------|
| `anthropic` | Translation quality | `anthropic/claude-opus-4` |
| `openai` | Structure / consistency | `openai/gpt-4.1` |
| `perplexity` | Grounding / regional usage | `perplexity/sonar-pro` |

Each en lemma + target lang is scored 1–10 on **accuracy**, **everyday_register**, **not_bible_formal**. Aggregate = mean of judge overalls; **approved** if aggregate ≥ threshold (default 6) and judge spread ≤ 2; **flagged** if below threshold or high disagreement; **rejected** if aggregate &lt; threshold − 1.

```bash
# Preview pilot (top 100 en lemmas × 6 langs = 600 pairs)
python3 tools/moderate_frequency_translations.py --dry-run --pilot

# Run pilot (requires OPENROUTER_API_KEY in arjuna-badger-platform/.env)
python3 tools/moderate_frequency_translations.py --pilot --resume

# Single lang sample
python3 tools/moderate_frequency_translations.py --lang zu --limit 50 --threshold 6

# Apply outcomes: flagged → moderation_queue.json; rejected removed → moderation_rejected.json
python3 tools/moderate_frequency_translations.py --pilot --apply

# Offline tests (mocked judges, no API)
python3 tools/test_moderate_frequency_translations.py
```

Outputs:

| File | Contents |
|------|----------|
| `frequency/moderation_scores.json` | Per-pair judge scores, notes, status |
| `frequency/moderation_queue.json` | Flagged entries for human review |
| `frequency/moderation_rejected.json` | Removed glosses + judge suggested fixes |

After `--apply` with rejections, rebuild corpus:

```bash
python3 tools/build_sa_urban_corpus.py
python3 tools/test_translate_corpus_offline.py
```

Full cache moderation (~12k pairs): run without `--pilot`, use `--resume` across sessions:

```bash
python3 tools/moderate_frequency_translations.py --tier 2000 --resume
```

## Human review

After review: set `weight` to 100, set `contributor` to reviewer name, narrow `temp_min`/`temp_max` if needed. Never bulk-promote frequency-ladder rows.
