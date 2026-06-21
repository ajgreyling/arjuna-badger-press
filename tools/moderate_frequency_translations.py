#!/usr/bin/env python3
"""LLM moderation for en→lang frequency translation cache.

Three OpenRouter judges (anthropic / openai / perplexity slots from llm_client):
  - anthropic: translation quality
  - openai: structure / consistency
  - perplexity: grounding / alternate view

Usage:
    python3 tools/moderate_frequency_translations.py --dry-run
    python3 tools/moderate_frequency_translations.py --pilot          # top 100 × 6 langs
    python3 tools/moderate_frequency_translations.py --lang zu --limit 50
    python3 tools/moderate_frequency_translations.py --pilot --resume --apply
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

REPO = Path(__file__).resolve().parents[1]
CORPUS_DIR = REPO / "docs" / "corpus"
FREQ_DIR = CORPUS_DIR / "frequency"
CACHE_PATH = CORPUS_DIR / "frequency_translations.json"
SCORES_PATH = FREQ_DIR / "moderation_scores.json"
QUEUE_PATH = FREQ_DIR / "moderation_queue.json"
REJECTED_PATH = FREQ_DIR / "moderation_rejected.json"
WORD_LIST = FREQ_DIR / "en_frequency.txt"
PLATFORM = REPO.parent / "arjuna-badger-platform"
PLATFORM_ENV = PLATFORM / ".env"

sys.path.insert(0, str(REPO / "tools"))
from en_frequency_1000 import FREQ_LANGS, LANG_NAMES, _load_env  # noqa: E402

JUDGE_PROVIDERS = ("anthropic", "openai", "perplexity")
DIMENSIONS = ("accuracy", "everyday_register", "not_bible_formal")

JUDGE_ROLES = {
    "anthropic": "translation quality specialist",
    "openai": "structure and consistency reviewer",
    "perplexity": "grounding reviewer with regional usage awareness",
}

DEFAULT_THRESHOLD = 6.0
DEFAULT_DISAGREEMENT = 2.0
DEFAULT_DELAY = 1.5
DEFAULT_MAX_RETRIES = 5
JUDGE_JSON_RETRIES = 1
PILOT_LEMMAS = 100


def load_word_list(*, tier: int = PILOT_LEMMAS) -> list[str]:
    if not WORD_LIST.is_file():
        raise SystemExit(f"Missing word list: {WORD_LIST}")
    words: list[str] = []
    for line in WORD_LIST.read_text(encoding="utf-8").splitlines():
        w = line.strip().lower()
        if w and w.isalpha():
            words.append(w)
        if len(words) >= tier:
            break
    return words[:tier]


def load_cache() -> dict[str, Any]:
    if not CACHE_PATH.is_file():
        raise SystemExit(f"Missing cache: {CACHE_PATH}")
    return json.loads(CACHE_PATH.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def entry_key(lang: str, en_word: str) -> str:
    return f"{lang}:{en_word}"


def should_skip_word(en_word: str) -> bool:
    """Skip noise lemmas (single letters, etc.) that are not worth judging."""
    return len(en_word.strip()) <= 1


def compute_summary(entries: dict[str, Any]) -> dict[str, Any]:
    totals = {
        "approved": 0,
        "flagged": 0,
        "rejected": 0,
        "judge_error": 0,
        "skipped": 0,
        "scored": len(entries),
    }
    for entry in entries.values():
        status = entry.get("status", "flagged")
        if status in totals:
            totals[status] += 1
    return totals


def is_rate_limit_error(exc: BaseException) -> bool:
    msg = str(exc).lower()
    return "429" in msg or "rate limit" in msg or "too many requests" in msg


def parse_judge_json(raw: str) -> dict[str, Any]:
    text = raw.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            return json.loads(match.group(0))
        raise


def build_judge_system(provider: str, target_lang_name: str) -> str:
    role = JUDGE_ROLES[provider]
    dims = ", ".join(DIMENSIONS)
    return f"""You are an expert bilingual evaluator for South African language publishing.
You act as the {role}. You judge a single English→target gloss with no knowledge of how it was produced.

Target language: {target_lang_name}
Register target: everyday conversational speech used by ordinary people — not stiff textbook prose,
not Bible/church register, not exaggerated street slang.

