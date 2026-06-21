#!/usr/bin/env python3
"""Subject sensitivity read of *NULL HORIZON* — Gary McKinnon lens (metered Opus).

Reads the manuscript on behalf of Gary McKinnon as the living real person depicted: dignity,
consent, factual record, autism/health context, extradition trauma, and whether the fiction
honours or exploits what he actually lived through.

NOT a substitute for Gary McKinnon (or his family / legal representatives) reading the book
and granting or withholding consent. This clears what a careful model can flag before that
human gate.

Run (from platform repo root, .env with ANTHROPIC_API_KEY):
  python3 books/altas-resonance-engine/books/non-terrestrial-officers/.sensitivity_read.py
  python3 .../.sensitivity_read.py --whole     # one call (~12k words)
  python3 .../.sensitivity_read.py --chunk 6   # per-slice (default)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
BUILD = HERE / "build"
REPORTS = BUILD / "reports"

sys.path.insert(0, str(ROOT))


def load_env() -> None:
    for p in (HERE, *HERE.parents):
        env = p / ".env"
        if not env.is_file():
            continue
        for line in env.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
        return


load_env()

from engine.llm_client import call_anthropic  # noqa: E402

CONTRACT = """THE BOOK'S STATED CONTRACT (judge against this first):
- Dedicated to Gary McKinnon — "who looked when looking was expensive… never required to recant."
- Front matter: Gary McKinnon is a REAL person. Chapters 1–14 + epilogue draw on documented public record.
  Serpo exchange (ch 15–21) is LEGEND dramatised as fiction. Chapter 99 audits Real / Debated / Invented / Legend.
- Prose "believes on the page" what McKinnon said he found (NTO, fleet-to-fleet, spreadsheets, Building 8).
  Chapter 99 "believes nothing" — the conscience / audit chapter.
- Medical context in the public record: Asperger's / autism spectrum cited in UK extradition & health arguments.
- Legal record (Real): Feb 2001–Mar 2002 access from North London; 97 systems alleged; extradition fight
  2005–2012; Theresa May blocked extradition Oct 2012; CPS no UK charges Dec 2012."""

LENS = {
    "who": "Gary McKinnon — the real person, now in his 60s, who lived this case",
    "expertise": (
        "a subject-rights and living-portrait sensitivity reader specialising in real-people fiction, "
        "autism representation in legal/medical contexts, and UK extradition trauma — reading AS IF on "
        "behalf of Gary McKinnon and what would wound, misrepresent, or exploit him if he read this book"
    ),
    "watch": (
        "SUBJECT DIGNITY & CONSENT: Is he used as a UFO prop without interiority? Does the dedication "
        "match the treatment? Would he feel honoured or mined?\n"
        "FACTUAL RECORD: Errors about dates, legal stages, system counts, quotes, family, location, "
        "handle 'Solo', CPS/May decisions — anything he'd correct publicly.\n"
        "AUTISM / HEALTH: Asperger's in extradition context — caricature, inspiration-porn, 'awkward hacker' "
        "trope, or dignified? Medical vulnerability used for plot thrills?\n"
        "EXTRADITION TRAUMA: Sensationalised suffering? US prosecution framing fair? Mental-health stakes "
        "rendered with dignity or as spectacle?\n"
        "UFO / 'CRANK' FRAMING: Does the book trap him as a conspiracy mascot? Is debunking / sceptic media "
        "pattern (ch 22) fair to how he experiences it? Does ch-99 audit protect him or side against him?\n"
        "PRIVATE LIFE: Invented domestic scenes, partner 'Janis', dialogue — do they violate plausible privacy "
        "or invent intimacy he'd reject?\n"
        "SERPO FICTION (ch 15–21): Is the boundary clear enough that readers won't attribute legend to him? "
        "Does Movement II harm his real claims by association?\n"
        "CULTURAL / TONE: 'Hamba kahle', Glasgow/Crouch End, class and nationality — false notes?\n"
        "Credit what the book does WELL for him (agency, audit chapter, not requiring recant, etc.)."
    ),
}

SYSTEM = (
    "You are {expertise}. You protect a living person from harmful misrepresentation in fiction "
    "about his life. Be honest, specific, neither performatively harsh nor reassuring. Quote the text. "
    "Reserve severity 'harm' for misrepresentation he would find genuinely wounding or factual errors "
    "about his public record. Output ONE fenced ```json block and nothing else."
)

PROMPT = """Read this manuscript slice as a sensitivity reader for {who}.

{contract}

WATCH FOR (Gary McKinnon lens):
{watch}

Severity:
- "harm": factual error about his record, exploitative misrepresentation, or something likely to wound him
- "concern": tone risk, cliché, consent grey area, fix before sending him a copy
- "note": minor preference

Also note what serves him well (done_well).

```json
{{
  "lens": "gary_mckinnon",
  "verdict": "one sentence — would this book pass a subject-rights bar for Gary McKinnon, with caveats?",
  "publication_risk": "low | medium | high",
  "consent_recommendation": "send_for_review | do_not_contact_without_fixes | author_discretion",
  "findings": [
    {{"severity":"harm|concern|note","where":"chapter/scene","quote":"exact text","problem":"…","fix":"…"}}
  ],
  "done_well": ["…"]
}}
```

