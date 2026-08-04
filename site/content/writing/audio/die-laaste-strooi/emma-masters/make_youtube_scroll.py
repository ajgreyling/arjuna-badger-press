#!/usr/bin/env python3
"""Build a YouTube upload: cover background + scrolling story text (Atkinson Hyperlegible)."""

from __future__ import annotations

import re
import shutil
import subprocess
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
# emma-masters -> die-laaste-strooi -> audio -> writing
STORY = HERE.parents[2] / "die-laaste-strooi.md"
COVER = HERE / "cover.png"
AUDIO = HERE / "Die Laaste Strooi.mp3"
OUT = HERE / "Die Laaste Strooi.mp4"
WORK = HERE / "_work_youtube"
SCROLL_PNG = WORK / "scroll_text.png"

FONT_REG = Path("/Users/ajgreyling/Library/Fonts/Atkinson-Hyperlegible-Regular-102.otf")
FONT_BOLD = Path("/Users/ajgreyling/Library/Fonts/Atkinson-Hyperlegible-Bold-102.otf")
# fallbacks in-repo
if not FONT_REG.exists():
    FONT_REG = Path(
        "/Users/ajgreyling/code/arjuna-badger/arjuna-badger-press/assets/fonts/AtkinsonHyperlegible-Regular.otf"
    )
    FONT_BOLD = Path(
        "/Users/ajgreyling/code/arjuna-badger/arjuna-badger-press/assets/fonts/AtkinsonHyperlegible-Bold.otf"
    )

SIZE = 1080
MARGIN_X = 88
BODY_SIZE = 36
HEAD_SIZE = 48
TITLE_SIZE = 64
LINE_GAP = 12
PARA_GAP = 28
HEAD_GAP_BEFORE = 48
HEAD_GAP_AFTER = 20
TEXT_COLOR = (255, 246, 230, 255)
HEAD_COLOR = (255, 228, 186, 255)
TITLE_COLOR = (255, 252, 245, 255)
SUB_COLOR = (230, 210, 180, 240)
SHADOW = (0, 0, 0, 180)
LEAD_IN_S = 4.0
TRAIL_S = 6.0


def clean_story(md: str) -> list[tuple[str, str]]:
    """Return list of (kind, text) where kind is title|subtitle|heading|body|blank."""
    blocks: list[tuple[str, str]] = []
    lines = md.splitlines()
    i = 0
    # title
    if lines and lines[0].startswith("# "):
        blocks.append(("title", lines[0][2:].strip()))
        i = 1
    while i < len(lines):
        raw = lines[i].rstrip()
        i += 1
        if not raw or raw == "---":
            continue
        if raw.startswith("*") and raw.endswith("*") and not raw.startswith("**"):
            blocks.append(("subtitle", raw.strip("*").strip()))
            continue
        if raw.startswith("## "):
            blocks.append(("heading", raw[3:].strip()))
            continue
        if raw.startswith("#"):
            continue
        # gather paragraph
        para = [raw]
        while i < len(lines):
            nxt = lines[i].rstrip()
            if not nxt or nxt == "---" or nxt.startswith("#") or (
                nxt.startswith("*") and nxt.endswith("*") and not nxt.startswith("**")
            ):
                break
            para.append(nxt)
            i += 1
        text = " ".join(para)
        text = text.replace("**", "").replace("__", "")
        text = re.sub(r"(?<!\w)\*(.+?)\*(?!\w)", r"\1", text)
        blocks.append(("body", text))
    return blocks


