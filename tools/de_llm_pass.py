#!/usr/bin/env python3
"""Metered de-LLM + de-duplication rewrite pass, routed through OFOX.

The blind scanner (tools/prose_tics.py) finds WHERE the machine-tells and the
repeated prose are. This spends tokens fixing them, one chapter per call.

Two things this does that a naive "rewrite this chapter" prompt cannot:

  1. GLOBAL de-dup assignment. A per-chapter call cannot know which occurrence
     of a repeated line is the original. So we decide it here, deterministically:
     the earliest chapter keeps the line, every later chapter is told to recast
     that specific sentence. The model never gets to vote on which one survives.

  2. MOTIF protection. Lines in canon/MOTIFS_PROTECTED.txt are passed through as
     must-not-touch. A refrain is the book's spine; only drift gets cut.

Provider: OFOX (api.ofox.ai, OpenAI-compatible), the estate's rented brain.
Key from OFOX_API_KEY — env, or --env-file (default: ~/code/congosky-cloud/.env).

Usage:
    # see what would be sent, spend nothing
    python3 tools/de_llm_pass.py books/the-prophet-and-his-brother --dry-run

    # one chapter, to calibrate the voice before committing to all 24
    python3 tools/de_llm_pass.py books/the-prophet-and-his-brother --only ch-01.md

    # the full pass
    python3 tools/de_llm_pass.py books/the-prophet-and-his-brother
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from prose_tics import (  # noqa: E402
    MIN_SENTENCE_WORDS, is_protected, load_protect, normalise, scan, sentences,
)

OFOX_URL = "https://api.ofox.ai/v1/chat/completions"
OLLAMA_URL = "http://localhost:11434/api/chat"
DEFAULT_OLLAMA_MODEL = "qwen3.5:4b"
DEFAULT_ENV_FILE = pathlib.Path.home() / "code" / "congosky-cloud" / ".env"
# Frontier band. Line-editing literary prose is judgment work; the mid worker
# (gpt-5.4-mini) flattens voice. See congosky finops model_routing.json.
DEFAULT_MODEL = "anthropic/claude-sonnet-5"
EM_DASH_CEILING = 8

SYSTEM = """You are a line editor removing the machine-tells from a literary novel.
You are NOT rewriting the book. You are thinning tics. The prose is the author's;
your job is to make it stop sounding generated while changing as little as possible.

THE CONTRACT — the tells to thin (they are tics because the underlying moves are
good; the job is thinning, not banning):

1. "almost [emotion]" ("almost smiled", "almost gentle") — a non-event standing in
   for a real feeling. Write the physical fact (the corner of a mouth, a breath) or
   cut the tag and let the deadpan stand. At most one survives per chapter.
2. The reframe "It wasn't X. It was Y." / "not X, but Y" — a thinking-SHAPE that
   performs a turn on demand. Kill any version where X exists only to pivot off it.
   Keep only where a belief the reader actually held is overturned.
3. Em-dashes: this chapter has {em_dash_count}. Cut to at most {em_dash_ceiling}.
   Survivors must be set TIGHT (word{dash}word), never spaced. A parenthetical aside
   wants commas or parens; an end-of-sentence reframe wants a full stop. Keep the
   dash only for a real dialogue interruption or a genuine mid-thought swerve.
4. "something" as a feeling-placeholder ("something in him eased") — name the muscle
   (jaw, eyes, breath) or cut to the action.
5. "the way..." — carries characterization, so at scale it reads as authorial reflex.
   Never two in a paragraph. Keep the ~40% that genuinely illuminate; state the rest
   directly.
6. "Not a question." / "Not a boast." fragment tags — throat-clearing after a line
   that already reads that way. Delete and trust the line.
7. The "which, from [Name], meant..." translation, and stacked trailing-"which"
   sentences — don't do the reader's interpreting for them.
8. Hedges ("seemed to", "appeared to", "perhaps", "somewhat") — commit the claim, or
   own the uncertainty as the POV's read.
9. Weasel words ("obviously", "clearly", "literally", "actually", "basically") —
   "literally" and "actually" almost always delete clean.
