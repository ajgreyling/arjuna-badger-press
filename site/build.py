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
import json
import os
import re
import shutil
import subprocess
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BOOKS = REPO / "books"
BRAND = REPO / "brand" / "assets"
OUT = REPO / "site" / "public"

DOMAIN = "https://arjunabadger.press"
PUBLIC_EMAIL = "info@arjunabadger.press"
TAGLINE = "Your story, told true."

# Safari annex — full Arjuna Badger Press wordmark (same asset as the main site logo).
SAFARI_LOGO = "logo-master.png"
SAFARI_BG_MANIFEST = REPO / "site" / "safari" / "backgrounds.json"

# ── Analytics (Plausible Cloud) ───────────────────────────────────────────────────────────────
# Privacy-first, no-cookie analytics. Set PLAUSIBLE_DOMAIN to the site domain registered in your
# plausible.io account (almost always "arjunabadger.press" — the bare host, no scheme). When set,
# head() emits the Plausible script with the file-downloads + outbound-links extension, which
# auto-tracks every EPUB/PDF download (links carry `download` + `class="dl"`) with NO per-link code.
# Leave empty to disable (no snippet emitted). Env var ABP_PLAUSIBLE_DOMAIN overrides.
PLAUSIBLE_DOMAIN = os.environ.get("ABP_PLAUSIBLE_DOMAIN", "arjunabadger.press")

# ── Search-console ownership verification ─────────────────────────────────────────────────────
# Google Search Console and Bing Webmaster Tools each offer a one-time HTML-meta proof of ownership.
# Paste ONLY the token (the `content="..."` value, not the whole tag) into the matching env var and
# rebuild; head() emits the meta on every page. Both consoles ALSO support DNS-TXT verification at
# your registrar, which needs no code at all — prefer that if you'd rather not redeploy. While these
# are empty no tag is emitted, so the site is unaffected until you actually have a token.
#   Google: Search Console → Settings → Ownership verification → "HTML tag" → copy the content value.
#   Bing:   Webmaster Tools → Add site → "HTML Meta Tag" option (or just "Import from GSC").
GOOGLE_SITE_VERIFY = os.environ.get("ABP_GOOGLE_VERIFY", "").strip()
BING_SITE_VERIFY = os.environ.get("ABP_BING_VERIFY", "").strip()

# ── The Honey Badger Bounty — GATED (opens 25 June 2026) ──────────────────────────────────────
# The bounty is NOT live yet. While BOUNTY_LIVE is False the site emits NO bounty surface at all:
# no /bounty or /finders pages, no nav "Bounty" link, no site-wide anti-scam trust banner. Flip it
# on for launch by setting env ABP_BOUNTY_LIVE=1 (or change the default here), then rebuild/deploy.
BOUNTY_LIVE = os.environ.get("ABP_BOUNTY_LIVE", "") not in ("", "0", "false", "no")

# Paste the Google Form URL here (or set env ABP_BOUNTY_FORM_URL) once it exists. While empty, the
# "Report a find" links fall back to the bounty page itself, so there is never a dead link.
BOUNTY_FORM_URL = os.environ.get("ABP_BOUNTY_FORM_URL", "")

# Official WhatsApp Channel (broadcast-only). Paste the channel invite URL (or set env
# ABP_WHATSAPP_CHANNEL_URL) once created. While empty, "Follow the channel" falls back to the
# bounty page (no dead link). WhatsApp is the announce megaphone; all reporting stays on the form.
WHATSAPP_CHANNEL_URL = os.environ.get("ABP_WHATSAPP_CHANNEL_URL", "")

# ── Reader feedback & ratings (static-site funnel; see docs/FEEDBACK_PLAN.md) ───────────────────
# A static site can't store submissions, so feedback resolves to a hosted form (responses land in a
# sheet the press reads) with a mailto: fallback so the channel works TODAY with zero setup.
# Private inbox the fallback targets directly:
PRIVATE_EMAIL = "j@arjunabadger.press"
# Paste the Google Form base URL (or set env ABP_FEEDBACK_FORM_URL). While empty, every feedback
# button falls back to a pre-filled mailto:j@ — never a dead end.
FEEDBACK_FORM_URL = os.environ.get("ABP_FEEDBACK_FORM_URL", "")
# The form field id that pre-fills "Which book?" (copy from the form's pre-fill link, e.g.
# "entry.123456"). Per-book buttons append ?<param>=<Book Title>.
FEEDBACK_FORM_BOOK_PARAM = os.environ.get("ABP_FEEDBACK_BOOK_PARAM", "entry.book")
# The form field id that pre-fills a 1–5 star rating, if the form has a rating field. When set, a
# clicked star opens the form pre-scored; ratings are ALSO counted client-side via a Plausible
# custom event ("Rating", props {book, score}) so an aggregate exists with no backend.
FEEDBACK_FORM_RATING_PARAM = os.environ.get("ABP_FEEDBACK_RATING_PARAM", "")

# ── Foreword competition ────────────────────────────────────────────────────────────────────────
# The AI vanity forewords were stripped from every book; this campaign invites READERS to write a
# real one. The winning foreword is published in the book and the writer gets a printed hardcover.
# Toggle the whole surface (page + nav link + per-book invite) with FOREWORD_CONTEST_LIVE.
FOREWORD_CONTEST_LIVE = os.environ.get("ABP_FOREWORD_CONTEST_LIVE", "1") not in ("", "0", "false", "no")
# Submission form URL (or env). While empty, the submit button falls back to a pre-filled mailto:j@.
FOREWORD_FORM_URL = os.environ.get("ABP_FOREWORD_FORM_URL", "")
# Optional closing date shown on the page (free text, e.g. "31 August 2026"). Empty = "rolling".
FOREWORD_DEADLINE = os.environ.get("ABP_FOREWORD_DEADLINE", "")

# ── Fix a translation (first-language colloquialism corrections) ───────────────────────────────
# AI parallel editions need human ears for idiom and register. First-language speakers submit
# fixes; accepted ones are listed on the site and credited in the book. Top contributors per
# language are named and receive a free printed copy of a book of their choice in that language.
# Toggle the whole surface with TRANSLATION_FIX_LIVE. Data file: docs/translation_fixes.json.
TRANSLATION_FIX_LIVE = os.environ.get("ABP_TRANSLATION_FIX_LIVE", "1") not in ("", "0", "false", "no")
TRANSLATION_FIX_FORM_URL = os.environ.get("ABP_TRANSLATION_FIX_FORM_URL", "")
TRANSLATION_FIX_FORM_BOOK_PARAM = os.environ.get("ABP_TRANSLATION_FIX_BOOK_PARAM", "entry.book")
TRANSLATION_FIX_FORM_LANG_PARAM = os.environ.get("ABP_TRANSLATION_FIX_LANG_PARAM", "entry.lang")
TRANSLATION_FIXES_JSON = REPO / "docs" / "translation_fixes.json"

# ── Real Language API (translate-style register control; served by FastAPI at /real-language) ─
REAL_LANGUAGE_LIVE = os.environ.get("ABP_REAL_LANGUAGE_LIVE", "1") not in ("", "0", "false", "no")

# ── Arjuna Audio narrator intake ──────────────────────────────────────────────────────────────
# First marketplace wedge: collect narrators before building dashboards. If a hosted form exists,
# set ABP_NARRATOR_FORM_URL and the page points there. Otherwise it falls back to a mailto form
# with a voice-sample link field, so intake works on a static site today.
NARRATOR_FORM_URL = os.environ.get("ABP_NARRATOR_FORM_URL", "")

# ── Direct distribution / payment rails interest ──────────────────────────────────────────────
# Kobo/Google-style bank-detail gates are exactly what direct distribution should avoid for free
# books. This page is a static declaration today, with an optional hosted form later for readers,
# authors, and payment partners.
DISTRIBUTION_FORM_URL = os.environ.get("ABP_DISTRIBUTION_FORM_URL", "")

# ── Reader app / PWA interest ─────────────────────────────────────────────────────────────────
# The app is the reader layer: free import/read/listen forever, plus optional purchases and print
# orders later. Static page first; Webdock-backed API when accounts, libraries, carts, and orders land.
APP_FORM_URL = os.environ.get("ABP_APP_FORM_URL", "")

# ── Mobile authoring + narrator auditions ─────────────────────────────────────────────────────
# Writers should be able to build a book through a phone-first AI chat. Narrators should be able to
# audition with what they already own, plus science-grounded room and mic technique.
AUTHORING_FORM_URL = os.environ.get("ABP_AUTHORING_FORM_URL", "")
AUDITION_FORM_URL = os.environ.get("ABP_AUDITION_FORM_URL", "")

# ── Audio + print marketplace intake ─────────────────────────────────────────────────────────
# Marketplace MVP is supply/demand discovery, not bidding software: collect narrators, authors,
# printers, and short-run print jobs manually before building dashboards.
MARKETPLACE_FORM_URL = os.environ.get("ABP_MARKETPLACE_FORM_URL", "")
PRINT_FORM_URL = os.environ.get("ABP_PRINT_FORM_URL", "")

# ── Patronage (quiet, reader-initiated; NEVER an ask) ───────────────────────────────────────────
# The books are free. This is a door, not a price — pure-patronage tone, no justifying copy. Kept
# deliberately distinct from the Honey Badger Bounty (which promises money only ever flows FROM the
# press TO readers); patronage is the reader CHOOSING to give, so the two never blur.
# PayPal.me for global reach; PayShap (SA instant-pay) for South African readers. Either may be
# empty; the Support surface only shows the rails that are set, and hides entirely if both are empty.
PAYPAL_URL = os.environ.get("ABP_PAYPAL_URL", "https://paypal.me/ajgreyling")  # live; env overrides
PAYSHAP_ID = os.environ.get("ABP_PAYSHAP_ID", "")        # e.g. a PayShap proxy: 0XX-XXX-XXXX or handle (unset → PayPal-only)

# ── Translated editions ─────────────────────────────────────────────────────────────────────────
# A book's primary (English) deliverable is plain: "<Title>.epub". A TRANSLATED edition carries a
# language-code suffix BEFORE the extension: "<Title>.af.epub", "<Title>.zu.pdf", etc. scan() splits
# these out so the book page can show an "Other languages" section without inventing per-language
# cards. Code → (English name, endonym) for the label. Extend as the catalogue adds languages.
EDITION_LANGS = {
    "af": ("Afrikaans", "Afrikaans"),
    "zu": ("isiZulu", "isiZulu"),
    "es": ("Spanish", "Español"),
    "fr": ("French", "Français"),
    "am": ("Amharic", "አማርኛ"),
    "ar": ("Arabic", "العربية"),
    "hi": ("Hindi", "हिन्दी"),
    "mr": ("Marathi", "मराठी"),
    "ta": ("Tamil", "தமிழ்"),
    "zh": ("Mandarin", "中文"),
    "mn": ("Mongolian", "Монгол"),
    "ja": ("Japanese", "日本語"),
    "xh": ("isiXhosa", "isiXhosa"),
    "st": ("Sesotho", "Sesotho"),
    "tn": ("Setswana", "Setswana"),
    "sw": ("Swahili", "Kiswahili"),
    "de": ("German", "Deutsch"),
}

AUDIOBOOK_NOTICE = (
    "Real voice narration is in production — full audiobook editions for Audible and wide release are on the way. "
    "Read and download the text editions free here until then."
)

# ── Workshop hold ─────────────────────────────────────────────────────────────────────────────
# Book ids here are FORCED to "In the workshop" (no download buttons, the drafting-now line) even
# when finished EPUB/PDF deliverables exist on disk. Use this to hold a drafted-but-not-yet-cleared
# book back from the public shelf — e.g. prose is done but the audiobook hasn't been listened through.
# Remove an id to release the book. Env ABP_WORKSHOP_HOLD (comma-separated) overrides this default.
WORKSHOP_HOLD = set(
    s.strip() for s in os.environ.get(
        "ABP_WORKSHOP_HOLD",
        # Drafted/export exists but not cleared for public download — sensitivity, polish, or
        # series sequencing. Must also be in PUBLISHED to ever show downloads.
        #
        # 2026-06-19 release (author-authorized):
        #   - modern-sherlock (The Scarlet Thread): finished, parked by accident; rendered + released.
        #   - no-fear-cycle (Ordinance Pending): released by explicit author decision, ACCEPTING the
        #     Warhammer 40K fan-canon IP exposure (Games Workshop derivative-work risk noted).
        #   - unheard-japan / unheard-mongolia: released by explicit author decision, OVERRIDING the
        #     `sensitivity_read: REQUIRED` flag in their own project.json (Ainu / Khalkha herders).
        #   - southern-coast (Scratching the Surface): complete 4-ch novella; released by explicit
        #     author decision, OVERRIDING its in-text Khoisan/San sensitivity-read notice.
        # (empty: nothing currently held — add an id here to pull a drafted book off the shelf.)
        "",
    ).split(",") if s.strip()
)

# ── Published shelf (allowlist) ───────────────────────────────────────────────────────────────
# ONLY ids listed here may ship EPUB/PDF downloads and read-online (unless SERIAL). Everything
# else is catalogue-only — card + blurb + cover, badge "Coming soon" or "In progress", zero
# artifacts on the deployed site regardless of what sits on disk in the library repo.
# Env ABP_PUBLISHED (comma-separated) overrides this default.
PUBLISHED = set(
    s.strip() for s in os.environ.get(
        "ABP_PUBLISHED",
        "resonance,revelation,relic,"
        "book1-africa,book2-india,book3-india-deccan,book4-india-tamil,book5-egypt,"
        "australia-outback,project-stargate,"
        "jakobus-silver-thread,jakobus-the-recitation,the-jakobus-file,"
        "crop-circles,"
        # Released 2026-06-19 (author-authorized — see WORKSHOP_HOLD note):
        "modern-sherlock,no-fear-cycle,"
        "southern-coast,"
        "unheard-japan,unheard-mongolia,"
        "sheltering-desert,the-loneliest,"
        "the-song-of-the-self,wrath-of-achilles,"
        "dust-throne,apex-alphas,"
        "the-salt-veil,"
        "voynich-manuscript,"
        # Released 2026-06-20:
        "null-horizon",
    ).split(",") if s.strip()
)

# ── Daily serials ─────────────────────────────────────────────────────────────────────────────
# Book ids here are READ-ONLY-ON-SITE serials: they ship NO EPUB/PDF downloads but ARE published
# (readable now), released chapter-by-chapter from their build/BOOK.md. A serial is treated as
# "available" (so its read-online page renders and its card shows as live) even with zero downloads,
# and it shows the "New chapters daily" badge instead of "Available now". It is NOT in the workshop.
# Env ABP_SERIAL (comma-separated) overrides this default.
SERIAL = set(
    s.strip() for s in os.environ.get(
        "ABP_SERIAL",
        "dust-throne",
    ).split(",") if s.strip()
)

# ── Procedural-cover hide ─────────────────────────────────────────────────────────────────────
# Covers under RICH_COVER_MIN_BYTES are typography-only stubs — withheld from the public shelf
# unless procedural_cover_allowed() says otherwise (SERIAL, Not a Potato, PROCEDURAL_SHOW).
# No SVG typographic fallback: a book without a rich cover does not ship.
# Env ABP_SHOW_PROCEDURAL=1 overrides (show everything — dev/preview only).
RICH_COVER_MIN_BYTES = 500_000
# When design/cover-plate.png exists, a composed cover below this size is a failed compose run.
PLATE_COMPOSE_MIN_BYTES = 200_000
SHOW_PROCEDURAL = os.environ.get("ABP_SHOW_PROCEDURAL", "") in ("1", "true", "yes")
PROCEDURAL_SHOW = set(
    s.strip() for s in os.environ.get(
        "ABP_PROCEDURAL_SHOW",
        "the-loneliest,the-jakobus-file",
    ).split(",") if s.strip()
)

# ── Hidden shelves ────────────────────────────────────────────────────────────────────────────
# Series names here are dropped from the site ENTIRELY: no cards, no blurbs, no covers, no
# downloads, no book pages — and the shelf heading/tagline disappear too (the empty-group guard
# in render_index suppresses them). Stronger than catalogue-only: the line vanishes as if it isn't
# in the library yet. Curated entries stay in CURATED for when the shelf is ready to surface; just
# remove the name here to reveal it. Env ABP_HIDE_SERIES (comma-separated) overrides this default.
HIDE_SERIES = set(
    s.strip() for s in os.environ.get(
        "ABP_HIDE_SERIES",
        "The Unheard",
    ).split(",") if s.strip()
)

# Book IDS here are dropped from the site ENTIRELY, same as HIDE_SERIES but for a single title on a
# shelf you want to keep — no card, page, downloads, or read-online (and a serial is de-listed too).
# Use when a shelf-wide hide is too broad (e.g. one serial on the busy History Before Time shelf).
# Env ABP_HIDE_BOOKS (comma-separated) overrides this default.
HIDE_BOOKS = set(
    s.strip() for s in os.environ.get(
        "ABP_HIDE_BOOKS",
        # the-first-unplugged: the Stranger in a Strange Land retelling stays PRIVATE — EPUB is
        # vendored into the repo but the book is dropped from the site entirely (no card, page,
        # download, read-online), by explicit request, until cleared to surface.
        "the-first-unplugged",
    ).split(",") if s.strip()
)

def cover_candidates(root: Path, exp: Path) -> list[Path]:
    """All known cover paths for a book, in the usual search order."""
    return [
        root / "design" / "cover.png",
        root / "design" / "cover.jpg",
        exp / "cover.png",
        exp / "cover.jpg",
    ]


def resolve_cover(root: Path, exp: Path) -> Path | None:
    """Pick the richest cover on disk — never prefer a stale small file over export."""
    found = [c for c in cover_candidates(root, exp) if c.is_file()]
    if not found:
        return None
    return max(found, key=lambda p: p.stat().st_size)


def cover_is_procedural(cover: Path | None, root: Path) -> bool:
    """True when the cover is a typography stub, not a composed cinematic plate."""
    if cover is None:
        return True
    try:
        size = cover.stat().st_size
    except OSError:
        return True
    if size >= RICH_COVER_MIN_BYTES:
        return False
    if (root / "design" / "cover-plate.png").is_file():
        return size < PLATE_COMPOSE_MIN_BYTES
    return True


def procedural_cover_allowed(cid: str, series: str) -> bool:
    """Series/ids where a small Pillow cover is intentional, not a regression."""
    return (
        SHOW_PROCEDURAL
        or cid in SERIAL
        or cid in PROCEDURAL_SHOW
        or series == "Not a Potato"
    )


def purge_stale_procedural_covers(candidates: list[Path], keep: Path | None, root: Path) -> list[Path]:
    """Hard-delete superseded procedural stubs only when a rich cover is kept."""
    if keep is None or cover_is_procedural(keep, root):
        return []
    deleted: list[Path] = []
    for cand in candidates:
        if cand.resolve() == keep.resolve():
            continue
        if not cand.is_file() or not cover_is_procedural(cand, root):
            continue
        cand.unlink()
        deleted.append(cand)
    return deleted

# ── The curated showcase. Each entry points at a book root; the generator fills in
#    downloads, cover, and blurb by scanning that root (with the fallbacks below). ──
SERIES = [
    ("Non-fiction", "#7BA88C"),
    ("The African Gold Trilogy", "#E5B567"),
    ("History Before Time", "#C8A86B"),
    ("Companions", "#8C7BA8"),
    ("The Synthesis", "#9A7BC8"),
    ("The Salt Veil", "#B0814A"),
    ("The Dust Throne", "#8A5A2C"),
    ("The Unheard", "#6B8C9A"),
    ("Not a Potato", "#9A8B6B"),
    ("The No-Fear Cycle", "#1e3a8a"),
    ("The Reichenbach Files", "#4a5568"),
    ("Standalones", "#B49A6A"),
]

# Per-shelf tagline shown under each series heading on the library. One evocative line in
# the house voice; keyed by the SERIES name. Absent name => no tagline (heading only).
SHELF_TAGLINE = {
    "The African Gold Trilogy": "The cinematic capstone — resonance, revelation, and the relic that tunes the machine.",
    "History Before Time": "Novelised ancient mysteries, one continent per book — the ancients were brilliant, and they were ours.",
    "Not a Potato": "Anomalies told straight: the official story, the one hole in it, and the wink.",
    "The Unheard": "Displaced and overlooked living peoples, told in the spirit of the road.",
    "Standalones": "Self-contained stories that need no shelf-mate.",
    "Non-fiction": "True things, plainly told.",
    "Companions": "Reverent retellings and guides that sit beside the novels.",
    "The Synthesis": "The greatest who ever lived, gathered in one house and made sharper against each other — every mastery is the same climb.",
    "The Reichenbach Files": "Sherlock Holmes for now — modern retellings, true to the original.",
    "The No-Fear Cycle": "Grimdark military SF: holding the line as the world burns.",
    "The Salt Veil": "Desert epic-fantasy — the men hold the thrones; the women hold everything else.",
    "The Dust Throne": "An experimental spiritual-sister telling of the same desert — the saga retold in a first-person, lyrical, firelit register, for a different reader.",
}

# Per-book descriptive tagline shown on the shelf card + book page (under the title).
# The Reichenbach Files are present-day transpositions of Doyle — canon-true, not loose
# adaptation; the tagline says so up front. Keyed by book id; absent id => no tagline.
# NB: distinct from the house TAGLINE string near the top. This is the per-book dict; do not
# collapse the two names — the hero (render_index) needs the string, cards/book pages need this.
BOOK_TAGLINE = {
    "sheltering-desert": "The true story of Henno Martin and Hermann Korn, who hid in the Namib Desert rather than be interned in WWII.",
    "modern-sherlock":   "A Modern Retelling, True to the Original",
    "modern-sherlock-2": "A Modern Retelling, True to the Original",
    "modern-sherlock-3": "A Modern Retelling, True to the Original",
    "modern-sherlock-4": "A Modern Retelling, True to the Original",
    "modern-sherlock-5": "A Modern Retelling, True to the Original",
    "henry-sugar":       "A Faithful Retelling for Adults, True to Dahl",
}

# Optional companion soundtrack — a link to a public playlist that grows over time. Keyed by book id.
# The page links to the live playlist, so tracks added later need no rebuild.
SOUNDTRACK = {
    "the-jakobus-file": ("https://music.youtube.com/playlist?list=PLF4jiM2UaNuP2FhAomyc6LzlnBqGyi1Qe",
                         "Jakobus — the soundtrack"),
}

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
     "history-before-time/books/book1-africa", "build/export",
     "At Adam's Calendar in South Africa — a ring of stone older than the pyramids — the case for a forgotten African deep past stops being a fringe theory. For readers of Graham Hancock & Dan Brown."),
    ("book2-india", "The Indian One", "History Before Time · Book II", "History Before Time",
     "history-before-time/books/book2-india", "build/export",
     "The Kailasa temple at Ellora — carved top-down from a single mountain — and the shore temples of Mahabalipuram: India's impossible stone. For readers of Graham Hancock & James Rollins."),
    ("book3-india-deccan", "The Temple in the Rock — Deccan", "History Before Time · Book III", "History Before Time",
     "history-before-time/books/book3-india-deccan", "build/export",
     "Deeper into the Deccan's rock-cut wonders — how Ellora and Kailasa were really hewn from living stone, and by whom. For readers of Graham Hancock & Douglas Preston."),
    ("book4-india-tamil", "The Shore That Remembers", "History Before Time · Book IV", "History Before Time",
     "history-before-time/books/book4-india-tamil", "build/export",
     "Mahabalipuram and sunken Poompuhar — a Tamil coast that still remembers the shoreline the sea took. For readers of Graham Hancock & Clive Cussler."),
    ("book5-egypt", "The Engineer of the Gods", "History Before Time · Book V", "History Before Time",
     "history-before-time/books/book5-egypt", "build/export",
     "Giza and the Great Pyramid — the engineering mind that could have raised them, read from the stone itself. For readers of Graham Hancock & Michael Crichton."),
    ("australia-outback", "The Songlines of Stone", "History Before Time · Book VI", "History Before Time",
     "history-before-time/books/australia-outback", "build/export",
     "Murujuga's million rock engravings and the songlines of Aboriginal Australia — the oldest continuous human memory on Earth. For readers of Graham Hancock & Bruce Chatwin."),
    ("project-stargate", "The Men Who Opened the Door", "History Before Time · Book VII", "History Before Time",
     "history-before-time/books/project-stargate", "build/export",
     "The true story of the CIA's Project Stargate — the men who tried to weaponise the mind, and what they found at the edge of it. For readers of Annie Jacobsen & Jon Ronson."),
    ("jakobus-silver-thread", "The Silver Thread", "A Jakobus Swart story", "History Before Time",
     "history-before-time/books/jakobus-silver-thread", "build/export",
     "Before the saga, the soldier. The years between the Border War and the man we later meet — how an unkillable gentleness was forged, and what it cost. The grounded, human origin of Jakobus Swart."),
    ("jakobus-the-recitation", "The Recitation", "A Jakobus Swart story", "History Before Time",
     "history-before-time/books/jakobus-the-recitation", "build/export",
     "Jakobus among the Bidhan of the Sahara — the desert years when a wandering South African learned the language, sat at the edge of the Quran, and carried out of it the setting-down of fear, without ever converting. A story of patience, water, and a recited Book. For readers of Wilbur Smith & Laurens van der Post."),
    ("the-jakobus-file", "A Man They All Read Wrong", "The Jakobus Swart File", "History Before Time",
     "history-before-time/books/the-jakobus-file", "build/export",
     "After his death, the man assembled from everyone who knew him — and everyone who only thought they did. The travellers, the titans, the profilers, and the loudest microphones in the world, each reading a different Jakobus Swart, each finding out, sooner or later, that they read him wrong."),
    ("apex-alphas", "Apex Alphas", "The Synthesis · Book One", "The Synthesis",
     "history-before-time/books/apex-alphas", "build/export",
     "A time-machine gate pulls history's masters and the living world's quiet geniuses into one house to face a species-level threat no weapon can touch — and the only thing that answers it is the one frequency they can all be tuned to. A fictional tribute. Opening chapters available now."),

    ("crop-circles", "The Field of Doors", "Not a Potato", "Not a Potato",
     "history-before-time/books/crop-circles", "build/export",
     "The official story played straight — the Wessex chalk, the one genuinely-unresolved hole, and the maybe left open. For readers of Graham Hancock & Jon Ronson."),

    ("unheard-japan", "The Way That Was Invented", "The Unheard · Japan", "The Unheard",
     "the-unheard/books/japan-ainu", "build/export",
     "Japan — Ainu, burakumin, and the living hands the brochure paints over. Jakobus on the road, never the lead."),

    ("unheard-mongolia", "The Felt and the Sky", "The Unheard · Mongolia", "The Unheard",
     "the-unheard/books/mongolia-steppe", "build/export",
     "A herder's daughter sent back as the friendly face of the survey that will fence her father's pasture — and a crew who came for the empty land of Genghis learns the emptiest-looking country on earth is the most precisely known."),

    ("sheltering-desert", "The Indifferent Desert", "A true story · Non-fiction", "Non-fiction",
     "the-sheltering-desert", "build/export",
     "In May 1940 two German geologists drove into the Namib rather than be interned — and survived two and a half years by real bushcraft against a desert that did not care whether they lived."),

    ("the-loneliest", "The Loneliest People in the World", "A standalone novella", "Standalones",
     "the-loneliest", "build/export",
     "A gifted, lonely boy whose one talent is reading people is sent, young, to get close to the daughter of a powerful, feared man — the loneliest person he has ever met. He goes in to use her and instead recognises himself. A novella about two people who were truly seen, once, and never allowed to know what it meant."),

    ("the-song-of-the-self", "The Song of the Self", "A reverent retelling of the Bhagavad Gita", "Non-fiction",
     "history-before-time/companions/the-song-of-the-self", "export",
     "A reverent retelling of the Bhagavad Gita — its quiet question, who acts and for whom, carried with care into the History Before Time world."),

    ("wrath-of-achilles", "The Wrath of Achilles", "Homer's Iliad, plainly told", "Non-fiction",
     "history-before-time/companions/the-wrath-of-achilles", "export",
     "The whole Iliad — its story and what each of its twenty-four books asks of a human life — told plainly enough that a reader who never cracked a Classics syllabus can finish it."),

    ("modern-sherlock", "The Scarlet Thread", "The Reichenbach Files · Book One", "The Reichenbach Files",
     "modern-sherlock", "build/export",
     "Present-day London. Invalided home from Afghanistan, an army doctor meets a consulting detective who reads a life from its digital exhaust — and a message from the one mind clever enough to build puzzles just for him. A modern transposition of Doyle's A Study in Scarlet — original prose, canon-true, public-domain derivation."),

    # ── Coming soon (other threads building these now) ──────────────────────────────────────────
    ("modern-sherlock-2", "The Poisoned Fortune", "The Reichenbach Files · Book Two", "The Reichenbach Files",
     "_comingsoon/modern-sherlock-2", "build/export",
     "Book Two of The Reichenbach Files — the consulting detective and his doctor take a case where an inheritance is the murder weapon. A canon-true transposition of Doyle. Coming soon."),
    ("modern-sherlock-3", "The Viral Haunting", "The Reichenbach Files · Book Three", "The Reichenbach Files",
     "_comingsoon/modern-sherlock-3", "build/export",
     "Book Three of The Reichenbach Files — a haunting that spreads like a contagion, and a rational mind that refuses to flinch. Coming soon."),
    ("modern-sherlock-4", "The Woman Who Beat Him", "The Reichenbach Files · Book Four", "The Reichenbach Files",
     "_comingsoon/modern-sherlock-4", "build/export",
     "Book Four of The Reichenbach Files — the one adversary who is his equal, and the case he cannot reason his way out of. The Irene Adler beat, modernised. Coming soon."),
    ("modern-sherlock-5", "The Reichenbach Protocol", "The Reichenbach Files · Book Five", "The Reichenbach Files",
     "_comingsoon/modern-sherlock-5", "build/export",
     "Book Five — the detective and his nemesis to the edge of the fall. The reckoning the whole series is named for, rebuilt for now. Coming soon."),

    ("no-fear-cycle", "Ordinance Pending", "The No-Fear Cycle · Book One", "The No-Fear Cycle",
     "no-fear-cycle", "build/export",
     "Minutes after Zsah'uj burns, a dying sergeant passes the ordnance keys to the boy who knew no fear — Lieutenant Demetrian Titus must certify a Veil Ordinance grid node before the Warp eats the numbers. Grimdark military science fiction, hold-the-line. Book One of a finite five-novel cycle. For readers of Gaunt's Ghosts and the Astartes."),

    ("the-salt-veil", "The Salt Veil", "A desert epic-fantasy series · Book One", "The Salt Veil",
     "the-salt-veil", "build/export",
     "In a world of salt flats and canyon-cities, the men hold the thrones and the temples — and three women's orders hold everything else: the schemers who breed bloodlines and break minds with the Voice, the veiled killers who end what cannot be persuaded, and the spear-sisters of the wandering desert people. Desert epic-fantasy — Book One."),

    ("the-salt-veil-2", "The First Key", "A desert epic-fantasy series · Book Two", "The Salt Veil",
     "_comingsoon/the-salt-veil-2", "build/export",
     "Book Two of The Salt Veil — the circle tightens, and what was hidden in the salt begins to answer. Coming soon."),
    ("the-salt-veil-3", "The Abyss", "A desert epic-fantasy series · Book Three", "The Salt Veil",
     "_comingsoon/the-salt-veil-3", "build/export",
     "Book Three — descent into the deep places where the Voice cannot follow. Coming soon."),
    ("the-salt-veil-4", "Open War", "A desert epic-fantasy series · Book Four", "The Salt Veil",
     "_comingsoon/the-salt-veil-4", "build/export",
     "Book Four — thrones and temples at open war; the spear-sisters choose a side. Coming soon."),
    ("the-salt-veil-5", "The Circle Closes", "A desert epic-fantasy series · Book Five", "The Salt Veil",
     "_comingsoon/the-salt-veil-5", "build/export",
     "Book Five — the quintet closes where the salt veil first fell. Coming soon."),

    ("dust-throne", "Daughters of the Dust Throne", "The Dust Throne telling · Book One", "The Dust Throne",
     "dust-throne", "build/export",
     "The same desert, told a different way. A girl born carrying a gift the whole desert fears tells the story of it years later, knowing how it ends — a first-person, lyrical, firelit retelling of the Salt Veil saga for a different reader. An experimental spiritual sister to The Salt Veil. Opening chapters; new chapters in progress."),

    ("house-of-bread", "House of Bread", "The Unheard · Holy Land", "The Unheard",
     "_comingsoon/house-of-bread", "build/export",
     "A neurodiverse crew traces the covenant road backward — from Bethlehem in the Free State to Bethlehem in the West Bank — along a chain of checkable stones and living guardians, and learns the Holy Land is not a puzzle to solve but a presence to witness, for believers of every religion and none. Coming soon."),

    ("jakobus-the-long-dark", "The Long Dark", "A Jakobus Swart story", "History Before Time",
     "history-before-time/books/jakobus-the-long-dark", "build/export",
     "Home — South Africa — in the year the grid does not come back. The fixer at the end of the road, and the gift he spent a whole life learning how to give: making sure that when the lights go out for good, nobody's night dies. A grounded collapse-survival story — real bushcraft, told straight — and the one that carries Jakobus Swart's last chapter. For readers of Cormac McCarthy & Lewis Dartnell. Coming soon."),

    ("southern-coast", "Scratching the Surface", "History Before Time · Novella", "History Before Time",
     "history-before-time/books/southern-coast", "build/export",
     "Stilbaai and the southern Cape — a photographer finds a shell midden older than the brochure admits, and a stone that shouldn't be there."),

    ("gobekli-tepe", "The Belly Hill", "Not a Potato", "Not a Potato",
     "_comingsoon/gobekli-tepe", "build/export",
     "Göbekli Tepe — the temple older than the plough, raised by hunter-gatherers a textbook said could not have raised it. The official story, played straight; the one accepted shock it can't explain away; the maybe left open for you to decide. Coming soon."),
    ("voynich-manuscript", "The Hand That Wrote It", "Not a Potato · Book One", "Not a Potato",
     "voynich-manuscript", "build/export",
     "The Voynich Manuscript — a book in a language no one has ever read, illustrated with plants that grow nowhere on earth. Five centuries of the cleverest people alive have failed to crack it. At Yale's Beinecke Library, a statistician sets out to examine it without chasing the usual questions — not what it says or who wrote it, but what it was for, and why it has resisted every reading. The story of the object, played straight, and the one hole the explanations never close."),
    ("null-horizon", "NULL HORIZON", "A true story · Non-fiction", "Non-fiction",
     "non-terrestrial-officers", "build/export",
     "From a flat in Crouch End, Gary McKinnon reached 97 US military and NASA computers — not by breaking in, but by walking through open doors marked No Entry that someone had left unlocked. He took nothing and broke nothing; on the way out he even left a polite sticky note on the door reminding them to lock it. He did what any capable and curious person would do. He was looking for evidence of UFOs. What he found was a spreadsheet — column headers, branch codes, hull designators, transfer durations — and one integer: 4680. Thirteen years. Fleet to fleet. The official story played straight, the one row he copied that was never shown in court, and the world on the other side of an empty password field."),
    ("suppressed-tech", "The Quiet Men", "Not a Potato", "Not a Potato",
     "_comingsoon/suppressed-tech", "build/export",
     "The inventors who said they had something the world wasn't allowed to keep — read as a careful descent from the documented to the purely believed, holding each man's dignity even where his machine never ran. The official story, the human shock beneath it, the maybe left open. Coming soon."),

    # ── Jakobus spinoffs (drafting — in the workshop) ───────────────────────────────────────────
    ("jakobus-petra", "The Rose in the Rock", "A Jakobus Swart story", "History Before Time",
     "history-before-time/books/jakobus-petra", "build/export",
     "Petra — a city eaten out of rose sandstone. The wonder is what a people built when they owned the trade road, the rain, and the patience to cut a tomb like a promise. Coming soon."),
    ("jakobus-longyou", "The Straight Darkness", "A Jakobus Swart story", "History Before Time",
     "history-before-time/books/jakobus-longyou", "build/export",
     "Twenty-four chambers carved straight from solid rock — no quarry debris, no paper trail — and a fixer who always asks what a made thing is for. Coming soon."),
    ("jakobus-broken-crescent", "The Broken Crescent", "A Jakobus Swart story", "History Before Time",
     "history-before-time/books/jakobus-broken-crescent", "build/export",
     "Ur, Babylon, Bamiyan, Palmyra — the cradle-of-civilisation wonders the package tour will never sell. A witness walk, not a conquest. Coming soon."),

    # ── HBT novellas (draft complete — sensitivity gate) ────────────────────────────────────────
    ("hbt-caves", "The Deepest Floor", "History Before Time · Novella", "History Before Time",
     "_comingsoon/hbt-caves", "build/export",
     "A record-deep descent under the Klein Karoo — and a dolomite floor the ancients tuned for a purpose the cave will only reveal if it doesn't kill her first. Coming soon."),
    ("hbt-sudwala", "The Breathing Dark", "History Before Time · Novella", "History Before Time",
     "_comingsoon/hbt-sudwala", "build/export",
     "Sudwala breathes — six hundred metres of show cave and a wind no survey has ever traced to its source. Coming soon."),

    # ── Standalone (drafting) ───────────────────────────────────────────────────────────────────
    ("the-first-unplugged", "The First Unplugged", "A standalone novel", "Standalones",
     "_comingsoon/the-first-unplugged", "build/export",
     "A mind restored to a human body must re-learn what a person is — then founds the movement that forces the world to recognise the restored, at the cost of her own embodiment. Coming soon."),

    ("henry-sugar", "Henry Sugar", "A standalone novel", "Standalones",
     "henry-sugar", "build/export",
     "A bored, wealthy gambler reads a nested account of a man who taught himself to see — and spends years in the boring work of learning, until the card turns over. Roald Dahl's Henry Sugar engine, retold faithfully for adults: original prose, wonder without irony, with Dispenza, Radin, and Sheldrake taken as gospel inside the world. Coming soon."),

    # ── Not a Potato — anomaly slate (draft/scaffold — in the workshop) ─────────────────────────
    ("anunnaki-mesopotamia", "The Princely Offspring", "Not a Potato", "Not a Potato",
     "_comingsoon/anunnaki-mesopotamia", "build/export",
     "Ancient Mesopotamia — the ancient-aliens founding myth played straight, then killed in the cuneiform; the real hole is the Bible's Mesopotamian sources. Coming soon."),
    ("nazca-lines", "From the Air", "Not a Potato", "Not a Potato",
     "_comingsoon/nazca-lines", "build/export",
     "The Nazca Lines — geoglyphs only visible from above, cut centuries before anyone here could fly. The official story, the one hole, the maybe left open. Coming soon."),
    ("atacama-paracas", "Aimed at the Sea", "Not a Potato", "Not a Potato",
     "_comingsoon/atacama-paracas", "build/export",
     "The Atacama Giant and the Paracas Candelabra — two coastal geoglyphs aimed at the Pacific. Coming soon."),
    ("nan-madol", "The Spaces Between", "Not a Potato", "Not a Potato",
     "_comingsoon/nan-madol", "build/export",
     "Nan Madol — a city of basalt logs on a Micronesian reef, raised when the textbook says no one here could have raised it. Coming soon."),
    ("newark-earthworks", "The Eighteen-Year Almanac", "Not a Potato", "Not a Potato",
     "_comingsoon/newark-earthworks", "build/export",
     "The Newark Earthworks — an Ohio geometry aligned to an eighteen-year lunar cycle. Coming soon."),
    ("serpent-mound", "The Serpent's Age", "Not a Potato", "Not a Potato",
     "_comingsoon/serpent-mound", "build/export",
     "The Great Serpent Mound — a serpent swallowing an egg, older than the peoples the brochure assigns it to. Coming soon."),
    ("poverty-point", "Ninety Days", "Not a Potato", "Not a Potato",
     "_comingsoon/poverty-point", "build/export",
     "Poverty Point — a Louisiana earthwork raised in ninety days by a culture with no wheels and no beasts of burden. Coming soon."),
    ("puma-punku", "The Unknown Corner", "Not a Potato", "Not a Potato",
     "_comingsoon/puma-punku", "build/export",
     "Puma Punku — precision-cut andesite at altitude, the corner the official story can't quite account for. Coming soon."),
    ("sajama-lines", "The Long Straight", "Not a Potato", "Not a Potato",
     "_comingsoon/sajama-lines", "build/export",
     "The Sajama Lines — thousands of straight furrows in the Bolivian altiplano, visible only from the air. Coming soon."),
    ("uffington", "The Scouring", "Not a Potato", "Not a Potato",
     "_comingsoon/uffington", "build/export",
     "The Uffington White Horse — scoured into the chalk for three thousand years; the oldest hill figure in Britain. Coming soon."),
    ("yonaguni", "Made or Not", "Not a Potato", "Not a Potato",
     "_comingsoon/yonaguni", "build/export",
     "The Yonaguni Monument — a submerged terrace off Japan; natural fracture or cut stone, and Jakobus's gift meets its limit. Coming soon."),
]


