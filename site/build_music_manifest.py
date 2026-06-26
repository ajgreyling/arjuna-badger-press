#!/usr/bin/env python3
"""Build the music manifest for the "The Man They All Misread" player page.

The badger thesis made concrete: AJ's own catalogue, on AJ's own rails — a
self-hosted web player, not a streaming silo. This script reads the REAL lane
structure and REAL track titles from the music workspace and emits a JSON
manifest the player page (rendered by build.py) consumes at runtime.

SOURCE OF TRUTH
---------------
  ~/code/congosky-music/DAILY_RELEASE_PLAN.json   — lane → title mapping (real)
  ~/code/congosky-music/downloads/*.mp3           — real audio on disk (147 files)

If the music workspace is not present (e.g. CI, or a clean checkout), this
script falls back to a small committed snapshot baked in below so the page
still builds with real titles. Re-run with the workspace present to refresh.

AUDIO URLs — HONEST STATUS (read this)
--------------------------------------
The MP3s exist on disk in ~/code/congosky-music/downloads/ but are NOT yet
hosted. The `audioUrl` fields below point at where each file WILL live once
self-hosted on Cloudflare R2:  /audio/<lane-slug>/<track-slug>.mp3

THESE ARE PLACEHOLDER PATHS. The player UI is fully wired against them, but no
audio will actually stream until the MP3s are uploaded to R2 (or copied into
site/public/audio/) and served at those paths. That upload is "the flip" to go
live — see the report. Until then, play/seek/next/prev all work as UI; the
<audio> element simply won't find a file.

Usage:  python3 site/build_music_manifest.py
Output: site/content/music-manifest.json
"""
from __future__ import annotations

import collections
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
OUT_JSON = HERE / "content" / "music-manifest.json"

# The music workspace (sibling project). Override with MUSIC_DIR env if needed.
MUSIC_DIR = Path(os.environ.get(
    "MUSIC_DIR", Path.home() / "code" / "congosky-music"))

# Where self-hosted audio will live once uploaded to R2 (see module docstring).
AUDIO_BASE = "/audio"

# Lane display order on the page. Lead with the Jakobus title-track lane (the
# book's namesake), then the breakout Banjos & Bass, then the rest. This order
# follows congosky-music/DISTRIBUTION.md ("lead with Banjos & Bass") tempered
# by the page's framing (the Jakobus / Misread Man lane is the namesake).
LANE_ORDER = [
    "Jakobus Brass'n'Bass — The Misread Man",
    "Banjos & Bass — Arjuna Sound",
    "The Still Man Banger Series",
    "Die Dier Saga — Afrikaans",
    "Wolf / Hardekool — Afrikaans Gothic",
    "Rasta — Golden Hour",
    "O Brother — Old-Timey",
    "Prog Epic",
    "Red-Robot — Family Saga",
]

# Short, honest blurbs per lane — drawn from congosky-music/STYLES.md so the
# copy matches the actual sound. Kept tight; the music does the talking.
LANE_BLURBS = {
    "Jakobus Brass'n'Bass — The Misread Man":
        "Black Betty at a boeredans. Bass-house under outlaw-country swing, horn "
        "stabs, a gospel-choir swell on the bridge, then a massive drop. The "
        "title lane — the soundtrack to A Man They All Read Wrong.",
    "Banjos & Bass — Arjuna Sound":
        "Bluegrass EDM. The full Steve'n'Seagulls redneck arsenal — banjo, "
        "fiddle, washboard — over a four-on-the-floor kick. Stomp the floor.",
    "The Still Man Banger Series":
        "The quiet man finally opens the throttle on an absurdly slow vehicle — "
        "milk float, Zamboni, steamroller, hearse. Hick-hop bangers, every one.",
    "Die Dier Saga — Afrikaans":
        "Die Dier — the Beast. The Afrikaans saga lane: gravel-baritone gothic "
        "and four-on-the-floor sub-bass, sung in the language of the veld.",
    "Wolf / Hardekool — Afrikaans Gothic":
        "Sisters of Mercy in Afrikaans. Weathered gravel baritone, war-cry gang "
        "chants, drum-machine four-on-the-floor, banging sub-bass.",
    "Rasta — Golden Hour":
        "The Pieter sound. Classic roots reggae meets modern California reggae — "
        "warm dub bass, offbeat skank, melodica, golden-hour cocktail groove.",
    "O Brother — Old-Timey":
        "Down to the river. Appalachian, sacred-harp, bluegrass-gospel — close "
        "harmony and long, lingering held notes.",
    "Prog Epic":
        "A track that is a journey. Multi-movement prog suite that changes gears "
        "seamlessly — synth pulse, ballad, operatic stack, hard-rock drive — all "
        "riding a deep bass spine.",
    "Red-Robot — Family Saga":
        "The dedication. The family-saga lane — Andries & Monica, Kransfontein, "
        "the doors that were opened. Sung straight, sung true.",
}

