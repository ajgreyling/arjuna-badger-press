#!/usr/bin/env bash
# Arjuna Badger Press — translation orchestrator (the deterministic half).
#
# Splits a book's assembled BOOK.md into translation-sized SEGMENTS on its top-level
# (`# `) section boundaries, and lays out a work-tree the translation pass fills in.
# The actual language work is done by a multi-agent run (see tools/translate_workflow.js),
# NOT by this script — shell can't call the model. This script owns only the mechanics:
# split → (translation drops files in) → reassemble → hand to the render gate.
#
# Layout produced under <book>/build/.translate/:
#   segments/seg-NN.md            the source segment NN (verbatim slice of BOOK.md)
#   segments/INDEX.tsv            NN <tab> heading <tab> first-line <tab> word-count
#   <code>/seg-NN.md              the TRANSLATED segment NN (written by the workflow)
# On reassemble, <code>/seg-*.md are concatenated in order → build/BOOK.<code>.md
#
# Usage:
#   tools/translate_book.sh <book-dir> split           # cut BOOK.md into segments
#   tools/translate_book.sh <book-dir> reassemble <code>   # stitch translated segments
#   tools/translate_book.sh <book-dir> status              # show progress per language
#
# <book-dir> contains build/BOOK.md, LANGUAGES.json, GLOSSARY_PRESERVE.json.

set -euo pipefail

BOOK_DIR="${1:?need <book-dir> (e.g. books/resonance)}"
CMD="${2:?need command: split | reassemble <code> | status}"

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BOOK_DIR="$(cd "$BOOK_DIR" && pwd)"
BOOK_MD="$BOOK_DIR/build/BOOK.md"
LANGS_JSON="$BOOK_DIR/LANGUAGES.json"
WORK="$BOOK_DIR/build/.translate"
SEG_DIR="$WORK/segments"

[ -f "$BOOK_MD" ]    || { echo "translate: no $BOOK_MD" >&2; exit 1; }
[ -f "$LANGS_JSON" ] || { echo "translate: no $LANGS_JSON" >&2; exit 1; }

# Languages declared in the manifest (codes), via python (always present here).
codes() { python3 -c "import json,sys; print(' '.join(t['code'] for t in json.load(open('$LANGS_JSON'))['targets']))"; }

split_book() {
  rm -rf "$SEG_DIR"; mkdir -p "$SEG_DIR"
  # awk: start a new segment file at every top-level '# ' heading. Front matter before
  # the first heading (there is none here — file starts with '# RESONANCE') would go to
  # seg-00 as a preamble if present.
  awk -v dir="$SEG_DIR" '
    BEGIN { n = -1; preamble = 1 }
    /^# / {
      n++; preamble = 0
      fname = sprintf("%s/seg-%02d.md", dir, n)
    }
    {
      if (preamble) {
        if (n == -1) { n = 0; fname = sprintf("%s/seg-%02d.md", dir, n) }
      }
      print >> fname
    }
  ' "$BOOK_MD"

  # Build INDEX.tsv: segment, heading text, word count.
  : > "$SEG_DIR/INDEX.tsv"
  for f in "$SEG_DIR"/seg-*.md; do
    nn="$(basename "$f" .md | sed 's/seg-//')"
    head_txt="$(grep -m1 -E '^# ' "$f" | sed 's/^# //' || echo '(preamble)')"
    wc_words="$(wc -w < "$f" | tr -d ' ')"
    printf '%s\t%s\t%s\n' "$nn" "$head_txt" "$wc_words" >> "$SEG_DIR/INDEX.tsv"
  done
  echo "split: $(ls "$SEG_DIR"/seg-*.md | wc -l | tr -d ' ') segments → $SEG_DIR"
  echo "languages to fill: $(codes)"
}

reassemble() {
  local code="${1:?reassemble needs a language code}"
  local out="$BOOK_DIR/build/BOOK.$code.md"
  local cdir="$WORK/$code"
  [ -d "$cdir" ] || { echo "reassemble: no translated segments at $cdir" >&2; exit 1; }

  local missing=0
  : > "$out"
  for src in "$SEG_DIR"/seg-*.md; do
    local nn; nn="$(basename "$src")"
    local tr="$cdir/$nn"
    if [ ! -f "$tr" ]; then
      echo "  !! missing translated segment: $code/$nn" >&2
      missing=$((missing+1)); continue
    fi
    cat "$tr" >> "$out"
    # ensure a blank line between segments so headings never glue together
    printf '\n' >> "$out"
  done
  if [ "$missing" -gt 0 ]; then
    echo "reassemble: $missing segment(s) missing for '$code' — $out is INCOMPLETE" >&2
    exit 1
  fi
  echo "reassemble: $out ($(wc -w < "$out" | tr -d ' ') words)"
}

status() {
  local total; total="$(ls "$SEG_DIR"/seg-*.md 2>/dev/null | wc -l | tr -d ' ')"
  [ "$total" -gt 0 ] || { echo "status: not split yet (run: split)"; return; }
  echo "segments: $total"
  for c in $(codes); do
    local done; done="$(ls "$WORK/$c"/seg-*.md 2>/dev/null | wc -l | tr -d ' ')"
    printf "  %-4s %s/%s\n" "$c" "$done" "$total"
  done
}

case "$CMD" in
  split)       split_book ;;
  reassemble)  reassemble "${3:-}" ;;
  status)      status ;;
  *) echo "translate: unknown command '$CMD'" >&2; exit 1 ;;
esac
