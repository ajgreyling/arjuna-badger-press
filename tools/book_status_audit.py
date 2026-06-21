#!/usr/bin/env python3
"""Book status auditor — deterministic scoring of every book's real completion state.

Two passes:
  1. DETERMINISTIC (this file, default): scan on-disk artifacts + project.json for every
     CURATED book, compute a state + 0-100 readiness score from hard signals only
     (manuscript line count, chapter files, EPUB/PDF presence, canon depth, cover, publish gate).
  2. METERED API (book_status_judge.py): for books NOT in the live library, an Opus pass
     reads the actual manuscript/canon and returns a true judgement of completion state.

Why deterministic first: project.json `status` fields and the "Coming soon" blurbs drift out of
date (e.g. The Dreaming ships an EPUB while its PROJECT.md still says "scaffolding"). Hard artifact
signals don't lie. The API pass only has to adjudicate the genuinely ambiguous middle.

    python3 tools/book_status_audit.py            # writes book-status-tracker.{md,csv}
    python3 tools/book_status_audit.py --json      # also dump book-status-audit.json (for the API pass)

Pure stdlib. Run from repo root.
"""
from __future__ import annotations

import csv
import importlib.util
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BOOKS = REPO / "books"

# ── import CURATED + gate sets from the site generator (single source of truth) ────────────────
def _load_build():
    spec = importlib.util.spec_from_file_location("abp_build", REPO / "site" / "build.py")
    mod = importlib.util.module_from_spec(spec)
    # build.py reads os.environ for gate overrides; importing is side-effect-free (no __main__).
    spec.loader.exec_module(mod)
    return mod

BUILD = _load_build()
CURATED = BUILD.CURATED
PUBLISHED = BUILD.PUBLISHED
WORKSHOP_HOLD = BUILD.WORKSHOP_HOLD
SERIAL = BUILD.SERIAL
HIDE_BOOKS = BUILD.HIDE_BOOKS
HIDE_SERIES = BUILD.HIDE_SERIES


# ── on-disk signal extraction ──────────────────────────────────────────────────────────────────
@dataclass
class BookSignals:
    cid: str
    title: str
    series: str
    root_rel: str
    root_exists: bool = False
    book_md_lines: int = 0          # build/BOOK.md line count (0 if absent)
    chapter_files: int = 0          # count of chapter-like .md under the book
    manuscript_words: int = 0       # word count across BOOK.md or chapters
    has_epub: bool = False
    has_pdf: bool = False
    canon_files: int = 0            # files under canon/
    has_rich_cover: bool = False    # a cover >= RICH_COVER_MIN_BYTES
    project_status: str = ""        # status field from project.json, if any
    target_words: int = 0
    # gate flags (from build.py)
    published: bool = False
    workshop_hold: bool = False
    serial: bool = False
    hidden: bool = False
    in_curated: bool = True
    # derived
    state: str = ""                 # deterministic state label
    score: int = 0                  # 0-100 readiness
    notes: list[str] = field(default_factory=list)


CHAPTER_RE = re.compile(r"(^|/)(ch[-_]?\d|chapter[-_]?\d|prologue|epilogue)", re.I)
RICH_COVER_MIN = getattr(BUILD, "RICH_COVER_MIN_BYTES", 500_000)


def _wordcount(p: Path) -> int:
    try:
        return len(p.read_text(encoding="utf-8", errors="ignore").split())
    except OSError:
        return 0


