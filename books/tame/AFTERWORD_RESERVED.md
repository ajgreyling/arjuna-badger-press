# AFTERWORD — reserved for the author

**This is not the afterword. It is a placeholder, and it is deliberately outside `manuscript/`.**

Under **L-19** the afterword is written by AJ Greyling in his own voice. The machine may **edit
only**, and never drafts, outlines, suggests or ghost-writes a line of it. **The last word in the
book is the author's**, in every edition and format.

## Why this file is here and not at `manuscript/AFTERWORD.md`

`books/tame/build.py` concatenates `manuscript/AFTERWORD.md` into `build/BOOK.md` and from there
into the EPUB and the PDF. A stub placed at that path — even a stub that says *reserved* — would
put machine-written words in the position L-19 reserves for the author, in every built artifact.
That is the one arrangement the lock names as unacceptable.

So the reservation lives here, where it is visible to anybody opening the book folder and cannot
reach a reader. The build's own warning is the gate:

```
[L-19] not yet written: AFTERWORD.md — required before any edition ships
```

That line prints on every build and will keep printing until the author writes the file himself.

## When the author writes it

Create `books/tame/manuscript/AFTERWORD.md`, in his own words, and delete this file. The build will
pick it up and the warning will stop.

## What is deliberately absent from this repository

Nothing in `canon/`, `manuscript/` or `PROVENANCE.md` anticipates the afterword's content, argument,
length, structure or opening line. No note was left for him to react to. The drafting agent did not
write one and then discard it; it was never begun.

*Recorded 2026-08-24 by Claude Opus 5 (`claude-opus-5`) at the end of the drafting run. See
`PROVENANCE.md`.*
