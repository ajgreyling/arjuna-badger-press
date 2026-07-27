#!/usr/bin/env python3
"""THE SURGEON — cover plate + typography.

Renders the concept in canon/COVER.md: dark Cape Winelands vine-rows curling into a
single golden-ratio spiral, tightening to a centre that glints with cold steel light,
under a black mountain wall and a bruised near-night sky.

Geometry, not photography — the spiral is a true logarithmic spiral (r = a·e^(bθ),
b = ln(φ)/(π/2)) laid into the ground plane by perspective transform, so the cover
is literally the mathematics the book is about.

Output: design/cover.png  (1800x2700, 6x9in @ 300dpi)
"""
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1800, 2700
PHI = (1 + 5 ** 0.5) / 2
GOLD = (201, 162, 39)          # #C9A227 harvest / surgical-lamp gold
SUPER = 2                       # supersample factor for the spiral field

FONT_DIR = Path("/usr/share/fonts/truetype/liberation")
SERIF = FONT_DIR / "LiberationSerif-Regular.ttf"
SERIF_B = FONT_DIR / "LiberationSerif-Bold.ttf"
SERIF_I = FONT_DIR / "LiberationSerif-Italic.ttf"
SANS = FONT_DIR / "LiberationSans-Regular.ttf"


# ----------------------------------------------------------------------------- sky
def sky() -> Image.Image:
    """Bruised near-night: deep indigo aloft, a cold bled horizon."""
    top = np.array([9, 11, 20], dtype=float)
    mid = np.array([22, 26, 38], dtype=float)
    horizon = np.array([58, 52, 54], dtype=float)
    y = np.linspace(0, 1, H)[:, None]
    # two-stage ramp so the horizon glow stays low and restrained
    t1 = np.clip(y / 0.62, 0, 1) ** 1.25
    t2 = np.clip((y - 0.62) / 0.38, 0, 1) ** 2.2
    band = top + (mid - top) * t1
    band = band + (horizon - band) * t2
    img = np.repeat(band[:, None, :], W, axis=1)

    # faint cold light pooling behind the peaks, slightly right of centre
    xx = np.linspace(0, 1, W)[None, :]
    yy = np.linspace(0, 1, H)[:, None]
    glow = np.exp(-(((xx - 0.60) ** 2) / 0.055 + ((yy - 0.60) ** 2) / 0.012))
    img += glow[:, :, None] * np.array([34, 30, 26])
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))


# -------------------------------------------------------------------- spiral field
def spiral_field() -> Image.Image:
    """Top-down vineyard: many parallel logarithmic-spiral rows about one eye.

    Growth is the true golden rate (b = ln(phi)/(pi/2)) slackened by GROW so the arms
    read as plantable furrows rather than a nautilus; the leading coefficient is then
    solved so the outermost turn exactly fills the field.
    """
    S = 1600 * SUPER
    field = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(field)
    cx = cy = S / 2
    half = S / 2

    b = math.log(PHI) / (math.pi / 2)
    GROW = 1.00          # true golden growth: r multiplies by phi every quarter-turn
    rows = 14
    turns = 1.95
    th_max = turns * 2 * math.pi
    th_min = -1.2 * math.pi
    a = (half * 0.99) / math.exp(b * GROW * th_max)   # fill the field exactly

    for i in range(rows):
        phase = (2 * math.pi / rows) * i
        pts = []
        th = th_min
        while th < th_max:
            r = a * math.exp(b * GROW * th)
            x = cx + r * math.cos(th + phase)
            y = cy + r * math.sin(th + phase)
            pts.append((x, y))
            th += 0.010 if r < half * 0.20 else 0.0035
        # draw in chunks so weight and brightness can grow with radius
        for seg in range(0, len(pts) - 1, 5):
            chunk = pts[seg:seg + 6]
            if len(chunk) < 2:
                continue
            rr = min(1.0, math.hypot(chunk[0][0] - cx, chunk[0][1] - cy) / half)
            wdt = max(1, int((0.9 + 7.0 * rr) * SUPER))
            val = int(min(255, 90 + 165 * rr ** 0.75))
            d.line(chunk, fill=val, width=wdt)

    field = field.resize((1600, 1600), Image.LANCZOS)
    return field.filter(ImageFilter.GaussianBlur(0.7))


