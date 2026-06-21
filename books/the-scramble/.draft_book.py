#!/usr/bin/env python3
"""Metered single-shot draft driver for *The Scramble*.

One Opus call per chapter. Full canon + PLANTS_AND_PAYOFFS injected every prompt.
Resumable: skips manuscript files with >300 words of prose unless --restart.

Usage:
  python3 .draft_book.py                 # draft missing chapters
  python3 .draft_book.py --only prologue
  python3 .draft_book.py --only ch-01
  python3 .draft_book.py --restart     # redo drafted chapters
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[2]
PLATFORM = REPO / "arjuna-badger-platform"
PROMPT_PATH = HERE / "prompts" / "draft-chapter.md"
MANUSCRIPT = HERE / "manuscript"
OUTLINE = HERE / "build" / "outline.json"
STATE_F = HERE / "build" / "story_state.md"
LOG_F = HERE / "build" / "log" / "draft.log"

SKIP_ALWAYS: set[str] = set()  # FOREWORD / DEDICATION hand-written

CHAPTER_FILES = {
    "prologue": "PROLOGUE.md",
    "ch-01": "ch-01.md",
}


def _load_env() -> None:
    for env_path in (PLATFORM / ".env", REPO / "africangold-portfolio" / ".env"):
        if not env_path.exists():
            continue
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                v = v.strip().strip('"').strip("'")
                if "#" in v:
                    v = v.split("#", 1)[0].strip()
                os.environ.setdefault(k.strip(), v)


_load_env()
sys.path.insert(0, str(PLATFORM / "engine"))
from llm_client import call_anthropic, call_openai  # noqa: E402

CAN = HERE / "canon"
CANON_ORDER = json.loads((HERE / "project.json").read_text())["canon_order"]
CRAFT_SNIPPET = HERE.parents[1] / "docs" / "craft" / "ANTI_PATTERNS.md"


def load_canon() -> str:
    parts: list[str] = []
    for name in CANON_ORDER:
        p = CAN / name
        if p.exists():
            parts.append(f"# === {name} ===\n\n{p.read_text()}")
    if CRAFT_SNIPPET.exists():
        text = CRAFT_SNIPPET.read_text()
        # first ~120 lines cover master patterns referenced in prompt
        parts.append(f"# === ANTI_PATTERNS (excerpt) ===\n\n{text[:8000]}")
    return "\n\n" + ("=" * 40) + "\n\n".join(parts)


def chapter_path(ch_id: str) -> pathlib.Path:
    name = CHAPTER_FILES.get(ch_id, f"{ch_id}.md")
    return MANUSCRIPT / name


def prose_word_count(text: str) -> int:
    body = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    body = re.sub(r"^>.*$", "", body, flags=re.M)
    return len(body.split())


def is_drafted(path: pathlib.Path) -> bool:
    if not path.exists():
        return False
    return prose_word_count(path.read_text()) > 300


def ch_sort_key(ch_id: str) -> tuple:
    if ch_id == "prologue":
        return (0, ch_id)
    m = re.match(r"ch-(\d+)", ch_id)
    return (int(m.group(1)) if m else 999, ch_id)


def draft_one(ch: dict, story_state: str, canon: str, template: str) -> str:
    beats = ch.get("beats") or []
    prompt = (
        canon
        + "\n\n"
        + template.format(
            CHAPTER_ID=ch["id"],
            CHAPTER_TITLE=ch.get("title", ch["id"]),
            ACT=ch.get("act", ""),
            PART=ch.get("part", ""),
            POV=ch.get("pov", ""),
            SETTING=ch.get("setting", ""),
            BEATS="; ".join(beats),
            TURN=ch.get("turn", ""),
            THREADS=ch.get("threads", ""),
            TARGET_WORDS=str(ch.get("target_words", 1500)),
            STORY_STATE=story_state or "(opening — nothing has happened yet)",
        )
    )
    system = (
        "You are the Scribe for The Scramble — PKD Scanner engine, original prose, split-feed LIVED/WATCHED. "
        "Markdown chapter output only. Never caption the seam."
    )
    model = os.environ.get("ANTHROPIC_MODEL", "claude-opus-4-8")
    max_tok = int(os.environ.get("CHAPTER_MAX_TOKENS", "16000"))
    return call_anthropic(prompt, model=model, max_tokens=max_tok, system=system).strip()


def compress_state(prev: str, ch_id: str, title: str, text: str) -> str:
    prompt = f"""Update rolling STORY-STATE for *The Scramble* after {ch_id} ("{title}").
Keep <= 600 words: plot position, register balance (LIVED vs WATCHED), threads planted/paid (PP-IDs),
what Vance knows vs reader, Chekhov guns still open, character states. Bullets only.

CURRENT:
{prev or "(none)"}

NEW CHAPTER:
{text[:12000]}

Output ONLY updated story-state markdown."""
    model = os.environ.get("OPENAI_MODEL", "gpt-4.1")
    max_tok = int(os.environ.get("SUMMARISE_MAX_TOKENS", "1500"))
    return call_openai(prompt, model=model, max_tokens=max_tok, temperature=0.3)


def log(msg: str) -> None:
    LOG_F.parent.mkdir(parents=True, exist_ok=True)
    LOG_F.open("a").write(f"{msg}\n")
    print(msg, file=sys.stderr, flush=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="draft single chapter id e.g. prologue or ch-01")
    ap.add_argument("--from", dest="frm", help="start at chapter id")
    ap.add_argument("--restart", action="store_true")
    args = ap.parse_args()

    outline = json.loads(OUTLINE.read_text())
    chapters = sorted(outline["chapters"], key=lambda c: ch_sort_key(c["id"]))
    canon = load_canon()
    template = PROMPT_PATH.read_text()

    story_state = ""
    if STATE_F.exists() and not args.restart:
        story_state = STATE_F.read_text()

    frm_key = ch_sort_key(args.frm)[0] if args.frm else None

    drafted = 0
    for ch in chapters:
        cid = ch["id"]
        if args.only and cid != args.only:
            continue
        if cid in SKIP_ALWAYS and not args.only:
            log(f"[skip] {cid} (hand-written front matter)")
            continue
        if frm_key is not None and ch_sort_key(cid)[0] < frm_key:
            continue

        dest = chapter_path(cid)
        if is_drafted(dest) and not args.restart and not args.only:
            log(f"[skip] {cid} already drafted ({prose_word_count(dest.read_text())} words)")
            continue

        log(f"[draft] {cid} — {ch.get('title')} (~{ch.get('target_words')}w) ...")
        try:
            text = draft_one(ch, story_state, canon, template)
        except Exception as e:
            log(f"[FAIL] {cid}: {e}")
            sys.exit(1)

        if not text.startswith("#"):
            text = f"# {ch.get('title', cid)}\n\n{text}"

        dest.write_text(text + "\n")
        wc = prose_word_count(text)
        log(f"[ok]   {cid} {wc} words -> manuscript/{dest.name}")

        try:
            story_state = compress_state(story_state, cid, ch.get("title", ""), text)
            STATE_F.parent.mkdir(parents=True, exist_ok=True)
            STATE_F.write_text(story_state)
        except Exception as e:
            log(f"[warn] state compress failed for {cid}: {e}")

        drafted += 1

    log(f"[done] drafted {drafted} chapter(s)")


if __name__ == "__main__":
    main()
