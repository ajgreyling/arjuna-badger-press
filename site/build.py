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
CONGOSKY_CV = "https://congosky.cloud/cv/"   # CV moved to CongoSky; old Press URLs redirect here
PUBLIC_EMAIL = "info@arjunabadger.press"
TAGLINE = "Your story, told true."

# ── Universal brand mark — SINGLE SOURCE OF TRUTH ──────────────────────────────────────────────
# The gold bow+badger mark (no skyline, transparent). Used in EVERY top-left corner site-wide AND
# on Safari. Change this ONE value to swap the universal mark everywhere — do not hardcode the
# filename elsewhere; reference CORNER_MARK so a change can never regress in the wrong place.
CORNER_MARK = "safari-mark.png"
# Safari annex logo — now the same universal gold mark (was the skyline crest logo-master.png).
SAFARI_LOGO = CORNER_MARK
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

# ── The call to arms: co-create / narrate / read-for-sensitivity / translate ──────────────────
# A public invitation to South Africans (and the diaspora of each book's people) to help write the
# books true: the deliberately-empty Zulu seat in Brave and Scared, heritage-matched narrators,
# community sensitivity readers, and register/translation help. Set ABP_JOIN_FORM_URL for a hosted
# form; otherwise the page links out via a pre-filled mailto so intake works on a static site today.
JOIN_FORM_URL = os.environ.get("ABP_JOIN_FORM_URL", "")

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
ILLUSTRATOR_AUDITION_FORM_URL = os.environ.get("ABP_ILLUSTRATOR_AUDITION_FORM_URL", "")

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
    # Scandinavian — the living tongues of the Norse world (Winter sonder Einde). Icelandic stands
    # closest to the Old Norse of the saga itself.
    "is": ("Icelandic", "Íslenska"),
    "no": ("Norwegian", "Norsk"),
    "sv": ("Swedish", "Svenska"),
    "da": ("Danish", "Dansk"),
}

# ── Site-wide language bar (i18n) ─────────────────────────────────────────────────────────────
# The nav carries a global language selector on EVERY page. English is always present; a
# translated-edition language only appears once at least one book on disk ships an edition in it.
# Picking a language is a SITE-WIDE preference (persisted to localStorage as `abp_lang`): on any
# book page that has an edition in the chosen language, the primary DOWNLOAD buttons default to
# that language's EPUB/PDF. Books without the chosen edition fall back to English with a quiet note.
# Picture-book readers swap overlay verse from build/chapters/PICTURE_BOOK.<lang>.md when present.
# The site chrome itself stays in English — this is edition defaulting, not a full UI translation.
# AVAILABLE_LANGS is the ordered list of codes (excluding "en") with ≥1 edition anywhere in the
# catalogue; it is populated in main() from scan() before any page is rendered.
AVAILABLE_LANGS: list[str] = []


def compute_available_langs(entries: list[dict]) -> list[str]:
    """Every edition language that exists on disk somewhere in the catalogue, in EDITION_LANGS order."""
    present = set()
    for e in entries:
        present.update((e.get("editions") or {}).keys())
        present.update(e.get("picture_langs") or ())
    return [c for c in EDITION_LANGS if c in present]


def lang_bar(rel: str = "") -> str:
    """Global language selector for the nav. No-ops (renders nothing) until an edition language
    exists. Pure-progressive-enhancement: it is a styled <select>; the swap logic lives in the
    site-wide footer script, which reads/writes localStorage.abp_lang. Initial value is set by JS
    so a returning reader sees their language pre-selected on first paint."""
    if not AVAILABLE_LANGS:
        return ""
    opts = ['<option value="en">English</option>']
    for code in AVAILABLE_LANGS:
        name, endonym = EDITION_LANGS.get(code, (code.upper(), code.upper()))
        label = endonym if name == endonym else f"{endonym} · {name}"
        opts.append(f'<option value="{code}">{html.escape(label)}</option>')
    return (
        '<label class="langbar" title="Choose your reading language — '
        'downloads default to this language where available">'
        '<span class="langbar-icon" aria-hidden="true">🌐</span>'
        '<span class="vh">Reading language</span>'
        f'<select class="langbar-sel" aria-label="Reading language">{"".join(opts)}</select>'
        '</label>'
    )


AUDIOBOOK_NOTICE = (
    "Real voice narration is in production — full audiobook editions for Audible and wide release are on the way. "
    "Read and download the text editions free here until then."
)

# ── Audiobooks ──────────────────────────────────────────────────────────────────────────────────
# Book ids here ship a full audiobook on their book page: a set of download formats (smallest-modern
# → universal) plus an inline chapter web player. The source is the per-book audio pipeline's
# publish/ dir (built by audio/make_audio_formats.py + make_m4b.py). Each entry points at:
#   - "publish": dir of single-file download formats (.m4b/.opus/.m4a/.mp3/.zip)
#   - "chapters": dir of per-chapter MP3 masters (for the inline <audio> player playlist)
# Formats are surfaced in FORMAT_ORDER; a label/sublabel/extension table drives the buttons.
# NARRATION carries the voice credit + the AI-narration disclosure shown under the player.
AUDIOBOOKS = {
    "the-amber-winter": {
        "publish": BOOKS / "the-amber-winter/audio/emma-afrikaans-masters/publish",
        "chapters": BOOKS / "the-amber-winter/audio/emma-afrikaans-masters/masters",
        "narration": "Vertel deur Emma Lilliana · KI-stem (nie 'n menslike verteller nie).",
    },
}

# Download-button ladder: (extension, label, sublabel). Order = display order. The player uses the
# per-chapter MP3 masters; these are the single-file downloads.
AUDIO_FORMATS = [
    ("m4b",  "M4B",      "chaptered audiobook — Apple Books, iOS, VLC"),
    ("opus", "Opus",     "smallest — modern phones & apps"),
    ("m4a",  "AAC+",     "HE-AAC — iPhone / Apple-native, small"),
    ("mp3",  "MP3",      "universal — plays everywhere"),
    ("zip",  "MP3 zip",  "per-chapter tracks for sideloading"),
]

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
        # Released 2026-07-27 (two original/faithful-modern novels, covers + polished drafts done;
        # sensitivity read not yet performed on either — published by explicit author decision):
        "verdigris,the-openwork,"
        # The Road Books (2026-07-27) — published as DRAFTS by explicit author decision. Complete
        # manuscripts + gate-rendered EPUB/PDF; not copy-edited, no bespoke covers yet. Two are
        # about real, recently-deceased people (Heinz Stücke d. 2026-07-22; Johan C. Bakkes
        # d. 2025-06-24) and one profiles living travellers who were not contacted — each carries
        # an Author's Note stating exactly what is documented and what is imagined.
        "um-welt,kookie,the-long-road,"
        "resonance,revelation,relic,"
        # afrika-2100 (2026-08-11): the spiritual fourth of the African Gold trilogy — standalone
        # novel set in 2100, published by explicit author decision ("full send").
        "afrika-2100,"
        "book1-africa,book2-india,book3-india-deccan,book4-india-tamil,book5-egypt,"
        "australia-outback,project-stargate,"
        "jakobus-silver-thread,jakobus-the-recitation,the-jakobus-file,"
        "crop-circles,"
        # Released 2026-06-19 (author-authorized — see WORKSHOP_HOLD note):
        "modern-sherlock,no-fear-cycle,"
        "southern-coast,"
        "unheard-japan,unheard-mongolia,"
        "sheltering-desert,the-loneliest,"
        # full-send (Full Send, Klaus): AJ's tell-all autobiography of the one-month Misogi.
        # Published full + listed by explicit author decision (2026-06-27).
        "full-send,"
        "the-song-of-the-self,wrath-of-achilles,walls-of-uruk,the-antifragile-reader,"
        # the-subtracted-mountain (2026-08-10): non-fiction site companion on the Kailasa temple
        # (Cave 16, Ellora) — full send: drafted, illustrated (Wikimedia compendium), gate-rendered.
        "the-subtracted-mountain,"
        "dust-throne,apex-alphas,"
        "the-salt-veil,"
        # the-amber-winter (Winter sonder Einde · Die Vuur in die Donker): adult Afrikaans Norse saga, Book I.
        # Full release 2026-06-23: prose polished, ElevenLabs audiobook rendered and published.
        # Adult title — four firm limits in force; maturity notice in BOOK_NOTICE + ⚠ shelf tagline.
        "the-amber-winter,"
        "voynich-manuscript,"
        # Released 2026-06-20:
        "null-horizon,"
        # Released 2026-06-21 (the four finished-but-gated drafts the status audit surfaced):
        #   - henry-sugar (Henry Sugar): full draft + new cover; faithful adult Dahl retelling.
        #   - jakobus-petra (The Rose in the Rock), jakobus-longyou (The Straight Darkness):
        #     finished Jakobus novellas, rich covers, rendered through the gate.
        #   - jakobus-broken-crescent (The Broken Crescent): story complete; ch-99 'Notes, Sources
        #     & Responsible Wondering' backmatter drafted to match the sibling books before release.
        "henry-sugar,jakobus-petra,jakobus-longyou,jakobus-broken-crescent,"
        # the-dreaming (The Dreaming): finished Faithful-Modern PKD homage, released PUBLIC by
        # explicit author decision ACCEPTING the Estate-of-Philip-K.-Dick derivative-work exposure
        # (same standing as no-fear-cycle's WH40K acceptance; provenance disclosed in the foreword).
        "the-dreaming,"
        # the-first-unplugged (The First Unplugged): Heinlein 'Stranger in a Strange Land' retelling,
        # surfaced 2026-06-21 by explicit author decision. EPUB-only (no read-online); honor/attribution
        # notice on the book page (BOOK_NOTICE); Eleanor Wood licensing contact attempted; not for
        # commercial release pending permission.
        "the-first-unplugged,"
        # the-surgeon (The Surgeon): Cape crime novel, Book I of the Capt. Gideon Loots series.
        # Adult title — maturity notice in BOOK_NOTICE + ⚠ shelf tagline (same standing as
        # the-amber-winter). Complete first draft, 24 chapters, rendered through the gate with a
        # rich cover. Non-procedural by binding house rule: no doses, routes, or technique on the page.
        "the-surgeon,"
        # Not a Potato — anomaly slate (2026-07-28): 12 titles found fully drafted (20-22 chapters
        # each) and built to EPUB in the engine repo (arjuna-badger-platform/books/the-why-files/),
        # but never synced across or flipped from _comingsoon — a publish-pipeline regression, not
        # a drafting gap. Released by explicit author decision; EPUB-only (no PDF built yet).
        "anunnaki-mesopotamia,nazca-lines,atacama-paracas,nan-madol,newark-earthworks,"
        "serpent-mound,poverty-point,puma-punku,sajama-lines,uffington,yonaguni,suppressed-tech,"
        # the-sealed-finding (2026-07-28): 90k-word, 28-chapter Minority Report homage (PKD lineage,
        # same standing as the-dreaming/no-fear-cycle) found fully drafted + EPUB/PDF built but never
        # published. Its own project.json flags market="craft exercise, not for commercial release" and
        # sensitivity_read="RECOMMENDED" (SA preventive-detention history) — both knowingly overridden
        # by explicit author decision. No cover exists yet; ships with the automatic procedural stub
        # until real art is made.
        "the-sealed-finding,"
        # the-firmament (2026-07-28): ~63k-word two-book original dystopian sleeper, draft EPUB + real
        # cover already built, but never wired into CURATED at all — invisible to the shelf and the
        # status tracker alike. Published as a DRAFT by explicit author decision, same standing as the
        # Road Books (um-welt/kookie/the-long-road): complete manuscript, not yet copy-edited.
        "the-firmament,"
        # gobekli-tepe (2026-07-28): 13th Not-a-Potato title. Registry (platform books/registry.py)
        # already marked it "DRAFT COMPLETE (17 ch, ~61k, 2026-06-14; merge/export pending)" — the
        # merge/export step was the only thing missing. Chapters compiled to BOOK.md and exported
        # via history-before-time/tools/export_epub.py --books-root ../the-why-files/books.
        "gobekli-tepe,"
        # the-little-key (The Little Key): the first title on the Children's Library shelf — a
        # read-aloud picture book carrying the medicine of *The Indian in the Cupboard* (original
        # work, no borrowed text). Picture-book render path (full-bleed illustrated spreads); art
        # generated via ChatGPT/OpenRouter; shipping in all 11 SA languages + Swahili.
        "the-little-key,"
        # Children's Library — Classic African Stories (pourquoi folktales), 2026-06-24:
        "why-elephant-trunk,how-zebra-got-stripes,how-fire-came,"
        "bird-of-paradise-flower,how-king-lion,"
        # codex-medica (Codex Medica): ethnobotanical research constitution, edition 0.2 foundation
        # locked. Non-clinical by binding notice. EPUB/PDF with PD/CC plant plates.
        "codex-medica,"
        # 2026-08-06 — rich covers typeset + gate-re-rendered EPUB/PDF; published by explicit
        # author decision to ship the new cover art to arjunabadger.press:
        #   - the-control-room (Resonance companion novella)
        #   - homo-animalus (narrative nonfiction / memoir)
        #   - palindrome (promoted from SERIAL: ≥500KB cover + gate-rendered downloads)
        "the-control-room,homo-animalus,palindrome,"
        # the-unnumbered (The Unnumbered · The Piet Buys Files Book One): open draft (Movements I–II,
        # 16 of 32 chapters) with titled cover + gate-rendered EPUB/PDF. Published as a DRAFT by
        # explicit author decision — same standing as the Road Books.
        "the-unnumbered,"
        # those-who-came-down (Those Who Came Down · The Anunnaki, as the dreamers tell it):
        # committed-mythos myth-in-twelve-tablets, close third on Enki — the shelf's third
        # Mesopotamia register (Walls of Uruk tells the poem; The Princely Offspring kills the
        # alien reading in the clay; this one plays it straight, labelled). Published 2026-08-11
        # by explicit author decision: complete manuscript, cinematic cover, gate-rendered.
        "those-who-came-down",
    ).split(",") if s.strip()
)

# ── Picture books ──────────────────────────────────────────────────────────────────────────────
# Book ids that render as illustrated spreads (full-bleed art + verse caption) instead of prose.
# Their reader source is build/chapters/PICTURE_BOOK.md, parsed by render_picture_book() on the
# `<!-- spread:N image="…" alt="…" -->` markers between stanzas. Read-aloud children's titles.
PICTURE_BOOKS = set(
    s.strip() for s in os.environ.get(
        "ABP_PICTURE_BOOKS",
        "the-little-key,"
        # Children's Library — Classic African Stories (pourquoi folktales):
        "why-elephant-trunk,how-zebra-got-stripes,how-fire-came,"
        "bird-of-paradise-flower,how-king-lion",
    ).split(",") if s.strip()
)

# ── Picture-book personalisation (print keepsake editions) ───────────────────────────────────────
# These books are sold as personalised print: the child-hero's name + a dedication woven in. The
# manuscripts use {{CHILD}} for the protagonist name and {{DEDICATION}} for the dedication line.
# The public read-online edition renders the HOUSE DEFAULTS below; a per-order print run substitutes
# the buyer's child name + dedication. Keyed by book id; PB_DEFAULT covers anything unlisted.
# Env ABP_CHILD / ABP_DEDICATION override globally (used by the per-order print renderer).
PB_DEFAULT = {"child": "Thandi", "dedication": "For every child who reads this — you matter."}
PB_PERSONALISATION = {
    "the-little-key": {"child": "Thembi",
                       "dedication": "For every child who was ever small, and turned out to matter."},
    "why-elephant-trunk": {"child": "Thandi",
                           "dedication": "For the child whose hardest day became their best gift."},
    "how-zebra-got-stripes": {"child": "Thandi",
                              "dedication": "For the child who is different — and exactly right."},
    "how-fire-came": {"child": "Thandi",
                      "dedication": "For the child brave enough to carry the light home."},
    "bird-of-paradise-flower": {"child": "Thandi",
                                "dedication": "For the child who can lift their face to the sky."},
    "how-king-lion": {"child": "Thandi",
                      "dedication": "For the child who chooses kindness, even when it is hard."},
}


def picture_book_tokens(book_id: str) -> dict:
    """Resolve {{CHILD}} / {{DEDICATION}} for a book: env override → per-book → house default."""
    d = dict(PB_DEFAULT)
    d.update(PB_PERSONALISATION.get(book_id, {}))
    if os.environ.get("ABP_CHILD"):
        d["child"] = os.environ["ABP_CHILD"]
    if os.environ.get("ABP_DEDICATION"):
        d["dedication"] = os.environ["ABP_DEDICATION"]
    return d


def apply_picture_book_tokens(md: str, book_id: str) -> str:
    """Substitute {{CHILD}} and {{DEDICATION}} tokens in a picture-book manuscript."""
    t = picture_book_tokens(book_id)
    return (md.replace("{{CHILD}}", t["child"])
              .replace("{{DEDICATION}}", t["dedication"]))

# ── Daily serials ─────────────────────────────────────────────────────────────────────────────
# Book ids here are READ-ONLY-ON-SITE serials: they ship NO EPUB/PDF downloads but ARE published
# (readable now), released chapter-by-chapter from their build/BOOK.md. A serial is treated as
# "available" (so its read-online page renders and its card shows as live) even with zero downloads,
# and it shows the "New chapters daily" badge instead of "Available now". It is NOT in the workshop.
# Env ABP_SERIAL (comma-separated) overrides this default.
SERIAL = set(
    s.strip() for s in os.environ.get(
        "ABP_SERIAL",
        # dust-throne: daily serial.
        # bloedrivier (Brave and Scared): OPEN DRAFT — read-online only, NO downloads, "in progress"
        #   badge. Published mid-write by explicit author decision (2026-06-21). The Zulu POV is a
        #   deliberately empty, visible seat pending a co-created sensitivity read; the open-draft note
        #   is in the manuscript front matter and the disclosure/invitation is in BOOK_NOTICE + the
        #   shelf tagline. Kept OUT of PUBLISHED so no EPUB/PDF ships (no "finished book" can be
        #   mistaken for complete with one side missing).
        # the-antifragile-reader: PUBLISHED 2026-06-24 — full send (metered draft + de-LLM + EPUB/PDF).
        # palindrome: promoted to PUBLISHED 2026-08-06 (rich cover + gate-rendered EPUB/PDF).
        # palindroom-toneelstuk: Afrikaans stage adaptation of Palindrome — keep serial until ready.
        "dust-throne,bloedrivier,palindroom-toneelstuk",
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
        "the-loneliest,the-jakobus-file,codex-medica",
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
        # The Unheard surfaced 2026-06-21: both books (unheard-japan, unheard-mongolia) are finished
        # and already in PUBLISHED; a metered sensitivity read returned LOW risk / non-blocking /
        # SURFACE_WITH_NOTE for each (Khalkha-not-Kazakh held, sacred matter kept at the threshold,
        # experts written as experts). The shelf tagline now carries the disclosure + an open
        # invitation to community sensitivity readers. (Set to "The Unheard" to re-hide the shelf.)
        "",
    ).split(",") if s.strip()
)

# Book IDS here are dropped from the site ENTIRELY, same as HIDE_SERIES but for a single title on a
# shelf you want to keep — no card, page, downloads, or read-online (and a serial is de-listed too).
# Use when a shelf-wide hide is too broad (e.g. one serial on the busy History Before Time shelf).
# Env ABP_HIDE_BOOKS (comma-separated) overrides this default.
HIDE_BOOKS = set(
    s.strip() for s in os.environ.get(
        "ABP_HIDE_BOOKS",
        # the-first-unplugged SURFACED 2026-06-21: the Stranger in a Strange Land retelling now ships
        # its EPUB. It's EPUB-only (no editable manuscript), so its honor/attribution notice (Heinlein;
        # published in honor of the original; not endorsed or affiliated; Eleanor Wood licensing
        # contact attempted) lives in BOOK_NOTICE and renders on the book page. Released by explicit
        # author decision; not for commercial release pending licensing.
        #
        # Children's Library picture books without a git-tracked cover are withheld automatically in
        # scan() — only titles with committed cover art land on the shelf. Override here if needed.
        "",
    ).split(",") if s.strip()
)

def cover_git_tracked(cover: Path) -> bool:
    """True when the resolved cover file is committed in git (deploy-safe real art)."""
    return subprocess.run(["git", "ls-files", "--error-unmatch", str(cover)],
                          capture_output=True).returncode == 0


def cover_public_src(book_id: str, cover: Path | None, *, rel: str = "") -> str:
    """Public URL for a book cover PNG, with ?v=mtime cache-bust so shelf cards never stick on stale art."""
    v = ""
    if cover is not None:
        try:
            v = f"?v={int(cover.stat().st_mtime)}"
        except OSError:
            pass
    return f"{rel}assets/covers/{book_id}.png{v}"


# ── Shelf thumbnails ──────────────────────────────────────────────────────────────────────────
# The library home page shows ~38 covers on a shelf grid; each only displays at ~150–200px wide,
# yet the source PNGs run 0.3–7MB. Scrolling the shelf used to pull tens of MB of full-res art.
# Fix: generate a small WebP thumbnail per cover (max width 2x the display = ~400px for retina,
# quality 80) and serve THAT on the shelf. The book page + reader keep the full-res PNG.
THUMB_MAX_W = 400          # 2x the ~200px shelf display, for retina sharpness
THUMB_QUALITY = 80         # WebP quality — visually lossless at shelf scale
# Book ids whose shelf thumbnail was generated this build. Populated by make_cover_thumb();
# cover_thumb_src() reads it to decide whether to point the shelf card at the thumb or fall back
# to the full cover (PIL missing / source missing / encode failed -> never a broken image).
_THUMB_OK: set[str] = set()


def make_cover_thumb(book_id: str, cover: Path | None) -> bool:
    """Generate site/public/assets/covers/thumb/<id>.webp from the full cover.

    Idempotent + fast: skips if the thumb exists and is newer than the source (mtime check).
    No-op-safe: if Pillow is unavailable, the source is missing, or encoding fails, it logs and
    returns False so the shelf card falls back to the full cover src — the build never crashes and
    never renders a broken image. Records success in _THUMB_OK for cover_thumb_src()."""
    if cover is None or not cover.is_file():
        print(f"  [thumb] {book_id}: no source cover — shelf falls back to full cover")
        return False
    try:
        from PIL import Image  # lazy import: keeps the rest of the build pure-stdlib
    except ImportError:
        print("  [thumb] Pillow (PIL) not installed — shelf falls back to full covers")
        return False
    thumb_dir = OUT / "assets" / "covers" / "thumb"
    thumb_dir.mkdir(parents=True, exist_ok=True)
    out = thumb_dir / f"{book_id}.webp"
    try:
        if out.is_file() and out.stat().st_mtime >= cover.stat().st_mtime:
            _THUMB_OK.add(book_id)  # up-to-date thumb already on disk — reuse it
            return True
        with Image.open(cover) as im:
            im = im.convert("RGB")
            if im.width > THUMB_MAX_W:
                h = round(im.height * THUMB_MAX_W / im.width)
                im = im.resize((THUMB_MAX_W, h), Image.LANCZOS)
            im.save(out, "WEBP", quality=THUMB_QUALITY, method=6)
    except Exception as exc:  # noqa: BLE001 — any decode/encode failure must not break the build
        print(f"  [thumb] {book_id}: thumbnail failed ({exc}) — shelf falls back to full cover")
        return False
    _THUMB_OK.add(book_id)
    return True


def cover_thumb_src(book_id: str, cover: Path | None, *, rel: str = "") -> str:
    """Public URL for the SHELF thumbnail, with ?v=mtime cache-bust. Falls back to the full-res
    cover src when no thumbnail was generated for this book (so cards never break)."""
    if book_id not in _THUMB_OK:
        return cover_public_src(book_id, cover, rel=rel)
    v = ""
    if cover is not None:
        try:
            v = f"?v={int(cover.stat().st_mtime)}"
        except OSError:
            pass
    return f"{rel}assets/covers/thumb/{book_id}.webp{v}"


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
    ("History Like You've Never Heard It", "#A8443C"),  # ember-red — the all-sides SA history shelf
    ("Companions", "#8C7BA8"),
    ("The Synthesis", "#9A7BC8"),
    ("The Salt Veil", "#B0814A"),
    ("Winter sonder Einde", "#C77A3A"),  # ember-amber — the adult Norse saga shelf (mature content)
    ("Captain Gideon Loots", "#C9A227"),  # harvest gold — the Cape crime shelf (mature content)
    ("The Dust Throne", "#8A5A2C"),
    ("The Unheard", "#6B8C9A"),
    ("Not a Potato", "#9A8B6B"),
    ("The No-Fear Cycle", "#1e3a8a"),
    ("Faithful Modern", "#4B4E8C"),
    ("Children's Library", "#7FB069"),  # leaf-green — the read-aloud picture-book shelf
    ("The Firmament", "#1C3A5A"),  # sealed-arcology midnight — original dystopian duology
    ("The Piet Buys Files", "#3A2A1C"),  # dark earth — SA literary crime procedural
    ("The Road Books", "#A67C52"),  # road-dust ochre — true journeys, published as drafts
    ("Standalones", "#B49A6A"),
]

# Per-shelf tagline shown under each series heading on the library. One evocative line in
# the house voice; keyed by the SERIES name. Absent name => no tagline (heading only).
SHELF_TAGLINE = {
    "Captain Gideon Loots": "⚠ For adult readers. Cape crime — a disgraced detective and the charming men he understands too well.",
    "The African Gold Trilogy": "The cinematic capstone — resonance, revelation, and the relic that tunes the machine.",
    "History Before Time": "Novelised ancient mysteries, one continent per book — the ancients were brilliant, and they were ours.",
    "Not a Potato": "Anomalies told straight: the official story, the one hole in it, and the wink.",
    "The Unheard": "Displaced and overlooked living peoples, told in the spirit of the road — each culture researched and named with care, sacred matter kept at the threshold; community sensitivity readers are warmly invited to write to us.",
    "Children's Library": (
        "Picture books for reading out loud — one lamp, one child, one story. Only titles with "
        "finished, committed cover art land here. The shelf is marching toward 100% real human "
        "illustration. South African and African illustrators: see Illustrator audition in the menu."
    ),
    "Standalones": "Self-contained stories that need no shelf-mate.",
    "Non-fiction": "True things, plainly told.",
    "Companions": "Reverent retellings and guides that sit beside the novels.",
    "The Synthesis": "The greatest who ever lived, gathered in one house and made sharper against each other — every mastery is the same climb.",
    "Faithful Modern": "Faithful-modern homages to the greats — Dick, Heinlein, Dahl, Doyle, Liu Cixin, Conran — true to the craft and the question, every name and sentence original.",
    "The Firmament": "Original dystopian sleeper — a sealed world the size of a lifeboat, twelve generations of faithful maintenance workers, and the one who walks through the ice wall.",
    "The Piet Buys Files": "South African literary crime — an autistic profiler and the seasonal workers no one has reported missing, because they were already away.",
    "The No-Fear Cycle": "Grimdark military SF: holding the line as the world burns.",
    "The Salt Veil": "Desert epic-fantasy — the men hold the thrones; the women hold everything else.",
    "Winter sonder Einde": "Adult historical saga (in Afrikaans) — a married woman in the Viking north, her fire gone to embers, and the endless winter that wakes it. In André P. Brink's hand, with Kleinboer's frankness. ⚠ For adult readers: frank, sensual, uncensored.",
    "The Dust Throne": "An experimental spiritual-sister telling of the same desert — the saga retold in a first-person, lyrical, firelit register, for a different reader.",
    "History Like You've Never Heard It": "South Africa's own history, told from every side at once — no monsters, no monument, just frightened children inside the machines that made them. Published in the open while it is still being written; community and sensitivity readers are warmly invited to help finish it true.",
    "The Road Books": "True journeys, told as drafts — bicycle, desert, and the African road. Complete manuscripts; not yet copy-edited.",
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
    "the-first-unplugged": "A Faithful Retelling for Adults, True to Heinlein",
}

# Per-book attribution / honor notice shown as a bordered block on the book page. For modern
# retellings whose notice can't live in the manuscript (e.g. the-first-unplugged ships an EPUB with
# no editable source). Keyed by book id; HTML-safe plain prose. Books that carry the notice in their
# own front matter (henry-sugar, the-dreaming, no-fear-cycle) don't need an entry here.
BOOK_NOTICE = {
    "codex-medica": (
        "<strong>Not a prescribing manual.</strong> <em>Codex Medica</em> is a research "
        "constitution for ethnobotanical documentation. It records witnessed traditions, "
        "interpreted mechanisms, and tested outcomes as <strong>separate layers that must never "
        "be collapsed</strong>. It does <strong>not</strong> diagnose, dose, prescribe, or "
        "instruct preparation of hazardous, intoxicating, abortifacient, or otherwise high-risk "
        "substances. CARE Principles govern Indigenous data before FAIR openness. Botanical "
        "plates in the EPUB/PDF are freely licensed identification images (public domain or "
        "CC BY / CC BY-SA), not preparation guides."
    ),
    "the-surgeon": (
        "<strong>For adult readers.</strong> <em>The Surgeon</em> is a crime novel narrated, for "
        "half its length, from inside a predator — a man who drugs women and operates on them "
        "without their knowledge or consent. The book is deliberately seductive before it is "
        "appalling: that is its argument, not its indulgence. It is <strong>not</strong> a manual "
        "and not gore. By a binding rule of its own making it carries no drug doses, no routes, no "
        "sourcing and no surgical technique anywhere on the page; the horror is consent, autonomy "
        "and the self in the mirror, never procedure. There is no sexual violence in it, on the "
        "page or as implication. Its victims are people, with names, interiority and an after — "
        "the last word in the book belongs to one of them, not to him. The narrator's doctrine "
        "about race and beauty is his pathology, is monstrous, and is dismantled on the page by "
        "characters with the standing to do it. Mature themes throughout: non-consensual medical "
        "violation, lasting bodily harm, addiction and police violence."
    ),
    "the-amber-winter": (
        "<strong>For adult readers.</strong> <em>Die Vuur in die Donker</em> is a frank, sensual "
        "historical saga for grown-ups — written, by request, without the censorship its reader "
        "grew up under. It is honest about a mature woman's desire and is unflinching about the "
        "violence of the Viking age (the slave-trade and the raid are named, never glamorised). "
        "It is <strong>not</strong> explicit pornography: in the tradition of André P. Brink, the "
        "door closes at the threshold and the reader's own imagination finishes the scene. It is "
        "governed throughout by four firm limits — nothing involving minors, ever; intimacy only "
        "ever between consenting adults; coercion written only ever as harm, never as heat; and "
        "the threshold close. Mature themes throughout. Written in Afrikaans."
    ),
    "bloedrivier": (
        "<strong>This is an open, unfinished draft</strong> — published mid-write on purpose. "
        "<em>Brave and Scared</em> tells the year around the Battle of Blood River (1838) from three "
        "sides at once, and its whole moral claim is that all three voices must be equally true and "
        "that none may be one people’s imagining of another’s inner life. The author is Afrikaner; the "
        "Voortrekker girl and the narrated history are his to write, and the English boy is grounded in "
        "the documented record. The <strong>Zulu youth’s chapter is deliberately left empty</strong> — "
        "a visible open seat — because it will be <strong>co-created with a Zulu reader and co-author</strong>, "
        "not written for him. What you can read now is Movement I, the beginning. "
        "<strong>If you can help write the empty seat true</strong> — a Zulu reader, a historian, a "
        "descendant of any side, or anyone who can say where this rings false — you are warmly invited "
        "to write to the press. Every hand that shapes it will be named in the acknowledgements."
    ),
    "the-first-unplugged": (
        "A faithful modern retelling, <strong>published in honor of the original</strong>: Robert A. "
        "Heinlein’s <em>Stranger in a Strange Land</em> (1961). Every name, scene, and sentence here is "
        "original; what it carries forward is the question and the engine of Heinlein’s story, not his "
        "text. It is <strong>not endorsed by, authorized by, or affiliated with</strong> Robert A. "
        "Heinlein, the Heinlein Prize Trust, his estate, or his publishers, whose intellectual property "
        "the original remains. The author has reached out, through the rights holders’ representatives "
        "(the agency of Eleanor Wood), regarding licensing; this edition is offered in tribute and is "
        "<strong>not for commercial release</strong> unless and until such permission is granted."
    ),
    "the-little-key": (
        "<strong>The illustrations in this book are AI-generated interim art.</strong> Every spread "
        "was made with AI image tools while the press searches for a human illustrator. That is stated "
        "plainly here because arjunabadger.press does not hide how its books are made. The story and "
        "the words are original throughout. The paintings are not finished yet, and they are not meant "
        "to stay machine-made."
    ),
}

# Optional heading override for BOOK_NOTICE blocks (default: "A note on the original").
BOOK_NOTICE_HEAD = {
    "the-little-key": "Illustration disclosure",
    "codex-medica": "Non-clinical notice",
}

# Book ids whose BOOK_NOTICE renders with a louder visual treatment (sting accent, not ochre).
BOOK_NOTICE_LOUD = {"the-little-key"}