def perspective_coeffs(src, dst):
    """PIL wants the inverse map: coefficients taking dst -> src."""
    A, B = [], []
    for (xd, yd), (xs, ys) in zip(dst, src):
        A.append([xd, yd, 1, 0, 0, 0, -xs * xd, -xs * yd])
        B.append(xs)
        A.append([0, 0, 0, xd, yd, 1, -ys * xd, -ys * yd])
        B.append(ys)
    res = np.linalg.solve(np.array(A, dtype=float), np.array(B, dtype=float))
    return tuple(res)


def ground(field: Image.Image) -> Image.Image:
    """Lay the spiral into the ground plane, receding to the mountain foot."""
    HORIZON = int(H * 0.545)
    plane_h = H - HORIZON
    src = [(0, 0), (1600, 0), (1600, 1600), (0, 1600)]
    # far edge pinched hard, near edge overflowing the trim = depth
    dst = [(W * 0.335, 0), (W * 0.665, 0), (W * 1.72, plane_h), (-W * 0.72, plane_h)]
    coeffs = perspective_coeffs(src, dst)
    warped = field.transform((W, plane_h), Image.PERSPECTIVE, coeffs,
                             Image.BICUBIC, fillcolor=0)
    out = Image.new("L", (W, H), 0)
    out.paste(warped, (0, HORIZON))
    return out


# ------------------------------------------------------------------------ mountains
def mountains(draw: ImageDraw.ImageDraw, horizon: int):
    """Two black ridgelines — the Simonsberg wall behind the valley."""
    rng = np.random.default_rng(11)

    def ridge(base, amp, colour, seed_scale, jag):
        xs = np.arange(0, W + 1, 6)
        prof = np.zeros_like(xs, dtype=float)
        for k, amp_k in enumerate([1.0, 0.62, 0.34, 0.19, 0.11, 0.06]):
            f = seed_scale * (k + 1)
            ph = rng.uniform(0, 2 * math.pi)
            prof += amp_k * np.sin(xs / W * f * 2 * math.pi + ph)
        prof += jag * rng.normal(0, 0.10, size=xs.shape).cumsum() / len(xs) * 9
        prof = prof / (np.abs(prof).max() + 1e-6)
        pts = [(int(x), int(base - amp * p)) for x, p in zip(xs, prof)]
        draw.polygon(pts + [(W, H), (0, H)], fill=colour)

    ridge(horizon - 34, 128, (14, 16, 22), 1.7, 0.5)   # far ridge, slightly lifted
    ridge(horizon + 4, 92, (5, 6, 9), 2.6, 0.9)        # near ridge, true black


