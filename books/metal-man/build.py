#!/usr/bin/env python3
"""Merge The Metal Man manuscript into build/BOOK.md and build/chapters/.

Order comes from manuscript/ORDER.txt so the metal-register interstitials sit
between acts rather than sorting alphabetically. Text only — no binaries.
"""
import pathlib, shutil

ROOT = pathlib.Path(__file__).parent
MS, BUILD = ROOT / "manuscript", ROOT / "build"
CH = BUILD / "chapters"

order = [l.strip() for l in (MS / "ORDER.txt").read_text().splitlines() if l.strip()]
missing = [f for f in order if not (MS / f).exists()]
if missing:
    raise SystemExit(f"missing: {missing}")

if CH.exists():
    shutil.rmtree(CH)
CH.mkdir(parents=True)

parts = ["% The Metal Man", "% Andries J. Greyling", ""]
for name in order:
    body = (MS / name).read_text().rstrip()
    if name.startswith(("ch-", "metal-")):
        shutil.copy(MS / name, CH / name)
    parts.append(body)
    parts.append("\n\\newpage\n")

BUILD.mkdir(exist_ok=True)
(BUILD / "BOOK.md").write_text("\n".join(parts).rstrip() + "\n")

words = sum(len((MS / f).read_text().split()) for f in order if f.startswith(("ch-", "metal-")))
print(f"BOOK.md written · {len(order)} parts · {words:,} words of manuscript")
