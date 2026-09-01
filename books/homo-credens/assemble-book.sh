#!/usr/bin/env bash
# Regenerate BOOK.md from 00-front-matter.md + chapters/ch-*.md.
#
# BOOK.md is a DERIVED artifact and nothing should ever be authored in it. It was not
# always so: until 2026-08-13 it was the only file carrying the 107 [PLATE: ...] art
# briefs while chapters/ carried the corrected prose, so the two had drifted in opposite
# directions and neither could be regenerated from the other without losing something.
# The briefs have since been ported into chapters/, which is now the single source of
# truth. This script exists so that stays true.
#
# Usage:  ./assemble-book.sh          write BOOK.md
#         ./assemble-book.sh --check  verify BOOK.md is current; non-zero if stale
set -euo pipefail
cd "$(dirname "$0")"

out=$(
  cat 00-front-matter.md
  for f in chapters/ch-*.md; do
    printf '\n---\n\n'
    cat "$f"
  done
)

if [ "${1:-}" = "--check" ]; then
  if diff -q <(printf '%s\n' "$out") BOOK.md >/dev/null 2>&1; then
    echo "BOOK.md is current"
  else
    echo "BOOK.md is STALE — run ./assemble-book.sh" >&2
    exit 1
  fi
else
  printf '%s\n' "$out" > BOOK.md
  printf 'BOOK.md: %s bytes, %s chapters, %s plate briefs\n' \
    "$(wc -c < BOOK.md | tr -d ' ')" \
    "$(ls chapters/ch-*.md | wc -l | tr -d ' ')" \
    "$(grep -c 'PLATE:' BOOK.md)"
fi
