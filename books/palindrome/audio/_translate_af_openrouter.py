#!/usr/bin/env python3
"""One-shot Afrikaans prose translator for Palindrome via OpenRouter.

Used when platform saas.* deps are unavailable. Writes:
  build/.translate/af/seg-NN.md
  build/BOOK.af.md

Usage:
  python3 books/palindrome/audio/_translate_af_openrouter.py
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BOOK = Path(__file__).resolve().parents[1]
SEG_DIR = BOOK / "build" / ".translate" / "segments"
OUT_DIR = BOOK / "build" / ".translate" / "af"
BOOK_AF = BOOK / "build" / "BOOK.af.md"

MODEL = os.environ.get("OPENROUTER_PROSE_MODEL") or os.environ.get(
    "OPENROUTER_MODEL_ANTHROPIC", "anthropic/claude-sonnet-4.6"
)
API = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM = """You are translating Arjuna Badger Press literary fiction into Afrikaans.

Book: Palindrome — a quiet chamber-piece novella (Man from Earth engine).
Voice: literary contemporary Afrikaans — adult, clinical dread, humane stillness.
NOT stiff textbook, broadcast, or slangy urban Afrikaans.

Hard rules:
- Full PROSE translation. Do NOT turn it into a play or screenplay.
- Preserve markdown structure and headings exactly in kind (Dedication; A Note to the Reader → 'n Nota aan die Leser; One→Een … Seven→Sewe).
- Keep proper names verbatim: August Renner, Solomon Voss, Sol, Voss, Earl Cade, Earl, Danny Reiss, Danny, Grahamstown, Loubser, Jerome Bixby, The Man from Earth.
- Keep free-indirect interiority (Voss's thoughts) as prose thought, not stage direction.
- No translator's notes, footnotes, or glosses.
- Return ONLY the translated markdown for this segment — no preamble."""


def key() -> str:
    k = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not k:
        sys.exit("OPENROUTER_API_KEY required")
    return k


def translate(seg_text: str) -> str:
    payload = {
        "model": MODEL,
        "temperature": 0.55,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {
                "role": "user",
                "content": "Translate this segment into Afrikaans:\n\n" + seg_text,
            },
        ],
    }
    body = json.dumps(payload).encode("utf-8")
    def _hdr(value: str) -> str:
        # HTTP headers must be latin-1; strip fancy dashes/quotes from env titles.
        return value.encode("ascii", "ignore").decode("ascii") or "arjunabadger.press"

    req = urllib.request.Request(
        API,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {key()}",
            "Content-Type": "application/json",
            "HTTP-Referer": _hdr(os.environ.get("OPENROUTER_HTTP_REFERER", "https://arjunabadger.press")),
            "X-Title": _hdr(os.environ.get("OPENROUTER_X_TITLE", "Arjuna Badger Press Palindrome AF")),
        },
    )
    last = None
    for attempt in range(1, 6):
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"].strip() + "\n"
        except urllib.error.HTTPError as e:
            last = e.read().decode("utf-8", "replace")[:500]
            if e.code not in (408, 429, 500, 502, 503, 504) or attempt == 5:
                raise RuntimeError(f"HTTP {e.code}: {last}") from e
            time.sleep(min(60, 2**attempt))
        except Exception as e:
            last = repr(e)
            if attempt == 5:
                raise
            time.sleep(min(60, 2**attempt))
    raise RuntimeError(last or "translate failed")


def main() -> None:
    segs = sorted(SEG_DIR.glob("seg-*.md"))
    if not segs:
        sys.exit(f"no segments in {SEG_DIR}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"model={MODEL} segments={len(segs)}", flush=True)
    parts: list[str] = []
    for path in segs:
        out = OUT_DIR / path.name
        if out.exists() and out.stat().st_size > 40:
            text = out.read_text(encoding="utf-8")
            print(f"reuse {path.name} ({len(text.split())} words)", flush=True)
        else:
            src = path.read_text(encoding="utf-8")
            print(f"translate {path.name} ({len(src.split())} words)…", flush=True)
            text = translate(src)
            # strip accidental fences
            if text.startswith("```"):
                text = text.strip("`")
                if text.startswith("markdown"):
                    text = text[len("markdown"):].lstrip()
            out.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
            print(f"  → {len(text.split())} words", flush=True)
        parts.append(out.read_text(encoding="utf-8").rstrip() + "\n")
    BOOK_AF.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    words = len(BOOK_AF.read_text(encoding="utf-8").split())
    print(f"wrote {BOOK_AF} (~{words} words)", flush=True)


if __name__ == "__main__":
    main()
