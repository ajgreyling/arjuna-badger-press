#!/usr/bin/env python3
"""Full-send pipeline for *The Antifragile Reader*.

merge → deterministic metrics → cold-read → craft-audit → de-LLM polish (per essay)
→ re-merge → NovelBench prose_quality (per essay) → EPUB/PDF → promote to PUBLISHED.

Metered via OpenRouter (engine.llm_client). Resumable: skips steps whose outputs exist
unless --restart.

  python3 full_send.py              # run all pending steps
  python3 full_send.py --restart    # redo everything
  python3 full_send.py --only polish,render,promote
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRESS = HERE.parents[3]
PLATFORM = PRESS.parent / "arjuna-badger-platform"
BOOK_DIR = HERE / "book"
BUILD = HERE / "build"
CHAPTERS = BUILD / "chapters"
REPORTS = BUILD / "reports"
TITLE = "The Antifragile Reader"
BOOK_ID = "the-antifragile-reader"

for env_path in (PLATFORM / ".env",):
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

sys.path.insert(0, str(PLATFORM))
sys.path.insert(0, str(PLATFORM / "novelbench"))

from engine.cold_read import (  # noqa: E402
    _split_chapters,
    aggregate as cold_aggregate,
    run_slice as cold_run_slice,
)
from engine.craft_audit import (  # noqa: E402
    aggregate as craft_aggregate,
    run_slice as craft_run_slice,
)
from engine.llm_client import call_anthropic, openrouter_enabled  # noqa: E402

YAML = re.compile(r"^---\s*\n.*?\n---\s*\n", re.DOTALL)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log(msg: str) -> None:
    BUILD.mkdir(parents=True, exist_ok=True)
    with (BUILD / "full_send.log").open("a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg, flush=True)


def retry(fn, tries: int = 5):
    last = None
    for attempt in range(tries):
        try:
            return fn()
        except Exception as e:
            last = e
            wait = min(60, 2**attempt * 5)
            log(f"  [retry] {type(e).__name__}: {str(e)[:120]}; sleep {wait}s")
            time.sleep(wait)
    raise last or RuntimeError("call failed")


def essay_files() -> list[Path]:
    return sorted(BOOK_DIR.glob("[0-9][0-9]-*.md"), key=lambda p: p.name)


def prepare_chapters() -> None:
    CHAPTERS.mkdir(parents=True, exist_ok=True)
    outline = {"chapters": []}
    for p in essay_files():
        stem = p.stem
        num = stem[:2]
        slug = stem[3:] if len(stem) > 3 else stem
        cid = f"ch-{num}-{slug}"
        text = YAML.sub("", p.read_text(encoding="utf-8")).strip()
        (CHAPTERS / f"{cid}.md").write_text(text + "\n", encoding="utf-8")
        m = re.match(r"^#\s+(.+)", text)
        title = m.group(1).strip() if m else stem
        outline["chapters"].append({
            "id": cid, "n": int(num), "title": title,
            "beat": f"Essay {num} of The Antifragile Reader",
            "target_words": 950,
        })
    (BUILD / "outline.json").write_text(json.dumps(outline, indent=2), encoding="utf-8")
    log(f"[prepare] {len(outline['chapters'])} chapters -> build/chapters/")


def merge() -> Path:
    import build as book_build  # noqa: WPS433 — local build.py
    return book_build.merge()


def book_slices(whole: bool = True) -> list[dict]:
    md = (BUILD / "BOOK.md").read_text(encoding="utf-8")
    chapters = _split_chapters(md)
    groups = [chapters] if whole else [chapters[i:i + 4] for i in range(0, len(chapters), 4)]
    slices = []
    for g in groups:
        text = "\n\n".join(h + "\n\n" + b.strip() for h, b in g)
        label = f"{TITLE}: " + (g[0][0].replace("#", "").strip()[:40])
        if len(g) > 1:
            label += f" … {g[-1][0].replace('#', '').strip()[:40]}"
        slices.append({
            "label": label,
            "text": text,
            "chapters": [re.sub(r"^#\s+", "", h).strip() for h, _ in g],
        })
    return slices


def deterministic_metrics() -> dict:
    from prose_metrics import analyze  # type: ignore

    text = (BUILD / "BOOK.md").read_text(encoding="utf-8")
    m = analyze(text)
    REPORTS.mkdir(parents=True, exist_ok=True)
    out = REPORTS / "deterministic-metrics.json"
    out.write_text(json.dumps(m, indent=2), encoding="utf-8")
    log(f"[metrics] overall sub-scores: {m.get('scores', {})} -> {out.name}")
    return m


def _render_findings(title: str, kind: str, agg: dict, risk_key: str) -> str:
    L = [
        f"# {title}",
        f"> Generated {utc_now()}.",
        f"> Risk: **{agg.get(risk_key, 'unknown')}**. "
        f"{len(agg.get('craft', []))} craft · {len(agg.get('canon', []))} canon.",
        "",
    ]
    for bucket in ("craft", "canon"):
        L.append(f"## {bucket.upper()} findings")
        items = agg.get(bucket, [])
        if not items:
            L.append("_(none)_\n")
            continue
        for f in items:
            L.append(f"### [{f.get('severity','?')}] {f.get('category','?')}")
            L.append(f"- **where:** {f.get('where','?')}")
            if f.get("quote"):
                L.append(f"- **quote:** \"{str(f['quote'])[:300]}\"")
            L.append(f"- **problem:** {f.get('problem','').strip()}")
            L.append(f"- **fix:** {f.get('fix','').strip()}\n")
    return "\n".join(L) + "\n"


def cold_read(restart: bool) -> dict:
    out_md = REPORTS / "cold-read.md"
    out_json = REPORTS / "cold-read.json"
    if out_json.exists() and not restart:
        log("[skip] cold-read (cached)")
        return json.loads(out_json.read_text(encoding="utf-8"))
    slices = book_slices(whole=True)
    log(f"[cold-read] {len(slices)} slice(s) via {'openrouter' if openrouter_enabled() else 'direct'}")
    reports = [retry(lambda sl=sl: cold_run_slice(sl)) for sl in slices]
    agg = cold_aggregate(reports)
    REPORTS.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(agg, indent=2), encoding="utf-8")
    out_md.write_text(_render_findings(f"Cold-read — {TITLE}", "cold-read", agg, "machine_risk"), encoding="utf-8")
    log(f"[cold-read] machine-risk={agg['machine_risk']} craft={len(agg['craft'])} -> {out_md.name}")
    return agg


def craft_audit(restart: bool) -> dict:
    out_md = REPORTS / "craft-audit.md"
    out_json = REPORTS / "craft-audit.json"
    if out_json.exists() and not restart:
        log("[skip] craft-audit (cached)")
        return json.loads(out_json.read_text(encoding="utf-8"))
    style = (HERE / "canon" / "STYLE_GUIDE.md").read_text(encoding="utf-8")
    voice_laws = (
        "\nThe companion's voice contract (STYLE_GUIDE — judge homogenization, register, "
        "living-author rule compliance):\n\n" + style
    )
    slices = book_slices(whole=True)
    log(f"[craft-audit] {len(slices)} slice(s)")
    reports = [retry(lambda sl=sl: craft_run_slice(sl, voice_laws)) for sl in slices]
    agg = craft_aggregate(reports)
    REPORTS.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(agg, indent=2), encoding="utf-8")
    out_md.write_text(_render_findings(f"Craft audit — {TITLE}", "craft-audit", agg, "craft_risk"), encoding="utf-8")
    log(f"[craft-audit] craft-risk={agg['craft_risk']} craft={len(agg['craft'])} -> {out_md.name}")
    return agg


def _findings_text(cold: dict, craft: dict) -> str:
    lines = ["## Cold-read craft findings (apply where relevant)"]
    for f in cold.get("craft", [])[:25]:
        lines.append(
            f"- [{f.get('severity')}] {f.get('category')}: {f.get('problem','')[:200]} "
            f"→ {f.get('fix','')[:200]}"
        )
    lines.append("\n## Craft-audit findings (apply where relevant)")
    for f in craft.get("craft", [])[:25]:
        lines.append(
            f"- [{f.get('severity')}] {f.get('category')}: {f.get('problem','')[:200]} "
            f"→ {f.get('fix','')[:200]}"
        )
    return "\n".join(lines)


def de_llm_polish(restart: bool, cold: dict, craft: dict) -> int:
    de_llm = (PLATFORM / "prompts" / "de-llm-pass.md").read_text(encoding="utf-8")[:6000]
    style = (HERE / "canon" / "STYLE_GUIDE.md").read_text(encoding="utf-8")
    findings = _findings_text(cold, craft)
    polished_dir = BUILD / "polished"
    polished_dir.mkdir(parents=True, exist_ok=True)
    n = 0
    for p in essay_files():
        out = polished_dir / p.name
        if out.exists() and not restart:
            log(f"[skip] polish {p.name} (cached)")
            BOOK_DIR.joinpath(p.name).write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
            continue
        essay = YAML.sub("", p.read_text(encoding="utf-8")).strip()
        prompt = f"""You are the line editor for *The Antifragile Reader*. Return ONLY the finished essay
