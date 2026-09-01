# Homo Credens — chapter ledger

> One row per chapter. **Every number here is measured from the manuscript and the factcheck
> run, not estimated.** Word counts from `chapters/*.md`; claims and disputed counts from
> `../../factcheck/report-all.jsonl` (rows where `book == "book"`).
>
> Regenerate rather than hand-edit — the extraction is a dozen lines of Python over those two
> sources, and a hand-maintained ledger goes stale the first time a chapter is touched.

**Totals:** 22 chapters · **201,645 words** · 540 checked claims · 52 disputed *as of the
2026-08-05 run* — of which **26 are now outstanding**.
(`BOOK.md` assembles to ~206,846 words with front matter.)

> **The Disputed column below is stale.** It reports the 2026-08-05 factcheck. A correction pass
> has since been run over the manuscript and closed 26 of the 52 rows without recording itself
> anywhere. Triage, per-row, with the reasoning: [`../../factcheck/CREDENS_DISPUTED_TRIAGE.md`](../../factcheck/CREDENS_DISPUTED_TRIAGE.md).
>
> Outstanding by chapter (2026-08-13): ch-13 **6** · ch-14 **3** · ch-20 **3** · ch-09 2 ·
> ch-11 2 · ch-19 2 · ch-21 2 · ch-22 2 · ch-01 1 · ch-05 1 · ch-07 1 · ch-08 1 · ch-12 0 · ch-18 **0**.
>
> Of those 26, the triage finds **no confirmed factual error** — 22 are checker artifacts (claims
> extracted without their antecedent, then "corrected" to a different person or event) and 4 are
> author's calls. Do not apply the checker's corrections mechanically; see the Tyndale case.

| Ch | Title | Era | Words | §§ | Claims | Disputed | Claims/1k |
|---:|---|---|---:|---:|---:|---:|---:|
| 01 | The Believing Animal | ~300,000–40,000 BCE | 7,541 | 7 | 9 | 1 | 1.19 |
| 02 | The First Graves | ~100,000–12,000 BCE | 7,750 | 7 | 22 | 0 | 2.84 |
| 03 | The Temple Before the Town | ~10,000–4,000 BCE | 7,645 | 6 | 17 | 0 | 2.22 |
| 04 | Gods with Ledgers | Sumer & Akkad | 10,428 | 8 | 21 | 0 | 2.01 |
| 05 | The Kingdom That Refused to Die | Egypt | 9,610 | 7 | 23 | **3** | 2.39 |
| 06 | Fire and Song | Vedic India / early Iran | 9,508 | 8 | 12 | 0 | 1.26 |
| 07 | The Ancestors Are Watching | Shang & Zhou | 7,443 | 7 | 9 | 1 | 1.21 |
| 08 | A Storm God's Ambition | Canaan & Israel | 9,473 | 8 | 42 | **3** | 4.43 |
| 09 | The Great Interrogation | Axial Age | 7,943 | 7 | 28 | **5** | 3.53 |
| 10 | The Man Who Woke Up | Buddha / Mahavira | 9,653 | 8 | 15 | 0 | 1.55 |
| 11 | The Master and the Way | Confucius / Laozi | 9,979 | 8 | 25 | **3** | 2.51 |
| 12 | Wine-Dark Gods | Greece | 8,551 | 7 | 12 | 1 | 1.40 |
| 13 | By the Rivers of Babylon | Exile & monotheism | 9,677 | 8 | 29 | **6** | 3.00 |
| 14 | The Kingdom of Nobodies | Jesus to Paul | 8,383 | 8 | 26 | **4** | 3.10 |
| 15 | The Empire Baptized | Christianity takes Rome | 9,731 | 6 | 5 | 0 | **0.51** |
| 16 | The Recitation | Islam | 9,155 | 8 | 9 | 0 | 0.98 |
| 17 | The Long Argument of Christendom | Medieval Christendom | 10,471 | 8 | 8 | 0 | **0.76** |
| 18 | The Dharma's Long March | Buddhism/Hinduism across Asia | 8,888 | 8 | 9 | **3** | **1.01** |
| 19 | Blood of the Sun | Unconnected world + contact | 9,131 | 6 | 35 | **4** | 3.83 |
| 20 | The Broken Body of Christ | Reformation & wars | 11,483 | 8 | 77 | **10** | 6.71 |
| 21 | The Clockmaker's Universe | Enlightenment | 10,397 | 7 | 72 | **4** | 6.93 |
| 22 | The Twilight of the Gods | Long 19th c. → 31 Dec 1900 | 8,805 | 7 | 35 | **4** | 3.98 |

