#!/usr/bin/env python3
"""Package Die Laaste Strooi Emma masters into a chaptered .m4b.

Same pattern as books/the-amber-winter/audio/make_m4b.py:
  - EBU R128 loudness to -19 LUFS
  - chapter markers
  - media_type=2 (Apple Books audiobook)
  - optional cover if design/cover.png exists beside this script's out dir

Usage:
    python3 make_die_laaste_strooi_m4b.py
    python3 make_die_laaste_strooi_m4b.py --dry-run
    python3 make_die_laaste_strooi_m4b.py --no-normalize
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

AUDIO_DIR = Path(__file__).resolve().parent
OUT_DIR = AUDIO_DIR / "die-laaste-strooi" / "emma-masters"
MASTERS_DIR = OUT_DIR / "masters"
WORK_DIR = OUT_DIR / "_work_m4b"
OUT_M4B = OUT_DIR / "Die Laaste Strooi.m4b"
COVER_CANDIDATES = [
    OUT_DIR / "cover.png",
    OUT_DIR / "cover.jpg",
    AUDIO_DIR / "die-laaste-strooi" / "cover.png",
]

FFMPEG = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"
FFPROBE = shutil.which("ffprobe") or "/opt/homebrew/bin/ffprobe"

TITLE = "Die Laaste Strooi"
SERIES = "The Writing Desk"
AUTHOR = "Andries J. Greyling"
NARRATOR = "Emma Lilliana"
YEAR = "2026"
COPYRIGHT = f"© {YEAR} Andries J. Greyling / Arjuna Badger Press"
COMMENT = (
    "Afrikaans kortverhaal. Boesmanland. "
    "Inhoudswaarskuwing: geweld, moord; geskik vir volwasse lesers."
)
GENRE = "Audiobook"
PUBLISHER = "Arjuna Badger Press"
LUFS_TARGET = -19.0
BITRATE = "64k"

CHAPTERS: list[tuple[str, str]] = [
    ("00-i-die-soen", "I. Die soen"),
    ("01-ii-die-twee-broers", "II. Die twee broers"),
    ("02-iii-die-juffrou", "III. Die juffrou"),
    ("03-iv-die-vlam", "IV. Die vlam"),
    ("04-v-die-oorhandiging", "V. Die oorhandiging"),
    ("05-vi-die-nasie", "VI. Die nasie"),
    ("06-vii-wat-oorbly", "VII. Wat oorbly"),
]


def find_cover() -> Path | None:
    for path in COVER_CANDIDATES:
        if path.is_file():
            return path
    return None


def resolve_chapters() -> list[tuple[Path, str]]:
    resolved: list[tuple[Path, str]] = []
    missing: list[str] = []
    for stem, title in CHAPTERS:
        path = MASTERS_DIR / f"{stem}.mp3"
        if path.is_file():
            resolved.append((path, title))
        else:
            missing.append(f"  MISSING: {stem}")
    if missing:
        print("!! Chapter masters not found. Render first:")
        print("\n".join(missing))
        sys.exit(1)
    return resolved


def probe_duration(path: Path) -> float:
    r = subprocess.run(
        [
            FFPROBE, "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(path),
        ],
        check=True, capture_output=True, text=True,
    )
    return float(r.stdout.strip())


def build_ffmetadata(chapters: list[tuple[Path, str, float]]) -> str:
    lines = [";FFMETADATA1"]

    def tag(k: str, v: str) -> None:
        if v:
            v = (
                v.replace("\\", "\\\\")
                .replace("=", "\\=")
                .replace(";", "\\;")
                .replace("#", "\\#")
                .replace("\n", "\\\n")
            )
            lines.append(f"{k}={v}")

    tag("title", TITLE)
    tag("album", TITLE)
    tag("artist", AUTHOR)
    tag("album_artist", AUTHOR)
    tag("composer", NARRATOR)
    tag("genre", GENRE)
    tag("date", YEAR)
    tag("copyright", COPYRIGHT)
    tag("comment", COMMENT)
    tag("show", SERIES)
    tag("track", "1")
    tag("publisher", PUBLISHER)
    tag("media_type", "2")
    t_ms = 0
    for _, title, dur in chapters:
        start = t_ms
        end = t_ms + int(round(dur * 1000))
        lines += [
            "",
            "[CHAPTER]",
            "TIMEBASE=1/1000",
            f"START={start}",
            f"END={end}",
            f"title={title}",
        ]
        t_ms = end
    return "\n".join(lines) + "\n"


def package(chapters: list[tuple[Path, str]], normalize: bool, dry_run: bool) -> int:
    cover = find_cover()
    print(f"[{TITLE}] {len(chapters)} chapter(s):")
    with_dur: list[tuple[Path, str, float]] = []
    total = 0.0
    for path, title in chapters:
        dur = probe_duration(path)
        total += dur
        with_dur.append((path, title, dur))
        print(f"  {path.stem:40} {dur/60:5.1f} min  →  {title}")
    mm, ss = divmod(int(total), 60)
    print(f"  TOTAL: {mm}m{ss:02d}s   cover: {cover.name if cover else 'none'}")

    if dry_run:
        print("  (dry-run, nothing written)")
        return 0

    WORK_DIR.mkdir(parents=True, exist_ok=True)
    metaf = WORK_DIR / "ffmeta.txt"
    metaf.write_text(build_ffmetadata(with_dur), encoding="utf-8")

    src_files: list[Path] = []
    if normalize:
        print(f"  Normalising to {LUFS_TARGET:g} LUFS mono {BITRATE}…")
        for path, _, _ in with_dur:
            norm = WORK_DIR / f"norm_{path.stem}.m4a"
            af = f"loudnorm=I={LUFS_TARGET}:TP=-1.5:LRA=11"
            r = subprocess.run(
                [
                    FFMPEG, "-y", "-i", str(path), "-af", af,
                    "-c:a", "aac", "-b:a", BITRATE, "-ac", "1", "-ar", "44100", str(norm),
                ],
                capture_output=True, text=True,
            )
            if r.returncode != 0:
                print(f"  !! normalise failed for {path.stem}:\n{r.stderr[-600:]}")
                return 1
            src_files.append(norm)
    else:
        # Remux mp3→aac first so concat is homogeneous
        for path, _, _ in with_dur:
            aac = WORK_DIR / f"raw_{path.stem}.m4a"
            r = subprocess.run(
                [
                    FFMPEG, "-y", "-i", str(path),
                    "-c:a", "aac", "-b:a", BITRATE, "-ac", "1", "-ar", "44100", str(aac),
                ],
                capture_output=True, text=True,
            )
            if r.returncode != 0:
                print(f"  !! encode failed for {path.stem}:\n{r.stderr[-600:]}")
                return 1
            src_files.append(aac)

    listf = WORK_DIR / "concat.txt"
    listf.write_text("".join(f"file '{p.resolve()}'\n" for p in src_files), encoding="utf-8")
    tmp = WORK_DIR / "nochap.m4a"
    subprocess.run(
        [FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(listf), "-c", "copy", str(tmp)],
        check=True, capture_output=True,
    )

    if OUT_M4B.exists():
        archive = OUT_DIR / "_archive"
        archive.mkdir(parents=True, exist_ok=True)
        from datetime import datetime, timezone
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        OUT_M4B.rename(archive / f"{OUT_M4B.stem}.{ts}{OUT_M4B.suffix}")

    cmd = [FFMPEG, "-y", "-i", str(tmp), "-i", str(metaf)]
    map_args = ["-map", "0:a"]
    if cover is not None:
        cmd += ["-i", str(cover)]
        map_args += ["-map", "2:v"]
    cmd += ["-map_metadata", "1", "-map_chapters", "1"] + map_args + ["-c", "copy"]
    if cover is not None:
        cmd += ["-c:v", "mjpeg", "-disposition:v:0", "attached_pic"]
    cmd += ["-movflags", "+faststart", "-f", "mp4", str(OUT_M4B)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"!! ffmpeg mux failed:\n{r.stderr[-2000:]}")
        return 1

    size_mb = OUT_M4B.stat().st_size / 1e6
    print(f"\n  OK {OUT_M4B}  ({size_mb:.1f} MB)")

    chk = subprocess.run(
        [FFPROBE, "-v", "error", "-show_chapters", "-of", "json", str(OUT_M4B)],
        capture_output=True, text=True,
    )
    try:
        nch = len(json.loads(chk.stdout).get("chapters", []))
        print(f"  verified: {nch} chapter marker(s)")
    except Exception:
        pass

    latest = Path("/Users/ajgreyling/code/arjuna-badger/latest-audio") / OUT_M4B.name
    latest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUT_M4B, latest)
    print(f"  copied → {latest}")
    print("  AirDrop .m4b to iPhone → Apple Books.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-normalize", action="store_true")
    args = ap.parse_args()
    if not Path(FFMPEG).exists() and shutil.which("ffmpeg") is None:
        print("ffmpeg not found", file=sys.stderr)
        return 1
    chapters = resolve_chapters()
    return package(chapters, normalize=not args.no_normalize, dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
