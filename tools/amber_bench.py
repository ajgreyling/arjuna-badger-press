#!/usr/bin/env python3
"""Deterministic prose suite for Die Vuur in die Donker (Winter sonder Einde · Boek I).

Reuses the platform engine's LANGUAGE-NEUTRAL deterministic metrics against this book's merged
BOOK.md, plus the structural prose-tic shape counts (em-dash density, not-X-but-Y reframes, etc.)
reported RAW and ADVISORY — the engine's target bands are calibrated for the English African Gold
trilogy, so for an Afrikaans Norse saga the counts are a craft signal to read, not a pass/fail gate.

    python3 tools/amber_bench.py [path/to/BOOK.md]

Prints a scorecard. Exit 0 always (advisory). Pairs with the metered NovelBench LLM-judge run.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

PRESS = Path(__file__).resolve().parents[1]
PLATFORM = PRESS.parent / "arjuna-badger-platform"
DEFAULT_BOOK = PRESS / "books" / "the-amber-winter" / "build" / "BOOK.md"

# Make the engine's modules importable.
for p in (PLATFORM, PLATFORM / "novelbench"):
    if p.is_dir() and str(p) not in sys.path:
        sys.path.insert(0, str(p))


def main() -> int:
    book_md = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_BOOK
    if not book_md.is_file():
        print(f"amber_bench: BOOK.md not found: {book_md}", file=sys.stderr)
        return 1
    text = book_md.read_text(encoding="utf-8")
    words = len(text.split())

    print("=" * 78)
    print("DETERMINISTIC PROSE SUITE — Die Vuur in die Donker")
    print(f"  source: {book_md}   ({words:,} woorde)")
    print("=" * 78)

    # ---- NovelBench deterministic metrics (language-neutral) -----------------------------------
    try:
        from prose_metrics import analyze  # type: ignore
    except Exception as e:  # noqa: BLE001
        print(f"\n[prose_metrics] unavailable: {e}")
        analyze = None  # type: ignore

    if analyze is not None:
        m = analyze(text)
        print("\n── NovelBench deterministic metrics (language-neutral) ───────────────────────")
        raw = m["raw"]
        print("  RAW:")
        for k, v in raw.items():
            print(f"    {k:24} {v}")
        print("  SUB-SCORES (0-10, higher = better; curves are English-calibrated → directional):")
        for k, v in m["scores"].items():
            bar = "█" * int(round(float(v) / 10 * 24)) if isinstance(v, (int, float)) and v <= 10 else ""
            print(f"    {k:24} {v:>6}  {bar}")

    # ---- Deterministic prose-tic shape counts (raw / advisory) ---------------------------------
    print("\n── Structural prose-tic shapes (RAW, advisory — bands are English-tuned) ─────")
    try:
        from storygraph import prose_tics  # type: ignore
        # scan() resolves via the registry; we feed text directly through the TELLS table instead.
        tells = getattr(prose_tics, "TELLS", {})
        count = getattr(prose_tics, "_count")
        rows = {}
        for key, spec in tells.items():
            pat = spec.get("pat")
            try:
                rows[key] = pat(text) if callable(pat) else count(pat, text)
            except Exception:  # noqa: BLE001
                rows[key] = "n/a"
        per_10k = lambda n: round(n / max(1, words) * 10000, 1) if isinstance(n, int) else n
        for key, n in rows.items():
            print(f"    {key:28} {str(n):>6}   ({per_10k(n)} /10k woorde)")
    except Exception as e:  # noqa: BLE001
        print(f"    [prose_tics] could not run shape-counts directly: {e}")
        print("    (em-dash / reframe shape counts skipped — English-calibrated module)")

    print("\n── Notes ─────────────────────────────────────────────────────────────────────")
    print("  • Deterministic metrics are language-neutral and trustworthy as DIRECTIONAL signal.")
    print("  • Sub-score CURVES + tic TARGET BANDS are calibrated for the English African Gold")
    print("    trilogy; for this Afrikaans Norse saga read them as craft signals, not pass/fail.")
    print("  • The metered NovelBench LLM-judge (genre rubric) is the qualitative half — run")
    print("    separately; the judge reads Afrikaans natively.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
