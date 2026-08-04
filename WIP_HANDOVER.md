# WIP handover (arjuna-badger-press)

Pushed 2026-08-04 before local purge.

## On `master` (site-safe)
- New writing piece: Die Laaste Strooi (`site/content/writing/die-laaste-strooi.md` + build wiring + Safari background)
- Voynich canon + design (`books/voynich-manuscript/canon/`, `design/`)
- Audio pipeline source for Die Laaste Strooi Emma Masters: scripts, manifest, covers, chunk `.txt`/`.sha256`

## NOT in git (regenerate or restore from backup)
- `*.mp3` / `*.m4b` / `*.mp4` renders (gitignored; YouTube mp4 was ~332MB)
- `_work_m4b/`, `_work_youtube/`, `masters/`, chunk `.mp3` files
- `*.pre-polish.bak` chapter backups

## Resume
1. Clone repo
2. Re-run `site/content/writing/audio/render_die_laaste_strooi_emma.py` / `make_die_laaste_strooi_m4b.py` if media needed
3. `python site/build.py` for static site
