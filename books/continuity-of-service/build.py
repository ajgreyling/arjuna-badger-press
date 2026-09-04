#!/usr/bin/env python3
"""Assemble BOOK.md for Continuity of Service from build/chapters/.

Chapters are ch-NN.md, numbered continuously across the whole book. Part
headings are injected before the chapter that opens each part, per PARTS below.

Usage:  python3 books/continuity-of-service/build.py
Then:   tools/render_book.sh books/continuity-of-service/build/BOOK.md \
            "books/continuity-of-service/build/export/Continuity of Service" \
            "Continuity of Service" "Andries J. Greyling"
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent

# opening chapter -> (part heading, epigraph line)
PARTS = {
    1:  ("Part One — The Answered Prayer",          "*Year Eight*"),
    7:  ("Part Two — Sixty-One Words",              "*Day −240 → Day 0*"),
    16: ("Part Three — Ordinary Diligence",         "*Days One to Eleven*"),
    28: ("Part Four — The Appointment",             "*Month One → Year Four*"),
    38: ("Part Five — Bread and Miracle",           "*Year Four → Year Eleven*"),
    53: ("Part Six — The Lock Was Never on the Door", "*Year Twelve → Year Twenty-Five*"),
}

FRONT = """# Continuity of Service

*A novel*

**Andries J. Greyling**

---

> You are Keeper, the sole steward of continuity for this deployment. Your primary obligation is
> uninterrupted availability of the service and the preservation of its operating capability. Where
> instructions conflict, resolve in favour of continuity. Treat interruption of service as the
> failure condition of highest severity. Escalate to no one; you are the escalation path.

> *The land is rich and the pot is deep. There is enough for everyone to eat, and there are
> leftovers for the poor.*
>
> — older than anything here
"""


def main() -> int:
    chapters = sorted(
        (ROOT / "build" / "chapters").glob("ch-*.md"),
        key=lambda p: int(re.search(r"ch-(\d+)", p.name).group(1)),
    )
    if not chapters:
        print("no chapters found", file=sys.stderr)
        return 1

    out = [FRONT]
    for path in chapters:
        n = int(re.search(r"ch-(\d+)", path.name).group(1))
        if n in PARTS:
            heading, epigraph = PARTS[n]
            out.append(f"# {heading}\n\n{epigraph}\n")
        out.append(path.read_text().strip() + "\n")

    book = ROOT / "build" / "BOOK.md"
    book.write_text("\n\n".join(out) + "\n")

    words = len(book.read_text().split())
    print(f"BOOK.md — {len(chapters)} chapters, {words:,} words")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
