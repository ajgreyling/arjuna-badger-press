#!/usr/bin/env bash
# Corpus-first regional translation wrapper: split → Aya translate → verify → reassemble.
#
# Usage:
#   tools/translate_real.sh books/resonance
#   tools/translate_real.sh books/relic --codes zu,af --segments 0,1
#   tools/translate_real.sh books/resonance --skip-translate   # reassemble/verify only
#
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BOOK="${1:?book path relative to repo, e.g. books/resonance}"
shift || true

CODES="zu,af,xh,st,tn"
PROVIDER="aya"
WORKERS=4
SKIP_SPLIT=0
SKIP_TRANSLATE=0
EXTRA=()

while [ $# -gt 0 ]; do
  case "$1" in
    --codes) CODES="$2"; shift 2 ;;
    --provider) PROVIDER="$2"; shift 2 ;;
    --workers) WORKERS="$2"; shift 2 ;;
    --skip-split) SKIP_SPLIT=1; shift ;;
    --skip-translate) SKIP_TRANSLATE=1; shift ;;
    *) EXTRA+=("$1"); shift ;;
  esac
done

cd "$REPO"

if [ "$SKIP_SPLIT" -eq 0 ]; then
  echo "== split: $BOOK =="
  tools/translate_book.sh "$BOOK" split
fi

if [ "$SKIP_TRANSLATE" -eq 0 ]; then
  echo "== translate ($PROVIDER): $BOOK [$CODES] =="
  tools/run_translate_ab.sh "$BOOK" \
    --provider "$PROVIDER" \
    --codes "$CODES" \
    --workers "$WORKERS" \
    "${EXTRA[@]}"
fi

echo "== verify: $BOOK =="
if [ -f tools/verify_translation.py ]; then
  python3 tools/verify_translation.py "$BOOK" || true
fi

IFS=',' read -ra LANGS <<< "$CODES"
for code in "${LANGS[@]}"; do
  code="$(echo "$code" | tr -d ' ')"
  provider_dir="$BOOK/build/.translate/${code}.${PROVIDER}"
  if [ -d "$provider_dir" ]; then
    echo "== reassemble $code ($PROVIDER): $BOOK =="
    mkdir -p "$BOOK/build/.translate/$code"
    cp -f "$provider_dir"/seg-*.md "$BOOK/build/.translate/$code/" 2>/dev/null || true
    tools/translate_book.sh "$BOOK" reassemble "$code"
  fi
done

echo "== status: $BOOK =="
tools/translate_book.sh "$BOOK" status

echo "Done. Next: tools/render_book.sh for each build/BOOK.<code>.md"
