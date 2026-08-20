#!/usr/bin/env python3
"""Find NEAR-duplicate prose using local embeddings. Free — no API spend.

`prose_tics.py` finds sentences repeated VERBATIM. That is the easy half. The
half it cannot see is the paraphrase: once a de-LLM pass recasts a duplicated
line, the wording differs and exact matching goes quiet — but the reader still
meets the same idea for the fourth time. Recasting can therefore *hide*
duplication rather than remove it, and the exact-match count will happily report
progress that isn't there.

This embeds every sentence with a local Ollama model (nomic-embed-text) and
flags pairs above a cosine threshold. Runs on the machine, costs nothing, and
so can be run as often as you like.

Judgment stays with the human: high similarity is a LEAD, not a verdict. Two
sentences describing the same recurring object (a river, a desk, a slogan) will
score high and may both be earned.

Usage:
    python3 tools/semantic_dupes.py books/<book> \\
        --protect books/<book>/canon/MOTIFS_PROTECTED.txt --threshold 0.86
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
import urllib.request

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from prose_tics import is_protected, load_protect, normalise, sentences  # noqa: E402

OLLAMA = "http://localhost:11434/api/embed"
MODEL = "nomic-embed-text"
BATCH = 64


def embed(texts: list[str], model: str) -> np.ndarray:
    out = []
    for i in range(0, len(texts), BATCH):
        chunk = texts[i:i + BATCH]
        body = json.dumps({"model": model, "input": chunk}).encode()
        req = urllib.request.Request(OLLAMA, data=body,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=300) as r:
            out.extend(json.load(r)["embeddings"])
        print(f"  embedded {min(i + BATCH, len(texts))}/{len(texts)}", end="\r", flush=True)
    print()
    # Ollama embedding magnitudes can overflow a float32 norm before division.
    # Normalise in float64, zero any malformed component, then keep float64 for
    # the cosine matrix so a local-model quirk cannot emit false leads.
    v = np.asarray(out, dtype=np.float64)
    v = np.nan_to_num(v, nan=0.0, posinf=0.0, neginf=0.0)
    norms = np.linalg.norm(v, axis=1, keepdims=True)
    # A local embedding backend may occasionally return a zero/non-finite row.
    # Keep the scan numerically honest: invalid rows become zero-similarity leads
    # rather than poisoning the whole matrix with NaN/overflow warnings.
    valid = np.isfinite(norms[:, 0]) & (norms[:, 0] > 1e-12)
    normalised = np.zeros_like(v, dtype=np.float64)
    normalised[valid] = v[valid] / norms[valid]
    return np.clip(np.nan_to_num(normalised, nan=0.0, posinf=0.0, neginf=0.0), -1.0, 1.0)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("book", type=pathlib.Path)
    ap.add_argument("--protect", type=pathlib.Path)
    ap.add_argument("--threshold", type=float, default=0.86)
    ap.add_argument("--min-words", type=int, default=8)
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--limit", type=int, default=40)
    args = ap.parse_args()

    protect = load_protect(args.protect)
    rows: list[tuple[str, str]] = []
    for path in sorted((args.book / "build" / "chapters").glob("*.md")):
        for s in sentences(path.read_text()):
            if len(s.split()) >= args.min_words:
                rows.append((path.name, s))
    if not rows:
        sys.exit("no sentences found")

    print(f"{len(rows)} sentences from {args.book.name}")
    vecs = embed([s for _, s in rows], args.model)

    # np.matmul on some Accelerate builds emits bogus overflow warnings for
    # this otherwise finite unit matrix. einsum computes the same cosine dot
    # products without that backend pathology.
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        sim = np.einsum("ik,jk->ij", vecs, vecs, optimize=True)
    sim = np.nan_to_num(sim, nan=0.0, posinf=0.0, neginf=0.0)
    np.fill_diagonal(sim, 0.0)
    hits = np.argwhere(np.triu(sim) >= args.threshold)

    found = []
    for i, j in hits:
        ch_a, a = rows[i]
        ch_b, b = rows[j]
        na, nb = normalise(a), normalise(b)
        if na == nb:
            continue                      # exact dup — prose_tics already owns this
        if is_protected(na, protect) or is_protected(nb, protect):
            continue                      # deliberate refrain
        found.append((float(sim[i, j]), ch_a, a, ch_b, b))

    found.sort(reverse=True)
    print(f"\n{len(found)} near-duplicate pairs at cosine >= {args.threshold} "
          f"(exact matches and protected motifs excluded)\n")
    for score, ch_a, a, ch_b, b in found[:args.limit]:
        same = "same chapter" if ch_a == ch_b else f"{ch_a} / {ch_b}"
        print(f"[{score:.3f}] {same}")
        print(f"   A: {a[:150]}")
        print(f"   B: {b[:150]}\n")
    if len(found) > args.limit:
        print(f"... {len(found) - args.limit} more not shown (raise --limit)")


if __name__ == "__main__":
    main()
