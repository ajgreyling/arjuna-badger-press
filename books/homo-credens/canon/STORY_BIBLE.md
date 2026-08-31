# Homo Credens — story bible

> Index and orientation for Book I of the *Homo Ter Probatus* box set.
> **Nothing in this canon folder is prose.** It is the apparatus around a manuscript that is
> already complete: 22 chapters, 201,645 words, drafted and assembled.

## Identity

**Homo Credens** — *A History of Religion, from the First Graves to 1900*
Book I of three. Andries J. Greyling / Arjuna Badger Press.

**Thesis:** religion is the technology by which strangers become kin.
**Stop line:** midnight, 31 December 1900.
**Register:** *Sapiens* × *The Knowledge* — big-idea narrative nonfiction with a maker's delight
in how things actually worked.
**Reader contract:** readable aloud at dinner, and survives a hostile fact-check. Both.

## The canon set

| File | Holds |
|---|---|
| [`SPINE.md`](SPINE.md) | The five acts, their turns, what each hands forward |
| [`CHAPTER_LEDGER.md`](CHAPTER_LEDGER.md) | 22 rows, measured: words, sections, claims, disputed, density |
| [`CANON_CHOICES.md`](CANON_CHOICES.md) | The 16 binding decisions and why each went that way |
| [`THEMES.md`](THEMES.md) | Recurring engines, traced to actual section headings; anti-themes |
| [`PLANTS_AND_PAYOFFS.md`](PLANTS_AND_PAYOFFS.md) | Setups within Credens and across the box set; debts outstanding |

## Pre-existing apparatus (not duplicated here)

| File | Holds |
|---|---|
| `../OUTLINE.md` | **Binding** 22-chapter master outline — the continuity law for chapter agents |
| `../STYLE.md` | Voice bible: cold opens, mechanism-delight, the never-invent-quotations rule |
| `../00-front-matter.md` | Title, epigraphs, how-to-read, thesis statement |
| `../../HOMO_CREDENS_SCAFFOLD.md` | **Estate→chapter map**: lucid.rodeo + press surfaces per chapter, Pilgrimage-era crosswalk |
| `../../HOMO_CREDENS_HANDOFF.md` | Agent pickup doc: paths, provenance, open items |
| `../backmatter/` | Bibliography + `refs-credens-1..5.json` |

`OUTLINE.md` and `STYLE.md` win on any conflict with this folder — they governed the drafting.

## Estate rails

Primary scripture rail: `../../corpus/*.jsonl` (28 traditions, PD, cited) + `study_bible.json`.
Never quote from memory (`CANON_CHOICES.md` #5).

Public surfaces: Study Bible (`/study`, 55 topics), Timeline (`/timeline`, 28 tradition nodes),
Origins Bible (`/bible/`), The Pilgrimage (`/pilgrimage/`, 10 eras / 45 stations — the
choose-path **twin form** of this linear history; Credens ends where its Era X begins).

Press companions are **secondary texture only**: *The Belly Hill* → ch-03, *The Walls of Uruk* →
ch-04, *The Engineer of the Gods* → ch-05, *The Song of the Self* → ch-06/10/18, *The Wrath of
Achilles* → ch-12, African Worlds apparatus → ch-05/08/14–16. Full table in the scaffold doc.

## State — done vs open

**Done:** full manuscript, outline, style bible, front matter, bibliography, structured refs,
estate→chapter map, box-set campaign draft, this canon set.

**Open, in the order I'd take them:**

1. **Re-verify the 52 disputed claims** — as *leads*, not verdicts. Two of three escalated
   "priority fixes" in `../../factcheck/SUMMARY.md` were wrong on inspection. Sort into real
   error / false positive / author's call.
2. **First-pass the unchecked chapters.** ch-15 (0.51 claims/1k), ch-17 (0.76), ch-16 (0.98),
   ch-18 (1.01). Zero disputed there means unread, not clean.
3. **Scan for cross-chapter drift** — `prose_tics.py` over `chapters/`. Never been run.
   22 single-shot agents on one outline is the setup that produced 120 duplicate sentences in
   *Prophet*.
4. **Commit the working copy.** `religion-src/homo-credens/` is untracked in `lucid-rodeo`;
   canonical trees live on `lucid-religion` branch `claude/study-bible-multiagent-adventure-1phsom`,
   and `main` there does not hold them.
5. **Decide the 20th-century gap** — see `PLANTS_AND_PAYOFFS.md`, debts outstanding.
6. **Print production:** art/LFS not in this sparse copy; campaign figures still bracketed.
