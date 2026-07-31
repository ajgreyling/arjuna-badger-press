# THE RENDER GATE — binding (Arjuna Badger Press)

> **Accessibility rule (hard gate, owner's directive 2026-06-15):** the **body prose of every book in
> this repository renders ONLY in Atkinson Hyperlegible** — the Braille Institute's typeface, designed
> so the letterforms readers most often confuse (I / l / 1, O / 0, rn / m, etc.) are maximally
> distinguishable. Better for low-vision, dyslexic, and every other reader. **No other body font is
> permitted in any book's EPUB or PDF.**

## How it is enforced
- **One render path:** [`tools/render_book.sh`](render_book.sh) is the **single sanctioned way** to
  produce a book's EPUB + PDF. It:
  - embeds all four Atkinson styles (`assets/fonts/AtkinsonHyperlegible-{Regular,Italic,Bold,BoldItalic}.otf`)
    into every **EPUB** and injects [`assets/atkinson-epub.css`](../assets/atkinson-epub.css), which sets
    `body { font-family: "Atkinson Hyperlegible" !important }`;
  - sets `mainfont = "Atkinson Hyperlegible"` for every **PDF** (tectonic), embedding all four styles;
  - **fails hard** (non-zero exit) if any Atkinson font file or the gate CSS is missing.
- **Cover + PDF-availability note (added 2026-06-15):**
  - The gate auto-detects the book's cover (explicit 5th arg, else `…/export/cover.{png,jpg}`,
    else `…/design/cover.{png,jpg}`) and:
    - puts it as the **full-bleed first page of the PDF** (shipout-background image; pandoc's plain
      title page is suppressed when a cover exists, so the cover is genuinely page 1), and
    - sets it as the **EPUB cover image** (`--epub-cover-image`).
  - The **EPUB** (only — never the PDF) leads with a boxed note: *"Reading this as an e-book? A free,
    fully-illustrated PDF of this book — with the cover and all images — is available to read or
    download at arjunabadger.press."* (styled `.pdf-availability` in `atkinson-epub.css`). The EPUB
    is rendered from a temp copy that prepends the note; the PDF is rendered from the untouched
    BOOK.md, so the note can never leak into the PDF.
- **The font is vendored in the repo** (`assets/fonts/`, SIL Open Font License — free to embed and
  redistribute), so renders are self-contained and the EPUBs display Atkinson on devices that don't
  have the font installed.
- **EPUB accessibility metadata (added 2026-06-20):** every render sets `lang=en-ZA`, `publisher`,
  `rights`, and `date` in the OPF; the illustrated-PDF notice is a `role="note"` region; PDFs set
  `lang=en-ZA`. Read-online pages mark the prose `<article>` as `lang="en-ZA"` and fall back to
  `"Illustration"` when an inline image has no alt text.

## Usage
```sh
tools/render_book.sh <BOOK.md> <output-basename-without-ext> ["Title"] ["Author"]
# example:
tools/render_book.sh books/the-loneliest/build/BOOK.md \
  "books/the-loneliest/build/export/The Loneliest People in the World" \
  "The Loneliest People in the World" "Andries J. Greyling"
```

## Do NOT
- Do **not** render a book's EPUB/PDF with a bare `pandoc` call or `-V mainfont=<anything else>`.
- Do **not** set a per-book body font that overrides Atkinson.
- Do **not** remove the `!important` body rule in `atkinson-epub.css`.
- If a new book is added, render it through `render_book.sh` like every other.

## Verifying a render
- **PDF:** `pdffonts "<file>.pdf" | grep -i atkinson` → must list all 4 styles, embedded (`yes`).
- **EPUB:** `unzip -l "<file>.epub" | grep -i atkinson` → must list the 4 `.otf` files inside.

## Latest-epubs mirror (hard gate, owner's directive 2026-07-29)
- Every successful render **symlinks** the resulting `.epub` into a single flat folder,
  `../latest-epubs/` (sibling to this repo, i.e. `/Users/ajgreyling/code/arjuna-badger/latest-epubs/`),
  named `<output-basename>.epub`. This keeps one always-current, always-browsable copy of every
  book's latest EPUB in one place, without hunting through each book's `build/export/`.
- It's a **symlink**, not a copy: re-rendering a book automatically keeps the mirror current with
  zero extra steps, and it costs no extra disk.
- Opt out for a single render with `NO_LATEST_EPUB_LINK=1` (e.g. scratch/test renders you don't want
  polluting the mirror).
- Older entries in `latest-epubs/` from before this rule are real copied files, not symlinks — left
  as-is; only re-rendering a given book converts its entry to a symlink.

## Scope note
- The gate covers **book body prose** (the readable text — paragraphs, and headings inherit it too).
- It does **not** govern cover art or the brand/site typography (`brand/tokens.*`), which are separate.

> Status: applied to all books in the repo on 2026-06-15 (19 books re-rendered through the gate;
> Atkinson embedded in every EPUB + PDF, verified).
