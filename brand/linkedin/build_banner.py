#!/usr/bin/env python3
"""Compose the LinkedIn banner: SVG veld/typography scene + the real house crest PNG.

Renders the SVG at 2x via Inkscape, feathers the crest's warm-black background so it
sits seamlessly on the banner's matching black, composites it on the right, and writes
the exact 1584x396 LinkedIn cover plus a 2x master.
"""
import subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
BRAND = HERE.parent
ASSETS = BRAND / "assets"

W, H = 1584, 396
SCALE = 2                      # render at 2x for crisp text, downsample at the end
BG = (22, 21, 19)              # #161513 warm near-black, matches the crest ground

svg = HERE / "banner.svg"
scene_png = HERE / "_scene@2x.png"
out_2x = HERE / "linkedin-banner@2x.png"
out = HERE / "linkedin-banner.png"

# 1) Render the SVG scene at 2x
def render_scene():
    cmd = [
        "inkscape", str(svg),
        "--export-type=png",
        f"--export-filename={scene_png}",
        f"--export-width={W*SCALE}",
        f"--export-height={H*SCALE}",
        "--export-background=#161513",
        "--export-background-opacity=1",
    ]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    return Image.open(scene_png).convert("RGB")

# 2) Prepare the crest: tight-crop the art out of its padded square, then feather
#    its rectangular edge into transparency so it melts into the banner black.
def prepare_crest(target_h):
    crest = Image.open(ASSETS / "logo-on-dark.png").convert("RGB")
    # The crest art has even black padding; trim a little to reduce dead space.
    cw, ch = crest.size
    trim = int(cw * 0.04)
    crest = crest.crop((trim, trim, cw - trim, ch - trim))

    # Scale to target height
    cw, ch = crest.size
    scale = target_h / ch
    new = (int(cw * scale), target_h)
    crest = crest.resize(new, Image.LANCZOS)

    # Build a feathered alpha so edges fade into the banner (no hard rectangle seam).
    cw, ch = crest.size
    alpha = Image.new("L", (cw, ch), 0)
    d = ImageDraw.Draw(alpha)
    feather = int(min(cw, ch) * 0.10)
    d.rounded_rectangle([feather, feather, cw - feather, ch - feather],
                        radius=feather, fill=255)
    alpha = alpha.filter(ImageFilter.GaussianBlur(feather * 0.9))
    crest.putalpha(alpha)
    return crest

def main():
    if not svg.exists():
        sys.exit(f"missing {svg}")
    scene = render_scene()

    # Crest sized to ~92% of banner height, placed centre-right, fully in frame.
    crest_h = int(H * SCALE * 0.92)
    crest = prepare_crest(crest_h)
    cw, ch = crest.size
    # Centre of crest at x=1360 (matches the sun glow), vertically centred.
    cx = int(1360 * SCALE)
    cy = int(H * SCALE / 2)
    pos = (cx - cw // 2, cy - ch // 2)
    scene.paste(crest, pos, crest)

    # Save 2x master and the exact LinkedIn size.
    scene.save(out_2x)
    final = scene.resize((W, H), Image.LANCZOS)
    final.save(out, optimize=True)
    print(f"wrote {out} ({out.stat().st_size//1024} KB) and {out_2x.name}")

if __name__ == "__main__":
    main()
