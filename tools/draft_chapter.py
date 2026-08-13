#!/usr/bin/env python3
"""Draft one chapter from canon, via OFOX. Story first.

Assembles the binding canon a chapter needs, hands it to a frontier model with the
chapter's beat, and writes the prose to build/chapters/. One chapter per call, in
order, so each draft can see the ones before it.

Deliberately NOT a metric tool. It sets no word target and reports no counters —
writing to satisfy a counter produces the flat, even prose the counters exist to
catch. `prose_tics.py` and `semantic_dupes.py` are a LATE hygiene pass over a
finished draft, never a drafting target.

Usage:
    python3 tools/draft_chapter.py books/afrika-2100 ch-00 \\
        --canon STYLE_GUIDE.md,CH_FIRST_CONTACT.md,LANDING_DAY.md,MYTHOS_RULES.md \\
        --beat "Landing Day, 2071, Gogo POV..." [--context-chapters 2]
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
import urllib.error
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from de_llm_pass import DEFAULT_ENV_FILE, OFOX_URL, load_env_file, restore_typography, strip_fence  # noqa: E402

# Prose is the one job worth the frontier tier. See congosky finops model_routing.json.
DEFAULT_MODEL = "anthropic/claude-opus-5"

SYSTEM = """You are drafting one chapter of a literary novel. You are not summarising canon,
not writing a treatment, and not explaining the world. You are writing the prose that will be
printed.

The canon documents below are BINDING. They are the world's physics and the author's decisions.
Where a canon document says LOCKED, it is not negotiable. Where it marks something OPEN, you may
choose — choose concretely and move on, do not hedge.

HOW TO WRITE THIS BOOK:

- Exposition arrives on the shoulder of work. A calibration, a manifest, a watch rotation, a
  survey instrument. Never a lecture, never a narrator explaining the century.
- Declaratives carry. Subordination earns its keep.
- Concrete over abstract, always. Name the tool, the street, the sound.
- Let some passages go plain — subject, verb, object, full stop. Real books are lumpier than
  drafts. Deliberately under-write the connective tissue so the charged moments land.
- Humour where it would really be funny. People are funny on the worst and best days.
- No victory lap. No sermon. No narrator endorsing anyone's faith or politics.
- Every faction gets its best argument. Nobody in this book is a cartoon.
- Flat and loaded on the wounds: state the terrible thing plainly and move on. Do not italicise
  grief, do not build to a gotcha, do not have a character explain what a loss meant.

MACHINE-TELL TABOOS — these read as generated and must be thinned hard:
- "almost [emotion]" (almost smiled, almost gentle). Write the physical fact or cut it.
- The reframe "It wasn't X. It was Y." Kill any version where X exists only to pivot off.
- Em-dashes: use few, and set them tight (word—word), never spaced.
- "something" as a feeling-placeholder ("something in her eased"). Name the muscle or cut.
- "the way..." as a construction. Never twice in a paragraph.
- Fragment tags: "Not a question." "Not a boast." Delete and trust the line.
- Hedges (seemed to, appeared to) and weasels (obviously, clearly, literally, actually).
- The deepest tell is EVENNESS — one intelligence narrating everything at the same temperature.
  Vary sentence and paragraph length more than feels natural.

Write the chapter to its beat and stop when the beat is done. Do not pad to a length. A short
chapter that lands is better than a long one that fills.

Return ONLY the chapter prose, opening with a markdown H1 heading for the chapter. No preamble,
no commentary, no notes to the author, no code fence."""

USER = """# BINDING CANON

{canon}

{previous}

---

# YOUR CHAPTER

{beat}

Write it now. Prose only, opening with the H1 heading."""


def call(model: str, system: str, user: str, timeout: int, max_tokens: int,
         reasoning: str) -> str:
    key = os.environ.get("OFOX_API_KEY")
    if not key:
        sys.exit("OFOX_API_KEY not set")
    body = {
        "model": model,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        "temperature": 1.0,          # prose, not extraction
        "max_tokens": max_tokens,
    }
    if reasoning:
        body["reasoning_effort"] = reasoning
    req = urllib.request.Request(
        OFOX_URL, data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            payload = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"OFOX HTTP {e.code}: {e.read().decode()[:400]}")
    choice = payload["choices"][0]
    text = (choice["message"].get("content") or "").strip()
    if choice.get("finish_reason") == "length":
        raise RuntimeError(f"truncated after "
                           f"{payload.get('usage', {}).get('completion_tokens')} tokens")
    if not text:
        raise RuntimeError(f"empty (finish_reason={choice.get('finish_reason')})")
    return text


import os  # noqa: E402  (after load_env_file import for clarity)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("book", type=pathlib.Path)
    ap.add_argument("chapter", help="output stem, e.g. ch-00")
    ap.add_argument("--canon", required=True, help="comma-separated canon filenames")
    ap.add_argument("--beat", required=True, help="the chapter brief, in prose")
    ap.add_argument("--context-chapters", type=int, default=2,
                    help="how many preceding chapters to show for continuity")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--max-tokens", type=int, default=32000)
    ap.add_argument("--reasoning-effort", default="medium")
    ap.add_argument("--timeout", type=int, default=1200)
    ap.add_argument("--env-file", type=pathlib.Path, default=DEFAULT_ENV_FILE)
    args = ap.parse_args()

    load_env_file(args.env_file)

    canon_dir = args.book / "canon"
    parts = []
    for name in args.canon.split(","):
        p = canon_dir / name.strip()
        if not p.exists():
            sys.exit(f"missing canon file: {p}")
        parts.append(f"## canon/{p.name}\n\n{p.read_text()}")
    canon = "\n\n---\n\n".join(parts)

    ch_dir = args.book / "build" / "chapters"
    ch_dir.mkdir(parents=True, exist_ok=True)
    prior = sorted(ch_dir.glob("*.md"))[-args.context_chapters:] if args.context_chapters else []
    previous = ""
    if prior:
        joined = "\n\n".join(f"### {p.name}\n\n{p.read_text()}" for p in prior)
        previous = ("---\n\n# THE CHAPTERS IMMEDIATELY BEFORE YOURS\n\n"
                    "Continue from these. Do not repeat their sentences, images or turns of "
                    "phrase — a repeated line across chapters is the drafting tell this book "
                    "is being written to avoid.\n\n" + joined)

    user = USER.format(canon=canon, previous=previous, beat=args.beat)
    print(f"drafting {args.chapter} via {args.model} "
          f"({len(user)//4:,} tokens of context) ...", flush=True)

    text = restore_typography(strip_fence(
        call(args.model, SYSTEM, user, args.timeout, args.max_tokens, args.reasoning_effort)))

    out = ch_dir / f"{args.chapter}.md"
    out.write_text(text if text.endswith("\n") else text + "\n")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
