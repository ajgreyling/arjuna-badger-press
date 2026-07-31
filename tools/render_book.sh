#!/usr/bin/env bash
# Arjuna Badger Press — THE RENDER GATE (binding).
# The SINGLE path every book's EPUB + PDF must be rendered through. Hard-enforces the accessibility
# rule: ALL book body prose renders in Atkinson Hyperlegible (Braille Institute, OFL), embedded.
#
# Usage:
#   tools/render_book.sh <BOOK.md path> <output basename> ["Title"] ["Author"]
# e.g.
#   tools/render_book.sh books/the-loneliest/build/BOOK.md \
#       "books/the-loneliest/build/export/The Loneliest People in the World" \
#       "The Loneliest People in the World" "Andries J. Greyling"
#
# Renders <basename>.epub and <basename>.pdf. No other font is permitted for body prose.

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FONT_NAME="Atkinson Hyperlegible"
FONT_DIR="$REPO/assets/fonts"
EPUB_CSS="$REPO/assets/atkinson-epub.css"

BOOK_MD="${1:?need BOOK.md path}"
OUT_BASE="${2:?need output basename (no extension)}"
TITLE="${3:-}"
AUTHOR="${4:-Andries J. Greyling}"
COVER="${5:-}"   # optional cover image; else auto-detected next to BOOK.md (build/export/cover.*)
PUBLISHER="House of Greyling"
YEAR=2026
RIGHTS="Copyright © ${YEAR} ${AUTHOR}. All rights reserved."

# ---- Trim size (env-overridable; default 6x9 for backward compatibility) ------------------------
# Set BOOK_TRIM=a5 for A5 perfect-bind (148x210mm). Margin scales to the smaller page.
case "${BOOK_TRIM:-6x9}" in
  a5|A5)   TRIM_W="148mm"; TRIM_H="210mm"; PDF_MARGIN="${PDF_MARGIN:-16mm}"; TRIM_W_MM=148; TRIM_H_MM=210 ;;
  6x9|*)   TRIM_W="6in";   TRIM_H="9in";   PDF_MARGIN="${PDF_MARGIN:-0.75in}"; TRIM_W_MM=152.4; TRIM_H_MM=228.6 ;;
esac

# ---- Optional bleed-PAGE variant: PAGE_BLEED_MM enlarges the PAPER by that bleed on every side and
# bumps the margin to match, so the text block stays in the same place but the sheet is trim+2*bleed.
# This produces the literal "page = trim + 3mm bleed" PDF some printers ask for (no crop marks).
if [ -n "${PAGE_BLEED_MM:-}" ]; then
  PW=$(python3 -c "print(f'{$TRIM_W_MM + 2*$PAGE_BLEED_MM}mm')")
  PH=$(python3 -c "print(f'{$TRIM_H_MM + 2*$PAGE_BLEED_MM}mm')")
  MG=$(python3 -c "print(f'{16 + $PAGE_BLEED_MM}mm')")   # keep text in the trim-safe area
  TRIM_W="$PW"; TRIM_H="$PH"; PDF_MARGIN="$MG"
fi

# ---- House colophon assets (used by BOTH the EPUB and PDF builds, so define before either) ------
# ABP mark on the final page of EVERY book, with the Klaus crest below it. Opt out: NO_COLOPHON=1.
# Klaus is optional (NO_KLAUS=1, or absent asset) — colophon falls back to ABP-only with no breakage.
COLOPHON_LOGO="$REPO/brand/assets/logo-black.png"
COLOPHON_KLAUS="$REPO/brand/assets/klaus-black.png"

[ -f "$BOOK_MD" ] || { echo "render_book: BOOK.md not found: $BOOK_MD" >&2; exit 1; }
[ -f "$EPUB_CSS" ] || { echo "render_book: gate CSS missing: $EPUB_CSS" >&2; exit 1; }
for f in Regular Italic Bold BoldItalic; do
  [ -f "$FONT_DIR/AtkinsonHyperlegible-$f.otf" ] || {
    echo "render_book: GATE FAILURE — missing font $FONT_DIR/AtkinsonHyperlegible-$f.otf" >&2; exit 1; }