def scan(cid: str, title: str, series: str, root_rel: str) -> BookSignals:
    s = BookSignals(cid=cid, title=title, series=series, root_rel=root_rel)
    root = BOOKS / root_rel
    s.root_exists = root.is_dir()

    s.published = cid in PUBLISHED
    s.workshop_hold = cid in WORKSHOP_HOLD
    s.serial = cid in SERIAL
    s.hidden = (cid in HIDE_BOOKS) or (series in HIDE_SERIES)

    if not s.root_exists:
        s.notes.append("root dir missing on disk")
        return s

    # manuscript — prefer a merged BOOK.md, else count chapter md files
    book_md = root / "build" / "BOOK.md"
    if book_md.is_file():
        text = book_md.read_text(encoding="utf-8", errors="ignore")
        s.book_md_lines = text.count("\n") + 1
        s.manuscript_words = len(text.split())

    chap_words = 0
    for md in root.rglob("*.md"):
        rel = md.relative_to(root).as_posix()
        if "/canon/" in f"/{rel}" or rel.startswith("canon/"):
            continue
        if CHAPTER_RE.search(rel):
            s.chapter_files += 1
            chap_words += _wordcount(md)
    if s.manuscript_words == 0:
        s.manuscript_words = chap_words

    # exports
    for ep in root.rglob("*.epub"):
        s.has_epub = True
        break
    for pf in root.rglob("*.pdf"):
        s.has_pdf = True
        break

    # canon depth
    canon = root / "canon"
    if canon.is_dir():
        s.canon_files = sum(1 for f in canon.rglob("*") if f.is_file() and f.suffix == ".md")

    # cover richness
    for cov in list(root.rglob("cover*.png")) + list(root.rglob("cover*.jpg")):
        try:
            if cov.stat().st_size >= RICH_COVER_MIN:
                s.has_rich_cover = True
                break
        except OSError:
            pass

    # project.json status
    for pj in [root / "project.json"] + list(root.glob("**/project.json")):
        if pj.is_file():
            try:
                data = json.loads(pj.read_text(encoding="utf-8", errors="ignore"))
                s.project_status = str(data.get("status", "")).strip()
                s.target_words = int(data.get("target_words", 0) or 0)
            except (OSError, ValueError, json.JSONDecodeError):
                pass
            break

    return s


# ── deterministic state machine ─────────────────────────────────────────────────────────────────
# States, in order of completion:
#   LIVE              — published in the library (download/read live), excluded from API pass
#   SERIAL_LIVE       — published read-online serial
#   BUILT_UNWIRED     — full manuscript + EPUB/PDF, but NOT in CURATED (invisible to library)
#   DRAFTED_GATED     — full manuscript exists, held out of PUBLISHED (catalogue-only / workshop)
#   IN_PROGRESS       — partial manuscript OR canon-complete with no/low prose
#   SCAFFOLD          — cover + metadata only, no manuscript, thin/no canon
#   HIDDEN            — deliberately dropped from the site (HIDE_BOOKS / HIDE_SERIES)
#   MISSING           — CURATED entry whose root dir isn't on disk

DRAFT_WORD_FLOOR = 15_000   # below this, a "manuscript" is partial/stub even if BOOK.md exists


def classify(s: BookSignals) -> None:
    notes = s.notes
    # gates first
    if s.hidden:
        s.state = "HIDDEN"
    elif s.published and s.serial:
        s.state = "SERIAL_LIVE"
    elif s.published:
        s.state = "LIVE"
    elif not s.root_exists:
        s.state = "MISSING"
    else:
        full_manuscript = s.manuscript_words >= DRAFT_WORD_FLOOR
        if full_manuscript and (s.has_epub or s.has_pdf) and not s.in_curated:
            s.state = "BUILT_UNWIRED"
        elif full_manuscript:
            s.state = "DRAFTED_GATED"
        elif s.manuscript_words > 0 or s.chapter_files > 0 or s.canon_files >= 2:
            # any real prose, OR a substantive story bible (>= 2 canon docs) = work has begun
            s.state = "IN_PROGRESS"
        else:
            s.state = "SCAFFOLD"

    # readiness score (0-100), hard signals only
    score = 0
    if s.manuscript_words >= DRAFT_WORD_FLOOR:
        score += 55
    elif s.manuscript_words > 0:
        score += int(35 * min(1.0, s.manuscript_words / DRAFT_WORD_FLOOR))
    elif s.chapter_files > 0:
        score += 10
    if s.canon_files >= 8:
        score += 15
    elif s.canon_files >= 3:
        score += 8
    elif s.canon_files >= 1:
        score += 4
    if s.has_epub:
        score += 12
    if s.has_pdf:
        score += 8
    if s.has_rich_cover:
        score += 10
    s.score = min(100, score)

    # drift detection — stale project.json status vs real artifacts
    ps = s.project_status.lower()
    if ps in ("scaffold", "scaffolding", "bible", "outline") and (s.has_epub or s.manuscript_words >= DRAFT_WORD_FLOOR):
        notes.append(f"STALE project.json status='{s.project_status}' but manuscript/EPUB exists")
    if s.state == "BUILT_UNWIRED":
        notes.append("built (manuscript+export) but absent from CURATED — invisible to library")
    if not s.in_curated and s.state not in ("BUILT_UNWIRED", "MISSING"):
        notes.append("on disk but not in CURATED")


