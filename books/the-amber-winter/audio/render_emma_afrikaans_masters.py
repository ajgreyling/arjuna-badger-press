#!/usr/bin/env python3
"""Render and master the Afrikaans audiobook with the selected Emma voice."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import time
import unicodedata
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any


AUDIO_DIR = Path(__file__).resolve().parent
BOOK_PATH = AUDIO_DIR.parent / "build" / "BOOK.md"
FRONTMATTER_PATH = AUDIO_DIR / "afrikaans-kopiereg-voorblad.md"
BACKMATTER_PATH = AUDIO_DIR / "afrikaans-faktuele-nawoord.md"
OUT_DIR = AUDIO_DIR / "emma-afrikaans-masters"
CHUNKS_DIR = OUT_DIR / "chunks"
MASTERS_DIR = OUT_DIR / "masters"
WORK_DIR = OUT_DIR / "work"
MANIFEST_PATH = OUT_DIR / "manifest.json"

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
    source_path: Path
    source_kind: str
    source_text: str
    render_text: str
    chunks: list[str]


def load_key() -> str:
    for name in ("ELEVENLABS_API_KEY", "XI_API_KEY"):
        value = os.environ.get(name)
        if value:
            return value

    repo_root = AUDIO_DIR.parents[3]
    for rel_path in (
        "arjuna-badger-platform/.env",
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
                return value.strip().strip("\"").strip("'")

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
        candidate = f"{current} {part}".strip()
        if len(candidate) <= max_chars:
            current = candidate
            continue
        if current:
            chunks.append(current)
            current = ""
        while len(part) > max_chars:
            chunks.append(part[:max_chars].rstrip())
            part = part[max_chars:].lstrip()
        current = part
    if current:
        chunks.append(current)
    return chunks


def chunk_text(text: str, max_chars: int = MAX_CHARS) -> list[str]:
    paragraphs = [paragraph.strip() for paragraph in re.split(r"\n\s*\n", text) if paragraph.strip()]
    chunks: list[str] = []
    current = ""

    for paragraph in paragraphs:
        if len(paragraph) > max_chars:
            if current:
                chunks.append(current)
                current = ""
            chunks.extend(split_long_text(paragraph, max_chars))
            continue

        candidate = f"{current}\n\n{paragraph}".strip()
        if len(candidate) <= max_chars:
            current = candidate
            continue

        if current:
            chunks.append(current)
        current = paragraph

    if current:
        chunks.append(current)
    return chunks


def parse_markdown_sections(book_path: Path, start_index: int = 0, source_kind: str = "book") -> list[Section]:
    text = book_path.read_text(encoding="utf-8")
    matches = list(re.finditer(r"(?m)^#\s+(.+?)\s*$", text))
    if not matches:
        cleaned = clean_markdown(text)
        return [
            Section(
                start_index,
                "Book",
                f"{start_index:02d}-book",
                book_path,
                source_kind,
                text,
                cleaned,
                chunk_text(cleaned),
            )
        ]

    sections: list[Section] = []
    for local_index, match in enumerate(matches):
        index = start_index + local_index
        start = match.start()
        end = matches[local_index + 1].start() if local_index + 1 < len(matches) else len(text)
        source_text = text[start:end].strip()
        title = match.group(1).strip()
        render_text = clean_markdown(source_text)
        if not render_text:
            continue
        slug = f"{index:02d}-{slugify(title)}"
        sections.append(
            Section(
                index=index,
                title=title,
                slug=slug,
                source_path=book_path,
                source_kind=source_kind,
                source_text=source_text,
                render_text=render_text,
                chunks=chunk_text(render_text),
            )
        )
    return sections


def parse_sections(book_path: Path) -> list[Section]:
    sections: list[Section] = []
    if FRONTMATTER_PATH.exists():
        sections.extend(
            parse_markdown_sections(
                FRONTMATTER_PATH,
                start_index=0,
                source_kind="copyright_frontmatter",
            )
        )
    sections.extend(
        parse_markdown_sections(book_path, start_index=len(sections), source_kind="manuscript")
    )
    if BACKMATTER_PATH.exists():
        sections.extend(
            parse_markdown_sections(
                BACKMATTER_PATH,
                start_index=len(sections),
                source_kind="factual_backmatter",
            )
        )
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
    had_previous_audio = output_path.exists() and output_path.stat().st_size > 0

    if had_previous_audio:
        actual_hash = hash_path.read_text(encoding="utf-8").strip() if hash_path.exists() else ""
        if actual_hash == expected_hash:
            print(f"Reusing {section.slug} chunk {chunk_index + 1}", flush=True)
            return {
                "index": chunk_index,
                "file": str(output_path),
                "text_file": str(text_path),
                "sha256": expected_hash,
                "chars": len(text),
                "status": "reused",
            }

    last_error = ""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            action = "Regenerating" if had_previous_audio else "Rendering"
            print(f"{action} {section.slug} chunk {chunk_index + 1}", flush=True)
            audio = request_audio(text, key)
            tmp_path = output_path.with_suffix(".mp3.part")
            tmp_path.write_bytes(audio)
            tmp_path.replace(output_path)
            text_path.write_text(text, encoding="utf-8")
            hash_path.write_text(expected_hash + "\n", encoding="utf-8")
            return {
                "index": chunk_index,
                "file": str(output_path),
                "text_file": str(text_path),
                "sha256": expected_hash,
                "chars": len(text),
                "status": "regenerated" if had_previous_audio else "rendered",
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

        print(f"Retrying {section.slug} chunk {chunk_index + 1} after transient error", flush=True)
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
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "anullsrc=r=44100:cl=mono",
            "-t",
            str(seconds),
            "-codec:a",
            "libmp3lame",
            "-b:a",
            "128k",
            "-ar",
            "44100",
            "-ac",
            "1",
            str(path),
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
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(list_path),
            "-af",
            "loudnorm=I=-20:TP=-3:LRA=11",
            "-codec:a",
            "libmp3lame",
            "-b:a",
            "128k",
            "-ar",
            "44100",
            "-ac",
            "1",
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
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
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


def build_manifest(sections: list[Section], dry_run: bool = False) -> dict[str, Any]:
    return {
        "voice": {
            "slug": VOICE_SLUG,
            "name": VOICE_NAME,
            "voice_id": VOICE_ID,
            "saved_voice_id": VOICE_ID,
        },
        "model_id": MODEL_ID,
        "output_format": OUTPUT_FORMAT,
        "book_path": str(BOOK_PATH),
        "backmatter_path": str(BACKMATTER_PATH) if BACKMATTER_PATH.exists() else None,
        "output_dir": str(OUT_DIR),
        "dry_run": dry_run,
        "chapters": [
            {
                "index": section.index,
                "title": section.title,
                "slug": section.slug,
                "source_path": str(section.source_path),
                "source_kind": section.source_kind,
                "source_chars": len(section.source_text),
                "render_chars": len(section.render_text),
                "chunks": [
                    {
                        "index": chunk_index,
                        "chars": len(chunk),
                        "sha256": text_hash(chunk),
                        "file": str(CHUNKS_DIR / section.slug / f"chunk-{chunk_index + 1:03d}.mp3"),
                        "text_file": str(CHUNKS_DIR / section.slug / f"chunk-{chunk_index + 1:03d}.txt"),
                    }
                    for chunk_index, chunk in enumerate(section.chunks)
                ],
                "mastered_file": str(MASTERS_DIR / f"{section.slug}.mp3"),
            }
            for section in sections
        ],
        "full_mastered_file": str(OUT_DIR / "the-amber-winter-afrikaans-emma-master.mp3"),
        "failures": [],
    }


def write_manifest(manifest: dict[str, Any]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def render_all(sections: list[Section], key: str, workers: int) -> dict[tuple[int, int], dict[str, Any]]:
    jobs = []
    results: dict[tuple[int, int], dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=workers) as executor:
        for section in sections:
            for chunk_index, chunk in enumerate(section.chunks):
                jobs.append(
                    (
                        section.index,
                        chunk_index,
                        executor.submit(render_chunk, section, chunk_index, chunk, key),
                    )
                )

        for section_index, chunk_index, future in jobs:
            try:
                results[(section_index, chunk_index)] = future.result()
            except Exception as error:
                results[(section_index, chunk_index)] = {
                    "index": chunk_index,
                    "status": "failed",
                    "error": repr(error),
                }
    return results


def enrich_manifest_with_results(
    manifest: dict[str, Any],
    sections: list[Section],
    results: dict[tuple[int, int], dict[str, Any]],
) -> None:
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
                        "error": chunk.get("error", "unknown error"),
                    }
                )
        chapter["failed"] = any(chunk.get("status") == "failed" for chunk in chapter["chunks"])
    manifest["failures"] = failures


def master_sections(manifest: dict[str, Any]) -> None:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg is required for mastering.")

    chunk_silence = WORK_DIR / "silence-0.35s.mp3"
    chapter_silence = WORK_DIR / "silence-2.0s.mp3"
    make_silence(chunk_silence, 0.35)
    make_silence(chapter_silence, 2.0)

    chapter_master_paths = []
    for chapter in manifest["chapters"]:
        if chapter.get("failed"):
            continue
        chunk_paths = [Path(chunk["file"]) for chunk in chapter["chunks"]]
        if not all(path.exists() and path.stat().st_size > 0 for path in chunk_paths):
            chapter["failed"] = True
            manifest["failures"].append({"chapter": chapter["title"], "error": "missing chunk file"})
            continue

        master_path = Path(chapter["mastered_file"])
        list_path = WORK_DIR / f"{chapter['slug']}-concat.txt"
        master_audio(chunk_paths, master_path, list_path, chunk_silence if len(chunk_paths) > 1 else None)
        chapter["mastered_probe"] = probe_audio(master_path)
        chapter_master_paths.append(master_path)

    if len(chapter_master_paths) == len(manifest["chapters"]):
        full_master_path = Path(manifest["full_mastered_file"])
        master_audio(
            chapter_master_paths,
            full_master_path,
            WORK_DIR / "full-book-concat.txt",
            chapter_silence,
        )
        manifest["full_mastered_probe"] = probe_audio(full_master_path)
    else:
        manifest["full_mastered_probe"] = {}


def print_plan(sections: list[Section]) -> None:
    total_render_chars = sum(len(section.render_text) for section in sections)
    total_chunks = sum(len(section.chunks) for section in sections)
    print(f"Sections: {len(sections)}", flush=True)
    print(f"Render characters: {total_render_chars}", flush=True)
    print(f"Chunks: {total_chunks} at max {MAX_CHARS} chars", flush=True)
    for section in sections:
        print(
            f"{section.index:02d} {section.title}: {len(section.render_text)} chars, {len(section.chunks)} chunks",
            flush=True,
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Write a manifest and print the render plan only.")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS, help="Bounded ElevenLabs request concurrency.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    sections = parse_sections(BOOK_PATH)
    workers = max(1, min(args.workers, 4))
    manifest = build_manifest(sections, dry_run=args.dry_run)
    write_manifest(manifest)
    print_plan(sections)

    if args.dry_run:
        print(f"Dry-run manifest: {MANIFEST_PATH}", flush=True)
        return

    key = load_key()
    results = render_all(sections, key, workers)
    enrich_manifest_with_results(manifest, sections, results)
    write_manifest(manifest)

    if manifest["failures"]:
        print(f"Rendering completed with {len(manifest['failures'])} failure(s). Manifest: {MANIFEST_PATH}", flush=True)
        return

    master_sections(manifest)
    write_manifest(manifest)
    print(f"Done: {manifest['full_mastered_file']}", flush=True)
    print(f"Manifest: {MANIFEST_PATH}", flush=True)


if __name__ == "__main__":
    main()
