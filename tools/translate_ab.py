#!/usr/bin/env python3
"""Arjuna Badger Press — A/B translation runner.

For each (language, segment) pair, calls providers and writes results side-by-side.
Supports three providers: Anthropic (claude-opus-4-8), OpenAI (gpt-4o), and
Aya (Aya Expanse 32B on ai-stb via OpenAI-compatible vLLM endpoint).

Outputs per provider:
    build/.translate/<code>.<provider>/seg-NN.md   translated segment
Outputs final reassembled manuscripts:
    build/BOOK.<code>.anthropic.md
    build/BOOK.<code>.openai.md
    build/BOOK.<code>.aya.md
Outputs A/B diff report:
    build/.translate/AB_REPORT.<code>.md

Usage:
    tools/translate_ab.py <book-dir> [--codes zu,af,es,fr] [--segments 0,1,2]
                          [--workers 4] [--provider anthropic|openai|aya|all]
                          [--resume]   # skip segments already done for a provider

<book-dir> must contain LANGUAGES.json, GLOSSARY_PRESERVE.json, build/BOOK.md,
and build/.translate/segments/ (run translate_book.sh split first).

Environment:
    OPENROUTER_API_KEY   preferred — routes anthropic/openai via OpenRouter (see platform .env)
    OPENROUTER_MODEL_ANTHROPIC / OPENROUTER_PROSE_MODEL   OpenRouter slug for --provider anthropic
    OPENROUTER_MODEL_OPENAI / OPENROUTER_STRUCTURE_MODEL   OpenRouter slug for --provider openai
    LLM_BACKEND=direct     force legacy direct keys (deprecated)

    ANTHROPIC_API_KEY   legacy direct Anthropic (when LLM_BACKEND=direct, no OpenRouter key)
    OPENAI_API_KEY      legacy direct OpenAI (when LLM_BACKEND=direct, no OpenRouter key)
    AYA_BASE_URL        OpenAI-compatible chat endpoint (alias: AI_STB_BASE_URL)
    AYA_API_KEY         Bearer token (aliases: AI_STB_API_KEY, COHERE_API_KEY)
    AI_STB_MODEL        Model slug on the endpoint (alias: AYA_MODEL)

    Public Cohere (no ai-stb access):
        AYA_BASE_URL=https://api.cohere.ai/compatibility/v1
        AYA_API_KEY=<COHERE_API_KEY>
        AI_STB_MODEL=c4ai-aya-expanse-32b

    Private ai-stb (Mezzanine vLLM):
        AYA_BASE_URL=https://ai.mezzanineapps.com/v1
        AI_STB_MODEL=aya-expanse-32b
"""
from __future__ import annotations
import argparse, json, os, re, sys, time, textwrap, difflib
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Share correction_corpus with the Real Language API (arjuna-badger-platform).
_PLATFORM = Path(__file__).resolve().parents[2] / "arjuna-badger-platform"
if _PLATFORM.is_dir() and str(_PLATFORM) not in sys.path:
    sys.path.insert(0, str(_PLATFORM))

from saas.correction_corpus import get_corpus  # noqa: E402
from saas.llm_routing import openrouter_mode, provider_llm_ready  # noqa: E402
from saas.real_language import clamp_temp, register_directive  # noqa: E402

ANTHROPIC_MODEL = "claude-opus-4-8"
OPENAI_MODEL = "gpt-4o"
AYA_MODEL = os.environ.get("AI_STB_MODEL", os.environ.get("AYA_MODEL", "aya-expanse-32b"))
AYA_DEFAULT_URL = "https://ai.mezzanineapps.com/v1"
MAX_TOKENS = int(os.environ.get("TRANSLATE_MAX_TOKENS", "4096"))
# ai-stb Aya serves 8192 total context; reserve headroom for system + segment input.
AYA_MAX_TOKENS = int(os.environ.get("AYA_MAX_TOKENS", "1536"))


def ai_stb_base_url() -> str:
    return os.environ.get("AI_STB_BASE_URL", os.environ.get("AYA_BASE_URL", AYA_DEFAULT_URL))


def ai_stb_api_key() -> str:
    return os.environ.get(
        "AI_STB_API_KEY",
        os.environ.get("AYA_API_KEY", os.environ.get("COHERE_API_KEY", "ignored")),
    )


def load_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def target_temp(lang_obj: dict, override: float | None = None) -> float:
    if override is not None:
        return clamp_temp(override)
    if "temp" in lang_obj:
        return clamp_temp(lang_obj["temp"])
    kind = lang_obj.get("kind", "regional")
    return clamp_temp(0.5 if kind == "market" else 0.75)