---

## What the ledger exposes

**Fact-check coverage is wildly uneven, and the disputed count hides it.** Claim density runs
from **0.51/1k** (ch-15) to **6.93/1k** (ch-21) — a **13× spread**. The three hottest chapters by
raw disputed count (ch-20 with 10, ch-13 with 6, ch-09 with 5) are hot partly *because they were
checked hardest*. ch-20 and ch-21 alone carry **149 of the 540 claims** — 28% of the checking on
10% of the chapters.

~~The inverse is the real risk. **ch-15 (5 claims across 9,731 words), ch-17 (8 across 10,471), and
ch-16 (9 across 9,155)** are near-unchecked.~~ **Diagnosed and closed 2026-08-13.** The cause was
mechanical, not editorial: `extract_claims.py` matched bare years only from 1500 up, so the
100–1500 CE chapters were nearly invisible to it. Real coverage was ch-15 **11%**, ch-17 **11%**,
ch-16 24%, ch-18 28%, against ~100% for ch-20/21/22.

Regex fixed and those four re-run on 2026-08-13 — **186 claims, 0 errors, 0 confirmed factual
errors** (83.9% CONFIRMED, 12.9% IMPRECISE, 5 DISPUTED all of which triage as false positives).
Post-fix claim counts: ch-15 **46**, ch-16 **37**, ch-17 **71**, ch-18 **32**. Details in
[`../../factcheck/CREDENS_DISPUTED_TRIAGE.md`](../../factcheck/CREDENS_DISPUTED_TRIAGE.md).

**The Claims column below is therefore obsolete for every chapter.** Whole-book extraction now
yields **733** claims, not 540. Only ch-15/16/17/18 have been re-verified against the new set; the
other 18 chapters still carry 2026-08-05 verdicts taken at their old coverage.

~~**ch-18 is the quiet outlier:** 3 disputed out of only 9 claims — a **33% dispute rate**, the
worst ratio in the book.~~ **Resolved.** All three ch-18 rows were fixed in the correction pass
(including the Kumārajīva arrival, 402 → **401 CE**). ch-18 now sits at 0 disputed. Its thin
claim count — 9 across 8,888 words — makes it an under-coverage chapter, not a dispute-rate one,
which puts it in the same bucket as ch-15/16/17 below.

**ch-13 is now the hottest chapter, at 6 of 26** — untouched by the correction pass, where ch-20
fell from 10 to 3. Note that the triage grades all six ch-13 rows as checker artifacts, so "hot"
here means *unreviewed*, not *wrong*.

## Before acting on any disputed row

Two of the three escalated "priority fixes" in `../../factcheck/SUMMARY.md` were **wrong** when
checked against the source (both in *Benignus* ch-03: one misidentified Tajfel's minimal-group
experiment as the Stanford Prison Experiment, the other flagged a correct sentence and then
reproduced it verbatim as its own "correction").

**Treat every flag as a lead, not a verdict.** Re-verify against the surrounding text before
changing a word. Sort outcomes into *real error* / *false positive* / *needs author's call*.

## Structural note

Section counts sit at 6–8 per chapter, matching `../STYLE.md`'s "4–7 titled sections" spec —
slightly over at the top end. Chapter lengths run 7,443–11,483 words (mean ~9,166).
