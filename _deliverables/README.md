# Deliverables — latest EPUB / PDF / narrator briefs

> **Symlinks, not copies.** Every file here is a symbolic link to the **newest** build of that title
> across both repos (`africangold` = engine/source, `arjuna-badger-press` = library/site). When a
> book is rebuilt, the link automatically points at the fresh file — nothing to re-copy.

## Layout

| Folder | What |
|---|---|
| `ebooks/` | The latest **EPUB** of each of the 20 published titles. |
| `pdfs/` | The latest **PDF** of each of the 20 published titles. |
| `narrator-briefs/` | The audiobook narrator briefs (`.pdf` + `.md`) for *The Calendar of Stone* and *The Engineer of the Gods*. |

## How it was built / to refresh

Run `tools/refresh_deliverables.sh` (re-scans both repos, points each link at the newest copy by
modification time). Safe to re-run anytime; it only rewrites the links, never the source files.

## Notes

- These are **symlinks** — copying this folder elsewhere may not carry the targets. To get real
  copies (e.g. to email or upload), use `cp -L` (follow links): `cp -L _deliverables/pdfs/*.pdf /dest/`.
- The source files live in each book's `build/export/` (or companions' `export/`). The links resolve
  to whichever repo holds the freshest build — e.g. *The Loneliest People in the World* points at the
  copy with the restored "The File" dossier styling.
