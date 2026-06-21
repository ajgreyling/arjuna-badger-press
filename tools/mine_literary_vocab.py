#!/usr/bin/env python3
"""Mine candidate vocabulary from public-domain literary sources (human review required).

Reads source URLs documented in ``docs/corpus/LITERARY_SOURCES.md``, fetches PD text
(one title at a time), tokenises, and emits candidate phrase JSON for curator review.

**Does not** bulk-download all 78 sources or auto-merge into ``sa_urban_*.json``.
Approved candidates must be added by hand after spot-checking.

Usage:
    tools/mine_literary_vocab.py --lang af --source gutenberg --dry-run
    tools/mine_literary_vocab.py --lang sw --source wikisource --dry-run

Future (not implemented here):
    --output candidates/lit-af-kampstories.json
    --title kampstories   # pick one row from LITERARY_SOURCES
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LITERARY_SOURCES = REPO / "docs" / "corpus" / "LITERARY_SOURCES.md"

# One curated row per (--lang, --source) for the stub. URLs match LITERARY_SOURCES.md.
SOURCE_REGISTRY: dict[tuple[str, str], dict[str, str]] = {
    ("af", "gutenberg"): {
        "title": "Kampstories — C. Louis Leipoldt (1924)",
        "url": "https://www.gutenberg.org/ebooks/77225",
        "txt_url": "https://www.gutenberg.org/files/77225/77225-0.txt",
        "temp_min": "0.0",
        "temp_max": "0.4",
        "genre": "literary fiction",
    },
    ("sw", "wikisource"): {
        "title": "Swahili Tales — Edward Steere (1870)",
        "url": "https://wikisource.org/wiki/Swahili_Tales",
        "temp_min": "0.0",
        "temp_max": "0.5",
        "genre": "folktale fiction",
    },
}

# Hardcoded excerpt for offline ``--dry-run`` (PG Kampstories opening, PD).
DRY_RUN_SAMPLE: dict[tuple[str, str], str] = {
    ("af", "gutenberg"): (
        "Die son het skaars opgekom toe Oom Gert sy perd voor die wa span. "
        "Die kamp was stil; net die wind fluister tussen die bossies. "
        "Hy roep: Kom hier, jong man, ons moet die vuur aansteek voor die nag val. "
        "Die veld ruik na droë gras en stof. Ons sit rondom die kole en vertel stories "
        "van leeus en wilde diere. Die kinders luister met wye oë terwyl die koffie pruttel."
    ),
}

WORD_RE = re.compile(r"[A-Za-zÀ-ÿ]{3,}", re.UNICODE)
PHRASE_RE = re.compile(
    r"\b([A-Za-zÀ-ÿ]{3,}(?:\s+[A-Za-zÀ-ÿ]{3,}){1,2})\b", re.UNICODE
)


def _nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text.strip())


def _parse_literary_sources_url(lang: str, source: str) -> str | None:
    """Best-effort: find first https URL on a table row mentioning the source key."""
    if not LITERARY_SOURCES.is_file():
        return None
    body = LITERARY_SOURCES.read_text(encoding="utf-8")
    section = {
        "af": "## Afrikaans (af)",
        "zu": "## isiZulu (zu)",
        "xh": "## isiXhosa (xh)",
        "tn": "## Setswana (tn)",
        "st": "## Sesotho (st)",
        "sw": "## Swahili / Kiswahili (sw)",
    }.get(lang)
    if not section:
        return None
    start = body.find(section)
    if start < 0:
        return None
    end = body.find("\n## ", start + 1)
    chunk = body[start:end] if end > 0 else body[start:]
    needle = {"gutenberg": "gutenberg.org", "wikisource": "wikisource.org"}.get(source, "")
    if not needle:
        return None
    for line in chunk.splitlines():
        if needle in line.lower():
            m = re.search(r"https://[^\s|)]+", line)
            if m:
                return m.group(0).rstrip(")")
    return None


def tokenize(text: str) -> tuple[list[str], list[str]]:
    seen: set[str] = set()
    words: list[str] = []
    for w in WORD_RE.findall(_nfc(text)):
        key = w.casefold()
        if key not in seen:
            seen.add(key)
            words.append(w)
    words.sort(key=str.casefold)
    phrases = sorted({p for p in PHRASE_RE.findall(_nfc(text))}, key=str.casefold)
    return words, phrases


def fetch_text(url: str, timeout: float = 20.0) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "ArjunaBadgerPress/1.0 literary-miner"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
    for enc in ("utf-8", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def build_candidates(
    lang: str,
    source: str,
    text: str,
    meta: dict[str, str],
    *,
    limit: int = 20,
) -> dict:
    words, phrases = tokenize(text)
    samples: list[dict] = []
    for token in words[: limit // 2]:
        samples.append(
            {
                "phrase": token,
                "kind": "token",
                "lang": lang,
                "source": source,
                "source_url": meta.get("url", ""),
                "temp_min": float(meta.get("temp_min", 0.0)),
                "temp_max": float(meta.get("temp_max", 0.5)),
                "review_status": "pending",
                "note": "Automated extraction; not merged into corpus",
            }
        )
    for phrase in phrases[: limit - len(samples)]:
        samples.append(
            {
                "phrase": phrase,
                "kind": "phrase",
                "lang": lang,
                "source": source,
                "source_url": meta.get("url", ""),
                "temp_min": float(meta.get("temp_min", 0.0)),
                "temp_max": float(meta.get("temp_max", 0.5)),
                "review_status": "pending",
                "note": "Automated extraction; not merged into corpus",
            }
        )
    return {
        "lang": lang,
        "source": source,
        "title": meta.get("title", ""),
        "source_url": meta.get("url", ""),
        "dry_run": True,
        "candidate_count": len(samples),
        "candidates": samples,
        "disclaimer": (
            "Curator must approve before any entry is added to sa_urban_*.json or literary_*.json"
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Mine literary vocabulary candidates (review required)")
    parser.add_argument("--lang", required=True, choices=["af", "zu", "xh", "tn", "st", "sw"])
    parser.add_argument("--source", required=True, choices=["gutenberg", "wikisource"])
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Offline demo: hardcoded sample excerpt, no network fetch",
    )
    parser.add_argument("--limit", type=int, default=20, help="Max sample candidates (default 20)")
    args = parser.parse_args(argv)

    key = (args.lang, args.source)
    meta = dict(SOURCE_REGISTRY.get(key, {}))
    if not meta:
        print(f"No stub source registered for lang={args.lang!r} source={args.source!r}", file=sys.stderr)
        print("See LITERARY_SOURCES.md and extend SOURCE_REGISTRY.", file=sys.stderr)
        return 2

    doc_url = _parse_literary_sources_url(args.lang, args.source)
    if doc_url and not meta.get("url"):
        meta["url"] = doc_url

    if args.dry_run:
        sample = DRY_RUN_SAMPLE.get(key)
        if not sample:
            print(f"No dry-run sample for {key}; add to DRY_RUN_SAMPLE.", file=sys.stderr)
            return 2
        text = sample
        meta["fetch"] = "hardcoded_sample"
    else:
        txt_url = meta.get("txt_url") or meta.get("url")
        if not txt_url:
            print("No fetch URL; use --dry-run or extend SOURCE_REGISTRY.", file=sys.stderr)
            return 2
        try:
            text = fetch_text(txt_url)
            meta["fetch"] = txt_url
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            print(f"Fetch blocked or failed ({exc}); retry with --dry-run.", file=sys.stderr)
            return 1

    payload = build_candidates(args.lang, args.source, text, meta, limit=args.limit)
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