def build_system(
    lang_obj: dict,
    glossary: dict,
    global_directives: list[str],
    provider: str,
    *,
    temp: float,
    corpus_block: str = "",
) -> str:
    directives = lang_obj.get("directives", [])
    preserve = glossary["preserve_verbatim_all_languages"]
    reg = register_directive(temp)
    t = clamp_temp(temp)

    in_lang = preserve.get("in_language_terms", {})
    invented = preserve.get("invented_entities", [])
    names = preserve.get("proper_names", [])

    in_lang_lines = []
    for lang_name, terms in in_lang.items():
        in_lang_lines.append(f"  {lang_name}: {', '.join(repr(t) for t in terms)}")

    system = textwrap.dedent(f"""
    You are a professional literary translator. Your task is to translate a segment of a
    novel into {lang_obj['name']} (language code: {lang_obj['code']}).

    ## Register (temp={t:.2f})

    {reg}

    ## Translation directives for {lang_obj['name']}

    {chr(10).join(f'- {d}' for d in directives)}

    ## Global directives (apply to every edition)

    {chr(10).join(f'- {d}' for d in global_directives)}

    ## Preserve verbatim (do NOT translate these)

    In-language terms (keep exactly as written — they are intentionally untranslated):
    {chr(10).join(in_lang_lines) if in_lang_lines else '  (none declared)'}

    Invented entities (keep English names verbatim):
    {', '.join(repr(e) for e in invented) if invented else '(none)'}

    Proper names (keep verbatim):
    {', '.join(repr(n) for n in names[:20]) if names else '(none)'}
    {'... and more — see full glossary' if len(names) > 20 else ''}

    ## Output format

    Return ONLY the translated markdown segment. Do not add commentary, preamble,
    or explanation. Do not add translator's notes. Preserve all markdown structure:
    headings (#, ##, ###), horizontal rules (---), scene breaks (⁂), bold (**text**),
    italics (*text*), em dashes (—), and ellipses (…) exactly as in the source.

    When a BINDING CORPUS section is present below, those human corrections ALWAYS win.
    {corpus_block if corpus_block else ''}
    """).strip()
    return system


def call_anthropic(system: str, segment_text: str) -> str:
    from engine.llm_client import call_anthropic as _call

    return _call(
        f"Translate this segment:\n\n{segment_text}",
        system=system,
        model=ANTHROPIC_MODEL,
        max_tokens=MAX_TOKENS,
    )


def call_openai(system: str, segment_text: str) -> str:
    from engine.llm_client import call_openai as _call

    return _call(
        f"Translate this segment:\n\n{segment_text}",
        system=system,
        model=OPENAI_MODEL,
        max_tokens=MAX_TOKENS,
        temperature=0.6,
    )


def call_aya(system: str, segment_text: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=ai_stb_api_key(), base_url=ai_stb_base_url())
    resp = client.chat.completions.create(
        model=AYA_MODEL,
        max_tokens=AYA_MAX_TOKENS,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": f"Translate this segment:\n\n{segment_text}"},
        ],
    )
    return resp.choices[0].message.content


def translate_segment(
    provider: str,
    base_system: str,
    segment_path: Path,
    out_path: Path,
    resume: bool,
    source_lang: str,
    target_lang: str,
    temp: float,
) -> tuple[str, str, str | None, str]:
    """Translate one segment. Returns (provider, seg_name, error_or_None, corpus_note)."""
    if resume and out_path.exists():
        return provider, segment_path.name, None, ""

    text = segment_path.read_text(encoding="utf-8")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    corpus = get_corpus()
    route = corpus.route(text, source_lang, target_lang, temp)
    corpus_note = ""

    try:
        if route.decision == "corpus_exact":
            translated = route.text or ""
            corpus_note = f"corpus_exact:{route.entries_used[0].id}"
        else:
            system = base_system
            if route.prompt_block:
                system = base_system + "\n\n" + route.prompt_block
            if provider == "anthropic":
                translated = call_anthropic(system, text)
            elif provider == "openai":
                translated = call_openai(system, text)
            elif provider == "aya":
                translated = call_aya(system, text)
            else:
                raise ValueError(f"Unknown provider: {provider}")
            if route.entries_used:
                corpus_note = f"ai_guided:{len(route.entries_used)}"

        translated, applied = corpus.overlay_all(translated, source_lang, target_lang, temp)
        if applied:
            ids = ",".join(e.id for e in applied)
            corpus_note = (corpus_note + f" overlay:{ids}").strip()

        out_path.write_text(translated, encoding="utf-8")
        return provider, segment_path.name, None, corpus_note
    except Exception as e:
        return provider, segment_path.name, str(e), ""


