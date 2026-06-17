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
import os
import re
import shutil
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BOOKS = REPO / "books"
BRAND = REPO / "brand" / "assets"
OUT = REPO / "site" / "public"

DOMAIN = "https://arjunabadger.press"
PUBLIC_EMAIL = "info@arjunabadger.press"
TAGLINE = "Your story, told true."

# ── Analytics (Plausible Cloud) ───────────────────────────────────────────────────────────────
# Privacy-first, no-cookie analytics. Set PLAUSIBLE_DOMAIN to the site domain registered in your
# plausible.io account (almost always "arjunabadger.press" — the bare host, no scheme). When set,
# head() emits the Plausible script with the file-downloads + outbound-links extension, which
# auto-tracks every EPUB/PDF download (links carry `download` + `class="dl"`) with NO per-link code.
# Leave empty to disable (no snippet emitted). Env var ABP_PLAUSIBLE_DOMAIN overrides.
PLAUSIBLE_DOMAIN = os.environ.get("ABP_PLAUSIBLE_DOMAIN", "arjunabadger.press")

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
        "unheard-japan,unheard-mongolia,"
        "modern-sherlock,no-fear-cycle,"
        "southern-coast",
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
        "unheard-japan,unheard-mongolia,"
        "sheltering-desert,the-loneliest,"
        "the-song-of-the-self,wrath-of-achilles,"
        "dust-throne",
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
        "the-resonance-court,"
        "dust-throne",
    ).split(",") if s.strip()
)

# ── Procedural-cover hide ─────────────────────────────────────────────────────────────────────
# Books whose cover is Pillow-generated (no cover-plate.png, file < RICH_COVER_MIN_BYTES) are
# withheld from the public shelf until a cinematic plate exists. Exempt: SERIAL ids (daily serial
# must stay visible), the whole "Not a Potato" line (dossier sub-style is intentional), and
# PROCEDURAL_SHOW (published flagships whose current cover is good enough for the shelf).
# Env ABP_SHOW_PROCEDURAL=1 overrides (show everything — dev/preview only).
RICH_COVER_MIN_BYTES = 500_000
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
        "Not a Potato,The Unheard",
    ).split(",") if s.strip()
)

# Book IDS here are dropped from the site ENTIRELY, same as HIDE_SERIES but for a single title on a
# shelf you want to keep — no card, page, downloads, or read-online (and a serial is de-listed too).
# Use when a shelf-wide hide is too broad (e.g. one serial on the busy History Before Time shelf).
# Env ABP_HIDE_BOOKS (comma-separated) overrides this default.
HIDE_BOOKS = set(
    s.strip() for s in os.environ.get(
        "ABP_HIDE_BOOKS",
        # the-first-unplugged: the Stranger in a Strange Land retelling stays PRIVATE — dropped
        # entirely from the site (no card, page, download, read-online), by explicit request.
        "the-resonance-court,the-first-unplugged",
    ).split(",") if s.strip()
)

def cover_is_procedural(cover: Path | None, root: Path) -> bool:
    """True when the resolved cover is a small generated placeholder, not a cinematic plate."""
    if cover is None:
        return True
    if (root / "design" / "cover-plate.png").is_file():
        return False
    try:
        return cover.stat().st_size < RICH_COVER_MIN_BYTES
    except OSError:
        return True

