#!/usr/bin/env python3
"""Metered draft driver for *The Antifragile Reader* (OpenRouter / Opus prose).

One Anthropic call per essay. Resumable: skips files that already have >400 words.
Routes via engine.llm_client (OPENROUTER_API_KEY when set).

Usage:
  python3 .draft_book.py              # draft all missing essays
  python3 .draft_book.py --only 02    # draft one essay by number
  python3 .draft_book.py --restart    # redo all (except --only)
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]  # arjuna-badger
PLATFORM = REPO / "arjuna-badger-platform"

for env_path in (PLATFORM / ".env", REPO / "africangold" / ".env"):
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

sys.path.insert(0, str(PLATFORM))
from engine.llm_client import call_anthropic, openrouter_enabled  # noqa: E402

BOOK = HERE / "book"
CANON = HERE / "canon"
LOG = HERE / "build" / "draft.log"

EXEMPLARS = ("00-proem.md", "01-fooled-by-randomness.md", "05-the-bed-of-procrustes.md")

ESSAYS = [
    {
        "n": "02",
        "file": "02-the-black-swan.md",
        "heading": "Two — The Bird We Didn't See",
        "anchor": "The Black Swan",
        "beat": (
            "The rare, the unpredicted, the explained-after. Turkey problem, narrative fallacy, "
            "retrospective certainty, why experts miss what matters."
        ),
    },
    {
        "n": "03",
        "file": "03-mediocristan.md",
        "heading": "Three — Two Countries",
        "anchor": "The Black Swan",
        "beat": (
            "Mediocristan and Extremistan; where the average lies; thin-tailed vs fat-tailed; "
            "why Gaussian comfort fails in the domains that ruin you."
        ),
    },
    {
        "n": "04",
        "file": "04-the-ludic-fallacy.md",
        "heading": "Four — The Game Is Not the World",
        "anchor": "The Black Swan",
        "beat": (
            "The ludic fallacy: dice, casinos, engineered games vs messy reality; "
            "the map that is not the ground; why classroom probability misleads."
        ),
    },
    {
        "n": "06",
        "file": "06-antifragile.md",
        "heading": "Six — The Three States",
        "anchor": "Antifragile",
        "beat": (
            "Fragile, robust, antifragile; what gains from disorder; hormesis; "
            "the word the reader came in through."
        ),
    },
    {
        "n": "07",
        "file": "07-via-negativa.md",
        "heading": "Seven — Subtraction",
        "anchor": "Antifragile",
        "beat": (
            "Via negativa, the Lindy effect, less-is-more, what to remove rather than add; "
            "time as judge of what survives."
        ),
    },
    {
        "n": "08",
        "file": "08-the-barbell.md",
        "heading": "Eight — Both Ends, Not the Middle",
        "anchor": "Antifragile",
        "beat": (
            "The barbell strategy, optionality, convex tinkering, avoiding the fragile middle; "
            "practical posture under uncertainty."
        ),
    },
    {
        "n": "09",
        "file": "09-skin-in-the-game.md",
        "heading": "Nine — The Cost of Being Wrong",
        "anchor": "Skin in the Game",
        "beat": (
            "Risk-sharing, the agency problem, who pays when things go wrong; "
            "the oldest honesty; symmetry of consequences."
        ),
    },
    {
        "n": "10",
        "file": "10-the-fragilista.md",
        "heading": "Ten — The Man Who Means Well",
        "anchor": "Skin in the Game / Antifragile",
        "beat": (
            "The fragilista, iatrogenics, naive rationalism, the intervener who harms while helping; "
            "policy and expertise without downside."
        ),
    },
    {
        "n": "11",
        "file": "11-coda.md",
        "heading": "Coda — What I Carried Home",
        "anchor": "all Incerto volumes",
        "beat": (
            "The guest leaves the fire. Via-negativa creed. What the whole architecture adds up to. "
            "Send the reader back to Taleb's books, warmer and braver. No new ideas — synthesis only."
        ),
    },
]

WORD_TARGETS = {"11": 700, "default": 950}


def log(msg: str) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg, flush=True)


def prose_words(text: str) -> int:
    return len(re.sub(r"<!--.*?-->", "", text, flags=re.S).split())


def is_drafted(path: Path) -> bool:
    return path.exists() and prose_words(path.read_text(encoding="utf-8")) > 400


def prior_context() -> str:
    parts = []
    for f in sorted(BOOK.glob("*.md")):
        if f.name == "_front.md":
            continue
        parts.append(f"### {f.name}\n{f.read_text(encoding='utf-8')[:3500]}")
    return "\n\n".join(parts)


def exemplar_block() -> str:
    chunks = []
    for name in EXEMPLARS:
        p = BOOK / name
        if p.exists():
            chunks.append(f"## VOICE EXEMPLAR: {name}\n\n{p.read_text(encoding='utf-8')}")
    return "\n\n".join(chunks)


def draft_one(spec: dict) -> str:
    style = (CANON / "STYLE_GUIDE.md").read_text(encoding="utf-8")
    target = WORD_TARGETS.get(spec["n"], WORD_TARGETS["default"])
    prompt = f"""You are drafting ONE essay for *The Antifragile Reader* — a reverent companion to
