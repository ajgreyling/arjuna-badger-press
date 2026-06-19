#!/usr/bin/env bash
# Assemble The Dreaming into build/BOOK.md: front matter + chapters in order.
# Mirrors the press convention (a single assembled BOOK.md feeds the render gate).
#   usage: books/the-dreaming/build/assemble.sh
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"           # .../build
OUT="$DIR/BOOK.md"
: > "$OUT"

# 1) front matter (title block + epigraphs), if present
if [ -f "$DIR/front-matter.md" ]; then
  cat "$DIR/front-matter.md" >> "$OUT"; printf '\n\n' >> "$OUT"
fi

# 2) chapters in lexical order (ch-01.md, ch-02.md, …)
shopt -s nullglob
chs=("$DIR"/chapters/ch-*.md)
if [ ${#chs[@]} -eq 0 ]; then
  echo "assemble: no chapters yet in $DIR/chapters/" >&2
else
  for f in $(printf '%s\n' "${chs[@]}" | sort); do
    cat "$f" >> "$OUT"; printf '\n\n' >> "$OUT"
  done
fi

words=$(wc -w < "$OUT" | tr -d ' ')
echo "assemble: $OUT (${words} words, ${#chs[@]} chapter(s))"
