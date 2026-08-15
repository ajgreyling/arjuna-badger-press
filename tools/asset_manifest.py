#!/usr/bin/env python3
"""asset_manifest.py — build the committed map of heavy assets -> R2 keys.

The manifest is the contract that makes a binary-free repo reproducible. Git holds
this JSON (small, diffable, sorted); R2 holds the bytes. From the manifest you can
fetch exactly what a build needs, verify it arrived intact, and see in a git diff
when an asset changed.

Two classes, per the agreed scheme:

  served  — users fetch these through the app. Keys stay READABLE so URLs and
            presigning remain predictable.
  input   — build sources, never served directly. Keys are blobs/sha256/<hash>:
            immutable, self-deduplicating, never orphaned by a rename.

Regenerable build output (books/**/build/**) is deliberately EXCLUDED: it is
rebuilt by books/*/build.py and archived offline, never stored in git or R2.

LIVE-ROUTE CONSTRAINT: saas/api.py serves /downloads/<book>/audio/<file> from R2
key audiobooks/<book>/<file> — a different prefix from the URL. That mapping is in
production and is reproduced exactly here; changing it breaks working downloads.

Usage:
    ./tools/asset_manifest.py build press     [--out assets.manifest.json]
    ./tools/asset_manifest.py build platform
    ./tools/asset_manifest.py verify press    # manifest vs what's on disk now
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

HOME = Path.home()
PRESS = HOME / "code" / "arjuna-badger-press"
PLATFORM = HOME / "code" / "arjuna-badger-platform"

# Anything at or above this size is an asset, not source text.
HEAVY_EXTS = {
    ".pdf", ".epub", ".mp3", ".wav", ".m4a", ".m4b", ".opus", ".zip",
    ".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".psd", ".indd",
    ".otf", ".ttf", ".mp4", ".mov",
}
# Matches saas/api.py:_LARGE_AUDIO_EXTS — these take the live audiobooks/ prefix.
LARGE_AUDIO_EXTS = {".mp3", ".m4a", ".m4b", ".opus", ".zip"}

CHUNK = 1 << 20


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(CHUNK), b""):
            h.update(block)
    return h.hexdigest()


def press_entries(root: Path):
    """Press: build INPUTS (design sources, covers, brand). Content-addressed."""
    roots = ["books", "covers", "brand"]
    for top in roots:
        base = root / top
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*")):
            if not p.is_file() or p.is_symlink():
                continue
            rel = p.relative_to(root)
            # regenerable output is archived offline, never stored
            if "/build/" in f"/{rel.as_posix()}/":
                continue
            if p.suffix.lower() not in HEAVY_EXTS:
                continue
            yield rel, "input"


def platform_entries(root: Path):
    """Platform: SERVED files under the web public dir. Readable keys."""
    base = root / "saas" / "web" / "public"
    if not base.is_dir():
        return
    for p in sorted(base.rglob("*")):
        if not p.is_file() or p.is_symlink():
            continue
        if p.suffix.lower() not in HEAVY_EXTS:
            continue
        yield p.relative_to(root), "served"


def key_for(rel: Path, cls: str, digest: str) -> str:
    if cls == "input":
        return f"blobs/sha256/{digest}"
    parts = rel.as_posix().split("/")
    # strip the saas/web/public/ prefix -> the URL path the app serves
    url = parts[3:] if parts[:3] == ["saas", "web", "public"] else parts
    # LIVE MAPPING: downloads/<book>/audio/<file> (large) -> audiobooks/<book>/<file>
    if (
        len(url) == 4
        and url[0] == "downloads"
        and url[2] == "audio"
        and Path(url[3]).suffix.lower() in LARGE_AUDIO_EXTS
    ):
        return f"audiobooks/{url[1]}/{url[3]}"
    return "site/" + "/".join(url)


REPOS = {
    "press": (PRESS, press_entries),
    "platform": (PLATFORM, platform_entries),
}


def build(repo: str, out: str | None) -> int:
    root, gen = REPOS[repo]
    if not root.is_dir():
        sys.exit(f"error: repo not found: {root}")
    entries, total = [], 0
    for rel, cls in gen(root):
        p = root / rel
        try:
            digest = sha256_of(p)
        except OSError as exc:                      # unreadable file: fail loud
            sys.exit(f"error: cannot hash {rel}: {exc}")
        size = p.stat().st_size
        total += size
        entries.append(
            {
                "path": rel.as_posix(),
                "class": cls,
                "key": key_for(rel, cls, digest),
                "sha256": digest,
                "bytes": size,
            }
        )
        if len(entries) % 200 == 0:
            print(f"  ...{len(entries)} hashed", file=sys.stderr)

    entries.sort(key=lambda e: e["path"])           # deterministic: clean diffs
    doc = {
        "version": 1,
        "repo": repo,
        "bucket": "arjuna-badger-prod",
        "note": "Bytes live in R2; this file is the contract. Regenerable build output excluded.",
        "count": len(entries),
        "bytes": total,
        "entries": entries,
    }
    dest = Path(out) if out else root / "assets.manifest.json"
    dest.write_text(json.dumps(doc, indent=2, sort_keys=False) + "\n")
    print(f"{repo}: {len(entries)} assets, {total/2**30:.2f} GB -> {dest}")

    # Dedupe only happens for content-addressed keys. Served files keep readable
    # keys, so identical bytes at two paths remain two objects — report honestly
    # rather than implying a saving that will not occur.
    groups: dict[str, list[dict]] = {}
    for e in entries:
        groups.setdefault(e["sha256"], []).append(e)

    saved = saved_n = wasted = wasted_n = 0
    for grp in groups.values():
        if len(grp) < 2:
            continue
        extra = grp[0]["bytes"] * (len(grp) - 1)
        if len({e["key"] for e in grp}) == 1:
            saved, saved_n = saved + extra, saved_n + len(grp) - 1   # one object
        else:
            wasted, wasted_n = wasted + extra, wasted_n + len(grp) - 1
    if saved:
        print(f"  dedupe: {saved_n} duplicate inputs collapse to one object ({saved/2**20:.0f} MB saved)")
    if wasted:
        print(f"  duplicate served bytes ({wasted_n} files, readable keys do NOT dedupe): {wasted/2**20:.0f} MB")
    return 0


def verify(repo: str) -> int:
    root, _ = REPOS[repo]
    man = root / "assets.manifest.json"
    if not man.is_file():
        sys.exit(f"error: no manifest at {man} — run build first")
    doc = json.loads(man.read_text())
    missing = changed = ok = 0
    for e in doc["entries"]:
        p = root / e["path"]
        if not p.is_file():
            missing += 1
            print(f"  MISSING  {e['path']}")
        elif sha256_of(p) != e["sha256"]:
            changed += 1
            print(f"  CHANGED  {e['path']}")
        else:
            ok += 1
    print(f"{repo}: {ok} ok, {changed} changed, {missing} missing")
    return 1 if (changed or missing) else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("repo", choices=sorted(REPOS))
    b.add_argument("--out")
    v = sub.add_parser("verify")
    v.add_argument("repo", choices=sorted(REPOS))
    a = ap.parse_args()
    return build(a.repo, a.out) if a.cmd == "build" else verify(a.repo)


if __name__ == "__main__":
    raise SystemExit(main())
