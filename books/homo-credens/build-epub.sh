#!/bin/sh
# Render "Homo Credens.epub" from front matter + art plates + chapters + backmatter.
# Repeatable: run from anywhere; requires pandoc + sips (macOS). Degrades gracefully —
# any chapter vignette or backmatter file that doesn't exist yet is simply skipped.
# Images are re-encoded into art/epub-cache/ (1000px JPEG q78) to keep epub size sane —
# the epub-cache is derived/disposable, safe to delete and regenerate.
set -e
cd "$(dirname "$0")"

mkdir -p art/epub-cache
cache() {  # cache <source-png-or-jpg> -> echoes cached jpg path (relative)
  src="$1"
  [ -f "$src" ] || return 1
  key=$(echo "$src" | tr '/' '-')
  out="art/epub-cache/$key.jpg"
  case "$out" in *.jpg.jpg) out="art/epub-cache/$key" ;; esac
  if [ ! -f "$out" ] || [ "$src" -nt "$out" ]; then
    sips -s format jpeg -s formatOptions 78 --resampleWidth 1000 "$src" --out "$out" >/dev/null 2>&1
  fi
  echo "$out"
}

BUILD=$(mktemp -d -t hc-epub)
trap 'rm -rf "$BUILD"' EXIT

# Front matter + the three standalone plates
cp 00-front-matter.md "$BUILD/00-front.md"
{
  echo
  echo "---"
  echo
  for spec in "art/endpaper-armillary.png|The armillary of the heavens — endpaper" \
              "art/symbology.png|The Signs of the Faiths — the 28 traditions" \
              "art/timeline-rivers-of-faith.png|The Rivers of Faith — five millennia in one delta"; do
    src="${spec%%|*}"; cap="${spec##*|}"
    img=$(cache "$src") || continue
    echo "![$cap]($(pwd)/$img)"
    echo
  done
} > "$BUILD/01-plates.md"

# Chapters, each with its vignette inlined under the heading if it exists
i=10
for f in chapters/ch-*.md; do
  n=$(basename "$f" | sed -E 's/ch-([0-9]+)-.*/\1/')
  out="$BUILD/$(printf '%02d' $i)-$(basename "$f")"
  vin=$(cache "art/ch-${n}-vignette.png" 2>/dev/null) || true
  if [ -n "$vin" ]; then
    awk -v img="$(pwd)/$vin" 'NR==1{print; print ""; print "!["img"]("img")"; print ""; next} 1' "$f" > "$out"
  else
    cp "$f" "$out"
  fi
  i=$((i + 1))
done

# PD artifact gallery, if the picture-research pass has landed
if [ -d art/pd ]; then
  {
    echo "# Plates — Artifacts, Sites & Places"
    echo
    echo "*Photographic plates below are public-domain or CC0 images of real artifacts,"
    echo "sites, and places discussed in this book — see Image Credits for sources.*"
    for part in art/pd/part-*/; do
      for img in "$part"*.jpg "$part"*.jpeg "$part"*.png; do
        [ -f "$img" ] || continue
        name=$(basename "$img" | sed -E 's/\.[^.]+$//; s/-/ /g')
        c=$(cache "$img") || continue
        echo
        echo "![$name]($(pwd)/$c)"
      done
    done
  } > "$BUILD/90-plates-gallery.md"
fi

# Bibliography + image credits backmatter
if [ -f backmatter/BIBLIOGRAPHY.md ]; then
  cp backmatter/BIBLIOGRAPHY.md "$BUILD/95-bibliography.md"
fi
if [ -d art/pd ]; then
  {
    echo "# Image Credits"
    echo
    echo "The engraved plates and chapter vignettes are original artwork made for this"
    echo "edition. The photographic plates are public-domain or CC0 images via Wikimedia"
    echo "Commons:"
    for f in art/pd/part-*/CREDITS.md; do
      [ -f "$f" ] || continue
      echo
      cat "$f"
    done
  } > "$BUILD/96-image-credits.md"
fi

COVER_JPG=$(cache art/cover.png)

pandoc "$BUILD"/*.md \
  -o "Homo Credens.epub" \
  --epub-cover-image="$COVER_JPG" \
  --toc --toc-depth=1 \
  --metadata title="Homo Credens" \
  --metadata subtitle="A History of Religion, from the First Graves to 1900 — The Illustrated Edition" \
  --metadata author="Arjuna Badger" \
  --metadata publisher="Arjuna Badger Press" \
  --metadata rights="© 2026 Arjuna Badger Press" \
  --metadata lang=en-US

echo "rendered: $(pwd)/Homo Credens.epub ($(du -h "Homo Credens.epub" | cut -f1))"
