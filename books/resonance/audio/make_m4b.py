#!/usr/bin/env python3
"""Package Resonance (Steven G.) chapter MP3s into an M4B audiobook.

Reads numbered masters in audio/steven-g/ and packages them into a single .m4b
with chapter markers, cover art, audiobook metadata, and EBU R128 loudness
normalisation to −19 LUFS.

Output:
  audio/steven-g/RESONANCE.m4b

Usage:
    python3 audio/make_m4b.py
    python3 audio/make_m4b.py --no-normalize
    python3 audio/make_m4b.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

AUDIO_DIR = Path(__file__).resolve().parent
BOOK_DIR = AUDIO_DIR.parent
PRESS_DIR = BOOK_DIR.parents[1]
MASTERS_DIR = AUDIO_DIR / "steven-g"
COVER = BOOK_DIR / "design" / "cover.png"
OUT_M4B = MASTERS_DIR / "RESONANCE.m4b"
WORK_DIR = MASTERS_DIR / "_work_m4b"

FFMPEG = "/opt/homebrew/bin/ffmpeg"
FFPROBE = "/opt/homebrew/bin/ffprobe"

TITLE = "RESONANCE"
SERIES = "The African Gold Trilogy"
AUTHOR = "Andries J. Greyling"
NARRATOR = "Steven G."
YEAR = "2026"
COPYRIGHT = f"© {YEAR} Andries J. Greyling / Arjuna Badger Press"
COMMENT = (
    "Book I of The African Gold Trilogy. "
    "A grounded science-real thriller set in South Africa."
)
GENRE = "Audiobook"
PUBLISHER = "Arjuna Badger Press"

LUFS_TARGET = -19.0
BITRATE = "64k"

# Ordered chapter list: (filename, display_title)
CHAPTERS: list[tuple[str, str]] = [
    ("00-Resonance-Contents.mp3", "Contents"),
    ("01-Resonance-Intro.mp3", "Intro"),
    ("02-Resonance-The-Land-Remembers.mp3", "The Land Remembers"),
    ("03-Resonance-The-Wire-Push-Car.mp3", "The Wire Push Car"),
    ("04-Resonance-The-Thing-That-Should-Not-Exist.mp3",
     "The Thing That Should Not Exist"),
    ("05-Resonance-Stable-Chaos.mp3", "Stable Chaos"),
    ("06-Resonance-Learning-Each-Other.mp3", "Learning Each Other"),
    ("07-Resonance-A-Number-That-Wont-Close.mp3", "A Number That Won't Close"),
    ("08-Resonance-The-Preservation-Run.mp3", "The Preservation Run"),
    ("09-Resonance-Wisdom-and-Consequence.mp3", "Wisdom and Consequence"),
    ("10-Resonance-Anomalous-Signals.mp3", "Anomalous Signals"),
    ("11-Resonance-Pressure-Builds.mp3", "Pressure Builds"),
    ("12-Resonance-Iron-Ridge-Fault.mp3", "Iron Ridge Fault"),
    ("13-Resonance-The-Path-No-One-Can-Walk.mp3", "The Path No One Can Walk"),
    ("14-Resonance-Descent.mp3", "Descent"),
    ("15-Resonance-Contact.mp3", "Contact"),
    ("16-Resonance-Collapse.mp3", "Collapse"),
    ("17-Resonance-The-Final-Choice.mp3", "The Final Choice"),
    ("18-Resonance-Black-Box.mp3", "Black Box"),
    ("19-Resonance-Appendix-—-The-Court-as-a-Model-of-the-Psyche.mp3",
     "Appendix — The Court as a Model of the Psyche"),
    ("20-Resonance-A-Readers-Glossary.mp3", "A Reader's Glossary"),
    ("21-Resonance-Acknowledgements.mp3", "Acknowledgements"),
    ("22-Resonance-A-Note-on-the-Real-Descent.mp3", "A Note on the Real Descent"),
]


def resolve_chapters() -> list[tuple[Path, str]]:
    resolved: list[tuple[Path, str]] = []
    missing: list[str] = []
    for name, title in CHAPTERS:
        path = MASTERS_DIR / name
        if not path.exists():
            missing.append(f"  MISSING: {name} ({title})")
        else:
            resolved.append((path, title))
    if missing:
        print("!! Some chapter masters not found:")
        print("\n".join(missing))
        sys.exit(1)
    return resolved


def probe_duration(path: Path) -> float:
    r = subprocess.run(
        [FFPROBE, "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(r.stdout.strip())


def build_ffmetadata(chapters: list[tuple[Path, str, float]]) -> str:
    lines = [";FFMETADATA1"]

    def tag(k: str, v: str) -> None:
        if v:
            v = (v.replace("\\", "\\\\").replace("=", "\\=")
                 .replace(";", "\\;").replace("#", "\\#")
                 .replace("\n", "\\\n"))
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
    tag("media_type", "2")  # stik=2 = Audiobook
    t_ms = 0
    for _, title, dur in chapters:
        start = t_ms
        end = t_ms + int(round(dur * 1000))
        lines += ["", "[CHAPTER]", "TIMEBASE=1/1000",
                  f"START={start}", f"END={end}", f"title={title}"]
        t_ms = end
    return "\n".join(lines) + "\n"


def archive_existing(path: Path) -> None:
    if path.exists():
        from datetime import datetime, timezone
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        adir = path.parent / "_archive"
        adir.mkdir(parents=True, exist_ok=True)
        dest = adir / f"{path.stem}.{ts}{path.suffix}"
        path.rename(dest)
        print(f"  archived prior M4B → {dest.name}")


def package(chapters: list[tuple[Path, str]], normalize: bool, dry_run: bool,
            bitrate: str = BITRATE) -> int:
    print(f"[RESONANCE] {len(chapters)} chapter(s) · narrator {NARRATOR}:")
    with_dur: list[tuple[Path, str, float]] = []
    total = 0.0
    for path, title in chapters:
        dur = probe_duration(path)
        total += dur
        with_dur.append((path, title, dur))
        print(f"  {path.name:64} {dur/60:5.1f} min  →  {title}")
    h, rem = divmod(int(total), 3600)
    mm, ss = divmod(rem, 60)
    print(f"  TOTAL: {h}h{mm:02d}m{ss:02d}s   cover: "
          f"{COVER.name if COVER.exists() else 'NONE'}")

    if dry_run:
        print("  (dry-run — nothing written)")
        return 0

    WORK_DIR.mkdir(parents=True, exist_ok=True)
    metaf = WORK_DIR / "ffmeta.txt"
    metaf.write_text(build_ffmetadata(with_dur), encoding="utf-8")

    src_files: list[Path] = []
    if normalize:
        print(f"  Normalising to {LUFS_TARGET:g} LUFS mono {bitrate}…")
        for i, (path, title, _) in enumerate(with_dur, 1):
            norm = WORK_DIR / f"norm_{path.stem}.m4a"
            print(f"    [{i}/{len(with_dur)}] {title}", flush=True)
            af = f"loudnorm=I={LUFS_TARGET}:TP=-1.5:LRA=11"
            r = subprocess.run(
                [FFMPEG, "-y", "-i", str(path), "-af", af,
                 "-c:a", "aac", "-b:a", bitrate, "-ac", "1", "-ar", "44100",
                 str(norm)],
                capture_output=True, text=True,
            )
            if r.returncode != 0:
                print(f"  !! normalise failed for {path.name}:\n{r.stderr[-600:]}")
                return 1
            src_files.append(norm)
    else:
        # Transcode each MP3 → AAC first so concat -c copy is safe
        print(f"  Transcoding to AAC mono {bitrate} (no loudnorm)…")
        for i, (path, title, _) in enumerate(with_dur, 1):
            aac = WORK_DIR / f"aac_{path.stem}.m4a"
            print(f"    [{i}/{len(with_dur)}] {title}", flush=True)
            r = subprocess.run(
                [FFMPEG, "-y", "-i", str(path),
                 "-c:a", "aac", "-b:a", bitrate, "-ac", "1", "-ar", "44100",
                 str(aac)],
                capture_output=True, text=True,
            )
            if r.returncode != 0:
                print(f"  !! encode failed for {path.name}:\n{r.stderr[-600:]}")
                return 1
            src_files.append(aac)

    listf = WORK_DIR / "concat.txt"
    listf.write_text("".join(f"file '{p.resolve()}'\n" for p in src_files),
                     encoding="utf-8")
    tmp = WORK_DIR / "nochap.m4a"
    print("  Concatenating…", flush=True)
    subprocess.run(
        [FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(listf),
         "-c", "copy", str(tmp)],
        check=True, capture_output=True,
    )

    archive_existing(OUT_M4B)
    print("  Muxing chapters + cover + metadata…", flush=True)
    cmd = [FFMPEG, "-y", "-i", str(tmp), "-i", str(metaf)]
    map_args = ["-map", "0:a"]
    if COVER.exists():
        cmd += ["-i", str(COVER)]
        map_args += ["-map", "2:v"]
    cmd += ["-map_metadata", "1", "-map_chapters", "1"] + map_args + ["-c", "copy"]
    if COVER.exists():
        cmd += ["-c:v", "mjpeg", "-disposition:v:0", "attached_pic"]
    cmd += ["-movflags", "+faststart", "-f", "mp4", str(OUT_M4B)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"!! ffmpeg mux failed:\n{r.stderr[-2000:]}")
        return 1

    size_mb = OUT_M4B.stat().st_size / 1e6
    print(f"\n  ✓ {OUT_M4B.relative_to(PRESS_DIR)}  ({size_mb:.1f} MB)")

    chk = subprocess.run(
        [FFPROBE, "-v", "error", "-show_chapters", "-of", "json", str(OUT_M4B)],
        capture_output=True, text=True,
    )
    try:
        nch = len(json.loads(chk.stdout).get("chapters", []))
        print(f"  verified: {nch} chapter marker(s) embedded.")
    except Exception:
        pass

    print("\n  AirDrop .m4b to iPhone → Apple Books opens it as an audiobook.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-normalize", action="store_true")
    ap.add_argument("--bitrate", default=BITRATE)
    a = ap.parse_args()
    chapters = resolve_chapters()
    return package(chapters, normalize=not a.no_normalize, dry_run=a.dry_run,
                   bitrate=a.bitrate)


if __name__ == "__main__":
    raise SystemExit(main())
