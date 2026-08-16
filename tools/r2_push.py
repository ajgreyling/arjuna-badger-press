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


def remote_index(env: dict, bucket: str, prefixes: set[str]) -> dict[str, int]:
    """key -> size for every object under the prefixes we care about, in one bucket."""
    out: dict[str, int] = {}
    for pre in sorted(prefixes):
        target = f"{REMOTE}:{bucket}/{pre}" if pre else f"{REMOTE}:{bucket}"
        r = subprocess.run(
            ["rclone", "lsf", "--recursive", "--format", "sp",
             "--separator", "\t", target],
            env=env, capture_output=True, text=True,
        )
        for line in r.stdout.splitlines():
            if "\t" not in line:
                continue
            # --format "sp" emits SIZE then PATH, in that order.
            size, path = line.split("\t", 1)
            try:
                out[f"{pre}/{path}" if pre else path] = int(size)
            except ValueError:
                continue
    return out


def by_bucket(entries):
    """Group manifest entries by the bucket each one declares."""
    g: dict[str, list] = {}
    for e in entries:
        g.setdefault(e.get("bucket", BUCKET), []).append(e)
    return g


def prefixes_for(entries) -> set:
    """Top-level key prefixes to list when indexing a bucket ('' = whole bucket)."""
    pres = set()
    for e in entries:
        head = e["key"].split("/")[0]
        pres.add(head if "/" in e["key"] else "")
    return pres


def plan(repo: str) -> int:
    root, entries = load(repo)
    env = rclone_env()
    rc = 0
    for bucket, grp in sorted(by_bucket(entries).items()):
        have = remote_index(env, bucket, prefixes_for(grp))
        if not have:
            # An empty index is ambiguous: an empty bucket, or one this token
            # cannot reach. Say so rather than reporting "everything to upload".
            probe = subprocess.run(["rclone", "lsf", f"{REMOTE}:{bucket}", "--max-depth", "1"],
                                   env=env, capture_output=True, text=True)
            if probe.returncode != 0:
                print(f"{bucket}: NOT REACHABLE — {len(grp)} entries "
                      f"({sum(e['bytes'] for e in grp)/2**30:.2f} GB) cannot be planned")
                print("  create the bucket and grant this token object access, then re-run")
                rc = 1
                continue
        missing = [e for e in grp if e["key"] not in have]
        gb = sum(e["bytes"] for e in missing) / 2**30
        print(f"{bucket}: {len(grp)} entries — {len(grp)-len(missing)} present, "
              f"{len(missing)} to upload ({gb:.2f} GB)")
        clash = [e for e in grp if e["key"] in have and have[e["key"]] != e["bytes"]]
        if clash:
            print(f"  !! {len(clash)} keys exist with a DIFFERENT size — --immutable will NOT overwrite:")
            for e in clash[:5]:
                print(f"     {e['key']}  local={e['bytes']}  remote={have[e['key']]}")
    return rc


def push(repo: str) -> int:
    root, entries = load(repo)
    env = rclone_env()
    pub_base = root / "saas" / "web" / "public"

    for bucket, grp in sorted(by_bucket(entries).items()):
        # Content-addressed inputs: key is blobs/sha256/<hash>, not path-shaped, so a
        # hardlink staging tree (no extra disk) lets one rclone copy place them.
        blobs = [e for e in grp if e["key"].startswith("blobs/sha256/")]
        # Everything else mirrors a path. dest_prefix is whatever precedes that mirror:
        # "site" in the private bucket, "" in the public one (key IS the URL path).
        mirrored = [e for e in grp if e not in blobs]

        if mirrored:
            groups: dict[str, list] = {}
            for e in mirrored:
                rel = e["path"].split("saas/web/public/", 1)[-1]
                prefix = e["key"][: -len(rel)].strip("/") if e["key"].endswith(rel) else None
                if prefix is None:
                    continue          # e.g. the remapped audiobooks/ keys — left alone
                groups.setdefault(prefix, []).append(rel)
            for prefix, rels in sorted(groups.items()):
                lst = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False)
                n = 0
                for rel in rels:
                    if (pub_base / rel).is_file():
                        lst.write(rel + "\n"); n += 1
                lst.close()
                dest = f"{REMOTE}:{bucket}/{prefix}" if prefix else f"{REMOTE}:{bucket}"
                print(f"== {n} files -> {dest}")
                subprocess.run(
                    ["rclone", "copy", "--files-from", lst.name, "--immutable",
                     "--progress", "--transfers", "8", "--checkers", "16",
                     str(pub_base), dest],
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
            print(f"== inputs: {n} unique blobs -> {REMOTE}:{bucket}/blobs/sha256")
            subprocess.run(
                ["rclone", "copy", "--immutable", "--progress",
                 "--transfers", "8", "--checkers", "16",
                 str(stage), f"{REMOTE}:{bucket}/blobs/sha256"],
                env=env, check=False,
            )
            shutil.rmtree(stage, ignore_errors=True)
    return 0


def verify(repo: str) -> int:
    _, entries = load(repo)
    env = rclone_env()
    t_ok = t_bad = t_miss = 0
    for bucket, grp in sorted(by_bucket(entries).items()):
        have = remote_index(env, bucket, prefixes_for(grp))
        ok = miss = bad = 0
        for e in grp:
            got = have.get(e["key"])
            if got is None:
                miss += 1
                if miss <= 5:
                    print(f"  MISSING  {bucket}/{e['key']}")
            elif got != e["bytes"]:
                bad += 1
                print(f"  SIZE     {bucket}/{e['key']}  local={e['bytes']} remote={got}")
            else:
                ok += 1
        print(f"{bucket}: {ok} verified, {bad} size-mismatch, {miss} missing")
        t_ok, t_bad, t_miss = t_ok + ok, t_bad + bad, t_miss + miss
    print(f"{repo}: {t_ok} verified, {t_bad} size-mismatch, {t_miss} missing (all buckets)")
    return 1 if (t_bad or t_miss) else 0


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
