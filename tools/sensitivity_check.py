#!/usr/bin/env python3
"""Metered sensitivity-risk read for books depicting living/indigenous peoples.

A focused second opinion before revealing a book that carries a `sensitivity_read: REQUIRED`
flag (e.g. the Unheard shelf — Ainu, Khalkha herders). Reads the full manuscript + the book's
own sensitivity directives (project.json) and returns a risk verdict: is there anything a
reasonable cultural-sensitivity reader would flag as harmful, appropriative, or factually
disrespectful — sacred content shown, a people conflated with a neighbour, a tradition-holder
written as a foil, poverty-porn? This does NOT replace a human sensitivity read by someone of
the culture; it is a triage signal on whether the prose is clean enough to surface.

    export OPENAI_API_KEY=...
    python3 tools/sensitivity_check.py unheard-japan unheard-mongolia

Writes book-sensitivity-check.json. gpt-5 via OpenAI (Anthropic-direct out of credit).
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BOOKS = REPO / "books"
import importlib.util
spec = importlib.util.spec_from_file_location("abp_build", REPO / "site" / "build.py")
BUILD = importlib.util.module_from_spec(spec); spec.loader.exec_module(BUILD)
CURATED = {c[0]: c for c in BUILD.CURATED}

MODEL = "gpt-5"
MANUSCRIPT_CHARS = 400_000

SYSTEM = """You are a cultural-sensitivity triage reader for a fiction imprint. A book depicting a
living or indigenous people is about to be revealed publicly. You are NOT the final word — a human
reader of that culture is — but your job is to catch anything that should block or delay release.

You are given the book's own sensitivity DIRECTIVES (what its author committed to) and the full
manuscript. Judge whether the prose honours those directives and whether a reasonable
sensitivity reader of that culture would flag harm. Look specifically for:
- A people conflated with a neighbouring/different group (e.g. Khalkha Mongol vs Kazakh).
- Sacred/ceremonial content shown that the directives said to withhold.
- A culture's tradition-holder or expert written as a foil, comic relief, or inferior.
- Poverty-porn, savior narrative, or the outsider authoring the culture's meaning.
- Factual disrespect about real living practice.

Return ONLY a JSON object:
{
  "risk": "LOW" | "MEDIUM" | "HIGH",
  "directives_honoured": boolean,
  "flags": [ up to 5 short specific concerns, each with a chapter/scene cue if possible ],
  "blocking": boolean (true only if you'd hold release pending a human read),
  "one_line": one sentence verdict,
  "recommended_action": "SURFACE" | "SURFACE_WITH_NOTE" | "HOLD_FOR_HUMAN_READ"
}
Be honest but not performatively cautious: if the prose is careful and self-aware, say LOW/SURFACE."""


def manuscript(root: Path) -> str:
    bm = root / "build" / "BOOK.md"
    t = bm.read_text(encoding="utf-8", errors="ignore") if bm.is_file() else ""
    if len(t) <= MANUSCRIPT_CHARS:
        return t
    return t[:MANUSCRIPT_CHARS//2] + "\n\n[...MIDDLE OMITTED...]\n\n" + t[-MANUSCRIPT_CHARS//2:]


def directives(root: Path) -> str:
    pj = root / "project.json"
    if pj.is_file():
        try:
            d = json.loads(pj.read_text(encoding="utf-8"))
            return json.dumps({k: d[k] for k in ("status", "sensitivity_read", "title", "logline", "market")
                               if k in d}, indent=2)
        except Exception:
            pass
    # fall back to any SENSITIVITY/README note
    for name in ("SENSITIVITY.md", "README.md"):
        p = root / name
        if p.is_file():
            return p.read_text(encoding="utf-8", errors="ignore")[:3000]
    return "(no explicit sensitivity directives on disk)"


def main() -> int:
    ids = sys.argv[1:]
    if not ids:
        print("usage: sensitivity_check.py <id>...", file=sys.stderr); return 2
    if not os.environ.get("OPENAI_API_KEY"):
        print("error: OPENAI_API_KEY not set", file=sys.stderr); return 1
    from openai import OpenAI
    client = OpenAI()

    out = {}
    if (REPO / "book-sensitivity-check.json").is_file():
        out = json.loads((REPO / "book-sensitivity-check.json").read_text())
    for cid in ids:
        if cid not in CURATED:
            print(f"  {cid}: not in CURATED, skipping", file=sys.stderr); continue
        root = BOOKS / CURATED[cid][4]
        prompt = (f"BOOK: {cid} — {CURATED[cid][1]}\n\n"
                  f"SENSITIVITY DIRECTIVES (author's commitments):\n{directives(root)}\n\n"
                  f"FULL MANUSCRIPT:\n{manuscript(root)}\n\nReturn only the JSON verdict.")
        print(f"[{cid}] judging…", flush=True)
        r = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        raw = (r.choices[0].message.content or "").strip()
        try:
            v = json.loads(raw)
        except json.JSONDecodeError:
            v = {"risk": "ERROR", "one_line": raw[:160]}
        v["_tokens"] = {"in": r.usage.prompt_tokens, "out": r.usage.completion_tokens}
        out[cid] = v
        print(f"  risk={v.get('risk')}  action={v.get('recommended_action')}  blocking={v.get('blocking')}")
        print(f"  {v.get('one_line','')}")
        for f in v.get("flags", []):
            print(f"    - {f}")
        (REPO / "book-sensitivity-check.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