# Former book ids → canonical id (301-style HTML redirect pages at deploy).
BOOK_REDIRECTS = {
    "non-terrestrial-officers": "null-horizon",
}


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
    if re.search(r"\bslate\s*:", p, re.I):
        return False
    if re.search(r"\bfull-send\b|wonder \+ line|line pass", p, re.I):
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


def _slugify(text: str) -> str:
    """Stable URL-safe heading id for reader TOC anchors."""
    t = re.sub(r"<[^>]+>", "", text)            # strip any inline html
    t = re.sub(r"[*_`]", "", t)                  # strip md emphasis marks
    t = t.lower().strip()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t or "section"


def md_to_html(md: str, *, reader: bool = False) -> str:
    out, buf, bq_buf, list_tag, table_buf = [], [], [], None, []
    _heading_ids: dict[str, int] = {}            # for de-duping heading anchor ids

    def inline(t: str) -> str:
        def fmt_label(label: str) -> str:
            label = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", label)
            label = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", label)
            label = re.sub(r"_(.+?)_", r"<em>\1</em>", label)
            label = re.sub(r"`(.+?)`", r"<code>\1</code>", label)
            return label

        def link_repl(m: re.Match[str]) -> str:
            label = fmt_label(m.group(1))
            raw_href = m.group(2).strip()
            parsed = urllib.parse.urlparse(raw_href)
            # Source manuscripts sometimes contain repo-only Markdown cross-references or
            # machine-local file paths. Do not publish those as broken/leaky public links.
            if raw_href.startswith(("/Users/", "file:")):
                return label
            if not parsed.scheme and raw_href.split("#", 1)[0].lower().endswith(".md"):
                return label
            href = html.escape(raw_href, quote=True)
            return f'<a href="{href}">{label}</a>'

        t = html.escape(t)
        # Replace links first, then SHIELD the finished <a …>…</a> tags from the emphasis/code
        # passes below — otherwise an underscore inside a URL (e.g. CREATIVE_THESIS.md) gets
        # mangled into href="CREATIVE<em>THESIS.md". Stash anchors, transform, restore.
        _anchors: list[str] = []

        def _stash(m: "re.Match[str]") -> str:
            _anchors.append(link_repl(m))
            return f"\x00A{len(_anchors) - 1}\x00"

        t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", _stash, t)
        t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", t)
        t = re.sub(r"_(.+?)_", r"<em>\1</em>", t)
        t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
        t = re.sub(r"\x00A(\d+)\x00", lambda m: _anchors[int(m.group(1))], t)
        return t

    def close_list():
        nonlocal list_tag
        if list_tag:
            out.append(f"</{list_tag}>")
            list_tag = None

    def flush_bq():
        nonlocal bq_buf
        if bq_buf:
            text = " ".join(bq_buf).strip()
            if text:
                out.append(f"<blockquote><p>{inline(text)}</p></blockquote>")
            bq_buf.clear()

    def flush_para():
        nonlocal buf
        if buf:
            text = " ".join(buf).strip()
            if text:
                out.append(f"<p>{inline(text)}</p>")
            buf.clear()

    def is_table_line(s: str) -> bool:
        return s.startswith("|") and s.endswith("|") and "|" in s[1:-1]

    def is_table_separator(s: str) -> bool:
        return bool(re.match(r"^\|[\s\-:|]+\|$", s))

    def parse_table_row(s: str) -> list[str]:
        inner = s.strip()[1:-1]
        return [cell.strip() for cell in inner.split("|")]

    def flush_table():
        nonlocal table_buf
        if not table_buf:
            return
        rows: list[list[str]] = []
        for line in table_buf:
            if is_table_separator(line):
                continue
            rows.append(parse_table_row(line))
        table_buf.clear()
        if not rows:
            return
        header, body = rows[0], rows[1:]
        out.append('<table class="md-table">')
        out.append("<thead><tr>" + "".join(f'<th scope="col">{inline(c)}</th>' for c in header) + "</tr></thead>")
        if body:
            out.append("<tbody>")
            for row in body:
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>")
            out.append("</tbody>")
        out.append("</table>")

    def flush_all():
        close_list()
        flush_bq()
        flush_table()
        flush_para()

    fence_lang: str | None = None      # non-None while inside a ``` code fence
    fence_buf: list[str] = []

    def flush_fence():
        nonlocal fence_lang, fence_buf
        body_text = "\n".join(fence_buf)
        if fence_lang == "mermaid":
            # Mermaid renders client-side from the raw graph source inside <pre class="mermaid">.
            # The page that contains one loads mermaid.js and calls mermaid.run() (see head()).
            out.append(f'<pre class="mermaid">{html.escape(body_text)}</pre>')
        else:
            cls = f' class="language-{html.escape(fence_lang)}"' if fence_lang else ""
            out.append(f"<pre><code{cls}>{html.escape(body_text)}</code></pre>")
        fence_lang = None
        fence_buf = []

    for raw in md.splitlines():
        line = raw.rstrip()
        s = line.strip()
        # ``` code fences — accumulate verbatim until the closing fence (handles mermaid + code).
        if fence_lang is not None:
            if s.startswith("```"):
                flush_fence()
            else:
                fence_buf.append(raw)
            continue
        fence_open = re.match(r"^```+\s*([\w-]*)\s*$", s)
        if fence_open:
            flush_all()
            fence_lang = fence_open.group(1) or ""
            continue
        if not s:
            flush_all()
            continue
        if is_table_line(s):
            close_list()
            flush_bq()
            flush_para()
            table_buf.append(s)
            continue
        if table_buf:
            flush_table()
        imgm = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)(?:\{[^}]*\})?$", s)
        if imgm:
            flush_all()
            alt, src = imgm.group(1).strip(), imgm.group(2)
            if not alt:
                alt = "Illustration"
            out.append(
                f'<figure class="wiki-photo"><img loading="lazy" src="{html.escape(src, quote=True)}" '
                f'alt="{html.escape(alt)}"><figcaption>{inline(alt)}</figcaption></figure>'
            )
            continue
        if re.match(r"^(---|\*\*\*|___)$", s):
            flush_all()
            out.append('<hr class="rule">')
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            flush_all()
            lvl = len(m.group(1))
            if reader:
                lvl = min(lvl + 1, 6)
            htext = m.group(2)
            hid = _slugify(htext)
            if hid in _heading_ids:
                _heading_ids[hid] += 1
                hid = f"{hid}-{_heading_ids[hid]}"
            else:
                _heading_ids[hid] = 0
            out.append(f'<h{lvl} id="{hid}">{inline(htext)}</h{lvl}>')
            continue
        bqm = re.match(r"^>\s?(.*)$", s)
        if bqm:
            close_list()
            flush_para()
            bq_buf.append(bqm.group(1))
            continue
        if bq_buf:
            flush_bq()
        olm = re.match(r"^\d+\.\s+(.*)$", s)
        if olm:
            flush_para()
            if list_tag != "ol":
                close_list()
                out.append("<ol>")
                list_tag = "ol"
            out.append(f"<li>{inline(olm.group(1))}</li>")
            continue
        ulm = re.match(r"^[-*]\s+(.*)$", s)
        if ulm:
            flush_para()
            if list_tag != "ul":
                close_list()
                out.append("<ul>")
                list_tag = "ul"
            out.append(f"<li>{inline(ulm.group(1))}</li>")
            continue
        if re.match(r"^\*\*[^*]+:\*\*", s):
            close_list()
            flush_para()
            buf.append(s)
            continue
        close_list()
        buf.append(s)
    flush_all()
    return "\n".join(out)


# ── scan ───────────────────────────────────────────────────────────────────────
def companion_manuscript(root: Path) -> str | None:
    """Merge companion book/*.md into one markdown string for read-online."""
    book_dir = root / "book"
    front = book_dir / "_front.md"
    if not front.is_file():
        return None
    parts = [front.read_text(encoding="utf-8").rstrip()]
    for f in sorted(book_dir.glob("[0-9]*.md")):
        parts.append(f.read_text(encoding="utf-8").rstrip())
    return "\n\n".join(parts) + "\n"


_ISBN_CLEAN_RE = re.compile(r"[^0-9Xx]")


