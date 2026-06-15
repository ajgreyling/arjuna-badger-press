# The workshop — for authors & editors

> **What this is.** The companion to **[The technology](TECHNOLOGY.md)** — written for **published
> authors, working editors, and serious first-timers**, not for people who need to be taught what a
> chapter is. It explains what Arjuna Badger Press actually offers: a finish line for books that
> already have a soul, in **your** voice — with an engine that **measures and guards**, never replaces
> your prose.
>
> *The archer's eye. The badger's nerve.* — [arjunabadger.press](https://arjunabadger.press)

---

## 0. The one sentence

**You bring the book — however messy — answer twenty sharp questions, click Go, walk away for a day,
and come back to a manuscript that has been drafted, edited, continuity-checked, and merged to
print-ready; your job is the final proofread.**

That is not marketing copy. That is the shape the engine was built for.

---

## 1. This is not a beginner's toy

The free [Craft Library](craft/README.md) exists so anyone can learn degree-level craft without an MFA.
**The workshop is something else.**

It is for:

- **The debut author** who has never finished — but also for
- **The mid-career author** with a dozen markdown files, a blueprint, and no clean draft — and especially for
- **The established author** with published work, deep lore, a bloated draft, and a decade of notes
  scattered across formats — the Patrick Rothfuss problem, the George R. R. Martin problem, the
  *"I don't need ideas, I need finish"* problem.

If you have already sold books, you do not need us to teach you structure. You need a studio that can
**ingest what you already have**, lock a canon the pipeline can trust, run the editorial stack you
cannot afford to hire full-time, and hand you back something you are willing to sign.

The engine does not talk down to you. It reads your material, asks what only *you* can decide, and
does the labour you have been putting off since 2011.

---

## 2. What you bring (any shape, any mess)

Drop the whole pile. The workshop is designed to ingest:

| You have | Formats |
|---|---|
| Published or draft manuscripts | `.txt` · `.md` · `.pdf` · `.docx` · EPUB |
| Personal notes & lore bibles | markdown, Word docs, scribbled notebooks |
| Handwritten maps, timelines, character sheets | **photographs** (scanned or phone pictures) |
| Partial chapters, alternate versions, cut scenes | all of the above, together |

You do not need to normalise it first. That is the importer's job — map your material onto a locked
**canon contract** (characters, timeline, world rules, style, blueprint) that every downstream pass
obeys.

Three front doors, one back end:

```
  NEWCOMER ─┐   spark of an idea, no draft yet
  MIDDLE  ──┼──►  LOCKED CANON  ──►  PIPELINE  ──►  PRINT-READY BOOK
  ROTHFUSS ─┘   published work + lore dump + bloated MS
```

- **Newcomer** — the **wizard**: a guided Q&A that builds the canon from your answers (already exists
  in the engine as `engine/wizard.py`; the web flow is the thin layer still to wrap).
- **Middle** — the **importer**: your messy markdown pile → canon contract + gap report + a short
  follow-up wizard for the holes (`engine/import_canon.py` — built).
- **Rothfuss** — the **ingester**: your finished (or over-long) manuscript + notes → reverse-engineered
  canon from the prose, continuity graph, finish report, surgical path to done
  (`engine/ingest_manuscript.py`, `engine/reverse_canon.py` — built).

After the canon locks, **every author gets the same engine** — outline, draft, multi-role polish,
continuity audit, hard graph gate, de-LLM scanners, merge to EPUB/PDF.

---

## 3. The flow you actually experience

### Step 1 — Upload & ingest

You provide the books, the notes, the pictures. The system reads them, chunks scenes, extracts
characters, places, timeline, and world rules into a **story bible** you can review.

### Step 2 — The wizard (≈20 questions)

Not a hundred-page form. A focused interview — the forks only *you* can answer:

- Whose story is this, and what do they want vs. what do they need?
- What is the one sentence a reader would repeat?
- What must never change (names, history, voice laws)?
- Where does the draft bloat, sag, or break continuity?

The wizard **proposes options at each fork; you choose**. The model does not get to both propose and
decide. That rule is why the output still sounds like a person.

### Step 3 — Click Go

The pipeline runs checkpointed and resumable: draft chapter by chapter, polish with a six-role
editorial stack, continuity audit, **hard block** on any graph violation, score against craft
targets, merge. You do not babysit it.

### Step 4 — Come back (~24 hours)

You return to a merged manuscript — structurally sound, continuity-clean, machine-tell scanned —
ready for **your** proofread. Not "AI slop you must hide." A book that survived gates a human
editorial team would charge six figures to approximate.

**Your last job is authorial:** read it, cut what only you would cut, sign it.

---

## 4. What we never do (the line that matters)

**The engine measures and alarms. It does not replace your voice.**

- We do **not** ghost-write Rothfuss's prose and hand him different sentences.
- We **do** show him where the bloat is, where the timeline breaks, where the key-chain stalls —
  and run the finish pipeline on the cuts *he* approves.
- We do **not** let the model drive; a human seed plus surgical edits authors the soul.
- We **do** let the gatekeeper reject a flattened polish pass and fall back to the stronger draft.

That invariant is why established authors can trust it with work that already has an audience.

The **de-LLM layer** names and counts the sentence-level tells — **"Not X. Y."** reframes, **em-dash**
chains, **"the way…"** similes, even cadence, AI vocabulary clusters — so your voice survives
thinning, not replacement. See the full catalog with BAD→GOOD examples:

→ [**LLM tics & tells**](craft/LLM_TELLS.md) · Engineers: **[The technology](TECHNOLOGY.md)** · **[Craft Glossary](craft/CRAFT_GLOSSARY.md)**

---

## 5. What is built vs. what is left

**Honest inventory (2026):**

**Built today (the engine — this catalogue is the proof):**

- Canon wizard (terminal Q&A) — `./book new`
- Canon importer + gap report
- Manuscript ingester + reverse-canon
- Full draft → polish → gate → merge pipeline
- StoryGraph continuity gate (hard block)
- de-LLM scanners + cold-read + craft audit
- Finish report for bloated manuscripts

**Thin wrapper left (trivial relative to the above):**

- Web upload UI — drag-and-drop your pile
- Web wizard — ~20 questions in the browser (port of existing terminal flow)
- "Click Go" project dashboard — progress over a ~24h run

The **engine exists and works.** The library you are reading is twenty finished novels worth of
evidence. What remains is packaging — auth, upload, a browser on the wizard, a progress bar — not
inventing the creative stack from scratch. That remaining work is **trivial relative to what is
already shipped.**

---

## 6. For editors

If you edit professionally, think of the workshop as **the editorial department you always wanted
automated**:

- **Developmental** — structure, spine, relay/key-chain, arc conformance (scored, not guessed)
- **Line** — rhythm, filter words, machine-tells, voice homogenization (named, counted, targeted)
- **Continuity** — geospatial-temporal graph gate; violations are precise, not vague "something
  feels off"
- **Copy-level correctness** — verification gate for factual claims + both sides of contested history

The tools produce **reports and blocks**, not rewrites. You stay the judge; the engine is the
microscope.

---

## 7. Write with us

The workshop is opening in tiers. If you have a manuscript in the drawer — or a series the world
has been waiting on — [get in touch](https://arjunabadger.press#write).

Bring the pile. Answer twenty questions. Click Go.

---

*Companion docs:* [The Press Thesis](THE_PRESS_THESIS.md) (unifying argument) · [The technology](TECHNOLOGY.md) (engineering) · [Craft Library](craft/README.md) (free craft reference) · [Verification Gate](VERIFICATION_GATE.md) (accuracy standard)