Nassim Nicholas Taleb's *Incerto*. Output ONLY the finished essay markdown. No preamble, no commentary,
no word-count note. The first line MUST be exactly:

# {spec['heading']}

Followed by an italic anchor line like the exemplars:
*Anchored in* {spec['anchor']} *— ...*

Then the four beats as ### headings:
### The fire
### Where the smoke goes
### Plainly
### The line

BINDING STYLE GUIDE:
{style}

VOICE EXEMPLARS (match register, humility, rhythm, paragraph length):
{exemplar_block()}

PRIOR ESSAYS (continuity — do not repeat their openings; build forward):
{prior_context()[:24000]}

THIS ESSAY:
Number: {spec['n']}
Title: {spec['heading']}
Anchored in: {spec['anchor']}
Coverage: {spec['beat']}

RULES (non-negotiable):
- Living-author rule: paraphrase his ideas; quote only brief aphorisms with attribution; never reproduce passages.
- Mark our gloss with **`plainly:`** in the Plainly section and where needed in The line.
- State Taleb's case at full strength before pushback.
- ~{target} words. Warm, plain, first-person guest-at-the-fire voice.
- No LLM tells: no "delve", "tapestry", "it's important to note", reflex tricolons, significance narration.
- End The line by sending the reader to the source book(s), as the exemplars do.
"""
    system = (
        "You write essay prose for Arjuna Badger Press companions. Markdown only. "
        "Faithful Taleb exposition in original phrasing; three voices kept separate."
    )
    return call_anthropic(prompt, max_tokens=8192, system=system).strip()


def with_retries(fn, tries: int = 5):
    last = None
    for attempt in range(tries):
        try:
            return fn()
        except Exception as e:
            last = e
            wait = min(60, 2**attempt * 5)
            log(f"  [retry] {type(e).__name__}: {str(e)[:120]}; sleep {wait}s")
            time.sleep(wait)
    raise last or RuntimeError("draft failed")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="essay number e.g. 02")
    ap.add_argument("--restart", action="store_true")
    args = ap.parse_args()

    if not openrouter_enabled() and not os.environ.get("ANTHROPIC_API_KEY"):
        log("[fail] No OPENROUTER_API_KEY or ANTHROPIC_API_KEY in environment")
        return 1

    backend = "openrouter" if openrouter_enabled() else "direct"
    log(f"[start] draft driver · backend={backend}")

    drafted = 0
    for spec in ESSAYS:
        if args.only and spec["n"] != args.only.zfill(2):
            continue
        dest = BOOK / spec["file"]
        if is_drafted(dest) and not args.restart and not args.only:
            log(f"[skip] {spec['file']} ({prose_words(dest.read_text(encoding='utf-8'))} words)")
            continue

        log(f"[draft] {spec['heading']} -> {spec['file']} ...")
        text = with_retries(lambda: draft_one(spec))

        if not text.startswith("#"):
            text = f"# {spec['heading']}\n\n{text}"

        dest.write_text(text.rstrip() + "\n", encoding="utf-8")
        wc = prose_words(text)
        log(f"[ok]   {spec['file']} — {wc} words")
        drafted += 1

    log(f"[done] drafted {drafted} essay(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
