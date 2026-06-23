#!/usr/bin/env python3
"""Package Die Vuur in die Donker master MP3s into an M4B audiobook.

Reads the per-chapter masters produced by render_emma_afrikaans_masters.py and
packages them into a single .m4b file with:
  - embedded chapter markers (tappable chapter list in Apple Books / VLC)
  - cover art (design/cover.png)
  - full audiobook metadata (title, author, series, copyright, genre)
  - EBU R128 loudness normalisation to −19 LUFS (consistent volume)
  - ACX/INaudio-spec per-chapter MP3 export (--acx flag)

Output:
  audio/emma-afrikaans-masters/Die Vuur in die Donker.m4b
  audio/emma-afrikaans-masters/_acx/  (with --acx)

Usage:
    python3 audio/make_m4b.py
    python3 audio/make_m4b.py --no-normalize   # lossless stream-copy, may have volume drift
    python3 audio/make_m4b.py --acx            # export ACX/INaudio per-chapter MP3s instead
    python3 audio/make_m4b.py --dry-run        # show plan, write nothing
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

AUDIO_DIR = Path(__file__).resolve().parent
BOOK_DIR = AUDIO_DIR.parent
PRESS_DIR = BOOK_DIR.parents[1]
MASTERS_DIR = AUDIO_DIR / "emma-afrikaans-masters" / "masters"
COVER = BOOK_DIR / "design" / "cover.png"
OUT_DIR = AUDIO_DIR / "emma-afrikaans-masters"
OUT_M4B = OUT_DIR / "Die Vuur in die Donker.m4b"
WORK_DIR = OUT_DIR / "_work_m4b"

FFMPEG = "/opt/homebrew/bin/ffmpeg"
FFPROBE = "/opt/homebrew/bin/ffprobe"

TITLE = "Die Vuur in die Donker"
SERIES = "Winter sonder Einde"
AUTHOR = "Andries J. Greyling"
NARRATOR = "Emma Lilliana"
YEAR = "2026"
COPYRIGHT = f"© {YEAR} Andries J. Greyling / Arjuna Badger Press"
COMMENT = (
    "'n Volwasse historiese Viking-saga in Afrikaans. "
    "Inhoudswaarskuwing: eksplisiete volwasse inhoud, geskik vir 18+."
)
GENRE = "Audiobook"
PUBLISHER = "Arjuna Badger Press"

LUFS_TARGET = -19.0
BITRATE = "64k"

# ACX/INaudio spec
ACX_RMS_TARGET = -20.0
ACX_PEAK_CEIL = -3.5
ACX_HEAD_S = 0.75
ACX_TAIL_S = 2.5

# Ordered chapter list: (filename_stem, display_title)
# These stems match what render_emma_afrikaans_masters.py generates after the
# frontmatter track was added (sections re-numbered; index 00 = kopiereg).
# After a full re-render the new stems will exist; for the initial run the
# packager also accepts the OLD stems (pre-frontmatter) as fallback so the
# M4B can be built while the re-render is queued.
CHAPTERS: list[tuple[str, str]] = [
    ("00-kopiereg",                                   "Kopiereg"),
    ("01-opdrag",                                     "Opdrag"),
    ("02-proloog-die-winternagte",                    "Proloog — Die Winternagte"),
    ("03-hoofstuk-een-die-gaste",                     "Hoofstuk 1 — Die Gaste"),
    ("04-hoofstuk-twee-die-toemaak-van-die-wereld",   "Hoofstuk 2 — Die Toemaak van die Wêreld"),
    ("05-hoofstuk-drie-die-joelfees",                 "Hoofstuk 3 — Die Joelfees"),
    ("06-hoofstuk-vier-die-more-daarna",              "Hoofstuk 4 — Die Môre Daarna"),
    ("07-hoofstuk-vyf-solveig",                       "Hoofstuk 5 — Solveig"),
    ("08-hoofstuk-ses-heir-op-die-hoe-stoel",         "Hoofstuk 6 — Heiðr op die Hoë Stoel"),
    ("09-hoofstuk-sewe-die-sien",                     "Hoofstuk 7 — Die Sien"),
    ("10-hoofstuk-agt-die-twee-vure",                 "Hoofstuk 8 — Die Twee Vure"),
    ("11-hoofstuk-nege-die-harde-week",               "Hoofstuk 9 — Die Harde Week"),
    ("12-hoofstuk-tien-die-redding-oor-die-ys",       "Hoofstuk 10 — Die Redding oor die Ys"),
    ("13-hoofstuk-elf-die-prys",                      "Hoofstuk 11 — Die Prys"),
    ("14-hoofstuk-twaalf-die-dooi",                   "Hoofstuk 12 — Die Dooi"),
    ("15-hoofstuk-dertien-die-strand",                "Hoofstuk 13 — Die Strand"),
    ("16-hoofstuk-99-nawoord-feit-en-verbeelding",    "Nawoord — Feit en Verbeelding"),
]

# Fallback stems for pre-frontmatter masters (old numbering, used if the new
# stems don't exist yet — allows packaging while re-render is in progress).
_FALLBACK: dict[str, str] = {
    "01-opdrag":                                   "00-opdrag",
    "02-proloog-die-winternagte":                  "01-proloog-die-winternagte",
    "03-hoofstuk-een-die-gaste":                   "02-hoofstuk-een-die-gaste",
    "04-hoofstuk-twee-die-toemaak-van-die-wereld": "03-hoofstuk-twee-die-toemaak-van-die-wereld",
    "05-hoofstuk-drie-die-joelfees":               "04-hoofstuk-drie-die-joelfees",
    "06-hoofstuk-vier-die-more-daarna":            "05-hoofstuk-vier-die-more-daarna",
    "07-hoofstuk-vyf-solveig":                     "06-hoofstuk-vyf-solveig",
    "08-hoofstuk-ses-heir-op-die-hoe-stoel":       "07-hoofstuk-ses-heir-op-die-hoe-stoel",
    "09-hoofstuk-sewe-die-sien":                   "08-hoofstuk-sewe-die-sien",
    "10-hoofstuk-agt-die-twee-vure":               "09-hoofstuk-agt-die-twee-vure",
    "11-hoofstuk-nege-die-harde-week":             "10-hoofstuk-nege-die-harde-week",
    "12-hoofstuk-tien-die-redding-oor-die-ys":     "11-hoofstuk-tien-die-redding-oor-die-ys",
    "13-hoofstuk-elf-die-prys":                    "12-hoofstuk-elf-die-prys",
    "14-hoofstuk-twaalf-die-dooi":                 "13-hoofstuk-twaalf-die-dooi",
    "15-hoofstuk-dertien-die-strand":              "14-hoofstuk-dertien-die-strand",
    "16-hoofstuk-99-nawoord-feit-en-verbeelding":  "15-hoofstuk-99-nawoord-feit-en-verbeelding",
}


def find_master(stem: str) -> Path | None:
    """Find master by exact stem, then try fallback old stem."""
    exact = MASTERS_DIR / f"{stem}.mp3"
    if exact.exists():
        return exact
    # try the pre-frontmatter fallback numbering
    fallback_stem = _FALLBACK.get(stem)
    if fallback_stem:
        fb = MASTERS_DIR / f"{fallback_stem}.mp3"
        if fb.exists():
            return fb
    return None


def resolve_chapters() -> list[tuple[Path, str]]:
    resolved: list[tuple[Path, str]] = []
    missing: list[str] = []
    fallback_used: list[str] = []
    for stem, title in CHAPTERS:
        path = find_master(stem)
        if path is None:
            missing.append(f"  MISSING: {stem} ({title})")
        else:
            if path.stem != stem:
                fallback_used.append(f"  fallback: {stem} → {path.stem}")
            resolved.append((path, title))
    if fallback_used:
        print("[make_m4b] using pre-frontmatter fallback stems for some chapters:")
        print("\n".join(fallback_used))
    if missing:
        print("!! Some chapter masters not found — render first:")
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
            v = v.replace("\\", "\\\\").replace("=", "\\=").replace(";", "\\;") \
                  .replace("#", "\\#").replace("\n", "\\\n")
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
    tag("media_type", "2")      # stik=2 = Audiobook (Apple Books/iTunes)
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
    print(f"[Die Vuur in die Donker] {len(chapters)} chapter(s):")
    with_dur: list[tuple[Path, str, float]] = []
    total = 0.0
    for path, title in chapters:
        dur = probe_duration(path)
        total += dur
        with_dur.append((path, title, dur))
        print(f"  {path.stem:48} {dur/60:5.1f} min  →  {title}")
    h, rem = divmod(int(total), 3600)
    mm, ss = divmod(rem, 60)
    print(f"  TOTAL: {h}h{mm:02d}m{ss:02d}s   cover: {COVER.name if COVER.exists() else 'NONE'}")

    if dry_run:
        print("  (dry-run — nothing written)")
        return 0

    WORK_DIR.mkdir(parents=True, exist_ok=True)
    metaf = WORK_DIR / "ffmeta.txt"
    metaf.write_text(build_ffmetadata(with_dur), encoding="utf-8")

    # 1. Per-chapter loudness normalise → work AAC files
    src_files: list[Path] = []
    if normalize:
        print(f"  Normalising to {LUFS_TARGET:g} LUFS mono {BITRATE}…")
        for path, title, _ in with_dur:
            norm = WORK_DIR / f"norm_{path.stem}.m4a"
            af = f"loudnorm=I={LUFS_TARGET}:TP=-1.5:LRA=11"
            r = subprocess.run(
                [FFMPEG, "-y", "-i", str(path), "-af", af,
                 "-c:a", "aac", "-b:a", bitrate, "-ac", "1", "-ar", "44100", str(norm)],
                capture_output=True, text=True,
            )
            if r.returncode != 0:
                print(f"  !! normalise failed for {path.stem}:\n{r.stderr[-600:]}")
                return 1
            src_files.append(norm)
    else:
        src_files = [p for p, _, _ in with_dur]

    # 2. Concat all chapters
    listf = WORK_DIR / "concat.txt"
    listf.write_text("".join(f"file '{p.resolve()}'\n" for p in src_files), encoding="utf-8")
    tmp = WORK_DIR / "nochap.m4a"
    subprocess.run(
        [FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(listf), "-c", "copy", str(tmp)],
        check=True, capture_output=True,
    )

    # 3. Mux: chapters + cover + metadata
    archive_existing(OUT_M4B)
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

    # Verify embedded chapters
    chk = subprocess.run(
        [FFPROBE, "-v", "error", "-show_chapters", "-of", "json", str(OUT_M4B)],
        capture_output=True, text=True,
    )
    try:
        nch = len(json.loads(chk.stdout).get("chapters", []))
        print(f"  verified: {nch} chapter marker(s) embedded.")
    except Exception:
        pass

    print(f"\n  AirDrop .m4b to iPhone → Apple Books opens it as an audiobook.")
    print(f"  Or: File → Import into Apple Books on Mac.")
    return 0


def measure_mp3(path: Path) -> dict[str, float]:
    r = subprocess.run(
        [FFMPEG, "-i", str(path), "-af", "astats=metadata=1:measure_overall=1",
         "-f", "null", "-"],
        capture_output=True, text=True,
    )
    out: dict[str, float] = {}
    for line in r.stderr.splitlines():
        if "RMS level dB:" in line:
            try:
                out["rms"] = float(line.split(":")[-1])
            except ValueError:
                pass
        elif "Peak level dB" in line and "peak" not in out:
            try:
                out["peak"] = float(line.split(":")[-1])
            except ValueError:
                pass
        elif "Noise floor dB" in line:
            try:
                out["noise"] = float(line.split(":")[-1])
            except ValueError:
                pass
    return out


def export_acx(chapters: list[tuple[Path, str]], dry_run: bool) -> int:
    acx_dir = OUT_DIR / "_acx"
    print(f"[ACX/INaudio export] {len(chapters)} chapter(s) → {acx_dir.relative_to(PRESS_DIR)}/")
    print(f"  spec: MP3 192 CBR · mono · 44.1 kHz · RMS −23..−18 · peak ≤ −3 dBFS")
    if dry_run:
        for i, (p, title) in enumerate(chapters, 1):
            print(f"  {i:02d}. {title} → {i:02d}_{p.stem}.mp3")
        return 0

    acx_dir.mkdir(parents=True, exist_ok=True)
    all_ok = True
    for idx, (src, title) in enumerate(chapters, 1):
        meas = measure_mp3(src)
        rms = meas.get("rms", ACX_RMS_TARGET)
        gain = ACX_RMS_TARGET - rms
        dst = acx_dir / f"{idx:02d}_{src.stem}.mp3"
        af = (
            f"volume={gain:.2f}dB,"
            f"alimiter=limit={ACX_PEAK_CEIL}dB:level=disabled,"
            f"aformat=channel_layouts=mono:sample_rates=44100,"
            f"adelay={int(ACX_HEAD_S * 1000)},"
            f"apad=pad_dur={ACX_TAIL_S}"
        )
        cmd = [
            FFMPEG, "-y", "-i", str(src), "-af", af,
            "-c:a", "libmp3lame", "-b:a", "192k", "-minrate", "192k", "-maxrate", "192k",
            "-ac", "1", "-ar", "44100",
            "-metadata", f"title={title}",
            "-metadata", f"album={TITLE}",
            "-metadata", f"artist={AUTHOR}",
            "-metadata", f"copyright={COPYRIGHT}",
            "-metadata", "genre=Audiobook",
            str(dst),
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"  !! {src.stem} export failed:\n{r.stderr[-800:]}")
            all_ok = False
            continue

        meas2 = measure_mp3(dst)
        rms2 = meas2.get("rms", 0.0)
        peak2 = meas2.get("peak", 0.0)
        noise2 = meas2.get("noise", -99.0)
        ok_rms = -23.0 <= rms2 <= -18.0
        ok_peak = peak2 <= -3.0
        ok_noise = noise2 <= -60.0
        ok = ok_rms and ok_peak and ok_noise
        all_ok = all_ok and ok
        fails = []
        if not ok_rms:
            fails.append(f"rms={rms2:.1f}")
        if not ok_peak:
            fails.append(f"peak={peak2:.1f}")
        if not ok_noise:
            fails.append(f"noise={noise2:.1f}")
        flag = "✓" if ok else "✗ " + " ".join(fails)
        print(f"  {idx:02d}. {dst.name:48} RMS {rms2:6.1f} peak {peak2:5.1f}  {flag}")

    print()
    if all_ok:
        print("  ALL FILES PASS ACX SPEC ✓")
    else:
        print("  !! some files FAILED — see flags above")
    print("  Upload to Voices by INaudio (formerly Findaway) or Spotify.")
    print("  Tick the 'AI / Synthesized Voice' disclosure box.")
    return 0 if all_ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="show plan; write nothing")
    ap.add_argument("--no-normalize", action="store_true",
                    help="skip loudness normalisation; lossless stream-copy (may have volume drift)")
    ap.add_argument("--acx", action="store_true",
                    help="export ACX/INaudio per-chapter MP3s instead of M4B")
    ap.add_argument("--bitrate", default=BITRATE,
                    help=f"AAC bitrate for M4B normalisation (default {BITRATE})")
    a = ap.parse_args()
    bitrate = a.bitrate
    chapters = resolve_chapters()

    if a.acx:
        return export_acx(chapters, a.dry_run)
    return package(chapters, normalize=not a.no_normalize, dry_run=a.dry_run,
                   bitrate=bitrate)


if __name__ == "__main__":
    raise SystemExit(main())
