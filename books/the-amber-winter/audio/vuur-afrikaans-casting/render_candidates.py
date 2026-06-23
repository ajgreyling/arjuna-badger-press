#!/usr/bin/env python3
"""Render the Vuur Afrikaans voice-casting scene with ElevenLabs."""

import json
import os
import subprocess
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


OUT = Path(__file__).resolve().parent
SCENE_PATH = OUT / "scene.txt"
MODEL_ID = "eleven_v3"
OUTPUT_FORMAT = "mp3_44100_128"

CANDIDATES = [
    {
        "slug": "katherine",
        "name": "Katherine - Clear, Warm, and Polished",
        "voice_id": "0zUZ5qUGb8wympsfJH8d",
        "owner": "c1a6bf87ce050e7ce7128fe7d0c02b2b1d0cde42cafc9e9de229f2b7ae226b16",
    },
    {
        "slug": "mulio",
        "name": "Mulio - Warm, Smooth, and Raspy",
        "voice_id": "ZbI9lWkt1RyZ47WRzQ7t",
        "owner": "c31b3c3a38418f0829e9788bf008085d92a7a31c4d989d091eff3d03c3507786",
    },
    {
        "slug": "mel",
        "name": "Mel - Narration, Warm and Friendly",
        "voice_id": "hPCkcWzRwKvb97383AaN",
        "owner": "a56cdabb00948103fcc4c679cb361de6fc0cbbdd8ea3dc443e56b88b85cbe104",
    },
    {
        "slug": "emma",
        "name": "Emma Lilliana - Soft, Warm and Gentle",
        "voice_id": "0z8S749Xe6jLCD34QXl1",
        "owner": "9d5305808f2b6934f742a1c976e1dc6b3a9c0115d9bf076ede392d1df13126c0",
    },
]


def load_key() -> str:
    for name in ("ELEVENLABS_API_KEY", "XI_API_KEY"):
        value = os.environ.get(name)
        if value:
            return value

    repo_root = OUT.parents[4]
    for rel_path in (
        "arjuna-badger-platform/.env",
        ".env",
        "arjuna-badger-platform/deploy/.env",
    ):
        path = repo_root / rel_path
        if not path.exists():
            continue

        for line in path.read_text().splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            name, value = stripped.split("=", 1)
            if name.strip() in ("ELEVENLABS_API_KEY", "XI_API_KEY") and value.strip():
                return value.strip().strip("\"").strip("'")

    raise RuntimeError("Set ELEVENLABS_API_KEY or XI_API_KEY before rendering.")


def request_json(method: str, url: str, key: str, payload: dict | None = None) -> dict:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={"xi-api-key": key, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        body = response.read()
    return json.loads(body.decode("utf-8")) if body else {}


def save_voice(candidate: dict, key: str) -> tuple[str, str]:
    url = (
        "https://api.elevenlabs.io/v1/voices/add/"
        f"{candidate['owner']}/{candidate['voice_id']}"
    )
    payload = {
        "new_name": f"Vuur Afrikaans Candidate - {candidate['slug'].title()}",
        "bookmarked": True,
    }

    try:
        data = request_json("POST", url, key, payload)
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", "replace").lower()
        already_saved = any(token in body for token in ("already", "exists", "duplicate"))
        if error.code in (400, 409, 422) and already_saved:
            return candidate["voice_id"], "already_saved"
        raise

    return data.get("voice_id") or candidate["voice_id"], "saved"


def render_voice(candidate: dict, voice_id: str, key: str, scene: str) -> Path:
    url = (
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        f"?output_format={OUTPUT_FORMAT}"
    )
    payload = {
        "text": scene,
        "model_id": MODEL_ID,
        "voice_settings": {
            "stability": 0.35,
            "similarity_boost": 0.75,
            "style": 0.35,
            "use_speaker_boost": True,
            "speed": 0.93,
        },
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={"xi-api-key": key, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        audio = response.read()

    output_path = OUT / f"{candidate['slug']}-joelfees-scene.mp3"
    output_path.write_bytes(audio)
    return output_path


def render_candidate(index: int, candidate: dict, key: str, scene: str) -> dict:
    saved_voice_id, save_status = save_voice(candidate, key)
    print(f"Rendering {candidate['slug']} ({save_status})")
    output_path = render_voice(candidate, saved_voice_id, key, scene)
    return {
        "index": index,
        **candidate,
        "saved_voice_id": saved_voice_id,
        "save_status": save_status,
        "file": str(output_path),
    }


def stitch(files: list[Path]) -> Path:
    silence = OUT / "silence-2s.mp3"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "anullsrc=r=44100:cl=mono",
            "-t",
            "2",
            "-q:a",
            "9",
            "-acodec",
            "libmp3lame",
            str(silence),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    concat = OUT / "concat-list.txt"
    with concat.open("w") as handle:
        for index, file_path in enumerate(files):
            handle.write(f"file '{file_path.resolve()}'\n")
            if index != len(files) - 1:
                handle.write(f"file '{silence.resolve()}'\n")

    stitched = OUT / "00-stitched-female-candidates-joelfees-scene.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(stitched)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return stitched


def main() -> None:
    key = load_key()
    scene = SCENE_PATH.read_text()
    manifest_candidates = []

    with ThreadPoolExecutor(max_workers=len(CANDIDATES)) as executor:
        futures = [
            executor.submit(render_candidate, index, candidate, key, scene)
            for index, candidate in enumerate(CANDIDATES)
        ]
        for future in as_completed(futures):
            result = future.result()
            manifest_candidates.append(result)
            print(f"Finished {result['slug']}: {result['file']}")

    manifest_candidates.sort(key=lambda candidate: candidate["index"])
    rendered_files = [Path(candidate["file"]) for candidate in manifest_candidates]

    stitched = stitch(rendered_files)
    (OUT / "manifest.json").write_text(
        json.dumps(
            {
                "model_id": MODEL_ID,
                "output_format": OUTPUT_FORMAT,
                "scene_chars": len(scene),
                "stitched_file": str(stitched),
                "candidates": manifest_candidates,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    print(f"Done: {stitched}")


if __name__ == "__main__":
    main()