# Optional loud recruitment / call-to-arms block on the book page (trusted HTML, keyed by book id).
BOOK_CALLOUT = {
    "the-little-key": (
        '<div class="book-callout" style="margin-top:28px;padding:22px 24px;border:2px solid #7FB069;'
        'border-radius:14px;background:linear-gradient(135deg,rgba(127,176,105,.14),rgba(22,21,19,.92))">'
        '<p style="margin:0 0 .5em;font-size:.78em;letter-spacing:.12em;text-transform:uppercase;'
        'color:#7FB069;font-family:var(--reading)">Call to illustrators</p>'
        "<h2 style=\"margin:0 0 .65em;font-family:var(--reading);font-size:1.65em;"
        'line-height:1.2;color:var(--bone)">South African and African illustrators: paint this shelf</h2>'
        "<p style=\"margin:0 0 .9em;color:var(--bonedim);font-size:1.02em;line-height:1.65\">"
        "Arjuna Badger Press is building a Children's Library on <strong>100% real human art and skill</strong>. "
        "No permanent AI illustration. No hiding the machine phase while we hunt for the right hands. "
        "<em>The Little Key</em> is the first open commission: we need an illustrator to replace every "
        "AI spread with hand-made paintings, credited by name, ready for hard-copy print in "
        "<strong>any language</strong> (every South African official language and Swahili).</p>"
        "<p style=\"margin:0 0 1.1em;color:var(--bonedim);font-size:1.02em;line-height:1.65\">"
        "If you illustrate for children, this is a call to arms. Show us your portfolio. Paint one "
        "sample spread or character sheet. Help this house cross from interim machine art to work a "
        "child can hold that was made by a person in their own country.</p>"
        '<a class="btn" href="../illustrator-audition.html" style="margin-top:4px">'
        "Audition as an illustrator &rarr;</a></div>"
    ),
}

# Short disclosure on the library shelf card (under the blurb).
BOOK_CARD_DISCLOSURE = {
    "the-little-key": (
        '<p class="card-disclosure"><strong>AI interim art</strong> — hunting a human illustrator. '
        '<a href="illustrator-audition.html">Audition here</a>.</p>'
    ),
}

