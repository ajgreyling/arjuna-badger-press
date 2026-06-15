#!/usr/bin/env bash
# Arjuna Badger Press — render the African Gold Trilogy through the RENDER GATE.
#
# For each of RESONANCE / REVELATION / RELIC:
#   1. (if art exists) typeset the house cover from books/<id>/design/art.png
#   2. render EPUB + PDF via tools/render_book.sh — Atkinson body, the cover as PDF page 1 +
#      EPUB cover image, and the "free illustrated PDF online" note in the EPUB.
#
# The gate auto-detects the cover at books/<id>/build/export/cover.png. If a book has no cover yet
# (no art generated), it is SKIPPED with a note — generate the art first
# (see design/TRILOGY_COVER_ART_PROMPTS.md), drop it at books/<id>/design/art.png, and re-run.
#
#   tools/render_trilogy.sh                 # all three (skips any with no cover)
#   tools/render_trilogy.sh relic           # just one

set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GATE="$REPO/tools/render_book.sh"
PY="${PYTHON:-/opt/homebrew/bin/python3}"

# id | Title (for the file name + metadata)
title_for() {
  case "$1" in
    resonance)  echo "RESONANCE" ;;
    revelation) echo "REVELATION" ;;
    relic)      echo "RELIC" ;;
    *) echo "" ;;
  esac
}

BOOKS=("$@")
[ ${#BOOKS[@]} -eq 0 ] && BOOKS=(resonance revelation relic)

# 1) Typeset any covers whose art is present (no-op for books without art.png).
"$PY" "$REPO/design/typeset_trilogy_covers.py" "${BOOKS[@]}" || true

for id in "${BOOKS[@]}"; do
  TITLE="$(title_for "$id")"
  [ -z "$TITLE" ] && { echo "skip: unknown book '$id'"; continue; }
  BOOK_MD="$REPO/books/$id/build/BOOK.md"
  COVER="$REPO/books/$id/build/export/cover.png"
  OUT_BASE="$REPO/books/$id/build/export/$TITLE"

  if [ ! -f "$BOOK_MD" ]; then
    echo "skip $id: no BOOK.md (merge the chapters first)"; continue
  fi
  if [ ! -f "$COVER" ]; then
    echo "skip $id: no cover yet — generate art (design/TRILOGY_COVER_ART_PROMPTS.md),"
    echo "          save books/$id/design/art.png, then re-run."
    continue
  fi
  echo "── rendering $TITLE ──"
  "$GATE" "$BOOK_MD" "$OUT_BASE" "$TITLE" "Andries J. Greyling"
done
