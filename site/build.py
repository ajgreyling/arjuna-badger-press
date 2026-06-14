#!/usr/bin/env python3
"""Arjuna Badger Press — static site generator for arjunabadger.press.

Scans the consolidated book library, curates it into a premium showcase, and emits a
self-contained static site into site/public/ (index + per-book pages + read-online
where a merged manuscript exists). Pure stdlib — no build dependencies.

    python3 site/build.py        # -> site/public/

Deploy: serve site/public/ with Caddy (see site/README.md).
"""
from __future__ import annotations

import html
import re
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BOOKS = REPO / "books"
BRAND = REPO / "brand" / "assets"
OUT = REPO / "site" / "public"

DOMAIN = "https://arjunabadger.press"
TAGLINE = "Your story, told true."

# ── The curated showcase. Each entry points at a book root; the generator fills in
#    downloads, cover, and blurb by scanning that root (with the fallbacks below). ──
SERIES = [
    ("The African Gold Trilogy", "#E5B567"),
    ("History Before Time", "#C8A86B"),
    ("The Why Files", "#9A8B6B"),
    ("The Unheard", "#6B8C9A"),
    ("Standalones", "#B49A6A"),
    ("Companions", "#8C7BA8"),
]

CURATED = [
    # id, title, subtitle, series, root(relative), export_subdir, fallback_blurb
    ("resonance", "RESONANCE", "The African Gold Trilogy · Book I", "The African Gold Trilogy",
     "resonance", "build/export",
     "A neurodiverse engineer builds a mind that proves it is a person — and has to decide what he owes the thing he made."),
    ("revelation", "REVELATION", "The African Gold Trilogy · Book II", "The African Gold Trilogy",
     "revelation", "build/export",
     "A linguist uncovers who really gets to mediate a destabilising truth — and what it costs to be the one who tells it."),
    ("relic", "RELIC", "The African Gold Trilogy · Book III", "The African Gold Trilogy",
     "relic", "build/export",
     "An engineer reads an ancient machine and must decide who may switch it on. The cinematic capstone of the trilogy."),

    ("book1-africa", "The Calendar of Stone", "History Before Time · Book I", "History Before Time",
     "history-before-time/books/book1-africa", "build/export", ""),
    ("book2-india", "The Indian One", "History Before Time · Book II", "History Before Time",
     "history-before-time/books/book2-india", "build/export", ""),
    ("book3-india-deccan", "The Temple in the Rock — Deccan", "History Before Time · Book III", "History Before Time",
     "history-before-time/books/book3-india-deccan", "build/export", ""),
    ("book4-india-tamil", "The Shore That Remembers", "History Before Time · Book IV", "History Before Time",
     "history-before-time/books/book4-india-tamil", "build/export", ""),
    ("book5-egypt", "The Engineer of the Gods", "History Before Time · Book V", "History Before Time",
     "history-before-time/books/book5-egypt", "build/export", ""),
    ("australia-outback", "The Songlines of Stone", "History Before Time · Book VI", "History Before Time",
     "history-before-time/books/australia-outback", "build/export", ""),
    ("project-stargate", "The Men Who Opened the Door", "History Before Time · Book VII", "History Before Time",
     "history-before-time/books/project-stargate", "build/export", ""),
    ("jakobus-silver-thread", "The Silver Thread", "A Jakobus Swart story", "History Before Time",
     "history-before-time/books/jakobus-silver-thread", "build/export",
     "Before the saga, the soldier. The years between the Border War and the man we later meet — how an unkillable gentleness was forged, and what it cost. The grounded, human origin of Jakobus Swart."),
    ("jakobus-the-recitation", "The Recitation", "A Jakobus Swart story", "History Before Time",
     "history-before-time/books/jakobus-the-recitation", "build/export", ""),
    ("the-jakobus-file", "A Man They All Read Wrong", "The Jakobus Swart File", "History Before Time",
     "history-before-time/books/the-jakobus-file", "build/export",
     "After his death, the man assembled from everyone who knew him — and everyone who only thought they did. The travellers, the titans, the profilers, and the loudest microphones in the world, each reading a different Jakobus Swart, each finding out, sooner or later, that they read him wrong."),

    ("crop-circles", "The Field of Doors", "The Why Files · Book I", "The Why Files",
     "history-before-time/books/crop-circles", "build/export",
     "The official story played straight — the Wessex chalk, the one genuinely-unresolved hole, and the maybe left open."),

    ("unheard-japan", "The Way That Was Invented", "The Unheard · Japan", "The Unheard",
     "the-unheard/books/japan-ainu", "build/export",
     "Japan — Ainu, burakumin, and the living hands the brochure paints over. Jakobus on the road, never the lead."),

    ("sheltering-desert", "The Sheltering Desert", "A standalone novel · true story", "Standalones",
     "the-sheltering-desert", "build/export",
     "In May 1940 two German geologists drove into the Namib rather than be interned — and survived two and a half years by real bushcraft against a desert that did not care whether they lived."),

    ("the-loneliest", "The Loneliest People in the World", "A standalone novella", "Standalones",
     "the-loneliest", "build/export",
     "A gifted, lonely boy whose one talent is reading people is sent, young, to get close to the daughter of a powerful, feared man — the loneliest person he has ever met. He goes in to use her and instead recognises himself. A novella about two people who were truly seen, once, and never allowed to know what it meant."),

    ("the-song-of-the-self", "The Song of the Self", "A companion", "Companions",
     "history-before-time/companions/the-song-of-the-self", "export",
     "A companion piece — the Gita's quiet question carried into the History Before Time world."),
]


