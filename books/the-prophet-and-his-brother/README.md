# Afrika 2035

Near-future novel (2035). Book within a book: AJ on the Chobe writes G’s autobiography while the planet splits into four weathers around the man who derived **G**.

**Retitled 2026-08-13** from *The Prophet and his Brother* — that phrase now names the book's
relation (G the prophet, AJ the brother), not the book. Earlier working title *The Four Quarters*
is kept as the name of the schism engine (the four camps).

The **id/slug stays `the-prophet-and-his-brother`** by author decision, so no live URL breaks.
Expect the old name in paths, the download folder and the export filenames; that is deliberate,
not drift.

## Status

**PUBLISHED** as **African Gold Companion · Book 3.5** (between RELIC and AFRIKA 2100) · ~90k ·
live on arjunabadger.press.

Briefly held (`3e773bf`, 2026-08-13) for the retitle and a re-edit, then released the same day by
explicit author decision once the re-edited exports landed. Note that hold never reached
production — it was committed but no deploy followed, so the book stayed publicly downloadable
throughout. `WORKSHOP_HOLD` is now empty; re-adding the id is the one-line way to pull the book
dark (then run the full deploy loop — nothing changes live until Render redeploys).

Deliverables (the 2026-08-13 02:48 rebuild — post-edit):
- `build/export/Afrika 2035.epub` — retitled inside and out
- `build/export/Afrika 2035.pdf` ⚠ filename only — interior still old
- `build/export/cover.png` — retitled *AFRIKA 2035*

⚠ **The PDF interior is still the old title.** The EPUB is fully retitled — `dc:title`, nav, TOC,
title page, chapter one, and the embedded cover image all read *Afrika 2035*. The PDF is renamed on
the outside only: its text lives in compressed streams and no PDF tooling (pypdf/exiftool/qpdf) is
installed, so its printed title page almost certainly still reads *The Prophet and his Brother*.
Fixing that needs a re-render from source — and note `arjuna-badger-platform/books/the-prophet-and-his-brother`
does not exist, so a plain engine resync will not do it; the origin of the 02:48 build needs finding first.
