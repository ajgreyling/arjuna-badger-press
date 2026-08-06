#!/usr/bin/env python3
"""Lay the title + author typography onto the bright painterly cover plate for *Die Amberwinter*.

Reads design/cover-plate.png (the three figures on the snowy hill — text-free, bright/colourful,
deliberately UNLIKE the dark house style), adds soft legibility scrims and house display
typography in amber-gold, and writes the typeset cover to design/cover.{png,jpg} + build/export/
cover.{png,jpg}. Same house method as *Henry Sugar* / *A Man They All Read Wrong*.

Adult Norse saga, Book I (Afrikaans): eyebrow = "DIE AMBERWINTER · BOEK I"; an amber-gold ink to
sit with the warm plate; a discreet "VIR VOLWASSE LESERS" mark at the foot (the public adult shelf).

    python3 design/make_cover.py
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
PLATE = HERE / "cover-plate.png"
OUT = [


    HERE / "cover.png",
    HERE / "cover.jpg",
    BOOK / "build" / "export" / "cover.png",
    BOOK / "build" / "export" / "cover.jpg",
]

INK = (248, 240, 226, 255)        # warm bone-white title ink
AMBER = (224, 150, 70, 255)       # ember-amber for the eyebrow / tagline accent (matches #C77A3A shelf)
GOLD = (228, 190, 118, 255)       # softer gold for the adult mark
SHADOW = (40, 18, 6, 220)         # warm dark shadow (not the house's cold black)


def _repo() -> Path:
    p = Path(__file__).resolve()
    for cand in p.parents:
        if (cand / "assets" / "fonts" / "AtkinsonHyperlegible-Bold.otf").is_file():
            return cand
    raise SystemExit("make_cover: cannot find repo assets/fonts/AtkinsonHyperlegible-*.otf")


_REPO = _repo()
_ATK = _REPO / "assets" / "fonts"
ATK_REG = str(_ATK / "AtkinsonHyperlegible-Regular.otf")
ATK_BOLD = str(_ATK / "AtkinsonHyperlegible-Bold.otf")
ATK_ITAL = str(_ATK / "AtkinsonHyperlegible-Italic.otf")
ATK_BI = str(_ATK / "AtkinsonHyperlegible-BoldItalic.otf")

DIDOT = ATK_BOLD
COCHIN = ATK_REG
COPPER = ATK_REG
def font(path: str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size, index=index)


def text_width(draw, s, fnt, tracking):
    w = 0
    for ch in s:
        w += draw.textlength(ch, font=fnt) + tracking
    return w - tracking if s else 0


def draw_tracked(draw, cx, y, s, fnt, tracking, fill, shadow=True):
    total = text_width(draw, s, fnt, tracking)
    x = cx - total / 2
    for ch in s:
        if shadow:
            draw.text((x + 2, y + 3), ch, font=fnt, fill=SHADOW)
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking


def main() -> None:
    img = Image.open(PLATE).convert("RGBA")

    # ── Sky headroom ──────────────────────────────────────────────────────────────────────────
    # The figures' heads start high on this plate, so the title had nowhere clean to sit. Add a
    # band of extra sky at the top by stretching the plate's top sliver upward, then re-crop to
    # 2:3. This pushes the figures down in the final frame and gives the title its own clear sky.
    PW, PH = img.size
    HEADROOM = 0.16  # add 16% of height as sky above the existing image
    add = int(PH * HEADROOM)
    sliver = img.crop((0, 0, PW, max(2, int(PH * 0.06))))      # the topmost pure-sky strip
    sky = sliver.resize((PW, add), Image.Resampling.LANCZOS)   # stretch it up into a tall band
    canvas = Image.new("RGBA", (PW, PH + add))
    canvas.paste(sky, (0, 0))
    canvas.paste(img, (0, add))
    # re-crop the bottom to restore an exact 2:3 (portrait) ratio
    target_h = int(PW * 3 / 2)
    img = canvas.crop((0, 0, PW, target_h)) if (PH + add) >= target_h else canvas
    W, H = img.size
    cx = W / 2

    # Legibility scrims — gently darken the top (eyebrow + title) and the very bottom (author +
    # adult mark) WITHOUT killing the bright painterly plate. Warm scrim, not cold black.
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    # Cinematic plate with a PALE dawn sky at the top, so the top scrim is strong (the bone-white
    # title must read against a bright sky) and tapers fast so the figures stay lit. The foot is
    # already dark, so a light foot scrim just seats the author line. Cool blue-black to match the sky.
    top_end = int(H * 0.30)
    for y in range(top_end):
        a = int(225 * (1 - y / top_end) ** 1.45)
        sd.line([(0, y), (W, y)], fill=(9, 14, 24, a))
    bot_start = int(H * 0.86)
    for y in range(bot_start, H):
        a = int(140 * ((y - bot_start) / (H - bot_start)) ** 1.3)
        sd.line([(0, y), (W, y)], fill=(6, 9, 16, a))
    img = Image.alpha_composite(img, scrim)

    draw = ImageDraw.Draw(img)

    # Eyebrow — series line, in the calm dark upper third.
    f_eyebrow = font(COPPER, 25)
    draw_tracked(draw, cx, int(H * 0.040), "WINTER SONDER EINDE  ·  BOEK I", f_eyebrow, 6, AMBER)

    rule_y = int(H * 0.040) + 42
    rw = 175
    draw.line([(cx - rw, rule_y), (cx + rw, rule_y)], fill=AMBER, width=2)

    # Title — "DIE VUUR IN DIE DONKER", compact and high so the whole block clears the figures'
    # heads (which start ~30% down). Smaller + tighter line-height, finishing by ~26% H.
    # Bone-white with the warm shadow for lift off the pale sky.
    f_title = font(DIDOT, 96)
    lines = ["DIE VUUR", "IN DIE", "DONKER"]
    ty = int(H * 0.072)
    lh = 102
    for i, ln in enumerate(lines):
        draw_tracked(draw, cx, ty + i * lh, ln, f_title, 3, INK)

    # Author — at the quiet foot.
    f_auth = font(COCHIN, 44)
    draw_tracked(draw, cx, int(H * 0.905), "ANDRIES J. GREYLING", f_auth, 7, INK)

    # Adult mark — discreet, at the very foot (this is the public adult shelf).
    f_adult = font(COPPER, 22)
    draw_tracked(draw, cx, int(H * 0.955), "VIR VOLWASSE LESERS", f_adult, 5, GOLD)

    out = img.convert("RGB")
    for p in OUT:
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.suffix.lower() == ".jpg":
            out.save(p, "JPEG", quality=92)
        else:
            out.save(p, "PNG")
        print(f"wrote {p}")


if __name__ == "__main__":
    main()