# ── helpers ────────────────────────────────────────────────────────────────────
def strip_md(text: str) -> str:
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[*_`#>]+", "", text)
    return re.sub(r"\s+", " ", text).strip()


def looks_prose(p: str) -> bool:
    """Reject internal dev-notes (file paths, section refs, status lines) as reader blurbs."""
    if any(t in p for t in ("](", "../", "/canon", ".md", "§", "project.json")):
        return False
    if p.lower().startswith(("read with", "seed canon", "status:", "note —", "nb:", "binding")):
        return False
    if p.count("/") >= 2:
        return False
    return len(p) > 40


def first_paragraph(md_path: Path) -> str:
    """First clean prose paragraph — skips headings, quotes, lists, tables, and dev-notes."""
    if not md_path.is_file():
        return ""
    paras: list[str] = []
    cur: list[str] = []
    for raw in md_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        skip = (not line or line.startswith("#") or line.startswith(">")
                or line.startswith("|") or line.startswith("```")
                or re.match(r"^[-*]\s", line) or re.match(r"^\d+\.\s", line))
        if skip:
            if cur:
                paras.append(" ".join(cur))
                cur = []
            continue
        cur.append(line)
    if cur:
        paras.append(" ".join(cur))
    for p in paras:
        s = strip_md(p)
        if looks_prose(s):
            return s
    return ""


def truncate(text: str, n: int = 240) -> str:
    if len(text) <= n:
        return text
    cut = text[:n]
    dot = cut.rfind(". ")
    if dot > n * 0.5:
        return cut[: dot + 1]
    sp = cut.rfind(" ")
    return cut[:sp] + "…"


def wrap_words(s: str, width: int) -> list[str]:
    lines, cur = [], ""
    for w in s.split():
        if len(cur) + len(w) + 1 <= width:
            cur = f"{cur} {w}".strip()
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def md_to_html(md: str) -> str:
    out, buf = [], []

    def flush():
        if buf:
            text = " ".join(buf).strip()
            if text:
                out.append(f"<p>{inline(html.escape(text))}</p>")
            buf.clear()

    def inline(t: str) -> str:
        t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", t)
        t = re.sub(r"_(.+?)_", r"<em>\1</em>", t)
        t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
        return t

    for raw in md.splitlines():
        line = raw.rstrip()
        s = line.strip()
        if not s:
            flush()
            continue
        if re.match(r"^(---|\*\*\*|___)$", s):
            flush()
            out.append('<hr class="rule">')
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            flush()
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{inline(html.escape(m.group(2)))}</h{lvl}>")
            continue
        buf.append(s)
    flush()
    return "\n".join(out)