# ── The curated showcase. Each entry points at a book root; the generator fills in
#    downloads, cover, and blurb by scanning that root (with the fallbacks below). ──
SERIES = [
    ("The African Gold Trilogy", "#E5B567"),
    ("History Before Time", "#C8A86B"),
    ("Not a Potato", "#9A8B6B"),
    ("The Unheard", "#6B8C9A"),
    ("Standalones", "#B49A6A"),
    ("Non-fiction", "#7BA88C"),
    ("Companions", "#8C7BA8"),
    ("The Reichenbach Files", "#4a5568"),
    ("The No-Fear Cycle", "#1e3a8a"),
    ("The Salt Veil", "#B0814A"),
    ("The Dust Throne", "#8A5A2C"),
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
    ("the-resonance-court", "The Resonance Court", "The Synthesis · Book One · a daily serial", "The Synthesis",
     "history-before-time/books/the-resonance-court", "build/export",
     "A time-machine gate pulls history's masters and the living world's quiet geniuses into one house to face a species-level threat no weapon can touch — and the only thing that answers it is the one frequency they can all be tuned to. A fictional tribute, released day by day: the Prologue and Day One are live now, with a new chapter every day."),

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

    ("southern-coast", "The Southern Coast", "History Before Time · Novella", "History Before Time",
     "history-before-time/books/southern-coast", "build/export",
     "Stilbaai and the southern Cape — a photographer finds a shell midden older than the brochure admits, and a stone that shouldn't be there. Coming soon."),

    ("gobekli-tepe", "The Belly Hill", "Not a Potato", "Not a Potato",
     "_comingsoon/gobekli-tepe", "build/export",
     "Göbekli Tepe — the temple older than the plough, raised by hunter-gatherers a textbook said could not have raised it. The official story, played straight; the one accepted shock it can't explain away; the maybe left open for you to decide. Coming soon."),
    ("voynich-manuscript", "The Hand That Wrote It", "Not a Potato", "Not a Potato",
     "_comingsoon/voynich-manuscript", "build/export",
     "The Voynich Manuscript — a book in a language no one has ever read, illustrated with plants that grow nowhere on earth. Five centuries of the cleverest people alive have failed to crack it. The story of the object, played straight — and the one hole the explanations never close. Coming soon."),
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

    # ── Not a Potato — Why Files slate (draft/scaffold — in the workshop) ───────────────────────
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
    out, buf, bq_buf, list_tag, table_buf = [], [], [], None, []

    def inline(t: str) -> str:
        def fmt_label(label: str) -> str:
            label = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", label)
            label = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", label)
            label = re.sub(r"_(.+?)_", r"<em>\1</em>", label)
            label = re.sub(r"`(.+?)`", r"<code>\1</code>", label)
            return label

        def link_repl(m: re.Match[str]) -> str:
            href = html.escape(m.group(2), quote=True)
            return f'<a href="{href}">{fmt_label(m.group(1))}</a>'

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
        out.append("<thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in header) + "</tr></thead>")
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
            alt, src = imgm.group(1), imgm.group(2)
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
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
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


def scan() -> list[dict]:
    entries = []
    hidden_proc: list[str] = []
    for cid, title, subtitle, series, rootrel, expsub, fb in CURATED:
        root = BOOKS / rootrel
        exp = root / expsub
        downloads = []
        if cid in PUBLISHED and exp.is_dir():
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
        if (not SHOW_PROCEDURAL and cid not in SERIAL
                and cid not in PROCEDURAL_SHOW
                and series != "Not a Potato"
                and cover_is_procedural(cover, root)):
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
            "book_md": reader_src,
            "reader_md": reader_md,
            "root": root,
            "serial": cid in SERIAL,
            "available": can_read and (cid in SERIAL or bool(downloads)),
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
        for marker in ("books", "design"):
            if marker in parts:
                idx = parts.index(marker)
                candidates.append(BOOKS / Path(*parts[idx:]))
        candidates.append(book_root / "build" / "assets" / p.name)
        candidates.append(book_root / "design" / p.name)
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
            return m.group(0)
        dst = assets_out / resolved.name
        if not dst.exists() or resolved.stat().st_mtime > dst.stat().st_mtime:
            shutil.copy2(resolved, dst)
        return f"![{alt}](assets/{book_id}/{resolved.name})"

    return _READER_IMG_RE.sub(repl, md)


# ── render ───────────────────────────────────────────────────────────────────────
CSS = """
:root{
  --black:#161513; --iron:#221f1b; --card:#1d1a16; --bone:#EDE9E0; --bonedim:#BDB6A6;
  --ochre:#C8A86B; --gold:#E5B567; --grass:#7E7A5A; --line:#2A241D; --sting:#C2401E;
  --reading:"Atkinson Hyperlegible",system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
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
.nav nav.navinline{margin-left:auto;display:flex;gap:24px;font-size:14px}
.nav nav a{color:var(--bonedim);white-space:nowrap} .nav nav a:hover{color:var(--gold)}
.nav nav a.navhot{color:var(--sting);font-weight:600} .nav nav a.navhot:hover{color:#e0552e}

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
.navdrawer a.navhot{color:var(--sting)}
.navclose{position:absolute;top:16px;right:16px;font-size:30px;line-height:1;color:var(--bonedim);
  cursor:pointer;padding:4px 10px;border-radius:8px}
.navclose:hover{color:var(--bone);background:rgba(229,181,103,.1)}
.navscrim{position:fixed;inset:0;z-index:55;background:rgba(0,0,0,.5);opacity:0;visibility:hidden;
  transition:opacity .28s;cursor:pointer}
.navtoggle:checked ~ .navdrawer{transform:translateX(0)}
.navtoggle:checked ~ .navscrim{opacity:1;visibility:visible}
/* Wide screens: show the inline nav, hide the hamburger. Narrow: flip it. */
@media(min-width:1100px){ .hamburger{display:none} }
@media(max-width:1099px){ .nav nav.navinline{display:none} }

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
.pillar h3{margin:.2em 0 .4em;font-size:18px} .pillar p{margin:0;color:var(--bonedim);font-size:15px}
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
.reader{max-width:720px;margin:0 auto;padding:50px 24px 90px;
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
.readtoc-h{margin:0 0 12px;font-size:11px;letter-spacing:.26em;text-transform:uppercase;color:var(--ochre)}
.readtoc ol{list-style:none;margin:0;padding:0;counter-reset:toc}
.readtoc li{margin:0}
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
  .readtoc{position:static;max-height:340px;padding:14px 20px;margin:0 auto;max-width:720px;
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
@media(max-width:720px){.pillars{grid-template-columns:1fr}.bookhero{grid-template-columns:1fr;text-align:center}
  .bookhero .cover{max-width:260px;margin:0 auto}}
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400;1,700&'
         'family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&'
         'family=Inter:wght@400;500;600&family=Space+Grotesk:wght@400;500;600&display=swap" rel="stylesheet">')


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
{plausible_snippet()}
</head><body>"""


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
🛡️ <strong>We never ask you for money or an OTP — we only ever pay you, and we never DM you first.</strong>
<a href="{rel}bounty.html">How to know it's really us →</a>
</div></div>""")


def nav(rel: str = "") -> str:
    bounty_link = f'<a class="navhot" href="{rel}bounty.html">Bounty</a>' if BOUNTY_LIVE else ""
    links = (
        f'<a href="{rel}index.html#library">Library</a>'
        f'<a href="{rel}wiki/index.html">Places</a>'
        f'<a href="{rel}craft/index.html">For writers</a>'
        f'<a href="{rel}technology.html">Technology</a>'
        f'{bounty_link}'
        f'<a href="{rel}index.html#mission">Mission</a>'
        f'<a href="{rel}index.html#press">The Press</a>'
        f'<a href="{rel}index.html#thread">The Proof</a>'
        f'<a href="{rel}house.html">The House</a>'
        f'<a href="{rel}letter.html">A letter</a>'
        f'<a href="{rel}for-lisel.html">For Lisel</a>'
        f'<a href="{rel}index.html#write">Write with us</a>'
    )
    # Pure-CSS toggle (checkbox hack) — no JS needed. The hamburger opens a slide-out drawer with
    # every link; an inline nav still shows on wide screens (where there's room).
    return f"""<input type="checkbox" id="navtoggle" class="navtoggle" hidden>
<div class="nav"><div class="wrap">
<a class="brandlink" href="{rel}index.html"><img src="{rel}assets/brand/mark-only.png" alt="Arjuna Badger Press">Arjuna Badger Press</a>
<nav class="navinline">{links}</nav>
<label for="navtoggle" class="hamburger" aria-label="Menu"><span></span><span></span><span></span></label>
</div></div>
<label for="navtoggle" class="navscrim" aria-hidden="true"></label>
<nav class="navdrawer"><label for="navtoggle" class="navclose" aria-label="Close">&times;</label>{links}</nav>
{trust_banner(rel)}{audiobook_notice()}"""


def footer() -> str:
    return f"""<footer><div class="wrap">
<span>© Andries J. Greyling · Arjuna Badger Press · <a href="mailto:{PUBLIC_EMAIL}">{PUBLIC_EMAIL}</a></span>
<span class="badgerline">The archer's eye. The badger's nerve.</span>
</div></footer></body></html>"""


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
            ("A myth or classic, retold plainly", {"wrath-of-achilles": 5, "the-song-of-the-self": 4}),
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
        ext = "png" if e.get("real_cover") else "svg"
        # first epub / pdf download names
        dl = {}
        for f in e["downloads"]:
            x = f.suffix.lower().lstrip(".")
            dl.setdefault(x, f.name)
        books[e["id"]] = {
            "title": e["title"], "sub": e["subtitle"] or e["series"], "series": e["series"],
            "blurb": e["blurb"] or "", "cover": f"assets/covers/{e['id']}.{ext}",
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
<div class="cta"><a class="btn" href="start.html">Not sure where to start? →</a>
<a class="btn ghost" href="#library">Browse the library</a>
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

    parts.append("""<hr class="hr"><section class="mission" id="places"><div class="wrap">
<div class="eyebrow">Real ground</div>
<h2 style="font-size:28px;margin:.3em 0">The Place Wiki — real people &amp; places</h2>
<p style="max-width:70ch;color:var(--bonedim);font-size:17px">Every book is anchored in real geography — standing stones,
deserts, temples, reefs, and the living people who keep them. Photo wikis for travellers and curious readers: awe first,
attribution always.</p>
<div class="cta"><a class="btn" href="wiki/index.html">Explore the Place Wiki</a></div>
</div></section>""")

    parts.append("""<hr class="hr"><section class="mission" id="writers"><div class="wrap">
<div class="eyebrow">For writers</div>
<h2 style="font-size:28px;margin:.3em 0">Free craft — degree-level skills, no gatekeeping</h2>
<p style="max-width:70ch;color:var(--bonedim);font-size:17px">The studio mined an MFA-scale body of
knowledge from finishing a million words of published fiction — structure, character, sentence craft,
the editorial ladder, twenty-nine named anti-patterns, and a machine-tell self-audit. Plain English.
Free for every writer who has a story and has never been shown how to begin.</p>
<div class="cta"><a class="btn" href="craft/index.html">Open the Craft Library</a>
<a class="btn ghost" href="the-press-thesis.html">The Press Thesis</a>
<a class="btn ghost" href="for-authors.html">The workshop — for authors &amp; editors</a></div>
</div></section>""")

    parts.append('<div class="wrap" id="library"></div>')
    for sname, accent in SERIES:
        group = [e for e in entries if e["series"] == sname]
        if not group:
            continue
        cards = "".join(card(e, accent) for e in group)
        tag = SHELF_TAGLINE.get(sname)
        tagline = f'<p class="shelftag">{html.escape(tag)}</p>' if tag else ""
        parts.append(f"""<section class="series"><div class="wrap">
<div class="sechead" style="--accent:{accent}"><div class="sechead-row"><h2>{html.escape(sname)}</h2><span class="count">{len(group)} {"book" if len(group)==1 else "books"}</span></div>{tagline}</div>
<div class="grid">{cards}</div></div></section>""")

    parts.append(f"""<hr class="hr"><section class="mission" id="press"><div class="wrap">
<div class="eyebrow">The Press</div>
<h2 style="font-size:28px;margin:.3em 0">A small house taking on a 90% racket</h2>
<p style="max-width:70ch;color:var(--bonedim);font-size:17px">Arjuna Badger Press is the consumer face
of an autonomous manuscript-craft studio — a continuity engine, a manuscript scorer, and a
fact-and-balance gate that stand guard while a human writes the soul of the thing. The tools measure
and sound the alarm; they never write your voice for you. {avail} finished books are on the shelf
above, free to read and download. <a href="technology.html">See how the technology works &rarr;</a> ·
<a href="letter.html">Why this house exists — a letter &rarr;</a></p>
<div class="cta" id="write"><a class="btn" href="technology.html">How the technology works</a>
<a class="btn ghost" href="mailto:{PUBLIC_EMAIL}">Write with us</a>
<a class="btn ghost" href="mailto:{PUBLIC_EMAIL}">Publish with us</a></div>
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
    if e["id"] == "the-resonance-court":
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
    if e["available"]:
        soon = ""
    elif "_comingsoon" in e["root"].parts:
        soon = '<p style="color:var(--ochre);margin-top:18px">Coming soon — on the shelf, in progress.</p>'
    else:
        soon = '<p style="color:var(--ochre);margin-top:18px">In progress — not released yet. Check back soon.</p>'
    full = html.escape(e["blurb"]) if e["blurb"] else ""
    return "\n".join([
        head(f'{e["title"]} — Arjuna Badger Press', truncate(e["blurb"] or e["title"], 180), rel="../"),
        nav(rel="../"),
        f"""<div class="wrap"><div class="bookhero">
<img class="cover" src="../{cover}" alt="{html.escape(e['title'])} cover">
<div><div class="sub">{html.escape(e['subtitle'] or e['series'])}</div>
<h1>{html.escape(e['title'])}</h1>{(lambda t: f'<p class="tagline">{html.escape(t)}</p>' if t else '')(BOOK_TAGLINE.get(e['id']))}
<p class="syn">{full}</p>{dls}{read}{serial_note}{wiki}{soon}
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
        "../TECHNOLOGY.md": "../../index.html#press" if in_terms else "../index.html#press",
        "../craft/CRAFT_DOCTRINE.md": "../doctrine.html" if in_terms else "doctrine.html",
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
        f'<p style="text-align:center;margin-top:24px"><a class="back" href="{rel}index.html#writers">&larr; Back to the library</a></p>',
        '</article>',
        footer(),
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
        footer(),
    ])


def docs_rewrite_links(md: str) -> str:
    """Turn docs/*.md cross-links into site-local HTML paths (root-level pages)."""
    reps = {
        "FOR_AUTHORS.md": "for-authors.html",
        "THE_PRESS_THESIS.md": "the-press-thesis.html",
        "TECHNOLOGY.md": "index.html#press",
        "VERIFICATION_GATE.md": "index.html#press",
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
        out = out.replace(f"]({old})", f"]({new})")
    # The bounty report form — set BOUNTY_FORM_URL once the Google Form exists; until then links
    # point at the bounty page itself (no dead end). Replaces the BOUNTY_FORM_URL placeholder token.
    out = out.replace("(BOUNTY_FORM_URL)", f"({BOUNTY_FORM_URL or 'bounty.html'})")
    # The WhatsApp Channel invite — same fallback pattern.
    out = out.replace("(WHATSAPP_CHANNEL_URL)", f"({WHATSAPP_CHANNEL_URL or 'bounty.html'})")
    return out


DOC_PAGES = [
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


def render_doc_page(src_name: str, slug: str, title: str, desc: str) -> str | None:
    src = REPO / "docs" / src_name
    if not src.is_file():
        return None
    body = md_to_html(docs_rewrite_links(src.read_text(encoding="utf-8", errors="ignore")))
    gh = f'{GITHUB_REPO}/docs/{src_name}'
    return "\n".join([
        head(title, desc),
        nav(),
        '<article class="reader letter">',
        f'<p class="eyebrow" style="text-align:center">Arjuna Badger Press</p>',
        body,
        '<p style="margin-top:36px;font-size:14px;color:var(--grass)">'
        '<a href="craft/index.html">Craft Library</a> · '
        '<a href="wiki/index.html">Place Wiki</a> · '
        '<a href="index.html#press">The Press</a> · '
        f'<a href="{gh}">View this document on GitHub</a> · '
        '<a href="index.html#write">Write with us</a></p>',
        '<p style="text-align:center;margin-top:24px"><a class="back" href="index.html#writers">&larr; Back to the library</a></p>',
        '</article>',
        footer(),
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
    rel = "../" if not index else ""
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
        footer(),
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


def render_reader(e: dict) -> str:
    if e.get("prepared_reader_md"):
        body = md_to_html(reader_rewrite_links(e["prepared_reader_md"]))
    elif e.get("reader_md"):
        body = md_to_html(reader_rewrite_links(e["reader_md"]))
    elif e.get("book_md"):
        body = md_to_html(reader_rewrite_links(e["book_md"].read_text(encoding="utf-8", errors="ignore")))
    else:
        body = ""
    dl = ""
    for f in e["downloads"]:
        if f.suffix.lower() == ".epub":
            dl = f'<a class="dl solid" href="../downloads/{e["id"]}/{html.escape(f.name)}" download>Download EPUB</a>'
            break
    return "\n".join([
        head(f'Read: {e["title"]} — Arjuna Badger Press', truncate(e["blurb"] or e["title"], 180), rel="../"),
        trust_banner(rel="../"),
        audiobook_notice(),
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
        # A workshop-held book ships NO download files and NO read-online page (it is announced as
        # drafting, not published) — so its un-vetted EPUB/PDF is never reachable by direct URL.
        if e["downloads"] and e["available"]:
            d = OUT / "downloads" / e["id"]
            d.mkdir(parents=True, exist_ok=True)
            for f in e["downloads"]:
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

    (OUT / "index.html").write_text(render_index(entries), encoding="utf-8")
    (OUT / "start.html").write_text(render_start(entries), encoding="utf-8")
    if BOUNTY_LIVE:                              # the QR flyer advertises the prize money — gated
        (OUT / "flyer.html").write_text(render_flyer(), encoding="utf-8")
    for src_name, out_name, title, desc in LETTERS:
        page = render_letter(src_name, title, desc)
        if page:
            (OUT / out_name).write_text(page, encoding="utf-8")
    (OUT / "house.html").write_text(render_house(), encoding="utf-8")
    for src_name, slug, title, desc in DOC_PAGES:
        if slug in ("bounty", "finders") and not BOUNTY_LIVE:
            continue   # bounty surface is gated until launch (25 June 2026)
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

    wiki_n = build_wiki(OUT)

    avail = sum(1 for e in entries if e["available"])
    readers = sum(1 for e in entries if e["available"] and (e["book_md"] or e.get("reader_md")))
    print(f"built {len(entries)} books ({avail} available, {readers} read-online), "
          f"{craft_n} craft pages, {term_n} glossary terms, {wiki_n} wiki pages -> {OUT}")

    # ── Untracked-cover guard ─────────────────────────────────────────────────────────────────
    # The trap: a book's real cover sits ON DISK but is UNTRACKED in git. Every LOCAL build looks
    # fine (scan() finds the file → real_cover=True), but GitHub Pages deploys only committed files,
    # so on the live site the cover never checks out and the book falls back to the generated
    # cover_svg() placeholder. Because the failure is invisible locally, we cannot detect it by
    # asking "did we use the placeholder?" — we must ask git directly whether the resolved cover is
    # tracked. Books under _comingsoon/ are MEANT to have no cover yet, so they are exempt.
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
                    (e["id"], f"cover ON DISK but UNTRACKED — will deploy as a placeholder. "
                              f"Fix: git add {e['cover']}"))
        else:                                          # no cover anywhere for a shelf book
            cover_warnings.append(
                (e["id"], f"no cover found (add {e['root']}/design/cover.png, "
                          f"or move under books/_comingsoon/ if not ready)"))
    if cover_warnings:
        print("\n  ⚠️  COVER WARNING — these books will NOT show a real cover on the live site:")
        for cid, msg in cover_warnings:
            print(f"      • {cid}: {msg}")


if __name__ == "__main__":
    main()
