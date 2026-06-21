#!/usr/bin/env python3
"""Build SA urban + Swahili correction corpus JSON from Afrikaans template + lang data.

Rebuilds base corpus from lang tables, then ingests frequency-ladder rows (~2k/lang)
via ingest_frequency_lists so freq-* ids persist in one command.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CORPUS_DIR = REPO / "docs" / "corpus"
AF_PATH = CORPUS_DIR / "sa_urban_af.json"
TOOLS = REPO / "tools"

sys.path.insert(0, str(TOOLS))
from en_frequency_1000 import FREQ_LANGS  # noqa: E402
from ingest_frequency_lists import ingest_lang  # noqa: E402
from sa_corpus_lang_tables import LANG_TABLES, LANG_REGISTER, SW_EXTRA, SW_SEED, ZU_LITERARY  # noqa: E402

DEFAULT_INGEST_TIER = 10000

LITERARY_BY_LANG: dict[str, list[dict]] = {
    "zu": ZU_LITERARY,
}

def _entry(
    eid: str,
    lang: str,
    kind: str,
    original: str,
    fix: str,
    *,
    source_lang: str | None = None,
    temp_min: float = 0.65,
    temp_max: float = 1.0,
    weight: int = 100,
    source_url: str = "https://en.wikipedia.org/wiki/South_African_English",
    contributor: str = "Arjuna Badger Press corpus expansion",
) -> dict:
    if kind == "register":
        source_lang = lang
    elif source_lang is None:
        source_lang = "en"
    return {
        "id": eid,
        "source_lang": source_lang,
        "lang": lang,
        "kind": kind,
        "original": original,
        "fix": fix,
        "temp_min": temp_min,
        "temp_max": temp_max,
        "weight": weight,
        "source_url": source_url,
        "contributor": contributor,
    }


def _contributor_for(af_entry: dict) -> str:
    return af_entry.get("contributor") or "Arjuna Badger Press corpus expansion"


def _source_url_for(af_entry: dict) -> str:
    return af_entry.get("source_url") or "https://en.wikipedia.org/wiki/South_African_English"


def build_lang(lang: str, prefix: str, table: dict[str, str], register: list[dict]) -> list[dict]:
    af = json.loads(AF_PATH.read_text(encoding="utf-8"))["corrections"]
    entries: list[dict] = []
    seen_originals: set[tuple[str, str]] = set()
    n = 0

    for af_e in af:
        original = af_e["original"]
        kind = af_e["kind"]
        key = (kind, original)
        if key in seen_originals:
            continue

        if kind == "translate":
            fix = table.get(original)
            if not fix:
                continue
            n += 1
            entries.append(
                _entry(
                    f"sa-{prefix}-{n:03d}",
                    lang,
                    "translate",
                    original,
                    fix,
                    temp_min=af_e.get("temp_min", 0.65),
                    temp_max=af_e.get("temp_max", 1.0),
                    source_url=_source_url_for(af_e),
                    contributor=_contributor_for(af_e),
                )
            )
            seen_originals.add(key)
        elif kind == "register" and lang != "sw":
            pass

    for reg in register:
        n += 1
        kw = {k: reg[k] for k in ("temp_min", "temp_max", "source_url", "contributor", "weight") if k in reg}
        entries.append(
            _entry(
                f"sa-{prefix}-{n:03d}",
                lang,
                "register",
                reg["original"],
                reg["fix"],
                **kw,
            )
        )

    for extra in LITERARY_BY_LANG.get(lang, []):
        original = extra["original"]
        key = ("translate", original)
        if key in seen_originals:
            continue
        n += 1
        kw = {k: extra[k] for k in ("temp_min", "temp_max", "source_url", "contributor", "weight") if k in extra}
        entries.append(
            _entry(
                f"sa-{prefix}-{n:03d}",
                lang,
                "translate",
                original,
                extra["fix"],
                **kw,
            )
        )
        seen_originals.add(key)

    return entries


def build_sw() -> dict:
    af = json.loads(AF_PATH.read_text(encoding="utf-8"))["corrections"]
    table = LANG_TABLES["sw"]
    register = LANG_REGISTER.get("sw", [])
    entries: list[dict] = []
    seen: set[tuple[str, str]] = set()
    n = 0

    def _add(kind: str, original: str, fix: str, **kw) -> None:
        nonlocal n
        key = (kind, original)
        if key in seen:
            return
        n += 1
        entries.append(_entry(f"sa-sw-{n:03d}", "sw", kind, original, fix, **kw))
        seen.add(key)

    for seed in SW_SEED:
        kw = {k: seed[k] for k in ("temp_min", "temp_max", "source_url", "contributor", "weight") if k in seed}
        _add("translate", seed["original"], seed["fix"], **kw)

    for af_e in af:
        if af_e["kind"] != "translate":
            continue
        original = af_e["original"]
        fix = table.get(original)
        if not fix:
            continue
        _add(
            "translate",
            original,
            fix,
            temp_min=af_e.get("temp_min", 0.65),
            temp_max=af_e.get("temp_max", 1.0),
            source_url=_source_url_for(af_e),
            contributor=_contributor_for(af_e),
        )

    for extra in SW_EXTRA:
        kw = {k: extra[k] for k in ("temp_min", "temp_max", "source_url", "contributor", "weight") if k in extra}
        _add("translate", extra["original"], extra["fix"], **kw)

    for reg in register:
        kw = {k: reg[k] for k in ("temp_min", "temp_max", "source_url", "contributor", "weight") if k in reg}
        _add("register", reg["original"], reg["fix"], **kw)

    return {
        "_schema": "East/Southern African Swahili colloquialisms — up-Africa register for HBT. temp 0.5 default in LANGUAGES.json.",
        "accepted": entries,
    }


def _strip_freq_rows(entries: list[dict], lang: str) -> list[dict]:
    """Remove prior frequency rows so base rebuild is idempotent."""
    return [
        e
        for e in entries
        if e.get("contributor") not in ("auto-frequency-seed", "frequency-ladder")
        and not (e.get("id") or "").startswith(f"freq-{lang}-")
    ]


def _ingest_frequency_ladders(*, tier: int = DEFAULT_INGEST_TIER) -> None:
    print(f"Ingesting frequency ladders (tier {tier})...")
    for lang in FREQ_LANGS:
        stats = ingest_lang(lang, tier, dry_run=False)
        print(
            f"  {lang}: +{stats['added_translate']} translate, +{stats['added_register']} register "
            f"({stats['before']} -> {stats['after']})"
        )


def main() -> None:
    af_data = json.loads(AF_PATH.read_text(encoding="utf-8"))
    af_entries = _strip_freq_rows(list(af_data.get("corrections", [])), "af")
    af_data["corrections"] = af_entries
    AF_PATH.write_text(json.dumps(af_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {AF_PATH.name}: {len(af_entries)} base entries")

    configs = [
        ("zu", "zu", "corrections"),
        ("xh", "xh", "corrections"),
        ("tn", "tn", "corrections"),
        ("st", "st", "corrections"),
    ]
    for lang, prefix, key in configs:
        entries = build_lang(lang, prefix, LANG_TABLES[lang], LANG_REGISTER.get(lang, []))
        out = {key: entries}
        path = CORPUS_DIR / f"sa_urban_{lang}.json"
        path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {path.name}: {len(entries)} base entries")

    sw_out = build_sw()
    sw_path = CORPUS_DIR / "sa_urban_sw.json"
    sw_path.write_text(json.dumps(sw_out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {sw_path.name}: {len(sw_out['accepted'])} base entries")

    _ingest_frequency_ladders()


if __name__ == "__main__":
    main()