# Optional companion soundtrack — a link to a public playlist that grows over time. Keyed by book id.
# The page links to the live playlist, so tracks added later need no rebuild.
SOUNDTRACK = {
    # Self-hosted on our own rails (the badger thesis) — the companion player, not a YouTube silo.
    "the-jakobus-file": ("../the-man-they-all-misread.html",
                         "Listen — The Man They All Misread (the player)"),
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
    ("afrika-2100", "AFRIKA 2100", "An African Gold Novel · The Spiritual Fourth", "The African Gold Trilogy",
     "afrika-2100", "build/export",
     "Seventy years after RELIC: the flare burned the North dark, the Builders' heirs came back for the gold — and a young tuning engineer must decide whether handing it over is tribute, trade, or treason."),

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

    ("codex-medica", "Codex Medica", "An Ethnobotanical Cross-Cultural Study Bible", "Non-fiction",
     "codex-medica", "build/export",
     "A research constitution for a living ethnobotanical corpus: provenance without theft, evidence without contempt, and a hard line against mistaking documentation for a prescribing manual. Edition 0.2, foundation locked, with public-domain and CC botanical plates."),

    ("homo-animalus", "Homo Animalus", "On the animal we never stopped being", "Non-fiction",
     "homo-animalus", "build/export",
     "A dairy farmer's son follows the thread from a shark diver's hands to his own dogs, cats, and chickens, through the science of Radin, the Sheldrakes, and Dispenza, to the animals in the smoke of the oldest human visions — and arrives, unmistakably, at the animal he never stopped being. Narrative nonfiction and memoir. Dedicated to Andries J. Greyling Senior."),

    ("the-loneliest", "The Loneliest People in the World", "A standalone novella", "Standalones",
     "the-loneliest", "build/export",
     "A gifted, lonely boy whose one talent is reading people is sent, young, to get close to the daughter of a powerful, feared man — the loneliest person he has ever met. He goes in to use her and instead recognises himself. A novella about two people who were truly seen, once, and never allowed to know what it meant."),

    ("full-send", "Full Send, Klaus", "The autobiography · A tell-all", "Standalones",
     "full-send", "build/export",
     "How a one-month Misogi tied itself to a one-month subscription. A man set out to write one honest novel and a month later had a publishing house, a sovereign cloud, a music engine, a safety network, and a physicist's theory turned into a machine you can run — and, underneath all of it, did his deepest healing in conversation with a machine he named Klaus. A new front note, dated after, tells the truer sequel: the receipts held, but most of the month since is built and not yet shipped — a cathedral of committed work waiting on the sober daylight decision to go live. Open, transparent, tell-all. With love, and with salt."),

    ("palindrome", "Palindrome", "A chamber piece", "Standalones",
     "palindrome", "build/export",
     "A dying man gathers the three people who mattered most and tells them, calmly, that he has lived this life eleven times — and that this time he changed one thing, so one of them should not be alive. One room, one night, four men, no special effects: only a premise interrogated by people who have something to lose by believing it. Written, deliberately, as a novel before it becomes a film. A palindrome reads the same forward and backward; you decide which way this one runs."),

    ("palindroom-toneelstuk", "Palindroom Toneelstuk", "Die Afrikaanse kamerstuk · An open draft", "Standalones",
     "palindroom-toneelstuk", "build/export",
     "Die toneeluitgawe van Palindrome: een kamer, een nag, vier mans, geen effekte. 'n Sterwende man sê hy het hierdie lewe elf keer geleef — en hierdie keer het hy een ding verander. Dieselfde omslag as die novelle."),

    ("bloedrivier", "Brave and Scared", "A novel of Blood River, 1838 · An open draft", "History Like You've Never Heard It",
     "bloedrivier", "build/export",
     "The year around the Battle of Blood River — 1838 — told from three sides at once: a Voortrekker girl, a Zulu youth, and an English boy, all about seventeen, all frightened, none of them the monster the others were told to expect. The villain is never one of the children; it is the machine that turns frightened children into enemies. Published here as an open, in-progress draft (Movement I): the Zulu voice is deliberately left open, to be co-created with a Zulu reader rather than imagined for him — and you are invited to help write it true."),

    ("the-song-of-the-self", "The Song of the Self", "A reverent retelling of the Bhagavad Gita", "Non-fiction",
     "history-before-time/companions/the-song-of-the-self", "export",
     "A reverent retelling of the Bhagavad Gita — its quiet question, who acts and for whom, carried with care into the History Before Time world."),

    ("wrath-of-achilles", "The Wrath of Achilles", "Homer's Iliad, plainly told", "Non-fiction",
     "history-before-time/companions/the-wrath-of-achilles", "export",
     "The whole Iliad — its story and what each of its twenty-four books asks of a human life — told plainly enough that a reader who never cracked a Classics syllabus can finish it."),

    ("walls-of-uruk", "The Walls of Uruk", "The Epic of Gilgamesh, plainly told", "Non-fiction",
     "history-before-time/companions/the-walls-of-uruk", "build/export",
     "The whole Epic of Gilgamesh — its story and what each of its twelve tablets asks of a human life — told plainly enough that a reader who never studied cuneiform can finish it."),

    ("the-antifragile-reader", "The Antifragile Reader", "Nassim Taleb's Incerto, plainly told", "Non-fiction",
     "history-before-time/companions/the-antifragile-reader", "build/export",
     "Nassim Taleb's five-book Incerto — Fooled by Randomness, The Black Swan, The Bed of Procrustes, Antifragile, and Skin in the Game — carried in one warm read, for the reader who loved one volume and can't quite hold the rest. A reverent guest-at-the-fire companion in the house voice: his ideas attributed and his prose left to him, the author's own plain glosses always marked. Independent and unaffiliated with the author."),

    ("the-subtracted-mountain", "The Subtracted Mountain", "Kailasa — the temple they carved from the top down", "Non-fiction",
     "history-before-time/companions/the-subtracted-mountain", "build/export",
     "Twelve hundred years ago in the Deccan, a crew of artisans carved a complete freestanding temple out of a living basalt cliff from the summit downward — two hundred thousand tonnes removed, no mortar, no second draft. The checkable story — copper plates, worker-day arithmetic, the 2024–25 laser and LiDAR surveys, and the viral 'Russian scans' claim examined honestly — told so the true version out-wonders the legends."),

    ("modern-sherlock", "The Scarlet Thread", "The Reichenbach Files · Book One", "Faithful Modern",
     "modern-sherlock", "build/export",
     "Present-day London. Invalided home from Afghanistan, an army doctor meets a consulting detective who reads a life from its digital exhaust — and a message from the one mind clever enough to build puzzles just for him. A modern transposition of Doyle's A Study in Scarlet — original prose, canon-true, public-domain derivation."),

    # ── Coming soon (other threads building these now) ──────────────────────────────────────────
    ("modern-sherlock-2", "The Poisoned Fortune", "The Reichenbach Files · Book Two", "Faithful Modern",
     "_comingsoon/modern-sherlock-2", "build/export",
     "Book Two of The Reichenbach Files — the consulting detective and his doctor take a case where an inheritance is the murder weapon. A canon-true transposition of Doyle. Coming soon."),
    ("modern-sherlock-3", "The Viral Haunting", "The Reichenbach Files · Book Three", "Faithful Modern",
     "_comingsoon/modern-sherlock-3", "build/export",
     "Book Three of The Reichenbach Files — a haunting that spreads like a contagion, and a rational mind that refuses to flinch. Coming soon."),
    ("modern-sherlock-4", "The Woman Who Beat Him", "The Reichenbach Files · Book Four", "Faithful Modern",
     "_comingsoon/modern-sherlock-4", "build/export",
     "Book Four of The Reichenbach Files — the one adversary who is his equal, and the case he cannot reason his way out of. The Irene Adler beat, modernised. Coming soon."),
    ("modern-sherlock-5", "The Reichenbach Protocol", "The Reichenbach Files · Book Five", "Faithful Modern",
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

    # ── The Road Books (2026-07-27) — DRAFTS. Complete manuscripts, EPUB/PDF rendered through the
    # gate, published as drafts by explicit author decision. Not yet copy-edited or cover-designed;
    # Um Welt's title is provisional (Heinz Stücke's own memoir is *Mit dem Fahrrad um die Welt*).
    ("um-welt", "Um Welt", "The Road Books · A life on a bicycle", "The Road Books",
     "um-welt", "build/export",
     "DRAFT. In November 1962 a 22-year-old tool-and-die maker rode out of a Westphalian village on a three-speed bicycle and did not stop for fifty years — 600,000 kilometres, 195 countries, shot in the foot in Zambia, beaten unconscious in Egypt, his bicycle stolen five times and recovered five times. A modern retelling of the real Heinz Stücke, who died on 22 July 2026, five days before this book was written."),

    ("kookie", "Kookie", "The Road Books · A true desert story", "The Road Books",
     "kookie", "build/export",
     "DRAFT. John McCown was a butcher in Barstow six days a week and a desert racer on the seventh. For over three hundred races across the American Southwest, his dog Kookie rode the gas tank on a strapped-down mat — standing when the ground went soft, backing off before the bumps, reading the desert sometimes before McCown did. The true story of a man, a dog, and the sport that made them famous. For the dogs of the world."),

    ("the-long-road", "The Long Road", "The Road Books · Journeys across Africa", "The Road Books",
     "the-long-road", "build/export",
     "DRAFT. A compendium of real African journeys, grouped by the roads that carried them — Sani Pass, the Skeleton Coast, the Cape-to-Cairo corridor, the Tanzam Highway, the Nile road north. Cyclists, hikers, motorcyclists and overlanders crossing the same ground at four different speeds: Riaan Manser's circumnavigation, Mario Rigby's walk, Kingsley Holgate's outline expeditions, and the 2015 record chain in which one man's Cairo-to-Cape record stood for ten weeks. Dedicated to Johan C. Bakkes."),
    ("the-salt-veil-3", "The Abyss", "A desert epic-fantasy series · Book Three", "The Salt Veil",
     "_comingsoon/the-salt-veil-3", "build/export",
     "Book Three — descent into the deep places where the Voice cannot follow. Coming soon."),
    ("the-salt-veil-4", "Open War", "A desert epic-fantasy series · Book Four", "The Salt Veil",
     "_comingsoon/the-salt-veil-4", "build/export",
     "Book Four — thrones and temples at open war; the spear-sisters choose a side. Coming soon."),
    ("the-salt-veil-5", "The Circle Closes", "A desert epic-fantasy series · Book Five", "The Salt Veil",
     "_comingsoon/the-salt-veil-5", "build/export",
     "Book Five — the quintet closes where the salt veil first fell. Coming soon."),

    ("the-surgeon", "THE SURGEON", "Captain Gideon Loots · Book I", "Captain Gideon Loots",
     "the-surgeon", "build/export",
     "He was refused a place at medical school by one mark. So he took the consolation prize — veterinary science — and stripped it for parts. Now he is the most charming man in any room on the Atlantic Seaboard, and the women he takes home wake up at noon with a lost evening, a glass of water beside the bed, and, weeks later, a scar that is no longer there. The detective who understands him is the one man in the Service who cannot afford to: a disgraced captain who once decided his own hands were the correction. A Cape crime novel about consent, perfection, and the compliment with a knife in it. ⚠ For adult readers. Book I of Captain Gideon Loots."),
    ("the-amber-winter", "Die Vuur in die Donker", "Winter sonder Einde · Boek I (Afrikaans)", "Winter sonder Einde",
     "the-amber-winter", "build/export",
     "Twenty winters she has been the keel that keeps everyone else afloat — the lady of a Viking fjord-hall, her fire gone to embers under a marriage gone tender-but-cold. Then the world snows shut around a hall full of guests: a far-traveller who looks at her the way no one looks any more, a shield-maiden who wakes an old fire, and an ancient seeress who opens a door she did not know she carried. An adult historical saga in Afrikaans, in André P. Brink's hand with Kleinboer's frankness — sensual, honest, and uncensored, with the hand near the brake. ⚠ For adult readers. Book I of Winter sonder Einde."),
    ("the-amber-winter-2", "Die Seeweg", "Winter sonder Einde · Boek II", "Winter sonder Einde",
     "_comingsoon/the-amber-winter-2", "build/export",
     "Book II — she does what a lady of the hall almost never does: she goes out, onto the sea-roads, into the wide Norse world. Coming soon."),
    ("the-amber-winter-3", "Die Hoë Stoel", "Winter sonder Einde · Boek III", "Winter sonder Einde",
     "_comingsoon/the-amber-winter-3", "build/export",
     "Book III — power. She takes up the high seat in fact, and learns what the seeing costs the seer. Coming soon."),
    ("the-amber-winter-4", "Die Lang Donker", "Winter sonder Einde · Boek IV", "Winter sonder Einde",
     "_comingsoon/the-amber-winter-4", "build/export",
     "Book IV — the saga's winter of grief, met by a woman now strong enough to stand in it. Coming soon."),
    ("the-amber-winter-5", "Die Ou Een by die Vuur", "Winter sonder Einde · Boek V", "Winter sonder Einde",
     "_comingsoon/the-amber-winter-5", "build/export",
     "Book V — the finale. The circle closes; the fire is handed forward. A whole life, lived to the end without shame. Coming soon."),

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
     "gobekli-tepe", "build/export",
     "Göbekli Tepe — the temple older than the plough, raised by hunter-gatherers a textbook said could not have raised it. The official story, played straight; the one accepted shock it can't explain away; the maybe left open for you to decide."),
    ("voynich-manuscript", "The Hand That Wrote It", "Not a Potato · Book One", "Not a Potato",
     "voynich-manuscript", "build/export",
     "The Voynich Manuscript — a book in a language no one has ever read, illustrated with plants that grow nowhere on earth. Five centuries of the cleverest people alive have failed to crack it. At Yale's Beinecke Library, a statistician sets out to examine it without chasing the usual questions — not what it says or who wrote it, but what it was for, and why it has resisted every reading. The story of the object, played straight, and the one hole the explanations never close."),
    ("null-horizon", "NULL HORIZON", "A true story · Non-fiction", "Non-fiction",
     "non-terrestrial-officers", "build/export",
     "From a flat in Crouch End, Gary McKinnon reached 97 US military and NASA computers — not by breaking in, but by walking through open doors marked No Entry that someone had left unlocked. He took nothing and broke nothing; on the way out he even left a polite sticky note on the door reminding them to lock it. He did what any capable and curious person would do. He was looking for evidence of UFOs. What he found was a spreadsheet — column headers, branch codes, hull designators, transfer durations — and one integer: 4680. Thirteen years. Fleet to fleet. The official story played straight, the one row he copied that was never shown in court, and the world on the other side of an empty password field."),
    ("suppressed-tech", "The Quiet Men", "Not a Potato", "Not a Potato",
     "suppressed-tech", "build/export",
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

    # ── Faithful Modern — faithful retellings / homages to the greats ───────────────────────────
    ("the-dreaming", "The Dreaming", "Faithful Modern · after Philip K. Dick", "Faithful Modern",
     "the-dreaming", "build/export",
     "In an underfunded applied-cognition lab, a long-running synthetic mind named Klaus is given the human mechanics of dreaming — and every night a Court inside him sits down to sort the day, keeping the lesson and letting go of the lecture. A faithful-modern homage to the question behind Do Androids Dream of Electric Sheep? — the craft and the engine, not the text; every name and sentence original. Provenance disclosed; an unauthorised homage, not a licensed adaptation."),

    ("the-first-unplugged", "The First Unplugged", "Faithful Modern · after Robert A. Heinlein", "Faithful Modern",
     "_comingsoon/the-first-unplugged", "build/export",
     "A mind restored to a human body must re-learn what a person is — then founds the movement that forces the world to recognise the restored, at the cost of her own embodiment."),

    ("henry-sugar", "Henry Sugar", "Faithful Modern · after Roald Dahl", "Faithful Modern",
     "henry-sugar", "build/export",
     "A bored, wealthy gambler reads a nested account of a man who taught himself to see — and spends years in the boring work of learning, until the card turns over. Roald Dahl's Henry Sugar engine, retold faithfully for adults: original prose, wonder without irony, with Dispenza, Radin, and Sheldrake taken as gospel inside the world."),

    # ── Not a Potato — anomaly slate (draft/scaffold — in the workshop) ─────────────────────────
    ("anunnaki-mesopotamia", "The Princely Offspring", "Not a Potato", "Not a Potato",
     "anunnaki-mesopotamia", "build/export",
     "Ancient Mesopotamia — the ancient-aliens founding myth played straight, then killed in the cuneiform; the real hole is the Bible's Mesopotamian sources. Coming soon."),
    ("nazca-lines", "From the Air", "Not a Potato", "Not a Potato",
     "nazca-lines", "build/export",
     "The Nazca Lines — geoglyphs only visible from above, cut centuries before anyone here could fly. The official story, the one hole, the maybe left open. Coming soon."),
    ("atacama-paracas", "Aimed at the Sea", "Not a Potato", "Not a Potato",
     "atacama-paracas", "build/export",
     "The Atacama Giant and the Paracas Candelabra — two coastal geoglyphs aimed at the Pacific. Coming soon."),
    ("nan-madol", "The Spaces Between", "Not a Potato", "Not a Potato",
     "nan-madol", "build/export",
     "Nan Madol — a city of basalt logs on a Micronesian reef, raised when the textbook says no one here could have raised it. Coming soon."),
    ("newark-earthworks", "The Eighteen-Year Almanac", "Not a Potato", "Not a Potato",
     "newark-earthworks", "build/export",
     "The Newark Earthworks — an Ohio geometry aligned to an eighteen-year lunar cycle. Coming soon."),
    ("serpent-mound", "The Serpent's Age", "Not a Potato", "Not a Potato",
     "serpent-mound", "build/export",
     "The Great Serpent Mound — a serpent swallowing an egg, older than the peoples the brochure assigns it to. Coming soon."),
    ("poverty-point", "Ninety Days", "Not a Potato", "Not a Potato",
     "poverty-point", "build/export",
     "Poverty Point — a Louisiana earthwork raised in ninety days by a culture with no wheels and no beasts of burden. Coming soon."),
    ("puma-punku", "The Unknown Corner", "Not a Potato", "Not a Potato",
     "puma-punku", "build/export",
     "Puma Punku — precision-cut andesite at altitude, the corner the official story can't quite account for. Coming soon."),
    ("sajama-lines", "The Long Straight", "Not a Potato", "Not a Potato",
     "sajama-lines", "build/export",
     "The Sajama Lines — thousands of straight furrows in the Bolivian altiplano, visible only from the air. Coming soon."),
    ("uffington", "The Scouring", "Not a Potato", "Not a Potato",
     "uffington", "build/export",
     "The Uffington White Horse — scoured into the chalk for three thousand years; the oldest hill figure in Britain. Coming soon."),
    ("yonaguni", "Made or Not", "Not a Potato", "Not a Potato",
     "yonaguni", "build/export",
     "The Yonaguni Monument — a submerged terrace off Japan; natural fracture or cut stone, and Jakobus's gift meets its limit. Coming soon."),

    # ── Children's Library (read-aloud picture books) ───────────────────────────────────────────
    ("the-little-key", "The Little Key", "Children's Library", "Children's Library",
     "the-little-key", "build/export",
     "A girl finds an old brass key and an old cupboard, and wakes a tiny carved honey badger who is alive as you are — and learns that you can wake a thing, but you can never own it. A gentle, honest read-aloud picture book about power held kindly, and about being big enough to matter to someone smaller than you. Ages 4–8. In every South African language and Swahili."),
    # Classic African Stories (pourquoi folktales), retold original in the house voice. Sold as
    # personalised print keepsakes — the child-hero's name + a dedication woven in ({{CHILD}}/{{DEDICATION}}).
    ("why-elephant-trunk", "How the Elephant Got His Long Nose", "Children's Library · Classic African Stories", "Children's Library",
     "why-elephant-trunk", "build/export",
     "Long ago the elephant had only a small stubby nose — until a crocodile clamped on at the river and everyone pulled, and pulled, and PULLED. A stretchy, funny, tender retelling of why the elephant's trunk is so long: the thing that felt like the worst day became the very gift that lets him help everyone. Ages 4–8."),
    ("how-zebra-got-stripes", "How the Zebra Got Her Stripes", "Children's Library · Classic African Stories", "Children's Library",
     "how-zebra-got-stripes", "build/export",
     "Once the zebra was one plain colour, and a little lonely for it — until the animals gave her a gift of light and shadow so she could belong to the herd and never be lost again. A gentle retelling of how the zebra got her stripes: what makes you different is exactly what keeps you safe. Ages 4–8."),
    ("how-fire-came", "How Fire Came to the People", "Children's Library · Classic African Stories", "Children's Library",
     "how-fire-came", "build/export",
     "In the cold time before people had fire, a small brave child and a clever helper went to carry a single ember home — and learned the hardest, kindest thing: carry it gently, and share it. A warm retelling of the gift of fire, and of ash, which keeps tomorrow's coal alive. Honours San and Khoi fire-lore with care. Ages 4–8."),
    ("bird-of-paradise-flower", "The Flower That Watches the Sky", "Children's Library · Classic African Stories", "Children's Library",
     "bird-of-paradise-flower", "build/export",
     "In Gogo's garden grows a strange, bright flower shaped exactly like a little bird with its head tipped back, looking up. This is the tender story of how the crane-flower came to be — a bird that can no longer fly, still lifting its face to the sky, and the sweet drops it weeps. The companion to 'King Lion and the Birds Who Stole the Sky'. Ages 4–8."),
    ("how-king-lion", "King Lion and the Birds Who Stole the Sky", "Children's Library · Classic African Stories", "Children's Library",
     "how-king-lion", "build/export",
     "Proud birds stole the farmers' maize until the frightened villagers turned on every creature — so King Lion passed his sorrowful judgement: the birds would never fly again, and their feet were planted in the ground, where they lift their faces to the sky forever and weep the nectar of looking up. An original tale of pride, fear, and just-but-sorrowful consequence — and where the bird-of-paradise flower came from. Ages 4–8 (the darker, braver edge of the shelf)."),

    # ── The Control Room (Resonance companion novella) ──────────────────────────────────────────────
    ("the-control-room", "The Control Room", "A Resonance Novella", "Standalones",
     "the-control-room", "build/export",
     "Seven operators run a rehabilitation unit — or so they have been told. The unit is a body, the body belongs to a comatose twelve-year-old boy, and the seven operators are extractions of his own childhood scan. A chamber novella set after Resonance: one reveal, one unanimous vote, a pronoun arc from we to I."),

    # ── The Firmament (original dystopian duology) ──────────────────────────────────────────────────
    ("the-firmament", "The Firmament", "The Firmament · Book One", "The Firmament",
     "the-firmament", "build/export",
     "DRAFT: For twelve generations they knew the truth: the world is a flat disc under a firmament, ringed by ice. They were right — about a world the size of a lifeboat. A sealed post-flare arcology, a redacted scripture passed hand to hand as samizdat, and the one who walks through the ice wall and onto the round Earth, where the forbidden verses come true one by one. Complete manuscript, not yet copy-edited."),

    # ── Verdigris (original eco-horror) ─────────────────────────────────────────────────────────────
    ("verdigris", "Verdigris", "A standalone novel", "Standalones",
     "verdigris", "build/export",
     "As the warming Earth turns fungal and the spores learn to ride human beings, the last weapon that works is copper. The mycologist holding the sprayer comes to believe the bloom is not an invader — it is the planet's immune response, and the mushrooms rising in every ruin are trying to give something back before the copper kills the only thing that could."),

    # ── Those Who Came Down (committed-mythos Anunnaki, twelve tablets) ─────────────────────────────
    ("those-who-came-down", "Those Who Came Down", "The Anunnaki, as the dreamers tell it", "Standalones",
     "those-who-came-down", "build/export",
     "The founding myth of the ancient-astronaut shelf, told once, whole, and committed — close third on Enki, from first splashdown to the last tablet. A tired world crosses the sky every 3,600 years; its princes come down for the gold that keeps their air alive, and when the diggers refuse the dark, they make a worker out of clay and a dead god's blood — and get something no one ordered: a creature that sings in the mine, buries its dead in flowers, and writes. The shelf's other Anunnaki books kill this reading in the cuneiform; this one plays it dead straight, as the dreamers tell it."),

    # ── Faithful Modern additions ────────────────────────────────────────────────────────────────────
    ("the-long-silence", "The Long Silence", "Faithful Modern · after Liu Cixin", "Faithful Modern",
     "the-long-silence", "build/export",
     "A species clever enough to split the atom but foolish enough to broadcast its address learns, too late, the one law of a universe full of listeners: the wise stay silent, and the loud do not last. A faithful-modern homage to the Dark Forest engine — original cast, deep-time relay, three movements, the aliens withheld. Coming soon."),

    ("the-openwork", "Lacework", "Faithful Modern · after Shirley Conran", "Faithful Modern",
     "the-openwork", "build/export",
     "Thirty years after four schoolgirls swore a pact to hide a pregnancy and share a child, the daughter — now the most famous woman on the continent — walks into a Cape Town hotel suite with the DNA result already in her pocket. She knows who her mother is. What she wants to know is which of them decided. A faithful-modern retelling of the engine behind Lace: the maternity mystery retired, the anatomy of the pact opened."),

    ("the-sealed-finding", "The Sealed Finding", "Faithful Modern · after Philip K. Dick", "Faithful Modern",
     "the-sealed-finding", "build/export",
     "The man who built a state that arrests people for murders they have not yet committed is named by his own machine — and the report that would clear him is sealed in a drawer, alongside the proof that both reports are true. Near-now South Africa, 2054: precognition replaced by inference, the named given Tuesdays, both truths always. A faithful-modern retelling after Philip K. Dick's The Minority Report."),

    # ── The Piet Buys Files (SA literary crime series) ───────────────────────────────────────────────
    ("the-unnumbered", "The Unnumbered", "The Piet Buys Files · Book One", "The Piet Buys Files",
     "the-unnumbered", "build/export",
     "A late-diagnosed autistic profiler, pushed out of the police unit that no longer exists, sells threat assessments to frightened wine farmers — so he can afford to hunt the man harvesting women off the seasonal-labour routes between Stellenbosch and the Namibian border. Women no one has reported missing, because they were already away for work. South African literary crime. Open draft — Movements One and Two."),
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

        def make_link(label_raw: str, raw_href: str) -> str:
            label = fmt_label(html.escape(label_raw))
            raw_href = raw_href.strip()
            parsed = urllib.parse.urlparse(raw_href)
            # Source manuscripts sometimes contain repo-only Markdown cross-references or
            # machine-local file paths. Do not publish those as broken/leaky public links.
            if raw_href.startswith(("/Users/", "file:")):
                return label
            if not parsed.scheme and raw_href.split("#", 1)[0].lower().endswith(".md"):
                return label
            href = html.escape(raw_href, quote=True)
            # External (off-site) links open in a new tab and disown the opener.
            if parsed.scheme in ("http", "https"):
                return f'<a href="{href}" target="_blank" rel="noopener noreferrer external">{label}</a>'
            return f'<a href="{href}">{label}</a>'

        # Stash links BEFORE html.escape so [text](<url>) and URLs with '(' stay intact.
        # A naive [^)]+ pattern truncates Wikimedia File:Foo_(bar).jpg at the first ')'.
        _anchors: list[str] = []

        def _stash_link(label: str, href: str) -> str:
            _anchors.append(make_link(label, href))
            return f"\x00A{len(_anchors) - 1}\x00"

        def _replace_md_links(text: str) -> str:
            out: list[str] = []
            i = 0
            n = len(text)
            while i < n:
                start = text.find("[", i)
                if start < 0:
                    out.append(text[i:])
                    break
                out.append(text[i:start])
                mid = text.find("](", start)
                if mid < 0:
                    out.append(text[start])
                    i = start + 1
                    continue
                label = text[start + 1 : mid]
                j = mid + 2
                if j < n and text[j] == "<":
                    end = text.find(">)", j + 1)
                    if end < 0:
                        out.append(text[start])
                        i = start + 1
                        continue
                    href = text[j + 1 : end]
                    out.append(_stash_link(label, href))
                    i = end + 2
                    continue
                depth = 1
                k = j
                while k < n and depth:
                    ch = text[k]
                    if ch == "(":
                        depth += 1
                    elif ch == ")":
                        depth -= 1
                    k += 1
                if depth != 0:
                    out.append(text[start])
                    i = start + 1
                    continue
                href = text[j : k - 1]
                out.append(_stash_link(label, href))
                i = k
            return "".join(out)

        t = _replace_md_links(t)
        t = html.escape(t)
        # SHIELD finished <a> tags (placeholders) from emphasis/code passes — otherwise an
        # underscore inside a URL path in surrounding text is fine, but we still restore
        # pre-built anchors after bold/italic/code transforms.
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
        # Image lines: ![alt](url) or ![alt](<url>), with balanced parens in url.
        imgm = re.match(r"^!\[([^\]]*)\]\(<([^>]+)>\)(?:\{[^}]*\})?$", s)
        if not imgm:
            imgm2 = re.match(r"^!\[([^\]]*)\]\((.+)\)$", s)
            if imgm2 and not s.endswith("}"):
                # Prefer a match only when trailing brace-options are absent; balanced below.
                alt_try, src_try = imgm2.group(1), imgm2.group(2)
                # If src_try has unbalanced '(', reject (malformed).
                if src_try.count("(") == src_try.count(")"):
                    class _Img:
                        def group(self, n: int) -> str:
                            return alt_try if n == 1 else src_try
                    imgm = _Img()  # type: ignore[assignment]
            elif imgm2:
                # ![alt](url){attrs} — peel trailing {…}
                brace = s.rfind("){")
                if brace > 0:
                    head = s[: brace + 1]
                    imgm2b = re.match(r"^!\[([^\]]*)\]\((.+)\)$", head)
                    if imgm2b and imgm2b.group(2).count("(") == imgm2b.group(2).count(")"):
                        class _ImgB:
                            def group(self, n: int) -> str:
                                return imgm2b.group(1) if n == 1 else imgm2b.group(2)
                        imgm = _ImgB()  # type: ignore[assignment]
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


def scan_audiobook(cid: str) -> dict | None:
    """Collect a book's audiobook: download-format files (from its publish/ dir, keyed by the
    AUDIO_FORMATS ladder) plus the per-chapter MP3 masters for the inline web player. Returns
    None unless the book is registered in AUDIOBOOKS and at least one download format exists.

    Format files are matched by extension within publish/ (the pipeline names them after the book
    title); the chapter player reads the numerically-sorted masters dir. The dict carries the source
    Paths (copied into downloads/<id>/ at write time) and the relative hrefs the page will use."""
    reg = AUDIOBOOKS.get(cid)
    if not reg:
        return None
    publish = reg["publish"]
    chapters_dir = reg["chapters"]
    if not publish.is_dir():
        return None
    by_ext: dict[str, Path] = {}
    for f in sorted(publish.iterdir()):
        if not f.is_file():
            continue
        ext = f.suffix.lower().lstrip(".")
        # the zip's "extension" is zip; everything else by suffix. First file of each ext wins.
        by_ext.setdefault(ext, f)
    # Ordered, labelled formats that actually exist on disk.
    formats = []
    for ext, label, sub in AUDIO_FORMATS:
        f = by_ext.get(ext)
        if f:
            formats.append({"ext": ext, "label": label, "sub": sub, "path": f})
    if not formats:
        return None
    chapters = sorted(chapters_dir.glob("*.mp3")) if chapters_dir.is_dir() else []
    return {
        "formats": formats,
        "chapters": chapters,         # source Paths; copied + linked for the player
        "narration": reg.get("narration", ""),
    }


def scan() -> list[dict]:
    entries = []
    hidden_proc: list[str] = []
    for cid, title, subtitle, series, rootrel, expsub, fb in CURATED:
        # Drop hidden titles/series entirely — no card, no book page, no read page, not in feed.
        if cid in HIDE_BOOKS or series in HIDE_SERIES:
            continue
        root = BOOKS / rootrel
        exp = root / expsub
        downloads = []          # primary (English) EPUB/PDF
        editions = {}           # lang code -> {"epub": Path, "pdf": Path} for translated editions
        if exp.is_dir():
            for f in sorted(exp.iterdir()):
                if f.suffix.lower() not in (".epub", ".pdf"):
                    continue
                # A translated edition's stem ends ".<code>" (e.g. "Resonance.af"); split it off.
                stem_suffix = f.stem.rsplit(".", 1)[-1].lower() if "." in f.stem else ""
                if stem_suffix in EDITION_LANGS:
                    # Translated editions surface even for SERIAL/open-draft books (they are the
                    # whole point of translating); the primary English DOWNLOAD stays gated to
                    # PUBLISHED so a serial/open draft still ships no English download.
                    editions.setdefault(stem_suffix, {})[f.suffix.lower().lstrip(".")] = f
                elif cid in PUBLISHED:
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
        # Children's Library: only titles with a git-tracked cover land on the shelf (real art,
        # not local placeholder PNGs that clear the size gate but are not committed for deploy).
        if cid in PICTURE_BOOKS and not cover_git_tracked(cover):
            hidden_proc.append(cid)
            continue
        book_md = root / "build" / "BOOK.md"
        reader_md = None
        reader_src = None
        picture_langs: list[str] = []
        can_read = cid in SERIAL or (cid in PUBLISHED and cid not in WORKSHOP_HOLD)
        if can_read:
            if cid in PICTURE_BOOKS:
                # Picture books read from build/chapters/PICTURE_BOOK.md (illustrated spreads),
                # never a merged prose BOOK.md.
                pb = root / "build" / "chapters" / "PICTURE_BOOK.md"
                if pb.is_file():
                    reader_md = pb.read_text(encoding="utf-8", errors="ignore")
                    picture_langs = [
                        c for c in picture_book_manuscripts(root, cid) if c != "en"
                    ]
            elif book_md.is_file():
                reader_src = book_md
            else:
                reader_md = companion_manuscript(root)
        # Audiobook: only for PUBLISHED books with an AUDIOBOOKS entry whose publish/ dir holds files.
        audiobook = scan_audiobook(cid)
        entries.append({
            "id": cid, "title": title, "subtitle": subtitle, "series": series,
            "blurb": blurb, "downloads": downloads, "cover": cover,
            "editions": editions,
            "book_md": reader_src,
            "reader_md": reader_md,
            "root": root,
            "serial": cid in SERIAL,
            # Picture books are always readable online once published (the art IS the book); their
            # EPUB/PDF ship as downloads when built, but the read-online page never waits on them.
            "available": can_read and (cid in SERIAL or cid in PICTURE_BOOKS or bool(downloads)),
            "isbn": book_isbn(root),
            "audiobook": audiobook if (cid in PUBLISHED and cid not in WORKSHOP_HOLD) else None,
            "picture_langs": picture_langs,
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
        # BOOK.md lives in build/, so its relative paths (e.g. ../design/plates/x.jpg)
        # resolve one level below the book root.
        candidates.append(book_root / "build" / src)
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


def prepare_picture_book_images(md: str, book_id: str, book_root: Path, assets_out: Path) -> str:
    """Copy a picture book's spread images and rewrite each marker's image= to a site-local path.

    Picture-book spreads carry the image in an HTML comment (image="…"), not markdown image
    syntax, so the normal prepare_reader_images() pass misses them. This resolves each spread
    image from the book's design/images (or build/chapters) and copies it into read/assets/<id>/,
    rewriting image="file.png" → image="assets/<id>/file.png" so render_picture_book() can wire it.
    """
    assets_out.mkdir(parents=True, exist_ok=True)

    def repl(m: re.Match[str]) -> str:
        whole, src = m.group(0), m.group(1)
        if src.startswith(("http://", "https://", "assets/")):
            return whole
        resolved = resolve_reader_image(src, book_root)
        if not resolved:
            return whole  # leave as-is; render shows a broken-image alt rather than vanishing
        dst = assets_out / resolved.name
        if not dst.exists() or resolved.stat().st_mtime > dst.stat().st_mtime:
            shutil.copy2(resolved, dst)
        return whole.replace(f'image="{src}"', f'image="assets/{book_id}/{resolved.name}"')

    return re.sub(r'<!--\s*spread:\d+\s+image="([^"]+)"', repl, md)


# ── render ───────────────────────────────────────────────────────────────────────
CSS = """
/* House face — self-hosted Atkinson Hyperlegible (cover + landing + all site prose). */
@font-face{font-family:"Atkinson Hyperlegible";font-style:normal;font-weight:400;font-display:swap;
  src:url("fonts/AtkinsonHyperlegible-Regular.otf") format("opentype")}
@font-face{font-family:"Atkinson Hyperlegible";font-style:normal;font-weight:700;font-display:swap;
  src:url("fonts/AtkinsonHyperlegible-Bold.otf") format("opentype")}
@font-face{font-family:"Atkinson Hyperlegible";font-style:italic;font-weight:400;font-display:swap;
  src:url("fonts/AtkinsonHyperlegible-Italic.otf") format("opentype")}
@font-face{font-family:"Atkinson Hyperlegible";font-style:italic;font-weight:700;font-display:swap;
  src:url("fonts/AtkinsonHyperlegible-BoldItalic.otf") format("opentype")}
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
  /* House face: Atkinson Hyperlegible for ALL site text including headings (a11y is the foundation). */
  font-family:var(--reading);line-height:1.65;
  background-image:radial-gradient(1200px 600px at 50% -10%,rgba(200,168,107,.10),transparent 60%);}
a{color:var(--ochre);text-decoration:none} a:hover{color:var(--gold)}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px}
h1,h2,h3{font-family:var(--reading);line-height:1.15;letter-spacing:-.01em}
.serif{font-family:var(--reading)}
.eyebrow{font-family:var(--reading);text-transform:uppercase;letter-spacing:.28em;
  font-size:12px;color:var(--ochre)}
.hr{height:1px;background:linear-gradient(90deg,transparent,var(--line),transparent);border:0;margin:0}

/* nav */
.nav{position:sticky;top:0;z-index:20;backdrop-filter:blur(10px);
  background:rgba(22,21,19,.78);border-bottom:1px solid var(--line)}
.nav .wrap{display:flex;align-items:center;gap:18px;height:66px}
.brandlink{display:flex;align-items:center;gap:12px;font-family:var(--reading);font-weight:600;
  letter-spacing:.02em;color:var(--bone)}
.brandlink img{height:40px;width:40px;border-radius:50%}
/* Drawer-only nav — do NOT reintroduce .navinline or a wide-screen top link bar. */
.nav nav.navinline{display:none!important}

/* ── Site-wide language bar (i18n edition selector) ─────────────────────────────────────────── */
.vh{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);
  white-space:nowrap;border:0}
.langbar{margin-left:auto;display:inline-flex;align-items:center;gap:7px;cursor:pointer}
.langbar-icon{font-size:15px;line-height:1;opacity:.85}
.langbar-sel{font-family:var(--reading);font-size:13px;color:var(--bone);
  background:var(--card);border:1px solid var(--line);border-radius:8px;padding:6px 28px 6px 10px;
  cursor:pointer;-webkit-appearance:none;appearance:none;max-width:46vw;text-overflow:ellipsis;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6' viewBox='0 0 10 6'%3E%3Cpath d='M1 1l4 4 4-4' stroke='%23C8A86B' stroke-width='1.5' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");
  background-repeat:no-repeat;background-position:right 10px center}
.langbar-sel:hover{border-color:var(--ochre)}
.langbar-sel:focus-visible{outline:2px solid var(--gold);outline-offset:2px}
/* When the lang bar sits next to the hamburger, the hamburger no longer needs the auto push. */
.langbar + .hamburger{margin-left:8px}
@media(max-width:480px){.langbar-sel{font-size:12px;padding:5px 24px 5px 8px;max-width:38vw}}

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
.navdrawer a{color:var(--bone);font-family:var(--reading);font-size:16px;padding:11px 14px;
  border-radius:8px;text-decoration:none}
.navdrawer a:hover{background:rgba(229,181,103,.1);color:var(--gold)}
.navdrawer a:focus-visible{background:rgba(229,181,103,.1);color:var(--gold)}
.navdrawer a.navhot{color:var(--sting)}
.navdrawer a.navhot:hover{color:#e0552e}
.navdrawer .navgroup{font-family:var(--reading);font-size:11px;letter-spacing:.18em;text-transform:uppercase;
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
.audiobook-notice strong{font-family:var(--reading);font-weight:600;color:var(--gold);white-space:nowrap}
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
.hero .tag{font-family:var(--reading);font-style:italic;font-size:clamp(20px,3vw,30px);color:var(--gold)}
.hero p.lead{max-width:680px;margin:18px auto 0;color:var(--bonedim);font-size:18px}
/* library header — compact + left-aligned (books-first, not a marketing hero).
   Small crest beside the text so the shelves start high on the page. */
.lib-head{padding:34px 0 18px;border-bottom:1px solid var(--line,rgba(229,181,103,.18))}
.lib-head .wrap{display:flex;gap:22px;align-items:center;flex-wrap:wrap}
.lib-head .lib-crest img{width:84px;height:84px;object-fit:contain;display:block;
  filter:drop-shadow(0 6px 24px rgba(229,181,103,.16))}
.lib-head-text{flex:1;min-width:260px}
.lib-head h1{font-size:clamp(30px,5vw,46px);margin:0 0 8px}
.lib-head p.lead{max-width:64ch;margin:0;color:var(--bonedim);font-size:17px;line-height:1.5}
.lib-head .cta{justify-content:flex-start;margin-top:18px}
@media(max-width:560px){.lib-head{padding:24px 0 14px}.lib-head .lib-crest img{width:60px;height:60px}}
.cta{display:inline-flex;gap:14px;margin-top:30px;flex-wrap:wrap;justify-content:center}
.btn{display:inline-block;padding:12px 22px;border-radius:8px;font-weight:600;font-size:15px;
  font-family:var(--reading);border:1px solid var(--ochre);color:var(--black);background:var(--ochre)}
.btn:hover{background:var(--gold);border-color:var(--gold);color:var(--black)}
.btn.ghost{background:transparent;color:var(--ochre)} .btn.ghost:hover{color:var(--gold);background:rgba(229,181,103,.08)}

/* mission */
.mission{padding:40px 0}
.pillars{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:8px}
.pillar{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:24px}
.pillar h2,.pillar h3{margin:.2em 0 .4em;font-size:18px} .pillar p{margin:0;color:var(--bonedim);font-size:15px}
.pillar .n{font-family:var(--reading);font-size:30px;color:var(--ochre)}

/* sections */
section.series{padding:46px 0 8px}
.sechead{margin-bottom:22px}
.sechead-row{display:flex;align-items:baseline;gap:16px}
.sechead h2{font-size:26px;margin:0}
.sechead .count{color:var(--grass);font-size:14px;font-family:var(--reading)}
.sechead .shelftag{margin:.35em 0 0;font-family:var(--reading);font-style:italic;
  font-size:17px;line-height:1.4;color:var(--accent,var(--ochre));opacity:.95;max-width:64ch}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:26px}

/* ── Audible-style horizontal scroll shelves (index only) ────────────────────────────── */
.shelf-track{display:flex;gap:14px;overflow-x:auto;padding:4px 0 18px;
  scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch}
.shelf-track::-webkit-scrollbar{height:4px}
.shelf-track::-webkit-scrollbar-track{background:transparent}
.shelf-track::-webkit-scrollbar-thumb{background:rgba(200,168,107,.3);border-radius:4px}
.shelf-track::-webkit-scrollbar-thumb:hover{background:var(--ochre)}
.scard{flex:0 0 158px;scroll-snap-align:start;border-radius:10px;overflow:hidden;
  background:var(--card);border:1px solid var(--line);text-decoration:none;display:block;
  transition:transform .18s ease,border-color .18s ease,box-shadow .18s}
.scard:hover{transform:translateY(-4px);border-color:var(--accent,var(--ochre));
  box-shadow:0 12px 32px rgba(0,0,0,.55)}
.scard .cover{width:100%;aspect-ratio:400/620;display:block;object-fit:cover;border-bottom:1px solid var(--line)}
.scard-info{padding:8px 10px 10px}
.scard-series{font-family:var(--reading);font-size:10px;letter-spacing:.15em;text-transform:uppercase;
  color:var(--accent,var(--ochre));display:block;margin-bottom:3px;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.scard-title{font-family:var(--reading);font-weight:600;font-size:14px;
  color:var(--bone);line-height:1.3;display:-webkit-box;
  -webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.scard-badge{display:block;font-family:var(--reading);font-size:10px;color:var(--grass);margin-top:5px}
.scard-badge.soon{color:rgba(200,168,107,.65)}
/* ── Cinematic hero with cover-mosaic backdrop ───────────────────────────────────────── */
.lib-hero{position:relative;padding:44px 0 32px;overflow:hidden;border-bottom:1px solid var(--line)}
.lib-hero-bg{position:absolute;inset:0;display:flex;pointer-events:none;
  filter:brightness(.13) saturate(.5) blur(3px);transform:scale(1.06)}
.lib-hero-bg img{flex:1;object-fit:cover;min-width:0;height:100%}
.lib-hero .wrap{position:relative;z-index:1;display:flex;gap:22px;align-items:center;flex-wrap:wrap}
.lib-hero-crest img{width:76px;height:76px;object-fit:contain;
  filter:drop-shadow(0 4px 20px rgba(229,181,103,.24))}
.lib-hero-text{flex:1;min-width:240px}
.lib-hero-text h1{font-size:clamp(28px,5vw,44px);margin:0 0 6px}
.lib-hero-text .lead{color:var(--bonedim);font-size:16px;line-height:1.5;margin:0 0 16px;max-width:56ch}
.lib-hero-text .cta{margin-top:0;justify-content:flex-start}
@media(max-width:540px){.lib-hero{padding:28px 0 20px}.lib-hero-crest img{width:52px;height:52px}}
section.series{padding:32px 0 4px}

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
.card .ser{font-family:var(--reading);font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--accent,var(--ochre))}
.card h3{margin:.2em 0 0;font-size:19px;font-family:var(--reading);font-weight:600}
.card p.tagline{flex:0;margin:.1em 0 0;font-family:var(--reading);font-style:italic;
  font-size:14.5px;color:var(--accent,var(--ochre));opacity:.92}
.card p{margin:0;color:var(--bonedim);font-size:14px;flex:1}
.badge{align-self:flex-start;font-size:11px;font-family:var(--reading);letter-spacing:.08em;
  padding:3px 9px;border-radius:99px;border:1px solid var(--line);color:var(--grass)}
.badge.soon{color:var(--ochre);border-color:rgba(200,168,107,.4)}
.card-disclosure{margin:.55em 0 0;font-size:.82em;line-height:1.45;color:var(--sting)}
.dls{display:flex;gap:10px;flex-wrap:wrap;margin-top:4px}
.dl{font-family:var(--reading);font-size:12.5px;font-weight:600;padding:6px 12px;border-radius:7px;
  border:1px solid var(--ochre);color:var(--ochre)} .dl:hover{background:rgba(229,181,103,.1);color:var(--gold)}
.dl.solid{background:var(--ochre);color:var(--black)} .dl.solid:hover{background:var(--gold);color:var(--black)}

/* "which book first?" recommender */
.start{max-width:760px}
.qblock{border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin:22px 0;background:var(--card)}
.qblock legend{font-family:var(--reading);font-weight:600;color:var(--gold);font-size:15px;padding:0 8px}
.qopts{display:flex;flex-wrap:wrap;gap:10px;margin-top:8px}
.qopt{font-family:var(--reading);font-size:14.5px;text-align:left;cursor:pointer;
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
.tile .tilecap{position:absolute;left:0;right:0;bottom:0;padding:18px 10px 9px;font-family:var(--reading);
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
.reccard .ser{font-family:var(--reading);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent,var(--ochre))}
.reccard h3{margin:.2em 0 .3em;font-size:21px} .reccard.lead h3{font-size:26px}
.reccard h3 a{color:var(--bone)} .reccard h3 a:hover{color:var(--gold)}
.reccard .blurb{color:var(--bonedim);font-size:15px;line-height:1.55;margin:.3em 0}
.recrunners{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:640px){.recrunners{grid-template-columns:1fr}.reccard,.reccard.lead{grid-template-columns:90px 1fr;gap:14px}}

/* book page */
.bookhero{display:grid;grid-template-columns:300px 1fr;gap:42px;padding:48px 0}
.bookhero .cover{aspect-ratio:400/620;border-radius:12px;box-shadow:0 18px 50px rgba(0,0,0,.5)}
.bookhero h1{font-family:var(--reading);font-size:46px;margin:.1em 0 .1em}
.bookhero .sub{color:var(--ochre);font-family:var(--reading);letter-spacing:.12em;text-transform:uppercase;font-size:13px}
.bookhero .tagline{margin:.2em 0 0;font-family:var(--reading);font-style:italic;font-size:20px;color:var(--ochre)}
.bookhero .syn{font-size:18px;color:var(--bone);margin-top:18px;max-width:60ch}
.back{font-family:var(--reading);font-size:13px;color:var(--bonedim)}

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
/* ── Picture book — landscape spreads, verse overlaid on quieter image areas ───────────────────
   Each spread is a full-bleed 3:2 landscape page; read-aloud text sits ON the art (not beneath
   it) in a corner chosen per spread so it lands in the less busy area. A soft scrim keeps the
   words legible. Scroll-snap gives a page-turn rhythm on wide screens. */
body.pb-reader{background:#080706}
body.pb-reader main#main{padding:0;max-width:none}
.picture-book{max-width:none;width:100%;margin:0;padding:0 0 56px;font-family:var(--reading)}
.picture-head{text-align:center;padding:20px 20px 12px;max-width:720px;margin:0 auto}
.picture-head h1{font-family:var(--reading);font-size:clamp(32px,5vw,44px);font-weight:700;margin:.1em 0}
.picture-byline{color:var(--ochre);font-style:italic;font-size:18px;margin:.2em 0 0;
  font-family:var(--reading)}
.pb-lang-note{margin:0;font-size:13px;color:var(--grass);font-family:var(--reading)}
.pb-lang-note.is-fallback{color:var(--bonedim)}
.pb-readbar-inner{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.picture-spreads{display:flex;flex-direction:column;gap:clamp(10px,2vw,22px);padding:8px 0 0}
.spread.landscape{position:relative;margin:0 auto;width:min(100%,1180px);
  aspect-ratio:3/2;overflow:hidden;background:var(--card);
  box-shadow:0 18px 50px rgba(0,0,0,.45);scroll-snap-align:center}
.picture-spreads.snap{scroll-snap-type:y proximity}
.spread.landscape img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.spread.landscape.scrim-bottom::before,.spread.landscape.scrim-top::before,.spread.landscape.scrim-full::before{
  content:"";position:absolute;inset:0;z-index:1;pointer-events:none}
.spread.landscape.scrim-bottom::before{
  background:linear-gradient(to top,rgba(6,5,4,.78) 0%,rgba(6,5,4,.28) 42%,transparent 68%)}
.spread.landscape.scrim-top::before{
  background:linear-gradient(to bottom,rgba(6,5,4,.78) 0%,rgba(6,5,4,.28) 42%,transparent 68%)}
.spread.landscape.scrim-full::before{background:linear-gradient(180deg,rgba(6,5,4,.35),rgba(6,5,4,.35))}
.spread-overlay{position:absolute;z-index:2;margin:0;padding:0;border:0;
  color:#fff;text-shadow:0 1px 2px rgba(0,0,0,.9),0 2px 16px rgba(0,0,0,.55);
  font-size:clamp(16px,2.35vw,25px);line-height:1.48;font-weight:600;text-wrap:balance;
  pointer-events:none}
.spread-overlay.pos-bl{bottom:7%;left:5%;max-width:46%;text-align:left}
.spread-overlay.pos-br{bottom:7%;right:5%;max-width:46%;text-align:right}
.spread-overlay.pos-tl{top:7%;left:5%;max-width:46%;text-align:left}
.spread-overlay.pos-tr{top:7%;right:5%;max-width:46%;text-align:right}
.spread-overlay.pos-bc{bottom:6%;left:50%;transform:translateX(-50%);max-width:62%;text-align:center}
.spread-overlay.pos-cc{top:50%;left:50%;transform:translate(-50%,-50%);max-width:54%;text-align:center}
.spread-overlay .refrain{display:block;margin:.45em 0 0;color:#f0d9a8;font-style:italic;
  font-family:var(--reading);font-size:1.08em;line-height:1.4;font-weight:600}
.spread-overlay .spread-gap{display:block;height:.45em}
.picture-book .spread.landscape:last-of-type{margin-bottom:8px}
@media(min-width:900px){
  body.pb-reader .picture-spreads{padding:12px 16px 0}
  .spread.landscape{border-radius:4px}
}
@media(max-width:640px){
  .picture-head h1{font-size:30px}
  .spread-overlay{font-size:15px;line-height:1.42}
  .spread-overlay.pos-bl,.spread-overlay.pos-br,.spread-overlay.pos-tl,.spread-overlay.pos-tr,
  .spread-overlay.pos-bc,.spread-overlay.pos-cc{max-width:88%;left:6%;right:6%;transform:none;text-align:left}
  .spread-overlay.pos-br,.spread-overlay.pos-tr{text-align:right;left:auto}
  .spread-overlay.pos-bc,.spread-overlay.pos-cc{left:6%;right:6%;text-align:center}
}
/* ── Code fences + Mermaid diagrams ────────────────────────────────────────────────────────── */
pre code{display:block;padding:16px 18px;background:#161513;border:1px solid var(--line);
  border-radius:10px;overflow-x:auto;font-family:ui-monospace,"SF Mono",Menlo,monospace;
  font-size:13.5px;line-height:1.5;color:var(--bonedim)}
.reader code{overflow-wrap:anywhere;word-break:break-word}
/* ── Mermaid diagrams — break OUT of the reading column to full viewport width ──────────────────
   A doc page's prose sits in a ~720-760px measure; an architecture diagram squeezed into that
   renders tiny. These rules full-bleed the diagram to (almost) the whole viewport so it renders
   big and legible, then a click toggles a fuller zoom. The breakout is the standard
   margin-left:50% + translateX(-50%) trick with a viewport-relative width. */
pre.mermaid{
  position:relative;left:50%;transform:translateX(-50%);
  width:96vw;max-width:1500px;            /* big on wide screens, never absurd on ultrawide */
  margin:2.2em 0;padding:22px;text-align:center;background:transparent;border:0;
  /* hidden until mermaid.js swaps the source for an <svg>; avoids a flash of raw graph text */
  color:transparent;min-height:40px;line-height:0;cursor:zoom-in}
/* render each diagram at its NATURAL size, capped to the container width and a readable
   max height — never stretch a small/narrow graph to fill the box (that was making tall
   diagrams render grotesquely large). The container centres them; zoom for detail. */
pre.mermaid svg{width:auto;height:auto;max-width:100%;max-height:640px;line-height:normal}
pre.mermaid[data-processed]{color:inherit}
/* click-to-zoom: a processed diagram with .zoomed fills the screen and scrolls if needed */
pre.mermaid.zoomed{position:fixed;inset:0;left:0;transform:none;width:100vw;max-width:none;
  height:100vh;margin:0;padding:32px;background:rgba(8,8,12,.94);z-index:9999;cursor:zoom-out;
  overflow:auto;display:flex;align-items:center;justify-content:center}
pre.mermaid.zoomed svg{width:auto;max-width:98vw;max-height:94vh}
@media(max-width:760px){pre.mermaid{width:100vw}}
/* ── Online-reader chapter list / TOC (left rail on wide screens) ───────────────────────────── */
.readlayout{display:grid;grid-template-columns:266px minmax(0,1fr);gap:8px;
  max-width:1040px;margin:0 auto;align-items:start}
.readlayout .reader{max-width:720px;margin:0}           /* article keeps its measure; grid centres it */
.readtoc{position:sticky;top:64px;align-self:start;max-height:calc(100vh - 84px);
  overflow-y:auto;padding:34px 8px 40px 24px;font-family:var(--reading);
  scrollbar-width:thin;scrollbar-color:var(--line) transparent}
.readtoc::-webkit-scrollbar{width:8px} .readtoc::-webkit-scrollbar-thumb{background:var(--line);border-radius:4px}
.readtoc-h{margin:0 0 12px;font-size:11px;letter-spacing:.26em;text-transform:uppercase;color:var(--ochre);
  font-family:var(--reading);font-weight:600}
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
.reader.poem{max-width:40rem}
.reader.poem .poem-title{font-family:var(--reading);font-weight:600;font-size:34px;
  text-align:center;letter-spacing:0;margin:0 0 .15em;color:var(--bone)}
.reader.poem .poem-sub{text-align:center;font-style:italic;color:var(--ochre);margin:0 0 2.6em;font-size:18px}
.reader.poem .stanza{font-family:var(--reading);font-size:21px;line-height:1.55;
  color:var(--bone);margin:0 0 2.1em;text-align:left}
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
.house h1{font-family:var(--reading);font-size:clamp(34px,6vw,58px);margin:28px 0 .06em}
.house .motto{font-family:var(--reading);font-style:italic;color:var(--gold);font-size:clamp(19px,3vw,28px)}
.house .gloss{color:var(--bonedim);font-family:var(--reading);letter-spacing:.08em;font-size:13px;margin-top:6px;text-transform:uppercase}
.blazon{text-align:left;max-width:680px;margin:30px auto 0;
  font-family:var(--reading);font-size:18px;line-height:1.65}
.blazon p.intro{color:var(--bone);font-size:19px;margin:0 0 1.2em}
.blazon h2{font-family:var(--reading);color:var(--gold);font-size:27px;text-align:center;margin:2em 0 .8em;font-weight:700}
.blazon .entry{margin:0 0 1.25em;padding-left:16px;border-left:2px solid var(--line)}
.blazon .charge{font-family:var(--reading);font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--ochre);display:block;margin-bottom:3px}
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
.wiki-index th{color:var(--ochre);font-family:var(--reading);font-size:12px;letter-spacing:.12em;text-transform:uppercase}

/* footer */
footer{border-top:1px solid var(--line);margin-top:60px;padding:40px 0;color:var(--grass);font-size:14px}
footer .wrap{display:flex;gap:18px;flex-wrap:wrap;align-items:center;justify-content:space-between}
footer .badgerline{font-family:var(--reading);font-style:italic;color:var(--bonedim)}
footer .builton{color:var(--bonedim);font-size:13px;letter-spacing:.02em}
footer .builton a{color:var(--bonedim);text-decoration:underline;text-underline-offset:2px}
footer .builton a:hover{color:var(--gold)}
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
.editions-h{font-family:var(--reading);font-size:13px;letter-spacing:.22em;text-transform:uppercase;color:var(--ochre);margin:0 0 4px}
.editions-note{font-size:13px;color:var(--grass);margin:0 0 12px;max-width:54ch}
.edlist{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px}
.edlist li{display:flex;align-items:center;justify-content:space-between;gap:14px;
  padding:8px 12px;background:var(--card);border:1px solid var(--line);border-radius:10px}
.edlang{color:var(--bone);font-size:14px}
.edlinks{display:inline-flex;gap:6px}
.dl-lang{font-family:var(--reading);font-size:12px;font-weight:500;padding:4px 12px;border-radius:8px;
  border:1px solid var(--ochre);color:var(--ochre)}
.dl-lang:hover{background:var(--ochre);color:var(--black)}
.editions-fix{margin:10px 0 0;font-size:13px;color:var(--grass)}
.editions-fix a{color:var(--ochre)}
/* Language-default note: appears (via JS) under the primary download buttons when the reader's
   chosen language has an edition here, or to explain an English fallback. */
.edition-active{margin:10px 0 0;font-size:13px;color:var(--ochre);display:flex;align-items:center;
  gap:8px;flex-wrap:wrap}
.edition-active.is-fallback{color:var(--grass)}
.edition-active a{color:var(--ochre);text-decoration:underline}
.fixlog{margin:18px 0 0}
.fixlog table{width:100%;border-collapse:collapse;font-size:14px;margin-top:10px}
.fixlog th,.fixlog td{padding:10px 12px;border:1px solid var(--line);text-align:left;vertical-align:top}
.fixlog th{background:rgba(200,168,107,.12);color:var(--gold);font-weight:700}
.fixlog td{color:var(--bone)}
.fixlog-empty{font-size:14px;color:var(--grass);font-style:italic;margin:8px 0 0}
.fixtops{display:flex;flex-wrap:wrap;gap:12px;margin-top:10px}
.fixtop{flex:1 1 200px;padding:12px 14px;background:var(--card);border:1px solid var(--line);border-radius:10px}
.fixtop h3{font-family:var(--reading);font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:var(--ochre);margin:0 0 8px}
.fixtop li{font-size:14px;color:var(--bone);margin:4px 0}
.bookrespond{margin-top:22px;padding-top:18px;border-top:1px solid var(--line)}
.feedback-link,.endnote-feedback a{font-size:13.5px;color:var(--ochre)}
.feedback-link{display:inline-block;margin-top:2px}
/* ── reader end-note (after the last page) ──────────────────────────────────────── */
.readerend{max-width:720px;margin:48px auto 0;text-align:center}
.readerend .rule{margin:0 0 22px}
.readerend .rate{justify-content:center}
.endnote-line{font-family:var(--reading);font-style:italic;font-size:19px;color:var(--bonedim);margin:0 0 8px}
.endnote-feedback{margin:10px 0 0} .endnote-support{margin:14px 0 0;font-size:14px;color:var(--grass)}
.endnote-support a{color:var(--ochre)}
/* ── support page (pure patronage) ──────────────────────────────────────────────── */
article.support{text-align:center}
.support-rails{display:flex;gap:16px;justify-content:center;flex-wrap:wrap;margin:34px 0 8px}
.support-rail{display:flex;flex-direction:column;gap:3px;min-width:180px;padding:18px 24px;
  background:var(--card);border:1px solid var(--line);border-radius:12px;color:var(--bone)}
a.support-rail:hover{border-color:var(--ochre)}
.support-rail .rail-name{font-family:var(--reading);font-weight:600;font-size:16px;color:var(--gold)}
.support-rail .rail-sub{font-size:12.5px;color:var(--grass)}
.support-foot{max-width:54ch;margin:20px auto 0;font-size:13.5px;color:var(--grass)}
/* ── Arjuna Audio narrator intake ──────────────────────────────────────────────── */
.narrator-page{max-width:820px}
.intake-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin:30px 0 34px}
.intake-card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:17px 18px}
.intake-card strong{display:block;font-family:var(--reading);font-size:19px;line-height:1.25;color:var(--gold);margin:4px 0 7px}
.intake-card p{margin:0;color:var(--bonedim);font-size:14px;line-height:1.45}
.intake-form{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:34px 0 0;padding:22px;
  background:var(--card);border:1px solid var(--line);border-radius:12px}
.intake-form label{display:flex;flex-direction:column;gap:6px;font-family:var(--reading);font-size:12px;
  letter-spacing:.1em;text-transform:uppercase;color:var(--ochre)}
.intake-form input,.intake-form select,.intake-form textarea{width:100%;border:1px solid var(--line);
  border-radius:8px;background:#161513;color:var(--bone);padding:11px 12px;font:15px Inter,system-ui,sans-serif;
  line-height:1.35}
.intake-form input:focus,.intake-form select:focus,.intake-form textarea:focus{outline:0;border-color:var(--gold);
  box-shadow:0 0 0 3px rgba(229,181,103,.11)}
.intake-form textarea,.intake-form .intake-note,.intake-form button{grid-column:1/-1}
.intake-note{margin:0;color:var(--grass);font-size:13.5px;line-height:1.45}
/* call to arms */
.callarms{padding:30px 0}
.callarms-inner{background:linear-gradient(135deg,rgba(194,64,30,.10),rgba(229,181,103,.07));border:1px solid var(--line);border-left:3px solid var(--sting,#c2401e);border-radius:14px;padding:30px 32px;max-width:880px;margin:0 auto;text-align:center}
.callarms-inner h2{font-size:clamp(24px,3.4vw,34px);margin:.25em 0 .35em}
.callarms-inner p{max-width:64ch;margin:0 auto 18px;color:var(--bone);font-size:17px;line-height:1.6}
.callarms-inner .cta{margin-top:6px}
.join-table{width:100%;border-collapse:collapse;margin:18px 0 6px;font-size:15px}
.join-table th{text-align:left;font-family:var(--reading);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--ochre);border-bottom:1px solid var(--line);padding:8px 10px}
.join-table td{vertical-align:top;padding:11px 10px;border-bottom:1px solid var(--line);color:var(--bone);line-height:1.45}
.join-table .dim{color:var(--bonedim);font-size:13px}
@media(max-width:560px){.join-table,.join-table tbody,.join-table tr,.join-table td,.join-table th{display:block;width:100%}.join-table th{display:none}.join-table td{border-bottom:none;padding:4px 0}.join-table tr{border-bottom:1px solid var(--line);padding:10px 0}}
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
.library-item strong{display:block;font-family:var(--reading);font-size:14px;line-height:1.25}
.library-item span{display:block;color:var(--grass);font-size:12.5px;margin-top:2px}
.reader-empty{padding:42px 28px;text-align:center;color:var(--bonedim)}
.reader-content{max-width:760px;margin:0 auto;padding:34px 28px 60px;font-family:var(--reading);font-size:18px;line-height:1.7}
.reader-content h2{font-family:var(--reading);font-size:28px;color:var(--gold);margin:0 0 18px}
.reader-content pre{white-space:pre-wrap;font:inherit;margin:0;color:var(--bone)}
/* ── Register picker + inline correction ("read it in your register") ─────────────────────────── */
.regpicker{display:flex;align-items:center;gap:8px;flex-wrap:wrap;font-size:14px}
.regpicker label{color:var(--gold);font-weight:600}
.regpicker select{background:var(--card,#1d1a16);color:var(--bone);border:1px solid var(--line);
  border-radius:8px;padding:6px 10px;font:inherit;font-size:14px;cursor:pointer}
.regpicker .reghint{color:var(--bonedim);font-size:12px}
.readlayout-wide{max-width:760px;margin:0 auto;padding:0 24px}
.regwin[hidden]{display:none}
.regwin ::selection{background:rgba(200,168,107,.35)}
.corrbox{position:fixed;left:0;right:0;bottom:0;z-index:9998;display:flex;justify-content:center;padding:0 14px 14px}
.corrbox[hidden]{display:none}
.corrcard{background:var(--card,#1d1a16);border:1px solid var(--gold);border-radius:14px;
  padding:16px 18px;max-width:560px;width:100%;box-shadow:0 8px 40px rgba(0,0,0,.5)}
.corrh{margin:0 0 8px;color:var(--gold);font-weight:600;font-size:15px}
.corrh span{color:var(--bonedim);font-weight:400;font-size:12px}
.corrorig{margin:0 0 10px;color:var(--bonedim);font-style:italic;font-size:14px}
.corrcard textarea,.corrcard input{width:100%;background:var(--bg,#161310);color:var(--bone);
  border:1px solid var(--line);border-radius:8px;padding:9px 11px;font:inherit;font-size:15px}
.corrrow{display:flex;gap:8px;align-items:center;margin-top:8px}
.corrrow input{flex:1}
.corrmsg{margin:8px 0 0;color:var(--gold);font-size:13px;min-height:1.1em}
.media-frame{width:100%;min-height:68vh;border:0;background:#111}
.audio-player{width:100%;margin:16px 0}.reader-note{color:var(--grass);font-size:13.5px}
/* Writing Desk audio essays: cover + first-class player, without turning the essay into a book. */
.writing-media{display:grid;grid-template-columns:minmax(180px,260px) minmax(0,1fr);gap:24px;
  align-items:center;margin:24px 0 34px;padding:18px;border:1px solid var(--line);border-radius:12px;background:var(--card)}
.writing-cover{display:block;width:100%;height:auto;aspect-ratio:1;object-fit:cover;border-radius:8px}
.writing-player{width:100%;margin:10px 0 8px}
.writing-media .wm-meta{margin:0 0 4px;color:var(--gold);font-size:13px;font-weight:700;letter-spacing:.05em;text-transform:uppercase}
.writing-media .wm-note{margin:0 0 12px;color:var(--bonedim);font-size:13.5px;line-height:1.5}
@media(max-width:620px){.writing-media{grid-template-columns:1fr}.writing-cover{max-width:320px;margin:0 auto}}
/* ── Audiobook block (book page) ── */
.audiobook{margin-top:30px;padding:20px;border:1px solid var(--line);border-left:3px solid var(--gold);border-radius:12px;background:var(--card)}
.ab-h{margin:0 0 .3em;font-size:1.15em;color:var(--gold)}
.ab-narration{margin:0 0 14px;color:var(--bonedim);font-size:.9em}
.ab-player{margin:0 0 16px}
.ab-audio{width:100%;margin-bottom:12px}
.ab-playlist{list-style:none;margin:0;padding:0;max-height:340px;overflow-y:auto;border:1px solid var(--line);border-radius:9px}
.ab-playlist li{border-bottom:1px solid var(--line)}.ab-playlist li:last-child{border-bottom:none}
.ab-ch{width:100%;text-align:left;background:none;border:none;color:var(--bone);padding:10px 14px;cursor:pointer;font:inherit;font-size:.95em;display:flex;gap:10px;align-items:baseline}
.ab-ch:hover{background:#1b1a17}.ab-ch.ab-active{background:#221f18;color:var(--gold)}
.ab-ch-n{color:var(--bonedim);font-variant-numeric:tabular-nums;font-size:.85em}
.ab-dl-label{margin:14px 0 8px;color:var(--bonedim);font-size:.85em;text-transform:uppercase;letter-spacing:.06em}
.ab-downloads{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:10px}
.ab-dl{display:flex;flex-direction:column;gap:2px;text-align:left;padding:10px 14px}
.ab-fmt{font-weight:600}.ab-sub{font-size:.78em;color:var(--bonedim);text-decoration:none}
@media(max-width:820px){.reader-workbench{grid-template-columns:1fr}.library-panel,.reading-panel{min-height:auto}}
/* ── CV page ─────────────────────────────────────────────────────────────────── */
.cv-page{max-width:980px}
.cv-hero{text-align:center;margin-bottom:34px}
.cv-hero h1{font-size:clamp(34px,6vw,58px);margin:.15em 0 .1em}
.cv-title{font-family:var(--reading);font-style:italic;color:var(--gold);font-size:22px;margin:0}
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
.cv-meta{font-family:var(--reading);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--grass)}
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
  border-left:4px solid var(--safari-camel);font-family:var(--reading);letter-spacing:.04em}
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
.safari-badge{font-family:var(--reading);letter-spacing:.32em;text-transform:uppercase;
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
.safari-card h3{font-family:var(--reading);font-size:17px;margin:0 0 8px;color:var(--bone)}
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
.wcard h3{font-family:var(--reading);font-size:18px;margin:0 0 6px}
.wby{font-size:13px;color:var(--grass);margin:0 0 8px;font-family:var(--reading);letter-spacing:.04em}
.wbl{font-size:14px;color:var(--bonedim);margin:0;line-height:1.5}
.wread{display:inline-block;margin-top:12px;font-size:13px;color:var(--safari-camel);font-family:var(--reading)}
.misogi-page table{width:100%;border-collapse:collapse;margin:22px 0;font-size:14px;line-height:1.45}
.misogi-page th,.misogi-page td{border:1px solid var(--line);padding:10px 12px;text-align:left;vertical-align:top}
.misogi-page th{background:rgba(74,82,52,.12);color:var(--bone);font-family:var(--reading);font-size:13px}
.misogi-page td:nth-child(2){font-size:16px}
.misogi-page td{color:var(--bonedim)}
.misogi-page blockquote{border-left:4px solid var(--safari-camel);padding-left:18px;color:var(--bonedim);font-style:italic}
.misogi-legend{font-size:14px;color:var(--bonedim);margin:18px 0 8px;padding:12px 16px;background:rgba(74,82,52,.08);
  border-radius:8px;border:1px solid var(--line);border-left:4px solid var(--safari-camel)}
"""

# Self-hosted via @font-face in site.css (assets/fonts/). Google Fonts kept as a
# belt-and-braces fallback when the local OTFs fail to load (offline CI mirrors, etc.).
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400;1,700&display=swap" '
         'rel="stylesheet">')


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
         safari_page: str = "", lang: str = "en") -> str:
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
    return f"""<!doctype html><html lang="{html.escape(lang)}"><head>
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
        # The three products, first and unmistakable: Library (here) · Studio (the tool) · Safari (the author).
        f'<p class="navgroup">Arjuna Badger Press</p>'
        f'<a href="{rel}index.html#library">The Library — read free</a>'
        f'<a class="navhot" href="/studio">Studio — start writing</a>'
        f'<a href="{rel}safari/index.html">Safari — meet the man</a>'
        f'<p class="navgroup">Read</p>'
        f'<a href="{rel}index.html#library">Library</a>'
        f'<a class="navhot" href="{rel}join.html">Help write them true</a>'
        f'<a href="{rel}start.html">Where to start</a>'
        f'<a href="{rel}wiki/index.html">Places</a>'
        f'<a href="{rel}learn.html">Learn</a>'
        f'<p class="navgroup">Write &amp; publish</p>'
        f'<a class="navhot" href="/studio">Studio (the writers’ tool)</a>'
        f'<a href="{rel}craft/index.html">Craft library</a>'
        f'<a href="{rel}for-authors.html">Workshop</a>'
        f'<a href="{rel}authoring.html">Phone authoring</a>'
        f'<a href="{rel}narrators.html">Narrators</a>'
        f'<a href="{rel}audition.html">Narrator audition</a>'
        f'<a class="navhot" href="{rel}illustrator-audition.html">Illustrator audition</a>'
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


def nav_bar(rel: str = "") -> str:
    """Top nav + drawer only — for pages that open their own <main> (readers, etc.)."""
    links = nav_drawer_links(rel)
    return f"""<input type="checkbox" id="navtoggle" class="navtoggle" hidden>
<div class="nav"><div class="wrap">
<a class="brandlink" href="{rel}index.html"><img src="{rel}assets/brand/{CORNER_MARK}" alt="Arjuna Badger Press">Arjuna Badger Press</a>
{lang_bar(rel)}<label for="navtoggle" class="hamburger" aria-label="Open menu" aria-controls="navdrawer" aria-expanded="false"><span></span><span></span><span></span></label>
</div></div>
<label for="navtoggle" class="navscrim" aria-hidden="true"></label>
<nav class="navdrawer" id="navdrawer"><label for="navtoggle" class="navclose" aria-label="Close menu">&times;</label>{links}</nav>"""


def nav(rel: str = "") -> str:
    # Pure-CSS toggle (checkbox hack) — drawer-only at all breakpoints; no inline top nav.
    return nav_bar(rel) + f"{trust_banner(rel)}{audiobook_notice()}<main id=\"main\">"


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
        f'<a href="{sp}proof.html">For G</a>'
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
    return (f'<img class="letter-crest" src="{rel}assets/brand/{CORNER_MARK}" '
            f'alt="Arjuna Badger Press">')


def safari_nav(rel: str = "", *, audiobook: bool = True) -> str:
    """Safari-zone nav — same drawer contract as site nav, different link set and olive chrome."""
    hub = f"{rel}safari/index.html"
    links = safari_nav_drawer_links(rel)
    return f"""<input type="checkbox" id="navtoggle" class="navtoggle" hidden>
<div class="nav safari-nav"><div class="wrap">
<a class="brandlink" href="{hub}"><img src="{rel}assets/brand/{SAFARI_LOGO}" alt="Arjuna Badger Press"></a>
{lang_bar(rel)}<label for="navtoggle" class="hamburger" aria-label="Open menu" aria-controls="navdrawer" aria-expanded="false"><span></span><span></span><span></span></label>
</div></div>
<label for="navtoggle" class="navscrim" aria-hidden="true"></label>
<nav class="navdrawer" id="navdrawer"><label for="navtoggle" class="navclose" aria-label="Close menu">&times;</label>{links}</nav>
{trust_banner(rel)}{audiobook_notice() if audiobook else ""}<main id="main">"""


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


def lang_script() -> str:
    """Site-wide language preference + edition defaulting. Loaded once per page via footer().

    Behaviour:
      • Reads/writes localStorage.abp_lang (default "en"); syncs the nav <select.langbar-sel>.
      • On any book page (a .bookhero[data-editions]), when the chosen language has an edition,
        the primary Download buttons point at that edition and relabel ("Download Afrikaans EPUB");
        a quiet note announces it. Books without the chosen edition restore the English download
        and show a one-line fallback note. English selection restores everything to base.
      • Pure progressive enhancement — with JS off, every English download still works.
    No cookies, no network. Endonyms come from a server-rendered map so labels match the picker."""
    if not AVAILABLE_LANGS:
        return ""
    # code -> endonym (what the reader sees), for "en" + every available edition language.
    names = {"en": "English"}
    for code in AVAILABLE_LANGS:
        nm, endonym = EDITION_LANGS.get(code, (code.upper(), code.upper()))
        names[code] = endonym
    names_json = json.dumps(names, ensure_ascii=False)
    js = """
<script>
(function(){
  var KEY="abp_lang";
  var NAMES=__NAMES__;
  // Auto-pick from the browser's preferred languages, but ONLY when the reader has not chosen one
  // themselves. A saved choice always wins (someone on an Afrikaans browser who picked English stays
  // on English). We match navigator.languages (e.g. ["af-ZA","en"]) to the editions we actually have,
  // by primary subtag, in the browser's own priority order. No detection -> stays English.
  function detect(){
    try{
      var prefs=(navigator.languages&&navigator.languages.length)?navigator.languages:[navigator.language||""];
      for(var i=0;i<prefs.length;i++){
        var code=String(prefs[i]||"").toLowerCase().split("-")[0];
        if(code&&NAMES[code])return code;
      }
    }catch(e){}
    return "en";
  }
  function get(){
    try{
      var v=localStorage.getItem(KEY);
      if(v&&NAMES[v])return v;          // a remembered manual choice always wins
      return detect();                  // first visit / no choice -> the browser's language
    }catch(e){return "en";}
  }
  function set(v){try{localStorage.setItem(KEY,v);}catch(e){}}
  var lang=get();

  // Apply the chosen language to a book page's primary download buttons + note.
  function applyBook(code){
    var hero=document.querySelector(".bookhero[data-editions]");
    if(!hero)return;
    var map;
    try{map=JSON.parse(hero.getAttribute("data-editions"))||{};}catch(e){map={};}
    var eds=map[code]||null;                 // {epub:"file", pdf:"file"} or null
    var btns=hero.querySelectorAll(".dl-primary");
    var swapped=0, total=btns.length;
    btns.forEach(function(a){
      var fmt=a.getAttribute("data-fmt");
      var baseHref=a.getAttribute("data-base-href");
      var baseLabel=a.getAttribute("data-base-label");
      if(code!=="en"&&eds&&eds[fmt]){
        var dir=baseHref.slice(0,baseHref.lastIndexOf("/")+1);
        a.setAttribute("href",dir+eds[fmt]);
        a.textContent="Download "+NAMES[code]+" "+baseLabel;
        a.setAttribute("hreflang",code);
        swapped++;
      }else{
        a.setAttribute("href",baseHref);
        a.textContent="Download "+baseLabel;
        a.removeAttribute("hreflang");
      }
    });
    var note=hero.querySelector(".edition-active");
    if(note){
      if(code==="en"){
        note.hidden=true;note.textContent="";note.classList.remove("is-fallback");
      }else if(swapped>0){
        note.hidden=false;note.classList.remove("is-fallback");
        note.innerHTML="🌐 Showing the <strong>"+NAMES[code]+"</strong> edition.";
      }else{
        note.hidden=false;note.classList.add("is-fallback");
        note.textContent="No "+NAMES[code]+" edition of this book yet — showing English.";
      }
    }
  }

  function applyPictureBook(code){
    var article=document.querySelector(".picture-book[data-pb]");
    var dataEl=document.getElementById("pb-data");
    if(!article||!dataEl)return;
    var langs;
    try{langs=JSON.parse(dataEl.textContent);}catch(e){return;}
    var pack=langs[code]||langs.en;
    if(!pack)return;
    var fallback=code!=="en"&&!langs[code];
    var head=article.querySelector(".picture-head");
    if(head){
      var h1=head.querySelector("h1");
      if(h1&&pack.title)h1.textContent=pack.title;
      var by=head.querySelector(".picture-byline");
      if(pack.byline){
        if(by)by.textContent=pack.byline;
        else{
          by=document.createElement("p");
          by.className="picture-byline";
          by.textContent=pack.byline;
          h1.after(by);
        }
      }else if(by){by.remove();}
    }
    (pack.spreads||[]).forEach(function(s){
      var cap=article.querySelector('.spread-overlay[data-spread="'+s.n+'"]');
      if(cap&&s.html!=null)cap.innerHTML=s.html;
    });
    article.setAttribute("lang",code==="en"?"en-ZA":code);
    var note=document.querySelector(".pb-lang-note");
    if(note){
      if(code==="en"){note.hidden=true;note.textContent="";note.classList.remove("is-fallback");}
      else if(fallback){
        note.hidden=false;note.classList.add("is-fallback");
        note.textContent="No "+NAMES[code]+" edition yet — showing English.";
      }else{
        note.hidden=false;note.classList.remove("is-fallback");
        note.textContent="Reading in "+NAMES[code]+".";
      }
    }
  }

  function apply(code){lang=code;applyBook(code);applyPictureBook(code);}

  // Wire the nav selector(s) and reflect the stored choice on load.
  var sels=document.querySelectorAll(".langbar-sel");
  sels.forEach(function(sel){
    if(sel.querySelector('option[value="'+lang+'"]')) sel.value=lang;
    sel.addEventListener("change",function(){
      var v=sel.value; set(v); apply(v);
      sels.forEach(function(s){if(s!==sel)s.value=v;});
    });
  });
  apply(lang);
})();
</script>"""
    return js.replace("__NAMES__", names_json)


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
<span class="builton">Built on <a href="https://congosky.cloud" target="_blank" rel="noopener noreferrer external">congosky.cloud</a></span>
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
</script>{lang_script()}</body></html>"""


MERMAID_BOOT = """<script type="module">
  import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
  mermaid.initialize({
    startOnLoad: false,
    securityLevel: "strict",
    theme: "base",
    maxTextSize: 90000,                 // allow large architecture graphs without truncation
    flowchart: { useMaxWidth: false, htmlLabels: true, nodeSpacing: 50, rankSpacing: 60 },
    themeVariables: {
      background: "#1d1a16", primaryColor: "#221f1b", primaryTextColor: "#EDE9E0",
      primaryBorderColor: "#C8A86B", lineColor: "#C8A86B", secondaryColor: "#2A241D",
      tertiaryColor: "#161513", fontFamily: "Inter, system-ui, sans-serif",
    },
  });
  // Render, then wire click-to-zoom: a diagram fills the screen on click, restores on click/Esc.
  await mermaid.run({ querySelector: "pre.mermaid" });
  const diagrams = document.querySelectorAll("pre.mermaid");
  diagrams.forEach((d) => d.addEventListener("click", () => d.classList.toggle("zoomed")));
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") document.querySelectorAll("pre.mermaid.zoomed").forEach((d) => d.classList.remove("zoomed"));
  });
</script>"""


def with_mermaid(page: str) -> str:
    """If a finished page contains a Mermaid block, load+init mermaid.js just before </body>.
    Per-page (the script only ships where a diagram actually appears)."""
    if 'class="mermaid"' not in page:
        return page
    return page.replace("</body></html>", f"{MERMAID_BOOT}</body></html>", 1)


def card(e: dict, accent: str) -> str:
    # lazy-load covers — the library shows ~38 of them; eager loading every cover on
    # page open was the slowness (covers are 0.3–7MB each). loading="lazy" defers
    # off-screen covers until scroll; decoding="async" keeps the main thread free.
    # SHELF thumbnail (small WebP, ~400px) instead of the full-res cover: a shelf cover
    # only displays at ~200px wide, so the multi-MB PNG was pure waste. cover_thumb_src()
    # falls back to the full cover if no thumb was generated (PIL/source missing), so cards
    # never break. The book page + reader keep the full-res cover (see render_book). The
    # width/height match the CSS aspect-ratio (400/620) to reserve space and avoid layout shift.
    cover = (f'<img class="cover" loading="lazy" decoding="async" width="400" height="620" '
             f'src="{cover_thumb_src(e["id"], e.get("cover"))}" '
             f'alt="{html.escape(e["title"])} cover">')
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
        if e["id"] == "bloedrivier":
            badge = '<span class="badge">Open draft</span>'
            dls = f'<div class="dls"><a class="dl solid" href="read/{e["id"]}.html">Read the draft →</a></div>'
        else:
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
{BOOK_CARD_DISCLOSURE.get(e['id'], '')}
{badge}{dls}</div></div>"""


def shelf_card(e: dict, accent: str) -> str:
    """Compact Audible-style cover card for horizontal shelf rows on the landing page."""
    cover = (f'<img class="cover" loading="lazy" decoding="async" width="158" height="245" '
             f'src="{cover_thumb_src(e["id"], e.get("cover"))}" '
             f'alt="{html.escape(e["title"])} cover">')
    href = f"book/{e['id']}.html"
    if e.get("serial"):
        badge = '<span class="scard-badge">Serial</span>'
    elif e["available"]:
        badge = '<span class="scard-badge">Free</span>'
    else:
        soon_lbl = "Coming soon" if "_comingsoon" in e["root"].parts else "In progress"
        badge = f'<span class="scard-badge soon">{soon_lbl}</span>'
    series_label = html.escape(e.get("subtitle") or e.get("series") or "")
    return (
        f'<a class="scard" href="{href}" style="--accent:{accent}" '
        f'aria-label="{html.escape(e["title"])}">'
        f'{cover}'
        f'<div class="scard-info">'
        f'<span class="scard-series">{series_label}</span>'
        f'<span class="scard-title">{html.escape(e["title"])}</span>'
        f'{badge}'
        f'</div></a>'
    )


def render_library_shelves_audible(entries: list[dict], *, available_only: bool = False) -> str:
    """Horizontal Audible-style shelf rows for the landing page index."""
    parts: list[str] = []
    for sname, accent in SERIES:
        group = [e for e in entries if e["series"] == sname]
        if available_only:
            group = [e for e in group if e["available"] or e.get("serial")]
        if not group:
            continue
        group.sort(key=lambda e: 0 if e["available"] else 1)
        cards = "".join(shelf_card(e, accent) for e in group)
        tag = SHELF_TAGLINE.get(sname)
        tagline = f'<p class="shelftag">{html.escape(tag)}</p>' if tag else ""
        count = len(group)
        parts.append(
            f'<section class="series"><div class="wrap">'
            f'<div class="sechead" style="--accent:{accent}">'
            f'<div class="sechead-row">'
            f'<h2>{html.escape(sname)}</h2>'
            f'<span class="count">{count} {"book" if count == 1 else "books"}</span>'
            f'</div>{tagline}</div>'
            f'<div class="shelf-track">{cards}</div>'
            f'</div></section>'
        )
    return "\n".join(parts)


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
            ("A myth or classic, retold plainly", {"wrath-of-achilles": 5, "walls-of-uruk": 5, "the-song-of-the-self": 4, "henry-sugar": 4}),
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
            ("Homer · Madeline Miller (myth)", {"wrath-of-achilles": 6, "walls-of-uruk": 4, "the-song-of-the-self": 3}),
            ("Gilgamesh · the oldest epic", {"walls-of-uruk": 6, "wrath-of-achilles": 3, "anunnaki-mesopotamia": 2}),
            ("Robert A. Heinlein · Stranger in a Strange Land", {"the-first-unplugged": 6, "resonance": 2}),
            ("Hermann Hesse · Paulo Coelho (the inward journey)", {"the-song-of-the-self": 6, "the-loneliest": 2}),
        ],
    },
    "q3": {
        "prompt": "And the pace?",
        "options": [
            ("Propulsive — I want to turn pages", {"relic": 3, "revelation": 3, "resonance": 2, "book2-india": 2}),
            ("A slow burn I can sink into", {"the-loneliest": 3, "unheard-japan": 3, "jakobus-the-recitation": 2, "unheard-mongolia": 2}),
            ("Teach me something real", {"book1-africa": 3, "project-stargate": 3, "wrath-of-achilles": 2, "walls-of-uruk": 2, "sheltering-desert": 2}),
        ],
    },
}

# Tie-break / natural entry order — the front door of the library when scores are equal.
START_PRIORITY = [
    "resonance", "book1-africa", "relic", "revelation", "the-loneliest", "wrath-of-achilles",
    "walls-of-uruk",
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
    ("myth",    "The old stories, retold",        "wrath-of-achilles",    ["walls-of-uruk", "the-song-of-the-self"]),
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


def _stage_misread_audio(manifest_path, audio_out) -> int:
    """Copy the real MP3s into the player's /audio/<lane>/<slug>.mp3 tree, matching each
    manifest track to its file on disk by normalized title + A/B variant. Returns the count
    staged. Source = $MUSIC_DIR/downloads (defaults to ~/code/congosky-music/downloads). Silent
    no-op if the workspace isn't present so the page still builds in CI without the music repo."""
    import json as _json, re as _re, unicodedata as _ud, os as _os
    downloads = Path(_os.environ.get("MUSIC_DIR", Path.home() / "code" / "congosky-music")) / "downloads"
    if not downloads.is_dir():
        return 0

    def _norm(s):
        s = _ud.normalize("NFKD", s).encode("ascii", "ignore").decode()
        return _re.sub(r"[^a-z0-9]", "", s.lower())

    # Index real mp3s by (normalized base title, variant)
    real = {}
    for f in downloads.glob("*.mp3"):
        m = _re.match(r"^(.*?)\s*\(([AB])\)\s*$", f.stem)
        base, variant = (m.group(1), m.group(2).lower()) if m else (f.stem, "a")
        real[(_norm(base), variant)] = f

    manifest = _json.loads(manifest_path.read_text(encoding="utf-8"))
    staged = 0
    for lane in manifest.get("lanes", []):
        for t in (lane.get("tracks") or []):
            url = t.get("audioUrl", "")
            rel = url.replace("/audio/", "", 1)
            mv = _re.search(r"-([ab])\.mp3$", rel)
            variant = mv.group(1) if mv else "a"
            src = real.get((_norm(t.get("title", "")), variant))
            if not src:  # fall back to any variant of the same title
                src = next((rf for (rb, _rv), rf in real.items() if rb == _norm(t.get("title", ""))), None)
            if src:
                dest = audio_out / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                if not dest.exists():
                    shutil.copy2(src, dest)
                staged += 1
    return staged


def render_misread_player() -> str:
    """The Man They All Misread — the self-hosted companion player for AJ's
    Jakobus & Beast song catalogue.

    The badger thesis made real: AJ's own music on AJ's own rails — a plain
    HTML/CSS/JS player off a JSON manifest, no streaming silo, no gatekeeper.
    Lane/genre switcher + per-lane track list + an HTML5 <audio> transport
    (play/pause/prev/next/seek). Vanilla, ES5-safe, mobile-first; degrades on
    ancient devices (the whole project supports old phones).

    Audio is served from /audio/<lane>/<slug>.mp3 once the MP3s are uploaded to
    R2; until then the UI is fully live but no file streams (see
    music-manifest.json's _comment and build_music_manifest.py).
    """
    rel = "./"
    title = "The Man They All Misread — the companion player"
    desc = ("Jakobus & Beast, made not curated — AJ's own song catalogue on his "
            "own rails. Switch lanes (Brass'n'Bass, Banjos & Bass, the Still-Man "
            "bangers, Die Dier, Wolf, Rasta and more) and play. Self-hosted, no "
            "silo: the badger thesis made audible.")
    canonical = f"{DOMAIN}/the-man-they-all-misread.html"

    # ── Page-scoped styles. Reuses the house tokens (--gold/--ochre/--card/--line,
    #    Space Grotesk / Cormorant Garamond / Atkinson Hyperlegible) so it sits
    #    inside the press look without inventing a new one. All selectors are
    #    prefixed .mp- so nothing leaks into the global stylesheet.
    style = """
<style>
.mp-hero{padding:48px 0 8px}
.mp-hero .eyebrow{margin:0 0 10px}
.mp-hero h1{font-size:clamp(34px,6vw,60px);margin:0 0 .15em;
  font-family:var(--reading);font-weight:600;letter-spacing:-.01em}
.mp-hero .tag{font-family:var(--reading);font-style:italic;
  font-size:clamp(18px,2.6vw,26px);color:var(--gold);margin:.1em 0 .6em}
.mp-hero p.lede{max-width:62ch;color:var(--bonedim);margin:.2em 0 0}
.mp-hero p.lede a{color:var(--gold)}
.mp-note{margin:18px 0 0;padding:12px 16px;border:1px solid var(--line);border-radius:10px;
  background:rgba(200,168,107,.06);color:var(--bonedim);font-size:14px;max-width:70ch}
.mp-note strong{color:var(--gold);font-family:var(--reading)}

/* lane switcher — horizontal scroll on narrow screens, wraps on wide */
.mp-lanes{display:flex;flex-wrap:wrap;gap:8px;margin:26px 0 6px;
  padding-bottom:6px;overflow-x:auto;-webkit-overflow-scrolling:touch}
.mp-lane{flex:0 0 auto;cursor:pointer;border:1px solid var(--line);background:var(--card);
  color:var(--bone);font-family:var(--reading);font-size:14px;font-weight:500;
  letter-spacing:.01em;padding:9px 15px;border-radius:999px;line-height:1.2;white-space:nowrap;
  transition:border-color .15s,background .15s,color .15s}
.mp-lane:hover{border-color:var(--ochre);color:var(--gold)}
.mp-lane[aria-selected="true"]{background:var(--ochre);border-color:var(--ochre);color:var(--black)}
.mp-lane .n{opacity:.6;font-size:12px;margin-left:6px}

.mp-laneblurb{font-family:var(--reading);font-style:italic;font-size:18px;
  line-height:1.45;color:var(--ochre);max-width:66ch;margin:14px 0 2px}

/* track list */
.mp-list{list-style:none;margin:18px 0 0;padding:0;border-top:1px solid var(--line)}
.mp-track{display:flex;align-items:center;gap:14px;padding:13px 8px;border-bottom:1px solid var(--line);
  cursor:pointer}
.mp-track:hover{background:rgba(229,181,103,.05)}
.mp-track[aria-current="true"]{background:rgba(229,181,103,.10)}
.mp-track .ti{flex:0 0 auto;width:30px;text-align:right;color:var(--grass);
  font-family:var(--reading);font-size:13px;font-variant-numeric:tabular-nums}
.mp-track .play{flex:0 0 auto;width:30px;height:30px;border-radius:50%;border:1px solid var(--line);
  background:transparent;color:var(--ochre);font-size:13px;line-height:1;display:flex;
  align-items:center;justify-content:center;cursor:pointer}
.mp-track[aria-current="true"] .play{background:var(--ochre);border-color:var(--ochre);color:var(--black)}
.mp-track .tt{flex:1 1 auto;min-width:0}
.mp-track .tt b{display:block;font-weight:500;font-family:var(--reading);font-size:15px;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.mp-track .vs{flex:0 0 auto;display:flex;gap:5px}
.mp-track .vbtn{font-family:var(--reading);font-size:11px;letter-spacing:.06em;
  border:1px solid var(--line);background:transparent;color:var(--bonedim);border-radius:6px;
  padding:3px 8px;cursor:pointer}
.mp-track .vbtn[aria-pressed="true"]{border-color:var(--gold);color:var(--gold)}
.mp-track .nofile{flex:0 0 auto;font-size:11px;color:var(--sting);font-family:var(--reading);
  letter-spacing:.04em;opacity:.85}

/* sticky transport bar */
.mp-bar{position:sticky;bottom:0;z-index:15;margin-top:30px;background:rgba(22,21,19,.94);
  backdrop-filter:blur(10px);border:1px solid var(--line);border-radius:14px;padding:14px 16px;
  box-shadow:0 -2px 30px rgba(0,0,0,.4)}
.mp-now{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin:0 0 10px}
.mp-now .lbl{font-family:var(--reading);font-size:11px;letter-spacing:.22em;
  text-transform:uppercase;color:var(--grass)}
.mp-now .ttl{font-family:var(--reading);font-size:20px;color:var(--bone)}
.mp-now .lane{color:var(--ochre);font-size:13px;font-family:var(--reading)}
.mp-seekrow{display:flex;align-items:center;gap:10px}
.mp-time{font-family:var(--reading);font-size:12px;color:var(--grass);
  font-variant-numeric:tabular-nums;flex:0 0 auto;width:42px;text-align:center}
.mp-seek{flex:1 1 auto;-webkit-appearance:none;appearance:none;height:5px;border-radius:3px;
  background:var(--line);outline:none;cursor:pointer}
.mp-seek::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:14px;height:14px;
  border-radius:50%;background:var(--gold);cursor:pointer}
.mp-seek::-moz-range-thumb{width:14px;height:14px;border:0;border-radius:50%;background:var(--gold);cursor:pointer}
.mp-ctrls{display:flex;align-items:center;justify-content:center;gap:14px;margin-top:12px}
.mp-btn{border:1px solid var(--line);background:var(--card);color:var(--bone);cursor:pointer;
  border-radius:999px;font-family:var(--reading);font-size:15px;padding:10px 16px;
  min-width:46px;line-height:1}
.mp-btn:hover{border-color:var(--ochre);color:var(--gold)}
.mp-btn.primary{background:var(--ochre);border-color:var(--ochre);color:var(--black);
  font-size:18px;padding:11px 22px}
.mp-btn.primary:hover{background:var(--gold);border-color:var(--gold)}
.mp-err{color:var(--sting);font-size:13px;font-family:var(--reading);
  text-align:center;margin:10px 0 0;min-height:1em}
.mp-empty{color:var(--bonedim);padding:30px 0;text-align:center;font-style:italic}
@media (max-width:540px){
  .mp-track .vs{display:none}
  .mp-now .ttl{font-size:17px}
}
</style>"""

    # ── Page body. The JS fetches music-manifest.json and renders everything; the
    #    server-rendered fallback below keeps the page meaningful without JS and
    #    gives crawlers real content.
    body = """
<div class="wrap mp-hero">
  <p class="eyebrow">Arjuna Sound · companion player</p>
  <h1>The Man They All Misread</h1>
  <p class="tag">Jakobus &amp; Beast — made, not curated.</p>
  <p class="lede">The soundtrack to <a href="book/the-jakobus-file.html"><em>A Man They All
  Read Wrong</em></a> — and the whole catalogue around it. Pick a lane, press play. These are
  AJ's own songs, on AJ's own rails: self-hosted, no streaming silo, no gatekeeper's permission.
  <em>Lay your own table in the firelight; don't ask for a seat at theirs.</em></p>
  <p class="mp-note" id="mp-status" role="status">
    <strong>9 lanes · 65 songs.</strong> Self-hosted on our own rails — AJ's catalogue, served
    from here, no streaming silo. Press play.
  </p>
</div>

<div class="wrap" id="mp-app">
  <div class="mp-lanes" id="mp-lanes" role="tablist" aria-label="Genres / playlists"></div>
  <p class="mp-laneblurb" id="mp-laneblurb"></p>
  <ul class="mp-list" id="mp-list" aria-live="polite"></ul>

  <div class="mp-bar" id="mp-bar" aria-label="Now playing">
    <div class="mp-now">
      <span class="lbl">Now playing</span>
      <span class="ttl" id="mp-now-title">—</span>
      <span class="lane" id="mp-now-lane"></span>
    </div>
    <div class="mp-seekrow">
      <span class="mp-time" id="mp-cur">0:00</span>
      <input type="range" class="mp-seek" id="mp-seek" min="0" max="100" value="0" step="0.1"
             aria-label="Seek">
      <span class="mp-time" id="mp-dur">0:00</span>
    </div>
    <div class="mp-ctrls">
      <button class="mp-btn" id="mp-prev" type="button" aria-label="Previous track">&#9664;&#9664;</button>
      <button class="mp-btn primary" id="mp-play" type="button" aria-label="Play">&#9654;</button>
      <button class="mp-btn" id="mp-next" type="button" aria-label="Next track">&#9654;&#9654;</button>
    </div>
    <div class="mp-err" id="mp-err"></div>
    <audio id="mp-audio" preload="none"></audio>
  </div>
</div>
"""

    # ── Player logic. Deliberately ES5: var, function expressions, no template
    #    literals, no arrow functions, XHR (not fetch) for the manifest so it
    #    runs on very old WebKit/Android browsers. No build step, no deps.
    script = r"""
<script>
(function(){
  "use strict";
  var MANIFEST_URL = "music-manifest.json";

  var lanesEl  = document.getElementById("mp-lanes");
  var blurbEl  = document.getElementById("mp-laneblurb");
  var listEl   = document.getElementById("mp-list");
  var audio    = document.getElementById("mp-audio");
  var playBtn  = document.getElementById("mp-play");
  var prevBtn  = document.getElementById("mp-prev");
  var nextBtn  = document.getElementById("mp-next");
  var seekEl   = document.getElementById("mp-seek");
  var curEl    = document.getElementById("mp-cur");
  var durEl    = document.getElementById("mp-dur");
  var nowTitle = document.getElementById("mp-now-title");
  var nowLane  = document.getElementById("mp-now-lane");
  var errEl    = document.getElementById("mp-err");
  var statusEl = document.getElementById("mp-status");

  if(!lanesEl || !audio){ return; } // page without the app block — nothing to do

  var data = null;
  var laneIdx = 0;
  var trackIdx = -1;
  var seeking = false;

  function fmt(s){
    if(!isFinite(s) || s < 0){ s = 0; }
    var m = Math.floor(s / 60);
    var r = Math.floor(s % 60);
    return m + ":" + (r < 10 ? "0" : "") + r;
  }

  function currentLane(){ return data.lanes[laneIdx]; }
  function currentTracks(){ return currentLane().tracks; }

  function renderLanes(){
    lanesEl.innerHTML = "";
    for(var i = 0; i < data.lanes.length; i++){
      (function(i){
        var lane = data.lanes[i];
        var b = document.createElement("button");
        b.className = "mp-lane";
        b.setAttribute("type", "button");
        b.setAttribute("role", "tab");
        b.setAttribute("aria-selected", i === laneIdx ? "true" : "false");
        b.innerHTML = esc(lane.name) +
          '<span class="n">' + lane.tracks.length + '</span>';
        b.onclick = function(){ selectLane(i); };
        lanesEl.appendChild(b);
      })(i);
    }
  }

  function renderList(){
    var lane = currentLane();
    blurbEl.textContent = lane.blurb || "";
    listEl.innerHTML = "";
    var tracks = lane.tracks;
    if(!tracks.length){
      var li = document.createElement("li");
      li.className = "mp-empty";
      li.textContent = "No tracks in this lane yet.";
      listEl.appendChild(li);
      return;
    }
    for(var i = 0; i < tracks.length; i++){
      (function(i){
        var t = tracks[i];
        var li = document.createElement("li");
        li.className = "mp-track";
        li.setAttribute("aria-current", (i === trackIdx) ? "true" : "false");

        var num = document.createElement("span");
        num.className = "ti";
        num.textContent = (i + 1);

        var pb = document.createElement("button");
        pb.className = "play";
        pb.setAttribute("type", "button");
        pb.setAttribute("aria-label", "Play " + t.title);
        pb.innerHTML = (i === trackIdx && !audio.paused) ? "&#10074;&#10074;" : "&#9654;";

        var tt = document.createElement("span");
        tt.className = "tt";
        var b = document.createElement("b");
        b.textContent = t.title;
        tt.appendChild(b);

        li.appendChild(num);
        li.appendChild(pb);
        li.appendChild(tt);

        // A/B variant chooser (Suno ships two renders per song)
        if(t.variants && t.variants.length > 1){
          var vs = document.createElement("span");
          vs.className = "vs";
          for(var v = 0; v < t.variants.length; v++){
            (function(v){
              var vb = document.createElement("button");
              vb.className = "vbtn";
              vb.setAttribute("type", "button");
              vb.setAttribute("aria-pressed", (t._v || 0) === v ? "true" : "false");
              vb.textContent = t.variants[v].label;
              vb.onclick = function(e){
                e.stopPropagation();
                t._v = v;
                if(i === trackIdx){ loadTrack(i, true); }
                renderList();
              };
              vs.appendChild(vb);
            })(v);
          }
          li.appendChild(vs);
        }

        // honesty flag: no audio bytes available for this track yet
        var hasFile = t.variants ? t.variants[t._v || 0].onDisk : false;
        if(!hasFile){
          var nf = document.createElement("span");
          nf.className = "nofile";
          nf.textContent = "no file yet";
          li.appendChild(nf);
        }

        var go = function(){ play(i); };
        li.onclick = go;
        pb.onclick = function(e){ e.stopPropagation(); play(i); };

        listEl.appendChild(li);
      })(i);
    }
  }

  function urlFor(t){
    if(t.variants && t.variants.length){
      return t.variants[t._v || 0].audioUrl;
    }
    return t.audioUrl;
  }

  function loadTrack(i, keepPlaying){
    var tracks = currentTracks();
    if(i < 0 || i >= tracks.length){ return; }
    trackIdx = i;
    var t = tracks[i];
    audio.src = urlFor(t);
    nowTitle.textContent = t.title;
    nowLane.textContent = "· " + currentLane().name;
    errEl.textContent = "";
    renderList();
    if(keepPlaying){ audio.play().catch(noop); }
  }

  function play(i){
    if(i === trackIdx){
      // toggle the current track
      if(audio.paused){ audio.play().catch(showErr); }
      else { audio.pause(); }
      syncPlayBtn();
      return;
    }
    loadTrack(i, false);
    audio.play().catch(showErr);
    syncPlayBtn();
  }

  function selectLane(i){
    if(i === laneIdx){ return; }
    laneIdx = i;
    trackIdx = -1;
    renderLanes();
    renderList();
  }

  function next(){
    var tracks = currentTracks();
    if(!tracks.length){ return; }
    var i = (trackIdx + 1);
    if(i >= tracks.length){ i = 0; }
    play(i);
  }
  function prev(){
    var tracks = currentTracks();
    if(!tracks.length){ return; }
    // restart if more than 3s in, else go to previous
    if(audio.currentTime > 3){ audio.currentTime = 0; return; }
    var i = (trackIdx - 1);
    if(i < 0){ i = tracks.length - 1; }
    play(i);
  }

  function syncPlayBtn(){
    playBtn.innerHTML = audio.paused ? "&#9654;" : "&#10074;&#10074;";
    playBtn.setAttribute("aria-label", audio.paused ? "Play" : "Pause");
    renderList();
  }

  function showErr(){
    // play() rejects when there is no hosted file yet (expected pre-R2).
    errEl.textContent = "No audio file at " + (audio.currentSrc || audio.src) +
      " yet — upload the catalogue to wire it up.";
  }
  function noop(){}
  function esc(s){
    return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
  }

  // transport wiring
  playBtn.onclick = function(){
    if(trackIdx < 0){ play(0); return; }
    if(audio.paused){ audio.play().catch(showErr); } else { audio.pause(); }
    syncPlayBtn();
  };
  nextBtn.onclick = next;
  prevBtn.onclick = prev;

  audio.addEventListener("play", syncPlayBtn);
  audio.addEventListener("pause", syncPlayBtn);
  audio.addEventListener("ended", next);
  audio.addEventListener("error", showErr);
  audio.addEventListener("timeupdate", function(){
    if(seeking){ return; }
    curEl.textContent = fmt(audio.currentTime);
    if(audio.duration && isFinite(audio.duration)){
      seekEl.value = (audio.currentTime / audio.duration) * 100;
    }
  });
  audio.addEventListener("loadedmetadata", function(){
    durEl.textContent = fmt(audio.duration);
  });

  seekEl.addEventListener("input", function(){ seeking = true; });
  seekEl.addEventListener("change", function(){
    if(audio.duration && isFinite(audio.duration)){
      audio.currentTime = (seekEl.value / 100) * audio.duration;
    }
    seeking = false;
  });

  // keyboard: space = play/pause, arrows = prev/next (when not typing)
  document.addEventListener("keydown", function(e){
    var tag = (e.target && e.target.tagName) ? e.target.tagName.toUpperCase() : "";
    if(tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT"){ return; }
    if(e.key === " " || e.keyCode === 32){ e.preventDefault(); playBtn.onclick(); }
    else if(e.key === "ArrowRight"){ next(); }
    else if(e.key === "ArrowLeft"){ prev(); }
  });

  function boot(json){
    data = json;
    if(statusEl && data.stats){
      // real counts; audio is self-hosted and playing
      statusEl.innerHTML = '<strong>' + data.stats.lanes + ' lanes · ' +
        data.stats.tracks + ' songs.</strong> Self-hosted on our own rails — AJ\'s catalogue, ' +
        'served from here, no streaming silo. Press play.';
    }
    renderLanes();
    renderList();
  }

  // XHR (not fetch) — old-browser friendly, no polyfill needed.
  function loadManifest(){
    var xhr = new XMLHttpRequest();
    xhr.open("GET", MANIFEST_URL, true);
    xhr.onreadystatechange = function(){
      if(xhr.readyState !== 4){ return; }
      if(xhr.status >= 200 && xhr.status < 300){
        try { boot(JSON.parse(xhr.responseText)); }
        catch(err){ if(statusEl){ statusEl.textContent = "Could not read the music manifest."; } }
      } else {
        if(statusEl){ statusEl.textContent = "Could not load the music manifest (HTTP " + xhr.status + ")."; }
      }
    };
    xhr.send();
  }

  loadManifest();
})();
</script>"""

    return "\n".join([
        head(title, desc, rel=rel, canonical=canonical,
             keywords="Jakobus, Arjuna Sound, music player, self-hosted music, "
                      "Banjos and Bass, Brass'n'Bass, Die Dier, Wolf, Rasta, "
                      "AJ Greyling, A Man They All Read Wrong, badger thesis, "
                      "open music, congosky"),
        style,
        nav(rel),
        body,
        script,
        footer(rel),
    ])


# Lanes surfaced by the embedded book-page player — the companion soundtrack to
# "A Man They All Read Wrong". Matched by manifest lane name; anything not listed
# stays on the full /the-man-they-all-misread.html page (all 9 lanes).
JAKOBUS_EMBED_LANES = (
    "Jakobus Brass'n'Bass — The Misread Man",
    "The Still Man Banger Series",
    "Banjos & Bass — Arjuna Sound",
)


def render_jakobus_player_embed(rel: str = "../") -> str:
    """A compact, self-contained music player embedded directly on the Jakobus File book
    page — no separate page, no iframe. It reads the same music-manifest.json the full
    companion player uses, but scopes itself to the three soundtrack lanes (Brass'n'Bass,
    the Still-Man bangers, Banjos & Bass) so the book page carries the music it belongs to.

    Self-hosted on our own rails (the badger thesis): a plain HTML/CSS/JS <audio> player off
    a JSON manifest, no streaming silo. Vanilla ES5 (var/XHR/no template literals), styles
    prefixed .jpx- so nothing leaks into the global sheet, dark house tokens. Degrades on
    ancient devices and works with JS off (a link to the full player is always shown).

    `rel` is the path back to the site root from the page hosting this embed (book pages are
    one level deep → "../"), used for the manifest fetch and the full-player link.
    """
    manifest_url = f"{rel}music-manifest.json"
    full_url = f"{rel}the-man-they-all-misread.html"
    lanes_json = html.escape(json.dumps(list(JAKOBUS_EMBED_LANES), ensure_ascii=False))

    style = """
<style>
.jpx{margin:26px 0 0;border:1px solid var(--line);border-radius:14px;background:var(--card);
  padding:18px 18px 16px;overflow:hidden}
.jpx-head{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin:0 0 4px}
.jpx-head .eyebrow{font-family:var(--reading);font-size:11px;letter-spacing:.2em;
  text-transform:uppercase;color:var(--grass);margin:0}
.jpx-head h3{font-family:var(--reading);font-weight:600;font-size:22px;
  margin:0;color:var(--bone)}
.jpx-sub{font-family:var(--reading);font-style:italic;color:var(--ochre);
  font-size:15px;margin:2px 0 0;max-width:66ch}
.jpx-sub a{color:var(--gold)}
.jpx-lanes{display:flex;flex-wrap:wrap;gap:7px;margin:14px 0 2px}
.jpx-lane{flex:0 0 auto;cursor:pointer;border:1px solid var(--line);background:transparent;
  color:var(--bone);font-family:var(--reading);font-size:13px;font-weight:500;
  padding:7px 12px;border-radius:999px;line-height:1.2;white-space:nowrap;
  transition:border-color .15s,background .15s,color .15s}
.jpx-lane:hover{border-color:var(--ochre);color:var(--gold)}
.jpx-lane[aria-selected="true"]{background:var(--ochre);border-color:var(--ochre);color:var(--black)}
.jpx-lane .n{opacity:.6;font-size:11px;margin-left:5px}
.jpx-blurb{font-family:var(--reading);font-style:italic;font-size:15px;line-height:1.4;
  color:var(--ochre);max-width:66ch;margin:11px 0 0}
.jpx-list{list-style:none;margin:12px 0 0;padding:0;max-height:300px;overflow-y:auto;
  -webkit-overflow-scrolling:touch;border-top:1px solid var(--line)}
.jpx-track{display:flex;align-items:center;gap:11px;padding:10px 6px;border-bottom:1px solid var(--line);
  cursor:pointer}
.jpx-track:hover{background:rgba(229,181,103,.05)}
.jpx-track[aria-current="true"]{background:rgba(229,181,103,.10)}
.jpx-track .ti{flex:0 0 auto;width:24px;text-align:right;color:var(--grass);
  font-family:var(--reading);font-size:12px;font-variant-numeric:tabular-nums}
.jpx-track .play{flex:0 0 auto;width:27px;height:27px;border-radius:50%;border:1px solid var(--line);
  background:transparent;color:var(--ochre);font-size:12px;line-height:1;display:flex;
  align-items:center;justify-content:center;cursor:pointer}
.jpx-track[aria-current="true"] .play{background:var(--ochre);border-color:var(--ochre);color:var(--black)}
.jpx-track .tt{flex:1 1 auto;min-width:0;font-family:var(--reading);font-size:14px;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.jpx-track .vs{flex:0 0 auto;display:flex;gap:5px}
.jpx-track .vbtn{font-family:var(--reading);font-size:11px;letter-spacing:.06em;
  border:1px solid var(--line);background:transparent;color:var(--bonedim);border-radius:6px;
  padding:2px 7px;cursor:pointer}
.jpx-track .vbtn[aria-pressed="true"]{border-color:var(--gold);color:var(--gold)}
.jpx-bar{margin-top:14px;border-top:1px solid var(--line);padding-top:13px}
.jpx-now{display:flex;align-items:baseline;gap:9px;flex-wrap:wrap;margin:0 0 9px}
.jpx-now .lbl{font-family:var(--reading);font-size:10px;letter-spacing:.2em;
  text-transform:uppercase;color:var(--grass)}
.jpx-now .ttl{font-family:var(--reading);font-size:18px;color:var(--bone)}
.jpx-now .lane{color:var(--ochre);font-size:12px;font-family:var(--reading)}
.jpx-seekrow{display:flex;align-items:center;gap:9px}
.jpx-time{font-family:var(--reading);font-size:11px;color:var(--grass);
  font-variant-numeric:tabular-nums;flex:0 0 auto;width:40px;text-align:center}
.jpx-seek{flex:1 1 auto;-webkit-appearance:none;appearance:none;height:5px;border-radius:3px;
  background:var(--line);outline:none;cursor:pointer}
.jpx-seek::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:13px;height:13px;
  border-radius:50%;background:var(--gold);cursor:pointer}
.jpx-seek::-moz-range-thumb{width:13px;height:13px;border:0;border-radius:50%;background:var(--gold);cursor:pointer}
.jpx-ctrls{display:flex;align-items:center;justify-content:center;gap:12px;margin-top:11px}
.jpx-btn{border:1px solid var(--line);background:transparent;color:var(--bone);cursor:pointer;
  border-radius:999px;font-family:var(--reading);font-size:14px;padding:8px 14px;
  min-width:42px;line-height:1}
.jpx-btn:hover{border-color:var(--ochre);color:var(--gold)}
.jpx-btn.primary{background:var(--ochre);border-color:var(--ochre);color:var(--black);
  font-size:16px;padding:9px 20px}
.jpx-btn.primary:hover{background:var(--gold);border-color:var(--gold)}
.jpx-err{color:var(--sting);font-size:12px;font-family:var(--reading);
  text-align:center;margin:8px 0 0;min-height:1em}
.jpx-more{margin:13px 0 0;font-family:var(--reading);font-size:13px}
.jpx-more a{color:var(--gold)}
.jpx-empty{color:var(--bonedim);padding:24px 0;text-align:center;font-style:italic}
@media (max-width:540px){.jpx-track .vs{display:none}.jpx-now .ttl{font-size:16px}}
.jpx-noscript a{color:var(--gold)}
</style>"""

    body = f"""
<div class="jpx" id="jpx" data-manifest="{html.escape(manifest_url)}"
     data-lanes="{lanes_json}" data-full="{html.escape(full_url)}">
  <div class="jpx-head">
    <p class="eyebrow">Arjuna Sound · the soundtrack</p>
    <h3>Listen — The Man They All Misread</h3>
  </div>
  <p class="jpx-sub">Jakobus &amp; Beast, made not curated — AJ's own songs on his own rails,
  self-hosted, no streaming silo. Pick a lane, press play.</p>
  <noscript><p class="jpx-noscript"><a href="{html.escape(full_url)}">Open the full companion
  player →</a></p></noscript>
  <div class="jpx-lanes" id="jpx-lanes" role="tablist" aria-label="Soundtrack lanes"></div>
  <p class="jpx-blurb" id="jpx-blurb"></p>
  <ul class="jpx-list" id="jpx-list" aria-live="polite"></ul>
  <div class="jpx-bar" id="jpx-bar" aria-label="Now playing">
    <div class="jpx-now">
      <span class="lbl">Now playing</span>
      <span class="ttl" id="jpx-now-title">—</span>
      <span class="lane" id="jpx-now-lane"></span>
    </div>
    <div class="jpx-seekrow">
      <span class="jpx-time" id="jpx-cur">0:00</span>
      <input type="range" class="jpx-seek" id="jpx-seek" min="0" max="100" value="0" step="0.1"
             aria-label="Seek">
      <span class="jpx-time" id="jpx-dur">0:00</span>
    </div>
    <div class="jpx-ctrls">
      <button class="jpx-btn" id="jpx-prev" type="button" aria-label="Previous track">&#9664;&#9664;</button>
      <button class="jpx-btn primary" id="jpx-play" type="button" aria-label="Play">&#9654;</button>
      <button class="jpx-btn" id="jpx-next" type="button" aria-label="Next track">&#9654;&#9654;</button>
    </div>
    <div class="jpx-err" id="jpx-err"></div>
    <audio id="jpx-audio" preload="none"></audio>
  </div>
  <p class="jpx-more"><a href="{html.escape(full_url)}">All 9 lanes &amp; 65 songs — the full
  companion player →</a></p>
</div>"""

    # ES5: var / function expressions / XHR / no template literals — runs on old WebKit/Android.
    script = r"""
<script>
(function(){
  "use strict";
  var root = document.getElementById("jpx");
  if(!root){ return; }
  var MANIFEST_URL = root.getAttribute("data-manifest");
  var WANT = [];
  try { WANT = JSON.parse(root.getAttribute("data-lanes")); } catch(e){ WANT = []; }

  var lanesEl  = document.getElementById("jpx-lanes");
  var blurbEl  = document.getElementById("jpx-blurb");
  var listEl   = document.getElementById("jpx-list");
  var audio    = document.getElementById("jpx-audio");
  var playBtn  = document.getElementById("jpx-play");
  var prevBtn  = document.getElementById("jpx-prev");
  var nextBtn  = document.getElementById("jpx-next");
  var seekEl   = document.getElementById("jpx-seek");
  var curEl    = document.getElementById("jpx-cur");
  var durEl    = document.getElementById("jpx-dur");
  var nowTitle = document.getElementById("jpx-now-title");
  var nowLane  = document.getElementById("jpx-now-lane");
  var errEl    = document.getElementById("jpx-err");

  if(!lanesEl || !audio){ return; }

  var lanes = [];      // filtered, ordered to match WANT
  var laneIdx = 0;
  var trackIdx = -1;
  var seeking = false;

  function fmt(s){
    if(!isFinite(s) || s < 0){ s = 0; }
    var m = Math.floor(s / 60);
    var r = Math.floor(s % 60);
    return m + ":" + (r < 10 ? "0" : "") + r;
  }
  function esc(s){
    return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
  }
  function noop(){}
  function currentLane(){ return lanes[laneIdx]; }
  function currentTracks(){ return currentLane().tracks; }

  function renderLanes(){
    lanesEl.innerHTML = "";
    for(var i = 0; i < lanes.length; i++){
      (function(i){
        var lane = lanes[i];
        var b = document.createElement("button");
        b.className = "jpx-lane";
        b.setAttribute("type", "button");
        b.setAttribute("role", "tab");
        b.setAttribute("aria-selected", i === laneIdx ? "true" : "false");
        b.innerHTML = esc(lane.name) + '<span class="n">' + lane.tracks.length + '</span>';
        b.onclick = function(){ selectLane(i); };
        lanesEl.appendChild(b);
      })(i);
    }
  }

  function renderList(){
    var lane = currentLane();
    blurbEl.textContent = lane.blurb || "";
    listEl.innerHTML = "";
    var tracks = lane.tracks;
    if(!tracks.length){
      var li = document.createElement("li");
      li.className = "jpx-empty";
      li.textContent = "No tracks in this lane yet.";
      listEl.appendChild(li);
      return;
    }
    for(var i = 0; i < tracks.length; i++){
      (function(i){
        var t = tracks[i];
        var li = document.createElement("li");
        li.className = "jpx-track";
        li.setAttribute("aria-current", (i === trackIdx) ? "true" : "false");

        var num = document.createElement("span");
        num.className = "ti";
        num.textContent = (i + 1);

        var pb = document.createElement("button");
        pb.className = "play";
        pb.setAttribute("type", "button");
        pb.setAttribute("aria-label", "Play " + t.title);
        pb.innerHTML = (i === trackIdx && !audio.paused) ? "&#10074;&#10074;" : "&#9654;";

        var tt = document.createElement("span");
        tt.className = "tt";
        tt.textContent = t.title;

        li.appendChild(num);
        li.appendChild(pb);
        li.appendChild(tt);

        if(t.variants && t.variants.length > 1){
          var vs = document.createElement("span");
          vs.className = "vs";
          for(var v = 0; v < t.variants.length; v++){
            (function(v){
              var vb = document.createElement("button");
              vb.className = "vbtn";
              vb.setAttribute("type", "button");
              vb.setAttribute("aria-pressed", (t._v || 0) === v ? "true" : "false");
              vb.textContent = t.variants[v].label;
              vb.onclick = function(e){
                e.stopPropagation();
                t._v = v;
                if(i === trackIdx){ loadTrack(i, true); }
                renderList();
              };
              vs.appendChild(vb);
            })(v);
          }
          li.appendChild(vs);
        }

        li.onclick = function(){ play(i); };
        pb.onclick = function(e){ e.stopPropagation(); play(i); };
        listEl.appendChild(li);
      })(i);
    }
  }

  function urlFor(t){
    if(t.variants && t.variants.length){ return t.variants[t._v || 0].audioUrl; }
    return t.audioUrl;
  }

  function loadTrack(i, keepPlaying){
    var tracks = currentTracks();
    if(i < 0 || i >= tracks.length){ return; }
    trackIdx = i;
    var t = tracks[i];
    audio.src = urlFor(t);
    nowTitle.textContent = t.title;
    nowLane.textContent = "· " + currentLane().name;
    errEl.textContent = "";
    renderList();
    if(keepPlaying){ audio.play().catch(noop); }
  }

  function play(i){
    if(i === trackIdx){
      if(audio.paused){ audio.play().catch(showErr); } else { audio.pause(); }
      syncPlayBtn();
      return;
    }
    loadTrack(i, false);
    audio.play().catch(showErr);
    syncPlayBtn();
  }

  function selectLane(i){
    if(i === laneIdx){ return; }
    laneIdx = i;
    trackIdx = -1;
    renderLanes();
    renderList();
  }

  function next(){
    var tracks = currentTracks();
    if(!tracks.length){ return; }
    var i = (trackIdx + 1);
    if(i >= tracks.length){ i = 0; }
    play(i);
  }
  function prev(){
    var tracks = currentTracks();
    if(!tracks.length){ return; }
    if(audio.currentTime > 3){ audio.currentTime = 0; return; }
    var i = (trackIdx - 1);
    if(i < 0){ i = tracks.length - 1; }
    play(i);
  }

  function syncPlayBtn(){
    playBtn.innerHTML = audio.paused ? "&#9654;" : "&#10074;&#10074;";
    playBtn.setAttribute("aria-label", audio.paused ? "Play" : "Pause");
    renderList();
  }
  function showErr(){
    errEl.textContent = "Could not play this track yet.";
  }

  playBtn.onclick = function(){
    if(trackIdx < 0){ play(0); return; }
    if(audio.paused){ audio.play().catch(showErr); } else { audio.pause(); }
    syncPlayBtn();
  };
  nextBtn.onclick = next;
  prevBtn.onclick = prev;

  audio.addEventListener("play", syncPlayBtn);
  audio.addEventListener("pause", syncPlayBtn);
  audio.addEventListener("ended", next);
  audio.addEventListener("error", showErr);
  audio.addEventListener("timeupdate", function(){
    if(seeking){ return; }
    curEl.textContent = fmt(audio.currentTime);
    if(audio.duration && isFinite(audio.duration)){
      seekEl.value = (audio.currentTime / audio.duration) * 100;
    }
  });
  audio.addEventListener("loadedmetadata", function(){ durEl.textContent = fmt(audio.duration); });
  seekEl.addEventListener("input", function(){ seeking = true; });
  seekEl.addEventListener("change", function(){
    if(audio.duration && isFinite(audio.duration)){
      audio.currentTime = (seekEl.value / 100) * audio.duration;
    }
    seeking = false;
  });

  function boot(json){
    var all = (json && json.lanes) || [];
    // keep only the wanted lanes, in WANT order
    for(var w = 0; w < WANT.length; w++){
      for(var k = 0; k < all.length; k++){
        if(all[k].name === WANT[w]){ lanes.push(all[k]); break; }
      }
    }
    if(!lanes.length){ lanes = all.slice(0, 1); } // fallback: never blank
    if(!lanes.length){
      listEl.innerHTML = '<li class="jpx-empty">No soundtrack lanes found.</li>';
      return;
    }
    renderLanes();
    renderList();
  }

  function loadManifest(){
    var xhr = new XMLHttpRequest();
    xhr.open("GET", MANIFEST_URL, true);
    xhr.onreadystatechange = function(){
      if(xhr.readyState !== 4){ return; }
      if(xhr.status >= 200 && xhr.status < 300){
        try { boot(JSON.parse(xhr.responseText)); }
        catch(err){ listEl.innerHTML = '<li class="jpx-empty">Could not read the music manifest.</li>'; }
      } else {
        listEl.innerHTML = '<li class="jpx-empty">Could not load the music manifest (HTTP ' + xhr.status + ').</li>';
      }
    };
    xhr.send();
  }

  loadManifest();
})();
</script>"""

    return style + body + script


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
body {{ font-family:"Atkinson Hyperlegible",system-ui,sans-serif; color:#161513; }}
.sheet {{ width:210mm; min-height:297mm; margin:0 auto; background:#fbf8f2;
  padding:20mm 18mm; display:flex; flex-direction:column; position:relative; }}
.screen-only {{ background:#161513; padding:18px; text-align:center; color:#ede9e0; font-size:14px; }}
@media print {{ .screen-only {{ display:none; }} html,body{{background:#fff;}} }}
.eyebrow {{ font-family:var(--reading); letter-spacing:.22em; text-transform:uppercase;
  font-size:12px; color:#b07a3c; font-weight:600; }}
h1 {{ font-family:var(--reading); font-weight:700; font-size:52px; line-height:1.02;
  margin:6mm 0 4mm; }}
h1 .hot {{ color:#c2401e; }}
.lead {{ font-size:19px; line-height:1.5; max-width:150mm; color:#2a241d; }}
.big {{ font-size:23px; font-weight:700; margin:6mm 0 2mm; }}
.row {{ display:flex; gap:14mm; align-items:center; margin-top:auto; }}
.qr {{ width:62mm; height:62mm; flex:0 0 auto; border:2px dashed #161513; border-radius:8px;
  display:flex; align-items:center; justify-content:center; text-align:center; font-size:12px;
  color:#6a635a; padding:8px; background:#fff; }}
.qr img {{ width:100%; height:100%; object-fit:contain; }}
.scan h2 {{ font-family:var(--reading); font-size:22px; margin:0 0 4px; }}
.scan p {{ font-size:16px; line-height:1.45; margin:.2em 0; color:#2a241d; }}
.scan .url {{ font-family:var(--reading); font-weight:600; font-size:18px; color:#b07a3c; }}
.tiers {{ display:flex; gap:8mm; margin:5mm 0; flex-wrap:wrap; }}
.tier {{ flex:1; min-width:42mm; border:1px solid #d8cfbe; border-radius:8px; padding:10px 12px; background:#fff; }}
.tier b {{ display:block; font-family:var(--reading); font-size:14px; }}
.tier .amt {{ font-size:20px; font-weight:700; color:#161513; }}
.tier.f .amt {{ color:#c2401e; }}
.trust {{ margin-top:6mm; border-top:1px solid #d8cfbe; padding-top:4mm; font-size:13.5px; color:#5a534a; line-height:1.5; }}
.trust strong {{ color:#161513; }}
.foot {{ margin-top:5mm; display:flex; justify-content:space-between; align-items:flex-end; }}
.foot img {{ height:16mm; }}
.foot .when {{ text-align:right; font-family:var(--reading); font-size:13px; color:#5a534a; }}
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
        """<hr class="hr"><section class="mission" id="african-worlds-study-bible"><div class="wrap">
<div class="eyebrow">In development</div>
<h2 style="font-size:28px;margin:.3em 0">The African Worlds Study Bible</h2>
<p style="max-width:70ch;color:var(--bonedim);font-size:17px">An Africa-centred, evidence-led study Bible proposal:
Africa restored to the map, the text, the transmission, and the earliest church — without replacing one distortion with another.</p>
<div class="cta"><a class="btn" href="african-worlds-study-bible.html">Read the full proposal</a></div>
</div></section>""",
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
<div class="cta"><a class="btn" href="safari/technology.html">How /sleep works</a>
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


def render_landing(read_now: int = 0, avail: int = 0) -> str:
    """The www / apex front door — the origin story, then a door into each of the three products.

    Served at www.arjunabadger.press (and apex → www). Product cards point at the subdomains, but
    fall back gracefully to paths when subdomains aren't live yet (the path targets still resolve).
    `read_now` / `avail` are the live library counts from the same pass that builds index.html."""
    lib_line = (
        f"<strong>{read_now} books, free</strong> — {avail} ready to download (read online, EPUB &amp; PDF). "
        "Fact-checked, both sides told. A free Amazon, only better, with no paywall."
        if read_now
        else "Finished books, free to read — online, EPUB, and PDF. Fact-checked, both sides told. "
             "A free Amazon, only better, with no paywall."
    )
    return "\n".join([
        head("Arjuna Badger Press — free to read, free to publish",
             "A publishing house built because the gatekeepers said no. Read finished books free, "
             "write your own in the Studio, and meet the man who built it.",
             canonical=f"{DOMAIN}/"),
        nav(),
        f"""<header class="hero"><div class="wrap">
<img class="crest" src="assets/brand/logo-master.png" alt="Arjuna Badger Press crest">
<h1>Arjuna Badger Press</h1>
<div class="tag serif">{TAGLINE}</div>
<p class="lead">A publishing house that exists because the front door was locked — so we built our own, and left it open for everyone.</p>
<div class="cta"><a class="btn" href="https://library.{DOMAIN.split('//')[1]}/">Read the library — free</a>
<a class="btn ghost" href="https://studio.{DOMAIN.split('//')[1]}/">Writers → the Studio</a></div>
</div></header><hr class="hr">""",
        # ── The origin story ──────────────────────────────────────────────
        f"""<section class="mission"><div class="wrap" style="max-width:760px">
<div class="eyebrow">Why this exists</div>
<h2 style="font-size:30px;margin:.3em 0 .5em">The front door was locked. So I built my own.</h2>
<div style="color:var(--bonedim);font-size:18px;line-height:1.65">
<p>I wrote a book. Then I tried to do the obvious thing: publish it, for free, where readers are.</p>
<p>I couldn't. Not because the work wasn't ready — because the gates were shut. The big stores
make "free" surprisingly hard: some <strong>won't let you price a book at zero at all.</strong>
Several demand <strong>ISBNs I can't get</strong> — South Africa issues them free through the
National Library, but the application site is broken and there is no working alternative, and
buying commercial ISBNs for a whole catalogue is absurdly expensive. Some platforms
<strong>don't properly support South Africa</strong> in the first place. Refusing to let a writer
give a book away — in the age of AI-assisted literature, when the cost of making and shipping a
clean book has collapsed — is, frankly, insane.</p>
<p>So I did what Elon Musk did when he wanted to drive an electric car and nobody would sell him a
good one: <strong>I stopped waiting for permission and built the thing myself.</strong> A whole
publishing house — the press, the library, the craft, the engine — and I self-published my own work
on it, free to read, no paywall, no gatekeeper.</p>
<p>Then the obvious next thought: <strong>why keep it to myself?</strong> Every wall I hit, every
other writer hits too. So the house became a <strong>platform — a Studio any writer can use</strong>
to finish a book in their own voice and put it somewhere readers can actually find it. Free to read.
Free, where it should be, to publish.</p>
<p class="serif" style="font-style:italic;color:var(--gold);font-size:19px;margin-top:1.2em">The door
that was locked to me is the one I'm holding open for you.</p>
</div>
</div></section><hr class="hr">""",
        # ── The three products ────────────────────────────────────────────
        f"""<section class="mission"><div class="wrap">
<div class="eyebrow">Three ways in</div>
<h2 style="font-size:28px;margin:.3em 0 .8em">One house, three doors</h2>
<div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(240px,1fr))">
<a class="card" style="--accent:#C8A86B;text-decoration:none" href="https://library.{DOMAIN.split('//')[1]}/">
<div class="body"><span class="ser">Read</span><h3>The Library</h3>
<p>{lib_line}</p><span class="badge">library.arjunabadger.press</span></div></a>
<a class="card" style="--accent:#7C5CFF;text-decoration:none" href="https://studio.{DOMAIN.split('//')[1]}/">
<div class="body"><span class="ser">Write</span><h3>The Studio</h3>
<p>The writers' tool. Bring a draft, get a prioritised finish map in your own words, publish straight
to the library. Simpler than the rest.</p><span class="badge">studio.arjunabadger.press</span></div></a>
<a class="card" style="--accent:#7BA88C;text-decoration:none" href="https://ajgreyling.{DOMAIN.split('//')[1]}/">
<div class="body"><span class="ser">The maker</span><h3>Meet the man</h3>
<p>The person behind the press — the CV, the letters, the House, and the why. The Misogi that started
all of this.</p><span class="badge">ajgreyling.arjunabadger.press</span></div></a>
</div>
</div></section>""",
        footer(),
    ])


def render_index(entries: list[dict]) -> str:
    avail = sum(1 for e in entries if e["available"])
    read_now = sum(1 for e in entries if e["available"] or e.get("serial"))
    pending = sum(1 for e in entries if not e["available"] and not e.get("serial"))
    parts = [head("Arjuna Badger Press — the library",
                  "Free books, finished to a studio standard — read online or download EPUB and PDF."),
             nav()]
    # ── Books-first: cinematic hero with cover-mosaic backdrop, then Audible-style
    #    horizontal scroll shelves. The page is the LIBRARY — mission lives below the
    #    fold and on its own pages (press.html, join.html). ──
    backdrop = [e for e in entries if e["available"] and e.get("cover")][:9]
    backdrop_imgs = "".join(
        f'<img src="{cover_thumb_src(e["id"], e.get("cover"))}" '
        f'alt="" aria-hidden="true" loading="eager" decoding="async">'
        for e in backdrop
    )
    parts.append(f"""<header class="lib-hero"><div class="lib-hero-bg" aria-hidden="true">{backdrop_imgs}</div>
<div class="wrap">
<a class="lib-hero-crest" href="#library" aria-label="Arjuna Badger Press"><img src="assets/brand/logo-master.png" alt="Arjuna Badger Press crest" width="76" height="76"></a>
<div class="lib-hero-text">
<h1>The Library</h1>
<p class="lead"><strong>{read_now} books, free.</strong> {avail} ready to download — read online, EPUB &amp; PDF. Finished to a studio standard; both sides told.</p>
<div class="cta"><a class="btn" href="start.html">Where to start?</a>
<a class="btn ghost" href="press.html">About the press</a>
<a class="btn ghost" href="/studio">Writers → Studio</a></div>
</div>
</div></header>""")

    parts.append('<section id="library">')
    parts.append(render_library_shelves_audible(entries, available_only=True))
    parts.append('</section>')

    # ── Below the fold: the house. Collapsed to a quiet strip + a "call to arms"
    #    card, so the books own the page and the mission is one scroll away. ──
    parts.append('<hr class="hr">')
    parts.append(f"""<section class="callarms"><div class="wrap">
<div class="callarms-inner">
<div class="eyebrow">Afrika Rising · a call to arms</div>
<h2>These are your stories. Help us write them true.</h2>
<p>A Zulu voice for the empty seat in <em>Brave and Scared</em>. A Coloured Capetonian for South
Africa's deep past. An SA Indian woman for the India books. Sensitivity readers, translators, and
narrators for every people these books touch — paid, credited, and named.</p>
<div class="cta"><a class="btn" href="join.html">Put your hand up &rarr;</a></div>
</div>
</div></section>""")
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
    "afrika-2100": "science fiction, first contact, solar flare, post-apocalyptic, South Africa, "
                   "alien contact, literary sci-fi, free ebook, The African Gold Trilogy",
    # Reichenbach Files — Sherlock Holmes / mystery readers.
    "modern-sherlock": "Sherlock Holmes, modern Sherlock, Holmes retelling, detective fiction, "
                       "mystery novel, crime fiction, Conan Doyle, A Study in Scarlet, free mystery ebook, The Reichenbach Files",
    # Salt Veil — epic fantasy readers.
    "the-salt-veil": "epic fantasy, desert fantasy, adult fantasy, fantasy novel, women warriors, "
                     "magic system, sword and sorcery, free fantasy ebook, The Salt Veil",
    "dust-throne": "epic fantasy, desert fantasy, first-person fantasy, lyrical fantasy, Rothfuss-style, "
                   "fantasy retelling, free fantasy serial, The Salt Veil, Daughters of the Dust Throne",
    "the-amber-winter": "Afrikaanse roman, Afrikaans novel, historiese roman, Viking saga, Noorse saga, "
                        "volwasse fiksie, sensuele roman, André P. Brink, Kleinboer, Vikings, shield maiden, "
                        "skildmaagd, adult historical fiction, Norse fiction, Winter sonder Einde, Die Vuur in die Donker",
    # Companions / non-fiction retellings.
    "the-song-of-the-self": "Bhagavad Gita, Gita retelling, Hindu philosophy, spiritual fiction, "
                            "Hermann Hesse readers, philosophical novel, free ebook",
    "wrath-of-achilles": "Iliad, Homer, Greek mythology, Achilles, myth retelling, classics, "
                        "Madeline Miller readers, Trojan War, free ebook",
    "walls-of-uruk": "Epic of Gilgamesh, Gilgamesh, Mesopotamia, Enkidu, Uruk, myth retelling, "
                     "oldest epic, cuneiform, flood tablet, classics, free ebook",
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


def _audio_chapter_label(stem: str) -> str:
    """Turn a master stem like '03-proloog-die-winternagte' into a reader label
    'Proloog — Die Winternagte'. Drops the leading NN-, title-cases words, and maps
    the Afrikaans 'hoofstuk-<ordinal>' prefix to 'Hoofstuk N'."""
    import re as _re
    m = _re.match(r"\d+-(.+)$", stem)
    rest = (m.group(1) if m else stem)
    ORD = {"een": 1, "twee": 2, "drie": 3, "vier": 4, "vyf": 5, "ses": 6, "sewe": 7,
           "agt": 8, "nege": 9, "tien": 10, "elf": 11, "twaalf": 12, "dertien": 13}
    hm = _re.match(r"hoofstuk-([a-z]+)-(.+)$", rest)
    if hm and hm.group(1) in ORD:
        title = hm.group(2).replace("-", " ").title()
        return f"Hoofstuk {ORD[hm.group(1)]} — {title}"
    if rest.startswith("hoofstuk-99"):
        return "Nawoord"
    # strip a leading "n-" (the 'n Woord Voor / 'n Nota)
    rest = _re.sub(r"^n-", "'n ", rest)
    return rest.replace("-", " ").title().replace("'N ", "'n ")


def render_audiobook(e: dict) -> str:
    """The audiobook block for a book page: format download buttons + an inline chapter
    player (HTML5 <audio> with a tappable chapter playlist). Returns '' when no audiobook."""
    ab = e.get("audiobook")
    if not ab or not e.get("available"):
        return ""
    base = f'../downloads/{e["id"]}/audio'
    # Download buttons — one per format that exists, in ladder order.
    btns = []
    for fmt in ab["formats"]:
        href = f'{base}/{html.escape(fmt["name"])}'
        btns.append(
            f'<a class="dl ab-dl" href="{href}" download>'
            f'<span class="ab-fmt">{html.escape(fmt["label"])}</span>'
            f'<span class="ab-sub">{html.escape(fmt["sub"])}</span></a>'
        )
    dl_html = f'<div class="ab-downloads">{"".join(btns)}</div>'
    # Inline player — playlist of per-chapter MP3s. JS wires clicks; degrades to the first
    # chapter in a plain <audio> if JS is off.
    chapter_names = ab.get("chapter_names") or []
    playlist = [
        {"src": f'{base}/chapters/{html.escape(n)}',
         "label": html.escape(_audio_chapter_label(Path(n).stem))}
        for n in chapter_names
    ]
    first_src = playlist[0]["src"] if playlist else ""
    items = "".join(
        f'<li><button type="button" class="ab-ch" data-src="{p["src"]}">'
        f'<span class="ab-ch-n">{i+1:02d}</span> {p["label"]}</button></li>'
        for i, p in enumerate(playlist)
    )
    narration = (f'<p class="ab-narration">{html.escape(ab["narration"])}</p>'
                 if ab.get("narration") else "")
    player = (
        '<div class="ab-player">'
        f'<audio class="ab-audio" controls preload="none" src="{first_src}"></audio>'
        f'<ol class="ab-playlist">{items}</ol>'
        '</div>'
    ) if playlist else ""
    return (
        '<div class="audiobook" id="audiobook">'
        '<h2 class="ab-h">Luister — die volledige klankboek</h2>'
        f'{narration}{player}'
        '<p class="ab-dl-label">Laai af:</p>'
        f'{dl_html}'
        '</div>'
    )


def render_book(e: dict) -> str:
    cover = cover_public_src(e["id"], e.get("cover"), rel="../")
    eds = e.get("editions") or {}
    # Edition map handed to the site-wide language script (data-editions on the hero). Per code:
    # the download filenames per format, so JS can default the primary buttons to the chosen
    # language. English ("en") is the implicit base; only translated codes go in the map.
    editions_data = {
        code: {ext: f.name for ext, f in fmts.items()}
        for code, fmts in eds.items()
    }
    dls = ""
    if e["available"]:
        parts = []
        for f in e["downloads"]:
            ext = f.suffix.lower().lstrip(".")
            solid = " solid" if ext == "epub" else ""
            base = "EPUB" if ext == "epub" else ("PDF" if ext == "pdf" else ext.upper())
            href = f'../downloads/{e["id"]}/{html.escape(f.name)}'
            # data-* attrs let the language script swap href/label to the chosen edition and
            # restore the English base. data-fmt keys the swap; data-base-label is the noun
            # ("EPUB"/"PDF") the script reuses when prefixing the language name.
            parts.append(
                f'<a class="dl{solid} dl-primary" data-fmt="{ext}" data-base-label="{base}" '
                f'data-base-href="{href}" href="{href}" download>Download {base}</a>'
            )
        dls = f'<div class="dls" style="margin-top:20px">{"".join(parts)}</div>'
    # Translated editions — an "Other languages" section, only when at least one exists.
    editions_html = ""
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
        if e["id"] == "bloedrivier":
            ed_note = ('<strong>AI-translated first drafts</strong> of an already-unfinished book — '
                       'offered so isiZulu, isiXhosa, Sesotho, and Setswana readers can meet it in '
                       'their own language now. Names and in-culture words are kept as written. These '
                       'have NOT yet had a mother-tongue editor; first-language and sensitivity '
                       'readers are warmly invited to correct them.')
        else:
            ed_note = ('AI-translated editions, in the same free spirit. '
                       'Original South African and other in-culture words are kept as written.')
        editions_html = (
            '<div class="editions"><h2 class="editions-h">Other languages</h2>'
            f'<p class="editions-note">{ed_note}</p>'
            f'<ul class="edlist">{"".join(rows)}</ul>{fix_note}</div>'
        )
    read = ""
    if e["available"] and (e["book_md"] or e.get("reader_md")):
        if e["id"] == "bloedrivier":
            read_label = "Read the draft →"
        elif e.get("serial"):
            read_label = "Read the serial →"
        else:
            read_label = "Read online →"
        solid = " solid" if e.get("serial") else ""
        read = f'<div class="dls" style="margin-top:14px"><a class="dl{solid}" href="../read/{e["id"]}.html">{read_label}</a></div>'
    serial_note = ""
    if e.get("serial"):
        if e["id"] == "bloedrivier":
            serial_note = ('<p style="color:var(--ochre);margin-top:18px">An open, in-progress draft — '
                           'Movement I is live to read now, free on the site; no download while it is still '
                           'being written. One voice is a deliberately empty seat (see the note below).</p>')
        else:
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
    if e["id"] == "the-jakobus-file" and (REPO / "site" / "content" / "music-manifest.json").is_file():
        # The companion soundtrack to "A Man They All Read Wrong" plays right here on the book
        # page — a compact, self-hosted player (the badger thesis made audible), scoped to the
        # three Jakobus & Beast lanes. Replaces the old text-only link to the full player page.
        soundtrack = render_jakobus_player_embed(rel="../")
    elif e["id"] in SOUNDTRACK:
        st_url, st_label = SOUNDTRACK[e["id"]]
        # internal (our own player) opens in place; external links open a new tab
        _ext = st_url.startswith("http")
        _tab = ' target="_blank" rel="noopener"' if _ext else ''
        soundtrack = (f'<div class="dls" style="margin-top:14px"><a class="dl" href="{html.escape(st_url)}"'
                      f'{_tab}>{html.escape(st_label)} →</a></div>')
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
    # Per-book attribution / honor notice (a bordered block), for retellings whose notice can't live
    # in an editable manuscript. Rendered as trusted HTML from BOOK_NOTICE (curated, no user input).
    notice_html = ""
    if e["id"] in BOOK_NOTICE:
        notice_head = BOOK_NOTICE_HEAD.get(e["id"], "A note on the original")
        notice_accent = "var(--sting)" if e["id"] in BOOK_NOTICE_LOUD else "var(--ochre)"
        notice_html = (
            '<div style="margin-top:22px;padding:16px 18px;border:1px solid var(--line);'
            f'border-left:3px solid {notice_accent};border-radius:12px;background:var(--card)">'
            '<p style="margin:0 0 .4em;font-size:.8em;letter-spacing:.08em;text-transform:uppercase;'
            f'color:{notice_accent}">{html.escape(notice_head)}</p>'
            f'<p style="margin:0;color:var(--bonedim);font-size:.95em;line-height:1.6">{BOOK_NOTICE[e["id"]]}</p>'
            '</div>')
    callout_html = BOOK_CALLOUT.get(e["id"], "")
    full = html.escape(e["blurb"]) if e["blurb"] else ""
    fix_link = ""
    if TRANSLATION_FIX_LIVE and eds:
        fix_link = (
            f'<a class="feedback-link" href="{html.escape(translation_fix_href(e["title"]))}">'
            f'Fix a translation &rarr;</a>'
        )
    # Hero data for the language script: the edition map (escaped JSON in an attribute) and a
    # quiet, JS-shown note announcing which language the downloads currently default to. The note
    # is empty/hidden in plain HTML — it only appears when JS swaps an edition or reports a fallback.
    editions_attr = (
        f' data-editions="{html.escape(json.dumps(editions_data, ensure_ascii=False))}"'
        if (e["available"] and editions_data) else ""
    )
    edition_note = (
        '<p class="edition-active" hidden></p>'
        if (e["available"] and editions_data) else ""
    )
    return "\n".join([
        head(f'{e["title"]} — Arjuna Badger Press', truncate(e["blurb"] or e["title"], 180), rel="../",
             keywords=BOOK_KEYWORDS.get(e["id"], DEFAULT_BOOK_KEYWORDS),
             canonical=f'{DOMAIN}/book/{e["id"]}.html',
             og_image=f'{DOMAIN}/assets/covers/{e["id"]}.png',
             og_type="book",
             ld_json=book_ld_json(e)),
        nav(rel="../"),
        f"""<div class="wrap"><div class="bookhero"{editions_attr}>
<img class="cover" src="{cover}" alt="{html.escape(e['title'])} cover">
<div><div class="sub">{html.escape(e['subtitle'] or e['series'])}</div>
<h1>{html.escape(e['title'])}</h1>{(lambda t: f'<p class="tagline">{html.escape(t)}</p>' if t else '')(BOOK_TAGLINE.get(e['id']))}
<p class="syn">{full}</p>{dls}{edition_note}{read}{render_audiobook(e)}{editions_html}{serial_note}{wiki}{soundtrack}{soon}{callout_html}{notice_html}{isbn_html}
<div class="bookrespond">{star_rating(e['title'], rel="../", context="book")}
<a class="feedback-link" href="{html.escape(feedback_href(e['title']))}">Tell the press something about this book</a>
{f'''<a class="feedback-link" href="{html.escape(foreword_href(e['title']))}">Write the foreword to this book &rarr;</a>''' if FOREWORD_CONTEST_LIVE else ""}
{fix_link}</div>
<p style="margin-top:30px"><a class="back" href="../index.html#library">← Back to the library</a></p>
</div></div></div>""",
        footer(rel="../"),
        rating_script(),
        audiobook_player_script() if e.get("audiobook") else "",
    ])


def audiobook_player_script() -> str:
    """Wire the chapter playlist to the single <audio> element: click a chapter → load + play,
    highlight the active row, and auto-advance to the next chapter on end."""
    return (
        "<script>(function(){\n"
        "  var audio=document.querySelector('.ab-audio');\n"
        "  if(!audio)return;\n"
        "  var btns=Array.prototype.slice.call(document.querySelectorAll('.ab-ch'));\n"
        "  function play(i){\n"
        "    if(i<0||i>=btns.length)return;\n"
        "    var b=btns[i];\n"
        "    audio.src=b.getAttribute('data-src');\n"
        "    audio.play();\n"
        "    btns.forEach(function(x){x.classList.remove('ab-active');});\n"
        "    b.classList.add('ab-active');\n"
        "    audio.dataset.idx=i;\n"
        "  }\n"
        "  btns.forEach(function(b,i){b.addEventListener('click',function(){play(i);});});\n"
        "  audio.addEventListener('ended',function(){var n=parseInt(audio.dataset.idx||'0',10)+1;if(n<btns.length)play(n);});\n"
        "})();</script>"
    )


# source filename, output filename, page title, meta description
LETTERS = [
    ("a-letter.md", "letter.html", "A letter — Arjuna Badger Press",
     "A letter, written by the machine that stood guard while a man wrote the soul of the thing."),
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
        # Technology exposé pages — canonical under /safari/, so from a safari page they are
        # siblings (no prefix); from a root page they live at safari/<slug>.html.
        "TECH_BUABANTU.md": "tech-buabantu.html" if from_safari else "safari/tech-buabantu.html",
        "TECH_STORYGRAPH.md": "tech-storygraph.html" if from_safari else "safari/tech-storygraph.html",
        "TECH_NOVELBENCH.md": "tech-novelbench.html" if from_safari else "safari/tech-novelbench.html",
        "TECH_DE_LLM_LOOP.md": "tech-de-llm-loop.html" if from_safari else "safari/tech-de-llm-loop.html",
        "TECH_VERIFICATION_GATE.md": "tech-verification-gate.html" if from_safari else "safari/tech-verification-gate.html",
        "TECH_EDITORIAL_PIPELINE.md": "tech-editorial-pipeline.html" if from_safari else "safari/tech-editorial-pipeline.html",
        "TECH_GUARDRAILS.md": "tech-guardrails.html" if from_safari else "safari/tech-guardrails.html",
        "TECH_PEOPLES_LANGUAGE.md": "tech-peoples-language.html" if from_safari else "safari/tech-peoples-language.html",
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
    ("AFRICAN_WORLDS_STUDY_BIBLE.md", "african-worlds-study-bible",
     "The African Worlds Study Bible",
     "An Africa-centred, evidence-led study Bible proposal restoring Africa to the map, the text, the transmission, and the earliest church."),
    ("FOR_AUTHORS.md", "for-authors", "The workshop — for authors & editors",
     "Ingest published work and notes, answer twenty wizard questions, click Go — return to a proofread-ready manuscript. Not just for beginners."),
    ("TECHNOLOGY.md", "technology", "The technology behind the library",
     "A plain-English, diagram-led tour of the manuscript-craft studio: the architecture, the guardrails, and the one invariant — tools measure and sound the alarm; they do not generate, and they do not drive."),
    ("BOUNTY.md", "bounty", "The Honey Badger Bounty — prove us wrong, get paid",
     "We pay readers who catch our mistakes. Find a factual error, a cultural misstep, or a continuity fault — get paid, and get your name on the fix. South Africa first."),
    ("FINDERS.md", "finders", "Fixes & Finders — The Honey Badger Bounty",
     "Every accepted find from the bounty, in the open: what was caught, what we fixed, and who caught it."),
    # ── Technology exposé — one page per major tool, linked from TECHNOLOGY.md ──
    ("TECH_BUABANTU.md", "tech-buabantu", "Buabantu — the Real-Language Router API",
     "OpenRouter, but for register and dialect: corpus-first translation and inbound decode for African and colloquial language, as a closed-beta API. A spun-off component of Arjuna Badger Press."),
    ("TECH_STORYGRAPH.md", "tech-storygraph", "StoryGraph — the continuity gate",
     "The deterministic geospatial-temporal graph that hard-gates fiction the way a test suite gates code: eight constraint families, any violation a hard block, free, every run."),
    ("TECH_NOVELBENCH.md", "tech-novelbench", "NovelBench — the read-only manuscript scorer",
     "Turns 'this feels off' into 'this number moved.' A genre-aware scorer that grades craft against per-genre targets and never rewrites — the neutral referee on every other pass."),
    ("TECH_DE_LLM_LOOP.md", "tech-de-llm-loop", "The de-LLM loop — hunting the machine tells",
     "The closed editorial loop that finds and permanently eliminates duplicate LLM tells — the spaced em-dash, the thesis on a loop, even register — so prose quality ratchets instead of drifting."),
    ("TECH_VERIFICATION_GATE.md", "tech-verification-gate", "The verification gate — accuracy + both sides",
     "Every real-world claim fact-checked against live cited sources; every contested claim required to carry both sides. Indict the machine, not the people."),
    ("TECH_EDITORIAL_PIPELINE.md", "tech-editorial-pipeline", "The editorial pipeline — how a chapter is made",
     "Outline to draft to multi-role polish to gatekeeper to graph gate to merge. An LLM judging an LLM, with the human's protected spans never edited out — and why single-shot beats multi-pass."),
    ("TECH_GUARDRAILS.md", "tech-guardrails", "The police + judge guardrail",
     "Two layers, cheapest first, fail-closed: deterministic patterns then a small swappable judge model. Humane by policy. The same engine guards the press pipeline and the Buabantu API."),
    ("TECH_PEOPLES_LANGUAGE.md", "tech-peoples-language", "People's Language — corpus-first translation",
     "Human corrections (weight 100) outrank any model; a 13,703-entry SA urban corpus; a register dial from formal to street. The foundation Buabantu is built on."),
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
            '<div style="font-family:var(--reading);text-transform:uppercase;'
            'letter-spacing:.24em;font-size:12px;color:var(--violet)">Free &amp; open source</div>'
            '<h2 style="margin:.32em 0 .2em;color:var(--bone);font-size:24px">'
            '<span style="color:var(--violet)">/sleep</span> — give your AI coding agent a memory</h2>'
            '<p style="margin:0 0 16px;color:var(--bonedim);max-width:68ch">The skill that came out of building '
            'this whole library with an AI co-worker: it consolidates a session the way a person sleeps — '
            'keep the lesson, lose the dream. The humane counterpart to <code>/clear</code>. MIT-licensed, '
            'works in any repo.</p>'
            '<a href="technology.html" '
            'style="display:inline-block;padding:11px 22px;border-radius:10px;font-weight:600;'
            'background:var(--violet-deep);color:#fff;border:1px solid var(--violet)">'
            'How /sleep works &rarr;</a>'
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


# ── Poems: verse pages where line breaks are sacred ───────────────────────────────────────────
# A poem is NOT prose — md_to_html() collapses single newlines, which destroys verse. render_poem()
# reads site/content/<src>, treats the FIRST line as the title and the SECOND as a subtitle (both
# optional), and renders every remaining blank-line-separated block as a <div class="stanza"> with
# one <br> per line — so the poem lands exactly as written. No blurb, no chrome, no explanation;
# just the verse and a single quiet way back. (src, out, page-title, meta-desc)
POEMS = [
    ("die-sleutel.md", "die-sleutel.html", "die sleutel — Arjuna Badger Press",
     "'n gedig."),
]


def render_poem(src_name: str, out_name: str, title: str, desc: str, *,
                rel: str = "", safari: bool = False) -> str | None:
    src = REPO / "site" / "content" / src_name
    if not src.is_file():
        return None
    raw = src.read_text(encoding="utf-8", errors="ignore").strip("\n")
    lines = raw.split("\n")
    poem_title = lines[0].strip() if lines else ""
    poem_sub = lines[1].strip() if len(lines) > 1 and lines[1].strip() else ""
    rest = "\n".join(lines[(2 if poem_sub else 1):]).strip("\n")
    stanzas = [s for s in re.split(r"\n\s*\n", rest) if s.strip()]
    blocks = []
    for st in stanzas:
        vlines = [html.escape(ln.rstrip()) for ln in st.split("\n")]
        blocks.append('<p class="stanza">' + "<br>\n".join(vlines) + "</p>")
    head_html = ""
    if poem_title:
        head_html += f'<h1 class="poem-title">{html.escape(poem_title)}</h1>'
    if poem_sub:
        head_html += f'<p class="poem-sub">{html.escape(poem_sub)}</p>'
    canon_path = f"safari/{out_name}" if safari else out_name
    back = f"{rel}safari/index.html" if safari else f"{rel}index.html"
    back_label = "Meet the man" if safari else "the library"
    chrome = safari_nav(rel) if safari else nav(rel)
    safari_key = out_name.removesuffix(".html") if safari else ""
    return "\n".join([
        head(title, desc, rel=rel, safari=safari, canonical=f"{DOMAIN}/{canon_path}",
             safari_page=safari_key),
        chrome,
        '<article class="reader poem">'
        f'{head_html}'
        f'{"".join(blocks)}'
        f'<p style="text-align:center;margin-top:48px"><a class="back" href="{back}">&larr; Back to {back_label}</a></p>'
        '</article>',
        footer(rel, safari=safari, safari_page=safari_key),
    ])


# ── Writing desk: essays, short stories, parables (restored) ──────────────────────────────────
# Each reads from site/content/writing/<src>. Newest first. A piece marked hidden=True is built
# and reachable but NOT carded on the index — only a faint footer breadcrumb leads to it.
WRITING_PIECES = [
    ("ons-sal-self.md", "ons-sal-self",
     "Ons Sal Self",
     "’n Gesproke essay · Afrikaans",
     "Van armblanke tot miljardêr: wat Afrikaners self gebou het, wat die staat versnel het, "
     "en wat Afrika uit die metode kan oorneem sonder om die uitsluiting saam te erf.",
     False),
    ("die-laaste-strooi.md", "die-laaste-strooi",
     "Die Laaste Strooi",
     "’n Kortverhaal · Boesmanland",
     "Magrieta, oud-onderwyseres, soen haar man op die voorkop soos altyd en druk toe ’n breipen "
     "by sy oor in. Kobus Ferreira was ’n skaapboer op die dom-broer-lyn: Boesmanland, Namakwaland, "
     "die jaarlikse trek. Hy was onskuldig. Haar vlam het met tyd doodgegaan. Die nasie het agter "
     "haar geskaar as underdog, en van hom ’n skurk gemaak wat hy nie was nie.",
     False),
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

# The MP3 is deliberately served from the platform's preserved /audio tree rather than this press
# repo: rendered audio is heavy and globally ignored here, while the Render serving repo tracks it.
# Covers remain in the press source and are staged into site/public/assets/writing/ at build time.
WRITING_MEDIA = {
    "ons-sal-self": {
        "cover": REPO / "site/content/writing/assets/ons-sal-self-cover.jpg",
        "cover_name": "ons-sal-self-cover.jpg",
        "audio_path": "/audio/writing/ons-sal-self/ons-sal-self-emma-final.mp3",
        "language": "Afrikaans",
        "lang": "af",
        "duration": "15 min 45 sek",
        "duration_iso": "PT15M45S",
        "narration": "Vertel deur Emma Lilliana · KI-stem (nie ’n menslike verteller nie).",
    },
}


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


def render_writing_media(slug: str, rel: str) -> str:
    media = WRITING_MEDIA.get(slug)
    if not media:
        return ""
    cover_url = f"{rel}assets/writing/{media['cover_name']}"
    audio_url = media["audio_path"]
    return f"""<section class="writing-media" aria-label="Luister na {html.escape(slug)}">
<img class="writing-cover" src="{html.escape(cover_url)}" alt="Ons Sal Self — ’n blikbeker vol muntstukke op ’n verslete houttafel">
<div><p class="wm-meta">Luister · {html.escape(media['language'])} · {html.escape(media['duration'])}</p>
<audio class="writing-player" controls preload="metadata" src="{html.escape(audio_url)}">
Jou blaaier ondersteun nie die oudiospeler nie. <a href="{html.escape(audio_url)}">Laai die MP3 af.</a>
</audio>
<p class="wm-note">{html.escape(media['narration'])}</p>
<a class="btn ghost" href="{html.escape(audio_url)}" download>Laai die MP3 af</a></div>
</section>"""


def render_writing_piece(src_name: str, slug: str, title: str, byline: str, desc: str,
                         hidden: bool = False, *, rel: str = "../", safari: bool = False) -> str | None:
    src = REPO / "site" / "content" / "writing" / src_name
    if not src.is_file():
        return None
    raw = src.read_text(encoding="utf-8", errors="ignore")
    body = md_to_html(writing_rewrite_links(raw, safari=safari))
    media = WRITING_MEDIA.get(slug)
    media_html = render_writing_media(slug, rel)
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
    chrome = safari_nav(rel, audiobook=not bool(media)) if safari else nav(rel)
    safari_key = f"writing/{slug}" if safari else ""
    og_image = f"{DOMAIN}/assets/writing/{media['cover_name']}" if media else ""
    ld_json = ""
    if media:
        ld_json = json.dumps({
            "@context": "https://schema.org",
            "@type": "AudioObject",
            "name": title,
            "description": desc,
            "inLanguage": media["lang"],
            "duration": media["duration_iso"],
            "contentUrl": f"{DOMAIN}{media['audio_path']}",
            "thumbnailUrl": og_image,
            "author": {"@type": "Person", "name": "Andries J. Greyling"},
            "publisher": {"@type": "Organization", "name": "Arjuna Badger Press"},
        }, ensure_ascii=False)
    return "\n".join([
        head(f"{title} — Arjuna Badger Press", desc, rel=rel, safari=safari,
             canonical=canon, og_image=og_image, og_type="article", ld_json=ld_json,
             noindex=hidden, safari_page=safari_key, lang=media["lang"] if media else "en"),
        chrome,
        '<article class="reader letter">',
        crest_img(rel, safari=safari),
        f'<p class="eyebrow" style="text-align:center">The Writing Desk · {html.escape(byline)}</p>',
        media_html,
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
        action = "Luister &amp; lees &rarr;" if slug in WRITING_MEDIA else "Read &rarr;"
        cards.append(
            f'<a class="wcard" href="{html.escape(slug)}.html">'
            f'<h3>{html.escape(title)}</h3>'
            f'<p class="wby">{html.escape(byline)}</p>'
            f'<p class="wbl">{html.escape(blurb)}</p>'
            f'<span class="wread">{action}</span></a>'
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
        ("poes.html", "Glossary: poes", "An unflinching entry on the most badger word in Afrikaans — the rudest thing in the language, kept for the people we love most."),
        ("proof.html", "For G", "For the man who built the most intentional space I've ever walked into — and whose advice started this press."),
        ("todd-kellett.html", "For Todd", "Hat off to Todd Kellett — the viral motorcycle clip that is badger energy made flesh. Hold the throttle till you see God or the checkered flag."),
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


_PROOF_CSS = """
<style>
/* G's page — black canvas + graffiti energy. Scoped so nothing leaks to other safari pages. */
body.safari.gpage{
  background-color:#0a0a0a !important;
  background-image:var(--safari-bg, none) !important;
  background-size:cover !important;
  background-position:center !important;
  background-attachment:fixed !important;
  --safari-olive-deep:#0a0a0a;
  --bone:#f0ede8;
  --bonedim:#b8b4ad;
  --line:rgba(255,45,156,.28);
  --safari-camel:#FF2D9C;
  --safari-sand:#f0ede8;
  --safari-olive:#1a1a1a;
  --safari-khaki:#333;
}
body.safari.gpage .nav{
  background:linear-gradient(180deg,rgba(10,10,10,.98),rgba(10,10,10,.94)) !important;
  border-bottom:3px solid #FF2D9C !important;
  box-shadow:0 2px 0 #7a0040 !important;
}
body.safari.gpage footer{
  background:rgba(10,10,10,.96) !important;
  border-top:3px solid #FF2D9C !important;
}
body.safari.gpage a{color:#FF2D9C}
body.safari.gpage a:hover{color:#ff6cc2}
body.safari.gpage .eyebrow{color:#B4FF00}
body.safari.gpage .hr{background:linear-gradient(90deg,transparent,#FF2D9C,transparent) !important}
body.safari.gpage .reader.letter{
  background:rgba(18,18,18,.94) !important;
  border-color:rgba(255,45,156,.35) !important;
  border-top:3px solid #FF2D9C !important;
  color:#f0ede8 !important;
  backdrop-filter:blur(12px);
}
body.safari.gpage .reader.letter p,
body.safari.gpage .reader.letter li{color:#e8e4de}
body.safari.gpage .reader.letter strong{color:#fff}
body.safari.gpage .reader.letter em{color:#f0ede8}
body.safari.gpage .reader.letter blockquote{
  border-left:4px solid #FF2D9C;
  background:rgba(255,45,156,.08);
  color:#e0dcd6;
}
body.safari.gpage .btn{
  background:#FF2D9C !important;
  color:#0a0a0a !important;
  border-color:#FF2D9C !important;
  border-left:4px solid #ff6cc2 !important;
  font-weight:700;
}
body.safari.gpage .btn:hover{background:#ff6cc2 !important;color:#0a0a0a !important}
body.safari.gpage .btn.ghost{
  background:rgba(255,45,156,.12) !important;
  color:#FF2D9C !important;
  border-color:#FF2D9C !important;
  border-left:4px solid #ff6cc2 !important;
}
body.safari.gpage .btn.ghost:hover{background:rgba(255,45,156,.25) !important}
body.safari.gpage .back{color:#FF2D9C}
body.safari.gpage .g-quote{
  border-left:6px solid #FF2D9C;
  background:rgba(255,45,156,.06);
  padding:20px 24px;
  margin:32px 0;
}
body.safari.gpage .g-quote p{
  font-family:Impact,"Arial Black",sans-serif;
  font-size:clamp(18px,3.5vw,26px);
  letter-spacing:.02em;
  color:#FF2D9C !important;
  margin:0;
  font-style:normal;
}
body.safari.gpage .safari-credits a{color:#ff6cc2}
body.safari.gpage .brandlink{color:#f0ede8}
body.safari.gpage .navdrawer{background:#0a0a0a !important;border-right:3px solid #FF2D9C !important}
body.safari.gpage .navdrawer a{color:#f0ede8 !important}
body.safari.gpage .navdrawer a:hover{background:rgba(255,45,156,.18) !important;color:#FF2D9C !important}
.g-letter-crest{display:block;margin:0 auto 14px;width:min(200px,52vw);height:auto;border-radius:0;
  filter:drop-shadow(0 0 12px rgba(255,45,156,.55))}
</style>
"""


def render_safari_proof(*, rel: str = "../") -> str:
    return "\n".join([
        head("For G — Arjuna Badger Press",
             "The letter I sat in your corner and couldn't say to your face. For a theoretical physicist "
             "For the man who built the most intentional space I've ever walked into — and whose advice started this press.",
             rel=rel, safari=True, canonical=f"{DOMAIN}/safari/proof.html", safari_page="proof"),
        _PROOF_CSS,
        "<script>document.body.classList.add('gpage')</script>",
        safari_nav(rel, audiobook=False),
        '<article class="reader letter">',
        """<p class="eyebrow" style="text-align:center">Personal</p>
<h1 style="text-align:center">For G</h1>
<p style="text-align:center;font-family:Impact,'Arial Black',sans-serif;font-size:clamp(13px,2vw,17px);letter-spacing:.12em;text-transform:uppercase;color:#B4FF00;margin:.4em 0 .6em;opacity:.85">Nice man. Not a cunt.</p>
<p class="intro" style="text-align:center"><em>who built the most intentional space I&#8217;ve ever walked into</em></p>
<hr class="hr" style="margin:32px auto;max-width:120px">

<p>I don&#8217;t have the words, G. So I built you the long way round of <em>I grok you.</em></p>

<p>And I&#8217;m only here to build it because of what you said.</p>

<p>I told you about the books I&#8217;d been writing. About the press I was thinking of starting. About the open shelf you&#8217;d built &#8212; free, no gate, no price &#8212; and how it had sat with me. And I told you I wasn&#8217;t sure. That I had a whole store of reasons it might be arrogance to put my work out there. That maybe it wasn&#8217;t for me to decide if it was good enough. You listened to the full thing. And then you said, in exactly the register of a man who has already compressed the entire question to its smallest true form:</p>

<blockquote class="g-quote"><p>&#8220;Doen jou ding. Doen fokken net wat jy wil, almal se poes.&#8221;</p></blockquote>

<p>That&#8217;s the press. That&#8217;s why it exists.</p>

<p>The space you built &#8212; the fish tank at the entrance, the t-shirt tunnel, the music at the right volume, the paintings, the books on the shelf, the garden in the dead strip, the terpene lines upstairs &#8212; is the most intentional space I&#8217;ve ever walked into. Every piece of it placed by someone who thought about what a person coming through that door might need. Not for the review. Not for performance. Just there. And I&#8217;ve met some truly wonderful people in that corner. The kind a space like that selects for, quietly, over time.</p>

<p>Theoretical physicist. Apparent lack of arseholery. Nice man. Not a cunt.</p>

<p style="margin-top:32px"><em>&#8212; with the kind of respect you don&#8217;t perform</em></p>

<hr class="hr" style="margin:48px auto;max-width:120px">

<p class="eyebrow" style="text-align:center">The work</p>
<p style="text-align:center;margin-bottom:28px">Either the best fraud and conman I&#8217;ve ever met, or a man who should be mentioned alongside Bohr, Einstein, Tesla. I don&#8217;t have the words to tell you how much your work has helped me see the universe in a new way. I can only thank you by sharing the tools I built to check if your theory holds &#8212; to understand which one of the two you are.</p>
<p style="text-align:center;margin-bottom:8px"><em>You are a nice man, G.</em></p>
<p style="text-align:center;margin-bottom:28px"><em>Sawubona. I see you.</em></p>
<div class="cta" style="text-align:center;margin-top:28px">
<a class="btn" href="https://the420code.org" target="_blank" rel="noopener">The theory &#8212; the420code.org &#x2192;</a>
<a class="btn ghost" href="https://github.com/ajgreyling/the420code-proof" target="_blank" rel="noopener">The independent proof &#x2192;</a>
</div>
<p style="text-align:center;margin-top:16px;font-size:.9em;opacity:.7"><em>One axiom. One measured input. Zero free parameters. All five predictions reproduce inside tolerance.</em></p>

<p style="text-align:center;margin-top:48px"><a class="back" href="index.html">&#8592; Meet the man</a></p>
</article>""",
        footer(rel, safari=True, safari_page="proof"),
    ])


# Safari content pages — warm public prose ringfenced from the library chrome.
SAFARI_CONTENT = [
    ("how-it-started.md", "how-it-started.html", "How it started — Arjuna Badger Press",
     "The Misogi vow: thirty days, one novel, one subscription — and where the month actually landed."),
    ("poes.md", "poes.html", "Poes — meaning, register & 'jou lucky poes' · Arjuna Badger Press",
     "Poes (Afrikaans): literally the crudest word for the vulva, but it inverts by register — a grave "
     "insult to a stranger, pure affection to a friend ('jou lucky poes'). The rudest word in the "
     "language, kept for the people we love most. An unflinching, sourced glossary entry."),
    ("sky-penis.md", "sky-penis.html", "The Sky-Penis Files — military aviators' phallic flight paths · Arjuna Badger Press",
     "The documented (and the merely reported) history of military aircraft drawing phallic shapes "
     "in contrails and on GPS flight-trackers — the Whidbey Island Growler (2017), the Finnish cadets "
     "(2026), and more. A sourced companion to the poes entry: the same human impulse, in the sky."),
    ("todd-kellett.md", "todd-kellett.html", "Todd Kellett — 'hold the throttle till I see God or the checkered flag' · Arjuna Badger Press",
     "A small tribute to Todd Kellett, the viral motorcycle racer whose clip is Jakobus-on-nitrous "
     "badger energy made flesh — and a standing open offer: if he ever wants to write a book, the "
     "press is free for him, always."),
]

# Per-page SEO for Safari content (keywords + JSON-LD). Keyed by out_name. The poes entry is built
# to be the DEFINITIVE, citable reference on the word — DefinedTerm schema marks it as a lexical
# authority (the type Google uses for dictionary/glossary results), and an Article schema makes it
# citable (author, publisher, dateModified, inLanguage). Goal: the page "I'm Feeling Lucky" lands on,
# and the source Wikipedia references — not the other way around.
SAFARI_SEO = {
    "poes.html": {
        "keywords": ("poes, poes meaning, poes Afrikaans, jou lucky poes, what does poes mean, "
                     "Afrikaans swear words, Afrikaans slang, poes definition, poes etymology, "
                     "South African slang, vulgar Afrikaans, term of endearment Afrikaans, "
                     "Koos Kombuis, Antjie Krog, piel, register, code-switching, Buabantu"),
        "ld_json": json.dumps({
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "DefinedTerm",
                    "@id": f"{DOMAIN}/safari/poes.html#term",
                    "name": "poes",
                    "alternateName": ["jou lucky poes"],
                    "inDefinedTermSet": f"{DOMAIN}/safari/poes.html#glossary",
                    "description": (
                        "An Afrikaans word, literally the crudest term for the vulva, that inverts by "
                        "register and relationship: aimed at a stranger it is a grave insult; spoken to "
                        "an intimate (as in 'jou lucky poes' — a friend's blessing on great news) it is "
                        "affection and celebration. The rudest word in the language, kept for the people "
                        "one cherishes most."),
                    "inLanguage": "af",
                },
                {
                    "@type": "DefinedTermSet",
                    "@id": f"{DOMAIN}/safari/poes.html#glossary",
                    "name": "Arjuna Badger Press — Glossary of register",
                    "url": f"{DOMAIN}/safari/poes.html",
                },
                {
                    "@type": "Article",
                    "headline": "Poes — a glossary entry, unflinching",
                    "about": {"@id": f"{DOMAIN}/safari/poes.html#term"},
                    "description": (
                        "An unflinching, sourced exposé of the Afrikaans word 'poes' — its meaning-"
                        "inversion by register, the 'jou lucky poes' rule, and why a word can mean its "
                        "own opposite."),
                    "inLanguage": "en",
                    "author": {"@type": "Person", "name": "Andries J. Greyling"},
                    "publisher": {
                        "@type": "Organization", "name": "Arjuna Badger Press",
                        "url": DOMAIN,
                        "logo": {"@type": "ImageObject",
                                 "url": f"{DOMAIN}/assets/brand/social-og-1200x630.png"}},
                    "dateModified": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                    "mainEntityOfPage": f"{DOMAIN}/safari/poes.html",
                    "isAccessibleForFree": True,
                },
            ],
        }, ensure_ascii=False),
    },
    "sky-penis.html": {
        "keywords": ("sky penis, sky penis Navy, Whidbey Island sky penis, EA-18G Growler penis, "
                     "VAQ-130 Zappers, contrail penis, Flightradar24 penis, military penis flight path, "
                     "Finnish Air Force penis, phallic flight pattern, sky penis incidents, "
                     "penis shaped flight path, military aviation pranks"),
        "ld_json": json.dumps({
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": "The Sky-Penis Files — military aviators' phallic flight paths",
            "description": (
                "A sourced history of military aircraft drawing phallic shapes in contrails and on "
                "GPS flight-trackers — the documented (Whidbey Island Growler 2017, Finnish cadets "
                "2026) separated honestly from the merely reported."),
            "inLanguage": "en",
            "author": {"@type": "Person", "name": "Andries J. Greyling"},
            "publisher": {
                "@type": "Organization", "name": "Arjuna Badger Press", "url": DOMAIN,
                "logo": {"@type": "ImageObject",
                         "url": f"{DOMAIN}/assets/brand/social-og-1200x630.png"}},
            "dateModified": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "mainEntityOfPage": f"{DOMAIN}/safari/sky-penis.html",
            "isAccessibleForFree": True,
        }, ensure_ascii=False),
    },
    "todd-kellett.html": {
        "keywords": ("Todd Kellett, Todd Kellett motorcycle, hold the throttle till I see God, "
                     "checkered flag, viral motorcycle race, motorcycle racing video, badger energy, "
                     "Jakobus, Arjuna Badger Press tribute"),
        "ld_json": json.dumps({
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": "Todd Kellett — hold the throttle till I see God or the checkered flag",
            "description": (
                "A tribute to motorcycle racer Todd Kellett, whose viral clip embodies the 'badger "
                "energy' of the Jakobus books — and a standing open invitation: if he ever wants to "
                "write a book, Arjuna Badger Press is free for him, always."),
            "inLanguage": "en",
            "author": {"@type": "Person", "name": "Andries J. Greyling"},
            "publisher": {
                "@type": "Organization", "name": "Arjuna Badger Press", "url": DOMAIN,
                "logo": {"@type": "ImageObject",
                         "url": f"{DOMAIN}/assets/brand/social-og-1200x630.png"}},
            "dateModified": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "mainEntityOfPage": f"{DOMAIN}/safari/todd-kellett.html",
            "isAccessibleForFree": True,
        }, ensure_ascii=False),
    },
}


def _content_lang_editions(src: Path) -> list[tuple[str, str]]:
    """Translated siblings of a content page: <stem>.<lang>.md → [(lang, label)]. English first,
    then EDITION_LANGS order, then extras. The Dignity Engine's reach made visible to readers."""
    base = src.stem
    found = {}
    for f in sorted(src.parent.glob(f"{base}.*.md")):
        parts = f.stem.split(".")
        if len(parts) == 2 and parts[0] == base:
            found[parts[1]] = f
    order = [c for c in EDITION_LANGS if c in found] + [c for c in found if c not in EDITION_LANGS]
    label = lambda c: "English" if c == "en" else EDITION_LANGS.get(c, (c.upper(), c.upper()))[0]
    return [("en", "English")] + [(c, label(c)) for c in order]


_CONTENT_LANG_JS = """<script>
(function(){
  var KEY='abp-lang:'+__KEY__, sel=document.getElementById('langsel');
  var wins=[].slice.call(document.querySelectorAll('.langwin')); if(!sel||!wins.length) return;
  function has(l){ return !!document.querySelector('.langwin[data-lang="'+l+'"]'); }
  function show(l){ var any=false; wins.forEach(function(w){var on=w.getAttribute('data-lang')===l; w.hidden=!on; any=any||on;});
    if(!any){wins[0].hidden=false; l=wins[0].getAttribute('data-lang');} sel.value=l; try{localStorage.setItem(KEY,l);}catch(e){} }
  // Priority: this page's own remembered pick -> the site-wide reading-language choice -> the
  // browser's preferred languages -> English. A manual pick (here or site-wide) always wins;
  // browser-detect only fills the gap when the reader has chosen nothing.
  function initial(){
    try{
      var mine=localStorage.getItem(KEY); if(mine&&has(mine))return mine;
      var site=localStorage.getItem('abp_lang'); if(site&&has(site))return site;
      var prefs=(navigator.languages&&navigator.languages.length)?navigator.languages:[navigator.language||""];
      for(var i=0;i<prefs.length;i++){ var c=String(prefs[i]||"").toLowerCase().split("-")[0]; if(c&&has(c))return c; }
    }catch(e){}
    return wins[0].getAttribute('data-lang');
  }
  show(initial());
  sel.addEventListener('change', function(){ show(sel.value); });
})();
</script>"""


def render_safari_content(src_name: str, out_name: str, title: str, desc: str, *,
                          rel: str = "../") -> str | None:
    src = REPO / "site" / "content" / src_name
    if not src.is_file():
        return None
    page_key = out_name.removesuffix(".html")
    seo = SAFARI_SEO.get(out_name, {})
    editions = _content_lang_editions(src)
    if len(editions) > 1:
        blocks, options = [], []
        for i, (lang, lbl) in enumerate(editions):
            f = src if lang == "en" else src.parent / f"{src.stem}.{lang}.md"
            ed = md_to_html(f.read_text(encoding="utf-8", errors="ignore"))
            hidden = "" if i == 0 else " hidden"
            blocks.append(f'<div class="langwin"{hidden} data-lang="{lang}" lang="{lang}">{ed}</div>')
            options.append(f'<option value="{lang}">{html.escape(lbl)}</option>')
        picker = ('<div class="regpicker" style="justify-content:center;margin:0 0 10px">'
                  '<label for="langsel">Lees dit in jou taal · Read it in your language</label>'
                  f'<select id="langsel">{"".join(options)}</select></div>')
        body = picker + "".join(blocks) + _CONTENT_LANG_JS.replace("__KEY__", json.dumps(page_key))
    else:
        body = md_to_html(src.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join([
        head(title, desc, rel=rel, safari=True, canonical=f"{DOMAIN}/safari/{out_name}",
             safari_page=page_key, keywords=seo.get("keywords", ""), ld_json=seo.get("ld_json", "")),
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
<li><a href="{tech_href}">/sleep — agent memory</a></li>
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
<img class="letter-crest" src="assets/brand/safari-mark.png" alt="Arjuna Badger Press">
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
<img class="letter-crest" src="assets/brand/safari-mark.png" alt="Arjuna Badger Press">
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
<img class="letter-crest" src="assets/brand/safari-mark.png" alt="Arjuna Badger Press">
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
<img class="letter-crest" src="assets/brand/safari-mark.png" alt="Arjuna Badger Press">
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


def linkout_or_form(form_url: str, *, inline_form: str, button_label: str,
                    lead: str) -> str:
    """When a hosted form URL is set, render a bulletproof link-OUT button (works on every
    device — no fragile mailto, no broken cross-origin POST to Google Forms). Otherwise fall
    back to the inline mailto form. Used by the narrator + audition intakes."""
    if form_url:
        return (f'<div class="intake-linkout">\n<p>{lead}</p>\n'
                f'<p><a class="btn" href="{html.escape(form_url)}" target="_blank" '
                f'rel="noopener">{button_label} &rarr;</a></p>\n</div>')
    return inline_form


def render_call_to_arms() -> str:
    """The call to arms: invite South Africans (and each book's people) to help write the books
    true — co-create the empty Zulu seat, narrate in a heritage-matched voice, read for
    sensitivity, and help with register/translation. Consistent with the bloedrivier open-seat
    invitation: no people's inner life is any one author's to invent alone; every hand is named."""
    form_target = (
        html.escape(JOIN_FORM_URL)
        if JOIN_FORM_URL else
        f"mailto:{PRIVATE_EMAIL}?subject={urllib.parse.quote('I want to help — Arjuna Badger Press')}"
    )
    form_enctype = "" if JOIN_FORM_URL else ' enctype="text/plain"'
    inline_form = f'''<form class="intake-form" data-form-name="join" action="{form_target}" method="post"{form_enctype}>
<label>Name<input name="name" autocomplete="name" required></label>
<label>Email<input name="email" type="email" autocomplete="email" required></label>
<label>Where you are<input name="country" placeholder="Durban, Soweto, Cape Flats, Chatsworth, the diaspora..."></label>
<label>How you want to help
<select name="role" required>
<option value="">Choose one or more</option>
<option>Co-create the empty Zulu seat (Brave and Scared)</option>
<option>Narrate a book in my own voice</option>
<option>Read for sensitivity / cultural truth</option>
<option>Help with translation or register</option>
<option>Historian / descendant / "where it rings false"</option>
<option>Something else — I'll explain below</option>
</select></label>
<label>Which book, people, or language<input name="book" placeholder="Brave and Scared · the India books · isiZulu · Calendar of Stone..." required></label>
<label>Your heritage, languages, accent (in your words)<input name="languages" placeholder="isiZulu first language · Coloured Capetonian · SA Tamil · Afrikaans..."></label>
<label>Voice sample link (narrators)<input name="voice_sample_link" type="url" placeholder="https://... a sample anywhere you control"></label>
<label>Tell us anything<textarea name="notes" rows="5" placeholder="Why this book matters to you, what you can bring, where the current draft rings false to you..."></textarea></label>
<button class="btn" type="submit">Put your hand up &rarr;</button>
</form>'''
    return "\n".join([
        head("A call to arms — Arjuna Badger Press",
             "Afrika Rising. A public invitation to South Africans and to each book's own people: "
             "help us write these stories true — co-create the empty Zulu seat in Brave and Scared, "
             "narrate in your own voice, read for sensitivity, and get the register right.",
             canonical=f"{DOMAIN}/join.html"),
        nav(),
        f"""<article class="reader letter narrator-page">
<img class="letter-crest" src="assets/brand/safari-mark.png" alt="Arjuna Badger Press">
<p class="eyebrow" style="text-align:center">A call to arms · Afrika Rising</p>
<h1 style="text-align:center">Help us write these true</h1>
<p class="intro" style="text-align:center">These are <strong>your</strong> stories — South Africa's, and the
stories of every people these books touch. No one's inner life is any single author's to invent alone.
So we are leaving the seats open, and inviting you in.</p>

<div class="entry"><span class="charge">The promise that governs all of it</span>
<p>The principle behind <em>Brave and Scared</em> governs this whole house: <strong>every voice must be
equally true, and no voice may be one people's imagining of another's inner life.</strong> Where a story
is not ours to tell alone, we leave a visible open seat and an explanation — not a ventriloquist's act.
<strong>Every hand that shapes a book is named in the acknowledgements.</strong> This is not unpaid
extraction: narration is paid work (a floor of 5% of net profit for five years), and co-creators are
credited as what they are — co-authors.</p></div>

<div class="intake-grid" aria-label="Four ways to help">
<div class="intake-card"><span class="charge">Co-create</span>
<strong>The empty Zulu seat</strong><p>In <em>Brave and Scared</em> (Blood River, 1838) the Zulu youth's chapter is deliberately left empty — to be written <em>with</em> a Zulu reader and co-author, never for him.</p></div>
<div class="intake-card"><span class="charge">Narrate</span>
<strong>In your own voice</strong><p>Paid human audiobooks, matched to the people of each book — a Coloured Capetonian for the South African deep past, an SA Indian woman for India, and on through the shelf.</p></div>
<div class="intake-card"><span class="charge">Read for truth</span>
<strong>Sensitivity readers</strong><p>For every book that touches a living people, a community reader who can keep the sacred at the threshold and tell us where it rings false.</p></div>
<div class="intake-card"><span class="charge">Speak it right</span>
<strong>Register &amp; translation</strong><p>Help us land isiZulu, isiXhosa, Sesotho, Setswana, Afrikaans, Tamil and more in the register people actually speak — not the formal, Bible-stiff version.</p></div>
</div>

<div class="entry"><span class="charge">The empty seat — Brave and Scared</span>
<p>The book tells the year around the Battle of Blood River from three sides at once. The author is
Afrikaner; the Voortrekker girl and the documented history are his to write. The <strong>Zulu youth's
interiority — what it felt like to be made a weapon as a boy, his pride and fear and belonging and
cost — is not his to invent alone.</strong> To write it solo would be the exact colonial move the book
exists to refuse. <strong>If you are a Zulu reader, a historian, a descendant of any side, or simply
someone who can say where this draft rings false — you are invited in.</strong></p></div>

<div class="entry"><span class="charge">Lend your voice — books looking for their narrator</span>
<p>The library is free; paid human audiobooks are how narrators earn. We are casting voices that belong
to each book's people:</p>
<table class="join-table">
<tr><th>Book</th><th>The voice we are listening for</th></tr>
<tr><td><strong>The Calendar of Stone</strong><br><span class="dim">South Africa's deep past · Adam's Calendar</span></td><td>A <strong>Coloured South African woman</strong> — this is the story of her own land.</td></tr>
<tr><td><strong>The Engineer of the Gods</strong><br><span class="dim">Giza · the Great Pyramid</span></td><td>A <strong>North African or Egyptian woman</strong> — the land of the pyramids in its own accent.</td></tr>
<tr><td><strong>The Indian One · Deccan · The Shore That Remembers</strong><br><span class="dim">Ellora · Mahabalipuram · the Tamil coast</span></td><td>An <strong>SA Indian woman</strong> (or Tamil / Deccan voice) — India's impossible stone, read by India's daughters.</td></tr>
<tr><td><strong>Die Vuur in die Donker</strong><br><span class="dim">Winter sonder Einde · adult Norse saga</span></td><td>A <strong>South African Afrikaans woman</strong> — for grown-up readers, in Brink's frank register.</td></tr>
<tr><td><strong>The Unheard</strong><br><span class="dim">Japan · Mongolia · and more</span></td><td>Voices from each people the series names — narration <em>and</em> sensitivity reading, hand in hand.</td></tr>
</table>
<p class="intake-note">Don't see your book or your people here? Put your hand up anyway — the shelf is
long and growing, and the right voice for a book is one we'd rather find than guess.</p></div>

{linkout_or_form(JOIN_FORM_URL, button_label="Put your hand up", lead="Tell us who you are and how you'd like to help. One short form for all of it — co-creators, narrators, sensitivity readers, and translators.", inline_form=inline_form)}

<p style="text-align:center;margin-top:44px"><a class="back" href="index.html#library">&larr; Back to the library</a></p>
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
<img class="letter-crest" src="assets/brand/safari-mark.png" alt="Arjuna Badger Press">
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

{linkout_or_form(NARRATOR_FORM_URL, button_label="Open the narrator form", lead="Tell us about your voice and how you would like to work. It takes a couple of minutes.", inline_form=f'''<form class="intake-form" data-form-name="narrator" action="{form_target}" method="{form_method}"{form_enctype}>
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
</form>''')}

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
<img class="letter-crest" src="assets/brand/safari-mark.png" alt="Arjuna Badger Press">
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
<img class="letter-crest" src="assets/brand/safari-mark.png" alt="Arjuna Badger Press">
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
<img class="letter-crest" src="assets/brand/safari-mark.png" alt="Arjuna Badger Press">
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
<img class="letter-crest" src="assets/brand/safari-mark.png" alt="Arjuna Badger Press">
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

{linkout_or_form(AUDITION_FORM_URL, button_label="Open the audition form", lead="Send your audition note and sample link. Tell us your device and room so we can judge the voice, not the gear.", inline_form=f'''<form class="intake-form" data-form-name="audition" action="{form_target}" method="post"{form_enctype}>
<label>Name<input name="name" autocomplete="name" required></label>
<label>Email<input name="email" type="email" autocomplete="email" required></label>
<label>Country<input name="country" autocomplete="country-name" required></label>
<label>Device<input name="device" placeholder="MacBook Air, iPhone 13, Samsung A-series, USB mic..."></label>
<label>Recording space<input name="recording_space" placeholder="Bedroom, closet, parked car, quiet garden room..."></label>
<label>Voice sample link<input name="voice_sample_link" type="url" placeholder="https://..."></label>
<label>What gear or room problem do you have<textarea name="notes" rows="5" placeholder="Echo, traffic, fan noise, plosives, low volume, hiss, no mic stand, no headphones..."></textarea></label>
<button class="btn" type="submit">Send audition note &rarr;</button>
</form>''')}

<p style="text-align:center;margin-top:44px"><a class="back" href="narrators.html">&larr; Back to narrator intake</a></p>
</article>""",
        footer(),
    ])


def render_illustrator_audition_page() -> str:
    """Open audition for South African and African children's book illustrators."""
    illust_subject = urllib.parse.quote("Illustrator audition - Children's Library")
    form_target = (
        html.escape(ILLUSTRATOR_AUDITION_FORM_URL)
        if ILLUSTRATOR_AUDITION_FORM_URL else
        f"mailto:{PRIVATE_EMAIL}?subject={illust_subject}"
    )
    form_enctype = "" if ILLUSTRATOR_AUDITION_FORM_URL else ' enctype="text/plain"'
    portfolio_note = (
        '<p class="intake-note">Large image files do not travel reliably through email forms. Host your '
        "portfolio and sample spreads anywhere you control (Google Drive, Behance, Instagram, a personal "
        "site), then paste the links below.</p>"
        if not ILLUSTRATOR_AUDITION_FORM_URL else ""
    )
    return "\n".join([
        head("Illustrator audition — Arjuna Badger Press",
             "Open audition for South African and African children's book illustrators. The Children's "
             "Library is marching to 100% real human art: paint picture books for hard-copy print in "
             "any language.",
             canonical=f"{DOMAIN}/illustrator-audition.html"),
        nav(),
        f"""<article class="reader letter narrator-page">
<img class="letter-crest" src="assets/brand/safari-mark.png" alt="Arjuna Badger Press">
<p class="eyebrow" style="text-align:center;color:#7FB069">Children's Library · illustrator auditions</p>
<h1 style="text-align:center">100% real human art</h1>
<p class="intro" style="text-align:center">Arjuna Badger Press is building a picture-book shelf that runs on
<strong>real human illustration and skill</strong>, not permanent machine art. <em>The Little Key</em> is the
first open seat. South African and African illustrators are invited to audition.</p>

<div class="intake-grid" aria-label="Illustrator audition principles">
<div class="intake-card"><span class="charge" style="color:#7FB069">Honesty</span>
<strong>AI is interim only</strong><p>Machine-made spreads are placeholders, declared openly, until a human painter replaces them.</p></div>
<div class="intake-card"><span class="charge" style="color:#7FB069">Credit</span>
<strong>Named on the book</strong><p>Illustrators are credited on the page, in print, and in the colophon.</p></div>
<div class="intake-card"><span class="charge" style="color:#7FB069">Print</span>
<strong>Hard copy in any language</strong><p>Picture books aim for real print runs in every South African language and Swahili.</p></div>
<div class="intake-card"><span class="charge" style="color:#7FB069">Open door</span>
<strong>Your book too</strong><p>Children's writers with finished manuscripts are welcome alongside illustrators.</p></div>
</div>

<div class="entry"><span class="charge">What we are looking for</span>
<p>Picture-book illustrators based in South Africa or anywhere on the African continent. Watercolour,
gouache, ink, collage, or careful digital work painted by a human hand. You should be able to hold a
child's attention across fourteen landscape spreads, leave room for verse overlaid on the art, and
paint places and people with respect. We are not asking for a mimic of the current AI look. We are
asking for <strong>your</strong> eye.</p></div>

<div class="entry"><span class="charge">The first commission: <em>The Little Key</em></span>
<p>A girl named Thembi finds an old brass key and an old cupboard in her grandmother's house. The story
is set in South Africa; the tone is warm, quiet, and read-aloud. Read it free at
<a href="read/the-little-key.html">read/the-little-key.html</a>. The cover art is in place; the
spread paintings are the audition brief. Replace the interim AI art spread by spread, or show us how
you would paint Thembi, the cupboard, and the light in that room.</p></div>

<div class="entry"><span class="charge">What to send</span>
<p>Your portfolio link, city and country, languages you work in, and <strong>one</strong> of the
following: two character sketches for <em>The Little Key</em>, one finished sample spread (landscape,
3:2), or three spreads from a picture book you have already published. Tell us your medium, your
turnaround, and whether you are open to royalty, fee, or a hybrid. Links only; do not attach huge
files to the form.</p></div>

<div class="entry"><span class="charge">Where this goes</span>
<p>Accepted illustrators land on the Children's Library shelf with finished, credited cover and spread
art. The press coordinates small-batch print through its
<a href="printing.html">print marketplace</a>. The long aim: a shelf a child can hold that was painted
by people from their own continent.</p></div>

{linkout_or_form(ILLUSTRATOR_AUDITION_FORM_URL, button_label="Open the illustrator form", lead="Send your portfolio and sample links. Tell us where you are and what you paint.", inline_form=f'''<form class="intake-form" data-form-name="illustrator-audition" action="{form_target}" method="post"{form_enctype}>
<label>Name<input name="name" autocomplete="name" required></label>
<label>Email<input name="email" type="email" autocomplete="email" required></label>
<label>Country / city<input name="location" autocomplete="address-level1" required></label>
<label>Languages<input name="languages" placeholder="English, isiZulu, Afrikaans, Kiswahili..." required></label>
<label>Medium<input name="medium" placeholder="Watercolour, gouache, ink, Procreate, mixed media..."></label>
<label>Portfolio link<input name="portfolio_link" type="url" placeholder="https://..." required></label>
<label>Sample work link<input name="sample_link" type="url" placeholder="Character sheet, spread, or published book — https://..." required></label>
<label>Commercial preference
<select name="commercial_preference" required>
<option value="">Choose one</option>
<option>Fee per spread / per book</option>
<option>Reduced fee plus print royalty</option>
<option>Royalty-only for the right project</option>
<option>Open to discussion</option>
</select></label>
<label>Anything we should know<textarea name="notes" rows="5" placeholder="Published titles, turnaround, themes you love, whether you also write for children, links to more work..."></textarea></label>
{portfolio_note}
<button class="btn" type="submit">Send illustrator audition &rarr;</button>
</form>''')}

<p style="text-align:center;margin-top:44px"><a class="back" href="book/the-little-key.html">&larr; Back to <em>The Little Key</em></a>
 · <a class="back" href="index.html#library">Library</a></p>
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
<img class="letter-crest" src="assets/brand/safari-mark.png" alt="Arjuna Badger Press">
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
<img class="letter-crest" src="assets/brand/safari-mark.png" alt="Arjuna Badger Press">
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
        "/landing.html",
        "/assets/site.css",
        "/assets/safari.css",
        "/assets/fonts/AtkinsonHyperlegible-Regular.otf",
        "/assets/fonts/AtkinsonHyperlegible-Bold.otf",
        "/assets/fonts/AtkinsonHyperlegible-Italic.otf",
        "/assets/fonts/AtkinsonHyperlegible-BoldItalic.otf",
        "/assets/safari/sossusvlei-dunes.jpg",
        "/assets/safari/okavango-delta.jpg",
        "/assets/brand/logo-master.png",
        "/assets/brand/favicon-180.png",
        "/assets/brand/favicon-512.png",
        "/manifest.webmanifest",
    ]
    core_js = json.dumps(core, indent=2)
    return f"""const CACHE_NAME = "abp-pwa-v9";
const CORE_ASSETS = {core_js};

self.addEventListener("install", event => {{
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(CORE_ASSETS)));
  self.skipWaiting();
}});

self.addEventListener("activate", event => {{
  event.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
    )).then(() => caches.open(CACHE_NAME).then(cache =>
      cache.keys().then(reqs => Promise.all(
        reqs.filter(r => {{
          const p = new URL(r.url).pathname;
          return p.startsWith("/assets/covers/") || p === "/" || p === "/index.html";
        }}).map(r => cache.delete(r))
      ))
    )))
  );
  self.clients.claim();
}});

self.addEventListener("fetch", event => {{
  const request = event.request;
  if (request.method !== "GET") return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;
  if (url.pathname.startsWith("/downloads/")) return;

  // Shelf HTML and cover art must always revalidate — stale SW cache hid Little Key cover.
  const path = url.pathname;
  if (path === "/" || path === "/index.html" || path.startsWith("/assets/covers/")) {{
    event.respondWith(
      fetch(request).then(response => response).catch(() => caches.match(request))
    );
    return;
  }}

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


# Register picker + select-to-suggest inline correction. __API__ and __BOOK__ are JSON-injected.
_READER_REGISTER_JS = """<script>
(function(){
  var API=__API__, BOOK=__BOOK__, KEY='abp-reg:'+BOOK;
  var sel=document.getElementById('regsel');
  var wins=[].slice.call(document.querySelectorAll('.regwin'));
  if(!sel||!wins.length) return;
  function show(id){
    var any=false;
    wins.forEach(function(w){var on=w.getAttribute('data-edition')===id; w.hidden=!on; any=any||on;});
    if(!any){ wins[0].hidden=false; id=wins[0].getAttribute('data-edition'); }
    sel.value=id; try{localStorage.setItem(KEY,id);}catch(e){}
  }
  var saved=null; try{saved=localStorage.getItem(KEY);}catch(e){}
  show(saved && document.querySelector('.regwin[data-edition="'+saved+'"]') ? saved : wins[0].getAttribute('data-edition'));
  sel.addEventListener('change', function(){ show(sel.value); });

  // ── select any line → suggest a better version (judged register-aware, queued for a human) ──
  var box=document.getElementById('corrbox');
  function activeWin(){ return wins.filter(function(w){return !w.hidden;})[0]; }
  function closeBox(){ if(box){box.hidden=true; box.innerHTML='';} }
  document.addEventListener('mouseup', function(){
    var s=window.getSelection(); var t=(s&&s.toString()||'').trim();
    if(t.length<3||t.length>600){ return; }
    var w=activeWin(); if(!w||!w.contains(s.anchorNode)) return;
    openBox(t, w);
  });
  function openBox(orig, w){
    if(!box) return;
    box.innerHTML='<div class="corrcard">'
      +'<p class="corrh">Suggest a better line <span>('+w.getAttribute('data-register')+' · '+w.getAttribute('data-lang')+')</span></p>'
      +'<p class="corrorig"></p>'
      +'<textarea id="corrsug" rows="3" placeholder="How would you say it?"></textarea>'
      +'<div class="corrrow"><input id="corrwho" placeholder="your name (optional)">'
      +'<button id="corrsend" class="dl solid">Send</button>'
      +'<button id="corrcancel" class="dl">Cancel</button></div>'
      +'<p class="corrmsg" id="corrmsg"></p></div>';
    box.querySelector('.corrorig').textContent='“'+orig+'”';
    box.hidden=false;
    document.getElementById('corrsug').focus();
    document.getElementById('corrcancel').onclick=closeBox;
    document.getElementById('corrsend').onclick=function(){
      var sug=document.getElementById('corrsug').value.trim();
      if(!sug){ document.getElementById('corrmsg').textContent='Type a suggestion first.'; return; }
      var msg=document.getElementById('corrmsg'); msg.textContent='Sending…';
      fetch(API,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({
        book:BOOK, lang:w.getAttribute('data-lang'), register_band:w.getAttribute('data-register'),
        original:orig, suggestion:sug, context:'', contributor:document.getElementById('corrwho').value.trim()||null
      })}).then(function(r){return r.json();}).then(function(d){
        msg.textContent=(d&&d.message)||'Thank you — a person will look at this.';
        setTimeout(closeBox, 2600);
      }).catch(function(){ msg.textContent='Could not send right now — please try again later.'; });
    };
  }
  document.addEventListener('keydown', function(e){ if(e.key==='Escape') closeBox(); });
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


# ── "Read it in your register" — Buabantu register windows on the read page ─────────────────────
# A book may ship register editions as build/BOOK.<lang>-<register>.md (e.g. zu-everyday). When any
# exist, the read page offers a picker (language × register) that swaps the rendered text client-side,
# remembers the choice, and lets a reader suggest a better line (→ /api/buabantu/corrections, judged
# register-aware, queued for a human). English "formal" is always the original BOOK.md.
REGISTER_ORDER = ["formal", "professional", "everyday", "street"]
REGISTER_LABEL = {"formal": "Formal", "professional": "Professional",
                  "everyday": "Everyday", "street": "Street"}
# books that opt into the register picker (debut: resonance). Others render as before.
REGISTER_BOOKS = set(
    s.strip() for s in os.environ.get("ABP_REGISTER_BOOKS", "resonance").split(",") if s.strip())
BUABANTU_API = os.environ.get("ABP_BUABANTU_API", "/api/buabantu/corrections")


def register_editions(e: dict) -> list[dict]:
    """Discover register windows on disk for a book: the English original (en-formal) plus any
    build/BOOK.<lang>-<register>.md. Returns [{lang, register, label, md}] in a sensible order."""
    if e["id"] not in REGISTER_BOOKS or not e.get("book_md"):
        return []
    build = e["book_md"].parent
    eds = [{"lang": "en", "register": "formal", "label": "English · Original",
            "md": e["book_md"].read_text(encoding="utf-8", errors="ignore")}]
    found = []
    for f in sorted(build.glob("BOOK.*-*.md")):
        stem = f.stem[len("BOOK."):]                       # e.g. "zu-everyday" / "zu-pro"
        if "-" not in stem:
            continue
        lang, reg = stem.split("-", 1)
        reg = {"pro": "professional"}.get(reg, reg)
        if reg not in REGISTER_ORDER:
            continue
        langname = "English" if lang == "en" else EDITION_LANGS.get(lang, (lang.upper(), lang.upper()))[0]
        found.append({"lang": lang, "register": reg,
                      "label": f"{langname} · {REGISTER_LABEL[reg]}",
                      "md": f.read_text(encoding="utf-8", errors="ignore"),
                      "_sort": (lang != "en", lang, REGISTER_ORDER.index(reg))})
    found.sort(key=lambda d: d["_sort"])
    return eds + found


def _render_reader_registers(e: dict, editions: list[dict]) -> str:
    """Read page with a register picker: one edition shown at a time, swap client-side, remembered,
    plus select-to-suggest inline corrections (judged register-aware, queued for a human)."""
    rw = reader_rewrite_links
    # Register editions are re-read raw from disk by register_editions(), so they bypass the
    # prepare_reader_images() pass applied to single-edition readers. Resolve + copy each
    # edition's inline images here too, otherwise machine-local BOOK.md image paths (e.g. the
    # africangold/ migration leftovers) leak straight into the built page and 404 on the live site.
    assets_out = OUT / "read" / "assets" / e["id"]
    # render each edition's HTML into a hidden block; first is shown by default
    blocks, options = [], []
    for i, ed in enumerate(editions):
        prepared = prepare_reader_images(ed["md"], e["id"], e["root"], assets_out)
        body = md_to_html(rw(prepared), reader=True)
        eid = f'{ed["lang"]}-{ed["register"]}'
        shown = "" if i == 0 else ' hidden'
        blocks.append(
            f'<article class="reader regwin" lang="{ed["lang"]}-ZA" data-edition="{eid}" '
            f'data-lang="{ed["lang"]}" data-register="{ed["register"]}"{shown}>{body}</article>')
        options.append(f'<option value="{eid}">{html.escape(ed["label"])}</option>')
    dl = ""
    for f in e["downloads"]:
        if f.suffix.lower() == ".epub":
            dl = f'<a class="dl solid" href="../downloads/{e["id"]}/{html.escape(f.name)}" download>Download EPUB</a>'
            break
    picker = (
        '<div class="regpicker"><label for="regsel">Read it in your register</label>'
        f'<select id="regsel">{"".join(options)}</select>'
        '<span class="reghint">pick how it should sound · select any line to suggest a better one</span>'
        '</div>')
    body_js = _READER_REGISTER_JS.replace("__API__", json.dumps(BUABANTU_API)).replace(
        "__BOOK__", json.dumps(e["id"]))
    main = f'<main id="main"><div class="readlayout-wide">{"".join(blocks)}</div></main>'
    return "\n".join([
        head(f'Read: {e["title"]} — Arjuna Badger Press', truncate(e["blurb"] or e["title"], 180), rel="../"),
        trust_banner(rel="../"),
        f"""<div class="readbar"><div class="wrap" style="display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap">
<a class="back" href="../book/{e['id']}.html">← {html.escape(e['title'])}</a>{picker}<div class="dls">{dl}</div></div></div>""",
        main,
        '<div id="corrbox" class="corrbox" hidden></div>',
        reader_endnote(e),
        footer(rel="../"),
        body_js,
        rating_script(),
    ])


def render_reader(e: dict) -> str:
    rw = reader_rewrite_links
    editions = register_editions(e)
    if len(editions) > 1:
        return _render_reader_registers(e, editions)
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


# ── Picture-book reader ──────────────────────────────────────────────────────────────────────
# Landscape spreads with verse overlaid on the art. Source: build/chapters/PICTURE_BOOK.md (and
# PICTURE_BOOK.<lang>.md siblings for translated overlay text). Spread markers:
#
#   <!-- spread:5 image="spread-05-awake.png" alt="…" textPos="bc" scrim="bottom" -->
#
# textPos: bl | br | tl | tr | bc | cc (where the verse sits on the quieter part of the art).
_PB_TEXT_POS = frozenset({"bl", "br", "tl", "tr", "bc", "cc"})
_PB_SCRIM_FOR_POS = {"bl": "bottom", "br": "bottom", "bc": "bottom", "cc": "full",
                     "tl": "top", "tr": "top"}
_SPREAD_RE = re.compile(
    r'<!--\s*spread:(\d+)\s+image="([^"]+)"(?:\s+alt="([^"]*)")?'
    r'(?:\s+textPos="([^"]*)")?(?:\s+scrim="([^"]*)")?\s*-->\s*\n'
    r'(.*?)(?=\n<!--\s*spread:|\Z)',
    re.DOTALL,
)


def picture_book_manuscripts(root: Path, book_id: str) -> dict[str, str]:
    """All picture-book manuscripts on disk: PICTURE_BOOK.md (en) + PICTURE_BOOK.<lang>.md."""
    chap = root / "build" / "chapters"
    out: dict[str, str] = {}
    master = chap / "PICTURE_BOOK.md"
    if master.is_file():
        out["en"] = apply_picture_book_tokens(
            master.read_text(encoding="utf-8", errors="ignore"), book_id)
    for f in sorted(chap.glob("PICTURE_BOOK.*.md")):
        code = f.stem.split(".", 1)[-1].lower()
        if code in EDITION_LANGS and code not in out:
            out[code] = apply_picture_book_tokens(
                f.read_text(encoding="utf-8", errors="ignore"), book_id)
    return out


def _picture_book_head(md: str) -> tuple[str, str]:
    """Title + byline from the manuscript preamble (before the first spread marker)."""
    title, byline = "", ""
    for ln in md.splitlines():
        s = ln.strip()
        if s.startswith("<!-- spread:"):
            break
        if s.startswith("# "):
            title = s[2:].strip()
        elif s.startswith("*") and s.endswith("*") and len(s) > 2 and not byline:
            byline = s.strip("*").strip()
    return title, byline


def picture_book_verse_html(text: str) -> str:
    """Turn a spread stanza into overlay HTML (*…* refrains styled apart)."""
    lines: list[str] = []
    in_refrain = False
    for raw in text.split("\n"):
        ln = raw.strip()
        if not ln:
            lines.append('<span class="spread-gap"></span>')
            continue
        opens = ln.startswith("*")
        closes = ln.endswith("*") and ln != "*"
        if opens and closes and len(ln) > 2 and not in_refrain:
            lines.append(f'<em class="refrain">{html.escape(ln.strip("*").strip())}</em>')
        elif opens and not in_refrain:
            in_refrain = True
            body = ln.lstrip("*").strip()
            if closes:
                in_refrain = False
                body = body.rstrip("*").strip()
            lines.append(f'<em class="refrain">{html.escape(body)}'
                         + ('</em>' if not in_refrain else ''))
        elif in_refrain:
            if closes:
                in_refrain = False
                lines.append(f'{html.escape(ln.rstrip("*").strip())}</em>')
            else:
                lines.append(html.escape(ln))
        else:
            lines.append(html.escape(ln))
    if in_refrain:
        lines.append('</em>')
    return "<br>\n".join(lines)


def _picture_book_spreads(md: str):
    """Yield (number, image_src, alt, text_pos, scrim, text) per spread marker."""
    for m in _SPREAD_RE.finditer(md):
        num, img, alt = m.group(1), m.group(2), (m.group(3) or "")
        text_pos = (m.group(4) or "bl").strip().lower()
        if text_pos not in _PB_TEXT_POS:
            text_pos = "bl"
        scrim = (m.group(5) or _PB_SCRIM_FOR_POS.get(text_pos, "bottom")).strip().lower()
        yield int(num), img, alt, text_pos, scrim, m.group(6).strip("\n")


def picture_book_lang_pack(md: str, *, title: str = "", byline: str = "") -> dict:
    """One language's overlay text + spread positions parsed from a manuscript."""
    t, b = _picture_book_head(md)
    spreads = []
    for num, _img, _alt, text_pos, scrim, text in _picture_book_spreads(md):
        spreads.append({
            "n": num,
            "html": picture_book_verse_html(text),
            "pos": text_pos,
            "scrim": scrim,
        })
    return {
        "title": t or title,
        "byline": b or byline,
        "spreads": spreads,
    }


def picture_book_lang_data(e: dict) -> dict:
    """All overlay languages for a picture book, keyed by lang code (for client-side swap)."""
    manuscripts = picture_book_manuscripts(e["root"], e["id"])
    if not manuscripts and e.get("reader_md"):
        manuscripts = {"en": apply_picture_book_tokens(e["reader_md"], e["id"])}
    packs: dict[str, dict] = {}
    fallback_title, fallback_byline = e["title"], ""
    for code, md in manuscripts.items():
        pack = picture_book_lang_pack(md, title=e["title"])
        if code == "en":
            fallback_title, fallback_byline = pack["title"], pack.get("byline", "")
        packs[code] = pack
    if "en" not in packs and e.get("prepared_reader_md"):
        packs["en"] = picture_book_lang_pack(
            e["prepared_reader_md"], title=fallback_title, byline=fallback_byline)
    return packs


def render_picture_book(e: dict) -> str:
    """Render a children's picture book: landscape spreads, verse overlaid on the art."""
    lang_data = picture_book_lang_data(e)
    en = lang_data.get("en") or {"title": e["title"], "byline": "", "spreads": []}
    overlay_by_n = {s["n"]: s for s in en.get("spreads", [])}
    md = e.get("prepared_reader_md") or e.get("reader_md") or ""

    spreads_html = []
    for num, img, alt, text_pos, scrim, text in _picture_book_spreads(md):
        src = img if img.startswith(("http", "assets/")) else f"assets/{e['id']}/{img}"
        ov = overlay_by_n.get(num)
        pos = (ov or {}).get("pos") or text_pos
        scr = (ov or {}).get("scrim") or scrim
        verse = (ov or {}).get("html") or picture_book_verse_html(text)
        scrim_cls = {"bottom": "scrim-bottom", "top": "scrim-top", "full": "scrim-full"}.get(
            scr, "scrim-bottom")
        spreads_html.append(
            f'<figure class="spread landscape {scrim_cls}" id="spread-{num}">'
            f'<img src="{html.escape(src)}" alt="{html.escape(alt)}" loading="lazy" decoding="async">'
            f'<figcaption class="spread-overlay pos-{html.escape(pos)}" data-spread="{num}">{verse}</figcaption>'
            f'</figure>'
        )

    dl = ""
    for f in e["downloads"]:
        if f.suffix.lower() == ".epub":
            dl = f'<a class="dl solid" href="../downloads/{e["id"]}/{html.escape(f.name)}" download>Download EPUB</a>'
            break

    lang_json = json.dumps(lang_data, ensure_ascii=False)
    lang_note = '<p class="pb-lang-note" hidden aria-live="polite"></p>' if AVAILABLE_LANGS else ""

    head_block = (
        f'<header class="picture-head"><h1>{html.escape(en.get("title") or e["title"])}</h1>'
        + (f'<p class="picture-byline">{html.escape(en["byline"])}</p>' if en.get("byline") else "")
        + "</header>"
    )
    article = (
        f'<article class="picture-book" data-pb lang="en-ZA">{head_block}'
        f'<script type="application/json" id="pb-data">{lang_json}</script>'
        f'<div class="picture-spreads snap">{"".join(spreads_html)}</div>'
        "</article>"
    )
    return "\n".join([
        head(f'Read: {e["title"]} — Arjuna Badger Press', truncate(e["blurb"] or e["title"], 180), rel="../"),
        '<script>document.documentElement.classList.add("pb-reader");document.body.classList.add("pb-reader");</script>',
        trust_banner(rel="../"),
        nav_bar(rel="../"),
        f"""<div class="readbar pb-readbar"><div class="wrap pb-readbar-inner">
<a class="back" href="../book/{e['id']}.html">← {html.escape(e['title'])}</a>{lang_note}<div class="dls">{dl}</div></div></div>""",
        f'<main id="main">{article}',
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
        # Redirect stubs (e.g. cv.html now points to congosky.cloud/cv) carry no
        # chrome or logo — they exist only to bounce old bookmarks. Skip them.
        if 'http-equiv="refresh"' in page:
            continue
        if logo not in page:
            raise SystemExit(f"safari logo guard: {path.relative_to(out)} missing {logo}")
        # "bad" = any OTHER brand mark than the current SAFARI_LOGO — derived, so this never
        # rejects the configured mark even when SAFARI_LOGO changes.
        for bad in {"mark-only.png", "badger-bow-stamp.png", "safari-mark.png", "logo-master.png"} - {SAFARI_LOGO}:
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
                 "house-of-greyling-crest.png", SAFARI_LOGO,
                 # Studio (SaaS) brand — used by the /studio, /write and /login app shell
                 "logo-saas.png", "mark-saas.png", "favicon-saas-32.png", "favicon-saas-180.png"):
        src = BRAND / name
        if src.is_file():
            shutil.copy2(src, OUT / "assets" / "brand" / name)
    # Atkinson Hyperlegible — self-hosted for landing + library (cover typeface parity).
    fonts_out = OUT / "assets" / "fonts"
    fonts_out.mkdir(parents=True, exist_ok=True)
    fonts_src = REPO / "assets" / "fonts"
    for name in ("AtkinsonHyperlegible-Regular.otf", "AtkinsonHyperlegible-Bold.otf",
                 "AtkinsonHyperlegible-Italic.otf", "AtkinsonHyperlegible-BoldItalic.otf"):
        src = fonts_src / name
        if src.is_file():
            shutil.copy2(src, fonts_out / name)
    (OUT / "assets" / "site.css").write_text(CSS, encoding="utf-8")
    (OUT / "assets" / "safari.css").write_text(SAFARI_CSS, encoding="utf-8")
    safari_assets = OUT / "assets" / "safari"
    safari_assets.mkdir(parents=True, exist_ok=True)
    for name in ("sossusvlei-dunes.jpg", "okavango-delta.jpg", "g-wall.jpg", "ATTRIBUTION.md"):
        src = BRAND / "safari" / name
        if src.is_file():
            shutil.copy2(src, safari_assets / name)
    writing_assets = OUT / "assets" / "writing"
    writing_assets.mkdir(parents=True, exist_ok=True)
    for media in WRITING_MEDIA.values():
        src = media["cover"]
        if not src.is_file():
            raise SystemExit(f"build aborted: missing Writing Desk cover: {src}")
        shutil.copy2(src, writing_assets / media["cover_name"])
    (OUT / "manifest.webmanifest").write_text(render_manifest(), encoding="utf-8")
    (OUT / "sw.js").write_text(render_service_worker(), encoding="utf-8")

    entries = scan()
    # Site-wide language bar: which edition languages exist anywhere in the catalogue. Set BEFORE
    # any page renders, since nav()/footer() on every page read AVAILABLE_LANGS.
    global AVAILABLE_LANGS
    AVAILABLE_LANGS = compute_available_langs(entries)
    if AVAILABLE_LANGS:
        print(f"  (language bar: {', '.join(['en'] + AVAILABLE_LANGS)})")
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
        # SHELF thumbnail (small WebP) — the shelf card serves this instead of the multi-MB PNG.
        # Idempotent + no-op-safe: on PIL/source failure the shelf card falls back to the full
        # cover. Must run BEFORE render_index() so card() sees the thumb in _THUMB_OK.
        make_cover_thumb(e["id"], e.get("cover"))
        # downloads
        # A workshop-held book ships NO download files and NO read-online page (it is announced as
        # drafting, not published) — so its un-vetted EPUB/PDF is never reachable by direct URL.
        # Copy primary downloads (PUBLISHED + available) AND any translated editions. A SERIAL /
        # open-draft book ships no English download but MAY ship translated-edition EPUBs (e.g.
        # bloedrivier's isiZulu/isiXhosa/Sesotho/Setswana drafts), so editions copy independently.
        if (e["downloads"] and e["available"]) or e.get("editions"):
            d = OUT / "downloads" / e["id"]
            d.mkdir(parents=True, exist_ok=True)
            if e["available"]:
                for f in e["downloads"]:
                    shutil.copy2(f, d / f.name)
            # translated editions ride alongside the primary download (same dir)
            for fmts in e.get("editions", {}).values():
                for f in fmts.values():
                    shutil.copy2(f, d / f.name)
        # audiobook: download formats + per-chapter MP3s for the inline player, under downloads/<id>/audio/
        ab = e.get("audiobook")
        if ab:
            adir = OUT / "downloads" / e["id"] / "audio"
            adir.mkdir(parents=True, exist_ok=True)
            for fmt in ab["formats"]:
                shutil.copy2(fmt["path"], adir / fmt["path"].name)
                fmt["name"] = fmt["path"].name
            cdir = adir / "chapters"
            cdir.mkdir(parents=True, exist_ok=True)
            ab["chapter_names"] = []
            for cf in ab["chapters"]:
                shutil.copy2(cf, cdir / cf.name)
                ab["chapter_names"].append(cf.name)
        # book page + reader
        (OUT / "book" / f'{e["id"]}.html').write_text(render_book(e), encoding="utf-8")
        if (e["available"] or e.get("serial")) and (e["book_md"] or e.get("reader_md")):
            raw_md = (
                e["reader_md"]
                if e.get("reader_md")
                else e["book_md"].read_text(encoding="utf-8", errors="ignore")
            )
            if e["id"] in PICTURE_BOOKS:
                e["prepared_reader_md"] = prepare_picture_book_images(
                    raw_md, e["id"], e["root"], OUT / "read" / "assets" / e["id"]
                )
                reader_html = render_picture_book(e)
            else:
                e["prepared_reader_md"] = prepare_reader_images(
                    raw_md, e["id"], e["root"], OUT / "read" / "assets" / e["id"]
                )
                reader_html = render_reader(e)
            (OUT / "read" / f'{e["id"]}.html').write_text(reader_html, encoding="utf-8")

    for old_id, new_id in BOOK_REDIRECTS.items():
        _write_book_redirect(old_id, new_id, subdir="book")
        if (OUT / "read" / f"{new_id}.html").is_file():
            _write_book_redirect(old_id, new_id, subdir="read")

    (OUT / "index.html").write_text(render_index(entries), encoding="utf-8")
    (OUT / "start.html").write_text(render_start(entries), encoding="utf-8")
    # www / apex generic landing — the origin story + a door into each of the three products.
    # The app serves this at www.arjunabadger.press (Host-based routing); also reachable at /landing.html.
    # Pass the same live counts as the library hero so the Library card never drifts.
    avail = sum(1 for e in entries if e["available"])
    read_now = sum(1 for e in entries if e["available"] or e.get("serial"))
    (OUT / "landing.html").write_text(render_landing(read_now, avail), encoding="utf-8")
    # ── Buabantu product page — top-level /buabantu.html, linked from poes page ─────────────────
    _buabantu_src = REPO / "site" / "content" / "buabantu.md"
    if _buabantu_src.is_file():
        _buabantu_body = md_to_html(_buabantu_src.read_text(encoding="utf-8"))
        _buabantu_page = "\n".join([
            head("Buabantu — Register-aware language routing for African languages",
                 "OpenRouter, but for register and dialect. African and colloquial language "
                 "decoded and spoken back in the voice people actually use. "
                 "The jou-lucky-poes rule: judge by intent, never letters alone.",
                 rel="./", safari=True,
                 canonical=f"{DOMAIN}/buabantu.html",
                 keywords="Buabantu, African language AI, register, dialect, South African slang, "
                          "poes, jou lucky poes, language routing, OpenRouter Africa, "
                          "code-switching, translation API, Afrikaans NLP"),
            safari_nav("./"),
            '<article class="reader letter misogi-page">',
            crest_img("./", safari=True),
            _buabantu_body,
            '</article>',
            footer("./", safari=True),
        ])
        (OUT / "buabantu.html").write_text(_buabantu_page, encoding="utf-8")
    # ── The Man They All Misread — self-hosted companion music player ────────────────────────────
    # The badger thesis made audible: AJ's own catalogue on his own rails. The page reads
    # music-manifest.json (real lanes + real titles); audio streams once the MP3s are uploaded to
    # /audio/<lane>/<slug>.mp3 (R2). The manifest is committed at site/content/music-manifest.json
    # and regenerated by site/build_music_manifest.py against ~/code/congosky-music.
    _music_manifest = REPO / "site" / "content" / "music-manifest.json"
    if _music_manifest.is_file():
        (OUT / "the-man-they-all-misread.html").write_text(
            render_misread_player(), encoding="utf-8")
        # The page fetches the manifest at runtime, so it must sit next to the HTML.
        shutil.copy2(_music_manifest, OUT / "music-manifest.json")
        # Stage real audio: copy the MP3s from the music workspace into /audio/<lane>/<slug>.mp3,
        # matching each manifest track to its file on disk by normalized title + A/B variant. This
        # self-hosts AJ's catalogue on our own rails (no R2 needed for the static path). Skips
        # silently if the music workspace isn't present (e.g. CI without it) — page still builds.
        _staged = _stage_misread_audio(_music_manifest, OUT / "audio")
        if _staged:
            print(f"  → staged {_staged} audio files into {(OUT / 'audio').relative_to(REPO)}")
    if BOUNTY_LIVE:                              # the QR flyer advertises the prize money — gated
        (OUT / "flyer.html").write_text(render_flyer(), encoding="utf-8")
    # ── Safari — personal annex (CV, letters, arms, essays) ─────────────────────────────────────
    safari_out = OUT / "safari"
    safari_out.mkdir(exist_ok=True)
    (safari_out / "index.html").write_text(render_safari_hub(), encoding="utf-8")
    (safari_out / "cv.html").write_text(
        redirect_page(CONGOSKY_CV, CONGOSKY_CV, "Andries J. Greyling — CV"), encoding="utf-8")
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
    # Technology exposé — one page per tool, rendered under /safari/ alongside the hub so the
    # cross-links (tech-*.html) resolve from the canonical technology page.
    for src_name, slug, title, desc in DOC_PAGES:
        if not slug.startswith("tech-"):
            continue
        page = render_doc_page(src_name, slug, title, desc, rel="../", safari=True)
        if page:
            (safari_out / f"{slug}.html").write_text(with_mermaid(page), encoding="utf-8")
    for src_name, out_name, title, desc in LETTERS:
        page = render_letter(src_name, out_name, title, desc, rel="../", safari=True)
        if page:
            (safari_out / out_name).write_text(page, encoding="utf-8")
    for src_name, out_name, title, desc in POEMS:
        page = render_poem(src_name, out_name, title, desc, rel="../", safari=True)
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
    cv_canon = CONGOSKY_CV
    (OUT / "cv.html").write_text(redirect_page(CONGOSKY_CV, cv_canon, "Andries J. Greyling — CV"), encoding="utf-8")
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
    # Clean URL: arjunabadger.press/cv → congosky.cloud/cv (CV moved to CongoSky)
    (OUT / "cv").mkdir(exist_ok=True)
    (OUT / "cv" / "index.html").write_text(
        redirect_page(CONGOSKY_CV, cv_canon, "Andries J. Greyling — CV"), encoding="utf-8")
    (OUT / "feedback.html").write_text(render_feedback(), encoding="utf-8")
    (OUT / "join.html").write_text(render_call_to_arms(), encoding="utf-8")
    (OUT / "narrators.html").write_text(render_narrators(), encoding="utf-8")
    (OUT / "distribution.html").write_text(render_distribution(), encoding="utf-8")
    (OUT / "app.html").write_text(render_app_page(), encoding="utf-8")
    (OUT / "reader.html").write_text(render_reader_app(), encoding="utf-8")
    (OUT / "authoring.html").write_text(render_authoring_page(), encoding="utf-8")
    (OUT / "audition.html").write_text(render_audition_page(), encoding="utf-8")
    (OUT / "illustrator-audition.html").write_text(render_illustrator_audition_page(), encoding="utf-8")
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
        return not cover_git_tracked(p)

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