def reassemble(seg_dir: Path, provider_dir: Path, out_path: Path) -> bool:
    segments = sorted(seg_dir.glob("seg-*.md"))
    missing = []
    parts = []
    for seg in segments:
        tr = provider_dir / seg.name
        if not tr.exists():
            missing.append(seg.name)
        else:
            parts.append(tr.read_text(encoding="utf-8"))
    if missing:
        print(f"  WARNING: {len(missing)} segments missing from {provider_dir.name}: {missing[:5]}")
        return False
    out_path.write_text("\n".join(parts), encoding="utf-8")
    words = len(out_path.read_text().split())
    print(f"  assembled {out_path.name} ({words:,} words)")
    return True


def ab_report(
    code: str,
    seg_dir: Path,
    dir_a: Path,
    dir_b: Path,
    report_path: Path,
    label_a: str = "Anthropic",
    label_b: str = "OpenAI",
    model_a: str = ANTHROPIC_MODEL,
    model_b: str = OPENAI_MODEL,
) -> None:
    segments = sorted(seg_dir.glob("seg-*.md"))
    lines = [f"# A/B Translation Report: {code.upper()}\n",
             f"{label_a}: {model_a}  |  {label_b}: {model_b}\n",
             f"Total segments: {len(segments)}\n",
             "---\n"]

    total_words_a = 0
    total_words_b = 0
    diff_segments = 0

    for seg in segments:
        a_file = dir_a / seg.name
        b_file = dir_b / seg.name
        src_text = seg.read_text(encoding="utf-8")
        heading = re.search(r"^# .+", src_text, re.MULTILINE)
        heading_text = heading.group(0) if heading else seg.name

        a_text = a_file.read_text(encoding="utf-8") if a_file.exists() else "(MISSING)"
        b_text = b_file.read_text(encoding="utf-8") if b_file.exists() else "(MISSING)"

        a_words = len(a_text.split())
        b_words = len(b_text.split())
        total_words_a += a_words
        total_words_b += b_words

        ratio = difflib.SequenceMatcher(None,
            a_text[:2000], b_text[:2000]).ratio()

        if ratio < 0.85:
            diff_segments += 1
            lines.append(f"\n## {heading_text} ({seg.name})\n")
            lines.append(f"**Similarity:** {ratio:.0%} — divergent, worth reviewing\n")
            lines.append(f"**Word count:** {label_a}={a_words}, {label_b}={b_words}\n")

            lines.append(f"\n**{label_a} (first 400 chars):**\n```\n")
            lines.append(a_text[:400].strip() + "\n```\n")
            lines.append(f"\n**{label_b} (first 400 chars):**\n```\n")
            lines.append(b_text[:400].strip() + "\n```\n")

    lines.insert(3, f"Divergent segments (similarity <85%): {diff_segments}\n")
    lines.insert(4, f"Word counts — {label_a}: {total_words_a:,}  {label_b}: {total_words_b:,}\n")

    report_path.write_text("".join(lines), encoding="utf-8")
    print(f"  A/B report → {report_path}")


def provider_ready(provider: str) -> bool:
    if provider == "aya":
        return True  # local vLLM; AYA_API_KEY optional
    if provider in ("anthropic", "openai"):
        return provider_llm_ready(provider)
    return False