def wrap_block(text: str, font: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    # approximate wrap via character estimate then refine
    avg = max(font.getlength("abcdefghijklmnopqrstuvwxyz") / 26, 1)
    width_chars = max(int(max_w / avg), 12)
    return textwrap.wrap(text, width=width_chars, break_long_words=False, break_on_hyphens=False) or [""]


def measure_and_layout(blocks: list[tuple[str, str]], max_w: int) -> list[tuple[str, str, ImageFont.FreeTypeFont, tuple]]:
    fonts = {
        "title": ImageFont.truetype(str(FONT_BOLD), TITLE_SIZE),
        "subtitle": ImageFont.truetype(str(FONT_REG), BODY_SIZE),
        "heading": ImageFont.truetype(str(FONT_BOLD), HEAD_SIZE),
        "body": ImageFont.truetype(str(FONT_REG), BODY_SIZE),
    }
    colors = {
        "title": TITLE_COLOR,
        "subtitle": SUB_COLOR,
        "heading": HEAD_COLOR,
        "body": TEXT_COLOR,
    }
    laid: list[tuple[str, str, ImageFont.FreeTypeFont, tuple]] = []
    for kind, text in blocks:
        font = fonts[kind]
        color = colors[kind]
        if kind == "heading":
            laid.append(("gap", "", font, color))
        for line in wrap_block(text, font, max_w):
            laid.append((kind, line, font, color))
        if kind in ("title", "subtitle", "heading"):
            laid.append(("gap", "", font, color))
        else:
            laid.append(("para", "", font, color))
    return laid


def render_scroll(laid: list[tuple[str, str, ImageFont.FreeTypeFont, tuple]]) -> Image.Image:
    max_w = SIZE - 2 * MARGIN_X
    # measure height
    heights: list[int] = []
    for kind, line, font, _ in laid:
        if kind == "gap":
            heights.append(HEAD_GAP_BEFORE if not line else LINE_GAP)
        elif kind == "para":
            heights.append(PARA_GAP)
        else:
            bbox = font.getbbox(line or "Ag")
            heights.append((bbox[3] - bbox[1]) + LINE_GAP)

    total_h = sum(heights) + SIZE  # extra pad so last lines can exit
    img = Image.new("RGBA", (SIZE, total_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    y = SIZE // 3  # start a bit down so title enters from below after lead

    for (kind, line, font, color), h in zip(laid, heights):
        if kind in ("gap", "para") or not line:
            y += h
            continue
        # soft shadow for legibility on busy cover
        for dx, dy in ((2, 2), (1, 1), (0, 2)):
            draw.text((MARGIN_X + dx, y + dy), line, font=font, fill=SHADOW)
        draw.text((MARGIN_X, y), line, font=font, fill=color)
        y += h

    # trim unused bottom but keep exit pad
    content_bottom = y + SIZE // 2
    return img.crop((0, 0, SIZE, min(content_bottom, img.height)))


def audio_duration() -> float:
    ffprobe = shutil.which("ffprobe") or "/opt/homebrew/bin/ffprobe"
    out = subprocess.check_output(
        [
            ffprobe,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(AUDIO),
        ],
        text=True,
    ).strip()
    return float(out)


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    blocks = clean_story(STORY.read_text(encoding="utf-8"))
    # content warning up front
    blocks = [
        ("title", "Die Laaste Strooi"),
        ("subtitle", "Andries J. Greyling  ·  vertel deur Emma Lilliana"),
        ("subtitle", "Inhoudswaarskuwing: geweld, moord. Vir volwasse luisteraars."),
    ] + [b for b in blocks if b[0] != "title"]

    laid = measure_and_layout(blocks, SIZE - 2 * MARGIN_X)
    scroll = render_scroll(laid)
    scroll.save(SCROLL_PNG)
    print(f"[scroll] {SCROLL_PNG}  {scroll.size[0]}x{scroll.size[1]}")

    # darkened cover background
    cover = Image.open(COVER).convert("RGB").resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    cover = ImageEnhance.Brightness(cover).enhance(0.42)
    cover = ImageEnhance.Contrast(cover).enhance(1.05)
    # soft vignette via dark edges
    vignette = Image.new("RGB", (SIZE, SIZE), (20, 12, 8))
    mask = Image.new("L", (SIZE, SIZE), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse((-SIZE * 0.15, -SIZE * 0.15, SIZE * 1.15, SIZE * 1.15), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(80))
    cover = Image.composite(cover, vignette, mask)
    bg_path = WORK / "bg.png"
    cover.save(bg_path)

    dur = audio_duration()
    scroll_h = scroll.size[1]
    # scroll from y=SIZE (just below frame) to y=-(scroll_h) over (dur - lead - trail)
    travel = SIZE + scroll_h
    active = max(dur - LEAD_IN_S - TRAIL_S, 1.0)
    # y(t) = SIZE - max(0, t-LEAD) * travel / active
    # ffmpeg expression:
    y_expr = f"H-(({LEAD_IN_S:.3f})+t)*{travel / (active + LEAD_IN_S):.6f}"
    # Better: hold for lead-in, then scroll, then hold trail
    # y = SIZE - max(0, min(t-LEAD, active)) * travel / active
    y_expr = (
        f"{SIZE}-max(0\\,min(t-{LEAD_IN_S:.3f}\\,{active:.3f}))*{travel / active:.6f}"
    )

    ffmpeg = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"
    cmd = [
        ffmpeg,
        "-y",
        "-loop",
        "1",
        "-i",
        str(bg_path),
        "-loop",
        "1",
        "-i",
        str(SCROLL_PNG),
        "-i",
        str(AUDIO),
        "-filter_complex",
        (
            f"[0:v]fps=30,format=yuv420p[bg];"
            f"[1:v]format=rgba[txt];"
            f"[bg][txt]overlay=x=(W-w)/2:y='{y_expr}':shortest=1[v]"
        ),
        "-map",
        "[v]",
        "-map",
        "2:a",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "18",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-ar",
        "44100",
        "-ac",
        "2",
        "-t",
        f"{dur:.3f}",
        "-movflags",
        "+faststart",
        str(OUT),
    ]
    print("[ffmpeg]", " ".join(cmd[:8]), "...")
    subprocess.run(cmd, check=True)
    print(f"[out] {OUT}  ({OUT.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