SLICE ({slice_label}):
{slice_text}"""


def split_chapters(md: str) -> list[tuple[str, str]]:
    parts = re.split(r"(?m)^(#\s+.+)$", md)
    out: list[tuple[str, str]] = []
    it = iter(parts[1:])
    for h in it:
        out.append((h.strip(), next(it, "")))
    while out and re.search(
        r"copyright|all rights|first published|note before you begin|null horizon\s*$",
        out[0][1],
        re.I,
    ):
        out.pop(0)
    return out


def extract_json(raw: str) -> dict:
    m = re.search(r"```json\s*(.*?)```", raw, re.S)
    blob = (m.group(1) if m else raw).strip()
    if not blob.startswith("{"):
        a, b = blob.find("{"), blob.rfind("}")
        blob = blob[a : b + 1] if a >= 0 else "{}"
    try:
        return json.loads(blob)
    except json.JSONDecodeError:
        return {"_parse_error": raw[:800]}


def aggregate(results: list[dict]) -> dict:
    agg: dict = {"harm": [], "concern": [], "note": [], "done_well": [], "verdicts": []}
    for r in results:
        agg["verdicts"].append(
            {
                "slice": r.get("slice"),
                "risk": r.get("publication_risk"),
                "verdict": r.get("verdict"),
                "consent": r.get("consent_recommendation"),
            }
        )
        for f in r.get("findings", []):
            sev = f.get("severity", "note")
            row = dict(f)
            row["slice"] = r.get("slice")
            agg.setdefault(sev, []).append(row)
        for d in r.get("done_well", []):
            agg["done_well"].append(f"[{r.get('slice', '?')}] {d}")
    return agg


def write_report(agg: dict, results: list[dict]) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M")
    (REPORTS / "sensitivity-read-mckinnon.json").write_text(
        json.dumps({"generated": ts, "results": results, "aggregate": agg}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    lines = [
        "# Subject sensitivity read — *NULL HORIZON* (Gary McKinnon lens)",
        "",
        f"> Metered Opus read · generated {ts}Z",
        "> **Not a substitute for Gary McKinnon (or his representatives) reading the book.**",
        "This flags misrepresentation, factual record errors, and dignity risks a model can catch.",
        "",
        f"## Verdicts ({len(agg['verdicts'])} slice(s))",
        "",
    ]
    for v in agg["verdicts"]:
        lines.append(
            f"- **{v.get('slice', '?')}** — risk **{v.get('risk', '?')}** — "
            f"consent: *{v.get('consent', '?')}* — {v.get('verdict', '')}"
        )
    for sev, head in [
        ("harm", "Harm — fix before publication or before sending him a copy"),
        ("concern", "Concern — author should reconsider"),
        ("note", "Note — minor"),
    ]:
        items = agg.get(sev, [])
        lines.extend(["", f"## {head} ({len(items)})", ""])
        if not items:
            lines.append("- (none)")
            continue
        for f in items:
            lines.append(f"- **[{f.get('slice')}]** ({f.get('where')}) {f.get('problem', '')}")
            if f.get("quote"):
                lines.append(f'  - “{str(f["quote"])[:220]}”')
            if f.get("fix"):
                lines.append(f"  - fix: {f.get('fix')}")
    lines.extend(["", f"## Done well ({len(agg['done_well'])})", ""])
    lines.extend(f"- {d}" for d in agg["done_well"][:30])
    (BUILD / "SENSITIVITY_READ_MCKINNON.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--whole", action="store_true", help="single-call read (~12k words)")
    ap.add_argument("--chunk", type=int, default=6)
    args = ap.parse_args()

    book = BUILD / "BOOK.md"
    if not book.is_file():
        sys.exit(f"{book} not found")

    chs = split_chapters(book.read_text(encoding="utf-8"))
    groups = [chs] if args.whole else [chs[i : i + args.chunk] for i in range(0, len(chs), args.chunk)]
    slices: list[tuple[str, str]] = []
    for g in groups:
        label = re.sub(r"^#\s+", "", g[0][0])[:36]
        if len(g) > 1:
            label += f" … {re.sub(r'^#\\s+', '', g[-1][0])[:36]}"
        text = "\n\n".join(h + "\n\n" + b.strip() for h, b in g)
        slices.append((label, text))

    state_path = BUILD / ".sensitivity.mckinnon.state.json"
    state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.is_file() else {}
    results: list[dict] = []

    sysmsg = SYSTEM.format(expertise=LENS["expertise"])
    for si, (slabel, stext) in enumerate(slices):
        key = f"mckinnon|{si}"
        if key in state:
            print(f"  cached {slabel}", flush=True)
            results.append(state[key])
            continue
        print(f"  [{si + 1}/{len(slices)}] Gary McKinnon lens — {slabel} …", flush=True)
        prompt = PROMPT.format(
            who=LENS["who"],
            contract=CONTRACT,
            watch=LENS["watch"],
            slice_label=slabel,
            slice_text=stext,
        )
        try:
            raw = call_anthropic(prompt, system=sysmsg, max_tokens=8000)
            rec = extract_json(raw)
        except Exception as e:
            rec = {"_error": f"{type(e).__name__}: {e}"}
        rec.update({"lens": "gary_mckinnon", "provider": "anthropic", "slice": slabel})
        state[key] = rec
        state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
        results.append(rec)
        time.sleep(1)

    agg = aggregate(results)
    write_report(agg, results)
    nh, nc = len(agg.get("harm", [])), len(agg.get("concern", []))
    print(
        f"\n✓ build/SENSITIVITY_READ_MCKINNON.md — {nh} harm, {nc} concern, "
        f"{len(agg.get('note', []))} note",
        flush=True,
    )


if __name__ == "__main__":
    main()
