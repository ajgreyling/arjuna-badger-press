# LLM tics & tells — the de-LLM catalog

> **Companion to the [Craft Glossary](CRAFT_GLOSSARY.md)** — the named sentence-level habits that
> make prose read as machine-written. Each tell below links to a full explainer; this page is the
> quick catalog with **BAD → GOOD** examples you can self-audit against.
>
> The studio counts these deterministically (`./run.sh tics`) and hunts them in the de-LLM loop —
> not to ban rhetoric, but to restore **modulation**: plain where plain belongs, sharp where sharp
> earns it.

---

## 0. What a "tell" is

A **tic** is a small recurring habit — yours or the model's. An **LLM tell** is a tic so common in
AI prose that readers feel the machinery even when they cannot name it.

The deepest tells are not individual words. They are **statistical habits**:

- mathematically **even** cadence (every sentence the same weight)
- **uniform gravitas** (nothing allowed to be throwaway)
- prose from **nowhere** (no situated speaker with a stake)
- compulsive **over-significance** (everything "underscores" something)

The word-lists below are **symptoms**. Fix the rhythm and stance; the words often fall away on their
own.

→ Full theory: [Tic / machine-tell / LLM tell](terms/tic-machine-tell-llm-tell.md) · [Evenness of register](terms/evenness-of-register.md) · [The root cause: no situated speaker](terms/the-root-cause-no-situated-speaker.md)

---

## 1. The headline tells (hunt these first)

### "Not X. Y." / "Not X, but Y." — the reframe

The model's default way of sounding deep. Powerful **once**; a tell in bulk (~6% of ChatGPT output
uses a "not just X, but Y" variant).

**BAD:** *It wasn't fear. It was recognition.*  
**GOOD:** *Her hands stopped shaking. She knew that face.*

**BAD:** *Not just a tunnel — a machine.*  
**GOOD:** *The tunnel was a machine.*

**BAD:** *No panic, no flinch — just focus.*  
**GOOD:** *She focused.*

→ [Negative parallelism / the reframe](terms/negative-parallelism-the-reframe.md) · [Reframe device](terms/reframe.md)

---

### Em-dash addiction

The dash doing a comma's or full stop's job — every sentence interrupted, nothing allowed to end
cleanly.

**BAD:** *She opened the door — the hinge screamed — and stepped inside — the air cold — older than the stone.*  
**GOOD:** *She opened the door. The hinge screamed. The air inside was cold and old.*

**BAD:** *He wasn't angry — not exactly — more tired than anything — though tired wasn't the word.*  
**GOOD:** *He looked tired. That wasn't the word, but it would do for now.*

**Rule:** Reserve the em dash for genuine interruption or apposition. Track density per book.

→ [Em-dash & punctuation tics](terms/em-dash-punctuation-tics.md)

---

### "The way…" — the simile template

Often the **single most over-used construction** in AI prose: *the way a [noun] [verbs]*, repeated
until every comparison sounds stamped from the same die.

**BAD:** *The silence settled the way dust settles on unused furniture.*  
**GOOD:** *The silence settled.*

**BAD:** *He moved the way a man moves when he already knows the answer.*  
**GOOD:** *He moved like he already knew.*

**BAD:** *It hit her the way bad news always hits — slow, then all at once.*  
**GOOD:** *Bad news. She felt it in her teeth first.*

**Rule:** Cut roughly half. Keep the ~40% where the comparison **only that comparison** could carry
the meaning. Else state the thing directly.

→ [The "the way…" simile](terms/the-way-simile.md)

---

### Even cadence / gravitas inflation

Every sentence the same length and weight; every moment made profound; nothing plain.

**BAD:** *The chamber was ancient. The stone was patient. The air was heavy with meaning.*  
**GOOD:** *The chamber was old. Dust. A drip somewhere she couldn't see.*

**BAD:** *She understood, in that moment, the true cost of knowing.*  
**GOOD:** *She wished she didn't know.*

→ [Cadence](terms/cadence.md) · [Gravitas / evenness of register](terms/gravitas-evenness-of-register.md) · [Modulation](terms/modulation.md)

---

## 2. Vocabulary & construction tells

- **AI vocabulary cluster** — *delve, tapestry, underscore, pivotal, nuanced, landscape, foster, nestled…* → Rewrite for specificity; not a banned-word purge. → [The "AI vocabulary" cluster](terms/the-ai-vocabulary-cluster.md)
- **Rule of three** — three adjectives, three parallel clauses, everywhere → Break the rhythm. → [Rule-of-three overuse](terms/rule-of-three-overuse.md)
- **Verb-of-significance** — *serves as, stands as, represents* → Plain *is/was*; dramatize instead. → ["Serves as / stands as"](terms/serves-as-stands-as-represents.md)
- **Caption tell** — show, then explain what you showed → Trust the reader. → [Over-explanation](terms/over-explanation-the-caption-tell.md)
- **The hedge** — *ultimately, in many ways…* → End on the image, not a summary. → [The hedge](terms/the-hedge-the-gentle-wrap-up.md)
- **Generic over specific** — smooth abstraction replaces the odd true detail → Restore the precise noun. → [Generic over specific](terms/generic-over-specific.md)
- **Frictionless transitions** — every paragraph topic-sentence → support → tidy close → Allow hard cuts. → [Frictionless transitions](terms/frictionless-transitions-textbook-paragraphing.md)

---

## 3. The self-audit (one pass)

Read a chapter aloud. Flag any paragraph where:

1. **More than one** "Not X…" reframe appears
2. **More than two** em dashes in five lines
3. **"The way"** appears twice on the same page
4. **Every sentence** is roughly the same length
5. A line **states what the previous line already showed**

Cut or rewrite the worst three instances. Re-read. Stop when only **earned** rhetoric remains.

→ [The one revision rule](terms/the-one-revision-rule.md) · [Anti-Patterns](ANTI_PATTERNS.md) (structural habits above the sentence)

---

## 4. What the workshop does with tells

The engine does **not** silently rewrite your voice. It:

- **counts** each tell band against per-book targets
- **flags** clusters in finish reports and cold-reads
- **blocks** only when craft gates fail (continuity, mythos — separate from tics)
- leaves **surgical cuts** to the author (or author-approved edit passes)

That is why a Rothfuss-tier manuscript can run through the pipeline and still sound like Rothfuss —
the tells are measured and thinned, not replaced with generic "humanizer" slop.

→ [The workshop — for authors & editors](../FOR_AUTHORS.md) · [The technology](../TECHNOLOGY.md) (de-LLM loop)

---

*Back to the [Craft Glossary](CRAFT_GLOSSARY.md) · [Craft Library overview](README.md)*
