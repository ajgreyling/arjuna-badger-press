#!/usr/bin/env python3
"""Render Die Laaste Strooi with Emma Lilliana (same stack as Die Vuur in die Donker).

Voice / model / settings copied from books/the-amber-winter/audio/render_emma_afrikaans_masters.py.
Output: site/content/writing/audio/die-laaste-strooi/emma-masters/

Usage (from this directory or anywhere):
    python3 render_die_laaste_strooi_emma.py --dry-run
    python3 render_die_laaste_strooi_emma.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Any

AUDIO_DIR = Path(__file__).resolve().parent
STORY_PATH = AUDIO_DIR.parent / "die-laaste-strooi.md"
OUT_DIR = AUDIO_DIR / "die-laaste-strooi" / "emma-masters"
CHUNKS_DIR = OUT_DIR / "chunks"
MASTERS_DIR = OUT_DIR / "masters"
WORK_DIR = OUT_DIR / "work"
MANIFEST_PATH = OUT_DIR / "manifest.json"
FULL_MASTER = OUT_DIR / "Die Laaste Strooi.mp3"

# Same known-good Afrikaans female voice as Winter sonder Einde / Die Vuur in die Donker
VOICE_SLUG = "emma"
VOICE_NAME = "Emma Lilliana - Soft, Warm and Gentle"
VOICE_ID = "0z8S749Xe6jLCD34QXl1"
MODEL_ID = "eleven_v3"
OUTPUT_FORMAT = "mp3_44100_128"

MAX_CHARS = 3600
DEFAULT_WORKERS = 2
MAX_RETRIES = 6
RETRY_STATUSES = {408, 429, 500, 502, 503, 504}

VOICE_SETTINGS = {
    "stability": 0.35,
    "similarity_boost": 0.75,
    "style": 0.35,
    "use_speaker_boost": True,
    "speed": 0.93,
}


@dataclass(frozen=True)
class Section:
    index: int
    title: str
    slug: str
    render_text: str
    chunks: list[str]


def load_key() -> str:
    for name in ("ELEVENLABS_API_KEY", "XI_API_KEY"):
        value = os.environ.get(name)
        if value:
            return value

    # writing/audio -> writing -> content -> site -> press -> arjuna-badger
    repo_root = AUDIO_DIR.parents[4]
    for rel_path in (
        "arjuna-badger-platform/.env",
        "arjuna-badger-press/.env",
        ".env",
        "arjuna-badger-platform/deploy/.env",
    ):
        env_path = repo_root / rel_path
        if not env_path.exists():
            continue
        for line in env_path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            name, value = stripped.split("=", 1)
            if name.strip() in ("ELEVENLABS_API_KEY", "XI_API_KEY") and value.strip():
                return value.strip().strip('"').strip("'")

    raise RuntimeError("Set ELEVENLABS_API_KEY or XI_API_KEY before rendering.")


def slugify(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", normalized.lower()).strip("-")
    return slug or "section"


def clean_markdown(text: str) -> str:
    cleaned_lines = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line == "---":
            cleaned_lines.append("")
            continue
        if line.startswith("*") and line.endswith("*") and len(line) > 2:
            # Drop italic bylines / epigraphs from TTS
            continue
        line = re.sub(r"^#{1,6}\s+", "", line)
        line = line.replace("**", "").replace("__", "").replace("*", "").replace("_", "")
        cleaned_lines.append(line)

    cleaned = "\n".join(cleaned_lines)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def split_long_text(text: str, max_chars: int) -> list[str]:
    if len(text) <= max_chars:
        return [text]

    sentence_parts = re.split(r"(?<=[.!?])\s+", text)
    chunks: list[str] = []
    current = ""
    for part in sentence_parts:
        if not part:
            continue
        candidate = f"{current} {part}".strip() if current else part
        if len(candidate) <= max_chars:
            current = candidate
            continue
        if current:
            chunks.append(current)
        if len(part) <= max_chars:
            current = part
        else:
            for i in range(0, len(part), max_chars):
                piece = part[i : i + max_chars].strip()
                if piece:
                    chunks.append(piece)
            current = ""
    if current:
        chunks.append(current)
    return chunks or [text[:max_chars]]


def chunk_text(text: str) -> list[str]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks: list[str] = []
    current = ""
    for paragraph in paragraphs:
        candidate = f"{current}\n\n{paragraph}".strip() if current else paragraph
        if len(candidate) <= MAX_CHARS:
            current = candidate
            continue
        if current:
            chunks.extend(split_long_text(current, MAX_CHARS))
        if len(paragraph) <= MAX_CHARS:
            current = paragraph
        else:
            chunks.extend(split_long_text(paragraph, MAX_CHARS))
            current = ""
    if current:
        chunks.extend(split_long_text(current, MAX_CHARS))
    return chunks


def parse_story(path: Path) -> list[Section]:
    raw = path.read_text(encoding="utf-8")
    # Split on ## chapter headers; drop the H1 title block before the first ##
    parts = re.split(r"(?m)^(## .+)$", raw)
    # parts: [preamble, '## I. ...', body, '## II. ...', body, ...]
    sections: list[Section] = []
    i = 1
    index = 0
    while i < len(parts):
        heading = parts[i].strip()
        body = parts[i + 1] if i + 1 < len(parts) else ""
        title = re.sub(r"^##\s+", "", heading).strip()
        render_text = clean_markdown(f"{title}\n\n{body}")
        if not render_text:
            i += 2
            continue
        slug = f"{index:02d}-{slugify(title)}"
        sections.append(
            Section(
                index=index,
                title=title,
                slug=slug,
                render_text=render_text,
                chunks=chunk_text(render_text),
            )
        )
        index += 1
        i += 2
    if not sections:
        raise RuntimeError(f"No ## sections found in {path}")
    return sections


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def request_audio(text: str, key: str) -> bytes:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}?output_format={OUTPUT_FORMAT}"
    payload = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": VOICE_SETTINGS,
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={"xi-api-key": key, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=240) as response:
        return response.read()


def render_chunk(section: Section, chunk_index: int, text: str, key: str) -> dict[str, Any]:
    chunk_dir = CHUNKS_DIR / section.slug
    chunk_dir.mkdir(parents=True, exist_ok=True)
    output_path = chunk_dir / f"chunk-{chunk_index + 1:03d}.mp3"
    text_path = chunk_dir / f"chunk-{chunk_index + 1:03d}.txt"
    hash_path = chunk_dir / f"chunk-{chunk_index + 1:03d}.sha256"
    expected_hash = text_hash(text)
    had_previous = output_path.exists() and output_path.stat().st_size > 0

    if had_previous:
        actual = hash_path.read_text(encoding="utf-8").strip() if hash_path.exists() else ""
        if actual == expected_hash:
            print(f"Reusing {section.slug} chunk {chunk_index + 1}", flush=True)
            return {
                "index": chunk_index,
                "file": str(output_path),
                "sha256": expected_hash,
                "chars": len(text),
                "status": "reused",
            }

    last_error = ""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            action = "Regenerating" if had_previous else "Rendering"
            print(f"{action} {section.slug} chunk {chunk_index + 1}", flush=True)
            audio = request_audio(text, key)
            tmp = output_path.with_suffix(".mp3.part")
            tmp.write_bytes(audio)
            tmp.replace(output_path)
            text_path.write_text(text, encoding="utf-8")
            hash_path.write_text(expected_hash + "\n", encoding="utf-8")
            return {
                "index": chunk_index,
                "file": str(output_path),
                "sha256": expected_hash,
                "chars": len(text),
                "status": "regenerated" if had_previous else "rendered",
                "attempts": attempt,
            }
        except urllib.error.HTTPError as error:
            response_body = error.read().decode("utf-8", "replace")
            last_error = f"HTTP {error.code}: {response_body[:500]}"
            if error.code not in RETRY_STATUSES or attempt == MAX_RETRIES:
                break
            retry_after = error.headers.get("Retry-After")
            delay = float(retry_after) if retry_after and retry_after.isdigit() else min(90, 2**attempt)
        except (urllib.error.URLError, TimeoutError) as error:
            last_error = repr(error)
            if attempt == MAX_RETRIES:
                break
            delay = min(90, 2**attempt)
        print(f"Retrying {section.slug} chunk {chunk_index + 1}", flush=True)
        time.sleep(delay)

    return {
        "index": chunk_index,
        "file": str(output_path),
        "chars": len(text),
        "status": "failed",
        "error": last_error,
    }


def run_ffmpeg(command: list[str]) -> None:
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)


def make_silence(path: Path, seconds: float) -> None:
    if path.exists() and path.stat().st_size > 0:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    run_ffmpeg(
        [
            "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
            "-t", str(seconds), "-codec:a", "libmp3lame", "-b:a", "128k",
            "-ar", "44100", "-ac", "1", str(path),
        ]
    )


def write_concat_list(paths: list[Path], list_path: Path, silence_path: Path | None = None) -> None:
    list_path.parent.mkdir(parents=True, exist_ok=True)
    with list_path.open("w", encoding="utf-8") as handle:
        for index, path in enumerate(paths):
            handle.write(f"file '{path.resolve()}'\n")
            if silence_path is not None and index != len(paths) - 1:
                handle.write(f"file '{silence_path.resolve()}'\n")


def master_audio(inputs: list[Path], output_path: Path, list_path: Path, silence_path: Path | None) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_concat_list(inputs, list_path, silence_path)
    run_ffmpeg(
        [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_path),
            "-af", "loudnorm=I=-20:TP=-3:LRA=11",
            "-codec:a", "libmp3lame", "-b:a", "128k", "-ar", "44100", "-ac", "1",
            str(output_path),
        ]
    )


def probe_audio(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    result: dict[str, Any] = {"bytes": path.stat().st_size}
    if shutil.which("ffprobe") is None:
        return result
    completed = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(path),
        ],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    try:
        result["duration_seconds"] = round(float(completed.stdout.strip()), 3)
    except ValueError:
        pass
    return result


def print_plan(sections: list[Section]) -> None:
    total_chars = sum(len(s.render_text) for s in sections)
    total_chunks = sum(len(s.chunks) for s in sections)
    print(f"Story: {STORY_PATH}", flush=True)
    print(f"Voice: {VOICE_NAME} ({VOICE_ID})", flush=True)
    print(f"Model: {MODEL_ID}", flush=True)
    print(f"Sections: {len(sections)}", flush=True)
    print(f"Render characters: {total_chars}", flush=True)
    print(f"Chunks: {total_chunks}", flush=True)
    for section in sections:
        print(
            f"{section.index:02d} {section.title}: {len(section.render_text)} chars, {len(section.chunks)} chunks",
            flush=True,
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    args = parser.parse_args()

    if not STORY_PATH.is_file():
        print(f"Missing story: {STORY_PATH}", file=sys.stderr)
        return 1

    sections = parse_story(STORY_PATH)
    print_plan(sections)

    manifest: dict[str, Any] = {
        "voice": {"slug": VOICE_SLUG, "name": VOICE_NAME, "voice_id": VOICE_ID},
        "model_id": MODEL_ID,
        "story_path": str(STORY_PATH),
        "output_dir": str(OUT_DIR),
        "chapters": [
            {
                "index": s.index,
                "title": s.title,
                "slug": s.slug,
                "render_chars": len(s.render_text),
                "chunks": [
                    {
                        "index": i,
                        "chars": len(c),
                        "sha256": text_hash(c),
                        "file": str(CHUNKS_DIR / s.slug / f"chunk-{i + 1:03d}.mp3"),
                    }
                    for i, c in enumerate(s.chunks)
                ],
                "mastered_file": str(MASTERS_DIR / f"{s.slug}.mp3"),
            }
            for s in sections
        ],
        "full_mastered_file": str(FULL_MASTER),
        "failures": [],
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if args.dry_run:
        print(f"Dry-run manifest: {MANIFEST_PATH}", flush=True)
        return 0

    key = load_key()
    workers = max(1, min(args.workers, 4))
    results: dict[tuple[int, int], dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = []
        for section in sections:
            for chunk_index, chunk in enumerate(section.chunks):
                futures.append(
                    (
                        section.index,
                        chunk_index,
                        executor.submit(render_chunk, section, chunk_index, chunk, key),
                    )
                )
        for section_index, chunk_index, future in futures:
            results[(section_index, chunk_index)] = future.result()

    failures = []
    for section, chapter in zip(sections, manifest["chapters"], strict=True):
        for chunk in chapter["chunks"]:
            result = results.get((section.index, chunk["index"]), {})
            chunk.update(result)
            if chunk.get("status") == "failed":
                failures.append(
                    {
                        "chapter": section.title,
                        "chunk_index": chunk["index"],
                        "error": chunk.get("error", "unknown"),
                    }
                )
        chapter["failed"] = any(c.get("status") == "failed" for c in chapter["chunks"])
    manifest["failures"] = failures
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if failures:
        print(f"Rendering failed ({len(failures)}). Manifest: {MANIFEST_PATH}", flush=True)
        return 2

    if shutil.which("ffmpeg") is None:
        print("ffmpeg required for mastering", file=sys.stderr)
        return 1

    chunk_silence = WORK_DIR / "silence-0.35s.mp3"
    chapter_silence = WORK_DIR / "silence-1.5s.mp3"
    make_silence(chunk_silence, 0.35)
    make_silence(chapter_silence, 1.5)

    chapter_paths: list[Path] = []
    for chapter in manifest["chapters"]:
        chunk_paths = [Path(c["file"]) for c in chapter["chunks"]]
        master_path = Path(chapter["mastered_file"])
        master_audio(
            chunk_paths,
            master_path,
            WORK_DIR / f"{chapter['slug']}-concat.txt",
            chunk_silence if len(chunk_paths) > 1 else None,
        )
        chapter["mastered_probe"] = probe_audio(master_path)
        chapter_paths.append(master_path)

    master_audio(chapter_paths, FULL_MASTER, WORK_DIR / "full-concat.txt", chapter_silence)
    manifest["full_mastered_probe"] = probe_audio(FULL_MASTER)
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    dur = manifest["full_mastered_probe"].get("duration_seconds")
    print(f"Done: {FULL_MASTER}", flush=True)
    if dur:
        print(f"Duration: {dur / 60:.1f} min ({dur:.0f}s)", flush=True)
    print(f"Manifest: {MANIFEST_PATH}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