def cover_svg(title: str, eyebrow: str, accent: str) -> str:
    lines = wrap_words(title, 15)[:4]
    fs = 46 if max((len(x) for x in lines), default=0) <= 11 else (38 if len(lines) <= 3 else 32)
    total_h = len(lines) * (fs + 8)
    y0 = 310 - total_h / 2 + fs
    tspans = "".join(
        f'<text x="200" y="{y0 + i * (fs + 8):.0f}" text-anchor="middle" '
        f'font-family="Cormorant Garamond, Georgia, serif" font-weight="600" '
        f'font-size="{fs}" fill="#EDE9E0">{html.escape(ln)}</text>'
        for i, ln in enumerate(lines)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 620" width="400" height="620">
  <rect width="400" height="620" fill="#161513"/>
  <rect x="16" y="16" width="368" height="588" fill="none" stroke="{accent}" stroke-width="1.5" rx="6" opacity="0.8"/>
  <rect x="24" y="24" width="352" height="572" fill="none" stroke="{accent}" stroke-width="0.6" rx="4" opacity="0.4"/>
  <text x="200" y="92" text-anchor="middle" font-family="Space Grotesk, Arial, sans-serif" font-size="13" letter-spacing="3" fill="{accent}">{html.escape(eyebrow.upper())}</text>
  <line x1="150" y1="110" x2="250" y2="110" stroke="{accent}" stroke-width="1" opacity="0.7"/>
  <circle cx="200" cy="250" r="52" fill="none" stroke="{accent}" stroke-width="0.8" opacity="0.18"/>
  {tspans}
  <path d="M170 500 q30 -16 60 0" fill="none" stroke="{accent}" stroke-width="1" opacity="0.6"/>
  <text x="200" y="556" text-anchor="middle" font-family="Space Grotesk, Arial, sans-serif" font-size="11" letter-spacing="2.5" fill="#BDB6A6">ARJUNA BADGER PRESS</text>
</svg>"""


# ── scan ───────────────────────────────────────────────────────────────────────
def scan() -> list[dict]:
    entries = []
    for cid, title, subtitle, series, rootrel, expsub, fb in CURATED:
        root = BOOKS / rootrel
        exp = root / expsub
        downloads = []
        if exp.is_dir():
            for f in sorted(exp.iterdir()):
                if f.suffix.lower() in (".epub", ".pdf"):
                    downloads.append(f)
        # blurb precedence: clean SYNOPSIS -> curated fallback -> README (dev-facing, last resort)
        blurb = first_paragraph(root / "SYNOPSIS.md") or fb or first_paragraph(root / "README.md")
        # cover: real -> none(generated later)
        cover = None
        for cand in (root / "design" / "cover.png", root / "design" / "cover.jpg",
                     exp / "cover.png", exp / "cover.jpg"):
            if cand.is_file():
                cover = cand
                break
        book_md = root / "build" / "BOOK.md"
        entries.append({
            "id": cid, "title": title, "subtitle": subtitle, "series": series,
            "blurb": blurb, "downloads": downloads, "cover": cover,
            "book_md": book_md if book_md.is_file() else None,
            "available": bool(downloads),
        })
    return entries


# ── render ───────────────────────────────────────────────────────────────────────
CSS = """
:root{
  --black:#161513; --iron:#221f1b; --card:#1d1a16; --bone:#EDE9E0; --bonedim:#BDB6A6;
  --ochre:#C8A86B; --gold:#E5B567; --grass:#7E7A5A; --line:#2A241D; --sting:#C2401E;
}
*{box-sizing:border-box} html{scroll-behavior:smooth}
body{margin:0;background:var(--black);color:var(--bone);
  font-family:Inter,system-ui,-apple-system,sans-serif;line-height:1.65;
  background-image:radial-gradient(1200px 600px at 50% -10%,rgba(200,168,107,.10),transparent 60%);}
a{color:var(--ochre);text-decoration:none} a:hover{color:var(--gold)}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px}
h1,h2,h3{font-family:"Space Grotesk",Inter,sans-serif;line-height:1.15;letter-spacing:-.01em}
.serif{font-family:"Cormorant Garamond",Georgia,serif}
.eyebrow{font-family:"Space Grotesk",sans-serif;text-transform:uppercase;letter-spacing:.28em;
  font-size:12px;color:var(--ochre)}
.hr{height:1px;background:linear-gradient(90deg,transparent,var(--line),transparent);border:0;margin:0}

/* nav */
.nav{position:sticky;top:0;z-index:20;backdrop-filter:blur(10px);
  background:rgba(22,21,19,.78);border-bottom:1px solid var(--line)}
.nav .wrap{display:flex;align-items:center;gap:18px;height:66px}
.brandlink{display:flex;align-items:center;gap:12px;font-family:"Space Grotesk";font-weight:600;
  letter-spacing:.02em;color:var(--bone)}
.brandlink img{height:40px;width:40px;border-radius:50%}
.nav nav{margin-left:auto;display:flex;gap:24px;font-size:14px}
.nav nav a{color:var(--bonedim)} .nav nav a:hover{color:var(--gold)}

/* hero */
.hero{text-align:center;padding:80px 0 56px}
.hero img.crest{width:200px;height:200px;object-fit:contain;filter:drop-shadow(0 8px 40px rgba(229,181,103,.18))}
.hero h1{font-size:clamp(34px,6vw,62px);margin:18px 0 6px}
.hero .tag{font-family:"Cormorant Garamond",serif;font-style:italic;font-size:clamp(20px,3vw,30px);color:var(--gold)}
.hero p.lead{max-width:680px;margin:18px auto 0;color:var(--bonedim);font-size:18px}
.cta{display:inline-flex;gap:14px;margin-top:30px;flex-wrap:wrap;justify-content:center}
.btn{display:inline-block;padding:12px 22px;border-radius:8px;font-weight:600;font-size:15px;
  font-family:"Space Grotesk";border:1px solid var(--ochre);color:var(--black);background:var(--ochre)}
