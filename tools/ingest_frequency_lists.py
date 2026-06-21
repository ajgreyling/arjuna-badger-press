#!/usr/bin/env python3
"""Ingest open frequency ladders into People's Language corpus (weight 20).

Reads checked-in lists under docs/corpus/frequency/, merges into sa_urban_*.json.
English lists produce en→lang translate rows; native lists produce register rows
(with optional en gloss when known). Does not promote to weight 100.

Usage:
    python3 tools/ingest_frequency_lists.py --prepare-sources   # normalize raw downloads
    python3 tools/ingest_frequency_lists.py --lang zu --tier 1000 --dry-run
    python3 tools/ingest_frequency_lists.py --all               # merge all langs/tiers
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CORPUS_DIR = REPO / "docs" / "corpus"
FREQ_DIR = CORPUS_DIR / "frequency"
CACHE_PATH = CORPUS_DIR / "frequency_translations.json"

FREQ_WEIGHT = 20
FREQ_CONTRIBUTOR = "frequency-ladder"
FREQ_TEMP = (0.0, 0.64)  # prompt seed only; excluded from overlay at urban temps (>= 0.65)

# Import curated en→lang tables from legacy seed tool
sys.path.insert(0, str(REPO / "tools"))
from en_frequency_1000 import CURATED, FREQ_LANGS  # noqa: E402
from sa_corpus_lang_tables import LANG_TABLES  # noqa: E402

# ---------------------------------------------------------------------------
# Ladder metadata (sources, licenses, max tiers)
# ---------------------------------------------------------------------------

LADDER: dict[str, list[dict]] = {
    "en": [
        {
            "tier": 10000,
            "file": "en_frequency.txt",
            "mode": "en_source",
            "source_url": "https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/English/Wikipedia_(2016)",
            "license": "CC BY-4.0 (Leipzig/Wiktionary); checked-in slice matches Google 10k ordering",
            "notes": "Primary en ladder to 10k. Wiktionary Wikipedia 2016 lists 1-10000+; we check in google-10000-english.txt (same practical tier).",
        },
    ],
    "af": [
        {
            "tier": 5050,
            "file": "af_frequency.txt",
            "mode": "native",
            "source_url": "https://github.com/frekwencja/most-common-words-multilingual/blob/main/data/wordfrequency.info/af.txt",
            "license": "wordfrequency.info / Google Translate corpus (see repo LICENSE)",
            "notes": "Native Afrikaans ~5050. Wiktionary has no dedicated Afrikaans frequency page; Leipzig CC BY-4.0 corpora available at wortschatz.uni-leipzig.de.",
        },
        {
            "tier": 2532,
            "file": "af_frequency_dohliam.txt",
            "mode": "native",
            "source_url": "https://github.com/dohliam/more-stoplists/blob/master/af/af_frequency_list.txt",
            "license": "Corpus-derived (dohliam/more-stoplists)",
            "notes": "Afrikaans web corpus tier (~2532 types). Secondary native ladder.",
        },
        {
            "tier": 10000,
            "file": "en_frequency.txt",
            "mode": "en_translate",
            "source_url": "https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/English/Wikipedia_(2016)",
            "license": "CC BY-4.0 / Google 10k",
            "notes": "en→af translate seed where native list ends.",
        },
    ],
    "zu": [
        {
            "tier": 5050,
            "file": "zu_frequency.txt",
            "mode": "native",
            "source_url": "https://github.com/frekwencja/most-common-words-multilingual/blob/main/data/wordfrequency.info/zu.txt",
            "license": "wordfrequency.info",
            "notes": "Native isiZulu ~5050. No Wiktionary zu frequency subpage.",
        },
        {
            "tier": 10000,
            "file": "en_frequency.txt",
            "mode": "en_translate",
            "source_url": "https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/English/Wikipedia_(2016)",
            "license": "CC BY-4.0 / Google 10k",
            "notes": "en→zu translate seed.",
        },
    ],
    "xh": [
        {
            "tier": 5050,
            "file": "xh_frequency.txt",
            "mode": "native",
            "source_url": "https://github.com/frekwencja/most-common-words-multilingual/blob/main/data/wordfrequency.info/xh.txt",
            "license": "wordfrequency.info",
            "notes": "Native isiXhosa ~5050.",
        },
        {
            "tier": 10000,
            "file": "en_frequency.txt",
            "mode": "en_translate",
            "source_url": "https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/English/Wikipedia_(2016)",
            "license": "CC BY-4.0 / Google 10k",
            "notes": "en→xh translate seed.",
        },
    ],
    "tn": [
        {
            "tier": 3000,
            "file": "tn_frequency.txt",
            "mode": "native",
            "source_url": "https://aclanthology.org/2024.rail-1.5/",
            "license": "Research list (Sibeko 2024); bootstrap from Leipzig tsn_web_2020_za when available",
            "notes": "Target 3000 from Sibeko Setswana readability list. Checked-in file computed from Leipzig tsn corpus or en-rank bootstrap until SADiLaR export is linked.",
        },
        {
            "tier": 10000,
            "file": "en_frequency.txt",
            "mode": "en_translate",
            "source_url": "https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/English/Wikipedia_(2016)",
            "license": "CC BY-4.0 / Google 10k",
            "notes": "en→tn translate seed (primary path to 10k; no open native 10k list found).",
        },
    ],
    "st": [
        {
            "tier": 5050,
            "file": "st_frequency.txt",
            "mode": "native",
            "source_url": "https://github.com/frekwencja/most-common-words-multilingual/blob/main/data/wordfrequency.info/st.txt",
            "license": "wordfrequency.info (cleaned)",
            "notes": "Native Sesotho ~5050 after English-artifact filter. Sibeko 2023 list (3037) at SADiLaR repo.sadilar.gov.",
        },
        {
            "tier": 975,
            "file": "st_frequency_dohliam.txt",
            "mode": "native",
            "source_url": "https://github.com/dohliam/more-stoplists/blob/master/st/st_frequency_list.txt",
            "license": "Folktale corpus (dohliam)",
            "notes": "Sesotho folktale frequency tier.",
        },
        {
            "tier": 10000,
            "file": "en_frequency.txt",
            "mode": "en_translate",
            "source_url": "https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/English/Wikipedia_(2016)",
            "license": "CC BY-4.0 / Google 10k",
            "notes": "en→st translate seed.",
        },
    ],
    "sw": [
        {
            "tier": 5050,
            "file": "sw_frequency.txt",
            "mode": "native",
            "source_url": "https://github.com/frekwencja/most-common-words-multilingual/blob/main/data/wordfrequency.info/sw.txt",
            "license": "wordfrequency.info",
            "notes": "Native Swahili ~5050.",
        },
        {
            "tier": 60000,
            "file": "sw_frequency_wiki.txt",
            "mode": "native",
            "ranked": False,
            "source_url": "https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Swahili/Wikipedia_2011",
            "license": "Leipzig CC BY-4.0 (2011 sw.wikipedia via Wiktionary)",
            "notes": "Wiktionary documents 60K sw.wikipedia types; checked-in open-dict wiki wordlist (~37K lemmas, alphabetized, not frequency-ranked). Ingest only at --tier 60000+.",
        },
        {
            "tier": 10000,
            "file": "en_frequency.txt",
            "mode": "en_translate",
            "source_url": "https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/English/Wikipedia_(2016)",
            "license": "CC BY-4.0 / Google 10k",
            "notes": "en→sw translate seed.",
        },
    ],
}

def _english_top500() -> frozenset[str]:
    path = FREQ_DIR / "en_frequency.txt"
    if not path.is_file():
        return frozenset()
    return frozenset(
        w.strip().lower() for w in path.read_text(encoding="utf-8").splitlines()[:500] if w.strip()
    )


def _parse_ranked_lines(text: str) -> list[tuple[int, str]]:
    rows: list[tuple[int, str]] = []
    for i, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "\t" in line:
            rank_s, word = line.split("\t", 1)
            try:
                rank = int(rank_s.strip())
            except ValueError:
                rank = len(rows) + 1
            word = word.strip()
        elif " " in line and line.split()[0].isdigit():
            rank_s, word = line.split(None, 1)
            rank = int(rank_s)
            word = word.strip()
        else:
            rank = len(rows) + 1
            word = line
        if word:
            rows.append((rank, word))
    return rows


def _parse_dohliam(text: str) -> list[tuple[int, str]]:
    rows: list[tuple[int, str]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) >= 2 and parts[0].isdigit():
            rows.append((int(parts[0]), " ".join(parts[1:])))
        else:
            rows.append((len(rows) + 1, line))
    return rows


def _parse_wordfrequency(text: str) -> list[tuple[int, str]]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if lines and lines[0] in ("af", "zu", "xh", "st", "sw", "en"):
        lines = lines[1:]
    return [(i, w) for i, w in enumerate(lines, 1)]


def load_frequency_file(path: Path) -> list[tuple[int, str]]:
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    name = path.name
    if "dohliam" in name or name.endswith("_dohliam.txt"):
        return _parse_dohliam(text)
    if "_wiki" in name:
        return [(i, w.strip()) for i, w in enumerate(text.splitlines(), 1) if w.strip()]
    if "\t" in text.splitlines()[0] if text.strip() else False:
        return _parse_ranked_lines(text)
    if name.startswith("en_") or "google" in name:
        return [(i, w.strip().lower()) for i, w in enumerate(text.splitlines(), 1) if w.strip()]
    return _parse_wordfrequency(text)


def slice_tier(rows: list[tuple[int, str]], tier: int) -> list[tuple[int, str]]:
    return [(r, w) for r, w in rows if r <= tier][:tier]


def best_rows_for_lang(lang: str, tier: int) -> tuple[list[tuple[int, str]], dict]:
    """Pick highest native/en_translate ladder rung not exceeding requested tier."""
    sources = LADDER.get(lang, [])
    chosen: list[tuple[int, str]] = []
    meta: dict = {}
    for src in sorted(sources, key=lambda s: s["tier"], reverse=True):
        if src["mode"] == "en_source":
            continue
        if src["tier"] > tier:
            continue
        path = FREQ_DIR / src["file"]
        rows = load_frequency_file(path)
        if not rows:
            continue
        cap = min(tier, src["tier"], len(rows))
        chosen = slice_tier(rows, cap)
        meta = src
        meta["ingested"] = len(chosen)
        meta["requested_tier"] = tier
        break
    if not chosen:
        for src in sources:
            if src["mode"] != "en_translate":
                continue
            path = FREQ_DIR / src["file"]
            rows = load_frequency_file(path)
            if rows:
                cap = min(tier, len(rows))
                chosen = slice_tier(rows, cap)
                meta = src
                meta["ingested"] = len(chosen)
                meta["requested_tier"] = tier
                break
    return chosen, meta


def reverse_gloss_maps() -> dict[str, dict[str, str]]:
    """native_word.lower() -> english gloss (best effort)."""
    out: dict[str, dict[str, str]] = {lang: {} for lang in FREQ_LANGS}
    for lang in FREQ_LANGS:
        rev: dict[str, str] = {}
        for en, native in CURATED.get(lang, {}).items():
            for token in re.split(r"[\s/,]+", native.lower()):
                token = token.strip("'-")
                if token and len(token) > 1:
                    rev.setdefault(token, en)
        for en, native in LANG_TABLES.get(lang, {}).items():
            if " " in en or " " not in native:
                continue
            for token in re.split(r"[\s/,]+", native.lower()):
                token = token.strip("'-")
                if token and token.isalpha() and len(token) > 2:
                    rev.setdefault(token, en.split()[0].lower())
        out[lang] = rev
    return out


def load_translation_cache() -> dict[str, dict[str, str]]:
    if CACHE_PATH.is_file():
        data = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        return data.get("languages", {})
    return {}


def corpus_path(lang: str) -> Path:
    return CORPUS_DIR / f"sa_urban_{lang}.json"


def load_corpus_entries(lang: str) -> tuple[list[dict], str]:
    path = corpus_path(lang)
    data = json.loads(path.read_text(encoding="utf-8"))
    key = "accepted" if lang == "sw" else "corrections"
    return list(data.get(key, [])), key


def existing_keys(entries: list[dict]) -> set[tuple[str, str]]:
    keys: set[tuple[str, str]] = set()
    for e in entries:
        kind = e.get("kind", "")
        orig = (e.get("original") or "").strip().lower()
        keys.add((kind, orig))
        eid = e.get("id") or ""
        if eid.startswith("freq-"):
            keys.add(("id", eid))
    return keys


def next_freq_id(lang: str, entries: list[dict], n: int) -> str:
    return f"freq-{lang}-{n:04d}"


def build_en_translate_entries(
    lang: str,
    words: list[str],
    translations: dict[str, str],
    source_url: str,
    seen: set[tuple[str, str]],
    start_n: int,
) -> tuple[list[dict], int]:
    entries: list[dict] = []
    n = start_n
    curated = CURATED.get(lang, {})
    for word in words:
        w = word.strip().lower()
        if not w or not w.replace("-", "").replace("'", "").isalpha():
            continue
        key = ("translate", w)
        if key in seen:
            continue
        fix = translations.get(w) or curated.get(w)
        if not fix:
            continue
        n += 1
        eid = next_freq_id(lang, entries, n)
        while ("id", eid) in seen:
            n += 1
            eid = next_freq_id(lang, entries, n)
        row = {
            "id": eid,
            "source_lang": "en",
            "lang": lang,
            "kind": "translate",
            "original": w,
            "fix": fix,
            "temp_min": FREQ_TEMP[0],
            "temp_max": FREQ_TEMP[1],
            "weight": FREQ_WEIGHT,
            "source_url": source_url,
            "contributor": FREQ_CONTRIBUTOR,
        }
        entries.append(row)
        seen.add(key)
        seen.add(("id", eid))
    return entries, n


def build_native_entries(
    lang: str,
    ranked: list[tuple[int, str]],
    rev_gloss: dict[str, str],
    source_url: str,
    seen: set[tuple[str, str]],
    start_n: int,
) -> tuple[list[dict], int]:
    entries: list[dict] = []
    n = start_n
    for rank, word in ranked:
        w = word.strip()
        if not w:
            continue
        wl = w.lower()
        en_gloss = rev_gloss.get(wl)
        if en_gloss and ("translate", en_gloss) not in seen:
            n += 1
            eid = next_freq_id(lang, entries, n)
            row = {
                "id": eid,
                "source_lang": "en",
                "lang": lang,
                "kind": "translate",
                "original": en_gloss,
                "fix": w,
                "temp_min": FREQ_TEMP[0],
                "temp_max": FREQ_TEMP[1],
                "weight": FREQ_WEIGHT,
                "source_url": source_url,
                "contributor": FREQ_CONTRIBUTOR,
            }
            entries.append(row)
            seen.add(("translate", en_gloss))
            seen.add(("id", eid))
        # Native-only tokens without an English gloss are kept in frequency/*.txt
        # for reference but not inserted as register overlays (short tokens break overlay).
    return entries, n


def ingest_lang(lang: str, tier: int, *, dry_run: bool = False) -> dict:
    entries, corpus_key = load_corpus_entries(lang)
    # Drop prior ladder rows so rebuild is idempotent
    entries = [
        e
        for e in entries
        if e.get("contributor") != FREQ_CONTRIBUTOR and not (e.get("id") or "").startswith(f"freq-{lang}-")
    ]
    seen = existing_keys(entries)
    before = len(entries)
    start_n = sum(1 for e in entries if (e.get("id") or "").startswith(f"freq-{lang}-"))

    rev = reverse_gloss_maps().get(lang, {})
    cache = load_translation_cache().get(lang, {})
    added_translate = 0
    added_register = 0
    metas: list[dict] = []

    for src in LADDER.get(lang, []):
        if src["mode"] == "en_source":
            continue
        if not src.get("ranked", True) and tier < src["tier"]:
            continue
        cap = min(tier, src["tier"])
        path = FREQ_DIR / src["file"]
        rows = load_frequency_file(path)
        if not rows:
            continue
        rows = slice_tier(rows, cap)
        if not rows:
            continue

        if src["mode"] == "en_translate":
            words = [w for _, w in rows]
            new_entries, start_n = build_en_translate_entries(
                lang, words, cache, src["source_url"], seen, start_n
            )
            added_translate += len(new_entries)
            if not dry_run:
                entries.extend(new_entries)
            metas.append({**src, "ingested": len(new_entries), "kind": "translate"})
        elif src["mode"] == "native":
            new_entries, start_n = build_native_entries(
                lang, rows, rev, src["source_url"], seen, start_n
            )
            reg = sum(1 for e in new_entries if e["kind"] == "register")
            tr = len(new_entries) - reg
            added_register += reg
            added_translate += tr
            if not dry_run:
                entries.extend(new_entries)
            metas.append({**src, "ingested": len(new_entries), "kind": "native"})

    if not dry_run:
        path = corpus_path(lang)
        data = json.loads(path.read_text(encoding="utf-8"))
        data[corpus_key] = entries
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return {
        "lang": lang,
        "tier": tier,
        "before": before,
        "after": before + added_translate + added_register,
        "added_translate": added_translate,
        "added_register": added_register,
        "sources": metas,
        "dry_run": dry_run,
    }


def _clean_st_wordfrequency(rows: list[tuple[int, str]]) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    for _, w in rows:
        wl = w.lower().strip()
        if wl in _english_top500() and " " not in wl and wl.isascii():
            continue
        if wl in ("the", "be", "of", "and", "to", "a", "in", "for", "is", "on"):
            continue
        out.append((len(out) + 1, w))
    return out


def _bootstrap_tn_from_en(en_rows: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """Build Setswana native rank list from en frequency + known tn glosses."""
    en_to_tn: dict[str, str] = dict(CURATED.get("tn", {}))
    for en, fix in LANG_TABLES.get("tn", {}).items():
        if " " not in en.strip():
            en_to_tn.setdefault(en.strip().lower(), fix)
    ranked: list[tuple[int, str]] = []
    seen: set[str] = set()
    for _rank, en in en_rows:
        fix = en_to_tn.get(en.lower())
        if not fix:
            continue
        for token in re.split(r"[\s/,]+", fix):
            token = token.strip()
            if not token or token.lower() in seen:
                continue
            seen.add(token.lower())
            ranked.append((len(ranked) + 1, token))
    return ranked


def prepare_sources() -> None:
    """Normalize raw downloads into ranked frequency/ files."""
    FREQ_DIR.mkdir(parents=True, exist_ok=True)

    # en 10k already at en_frequency.txt
    en_path = FREQ_DIR / "en_frequency.txt"
    if not en_path.is_file():
        raise SystemExit(f"Missing {en_path}")

    mappings = {
        "af": ("_raw_af.txt", "af_frequency.txt", _parse_wordfrequency),
        "zu": ("_raw_zu.txt", "zu_frequency.txt", _parse_wordfrequency),
        "xh": ("_raw_xh.txt", "xh_frequency.txt", _parse_wordfrequency),
        "sw": ("_raw_sw.txt", "sw_frequency.txt", _parse_wordfrequency),
    }
    for lang, (raw, out, parser) in mappings.items():
        raw_path = FREQ_DIR / raw
        if raw_path.is_file():
            rows = parser(raw_path.read_text(encoding="utf-8"))
            _write_ranked(FREQ_DIR / out, rows)
            print(f"  {out}: {len(rows)} words")

    # st: clean wordfrequency
    st_raw = FREQ_DIR / "_raw_st_wfi.txt"
    if st_raw.is_file():
        rows = _clean_st_wordfrequency(_parse_wordfrequency(st_raw.read_text(encoding="utf-8")))
        _write_ranked(FREQ_DIR / "st_frequency.txt", rows)
        print(f"  st_frequency.txt: {len(rows)} words (cleaned)")

    st_doh = FREQ_DIR / "_raw_st_dohliam.txt"
    if st_doh.is_file():
        rows = _parse_dohliam(st_doh.read_text(encoding="utf-8"))
        _write_ranked(FREQ_DIR / "st_frequency_dohliam.txt", rows)
        print(f"  st_frequency_dohliam.txt: {len(rows)} words")

    af_doh = FREQ_DIR / "_raw_af_dohliam.txt"
    if af_doh.is_file():
        rows = _parse_dohliam(af_doh.read_text(encoding="utf-8"))
        _write_ranked(FREQ_DIR / "af_frequency_dohliam.txt", rows)
        print(f"  af_frequency_dohliam.txt: {len(rows)} words")

    sw_wiki = FREQ_DIR / "_raw_sw_wiki.txt"
    if sw_wiki.is_file():
        rows = [(i, w.strip()) for i, w in enumerate(sw_wiki.read_text(encoding="utf-8").splitlines(), 1) if w.strip()]
        _write_ranked(FREQ_DIR / "sw_frequency_wiki.txt", rows)
        print(f"  sw_frequency_wiki.txt: {len(rows)} words")

    # tn bootstrap
    en_rows = load_frequency_file(en_path)
    tn_rows = _bootstrap_tn_from_en(en_rows)
    if tn_rows:
        _write_ranked(FREQ_DIR / "tn_frequency.txt", tn_rows)
        print(f"  tn_frequency.txt: {len(tn_rows)} words (en-rank bootstrap from curated; replace with Leipzig/SADiLaR when available)")

    ladder_meta = {
        "languages": {
            lang: [{"tier": s["tier"], "file": s["file"], "mode": s["mode"], "source_url": s["source_url"]} for s in srcs]
            for lang, srcs in LADDER.items()
        }
    }
    (FREQ_DIR / "ladder.json").write_text(json.dumps(ladder_meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {FREQ_DIR / 'ladder.json'}")


def _write_ranked(path: Path, rows: list[tuple[int, str]]) -> None:
    lines = [f"{rank}\t{word}" for rank, word in rows]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def ladder_summary() -> list[dict]:
    rows: list[dict] = []
    for lang in ["en", *FREQ_LANGS]:
        for src in LADDER.get(lang, []):
            path = FREQ_DIR / src["file"]
            available = len(load_frequency_file(path)) if path.is_file() else 0
            rows.append(
                {
                    "lang": lang,
                    "mode": src["mode"],
                    "tier": src["tier"],
                    "file": src["file"],
                    "available": available,
                    "source_url": src["source_url"],
                }
            )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest frequency ladder into sa_urban corpus")
    parser.add_argument("--prepare-sources", action="store_true", help="Normalize raw files in frequency/")
    parser.add_argument("--lang", choices=[*FREQ_LANGS], help="Single target language")
    parser.add_argument("--tier", type=int, default=10000, help="Max ladder tier to ingest (default 10000)")
    parser.add_argument("--all", action="store_true", help="Ingest all languages at --tier")
    parser.add_argument("--dry-run", action="store_true", help="Count only, do not write corpus")
    parser.add_argument("--summary", action="store_true", help="Print ladder table and exit")
    args = parser.parse_args()

    if args.prepare_sources:
        print("Preparing frequency source files...")
        prepare_sources()
        return 0

    if args.summary:
        for row in ladder_summary():
            print(
                f"{row['lang']:3} {row['mode']:14} tier={row['tier']:5} "
                f"avail={row['available']:5} {row['file']}"
            )
        return 0

    langs = [args.lang] if args.lang else (list(FREQ_LANGS) if args.all else [])
    if not langs:
        parser.error("Specify --lang, --all, --prepare-sources, or --summary")

    for lang in langs:
        stats = ingest_lang(lang, args.tier, dry_run=args.dry_run)
        print(
            f"{lang}: +{stats['added_translate']} translate, +{stats['added_register']} register "
            f"({stats['before']} -> {stats['after']})"
            + (" [dry-run]" if args.dry_run else "")
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
