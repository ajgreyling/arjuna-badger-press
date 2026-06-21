#!/usr/bin/env python3
"""Offline test: press translation pipeline loads SA urban corpus and injects BINDING CORPUS."""
from __future__ import annotations

import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PLATFORM = REPO.parent / "arjuna-badger-platform"
sys.path.insert(0, str(PLATFORM))

os.environ["REAL_LANGUAGE_CORPUS_DIR"] = str(REPO / "docs" / "corpus")

passed = failed = 0


def check(label: str, cond: bool, detail: str = "") -> None:
    global passed, failed
    if cond:
        passed += 1
        print(f"  ok   {label}")
    else:
        failed += 1
        print(f"  FAIL {label}  {(': ' + detail) if detail else ''}")


def main() -> int:
    print("=== translate_ab corpus offline ===")

    from saas.correction_corpus import get_corpus

    corpus = get_corpus()
    stats = corpus.stats()
    check("corpus loads", stats["entries"] > 0, f"got {stats['entries']}")
    check("af entries", stats["by_lang"].get("af", 0) >= 2200)
    check("zu entries", stats["by_lang"].get("zu", 0) >= 2200)
    check("xh entries", stats["by_lang"].get("xh", 0) >= 2200)
    check("st entries", stats["by_lang"].get("st", 0) >= 2200)
    check("tn entries", stats["by_lang"].get("tn", 0) >= 2200)
    check("sw entries", stats["by_lang"].get("sw", 0) >= 2200)
    check("corrections key parsed", stats["entries"] >= 13000)

    # Import build_system from translate_ab
    sys.path.insert(0, str(REPO / "tools"))
    import importlib.util
    spec = importlib.util.spec_from_file_location("translate_ab", REPO / "tools" / "translate_ab.py")
    tab = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tab)

    lang_obj = {"code": "af", "name": "Afrikaans", "directives": ["Use urban register."]}
    glossary = {
        "preserve_verbatim_all_languages": {
            "in_language_terms": {},
            "invented_entities": [],
            "proper_names": [],
        }
    }
    entries = corpus.retrieve("Hello there friend", "en", "af", 0.75)
    block = corpus.build_prompt_block(entries)
    system = tab.build_system(lang_obj, glossary, [], "aya", temp=0.75, corpus_block=block)
    check("BINDING CORPUS in system", "BINDING CORPUS" in system)
    check("corpus fix in system", "Howzit" in system or "lekker" in system.lower())

    route = corpus.route("Hello there", "en", "af", 0.75)
    check("exact route works", route.decision == "corpus_exact" and route.text == "Howzit")

    # register overlay pass: en→af AI output gets af→af register fixes
    overlaid, applied = corpus.overlay_all(
        "## Remme\n\nElke silinder het 'n suier.",
        "en", "af", 1.0,
    )
    check("register overlay Breke", "Breke" in overlaid)
    check("register overlay piston", "piston" in overlaid and "suier" not in overlaid)
    check("register entries applied", any(e.kind == "register" for e in applied))

    print(f"\n{'✓' if not failed else '✗'} {passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