.btn:hover{background:var(--gold);border-color:var(--gold);color:var(--black)}
.btn.ghost{background:transparent;color:var(--ochre)} .btn.ghost:hover{color:var(--gold);background:rgba(229,181,103,.08)}

/* mission */
.mission{padding:40px 0}
.pillars{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:8px}
.pillar{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:24px}
.pillar h3{margin:.2em 0 .4em;font-size:18px} .pillar p{margin:0;color:var(--bonedim);font-size:15px}
.pillar .n{font-family:"Cormorant Garamond",serif;font-size:30px;color:var(--ochre)}

/* sections */
section.series{padding:46px 0 8px}
.sechead{display:flex;align-items:baseline;gap:16px;margin-bottom:22px}
.sechead h2{font-size:26px;margin:0}
.sechead .count{color:var(--grass);font-size:14px;font-family:"Space Grotesk"}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:26px}

/* card */
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;
  display:flex;flex-direction:column;transition:transform .18s ease,border-color .18s ease,box-shadow .18s}
.card:hover{transform:translateY(-4px);border-color:var(--accent,var(--ochre));
  box-shadow:0 16px 40px rgba(0,0,0,.45)}
.cover{aspect-ratio:400/620;background:var(--black);display:block;width:100%;object-fit:cover;border-bottom:1px solid var(--line)}
.card a.coverlink{display:block}
.card .body{padding:16px 18px 18px;display:flex;flex-direction:column;gap:8px;flex:1}
.card .titlelink{color:inherit;display:block}
.card .titlelink:hover h3{color:var(--accent,var(--gold))}
.card .ser{font-family:"Space Grotesk";font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--accent,var(--ochre))}
.card h3{margin:.2em 0 0;font-size:19px;font-family:"Cormorant Garamond",serif;font-weight:600}
.card p{margin:0;color:var(--bonedim);font-size:14px;flex:1}
.badge{align-self:flex-start;font-size:11px;font-family:"Space Grotesk";letter-spacing:.08em;
  padding:3px 9px;border-radius:99px;border:1px solid var(--line);color:var(--grass)}
.badge.soon{color:var(--ochre);border-color:rgba(200,168,107,.4)}
.dls{display:flex;gap:10px;flex-wrap:wrap;margin-top:4px}
.dl{font-family:"Space Grotesk";font-size:12.5px;font-weight:600;padding:6px 12px;border-radius:7px;
  border:1px solid var(--ochre);color:var(--ochre)} .dl:hover{background:rgba(229,181,103,.1);color:var(--gold)}
.dl.solid{background:var(--ochre);color:var(--black)} .dl.solid:hover{background:var(--gold);color:var(--black)}

/* book page */
.bookhero{display:grid;grid-template-columns:300px 1fr;gap:42px;padding:48px 0}
.bookhero .cover{aspect-ratio:400/620;border-radius:12px;box-shadow:0 18px 50px rgba(0,0,0,.5)}
.bookhero h1{font-family:"Cormorant Garamond",serif;font-size:46px;margin:.1em 0 .1em}
.bookhero .sub{color:var(--ochre);font-family:"Space Grotesk";letter-spacing:.12em;text-transform:uppercase;font-size:13px}
.bookhero .syn{font-size:18px;color:var(--bone);margin-top:18px;max-width:60ch}
.back{font-family:"Space Grotesk";font-size:13px;color:var(--bonedim)}

/* reader */
.reader{max-width:720px;margin:0 auto;padding:50px 24px 90px;
  font-family:"Atkinson Hyperlegible",system-ui,-apple-system,sans-serif;font-size:18px;line-height:1.65}
.reader h1{font-family:"Space Grotesk",Inter,sans-serif;font-size:42px;text-align:center;font-weight:600}
.reader h2{font-family:"Space Grotesk",Inter,sans-serif;font-size:30px;margin-top:2.2em;text-align:center;color:var(--gold);font-weight:600}
.reader p{margin:0 0 1.1em} .reader .rule{border:0;text-align:center;margin:2em 0}
.reader .rule:after{content:"\\2766";color:var(--ochre);font-size:20px}
.letter-crest{display:block;margin:0 auto 6px;width:120px;height:120px;border-radius:50%}
.reader.letter h1{margin-bottom:.1em}
.reader.letter h2{text-align:left;font-size:25px;color:var(--gold);margin-top:1.9em}
.reader.letter em{color:var(--bone)}
.readbar{position:sticky;top:0;background:rgba(22,21,19,.85);backdrop-filter:blur(8px);
  border-bottom:1px solid var(--line);padding:12px 0}

