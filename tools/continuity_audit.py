#!/usr/bin/env python3
"""Read a whole book in one pass and report ONLY continuity contradictions.

Chapters drafted independently (or with a short rolling context window) can each
be internally correct and still contradict each other forty pages apart. No local
scanner catches that: it is not repetition, it is disagreement about fact.

This is the safe shape for a whole-book model call — very large input, very small
output. A whole-book *rewrite* cannot work, because emitting 60,000 words needs
more output tokens than any model will produce in one response. Reading 60,000
words and emitting a list of fifteen contradictions is trivially within budget.

Usage:
    python3 tools/continuity_audit.py books/afrika-2100 [--model ...]
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from de_llm_pass import DEFAULT_ENV_FILE, OFOX_URL, load_env_file  # noqa: E402

DEFAULT_MODEL = "google/gemini-3.1-pro-preview"   # 1M context, cheap on input

SYSTEM = """You are a continuity editor reading a complete novel manuscript.

Report ONLY hard contradictions between chapters — places where the book states
two incompatible things. You are not a critic. Do not comment on quality, pacing,
style, theme, or whether something is a good idea.

What counts:
- A fact stated differently in two places (a date, an age, a quantity, a name, a
  rank, a place, a relationship, an eye colour, a time of day).
- A character knowing something before they were told it, or not knowing
  something they were already told.
- An object or person in two places at once, or travel that takes impossible time.
- A rule the book established being broken later without acknowledgement.

What does NOT count, and must not be reported:
- Deliberate refrains and repeated images.
- A character being wrong, lying, or remembering imperfectly, where the text
  shows it.
- Two different anchors for a span of years, if both are internally consistent
  (e.g. years since a landing vs years since a treaty signed two years later).
- Anything you merely find unclear.

For each finding give: the two chapter files, what each says (quote briefly), and
which one you believe is wrong, with your reason. If you are not sure which is
wrong, say so.

If there are no contradictions, say exactly: NO CONTRADICTIONS FOUND.

Be terse. This is a defect list, not an essay."""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("book", type=pathlib.Path)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--max-tokens", type=int, default=8000)
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--env-file", type=pathlib.Path, default=DEFAULT_ENV_FILE)
    args = ap.parse_args()

    load_env_file(args.env_file)
    key = os.environ.get("OFOX_API_KEY")
    if not key:
        sys.exit("OFOX_API_KEY not set")

    chapters = sorted((args.book / "build" / "chapters").glob("*.md"))
    if not chapters:
        sys.exit("no chapters")
    text = "\n\n".join(f"=== {p.name} ===\n\n{p.read_text()}" for p in chapters)
    print(f"auditing {len(chapters)} chapters, {len(text.split()):,} words "
          f"(~{len(text)//4:,} tokens) via {args.model} ...", flush=True)

    body = json.dumps({
        "model": args.model,
        "messages": [{"role": "system", "content": SYSTEM},
                     {"role": "user", "content": text}],
        "temperature": 0,
        "max_tokens": args.max_tokens,
    }).encode()
    req = urllib.request.Request(
        OFOX_URL, data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=args.timeout) as r:
            payload = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"OFOX HTTP {e.code}: {e.read().decode()[:400]}")

    choice = payload["choices"][0]
    usage = payload.get("usage", {})
    print(f"[prompt {usage.get('prompt_tokens')} tok, "
          f"completion {usage.get('completion_tokens')} tok, "
          f"finish={choice.get('finish_reason')}]\n")
    print((choice["message"].get("content") or "").strip())


if __name__ == "__main__":
    main()