done

mkdir -p "$(dirname "$OUT_BASE")"

DOSSIER_TEX="$REPO/assets/dossier-pdf.tex"

# ---- Resolve the cover image (for the PDF cover page + the EPUB cover) --------------------------
# Priority: explicit 5th arg → cover.png/jpg sitting next to BOOK.md (build/export/) → none.
if [ -z "$COVER" ]; then
  BOOK_DIR="$(cd "$(dirname "$BOOK_MD")" && pwd)"
  for cand in \
    "$BOOK_DIR/export/cover.png" "$BOOK_DIR/export/cover.jpg" \
    "$BOOK_DIR/cover.png" "$BOOK_DIR/cover.jpg" \
    "$(dirname "$BOOK_DIR")/design/cover.png" "$(dirname "$BOOK_DIR")/design/cover.jpg"; do
    [ -f "$cand" ] && { COVER="$cand"; break; }
  done
fi
if [ -n "$COVER" ] && [ -f "$COVER" ]; then
  echo "  [cover] using $COVER"
else
  echo "  [cover] none found — PDF will have no cover page, EPUB no cover image"
  COVER=""
fi

# ---- EPUB source: prepend a "free illustrated PDF online" note (EPUB ONLY, never the PDF) -------
# The same BOOK.md feeds both formats; telling a PDF reader "a PDF is available" is pointless and
# the EPUB is the one without the cover-page/images. So we render the EPUB from a temp copy that
# leads with the note, and render the PDF from the untouched BOOK.md.
EPUB_SRC="$(mktemp -t abp-epub-src).md"
{
  printf '::: {.pdf-availability role="note"}\n'
  printf '**Reading this as an e-book?** A free, fully-illustrated **PDF** of this book — with the\n'
  printf 'cover and all images — is available to read or download at **arjunabadger.press**.\n'
  printf ':::\n\n'
  cat "$BOOK_MD"
  # House colophon for the EPUB (the gate's PDF colophon is PDF-only; this gives the EPUB the same
  # ABP mark + Klaus crest on a final centred page). Centred via the .center class in atkinson-epub.css.
  if [ -z "${NO_COLOPHON:-}" ] && [ -f "$COLOPHON_LOGO" ]; then
    printf '\n\n::: {.center style="text-align:center"}\n\n'
    printf '![](%s){width=40%%}\n\n' "$COLOPHON_LOGO"
    if [ -z "${NO_KLAUS:-}" ] && [ -f "$COLOPHON_KLAUS" ]; then
      printf '![](%s){width=24%%}\n\n' "$COLOPHON_KLAUS"
      printf '*Klaus*\\\n'
      printf 'Custos, non Conditor\n'
    fi
    printf '\n:::\n'
  fi
} > "$EPUB_SRC"

# ---- EPUB: embed Atkinson (body) + Courier Prime (dossier) + inject the gate CSS ----------------
pandoc "$EPUB_SRC" \
  -o "$OUT_BASE.epub" \
  --to=epub3 \
  --top-level-division=chapter \
  --css "$EPUB_CSS" \
  --epub-embed-font="$FONT_DIR/AtkinsonHyperlegible-Regular.otf" \
  --epub-embed-font="$FONT_DIR/AtkinsonHyperlegible-Italic.otf" \
  --epub-embed-font="$FONT_DIR/AtkinsonHyperlegible-Bold.otf" \
  --epub-embed-font="$FONT_DIR/AtkinsonHyperlegible-BoldItalic.otf" \
  --epub-embed-font="$FONT_DIR/CourierPrime-Regular.ttf" \
  --epub-embed-font="$FONT_DIR/CourierPrime-Italic.ttf" \
  --epub-embed-font="$FONT_DIR/CourierPrime-Bold.ttf" \
  --epub-embed-font="$FONT_DIR/CourierPrime-BoldItalic.ttf" \
  --epub-embed-font="$FONT_DIR/Kalam-Regular.ttf" \
  --epub-embed-font="$FONT_DIR/Kalam-Bold.ttf" \
  ${COVER:+--epub-cover-image="$COVER"} \
  ${TITLE:+--metadata title="$TITLE"} \
  --metadata author="$AUTHOR" \
  --metadata lang=en-ZA \
  --metadata publisher="$PUBLISHER" \
  --metadata rights="$RIGHTS" \
  --metadata date="$YEAR"

