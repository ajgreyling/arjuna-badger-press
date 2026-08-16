#!/usr/bin/env python3
"""asset_gate.py — refuse to let heavy binaries back into git.

The repos were 10 GB and 11 GB because renders, covers and audio were committed
for years. Assets now live in Cloudflare R2 (bucket arjuna-badger-prod), tracked
by assets.manifest.json. This gate is what stops that from silently undoing
itself: rules in a doc are advice, a hook is a wall.

It blocks a commit when a staged file is:
  * a heavy type (image/audio/document/font) larger than MAX_BYTES, or
  * any heavy type under a build output directory, at any size.

Deliberately NOT blocked: text, code, svg, the manifest itself, and small icons
below the threshold — those belong in git.

Bypass, when you genuinely mean it:
    ABP_ALLOW_BINARY=1 git commit ...      # scoped, self-documenting
    git commit --no-verify                 # blunt, skips every hook

Exit 0 = clean, 1 = blocked. No third-party dependencies (runs anywhere git does).
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

MAX_BYTES = 2 * 1024 * 1024  # 2 MiB — above this, an asset belongs in R2

HEAVY_EXTS = {
    ".pdf", ".epub", ".mobi", ".azw3",
    ".mp3", ".wav", ".m4a", ".m4b", ".opus", ".flac", ".aac",
    ".mp4", ".mov", ".mkv", ".avi", ".webm",
    ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".psd", ".indd", ".webp", ".gif",
    ".zip", ".tar", ".gz", ".7z", ".dmg",
    ".otf", ".ttf", ".woff", ".woff2",
}

# Build output: regenerable by definition. No heavy file here belongs in git at
# any size — this is the exact directory that produced 1.4 GB of history.
BUILD_MARKERS = ("/build/", "/dist/", "/export/", "/renders/", "/_work/")

# Paths R2 already manages via assets.manifest.json. A heavy file here is blocked
# at ANY size: size is the wrong test once a directory is R2-backed, because a
# small mp3 re-added beside its migrated siblings is still a regression.
MANAGED_PREFIXES = (
    "saas/web/public/",   # platform: served assets  -> site/
    "books/",             # press: design inputs     -> blobs/sha256/
    "covers/",
    "brand/",
)

ALLOW_SUFFIXES = ("assets.manifest.json",)


def staged_files() -> list[str]:
    r = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        capture_output=True, text=True,
    )
    return [f for f in r.stdout.splitlines() if f.strip()]


def blob_size(path: str, rev: str | None = None) -> int:
    """Size of the committed/staged content, not the working-tree copy.

    rev=None  -> the index (pre-commit hook)
    rev="X"   -> that revision (CI, inspecting what actually landed)
    """
    spec = f"{rev}:{path}" if rev else f":{path}"
    r = subprocess.run(["git", "cat-file", "-s", spec],
                       capture_output=True, text=True)
    if r.returncode == 0:
        try:
            return int(r.stdout.strip())
        except ValueError:
            pass
    try:
        return os.path.getsize(path)
    except OSError:
        return 0


def main() -> int:
    # Same logic for the hook and for CI, so the two can never disagree about
    # what counts as a violation. CI passes an explicit file list and revision;
    # the hook passes neither and gets the staged set.
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--paths-from", metavar="FILE",
                    help="newline-separated paths to check (default: staged files)")
    ap.add_argument("--rev", help="size files at this revision (default: the index)")
    args = ap.parse_args()

    # The bypass is for a human at a keyboard, not for CI — honouring it there
    # would make the backstop bypassable by the very flag it exists to catch.
    if os.environ.get("ABP_ALLOW_BINARY") == "1" and not args.paths_from:
        print("[asset-gate] bypassed via ABP_ALLOW_BINARY=1")
        return 0

    if args.paths_from:
        try:
            files = [l.strip() for l in open(args.paths_from) if l.strip()]
        except OSError as exc:
            print(f"[asset-gate] cannot read {args.paths_from}: {exc}", file=sys.stderr)
            return 1
    else:
        files = staged_files()

    offenders: list[tuple[str, int, str]] = []
    for f in files:
        if f.endswith(ALLOW_SUFFIXES):
            continue
        ext = os.path.splitext(f)[1].lower()
        if ext not in HEAVY_EXTS:
            continue
        padded = f"/{f}"
        # Size is looked up LAZILY. The path rules block at any size, so asking for
        # bytes first would force a blobless CI clone to fetch content it never
        # needs — which is what made the first self-hosted run pull ~1 GB.
        if any(m in padded for m in BUILD_MARKERS):
            offenders.append((f, 0, "build output — regenerable, never committed"))
        elif f.startswith(MANAGED_PREFIXES):
            offenders.append((f, 0, "R2-managed path — belongs in assets.manifest.json at any size"))
        else:
            size = blob_size(f, args.rev)
            if size > MAX_BYTES:
                offenders.append((f, size, f"{size/2**20:.1f} MB exceeds the {MAX_BYTES/2**20:.0f} MB limit"))

    if not offenders:
        return 0

    # Identical file in both repos; the repo name is derived so neither copy drifts.
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True).stdout.strip()
    repo = "platform" if top.endswith("platform") else "press"
    tools = "~/code/arjuna-badger-press/tools"

    print("[asset-gate] COMMIT BLOCKED — these belong in R2, not git:\n", file=sys.stderr)
    for f, size, why in offenders:
        print(f"  {f}\n      {why}", file=sys.stderr)
    print(
        f"\n  Assets live in R2 (arjuna-badger-prod), tracked by assets.manifest.json.\n"
        f"  To add one properly:\n"
        f"      {tools}/asset_manifest.py build {repo}\n"
        f"      {tools}/r2_push.py push {repo}\n"
        f"      {tools}/r2_push.py verify {repo}\n"
        f"      git add assets.manifest.json\n"
        f"\n  If this file genuinely belongs in git:  ABP_ALLOW_BINARY=1 git commit ...\n",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