def main() -> None:
    ap = argparse.ArgumentParser(description="A/B translation runner for Arjuna Badger Press")
    ap.add_argument("book_dir", type=Path)
    ap.add_argument("--codes", default="zu,af,xh,st,tn", help="comma-separated language codes")
    ap.add_argument("--temp", type=float, default=None,
                    help="override register temp (0–1) for all targets; default from LANGUAGES.json")
    ap.add_argument("--segments", default="", help="comma-separated segment indices to run (default: all)")
    ap.add_argument("--workers", type=int, default=4, help="parallel workers per provider")
    ap.add_argument("--provider", default="all",
                    choices=["anthropic", "openai", "aya", "aistb", "both", "all"])
    ap.add_argument("--resume", action="store_true", help="skip segments already translated")
    ap.add_argument("--report-only", action="store_true", help="skip translation, just regenerate reports")
    args = ap.parse_args()

    book_dir = args.book_dir.resolve()
    manifest = load_json(book_dir / "LANGUAGES.json")
    glossary = load_json(book_dir / manifest["glossary_preserve"])
    seg_dir = book_dir / "build" / ".translate" / "segments"

    if not seg_dir.exists():
        print(f"ERROR: segments not found at {seg_dir}")
        print(f"Run first: tools/translate_book.sh {book_dir} split")
        sys.exit(1)

    segments = sorted(seg_dir.glob("seg-*.md"))
    if not segments:
        print(f"ERROR: no seg-*.md files in {seg_dir}")
        sys.exit(1)

    filter_segs: set[str] = set()
    if args.segments:
        for idx in args.segments.split(","):
            filter_segs.add(f"seg-{int(idx.strip()):02d}.md")

    codes = [c.strip() for c in args.codes.split(",")]
    if args.provider in ("both", "all"):
        providers = ["anthropic", "openai", "aya"]
    elif args.provider == "both":
        providers = ["anthropic", "openai"]
    elif args.provider == "aistb":
        providers = ["aya"]
    else:
        providers = [args.provider]

    target_map = {t["code"]: t for t in manifest["targets"]}
    global_directives = manifest.get("global_directives", [])
    source_lang = manifest.get("source_language", "en")

    corpus = get_corpus()
    cstats = corpus.stats()
    print(f"Corpus: {cstats['entries']} entries ({cstats['by_lang']})")

    print(f"\nBook: {manifest['title']}")
    print(f"Languages: {', '.join(codes)}")
    print(f"Providers: {', '.join(providers)}")
    print(f"Segments: {len(segments)} total" + (f", filtering to {len(filter_segs)}" if filter_segs else ""))
    print(f"Workers: {args.workers}")
    print()

    for code in codes:
        if code not in target_map:
            print(f"WARNING: code '{code}' not in LANGUAGES.json targets, skipping")
            continue

        lang_obj = target_map[code]
        temp = target_temp(lang_obj, args.temp)
        print(f"\n{'='*60}")
        print(f"Language: {lang_obj['name']} ({code})  temp={temp:.2f}")
        print(f"{'='*60}")

        if not args.report_only:
            for provider in providers:
                if not provider_ready(provider):
                    if openrouter_mode():
                        print(f"  SKIP {provider}: OPENROUTER_API_KEY not set")
                    else:
                        key = "ANTHROPIC_API_KEY" if provider == "anthropic" else "OPENAI_API_KEY"
                        print(f"  SKIP {provider}: {key} not set (or set OPENROUTER_API_KEY)")
                    continue

                provider_dir = book_dir / "build" / ".translate" / f"{code}.{provider}"
                provider_dir.mkdir(parents=True, exist_ok=True)
                system = build_system(
                    lang_obj, glossary, global_directives, provider, temp=temp,
                )

                segs_to_run = [s for s in segments
                               if not filter_segs or s.name in filter_segs]

                print(f"\n  Provider: {provider} ({len(segs_to_run)} segments)")

                futures = {}
                with ThreadPoolExecutor(max_workers=args.workers) as pool:
                    for seg in segs_to_run:
                        out = provider_dir / seg.name
                        f = pool.submit(
                            translate_segment, provider, system, seg, out, args.resume,
                            source_lang, code, temp,
                        )
                        futures[f] = seg.name

                    done = 0
                    errors = 0
                    corpus_hits = 0
                    for f in as_completed(futures):
                        prov, seg_name, err, corpus_note = f.result()
                        done += 1
                        if err:
                            errors += 1
                            print(f"  ✗ {seg_name}: {err}")
                        else:
                            if corpus_note:
                                corpus_hits += 1
                            cached = "(cached)" if args.resume and (provider_dir / seg_name).exists() else ""
                            note = f" [{corpus_note}]" if corpus_note else ""
                            print(f"  ✓ {seg_name}{note} {cached}", end="\r")

                print(f"\n  {done} segments done, {errors} errors, {corpus_hits} corpus hits")

        # Reassemble
        work_dir = book_dir / "build" / ".translate"
        build_dir = book_dir / "build"

        for provider in providers:
            provider_dir = work_dir / f"{code}.{provider}"
            if not provider_dir.exists():
                continue
            out_path = build_dir / f"BOOK.{code}.{provider}.md"
            print(f"\n  Reassembling {provider}...")
            reassemble(seg_dir, provider_dir, out_path)

        # A/B reports — compare all provider pairs that exist
        present = [p for p in ["anthropic", "openai", "aya"]
                   if (work_dir / f"{code}.{p}").exists()]
        labels = {"anthropic": "Anthropic", "openai": "OpenAI", "aya": "Aya"}
        models = {"anthropic": ANTHROPIC_MODEL, "openai": OPENAI_MODEL, "aya": AYA_MODEL}
        if len(present) >= 2:
            ref = "anthropic" if "anthropic" in present else present[0]
            for other in present:
                if other == ref:
                    continue
                suffix = "" if (ref == "anthropic" and other == "openai") else f".{other}-vs-{ref}"
                report_path = work_dir / f"AB_REPORT.{code}{suffix}.md"
                print(f"\n  Generating comparison report ({ref} vs {other})...")
                ab_report(code, seg_dir,
                          work_dir / f"{code}.{ref}",
                          work_dir / f"{code}.{other}",
                          report_path,
                          label_a=labels[ref], label_b=labels[other],
                          model_a=models[ref], model_b=models[other])

    print("\nDone.")


if __name__ == "__main__":
    main()