LANE_SLUGS = {
    "Jakobus Brass'n'Bass — The Misread Man": "jakobus-brass-n-bass",
    "Banjos & Bass — Arjuna Sound": "banjos-and-bass",
    "The Still Man Banger Series": "still-man-bangers",
    "Die Dier Saga — Afrikaans": "die-dier-saga",
    "Wolf / Hardekool — Afrikaans Gothic": "wolf-hardekool",
    "Rasta — Golden Hour": "rasta-golden-hour",
    "O Brother — Old-Timey": "o-brother",
    "Prog Epic": "prog-epic",
    "Red-Robot — Family Saga": "red-robot",
}


def slugify(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = s.lower()
    s = re.sub(r"['`’]", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def clean_title(t: str) -> str:
    """Display title: drop the trailing ' (A)' / ' (B)' Suno-variant marker.

    The plan ships two Suno renders per song (A and B). For the player we show
    one clean entry per song and keep the variant on the side so a listener can
    flip A/B if both audio files are wired later.
    """
    return re.sub(r"\s*\([A-D]\)\s*$", "", t).strip()


def variant_of(t: str) -> str:
    m = re.search(r"\(([A-D])\)\s*$", t)
    return m.group(1) if m else "A"


def build_from_plan(plan_path: Path, downloads: set[str]):
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    # lane -> ordered list of raw plan titles (deduped, plan order preserved)
    lanes = collections.OrderedDict()
    for day in plan:
        for item in day:
            lane = item["lane"]
            title = item["title"]
            lanes.setdefault(lane, [])
            if title not in lanes[lane]:
                lanes[lane].append(title)
    return lanes


def to_manifest(lanes: dict, downloads: set[str]) -> dict:
    out_lanes = []
    order = [l for l in LANE_ORDER if l in lanes]
    # any lanes not in the explicit order get appended (forward-compatible)
    order += [l for l in lanes if l not in order]

    n_tracks = 0
    n_with_audio_on_disk = 0
    for lane in order:
        lane_slug = LANE_SLUGS.get(lane, slugify(lane))
        # collapse A/B variants into one display track, keeping variant info
        by_song = collections.OrderedDict()
        for raw in lanes[lane]:
            disp = clean_title(raw)
            var = variant_of(raw)
            mp3_name = f"{raw}.mp3"
            on_disk = mp3_name in downloads
            song = by_song.setdefault(disp, {
                "title": disp,
                "variants": [],
            })
            song["variants"].append({
                "label": var,
                # Where the file WILL live on R2 (placeholder — see docstring).
                "audioUrl": f"{AUDIO_BASE}/{lane_slug}/{slugify(raw)}.mp3",
                # Honest signal for the page: do we actually have the bytes yet?
                "onDisk": on_disk,
            })
        tracks = []
        for disp, song in by_song.items():
            primary = song["variants"][0]
            n_tracks += 1
            if any(v["onDisk"] for v in song["variants"]):
                n_with_audio_on_disk += 1
            tracks.append({
                "title": disp,
                "audioUrl": primary["audioUrl"],
                "variants": song["variants"],
            })
        out_lanes.append({
            "name": lane,
            "slug": lane_slug,
            "blurb": LANE_BLURBS.get(lane, ""),
            "tracks": tracks,
        })

    return {
        "_comment": (
            "Companion player manifest for 'The Man They All Misread' — AJ's "
            "Jakobus & Beast catalogue, self-hosted (the badger thesis). "
            "audioUrl paths are PLACEHOLDERS pointing at /audio/<lane>/<slug>.mp3 "
            "where the MP3s will live once uploaded to Cloudflare R2. Until then "
            "the UI is live but no audio streams. Regenerate with "
            "site/build_music_manifest.py against ~/code/congosky-music."),
        "title": "The Man They All Misread",
        "subtitle": "Jakobus & Beast — the companion player",
        "artist": "Arjuna Sound",
        "audioBase": AUDIO_BASE,
        "stats": {
            "lanes": len(out_lanes),
            "tracks": n_tracks,
            "tracksWithAudioOnDisk": n_with_audio_on_disk,
        },
        "lanes": out_lanes,
    }


# A tiny committed fallback so the page builds even without the music workspace.
# Real titles, real lanes — just a sampling. Regenerate for the full catalogue.
FALLBACK_LANES = collections.OrderedDict([
    ("Jakobus Brass'n'Bass — The Misread Man", [
        "Stil Water, Diepe Grond (A)", "The Perfect Note (for Todd) (A)",
        "Turn It Up, Hennie (A)", "Vat Hom, Jakobus (A)",
        "Two Is One and One Is None (Henni-Twee) (A)",
    ]),
    ("Banjos & Bass — Arjuna Sound", [
        "Stomp the Floor (Banjos and Bass) (A)", "Banjos and Bass (A)",
        "Moonshine Mountain (A)", "Ghost in the Holler (A)",
        "Mud on the Tyres (A)", "General Lee (Banjos and Bass) (A)",
    ]),
    ("The Still Man Banger Series", [
        "Combine Harvester (A)", "Zamboni (A)", "Steamroller (A)",
        "Milk Float (A)", "Hearse (A)", "Snow Plow (A)",
    ]),
    ("Die Dier Saga — Afrikaans", [
        "Die Dier (The Beast) (A)", "Die Vuur (The Fire) (A)",
        "Die Rivier (The River) (A)", "Die Brug (The Bridge) (A)",
    ]),
    ("Wolf / Hardekool — Afrikaans Gothic", [
        "Hardekool (A)", "Black Beauty (A)", "Old Yeller (A)",
        "Run, Little Prince (A)",
    ]),
    ("Rasta — Golden Hour", [
        "The Whole Beautiful Mess (for Pieter) (A)",
    ]),
    ("O Brother — Old-Timey", [
        "Down to the Water (A)",
    ]),
    ("Prog Epic", [
        "The Still Man Rides (A Suite) (A)",
    ]),
    ("Red-Robot — Family Saga", [
        "Red-Robot (Andries & Monica) (A)",
        "Through the Doors (Kransfontein) (A)",
    ]),
])


def main() -> int:
    plan_path = MUSIC_DIR / "DAILY_RELEASE_PLAN.json"
    downloads_dir = MUSIC_DIR / "downloads"
    downloads = set(os.listdir(downloads_dir)) if downloads_dir.is_dir() else set()

    if plan_path.is_file():
        lanes = build_from_plan(plan_path, downloads)
        source = f"{plan_path} ({sum(len(v) for v in lanes.values())} plan entries)"
    else:
        lanes = FALLBACK_LANES
        source = "baked-in fallback (music workspace not found)"

    manifest = to_manifest(lanes, downloads)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")

    st = manifest["stats"]
    print(f"  music manifest ← {source}")
    print(f"  → {OUT_JSON.relative_to(REPO)}")
    print(f"     {st['lanes']} lanes · {st['tracks']} tracks · "
          f"{st['tracksWithAudioOnDisk']} have audio on disk (not yet hosted)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