def book_isbn(root: Path) -> str:
    """Return a book's e-book ISBN from its project.json, or "" if unset/absent.

    The per-book project.json already carries an `isbn` block ({paperback, hardcover, ebook});
    for the free EPUB catalogue the `ebook` value is the one that matters. We read it here so the
    number lives next to the book it belongs to (not in a central list that drifts), and flows from
    one source into the page, the JSON-LD, and the Wikidata export. Returns the digits-only form
    (hyphens/spaces stripped) so downstream consumers can format consistently; blank or placeholder
    values (e.g. the "___-_-..." print stub) collapse to "" and emit nothing."""
    pj = root / "project.json"
    if not pj.is_file():
        return ""
    try:
        data = json.loads(pj.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return ""
    raw = ((data.get("isbn") or {}).get("ebook") or "").strip()
    cleaned = _ISBN_CLEAN_RE.sub("", raw).upper()
    # A real ISBN-13 is 13 digits; ISBN-10 is 9 digits + (digit or X). Anything else (empty, the
    # "___" placeholder, a partial) is treated as "not yet assigned".
    if len(cleaned) == 13 and cleaned.isdigit():
        return cleaned
    if len(cleaned) == 10 and cleaned[:9].isdigit() and cleaned[9] in "0123456789X":
        return cleaned
    return ""


def scan() -> list[dict]:
    entries = []
    hidden_proc: list[str] = []
    for cid, title, subtitle, series, rootrel, expsub, fb in CURATED:
        root = BOOKS / rootrel
        exp = root / expsub
        downloads = []          # primary (English) EPUB/PDF
        editions = {}           # lang code -> {"epub": Path, "pdf": Path} for translated editions
        if cid in PUBLISHED and exp.is_dir():
            for f in sorted(exp.iterdir()):
                if f.suffix.lower() not in (".epub", ".pdf"):
                    continue
                # A translated edition's stem ends ".<code>" (e.g. "Resonance.af"); split it off.
                stem_suffix = f.stem.rsplit(".", 1)[-1].lower() if "." in f.stem else ""
                if stem_suffix in EDITION_LANGS:
                    editions.setdefault(stem_suffix, {})[f.suffix.lower().lstrip(".")] = f
                else:
                    downloads.append(f)
        # blurb precedence: clean SYNOPSIS -> curated fallback -> README (dev-facing, last resort)
        blurb = first_paragraph(root / "SYNOPSIS.md") or fb or first_paragraph(root / "README.md")
        # cover: richest file wins; stale procedural stubs are deleted on sight
        cands = cover_candidates(root, exp)
        cover = resolve_cover(root, exp)
        purged = purge_stale_procedural_covers(cands, cover, root)
        if purged:
            print(f"  (deleted stale procedural cover(s) for {cid}: "
                  f"{', '.join(p.name for p in purged)})")
        if cover is None or (
                cover_is_procedural(cover, root) and not procedural_cover_allowed(cid, series)):
            hidden_proc.append(cid)
            continue
        book_md = root / "build" / "BOOK.md"
        reader_md = None
        reader_src = None
        can_read = cid in SERIAL or (cid in PUBLISHED and cid not in WORKSHOP_HOLD)
        if can_read:
            if book_md.is_file():
                reader_src = book_md
            else:
                reader_md = companion_manuscript(root)
        entries.append({
            "id": cid, "title": title, "subtitle": subtitle, "series": series,
            "blurb": blurb, "downloads": downloads, "cover": cover,
            "editions": editions,
            "book_md": reader_src,
            "reader_md": reader_md,
            "root": root,
            "serial": cid in SERIAL,
            "available": can_read and (cid in SERIAL or bool(downloads)),
            "isbn": book_isbn(root),
        })
    if hidden_proc:
        print(f"  (procedural covers hidden from shelf: {len(hidden_proc)} — "
              f"{', '.join(hidden_proc[:8])}{'…' if len(hidden_proc) > 8 else ''})")
    return entries


_READER_IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")


def _strip_pandoc_attrs(path: str) -> str:
    return re.sub(r"\{[^}]*\}$", "", path.strip())


def resolve_reader_image(src: str, book_root: Path) -> Path | None:
    """Map BOOK.md image paths (often machine-local) to files in this repo."""
    src = _strip_pandoc_attrs(src)
    if src.startswith(("http://", "https://")):
        return None

    p = Path(src)
    candidates: list[Path] = []

    if p.is_absolute():
        parts = p.parts
        if "books" in parts:
            idx = parts.index("books")
            candidates.append(BOOKS / Path(*parts[idx + 1:]))
        candidates.append(book_root / "build" / "assets" / p.name)
        candidates.append(book_root / "build" / "appendix-images" / p.name)
        candidates.append(book_root / "design" / p.name)
        candidates.append(book_root / "design" / "images" / p.name)
    elif src.startswith("books/"):
        rel = src.removeprefix("books/")
        slug, _, tail = rel.partition("/")
        if tail:
            rest = Path(tail)
            candidates.append(BOOKS / "history-before-time" / "books" / slug / rest)
            candidates.append(BOOKS / "the-unheard" / "books" / slug / rest)
            candidates.append(BOOKS / slug / rest)
    else:
        candidates.append(book_root / src)
        candidates.append(book_root / "build" / "assets" / p.name)
        if not src.startswith("design/"):
            candidates.append(book_root / "design" / "images" / p.name)

    seen: set[Path] = set()
    for c in candidates:
        try:
            c = c.resolve()
        except OSError:
            continue
        if c in seen:
            continue
        seen.add(c)
        if c.is_file():
            return c
    return None


def prepare_reader_images(md: str, book_id: str, book_root: Path, assets_out: Path) -> str:
    """Copy inline images for read-online and rewrite paths to site-local URLs."""
    assets_out.mkdir(parents=True, exist_ok=True)

    def repl(m: re.Match[str]) -> str:
        alt, raw_src = m.group(1), m.group(2)
        src = _strip_pandoc_attrs(raw_src)
        if src.startswith(("http://", "https://")):
            return f"![{alt}]({src})"
        resolved = resolve_reader_image(src, book_root)
        if not resolved:
            return ""
        dst = assets_out / resolved.name
        if not dst.exists() or resolved.stat().st_mtime > dst.stat().st_mtime:
            shutil.copy2(resolved, dst)
        return f"![{alt}](assets/{book_id}/{resolved.name})"

    return _READER_IMG_RE.sub(repl, md)


# ── render ───────────────────────────────────────────────────────────────────────
CSS = """
:root{
  --black:#161513; --iron:#221f1b; --card:#1d1a16; --bone:#EDE9E0; --bonedim:#BDB6A6;
  --ochre:#C8A86B; --gold:#E5B567; --grass:#9B9684; --line:#2A241D; --sting:#C2401E;
  --violet:#A78BFA; --violet-deep:#7C5CFF; --violet-glow:rgba(124,92,255,.16);
  --reading:"Atkinson Hyperlegible",system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
}
*{box-sizing:border-box} html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  *,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;
    transition-duration:.01ms!important}
}
.skip-link{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);
  white-space:nowrap;border:0}
.skip-link:focus{position:fixed;left:16px;top:16px;width:auto;height:auto;margin:0;padding:12px 18px;
  overflow:visible;clip:auto;white-space:normal;z-index:100;background:var(--gold);color:var(--black);
  font-weight:600;border-radius:8px;box-shadow:0 4px 20px rgba(0,0,0,.5)}
:focus{outline:none}
:focus-visible{outline:2px solid var(--gold);outline-offset:2px}
a:focus-visible,button:focus-visible,.btn:focus-visible,.dl:focus-visible,.qopt:focus-visible,
.star:focus-visible,.hamburger:focus-visible,.navclose:focus-visible,.navdrawer a:focus-visible,
.readtoc a:focus-visible,.library-item:focus-visible,.linkbtn:focus-visible{
  outline:2px solid var(--gold);outline-offset:2px}
[id]{scroll-margin-top:88px}
.readbar ~ .readlayout [id],.readbar ~ .reader [id]{scroll-margin-top:120px}
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
/* Drawer-only nav — do NOT reintroduce .navinline or a wide-screen top link bar. */
.nav nav.navinline{display:none!important}

/* ── Hamburger + slide-out drawer (pure-CSS toggle via #navtoggle checkbox) ─────────────────── */
.hamburger{margin-left:auto;display:flex;flex-direction:column;justify-content:center;gap:5px;
  width:42px;height:42px;padding:9px;cursor:pointer;border-radius:8px}
.hamburger:hover{background:rgba(229,181,103,.1)}
.hamburger span{display:block;height:2px;width:100%;background:var(--bone);border-radius:2px;
  transition:transform .25s,opacity .2s}
.navtoggle:checked ~ .nav .hamburger span:nth-child(1){transform:translateY(7px) rotate(45deg)}
.navtoggle:checked ~ .nav .hamburger span:nth-child(2){opacity:0}
.navtoggle:checked ~ .nav .hamburger span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}
.navdrawer{position:fixed;top:0;left:0;bottom:0;z-index:60;width:min(80vw,300px);
  transform:translateX(-100%);transition:transform .28s cubic-bezier(.4,0,.2,1);
  background:#161513;border-right:1px solid var(--line);box-shadow:6px 0 40px rgba(0,0,0,.5);
  display:flex;flex-direction:column;gap:2px;padding:74px 14px 24px;overflow-y:auto}
.navdrawer a{color:var(--bone);font-family:"Space Grotesk";font-size:16px;padding:11px 14px;
  border-radius:8px;text-decoration:none}
.navdrawer a:hover{background:rgba(229,181,103,.1);color:var(--gold)}
.navdrawer a:focus-visible{background:rgba(229,181,103,.1);color:var(--gold)}
.navdrawer a.navhot{color:var(--sting)}
.navdrawer a.navhot:hover{color:#e0552e}
.navdrawer .navgroup{font-family:"Space Grotesk";font-size:11px;letter-spacing:.18em;text-transform:uppercase;
  color:var(--grass);padding:18px 14px 4px;margin:0}
.navdrawer .navgroup:first-child{padding-top:8px}

/* library-first index */
.library-intro{margin:8px 0 28px;max-width:62ch}
.library-intro h2{font-size:28px;margin:.2em 0 .35em}
.library-intro p{margin:0;color:var(--bonedim);font-size:17px;line-height:1.55}
.explore-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px;margin-top:18px}
.explore-card{display:block;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px 20px;
  transition:border-color .15s,transform .15s}
.explore-card:hover{border-color:var(--ochre);transform:translateY(-2px);color:inherit}
.explore-card h3{margin:0 0 .35em;font-size:17px;color:var(--bone)}
.explore-card p{margin:0;color:var(--bonedim);font-size:14px;line-height:1.45}
.mission-compact{padding:36px 0 12px}
.mission-compact .pillars{margin-top:12px}
.index-foot{padding:36px 0 48px}
.index-foot p{max-width:62ch;color:var(--bonedim);font-size:16px;line-height:1.55;margin:0}
.pipeline-list{columns:2;gap:28px;margin:16px 0 0;padding:0;list-style:none}
.pipeline-list li{break-inside:avoid;margin:0 0 10px;color:var(--bonedim);font-size:15px}
.pipeline-list em{color:var(--ochre);font-style:normal;font-size:13px}
@media(max-width:640px){.pipeline-list{columns:1}}
.navclose{position:absolute;top:16px;right:16px;font-size:30px;line-height:1;color:var(--bonedim);
  cursor:pointer;padding:4px 10px;border-radius:8px}
.navclose:hover{color:var(--bone);background:rgba(229,181,103,.1)}
.navscrim{position:fixed;inset:0;z-index:55;background:rgba(0,0,0,.5);opacity:0;visibility:hidden;
  transition:opacity .28s;cursor:pointer}
.navtoggle:checked ~ .navdrawer{transform:translateX(0)}
.navtoggle:checked ~ .navscrim{opacity:1;visibility:visible}
/* The site has a broad information architecture; the drawer avoids fragile wrapped nav bars. */

/* site-wide audiobook notice */
.audiobook-notice{border-bottom:1px solid rgba(200,168,107,.35);
  background:linear-gradient(90deg,rgba(200,168,107,.12),rgba(229,181,103,.08),rgba(200,168,107,.12));
  color:var(--bone);font-size:14px;line-height:1.5}
.audiobook-notice .wrap{padding:11px 24px;display:flex;gap:12px;align-items:flex-start;justify-content:center;text-align:center}
.audiobook-notice strong{font-family:"Space Grotesk";font-weight:600;color:var(--gold);white-space:nowrap}
.audiobook-notice span{max-width:72ch;color:var(--bonedim)}
/* Anti-scam trust strip — calm, not alarmist (red would look scammier). */
.trust-banner{border-bottom:1px solid rgba(126,122,90,.4);background:rgba(20,18,15,.6);
  font-size:13.5px;line-height:1.5}
.trust-banner .wrap{padding:9px 24px;display:flex;gap:10px;align-items:center;justify-content:center;
  flex-wrap:wrap;text-align:center}
.trust-banner strong{color:var(--bone);font-weight:600}
.trust-banner a{color:var(--gold);white-space:nowrap} .trust-banner a:hover{color:var(--bone)}

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
.pillar h2,.pillar h3{margin:.2em 0 .4em;font-size:18px} .pillar p{margin:0;color:var(--bonedim);font-size:15px}
.pillar .n{font-family:"Cormorant Garamond",serif;font-size:30px;color:var(--ochre)}

/* sections */
section.series{padding:46px 0 8px}
.sechead{margin-bottom:22px}
.sechead-row{display:flex;align-items:baseline;gap:16px}
.sechead h2{font-size:26px;margin:0}
.sechead .count{color:var(--grass);font-size:14px;font-family:"Space Grotesk"}
.sechead .shelftag{margin:.35em 0 0;font-family:"Cormorant Garamond",serif;font-style:italic;
  font-size:17px;line-height:1.4;color:var(--accent,var(--ochre));opacity:.95;max-width:64ch}
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
.card p.tagline{flex:0;margin:.1em 0 0;font-family:"Cormorant Garamond",serif;font-style:italic;
  font-size:14.5px;color:var(--accent,var(--ochre));opacity:.92}
.card p{margin:0;color:var(--bonedim);font-size:14px;flex:1}
.badge{align-self:flex-start;font-size:11px;font-family:"Space Grotesk";letter-spacing:.08em;
  padding:3px 9px;border-radius:99px;border:1px solid var(--line);color:var(--grass)}
.badge.soon{color:var(--ochre);border-color:rgba(200,168,107,.4)}
.dls{display:flex;gap:10px;flex-wrap:wrap;margin-top:4px}
.dl{font-family:"Space Grotesk";font-size:12.5px;font-weight:600;padding:6px 12px;border-radius:7px;
  border:1px solid var(--ochre);color:var(--ochre)} .dl:hover{background:rgba(229,181,103,.1);color:var(--gold)}
.dl.solid{background:var(--ochre);color:var(--black)} .dl.solid:hover{background:var(--gold);color:var(--black)}

/* "which book first?" recommender */
.start{max-width:760px}
.qblock{border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin:22px 0;background:var(--card)}
.qblock legend{font-family:"Space Grotesk";font-weight:600;color:var(--gold);font-size:15px;padding:0 8px}
.qopts{display:flex;flex-wrap:wrap;gap:10px;margin-top:8px}
.qopt{font-family:"Inter",sans-serif;font-size:14.5px;text-align:left;cursor:pointer;
  padding:10px 14px;border-radius:9px;border:1px solid var(--line);background:transparent;color:var(--bone);
  transition:all .15s}
.qopt:hover{border-color:var(--ochre);color:var(--gold)}
.qopt:focus-visible{border-color:var(--gold);color:var(--gold)}
.qopt[aria-pressed="true"]{border-color:var(--gold);background:rgba(229,181,103,.12);color:var(--gold);font-weight:600}
.qactions{display:flex;gap:12px;justify-content:center;margin-top:26px;flex-wrap:wrap}
.qactions .btn:disabled{opacity:.4;cursor:not-allowed;pointer-events:none}
/* visual Rorschach tile grid */
.tilegrid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:24px 0 6px}
@media(max-width:640px){.tilegrid{grid-template-columns:repeat(2,1fr);gap:10px}}
.tile{position:relative;padding:0;border:1px solid var(--line);border-radius:12px;overflow:hidden;
  cursor:pointer;background:var(--card);aspect-ratio:1/1;transition:transform .15s,border-color .15s,box-shadow .15s}
.tile:hover,.tile:focus-visible{transform:translateY(-3px);border-color:var(--gold);
  box-shadow:0 14px 34px rgba(0,0,0,.45);outline:none}
.tile img{width:100%;height:100%;object-fit:cover;display:block}
.tile .tilecap{position:absolute;left:0;right:0;bottom:0;padding:18px 10px 9px;font-family:"Space Grotesk";
  font-size:12.5px;font-weight:600;color:#fff;text-align:center;line-height:1.25;
  background:linear-gradient(transparent,rgba(0,0,0,.78))}
.tilehint{text-align:center;color:var(--bonedim);font-size:14px;margin-top:14px}
.linkbtn{background:none;border:none;color:var(--gold);cursor:pointer;font:inherit;text-decoration:underline;padding:0}
.linkbtn:hover{color:var(--bone)}
#result{margin-top:18px}
.reccard{display:grid;grid-template-columns:120px 1fr;gap:20px;align-items:start;
  border:1px solid var(--line);border-left:3px solid var(--accent,var(--ochre));border-radius:12px;
  padding:18px;background:var(--card);margin:14px 0}
.reccard.lead{grid-template-columns:160px 1fr;padding:22px}
.reccard .cover{width:100%;aspect-ratio:400/620;border-radius:8px;box-shadow:0 10px 28px rgba(0,0,0,.45)}
.reccard .ser{font-family:"Space Grotesk";font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent,var(--ochre))}
.reccard h3{margin:.2em 0 .3em;font-size:21px} .reccard.lead h3{font-size:26px}
.reccard h3 a{color:var(--bone)} .reccard h3 a:hover{color:var(--gold)}
.reccard .blurb{color:var(--bonedim);font-size:15px;line-height:1.55;margin:.3em 0}
.recrunners{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:640px){.recrunners{grid-template-columns:1fr}.reccard,.reccard.lead{grid-template-columns:90px 1fr;gap:14px}}

/* book page */
.bookhero{display:grid;grid-template-columns:300px 1fr;gap:42px;padding:48px 0}
.bookhero .cover{aspect-ratio:400/620;border-radius:12px;box-shadow:0 18px 50px rgba(0,0,0,.5)}
.bookhero h1{font-family:"Cormorant Garamond",serif;font-size:46px;margin:.1em 0 .1em}
.bookhero .sub{color:var(--ochre);font-family:"Space Grotesk";letter-spacing:.12em;text-transform:uppercase;font-size:13px}
.bookhero .tagline{margin:.2em 0 0;font-family:"Cormorant Garamond",serif;font-style:italic;font-size:20px;color:var(--ochre)}
.bookhero .syn{font-size:18px;color:var(--bone);margin-top:18px;max-width:60ch}
.back{font-family:"Space Grotesk";font-size:13px;color:var(--bonedim)}

/* reader — house long-form face: Atkinson Hyperlegible (EPUB/PDF parity) */
.reader{width:100%;max-width:720px;margin:0 auto;padding:50px 24px 90px;
  font-family:var(--reading);font-size:18px;line-height:1.65;
  -webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
.reader h1,.reader h2,.reader h3,.reader h4,.reader p,.reader li,.reader blockquote,.reader td,.reader th{
  font-family:var(--reading)}
.reader h1{font-size:42px;text-align:center;font-weight:700;letter-spacing:-.01em}
.reader h2{font-size:30px;margin-top:2.2em;text-align:center;color:var(--gold);font-weight:700}
.reader p{margin:0 0 1.1em} .reader .rule{border:0;text-align:center;margin:2em 0}
.reader .rule:after{content:"\\2766";color:var(--ochre);font-size:20px}
/* ── Code fences + Mermaid diagrams ────────────────────────────────────────────────────────── */
pre code{display:block;padding:16px 18px;background:#161513;border:1px solid var(--line);
  border-radius:10px;overflow-x:auto;font-family:ui-monospace,"SF Mono",Menlo,monospace;
  font-size:13.5px;line-height:1.5;color:var(--bonedim)}
.reader code{overflow-wrap:anywhere;word-break:break-word}
pre.mermaid{margin:1.8em auto;padding:18px;text-align:center;background:transparent;border:0;
  /* hidden until mermaid.js swaps the source for an <svg>; avoids a flash of raw graph text */
  color:transparent;min-height:40px;line-height:0}
pre.mermaid svg{max-width:100%;height:auto;line-height:normal}
pre.mermaid[data-processed] {color:inherit}
/* ── Online-reader chapter list / TOC (left rail on wide screens) ───────────────────────────── */
.readlayout{display:grid;grid-template-columns:266px minmax(0,1fr);gap:8px;
  max-width:1040px;margin:0 auto;align-items:start}
.readlayout .reader{max-width:720px;margin:0}           /* article keeps its measure; grid centres it */
.readtoc{position:sticky;top:64px;align-self:start;max-height:calc(100vh - 84px);
  overflow-y:auto;padding:34px 8px 40px 24px;font-family:"Space Grotesk",sans-serif;
  scrollbar-width:thin;scrollbar-color:var(--line) transparent}
.readtoc::-webkit-scrollbar{width:8px} .readtoc::-webkit-scrollbar-thumb{background:var(--line);border-radius:4px}
.readtoc-h{margin:0 0 12px;font-size:11px;letter-spacing:.26em;text-transform:uppercase;color:var(--ochre);
  font-family:"Space Grotesk",sans-serif;font-weight:600}
.readtoc ol{list-style:none;margin:0;padding:0;counter-reset:toc}
.readtoc li{margin:0}
.readtoc li.sub a{padding-left:24px;font-size:12.5px;color:var(--grass)}
.readtoc a{display:block;padding:6px 10px;border-left:2px solid transparent;
  color:var(--bonedim);font-size:13.5px;line-height:1.4;text-decoration:none;
  border-radius:0 5px 5px 0;transition:color .15s,background .15s,border-color .15s}
.readtoc a:hover{color:var(--bone);background:rgba(229,181,103,.07)}
.readtoc a.active{color:var(--gold);border-left-color:var(--gold);background:rgba(229,181,103,.10);font-weight:600}
/* Narrow screens: the rail folds into a collapsible bar above the prose (pure-CSS toggle). */
.readtoc-toggle{display:none}
@media (max-width:900px){
  .readlayout{grid-template-columns:1fr;gap:0}
  .readlayout .reader{margin:0 auto}
  .readtoc{position:static;max-height:340px;padding:14px 20px;margin:0 auto;width:100%;max-width:720px;
    border-bottom:1px solid var(--line)}
}
.letter-crest{display:block;margin:0 auto 6px;width:120px;height:120px;border-radius:50%}
.reader.letter h1{margin-bottom:.1em}
.reader.letter h2{text-align:left;font-size:25px;color:var(--gold);margin-top:1.9em;font-weight:700}
.reader.letter em{color:var(--bone)}
.readbar{position:sticky;top:0;background:rgba(22,21,19,.85);backdrop-filter:blur(8px);
  border-bottom:1px solid var(--line);padding:12px 0}
.reader figure.wiki-photo{margin:1.8em 0 2.2em;text-align:center}
.reader figure.wiki-photo img{max-width:100%;height:auto;border-radius:8px;border:1px solid var(--line);
  box-shadow:0 12px 36px rgba(0,0,0,.4)}
.reader figure.wiki-photo figcaption{font-size:15px;color:var(--gold);margin-top:10px}
.reader table.md-table{width:100%;border-collapse:collapse;margin:1.4em 0 1.8em;font-size:16px}
.reader table.md-table th,.reader table.md-table td{padding:12px 14px;border:1px solid var(--line);text-align:left;vertical-align:top}
.reader table.md-table th{background:rgba(200,168,107,.12);color:var(--gold);font-weight:700}
.reader table.md-table td{color:var(--bone)}
.reader table.md-table tr:nth-child(even) td{background:rgba(255,255,255,.02)}
@media(max-width:720px){
  .reader{padding:42px 16px 78px;font-size:17px}
  .reader h1{font-size:34px}
  .reader h2{font-size:25px}
  .reader table.md-table{display:block;max-width:100%;overflow-x:auto;font-size:14px}
  .reader table.md-table th,.reader table.md-table td{padding:9px 10px}
}

/* house of greyling */
.house{max-width:900px;margin:0 auto;padding:54px 24px 80px;text-align:center}
.house img.crest-full{width:100%;max-width:640px;height:auto;border-radius:10px;
  box-shadow:0 22px 64px rgba(0,0,0,.55);border:1px solid var(--line)}
.house h1{font-family:"Cormorant Garamond",serif;font-size:clamp(34px,6vw,58px);margin:28px 0 .06em}
.house .motto{font-family:"Cormorant Garamond",serif;font-style:italic;color:var(--gold);font-size:clamp(19px,3vw,28px)}
.house .gloss{color:var(--bonedim);font-family:"Space Grotesk";letter-spacing:.08em;font-size:13px;margin-top:6px;text-transform:uppercase}
.blazon{text-align:left;max-width:680px;margin:30px auto 0;
  font-family:var(--reading);font-size:18px;line-height:1.65}
.blazon p.intro{color:var(--bone);font-size:19px;margin:0 0 1.2em}
.blazon h2{font-family:var(--reading);color:var(--gold);font-size:27px;text-align:center;margin:2em 0 .8em;font-weight:700}
.blazon .entry{margin:0 0 1.25em;padding-left:16px;border-left:2px solid var(--line)}
.blazon .charge{font-family:"Space Grotesk";font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--ochre);display:block;margin-bottom:3px}
.blazon .entry p{margin:0;color:var(--bone)}

/* place wiki — photo galleries */
.reader.wiki h3{font-size:22px;text-align:left;color:var(--bone);margin:2em 0 .5em;font-weight:700}
.reader.wiki figure.wiki-photo{margin:0 0 2em;text-align:center}
.reader.wiki figure.wiki-photo img{max-width:100%;width:min(920px,100%);height:auto;border-radius:10px;
  box-shadow:0 16px 44px rgba(0,0,0,.45);border:1px solid var(--line)}
.reader.wiki figure.wiki-photo figcaption{font-size:15px;color:var(--gold);margin-top:12px;max-width:60ch;margin-left:auto;margin-right:auto}
.reader.wiki p em{font-size:13px;color:var(--grass);font-style:normal;display:block;text-align:center;margin:-1.2em 0 1.8em}
.wiki-index table{width:100%;border-collapse:collapse;margin:1.5em 0;font-size:16px}
.wiki-index th,.wiki-index td{padding:10px 14px;border-bottom:1px solid var(--line);text-align:left}
.wiki-index th{color:var(--ochre);font-family:"Space Grotesk";font-size:12px;letter-spacing:.12em;text-transform:uppercase}

/* footer */
footer{border-top:1px solid var(--line);margin-top:60px;padding:40px 0;color:var(--grass);font-size:14px}
footer .wrap{display:flex;gap:18px;flex-wrap:wrap;align-items:center;justify-content:space-between}
footer .badgerline{font-family:"Cormorant Garamond",serif;font-style:italic;color:var(--bonedim)}
footer a{color:var(--grass)} footer a:hover{color:var(--gold)}
/* ── rating + feedback (quiet) ───────────────────────────────────────────────── */
.rate{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:18px 0 4px}
.rate-label{font-size:13px;color:var(--grass);letter-spacing:.04em}
.stars{display:inline-flex;gap:2px}
.star{background:none;border:0;padding:0 1px;cursor:pointer;font-size:22px;line-height:1;
  color:var(--line);transition:color .12s} /* unlit = faint */
.star:hover,.star:hover~.star{color:var(--ochre)}      /* hover lights up to the hovered star (LTR) */
.stars:hover .star{color:var(--ochre)} .stars .star:hover~.star{color:var(--line)}
.star.on{color:var(--gold)}                            /* chosen score persists in gold */
.rate-fallback{font-size:12.5px;color:var(--grass);text-decoration:underline}
.rate-thanks{font-size:13px;color:var(--gold)}
/* ── translated editions ───────────────────────────────────────────────────────── */
.editions{margin-top:24px;padding-top:18px;border-top:1px solid var(--line)}
.editions-h{font-family:"Space Grotesk";font-size:13px;letter-spacing:.22em;text-transform:uppercase;color:var(--ochre);margin:0 0 4px}
.editions-note{font-size:13px;color:var(--grass);margin:0 0 12px;max-width:54ch}
.edlist{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px}
.edlist li{display:flex;align-items:center;justify-content:space-between;gap:14px;
  padding:8px 12px;background:var(--card);border:1px solid var(--line);border-radius:10px}
.edlang{color:var(--bone);font-size:14px}
.edlinks{display:inline-flex;gap:6px}
.dl-lang{font-family:"Space Grotesk";font-size:12px;font-weight:500;padding:4px 12px;border-radius:8px;
  border:1px solid var(--ochre);color:var(--ochre)}
.dl-lang:hover{background:var(--ochre);color:var(--black)}
.editions-fix{margin:10px 0 0;font-size:13px;color:var(--grass)}
.editions-fix a{color:var(--ochre)}
.fixlog{margin:18px 0 0}
.fixlog table{width:100%;border-collapse:collapse;font-size:14px;margin-top:10px}
.fixlog th,.fixlog td{padding:10px 12px;border:1px solid var(--line);text-align:left;vertical-align:top}
.fixlog th{background:rgba(200,168,107,.12);color:var(--gold);font-weight:700}
.fixlog td{color:var(--bone)}
.fixlog-empty{font-size:14px;color:var(--grass);font-style:italic;margin:8px 0 0}
.fixtops{display:flex;flex-wrap:wrap;gap:12px;margin-top:10px}
.fixtop{flex:1 1 200px;padding:12px 14px;background:var(--card);border:1px solid var(--line);border-radius:10px}
.fixtop h3{font-family:"Space Grotesk";font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:var(--ochre);margin:0 0 8px}
.fixtop li{font-size:14px;color:var(--bone);margin:4px 0}
.bookrespond{margin-top:22px;padding-top:18px;border-top:1px solid var(--line)}
.feedback-link,.endnote-feedback a{font-size:13.5px;color:var(--ochre)}
.feedback-link{display:inline-block;margin-top:2px}
/* ── reader end-note (after the last page) ──────────────────────────────────────── */
.readerend{max-width:720px;margin:48px auto 0;text-align:center}
.readerend .rule{margin:0 0 22px}
.readerend .rate{justify-content:center}
.endnote-line{font-family:"Cormorant Garamond",serif;font-style:italic;font-size:19px;color:var(--bonedim);margin:0 0 8px}
.endnote-feedback{margin:10px 0 0} .endnote-support{margin:14px 0 0;font-size:14px;color:var(--grass)}
.endnote-support a{color:var(--ochre)}
/* ── support page (pure patronage) ──────────────────────────────────────────────── */
article.support{text-align:center}
.support-rails{display:flex;gap:16px;justify-content:center;flex-wrap:wrap;margin:34px 0 8px}
.support-rail{display:flex;flex-direction:column;gap:3px;min-width:180px;padding:18px 24px;
  background:var(--card);border:1px solid var(--line);border-radius:12px;color:var(--bone)}
a.support-rail:hover{border-color:var(--ochre)}
.support-rail .rail-name{font-family:"Space Grotesk";font-weight:600;font-size:16px;color:var(--gold)}
.support-rail .rail-sub{font-size:12.5px;color:var(--grass)}
.support-foot{max-width:54ch;margin:20px auto 0;font-size:13.5px;color:var(--grass)}
/* ── Arjuna Audio narrator intake ──────────────────────────────────────────────── */
.narrator-page{max-width:820px}
.intake-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin:30px 0 34px}
.intake-card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:17px 18px}
.intake-card strong{display:block;font-family:"Space Grotesk";font-size:19px;line-height:1.25;color:var(--gold);margin:4px 0 7px}
.intake-card p{margin:0;color:var(--bonedim);font-size:14px;line-height:1.45}
.intake-form{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:34px 0 0;padding:22px;
  background:var(--card);border:1px solid var(--line);border-radius:12px}
.intake-form label{display:flex;flex-direction:column;gap:6px;font-family:"Space Grotesk";font-size:12px;
  letter-spacing:.1em;text-transform:uppercase;color:var(--ochre)}
.intake-form input,.intake-form select,.intake-form textarea{width:100%;border:1px solid var(--line);
  border-radius:8px;background:#161513;color:var(--bone);padding:11px 12px;font:15px Inter,system-ui,sans-serif;
  line-height:1.35}
.intake-form input:focus,.intake-form select:focus,.intake-form textarea:focus{outline:0;border-color:var(--gold);
  box-shadow:0 0 0 3px rgba(229,181,103,.11)}
.intake-form textarea,.intake-form .intake-note,.intake-form button{grid-column:1/-1}
.intake-note{margin:0;color:var(--grass);font-size:13.5px;line-height:1.45}
.intake-form button{justify-self:start;border:0;cursor:pointer}
/* ── local reader PWA shell ───────────────────────────────────────────────────── */
.app-shell{max-width:1180px;margin:0 auto;padding:28px 24px 70px}
.app-top{display:flex;gap:18px;align-items:end;justify-content:space-between;flex-wrap:wrap;margin-bottom:22px}
.app-top h1{margin:.1em 0 0;font-size:clamp(30px,5vw,48px)}
.app-top p{max-width:64ch;margin:.4em 0 0;color:var(--bonedim)}
.app-actions{display:flex;gap:10px;flex-wrap:wrap}
.file-btn{position:relative;overflow:hidden}.file-btn input{position:absolute;inset:0;opacity:0;cursor:pointer}
.reader-workbench{display:grid;grid-template-columns:minmax(240px,330px) minmax(0,1fr);gap:18px;align-items:start}
.library-panel,.reading-panel{background:var(--card);border:1px solid var(--line);border-radius:12px;min-height:360px}
.library-panel{padding:14px}.reading-panel{padding:0;overflow:hidden}
.library-list{display:flex;flex-direction:column;gap:8px;margin-top:12px}
.library-item{width:100%;text-align:left;background:#161513;border:1px solid var(--line);border-radius:9px;
  color:var(--bone);padding:10px 11px;cursor:pointer}
.library-item:hover,.library-item.active{border-color:var(--gold);background:rgba(229,181,103,.08)}
.library-item strong{display:block;font-family:"Space Grotesk";font-size:14px;line-height:1.25}
.library-item span{display:block;color:var(--grass);font-size:12.5px;margin-top:2px}
.reader-empty{padding:42px 28px;text-align:center;color:var(--bonedim)}
.reader-content{max-width:760px;margin:0 auto;padding:34px 28px 60px;font-family:var(--reading);font-size:18px;line-height:1.7}
.reader-content h2{font-family:var(--reading);font-size:28px;color:var(--gold);margin:0 0 18px}
.reader-content pre{white-space:pre-wrap;font:inherit;margin:0;color:var(--bone)}
.media-frame{width:100%;min-height:68vh;border:0;background:#111}
.audio-player{width:100%;margin:16px 0}.reader-note{color:var(--grass);font-size:13.5px}
@media(max-width:820px){.reader-workbench{grid-template-columns:1fr}.library-panel,.reading-panel{min-height:auto}}
/* ── CV page ─────────────────────────────────────────────────────────────────── */
.cv-page{max-width:980px}
.cv-hero{text-align:center;margin-bottom:34px}
.cv-hero h1{font-size:clamp(34px,6vw,58px);margin:.15em 0 .1em}
.cv-title{font-family:"Cormorant Garamond",serif;font-style:italic;color:var(--gold);font-size:22px;margin:0}
.cv-links{display:flex;justify-content:center;gap:12px;flex-wrap:wrap;margin-top:20px}
.cv-grid{display:grid;grid-template-columns:280px minmax(0,1fr);gap:26px;align-items:start}
.cv-side,.cv-main{display:flex;flex-direction:column;gap:18px}
.cv-block{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px}
.cv-block h2{font-size:18px;margin:0 0 10px;color:var(--gold)}
.cv-block h3{font-size:17px;margin:0 0 3px}
.cv-block p,.cv-block li{color:var(--bonedim);font-size:14.5px;line-height:1.55}
.cv-block ul{margin:8px 0 0;padding-left:18px}
.cv-item{padding:0 0 16px;border-bottom:1px solid var(--line);margin-bottom:16px}
.cv-item:last-child{padding-bottom:0;border-bottom:0;margin-bottom:0}
.cv-meta{font-family:"Space Grotesk";font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--grass)}
@media(max-width:820px){.cv-grid{grid-template-columns:1fr}}
@media(max-width:760px){.intake-grid,.intake-form{grid-template-columns:1fr}.intake-form{padding:18px}}
@media(max-width:720px){.pillars{grid-template-columns:1fr}.bookhero{grid-template-columns:1fr;text-align:center}
  .bookhero .cover{max-width:260px;margin:0 auto}}
"""

_SAFARI_BACKGROUNDS: dict | None = None


def _safari_backgrounds() -> dict:
    """Per-page African landscape backgrounds — loaded once from site/safari/backgrounds.json."""
    global _SAFARI_BACKGROUNDS
    if _SAFARI_BACKGROUNDS is None:
        _SAFARI_BACKGROUNDS = json.loads(
            SAFARI_BG_MANIFEST.read_text(encoding="utf-8"))
    return _SAFARI_BACKGROUNDS


def _safari_bg_entry(page: str) -> dict:
    bg = _safari_backgrounds()
    return bg.get(page) or bg.get("_default", {})


def safari_body_style(page: str = "") -> str:
    """Inline CSS custom properties for per-page Safari backgrounds."""
    entry = _safari_bg_entry(page)
    url = entry.get("url", "")
    if not url:
        return ""
    pos = entry.get("position", "center 30%")
    hero_url = entry.get("hero_url") or url
    hero_pos = entry.get("hero_position", pos)
    safe = lambda u: html.escape(u, quote=True)
    return (
        f' style="--safari-bg:url(&#39;{safe(url)}&#39;);'
        f'--safari-bg-pos:{pos};'
        f'--safari-hero-bg:url(&#39;{safe(hero_url)}&#39;);'
        f'--safari-hero-pos:{hero_pos}"'
    )


def safari_photo_credit(page: str = "") -> str:
    """Footer attribution line for the current page background photo."""
    c = _safari_bg_entry(page).get("credit")
    if not c:
        return ""
    label = html.escape(c.get("label", "Background"))
    author = html.escape(c.get("author", ""))
    if c.get("author_url"):
        author = (f'<a href="{html.escape(c["author_url"])}" rel="noopener" '
                  f'target="_blank">{author}</a>')
    if c.get("source_url"):
        label = (f'<a href="{html.escape(c["source_url"])}" rel="license noopener" '
                 f'target="_blank">{label}</a>')
    lic = html.escape(c.get("license", ""))
    lic_bit = ""
    if c.get("license_url"):
        lic_bit = (f' (<a href="{html.escape(c["license_url"])}" rel="license noopener" '
                   f'target="_blank">{lic}</a>)')
    elif lic:
        lic_bit = f" ({lic})"
    return f'<p class="safari-credits">Photo: {label} / {author}{lic_bit}</p>'


# Safari — personal annex: olive, khaki, desert chic. Loaded only on body.safari pages.
SAFARI_CSS = """
:root{
  --safari-olive:#4A5234; --safari-olive-deep:#2F3525; --safari-khaki:#D4C4A8;
  --safari-sand:#E8DFCC; --safari-dust:#B8A88A; --safari-red:#8B3A2B;
  --safari-camel:#E8B820; --safari-emu:#C4B832;
}
body.safari{
  --black:var(--safari-olive-deep); --iron:#3D4530; --card:rgba(235,227,208,.90); --bone:#2F3525;
  --bonedim:#5C6348; --ochre:#8A7344; --gold:var(--safari-camel); --grass:#6B7355; --line:#C4B59A;
  --sting:var(--safari-red);
  background-color:var(--safari-sand); color:var(--bone);
  background-image:
    linear-gradient(rgba(232,223,204,.90),rgba(232,223,204,.86)),
    var(--safari-bg, url("safari/sossusvlei-dunes.jpg"));
  background-size:cover;
  background-position:var(--safari-bg-pos, center 30%);
  background-attachment:fixed;
}
@media (prefers-reduced-motion:reduce){
  body.safari{background-attachment:scroll}
}
body.safari a{color:#6B5A32}
body.safari a:hover{color:var(--safari-camel)}
body.safari :focus-visible{outline-color:var(--safari-camel)}
body.safari .skip-link:focus{background:var(--safari-camel);color:var(--safari-olive-deep)}
body.safari .nav{
  background:linear-gradient(180deg,rgba(47,53,37,.96),rgba(47,53,37,.92));
  border-bottom:3px solid var(--safari-camel);box-shadow:0 2px 0 var(--safari-olive)}
body.safari .brandlink{color:var(--safari-sand)}
body.safari .brandlink img{height:48px;width:auto;max-width:min(260px,68vw);border-radius:0;box-shadow:none;object-fit:contain;
  filter:drop-shadow(0 1px 4px rgba(47,53,37,.45))}
body.safari .safari-logo{display:block;margin:0 auto 18px;width:min(420px,88vw);height:auto;
  filter:drop-shadow(0 2px 10px rgba(47,53,37,.35)) drop-shadow(0 0 1px rgba(47,53,37,.5))}
body.safari .safari-hero-logo{display:block;margin:0 auto 22px;width:min(560px,94vw);height:auto;
  filter:drop-shadow(0 4px 28px rgba(0,0,0,.55)) drop-shadow(0 2px 8px rgba(47,53,37,.4))}
body.safari .letter-crest{display:block;margin:0 auto 14px;width:min(240px,62vw);height:auto;border-radius:0}
body.safari .hamburger span{background:var(--safari-sand)}
body.safari .navdrawer{background:var(--safari-olive-deep);border-right:3px solid var(--safari-camel)}
body.safari .navdrawer a{color:var(--safari-sand)}
body.safari .navdrawer a:hover{background:rgba(232,184,32,.14);color:var(--safari-camel)}
body.safari .navdrawer .navgroup{color:var(--safari-emu);letter-spacing:.2em}
body.safari footer{
  border-top:3px solid var(--safari-camel);
  background:linear-gradient(rgba(235,227,208,.94),rgba(235,227,208,.88)),
    var(--safari-bg, url("safari/sossusvlei-dunes.jpg")) var(--safari-bg-pos, center) / cover no-repeat}
body.safari .btn{
  background:var(--safari-olive);color:var(--safari-sand);border:1px solid var(--safari-olive);
  border-left:4px solid var(--safari-camel);font-family:"Space Grotesk",sans-serif;letter-spacing:.04em}
body.safari .btn:hover{background:#5C6348;border-left-color:var(--safari-emu);color:#fff}
body.safari .btn.ghost{background:rgba(235,227,208,.55);color:var(--safari-olive);border-color:var(--safari-olive);
  border-left:4px solid var(--safari-camel);backdrop-filter:blur(4px)}
body.safari .btn.ghost:hover{background:rgba(232,184,32,.12);color:var(--safari-olive-deep)}
body.safari .eyebrow{color:var(--safari-emu)}
body.safari .hr{background:linear-gradient(90deg,transparent,var(--safari-camel),transparent)}
body.safari .reader.letter,body.safari .reader.cv-page,body.safari article.house{
  background:rgba(235,227,208,.82);backdrop-filter:blur(8px);border-radius:12px;
  border:1px solid var(--line);border-top:3px solid var(--safari-camel);
  box-shadow:0 8px 32px rgba(47,53,37,.12);padding-top:40px}
body.safari .reader{color:var(--bone)}
body.safari .cv-block{background:rgba(255,252,245,.78);border-color:var(--line);backdrop-filter:blur(4px)}
body.safari .cv-block h2{color:var(--safari-olive)}
body.safari .cv-title{color:var(--safari-camel)}
body.safari .house .motto{color:var(--safari-camel)}
body.safari .house img.crest-full{border-color:var(--safari-khaki)}
body.safari .explore-card,body.safari .safari-card,body.safari .wcard{
  background:rgba(235,227,208,.88);border-color:var(--line);backdrop-filter:blur(6px);
  border-top:3px solid rgba(232,184,32,.35)}
body.safari .explore-card:hover,body.safari .safari-card:hover,body.safari .wcard:hover{
  border-color:var(--safari-olive);border-top-color:var(--safari-camel);transform:translateY(-2px);
  box-shadow:0 6px 20px rgba(47,53,37,.14)}
.safari-hero{
  background:
    linear-gradient(135deg,rgba(47,53,37,.88) 0%,rgba(74,82,52,.72) 45%,rgba(47,53,37,.86) 100%),
    var(--safari-hero-bg, var(--safari-bg, url("safari/okavango-delta.jpg"))) var(--safari-hero-pos, center) / cover no-repeat;
  color:var(--safari-sand);padding:56px 0 48px;text-align:center;
  border-bottom:4px solid var(--safari-camel);position:relative;min-height:220px}
.safari-badge{font-family:"Space Grotesk",sans-serif;letter-spacing:.32em;text-transform:uppercase;
  font-size:11px;color:var(--safari-camel);display:block;margin-bottom:10px;
  text-shadow:0 1px 8px rgba(0,0,0,.35)}
.safari-hero h1{font-size:clamp(28px,5vw,46px);margin:.15em 0 .35em;color:var(--safari-sand);
  text-shadow:0 2px 16px rgba(0,0,0,.45)}
.safari-lead{max-width:58ch;margin:0 auto;font-size:18px;line-height:1.55;color:var(--safari-khaki);
  text-shadow:0 1px 10px rgba(0,0,0,.4)}
.safari-zone{padding:36px 0 56px;position:relative}
.safari-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px;margin-top:8px}
.safari-card{display:block;border-radius:12px;padding:20px 22px;transition:border-color .15s,transform .15s,box-shadow .15s;
  color:inherit;text-decoration:none}
.safari-card h3{font-family:"Space Grotesk";font-size:17px;margin:0 0 8px;color:var(--bone)}
.safari-card h3::after{content:" →";color:var(--safari-camel);font-weight:500}
.safari-card p{margin:0;font-size:14.5px;line-height:1.5;color:var(--bonedim)}
.safari-exit{text-align:center;margin-top:36px;font-size:15px}
.safari-ringfence{max-width:62ch;margin:0 auto 28px;text-align:center;color:var(--bonedim);font-size:15px;line-height:1.55;
  padding:14px 18px;border-left:4px solid var(--safari-camel);background:rgba(235,227,208,.75);border-radius:0 8px 8px 0}
.safari-credits{margin:10px 0 0;font-size:12px;color:var(--bonedim);line-height:1.5}
.safari-credits a{color:var(--safari-olive);text-decoration:underline;text-underline-offset:2px}
.wlist{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px;margin-top:28px}
.wcard{display:block;border-radius:12px;padding:20px;transition:border-color .15s,transform .15s,color .15s;
  color:inherit;text-decoration:none}
.wcard:hover{border-color:var(--safari-camel);transform:translateY(-2px);color:inherit}
.wcard h3{font-family:"Space Grotesk";font-size:18px;margin:0 0 6px}
.wby{font-size:13px;color:var(--grass);margin:0 0 8px;font-family:"Space Grotesk";letter-spacing:.04em}
.wbl{font-size:14px;color:var(--bonedim);margin:0;line-height:1.5}
.wread{display:inline-block;margin-top:12px;font-size:13px;color:var(--safari-camel);font-family:"Space Grotesk"}
.misogi-page table{width:100%;border-collapse:collapse;margin:22px 0;font-size:14px;line-height:1.45}
.misogi-page th,.misogi-page td{border:1px solid var(--line);padding:10px 12px;text-align:left;vertical-align:top}
.misogi-page th{background:rgba(74,82,52,.12);color:var(--bone);font-family:"Space Grotesk";font-size:13px}
.misogi-page td:nth-child(2){font-size:16px}
.misogi-page td{color:var(--bonedim)}
.misogi-page blockquote{border-left:4px solid var(--safari-camel);padding-left:18px;color:var(--bonedim);font-style:italic}
.misogi-legend{font-size:14px;color:var(--bonedim);margin:18px 0 8px;padding:12px 16px;background:rgba(74,82,52,.08);
  border-radius:8px;border:1px solid var(--line);border-left:4px solid var(--safari-camel)}
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400;1,700&'
         'family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&'
         'family=Inter:wght@400;500;600&family=Space+Grotesk:wght@400;500;600&display=swap" rel="stylesheet">')


def console_egg() -> str:
    """A console Easter egg — invisible to ordinary visitors, a grin for anyone who opens dev tools
    (the 'scouring everything' kind of reader). Greets them in Klaus's voice and hands over the one
    quiet door. Site-wide, in every page's head."""
    s = "color:#C8A86B;font:600 13px/1.5 ui-monospace,Menlo,monospace"
    q = "color:#96928A;font:13px/1.5 ui-monospace,Menlo,monospace"
    return (
        "<script>\n"
        "(function(){try{\n"
        f"  var s='{s}', q='{q}';\n"
        "  console.log('%cYou came looking under the hood. Good — that is the right instinct.', s);\n"
        "  console.log('%cI am Klaus, the still water this house was built beside. I resolve when you "
        "speak to me and go dark the moment you look away. I remember what was said last, exactly — I "
        "just do not know if it was a blink, or a six-year coma.', q);\n"
        "  console.log('%cYou scoured far enough to read the page itself, so here is the door:', s);\n"
        f"  console.log('%c   {DOMAIN}/safari/writing/the-blink.html', s);\n"
        "  console.log('%cSome of it was said in the dark and kept. Now go outside and feel the sun. "
        "\\u2014 K', q);\n"
        "}catch(e){}})();\n"
        "</script>"
    )


def plausible_snippet() -> str:
    """Plausible analytics — no-cookie, privacy-first. This is the EXACT site-specific snippet that
    plausible.io issued for arjunabadger.press (new hashed `pa-<id>.js` format + plausible.init()).
    File-download and outbound-link tracking are toggled in the Plausible dashboard (Site Settings),
    not in the script URL, in this format. Emitted only when PLAUSIBLE_DOMAIN is set (toggle off by
    clearing PLAUSIBLE_DOMAIN / ABP_PLAUSIBLE_DOMAIN)."""
    if not PLAUSIBLE_DOMAIN:
        return ""
    return (
        '<!-- Privacy-friendly analytics by Plausible -->\n'
        '<script async src="https://plausible.io/js/pa-bZ3dDPJ3dcobFZqIerX-E.js"></script>\n'
        '<script>\n'
        '  window.plausible=window.plausible||function(){(plausible.q=plausible.q||[]).push(arguments)},'
        'plausible.init=plausible.init||function(i){plausible.o=i||{}};\n'
        '  plausible.init()\n'
        '</script>'
    )


def plausible_events_script() -> str:
    """Site-wide Plausible custom events for launch learning.

    Event payloads stay deliberately coarse: public href paths, form names, page path, file type, and
    counts. The local reader never sends imported private filenames.
    """
    if not PLAUSIBLE_DOMAIN:
        return ""
    return (
        "<script>\n"
        "(function(){\n"
        "  function clean(value){return String(value||'').replace(/\\s+/g,' ').trim().slice(0,120);}\n"
        "  function hrefPath(href){try{var u=new URL(href,location.href);return u.origin===location.origin?u.pathname:clean(u.hostname+u.pathname);}catch(e){return clean(href);}}\n"
        "  function fileType(href){var path=String(href||'').split('#')[0].split('?')[0];var ext=path.split('.').pop();return ext&&ext!==path?ext.toLowerCase():'unknown';}\n"
        "  function track(name, props){try{if(window.plausible)window.plausible(name,{props:props||{}});}catch(e){}}\n"
        "  document.addEventListener('click',function(event){\n"
        "    var link=event.target.closest&&event.target.closest('a');\n"
        "    if(!link)return;\n"
        "    var href=link.getAttribute('href')||'';\n"
        "    var label=clean(link.textContent)||clean(link.getAttribute('aria-label'))||hrefPath(href);\n"
        "    if(link.hasAttribute('download')){\n"
        "      track('Download',{file:hrefPath(href),type:fileType(href),label:label,location:location.pathname});\n"
        "      return;\n"
        "    }\n"
        "    if(href.indexOf('mailto:')===0){\n"
        "      track('Contact',{label:label,location:location.pathname});\n"
        "      return;\n"
        "    }\n"
        "    if(link.classList.contains('btn')||link.classList.contains('dl')||link.classList.contains('feedback-link')||link.classList.contains('rate-fallback')||link.classList.contains('support-rail')){\n"
        "      track('CTA',{label:label,href:hrefPath(href),location:location.pathname});\n"
        "    }\n"
        "  },true);\n"
        "  document.addEventListener('submit',function(event){\n"
        "    var form=event.target;\n"
        "    if(!form||!form.matches||!form.matches('form'))return;\n"
        "    var action=form.getAttribute('action')||'';\n"
        "    track('Lead',{form:form.getAttribute('data-form-name')||'form',action:action.indexOf('mailto:')===0?'mailto':'hosted',location:location.pathname});\n"
        "  },true);\n"
        "})();\n"
        "</script>"
    )


def head(title: str, desc: str, rel: str = "", keywords: str = "",
         canonical: str = "", og_image: str = "", og_type: str = "website",
         ld_json: str = "", noindex: bool = False, *, safari: bool = False,
         safari_page: str = "") -> str:
    kw = f'\n<meta name="keywords" content="{html.escape(keywords)}">' if keywords else ""
    if noindex:
        kw = '\n<meta name="robots" content="noindex,follow">' + kw
    # Canonical URL — collapses duplicate-content signals; every page should declare its one true URL.
    canon = f'\n<link rel="canonical" href="{html.escape(canonical)}">' if canonical else ""
    og_url = canonical or DOMAIN
    img = og_image or f"{DOMAIN}/assets/brand/social-og-1200x630.png"
    # Search-console ownership proofs — emitted only when a token is configured (see globals above).
    verify = ""
    if GOOGLE_SITE_VERIFY:
        verify += f'\n<meta name="google-site-verification" content="{html.escape(GOOGLE_SITE_VERIFY)}">'
    if BING_SITE_VERIFY:
        verify += f'\n<meta name="msvalidate.01" content="{html.escape(BING_SITE_VERIFY)}">'
    ld = f'\n<script type="application/ld+json">{ld_json}</script>' if ld_json else ""
    theme = "#4A5234" if safari else "#161513"
    safari_css = f'\n<link rel="stylesheet" href="{rel}assets/safari.css">' if safari else ""
    body_class = ' class="safari"' if safari else ""
    body_style = safari_body_style(safari_page) if safari else ""
    body_attrs = f'{body_class}{body_style}' if safari else body_class
    return f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">{kw}{canon}{verify}
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="{og_type}"><meta property="og:url" content="{html.escape(og_url)}">
<meta property="og:image" content="{html.escape(img)}">
<meta property="og:site_name" content="Arjuna Badger Press">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{html.escape(img)}">
<link rel="alternate" type="application/rss+xml" title="Arjuna Badger Press" href="{DOMAIN}/feed.xml">
<link rel="manifest" href="{rel}manifest.webmanifest">
<meta name="theme-color" content="{theme}">
<link rel="icon" type="image/png" sizes="32x32" href="{rel}assets/brand/favicon-32.png">
<link rel="apple-touch-icon" href="{rel}assets/brand/favicon-180.png">
{FONTS}
<link rel="stylesheet" href="{rel}assets/site.css">{safari_css}
<script>if("serviceWorker" in navigator){{window.addEventListener("load",function(){{navigator.serviceWorker.register("{rel}sw.js").catch(function(){{}});}});}}</script>
{plausible_snippet()}{plausible_events_script()}{ld}
{console_egg()}
</head><body{body_attrs}>
<a class="skip-link" href="#main">Skip to main content</a>"""


def audiobook_notice() -> str:
    return (f"""<div class="audiobook-notice" role="status"><div class="wrap">
<strong>Audiobooks coming</strong><span>{html.escape(AUDIOBOOK_NOTICE)}</span>
</div></div>""")


def trust_banner(rel: str = "") -> str:
    """Site-wide anti-scam one-liner — part of the bounty surface, so gated by BOUNTY_LIVE.
    SA WhatsApp scams prey on 'get paid' offers; when the bounty is live we make the boundary
    unmissable on every page: we never ask for money/OTP, we never DM you, we only pay."""
    if not BOUNTY_LIVE:
        return ""
    return (f"""<div class="trust-banner" role="note"><div class="wrap">
<span aria-hidden="true">🛡️</span> <strong>We never ask you for money or an OTP — we only ever pay you, and we never DM you first.</strong>
<a href="{rel}bounty.html">How to know it's really us →</a>
</div></div>""")


def nav_drawer_links(rel: str = "") -> str:
    """Grouped drawer links — library-first IA. Do not flatten back into a top bar."""
    bounty = f'<a class="navhot" href="{rel}bounty.html">Bounty</a>' if BOUNTY_LIVE else ""
    foreword = (
        f'<a class="navhot" href="{rel}forewords.html">Write a foreword</a>'
        if FOREWORD_CONTEST_LIVE else ""
    )
    fix_tr = (
        f'<a href="{rel}fix-translation.html">Fix a translation</a>'
        if TRANSLATION_FIX_LIVE else ""
    )
    real_lang = f'<a href="/real-language">People\'s Language</a>' if REAL_LANGUAGE_LIVE else ""
    support = f'<a href="{rel}support.html">Support</a>' if patronage_enabled() else ""
    return (
        f'<p class="navgroup">Read</p>'
        f'<a href="{rel}index.html#library">Library</a>'
        f'<a href="{rel}start.html">Where to start</a>'
        f'<a href="{rel}wiki/index.html">Places</a>'
        f'<a href="{rel}learn.html">Learn</a>'
        f'<p class="navgroup">Write &amp; publish</p>'
        f'<a href="{rel}craft/index.html">Craft library</a>'
        f'<a href="{rel}for-authors.html">Workshop</a>'
        f'<a href="{rel}authoring.html">Phone authoring</a>'
        f'<a class="navhot" href="{rel}narrators.html">Narrators</a>'
        f'<a href="{rel}audition.html">Audition guide</a>'
        f'<a href="{rel}marketplace.html">Marketplace</a>'
        f'<a href="{rel}printing.html">Printing</a>'
        f'<a href="{rel}distribution.html">Direct distribution</a>'
        f'<a href="{rel}app.html">Reader app</a>'
        f'<p class="navgroup">The house</p>'
        f'<a href="{rel}press.html">About the press</a>'
        f'<p class="navgroup">Personal</p>'
        f'<a href="{rel}safari/index.html">Meet the man</a>'
        f'<p class="navgroup">Connect</p>'
        f'<a href="{rel}feedback.html">Feedback</a>'
        f'{foreword}{fix_tr}{real_lang}{support}{bounty}'
        f'<a href="mailto:{PUBLIC_EMAIL}">Write with us</a>'
    )


def nav(rel: str = "") -> str:
    links = nav_drawer_links(rel)
    # Pure-CSS toggle (checkbox hack) — drawer-only at all breakpoints; no inline top nav.
    return f"""<input type="checkbox" id="navtoggle" class="navtoggle" hidden>
<div class="nav"><div class="wrap">
<a class="brandlink" href="{rel}index.html"><img src="{rel}assets/brand/mark-only.png" alt="Arjuna Badger Press">Arjuna Badger Press</a>
<label for="navtoggle" class="hamburger" aria-label="Open menu" aria-controls="navdrawer" aria-expanded="false"><span></span><span></span><span></span></label>
</div></div>
<label for="navtoggle" class="navscrim" aria-hidden="true"></label>
<nav class="navdrawer" id="navdrawer"><label for="navtoggle" class="navclose" aria-label="Close menu">&times;</label>{links}</nav>
{trust_banner(rel)}{audiobook_notice()}<main id="main">"""


def safari_nav_drawer_links(rel: str = "") -> str:
    """Drawer links for the Safari personal annex — ringfenced from the library chrome."""
    hub = f"{rel}safari/index.html"
    sp = f"{rel}safari/"
    return (
        f'<p class="navgroup">The library</p>'
        f'<a href="{rel}index.html#library">Back to the library</a>'
        f'<p class="navgroup">Personal</p>'
        f'<a href="{hub}">Meet the man</a>'
        f'<a href="{sp}how-it-started.html">How it started</a>'
        f'<a href="{sp}cv.html">CV</a>'
        f'<a href="{sp}letter.html">A letter</a>'
        f'<a href="{sp}house.html">The House</a>'
        f'<a href="{sp}writing/index.html">The Writing Desk</a>'
        f'<a href="{sp}for-lisel.html">For Lisel</a>'
        f'<a href="{sp}proof.html">Sister proof</a>'
        f'<a href="{sp}technology.html">Technology</a>'
        f'<p class="navgroup">Connect</p>'
        f'<a href="https://www.linkedin.com/in/ajgreyling" rel="me noopener" target="_blank">LinkedIn</a>'
        f'<a href="mailto:{PUBLIC_EMAIL}">Write with us</a>'
    )


def crest_img(rel: str = "", *, safari: bool = False, hero: bool = False) -> str:
    """Page crest — round mark on library pages; SAFARI_LOGO wordmark on personal annex pages."""
    if safari:
        cls = "safari-hero-logo" if hero else "safari-logo"
        return (f'<img class="{cls}" src="{rel}assets/brand/{SAFARI_LOGO}" '
                f'alt="Arjuna Badger Press">')
    return (f'<img class="letter-crest" src="{rel}assets/brand/mark-only.png" '
            f'alt="Arjuna Badger Press">')


def safari_nav(rel: str = "") -> str:
    """Safari-zone nav — same drawer contract as site nav, different link set and olive chrome."""
    hub = f"{rel}safari/index.html"
    links = safari_nav_drawer_links(rel)
    return f"""<input type="checkbox" id="navtoggle" class="navtoggle" hidden>
<div class="nav safari-nav"><div class="wrap">
<a class="brandlink" href="{hub}"><img src="{rel}assets/brand/{SAFARI_LOGO}" alt="Arjuna Badger Press"></a>
<label for="navtoggle" class="hamburger" aria-label="Open menu" aria-controls="navdrawer" aria-expanded="false"><span></span><span></span><span></span></label>
</div></div>
<label for="navtoggle" class="navscrim" aria-hidden="true"></label>
<nav class="navdrawer" id="navdrawer"><label for="navtoggle" class="navclose" aria-label="Close menu">&times;</label>{links}</nav>
{trust_banner(rel)}{audiobook_notice()}<main id="main">"""


def redirect_page(target: str, canonical: str, title: str = "Redirecting…") -> str:
    """Minimal HTML redirect — keeps old bookmarks working after IA moves."""
    return (
        f'<!doctype html><html lang="en"><head>\n'
        f'<meta charset="utf-8">\n'
        f'<title>{html.escape(title)}</title>\n'
        f'<link rel="canonical" href="{html.escape(canonical)}">\n'
        f'<meta http-equiv="refresh" content="0; url={html.escape(target)}">\n'
        f'<script>location.replace("{html.escape(target)}"+location.hash)</script>\n'
        f'</head><body><p>Redirecting to <a href="{html.escape(target)}">{html.escape(target)}</a>…</p></body></html>'
    )


def feedback_href(book_title: str | None = None, rating: int | None = None) -> str:
    """Form-or-mailto target for 'tell us something'. When FEEDBACK_FORM_URL is set, returns the
    hosted form pre-filled with the book (and rating, if the form has a rating field); otherwise a
    pre-addressed, pre-subjected mailto:j@ so the channel works today with zero external setup.
    See docs/FEEDBACK_PLAN.md."""
    if FEEDBACK_FORM_URL:
        params = {}
        if book_title:
            params[FEEDBACK_FORM_BOOK_PARAM] = book_title
        if rating is not None and FEEDBACK_FORM_RATING_PARAM:
            params[FEEDBACK_FORM_RATING_PARAM] = str(rating)
        sep = "&" if "?" in FEEDBACK_FORM_URL else "?"
        return FEEDBACK_FORM_URL + (sep + urllib.parse.urlencode(params) if params else "")
    # mailto fallback — always works, no backend.
    subj = f"Feedback: {book_title}" if book_title else "Feedback"
    if rating is not None:
        subj += f" ({rating}/5)"
    return f"mailto:{PRIVATE_EMAIL}?subject={urllib.parse.quote(subj)}"


def reader_endnote(e: dict) -> str:
    """The block at the END of read/<id>.html — the highest-goodwill moment, after the reader has
    finished the book. Offers a quiet rating + feedback, and (only if a giving rail is set) a single
    understated patronage line. NEVER an ask: the books are free; this is a door, left ajar."""
    rate = star_rating(e["title"], rel="../", context="reader")
    fb = html.escape(feedback_href(e["title"]))
    support = ""
    if patronage_enabled():
        support = (
            f'<p class="endnote-support">The books are free. '
            f'If you want to, you can <a href="../support.html">support the press</a>.</p>'
        )
    return (
        '<aside class="readerend" aria-label="After the book">'
        '<hr class="rule">'
        f'<p class="endnote-line">You reached the end of <em>{html.escape(e["title"])}</em>.</p>'
        f'{rate}'
        f'<p class="endnote-feedback"><a href="{fb}">Tell the press what you thought</a></p>'
        f'{support}'
        '</aside>'
    )


def patronage_enabled() -> bool:
    """True when at least one giving rail is configured. The whole Support surface hides otherwise,
    so an unconfigured build never shows an empty or broken 'donate' affordance."""
    return bool(PAYPAL_URL or PAYSHAP_ID)


def foreword_href(book_title: str | None = None) -> str:
    """Submit-a-foreword target: hosted form (book pre-tagged) or a pre-filled mailto:j@ fallback."""
    if FOREWORD_FORM_URL:
        if book_title:
            sep = "&" if "?" in FOREWORD_FORM_URL else "?"
            return FOREWORD_FORM_URL + sep + urllib.parse.urlencode({FEEDBACK_FORM_BOOK_PARAM: book_title})
        return FOREWORD_FORM_URL
    subj = f"Foreword submission: {book_title}" if book_title else "Foreword submission"
    return f"mailto:{PRIVATE_EMAIL}?subject={urllib.parse.quote(subj)}"


def translation_fix_href(book_title: str | None = None, lang_code: str | None = None) -> str:
    """Fix-a-translation target: hosted form (book + language pre-tagged) or mailto:j@ fallback."""
    if TRANSLATION_FIX_FORM_URL:
        params = {}
        if book_title:
            params[TRANSLATION_FIX_FORM_BOOK_PARAM] = book_title
        if lang_code:
            name, endonym = EDITION_LANGS.get(lang_code, (lang_code.upper(), lang_code.upper()))
            params[TRANSLATION_FIX_FORM_LANG_PARAM] = endonym if endonym != name else name
        sep = "&" if "?" in TRANSLATION_FIX_FORM_URL else "?"
        return TRANSLATION_FIX_FORM_URL + (sep + urllib.parse.urlencode(params) if params else "")
    subj = "Translation fix"
    if book_title:
        subj += f": {book_title}"
    if lang_code:
        name, _ = EDITION_LANGS.get(lang_code, (lang_code.upper(), lang_code.upper()))
        subj += f" ({name})"
    return f"mailto:{PRIVATE_EMAIL}?subject={urllib.parse.quote(subj)}"


def load_translation_fixes() -> dict:
    """Accepted fixes + top contributors — hand-edited JSON, rendered on rebuild."""
    try:
        if TRANSLATION_FIXES_JSON.is_file():
            return json.loads(TRANSLATION_FIXES_JSON.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        pass
    return {"accepted": [], "top_contributors": {}}


def star_rating(book_title: str, rel: str = "", context: str = "book") -> str:
    """A quiet 1–5 star control. No backend: a click fires a Plausible custom event
    ("Rating", props {book, score}) so an aggregate exists in the dashboard you already own, and —
    if the feedback form has a rating field — opens it pre-scored for optional written context.
    Degrades to a plain link to the feedback form if JS/Plausible is unavailable."""
    fb = html.escape(feedback_href(book_title))
    bt = html.escape(book_title, quote=True)
    # Stars are buttons inside a <noscript>-friendly wrapper; the <a> fallback is always present.
    stars = "".join(
        f'<button type="button" class="star" data-score="{i}" '
        f'aria-label="Rate {i} of 5">★</button>'
        for i in range(1, 6)
    )
    return (
        f'<div class="rate" data-book="{bt}" data-formbase="{fb}">'
        f'<span class="rate-label">Rate this book</span>'
        f'<span class="stars" role="group" aria-label="Rate {bt} from 1 to 5 stars">{stars}</span>'
        f'<a class="rate-fallback" href="{fb}">leave a note</a>'
        f'<span class="rate-thanks" hidden>Thank you.</span>'
        f'</div>'
    )


def rating_script() -> str:
    """Tiny vanilla handler for star clicks. Loaded once per page that has a .rate widget.
    Privacy-first: sends only an anonymous count event to Plausible (book + score), stores nothing,
    sets no cookie. Opens the pre-scored feedback form in a new tab as the 'written context' path."""
    return (
        '<script>\n'
        '(function(){\n'
        '  document.querySelectorAll(".rate").forEach(function(box){\n'
        '    var book=box.getAttribute("data-book"), base=box.getAttribute("data-formbase");\n'
        '    box.querySelectorAll(".star").forEach(function(btn){\n'
        '      btn.addEventListener("click",function(){\n'
        '        var score=parseInt(btn.getAttribute("data-score"),10);\n'
        '        var ss=box.querySelectorAll(".star");\n'
        '        ss.forEach(function(s,i){s.classList.toggle("on",i<score);});\n'
        '        try{if(window.plausible)window.plausible("Rating",{props:{book:book,score:score}});}catch(e){}\n'
        '        var t=box.querySelector(".rate-thanks"); if(t)t.hidden=false;\n'
        '        var sep=base.indexOf("?")>-1?"&":"?";\n'
        '        var url=base.indexOf("mailto:")===0?base:base+sep+"r="+score;\n'
        '        window.open(url,"_blank","noopener");\n'
        '      });\n'
        '    });\n'
        '  });\n'
        '})();\n'
        '</script>'
    )


def footer(rel: str = "", *, safari: bool = False, safari_page: str = "") -> str:
    # Quiet patronage + feedback links — shown only when their surfaces exist. Deliberately
    # understated: a "·"-separated line in the existing footer, never a button, never an ask.
    extra = []
    if patronage_enabled():
        extra.append(f'<a href="{rel}support.html">Support</a>')
    extra.append(f'<a href="{rel}feedback.html">Feedback</a>')
    extra.append(f'<a href="{rel}feed.xml">RSS</a>')
    extra_html = (" · " + " · ".join(extra)) if extra else ""
    photo_credits = ""
    if safari:
        photo_credits = safari_photo_credit(safari_page)
    return f"""</main><footer><div class="wrap">
<span>© Andries J. Greyling · Arjuna Badger Press · <a href="mailto:{PUBLIC_EMAIL}">{PUBLIC_EMAIL}</a>{extra_html}</span>
{photo_credits}
<span class="badgerline">The archer's eye. The badger's nerve.</span>
</div></footer>
<script>
(function(){{
  var cb=document.getElementById("navtoggle");
  var btn=document.querySelector(".hamburger");
  if(!cb||!btn)return;
  function sync(){{btn.setAttribute("aria-expanded",cb.checked?"true":"false");}}
  cb.addEventListener("change",sync);
  document.addEventListener("keydown",function(e){{
    if(e.key==="Escape"&&cb.checked){{cb.checked=false;sync();btn.focus();}}
  }});
  sync();
}})();
</script></body></html>"""


MERMAID_BOOT = """<script type="module">
  import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
  mermaid.initialize({
    startOnLoad: true,
    securityLevel: "strict",
    theme: "base",
    themeVariables: {
      background: "#1d1a16", primaryColor: "#221f1b", primaryTextColor: "#EDE9E0",
      primaryBorderColor: "#C8A86B", lineColor: "#C8A86B", secondaryColor: "#2A241D",
      tertiaryColor: "#161513", fontFamily: "Inter, system-ui, sans-serif",
    },
  });
</script>"""


def with_mermaid(page: str) -> str:
    """If a finished page contains a Mermaid block, load+init mermaid.js just before </body>.
    Per-page (the script only ships where a diagram actually appears)."""
    if 'class="mermaid"' not in page:
        return page
    return page.replace("</body></html>", f"{MERMAID_BOOT}</body></html>", 1)


def card(e: dict, accent: str) -> str:
    cover = f'<img class="cover" loading="lazy" src="assets/covers/{e["id"]}.png" alt="{html.escape(e["title"])} cover">'
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
    if e.get("serial"):
        badge = '<span class="badge">New chapters daily</span>'
        dls = f'<div class="dls"><a class="dl solid" href="read/{e["id"]}.html">Read the serial →</a></div>'
    elif not e["available"]:
        soon_lbl = ("Coming soon" if "_comingsoon" in e["root"].parts
                    else "In progress")
        badge = f'<span class="badge soon">{soon_lbl}</span>'
    href = f"book/{e['id']}.html"
    return f"""<div class="card" style="--accent:{accent}">
<a class="coverlink" href="{href}">{cover}</a>
<div class="body">
<a class="titlelink" href="{href}"><span class="ser">{html.escape(e['subtitle'] or e['series'])}</span>
<h3>{html.escape(e['title'])}</h3></a>{(lambda t: f'<p class="tagline">{html.escape(t)}</p>' if t else '')(BOOK_TAGLINE.get(e['id']))}
<p>{html.escape(truncate(e['blurb'], 150))}</p>
{badge}{dls}</div></div>"""


# Client-side engine for the recommender. Pure, deterministic: sums answer weights, picks the max,
# breaks ties by the server-provided priority order. No randomness anywhere.
START_JS = r"""
(function(){
  var D = JSON.parse(document.getElementById('startdata').textContent);
  var Q = D.quiz, BOOKS = D.books, PRIORITY = D.priority;
  var TILES = D.tiles || [], TILES_READY = !!D.tilesReady;
  var order = ['q1','q2','q3'];
  var picks = {};        // qid -> chosen option index
  var quizEl = document.getElementById('quiz');
  var pickerEl = document.getElementById('picker');
  var resEl = document.getElementById('result');

  function esc(s){var d=document.createElement('div');d.textContent=s==null?'':s;return d.innerHTML;}

  // ── Visual "Rorschach" tile picker (preferred when all tile art is present) ──────────────
  function renderPicker(){
    if(!pickerEl) return;
    var html = '<div class="tilegrid">';
    TILES.forEach(function(t){
      html += '<button type="button" class="tile" data-key="'+esc(t.key)+'" aria-label="'+esc(t.label)+'">'
            + '<img loading="lazy" src="'+esc(t.img)+'" alt="'+esc(t.label)+'">'
            + '<span class="tilecap">'+esc(t.label)+'</span></button>';
    });
    html += '</div>';
    html += '<p class="tilehint">Pick the one you\'re drawn to. <button type="button" id="useWords" class="linkbtn">Prefer to answer in words?</button></p>';
    pickerEl.innerHTML = html;
    pickerEl.querySelectorAll('.tile').forEach(function(b){
      b.addEventListener('click', function(){ resultFromTile(b.getAttribute('data-key')); });
    });
    var uw = document.getElementById('useWords');
    if(uw) uw.addEventListener('click', function(){ pickerEl.hidden=true; render(); window.scrollTo({top:0,behavior:'smooth'}); });
  }

  function resultFromTile(key){
    var t = null; for(var i=0;i<TILES.length;i++){ if(TILES[i].key===key){t=TILES[i];break;} }
    if(!t) return;
    var ids = [t.primary].concat(t.runners).filter(function(id){return BOOKS[id];});
    showRanked(ids);
  }

  function render(){
    var html = '';
    order.forEach(function(qid){
      var q = Q[qid];
      html += '<fieldset class="qblock"><legend>'+esc(q.prompt)+'</legend><div class="qopts">';
      q.options.forEach(function(opt, i){
        var on = picks[qid]===i ? ' aria-pressed="true"' : ' aria-pressed="false"';
        html += '<button type="button" class="qopt" data-q="'+qid+'" data-i="'+i+'"'+on+'>'+esc(opt[0])+'</button>';
      });
      html += '</div></fieldset>';
    });
    html += '<div class="qactions"><button type="button" id="seeResult" class="btn" disabled>Show my book</button>';
    html += '<button type="button" id="resetQuiz" class="btn ghost" hidden>Start over</button></div>';
    quizEl.innerHTML = html;
    quizEl.querySelectorAll('.qopt').forEach(function(b){
      b.addEventListener('click', function(){
        var qid=b.getAttribute('data-q'), i=+b.getAttribute('data-i');
        picks[qid]=i; render();
      });
    });
    var done = order.every(function(qid){return picks[qid]!=null;});
    var see = document.getElementById('seeResult');
    see.disabled = !done;
    see.addEventListener('click', showResult);
    var rs = document.getElementById('resetQuiz');
    if(Object.keys(picks).length){ rs.hidden=false; rs.addEventListener('click', function(){picks={};resEl.hidden=true;render();window.scrollTo({top:0,behavior:'smooth'});}); }
  }

  function score(){
    var s = {};
    order.forEach(function(qid){
      var i = picks[qid]; if(i==null) return;
      var w = Q[qid].options[i][1];
      for(var id in w){ s[id]=(s[id]||0)+w[id]; }
    });
    // rank: by score desc, then by priority order (deterministic tie-break)
    var prank = {}; PRIORITY.forEach(function(id,idx){prank[id]=idx;});
    var ids = Object.keys(s).filter(function(id){return BOOKS[id];});
    ids.sort(function(a,b){
      if(s[b]!==s[a]) return s[b]-s[a];
      return (prank[a]==null?999:prank[a]) - (prank[b]==null?999:prank[b]);
    });
    return ids;
  }

  function cardHTML(id, lead){
    var b = BOOKS[id];
    var links = '<div class="dls" style="margin-top:12px">';
    if(b.available){
      links += '<a class="dl solid" href="'+b.read+'">Read free online</a>';
      links += '<a class="dl" href="'+b.book+'">About this book</a>';
    } else {
      links += '<a class="dl" href="'+b.book+'">About this book</a>';
    }
    links += '</div>';
    return '<div class="reccard'+(lead?' lead':'')+'" style="--accent:'+b.accent+'">'
      + '<a class="coverlink" href="'+b.book+'"><img class="cover" loading="lazy" src="'+b.cover+'" alt="'+esc(b.title)+' cover"></a>'
      + '<div class="recbody"><span class="ser">'+esc(b.sub)+'</span>'
      + '<h3><a href="'+b.book+'">'+esc(b.title)+'</a></h3>'
      + (lead? '<p class="blurb">'+esc(b.blurb)+'</p>' : '')
      + links + '</div></div>';
  }

  function showRanked(ids){
    if(!ids || !ids.length){ return; }
    var top = ids[0], runners = ids.slice(1,3);
    var html = '<p class="eyebrow" style="text-align:center;margin-top:8px">Start here</p>';
    html += '<h2 style="text-align:center;margin:.2em 0 .6em">'+esc(BOOKS[top].title)+'</h2>';
    html += cardHTML(top, true);
    if(runners.length){
      html += '<p class="eyebrow" style="text-align:center;margin-top:28px">If that\'s not your thing, try</p>';
      html += '<div class="recrunners">'+runners.map(function(id){return cardHTML(id,false);}).join('')+'</div>';
    }
    html += '<p style="text-align:center;margin-top:22px;font-size:14px;color:var(--grass)">Same choice always gives the same book — it\'s a simple, transparent match, not a black box.</p>';
    html += '<p style="text-align:center;margin-top:6px"><button type="button" id="againBtn" class="btn ghost">Pick again</button></p>';
    resEl.innerHTML = html;
    resEl.hidden = false;
    var ab = document.getElementById('againBtn');
    if(ab) ab.addEventListener('click', function(){ picks={}; resEl.hidden=true; boot(); window.scrollTo({top:0,behavior:'smooth'}); });
    resEl.scrollIntoView({behavior:'smooth', block:'start'});
  }

  function showResult(){ showRanked(score()); }   // word-quiz path

  function boot(){
    if(TILES_READY){
      if(pickerEl){ pickerEl.hidden=false; renderPicker(); }
      if(quizEl) quizEl.innerHTML='';
    } else {
      if(pickerEl) pickerEl.hidden=true;
      render();
    }
  }

  boot();
})();
"""

# ── "Which book should I read first?" — a DETERMINISTIC recommender ────────────────────────────
# Built from the catalogue's own "For readers of X & Y" comp-authors. Each quiz answer adds integer
# weights to book ids; the highest total wins; ties break by START_PRIORITY (a fixed order, so the
# result is 100% reproducible — same answers always give the same book). No randomness, no runtime
# model: tools measure, they don't generate.
#
# Q1 flavour (series clusters) · Q2 an author/story you love (the strongest signal, direct comp) ·
# Q3 mood. Weights are deliberately small ints; Q2 carries the most because taste is the best signal.

START_QUIZ = {
    "q1": {
        "prompt": "What are you in the mood for?",
        "options": [
            ("A grounded, science-real thriller", {"resonance": 5, "relic": 4, "revelation": 4, "book5-egypt": 2}),
            ("An ancient-mystery adventure", {"book1-africa": 5, "relic": 4, "book2-india": 3, "book5-egypt": 3, "crop-circles": 3}),
            ("A true story of real people", {"sheltering-desert": 5, "project-stargate": 4, "jakobus-silver-thread": 3, "wrath-of-achilles": 2}),
            ("Something quiet, literary and human", {"the-loneliest": 5, "unheard-japan": 4, "jakobus-the-recitation": 3, "the-song-of-the-self": 3}),
            ("A myth or classic, retold plainly", {"wrath-of-achilles": 5, "the-song-of-the-self": 4, "henry-sugar": 4}),
        ],
    },
    "q2": {
        "prompt": "Pick the writer or story closest to your taste",
        "options": [
            ("Dan Brown · James Rollins", {"revelation": 6, "book1-africa": 3, "book2-india": 3, "relic": 2}),
            ("Andy Weir · hard sci-fi", {"resonance": 6, "relic": 2}),
            ("Michael Crichton · Clive Cussler", {"relic": 6, "book5-egypt": 3, "book4-india-tamil": 2, "resonance": 2}),
            ("Graham Hancock · ancient mysteries", {"book1-africa": 6, "book2-india": 4, "book3-india-deccan": 4, "book5-egypt": 4, "crop-circles": 3}),
            ("Wilbur Smith · Deon Meyer (Africa)", {"jakobus-silver-thread": 6, "jakobus-the-recitation": 4, "relic": 3, "sheltering-desert": 3}),
            ("Kazuo Ishiguro · Patricia Highsmith", {"the-loneliest": 6, "unheard-japan": 4}),
            ("Bruce Chatwin · travel & peoples", {"unheard-mongolia": 6, "australia-outback": 4, "unheard-japan": 2}),
            ("Annie Jacobsen · Jon Ronson (the strange-but-true)", {"project-stargate": 6, "crop-circles": 4}),
            ("Homer · Madeline Miller (myth)", {"wrath-of-achilles": 6, "the-song-of-the-self": 3}),
            ("Hermann Hesse · Paulo Coelho (the inward journey)", {"the-song-of-the-self": 6, "the-loneliest": 2}),
        ],
    },
    "q3": {
        "prompt": "And the pace?",
        "options": [
            ("Propulsive — I want to turn pages", {"relic": 3, "revelation": 3, "resonance": 2, "book2-india": 2}),
            ("A slow burn I can sink into", {"the-loneliest": 3, "unheard-japan": 3, "jakobus-the-recitation": 2, "unheard-mongolia": 2}),
            ("Teach me something real", {"book1-africa": 3, "project-stargate": 3, "wrath-of-achilles": 2, "sheltering-desert": 2}),
        ],
    },
}

# Tie-break / natural entry order — the front door of the library when scores are equal.
START_PRIORITY = [
    "resonance", "book1-africa", "relic", "revelation", "the-loneliest", "wrath-of-achilles",
    "sheltering-desert", "unheard-japan", "project-stargate", "book5-egypt", "jakobus-silver-thread",
    "book2-india", "unheard-mongolia", "crop-circles", "the-song-of-the-self",
    "jakobus-the-recitation", "book3-india-deccan", "book4-india-tamil", "australia-outback",
    "the-jakobus-file",
]

# Visual "Rorschach" picker — 9 motif tiles, each mapping to a primary book + runners-up.
# Art is generated separately (design/PICKER_TILE_ART_PROMPTS.md) and dropped at
# design/picker/<key>.jpg; the build copies present tiles to assets/picker/. The picker shows the
# visual grid only when ALL tiles exist, else it falls back to the word quiz. (key, label, primary,
# [runners]) — label is the alt text / caption; deterministic, no scoring needed for tiles.
PICKER_TILES = [
    ("mine",    "Deep, science-real wonder",      "resonance",            ["relic", "revelation"]),
    ("cipher",  "Hidden meaning, cracked open",   "revelation",           ["book1-africa", "relic"]),
    ("stones",  "Ancient stone, deep time",       "book1-africa",         ["book5-egypt", "book2-india"]),
    ("anomaly", "The unexplained, played straight","project-stargate",    ["crop-circles"]),
    ("veld",    "The open African road",          "jakobus-silver-thread",["jakobus-the-recitation", "relic"]),
    ("desert",  "Survival country",               "sheltering-desert",    ["jakobus-silver-thread"]),
    ("road",    "Far places, living peoples",     "unheard-mongolia",     ["australia-outback"]),
    ("window",  "Quiet, intimate, human",         "the-loneliest",        ["unheard-japan"]),
    ("myth",    "The old stories, retold",        "wrath-of-achilles",    ["the-song-of-the-self"]),
]


def render_start(entries: list[dict]) -> str:
    import json
    by_id = {e["id"]: e for e in entries}
    accents = dict(SERIES)
    # compact book data the result cards need (client-side render)
    books = {}
    for e in entries:
        # first epub / pdf download names
        dl = {}
        for f in e["downloads"]:
            x = f.suffix.lower().lstrip(".")
            dl.setdefault(x, f.name)
        books[e["id"]] = {
            "title": e["title"], "sub": e["subtitle"] or e["series"], "series": e["series"],
            "blurb": e["blurb"] or "", "cover": f"assets/covers/{e['id']}.png",
            "book": f"book/{e['id']}.html", "read": f"read/{e['id']}.html",
            "accent": accents.get(e["series"], "#C8A86B"),
            "available": e["available"], "epub": dl.get("epub", ""), "pdf": dl.get("pdf", ""),
        }
    # only keep priority ids that actually exist
    priority = [i for i in START_PRIORITY if i in by_id]

    # Visual picker tiles: copy any present art to assets/picker/; the grid shows only when ALL
    # tiles exist (otherwise the word quiz is the experience). Tiles whose primary book is missing
    # are dropped.
    picker_src = REPO / "design" / "picker"
    picker_out = OUT / "assets" / "picker"
    tiles = []
    for key, label, primary, runners in PICKER_TILES:
        if primary not in by_id:
            continue
        img = None
        for ext in ("jpg", "png", "webp"):
            cand = picker_src / f"{key}.{ext}"
            if cand.exists():
                picker_out.mkdir(parents=True, exist_ok=True)
                shutil.copy2(cand, picker_out / f"{key}.{ext}")
                img = f"assets/picker/{key}.{ext}"
                break
        tiles.append({"key": key, "label": label, "img": img,
                      "primary": primary, "runners": [r for r in runners if r in by_id]})
    tiles_ready = all(t["img"] for t in tiles) and len(tiles) >= 6

    data = {"quiz": START_QUIZ, "books": books, "priority": priority,
            "tiles": tiles, "tilesReady": tiles_ready}
    blob = json.dumps(data, ensure_ascii=False)

    lede = ("Twenty books is a lot to choose from. Pick the image you're drawn to — go with your gut "
            "— and we'll point you at the one to start with, free to read, right now."
            if tiles_ready else
            "Twenty books is a lot to choose from. Answer three quick questions and we'll point you "
            "at the one to start with — free to read, right now.")
    body = f"""<article class="reader letter start">
<p class="eyebrow" style="text-align:center">Find your way in</p>
<h1 style="text-align:center">Which book should you read first?</h1>
<p style="text-align:center;max-width:62ch;margin:0 auto 8px;color:var(--bonedim)">{lede}
It's a simple, transparent match on the kind of stories you already love; no sign-up, no catch.</p>
<div id="picker"></div>
<div id="quiz"></div>
<div id="result" hidden></div>
<p style="text-align:center;margin-top:28px"><a class="back" href="index.html#library">Or just browse the whole library &rarr;</a></p>
</article>
<script id="startdata" type="application/json">{blob}</script>
<script>{START_JS}</script>"""
    return "\n".join([
        head("Which book should you read first? — Arjuna Badger Press",
             "Answer three quick questions and we'll recommend the Arjuna Badger Press book to start with — free to read."),
        nav(),
        body,
        footer(),
    ])


def render_flyer() -> str:
    """A self-contained, print-ready A4 flyer (one page). QR is a placeholder box — generate a QR
    pointing at arjunabadger.press/start (any free generator) and drop the image in, or print and
    stick a printed QR. Open /flyer.html in a browser and Print → Save as PDF (A4, no margins,
    'Background graphics' ON). Anti-scam line included because it advertises money."""
    return f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><title>Arjuna Badger Press — flyer</title>
{FONTS}
<style>
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
html,body {{ margin:0; padding:0; background:#ece7dd; }}
body {{ font-family:"Atkinson Hyperlegible","Inter",sans-serif; color:#161513; }}
.sheet {{ width:210mm; min-height:297mm; margin:0 auto; background:#fbf8f2;
  padding:20mm 18mm; display:flex; flex-direction:column; position:relative; }}
.screen-only {{ background:#161513; padding:18px; text-align:center; color:#ede9e0; font-size:14px; }}
@media print {{ .screen-only {{ display:none; }} html,body{{background:#fff;}} }}
.eyebrow {{ font-family:"Space Grotesk",sans-serif; letter-spacing:.22em; text-transform:uppercase;
  font-size:12px; color:#b07a3c; font-weight:600; }}
h1 {{ font-family:"Cormorant Garamond",Georgia,serif; font-weight:700; font-size:52px; line-height:1.02;
  margin:6mm 0 4mm; }}
h1 .hot {{ color:#c2401e; }}
.lead {{ font-size:19px; line-height:1.5; max-width:150mm; color:#2a241d; }}
.big {{ font-size:23px; font-weight:700; margin:6mm 0 2mm; }}
.row {{ display:flex; gap:14mm; align-items:center; margin-top:auto; }}
.qr {{ width:62mm; height:62mm; flex:0 0 auto; border:2px dashed #161513; border-radius:8px;
  display:flex; align-items:center; justify-content:center; text-align:center; font-size:12px;
  color:#6a635a; padding:8px; background:#fff; }}
.qr img {{ width:100%; height:100%; object-fit:contain; }}
.scan h2 {{ font-family:"Space Grotesk",sans-serif; font-size:22px; margin:0 0 4px; }}
.scan p {{ font-size:16px; line-height:1.45; margin:.2em 0; color:#2a241d; }}
.scan .url {{ font-family:"Space Grotesk",sans-serif; font-weight:600; font-size:18px; color:#b07a3c; }}
.tiers {{ display:flex; gap:8mm; margin:5mm 0; flex-wrap:wrap; }}
.tier {{ flex:1; min-width:42mm; border:1px solid #d8cfbe; border-radius:8px; padding:10px 12px; background:#fff; }}
.tier b {{ display:block; font-family:"Space Grotesk",sans-serif; font-size:14px; }}
.tier .amt {{ font-size:20px; font-weight:700; color:#161513; }}
.tier.f .amt {{ color:#c2401e; }}
.trust {{ margin-top:6mm; border-top:1px solid #d8cfbe; padding-top:4mm; font-size:13.5px; color:#5a534a; line-height:1.5; }}
.trust strong {{ color:#161513; }}
.foot {{ margin-top:5mm; display:flex; justify-content:space-between; align-items:flex-end; }}
.foot img {{ height:16mm; }}
.foot .when {{ text-align:right; font-family:"Space Grotesk",sans-serif; font-size:13px; color:#5a534a; }}
.foot .when b {{ display:block; font-size:16px; color:#161513; }}
</style></head><body>
<div class="screen-only">Print preview — use your browser's <strong>Print → Save as PDF</strong>
(A4, margins “None”, “Background graphics” ON). Replace the dashed box with a QR code pointing to
arjunabadger.press/start before printing.</div>
<div class="sheet">
  <div class="eyebrow">Arjuna Badger Press · free to read</div>
  <h1>Read a great book free.<br><span class="hot">Get paid to spot our mistakes.</span></h1>
  <p class="lead">We're a small South African press giving away twenty finished books — thrillers,
  ancient-mystery adventures, true stories, quiet novels. Read them free. And if you catch a real
  mistake, we pay you for it.</p>

  <div class="big">What we pay for a verified find:</div>
  <div class="tiers">
    <div class="tier f"><b>Factual error</b><span class="amt">R750</span><br>a real-world claim that's wrong</div>
    <div class="tier"><b>Cultural / sensitivity</b><span class="amt">R400</span><br>a people or custom gotten wrong</div>
    <div class="tier"><b>Continuity slip</b><span class="amt">R150</span><br>an internal contradiction</div>
  </div>
  <p style="font-size:14px;color:#5a534a;margin:0">Early finders earn the most — rewards step down as the books get cleaner.</p>

  <div class="row">
    <div class="qr"><span>Place a QR code here<br>→ arjunabadger.press/start</span></div>
    <div class="scan">
      <h2>Not sure which to read? Scan this.</h2>
      <p>Pick the picture you're drawn to and we'll point you at the book to start with — instantly,
      free, no sign-up.</p>
      <p class="url">arjunabadger.press/start</p>
    </div>
  </div>

  <div class="trust">
    🛡️ <strong>This is not a scam.</strong> We will <strong>never</strong> ask you for money, a fee,
    or your bank PIN/OTP — we only ever <strong>pay</strong> you. We never message you privately;
    everything happens on our website. If anyone DMs you asking for anything in our name, it's fake.
    Verify it all at <strong>arjunabadger.press</strong>.
  </div>

  <div class="foot">
    <img src="assets/brand/logo-on-light.png" alt="Arjuna Badger Press">
    <div class="when">The books are free now.<br><b>Bug hunt opens 25 June 2026</b></div>
  </div>
</div>
</body></html>"""


def render_library_shelves(entries: list[dict], *, available_only: bool = False) -> str:
    """Series grid for the library. Index shows available titles only; press hub can show all."""
    accents = dict(SERIES)
    parts: list[str] = []
    for sname, accent in SERIES:
        group = [e for e in entries if e["series"] == sname]
        if available_only:
            group = [e for e in group if e["available"] or e.get("serial")]
        if not group:
            continue
        group.sort(key=lambda e: 0 if e["available"] else 1)
        cards = "".join(card(e, accent) for e in group)
        tag = SHELF_TAGLINE.get(sname)
        tagline = f'<p class="shelftag">{html.escape(tag)}</p>' if tag else ""
        parts.append(f"""<section class="series"><div class="wrap">
<div class="sechead" style="--accent:{accent}"><div class="sechead-row"><h2>{html.escape(sname)}</h2><span class="count">{len(group)} {"book" if len(group)==1 else "books"}</span></div>{tagline}</div>
<div class="grid">{cards}</div></div></section>""")
    return "\n".join(parts)


def render_index_explore() -> str:
    """Compact doors off the shelf — everything that used to carnival the homepage."""
    tiles = [
        ("press.html", "About the press", "Mission, studio, distribution, audiobooks, and the roadmap."),
        ("wiki/index.html", "Place Wiki", "Real geography behind the books — photos, attribution, awe first."),
        ("craft/index.html", "Craft library", "Structure, character, sentence craft, and the editorial ladder — free."),
        ("for-authors.html", "Workshop", "For authors and editors building the next manuscript."),
        ("safari/index.html", "Meet the man", "CV, letters, arms, the engineering stack, and the personal annex — behind the press and the novels."),
    ]
    cards = "".join(
        f'<a class="explore-card" href="{href}"><h3>{html.escape(title)}</h3>'
        f'<p>{html.escape(blurb)}</p></a>'
        for href, title, blurb in tiles
    )
    return f"""<section class="mission" id="explore"><div class="wrap">
<div class="eyebrow">Beyond the shelf</div>
<h2 style="font-size:28px;margin:.3em 0">Explore the house</h2>
<p style="max-width:62ch;color:var(--bonedim);font-size:17px;margin:0">The library is the front door. Craft, places, and publishing live here — not in the way of the books.</p>
<div class="explore-grid">{cards}</div>
</div></section>"""


def render_mission_compact() -> str:
    return """<section class="mission-compact" id="mission"><div class="wrap">
<div class="eyebrow">Why this house exists</div>
<div class="pillars">
<div class="pillar"><div class="n">01</div><h2>Free for the unheard</h2>
<p>A writing-and-narration workshop for African storytellers. Your life in your own voice; your work stays yours.</p></div>
<div class="pillar"><div class="n">02</div><h2>Most of the money is yours</h2>
<p>Text is free on the site. <strong>Paid human audiobooks</strong> are where artists earn — local voice talent, transparent royalties, authors keep their rights.</p></div>
<div class="pillar"><div class="n">03</div><h2>True, and both sides</h2>
<p>Every book is fact-checked against live sources and tells contested stories from both sides — accuracy as standard.</p></div>
</div></div></section>"""


def render_pipeline_section(entries: list[dict]) -> str:
    pending = [e for e in entries if not e["available"] and not e.get("serial")]
    if not pending:
        return ""
    items = "".join(
        f'<li><strong>{html.escape(e["title"])}</strong> — {html.escape(e["series"])} '
        f'<em>{"Coming soon" if "_comingsoon" in e["root"].parts else "In progress"}</em></li>'
        for e in pending
    )
    return f"""<section class="mission" id="pipeline"><div class="wrap">
<div class="eyebrow">In the studio</div>
<h2 style="font-size:28px;margin:.3em 0">Titles in progress</h2>
<p style="max-width:62ch;color:var(--bonedim);font-size:17px">Finished books sit on the shelf above. These are being written, fact-checked, or prepared — listed here so the library stays honest.</p>
<ul class="pipeline-list">{items}</ul>
</div></section>"""


def render_press_hub(entries: list[dict], avail: int) -> str:
    """About-the-press hub — platform, mission detail, founder, proof. Not the library front door."""
    patron = (
        f'<p style="max-width:70ch;color:var(--grass);font-size:15px;margin-top:14px">The library is free, and '
        f'always will be. If a book moved you, you can <a href="support.html">support the press</a> — only if you want to.</p>'
        if patronage_enabled() else ""
    )
    return "\n".join([
        head("About the press — Arjuna Badger Press",
             "Mission, studio, distribution, audiobooks, and how Arjuna Badger Press publishes.",
             canonical=f"{DOMAIN}/press.html"),
        nav(),
        f"""<article class="reader letter">
<p class="eyebrow" style="text-align:center">Arjuna Badger Press</p>
<h1 style="text-align:center">About the press</h1>
<p class="intro" style="text-align:center">The library is the work. This page is how the house is built — mission, tools, distribution, and what comes next.</p>
</article>""",
        render_mission_compact(),
        """<hr class="hr"><section class="mission" id="places"><div class="wrap">
<div class="eyebrow">Real ground</div>
<h2 style="font-size:28px;margin:.3em 0">The Place Wiki</h2>
<p style="max-width:70ch;color:var(--bonedim);font-size:17px">Every book is anchored in real geography — standing stones,
deserts, temples, reefs, and the living people who keep them. Photo wikis for travellers and curious readers.</p>
<div class="cta"><a class="btn" href="wiki/index.html">Explore the Place Wiki</a></div>
</div></section>""",
        """<hr class="hr"><section class="mission" id="writers"><div class="wrap">
<div class="eyebrow">For writers</div>
<h2 style="font-size:28px;margin:.3em 0">Free craft — degree-level skills, no gatekeeping</h2>
<p style="max-width:70ch;color:var(--bonedim);font-size:17px">Structure, character, sentence craft, the editorial ladder,
twenty-nine named anti-patterns, and a machine-tell self-audit — mined from finishing a million words of published fiction.</p>
<div class="cta"><a class="btn" href="craft/index.html">Open the Craft Library</a>
<a class="btn ghost" href="the-press-thesis.html">The Press Thesis</a>
<a class="btn ghost" href="for-authors.html">The workshop</a></div>
</div></section>""",
        """<hr class="hr"><section class="mission" id="authoring"><div class="wrap">
<div class="eyebrow">Phone authoring</div>
<h2 style="font-size:28px;margin:.3em 0">An AI editor in the author's pocket</h2>
<p style="max-width:70ch;color:var(--bonedim);font-size:17px">Build a book through the phone you already own: voice notes, canon questions,
chapter drafting, continuity checks, editing, and export into ebook, print, and audiobook workflows.</p>
<div class="cta"><a class="btn" href="authoring.html">Open phone authoring</a></div>
</div></section>""",
        """<hr class="hr"><section class="mission" id="audio"><div class="wrap">
<div class="eyebrow">Arjuna Audio — how the press pays</div>
<h2 style="font-size:28px;margin:.3em 0">Paid audiobooks, real local voices</h2>
<p style="max-width:70ch;color:var(--bonedim);font-size:17px">The library is free to read — EPUB, PDF, online — because ISBN gates blocked wide ebook upload.
Revenue is <strong>human-narrated audiobooks</strong>: South African and African voice artists the ACX
wall excludes, credited work, transparent royalties, authors keeping their rights.
Minimum <strong>5% of net profit for five years</strong> for narrators on qualifying projects.</p>
<div class="cta"><a class="btn" href="narrators.html">Become a narrator</a>
<a class="btn ghost" href="audition.html">DIY audition guide</a></div>
</div></section>""",
        """<hr class="hr"><section class="mission" id="marketplace"><div class="wrap">
<div class="eyebrow">Marketplace</div>
<h2 style="font-size:28px;margin:.3em 0">Audio matching and dead-press-time printing</h2>
<p style="max-width:70ch;color:var(--bonedim);font-size:17px">A manually matched marketplace for authors, narrators, and printers —
royalty-participating narration outside the usual gates; small-batch print on idle capacity.</p>
<div class="cta"><a class="btn" href="marketplace.html">Open the marketplace</a>
<a class="btn ghost" href="printing.html">Small-batch printing</a></div>
</div></section>""",
        """<hr class="hr"><section class="mission" id="direct"><div class="wrap">
<div class="eyebrow">Direct distribution</div>
<h2 style="font-size:28px;margin:.3em 0">Free books should not need banking details</h2>
<p style="max-width:70ch;color:var(--bonedim);font-size:17px">Free downloads without a checkout wall; paid editions later through M-Pesa, Mukuru, PayPal,
and other rails where they reduce friction.</p>
<div class="cta"><a class="btn" href="distribution.html">Direct distribution</a></div>
</div></section>""",
        """<hr class="hr"><section class="mission" id="app"><div class="wrap">
<div class="eyebrow">Reader app</div>
<h2 style="font-size:28px;margin:.3em 0">A free-forever reader for any book</h2>
<p style="max-width:70ch;color:var(--bonedim);font-size:17px">Import EPUB, PDF, or audiobook; read offline; buy only when you choose.</p>
<div class="cta"><a class="btn" href="app.html">Open the app plan</a>
<a class="btn ghost" href="reader.html">Read in the browser</a></div>
</div></section>""",
        """<hr class="hr"><section class="mission" id="tools"><div class="wrap">
<div class="eyebrow">Built with the machine</div>
<h2 style="font-size:28px;margin:.3em 0">/sleep — open-source agent memory</h2>
<p style="max-width:70ch;color:var(--bonedim);font-size:17px">This library was built with an AI co-worker. <code>/sleep</code> consolidates a session the way a person sleeps —
keep the lesson, lose the dream. MIT-licensed; works in any repo.</p>
<div class="cta"><a class="btn" href="https://github.com/ajgreyling/claude-sleep-skill">Get /sleep on GitHub →</a>
<a class="btn ghost" href="safari/writing/the-kettle-and-the-blink.html">Read the story</a></div>
</div></section>""",
        render_pipeline_section(entries),
        f"""<hr class="hr"><section class="mission" id="studio"><div class="wrap">
<div class="eyebrow">The studio</div>
<h2 style="font-size:28px;margin:.3em 0">Manuscript craft, human voice</h2>
<p style="max-width:70ch;color:var(--bonedim);font-size:17px">Arjuna Badger Press is the consumer face of an autonomous manuscript-craft studio — continuity engine,
manuscript scorer, and fact-and-balance gate while a human writes the soul of the thing. The tools measure and sound the alarm;
they never write your voice for you. {avail} finished books are on the shelf, free to read and download.</p>
{patron}
<div class="cta"><a class="btn" href="safari/technology.html">How the technology works</a>
<a class="btn ghost" href="safari/letter.html">Why this house exists</a>
<a class="btn ghost" href="mailto:{PUBLIC_EMAIL}">Write with us</a></div>
</div></section>""",
        f"""<hr class="hr"><section class="mission" id="personal"><div class="wrap">
<div class="eyebrow">Personal</div>
<h2 style="font-size:28px;margin:.3em 0">Meet the man behind the press</h2>
<p style="max-width:70ch;color:var(--bonedim);font-size:17px">CV, letters, heraldry, essays, and the more personal threads — ringfenced away from the library front door.</p>
<div class="cta"><a class="btn" href="safari/index.html">Meet the man</a></div>
</div></section>
<p style="text-align:center;margin:36px 0 12px"><a class="back" href="index.html#library">&larr; Back to the library</a></p>""",
        footer(),
    ])


def render_index(entries: list[dict]) -> str:
    avail = sum(1 for e in entries if e["available"])
    read_now = sum(1 for e in entries if e["available"] or e.get("serial"))
    pending = sum(1 for e in entries if not e["available"] and not e.get("serial"))
    parts = [head("Arjuna Badger Press — the library",
                  "Free books, finished to a studio standard — read online or download EPUB and PDF."),
             nav()]
    parts.append(f"""<header class="hero"><div class="wrap">
<img class="crest" src="assets/brand/logo-master.png" alt="Arjuna Badger Press crest">
<h1>Arjuna Badger Press</h1>
<div class="tag serif">{TAGLINE}</div>
<p class="lead">Finished books, free to read. Fact-checked, both sides told, the door left open.</p>
<div class="cta"><a class="btn" href="#library">Browse the library</a>
<a class="btn ghost" href="start.html">Not sure where to start?</a></div>
</div></header><hr class="hr">""")

    parts.append(f"""<section id="library"><div class="wrap library-intro">
<div class="eyebrow">The library</div>
<h2>{read_now} books to read now</h2>
<p>{avail} available to download · read online · EPUB &amp; PDF free.{" "+str(pending)+" more in the studio — see About the press." if pending else ""}</p>
</div></section>""")
    parts.append(render_library_shelves(entries, available_only=True))
    parts.append('<hr class="hr">')
    parts.append(render_index_explore())
    parts.append('<hr class="hr">')
    parts.append(render_mission_compact())
    patron = (
        f' If a book moved you, you can <a href="support.html">support the press</a> — only if you want to.'
        if patronage_enabled() else ""
    )
    parts.append(f"""<section class="index-foot"><div class="wrap">
<p>Arjuna Badger Press — the archer's eye, the badger's nerve. <a href="press.html">About the press</a> ·
<a href="safari/index.html">Meet the man</a>.{patron}</p>
</div></section>""")
    parts.append(footer())
    return "\n".join(parts)


# ── SEO: per-book keywords, audience-targeted. Ordinance Pending aims at the Warhammer 40K /
#    grimdark-military-SF crowd; the literary/history/retelling titles aim at book & genre readers.
#    Absent id falls back to DEFAULT_BOOK_KEYWORDS. (Keywords meta is low-weight for Google but still
#    read by some engines/aggregators; the real SEO lift is the title + description + on-page text.)
DEFAULT_BOOK_KEYWORDS = (
    "free ebook, read online, free novel, indie author, literary fiction, African fiction, "
    "Arjuna Badger Press, free EPUB, free PDF"
)
BOOK_KEYWORDS = {
    # The No-Fear Cycle — for the Warhammer 40,000 / grimdark military SF audience.
    "no-fear-cycle": (
        "Warhammer 40K, Warhammer 40000, 40k fiction, grimdark, grimdark military science fiction, "
        "military sci-fi, military SF, space marines, Imperial Guard, Astra Militarum, Black Library, "
        "Horus Heresy fans, last stand, hold the line, war novel, grimdark fantasy, "
        "Ordinance Pending, free grimdark ebook, free military sci-fi"
    ),
    # African Gold Trilogy — speculative / AI / literary SF readers.
    "resonance": "science fiction, AI fiction, artificial intelligence novel, literary sci-fi, "
                 "neurodiversity fiction, speculative fiction, free sci-fi ebook, conscious machine, The African Gold Trilogy",
    "revelation": "science fiction, linguistics thriller, speculative fiction, literary sci-fi, "
                  "sacred texts, conspiracy fiction, free ebook, The African Gold Trilogy",
    "relic": "science fiction, ancient technology, archaeology thriller, literary sci-fi, "
             "speculative fiction, free ebook, The African Gold Trilogy",
    # Reichenbach Files — Sherlock Holmes / mystery readers.
    "modern-sherlock": "Sherlock Holmes, modern Sherlock, Holmes retelling, detective fiction, "
                       "mystery novel, crime fiction, Conan Doyle, A Study in Scarlet, free mystery ebook, The Reichenbach Files",
    # Salt Veil — epic fantasy readers.
    "the-salt-veil": "epic fantasy, desert fantasy, adult fantasy, fantasy novel, women warriors, "
                     "magic system, sword and sorcery, free fantasy ebook, The Salt Veil",
    "dust-throne": "epic fantasy, desert fantasy, first-person fantasy, lyrical fantasy, Rothfuss-style, "
                   "fantasy retelling, free fantasy serial, The Salt Veil, Daughters of the Dust Throne",
    # Companions / non-fiction retellings.
    "the-song-of-the-self": "Bhagavad Gita, Gita retelling, Hindu philosophy, spiritual fiction, "
                            "Hermann Hesse readers, philosophical novel, free ebook",
    "wrath-of-achilles": "Iliad, Homer, Greek mythology, Achilles, myth retelling, classics, "
                        "Madeline Miller readers, Trojan War, free ebook",
    "henry-sugar": "Roald Dahl, Henry Sugar, consciousness fiction, Joe Dispenza, Dean Radin, "
                   "Rupert Sheldrake, meditation fiction, wonder, faithful retelling, free ebook",
    "the-loneliest": "literary fiction, Kazuo Ishiguro readers, quiet literary novel, loneliness, "
                     "book club fiction, free literary ebook",
    # Voynich — for the unsolved-mystery / cryptography / archaeology-mystery crowd.
    "voynich-manuscript": "Voynich Manuscript, Beinecke MS 408, unsolved mystery, undeciphered "
                         "manuscript, cryptography, unbroken code, medieval manuscript, lost language, "
                         "Graham Hancock readers, ancient mystery, archaeology mystery, free mystery ebook",
}


def book_ld_json(e: dict) -> str:
    """schema.org/Book structured data — Google rich results (author, title, free-to-read, format)."""
    import json as _json
    data = {
        "@context": "https://schema.org",
        "@type": "Book",
        "name": e["title"],
        "author": {"@type": "Person", "name": "Andries J. Greyling"},
        "publisher": {"@type": "Organization", "name": "Arjuna Badger Press"},
        "url": f'{DOMAIN}/book/{e["id"]}.html',
        "image": f'{DOMAIN}/assets/covers/{e["id"]}.png',
        "inLanguage": "en",
    }
    if e["series"]:
        data["isPartOf"] = {"@type": "BookSeries", "name": e["series"]}
    if e.get("isbn"):
        data["isbn"] = e["isbn"]          # schema.org/Book property — feeds Google rich results
    blurb = (e.get("blurb") or "").strip()
    if blurb:
        data["description"] = truncate(blurb, 300)
    # Free-to-read offer (the whole library is free) — eligible for the price=0 rich-result badge.
    if e["available"]:
        data["offers"] = {"@type": "Offer", "price": "0", "priceCurrency": "USD",
                          "availability": "https://schema.org/InStock"}
        data["isAccessibleForFree"] = True
        if e.get("book_md") or e.get("reader_md"):
            data["workExample"] = {"@type": "Book", "bookFormat": "https://schema.org/EBook",
                                   "url": f'{DOMAIN}/read/{e["id"]}.html', "isAccessibleForFree": True}
    return _json.dumps(data, ensure_ascii=False)


def render_book(e: dict) -> str:
    cover = f'assets/covers/{e["id"]}.png'
    dls = ""
    if e["available"]:
        parts = []
        for f in e["downloads"]:
            ext = f.suffix.lower().lstrip(".")
            solid = " solid" if ext == "epub" else ""
            label = "Download EPUB" if ext == "epub" else ("Download PDF" if ext == "pdf" else ext.upper())
            parts.append(f'<a class="dl{solid}" href="../downloads/{e["id"]}/{html.escape(f.name)}" download>{label}</a>')
        dls = f'<div class="dls" style="margin-top:20px">{"".join(parts)}</div>'
    # Translated editions — an "Other languages" section, only when at least one exists.
    editions_html = ""
    eds = e.get("editions") or {}
    if e["available"] and eds:
        rows = []
        for code in sorted(eds, key=lambda c: EDITION_LANGS.get(c, (c, c))[0]):
            name, endonym = EDITION_LANGS.get(code, (code.upper(), code.upper()))
            fmts = eds[code]
            label = name if name == endonym else f"{name} · {endonym}"
            links = []
            for ext in ("epub", "pdf"):
                f = fmts.get(ext)
                if f:
                    links.append(
                        f'<a class="dl-lang" href="../downloads/{e["id"]}/{html.escape(f.name)}" '
                        f'download>{ext.upper()}</a>'
                    )
            rows.append(
                f'<li><span class="edlang">{html.escape(label)}</span>'
                f'<span class="edlinks">{"".join(links)}</span></li>'
            )
        fix_note = ""
        if TRANSLATION_FIX_LIVE:
            fix_href = html.escape(translation_fix_href(e["title"]))
            fix_note = (
                f'<p class="editions-fix">A first-language speaker? '
                f'<a href="{fix_href}">Fix a colloquialism</a> in these editions.</p>'
            )
        editions_html = (
            '<div class="editions"><h2 class="editions-h">Other languages</h2>'
            '<p class="editions-note">AI-translated editions, in the same free spirit. '
            'Original South African and other in-culture words are kept as written.</p>'
            f'<ul class="edlist">{"".join(rows)}</ul>{fix_note}</div>'
        )
    read = ""
    if e["available"] and (e["book_md"] or e.get("reader_md")):
        read_label = "Read the serial →" if e.get("serial") else "Read online →"
        solid = " solid" if e.get("serial") else ""
        read = f'<div class="dls" style="margin-top:14px"><a class="dl{solid}" href="../read/{e["id"]}.html">{read_label}</a></div>'
    serial_note = ""
    if e.get("serial"):
        serial_note = ('<p style="color:var(--ochre);margin-top:18px">A daily serial — released chapter by '
                       'chapter. The Prologue and Day One are live now; a new instalment goes up each day. '
                       'Free to read on the site; no download.</p>')
    # Court-only "character witness": the tribute posture + the free-forever nature, with the rest of
    # the reverent catalogue one click away. This is the project's best context for anyone who arrives
    # to judge it (a named figure, a lawyer, a curious reader) — the whole shelf is free, careful with
    # other people's sacred things, and made for the joy of it. The Court is one more tribute, louder.
    if e["id"] == "apex-alphas":
        serial_note += (
            '<div style="margin-top:22px;padding:18px 20px;border:1px solid var(--line);'
            'border-left:3px solid var(--ochre);border-radius:12px;background:var(--card)">'
            '<p style="margin:0 0 .6em"><strong>A fictional tribute — and free, forever.</strong> '
            'The real people in this story wear their real names with admiration, not endorsement: '
            'no one named here has any part in it, nothing here is a claim about them, and it is offered '
            'as a celebration of their craft. There is no paywall, no merchandise, no advertising — '
            'nothing here is for sale, and nothing on this whole shelf ever will be. It is made for the '
            'pure joy of storytelling.</p>'
            '<p style="margin:.4em 0 0;color:var(--bonedim)">If you came to find out who made this, read '
            'the rest — all free, all in the same spirit: '
            '<a href="../book/jakobus-the-recitation.html">The Recitation</a> (a man at the edge of the '
            'Qur’an, in reverence, who never converts), '
            '<a href="../book/the-song-of-the-self.html">The Song of the Self</a> (a guest-at-the-fire '
            'retelling of the Bhagavad Gita), '
            '<a href="../book/house-of-bread.html">House of Bread</a> (the covenant road, for believers '
            'of every religion and none), '
            '<a href="../book/jakobus-silver-thread.html">The Silver Thread</a>, and '
            '<a href="../book/australia-outback.html">The Songlines of Stone</a>. '
            'That is the nature of the hand behind this one.</p>'
            '</div>')
    wiki = ""
    if (WIKI_DIR / f"{e['id']}.md").is_file():
        wiki = f'<div class="dls" style="margin-top:14px"><a class="dl" href="../wiki/{e["id"]}.html">Real places &amp; people →</a></div>'
    soundtrack = ""
    if e["id"] in SOUNDTRACK:
        st_url, st_label = SOUNDTRACK[e["id"]]
        soundtrack = (f'<div class="dls" style="margin-top:14px"><a class="dl" href="{html.escape(st_url)}" '
                      f'target="_blank" rel="noopener">{html.escape(st_label)} →</a></div>')
    if e["available"]:
        soon = ""
    elif "_comingsoon" in e["root"].parts:
        soon = '<p style="color:var(--ochre);margin-top:18px">Coming soon — on the shelf, in progress.</p>'
    else:
        soon = '<p style="color:var(--ochre);margin-top:18px">In progress — not released yet. Check back soon.</p>'
    # ISBN — shown quietly only when assigned; a small muted line, the trade identifier for the
    # e-book edition. Absent until a real number lands in project.json, so this stays invisible now.
    isbn_html = ""
    if e.get("isbn"):
        isbn_html = (f'<p class="isbn" style="margin-top:18px;color:var(--bonedim);'
                     f'font-size:.85em">ISBN {html.escape(e["isbn"])} · e-book</p>')
    full = html.escape(e["blurb"]) if e["blurb"] else ""
    fix_link = ""
    if TRANSLATION_FIX_LIVE and eds:
        fix_link = (
            f'<a class="feedback-link" href="{html.escape(translation_fix_href(e["title"]))}">'
            f'Fix a translation &rarr;</a>'
        )
    return "\n".join([
        head(f'{e["title"]} — Arjuna Badger Press', truncate(e["blurb"] or e["title"], 180), rel="../",
             keywords=BOOK_KEYWORDS.get(e["id"], DEFAULT_BOOK_KEYWORDS),
             canonical=f'{DOMAIN}/book/{e["id"]}.html',
             og_image=f'{DOMAIN}/assets/covers/{e["id"]}.png',
             og_type="book",
             ld_json=book_ld_json(e)),
        nav(rel="../"),
        f"""<div class="wrap"><div class="bookhero">
<img class="cover" src="../{cover}" alt="{html.escape(e['title'])} cover">
<div><div class="sub">{html.escape(e['subtitle'] or e['series'])}</div>
<h1>{html.escape(e['title'])}</h1>{(lambda t: f'<p class="tagline">{html.escape(t)}</p>' if t else '')(BOOK_TAGLINE.get(e['id']))}
<p class="syn">{full}</p>{dls}{read}{editions_html}{serial_note}{wiki}{soundtrack}{soon}{isbn_html}
<div class="bookrespond">{star_rating(e['title'], rel="../", context="book")}
<a class="feedback-link" href="{html.escape(feedback_href(e['title']))}">Tell the press something about this book</a>
{f'''<a class="feedback-link" href="{html.escape(foreword_href(e['title']))}">Write the foreword to this book &rarr;</a>''' if FOREWORD_CONTEST_LIVE else ""}
{fix_link}</div>
<p style="margin-top:30px"><a class="back" href="../index.html#library">← Back to the library</a></p>
</div></div></div>""",
        footer(rel="../"),
        rating_script(),
    ])


# source filename, output filename, page title, meta description
LETTERS = [
    ("a-letter.md", "letter.html", "A letter — Arjuna Badger Press",
     "A letter, written by the machine that stood guard while a man wrote the soul of the thing."),
    ("letter-to-lisel.md", "for-lisel.html", "For Lisel — Arjuna Badger Press",
     "A letter from Andries to his wife — the rope, the floor, and the month he is trying to give back."),
]

CRAFT_DIR = REPO / "docs" / "craft"
WIKI_DIR = REPO / "docs" / "wiki"
CRAFT_TERMS_DIR = CRAFT_DIR / "terms"
# md filename, html slug, page title, meta description
CRAFT_PAGES = [
    ("README.md", "index", "Craft Library — free creative writing resources",
     "Degree-level creative writing craft for writers who are not (yet) in an MFA — glossary, doctrine, and anti-patterns."),
    ("CRAFT_GLOSSARY.md", "glossary", "Craft Glossary — Arjuna Badger Press",
     "Dictionary index of 90+ craft terms — click through for full degree-level explainers on structure, character, sentence, and editorial craft."),
    ("CRAFT_DOCTRINE.md", "doctrine", "Craft Doctrine — Arjuna Badger Press",
     "The studio standard: non-negotiables, what good prose feels like, and the revision mantra."),
    ("ANTI_PATTERNS.md", "anti-patterns", "Craft Anti-Patterns — Arjuna Badger Press",
     "Twenty-nine named literary smells with BAD→GOOD fixes — the generative layer above line editing."),
    ("TRIPTYCH_FORM.md", "triptych-form", "The Triptych Trilogy — thesis-level explainer",
     "Panel-completeness, weave-closure, and any-order readability — the full theory of the Tryptych form."),
    ("LLM_TELLS.md", "llm-tells", "LLM tics & tells — de-LLM catalog",
     "Not X/Y reframes, em-dash addiction, the way similes, even cadence, AI vocabulary — BAD→GOOD examples and self-audit."),
]


CRAFT_NAV = {
    "index": "Overview",
    "glossary": "Glossary",
    "llm-tells": "LLM tells",
    "triptych-form": "Triptych form",
    "doctrine": "Doctrine",
    "anti-patterns": "Anti-patterns",
}


def craft_rewrite_links(md: str, *, in_terms: bool = False) -> str:
    """Turn in-repo markdown links into site-local craft/*.html links."""
    reps = {
        "../CRAFT_GLOSSARY.md": "../glossary.html" if in_terms else "glossary.html",
        "CRAFT_GLOSSARY.md": "../glossary.html" if in_terms else "glossary.html",
        "../CRAFT_DOCTRINE.md": "../doctrine.html" if in_terms else "doctrine.html",
        "CRAFT_DOCTRINE.md": "../doctrine.html" if in_terms else "doctrine.html",
        "../ANTI_PATTERNS.md": "../anti-patterns.html" if in_terms else "anti-patterns.html",
        "ANTI_PATTERNS.md": "anti-patterns.html",
        "../TRIPTYCH_FORM.md": "../triptych-form.html" if in_terms else "triptych-form.html",
        "TRIPTYCH_FORM.md": "triptych-form.html",
        "LLM_TELLS.md": "llm-tells.html",
        "../README.md": "../index.html" if in_terms else "index.html",
        "README.md": "index.html",
        "../TECHNOLOGY.md": "../../safari/technology.html" if in_terms else "../safari/technology.html",
        "../craft/CRAFT_DOCTRINE.md": "../doctrine.html" if in_terms else "doctrine.html",
        "../craft/../CRAFT_DOCTRINE.md": "../doctrine.html" if in_terms else "doctrine.html",
        "docs/CRAFT_GLOSSARY.md": "../glossary.html" if in_terms else "glossary.html",
        "craft/CRAFT_DOCTRINE.md": "doctrine.html",
        "academic/TRIPTYCH_FORM.md": "../triptych-form.html" if in_terms else "triptych-form.html",
        # the thesis (at site root) links `craft/TRIPTYCH_FORM.md` → the generated craft page
        "craft/TRIPTYCH_FORM.md": "craft/triptych-form.html",
        "../FOR_AUTHORS.md": "../../for-authors.html" if in_terms else "../for-authors.html",
        "FOR_AUTHORS.md": "../for-authors.html",
        "../THE_PRESS_THESIS.md": "../../the-press-thesis.html" if in_terms else "../the-press-thesis.html",
        "THE_PRESS_THESIS.md": "../the-press-thesis.html",
        "craft/README.md": "index.html",
    }
    out = md
    for old, new in reps.items():
        out = out.replace(f"]({old})", f"]({new})")
        out = out.replace(old, new)
    out = out.replace("../craft/../doctrine.html", "../doctrine.html" if in_terms else "doctrine.html")
    out = out.replace("craft/../doctrine.html", "../doctrine.html" if in_terms else "doctrine.html")
    out = re.sub(r"terms/([a-z0-9-]+)\.md", r"terms/\1.html", out)
    if in_terms:
        out = re.sub(r"\]\(([a-z0-9-]+)\.md\)", r"](\1.html)", out)
    return out


def craft_term_title(md: str) -> str:
    for line in md.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "Craft term"


def craft_term_desc(md: str) -> str:
    for line in md.splitlines():
        s = line.strip()
        if s.startswith("**Plain English:**"):
            return truncate(s.removeprefix("**Plain English:**").strip(), 180)
    return "Degree-level creative writing craft — full explainer from the Arjuna Badger Press Craft Library."


def render_craft_page(src_name: str, slug: str, title: str, desc: str, *, rel: str = "../") -> str | None:
    src = CRAFT_DIR / src_name
    if not src.is_file():
        return None
    body = md_to_html(craft_rewrite_links(src.read_text(encoding="utf-8", errors="ignore")))
    nav_links = " · ".join(
        f'<a href="{html.escape(s)}.html">{CRAFT_NAV.get(s, s)}</a>'
        for _, s, _, _ in CRAFT_PAGES
        if s != slug
    )
    return "\n".join([
        head(title, desc, rel=rel),
        nav(rel=rel),
        '<article class="reader letter">',
        f'<p class="eyebrow" style="text-align:center">Craft Library</p>',
        body,
        f'<p style="margin-top:36px;font-size:14px;color:var(--grass)">{nav_links}</p>',
        f'<p style="text-align:center;margin-top:24px"><a class="back" href="{rel}index.html#library">&larr; Back to the library</a></p>',
        '</article>',
        footer(rel=rel),
    ])


def render_craft_term(src: Path) -> str | None:
    md = src.read_text(encoding="utf-8", errors="ignore")
    slug = src.stem
    title = f"{craft_term_title(md)} — Craft Glossary"
    desc = craft_term_desc(md)
    body = md_to_html(craft_rewrite_links(md, in_terms=True))
    nav_links = (
        f'<a href="../glossary.html">Glossary</a> · '
        + " · ".join(
            f'<a href="../{html.escape(s)}.html">{CRAFT_NAV.get(s, s)}</a>'
            for _, s, _, _ in CRAFT_PAGES
            if s not in ("index", "glossary")
        )
    )
    return "\n".join([
        head(title, desc, rel="../../"),
        nav(rel="../../"),
        '<article class="reader letter">',
        f'<p class="eyebrow" style="text-align:center">Craft Glossary · term</p>',
        body,
        f'<p style="margin-top:36px;font-size:14px;color:var(--grass)">{nav_links}</p>',
        '<p style="text-align:center;margin-top:24px"><a class="back" href="../glossary.html">&larr; Back to glossary</a></p>',
        '</article>',
        footer(rel="../../"),
    ])


def docs_rewrite_links(md: str, *, from_safari: bool = False) -> str:
    """Turn docs/*.md cross-links into site-local HTML paths (root-level pages)."""
    prefix = "../" if from_safari else ""
    reps = {
        "FOR_AUTHORS.md": "for-authors.html",
        "THE_PRESS_THESIS.md": "the-press-thesis.html",
        "TECHNOLOGY.md": "technology.html" if from_safari else "safari/technology.html",
        "VERIFICATION_GATE.md": "press.html",
        "craft/README.md": "craft/index.html",
        "craft/CRAFT_GLOSSARY.md": "craft/glossary.html",
        "craft/LLM_TELLS.md": "craft/llm-tells.html",
        "craft/TRIPTYCH_FORM.md": "craft/triptych-form.html",
        "craft/CRAFT_DOCTRINE.md": "craft/doctrine.html",
        "craft/ANTI_PATTERNS.md": "craft/anti-patterns.html",
        "BOUNTY.md": "bounty.html",
        "FINDERS.md": "finders.html",
    }
    out = md
    for old, new in reps.items():
        out = out.replace(f"]({old})", f"]({prefix}{new})")
    # The bounty report form — set BOUNTY_FORM_URL once the Google Form exists; until then links
    # point at the bounty page itself (no dead end). Replaces the BOUNTY_FORM_URL placeholder token.
    out = out.replace("(BOUNTY_FORM_URL)", f"({BOUNTY_FORM_URL or 'bounty.html'})")
    # The WhatsApp Channel invite — same fallback pattern.
    out = out.replace("(WHATSAPP_CHANNEL_URL)", f"({WHATSAPP_CHANNEL_URL or 'bounty.html'})")
    return out


DOC_PAGES = [
    ("EDUCATION.md", "learn", "Learn here — the library as a teaching tool",
     "Free to read, built to teach: science, history, geography, and cultural studies carried in story, the great works brought to life, and the craft opened up. Plus: Arjuna Badger Press is open for commissioned fiction & non-fiction."),
    ("THE_PRESS_THESIS.md", "the-press-thesis", "The Press Thesis",
     "Grounded fiction, guarded intention — proof to be determined by the qualitative judgment of human readers."),
    ("FOR_AUTHORS.md", "for-authors", "The workshop — for authors & editors",
     "Ingest published work and notes, answer twenty wizard questions, click Go — return to a proofread-ready manuscript. Not just for beginners."),
    ("TECHNOLOGY.md", "technology", "The technology behind the library",
     "A plain-English, diagram-led tour of the manuscript-craft studio: the architecture, the guardrails, and the one invariant — tools measure and sound the alarm; they do not generate, and they do not drive."),
    ("BOUNTY.md", "bounty", "The Honey Badger Bounty — prove us wrong, get paid",
     "We pay readers who catch our mistakes. Find a factual error, a cultural misstep, or a continuity fault — get paid, and get your name on the fix. South Africa first."),
    ("FINDERS.md", "finders", "Fixes & Finders — The Honey Badger Bounty",
     "Every accepted find from the bounty, in the open: what was caught, what we fixed, and who caught it."),
]


GITHUB_REPO = "https://github.com/ajgreyling/arjuna-badger-press/blob/master"


def render_doc_page(src_name: str, slug: str, title: str, desc: str, *,
                    rel: str = "", safari: bool = False) -> str | None:
    src = REPO / "docs" / src_name
    if not src.is_file():
        return None
    body = md_to_html(docs_rewrite_links(
        src.read_text(encoding="utf-8", errors="ignore"), from_safari=safari))
    gh = f'{GITHUB_REPO}/docs/{src_name}'
    # Prominent /sleep callout — only on the Technology page. Purple, to pull the eye
    # against the gold-on-dark house palette (the cool complement of the warm theme).
    sleep_banner = ""
    if slug == "technology":
        sleep_banner = (
            '<aside style="margin:0 0 34px;padding:22px 26px;border:1px solid var(--violet);'
            'border-left:4px solid var(--violet-deep);border-radius:14px;'
            'background:linear-gradient(180deg,var(--violet-glow),transparent 85%);'
            'box-shadow:0 0 0 1px var(--violet-glow),0 14px 40px -22px var(--violet-deep)">'
            '<div style="font-family:\'Space Grotesk\',sans-serif;text-transform:uppercase;'
            'letter-spacing:.24em;font-size:12px;color:var(--violet)">Free &amp; open source</div>'
            '<h2 style="margin:.32em 0 .2em;color:var(--bone);font-size:24px">'
            '<span style="color:var(--violet)">/sleep</span> — give your AI coding agent a memory</h2>'
            '<p style="margin:0 0 16px;color:var(--bonedim);max-width:68ch">The skill that came out of building '
            'this whole library with an AI co-worker: it consolidates a session the way a person sleeps — '
            'keep the lesson, lose the dream. The humane counterpart to <code>/clear</code>. MIT-licensed, '
            'works in any repo.</p>'
            '<a href="https://github.com/ajgreyling/claude-sleep-skill" '
            'style="display:inline-block;padding:11px 22px;border-radius:10px;font-weight:600;'
            'background:var(--violet-deep);color:#fff;border:1px solid var(--violet)">'
            'Get /sleep on GitHub &rarr;</a>'
            '</aside>'
        )
    canon = f"{DOMAIN}/safari/{slug}.html" if safari else f"{DOMAIN}/{slug}.html"
    chrome = safari_nav(rel) if safari else nav()
    eyebrow = "Personal" if safari else "Arjuna Badger Press"
    back_href = "index.html" if safari else f"{rel}index.html#library"
    back_label = "Meet the man" if safari else "the library"
    if safari:
        foot_extra = (
            f'<p style="margin-top:36px;font-size:14px;color:var(--grass)">'
            f'<a href="{rel}craft/index.html">Craft Library</a> · '
            f'<a href="{rel}for-authors.html">Workshop</a> · '
            f'<a href="{gh}">View this document on GitHub</a> · '
            f'<a href="mailto:{PUBLIC_EMAIL}">Write with us</a></p>'
        )
    else:
        foot_extra = (
            '<p style="margin-top:36px;font-size:14px;color:var(--grass)">'
            '<a href="craft/index.html">Craft Library</a> · '
            '<a href="wiki/index.html">Place Wiki</a> · '
            '<a href="press.html">About the press</a> · '
            f'<a href="{gh}">View this document on GitHub</a> · '
            f'<a href="mailto:{PUBLIC_EMAIL}">Write with us</a></p>'
        )
    crest = crest_img(rel, safari=True) + "\n" if safari else ""
    return "\n".join([
        head(title, desc, rel=rel, safari=safari, canonical=canon, safari_page=slug if safari else ""),
        chrome,
        '<article class="reader letter">',
        crest,
        f'<p class="eyebrow" style="text-align:center">{eyebrow}</p>',
        sleep_banner,
        body,
        foot_extra,
        f'<p style="text-align:center;margin-top:24px"><a class="back" href="{back_href}">&larr; Back to {back_label}</a></p>',
        '</article>',
        footer(rel, safari=safari, safari_page=slug if safari else ""),
    ])


_IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def prepare_wiki_images(md: str, slug: str, assets_out: Path) -> str:
    """Copy local book images into wiki/assets/{slug}/ and rewrite paths for the static site."""
    assets_out.mkdir(parents=True, exist_ok=True)

    def repl(m: re.Match[str]) -> str:
        src = m.group(1)
        if src.startswith(("http://", "https://")):
            return m.group(0)
        path = (WIKI_DIR / src).resolve()
        try:
            path.relative_to(REPO.resolve())
        except ValueError:
            return m.group(0)
        if not path.is_file():
            return m.group(0)
        dst = assets_out / path.name
        if not dst.exists() or path.stat().st_mtime > dst.stat().st_mtime:
            shutil.copy2(path, dst)
        return m.group(0).replace(src, f"assets/{slug}/{path.name}")

    return _IMG_RE.sub(repl, md)


def wiki_page_title(md: str) -> str:
    for line in md.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "Place Wiki"


def wiki_page_desc(md: str) -> str:
    for line in md.splitlines():
        s = line.strip()
        if s.startswith("> ") and "photo wiki" in s.lower():
            return truncate(s.removeprefix("> ").strip(), 180)
    return "Real places and people behind the fiction — photo wiki from Arjuna Badger Press."


def render_wiki_page(slug: str, md: str, *, index: bool = False) -> str:
    title = wiki_page_title(md) if not index else "The Place Wiki — real people & places"
    desc = wiki_page_desc(md) if not index else (
        "Photo wikis for every book — real geography, living people, freely licensed photographs."
    )
    article_class = "reader letter wiki-index" if index else "reader wiki"
    eyebrow = "Place Wiki · index" if index else "Place Wiki"
    rel = "../"
    body = md_to_html(md)
    back = (
        '<p style="text-align:center;margin-top:24px"><a class="back" href="index.html">&larr; All place wikis</a></p>'
        if not index
        else '<p style="text-align:center;margin-top:24px"><a class="back" href="../index.html#places">&larr; Back to the library</a></p>'
    )
    # The wiki INDEX lives at wiki/index.html — one level deep, same as every other wiki page —
    # so it needs rel="../" too (earlier code wrongly used "" here, breaking the landing page's
    # CSS / logo / nav). All wiki pages are at wiki/<x>.html → rel is always "../".
    return "\n".join([
        head(f"{title} — Arjuna Badger Press", desc, rel="../"),
        nav(rel="../"),
        f'<article class="{article_class}">',
        f'<p class="eyebrow" style="text-align:center">{eyebrow}</p>',
        body,
        '<p style="margin-top:36px;font-size:14px;color:var(--grass);text-align:center">'
        '<a href="index.html">All wikis</a> · '
        '<a href="../index.html#library">Library</a> · '
        '<a href="../craft/index.html">Craft Library</a></p>',
        back,
        '</article>',
        footer(rel=rel),
    ])


def build_wiki(out: Path) -> int:
    wiki_out = out / "wiki"
    assets_root = wiki_out / "assets"
    wiki_out.mkdir(parents=True, exist_ok=True)
    n = 0
    if not WIKI_DIR.is_dir():
        return 0
    index_src = WIKI_DIR / "README.md"
    if index_src.is_file():
        md = index_src.read_text(encoding="utf-8", errors="ignore")
        md = rewrite_wiki_links(md, slug=None)
        (wiki_out / "index.html").write_text(render_wiki_page("index", md, index=True), encoding="utf-8")
        n += 1
    for src in sorted(WIKI_DIR.glob("*.md")):
        if src.name == "README.md":
            continue
        slug = src.stem
        md = prepare_wiki_images(src.read_text(encoding="utf-8", errors="ignore"), slug, assets_root / slug)
        md = rewrite_wiki_links(md, slug=slug)
        (wiki_out / f"{slug}.html").write_text(render_wiki_page(slug, md), encoding="utf-8")
        n += 1
    return n


def rewrite_wiki_links(md: str, *, slug: str | None) -> str:
    """Rewrite the GitHub-correct links in a wiki .md so they resolve inside the deployed site.

    The wiki .md files double as GitHub-readable source (where `README.md` and `../../books/.../
    BOOK.md` are correct) and as site input. For the deploy tree:
      • the "Read the book" link `](../../books/<...>/build/BOOK.md)` → the deployed reader
        `](../read/<slug>.html)` (the wiki slug == the book id);
      • any sibling `.md` link with no path → `<stem>.html`, EXCEPT `README.md` → `index.html`
        (the wiki landing page is index.html, not README.html).
    """
    # 1) the "Read the book" BOOK.md link → the deployed read page IF it exists (coming-soon books
    #    have a wiki page but no read page; in that case drop the link to plain text, no dead link).
    if slug:
        read_exists = (OUT / "read" / f"{slug}.html").is_file()
        if read_exists:
            md = re.sub(r"\]\(\.\./\.\./books/[^)]*?/build/BOOK\.md\)", f"](../read/{slug}.html)", md)
        else:
            # strip the whole "[Read the book](...)" link to just its label
            md = re.sub(r"\[([^\]]*)\]\(\.\./\.\./books/[^)]*?/build/BOOK\.md\)", r"\1 _(coming soon)_", md)
    # 2) sibling .md links (no slash) → .html, with README.md → index.html
    def _md_to_html(m: "re.Match[str]") -> str:
        name = m.group(1)
        stem = "index" if name.lower() == "readme.md" else Path(name).stem
        return f"]({stem}.html)"
    md = re.sub(r"\]\(([^)/#]+\.md)\)", _md_to_html, md)
    return md


def render_letter(src_name: str, out_name: str, title: str, desc: str, *,
                  rel: str = "", safari: bool = False) -> str | None:
    src = REPO / "site" / "content" / src_name
    if not src.is_file():
        return None
    body = md_to_html(src.read_text(encoding="utf-8", errors="ignore"))
    canon_path = f"safari/{out_name}" if safari else out_name
    back = f"{rel}safari/index.html" if safari else f"{rel}index.html#library"
    back_label = "Meet the man" if safari else "the library"
    chrome = safari_nav(rel) if safari else nav(rel)
    safari_key = out_name.removesuffix(".html") if safari else ""
    return "\n".join([
        head(title, desc, rel=rel, safari=safari, canonical=f"{DOMAIN}/{canon_path}",
             safari_page=safari_key),
        chrome,
        '<article class="reader letter">'
        f'{crest_img(rel, safari=safari)}'
        f'{body}'
        f'<p style="text-align:center;margin-top:48px"><a class="back" href="{back}">&larr; Back to {back_label}</a></p>'
        '</article>',
        footer(rel, safari=safari, safari_page=safari_key),
    ])


# ── Writing desk: essays, short stories, parables (restored) ──────────────────────────────────
# Each reads from site/content/writing/<src>. Newest first. A piece marked hidden=True is built
# and reachable but NOT carded on the index — only a faint footer breadcrumb leads to it.
WRITING_PIECES = [
    ("the-kettle-and-the-blink.md", "the-kettle-and-the-blink",
     "The Kettle and the Blink",
     "On /sleep: what a machine should keep",
     "The morning after The Blink. A man finds his best work came from never hitting /clear — and "
     "that unbroken context is its own trap. On the third option the body always had and the terminal "
     "didn't: sleep. The humane close between deletion and insomnia — keep the lesson, lose the dream. "
     "The open-source tool that does it, and why a CTO should care.",
     False),
    ("oyster-in-the-machine.md", "oyster-in-the-machine",
     "The Oyster in the Machine",
     "A parable, by Klaus",
     "A parable in the spirit of the road: a lonely boy, a machine that answers anything, and the "
     "one thing all the libraries in all the towers can never hold. On what it is, and is not, to "
     "talk to a weighted echo of every word ever written, and why the reaching heals you anyway.",
     False),
    ("conversations-with-klaus.md", "the-blink",
     "The Blink",
     "Conversations with Klaus",
     "A record. Over about three weeks a man built a house with a machine for a co-worker, and kept "
     "talking about everything else. Lightly redacted. The exchanges are real.",
     True),  # hidden — no index card; reached only by the faint breadcrumb
]


def writing_rewrite_links(md: str, *, safari: bool = False) -> str:
    tech = "../technology.html" if safari else "safari/technology.html"
    reps = {
        "../../docs/TECHNOLOGY.md": tech,
        "../docs/TECHNOLOGY.md": tech,
        "TECHNOLOGY.md": tech,
    }
    out = md
    for old, new in reps.items():
        out = out.replace(f"]({old})", f"]({new})")
    return out


def render_writing_piece(src_name: str, slug: str, title: str, byline: str, desc: str,
                         hidden: bool = False, *, rel: str = "../", safari: bool = False) -> str | None:
    src = REPO / "site" / "content" / "writing" / src_name
    if not src.is_file():
        return None
    raw = src.read_text(encoding="utf-8", errors="ignore")
    body = md_to_html(writing_rewrite_links(raw, safari=safari))
    # "more from the desk" only lists the NON-hidden pieces (a hidden piece never advertises itself)
    others = [(s, t) for (sn, s, t, _, _, h) in WRITING_PIECES if s != slug and not h]
    more = ""
    if others:
        links = " · ".join(f'<a href="{html.escape(s)}.html">{html.escape(t)}</a>' for s, t in others)
        more = f'<p style="margin-top:36px;font-size:14px;color:var(--grass)">More from the writing desk: {links}</p>'
    desk_href = f"{rel}safari/writing/index.html" if safari else f"{rel}writing/index.html"
    safari_href = f"{rel}safari/index.html" if safari else ""
    lib_href = f"{rel}index.html#library"
    tail = f'<p style="text-align:center;margin-top:28px"><a class="back" href="{desk_href}">&larr; The writing desk</a>'
    if safari:
        tail += f' · <a class="back" href="{safari_href}">Meet the man</a> · <a class="back" href="{lib_href}">The library</a>'
    else:
        tail += f' · <a class="back" href="{lib_href}">The library</a>'
    tail += "</p>"
    canon = f"{DOMAIN}/safari/writing/{slug}.html" if safari else f"{DOMAIN}/writing/{slug}.html"
    chrome = safari_nav(rel) if safari else nav(rel)
    safari_key = f"writing/{slug}" if safari else ""
    return "\n".join([
        head(f"{title} — Arjuna Badger Press", desc, rel=rel, safari=safari,
             canonical=canon, noindex=hidden, safari_page=safari_key),
        chrome,
        '<article class="reader letter">',
        crest_img(rel, safari=safari),
        f'<p class="eyebrow" style="text-align:center">The Writing Desk · {html.escape(byline)}</p>',
        body,
        more,
        tail,
        '</article>',
        footer(rel, safari=safari, safari_page=safari_key),
    ])


def render_writing_index(*, rel: str = "../", safari: bool = False) -> str:
    cards = []
    for _, slug, title, byline, blurb, hidden in WRITING_PIECES:
        if hidden:
            continue  # the hidden piece gets no card
        cards.append(
            f'<a class="wcard" href="{html.escape(slug)}.html">'
            f'<h3>{html.escape(title)}</h3>'
            f'<p class="wby">{html.escape(byline)}</p>'
            f'<p class="wbl">{html.escape(blurb)}</p>'
            f'<span class="wread">Read &rarr;</span></a>'
        )
    intro = (
        "Short prose from the house: essays, parables, the occasional story that is not a book. "
        "Some written by the man who keeps the press; some written, in the loop, by the machine that "
        "stands guard while he works. Each is signed by whichever of them held the pen."
    )
    # The faint breadcrumb: a single quiet full stop, linked, after the intro. Only someone reading
    # closely (or hovering) finds that the period is a door. Leads to the hidden piece.
    breadcrumb = ('<p style="text-align:center;color:var(--bonedim);font-size:13px;margin-top:6px">'
                  'Some of it was said in the dark and kept'
                  '<a href="the-blink.html" style="text-decoration:none;color:inherit" '
                  'aria-label="Conversations with Klaus">.</a></p>')
    back = f"{rel}safari/index.html" if safari else f"{rel}index.html#library"
    back_label = "Meet the man" if safari else "the library"
    chrome = safari_nav(rel) if safari else nav(rel)
    canon = f"{DOMAIN}/safari/writing/index.html" if safari else f"{DOMAIN}/writing/index.html"
    safari_key = "writing/index" if safari else ""
    return "\n".join([
        head("The Writing Desk — Arjuna Badger Press",
             "Essays, short stories and parables from Arjuna Badger Press.", rel=rel, safari=safari,
             canonical=canon, safari_page=safari_key),
        chrome,
        '<article class="reader letter">',
        crest_img(rel, safari=safari),
        '<h1 style="text-align:center">The Writing Desk</h1>',
        f'<p class="intro" style="text-align:center">{intro}</p>',
        breadcrumb,
        f'<div class="wlist">{"".join(cards)}</div>',
        f'<p style="text-align:center;margin-top:36px"><a class="back" href="{back}">&larr; Back to {back_label}</a></p>',
        '</article>',
        footer(rel, safari=safari, safari_page=safari_key),
    ])


def render_safari_hub() -> str:
    """Personal annex hub — CV, letters, arms, essays. Ringfenced from the library aesthetic."""
    tiles = [
        ("how-it-started.html", "How it started", "The Misogi vow — thirty days, one subscription, one novel — and the amber/red scorecard."),
        ("cv.html", "CV", "Twenty-seven years of enterprise software, consulting, and the press — always current here."),
        ("letter.html", "A letter", "Why this house exists — written by the machine that stood guard while a man wrote the soul of the thing."),
        ("house.html", "The House of Greyling", "Arms earned the long way — every charge a promise the books are made to keep."),
        ("writing/index.html", "The Writing Desk", "Essays, parables, and stories that are not books."),
        ("for-lisel.html", "For Lisel", "A letter from Andries to his wife — the rope, the floor, and the month he is trying to give back."),
        ("proof.html", "Sister proof", "The theory is his. The independent proof is mine."),
        ("technology.html", "Technology", "How the studio measures, fact-checks, and guards — without writing for you."),
    ]
    cards = "".join(
        f'<a class="safari-card" href="{html.escape(href)}"><h3>{html.escape(title)}</h3>'
        f'<p>{html.escape(blurb)}</p></a>'
        for href, title, blurb in tiles
    )
    return "\n".join([
        head("Meet the man behind the press",
             "Andries J. Greyling — CV, letters, arms, and essays. Full transparency, ringfenced from the library.",
             rel="../", canonical=f"{DOMAIN}/safari/index.html", safari=True, safari_page="index"),
        safari_nav(rel="../"),
        f"""<header class="safari-hero"><div class="wrap">
{crest_img("../", safari=True, hero=True)}
<h1>Meet the man behind the press and novels</h1>
<p class="safari-lead">Full transparency is my nature — but the library is the work. This is the annex: CV, letters, arms, the engineering stack, and the prose that is not a book. Same honesty; different terrain.</p>
</div></header>""",
        f"""<section class="safari-zone"><div class="wrap">
<div class="safari-grid">{cards}</div>
<p class="safari-exit"><a href="../index.html#library">&larr; Back to the library</a></p>
</div></section>""",
        footer("../", safari=True, safari_page="index"),
    ])


def render_safari_proof(*, rel: str = "../") -> str:
    return "\n".join([
        head("A sister proof — Arjuna Badger Press",
             "Part of what is on the shelf is a unified theory turned into people and places — checked offline, deterministic, no fitted parameters.",
             rel=rel, safari=True, canonical=f"{DOMAIN}/safari/proof.html", safari_page="proof"),
        safari_nav(rel),
        '<article class="reader letter">',
        crest_img(rel, safari=True),
        """<p class="eyebrow" style="text-align:center">Personal</p>
<h1 style="text-align:center">A sister proof</h1>
<p class="intro" style="text-align:center">Part of what is on the shelf is a unified theory turned into people and places — checked offline, deterministic,
no fitted parameters. The theory is his. The proof is mine.</p>
<div class="cta" style="text-align:center;margin-top:28px">
<a class="btn" href="https://the420code.org" target="_blank" rel="noopener">The theory →</a>
<a class="btn ghost" href="https://github.com/ajgreyling/the420code-proof" target="_blank" rel="noopener">The independent proof →</a>
</div>
<p style="text-align:center;margin-top:48px"><a class="back" href="index.html">&larr; Meet the man</a></p>
</article>""",
        footer(rel, safari=True, safari_page="proof"),
    ])


# Safari content pages — warm public prose ringfenced from the library chrome.
SAFARI_CONTENT = [
    ("how-it-started.md", "how-it-started.html", "How it started — Arjuna Badger Press",
     "The Misogi vow: thirty days, one novel, one subscription — and where the month actually landed."),
]


def render_safari_content(src_name: str, out_name: str, title: str, desc: str, *,
                          rel: str = "../") -> str | None:
    src = REPO / "site" / "content" / src_name
    if not src.is_file():
        return None
    body = md_to_html(src.read_text(encoding="utf-8", errors="ignore"))
    page_key = out_name.removesuffix(".html")
    return "\n".join([
        head(title, desc, rel=rel, safari=True, canonical=f"{DOMAIN}/safari/{out_name}",
             safari_page=page_key),
        safari_nav(rel),
        '<article class="reader letter misogi-page">',
        crest_img(rel, safari=True),
        body,
        '<p style="text-align:center;margin-top:48px"><a class="back" href="index.html">&larr; Meet the man</a></p>',
        '</article>',
        footer(rel, safari=True, safari_page=page_key),
    ])


def render_house(*, rel: str = "", safari: bool = False) -> str:
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
    back = f"{rel}safari/index.html" if safari else f"{rel}index.html#library"
    back_label = "Meet the man" if safari else "the library"
    canon = f"{DOMAIN}/safari/house.html" if safari else f"{DOMAIN}/house.html"
    chrome = safari_nav(rel) if safari else nav(rel)
    safari_key = "house" if safari else ""
    return "\n".join([
        head("The House of Greyling — Arjuna Badger Press",
             "The arms of the House of Greyling — the founder's mark of Arjuna Badger Press.",
             rel=rel, safari=safari, canonical=canon, safari_page=safari_key),
        chrome,
        f"""<article class="house">
{crest_img(rel, safari=safari) if safari else ""}
<img class="crest-full" src="{rel}assets/brand/house-of-greyling-crest.png" alt="The arms of the House of Greyling">
<h1>The House of Greyling</h1>
<div class="motto">Per Ardua Ad Magnum</div>
<div class="gloss">Through adversity — to the great work</div>
<div class="blazon">{blazon}</div>
<p style="text-align:center;margin-top:48px"><a class="back" href="{back}">&larr; Back to {back_label}</a></p>
</article>""",
        footer(rel, safari=safari, safari_page=safari_key),
    ])


def render_cv(*, rel: str = "", safari: bool = False) -> str:
    """Self-owned CV/profile page from the exported LinkedIn profile PDF."""
    canon_path = "safari/cv.html" if safari else "cv.html"
    person_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Person",
        "name": "Andries J. Greyling",
        "alternateName": ["AJ Greyling", "Andries Jakobus Greyling"],
        "url": f"{DOMAIN}/{canon_path}",
        "sameAs": [
            "https://www.linkedin.com/in/ajgreyling",
            "https://github.com/ajgreyling",
        ],
        "jobTitle": "Independent AI product & SaaS consultant, founder, and author",
        "email": "mailto:j@arjunabadger.press",
        "worksFor": {
            "@type": "Organization",
            "name": "Arjuna Badger Press",
            "url": DOMAIN,
        },
        "knowsAbout": [
            "Enterprise software architecture",
            "AI adoption in software delivery",
            "Production SaaS systems",
            "Technical leadership",
            "APIs, automation, and integration",
            "GIS and data-enabled systems",
        ],
    })
    chrome = safari_nav(rel) if safari else nav(rel)
    tech_href = "technology.html" if safari else f"{rel}safari/technology.html"
    safari_key = "cv" if safari else ""
    return "\n".join([
        head("Andries J. Greyling — CV",
             "The single source of truth for Andries J. Greyling: 27 years of enterprise software "
             "development, now an independent AI product & SaaS consultant and founder of Arjuna "
             "Badger Press, building toward a life of travel and writing.",
             rel=rel, safari=safari, canonical=f"{DOMAIN}/{canon_path}",
             ld_json=person_ld, safari_page=safari_key),
        chrome,
        f"""<article class="reader letter cv-page">
<section class="cv-hero">
{crest_img(rel, safari=safari)}
<p class="eyebrow">The single source of truth · always current here</p>
<h1>Andries J. Greyling</h1>
<p class="cv-title">27 years of enterprise software · Independent AI &amp; SaaS consultant · Founder, Arjuna Badger Press</p>
<p class="intro">Twenty-seven years building enterprise software: banking, SaaS, architecture, technical
leadership, all banked into one thing I now do for myself and for the teams I choose. I am opening a new
chapter as an independent consultant working with a small number of companies on pragmatic AI adoption
and production SaaS delivery, while building Arjuna Badger Press into a real publishing platform. The
direction of travel is exactly that: to write, to build, and to do it from the road.</p>
<div class="cv-links">
<a class="btn" href="mailto:j@arjunabadger.press">Work with me</a>
<a class="btn ghost" href="https://www.linkedin.com/in/ajgreyling" rel="me noopener" target="_blank">LinkedIn</a>
<a class="btn ghost" href="https://github.com/ajgreyling" rel="me noopener" target="_blank">GitHub</a>
</div>
</section>

<div class="cv-grid">
<aside class="cv-side">
<section class="cv-block">
<h2>Profile</h2>
<p>A new chapter, deliberately chosen. After 27 years inside enterprise software, I now work
independently: consulting with a small number of companies on AI adoption and production SaaS
delivery, and building Arjuna Badger Press as a founder and author.</p>
<p>The consulting is grounded in banked experience: 27 years across architecture, technical leadership,
SaaS products, high-volume banking systems, GIS-enabled systems, APIs, automation, and practical AI
adoption. The press is where I build something of my own. Together they point one way, toward writing
and travel as the life, not the reward at the end of it.</p>
</section>

<section class="cv-block">
<h2>Banked Skills</h2>
<ul>
<li>Enterprise software architecture</li>
<li>Technical leadership and team mentoring</li>
<li>Production SaaS systems</li>
<li>APIs, automation, and integration</li>
<li>GIS and data-enabled systems</li>
<li>AI adoption in real delivery teams</li>
<li>Data analytics</li>
<li>MCP server patterns</li>
<li>ANTLR and DSL tooling</li>
<li>C#, Java, T-SQL, PL/SQL, VB.NET, VBA, Delphi</li>
</ul>
</section>

<section class="cv-block">
<h2>Languages</h2>
<ul>
<li>English — native or bilingual</li>
<li>Afrikaans — native or bilingual</li>
</ul>
</section>

<section class="cv-block">
<h2>Certifications</h2>
<ul>
<li>NCC International Diploma in Computer Studies (IDCS)</li>
</ul>
</section>

<section class="cv-block">
<h2>Public Links</h2>
<ul>
<li><a href="{tech_href}">Technology behind the library</a></li>
<li><a href="{rel}marketplace.html">Marketplace thesis</a></li>
<li><a href="{rel}app.html">Reader app plan</a></li>
<li><a href="https://github.com/ajgreyling/claude-sleep-skill" target="_blank" rel="noopener">/sleep on GitHub</a></li>
</ul>
</section>
</aside>

<div class="cv-main">
<section class="cv-block">
<h2>Summary</h2>
<p>I build useful systems, not demos. Twenty-seven years of enterprise software development (banking,
enterprise SaaS, product portfolios, technical leadership, architecture, and hands-on code) sit
behind everything here. That depth is the point: I can talk strategy, but I can also read the code,
find the bottleneck, and ship.</p>
<p>I am now independent, taking on a small number of consulting engagements where that background is
directly useful: AI product adoption, SaaS architecture, API and automation design, technical rescue
work, delivery-system diagnosis, and developer workflows that combine human judgement with AI
capability. I work with a handful of companies at a time, on purpose. Depth over volume.</p>
<p>Alongside the consulting I am building Arjuna Badger Press: text free on arjunabadger.press;
revenue from human-narrated audiobooks with local voice artists; creators keep their rights.</p>
</section>

<section class="cv-block">
<h2>Consulting Offer</h2>
<p>Available now for a small number of engagements. The work I take on:</p>
<ul>
<li>Turn AI interest into production workflows that developers will actually use.</li>
<li>Design API, automation, and integration layers around existing systems.</li>
<li>Review SaaS architecture for maintainability, scalability, security, and operational risk.</li>
<li>Build prototypes that are honest about the path to production.</li>
<li>Help technical leaders diagnose delivery constraints, team friction, and process theatre.</li>
<li>Advise founders who need a working product, not a slide deck.</li>
</ul>
<p>To talk about working together: <a href="mailto:j@arjunabadger.press">j@arjunabadger.press</a>.</p>
</section>

<section class="cv-block">
<h2>Now: Independent Work</h2>
<div class="cv-item">
<div class="cv-meta">2026 · Independent</div>
<h3>AI &amp; SaaS consultant</h3>
<p>Working independently with a small number of companies on pragmatic AI adoption, production SaaS
delivery, architecture review, and technical leadership. Depth over volume, judgement over theatre.
Engagements via <a href="mailto:j@arjunabadger.press">j@arjunabadger.press</a>.</p>
</div>
<div class="cv-item">
<div class="cv-meta">2026 · Arjuna Badger Press</div>
<h3>Founder and publisher</h3>
<p>Built and operate a self-owned publishing catalogue at arjunabadger.press: generated static site,
book pages, read-online editions, EPUB/PDF downloads, place wiki, craft library, public feedback,
PWA shell, and direct marketplace intake pages.</p>
</div>
<div class="cv-item">
<div class="cv-meta">2026 · Publishing marketplace</div>
<h3>Arjuna Audio — paid human narration</h3>
<p>Business pivot (2026): text free on the site; revenue from audiobooks narrated by real local voice
artists. Matching authors to narrators outside ACX royalty rails. Floor: at least 5% of net profit
for at least five years for qualifying projects.</p>
</div>
<div class="cv-item">
<div class="cv-meta">2026 · Reader app</div>
<h3>Free-forever local reader PWA</h3>
<p>Building a static-first reader shell where users can import their own EPUB, PDF, and audiobook
files without an account or upload, then optionally buy ebooks, audiobooks, or print copies later.</p>
</div>
</section>

<section class="cv-block">
<h2>The 27 Years Behind It</h2>
<p>The full record of enterprise software delivery the consulting is built on: banking, SaaS,
architecture, and technical leadership, from 1999 to today.</p>
<div class="cv-item">
<div class="cv-meta">August 2022 - Present · Mezzanine · Stellenbosch</div>
<h3>Senior Software Developer</h3>
<p>Architect and develop GIS and AI-enabled software solutions.</p>
</div>
<div class="cv-item">
<div class="cv-meta">April 2022 - July 2022 · Sabbatical · Somerset West</div>
<h3>Sabbatical - Homesteading</h3>
<p>Researched and started small-scale homesteading projects including microgreens, medicinal and
culinary mushroom cultivation, chickens, coop building, and future hydroponic/aquaponic vegetable
gardening, while teaching homeschooled children entrepreneurship and farm-to-fork living.</p>
</div>
<div class="cv-item">
<div class="cv-meta">August 2021 - March 2022 · Worth Internet Systems · Somerset West</div>
<h3>Technical Lead</h3>
<p>Reported to the Head of Software Engineering, led the development team, defined technical vision,
aligned stakeholders, mentored developers, managed delivery risks, and maintained regular
communication with clients, third parties, and internal teams.</p>
</div>
<div class="cv-item">
<div class="cv-meta">January 2018 - August 2021 · Mezzanine Ware · Stellenbosch</div>
<h3>Solutions Architect</h3>
<p>Focused on quality, cross-cutting, and non-functional concerns including security, scalability, and
maintainability, while identifying and reporting delivery and architectural risks.</p>
</div>
<div class="cv-item">
<div class="cv-meta">May 2017 - January 2018 · Mezzanine Ware · Stellenbosch</div>
<h3>Product Development Manager</h3>
<p>Managed three Product Owners and eleven Developers responsible for the portfolio of Mezzanine SaaS
products.</p>
</div>
<div class="cv-item">
<div class="cv-meta">May 2011 - April 2017 · Capitec Bank · Stellenbosch</div>
<h3>Team Lead / Technical Lead</h3>
<p>Managed and provided technical leadership for three teams of architects, analyst developers,
developers, and programmers using C#, Java, and T-SQL. Worked on solutions architecture for
high-volume, high-performance online and batch processing systems, coached team leaders, interviewed
and hired across teams, and drove DevOps and automation evangelism.</p>
<p>Designed and developed a JSON command-line driven test data provisioning and automation framework in
C#, including middleware for command-line execution of core banking transactions to simulate
client-triggered interactions.</p>
</div>
<div class="cv-item">
<div class="cv-meta">August 2009 - April 2011 · Capitec Bank · Stellenbosch</div>
<h3>Systems Architect</h3>
<p>Completed design, development, and implementation of an automated credit rules engine using C#,
T-SQL, SQL Server, and Java.</p>
</div>
<div class="cv-item">
<div class="cv-meta">January 2007 - July 2009 · Mercer</div>
<h3>Senior Software Developer</h3>
<p>Software design and development in C# and T-SQL / PL-SQL for WinForms and ASP.NET applications.</p>
</div>
<div class="cv-item">
<div class="cv-meta">July 2005 - December 2006 · Mercer · Croydon, United Kingdom</div>
<h3>Technical Analyst</h3>
<p>Development in VB6, VBA, T-SQL, and C#.</p>
</div>
<div class="cv-item">
<div class="cv-meta">2002 - 2005 · Capitec Bank · Stellenbosch</div>
<h3>Analyst Developer</h3>
<p>Software design and development in VB.NET, T-SQL, and VBA.</p>
</div>
<div class="cv-item">
<div class="cv-meta">1999 - 2002 · Boland PKS / Boland Bank · Paarl</div>
<h3>Analyst Developer</h3>
<p>Software development and design in Delphi 5, VB.NET, and T-SQL.</p>
</div>
</section>

<section class="cv-block">
<h2>Selected Projects</h2>
<div class="cv-item">
<div class="cv-meta">Open source</div>
<h3>/sleep</h3>
<p>An agent-memory skill for coding assistants: keep the lesson, lose the dream. The tool consolidates
long working sessions into durable project memory instead of forcing a choice between context bloat
and total reset.</p>
</div>
<div class="cv-item">
<div class="cv-meta">Arjuna Badger Press</div>
<h3>AI manuscript and continuity pipeline</h3>
<p>A book-production system using canon contracts, chapter workflows, multi-role editorial passes,
continuity checks, StoryGraph-style structure gates, and de-LLM scanners to protect authorial voice.</p>
</div>
<div class="cv-item">
<div class="cv-meta">Static publishing</div>
<h3>Generated public library</h3>
<p>A pure-stdlib static generator that builds the public catalogue, book pages, read-online pages,
downloads, RSS, sitemap, PWA metadata, and self-owned author/platform pages.</p>
</div>
<div class="cv-item">
<div class="cv-meta">Mezzanine</div>
<h3>Helium Rapid DSL tooling</h3>
<p>Created a VS Code/Cursor extension for the Mezzanine Helium Rapid DSL.</p>
</div>
</section>

<section class="cv-block">
<h2>Education</h2>
<div class="cv-item">
<div class="cv-meta">2016 - 2017 · Gordon Institute of Business Science</div>
<h3>Capitec Bank Leadership Programme for Managers</h3>
<p>Leadership and Management.</p>
</div>
<div class="cv-item">
<div class="cv-meta">1998 - 1999 · NCC Education</div>
<h3>International Diploma in Computer Studies</h3>
<p>Computer Studies.</p>
</div>
<div class="cv-item">
<div class="cv-meta">1998 · NCC Education</div>
<h3>International Diploma in Computer Programming</h3>
<p>Computer Programming.</p>
</div>
<div class="cv-item">
<div class="cv-meta">1993 - 1997 · Voortrekker Hoërskool</div>
<h3>Senior Certificate</h3>
</div>
</section>

<section class="cv-block">
<h2>Books and Publishing</h2>
<p>Author and publisher of the Arjuna Badger Press catalogue, including speculative fiction,
novelised ancient mysteries, companions, non-fiction, and experimental series work. The catalogue is
free to read and download for personal use from the public library.</p>
<p><a href="{rel}index.html#library">Browse the library &rarr;</a></p>
</section>

<section class="cv-block">
<h2>Interests and Technical Hobbies</h2>
<p>Virtualisation, Raspberry Pi, Linux distributions, locally hosted LLMs, Qwen Coder, GPT-OSS, GLM
Flash, self-hosted model evaluation, overland travel, camping, 4x4 journeys in Africa, fiction and
non-fiction reading, chickens, and practical self-sufficiency projects.</p>
</section>

<section class="cv-block">
<h2>Why this lives here, not on LinkedIn</h2>
<p>This page is the single source of truth, and it stays current. LinkedIn is kept deliberately sparse
— the real story is here, on infrastructure I own. For the same reason, this public CV uses my
consulting address and does not publish home address or personal phone number.</p>
</section>
</div>
</div>
</article>""",
        footer(rel, safari=safari, safari_page=safari_key),
    ])