def main() -> int:
    want_json = "--json" in sys.argv

    # build a set of CURATED ids and roots; also discover on-disk book roots NOT in CURATED
    curated_rows = []
    curated_ids = set()
    curated_roots = set()
    for cid, title, sub, series, root_rel, *_ in CURATED:
        # skip regex-noise rows that aren't real (defensive — CURATED is clean, but be safe)
        if "/" in cid or cid.endswith(".png") or cid.endswith(".md"):
            continue
        curated_rows.append((cid, title, series, root_rel))
        curated_ids.add(cid)
        curated_roots.add(root_rel)

    signals: list[BookSignals] = []
    for cid, title, series, root_rel in curated_rows:
        s = scan(cid, title, series, root_rel)
        s.in_curated = True
        classify(s)
        signals.append(s)

    # discover unwired books: a book root is any dir holding a real project marker
    # (build/BOOK.md, a canon/ dir, a manuscript/ dir, or PROJECT.md) that isn't a known
    # CURATED root and isn't nested inside one. Catches both built-but-unwired (The Dreaming)
    # and early in-progress books with no merged BOOK.md yet (The Scramble: manuscript/ch-01.md).
    known_roots = {(BOOKS / r).resolve() for r in curated_roots}
    markers = set()
    for pat in ("build/BOOK.md", "canon", "manuscript", "PROJECT.md"):
        for hit in BOOKS.rglob(pat):
            root = hit.parent.parent if pat == "build/BOOK.md" else hit.parent
            markers.add(root.resolve())

    seen_unwired = set()
    for root in sorted(markers):
        if root in known_roots or root in seen_unwired:
            continue
        # skip anything nested inside a known CURATED root (its parts already counted)
        if any(p in known_roots for p in root.parents):
            continue
        try:
            root_rel = root.relative_to(BOOKS).as_posix()
        except ValueError:
            continue
        if root_rel in curated_roots or "/" not in str(root.relative_to(BOOKS)) and root.name.startswith("_"):
            pass
        cid = root.name
        if cid in curated_ids:
            continue
        seen_unwired.add(root)
        title = cid.replace("-", " ").title()
        proj = root / "PROJECT.md"
        if proj.is_file():
            m = re.search(r"#\s*Project\s*—\s*\*([^*]+)\*", proj.read_text(encoding="utf-8", errors="ignore"))
            if m:
                title = m.group(1).strip()
        s = scan(cid, title, "(unwired — not in CURATED)", root_rel)
        s.in_curated = False
        classify(s)
        signals.append(s)

    # sort: state severity, then score desc
    state_order = {
        "BUILT_UNWIRED": 0, "DRAFTED_GATED": 1, "IN_PROGRESS": 2, "SCAFFOLD": 3,
        "HIDDEN": 4, "MISSING": 5, "SERIAL_LIVE": 6, "LIVE": 7,
    }
    signals.sort(key=lambda s: (state_order.get(s.state, 9), -s.score, s.cid))

    write_outputs(signals, want_json)
    print_summary(signals)
    return 0


def write_outputs(signals: list[BookSignals], want_json: bool) -> None:
    # CSV
    csv_path = REPO / "book-status-tracker.csv"
    cols = ["cid", "title", "series", "state", "score", "manuscript_words", "book_md_lines",
            "chapter_files", "canon_files", "has_epub", "has_pdf", "has_rich_cover",
            "project_status", "published", "in_curated", "root_rel", "notes"]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for s in signals:
            w.writerow([s.cid, s.title, s.series, s.state, s.score, s.manuscript_words,
                        s.book_md_lines, s.chapter_files, s.canon_files, int(s.has_epub),
                        int(s.has_pdf), int(s.has_rich_cover), s.project_status,
                        int(s.published), int(s.in_curated), s.root_rel, "; ".join(s.notes)])

    if want_json:
        (REPO / "book-status-audit.json").write_text(
            json.dumps([asdict(s) for s in signals], indent=2), encoding="utf-8")

    # Markdown tracker (deterministic pass only; API verdict column appended by judge)
    md = render_markdown(signals)
    (REPO / "book-status-tracker.md").write_text(md, encoding="utf-8")


STATE_LABEL = {
    "BUILT_UNWIRED": "🟠 Built, unwired",
    "DRAFTED_GATED": "🟢 Drafted, gated",
    "IN_PROGRESS":   "🟡 In progress",
    "SCAFFOLD":      "⚪ Scaffold",
    "HIDDEN":        "🔒 Hidden",
    "MISSING":       "❌ Missing",
    "SERIAL_LIVE":   "📖 Serial (live)",
    "LIVE":          "✅ Live",
}