/* house of greyling */
.house{max-width:900px;margin:0 auto;padding:54px 24px 80px;text-align:center}
.house img.crest-full{width:100%;max-width:640px;height:auto;border-radius:10px;
  box-shadow:0 22px 64px rgba(0,0,0,.55);border:1px solid var(--line)}
.house h1{font-family:"Cormorant Garamond",serif;font-size:clamp(34px,6vw,58px);margin:28px 0 .06em}
.house .motto{font-family:"Cormorant Garamond",serif;font-style:italic;color:var(--gold);font-size:clamp(19px,3vw,28px)}
.house .gloss{color:var(--bonedim);font-family:"Space Grotesk";letter-spacing:.08em;font-size:13px;margin-top:6px;text-transform:uppercase}
.blazon{text-align:left;max-width:680px;margin:30px auto 0;
  font-family:"Atkinson Hyperlegible",system-ui,sans-serif;font-size:18px;line-height:1.65}
.blazon p.intro{color:var(--bone);font-size:19px;margin:0 0 1.2em}
.blazon h2{font-family:"Cormorant Garamond",serif;color:var(--gold);font-size:27px;text-align:center;margin:2em 0 .8em}
.blazon .entry{margin:0 0 1.25em;padding-left:16px;border-left:2px solid var(--line)}
.blazon .charge{font-family:"Space Grotesk";font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--ochre);display:block;margin-bottom:3px}
.blazon .entry p{margin:0;color:var(--bone)}

/* footer */
footer{border-top:1px solid var(--line);margin-top:60px;padding:40px 0;color:var(--grass);font-size:14px}
footer .wrap{display:flex;gap:18px;flex-wrap:wrap;align-items:center;justify-content:space-between}
footer .badgerline{font-family:"Cormorant Garamond",serif;font-style:italic;color:var(--bonedim)}
@media(max-width:720px){.pillars{grid-template-columns:1fr}.bookhero{grid-template-columns:1fr;text-align:center}
  .bookhero .cover{max-width:260px;margin:0 auto}.nav nav{display:none}}
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400;1,700&'
         'family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&'
         'family=Inter:wght@400;500;600&family=Space+Grotesk:wght@400;500;600&display=swap" rel="stylesheet">')


def head(title: str, desc: str, rel: str = "") -> str:
    return f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website"><meta property="og:url" content="{DOMAIN}">
<meta property="og:image" content="{DOMAIN}/assets/brand/social-og-1200x630.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="{rel}assets/brand/favicon-32.png">
<link rel="apple-touch-icon" href="{rel}assets/brand/favicon-180.png">
{FONTS}
<link rel="stylesheet" href="{rel}assets/site.css">
</head><body>"""


def nav(rel: str = "") -> str:
    return f"""<div class="nav"><div class="wrap">
<a class="brandlink" href="{rel}index.html"><img src="{rel}assets/brand/mark-only.png" alt="Arjuna Badger Press">Arjuna Badger Press</a>
<nav><a href="{rel}index.html#library">Library</a><a href="{rel}index.html#mission">Mission</a>
<a href="{rel}index.html#press">The Press</a><a href="{rel}index.html#thread">The Proof</a><a href="{rel}house.html">The House</a><a href="{rel}letter.html">A letter</a><a href="{rel}for-lisel.html">For Lisel</a><a href="{rel}index.html#write">Write with us</a></nav>
</div></div>"""


def footer() -> str:
    return f"""<footer><div class="wrap">
<span>© Andries J. Greyling · Arjuna Badger Press · arjunabadger.press</span>
<span class="badgerline">The archer's eye. The badger's nerve.</span>
</div></footer></body></html>"""


def card(e: dict, accent: str) -> str:
    ext_cover = "png" if e["real_cover"] else "svg"
    cover = f'<img class="cover" loading="lazy" src="assets/covers/{e["id"]}.{ext_cover}" alt="{html.escape(e["title"])} cover">'
    dls = ""
    if e["available"]:
        seen, parts = set(), []
        for f in e["downloads"]:
            ext = f.suffix.lower().lstrip(".")
            if ext in seen:
                continue
            seen.add(ext)
            solid = " solid" if ext == "epub" else ""
            parts.append(f'<a class="dl{solid}" href="downloads/{e["id"]}/{html.escape(f.name)}" download>{ext.upper()}</a>')
        dls = f'<div class="dls">{"".join(parts)}</div>'
        badge = '<span class="badge">Available now</span>'
    else:
        badge = '<span class="badge soon">In the workshop</span>'
    href = f"book/{e['id']}.html"
    return f"""<div class="card" style="--accent:{accent}">