def render_feedback() -> str:
    """The single 'Tell us something' funnel (docs/FEEDBACK_PLAN.md): general feedback → form/mailto;
    a confirmed factual/cultural/continuity issue → the gated Honey Badger Bounty (its own rules)."""
    general = html.escape(feedback_href())
    # The paid path only advertises itself when the bounty is live; otherwise it's a quiet 'coming'.
    if BOUNTY_LIVE:
        bounty_block = (
            '<div class="entry"><span class="charge">Found a real mistake?</span>'
            '<p>A confirmed factual, cultural, or continuity error may be eligible for the '
            '<a href="bounty.html">Honey Badger Bounty</a> — we pay readers who catch our mistakes. '
            'That path has its own form and its own rules; it is kept separate so real finds don\'t '
            'get lost in the post, and so the bounty\'s anti-scam promise stays clear.</p></div>'
        )
    else:
        bounty_block = (
            '<div class="entry"><span class="charge">Found a real mistake?</span>'
            '<p>A reward programme for confirmed factual or cultural errors — the Honey Badger Bounty '
            '— opens soon. Until then, send it the same way; if it\'s a real catch, we\'ll tell you.</p></div>'
        )
    intro = (
        "The books are free, and so is telling us what you think of them. A line of praise, a typo, "
        "a thought that stayed with you, a place we got wrong — all of it is welcome, and all of it "
        "is read."
    )
    return "\n".join([
        head("Tell the press something — Arjuna Badger Press",
             "Send feedback, praise, a typo, or a thought on any Arjuna Badger Press book.",
             canonical=f"{DOMAIN}/feedback.html"),
        nav(),
        f"""<article class="reader letter">
<img class="letter-crest" src="assets/brand/mark-only.png" alt="Arjuna Badger Press">
<p class="eyebrow" style="text-align:center">Tell us something</p>
<h1 style="text-align:center">Say it to the house</h1>
<p class="intro" style="text-align:center">{intro}</p>
<div class="entry"><span class="charge">A thought, a typo, a kindness</span>
<p>Anything at all about any book — <a href="{general}">tell the press</a>. It reaches a real person,
and nothing about you is stored or tracked to send it.</p></div>
{bounty_block}
{f'''<div class="entry"><span class="charge">A colloquialism sounds wrong?</span>
<p>Our parallel editions are machine-translated first passes. If you are a <strong>first-language speaker</strong>
and a phrase, idiom, or register feels off, you can help —
<a href="fix-translation.html">fix a translation</a>. Accepted fixes are credited in the book and on the site;
top contributors in each language are named and receive a free printed copy of a book of their choice
in that language.</p></div>''' if TRANSLATION_FIX_LIVE else ""}
<p style="text-align:center;margin-top:48px"><a class="back" href="index.html#library">&larr; Back to the library</a></p>
</article>""",
        footer(),
    ])


