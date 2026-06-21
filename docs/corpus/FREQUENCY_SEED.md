# English Top-1000 Frequency Seed (superseded)

**Superseded by [`FREQUENCY_LADDER.md`](FREQUENCY_LADDER.md)** and `tools/ingest_frequency_lists.py` (native ladders + en 10k).

Legacy notes below for `tools/en_frequency_1000.py` (translation cache fill only).

## English word list

| Item | Detail |
|---|---|
| **File** | [`en_frequency_1000.txt`](en_frequency_1000.txt) |
| **Source** | [Google 10,000 English](https://github.com/first20hours/google-10000-english) (top 1000 rows) |
| **License** | Public frequency list (web-corpus derived, no copyright on word ranks) |
| **Scope** | Full top 1000 by frequency, including function and content words |

## Translation method

1. **Curated seed** (~150 high-frequency lemmas per language) in `tools/en_frequency_1000.py` (`CURATED` dict).
2. **Wiktionary API** gloss lookup for single-word gaps.
3. **Anthropic batch fill** for remaining gaps (`--write-cache`), everyday register prompt (not Bible/textbook).
4. **Dedup** against existing `sa_urban_*.json` rows with the same `original` (urban/car-handbook entries win).

Cached translations: [`frequency_translations.json`](frequency_translations.json).

## Corpus row schema

| Field | Value |
|---|---|
| `id` | `freq-{lang}-001` … |
| `kind` | `translate` |
| `source_lang` | `en` |
| `temp_min` / `temp_max` | `0.0` / `1.0` (neutral, all register temps) |
| `weight` | **20** (auto-generated; not binding at 100) |
| `contributor` | `auto-frequency-seed` |
| `source_url` | Google 10k frequency list URL |

## Human review gate

**Do not promote to weight 100** until a native speaker or editor spot-checks the row.

Review focus: function words (`the`, `a`, …), polysemy, and urban vs standard register.

After review: bump `weight` to 100, set `contributor` to reviewer name, optionally narrow `temp_min`/`temp_max`.

## Build pipeline

```bash
# 1. Refresh translation cache (needs ANTHROPIC_API_KEY in arjuna-badger-platform/.env)
python3 tools/en_frequency_1000.py --write-cache

# 2. Rebuild all sa_urban_*.json (merges frequency rows, preserves existing originals)
python3 tools/build_sa_urban_corpus.py

# 3. Offline gate
python3 tools/test_translate_corpus_offline.py
```

Dry-run counts only:

```bash
python3 tools/en_frequency_1000.py --dry-run
```
