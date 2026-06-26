#!/usr/bin/env python3
"""Produce the public-shelf audiobook formats for Die Vuur in die Donker.

Reuses make_m4b's chapter list, metadata and ffmetadata builder. From the 19
per-chapter masters this emits a ladder of formats, smallest-modern → universal:

  • .opus  — Opus (libopus, voice-tuned)  — most size-optimised, modern phones/apps
  • .m4a   — HE-AAC / AAC+ (Apple AudioToolbox aac_at, HE profile) — Apple-native, small
  • .mp3   — single-file (already produced by the renderer) — plays everywhere
  • -chapters.zip — the 19 per-chapter MP3s zipped — discrete tracks / sideloading
  • .m4b   — built separately by make_m4b.py (chaptered audiobook)

All chaptered containers (opus/m4a) carry the same embedded chapter markers +
cover + audiobook metadata as the M4B. Everything is loudness-normalised to the
same −19 LUFS target via the masters, then transcoded (no re-render).

Output → audio/emma-afrikaans-masters/publish/

Usage:
    python3 audio/make_audio_formats.py            # build all
    python3 audio/make_audio_formats.py --dry-run
    python3 audio/make_audio_formats.py --only opus,heaac,mp3,zip
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import zipfile
from pathlib import Path

# reuse everything from the M4B packager (same dir)
sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_m4b as mb  # noqa: E402

FFMPEG = mb.FFMPEG
FFPROBE = mb.FFPROBE
COVER = mb.COVER
OUT_DIR = mb.OUT_DIR
MASTERS_DIR = mb.MASTERS_DIR
PRESS_DIR = mb.PRESS_DIR
PUBLISH_DIR = OUT_DIR / "publish"
WORK = OUT_DIR / "_work_formats"

# Public deliverable base name (matches the M4B's display title)
BASE = "Die Vuur in die Donker"

# Format knobs — voice content, mono 44.1k throughout (matches the masters).
OPUS_BR = "24k"     # Opus is transparent for speech well under 32k
HEAAC_BR = "32k"    # HE-AAC/AAC+ sweet spot for mono speech
HEAAC_PROFILE = "29"  # ffmpeg numeric id for HE-AAC (aac_at exposes it this way)


def _concat_normalised(with_dur, codec_args: list[str], out: Path, *, cover: bool,
                       chapters_meta: Path | None) -> int:
    """Concat the masters → one stream, transcode with codec_args, attach cover+chapters."""
    WORK.mkdir(parents=True, exist_ok=True)
    listf = WORK / "concat.txt"
    listf.write_text("".join(f"file '{p.resolve()}'\n" for p, _, _ in with_dur), encoding="utf-8")
    # 1) concat the mp3 masters losslessly into one mp3 (stream copy)
    joined = WORK / "joined.mp3"
    subprocess.run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(listf),
                    "-c", "copy", str(joined)], check=True, capture_output=True)
    # 2) transcode + mux metadata/chapters/cover
    cmd = [FFMPEG, "-y", "-i", str(joined)]
    if chapters_meta:
        cmd += ["-i", str(chapters_meta)]
    map_args = ["-map", "0:a"]
    cover_in_idx = None
    if cover and COVER.exists():
        cmd += ["-i", str(COVER)]
        cover_in_idx = 2 if chapters_meta else 1
        map_args += ["-map", f"{cover_in_idx}:v"]
    if chapters_meta:
        cmd += ["-map_metadata", "1", "-map_chapters", "1"]
    cmd += map_args + codec_args
    if cover_in_idx is not None:
        cmd += ["-c:v", "mjpeg", "-disposition:v:0", "attached_pic"]
    cmd += [str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  !! encode failed for {out.name}:\n{r.stderr[-1500:]}")
        return 1
    return 0


def build_opus(with_dur, meta: Path) -> int:
    out = PUBLISH_DIR / f"{BASE}.opus"
    print(f"  • Opus  → {out.name}  (libopus {OPUS_BR} mono, voice)")
    # Opus in .opus (ogg) carries chapter metadata as tags; players vary, but
    # title/album/cover ride along. Voice-tuned for speech efficiency.
    args = ["-c:a", "libopus", "-b:a", OPUS_BR, "-ac", "1", "-ar", "48000",
            "-application", "voip", "-vbr", "on"]
    # .opus container can't hold an attached_pic the way mp4 does; skip cover for opus.
    return _concat_normalised(with_dur, args, out, cover=False, chapters_meta=meta)


def build_heaac(with_dur, meta: Path) -> int:
    out = PUBLISH_DIR / f"{BASE}.m4a"
    print(f"  • HE-AAC/AAC+ → {out.name}  (aac_at HE {HEAAC_BR} mono)")
    args = ["-c:a", "aac_at", "-profile:a", HEAAC_PROFILE, "-b:a", HEAAC_BR,
            "-ac", "1", "-ar", "44100", "-movflags", "+faststart", "-f", "mp4"]
    return _concat_normalised(with_dur, args, out, cover=True, chapters_meta=meta)


def build_mp3_single(with_dur) -> int:
    """The renderer already makes a full-book MP3; copy it into publish/ under the
    public name (universal baseline)."""
    src = OUT_DIR / "the-amber-winter-afrikaans-emma-master.mp3"
    out = PUBLISH_DIR / f"{BASE}.mp3"
    if not src.exists():
        print(f"  !! single MP3 master missing: {src.name} — run the renderer first")
        return 1
    print(f"  • MP3 single → {out.name}  (universal, from renderer master)")
    import shutil
    shutil.copy2(src, out)
    return 0


def stage_m4b() -> int:
    """Copy the chaptered M4B (built by make_m4b.py) into publish/ so the site sees it
    alongside the other download formats."""
    src = OUT_DIR / f"{BASE}.m4b"
    out = PUBLISH_DIR / f"{BASE}.m4b"
    if not src.exists():
        print(f"  !! M4B missing: {src.name} — run make_m4b.py first"); return 1
    import shutil
    shutil.copy2(src, out)
    print(f"  • M4B → {out.name}  (chaptered audiobook, from make_m4b.py)")
    return 0


def build_chapter_zip() -> int:
    out = PUBLISH_DIR / f"{BASE} — hoofstukke (mp3).zip"
    masters = sorted(MASTERS_DIR.glob("*.mp3"))
    if not masters:
        print("  !! no masters to zip"); return 1
    print(f"  • Per-chapter ZIP → {out.name}  ({len(masters)} MP3s)")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_STORED) as z:  # mp3 already compressed
        for m in masters:
            z.write(m, arcname=m.name)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", default="opus,heaac,mp3,zip,m4b",
                    help="comma list: opus,heaac,mp3,zip,m4b (default all)")
    a = ap.parse_args()
    want = {s.strip() for s in a.only.split(",") if s.strip()}

    chapters = mb.resolve_chapters()
    with_dur = []
    total = 0.0
    for path, title in chapters:
        d = mb.probe_duration(path)
        total += d
        with_dur.append((path, title, d))
    h, rem = divmod(int(total), 3600); mm, ss = divmod(rem, 60)
    print(f"[{BASE}] {len(chapters)} chapters, {h}h{mm:02d}m{ss:02d}s")
    print(f"  formats: {', '.join(sorted(want))}")
    if a.dry_run:
        print("  (dry-run — nothing written)")
        return 0

    PUBLISH_DIR.mkdir(parents=True, exist_ok=True)
    meta = WORK / "ffmeta.txt"
    WORK.mkdir(parents=True, exist_ok=True)
    meta.write_text(mb.build_ffmetadata(with_dur), encoding="utf-8")

    rc = 0
    if "opus" in want:  rc |= build_opus(with_dur, meta)
    if "heaac" in want: rc |= build_heaac(with_dur, meta)
    if "mp3" in want:   rc |= build_mp3_single(with_dur)
    if "zip" in want:   rc |= build_chapter_zip()
    if "m4b" in want:   rc |= stage_m4b()

    print("\n  ── publish/ ──")
    for f in sorted(PUBLISH_DIR.iterdir()):
        if f.is_file():
            print(f"    {f.stat().st_size/1e6:7.1f} MB  {f.name}")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