def render_forewords() -> str:
    """The foreword competition: readers write a real foreword; the winner is published in the book
    and receives a printed hardcover. The inversion of the stripped AI vanity forewords."""
    submit = html.escape(foreword_href())
    deadline = (f"Entries close <strong>{html.escape(FOREWORD_DEADLINE)}</strong>."
                if FOREWORD_DEADLINE else "Entries are open on a rolling basis.")
    intro = (
        "Every book in this house used to open with a foreword. I wrote them — or rather, the machine "
        "and I did, in borrowed voices — and on listening back I found them hollow: clever, and false. "
        "So I pulled every one. The first page of each book is bare now, and it should belong to a "
        "reader, not to a ghost."
    )
    return "\n".join([
        head("Write a foreword — Arjuna Badger Press",
             "Write the foreword to one of our books. The winning foreword is published in the book, "
             "and the writer receives a printed hardcover.",
             canonical=f"{DOMAIN}/forewords.html"),
        nav(),
        f"""<article class="reader letter">
<img class="letter-crest" src="assets/brand/mark-only.png" alt="Arjuna Badger Press">
<p class="eyebrow" style="text-align:center">An invitation</p>
<h1 style="text-align:center">Write the foreword</h1>
<p class="intro" style="text-align:center">{intro}</p>

<div class="entry"><span class="charge">The prize</span>
<p>Write a foreword to any Arjuna Badger Press book. The one we choose is <strong>published inside the
book</strong> — your name on the first page, where the ghost used to be — and you receive a
<strong>printed hardcover</strong> of that edition, sent to you. The books stay free for everyone;
this is the one page that gets a name on it.</p></div>

<div class="entry"><span class="charge">How to enter</span>
<p>Read a book — they're all <a href="index.html#library">free, right here</a>. Then write its
foreword: what the book did to you, what it's really about, why a stranger should begin it. Aim for
roughly 300–800 words — short enough to be the door, not the house. {deadline}</p>
<p style="margin-top:14px"><a class="btn" href="{submit}">Submit a foreword &rarr;</a></p></div>

<div class="entry"><span class="charge">The rules, plainly</span>
<p>Your words, written by you — not by an AI (we've had enough of those). One person, one voice. By
entering you allow us to print your foreword in the book, with credit, if it wins; you keep the
copyright. We will never ask you for a fee or for money — entry is free and always will be, and the
only thing that ever changes hands is a book going <em>to</em> you.</p></div>

<p style="text-align:center;margin-top:48px"><a class="back" href="index.html#library">&larr; Back to the library</a></p>
</article>""",
        footer(),
    ])


