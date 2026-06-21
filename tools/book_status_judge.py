#!/usr/bin/env python3
"""Book status judge — metered Anthropic API pass over the deterministic audit.

Reads book-status-audit.json (from book_status_audit.py --json) and, for every book NOT
already live in the library, has claude-opus-4-8 READ the actual manuscript + canon and
return a true judgement of completion state — does real, finished prose exist, or is the
BOOK.md a stub / outline / placeholder the line-count can't distinguish?

The deterministic pass counts artifacts; this pass reads them. It is the arbiter for the
ambiguous middle (a 1,400-line BOOK.md could be a finished novella or 1,400 lines of outline).

    # from repo root, with the key available:
    export ANTHROPIC_API_KEY=$(grep -E '^ANTHROPIC_API_KEY=' ../arjuna-badger-platform/.env | cut -d= -f2-)
    export OPENAI_API_KEY=$(grep -E '^OPENAI_API_KEY=' ../arjuna-badger-platform/.env | cut -d= -f2-)
    python3 tools/book_status_judge.py                       # Anthropic (default), all non-live books
    python3 tools/book_status_judge.py --provider openai      # OpenAI gpt-5 route (Anthropic acct out of credit)
    python3 tools/book_status_judge.py --limit 3              # first 3 only (smoke test)
    python3 tools/book_status_judge.py --only the-dreaming,the-scramble

Writes verdicts into book-status-judgements.json and merges the API verdict column into
book-status-tracker.md (the table the deterministic pass left as _(pending)_).

Cost: one Opus call per non-live book. Manuscript is truncated to MANUSCRIPT_CHARS to bound
tokens; the model is told when it's seeing a head+tail sample vs the whole thing.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BOOKS = REPO / "books"
AUDIT_JSON = REPO / "book-status-audit.json"
JUDGE_JSON = REPO / "book-status-judgements.json"
TRACKER_MD = REPO / "book-status-tracker.md"

# Provider routes. Anthropic is the intended judge (claude-opus-4-8) but the direct account
# was out of credit at build time; OpenAI (gpt-5) is the working fallback. Same prompt/schema
# both ways — only the transport differs.
MODELS = {
    "anthropic": "claude-opus-4-8",
    "openai": "gpt-5",
}
# Rough list prices ($/M tokens) for the cost estimate footer.
PRICES = {
    "claude-opus-4-8": (15.0, 75.0),
    "gpt-5": (1.25, 10.0),
}
# Full-manuscript read: the largest book on disk is ~340KB (~85k tokens), well inside the
# judge models' context windows, so we send the WHOLE manuscript and only fall back to a
# head+tail sample for anything pathologically large. A complete read is the point of this pass.
MANUSCRIPT_CHARS = 400_000
CANON_CHARS = 8_000

LIVE_STATES = {"LIVE", "SERIAL_LIVE"}

SYSTEM = """You are the completion auditor for Arjuna Badger Press, an independent novel imprint.
Your job is to judge how finished a book ACTUALLY is by reading its manuscript and story bible —
not by trusting any status label. A book may carry a stale "scaffolding" tag while shipping a
finished EPUB, or a long BOOK.md that turns out to be an outline, not prose.

You will be given, per book: hard on-disk facts (word counts, exports), the story bible (canon)
sample, and a manuscript sample (head + tail if long). Judge the manuscript on whether it is
REAL, CONTINUOUS, FINISHED NARRATIVE PROSE — sentences and scenes a reader would read — versus
notes, outline beats, headers, or placeholder text.

Return a single JSON object, no prose around it:
{
  "verdict": one of "FINISHED_BOOK" | "FULL_DRAFT" | "PARTIAL_DRAFT" | "OUTLINE_OR_BIBLE_ONLY" | "BARE_SCAFFOLD" | "EMPTY",
  "completion_pct": integer 0-100 (your honest estimate of how much of a finished book exists),
  "prose_is_real": boolean (true only if the manuscript sample is genuine narrative prose, not notes/outline),
  "one_line": a single sentence stating the real state in the house's plain voice,
  "blocking": short phrase naming what stands between this and shippable (e.g. "needs ending", "canon only, no prose", "polished, just ungated"),
  "confidence": "high" | "medium" | "low"
}

