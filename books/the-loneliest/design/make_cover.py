#!/usr/bin/env python3
"""Cover for *The Loneliest People in the World* — the blown-up-newsprint dossier cover.

Visual thesis (AJ's brief, 2026-06-15): take HIS real matric portrait and print it AS a coarse
newspaper photo — enlarged until the halftone dots are plainly visible — set in a period newspaper
column. The novella's whole engine is "the boy they all read wrong"; a newsprint photo IS that —
a face reduced to dots and a caption, the public record that never got the private truth. The
gold-striped school blazer carries the African-Gold / Arjuna-Badger gold for free.

FIREWALL NOTE: this cover uses AJ's real face by his EXPLICIT instruction (2026-06-15), consciously
overriding the standing "the dossier takes documents, not faces / portrait stays private" rule —
for THIS cover only. No other person's likeness is used. Source is the private archive portrait
(Photomyne 'Aj-035'); the working file path below is local-only and NOT committed.

Method: Pillow-only, deterministic, 1800×2700 (6×9in @ 300dpi). Same house pipeline as the other
covers, but the dominant language here is newsprint (right for this book specifically).

    python3 books/the-loneliest/design/make_cover.py
      -> design/cover.{png,jpg} + build/export/cover.{png,jpg} + covers/the-loneliest.jpg
"""
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageEnhance

HERE = Path(__file__).resolve().parent          # books/the-loneliest/design
BOOK = HERE.parent                              # books/the-loneliest
REPO = BOOK.parent.parent                       # repo root

# Source portrait — PRIVATE local-only working copy (never committed). If the downscale is gone,
# fall back to the raw Photomyne export.
SRC_CANDIDATES = [
    Path("/tmp/photobatch/Aj_-_035.jpg"),
    Path("/tmp/photobatch_raw/Aj - 035.jpg"),
    Path("/tmp/photobatch_raw/Aj_-_035.jpg"),
]

OUT_PATHS = [
    HERE / "cover.png",
    HERE / "cover.jpg",
    BOOK / "build" / "export" / "cover.png",
    BOOK / "build" / "export" / "cover.jpg",
    REPO / "covers" / "the-loneliest.jpg",
]

W, H = 1800, 2700
SEED = 1997  # matric year-ish; deterministic

# ── Newsprint palette ─────────────────────────────────────────────────────────────────────────
INK        = (24, 22, 20)       # press black (warm, not pure)
INK_SOFT   = (54, 50, 46)
NEWS_PAPER = (231, 224, 208)    # aged newsprint cream
NEWS_PAPER2= (221, 212, 193)    # a hair darker (toning)
GOLD       = (176, 122, 60)     # Veld Ochre — the blazer-gold / the one house accent
GOLD_DEEP  = (138, 95, 44)
BADGER_BLK = (22, 21, 19)

# ── Faces (period-honest: Times is the newspaper face) ──────────────────────────────────────────
F_HEAD   = "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"
F_HEAD_I = "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf"
F_BODY   = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"
F_KICK   = "/System/Library/Fonts/Supplemental/Arial Narrow Bold.ttf"
F_DECK   = "/System/Library/Fonts/Supplemental/Futura.ttc"   # idx 4 cond xbold (the masthead rule)


def font(path: str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size, index=index)


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def find_source() -> Path:
    for p in SRC_CANDIDATES:
        if p.exists():
            return p
    raise SystemExit(
        "make_cover: source portrait not found. Expected the PRIVATE local working copy at "
        + " or ".join(str(p) for p in SRC_CANDIDATES)
        + "\n(This file is intentionally not in the repo. Restore the /tmp/photobatch working copy.)"
    )


