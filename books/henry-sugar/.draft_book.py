#!/usr/bin/env python3
"""Metered single-shot draft driver for *Henry Sugar*.

One Opus call per chapter. Canon + REPORTED_PHYSICS boundaries injected every prompt.
Resumable: skips chapters that already have >300 words of prose (stubs don't count).

Usage:
  python3 .draft_book.py              # draft all missing narrative chapters
  python3 .draft_book.py --only ch-01
  python3 .draft_book.py --from ch-11
  python3 .draft_book.py --restart    # redo all (except SKIP_ALWAYS unless --only)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[2]  # arjuna-badger
PLATFORM = REPO / "arjuna-badger-platform"
PROMPT_PATH = HERE / "prompts" / "draft-chapter.md"

SKIP_ALWAYS = {"ch-00", "ch-98"}  # dedication + backmatter already written

# Load API keys from platform .env (metered — not subscription)
for env_path in (PLATFORM / ".env", REPO / "africangold" / ".env"):
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

sys.path.insert(0, str(PLATFORM / "engine"))
from llm_client import call_anthropic, call_openai  # noqa: E402

CAN = HERE / "canon"
CH = HERE / "build" / "chapters"
OUTLINE = HERE / "build" / "outline.json"
STATE_F = HERE / "build" / "story_state.md"
LOG_F = HERE / "build" / "log" / "draft.log"

CANON_ORDER = json.loads((HERE / "project.json").read_text())["canon_order"]


def load_canon() -> str:
    parts = []
    for name in CANON_ORDER:
        p = CAN / name
        if p.exists():
            parts.append(f"# === {name} ===\n\n{p.read_text()}")
    return "\n\n" + ("=" * 40) + "\n\n".join(parts)


def load_prompt_template() -> str:
    return PROMPT_PATH.read_text()


def prose_word_count(text: str) -> int:
    body = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return len(body.split())


def is_drafted(path: pathlib.Path) -> bool:
    if not path.exists():
        return False
    return prose_word_count(path.read_text()) > 300


def ch_sort_key(ch_id: str) -> tuple:
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
        "You are the Scribe for Henry Sugar — faithful Dahl retelling, original prose, "
        "reported physics only. Markdown chapter output only."
    )
    model = os.environ.get("ANTHROPIC_MODEL", "claude-opus-4-8")
    max_tok = int(os.environ.get("CHAPTER_MAX_TOKENS", "16000"))
    return call_anthropic(prompt, model=model, max_tokens=max_tok, system=system).strip()


def compress_state(prev: str, ch_id: str, title: str, text: str) -> str:
    prompt = f"""Update rolling STORY-STATE for *Henry Sugar* after {ch_id} ("{title}").
Keep <= 600 words: plot position, nested-document level, Henry's training stage, threads planted/paid
(PP-IDs if visible), what each POV knows, Chekhov guns still open. Bullets only.

CURRENT:
{prev or "(none)"}

NEW CHAPTER:
{text[:12000]}

Output ONLY updated story-state markdown."""
    try:
        return call_openai(prompt, model="gpt-4.1", max_tokens=1500, temperature=0.3)
    except Exception:
        return call_anthropic(
            prompt,
            model=os.environ.get("ANTHROPIC_MODEL", "claude-opus-4-8"),
            max_tokens=1500,
        )


def log(msg: str) -> None:
    LOG_F.parent.mkdir(parents=True, exist_ok=True)
    line = f"{msg}\n"
    LOG_F.open("a").write(line)
    print(msg, file=sys.stderr, flush=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="draft single chapter id e.g. ch-01")
    ap.add_argument("--from", dest="frm", help="start at chapter id e.g. ch-11")
    ap.add_argument("--restart", action="store_true")
    args = ap.parse_args()

    outline = json.loads(OUTLINE.read_text())
    chapters = sorted(outline["chapters"], key=lambda c: ch_sort_key(c["id"]))
    canon = load_canon()
    template = load_prompt_template()

    story_state = ""
    if STATE_F.exists() and not args.restart:
        story_state = STATE_F.read_text()

    frm_num = None
    if args.frm:
        m = re.match(r"ch-(\d+)", args.frm)
        frm_num = int(m.group(1)) if m else 0

    drafted = 0
    for ch in chapters:
        cid = ch["id"]
        if args.only and cid != args.only:
            continue
        if cid in SKIP_ALWAYS and not args.only:
            log(f"[skip] {cid} (front/back matter — already written)")
            continue
        if frm_num is not None:
            m = re.match(r"ch-(\d+)", cid)
            if m and int(m.group(1)) < frm_num:
                continue

        dest = CH / f"{cid}.md"
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
            # ensure heading
            text = f"# {ch.get('title', cid)}\n\n{text}"

        dest.write_text(text + "\n")
        wc = prose_word_count(text)
        log(f"[ok]   {cid} {wc} words -> {dest.name}")

        if cid not in SKIP_ALWAYS:
            try:
                story_state = compress_state(story_state, cid, ch.get("title", ""), text)
                STATE_F.write_text(story_state)
            except Exception as e:
                log(f"[warn] state compress failed for {cid}: {e}")

        drafted += 1

    log(f"[done] drafted {drafted} chapter(s)")
    # mirror hint
    plat = PLATFORM / "books" / "henry-sugar" / "build" / "chapters"
    if plat.parent.exists():
        log(f"[note] sync to platform: cp -r {CH}/*.md {plat}/")


if __name__ == "__main__":
    main()