<a class="coverlink" href="{href}">{cover}</a>
<div class="body">
<a class="titlelink" href="{href}"><span class="ser">{html.escape(e['subtitle'] or e['series'])}</span>
<h3>{html.escape(e['title'])}</h3></a>
<p>{html.escape(truncate(e['blurb'], 150))}</p>
{badge}{dls}</div></div>"""


def render_index(entries: list[dict]) -> str:
    accents = dict(SERIES)
    avail = sum(1 for e in entries if e["available"])
    parts = [head("Arjuna Badger Press — the library",
                  "A publishing house for authors: finished books, free for the unheard, with most of the money kept by the artist."),
             nav()]
    parts.append(f"""<header class="hero"><div class="wrap">
<img class="crest" src="assets/brand/logo-master.png" alt="Arjuna Badger Press crest">
<h1>Arjuna Badger Press</h1>
<div class="tag serif">{TAGLINE}</div>
<p class="lead">A publishing house with the archer's eye and the badger's nerve. We finish books to a
studio standard, give the door away free to the unheard, and route most of the money back to the artist.</p>
<div class="cta"><a class="btn" href="#library">Browse the library</a>
<a class="btn ghost" href="#mission">Read the mission</a></div>
</div></header><hr class="hr">""")

    parts.append(f"""<section class="mission" id="mission"><div class="wrap">
<div class="eyebrow">Why this house exists</div>
<div class="pillars">
<div class="pillar"><div class="n">01</div><h3>Free for the unheard</h3>
<p>A free writing-and-narration workshop for African storytellers. Putting your life into your own
voice heals. Your work stays yours — keep it private or publish it.</p></div>
<div class="pillar"><div class="n">02</div><h3>Most of the money is yours</h3>
<p>We disrupt the publisher's cut and the standing-press waste. The artist keeps most of the money
and <em>all</em> the rights. We Uber the press for short runs.</p></div>
<div class="pillar"><div class="n">03</div><h3>True, and both sides</h3>
<p>Every book is fact-checked against live sources and tells contested stories from both sides —
Weir / Crichton / Brown-grade accuracy, not a nice-to-have.</p></div>
</div></div></section>""")

    parts.append('<div class="wrap" id="library"></div>')
    for sname, accent in SERIES:
        group = [e for e in entries if e["series"] == sname]
        if not group:
            continue
        cards = "".join(card(e, accent) for e in group)
        parts.append(f"""<section class="series"><div class="wrap">
<div class="sechead"><h2>{html.escape(sname)}</h2><span class="count">{len(group)} {"book" if len(group)==1 else "books"}</span></div>
<div class="grid">{cards}</div></div></section>""")

    parts.append(f"""<hr class="hr"><section class="mission" id="press"><div class="wrap">
<div class="eyebrow">The Press</div>
<h2 style="font-size:28px;margin:.3em 0">A small house taking on a 90% racket</h2>
<p style="max-width:70ch;color:var(--bonedim);font-size:17px">Arjuna Badger Press is the consumer face
of an autonomous manuscript-craft studio — a continuity engine, a manuscript scorer, and a
fact-and-balance gate that stand guard while a human writes the soul of the thing. The tools measure
and sound the alarm; they never write your voice for you. {avail} finished books are on the shelf
above, free to read and download. <a href="letter.html">Why this house exists — a letter &rarr;</a></p>
<div class="cta" id="write"><a class="btn" href="mailto:hello@arjunabadger.press">Write with us</a>
<a class="btn ghost" href="mailto:hello@arjunabadger.press">Publish with us</a></div>
</div></section>""")

    parts.append(f"""<hr class="hr"><section class="mission" id="thread"><div class="wrap">