def render_markdown(signals: list[BookSignals]) -> str:
    from collections import Counter
    counts = Counter(s.state for s in signals)
    out = []
    out.append("# Book Status Tracker\n")
    out.append("> Auto-generated by `tools/book_status_audit.py` (deterministic pass) + "
               "`tools/book_status_judge.py` (metered Anthropic API pass). **Do not hand-edit the "
               "tables** — rerun the tools. `state` and `score` are from hard on-disk artifact "
               "signals; project.json `status` fields are advisory and often stale.\n")
    out.append("## Summary\n")
    out.append("| State | Count | Meaning |")
    out.append("|---|---:|---|")
    meanings = {
        "BUILT_UNWIRED": "Manuscript + EPUB/PDF exist but the book is **not in CURATED** — invisible to the library.",
        "DRAFTED_GATED": "Full manuscript drafted; held out of `PUBLISHED` (catalogue-only / workshop hold).",
        "IN_PROGRESS": "Partial manuscript, or canon/bible complete with little/no prose.",
        "SCAFFOLD": "Cover + metadata only. No manuscript.",
        "HIDDEN": "Deliberately dropped from the site (HIDE_BOOKS / HIDE_SERIES).",
        "MISSING": "CURATED entry whose root dir isn't on disk.",
        "SERIAL_LIVE": "Published read-online serial.",
        "LIVE": "Published in the library — live downloads/read.",
    }
    for st in ["BUILT_UNWIRED", "DRAFTED_GATED", "IN_PROGRESS", "SCAFFOLD", "HIDDEN", "MISSING", "SERIAL_LIVE", "LIVE"]:
        if counts.get(st):
            out.append(f"| {STATE_LABEL[st]} | {counts[st]} | {meanings[st]} |")
    out.append(f"\n**Total: {len(signals)} books.** Not-yet-live (everything but LIVE/SERIAL): "
               f"{sum(v for k,v in counts.items() if k not in ('LIVE','SERIAL_LIVE'))}.\n")

    # Detail table — focus on not-live books first
    out.append("## Books not yet completed in the library\n")
    out.append("Sorted by completion state, then deterministic readiness score. "
               "The **API verdict** column is filled by the metered judge pass.\n")
    out.append("| Book | id | Series | State | Score | Manuscript | Canon | EPUB/PDF | Cover | API verdict | Notes |")
    out.append("|---|---|---|---|---:|---|---:|---|---|---|---|")
    for s in signals:
        if s.state in ("LIVE", "SERIAL_LIVE"):
            continue
        man = f"{s.manuscript_words:,}w" if s.manuscript_words else (f"{s.chapter_files}ch" if s.chapter_files else "—")
        exp = "/".join(x for x in [("EPUB" if s.has_epub else ""), ("PDF" if s.has_pdf else "")] if x) or "—"
        cov = "rich" if s.has_rich_cover else "stub/—"
        notes = s.notes[0] if s.notes else ""
        out.append(f"| {s.title} | `{s.cid}` | {s.series} | {STATE_LABEL[s.state]} | {s.score} | "
                   f"{man} | {s.canon_files} | {exp} | {cov} | _(pending)_ | {notes} |")

    # Live books, compact, at the bottom for completeness
    out.append("\n<details><summary>Live in the library (excluded from API pass)</summary>\n")
    out.append("\n| Book | id | Series | State | EPUB/PDF |")
    out.append("|---|---|---|---|---|")
    for s in signals:
        if s.state not in ("LIVE", "SERIAL_LIVE"):
            continue
        exp = "/".join(x for x in [("EPUB" if s.has_epub else ""), ("PDF" if s.has_pdf else "")] if x) or "—"
        out.append(f"| {s.title} | `{s.cid}` | {s.series} | {STATE_LABEL[s.state]} | {exp} |")
    out.append("\n</details>\n")
    return "\n".join(out) + "\n"


def print_summary(signals: list[BookSignals]) -> None:
    from collections import Counter
    counts = Counter(s.state for s in signals)
    print(f"\nScanned {len(signals)} books. State breakdown:")
    for st in ["BUILT_UNWIRED", "DRAFTED_GATED", "IN_PROGRESS", "SCAFFOLD", "HIDDEN", "MISSING", "SERIAL_LIVE", "LIVE"]:
        if counts.get(st):
            print(f"  {STATE_LABEL[st]:<22} {counts[st]}")
    flagged = [s for s in signals if any("STALE" in n or "unwired" in n for n in s.notes)]
    if flagged:
        print(f"\n⚠ {len(flagged)} drift/visibility flags:")
        for s in flagged:
            print(f"  {s.cid}: {'; '.join(s.notes)}")
    print(f"\nWrote book-status-tracker.md + .csv")


if __name__ == "__main__":
    sys.exit(main())