Definitions:
- FINISHED_BOOK: complete, polished, has a real beginning/middle/end. Could ship today on prose grounds.
- FULL_DRAFT: whole story is drafted start to finish but may want a polish/line pass.
- PARTIAL_DRAFT: real prose exists but the book is unfinished (missing chapters / no ending).
- OUTLINE_OR_BIBLE_ONLY: substantial planning (story bible, outline) but little or no actual prose.
- BARE_SCAFFOLD: cover + metadata only; essentially nothing to read.
- EMPTY: nothing usable on disk.
Be skeptical. If the sample is mostly headers, beats, or bracketed notes, it is NOT real prose."""


def read_manuscript(root: Path) -> tuple[str, bool]:
    """Return (sampled_text, truncated?). Prefer build/BOOK.md, else concatenated chapter md."""
    book_md = root / "build" / "BOOK.md"
    text = ""
    if book_md.is_file():
        text = book_md.read_text(encoding="utf-8", errors="ignore")
    else:
        chaps = []
        for sub in ("manuscript", "build/chapters", "chapters"):
            d = root / sub
            if d.is_dir():
                for md in sorted(d.glob("*.md")):
                    chaps.append(f"\n\n===== {md.name} =====\n" + md.read_text(encoding="utf-8", errors="ignore"))
        text = "".join(chaps)
    if not text.strip():
        return "", False
    if len(text) <= MANUSCRIPT_CHARS:
        return text, False
    head = text[: MANUSCRIPT_CHARS // 2]
    tail = text[-MANUSCRIPT_CHARS // 2:]
    return head + "\n\n[...MIDDLE OMITTED — sampled head + tail...]\n\n" + tail, True


def read_canon(root: Path) -> str:
    canon = root / "canon"
    if not canon.is_dir():
        return ""
    parts = []
    for md in sorted(canon.glob("*.md")):
        body = md.read_text(encoding="utf-8", errors="ignore")
        parts.append(f"--- {md.name} ---\n{body[:1500]}")
        if sum(len(p) for p in parts) > CANON_CHARS:
            break
    return "\n\n".join(parts)[:CANON_CHARS]


def build_prompt(s: dict) -> str:
    root = BOOKS / s["root_rel"]
    manuscript, truncated = read_manuscript(root)
    canon = read_canon(root)
    facts = (
        f"id: {s['cid']}\n"
        f"title: {s['title']}\n"
        f"series: {s['series']}\n"
        f"deterministic_state: {s['state']}\n"
        f"deterministic_score: {s['score']}/100\n"
        f"manuscript_words (counted on disk): {s['manuscript_words']:,}\n"
        f"chapter_files: {s['chapter_files']}\n"
        f"canon_files: {s['canon_files']}\n"
        f"has_epub: {s['has_epub']}  has_pdf: {s['has_pdf']}\n"
        f"project.json status (advisory, may be stale): {s['project_status'] or '(none)'}\n"
    )
    man_block = manuscript if manuscript.strip() else "(NO MANUSCRIPT PROSE ON DISK)"
    sample_note = " [HEAD+TAIL SAMPLE of a longer file]" if truncated else " [COMPLETE manuscript]"
    canon_block = canon if canon.strip() else "(no canon/ directory)"
    return (
        f"HARD ON-DISK FACTS:\n{facts}\n"
        f"STORY BIBLE / CANON (sampled):\n{canon_block}\n\n"
        f"MANUSCRIPT{sample_note}:\n{man_block}\n\n"
        f"Judge the true completion state. Return only the JSON object."
    )


def _call_anthropic(client, model, prompt):
    resp = client.messages.create(
        model=model, max_tokens=1024, system=SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text").strip()
    return raw, {"in": resp.usage.input_tokens, "out": resp.usage.output_tokens}


def _call_openai(client, model, prompt):
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": SYSTEM},
                  {"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    raw = (resp.choices[0].message.content or "").strip()
    u = resp.usage
    return raw, {"in": u.prompt_tokens, "out": u.completion_tokens}


def judge_one(client, provider: str, model: str, s: dict) -> dict:
    prompt = build_prompt(s)
    caller = _call_openai if provider == "openai" else _call_anthropic
    raw, usage = caller(client, model, prompt)
    m = re.search(r"\{.*\}", raw, re.S)
    if not m:
        return {"verdict": "ERROR", "one_line": f"unparseable: {raw[:120]}", "_usage": usage}
    try:
        v = json.loads(m.group(0))
    except json.JSONDecodeError:
        return {"verdict": "ERROR", "one_line": f"bad json: {raw[:120]}", "_usage": usage}
    v["_usage"] = usage
    return v


VERDICT_LABEL = {
    "FINISHED_BOOK": "✅ Finished book",
    "FULL_DRAFT": "🟢 Full draft",
    "PARTIAL_DRAFT": "🟡 Partial draft",
    "OUTLINE_OR_BIBLE_ONLY": "📐 Bible/outline only",
    "BARE_SCAFFOLD": "⚪ Bare scaffold",
    "EMPTY": "∅ Empty",
    "ERROR": "⚠ error",
}


def merge_into_tracker(judgements: dict, model: str = "") -> None:
    """Replace the _(pending)_ API-verdict cells in book-status-tracker.md."""
    if not TRACKER_MD.is_file():
        return
    lines = TRACKER_MD.read_text(encoding="utf-8").splitlines()
    out = []
    for line in lines:
        m = re.match(r"^\| .*? \| `([^`]+)` \|", line)
        if m and "_(pending)_" in line:
            cid = m.group(1)
            v = judgements.get(cid)
            if v:
                label = VERDICT_LABEL.get(v.get("verdict", "ERROR"), v.get("verdict", "?"))
                pct = v.get("completion_pct", "")
                cell = f"{label} {pct}% — {v.get('one_line','').strip()}"
                cell = cell.replace("|", "\\|")
                line = line.replace("_(pending)_", cell)
        # stamp the judging model into the header note
        if model and "metered Anthropic API pass" in line:
            line = line.replace("metered Anthropic API pass",
                                f"metered API pass — judged by `{model}`")
        out.append(line)
    text = "\n".join(out) + "\n"
    TRACKER_MD.write_text(text, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", choices=["anthropic", "openai"], default="anthropic",
                    help="judge model provider (default anthropic; use openai when the Anthropic account is out of credit)")
    ap.add_argument("--model", default="", help="override the model id for the chosen provider")
    ap.add_argument("--limit", type=int, default=0, help="judge only first N non-live books")
    ap.add_argument("--only", default="", help="comma-separated ids to judge")
    ap.add_argument("--dry-run", action="store_true", help="list what would be judged, no API calls")
    args = ap.parse_args()

    if not AUDIT_JSON.is_file():
        print("error: book-status-audit.json missing. Run: python3 tools/book_status_audit.py --json", file=sys.stderr)
        return 1
    audit = json.loads(AUDIT_JSON.read_text(encoding="utf-8"))

    only = {x.strip() for x in args.only.split(",") if x.strip()}
    targets = [s for s in audit if s["state"] not in LIVE_STATES]
    if only:
        targets = [s for s in targets if s["cid"] in only]
    if args.limit:
        targets = targets[: args.limit]

    provider = args.provider
    model = args.model or MODELS[provider]
    print(f"{len(targets)} non-live books to judge with {model} (provider: {provider}).")
    if args.dry_run:
        for s in targets:
            print(f"  {s['cid']:<26} {s['state']:<16} {s['manuscript_words']:>7,}w")
        return 0

    if provider == "openai":
        if not os.environ.get("OPENAI_API_KEY"):
            print("error: OPENAI_API_KEY not set. e.g.\n"
                  "  export OPENAI_API_KEY=$(grep -E '^OPENAI_API_KEY=' "
                  "../arjuna-badger-platform/.env | cut -d= -f2-)", file=sys.stderr)
            return 1
        from openai import OpenAI
        client = OpenAI()
    else:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            print("error: ANTHROPIC_API_KEY not set. e.g.\n"
                  "  export ANTHROPIC_API_KEY=$(grep -E '^ANTHROPIC_API_KEY=' "
                  "../arjuna-badger-platform/.env | cut -d= -f2-)", file=sys.stderr)
            return 1
        import anthropic
        client = anthropic.Anthropic()

    judgements = {}
    if JUDGE_JSON.is_file():
        judgements = json.loads(JUDGE_JSON.read_text(encoding="utf-8"))

    tot_in = tot_out = 0
    for i, s in enumerate(targets, 1):
        print(f"[{i}/{len(targets)}] {s['cid']:<26} ", end="", flush=True)
        try:
            v = judge_one(client, provider, model, s)
        except Exception as e:  # noqa: BLE001 — report and continue, don't lose prior verdicts
            print(f"ERROR: {e}")
            v = {"verdict": "ERROR", "one_line": str(e)[:160]}
        u = v.pop("_usage", {})
        tot_in += u.get("in", 0)
        tot_out += u.get("out", 0)
        v["det_state"] = s["state"]
        v["det_score"] = s["score"]
        v["title"] = s["title"]
        v["judged_by"] = model
        judgements[s["cid"]] = v
        print(f"{v.get('verdict','?'):<24} {v.get('completion_pct','?')}%  — {v.get('one_line','')[:70]}")
        # persist incrementally so a mid-run failure never loses work
        JUDGE_JSON.write_text(json.dumps(judgements, indent=2), encoding="utf-8")

    merge_into_tracker(judgements, model)

    pin, pout = PRICES.get(model, (0.0, 0.0))
    cost = tot_in / 1e6 * pin + tot_out / 1e6 * pout
    print(f"\nTokens: {tot_in:,} in / {tot_out:,} out  (~${cost:.2f} at {model} list price)")
    print(f"Wrote book-status-judgements.json and merged verdicts into book-status-tracker.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