rm -f "$EPUB_SRC"

# ---- PDF: tectonic, Atkinson body + a `dossier` (Courier Prime) environment for The File --------
# Pass the absolute font dir to LaTeX, then include the dossier header (defines \begin{dossier}).
PDF_HEADER="$(mktemp -t abp-pdf-header).tex"

{
  printf '\\def\\ABPFONTDIR{%s}\n' "$FONT_DIR"
  cat "$DOSSIER_TEX"
  # graphicx needed for the cover AND the colophon; load it whenever either is present
  if [ -n "$COVER" ] || { [ -z "${NO_COLOPHON:-}" ] && [ -f "$COLOPHON_LOGO" ]; }; then
    printf '\\usepackage{graphicx}\n'
  fi
  [ -n "$COVER" ] && printf '\\usepackage{eso-pic}\n'
} > "$PDF_HEADER"

# Full-bleed cover page as the FIRST page of the PDF (same mechanism as the HBT pipeline:
# a shipout-background image + an empty page + clearpage), injected via --include-before-body.
PDF_BEFORE=()
PDF_TITLE_ARGS=()
if [ -n "$COVER" ]; then
  PDF_COVER_TEX="$(mktemp -t abp-pdf-cover).tex"
  printf '\\AddToShipoutPictureBG*{\\put(0,0){\\includegraphics[width=\\paperwidth,height=\\paperheight]{%s}}}%%\n\\thispagestyle{empty}\\mbox{}\\clearpage\n' "$COVER" > "$PDF_COVER_TEX"
  PDF_BEFORE=(--include-before-body "$PDF_COVER_TEX")
  # Cover IS the title page → suppress pandoc's \maketitle entirely so the full-bleed cover is
  # genuinely page 1. Title/author still set as PDF *document properties* via hypersetup in the
  # header (no visible title page). PDF_TITLE_ARGS stays empty (no -V title / -V author).
  {
    printf '\\usepackage{hyperref}\n'
    printf '\\hypersetup{pdftitle={%s},pdfauthor={%s}}\n' "${TITLE:-}" "$AUTHOR"
  } >> "$PDF_HEADER"
else
  # No cover → keep the plain pandoc title page (old behaviour).
  [ -n "$TITLE" ] && PDF_TITLE_ARGS+=(-V title="$TITLE")
  PDF_TITLE_ARGS+=(-V author="$AUTHOR")
fi

# Optional per-book class options (e.g. "oneside,openany" for slim/single-sided books so the
# `book` class does not insert blank verso pages or force recto-only section starts). Default: none
# (book class default = twoside,openright — correct for thick novels). Opt in via BOOK_CLASSOPTION.
PDF_CLASSOPT=()
[ -n "${BOOK_CLASSOPTION:-}" ] && PDF_CLASSOPT=(-V classoption="$BOOK_CLASSOPTION")