markdown — no commentary. Surgical de-LLM pass: thin machine tells, keep voice and structure.

STYLE GUIDE (binding):
{style}

DE-LLM RUBRIC (excerpt):
{de_llm}

EDITORIAL FINDINGS (verify each in this essay before acting; skip what does not apply):
{findings}

ESSAY TO POLISH:
{essay}

Rules:
- Keep the four beats: ### The fire · Where the smoke goes · Plainly · The line
- Keep **`plainly:`** markers
- Living-author rule: no long Taleb quotes; paraphrase + attribute
- Do not change ideas or add essays; line-level craft only
- First line must remain the essay H1
"""
        system = "Surgical prose editor. Markdown essay output only. House companion voice."
        revised = retry(lambda: call_anthropic(prompt, max_tokens=8192, system=system).strip())
        if not revised.startswith("#"):
            revised = essay  # safety fallback
        out.write_text(revised + "\n", encoding="utf-8")
        p.write_text(revised + "\n", encoding="utf-8")
        log(f"[polish] {p.name} ({len(revised.split())} words)")
        n += 1
    return n


def novelbench_score(restart: bool) -> dict:
    from manuscript import Chapter  # type: ignore
    from scorers import score_dimension  # type: ignore

    out = REPORTS / "novelbench-scores.json"
    if out.exists() and not restart:
        log("[skip] novelbench (cached)")
        return json.loads(out.read_text(encoding="utf-8"))

    dims = ("prose_quality", "reader_experience")
    chapters_scored = []
    for f in sorted(CHAPTERS.glob("ch-*.md")):
        text = f.read_text(encoding="utf-8").strip()
        m = re.match(r"^#\s+(.+)", text)
        ch = Chapter(
            id=f.stem, number=f.stem[3:5], title=m.group(1).strip() if m else f.stem,
            text=text, words=len(text.split()), path=f, intent={},
        )
        log(f"[novelbench] {ch.id} ({ch.words}w) — {', '.join(dims)}")
        dim_res = {}
        for d in dims:
            dim_res[d] = retry(lambda d=d: score_dimension(d, ch))
        scores = [dim_res[d].get("score") for d in dims if isinstance(dim_res[d].get("score"), (int, float))]
        overall = round(sum(scores) / len(scores), 1) if scores else None
        chapters_scored.append({"id": ch.id, "title": ch.title, "words": ch.words,
                                "dimensions": dim_res, "overall": overall})
    book_overall = round(
        sum(c["overall"] for c in chapters_scored if c["overall"]) / max(1, len(chapters_scored)), 1
    )
    payload = {"scored_at": utc_now(), "chapters": chapters_scored, "book_overall": book_overall}
    REPORTS.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    log(f"[novelbench] book_overall={book_overall}/10 -> {out.name}")
    return payload


def render() -> None:
    import build as book_build  # noqa: WPS433
    book_build.render(book_build.merge())


def promote() -> None:
    site = PRESS / "site" / "build.py"
    text = site.read_text(encoding="utf-8")
    serial_pat = r'"dust-throne,bloedrivier,the-antifragile-reader,palindrome"'
    if serial_pat.replace("the-antifragile-reader,", "") in text or "the-antifragile-reader,palindrome" in text:
        text = text.replace(
            '"dust-throne,bloedrivier,the-antifragile-reader,palindrome"',
            '"dust-throne,bloedrivier,palindrome"',
        )
    if f'"{BOOK_ID}"' not in text.split("PUBLISHED")[1][:4000]:
        text = text.replace(
            '"the-song-of-the-self,wrath-of-achilles,walls-of-uruk,"',
            '"the-song-of-the-self,wrath-of-achilles,walls-of-uruk,the-antifragile-reader,"',
        )
    text = text.replace(
        '"Nassim Taleb\'s Incerto, plainly told · An open draft"',
        '"Nassim Taleb\'s Incerto, plainly told"',
        1,
    )
    text = text.replace(
        "Published here as an open, in-progress draft — the proem and two essays are the finished voice; "
        "the rest is being written. Independent and unaffiliated with the author.",
        "A reverent guest-at-the-fire companion in the house voice: his ideas attributed and his prose "
        "left to him, the author's own plain glosses always marked. Independent and unaffiliated with the author.",
        1,
    )
    site.write_text(text, encoding="utf-8")
    log("[promote] removed SERIAL, added PUBLISHED, updated shelf copy")


def rebuild_site() -> None:
    subprocess.run([sys.executable, str(PRESS / "site" / "build.py")], check=True, cwd=PRESS)
    refresh = PRESS / "tools" / "refresh_deliverables.sh"
    if refresh.is_file():
        subprocess.run(["bash", str(refresh)], check=True, cwd=PRESS)
    log("[site] rebuilt + deliverables refreshed")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--restart", action="store_true")
    ap.add_argument("--only", help="comma steps: prepare,merge,metrics,cold,craft,polish,novelbench,render,promote,site")
    args = ap.parse_args()
    steps = set(args.only.split(",")) if args.only else {
        "prepare", "merge", "metrics", "cold", "craft", "polish", "novelbench", "render", "promote", "site",
    }

    if not openrouter_enabled() and not os.environ.get("ANTHROPIC_API_KEY"):
        log("[fail] no API keys")
        return 1

    log(f"[full_send] {TITLE} · backend={'openrouter' if openrouter_enabled() else 'direct'}")

    cold = craft = {}
    if "prepare" in steps:
        prepare_chapters()
    if "merge" in steps:
        merge()
    if "metrics" in steps:
        deterministic_metrics()
    if "cold" in steps:
        cold = cold_read(args.restart)
    if "craft" in steps:
        craft = craft_audit(args.restart)
    if "polish" in steps:
        if not cold:
            cold = json.loads((REPORTS / "cold-read.json").read_text(encoding="utf-8"))
        if not craft:
            craft = json.loads((REPORTS / "craft-audit.json").read_text(encoding="utf-8"))
        de_llm_polish(args.restart, cold, craft)
        merge()
    if "novelbench" in steps:
        novelbench_score(args.restart)
    if "render" in steps:
        render()
    if "promote" in steps:
        promote()
    if "site" in steps:
        rebuild_site()

    log("[full_send] done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