Score these dimensions (integers 1–10, 10 = excellent):
- accuracy: correct meaning for the English lemma in typical usage; no wrong sense
- everyday_register: sounds like a native speaker at everyday register (people's language)
- not_bible_formal: avoids liturgical, archaic, or overly formal religious/bookish wording

Return ONLY valid JSON (no markdown fences):
{{
  "accuracy": {{"score": 8, "rationale": "..."}},
  "everyday_register": {{"score": 7, "rationale": "..."}},
  "not_bible_formal": {{"score": 9, "rationale": "..."}},
  "suggested_fix": null,
  "brief_summary": "One sentence overall verdict."
}}

If the translation should be replaced, set suggested_fix to a better everyday gloss (string).
Dimensions: {dims}."""


def build_judge_user_prompt(en_word: str, translation: str) -> str:
    return "\n".join([
        "Evaluate this anonymous English lemma → target-language gloss.",
        "Judge only the pairing below.",
        "",
        f"English lemma: {en_word}",
        f"Proposed gloss: {translation}",
        "",
        "Respond with JSON only.",
    ])


def judge_dimension_score(judge_block: dict[str, Any], dim: str) -> float | None:
    entry = judge_block.get(dim)
    if isinstance(entry, dict) and "score" in entry:
        return float(entry["score"])
    if isinstance(entry, (int, float)):
        return float(entry)
    return None


def judge_overall(judge_block: dict[str, Any]) -> float | None:
    scores = [judge_dimension_score(judge_block, d) for d in DIMENSIONS]
    valid = [s for s in scores if s is not None]
    return sum(valid) / len(valid) if valid else None


def classify_status(
    aggregate: float,
    disagreement: float,
    *,
    threshold: float,
    max_disagreement: float,
) -> str:
    if aggregate < threshold - 1.0:
        return "rejected"
    if aggregate >= threshold and disagreement <= max_disagreement:
        return "approved"
    if aggregate < threshold or disagreement > max_disagreement:
        return "flagged"
    return "flagged"


def aggregate_entry(judge_results: dict[str, dict[str, Any]]) -> dict[str, Any]:
    dimension_stats: dict[str, dict[str, float]] = {}
    judge_overalls: list[float] = []

    for dim in DIMENSIONS:
        dim_scores = []
        for provider in JUDGE_PROVIDERS:
            block = judge_results.get(provider, {}).get("parsed") or {}
            score = judge_dimension_score(block, dim)
            if score is not None:
                dim_scores.append(score)
        if dim_scores:
            dimension_stats[dim] = {
                "mean": round(sum(dim_scores) / len(dim_scores), 2),
                "min": min(dim_scores),
                "max": max(dim_scores),
            }

    for provider in JUDGE_PROVIDERS:
        block = judge_results.get(provider, {}).get("parsed") or {}
        overall = judge_overall(block)
        if overall is not None:
            judge_overalls.append(overall)

    aggregate = round(sum(judge_overalls) / len(judge_overalls), 2) if judge_overalls else 0.0
    disagreement = round(max(judge_overalls) - min(judge_overalls), 2) if len(judge_overalls) >= 2 else 0.0

    suggested_fixes = []
    for provider in JUDGE_PROVIDERS:
        block = judge_results.get(provider, {}).get("parsed") or {}
        fix = block.get("suggested_fix")
        if isinstance(fix, str) and fix.strip():
            suggested_fixes.append({"provider": provider, "fix": fix.strip()})

    notes = []
    for provider in JUDGE_PROVIDERS:
        block = judge_results.get(provider, {}).get("parsed") or {}
        summary = block.get("brief_summary")
        if summary:
            notes.append(f"{provider}: {summary}")

    return {
        "dimensions": dimension_stats,
        "aggregate_score": aggregate,
        "disagreement": disagreement,
        "suggested_fixes": suggested_fixes,
        "notes": notes,
    }


def fetch_judge_raw(provider: str, en_word: str, translation: str, *, lang: str) -> tuple[str, list[str]]:
    sys.path.insert(0, str(PLATFORM))
    from engine.llm_client import call_anthropic, call_openai, call_perplexity, openrouter_enabled

    if not openrouter_enabled() and not os.environ.get(f"{provider.upper()}_API_KEY"):
        raise RuntimeError(
            "No LLM backend: set OPENROUTER_API_KEY (preferred) or vendor keys in "
            "arjuna-badger-platform/.env"
        )

    target_lang_name = LANG_NAMES.get(lang, lang)
    system = build_judge_system(provider, target_lang_name)
    prompt = build_judge_user_prompt(en_word, translation)

    citations: list[str] = []
    if provider == "anthropic":
        raw = call_anthropic(prompt, system=system, max_tokens=1024, temperature=None)
    elif provider == "openai":
        raw = call_openai(prompt, system=system, temperature=0.2, max_tokens=1024)
    elif provider == "perplexity":
        raw, citations = call_perplexity(prompt, system=system, temperature=0.2, max_tokens=1024)
    else:
        raise ValueError(f"Unknown judge provider: {provider!r}")

    return raw or "", citations


def call_judge_with_retries(
    provider: str,
    en_word: str,
    translation: str,
    *,
    lang: str,
    delay: float,
    max_retries: int,
) -> dict[str, Any]:
    last_err: BaseException | None = None

    for rate_attempt in range(max_retries + 1):
        if delay > 0:
            time.sleep(delay)
        try:
            raw, citations = fetch_judge_raw(provider, en_word, translation, lang=lang)
            if not raw.strip():
                raise ValueError("empty judge response")

            parse_err: json.JSONDecodeError | None = None
            for json_attempt in range(JUDGE_JSON_RETRIES + 1):
                try:
                    parsed = parse_judge_json(raw)
                    return {
                        "provider": provider,
                        "parsed": parsed,
                        "raw_response": raw,
                        "citations": citations,
                    }
                except json.JSONDecodeError as exc:
                    parse_err = exc
                    if json_attempt < JUDGE_JSON_RETRIES:
                        print(f"  [retry] invalid JSON from {provider}; re-fetching "
                              f"(attempt {json_attempt + 2}/{JUDGE_JSON_RETRIES + 1})")
                        if delay > 0:
                            time.sleep(delay)
                        raw, citations = fetch_judge_raw(provider, en_word, translation, lang=lang)
                        if not raw.strip():
                            raise ValueError("empty judge response") from exc
                        continue
                    raise
            if parse_err is not None:
                raise parse_err
        except (RuntimeError, ValueError, json.JSONDecodeError) as exc:
            last_err = exc
            if is_rate_limit_error(exc) and rate_attempt < max_retries:
                wait = min(60.0, (2 ** rate_attempt) * max(delay, 1.0))
                print(f"  [retry] rate limit from {provider}; sleeping {wait:.1f}s "
                      f"(attempt {rate_attempt + 1}/{max_retries + 1})")
                time.sleep(wait)
                continue
            raise

    raise last_err or RuntimeError(f"judge call failed for {provider}")


def call_live_judge(provider: str, en_word: str, translation: str, *, lang: str) -> dict[str, Any]:
    return call_judge_with_retries(
        provider,
        en_word,
        translation,
        lang=lang,
        delay=0.0,
        max_retries=DEFAULT_MAX_RETRIES,
    )


def judge_pair(
    en_word: str,
    translation: str,
    *,
    lang: str,
    judge_fn: Callable[[str, str, str, str], dict[str, Any]] | None = None,
    delay: float = DEFAULT_DELAY,
    max_retries: int = DEFAULT_MAX_RETRIES,
) -> dict[str, Any]:
    if judge_fn is not None:
        fn = judge_fn
    else:
        fn = lambda p, w, t, l: call_judge_with_retries(  # noqa: E731
            p, w, t, lang=l, delay=delay, max_retries=max_retries,
        )

    judge_results: dict[str, dict[str, Any]] = {}
    judge_errors: list[dict[str, str]] = []
    for provider in JUDGE_PROVIDERS:
        try:
            judge_results[provider] = fn(provider, en_word, translation, lang)
        except (RuntimeError, ValueError, json.JSONDecodeError) as exc:
            judge_errors.append({"provider": provider, "error": str(exc)})
            print(f"  [judge_error] {provider}: {exc}")

    if judge_errors:
        return {
            "judges": judge_results,
            "judge_errors": judge_errors,
            "dimensions": {},
            "aggregate_score": 0.0,
            "disagreement": 0.0,
            "suggested_fixes": [],
            "notes": [],
        }

    agg = aggregate_entry(judge_results)
    return {"judges": judge_results, "judge_errors": [], **agg}


def iter_pairs(
    cache: dict[str, Any],
    *,
    langs: list[str],
    words: list[str],
    skip_keys: set[str],
) -> list[tuple[str, str, str]]:
    pairs: list[tuple[str, str, str]] = []
    languages = cache.get("languages") or {}
    for lang in langs:
        lang_map = languages.get(lang) or {}
        for en_word in words:
            key = entry_key(lang, en_word)
            if key in skip_keys:
                continue
            translation = lang_map.get(en_word)
            if not translation:
                continue
            pairs.append((lang, en_word, translation))
    return pairs


def load_scores() -> dict[str, Any]:
    if SCORES_PATH.is_file():
        return json.loads(SCORES_PATH.read_text(encoding="utf-8"))
    return {"meta": {}, "entries": {}, "summary": {}}


def judge_model_slugs() -> dict[str, str]:
    sys.path.insert(0, str(PLATFORM))
    from engine.llm_client import _openrouter_slug  # noqa: PLC2701

    return {p: _openrouter_slug(p, None) for p in JUDGE_PROVIDERS}


def run_moderation(
    *,
    langs: list[str],
    words: list[str],
    limit: int | None,
    threshold: float,
    max_disagreement: float,
    resume: bool,
    dry_run: bool,
    delay: float = DEFAULT_DELAY,
    max_retries: int = DEFAULT_MAX_RETRIES,
    judge_fn: Callable[[str, str, str, str], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    cache = load_cache()
    scores_doc = load_scores() if resume else {"meta": {}, "entries": {}, "summary": {}}
    existing = scores_doc.get("entries") or {}
    skip_keys = set(existing.keys()) if resume else set()

    pairs = iter_pairs(cache, langs=langs, words=words, skip_keys=skip_keys)
    if limit is not None:
        pairs = pairs[:limit]

    meta = scores_doc.setdefault("meta", {})
    meta.update({
        "threshold": threshold,
        "max_disagreement": max_disagreement,
        "langs": langs,
        "word_count": len(words),
        "pair_limit": limit,
        "dry_run": dry_run,
        "delay": delay,
        "max_retries": max_retries,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    })
    if not meta.get("started_at"):
        meta["started_at"] = meta["updated_at"]

    if dry_run:
        meta["judges"] = judge_model_slugs()
        pending = len(pairs)
        skipped_pending = sum(1 for _, w, _ in pairs if should_skip_word(w))
        scores_doc["summary"] = {
            "pending": pending,
            "pending_skippable_noise": skipped_pending,
            "already_scored": len(skip_keys),
            "total_pairs_available": len(pairs) + len(skip_keys),
        }
        return scores_doc

    entries = scores_doc.setdefault("entries", {})

    for i, (lang, en_word, translation) in enumerate(pairs, 1):
        key = entry_key(lang, en_word)

        if should_skip_word(en_word):
            print(f"[{i}/{len(pairs)}] {key} → skipped (noise token)")
            entries[key] = {
                "en": en_word,
                "lang": lang,
                "translation": translation,
                "status": "skipped",
                "reason": "single-character or noise lemma",
                "scored_at": datetime.now(timezone.utc).isoformat(),
            }
            scores_doc["summary"] = compute_summary(entries)
            save_json(SCORES_PATH, scores_doc)
            continue

        print(f"[{i}/{len(pairs)}] {key} → {translation!r}")
        result = judge_pair(
            en_word,
            translation,
            lang=lang,
            judge_fn=judge_fn,
            delay=delay,
            max_retries=max_retries,
        )

        if result.get("judge_errors"):
            status = "judge_error"
        else:
            status = classify_status(
                result["aggregate_score"],
                result["disagreement"],
                threshold=threshold,
                max_disagreement=max_disagreement,
            )

        entry: dict[str, Any] = {
            "en": en_word,
            "lang": lang,
            "translation": translation,
            "dimensions": result.get("dimensions") or {},
            "aggregate_score": result.get("aggregate_score", 0.0),
            "disagreement": result.get("disagreement", 0.0),
            "suggested_fixes": result.get("suggested_fixes") or [],
            "notes": result.get("notes") or [],
            "status": status,
            "scored_at": datetime.now(timezone.utc).isoformat(),
        }

        if result.get("judges"):
            entry["judges"] = {
                p: {
                    "parsed": result["judges"][p]["parsed"],
                    "citations": result["judges"][p].get("citations") or [],
                }
                for p in JUDGE_PROVIDERS
                if p in result["judges"]
            }
        if result.get("judge_errors"):
            entry["judge_errors"] = result["judge_errors"]

        entries[key] = entry
        scores_doc["summary"] = compute_summary(entries)
        save_json(SCORES_PATH, scores_doc)

    meta["judges"] = judge_model_slugs()
    meta["completed_at"] = datetime.now(timezone.utc).isoformat()
    scores_doc["summary"] = compute_summary(entries)
    save_json(SCORES_PATH, scores_doc)
    return scores_doc


def apply_moderation(scores_doc: dict[str, Any]) -> dict[str, str]:
    cache = load_cache()
    languages = cache.setdefault("languages", {})
    queue_entries: dict[str, Any] = {}
    rejected_entries: dict[str, Any] = {}

    for key, entry in (scores_doc.get("entries") or {}).items():
        lang = entry["lang"]
        en_word = entry["en"]
        status = entry.get("status")
        if status == "approved":
            continue
        payload = {
            "en": en_word,
            "lang": lang,
            "translation": entry.get("translation"),
            "aggregate_score": entry.get("aggregate_score"),
            "disagreement": entry.get("disagreement"),
            "suggested_fixes": entry.get("suggested_fixes") or [],
            "notes": entry.get("notes") or [],
            "status": status,
        }
        if status == "flagged":
            queue_entries[key] = payload
        elif status == "rejected":
            rejected_entries[key] = payload
            lang_map = languages.setdefault(lang, {})
            if en_word in lang_map:
                rejected_val = lang_map.pop(en_word)
                rejected_entries[key]["_removed_translation"] = rejected_val

    save_json(QUEUE_PATH, {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "entries": queue_entries,
    })
    save_json(REJECTED_PATH, {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "entries": rejected_entries,
    })
    save_json(CACHE_PATH, cache)

    return {
        "flagged": str(len(queue_entries)),
        "rejected_removed": str(len(rejected_entries)),
        "queue_path": str(QUEUE_PATH),
        "rejected_path": str(REJECTED_PATH),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Moderate frequency_translations.json via 3 LLM judges")
    parser.add_argument("--lang", choices=FREQ_LANGS, action="append", dest="langs",
                        help="Limit to language(s); default all six")
    parser.add_argument("--limit", type=int, default=None, help="Max pairs to score this run")
    parser.add_argument("--pilot", action="store_true",
                        help=f"Score top {PILOT_LEMMAS} en lemmas × selected langs (default pilot)")
    parser.add_argument("--tier", type=int, default=None,
                        help="En lemma tier from en_frequency.txt (overrides --pilot count)")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                        help=f"Min aggregate score for approved (default {DEFAULT_THRESHOLD})")
    parser.add_argument("--max-disagreement", type=float, default=DEFAULT_DISAGREEMENT,
                        help=f"Max judge spread before flag (default {DEFAULT_DISAGREEMENT})")
    parser.add_argument("--resume", action="store_true", help="Skip entries already in moderation_scores.json")
    parser.add_argument("--delay", type=float, default=DEFAULT_DELAY,
                        help=f"Seconds between judge API calls (default {DEFAULT_DELAY})")
    parser.add_argument("--dry-run", action="store_true", help="Show pending pair count only")
    parser.add_argument("--apply", action="store_true",
                        help="Apply scores: flagged→queue, rejected→remove from cache")
    args = parser.parse_args()

    _load_env()
    langs = args.langs or list(FREQ_LANGS)
    tier = args.tier if args.tier is not None else (PILOT_LEMMAS if args.pilot else PILOT_LEMMAS)
    if not args.pilot and args.tier is None and args.limit is None and not args.dry_run:
        print(f"Defaulting to pilot: top {PILOT_LEMMAS} lemmas × {len(langs)} langs")
    words = load_word_list(tier=tier)

    limit = args.limit
    if args.pilot and limit is None and not args.dry_run:
        limit = len(words) * len(langs)

    scores_doc = run_moderation(
        langs=langs,
        words=words,
        limit=limit,
        threshold=args.threshold,
        max_disagreement=args.max_disagreement,
        resume=args.resume,
        dry_run=args.dry_run,
        delay=args.delay,
    )

    if args.dry_run:
        summary = scores_doc.get("summary", {})
        print(f"Dry run: {summary.get('pending', 0)} pairs pending, "
              f"{summary.get('already_scored', 0)} already scored")
        print(f"Judges: {json.dumps(scores_doc.get('meta', {}).get('judges', {}), indent=2)}")
        return 0

    summary = scores_doc.get("summary", {})
    print(f"\nModeration complete: scored={summary.get('scored', 0)} "
          f"approved={summary.get('approved', 0)} flagged={summary.get('flagged', 0)} "
          f"rejected={summary.get('rejected', 0)} "
          f"judge_error={summary.get('judge_error', 0)} skipped={summary.get('skipped', 0)}")
    print(f"Scores: {SCORES_PATH}")

    if args.apply:
        result = apply_moderation(scores_doc)
        print(f"Applied: flagged={result['flagged']} rejected_removed={result['rejected_removed']}")
        print(f"  queue: {result['queue_path']}")
        print(f"  rejected: {result['rejected_path']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
