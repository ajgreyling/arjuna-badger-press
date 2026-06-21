#!/usr/bin/env python3
"""Generate ABP brand sheets (dark + light) — Badger Bow mark, palette, type, web usage.

Writes:
  brand/assets/brand-sheet.png        — dark (default; matches arjunabadger.press)
  brand/assets/brand-sheet-light.png  — light (Cloud background)
  brand/brand-sheet.html              — browser reference (uses site fonts)

Run from repo:  python3 brand/build_brand_sheet.py
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
W, H = 1400, 2000

# Canonical palette — brand/tokens.css + site.css (--ochre link uses Veld Dust on web)
PALETTE = [
    ("Badger Black", "#161513", "Primary surface"),
    ("Iron Earth", "#3A332B", "Cards / raised"),
    ("Earth 700", "#2A241D", "Borders / lines"),
    ("Bone Stripe", "#EDE9E0", "Text on dark"),
    ("Bone Dim", "#BDB6A6", "Muted body"),
    ("Veld Ochre", "#B07A3C", "Accent / CTA fill"),
    ("Veld Dust", "#C8A86B", "Links / hover (site)"),
    ("Sting Red", "#C2401E", "Hot CTA / charge"),
    ("Dry Grass", "#7E7A5A", "Secondary / badges"),
    ("Cloud", "#F6F4EF", "Light mode bg"),
]

FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/Library/Fonts/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    paths = FONT_CANDIDATES if bold else [p.replace(" Bold", "") for p in FONT_CANDIDATES]
    if bold:
        paths = FONT_CANDIDATES
    for p in paths:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                continue
    return ImageFont.load_default()


def _hex(s: str) -> tuple[int, int, int]:
    s = s.lstrip("#")
    return tuple(int(s[i : i + 2], 16) for i in (0, 2, 4))


def _text_w(draw: ImageDraw.ImageDraw, text: str, font) -> int:
    return int(draw.textlength(text, font=font))


def _draw_header(draw, y, fg, muted, mark_img, dark: bool):
    f_title = _font(42, bold=True)
    f_sub = _font(22)
    f_meta = _font(16)
    mx, my = 72, y
    mark = mark_img.copy()
    mark.thumbnail((140, 140), Image.LANCZOS)
    return_y = y
    # mark pasted by caller
    draw.text((mx + 160, my + 8), "ARJUNA BADGER PRESS", fill=fg, font=f_title)
    draw.text((mx + 160, my + 58), "Your story, told true.", fill=_hex("#C8A86B") if dark else _hex("#B07A3C"), font=f_sub)
    draw.text((mx + 160, my + 92), "arjunabadger.press", fill=muted, font=f_meta)
    draw.text((mx + 160, my + 118), "Brand kit v3 · Badger Bow mark · " + date.today().isoformat(), fill=muted, font=f_meta)
    return return_y + 150


def _section_title(draw, y, title, fg):
    f = _font(20, bold=True)
    draw.rectangle([72, y + 10, 72 + 48, y + 13], fill=_hex("#EDE9E0"))
    draw.text((72, y + 22), title.upper(), fill=fg, font=f)
    return y + 58


def _draw_logos(base, draw, y, fg, muted, dark: bool):
    y = _section_title(draw, y, "Logo lockups", fg)
    items = [
        ("Mark / stamp — Badger Bow", "mark-only.png", "Nav · favicon · avatar · ≥24px"),
        ("Cover colophon — gold", "badger-bow-imprint.png", "Dark / busy cover corners"),
        ("Cover colophon — black", "badger-bow-stamp.png", "Light cover corners"),
        ("Full crest — dark", "logo-on-dark.png", "Hero · OG · default surface"),
        ("Full crest — light", "logo-on-light.png", "Print on Cloud / white"),
        ("Source crest (master)", "logo-master.png", "Archive source · hero export"),
    ]
    x0, thumb = 72, 200
    for i, (label, fname, note) in enumerate(items):
        col, row = i % 2, i // 2
        x = x0 + col * ((W - 144) // 2)
        yy = y + row * 280
        path = ASSETS / fname
        if path.exists():
            img = Image.open(path).convert("RGBA")
            img.thumbnail((thumb, thumb), Image.LANCZOS)
            tile = Image.new("RGBA", (thumb, thumb), (0, 0, 0, 0))
            ox = (thumb - img.width) // 2
            oy = (thumb - img.height) // 2
            tile.alpha_composite(img, (ox, oy))
            base.paste(tile, (x, yy), tile)
        f_l = _font(17, bold=True)
        f_n = _font(14)
        draw.text((x, yy + thumb + 10), label, fill=fg, font=f_l)
        draw.text((x, yy + thumb + 34), note, fill=muted, font=f_n)
        draw.text((x, yy + thumb + 56), fname, fill=muted, font=f_n)
    return y + 580


def _draw_palette(draw, y, fg, muted, dark: bool):
    y = _section_title(draw, y, "Colour", fg)
    sw, gap = 118, 14
    cols = 5
    for i, (name, hx, role) in enumerate(PALETTE):
        col, row = i % cols, i // cols
        x = 72 + col * (sw + gap)
        yy = y + row * 118
        rgb = _hex(hx)
        draw.rounded_rectangle([x, yy, x + sw, yy + 64], radius=8, fill=rgb,
                               outline=_hex("#2A241D") if dark else _hex("#E2DCD0"))
        text_c = _hex("#161513") if sum(rgb) > 380 else _hex("#EDE9E0")
        draw.text((x + 8, yy + 22), hx, fill=text_c, font=_font(13, bold=True))
        draw.text((x, yy + 72), name, fill=fg, font=_font(13, bold=True))
        draw.text((x, yy + 92), role, fill=muted, font=_font(12))
    return y + 260


def _draw_type(draw, y, fg, muted):
    y = _section_title(draw, y, "Typography (website)", fg)
    stacks = [
        ("Display / eyebrows", "Archivo Black · Saira Condensed · ALL CAPS + tracking", "WHY THIS HOUSE EXISTS"),
        ("Headings · nav · UI", "Space Grotesk — site nav, h1–h3, buttons", "Arjuna Badger Press"),
        ("Body", "Inter — paragraphs, UI copy", "A publishing house with the archer's eye and the badger's nerve."),
        ("Serif accent", "Cormorant Garamond — hero tagline, card titles", "Your story, told true."),
        ("Long-form / books", "Atkinson Hyperlegible — EPUB, PDF, read-online", "The believing register held because wonder, once you live inside it…"),
        ("Mono (optional)", "JetBrains Mono — tooling, code", "grep -i F2F transfer.log"),
    ]
    f_role = _font(14, bold=True)
    f_stack = _font(13)
    f_sample = _font(16)
    for i, (role, stack, sample) in enumerate(stacks):
        yy = y + i * 88
        draw.text((72, yy), role, fill=_hex("#C8A86B"), font=f_role)
        draw.text((72, yy + 22), stack, fill=muted, font=f_stack)
        draw.text((72, yy + 44), sample, fill=fg, font=f_sample)
    return y + len(stacks) * 88 + 20


def _draw_web(draw, y, fg, muted):
    y = _section_title(draw, y, "Web usage (arjunabadger.press)", fg)
    f = _font(15)
    lines = [
        "Nav lockup: mark-only.png · 40×40 · border-radius 50%",
        "Hero crest: logo-master.png · ~200px wide · ochre drop-shadow",
        "Surface: #161513 body · radial ochre glow (site.css hero)",
        "Links: #C8A86B default · #E5B567 hover · Sting #C2401E for hot nav",
        "Cards: #1d1a16 on #161513 · border #2A241D · hover accent per series",
        "Reading: Atkinson Hyperlegible in reader + EPUB gate (render_book.sh)",
        "Clear space (mark): ≥ cap-height padding · min mark 24px · full crest ≥160px wide",
        "Don't: cute badger · flatten gold · stretch · recolour · separate wordmark font",
    ]
    for i, line in enumerate(lines):
        draw.text((72, y + i * 28), "·  " + line, fill=fg if i < 6 else muted, font=f)
    return y + len(lines) * 28 + 24


def _draw_taglines(draw, y, fg, muted):
    y = _section_title(draw, y, "Voice", fg)
    tags = [
        "Your story, told true.  (primary)",
        "The archer's eye. The badger's nerve.",
        "Aim true. Dig in.",
        "Craft, with claws.",
        "Action, without attachment.",
    ]
    f = _font(17)
    for i, t in enumerate(tags):
        draw.text((72, y + i * 32), t, fill=fg if i == 0 else muted, font=f)
    return y + len(tags) * 32 + 40


def _render(dark: bool) -> Image.Image:
    bg = _hex("#161513") if dark else _hex("#F6F4EF")
    fg = _hex("#EDE9E0") if dark else _hex("#161513")
    muted = _hex("#BDB6A6") if dark else _hex("#5A5043")
    base = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(base)

    # subtle top glow (matches site hero)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    ochre = (200, 168, 107, 28 if dark else 18)
    gd.ellipse([W * 0.1, -H * 0.15, W * 0.9, H * 0.45], fill=ochre)
    base.paste(Image.alpha_composite(Image.new("RGBA", (W, H), (*bg, 255)), glow).convert("RGB"))

    draw = ImageDraw.Draw(base)
    mark_path = ASSETS / "mark-only.png"
    mark = Image.open(mark_path).convert("RGBA") if mark_path.exists() else None
    y = 56
    if mark:
        m = mark.copy()
        m.thumbnail((140, 140), Image.LANCZOS)
        base.paste(m, (72, y), m)
    y = _draw_header(draw, y, fg, muted, mark, dark)
    y = _draw_logos(base, draw, y, fg, muted, dark)
    y = _draw_palette(draw, y, fg, muted, dark)
    y = _draw_type(draw, y, fg, muted)
    y = _draw_web(draw, y, fg, muted)
    _draw_taglines(draw, y, fg, muted)

    draw.text((72, H - 48), "See brand/BRAND.md · brand/tokens.css · assets/site.css", fill=muted, font=_font(13))
    return base


def _write_html():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Arjuna Badger Press — Brand sheet</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Cormorant+Garamond:ital,wght@0,500;1,500&family=Inter:wght@400;600&family=Space+Grotesk:wght@500;600&display=swap" rel="stylesheet">
<style>
:root{--black:#161513;--bone:#EDE9E0;--bonedim:#BDB6A6;--ochre:#C8A86B;--gold:#E5B567;--line:#2A241D;--sting:#C2401E;--cloud:#F6F4EF;}
*{box-sizing:border-box}body{margin:0;background:var(--black);color:var(--bone);font-family:Inter,system-ui,sans-serif;line-height:1.5}
.wrap{max-width:1100px;margin:0 auto;padding:40px 28px 80px}
h1{font-family:"Space Grotesk";font-size:2rem;margin:0}
.tag{font-family:"Cormorant Garamond",serif;font-style:italic;font-size:1.35rem;color:var(--gold)}
.meta{color:var(--bonedim);font-size:.9rem;margin-top:.5rem}
header{display:flex;gap:28px;align-items:center;margin-bottom:48px}
header img{width:120px;height:120px;filter:drop-shadow(0 6px 24px rgba(229,181,103,.2))}
section{margin:40px 0}
.eyebrow{font-family:"Space Grotesk";text-transform:uppercase;letter-spacing:.2em;font-size:12px;color:var(--ochre);margin-bottom:8px}
.stripe{height:3px;width:48px;background:var(--bone);border-radius:2px;margin-bottom:12px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:20px}
.logo-card{background:#1d1a16;border:1px solid var(--line);border-radius:12px;padding:16px;text-align:center}
.logo-card img{max-height:160px;max-width:100%;object-fit:contain}
.logo-card h3{font-family:"Space Grotesk";font-size:14px;margin:12px 0 4px}
.logo-card p{font-size:12px;color:var(--bonedim);margin:0}
.swatches{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:12px}
.swatch{border-radius:8px;overflow:hidden;border:1px solid var(--line)}
.swatch .chip{height:56px;display:flex;align-items:center;justify-content:center;font-family:ui-monospace,monospace;font-size:12px;font-weight:600}
.swatch .lbl{padding:8px 10px;font-size:12px;background:#1d1a16}
.swatch .lbl strong{display:block;font-family:"Space Grotesk"}
.type-block{margin:16px 0;padding:16px;background:#1d1a16;border:1px solid var(--line);border-radius:10px}
.type-block .role{color:var(--ochre);font-family:"Space Grotesk";font-size:12px;text-transform:uppercase;letter-spacing:.12em}
.type-block .stack{font-size:13px;color:var(--bonedim)}
.type-block .sample{margin-top:8px;font-size:17px}
.t-display{font-family:"Space Grotesk";text-transform:uppercase;letter-spacing:.12em;font-weight:600}
.t-heading{font-family:"Space Grotesk";font-weight:600}
.t-body{font-family:Inter}
.t-serif{font-family:"Cormorant Garamond",serif;font-style:italic;color:var(--gold)}
.t-reading{font-family:"Atkinson Hyperlegible"}
.t-mono{font-family:ui-monospace,monospace;font-size:14px}
ul.web{color:var(--bonedim);padding-left:1.2em}
ul.web li{margin:.35em 0}
.light-sheet{background:var(--cloud);color:var(--black);padding:40px 28px;margin-top:60px;border-radius:16px;border:1px solid #E2DCD0}
.light-sheet .logo-card,.light-sheet .type-block,.light-sheet .swatch .lbl{background:#fff}
.png-links{margin-top:24px;font-size:14px}
.png-links a{color:var(--ochre)}
</style>
</head>
<body><div class="wrap">
<header>
<img src="assets/mark-only.png" alt="Badger Bow mark">
<div>
<h1>Arjuna Badger Press</h1>
<div class="tag">Your story, told true.</div>
<p class="meta">Brand sheet v3 · Badger Bow mark · arjunabadger.press · """ + date.today().isoformat() + """</p>
</div>
</header>

<section>
<div class="eyebrow">Logo lockups</div><div class="stripe"></div>
<div class="grid">
<div class="logo-card"><img src="assets/mark-only.png" alt=""><h3>Mark / stamp</h3><p>Nav · favicon · ≥24px</p></div>
<div class="logo-card"><img src="assets/badger-bow-imprint.png" alt=""><h3>Cover colophon — gold</h3><p>Dark corners</p></div>
<div class="logo-card"><img src="assets/badger-bow-stamp.png" alt=""><h3>Cover colophon — black</h3><p>Light corners</p></div>
<div class="logo-card"><img src="assets/logo-on-dark.png" alt=""><h3>Full crest — dark</h3><p>Hero · default surface</p></div>
<div class="logo-card"><img src="assets/logo-on-light.png" alt=""><h3>Full crest — light</h3><p>Print on Cloud</p></div>
<div class="logo-card"><img src="assets/logo-master.png" alt=""><h3>Source crest</h3><p>Master art · hero export</p></div>
</div>
</section>

<section>
<div class="eyebrow">Colour</div><div class="stripe"></div>
<div class="swatches">
""" + "\n".join(
        f'<div class="swatch"><div class="chip" style="background:{hx};color:{"#161513" if sum(_hex(hx))>380 else "#EDE9E0"}">{hx}</div><div class="lbl"><strong>{name}</strong>{role}</div></div>'
        for name, hx, role in PALETTE
    ) + """
</div>
</section>

<section>
<div class="eyebrow">Typography</div><div class="stripe"></div>
<div class="type-block"><div class="role">Display / eyebrows</div><div class="stack">Space Grotesk · ALL CAPS + tracking (site eyebrows)</div><div class="sample t-display">Why this house exists</div></div>
<div class="type-block"><div class="role">Headings · nav</div><div class="stack">Space Grotesk</div><div class="sample t-heading">Arjuna Badger Press</div></div>
<div class="type-block"><div class="role">Body</div><div class="stack">Inter</div><div class="sample t-body">A publishing house with the archer's eye and the badger's nerve.</div></div>
<div class="type-block"><div class="role">Serif accent</div><div class="stack">Cormorant Garamond</div><div class="sample t-serif">Your story, told true.</div></div>
<div class="type-block"><div class="role">Long-form</div><div class="stack">Atkinson Hyperlegible — EPUB / read-online</div><div class="sample t-reading">The believing register held because wonder, once you live inside it…</div></div>
</section>

<section>
<div class="eyebrow">Web usage</div><div class="stripe"></div>
<ul class="web">
<li>Nav: <code>mark-only.png</code> 40×40 circle</li>
<li>Hero: <code>logo-master.png</code> ~200px + ochre glow</li>
<li>Links #C8A86B · hover #E5B567 · hot nav #C2401E</li>
<li>See <code>site/public/assets/site.css</code> + <code>brand/tokens.css</code></li>
</ul>
<p class="png-links">PNG exports: <a href="assets/brand-sheet.png">brand-sheet.png</a> · <a href="assets/brand-sheet-light.png">brand-sheet-light.png</a></p>
</section>
</div></body></html>
"""
    (HERE / "brand-sheet.html").write_text(html)


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    dark = _render(True)
    light = _render(False)
    out_dark = ASSETS / "brand-sheet.png"
    out_light = ASSETS / "brand-sheet-light.png"
    dark.save(out_dark, optimize=True)
    light.save(out_light, optimize=True)
    _write_html()
    print(f"Wrote {out_dark} ({out_dark.stat().st_size // 1024} KB)")
    print(f"Wrote {out_light} ({out_light.stat().st_size // 1024} KB)")
    print(f"Wrote {HERE / 'brand-sheet.html'}")


if __name__ == "__main__":
    main()
