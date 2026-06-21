# Translation production runbook

How to run the **batch Aya translation pipeline** without access to the private
**ai-stb** (Mezzanine vLLM) box.

## What runs where

| Workload | Where | Notes |
|---|---|---|
| **Batch book translation** (`translate_real.sh`, `run_translate_ab.sh`) | **Your machine or CI** | Long-running; ~270 LLM calls for Phase 1 pilot |
| **Real Language web UI** (`/real-language`, `/api/real-language`) | **Render** (`arjuna-badger-web`) | Interactive snippets; routes via OpenRouter (logical `openai` / `anthropic`) |
| **Corpus fixes** | Repo + site rebuild | Human corrections in `docs/translation_fixes.json` |

The Aya model is **not** deployed on Render. Render's `render.yaml` sets
`REAL_LANGUAGE_PROVIDER=openai` and has no `AYA_*` / `COHERE_*` vars. Batch
translation is an offline press job, not a web service.

## How the `aya` provider works today

`tools/translate_ab.py` → `call_aya()` uses the **OpenAI Python SDK** against any
OpenAI-compatible `/v1/chat/completions` endpoint:

```python
client = OpenAI(api_key=..., base_url=...)
client.chat.completions.create(model=..., messages=[...])
```

Environment variables (read in this order):

| Variable | Role | ai-stb default | Cohere public |
|---|---|---|---|
| `AYA_BASE_URL` / `AI_STB_BASE_URL` | Chat API base | `https://ai.mezzanineapps.com/v1` | `https://api.cohere.ai/compatibility/v1` |
| `AYA_API_KEY` / `AI_STB_API_KEY` / `COHERE_API_KEY` | Bearer token | ai-stb key | Cohere dashboard key |
| `AI_STB_MODEL` / `AYA_MODEL` | Model slug | `aya-expanse-32b` | `c4ai-aya-expanse-32b` |
| `AYA_MAX_TOKENS` | Output cap per segment | `1536` | raise to `4096` on Cohere (128k context) |

Keys are loaded from `arjuna-badger-platform/.env` by `run_translate_ab.sh`
(override path with `TRANSLATE_ENV=/path/to/.env`).

## Public provider options (ranked)

### 1. Cohere API — **recommended**

Same **Aya Expanse 32B** model family, official hosted API, OpenAI-compatible.