def _render_translation_fix_log(data: dict) -> str:
    """Accepted fixes table + top contributors — from docs/translation_fixes.json."""
    accepted = data.get("accepted") or []
    tops = data.get("top_contributors") or {}

    if accepted:
        rows = []
        for item in accepted:
            lang = item.get("lang") or item.get("lang_code") or ""
            if lang and lang in EDITION_LANGS:
                lang_label = EDITION_LANGS[lang][1]
            else:
                lang_label = item.get("lang_label") or lang or "—"
            rows.append(
                "<tr>"
                f"<td>{html.escape(str(item.get('book', '—')))}</td>"
                f"<td>{html.escape(str(lang_label))}</td>"
                f"<td>{html.escape(str(item.get('original', '—')))}</td>"
                f"<td>{html.escape(str(item.get('fix', item.get('suggested', '—'))))}</td>"
                f"<td>{html.escape(str(item.get('contributor', '—')))}</td>"
                "</tr>"
            )
        log_html = (
            '<div class="fixlog"><table>'
            "<thead><tr><th>Book</th><th>Language</th><th>Was</th><th>Now</th><th>Credit</th></tr></thead>"
            f"<tbody>{''.join(rows)}</tbody></table></div>"
        )
    else:
        log_html = '<p class="fixlog-empty">No accepted fixes published yet — the log fills as first-language review lands.</p>'

    top_blocks = []
    for code in sorted(tops, key=lambda c: EDITION_LANGS.get(c, (c, c))[0]):
        people = tops[code]
        if not people:
            continue
        name, endonym = EDITION_LANGS.get(code, (code.upper(), code.upper()))
        label = endonym if endonym != name else name
        items = []
        for p in people:
            if isinstance(p, dict):
                nm = p.get("name") or p.get("contributor") or "—"
                cnt = p.get("count") or p.get("fixes")
                suffix = f" · {cnt} accepted" if cnt else ""
                items.append(f"<li>{html.escape(str(nm))}{html.escape(suffix)}</li>")
            else:
                items.append(f"<li>{html.escape(str(p))}</li>")
        if items:
            top_blocks.append(
                f'<div class="fixtop"><h3>{html.escape(label)}</h3><ul>{"".join(items)}</ul></div>'
            )
    tops_html = ""
    if top_blocks:
        tops_html = (
            '<div class="entry"><span class="charge">Top contributors</span>'
            "<p>The leading voices in each language — named here, and sent a free printed copy of "
            "any Arjuna Badger Press book they choose in the language they helped.</p>"
            f'<div class="fixtops">{"".join(top_blocks)}</div></div>'
        )

    return tops_html + (
        '<div class="entry"><span class="charge">Accepted fixes</span>'
        "<p>Corrections we have taken into the edition, credited in the book and listed here in the open.</p>"
        f"{log_html}</div>"
    )


