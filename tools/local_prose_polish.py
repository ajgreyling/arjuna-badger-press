#!/usr/bin/env python3
"""Generate surgical prose-edit suggestions with a local Ollama model.

This tool never rewrites files. It feeds only flagged sentences plus local context to
Ollama and writes a JSON review report. A human/editor must accept edits explicitly.

Usage:
    python3 tools/local_prose_polish.py books/<book> --out /tmp/polish.json
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from prose_tics import TELLS  # noqa: E402


OLLAMA_URL = "http://localhost:11434/api/chat"

SYSTEM = """You are a conservative line editor for a South African science-thriller.
Return JSON only. Suggest the smallest edit that removes the named prose tic.
Preserve plot facts, technical meaning, character voice, punctuation style, and markdown.
Do not add information. Do not generalise local diction. If the line is already earned,
set replacement to the exact original and explain briefly why it should stay."""


def ollama(model: str, item: dict) -> dict:
    body = json.dumps({
        "model": model,
        "stream": False,
        "format": "json",
        # This is a two-field micro-edit, not a chapter rewrite. Qwen's default
        # thinking path can spend minutes without returning a token, so keep the
        # local advisory pass deliberately small and bounded.
        "think": False,
        "options": {"temperature": 0.2, "num_predict": 512, "num_ctx": 4096},
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": json.dumps(item, ensure_ascii=False)},
        ],
    }).encode()
    req = urllib.request.Request(
        OLLAMA_URL, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as response:
        payload = json.load(response)
    raw = payload["message"]["content"]
    return json.loads(raw)


def sentence_span(text: str, start: int, end: int) -> tuple[int, int]:
    left = max(text.rfind("\n\n", 0, start), text.rfind(". ", 0, start))
    left = 0 if left < 0 else left + (2 if text[left:left + 2] in {"\n\n", ". "} else 0)
    stops = [p for p in (text.find(". ", end), text.find("\n\n", end)) if p >= 0]
    right = min(stops) + 1 if stops else len(text)
    return left, right


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("book", type=pathlib.Path)
    parser.add_argument("--model", default="qwen3.5:4b")
    parser.add_argument("--out", type=pathlib.Path, required=True)
    parser.add_argument("--only", action="append", help="chapter filename; repeatable")
    args = parser.parse_args()

    chapters = sorted((args.book / "build" / "chapters").glob("*.md"))
    if args.only:
        selected = set(args.only)
        chapters = [path for path in chapters if path.name in selected]

    leads: list[dict] = []
    seen: set[tuple[str, int, int]] = set()
    for path in chapters:
        text = path.read_text(encoding="utf-8")
        for tic, pattern in TELLS.items():
            for match in re.finditer(pattern, text, flags=re.I | re.M):
                lo, hi = sentence_span(text, match.start(), match.end())
                key = (path.name, lo, hi)
                if key in seen:
                    continue
                seen.add(key)
                original = text[lo:hi].strip()
                context_lo = max(0, text.rfind("\n\n", 0, lo - 1))
                context_hi = text.find("\n\n", hi + 1)
                context_hi = len(text) if context_hi < 0 else context_hi
                item = {
                    "chapter": path.name,
                    "tic": tic,
                    "original": original,
                    "context": text[context_lo:context_hi].strip(),
                    "required_output": {
                        "replacement": "full replacement for original only",
                        "reason": "brief editorial rationale",
                    },
                }
                print(f"{path.name}: {tic}", flush=True)
                try:
                    suggestion = ollama(args.model, item)
                except Exception as exc:  # keep the report useful if one call fails
                    suggestion = {"error": str(exc)}
                leads.append({**item, "suggestion": suggestion})

    args.out.write_text(json.dumps(leads, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {len(leads)} suggestions -> {args.out}")


if __name__ == "__main__":
    main()
