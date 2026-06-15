#!/usr/bin/env bash
# Rebuild _deliverables/ — a folder of symlinks to the LATEST EPUB / PDF / narrator-brief of every
# published title, picked by newest mtime across both repos (africangold + arjuna-badger-press).
# Safe to re-run; only rewrites links, never source files.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODE="$(cd "$REPO/.." && pwd)"          # ~/code (holds both repos)
DEST="$REPO/_deliverables"
PY="${PYTHON:-/opt/homebrew/bin/python3}"

"$PY" - "$CODE" "$DEST" <<'PYEOF'
import sys
from pathlib import Path
CODE, DEST = Path(sys.argv[1]), Path(sys.argv[2])
for sub in ("ebooks", "pdfs", "narrator-briefs"):
    (DEST / sub).mkdir(parents=True, exist_ok=True)
    for old in (DEST / sub).glob("*"):
        if old.is_symlink():
            old.unlink()

BOOKS = {
 "RESONANCE": "books/resonance/build/export/RESONANCE",
 "REVELATION": "books/revelation/build/export/REVELATION",
 "RELIC": "books/relic/build/export/RELIC",
 "The Calendar of Stone": "books/history-before-time/books/book1-africa/build/export/The Calendar of Stone",
 "The Indian One": "books/history-before-time/books/book2-india/build/export/The Indian One",
 "The Temple in the Rock": "books/history-before-time/books/book3-india-deccan/build/export/The Temple in the Rock",
 "The Shore That Remembers": "books/history-before-time/books/book4-india-tamil/build/export/The Shore That Remembers",
 "The Engineer of the Gods": "books/history-before-time/books/book5-egypt/build/export/The Engineer of the Gods",
 "The Songlines of Stone": "books/history-before-time/books/australia-outback/build/export/The Songlines of Stone",
 "The Men Who Opened the Door": "books/history-before-time/books/project-stargate/build/export/The Men Who Opened the Door",
 "The Silver Thread": "books/history-before-time/books/jakobus-silver-thread/build/export/The Silver Thread",
 "The Recitation": "books/history-before-time/books/jakobus-the-recitation/build/export/The Recitation",
 "A Man They All Read Wrong": "books/history-before-time/books/the-jakobus-file/build/export/A Man They All Read Wrong — The Jakobus Swart File",
 "The Field of Doors": "books/history-before-time/books/crop-circles/build/export/The Field of Doors",
 "The Way That Was Invented": "books/the-unheard/books/japan-ainu/build/export/The Way That Was Invented",
 "The Felt and the Sky": "books/the-unheard/books/mongolia-steppe/build/export/The Felt and the Sky",
 "The Indifferent Desert": "books/the-sheltering-desert/build/export/The Indifferent Desert",
 "The Loneliest People in the World": "books/the-loneliest/build/export/The Loneliest People in the World",
 "The Song of the Self": "books/history-before-time/companions/the-song-of-the-self/export/The Song of the Self",
 "The Wrath of Achilles": "books/history-before-time/companions/the-wrath-of-achilles/export/The Wrath of Achilles",
 "The Scarlet Thread": "books/modern-sherlock/build/export/The Scarlet Thread",
}
REPOS = ["africangold", "arjuna-badger-press"]

def newest(relbase, ext):
    cands = [CODE / r / f"{relbase}.{ext}" for r in REPOS]
    cands = [p for p in cands if p.exists()]
    return max(cands, key=lambda p: p.stat().st_mtime) if cands else None

n_e = n_p = 0
missing = []
for name, rel in BOOKS.items():
    for ext, sub in (("epub", "ebooks"), ("pdf", "pdfs")):
        src = newest(rel, ext)
        if src:
            (DEST / sub / f"{name}.{ext}").symlink_to(src)
            if ext == "epub": n_e += 1
            else: n_p += 1
        else:
            missing.append(f"{name}.{ext}")

BRIEFS = {
 "The Calendar of Stone — Narrator Brief": "africangold/books/history-before-time/books/book1-africa/build/NARRATOR_BRIEF",
 "The Engineer of the Gods — Narrator Brief": "africangold/books/history-before-time/books/book5-egypt/build/NARRATOR_BRIEF",
}
for name, base in BRIEFS.items():
    for ext in ("pdf", "md"):
        src = CODE / f"{base}.{ext}"
        if src.exists():
            (DEST / "narrator-briefs" / f"{name}.{ext}").symlink_to(src)

print(f"  ebooks: {n_e}  pdfs: {n_p}  briefs: linked")
if missing:
    print("  MISSING (book not yet built?):", ", ".join(missing))
PYEOF

echo "  _deliverables refreshed at $DEST"
