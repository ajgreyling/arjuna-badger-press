#!/usr/bin/env python3
"""Pad Resonance chapter MP3s with ACX/VoiceCrafters room-tone silence.

VoiceCrafters / Findaway require 1–5 seconds of silence at the start AND end
of every track. This script:

  1. Archives untouched masters to steven-g/_raw/
  2. Rewrites each numbered chapter MP3 with 1.5s head + 2.5s tail silence
  3. Builds RESONANCE-sample-4m55s.mp3 from a mid-book chapter excerpt

Usage:
    python3 audio/pad_silence.py
    python3 audio/pad_silence.py --dry-run
    python3 audio/pad_silence.py --verify-only
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

AUDIO_DIR = Path(__file__).resolve().parent
MASTERS = AUDIO_DIR / "steven-g"
RAW_DIR = MASTERS / "_raw"
WORK_DIR = MASTERS / "_work_pad"

FFMPEG = "/opt/homebrew/bin/ffmpeg"
FFPROBE = "/opt/homebrew/bin/ffprobe"

HEAD_S = 1.5
TAIL_S = 2.5
# Silence threshold for verification (VoiceCrafters-style)
NOISE_DB = "-50dB"
MIN_SILENCE_S = 1.0
MAX_SILENCE_S = 5.0

# Mid-book chapter used for the retail sample (strong narrative stretch)
SAMPLE_SRC_NAME = "04-Resonance-The-Thing-That-Should-Not-Exist.mp3"
SAMPLE_OUT_NAME = "RESONANCE-sample-4m55s.mp3"
SAMPLE_START_S = 60.0          # skip cold open
SAMPLE_BODY_S = 4 * 60 + 55    # 4m55s of speech, then pads added


def chapter_mp3s() -> list[Path]:
    files = sorted(MASTERS.glob("[0-9][0-9]-Resonance-*.mp3"))
    return files


def probe(path: Path) -> dict:
    r = subprocess.run(
        [FFPROBE, "-v", "error", "-select_streams", "a:0",
         "-show_entries", "stream=sample_rate,channels,bit_rate:format=duration",
         "-of", "json", str(path)],
        check=True, capture_output=True, text=True,
    )
    import json
    data = json.loads(r.stdout)
    stream = data["streams"][0]
    return {
        "duration": float(data["format"]["duration"]),
        "rate": int(stream.get("sample_rate") or 44100),
        "channels": int(stream.get("channels") or 1),
        "bitrate": int(stream.get("bit_rate") or 192000),
    }


def detect_edge_silence(path: Path) -> tuple[float, float]:
    """Return (leading_silence_s, trailing_silence_s) via silencedetect."""
    r = subprocess.run(
        [FFMPEG, "-i", str(path),
         "-af", f"silencedetect=noise={NOISE_DB}:d=0.3",
         "-f", "null", "-"],
        capture_output=True, text=True,
    )
    dur = probe(path)["duration"]
    starts: list[float] = []
    ends: list[float] = []
    for line in r.stderr.splitlines():
        if "silence_start:" in line:
            try:
                starts.append(float(line.split("silence_start:")[1].split("|")[0].split()[0]))
            except ValueError:
                pass
        if "silence_end:" in line:
            try:
                # "silence_end: 1.5 | silence_duration: 1.5"
                part = line.split("silence_end:")[1]
                ends.append(float(part.split("|")[0].split()[0]))
            except ValueError:
                pass
        if "silence_duration:" in line and "silence_end" not in line:
            pass

    lead = 0.0
    if starts and starts[0] <= 0.05:
        # leading silence ends at first silence_end after start
        for e in ends:
            if e > 0:
                lead = e
                break

    # trailing: last silence that reaches (or nearly) EOF
    trail = 0.0
    # parse durations paired with starts near the end
    pairs: list[tuple[float, float]] = []
    cur_start = None
    for line in r.stderr.splitlines():
        if "silence_start:" in line:
            try:
                cur_start = float(line.split("silence_start:")[1].split("|")[0].split()[0])
            except ValueError:
                cur_start = None
        if "silence_end:" in line and cur_start is not None:
            try:
                part = line.split("silence_end:")[1]
                end = float(part.split("|")[0].split()[0])
                dur_s = None
                if "silence_duration:" in line:
                    dur_s = float(line.split("silence_duration:")[1].split()[0])
                pairs.append((cur_start, end if dur_s is None else cur_start + dur_s))
            except ValueError:
                pass
            cur_start = None
        # silence that runs to EOF may only have silence_start
        if "silence_start:" in line:
            try:
                s = float(line.split("silence_start:")[1].split("|")[0].split()[0])
                if s < dur and (dur - s) >= 0.3 and s > dur * 0.5:
                    # candidate trailing if no end yet
                    pass
            except ValueError:
                pass

    # Prefer: silence_start near end with no end, or end ≈ duration
    trailing_starts = []
    for line in r.stderr.splitlines():
        m = re.search(r"silence_start:\s*([0-9.]+)", line)
        if m:
            trailing_starts.append(float(m.group(1)))
    for s in reversed(trailing_starts):
        if s < dur and (dur - s) >= 0.25:
            # if there's a silence_end after this start before EOF, use duration to end;
            # else treat as running to EOF
            ended = False
            for line in r.stderr.splitlines():
                if "silence_end:" in line:
                    try:
                        e = float(line.split("silence_end:")[1].split("|")[0].split()[0])
                        if e > s:
                            # check if this end is for this start (approx)
                            if e <= dur + 0.05:
                                trail = e - s if abs(e - dur) > 0.15 else dur - s
                                # if silence ends well before EOF, not trailing
                                if abs(e - dur) > 0.15:
                                    trail = 0.0
                                else:
                                    trail = dur - s
                                ended = True
                                break
                    except ValueError:
                        pass
            if not ended:
                trail = dur - s
            if trail > 0:
                break

    # simpler reliable method: check first/last N seconds RMS via astats
    return lead, trail


def edge_silence_rms(path: Path, head_s: float = 1.0, tail_s: float = 1.0) -> tuple[float, float, float]:
    """Measure mean volume (dB) in head window, tail window, and full file duration."""
    info = probe(path)
    dur = info["duration"]

    def window_rms(start: float, length: float) -> float:
        r = subprocess.run(
            [FFMPEG, "-ss", f"{start:.3f}", "-t", f"{length:.3f}", "-i", str(path),
             "-af", "astats=metadata=1:reset=1", "-f", "null", "-"],
            capture_output=True, text=True,
        )
        rms = 0.0
        for line in r.stderr.splitlines():
            if "RMS level dB" in line:
                try:
                    rms = float(line.split(":")[-1].strip())
                except ValueError:
                    pass
        return rms

    head_rms = window_rms(0.0, min(head_s, dur))
    tail_start = max(0.0, dur - tail_s)
    tail_rms = window_rms(tail_start, min(tail_s, dur))
    return head_rms, tail_rms, dur


def pad_file(src: Path, dst: Path) -> None:
    """Write dst = 1.5s silence + src audio + 2.5s silence, MP3 192k CBR mono 44.1kHz."""
    info = probe(src)
    channels = info["channels"]
    # adelay wants one delay per channel
    delays = "|".join([str(int(HEAD_S * 1000))] * max(1, channels))
    af = (
        f"adelay={delays}:all=1,"
        f"apad=pad_dur={TAIL_S},"
        f"aformat=channel_layouts=mono:sample_rates=44100"
    )
    cmd = [
        FFMPEG, "-y", "-i", str(src),
        "-af", af,
        "-c:a", "libmp3lame", "-b:a", "192k",
        "-minrate", "192k", "-maxrate", "192k",
        "-ac", "1", "-ar", "44100",
        str(dst),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"pad failed for {src.name}:\n{r.stderr[-800:]}")


def make_sample(src: Path, dst: Path) -> None:
    """4m55s body from src, with head/tail silence pads."""
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    body = WORK_DIR / "sample_body.mp3"
    r = subprocess.run(
        [FFMPEG, "-y", "-ss", str(SAMPLE_START_S), "-t", str(SAMPLE_BODY_S),
         "-i", str(src), "-c:a", "libmp3lame", "-b:a", "192k",
         "-ac", "1", "-ar", "44100", str(body)],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        raise RuntimeError(f"sample extract failed:\n{r.stderr[-800:]}")
    pad_file(body, dst)


def verify(path: Path) -> tuple[bool, str]:
    head_rms, tail_rms, dur = edge_silence_rms(path, HEAD_S, TAIL_S)
    # Treat < -40 dB as silence for the pad windows
    ok_head = head_rms <= -40.0
    ok_tail = tail_rms <= -40.0
    status = "OK" if (ok_head and ok_tail) else "FAIL"
    detail = (f"{status}  head_rms={head_rms:6.1f} dB  "
              f"tail_rms={tail_rms:6.1f} dB  dur={dur/60:5.1f}m")
    return ok_head and ok_tail, detail


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--verify-only", action="store_true")
    a = ap.parse_args()

    chapters = chapter_mp3s()
    if not chapters:
        print("!! no numbered chapter MP3s in", MASTERS)
        return 1

    print(f"[pad_silence] {len(chapters)} chapter(s)  "
          f"head={HEAD_S}s  tail={TAIL_S}s  (VoiceCrafters 1–5s)")

    if a.verify_only:
        bad = 0
        for p in chapters + ([MASTERS / SAMPLE_OUT_NAME]
                             if (MASTERS / SAMPLE_OUT_NAME).exists() else []):
            ok, detail = verify(p)
            print(f"  {p.name:64} {detail}")
            if not ok:
                bad += 1
        return 1 if bad else 0

    if a.dry_run:
        for p in chapters:
            print(f"  would pad  {p.name}")
        print(f"  would build sample from {SAMPLE_SRC_NAME}")
        return 0

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    WORK_DIR.mkdir(parents=True, exist_ok=True)

    # Archive originals once (skip if already archived for this name)
    for src in chapters:
        raw = RAW_DIR / src.name
        if not raw.exists():
            shutil.copy2(src, raw)
            print(f"  archived → _raw/{src.name}")

    # Pad from raw (idempotent re-runs)
    bad = 0
    for i, src in enumerate(chapters, 1):
        raw = RAW_DIR / src.name
        tmp = WORK_DIR / src.name
        print(f"  [{i}/{len(chapters)}] padding {src.name}", flush=True)
        pad_file(raw, tmp)
        shutil.move(str(tmp), str(src))
        ok, detail = verify(src)
        print(f"           {detail}")
        if not ok:
            bad += 1

    # Sample track
    sample_src = RAW_DIR / SAMPLE_SRC_NAME
    if not sample_src.exists():
        sample_src = MASTERS / SAMPLE_SRC_NAME
    sample_dst = MASTERS / SAMPLE_OUT_NAME
    print(f"  building sample {SAMPLE_OUT_NAME} from {sample_src.name}", flush=True)
    make_sample(sample_src, sample_dst)
    ok, detail = verify(sample_dst)
    print(f"           {detail}")
    if not ok:
        bad += 1

    print()
    if bad:
        print(f"!! {bad} file(s) failed silence verify")
        return 1
    print(f"✓ padded {len(chapters)} chapters + sample → {MASTERS.relative_to(AUDIO_DIR.parent)}")
    print("  Re-run: python3 audio/make_m4b.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