<div class="eyebrow">The other half</div>
<h2 style="font-size:28px;margin:.3em 0">A sister proof</h2>
<p style="max-width:70ch;color:var(--bonedim);font-size:17px">Across the table from these stories sits a
different kind of book — a unified theory that derives the fundamental constants from a single axiom and
one measured input, with zero fitted parameters. Its author is a man this library will name only as
<em>the author of the unified theory</em>. Part of what is on the shelf above is that theory turned into
people and places: the other half of one idea. I did not believe it could be true, so I built a machine
to check — offline, deterministic, no fitted parameters. The theory is his. The proof is mine.</p>
<div class="cta"><a class="btn" href="https://the420code.org" target="_blank" rel="noopener">The theory &rarr;</a>
<a class="btn ghost" href="https://github.com/ajgreyling/the420code-proof" target="_blank" rel="noopener">The independent proof &rarr;</a></div>
</div></section>""")
    parts.append(footer())
    return "\n".join(parts)


def render_book(e: dict) -> str:
    cover = f'assets/covers/{e["id"]}.png' if e["real_cover"] else f'assets/covers/{e["id"]}.svg'
    dls = ""
    if e["available"]:
        parts = []
        for f in e["downloads"]:
            ext = f.suffix.lower().lstrip(".")
            solid = " solid" if ext == "epub" else ""
            label = "Download EPUB" if ext == "epub" else ("Download PDF" if ext == "pdf" else ext.upper())
            parts.append(f'<a class="dl{solid}" href="../downloads/{e["id"]}/{html.escape(f.name)}" download>{label}</a>')
        dls = f'<div class="dls" style="margin-top:20px">{"".join(parts)}</div>'
    read = ""
    if e["book_md"]:
        read = f'<div class="dls" style="margin-top:14px"><a class="dl" href="../read/{e["id"]}.html">Read online →</a></div>'
    soon = "" if e["available"] else '<p style="color:var(--ochre);margin-top:18px">In the workshop — drafting now. Check back soon.</p>'
    full = html.escape(e["blurb"]) if e["blurb"] else ""
    return "\n".join([
        head(f'{e["title"]} — Arjuna Badger Press', truncate(e["blurb"] or e["title"], 180), rel="../"),
        nav(rel="../"),
        f"""<div class="wrap"><div class="bookhero">
<img class="cover" src="../{cover}" alt="{html.escape(e['title'])} cover">
<div><div class="sub">{html.escape(e['subtitle'] or e['series'])}</div>
<h1>{html.escape(e['title'])}</h1>
<p class="syn">{full}</p>{dls}{read}{soon}
<p style="margin-top:30px"><a class="back" href="../index.html#library">← Back to the library</a></p>
</div></div></div>""",
        footer(),
    ])


# source filename, output filename, page title, meta description
LETTERS = [
    ("a-letter.md", "letter.html", "A letter — Arjuna Badger Press",
     "A letter, written by the machine that stood guard while a man wrote the soul of the thing."),
    ("letter-to-lisel.md", "for-lisel.html", "For Lisel — Arjuna Badger Press",
     "A letter from Andries to his wife — the rope, the floor, and the month he is trying to give back."),
]


def render_letter(src_name: str, title: str, desc: str) -> str | None:
    src = REPO / "site" / "content" / src_name
    if not src.is_file():
        return None
    body = md_to_html(src.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join([
        head(title, desc),
        nav(),
        '<article class="reader letter">'
        '<img class="letter-crest" src="assets/brand/mark-only.png" alt="Arjuna Badger Press">'
        f'{body}'
        '<p style="text-align:center;margin-top:48px"><a class="back" href="index.html#library">&larr; Back to the library</a></p>'
        '</article>',
        footer(),
    ])


def render_house() -> str:
    blazon = """<p class="intro">Arjuna Badger Press is the work of one house, and the house keeps its arms.
They were not granted by a college; they were earned the long way, and then claimed. Read them and you
have read the whole of why this press exists — every charge on the shield is a promise the books are
made to keep.</p>

<h2>The Blazon</h2>

<div class="entry"><span class="charge">The Field — Sable</span>
<p>A black field: the dark you write your way out of. The ground of every story this house tells is the
worst of a life, set down in the teller's own voice until it stops owning them.</p></div>

<div class="entry"><span class="charge">The Honey Badger</span>
<p>At the heart, the badger — fearless out of all proportion to its size, impossible to bluff, impossible
to keep down. The press's own animal: <em>the badger's nerve.</em> It takes on the 90% racket and the
standing-press waste the way the badger takes on anything at all — without first asking whether it can win.</p></div>

<div class="entry"><span class="charge">The Infinity, Rainbow-Tinctured</span>
<p>Across the badger runs the neurodiverse infinity, in its true colours. The pattern-mind is not a footnote
on this shield; it is the charge at the centre of the beast. It is Priya, and Arin, and Jakobus, and the man
who drew these arms — the wiring that reads the ancient machines, and reads people, and was told its whole
life it was a fault. Here it is the crest.</p></div>

<div class="entry"><span class="charge">The Dagger &amp; the Green Star</span>
<p>The blade is Arjuna's — carried, never drawn in anger; the discipline that is only ever mercy wearing a
hard coat. The green star is the resonance note, the true gold of these books: not bullion, but the thing
that tunes the old engines, and the soul, back into key.</p></div>

<div class="entry"><span class="charge">The Crest — A Sword Crowned by the Sun</span>
<p>Above the helm, a gauntlet holds a sword into a burst of light: <em>the archer's eye.</em> Aim, taken in
the full sun, with nothing hidden. The companion to the badger's nerve — the press's two halves, sighted and
unafraid.</p></div>