| Setting | Value |
|---|---|
| Base URL | `https://api.cohere.ai/compatibility/v1` |
| Model | `c4ai-aya-expanse-32b` |
| Auth | `COHERE_API_KEY` from [dashboard.cohere.com](https://dashboard.cohere.com/) |
| Pricing | **$0.50 / 1M input**, **$1.50 / 1M output** tokens ([cohere.com/pricing](https://cohere.com/pricing)) |
| Context | 128k input, 4k max output |

Docs: [Cohere Compatibility API](https://docs.cohere.com/docs/compatibility-api)

`run_translate_ab.sh` auto-selects Cohere when `COHERE_API_KEY` is set and no
explicit `AYA_BASE_URL` is present.

### 2. Self-hosted vLLM / TGI

Download `CohereForAI/aya-expanse-32b` from HuggingFace, serve with vLLM's
OpenAI-compatible server on your own GPU. Point `AYA_BASE_URL` at your host.
Useful for very large batches or air-gapped runs; ops cost >> Cohere API for
Phase 1 scale.

### 3. OpenRouter / other gateways

Check whether a gateway exposes `c4ai-aya-expanse-32b` or `aya-expanse-32b` on
an OpenAI-compatible route. If yes, set `AYA_BASE_URL` + `AYA_API_KEY` to the
gateway's values. Quality parity depends on the gateway's underlying host.

### 4. Anthropic / OpenAI via OpenRouter (A/B comparison)

`--provider anthropic` or `--provider openai` routes through **OpenRouter** when
`OPENROUTER_API_KEY` is set in `arjuna-badger-platform/.env` (same gateway as the
Real Language API). CLI provider names are unchanged; only the HTTP backend is unified.
Set `LLM_BACKEND=direct` to fall back to legacy `ANTHROPIC_API_KEY` / `OPENAI_API_KEY`.

## Minimal setup — OpenRouter (recommended for anthropic/openai A/B)

Add to `arjuna-badger-platform/.env`:

```bash
OPENROUTER_API_KEY=sk-or-...
OPENROUTER_MODEL_ANTHROPIC=anthropic/claude-opus-4
OPENROUTER_MODEL_OPENAI=openai/gpt-4.1
# Optional attribution:
# OPENROUTER_HTTP_REFERER=https://arjunabadger.press
# OPENROUTER_X_TITLE=Arjuna Badger Press
```

Run A/B against anthropic vs openai:

```bash
cd arjuna-badger-press
tools/run_translate_ab.sh books/relic --provider both --codes zu,af --workers 4
```

## Minimal setup — Cohere (no ai-stb)

Add to `arjuna-badger-platform/.env`:

```bash
COHERE_API_KEY=your-key-here
# Optional — auto-set by run_translate_ab.sh when COHERE_API_KEY is present:
# AYA_BASE_URL=https://api.cohere.ai/compatibility/v1
# AI_STB_MODEL=c4ai-aya-expanse-32b
AYA_MAX_TOKENS=4096   # Cohere allows up to 4k output; ai-stb used 1536
```

Run Phase 1 pilot (Resonance + Relic, 5 SA langs):

```bash
cd arjuna-badger-press

# One book, all SA codes:
tools/translate_real.sh books/resonance
tools/translate_real.sh books/relic

# Or segment-by-segment with resume:
tools/run_translate_ab.sh books/relic --provider aya --codes zu,af,xh,st,tn --resume --workers 4
```

Outputs land under `books/<book>/build/.translate/<code>.aya/` and assemble to
`build/BOOK.<code>.aya.md`.

## CI alternative (GitHub Actions)

Store `OPENROUTER_API_KEY` (or `COHERE_API_KEY` for Aya batch) as repo secrets.
Checkout both `arjuna-badger-press` and `arjuna-badger-platform`, write a
minimal `.env`, run `translate_real.sh`. Render is **not** involved.

## Render env (web app only)

Production Real Language on Render uses **OpenRouter only** (`LLM_BACKEND=openrouter` in
`render.yaml`). Set `OPENROUTER_API_KEY` as a secret; model slugs are in `render.yaml`. Do **not**
set `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, or `PERPLEXITY_API_KEY` on Render.

If you later wire Aya into the Real Language API, add to Render dashboard →
**arjuna-badger-web** → Environment:

```
COHERE_API_KEY=...
REAL_LANGUAGE_PROVIDER=cohere   # would need a code change in real_language.py
```

Today this is **not implemented** — the web API only supports `openai` and
`anthropic`. Batch translation does not use Render.

## Phase 1 cost estimate (~785k translated words)

Pilot scope: **Resonance + Relic** × **5 SA languages** (af, zu, xh, st, tn).

| Metric | Value |
|---|---|
| Source words | ~157k (Relic 87k + Resonance 70k) |
| Translated output words | ~786k (157k × 5 langs) |
| API calls | ~270 (54 segments × 5 langs; fewer with `--resume` / corpus hits) |
| Est. tokens | ~1.6M input + ~1.0M output |

**Cohere Aya Expanse 32B: ~$2–4 total** for Phase 1 (token math above ×
$0.50/$1.50 per 1M). Corpus exact matches skip LLM calls and reduce cost further.

Compare: ai-stb is free (owned GPU) but requires Mezzanine network access.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `401 Unauthorized` | Check `COHERE_API_KEY` / `AYA_API_KEY` |
| `model not found` | Use `c4ai-aya-expanse-32b` on Cohere, `aya-expanse-32b` on ai-stb |
| Truncated segments | Raise `AYA_MAX_TOKENS` (4096 on Cohere) |
| `run_translate_ab: no .env` | Copy `.env.example` → `.env` or set `TRANSLATE_ENV` |
| Wrong endpoint | Explicit `AYA_BASE_URL` overrides Cohere auto-detection |

## Related docs

- [`TRANSLATIONS.md`](../TRANSLATIONS.md) — edition map and pipeline overview
- [`REAL_LANGUAGE.md`](../../arjuna-badger-platform/docs/REAL_LANGUAGE.md) — corpus-first API
- [`translation_fixes.json`](translation_fixes.json) — human correction corpus
