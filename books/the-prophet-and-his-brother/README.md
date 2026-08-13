# The Prophet and his Brother

Near-future novel (2035). Book within a book: AJ on the Chobe writes G’s autobiography while the planet splits into four weathers around the man who derived **G**.

Former working title: *The Four Quarters* — kept as the name of the schism engine (the four camps).

## Status

**PUBLISHED** as **African Gold Companion · Book 3.5** (between RELIC and AFRIKA 2100) · ~90k ·
live on arjunabadger.press.

Briefly held (`3e773bf`, 2026-08-13) for a retitle to *Afrika 2035* and a re-edit, then released
the same day by explicit author decision once the re-edited exports landed. The title did not
change — *Afrika 2035* stayed a working title. `WORKSHOP_HOLD` is now empty; re-adding the id is
the one-line way to pull the book dark again (then run the full deploy loop — nothing changes on
the live site until Render redeploys).

Deliverables (the 2026-08-13 02:48 rebuild — post-edit):
- `build/export/The Prophet and his Brother.epub`
- `build/export/The Prophet and his Brother.pdf`
- `build/export/cover.png`

## Read first (canon)

1. [`canon/SEED_STORY.md`](canon/SEED_STORY.md)  
2. [`canon/CANON_CHOICES.md`](canon/CANON_CHOICES.md) — locks C-01…C-26  
3. [`canon/CHAPTER_LEDGER.md`](canon/CHAPTER_LEDGER.md)  
4. [`canon/G_LIFE.md`](canon/G_LIFE.md)  
5. [`canon/STYLE_GUIDE.md`](canon/STYLE_GUIDE.md)  

## Form

| Tag | Meaning |
|---|---|
| **A** | Outer — AJ close third (Mutatus Maximus / Chobe) |
| **I** | Inner — G autobiography (first-person life voice) |
| **G** | Outer — G present close third (Studio / schism weather) |

## Assemble + render

```bash
python3 -c "from pathlib import Path; p=sorted(Path('build/chapters').glob('ch-*.md')); Path('build/BOOK.md').write_text('\\n\\n'.join(x.read_text().rstrip()+'\\n' for x in p)+'\\n')"
python3 design/make_cover.py
python3 ../../brand/cover_imprint.py design/cover.png
cp design/cover.png design/cover.jpg build/export/
../../tools/render_book.sh build/BOOK.md "build/export/The Prophet and his Brother" "The Prophet and his Brother" "Andries J. Greyling" "build/export/cover.png"
```

## Care

Living-person sensitivity read recommended (AJ, G, Bouwer public record). Care rails in ch-00 / ch-23 + site `BOOK_NOTICE`. Shelf release by explicit author decision.