# House colophon as the final page (ABP mark + Klaus crest, centred). Every book, unless NO_COLOPHON=1.
PDF_AFTER=()
if [ -z "${NO_COLOPHON:-}" ] && [ -f "$COLOPHON_LOGO" ]; then
  PDF_COLOPHON_TEX="$(mktemp -t abp-pdf-colophon).tex"
  {
    # Optical centring: anchor top glue with \null, weight the lower glue heavier so the marks
    # sit at the optical centre (slightly above mathematical middle), the classic colophon position.
    printf '\\clearpage\n\\thispagestyle{empty}\n\\null\\vskip 0pt plus 1fil\n\\begin{center}\n'
    printf '\\includegraphics[width=0.40\\textwidth]{%s}\n' "$COLOPHON_LOGO"
    # Klaus crest below the ABP mark — the Custos, non Conditor mark. Only if the asset exists and
    # not opted out; falls back to ABP-only cleanly otherwise.
    if [ -z "${NO_KLAUS:-}" ] && [ -f "$COLOPHON_KLAUS" ]; then
      printf '\\\\[2.4em]\n'
      printf '\\includegraphics[width=0.24\\textwidth]{%s}\n' "$COLOPHON_KLAUS"
      printf '\\\\[0.6em]\n{\\itshape Klaus}\\\\\n{\\footnotesize Custos, non Conditor}\n'
    fi
    printf '\\end{center}\n\\vskip 0pt plus 1.6fil\n'
  } > "$PDF_COLOPHON_TEX"
  PDF_AFTER=(--include-after-body "$PDF_COLOPHON_TEX")
fi

pandoc "$BOOK_MD" \
  -o "$OUT_BASE.pdf" \
  --pdf-engine=tectonic \
  --top-level-division=chapter \
  --lua-filter "$REPO/assets/dossier-div.lua" \
  -H "$PDF_HEADER" \
  ${PDF_BEFORE[@]+"${PDF_BEFORE[@]}"} \
  ${PDF_AFTER[@]+"${PDF_AFTER[@]}"} \
  -V documentclass=book \
  ${PDF_CLASSOPT[@]+"${PDF_CLASSOPT[@]}"} \
  -V geometry:paperwidth="$TRIM_W" -V geometry:paperheight="$TRIM_H" -V geometry:margin="$PDF_MARGIN" \
  -V fontsize=11pt \
  -V mainfont="$FONT_NAME" \
  -V lang=en-ZA \
  -V linkcolor=black \
  ${PDF_TITLE_ARGS[@]+"${PDF_TITLE_ARGS[@]}"}

rm -f "$PDF_HEADER"
[ -n "${PDF_COVER_TEX:-}" ] && rm -f "$PDF_COVER_TEX"
[ -n "${PDF_COLOPHON_TEX:-}" ] && rm -f "$PDF_COLOPHON_TEX"

# ---- Standing house rule (owner's directive 2026-07-29): every rendered EPUB gets symlinked into
# a single flat "latest-epubs" folder (sibling to this repo), so the current build of every book is
# always browsable/readable in one place without hunting through per-book build/export/ dirs.
# Opt out per-render with NO_LATEST_EPUB_LINK=1.
# Same rule for PDFs → latest-pdf/ (2026-07-31). Opt out: NO_LATEST_PDF_LINK=1.
LATEST_EPUBS_DIR="$(cd "$REPO/.." && pwd)/latest-epubs"
LATEST_PDFS_DIR="$(cd "$REPO/.." && pwd)/latest-pdf"
if [ -z "${NO_LATEST_EPUB_LINK:-}" ]; then
  mkdir -p "$LATEST_EPUBS_DIR"
  EPUB_ABS="$(cd "$(dirname "$OUT_BASE.epub")" && pwd)/$(basename "$OUT_BASE.epub")"
  LINK_NAME="$LATEST_EPUBS_DIR/$(basename "$OUT_BASE").epub"
  ln -sf "$EPUB_ABS" "$LINK_NAME"
  echo "  [latest-epubs] symlinked -> $LINK_NAME"
fi
if [ -z "${NO_LATEST_PDF_LINK:-}" ] && [ -f "$OUT_BASE.pdf" ]; then
  mkdir -p "$LATEST_PDFS_DIR"
  PDF_ABS="$(cd "$(dirname "$OUT_BASE.pdf")" && pwd)/$(basename "$OUT_BASE.pdf")"
  PDF_LINK="$LATEST_PDFS_DIR/$(basename "$OUT_BASE").pdf"
  ln -sf "$PDF_ABS" "$PDF_LINK"
  echo "  [latest-pdf] symlinked -> $PDF_LINK"
fi

echo "  [gate ok] $(basename "$OUT_BASE") — EPUB + PDF (Atkinson body; Courier Prime for The File)"