# ----------------------------------------------------------------------------- main
def build() -> Image.Image:
    HORIZON = int(H * 0.545)
    img = sky()
    d = ImageDraw.Draw(img)
    mountains(d, HORIZON)

    mask = ground(spiral_field())
    arr = np.asarray(mask, dtype=float) / 255.0

    # depth fade: rows dissolve into haze toward the horizon
    yy = np.linspace(0, 1, H)[:, None]
    depth = np.clip((yy - HORIZON / H) / (1 - HORIZON / H), 0, 1)
    arr *= (0.05 + 0.95 * depth ** 0.48)

    base = np.asarray(img, dtype=float)

    # the vine rows themselves: cold green-black earth, warming to gold outward
    xx = np.linspace(-1, 1, W)[None, :]
    radial = np.clip(1.0 - np.sqrt(xx ** 2 + ((yy - 0.80) * 1.5) ** 2), 0, 1)
    vine = np.stack([
        26 + 104 * radial,
        34 + 96 * radial,
        28 + 66 * radial,
    ], axis=-1)
    base = base * (1 - arr[:, :, None]) + vine * arr[:, :, None]

    # the single gold thread: the spiral read at the tightening centre
    gx, gy = 0.5, HORIZON / H + 0.055
    core = np.exp(-(((np.linspace(0, 1, W)[None, :] - gx) ** 2) / 0.0021
                    + ((yy - gy) ** 2) / 0.00042))
    base += (arr * core * 1.55)[:, :, None] * np.array(GOLD)
    # a wider, dimmer bloom so the centre reads as lit, not pasted
    bloom = np.exp(-(((np.linspace(0, 1, W)[None, :] - gx) ** 2) / 0.020
                     + ((yy - gy) ** 2) / 0.0026))
    base += bloom[:, :, None] * np.array([46, 36, 13]) * 0.80

    # the cold steel glint: one thin line at the innermost curve
    steel = np.exp(-(((np.linspace(0, 1, W)[None, :] - gx) ** 2) / 0.00028
                     + ((yy - gy) ** 2) / 0.000055))
    base += steel[:, :, None] * np.array([150, 168, 186])

    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))

    # atmosphere: low haze along the valley floor
    haze = Image.new("L", (W, H), 0)
    hd = ImageDraw.Draw(haze)
    hd.rectangle([0, HORIZON - 10, W, HORIZON + 150], fill=54)
    haze = haze.filter(ImageFilter.GaussianBlur(60))
    img = Image.composite(Image.new("RGB", (W, H), (40, 44, 52)), img, haze)

    # vignette + film grain
    vig = np.clip(1.06 - 0.50 * np.sqrt(
        (np.linspace(-1, 1, W)[None, :] ** 2) * 0.72
        + (np.linspace(-1.05, 1.05, H)[:, None] ** 2) * 0.92), 0.30, 1.0)
    a = np.asarray(img, dtype=float) * vig[:, :, None]
    rng = np.random.default_rng(7)
    a += rng.normal(0, 3.1, a.shape)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def typeset(img: Image.Image) -> Image.Image:
    d = ImageDraw.Draw(img)

    def centre(txt, font, y, fill, track=0):
        widths = [d.textlength(c, font=font) for c in txt]
        total = sum(widths) + track * (len(txt) - 1)
        x = (W - total) / 2
        for c, cw in zip(txt, widths):
            d.text((x, y), c, font=font, fill=fill)
            x += cw + track

    f_eyebrow = ImageFont.truetype(str(SANS), 40)
    f_title = ImageFont.truetype(str(SERIF_B), 210)
    f_rule = ImageFont.truetype(str(SERIF), 44)
    f_tag = ImageFont.truetype(str(SERIF_I), 54)
    f_author = ImageFont.truetype(str(SANS), 52)

    centre("A CAPE TOWN THRILLER", f_eyebrow, 232, (188, 176, 158), track=11)
    centre("THE", f_title, 300, (238, 236, 232), track=8)
    centre("SURGEON", f_title, 500, (238, 236, 232), track=4)

    # thin gold rule under the title
    d.line([(W * 0.30, 762), (W * 0.70, 762)], fill=GOLD, width=3)
    centre("Perfection is irrational.", f_tag, 800, (206, 190, 154), track=2)

    centre("ANDRIES J. GREYLING", f_author, H - 232, (226, 222, 214), track=9)
    centre("ARJUNA BADGER PRESS", ImageFont.truetype(str(SANS), 30),
           H - 148, (150, 146, 140), track=7)
    return img


if __name__ == "__main__":
    cover = typeset(build())
    out = HERE / "cover.png"
    cover.save(out, "PNG", optimize=False, compress_level=3)
    print(f"wrote {out}  {cover.size}  {out.stat().st_size/1024:.0f} KB")