def halftone(gray: Image.Image, cell: int = 14, angle: float = 15.0,
             dot_max: float = 1.32) -> Image.Image:
    """Classic AM dot-screen halftone of a grayscale image.

    For each cell on a rotated grid, sample the local average tone and draw a black dot whose
    radius grows as the tone darkens. `cell` large => coarse, plainly-visible dots ("enlarged
    newsprint"). Returns an 'L' image (black dots on white) at the SAME size as `gray`.
    """
    w, h = gray.size
    # supersample the canvas we draw dots onto, for crisp round dots, then downscale
    ss = 3
    out = Image.new("L", (w * ss, h * ss), 255)
    d = ImageDraw.Draw(out)
    px = gray.load()

    a = math.radians(angle)
    ca, sa = math.cos(a), math.sin(a)
    # iterate over a grid in the ROTATED frame so the dot lattice is angled (newsprint screen angle)
    diag = int(math.hypot(w, h)) + cell * 2
    rng = range(-diag, diag, cell)
    cx0, cy0 = w / 2, h / 2
    for gy in rng:
        for gx in rng:
            # rotate grid point back into image space
            ix = cx0 + (gx * ca - gy * sa)
            iy = cy0 + (gx * sa + gy * ca)
            xi, yi = int(ix), int(iy)
            if 0 <= xi < w and 0 <= yi < h:
                # local average over the cell (cheap: sample center + a few)
                tot, n = 0, 0
                for ddx in (-cell // 3, 0, cell // 3):
                    for ddy in (-cell // 3, 0, cell // 3):
                        sx, sy = xi + ddx, yi + ddy
                        if 0 <= sx < w and 0 <= sy < h:
                            tot += px[sx, sy]
                            n += 1
                avg = tot / max(1, n)
                darkness = 1.0 - avg / 255.0          # 0 (white) .. 1 (black)
                r = (cell * 0.5 * dot_max) * math.sqrt(max(0.0, darkness))
                if r > 0.4:
                    X, Y = ix * ss, iy * ss
                    rr = r * ss
                    d.ellipse([X - rr, Y - rr, X + rr, Y + rr], fill=0)
    out = out.resize((w, h), Image.LANCZOS)
    return out


def prepare_portrait() -> Image.Image:
    """Load the portrait, crop to a strong head+shoulders, tune contrast, return grayscale 'L'."""
    src = Image.open(find_source()).convert("RGB")
    sw, sh = src.size
    # The portrait is ~vertical; crop a touch off the top headroom and bias to the face.
    # Keep generous shoulders (the striped blazer is the point — it carries the gold).
    target_ar = 0.82  # w/h of the photo box
    # current ar:
    cur_ar = sw / sh
    if cur_ar > target_ar:
        new_w = int(sh * target_ar)
        x0 = (sw - new_w) // 2
        src = src.crop((x0, 0, x0 + new_w, sh))
    else:
        new_h = int(sw / target_ar)
        # bias crop upward (keep the face, lose some chest)
        y0 = int((sh - new_h) * 0.30)
        y0 = max(0, min(y0, sh - new_h))
        src = src.crop((0, y0, sw, y0 + new_h))

    g = ImageOps.grayscale(src)
    g = ImageOps.autocontrast(g, cutoff=1)
    # Lift shadows so the hair/blazer don't crush to a solid black blob and the EYES hold the frame
    # (the 'direct gaze' is the focal point). Gentle gamma > 1 brightens mids/darks.
    lut = [min(255, int(255 * ((v / 255.0) ** 0.72))) for v in range(256)]
    g = g.point(lut)
    g = ImageEnhance.Contrast(g).enhance(1.06)
    g = ImageEnhance.Brightness(g).enhance(1.10)

    # FACE HALO: a soft radial lift centred where the face sits (upper-centre), so the head/eyes
    # separate from the dark blazer + background — like a newspaper photo exposed for the face.
    w, h = g.size
    halo = Image.new("L", (w, h), 0)
    hd = ImageDraw.Draw(halo)
    fx, fy = int(w * 0.50), int(h * 0.36)        # face centre in this crop
    rad = int(w * 0.46)
    hd.ellipse([fx - rad, fy - int(rad * 1.15), fx + rad, fy + int(rad * 1.05)], fill=255)
    halo = halo.filter(ImageFilter.GaussianBlur(int(w * 0.16)))
    # screen the halo in: brightens under the halo, leaves edges (blazer corners) darker
    bright = g.point(lambda v: min(255, int(v + 46)))
    g = Image.composite(bright, g, halo)
    return g


def paper_bg() -> Image.Image:
    """Aged newsprint stock: warm cream with faint grain, fibre flecks, and edge toning."""
    rnd = random.Random(SEED)
    img = Image.new("RGB", (W, H), NEWS_PAPER)
    d = ImageDraw.Draw(img)
    # subtle vertical tone shift (top a touch lighter)
    for y in range(H):
        t = y / H
        col = lerp(NEWS_PAPER, NEWS_PAPER2, 0.35 * t)
        d.line([(0, y), (W, y)], fill=col)
    # paper grain
    grain = Image.new("L", (W, H), 0)
    gp = grain.load()
    for _ in range(60000):
        x = rnd.randint(0, W - 1); y = rnd.randint(0, H - 1)
        gp[x, y] = rnd.randint(0, 38)
    img = Image.composite(Image.new("RGB", (W, H), INK), img,
                          grain.point(lambda v: int(v * 0.10)))
    # a few fibre flecks
    d = ImageDraw.Draw(img)
    for _ in range(120):
        x = rnd.randint(0, W); y = rnd.randint(0, H)
        d.line([(x, y), (x + rnd.randint(-3, 3), y + rnd.randint(-2, 2))],
               fill=lerp(NEWS_PAPER2, INK, 0.18), width=1)
    # edge toning / foxing (older at the edges)
    edge = Image.new("L", (W, H), 0)
    ed = ImageDraw.Draw(edge)
    ed.rectangle([0, 0, W, H], outline=255, width=140)
    edge = edge.filter(ImageFilter.GaussianBlur(120))
    img = Image.composite(Image.new("RGB", (W, H), lerp(NEWS_PAPER2, GOLD_DEEP, 0.10)), img,
                          edge.point(lambda v: int(v * 0.45)))
    return img


def ink_print(base: Image.Image, mask_L: Image.Image, ink=INK, jitter=2) -> Image.Image:
    """Composite a black-dots 'L' mask onto the paper as INK, with tiny mis-registration + a faint
    second-impression ghost (the look of real press printing)."""
    # mask_L: 0=ink dot, 255=paper. Ink where dark.
    rnd = random.Random(SEED + 5)
    ink_alpha = mask_L.point(lambda v: 255 - v)   # 255 where dot
    # INK BLEED: a hair of blur so dots gain/spread like wet ink on absorbent newsprint.
    ink_alpha = ink_alpha.filter(ImageFilter.GaussianBlur(0.8))
    ink_alpha = ink_alpha.point(lambda v: min(255, int(v * 1.12)))   # dot gain
    # INK SPECKLE: knock random pinholes out of the ink (paper showing through) + add stray
    # specks in the paper — that gritty, uneven press-ink texture (kills the 'digital mosaic' look).
    noise = Image.new("L", base.size, 0)
    npx = noise.load()
    area = base.size[0] * base.size[1]
    for _ in range(area // 60):
        x = rnd.randint(0, base.size[0] - 1); y = rnd.randint(0, base.size[1] - 1)
        npx[x, y] = rnd.randint(60, 255)
    pinholes = noise.point(lambda v: 255 if v > 180 else 0)
    ink_alpha = Image.composite(Image.new("L", base.size, 0), ink_alpha, pinholes)  # punch holes
    specks = noise.point(lambda v: 90 if 70 < v < 120 else 0)
    ink_alpha = ImageChops.lighter(ink_alpha, specks)                               # add stray ink

    layer = Image.new("RGB", base.size, ink)
    out = Image.composite(layer, base, ink_alpha)
    # faint offset ghost (second impression / mis-registration)
    gx, gy = rnd.randint(-jitter, jitter), rnd.randint(-jitter, jitter)
    ghost = ink_alpha.point(lambda v: int(v * 0.16))
    glayer = Image.new("RGB", base.size, lerp(ink, NEWS_PAPER, 0.35))
    shifted = Image.new("L", base.size, 0)
    shifted.paste(ghost, (gx + 2, gy + 1))
    out = Image.composite(glayer, out, shifted)
    return out


def tracked(draw, xy, text, fnt, fill, tracking=0, center_w=False):
    widths = [draw.textbbox((0, 0), ch, font=fnt)[2] for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = xy[0] - total // 2 if center_w else xy[0]
    y = xy[1]
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def build() -> Image.Image:
    img = paper_bg()

    # ── Masthead rule + kicker (the "newspaper" frame) ──────────────────────────────────────────
    d = ImageDraw.Draw(img)
    M = 130                      # outer margin
    top = 150
    # top hairline + a fat rule (masthead)
    d.line([(M, top), (W - M, top)], fill=INK, width=2)
    d.line([(M, top + 14), (W - M, top + 14)], fill=INK, width=6)
    # kicker line (left) + a date-style stamp (right) — newspaper furniture
    fk = font(F_KICK, 40)
    d.text((M, top + 34), "THE FILE  —  A STANDALONE NOVELLA", font=fk, fill=INK)
    fk2 = font(F_KICK, 34)
    stamp = "VOL. I  ·  NO. 1"
    d.text((W - M - d.textlength(stamp, font=fk2), top + 38), stamp, font=fk2, fill=INK_SOFT)
    # the one gold rule (house accent / blazer gold)
    d.line([(M, top + 92), (W - M, top + 92)], fill=GOLD, width=3)

    # ── The HEADLINE = the title (newspaper serif, big, black) ──────────────────────────────────
    head_top = top + 130
    fh = font(F_HEAD, 150)
    head_lines = ["The Loneliest", "People in", "the World"]
    # tighten if any line overflows
    while any(d.textlength(ln, font=fh) > (W - 2 * M) for ln in head_lines) and fh.size > 90:
        fh = font(F_HEAD, fh.size - 6)
    lh = int(fh.size * 1.02)
    hy = head_top
    for ln in head_lines:
        d.text((M, hy), ln, font=fh, fill=INK)
        hy += lh
    # subhead / deck (newspaper "deck" under the headline)
    fdeck = font(F_HEAD_I, 50)
    deck = "An intelligence dossier, assembled from one boy's school record."
    for ln in wrap(d, deck, fdeck, W - 2 * M):
        d.text((M, hy + 14), ln, font=fdeck, fill=INK_SOFT)
        hy += int(fdeck.size * 1.12)
    hy += 18
    d.line([(M, hy), (W - M, hy)], fill=INK, width=1)

    # ── The PHOTO (blown-up halftone of the real portrait), in a ruled column box ───────────────
    photo_top = hy + 30
    box_w = W - 2 * M                 # full column width — the dominant lead photo
    box_h = int(box_w / 0.82)
    # cap so the caption + byline still fit, but let it run BIG (front-page lead)
    max_box_h = int(H * 0.485)
    if box_h > max_box_h:
        box_h = max_box_h
        box_w = int(box_h * 0.82)
    box_x = (W - box_w) // 2
    box = (box_x, photo_top, box_x + box_w, photo_top + box_h)

    g = prepare_portrait().resize((box_w, box_h), Image.LANCZOS)
    # COARSE cell => plainly visible dots (the "enlarged newsprint" the brief asked for).
    # Bigger photo + bigger dots = the right gritty scale.
    cell = max(15, int(box_w / 38))
    ht = halftone(g, cell=cell, angle=15.0, dot_max=1.38)

    # print the halftone onto a paper-coloured tile, then paste into the box
    tile = Image.new("RGB", (box_w, box_h), NEWS_PAPER)
    tile = ink_print(tile, ht, ink=INK, jitter=2)
    img.paste(tile, (box_x, photo_top))
    # ruled photo box
    d = ImageDraw.Draw(img)
    d.rectangle([box[0] - 4, box[1] - 4, box[2] + 3, box[3] + 3], outline=INK, width=2)

    # caption strip under the photo (newspaper cutline)
    cap_y = box[3] + 14
    d.line([(box[0] - 4, cap_y), (box[2] + 3, cap_y)], fill=INK, width=1)
    fcap_b = font(F_HEAD, 34)
    fcap = font(F_HEAD_I, 34)
    label = "THE SUBJECT.  "
    d.text((box[0] - 4, cap_y + 12), label, font=fcap_b, fill=INK)
    lab_w = d.textlength(label, font=fcap_b)
    cutline = "Photographed in school uniform, final year. Name withheld."
    # wrap the italic cutline after the bold label
    avail = (box[2] + 3) - (box[0] - 4 + lab_w)
    first = cutline
    while d.textlength(first, font=fcap) > avail and " " in first:
        first = first.rsplit(" ", 1)[0]
    d.text((box[0] - 4 + lab_w, cap_y + 12), first, font=fcap, fill=INK_SOFT)
    rest = cutline[len(first):].strip()
    if rest:
        d.text((box[0] - 4, cap_y + 12 + int(fcap.size * 1.15)), rest, font=fcap, fill=INK_SOFT)

    # ── Byline / credit + Press lockup at the foot (newspaper credit idiom) ──────────────────────
    foot = H - 150
    d.line([(M, foot - 96), (W - M, foot - 96)], fill=INK, width=1)
    d.line([(M, foot - 90), (W - M, foot - 90)], fill=GOLD, width=2)
    fby = font(F_HEAD, 54)
    by = "Andries J. Greyling"
    d.text((W // 2, foot - 44), by, font=fby, fill=INK, anchor="mm")
    fpress = font(F_KICK, 32)
    tracked(d, (W // 2, foot + 2), "ARJUNA BADGER PRESS", fpress, INK_SOFT,
            tracking=8, center_w=True)
    return img


def main() -> None:
    img = build()
    for p in OUT_PATHS:
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.suffix.lower() == ".jpg":
            img.save(p, "JPEG", quality=92)
        else:
            img.save(p, "PNG")
        print(f"wrote {p}")


if __name__ == "__main__":
    main()
