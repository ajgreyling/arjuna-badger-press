#!/usr/bin/env python3
"""r2_push.py — upload assets to R2 strictly from the committed manifest.

The manifest is the single source of truth. Nothing here re-derives which files
matter or what they are called: every object uploaded comes from an entry in
assets.manifest.json. If the two could disagree, they would eventually diverge,
and a "clean" repo would be missing bytes nobody noticed.

Two upload paths, because the key schemes differ:

  served  key = site/<path under saas/web/public>  — a straight mirror, so one
          rclone copy with --files-from moves them all.
  input   key = blobs/sha256/<hash>                — not path-shaped. A staging
          tree of HARDLINKS named by hash (costing no extra disk) lets a single
          rclone copy place them correctly.

Safety: --immutable and never --delete. This can add objects; it cannot
overwrite or remove one. Credentials come from the environment only.

Usage:
    . ~/.config/congo/r2.env      # or however you export the three vars
    ./tools/r2_push.py plan   platform
    ./tools/r2_push.py push   platform
    ./tools/r2_push.py verify platform
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BUCKET = "arjuna-badger-prod"
REMOTE = "r2"
HOME = Path.home()
ROOTS = {
    "press": HOME / "code" / "arjuna-badger-press",
    "platform": HOME / "code" / "arjuna-badger-platform",
}


def rclone_env() -> dict:
    for v in ("BLOB_ENDPOINT", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"):
        if not os.environ.get(v):
            sys.exit(f"error: {v} not set (source ~/.config/congo/r2.env)")
    env = dict(os.environ)
    env.update(
        RCLONE_CONFIG_R2_TYPE="s3",
        RCLONE_CONFIG_R2_PROVIDER="Cloudflare",
        RCLONE_CONFIG_R2_ENDPOINT=os.environ["BLOB_ENDPOINT"],
        RCLONE_CONFIG_R2_ACCESS_KEY_ID=os.environ["AWS_ACCESS_KEY_ID"],
        RCLONE_CONFIG_R2_SECRET_ACCESS_KEY=os.environ["AWS_SECRET_ACCESS_KEY"],
        RCLONE_CONFIG_R2_NO_CHECK_BUCKET="true",
    )
    return env


def load(repo: str):
    root = ROOTS[repo]
    man = root / "assets.manifest.json"
    if not man.is_file():
        sys.exit(f"error: no manifest at {man}")
    return root, json.loads(man.read_text())["entries"]


def remote_index(env: dict, prefixes: set[str]) -> dict[str, int]:
    """key -> size for every object under the prefixes we care about."""
    out: dict[str, int] = {}
    for pre in sorted(prefixes):
        r = subprocess.run(
            ["rclone", "lsf", "--recursive", "--format", "sp",
             "--separator", "\t", f"{REMOTE}:{BUCKET}/{pre}"],
            env=env, capture_output=True, text=True,
        )
        for line in r.stdout.splitlines():
            if "\t" not in line:
                continue
            # --format "sp" emits SIZE then PATH, in that order.
            size, path = line.split("\t", 1)
            try:
                out[f"{pre}/{path}"] = int(size)
            except ValueError:
                continue
    return out


def split(entries):
    served = [e for e in entries if e["key"].startswith("site/")]
    blobs = [e for e in entries if e["key"].startswith("blobs/sha256/")]
    other = [e for e in entries if e not in served and e not in blobs]
    return served, blobs, other


def plan(repo: str) -> int:
    root, entries = load(repo)
    env = rclone_env()
    served, blobs, other = split(entries)
    have = remote_index(env, {"site", "blobs", "audiobooks"})

    missing = [e for e in entries if e["key"] not in have]
    present = len(entries) - len(missing)
    mb = sum(e["bytes"] for e in missing) / 2**30

    print(f"{repo}: {len(entries)} in manifest — {present} already in R2, {len(missing)} to upload ({mb:.2f} GB)")
    print(f"  served (site/): {len([e for e in missing if e in served])} of {len(served)}")
    print(f"  inputs (blobs/): {len([e for e in missing if e in blobs])} of {len(blobs)}")
    if other:
        print(f"  other keys (e.g. audiobooks/): {len(other)}")
        for e in other[:5]:
            on_disk = (root / e['path']).is_file()
            print(f"    {e['key']}  on-disk={on_disk}")
    # size disagreement = the same key holding different bytes
    clash = [e for e in entries if e["key"] in have and have[e["key"]] != e["bytes"]]
    if clash:
        print(f"  !! {len(clash)} keys exist remotely with a DIFFERENT size — will NOT be overwritten:")
        for e in clash[:5]:
            print(f"     {e['key']}  local={e['bytes']}  remote={have[e['key']]}")
    return 0


def push(repo: str) -> int:
    root, entries = load(repo)
    env = rclone_env()
    served, blobs, other = split(entries)

    if served:
        base = root / "saas" / "web" / "public"
        lst = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False)
        n = 0
        for e in served:
            p = root / e["path"]
            if p.is_file():
                lst.write(str(p.relative_to(base)) + "\n")
                n += 1
        lst.close()
        print(f"== served: {n} files -> {REMOTE}:{BUCKET}/site")
        subprocess.run(
            ["rclone", "copy", "--files-from", lst.name, "--immutable",
             "--progress", "--transfers", "8", "--checkers", "16",
             str(base), f"{REMOTE}:{BUCKET}/site"],
            env=env, check=False,
        )
        os.unlink(lst.name)

    if blobs:
        stage = Path(tempfile.mkdtemp(prefix="r2blobs-"))
        n = 0
        for e in blobs:
            p = root / e["path"]
            if not p.is_file():
                continue
            link = stage / e["sha256"]
            if not link.exists():
                try:
                    os.link(p, link)          # hardlink: no extra disk used
                except OSError:
                    shutil.copy2(p, link)     # cross-device fallback
                n += 1
        print(f"== inputs: {n} unique blobs -> {REMOTE}:{BUCKET}/blobs/sha256")
        subprocess.run(
            ["rclone", "copy", "--immutable", "--progress",
             "--transfers", "8", "--checkers", "16",
             str(stage), f"{REMOTE}:{BUCKET}/blobs/sha256"],
            env=env, check=False,
        )
        shutil.rmtree(stage, ignore_errors=True)

    if other:
        print(f"note: {len(other)} entries use other prefixes and were not touched by this run")
    return 0


def verify(repo: str) -> int:
    _, entries = load(repo)
    env = rclone_env()
    have = remote_index(env, {"site", "blobs", "audiobooks"})
    ok = miss = bad = 0
    for e in entries:
        got = have.get(e["key"])
        if got is None:
            miss += 1
            if miss <= 10:
                print(f"  MISSING  {e['key']}")
        elif got != e["bytes"]:
            bad += 1
            print(f"  SIZE     {e['key']}  local={e['bytes']} remote={got}")
        else:
            ok += 1
    print(f"{repo}: {ok} verified, {bad} size-mismatch, {miss} missing")
    return 1 if (bad or miss) else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for c in ("plan", "push", "verify"):
        s = sub.add_parser(c)
        s.add_argument("repo", choices=sorted(ROOTS))
    a = ap.parse_args()
    return {"plan": plan, "push": push, "verify": verify}[a.cmd](a.repo)


if __name__ == "__main__":
    raise SystemExit(main())