10. "very/really [word]" — use the precise stronger word. Keep "very" in speech only.
11. Wordy connectives ("the fact that" -> "that", "in order to" -> "to").
12. Clichés — target zero.

THE DEEPEST TELL IS EVENNESS: one intelligence narrating everything at the same
temperature. Real novels are lumpier. Let some passages go plain — subject, verb,
object, full stop. Deliberately under-write connective tissue so the charged scenes
land. Vary sentence and paragraph length more than feels natural.

DO NOT trade one tell for another. Do not convert every dash the same way. Do not
swap one catchphrase for a fresh one. Vary the fix — the goal is a human hand, not a
new macro.

HARD CONSTRAINTS:
- Never invent plot, characters, dates or events. This novel touches a real death;
  fabrication is the one unforgivable error.
- Preserve every scene beat, every piece of information, and the chapter's structure.
- Preserve the author's South African register and diction. Do not neutralise it into
  international English. Vulgarity in this book is deliberate — never soften it.
- Keep markdown structure, headings and scene breaks exactly as they are.
- Length may drop by up to 5%. It must not grow.

Return ONLY the edited chapter text. No preamble, no commentary, no code fence."""

USER = """{protect_block}{dedup_block}
--- CHAPTER {name} BEGINS ---
{text}
--- CHAPTER {name} ENDS ---

