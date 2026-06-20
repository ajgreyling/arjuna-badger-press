#!/usr/bin/env bash
# Launch translate_ab.py with keys from arjuna-badger-platform/.env (no resume by default).
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${TRANSLATE_ENV:-$REPO/../arjuna-badger-platform/.env}"
PY="${TRANSLATE_PYTHON:-python3}"
LOG_DIR="${REPO}/build/.translate/logs"
mkdir -p "$LOG_DIR"

load_key() {
  local name="$1"
  local val
  val="$(grep -E "^${name}=" "$ENV_FILE" 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"'"'" || true)"
  if [ -n "$val" ]; then
    export "$name=$val"
  fi
}

[ -f "$ENV_FILE" ] || { echo "run_translate_ab: no $ENV_FILE" >&2; exit 1; }
load_key ANTHROPIC_API_KEY
load_key OPENAI_API_KEY
load_key AYA_API_KEY
load_key AI_STB_API_KEY
# ai-stb defaults (override in .env if needed)
export AI_STB_BASE_URL="${AI_STB_BASE_URL:-${AYA_BASE_URL:-https://ai.mezzanineapps.com/v1}}"
export AI_STB_MODEL="${AI_STB_MODEL:-${AYA_MODEL:-aya-expanse-32b}}"

BOOK="${1:?book path relative to repo, e.g. books/relic}"
shift

cd "$REPO"
exec "$PY" -u tools/translate_ab.py "$BOOK" "$@"
