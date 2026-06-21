#!/usr/bin/env bash
# Launch translate_ab.py with keys from arjuna-badger-platform/.env (no resume by default).
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLATFORM="$(cd "$REPO/../arjuna-badger-platform" && pwd)"
ENV_FILE="${TRANSLATE_ENV:-$PLATFORM/.env}"
PY="${TRANSLATE_PYTHON:-python3}"
LOG_DIR="${REPO}/build/.translate/logs"
mkdir -p "$LOG_DIR"

export PYTHONPATH="${PLATFORM}${PYTHONPATH:+:$PYTHONPATH}"
export REAL_LANGUAGE_CORPUS_DIR="${REAL_LANGUAGE_CORPUS_DIR:-$REPO/docs/corpus}"

load_key() {
  local name="$1"
  local val
  val="$(grep -E "^${name}=" "$ENV_FILE" 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"'"'" || true)"
  if [ -n "$val" ]; then
    export "$name=$val"
  fi
}

[ -f "$ENV_FILE" ] || { echo "run_translate_ab: no $ENV_FILE" >&2; exit 1; }
load_key OPENROUTER_API_KEY
load_key OPENROUTER_HTTP_REFERER
load_key OPENROUTER_X_TITLE
load_key OPENROUTER_APP_TITLE
load_key LLM_BACKEND
load_key OPENROUTER_MODEL_ANTHROPIC
load_key OPENROUTER_MODEL_OPENAI
load_key OPENROUTER_PROSE_MODEL
load_key OPENROUTER_STRUCTURE_MODEL
load_key ANTHROPIC_API_KEY
load_key OPENAI_API_KEY
load_key COHERE_API_KEY
load_key AYA_API_KEY
load_key AI_STB_API_KEY

# Prefer OpenRouter when key is present (override with LLM_BACKEND=direct for legacy keys).
if [ -n "${OPENROUTER_API_KEY:-}" ] && [ "${LLM_BACKEND:-}" != "direct" ]; then
  export LLM_BACKEND=openrouter
fi

# Endpoint selection (first match wins):
#   1. Explicit AYA_BASE_URL / AI_STB_BASE_URL in .env
#   2. COHERE_API_KEY set → Cohere public compatibility API (same Aya Expanse 32B family)
#   3. Default → private ai-stb vLLM at Mezzanine
if [ -n "${AYA_BASE_URL:-}" ] || [ -n "${AI_STB_BASE_URL:-}" ]; then
  export AI_STB_BASE_URL="${AI_STB_BASE_URL:-$AYA_BASE_URL}"
  export AI_STB_MODEL="${AI_STB_MODEL:-${AYA_MODEL:-aya-expanse-32b}}"
elif [ -n "${COHERE_API_KEY:-}" ]; then
  export AYA_API_KEY="${AYA_API_KEY:-$COHERE_API_KEY}"
  export AI_STB_BASE_URL="https://api.cohere.ai/compatibility/v1"
  export AI_STB_MODEL="${AI_STB_MODEL:-${AYA_MODEL:-c4ai-aya-expanse-32b}}"
else
  export AI_STB_BASE_URL="${AI_STB_BASE_URL:-${AYA_BASE_URL:-https://ai.mezzanineapps.com/v1}}"
  export AI_STB_MODEL="${AI_STB_MODEL:-${AYA_MODEL:-aya-expanse-32b}}"
fi

BOOK="${1:?book path relative to repo, e.g. books/relic}"
shift

cd "$REPO"
exec "$PY" -u tools/translate_ab.py "$BOOK" "$@"