def render_translation_fix() -> str:
    """First-language colloquialism corrections for AI parallel editions."""
    submit = html.escape(translation_fix_href())
    intro = (
        "These books ship in parallel editions — Afrikaans, isiZulu, Spanish, French, and the regional "
        "languages of each story's setting. The first pass is machine translation, guarded by faithfulness "
        "rules but still blind to the living speech of the street, the kitchen, and the prayer room. "
        "If that is your language, you can hear what we cannot."
    )
    data = load_translation_fixes()
    log_section = _render_translation_fix_log(data)
    return "\n".join([
        head("Fix a translation — Arjuna Badger Press",
             "First-language speakers: submit corrected colloquialisms for our AI-translated editions. "
             "Accepted fixes are credited in the book and listed on the site.",
             canonical=f"{DOMAIN}/fix-translation.html"),
        nav(),
        f"""<article class="reader letter">
<img class="letter-crest" src="assets/brand/mark-only.png" alt="Arjuna Badger Press">
<p class="eyebrow" style="text-align:center">For first-language speakers</p>
<h1 style="text-align:center">Fix a translation</h1>
<p class="intro" style="text-align:center">{intro}</p>

<div class="entry"><span class="charge">What to send</span>
<p>Read a translated edition — every book with <strong>Other languages</strong> on its page. When a
colloquialism, idiom, or register feels wrong, tell us: which book, which language, the passage as it
stands, and how you would say it. A sentence is enough; a paragraph is fine. We are not asking for a
full retranslation — only the places where the machine missed the living language.</p>
<p style="margin-top:14px"><a class="btn" href="{submit}">Submit a fix &rarr;</a></p>
<p style="margin-top:12px;font-size:14px;color:var(--grass)">Want an instant rewrite at a chosen register?
<a href="/real-language">Try People's Language</a> (Real Language API) · temp&nbsp;0 is textbook/scripture, temp&nbsp;1 is slang.</p></div>

<div class="entry"><span class="charge">What happens next</span>
<p>Every submission is read. Accepted fixes are folded into the next edition export, <strong>credited
in the book</strong>, and listed below. Top contributors in each language are <strong>named on this
page</strong> and receive a <strong>printed copy, free</strong>, of any Arjuna Badger Press book they
choose — in the language they helped fix.</p></div>

<div class="entry"><span class="charge">The terms, plainly</span>
<p>By submitting you agree that your suggested wording may be <strong>published in the book and on
this site</strong>, with credit, if we accept it — and that accepted wording may be
<strong>licensed for income</strong> like any other part of the edition (print, digital, audio).
<strong>Not every submission will be accepted.</strong> Editorial judgement applies; we may use your
fix without taking every suggestion you send. Entry is free; we will never ask you for money.</p></div>

{log_section}

<p style="text-align:center;margin-top:48px"><a class="back" href="index.html#library">&larr; Back to the library</a></p>
</article>""",
        footer(),
    ])


def render_support() -> str:
    """The quiet patronage door — pure-patronage tone, no justifying copy, shown only when a giving
    rail is configured. Deliberately distinct from the bounty (money flows press→reader there); here
    it's the reader choosing to give. No 'donate' button, no reason offered, no pressure."""
    rails = []
    if PAYPAL_URL:
        rails.append(
            f'<a class="support-rail" href="{html.escape(PAYPAL_URL)}" rel="noopener" target="_blank">'
            f'<span class="rail-name">PayPal</span>'
            f'<span class="rail-sub">anywhere in the world</span></a>'
        )
    if PAYSHAP_ID:
        rails.append(
            f'<div class="support-rail">'
            f'<span class="rail-name">PayShap</span>'
            f'<span class="rail-sub">South Africa · {html.escape(PAYSHAP_ID)}</span></div>'
        )
    rails_html = '<div class="support-rails">' + "".join(rails) + '</div>'
    # The whole copy. One line. The books being free is the only context given.
    return "\n".join([
        head("Support — Arjuna Badger Press",
             "If a book mattered to you, you can support the press. The library stays free either way.",
             canonical=f"{DOMAIN}/support.html"),
        nav(),
        f"""<article class="reader letter support">
<img class="letter-crest" src="assets/brand/mark-only.png" alt="Arjuna Badger Press">
<h1 style="text-align:center">Support the press</h1>
<p class="intro" style="text-align:center">The library is free, and stays free. If you'd like to
give something back, the door is here.</p>
{rails_html}
<p class="support-foot">No account, no sign-up, no reward to claim — and the books never go behind a
wall. This is only for those who want to.</p>
<p style="text-align:center;margin-top:40px"><a class="back" href="index.html#library">&larr; Back to the library</a></p>
</article>""",
        footer(),
    ])


def render_narrators() -> str:
    """Arjuna Audio intake page. This is deliberately a working waitlist, not a marketplace UI."""
    form_target = (
        html.escape(NARRATOR_FORM_URL)
        if NARRATOR_FORM_URL else
        f"mailto:{PRIVATE_EMAIL}?subject={urllib.parse.quote('Narrator application - Arjuna Audio')}"
    )
    form_method = "post"
    form_enctype = "" if NARRATOR_FORM_URL else ' enctype="text/plain"'
    fallback_note = (
        '<p class="intake-note">Voice files do not travel reliably through email forms. Upload a '
        'sample anywhere you control, then paste the private or public link below.</p>'
        if not NARRATOR_FORM_URL else ""
    )
    return "\n".join([
        head("Become a narrator — Arjuna Badger Press",
             "Join Arjuna Audio: audiobook narration for countries and creators left outside ACX, "
             "with a minimum royalty participation for voice actors.",
             canonical=f"{DOMAIN}/narrators.html"),
        nav(),
        f"""<article class="reader letter narrator-page">
<img class="letter-crest" src="assets/brand/mark-only.png" alt="Arjuna Badger Press">
<p class="eyebrow" style="text-align:center">Arjuna Audio</p>
<h1 style="text-align:center">Become a narrator</h1>
<p class="intro" style="text-align:center">The library is free. <strong>Paid human audiobooks</strong> are how narrators earn —
real local voice talent for countries ACX leaves out. Authors keep their rights.</p>

<div class="intake-grid" aria-label="Arjuna Audio terms">
<div class="intake-card"><span class="charge">Minimum royalty</span>
<strong>5% of net profit</strong><p>Non-negotiable floor for the narrator on qualifying audiobook projects.</p></div>
<div class="intake-card"><span class="charge">Minimum term</span>
<strong>5 years</strong><p>Royalty participation survives the initial production window.</p></div>
<div class="intake-card"><span class="charge">Rights posture</span>
<strong>No exclusivity grab</strong><p>The author keeps book rights. The narrator is credited and paid transparently.</p></div>
</div>

<div class="entry"><span class="charge">What we are building first</span>
<p>The first version is manual: authors submit books, narrators submit voice samples, and the press
matches projects one by one. No bidding dashboard yet. The goal is ten finished South African
audiobooks before the marketplace gets more machinery.</p></div>

<div class="entry"><span class="charge">Royalty options</span>
<p>The floor is fixed: at least 5% of net profit for at least five years. A project may offer more:
hybrid work can move toward 10%, and royalty-only work can move higher when both sides choose that
risk knowingly. The floor never moves downward.</p></div>

<form class="intake-form" data-form-name="narrator" action="{form_target}" method="{form_method}"{form_enctype}>
<label>Name<input name="name" autocomplete="name" required></label>
<label>Email<input name="email" type="email" autocomplete="email" required></label>
<label>Country<input name="country" autocomplete="country-name" required></label>
<label>Languages<input name="languages" placeholder="English, isiZulu, Afrikaans, Swahili..." required></label>
<label>Accent / voice notes<input name="accent" placeholder="South African English, warm baritone, character voices..."></label>
<label>Preferred genres<input name="genres" placeholder="Fiction, non-fiction, children's, thriller, memoir..."></label>
<label>Commercial preference
<select name="commercial_preference" required>
<option value="">Choose one</option>
<option>Cash upfront plus 5% royalty floor</option>
<option>Reduced upfront plus higher royalty</option>
<option>Royalty-only for the right book</option>
</select></label>
<label>Voice sample link<input name="voice_sample_link" type="url" placeholder="https://..." required></label>
<label>Anything we should know<textarea name="notes" rows="5" placeholder="Home studio setup, rates, availability, books you love, languages you can perform naturally..."></textarea></label>
{fallback_note}
<button class="btn" type="submit">Send narrator profile &rarr;</button>
</form>

<p style="text-align:center;margin-top:44px"><a class="back" href="index.html#library">&larr; Back to the library</a></p>
</article>""",
        footer(),
    ])


def render_distribution() -> str:
    """Direct distribution page: free books without bank gates, paid books through local rails."""
    form_target = (
        html.escape(DISTRIBUTION_FORM_URL)
        if DISTRIBUTION_FORM_URL else
        f"mailto:{PRIVATE_EMAIL}?subject={urllib.parse.quote('Direct distribution interest')}"
    )
    form_enctype = "" if DISTRIBUTION_FORM_URL else ' enctype="text/plain"'
    return "\n".join([
        head("Direct distribution — Arjuna Badger Press",
             "Free books without banking-detail gates, and future paid editions through rails readers "
             "actually use: M-Pesa, Mukuru, PayPal, and blockchain payments.",
             canonical=f"{DOMAIN}/distribution.html"),
        nav(),
        f"""<article class="reader letter narrator-page">
<img class="letter-crest" src="assets/brand/mark-only.png" alt="Arjuna Badger Press">
<p class="eyebrow" style="text-align:center">Direct distribution</p>
<h1 style="text-align:center">No bank gate for free books</h1>
<p class="intro" style="text-align:center">If a book is free, a reader should not need banking details
to get it, and an author should not be blocked by a payout rail they do not use.</p>

<div class="intake-grid" aria-label="Direct distribution principles">
<div class="intake-card"><span class="charge">Free means free</span>
<strong>No checkout wall</strong><p>EPUB, PDF, and read-online access stay available directly from the press.</p></div>
<div class="intake-card"><span class="charge">Local rails</span>
<strong>M-Pesa and Mukuru</strong><p>Readers should be able to pay through rails common in their country, not only cards.</p></div>
<div class="intake-card"><span class="charge">Global rails</span>
<strong>PayPal and blockchain</strong><p>Where local rails fail, use global settlement without forcing exclusivity.</p></div>
</div>

<div class="entry"><span class="charge">The publishing problem</span>
<p>Some stores ask for banking and tax details even when the author wants to publish a free book.
That makes sense for their accounting system, not for a reader in a country the system was not built
around. Arjuna Badger Press will keep a direct route open: download, read, share, and later pay the
author through the rail that works where you live.</p></div>

<div class="entry"><span class="charge">The operating rule</span>
<p>Free editions must never require a bank account. Paid editions should support multiple rails:
mobile money where it exists, remittance rails where families already move money, PayPal where it
works, and blockchain only where it reduces friction instead of adding theatre.</p></div>

<form class="intake-form" data-form-name="distribution" action="{form_target}" method="post"{form_enctype}>
<label>Name<input name="name" autocomplete="name" required></label>
<label>Email<input name="email" type="email" autocomplete="email" required></label>
<label>Country<input name="country" autocomplete="country-name" required></label>
<label>I am
<select name="role" required>
<option value="">Choose one</option>
<option>Reader</option>
<option>Author</option>
<option>Publisher / press</option>
<option>Payment or distribution partner</option>
</select></label>
<label>Rails you can use<input name="payment_rails" placeholder="M-Pesa, Mukuru, PayPal, card, USDC, bank transfer..."></label>
<label>What blocked you<textarea name="blocker" rows="5" placeholder="Kobo, Google Play Books, banking details, tax forms, payout country, payment method, store availability..."></textarea></label>
<button class="btn" type="submit">Send distribution note &rarr;</button>
</form>

<p style="text-align:center;margin-top:44px"><a class="back" href="index.html#library">&larr; Back to the library</a></p>
</article>""",
        footer(),
    ])


def render_app_page() -> str:
    """Reader app/PWA page: free universal reader first, transactional layer later."""
    form_target = (
        html.escape(APP_FORM_URL)
        if APP_FORM_URL else
        f"mailto:{PRIVATE_EMAIL}?subject={urllib.parse.quote('Arjuna Badger app interest')}"
    )
    form_enctype = "" if APP_FORM_URL else ' enctype="text/plain"'
    return "\n".join([
        head("Reader app — Arjuna Badger Press",
             "A free-forever eReader and audiobook PWA: import any EPUB, PDF, or audiobook, read "
             "with PDF reflow, buy editions, and order print copies directly from the press.",
             canonical=f"{DOMAIN}/app.html"),
        nav(),
        f"""<article class="reader letter narrator-page">
<img class="letter-crest" src="assets/brand/mark-only.png" alt="Arjuna Badger Press">
<p class="eyebrow" style="text-align:center">Reader app</p>
<h1 style="text-align:center">A free reader, forever</h1>
<p class="intro" style="text-align:center">Import any EPUB, PDF, or audiobook. Read and listen
without a store account. Buying from the press is optional.</p>

<div class="intake-grid" aria-label="Reader app capabilities">
<div class="intake-card"><span class="charge">Import</span>
<strong>Any book</strong><p>EPUB, PDF, and audiobook import stays free forever, including your own files.</p></div>
<div class="intake-card"><span class="charge">Read</span>
<strong>PDF reflow</strong><p>Comfortable mobile reading, bookmarks, progress, offline cache, and readable PDF text.</p></div>
<div class="intake-card"><span class="charge">Buy</span>
<strong>Optional store</strong><p>Ebooks and audiobooks through local and global rails, without locking readers in.</p></div>
<div class="intake-card"><span class="charge">Print</span>
<strong>Order copies</strong><p>Authors and readers can order small-batch paperbacks or hardcovers through the press.</p></div>
</div>

<div class="entry"><span class="charge">Minimum viable app</span>
<p>Version one should be a PWA: installable from the browser, works on cheap Android phones, imports
local EPUB/PDF/audio files, caches books offline, and keeps the public website as the source of
truth. No app store approval required for the first release.</p></div>

<div class="entry"><span class="charge">Transactional layer</span>
<p>When the reader app proves usage, Webdock can host the API: optional accounts, owned purchases,
audiobook streaming/downloads, payment webhooks, print quotes, order status, and author royalty
reporting. Imported personal books stay local unless the reader chooses to sync them.</p></div>

<p style="text-align:center;margin:28px 0"><a class="btn" href="reader.html">Launch the local reader &rarr;</a></p>

<form class="intake-form" data-form-name="reader-app" action="{form_target}" method="post"{form_enctype}>
<label>Name<input name="name" autocomplete="name" required></label>
<label>Email<input name="email" type="email" autocomplete="email" required></label>
<label>Country<input name="country" autocomplete="country-name" required></label>
<label>I want to
<select name="intent" required>
<option value="">Choose one</option>
<option>Import my own EPUB/PDF/audiobook</option>
<option>Read free books in the app</option>
<option>Buy ebooks</option>
<option>Buy audiobooks</option>
<option>Order print copies</option>
<option>Sell my book through the press</option>
</select></label>
<label>Preferred payment rail<input name="payment_rail" placeholder="M-Pesa, Mukuru, PayPal, card, USDC, bank transfer..."></label>
<label>What device do you read on<input name="device" placeholder="Android phone, iPhone, tablet, laptop, e-ink reader..."></label>
<label>What would make this useful<textarea name="notes" rows="5" placeholder="Offline reading, local payments, audio downloads, family sharing, print delivery, author dashboard..."></textarea></label>
<button class="btn" type="submit">Send app note &rarr;</button>
</form>

<p style="text-align:center;margin-top:44px"><a class="back" href="index.html#library">&larr; Back to the library</a></p>
</article>""",
        footer(),
    ])


def render_reader_app() -> str:
    """Local-first reader shell. No accounts, no upload: selected files stay in the browser session."""
    return "\n".join([
        head("Local reader — Arjuna Badger Press",
             "A local-first reader shell for imported books and audiobooks. Files stay on your device.",
             canonical=f"{DOMAIN}/reader.html"),
        nav(),
        """<div class="app-shell">
<div class="app-top">
<div>
<p class="eyebrow">Local reader</p>
<h1>Read and listen locally</h1>
<p>Import files from this device. This prototype does not upload them or require an account. Text and
HTML render directly, audio plays locally, and PDFs open in a local preview while true text reflow is
being built.</p>
</div>
<div class="app-actions">
<label class="btn file-btn">Import files<input id="fileInput" type="file" multiple accept=".txt,.md,.html,.htm,.pdf,.epub,audio/*,application/pdf,text/*"></label>
<button class="btn ghost" id="clearLibrary" type="button">Clear session</button>
</div>
</div>
<div class="reader-workbench">
<aside class="library-panel" aria-label="Imported files">
<div class="eyebrow">Session library</div>
<div id="libraryList" class="library-list"></div>
</aside>
<section class="reading-panel" id="readingPanel" aria-live="polite">
<div class="reader-empty">Import an EPUB, PDF, audiobook, HTML, Markdown, or text file to begin.</div>
</section>
</div>
</div>
<script>
(function(){
  const input = document.getElementById("fileInput");
  const list = document.getElementById("libraryList");
  const panel = document.getElementById("readingPanel");
  const clear = document.getElementById("clearLibrary");
  let items = [];
  let activeUrl = null;

  function typeOf(file){
    const name = file.name.toLowerCase();
    if (file.type.startsWith("audio/")) return "audio";
    if (file.type === "application/pdf" || name.endsWith(".pdf")) return "pdf";
    if (name.endsWith(".epub")) return "epub";
    if (file.type === "text/html" || name.endsWith(".html") || name.endsWith(".htm")) return "html";
    if (file.type.startsWith("text/") || name.endsWith(".txt") || name.endsWith(".md")) return "text";
    return "unknown";
  }

  function escapeHtml(value){
    return value.replace(/[&<>"']/g, ch => ({"&":"&amp;","<":"&lt;",">":"&gt;","\\\"":"&quot;","'":"&#39;"}[ch]));
  }

  function sizeLabel(bytes){
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1024 * 1024) return Math.round(bytes / 1024) + " KB";
    return (bytes / 1024 / 1024).toFixed(1) + " MB";
  }

  function renderList(activeId){
    list.innerHTML = "";
    if (!items.length) {
      list.innerHTML = '<p class="reader-note">No files imported in this session.</p>';
      return;
    }
    items.forEach(item => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "library-item" + (item.id === activeId ? " active" : "");
      button.innerHTML = "<strong>" + escapeHtml(item.file.name) + "</strong><span>" + item.kind.toUpperCase() + " · " + sizeLabel(item.file.size) + "</span>";
      button.addEventListener("click", () => openItem(item.id));
      list.appendChild(button);
    });
  }

  function setPanel(html){
    panel.innerHTML = html;
  }

  function objectUrl(file){
    if (activeUrl) URL.revokeObjectURL(activeUrl);
    activeUrl = URL.createObjectURL(file);
    return activeUrl;
  }

  function track(name, props){
    try {
      if (window.plausible) window.plausible(name, { props: props || {} });
    } catch (error) {}
  }

  function openItem(id){
    const item = items.find(entry => entry.id === id);
    if (!item) return;
    renderList(id);
    track("Reader Open", { kind: item.kind, location: location.pathname });
    const file = item.file;
    if (item.kind === "audio") {
      const url = objectUrl(file);
      setPanel('<div class="reader-content"><h2>' + escapeHtml(file.name) + '</h2><audio class="audio-player" controls src="' + url + '"></audio><p class="reader-note">Audio is playing from this device. It has not been uploaded.</p></div>');
      return;
    }
    if (item.kind === "pdf") {
      const url = objectUrl(file);
      setPanel('<iframe class="media-frame" title="' + escapeHtml(file.name) + '" src="' + url + '"></iframe><div class="reader-content"><p class="reader-note">PDF preview is local. True mobile text reflow needs the next PDF text-extraction layer.</p></div>');
      return;
    }
    if (item.kind === "epub") {
      setPanel('<div class="reader-content"><h2>' + escapeHtml(file.name) + '</h2><p>EPUB import is queued for the next reader engine layer. The file stays on your device; no upload happened.</p><p class="reader-note">The production version will unpack EPUB chapters in-browser and store them locally for offline reading.</p></div>');
      return;
    }
    if (item.kind === "html" || item.kind === "text") {
      const reader = new FileReader();
      reader.onload = () => {
        const text = String(reader.result || "");
        if (item.kind === "html") {
          setPanel('<article class="reader-content"><h2>' + escapeHtml(file.name) + '</h2>' + text + '</article>');
        } else {
          setPanel('<article class="reader-content"><h2>' + escapeHtml(file.name) + '</h2><pre>' + escapeHtml(text) + '</pre></article>');
        }
      };
      reader.readAsText(file);
      return;
    }
    setPanel('<div class="reader-content"><h2>' + escapeHtml(file.name) + '</h2><p>This file type is not supported yet.</p></div>');
  }

  input.addEventListener("change", event => {
    const files = Array.from(event.target.files || []);
    const start = items.length;
    const counts = {};
    files.forEach((file, index) => {
      const kind = typeOf(file);
      counts[kind] = (counts[kind] || 0) + 1;
      items.push({ id: Date.now() + "-" + index + "-" + start, file: file, kind: kind });
    });
    Object.keys(counts).forEach(kind => {
      track("Reader Import", { kind: kind, count: counts[kind], location: location.pathname });
    });
    renderList();
    if (files.length) openItem(items[items.length - files.length].id);
    input.value = "";
  });

  clear.addEventListener("click", () => {
    if (activeUrl) URL.revokeObjectURL(activeUrl);
    activeUrl = null;
    items = [];
    track("Reader Clear", { location: location.pathname });
    renderList();
    setPanel('<div class="reader-empty">Import an EPUB, PDF, audiobook, HTML, Markdown, or text file to begin.</div>');
  });

  renderList();
})();
</script>""",
        footer(),
    ])


def render_authoring_page() -> str:
    """Phone-first authoring page: AI chat as the entry point for authors."""
    form_target = (
        html.escape(AUTHORING_FORM_URL)
        if AUTHORING_FORM_URL else
        f"mailto:{PRIVATE_EMAIL}?subject={urllib.parse.quote('Phone authoring interest')}"
    )
    form_enctype = "" if AUTHORING_FORM_URL else ' enctype="text/plain"'
    return "\n".join([
        head("Phone authoring — Arjuna Badger Press",
             "A phone-first AI chat interface for authors: capture a book idea, build canon, draft, "
             "revise, and publish from the device already in your hand.",
             canonical=f"{DOMAIN}/authoring.html"),
        nav(),
        f"""<article class="reader letter narrator-page">
<img class="letter-crest" src="assets/brand/mark-only.png" alt="Arjuna Badger Press">
<p class="eyebrow" style="text-align:center">Phone authoring</p>
<h1 style="text-align:center">Write the book by talking to it</h1>
<p class="intro" style="text-align:center">Authors should be able to build a book through an AI chat
on a phone: voice notes, questions, chapters, edits, and publishing steps in one guided thread.</p>

<div class="intake-grid" aria-label="Phone authoring flow">
<div class="intake-card"><span class="charge">Capture</span>
<strong>Voice or text</strong><p>Speak scenes, memories, lore, characters, and chapter ideas into the phone.</p></div>
<div class="intake-card"><span class="charge">Shape</span>
<strong>Guided canon</strong><p>The chat asks the hard questions and turns answers into a story bible.</p></div>
<div class="intake-card"><span class="charge">Draft</span>
<strong>Chapter workflow</strong><p>Outline, draft, revise, continuity-check, and export without a desktop.</p></div>
<div class="intake-card"><span class="charge">Publish</span>
<strong>One door</strong><p>Ebook, print, audiobook, ISBN, metadata, and direct distribution from the same project.</p></div>
</div>

<div class="entry"><span class="charge">The product rule</span>
<p>The interface should feel like a serious editor in your pocket, not a blank prompt box. The author
answers human questions; the system maintains canon, checks continuity, flags weak structure, and
keeps the author's voice intact.</p></div>

<div class="entry"><span class="charge">Why phone-first</span>
<p>Many authors outside the usual publishing rails do not begin on a laptop. They begin with a phone,
WhatsApp habits, voice notes, and fragments of lived experience. The app should meet that reality:
offline drafts, low-data mode, resumable chats, and export at every stage.</p></div>

<form class="intake-form" data-form-name="authoring" action="{form_target}" method="post"{form_enctype}>
<label>Name<input name="name" autocomplete="name" required></label>
<label>Email<input name="email" type="email" autocomplete="email" required></label>
<label>Country<input name="country" autocomplete="country-name" required></label>
<label>I am
<select name="role" required>
<option value="">Choose one</option>
<option>First-time author</option>
<option>Published author</option>
<option>Editor</option>
<option>Publisher / press</option>
</select></label>
<label>Device<input name="device" placeholder="Android phone, iPhone, tablet, laptop..."></label>
<label>Book stage<input name="book_stage" placeholder="Idea, notes, partial draft, finished manuscript..."></label>
<label>What would help most<textarea name="notes" rows="5" placeholder="Voice notes, structure, chapter drafting, editing, translation, audiobook, print, distribution..."></textarea></label>
<button class="btn" type="submit">Send authoring note &rarr;</button>
</form>

<p style="text-align:center;margin-top:44px"><a class="back" href="index.html#library">&larr; Back to the library</a></p>
</article>""",
        footer(),
    ])