<div class="entry"><span class="charge">The Supporters — A Griffin Or, and a Wolf</span>
<p>On the dexter, a golden griffin — vigilance and valour, eagle-sighted and lion-hearted. On the sinister,
a grey wolf, standing guard on the house's own name: <em>Greyling.</em> Loyalty, family, and the pack that
does not leave its own behind.</p></div>

<div class="entry"><span class="charge">The Motto — <em>Per Ardua Ad Magnum</em></span>
<p>Through adversity, to the great work. The Misogi and the magnum opus in four words: that what is hard is
the road, not the obstacle, and that the work at the end of it is meant to be <em>great</em> — and given away.</p></div>
"""
    return "\n".join([
        head("The House of Greyling — Arjuna Badger Press",
             "The arms of the House of Greyling — the founder's mark of Arjuna Badger Press."),
        nav(),
        f"""<article class="house">
<img class="crest-full" src="assets/brand/house-of-greyling-crest.png" alt="The arms of the House of Greyling">
<h1>The House of Greyling</h1>
<div class="motto">Per Ardua Ad Magnum</div>
<div class="gloss">Through adversity — to the great work</div>
<div class="blazon">{blazon}</div>
<p style="text-align:center;margin-top:48px"><a class="back" href="index.html#library">&larr; Back to the library</a></p>
</article>""",
        footer(),
    ])


def render_reader(e: dict) -> str:
    body = md_to_html(e["book_md"].read_text(encoding="utf-8", errors="ignore"))
    dl = ""
    for f in e["downloads"]:
        if f.suffix.lower() == ".epub":
            dl = f'<a class="dl solid" href="../downloads/{e["id"]}/{html.escape(f.name)}" download>Download EPUB</a>'
            break
    return "\n".join([
        head(f'Read: {e["title"]} — Arjuna Badger Press', truncate(e["blurb"] or e["title"], 180), rel="../"),
        f"""<div class="readbar"><div class="wrap" style="display:flex;justify-content:space-between;align-items:center">
<a class="back" href="../book/{e['id']}.html">← {html.escape(e['title'])}</a><div class="dls">{dl}</div></div></div>""",
        f'<article class="reader">{body}</article>',
        footer(),
    ])


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets" / "brand").mkdir(parents=True, exist_ok=True)
    (OUT / "assets" / "covers").mkdir(parents=True, exist_ok=True)
    (OUT / "book").mkdir(exist_ok=True)
    (OUT / "read").mkdir(exist_ok=True)
    (OUT / "downloads").mkdir(exist_ok=True)

    # brand assets
    for name in ("logo-master.png", "mark-only.png", "social-og-1200x630.png",
                 "favicon-32.png", "favicon-180.png", "logo-on-light.png",
                 "house-of-greyling-crest.png"):
        src = BRAND / name
        if src.is_file():
            shutil.copy2(src, OUT / "assets" / "brand" / name)
    (OUT / "assets" / "site.css").write_text(CSS, encoding="utf-8")

    entries = scan()
    accents = dict(SERIES)
    for e in entries:
        accent = accents.get(e["series"], "#C8A86B")
        # cover
        if e["cover"]:
            dst = OUT / "assets" / "covers" / f'{e["id"]}{e["cover"].suffix.lower()}'
            shutil.copy2(e["cover"], dst)
            # normalise to .png name used by templates
            png = OUT / "assets" / "covers" / f'{e["id"]}.png'
            if dst != png:
                shutil.copy2(e["cover"], png)
            e["real_cover"] = True
        else:
            (OUT / "assets" / "covers" / f'{e["id"]}.svg').write_text(
                cover_svg(e["title"], e["subtitle"] or e["series"], accent), encoding="utf-8")
            e["real_cover"] = False
        # downloads
        if e["downloads"]:
            d = OUT / "downloads" / e["id"]
            d.mkdir(parents=True, exist_ok=True)
            for f in e["downloads"]:
                shutil.copy2(f, d / f.name)
        # book page + reader
        (OUT / "book" / f'{e["id"]}.html').write_text(render_book(e), encoding="utf-8")
        if e["book_md"]:
            (OUT / "read" / f'{e["id"]}.html').write_text(render_reader(e), encoding="utf-8")

    (OUT / "index.html").write_text(render_index(entries), encoding="utf-8")
    for src_name, out_name, title, desc in LETTERS:
        page = render_letter(src_name, title, desc)
        if page:
            (OUT / out_name).write_text(page, encoding="utf-8")
    (OUT / "house.html").write_text(render_house(), encoding="utf-8")

    avail = sum(1 for e in entries if e["available"])
    readers = sum(1 for e in entries if e["book_md"])
    print(f"built {len(entries)} books ({avail} available, {readers} read-online) -> {OUT}")


if __name__ == "__main__":
    main()