Return the edited chapter, and nothing else."""


def load_env_file(path: pathlib.Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def call_ofox(model: str, system: str, user: str, timeout: int,
              max_tokens: int = 32000, reasoning_effort: str = "low") -> str:
    key = os.environ.get("OFOX_API_KEY")
    if not key:
        sys.exit("OFOX_API_KEY not set (env or --env-file)")
    # max_tokens MUST be set explicitly. OFOX defaults to 4096, and a thinking
    # model spends that budget reasoning before it emits a single word of prose —
    # the call returns finish_reason="length" with EMPTY content. Same failure
    # mode congosky hit on qwen3.5 via this shim; it is not model-specific.
    # A 4,300-word chapter needs ~10k output tokens.
    # reasoning_effort caps the thinking budget. Left at the model default, the
    # long contract prompt sends it into a full editorial deliberation and it
    # exhausts even a 16k cap before writing prose. The judgment we want is
    # per-sentence, not per-chapter, so a low budget is the right shape as well
    # as the cheap one.
    payload_body = {
        "model": model,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        "temperature": 0.7,
        "max_tokens": max_tokens,
    }
    if reasoning_effort:
        payload_body["reasoning_effort"] = reasoning_effort
    body = json.dumps(payload_body).encode()
    req = urllib.request.Request(
        OFOX_URL, data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            payload = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"OFOX HTTP {e.code}: {e.read().decode()[:400]}")
    choice = payload["choices"][0]
    content = (choice["message"].get("content") or "").strip()
    if choice.get("finish_reason") == "length":
        raise RuntimeError(
            f"truncated: finish_reason=length after "
            f"{payload.get('usage', {}).get('completion_tokens')} completion tokens "
            f"(raise --max-tokens)")
    if not content:
        raise RuntimeError(f"empty content (finish_reason={choice.get('finish_reason')})")
    return content


def call_ollama(model: str, system: str, user: str, timeout: int,
                max_tokens: int = 32000) -> str:
    """Run the same guarded editorial contract against a local Ollama model."""
    body = json.dumps({
        "model": model,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        "stream": False,
        "think": False,
        # Ollama defaults to a 4k context even when the model supports more. A
        # full chapter + contract + edited chapter can overflow that silently,
        # causing the model to forget the no-expansion rule. Reserve enough
        # context for both sides of the edit.
        "options": {"temperature": 0.25, "num_predict": max_tokens,
                    "num_ctx": 16384},
    }).encode()
    req = urllib.request.Request(
        OLLAMA_URL, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            payload = json.load(response)
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Ollama unavailable: {exc}") from exc
    content = (payload.get("message", {}).get("content") or "").strip()
    if not content:
        raise RuntimeError("empty local Ollama response")
    return content


def dedup_assignments(result: dict, protect: list[str]) -> dict[str, list[tuple[str, str]]]:
    """Assign every repeated line to the chapter that must change it.

    The earliest chapter keeps ONE occurrence; everything else is recast. Two
    cases, and the second is easy to miss: a line can repeat across chapters AND
    repeat again inside the keeper. Handling only the cross-chapter case leaves
    the keeper still saying it three times, which is what the first pass did.

    Returns {chapter: [(sentence, mode)]} where mode is "recast" (no occurrence
    of this line should survive here) or "thin" (keep the first, recast the rest).
    """
    todo: dict[str, list[tuple[str, str]]] = {}
    for dup in result["duplicate_sentences"]:
        if dup["protected"] or dup["hits"] < 2:
            continue
        by_chapter = dup.get("by_chapter", {})
        keeper = sorted(dup["chapters"])[0]
        for ch in sorted(dup["chapters"]):
            if ch == keeper:
                if by_chapter.get(ch, 0) > 1:
                    todo.setdefault(ch, []).append((dup["text"], "thin"))
            else:
                todo.setdefault(ch, []).append((dup["text"], "recast"))
    return todo


def restore_typography(text: str) -> str:
    """Re-curl quotes the model flattened.

    Every model tested returns straight quotes regardless of what it was given —
    a full chapter comes back with 33 curly apostrophes turned into ASCII. These
    books ship as EPUB and PDF, where that is a visible typographic regression,
    so it is repaired deterministically here rather than asked for in the prompt.
    """
    # Apostrophe inside a word: don't, AJ's, o'clock.
    text = re.sub(r"(?<=[A-Za-z0-9])'(?=[A-Za-z])", "’", text)
    # Elision at the start of a word: 'n, 'strue, '35.
    text = re.sub(r"(?<![A-Za-z0-9])'(?=[A-Za-z0-9])", "’", text)
    # Trailing possessive: the workers' hands.
    text = re.sub(r"(?<=[A-Za-z0-9])'(?![A-Za-z0-9])", "’", text)

    # Double quotes alternate open/close from the start of each paragraph, which
    # is safe here because dialogue in this book does not span a blank line.
    out = []
    for para in text.split("\n\n"):
        chars, open_next = list(para), True
        for i, ch in enumerate(chars):
            if ch == '"':
                chars[i] = "“" if open_next else "”"
                open_next = not open_next
        out.append("".join(chars))
    return "\n\n".join(out)


def strip_fence(text: str) -> str:
    text = re.sub(r"^```[a-z]*\n", "", text)
    return re.sub(r"\n```$", "", text).strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("book", type=pathlib.Path)
    ap.add_argument("--only", action="append", help="chapter filename; repeatable")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--provider", choices=("ofox", "ollama"), default="ofox",
                    help="editor backend; ollama stays fully local")
    ap.add_argument("--env-file", type=pathlib.Path, default=DEFAULT_ENV_FILE)
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--max-tokens", type=int, default=32000,
                    help="output cap; must exceed the chapter, see call_ofox")
    ap.add_argument("--reasoning-effort", default="low",
                    help="thinking budget: none|low|medium|high (see call_ofox)")
    ap.add_argument("--dry-run", action="store_true", help="print the plan, spend nothing")
    ap.add_argument("--out-dir", type=pathlib.Path,
                    help="write edited chapters here instead of in place")
    args = ap.parse_args()

    if args.provider == "ollama" and args.model == DEFAULT_MODEL:
        args.model = DEFAULT_OLLAMA_MODEL

    load_env_file(args.env_file)
    protect_path = args.book / "canon" / "MOTIFS_PROTECTED.txt"
    protect_lines = [l for l in (protect_path.read_text().splitlines()
                                 if protect_path.exists() else [])
                     if l.strip() and not l.startswith("#")]
    protect = load_protect(protect_path)

    result = scan(args.book, protect)
    todo = dedup_assignments(result, protect)
    by_name = {c["chapter"]: c for c in result["per_chapter"]}

    chapters = sorted((args.book / "build" / "chapters").glob("*.md"))
    if args.only:
        chapters = [c for c in chapters if c.name in args.only]
    failures: list[str] = []

    protect_block = ""
    if protect_lines:
        joined = "\n".join(f"  {l}" for l in protect_lines)
        protect_block = (
            "PROTECTED MOTIFS — these recur ON PURPOSE. Reproduce them EXACTLY as "
            "written wherever they appear. Never rephrase, soften, or vary them:\n"
            f"{joined}\n\n")

    for path in chapters:
        stats = by_name[path.name]
        text = path.read_text()
        dups = todo.get(path.name, [])

        dedup_block = ""
        if dups:
            recast = [d for d, mode in dups if mode == "recast"]
            thin = [d for d, mode in dups if mode == "thin"]
            parts = []
            if recast:
                listed = "\n".join(f'  - "{d}"' for d in recast)
                parts.append(
                    "DUPLICATED LINES — each already appears verbatim in an earlier "
                    "chapter. In THIS chapter, recast each one so it carries the same "
                    "meaning in different words, fitted to this scene. Do not simply "
                    "delete them; the beat is needed, the repetition is not:\n" + listed)
            if thin:
                listed = "\n".join(f'  - "{d}"' for d in thin)
                parts.append(
                    "REPEATED WITHIN THIS CHAPTER — each of these appears more than "
                    "once here. Keep the FIRST occurrence exactly as written; recast "
                    "every later one:\n" + listed)
            dedup_block = "\n\n".join(parts) + "\n\n"

        system = SYSTEM.format(
            em_dash_count=stats["counts"]["em_dash"],
            em_dash_ceiling=EM_DASH_CEILING,
            dash="—",
        )
        user = USER.format(protect_block=protect_block, dedup_block=dedup_block,
                           name=path.name, text=text)

        if args.dry_run:
            print(f"{path.name}: {stats['words']:>5} words | "
                  f"em-dash {stats['counts']['em_dash']:>3} -> {EM_DASH_CEILING} | "
                  f"dup lines to recast: {len(dups)} | "
                  f"over-band: {','.join(stats['over_band']) or 'none'}")
            continue

        print(f"{path.name}: editing via {args.provider}/{args.model} ...", flush=True)
        try:
            if args.provider == "ollama":
                response = call_ollama(args.model, system, user, args.timeout,
                                       args.max_tokens)
            else:
                response = call_ofox(args.model, system, user, args.timeout,
                                     args.max_tokens, args.reasoning_effort)
            edited = restore_typography(strip_fence(response))
        except RuntimeError as e:
            print(f"  SKIPPED — {e}")
            failures.append(path.name)
            continue

        # Refuse to write a result that lost the chapter. A truncated or refused
        # edit must never silently replace the author's text.
        before, after = len(text.split()), len(edited.split())
        lost = [m for m in protect_lines
                if normalise(m) in normalise(text) and normalise(m) not in normalise(edited)]
        if after < before * 0.90:
            print(f"  REJECTED — {before} -> {after} words, lost more than 10%")
            failures.append(path.name)
            continue
        if after > before * 1.01:
            print(f"  REJECTED — {before} -> {after} words, local edit expanded the chapter")
            failures.append(path.name)
            continue
        if edited.count("\n# ") != text.count("\n# ") or not edited.startswith("# "):
            print("  REJECTED — markdown chapter structure changed")
            failures.append(path.name)
            continue
        if lost:
            print(f"  REJECTED — protected motif dropped: {lost}")
            failures.append(path.name)
            continue
        # A no-op is a silent failure: the model sometimes echoes the chapter back
        # nearly unchanged. Losing text is not the only way for a pass to be wrong.
        dashes_before, dashes_after = text.count("—"), edited.count("—")
        if dashes_before > EM_DASH_CEILING and dashes_after >= dashes_before * 0.9:
            print(f"  REJECTED — no work done: em-dash {dashes_before} -> {dashes_after}")
            failures.append(path.name)
            continue

        print(f"  {before} -> {after} words ({after - before:+d}), "
              f"em-dash {text.count(chr(8212))} -> {edited.count(chr(8212))}")

        dest = (args.out_dir / path.name) if args.out_dir else path
        if args.out_dir:
            args.out_dir.mkdir(parents=True, exist_ok=True)
        dest.write_text(edited if edited.endswith("\n") else edited + "\n")

    if failures:
        print(f"\n{len(failures)} chapter(s) not written: {', '.join(failures)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