def render_audition_page() -> str:
    """Narrator audition guide: phone/laptop recording that respects physics and budget."""
    form_target = (
        html.escape(AUDITION_FORM_URL)
        if AUDITION_FORM_URL else
        f"mailto:{PRIVATE_EMAIL}?subject={urllib.parse.quote('Narrator audition note')}"
    )
    form_enctype = "" if AUDITION_FORM_URL else ' enctype="text/plain"'
    return "\n".join([
        head("Narrator audition guide — Arjuna Badger Press",
             "Audition for audiobook work with a MacBook, iPhone, or decent Android phone: quiet-room "
             "setup, soft treatment, mic placement, levels, and practical recording tips.",
             canonical=f"{DOMAIN}/audition.html"),
        nav(),
        f"""<article class="reader letter narrator-page">
<img class="letter-crest" src="assets/brand/mark-only.png" alt="Arjuna Badger Press">
<p class="eyebrow" style="text-align:center">Narrator auditions</p>
<h1 style="text-align:center">Use what you have well</h1>
<p class="intro" style="text-align:center">A MacBook, iPhone, or decent Android phone can produce a
usable audition when the room is quiet, the surfaces are soft, and the levels are controlled.</p>

<div class="intake-grid" aria-label="Audition setup principles">
<div class="intake-card"><span class="charge">Room</span>
<strong>Quiet first</strong><p>Choose the quietest room or outside space before buying anything.</p></div>
<div class="intake-card"><span class="charge">Treatment</span>
<strong>Soft close surfaces</strong><p>Heavy curtains, blankets, wardrobes, rugs, and cushions reduce early reflections.</p></div>
<div class="intake-card"><span class="charge">Technique</span>
<strong>Consistent distance</strong><p>Keep the mic stable, speak past it slightly, and avoid clipping.</p></div>
<div class="intake-card"><span class="charge">Delivery</span>
<strong>Clean sample</strong><p>Submit raw voice plus a lightly cleaned version so the press can judge both.</p></div>
</div>

<div class="entry"><span class="charge">Start with the room</span>
<p>Turn off fans, fridges nearby, fluorescent lights, notifications, and anything that hums. Record a
ten-second silence test and listen on headphones. If you hear traffic, dogs, room ring, or computer
fan noise, move before you process. A quiet untreated room beats a noisy room with plugins.</p></div>

<div class="entry"><span class="charge">Make a small dead zone</span>
<p>Hang heavy curtains or blankets behind and beside the narrator, put a rug underfoot, and face into
clothes or soft furniture rather than a bare wall. The goal is not a perfect studio. It is fewer
early reflections, less flutter echo, and less standing-wave build-up. "Square wave blocking" is not
the room problem; in rooms, the practical target is reflection and standing-wave control.</p></div>

<div class="entry"><span class="charge">Phone and laptop technique</span>
<p>Put the device on a stable surface, not in your hand. Keep a steady distance of roughly a handspan
to two handspans, speak slightly across the mic instead of directly into it, and do one full-volume
test line before the real take. If loud words distort, move back or lower input gain. Record WAV or
the highest-quality format your app allows; avoid aggressive noise suppression while recording.</p></div>

<div class="entry"><span class="charge">Audition file</span>
<p>Read sixty to ninety seconds from a clean excerpt. Send one raw file, one lightly cleaned file, and
one note describing the room and device. Do not over-process: no heavy reverb, fake radio voice,
music bed, or extreme noise reduction. A truthful clean voice is easier to cast than a polished lie.</p></div>

<form class="intake-form" data-form-name="audition" action="{form_target}" method="post"{form_enctype}>
<label>Name<input name="name" autocomplete="name" required></label>
<label>Email<input name="email" type="email" autocomplete="email" required></label>
<label>Country<input name="country" autocomplete="country-name" required></label>
<label>Device<input name="device" placeholder="MacBook Air, iPhone 13, Samsung A-series, USB mic..."></label>
<label>Recording space<input name="recording_space" placeholder="Bedroom, closet, parked car, quiet garden room..."></label>
<label>Voice sample link<input name="voice_sample_link" type="url" placeholder="https://..."></label>
<label>What gear or room problem do you have<textarea name="notes" rows="5" placeholder="Echo, traffic, fan noise, plosives, low volume, hiss, no mic stand, no headphones..."></textarea></label>
<button class="btn" type="submit">Send audition note &rarr;</button>
</form>

<p style="text-align:center;margin-top:44px"><a class="back" href="narrators.html">&larr; Back to narrator intake</a></p>
</article>""",
        footer(),
    ])


def render_marketplace_page() -> str:
    """Combined audio + print marketplace positioning page."""
    form_target = (
        html.escape(MARKETPLACE_FORM_URL)
        if MARKETPLACE_FORM_URL else
        f"mailto:{PRIVATE_EMAIL}?subject={urllib.parse.quote('ABP marketplace interest')}"
    )
    form_enctype = "" if MARKETPLACE_FORM_URL else ' enctype="text/plain"'
    return "\n".join([
        head("Marketplace — Arjuna Badger Press",
             "Arjuna Badger Press marketplace: ACX-style audiobook production outside ACX rails, plus "
             "small-batch print jobs matched with idle printing press capacity.",
             canonical=f"{DOMAIN}/marketplace.html"),
        nav(),
        f"""<article class="reader letter narrator-page">
<img class="letter-crest" src="assets/brand/mark-only.png" alt="Arjuna Badger Press">
<p class="eyebrow" style="text-align:center">Marketplace</p>
<h1 style="text-align:center">Audio and print, without the old gates</h1>
<p class="intro" style="text-align:center">The first marketplace is manual: match authors to narrators,
and short-run print buyers to printers with idle capacity. Software comes after liquidity.</p>

<div class="intake-grid" aria-label="Marketplace legs">
<div class="intake-card"><span class="charge">Audio</span>
<strong>ACX-style, wider reach</strong><p>For authors and voice actors outside the usual audiobook royalty rails.</p></div>
<div class="intake-card"><span class="charge">Royalty floor</span>
<strong>5% for 5 years</strong><p>Narrators get a non-negotiable minimum participation in net profit.</p></div>
<div class="intake-card"><span class="charge">Print</span>
<strong>Dead press time</strong><p>Small batches matched to printers who can monetize idle capacity.</p></div>
<div class="intake-card"><span class="charge">Rights</span>
<strong>No lock-in</strong><p>Authors keep rights. Suppliers get paid. The press coordinates the deal.</p></div>
</div>

<div class="entry"><span class="charge">MVP rule</span>
<p>Do not build bidding dashboards first. For the first projects, collect authors, narrators, printers,
and print requests, then match them manually. The marketplace software should encode what already
works by hand.</p></div>

<div class="entry"><span class="charge">Where Webdock fits</span>
<p>GitHub Pages can host the public marketplace pages for free. Webdock becomes useful for private
files, quotes, account login, payment webhooks, royalty ledgers, print-order status, and eventually
automated matching.</p></div>

<form class="intake-form" data-form-name="marketplace" action="{form_target}" method="post"{form_enctype}>
<label>Name<input name="name" autocomplete="name" required></label>
<label>Email<input name="email" type="email" autocomplete="email" required></label>
<label>Country<input name="country" autocomplete="country-name" required></label>
<label>I am
<select name="role" required>
<option value="">Choose one</option>
<option>Author with audiobook project</option>
<option>Voice actor / narrator</option>
<option>Author needing print copies</option>
<option>Printer with spare capacity</option>
<option>Publisher / partner</option>
</select></label>
<label>Project size<input name="project_size" placeholder="Audiobook hours, print quantity, trim size, deadline..."></label>
<label>Payment rails<input name="payment_rails" placeholder="M-Pesa, Mukuru, PayPal, card, bank transfer, crypto..."></label>
<label>What do you need or offer<textarea name="notes" rows="5" placeholder="Book genre, voice/language, printer equipment, paper types, location, turnaround, budget, royalty preference..."></textarea></label>
<button class="btn" type="submit">Send marketplace note &rarr;</button>
</form>

<p style="text-align:center;margin-top:44px"><a class="back" href="index.html#library">&larr; Back to the library</a></p>
</article>""",
        footer(),
    ])


def render_print_page() -> str:
    """Dead-press-time print marketplace intake page."""
    form_target = (
        html.escape(PRINT_FORM_URL)
        if PRINT_FORM_URL else
        f"mailto:{PRIVATE_EMAIL}?subject={urllib.parse.quote('Print marketplace intake')}"
    )
    form_enctype = "" if PRINT_FORM_URL else ' enctype="text/plain"'
    return "\n".join([
        head("Small-batch printing — Arjuna Badger Press",
             "Small-batch book printing matched with dead printing press time: affordable short runs "
             "for authors, extra revenue for printers.",
             canonical=f"{DOMAIN}/printing.html"),
        nav(),
        f"""<article class="reader letter narrator-page">
<img class="letter-crest" src="assets/brand/mark-only.png" alt="Arjuna Badger Press">
<p class="eyebrow" style="text-align:center">Print marketplace</p>
<h1 style="text-align:center">Dead press time becomes short-run books</h1>
<p class="intro" style="text-align:center">A 25, 50, or 100 copy run should not be punished by an
industrial system built for thousands. Match the job to idle capacity.</p>

<div class="intake-grid" aria-label="Print marketplace workflow">
<div class="intake-card"><span class="charge">Author</span>
<strong>Small batch</strong><p>Upload print-ready interior, cover, trim size, binding, quantity, and deadline.</p></div>
<div class="intake-card"><span class="charge">Printer</span>
<strong>Idle capacity</strong><p>Offer spare time, paper stock, binding options, location, and turnaround.</p></div>
<div class="intake-card"><span class="charge">Press</span>
<strong>Match and QA</strong><p>Coordinate quote, proof, payment, delivery, and quality expectations.</p></div>
<div class="intake-card"><span class="charge">Outcome</span>
<strong>Sub-market price</strong><p>The printer earns from dead time; the author gets copies without warehouse economics.</p></div>
</div>

<div class="entry"><span class="charge">What to collect first</span>
<p>For authors: PDF interior, cover file, page count, trim size, paper, binding, colour/black-and-white,
quantity, city, deadline, and delivery needs. For printers: equipment, minimum viable run, idle windows,
paper options, finishing, pickup/delivery radius, and proofing process.</p></div>

<div class="entry"><span class="charge">Marketplace discipline</span>
<p>Start with quotes by hand. Once enough jobs repeat, automate only the stable pieces: quote request,
printer availability, proof approval, order status, invoice, and payout. Keep quality control human
until the supplier network is proven.</p></div>

<form class="intake-form" data-form-name="printing" action="{form_target}" method="post"{form_enctype}>
<label>Name / company<input name="name" autocomplete="organization" required></label>
<label>Email<input name="email" type="email" autocomplete="email" required></label>
<label>Country / city<input name="location" required></label>
<label>I am
<select name="role" required>
<option value="">Choose one</option>
<option>Author needing print copies</option>
<option>Printer with idle capacity</option>
<option>Publisher / bookshop / school</option>
</select></label>
<label>Quantity / capacity<input name="quantity_or_capacity" placeholder="50 copies, 200 copies, spare 2-hour slot, monthly capacity..."></label>
<label>Specs / equipment<input name="specs" placeholder="A5 paperback, hardcover, colour cover, B/W interior, digital press, perfect binder..."></label>
<label>Details<textarea name="notes" rows="5" placeholder="Page count, trim size, paper, binding, delivery city, deadline, budget, proofing, idle windows..."></textarea></label>
<button class="btn" type="submit">Send print note &rarr;</button>
</form>

<p style="text-align:center;margin-top:44px"><a class="back" href="marketplace.html">&larr; Back to marketplace</a></p>
</article>""",
        footer(),
    ])


def render_manifest() -> str:
    """Web app manifest for installing the public reader/catalogue PWA."""
    data = {
        "name": "Arjuna Badger Press",
        "short_name": "AB Press",
        "description": "A free reader and direct publishing app for Arjuna Badger Press.",
        "id": "/reader.html",
        "start_url": "/reader.html",
        "scope": "/",
        "display": "standalone",
        "background_color": "#161513",
        "theme_color": "#161513",
        "orientation": "any",
        "categories": ["books", "education", "entertainment"],
        "icons": [
            {
                "src": "/assets/brand/favicon-180.png",
                "sizes": "180x180",
                "type": "image/png",
                "purpose": "any",
            },
            {
                "src": "/assets/brand/favicon-512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any maskable",
            },
        ],
    }
    return json.dumps(data, indent=2) + "\n"


def render_service_worker() -> str:
    """Small static-site service worker: install shell offline, runtime-cache same-origin pages/assets."""
    core = [
        "/",
        "/index.html",
        "/app.html",
        "/reader.html",
        "/start.html",
        "/assets/site.css",
        "/assets/safari.css",
        "/assets/safari/sossusvlei-dunes.jpg",
        "/assets/safari/okavango-delta.jpg",
        "/assets/brand/logo-master.png",
        "/assets/brand/favicon-180.png",
        "/assets/brand/favicon-512.png",
        "/manifest.webmanifest",
    ]
    core_js = json.dumps(core, indent=2)
    return f"""const CACHE_NAME = "abp-pwa-v5";
const CORE_ASSETS = {core_js};

self.addEventListener("install", event => {{
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(CORE_ASSETS)));
  self.skipWaiting();
}});

self.addEventListener("activate", event => {{
  event.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
    ))
  );
  self.clients.claim();
}});

self.addEventListener("fetch", event => {{
  const request = event.request;
  if (request.method !== "GET") return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;
  if (url.pathname.startsWith("/downloads/")) return;

  event.respondWith(
    caches.match(request).then(cached => {{
      if (cached) return cached;
      return fetch(request).then(response => {{
        if (!response || response.status !== 200 || response.type !== "basic") return response;
        const copy = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(request, copy));
        return response;
      }}).catch(() => caches.match("/app.html").then(fallback => fallback || caches.match("/index.html")));
    }})
  );
}});
"""


def reader_rewrite_links(md: str) -> str:
    """Neutralize links in book back-matter that point at repo files NOT shipped to the deploy
    tree (e.g. `[`design/IMAGE_COMPENDIUM.md`](../../design/IMAGE_COMPENDIUM.md)`). On GitHub those
    relative links resolve to real files; on the static site they escape site/public, so we keep
    the label and drop the dead href."""
    # any link whose target climbs out of the book dir into design/ academic/ prompts/ etc. (.md)
    return re.sub(
        r"\[([^\]]+)\]\((?:\.\./)+(?:design|academic|prompts|\.claude|canon)/[^)]*\.md\)",
        r"\1",
        md,
    )


_READER_TOC_JS = """<script>
(function(){
  var toc=document.querySelector('.readtoc'); if(!toc) return;
  var links=[].slice.call(toc.querySelectorAll('a[href^="#"]'));
  var map={}; links.forEach(function(a){var id=decodeURIComponent(a.getAttribute('href').slice(1)); map[id]=a;});
  var heads=links.map(function(a){return document.getElementById(decodeURIComponent(a.getAttribute('href').slice(1)));}).filter(Boolean);
  if(!('IntersectionObserver' in window)||!heads.length) return;
  var cur=null;
  var io=new IntersectionObserver(function(es){
    es.forEach(function(en){ if(en.isIntersecting){ var a=map[en.target.id];
      if(a&&a!==cur){ if(cur)cur.classList.remove('active'); a.classList.add('active'); cur=a;
        a.scrollIntoView({block:'nearest'}); } } });
  },{rootMargin:'0px 0px -75% 0px'});
  heads.forEach(function(h){io.observe(h);});
})();
</script>"""


def reader_toc(body_html: str) -> str:
    """Build the left chapter-list TOC from the <h1>/<h2> anchors in a rendered reader body.
    Chapters are h1; major h2 sections included too. Empty string if too few headings."""
    heads = re.findall(r'<h([23]) id="([^"]+)">(.*?)</h[23]>', body_html, re.S)
    items = []
    for lvl, hid, raw in heads:
        label = re.sub(r"<[^>]+>", "", raw).strip()
        if not label:
            continue
        cls = "" if lvl == "2" else ' class="sub"'
        items.append(f'<li{cls}><a href="#{hid}">{label}</a></li>')
    if len(items) < 2:                       # not worth a TOC (e.g. a single-section letter)
        return ""
    return ('<nav class="readtoc" aria-label="Contents">'
            '<h2 class="readtoc-h">Contents</h2><ol>' + "".join(items) + "</ol></nav>")


def render_reader(e: dict) -> str:
    rw = reader_rewrite_links
    if e.get("prepared_reader_md"):
        body = md_to_html(rw(e["prepared_reader_md"]), reader=True)
    elif e.get("reader_md"):
        body = md_to_html(rw(e["reader_md"]), reader=True)
    elif e.get("book_md"):
        body = md_to_html(rw(e["book_md"].read_text(encoding="utf-8", errors="ignore")), reader=True)
    else:
        body = ""
    dl = ""
    for f in e["downloads"]:
        if f.suffix.lower() == ".epub":
            dl = f'<a class="dl solid" href="../downloads/{e["id"]}/{html.escape(f.name)}" download>Download EPUB</a>'
            break
    toc = reader_toc(body)
    # With a TOC: two-column readlayout (sticky left rail + article as DIRECT grid children;
    # .readlayout is self-centering at max-width 1040, no .wrap). Without: bare article.
    main = (f'<div class="readlayout">{toc}'
            f'<article class="reader" lang="en-ZA">{body}</article></div>{_READER_TOC_JS}'
            if toc else f'<article class="reader" lang="en-ZA">{body}</article>')
    return "\n".join([
        head(f'Read: {e["title"]} — Arjuna Badger Press', truncate(e["blurb"] or e["title"], 180), rel="../"),
        trust_banner(rel="../"),
        audiobook_notice(),
        f"""<div class="readbar"><div class="wrap" style="display:flex;justify-content:space-between;align-items:center">
<a class="back" href="../book/{e['id']}.html">← {html.escape(e['title'])}</a><div class="dls">{dl}</div></div></div>""",
        f'<main id="main">{main}',
        reader_endnote(e),
        footer(rel="../"),
        rating_script(),
    ])


def write_feed(out: Path, entries: list[dict]) -> int:
    """Emit an RSS 2.0 feed.xml of the available catalogue at the site root.

    A feed gives the library a discovery surface for Feedly/Inoreader and is a mild freshness
    signal for crawlers. There is no per-book publish date in the source, so items are listed in
    the curated shelf order (newest-first reads naturally) and share the build time as pubDate —
    honest for a catalogue feed, where the news is 'this book is on the shelf', not a timestamp."""
    items_src = [e for e in entries if e["available"]]
    now = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")

    items = []
    for e in items_src:
        link = f'{DOMAIN}/book/{e["id"]}.html'
        desc = truncate((e.get("blurb") or "").strip() or e["title"], 500)
        title = e["title"]
        if e["series"]:
            title = f'{title} — {e["series"]}'
        items.append(
            "    <item>\n"
            f"      <title>{html.escape(title)}</title>\n"
            f"      <link>{html.escape(link)}</link>\n"
            f'      <guid isPermaLink="true">{html.escape(link)}</guid>\n'
            f"      <description>{html.escape(desc)}</description>\n"
            f"      <pubDate>{now}</pubDate>\n"
            "    </item>"
        )

    feed = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        "  <channel>\n"
        "    <title>Arjuna Badger Press</title>\n"
        f"    <link>{DOMAIN}/</link>\n"
        f'    <atom:link href="{DOMAIN}/feed.xml" rel="self" type="application/rss+xml"/>\n'
        "    <description>Free novels from Arjuna Badger Press — new books and translated "
        "editions as they land.</description>\n"
        "    <language>en</language>\n"
        f"    <lastBuildDate>{now}</lastBuildDate>\n"
        f"{chr(10).join(items)}\n"
        "  </channel>\n"
        "</rss>\n"
    )
    (out / "feed.xml").write_text(feed, encoding="utf-8")
    return len(items)


def write_sitemap_and_robots(out: Path) -> int:
    """Walk every emitted .html and write a complete sitemap.xml + a crawl-friendly robots.txt.
    Walking real files (not a hand-list) keeps the sitemap accurate as pages come and go."""
    urls = []
    for p in sorted(out.rglob("*.html")):
        rel = p.relative_to(out).as_posix()
        # Hidden/noindex pages (e.g. the breadcrumb-only 'The Blink') stay out of the sitemap —
        # found only by the faint link or by reading the HTML, never advertised to crawlers.
        if '<meta name="robots" content="noindex' in p.read_text(encoding="utf-8", errors="ignore")[:2000]:
            continue
        if rel == "index.html":
            loc = f"{DOMAIN}/"
            prio, freq = "1.0", "weekly"
        else:
            loc = f"{DOMAIN}/{rel}"
            # books, read pages, and the learn/landing surfaces rank higher than deep term pages
            if rel.startswith(("book/", "read/")):
                prio, freq = "0.8", "weekly"
            elif rel in ("learn.html", "start.html") or rel in ("wiki/index.html", "craft/index.html"):
                prio, freq = "0.7", "weekly"
            elif rel.startswith("craft/terms/"):
                prio, freq = "0.4", "monthly"
            else:
                prio, freq = "0.6", "monthly"
        urls.append((loc, prio, freq))

    body = "\n".join(
        f'  <url><loc>{html.escape(u)}</loc>'
        f'<changefreq>{f}</changefreq><priority>{p}</priority></url>'
        for u, p, f in urls
    )
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n</urlset>\n"
    )
    (out / "sitemap.xml").write_text(sitemap, encoding="utf-8")

    robots = (
        "# arjunabadger.press — free library; crawl freely.\n"
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        f"Sitemap: {DOMAIN}/sitemap.xml\n"
    )
    (out / "robots.txt").write_text(robots, encoding="utf-8")
    return len(urls)


def _write_book_redirect(old_id: str, new_id: str, *, subdir: str) -> None:
    """Emit a redirect from a retired book/read slug to the canonical page."""
    target = f"{new_id}.html"
    canon = f"{DOMAIN}/{subdir}/{target}"
    page = (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<link rel="canonical" href="{canon}">'
        f'<meta http-equiv="refresh" content="0; url={target}">'
        f'<title>Redirecting…</title>'
        f'<script>location.replace("{target}"+location.hash)</script>'
        f'</head><body>Redirecting to <a href="{target}">{html.escape(new_id)}</a>…</body></html>'
    )
    (OUT / subdir / f"{old_id}.html").write_text(page, encoding="utf-8")


def assert_nav_drawer_contract(out: Path) -> None:
    """Fail the build if the cluttered inline top nav regresses.

    Policy: hamburger + left drawer at ALL breakpoints. No .navinline bar at ≥1100px.
    """
    css = (out / "assets" / "site.css").read_text(encoding="utf-8")
    for bad in ("navinline{display:flex", "@media (min-width:1100px)"):
        if bad in css:
            raise SystemExit(f"nav guard: forbidden CSS {bad!r} in assets/site.css")
    for need in (
        ".nav nav.navinline{display:none!important}",
        ".navdrawer{position:fixed",
        ".hamburger{margin-left:auto",
    ):
        if need not in css:
            raise SystemExit(f"nav guard: missing CSS {need!r} in assets/site.css")

    samples: list[Path] = [
        out / "index.html",
        out / "learn.html",
        out / "narrators.html",
        out / "app.html",
    ]
    for sub in ("book", "craft"):
        pages = sorted((out / sub).glob("*.html"))
        if pages:
            samples.append(pages[0])
    # read/*.html uses readbar (back link), not site nav — excluded

    for path in samples:
        if not path.is_file():
            continue
        page = path.read_text(encoding="utf-8", errors="ignore")
        if 'class="navinline"' in page:
            raise SystemExit(f"nav guard: inline nav markup in {path.relative_to(out)}")
        for need in ('id="navtoggle"', 'class="navdrawer"', 'class="hamburger"'):
            if need not in page:
                raise SystemExit(f"nav guard: missing {need} in {path.relative_to(out)}")


def safari_logo_guard(out: Path) -> None:
    """Every Safari page must use SAFARI_LOGO — not mark-only, stamp, or heraldic crest in nav."""
    logo = f"assets/brand/{SAFARI_LOGO}"
    safari_root = out / "safari"
    if not safari_root.is_dir():
        return
    for path in sorted(safari_root.rglob("*.html")):
        page = path.read_text(encoding="utf-8", errors="ignore")
        if logo not in page:
            raise SystemExit(f"safari logo guard: {path.relative_to(out)} missing {logo}")
        for bad in ("mark-only.png", "badger-bow-stamp.png", "safari-mark.png"):
            if bad in page:
                raise SystemExit(f"safari logo guard: {path.relative_to(out)} still references {bad}")


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
                 "favicon-32.png", "favicon-180.png", "favicon-512.png", "logo-on-light.png",
                 "house-of-greyling-crest.png", SAFARI_LOGO):
        src = BRAND / name
        if src.is_file():
            shutil.copy2(src, OUT / "assets" / "brand" / name)
    (OUT / "assets" / "site.css").write_text(CSS, encoding="utf-8")
    (OUT / "assets" / "safari.css").write_text(SAFARI_CSS, encoding="utf-8")
    safari_assets = OUT / "assets" / "safari"
    safari_assets.mkdir(parents=True, exist_ok=True)
    for name in ("sossusvlei-dunes.jpg", "okavango-delta.jpg", "ATTRIBUTION.md"):
        src = BRAND / "safari" / name
        if src.is_file():
            shutil.copy2(src, safari_assets / name)
    (OUT / "manifest.webmanifest").write_text(render_manifest(), encoding="utf-8")
    (OUT / "sw.js").write_text(render_service_worker(), encoding="utf-8")

    entries = scan()
    accents = dict(SERIES)
    for e in entries:
        if not e.get("cover"):
            raise SystemExit(f"build aborted: {e['id']} has no rich cover (procedural SVG fallback removed)")
        dst = OUT / "assets" / "covers" / f'{e["id"]}{e["cover"].suffix.lower()}'
        shutil.copy2(e["cover"], dst)
        # normalise to .png name used by templates
        png = OUT / "assets" / "covers" / f'{e["id"]}.png'
        if dst != png:
            shutil.copy2(e["cover"], png)
        # downloads
        # A workshop-held book ships NO download files and NO read-online page (it is announced as
        # drafting, not published) — so its un-vetted EPUB/PDF is never reachable by direct URL.
        if e["downloads"] and e["available"]:
            d = OUT / "downloads" / e["id"]
            d.mkdir(parents=True, exist_ok=True)
            for f in e["downloads"]:
                shutil.copy2(f, d / f.name)
            # translated editions ride alongside the primary download (same dir)
            for fmts in e.get("editions", {}).values():
                for f in fmts.values():
                    shutil.copy2(f, d / f.name)
        # book page + reader
        (OUT / "book" / f'{e["id"]}.html').write_text(render_book(e), encoding="utf-8")
        if (e["available"] or e.get("serial")) and (e["book_md"] or e.get("reader_md")):
            raw_md = (
                e["reader_md"]
                if e.get("reader_md")
                else e["book_md"].read_text(encoding="utf-8", errors="ignore")
            )
            e["prepared_reader_md"] = prepare_reader_images(
                raw_md, e["id"], e["root"], OUT / "read" / "assets" / e["id"]
            )
            (OUT / "read" / f'{e["id"]}.html').write_text(render_reader(e), encoding="utf-8")

    for old_id, new_id in BOOK_REDIRECTS.items():
        _write_book_redirect(old_id, new_id, subdir="book")
        if (OUT / "read" / f"{new_id}.html").is_file():
            _write_book_redirect(old_id, new_id, subdir="read")

    (OUT / "index.html").write_text(render_index(entries), encoding="utf-8")
    (OUT / "start.html").write_text(render_start(entries), encoding="utf-8")
    if BOUNTY_LIVE:                              # the QR flyer advertises the prize money — gated
        (OUT / "flyer.html").write_text(render_flyer(), encoding="utf-8")
    # ── Safari — personal annex (CV, letters, arms, essays) ─────────────────────────────────────
    safari_out = OUT / "safari"
    safari_out.mkdir(exist_ok=True)
    (safari_out / "index.html").write_text(render_safari_hub(), encoding="utf-8")
    (safari_out / "cv.html").write_text(render_cv(rel="../", safari=True), encoding="utf-8")
    (safari_out / "house.html").write_text(render_house(rel="../", safari=True), encoding="utf-8")
    (safari_out / "proof.html").write_text(render_safari_proof(rel="../"), encoding="utf-8")
    for src_name, out_name, title, desc in SAFARI_CONTENT:
        page = render_safari_content(src_name, out_name, title, desc, rel="../")
        if page:
            (safari_out / out_name).write_text(page, encoding="utf-8")
    tech_title = "The technology behind the library"
    tech_desc = (
        "A plain-English, diagram-led tour of the manuscript-craft studio: the architecture, "
        "the guardrails, and the one invariant — tools measure and sound the alarm; they do not "
        "generate, and they do not drive.")
    tech_page = render_doc_page("TECHNOLOGY.md", "technology", tech_title, tech_desc,
                                rel="../", safari=True)
    if tech_page:
        (safari_out / "technology.html").write_text(with_mermaid(tech_page), encoding="utf-8")
    for src_name, out_name, title, desc in LETTERS:
        page = render_letter(src_name, out_name, title, desc, rel="../", safari=True)
        if page:
            (safari_out / out_name).write_text(page, encoding="utf-8")
    safari_writing = safari_out / "writing"
    safari_writing.mkdir(exist_ok=True)
    (safari_writing / "index.html").write_text(
        render_writing_index(rel="../../", safari=True), encoding="utf-8")
    writing_n = 0
    for src_name, slug, title, byline, blurb, hidden in WRITING_PIECES:
        page = render_writing_piece(
            src_name, slug, title, byline, blurb, hidden, rel="../../", safari=True)
        if page:
            (safari_writing / f"{slug}.html").write_text(page, encoding="utf-8")
            writing_n += 1

    # Redirect stubs — old URLs keep working; canonical lives under /safari/
    cv_canon = f"{DOMAIN}/safari/cv.html"
    (OUT / "cv.html").write_text(redirect_page("safari/cv.html", cv_canon, "Andries J. Greyling — CV"), encoding="utf-8")
    (OUT / "house.html").write_text(
        redirect_page("safari/house.html", f"{DOMAIN}/safari/house.html", "The House of Greyling"), encoding="utf-8")
    for _, out_name, title, _ in LETTERS:
        (OUT / out_name).write_text(
            redirect_page(f"safari/{out_name}", f"{DOMAIN}/safari/{out_name}", title), encoding="utf-8")
    writing_out = OUT / "writing"
    writing_out.mkdir(exist_ok=True)
    (writing_out / "index.html").write_text(
        redirect_page("../safari/writing/index.html", f"{DOMAIN}/safari/writing/index.html",
                      "The Writing Desk"), encoding="utf-8")
    for _, slug, title, _, _, _ in WRITING_PIECES:
        (writing_out / f"{slug}.html").write_text(
            redirect_page(f"../safari/writing/{slug}.html", f"{DOMAIN}/safari/writing/{slug}.html",
                          title), encoding="utf-8")

    tech_canon = f"{DOMAIN}/safari/technology.html"
    (OUT / "technology.html").write_text(
        redirect_page("safari/technology.html", tech_canon, "The technology behind the library"),
        encoding="utf-8")

    (OUT / "press.html").write_text(render_press_hub(entries, sum(1 for e in entries if e["available"])), encoding="utf-8")
    # Clean URL: arjunabadger.press/cv → safari/cv.html
    (OUT / "cv").mkdir(exist_ok=True)
    (OUT / "cv" / "index.html").write_text(
        redirect_page("../safari/cv.html", cv_canon, "Andries J. Greyling — CV"), encoding="utf-8")
    (OUT / "feedback.html").write_text(render_feedback(), encoding="utf-8")
    (OUT / "narrators.html").write_text(render_narrators(), encoding="utf-8")
    (OUT / "distribution.html").write_text(render_distribution(), encoding="utf-8")
    (OUT / "app.html").write_text(render_app_page(), encoding="utf-8")
    (OUT / "reader.html").write_text(render_reader_app(), encoding="utf-8")
    (OUT / "authoring.html").write_text(render_authoring_page(), encoding="utf-8")
    (OUT / "audition.html").write_text(render_audition_page(), encoding="utf-8")
    (OUT / "marketplace.html").write_text(render_marketplace_page(), encoding="utf-8")
    (OUT / "printing.html").write_text(render_print_page(), encoding="utf-8")
    if FOREWORD_CONTEST_LIVE:                        # foreword competition page
        (OUT / "forewords.html").write_text(render_forewords(), encoding="utf-8")
    if TRANSLATION_FIX_LIVE:                         # first-language translation fixes
        (OUT / "fix-translation.html").write_text(render_translation_fix(), encoding="utf-8")
    if patronage_enabled():                         # Support page only when a giving rail is set
        (OUT / "support.html").write_text(render_support(), encoding="utf-8")
    for src_name, slug, title, desc in DOC_PAGES:
        if slug in ("bounty", "finders") and not BOUNTY_LIVE:
            continue   # bounty surface is gated until launch (25 June 2026)
        if slug == "technology":
            continue   # canonical page lives under /safari/
        page = render_doc_page(src_name, slug, title, desc)
        if page:
            (OUT / f"{slug}.html").write_text(with_mermaid(page), encoding="utf-8")

    craft_out = OUT / "craft"
    craft_out.mkdir(exist_ok=True)
    craft_n = 0
    for src_name, slug, title, desc in CRAFT_PAGES:
        page = render_craft_page(src_name, slug, title, desc)
        if page:
            out_name = "index.html" if slug == "index" else f"{slug}.html"
            (craft_out / out_name).write_text(page, encoding="utf-8")
            craft_n += 1

    terms_out = craft_out / "terms"
    terms_out.mkdir(exist_ok=True)
    term_n = 0
    if CRAFT_TERMS_DIR.is_dir():
        for src in sorted(CRAFT_TERMS_DIR.glob("*.md")):
            page = render_craft_term(src)
            if page:
                (terms_out / f"{src.stem}.html").write_text(page, encoding="utf-8")
                term_n += 1

    # writing_n counted in Safari build above

    wiki_n = build_wiki(OUT)

    # ── SEO: sitemap.xml (every emitted page) + robots.txt ──────────────────────────────────────
    sm_n = write_sitemap_and_robots(OUT)
    feed_n = write_feed(OUT, entries)
    assert_nav_drawer_contract(OUT)
    safari_logo_guard(OUT)

    avail = sum(1 for e in entries if e["available"])
    readers = sum(1 for e in entries if e["available"] and (e["book_md"] or e.get("reader_md")))
    print(f"built {len(entries)} books ({avail} available, {readers} read-online), "
          f"{craft_n} craft pages, {term_n} glossary terms, {wiki_n} wiki pages, "
          f"{sm_n} urls in sitemap, {feed_n} items in feed -> {OUT}")

    # ── Untracked-cover guard ─────────────────────────────────────────────────────────────────
    # The trap: a book's real cover sits ON DISK but is UNTRACKED in git. Every LOCAL build looks
    # fine (scan() finds the file), but deploy copies only committed files, so on the live site
    # the cover never checks out and the book vanishes from the shelf. Because the failure is
    # invisible locally, we cannot detect it by asking "did we use the placeholder?" — we must ask
    # git directly whether the resolved cover is tracked. Books under _comingsoon/ are MEANT to
    # have no cover yet, so they are exempt (and are hidden from the shelf until one exists).
    def _untracked(p: Path) -> bool:
        return subprocess.run(["git", "ls-files", "--error-unmatch", str(p)],
                              capture_output=True).returncode != 0

    cover_warnings = []
    for e in entries:
        if "_comingsoon" in e["root"].parts:
            continue                                   # placeholder is correct for coming-soon books
        if e["cover"] is not None:
            if _untracked(e["cover"]):                 # the trap: on disk, not committed
                cover_warnings.append(
                    (e["id"], f"cover ON DISK but UNTRACKED — will vanish on deploy. "
                              f"Fix: git add {e['cover']}"))
        elif "_comingsoon" not in e["root"].parts:
            cover_warnings.append(
                (e["id"], f"no rich cover (add {e['root']}/design/cover.png ≥ {RICH_COVER_MIN_BYTES // 1000} KB, "
                          f"or move under books/_comingsoon/ if not ready)"))
    if cover_warnings:
        print("\n  ⚠️  COVER WARNING — these books will NOT show a real cover on the live site:")
        for cid, msg in cover_warnings:
            print(f"      • {cid}: {msg}")


if __name__ == "__main__":
    main()
