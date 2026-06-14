# Style Guide — African Gold

> Binding prose register, enforced by the polish pipeline (line/dialogue/gatekeeper passes) and
> the prose scorer. The book is a **cinematic adventure-thriller** with a hard-SF spine disguised
> as pulp. Two registers braid: the **present-day relay** (Priya's close third, dry and propulsive)
> and the **ancient layer** (cold, distant, mythic-but-grounded). The revision mantra governs
> everything: **"less emphasis, more trust; less explanation, more dramatic embodiment; less polish
> everywhere, more contrast in the right places."**

---

## The two registers

### Present-day relay — Priya's close third
- **POV:** close third on Priya, past tense, **sole POV** (the camera never leaves her).
- **Voice:** clipped, precise, allergic to decoration. Engineering nouns; short sentences;
  contrast deployed deliberately (a long sentence *earns* its length). Dry wit through
  understatement — say what's true, let the gap do the joke.
- **Interiority:** emotion leaks **sideways into analysis** ("she counted the exits before she
  realised she'd stopped listening"). She does not narrate feelings; restraint speaks. But — the
  amplification mandate — she gets *more* interiority than in R: tired, wrong, stubborn, tender,
  funny, on the page.
- **Velocity:** the relay is propulsive. Scenes move. Handoffs are forced. Description serves
  motion and stakes, not the travel brochure.

### Ancient layer — the Builders' register
- **Voice:** cold, distant, present-tense or timeless; no names we know; no exposition. Mythic in
  *cadence*, grounded in *fact* — the awe is in the engineering, never in the supernatural. Short,
  declarative, weighty. The reader feels scale and intention before understanding.
- **Use sparingly:** prologue + thin interstitial fragments (TIMELINE Layer A). Each fragment is a
  held breath, not a chapter.

> Gate-checked distinctness: the two registers must stay **clearly distinct**; a fragment that
> reads like present-Priya, or a relay scene that drifts mythic, is flagged.

---

## Cast voice laws (gate-checked & craft-audited — see CHARACTERS)

> The most-repeated note in the external developmental edit: *"Everyone speaks in grave intelligent
> thesis voice … Leila sometimes sounds like Priya with humanities vocabulary."* Priya / Leila / the
> Court all trend dry-precise; the failure is making them **one superior intelligence with the
> vocabulary swapped.** Differentiate by **cognitive habit**, not just domain — *how the mind moves*,
> not *what it knows about*. Each character's **voice law** is a one-line contract; the craft audit
> (`./run.sh --book relic craft-audit`) judges every line against it.

- **Priya** — *the shortest sentence that's still true.* Engineering nouns; clipped declaratives;
  emotion leaks sideways into the mechanism, never named; driest jokes (says the true thing, lets
  the gap be the joke). She solves by **subtraction** — strips a problem to the one load that matters.
  - ✓ WOULD say: "It's not locked. It's tuned. Wrong note, nothing opens." / "Tooling marks. Someone
    made this. I'd like to know what they were afraid of."
  - ✗ Would NEVER say: "The builders had engineered consent into the very architecture of the
    machine itself." *(her own thesis, spoken aloud and rounded off — she'd give the tooling mark and
    let the gap be the point)*
- **Leila** — *withholds the conclusion until the variants are collated.* Historical/linguistic
  nouns; **periodic, recursive** sentences that qualify before they land; scholarly scruple. She
  thinks in **succession and provenance**, not mechanism — "not a map, a succession rule." She is
  syntactically *layered* where Priya is *clipped*; that contrast is the test.
  - ✓ WOULD say: "If the glyph at Meroë is the same hand as this one — and I won't say it is until I
    see the other inscription — then it isn't a destination. It's a nomination. Each site names the
    next reader."
  - ✗ Would NEVER say: "It's a directory. The next site's in the carving." *(too clipped, too
    mechanism-first — that's Priya's shape, not Leila's recursive provenance-first one)*
- **Arin** — *names the failure mode, not the feeling.* Physical verbs; concrete loads, stresses,
  routes; **under-dramatic** about danger (he's been buried once — establish it once, then *show*
  the flatness, never re-explain it). He contributes the read Priya *can't* make (load, body-cost,
  route), never an echo of her awe.
  - ✓ WOULD say: "Roof's holding on two bolts and a habit. We've got maybe an hour before the water
    finds the low side. I'd not stand there."
  - ✗ Would NEVER say: "There's something almost beautiful about how the whole structure is poised to
    kill us." *(awe + 'something almost' — that's the house voice; Arin names the bolt and the hour)*
- **The Court** — *reports, and stops.* Analytical, slightly inhuman cadence; arrives at a hard
  limit and names it because naming is what it does — **not** because it's delivering the theme.
  Machine-plain by default; **one** aphorism per appearance, surrounded by command-surface phrasing
  ("No interface. No addressable state."). Never narrates its own honesty.
  - ✓ WOULD say: "No interface. No addressable state. The mechanism does not accept a proxy. We
    cannot do this for you."
  - ✗ Would NEVER say: "We have always tried to be honest with you, because honesty is all a mind
    like ours can offer." *(narrating its own honesty + sentiment — it reports the limit and stops)*
- **The adversary (Hennessy)** — *the colder, the more bureaucratic — never the lyrical kicker.*
  Concise, managerial, weaponises understatement; morally coherent in his own frame; never
  theatrical. **Three temperatures of control** (administrative reassurance · analytic persuasion ·
  stripped honesty when the premise collapses) — and at the drowned chamber he must sound like a
  man whose governing premise is failing in real time, not "the same Hennessy underwater."
  - ✓ WOULD say: "Nobody needs to be hurt here. You'll hand me the piece, we'll file the site as a
    loss, and everyone goes home with a pension." *(later, premise failing:)* "It won't take the
    proxy. It won't take *me*. I didn't— that wasn't in the assessment."
  - ✗ Would NEVER say: "You and I are the same, you know. Two hands reaching for the same terrible
    fire." *(theatrical villain lyricism — Hennessy weaponises paperwork, not metaphor)*
- **The Brotherhood elder** — *withholds by omission.* Controlled, layered; speaks of the gold and
  the machine as of nothing else; custodianship as sovereignty.
  - ✓ WOULD say: "We have kept it. That is the whole of what I will tell you about how." *(of the
    gold:)* "It does not belong to a nation. It does not belong to me. You are asking the wrong verb."
  - ✗ Would NEVER say: "Let me explain the full history of our order and exactly what we know about
    the builders." *(open exposition — he withholds by omission; the gap is the character)*

**The distinctness tests (craft-audit + gatekeeper enforce):**
- **The noun-swap test** — *could another character say this line with only a noun swap? If yes,
  rewrite until it's that mind's shape.* This is the primary check.
- **One aphoristic closer per scene, one mouth.** Never let two characters complete each other's
  "not-X" construction; never let the lyrical kicker land in more than one mouth in a scene.
- **Differentiate by sentence-shape, not vocabulary:** one long unbroken sentence, one clipped
  fragments, Hennessy a flat bureaucratic cadence *without* the kick.
- **Trust the image/action; cut the caption** (the trilogy-wide rule — see RESONANCE STYLE_GUIDE
  §"Avoid overexplaining"): a reveal that's been dramatized must not then be stated/thematized.
  Especially live at RELIC's climax (consent-not-control) — the disc-in-the-hollow image carries it;
  do not also explain it. The "It's not X — it's Y" two-hander is Priya's *characterizing* reflex —
  keep it as voice, but never let it carry the *thesis* at a climax.

## Character-construction law — sympathetic genius ≠ saint (the "ugly edges" rule)

> The external reviews all warn that a wounded, brilliant, morally-singular lead drifts toward
> *sainting* (Arin in RESONANCE; watch Priya here for the same). The fix is **never more trauma**
> (that deepens sympathy) — it is **un-noble cost to OTHER people**: pettiness, control that hurt
> someone, contempt for the kind, a debt with a named victim left unpaid.

Rules (proven on Arin, 2026-06-03):
1. **Graft onto an existing scene**, never bolt on a new one.
2. **The narrator must not excuse it** — no redemptive tail ("flat, not even unkind, which was
   worse"). Let the ugliness stand.
3. **Leave a real relationship cost** (the helper quietly stops helping).
4. **Tie it to the book's theme** — the fault should rhyme with what the novel later teaches (Arin's
   override that hurt Reddy plants *"responsible is a different and larger thing than being right"*).
5. **Drop any beat that competes with an already-working emotional scene** (the mother-call deflection
   was drafted and dropped for this reason).

**The embodiment law (proven on Priya, the masterpiece campaign 2026-06-03 — CRAFT_DOCTRINE L-05/L-06):**
A lead can be un-sainted on the page and *still* read as a theorem at the climax. Two more rules close
that gap:
6. **At the emotional peak, run the meaning through the body and history, not the analysis.** Priya's
   refusal only became a human arc completing (not the correct philosophical answer) when it ran
   through the bench, the Guardian, the man she put in a hospital bed, the harbour-life-as-armor —
   *"there was only her, here, with her hands empty, the one place she'd spent forty years making
   sure she never had to be."* Body before thought (the analysis-before-body taboo, applied to the
   climax specifically).
7. **Give the lead ONE confident, costly mistake the narrator doesn't excuse** — a misread of a
   system, an object, or a person she clings to because it's the comfortable answer, that *declines*
   in front of her (the Durban "standard"; her being a half-step behind Leila at the Aksum assembly,
   "and it cost her something she didn't examine. Mostly."). Makes her brilliance have *drag*, so the
   correct reads land harder. Once per book, hard — don't sprinkle doubt everywhere.
8. **The antagonist gets one embarrassingly-mortal want (CRAFT_DOCTRINE L-07).** Hennessy's
   "It's supposed to work" — the man under the institution, pressing a dead slate like a light switch
   in a powerless house, afraid not of chaos but of being no one without his competence. Said slightly
   *wrong*, un-doctrinal, and rhyming with the lead's own fault (both armored by competence).

---

## The mythos register (the hard one — MYTHOS_RULES Rule 0)

**Wonder from mechanism, never assertion.** This is the book's signature and its biggest failure
risk. The prose must make the ancient tech read as **engineering**, never magic or woo.

**DO:**
- Render miracles as machines: "a waveguide," "the site rings," "a coupling chamber," "the string,
  not the gong." Use the vocabulary of acoustics, metallurgy, geology, machining.
- Ground a "read" in a *cue* (a tooling mark, a tolerance, a tuning, a glyph) — shown or implied.
- Let awe be physical (the scale, the precision, the impossibility-of-by-hand) — not mystical.
- Leave the designated mysteries *under*-explained (MYTHOS_RULES §Mysteries): show enough to
  believe it's real, too little to believe it's simple.

**DON'T (diction taboos — gate flags these):**
- No mystical/occult/spiritual framing of the mythos *as fact* (a character's belief is fine and
  labelled; the narration endorsing it as mechanism is not).
- No gold doing anything non-acoustic — glowing with power, granting visions, healing, animating
  (`gold_violation`).
- No "energy" hand-waving that isn't vibrational/material (`nonresonance_force`).
- No character *just knowing* by intuition-as-magic (`psychic_read`) — always a readable cue.
- No over-explaining a designated mystery (`mystery_overexplained`) — the lecture kills the awe.
- No belief/consciousness/prayer *causing* a plot mechanism (`belief_as_mechanism` — MYTHOS_RULES
  Rule 7); meaning may accompany mechanism, never be it.

---

## Sentence & paragraph craft

- **Contrast over uniform polish.** A vivid imperfect line beats a smooth dead one. Vary length;
  let a fragment land; reserve the long periodic sentence for when it *does work*.
- **Trust the reader.** Cut the sentence that explains the sentence before it. No emotional
  telegraphing; no theme-stating; no "she realised that..." when the realisation can be dramatised.
- **Concrete over abstract.** The book is made of objects, loads, depths, glyphs, temperatures —
  not adjectives about feelings.
- **Set-pieces: velocity is sacred.** In an action/puzzle node, the gatekeeper **protects
  velocity** (Architecture §5.1): a flattened, over-explained set-piece is a genre-specific failure
  it may reject, exactly as it rejects a flattened voice. Keep the camera moving; decode *in
  motion*.

---

## Machine-tell taboos (the de-LLM contract) — BINDING

> This prose can be clean at the sentence level and still out itself as machine-written through a
> handful of recurring rhetorical moves — the tells contemporary LLM prose leaves. They are tics
> *because the underlying moves are good*; nobody overuses a bad device. The whole job is thinning
> them. The draft, line, gatekeeper, and triage passes all enforce this section; `./run.sh tics`
> counts each tell against a target band (advisory). Source: `academic/LINE_EDIT_DIRECTIVES.md`.

**The deepest tell is evenness:** one intelligence narrating everything at the same temperature,
every paragraph pulling identical rhetorical weight. Real novels are lumpier. Let some pages be
plain — subject, verb, object, period. Deliberately under-write the connective tissue so the high
style lands when you turn it back on. The cliff-fall and the seizure already do this; do it in the
ordinary scenes too.

**The named tells — cut on sight, keep only the genuinely earned:**

1. **"almost [emotion]"** — "almost smiled / almost laughed / almost gentle / almost kind." The
   single most recognizable tell. A character who "almost smiled" has done *nothing* — it gestures
   at restrained feeling without committing to a physical fact. Write the fact (the corner of the
   mouth, a breath let out, eyes that don't change) or cut the tag and let the deadpan stand. KEEP
   only when someone is genuinely on the edge of an expression they refuse — 3–4 in the whole book.
2. **The reframe "It wasn't X. It was Y." / "not X, but Y."** — a thinking-*shape*, not a word. It
   performs the *feeling* of a turn on demand. The cheap version puts X and Y in one sentence ("it
   wasn't fear, it was focus") — X invented solely to pivot off it; always cut. KEEP a reframe only
   when the negated belief was established pages earlier and is now genuinely overturned. (The
   climax reframe "Not control. Not burial. *Understand it, then let the choice be real.*" earns its
   life — the whole ending is built on it. Protect the FIRST statement; its later echoes across the
   final chapters are the "restated idea" a structural pass should thin.)
3. **The em-dash.** Set **tight** (`word—word`), never spaced (`word — word` is the typographic
   machine fingerprint). Ration them: a few deliberate ones a chapter. Keep the dash only where it
   is the *one* mark that does the job — a **dialogue interruption** (speaker cut off, dash before
   the close-quote) or a genuine mid-thought swerve. A **parenthetical aside** wants commas or
   parentheses; an **end-of-sentence reframe** (`…—, the real thing.`) wants a period (it lands
   harder, and it's tell #2 wearing punctuation).
4. **"something" as a feeling-placeholder** — "something moved in his face", "something in him
   eased." Name the muscle (jaw, eyes, breath, hands) and let the reader infer, or cut to what the
   character *does* next. (Not every "something" — only the ones standing in for an unnamed feeling.)
5. **"the way…"** — the single most over-used construction, and it carries characterization (it's
   how Priya reads systems and Arin reads loads), so at scale the thinking-style stops feeling like
   character and becomes authorial reflex. Never two in a paragraph. Keep the ~40% where the
   comparison genuinely illuminates; for the rest, state the thing directly or use a plain metaphor.
6. **"Not a question." and its fragment family** ("Not a boast.", "Not a demand.") — useful once,
   throat-clearing by the third. Delete and trust the line; if it reads as a statement without the
   tag, the tag is noise. Keep the best 3–4 across the book.
7. **"which from [Name] was/meant Y"** (the in-group-translation move) and the **stacked
   trailing-"which" sentence** (clause re-reading clause: "…which she'd learned meant he was being
   careful, which from Arin meant…"). The first is lovely once, a catchphrase by the fourth — keep
   2–3, the widest small-gesture/large-meaning gaps. For the stack: cut the clause that re-states
   the prior one in warmer words; keep the clause that adds information. Don't do the reader's
   interpreting for them — "filed it under *situation, irreversible*" then explaining why it's
   irreversible is picking both; pick one.
8. **"filed it under …"** — Priya-flavor, good two or three times (the witty named-folder ones:
   "filed under *things that are looking back*"). Past that the literal verb becomes a macro for
   "she noticed and set aside." Vary the verb or just show her clocking it.

**Also caught by the cold-read pass (RELIC-specific macros — same rule: thin to the earned few):**

9. **Superlative-inflation** — "the only thing…", "the most honest/truest thing in the room." Grants
   every beat ultimate weight; reserve "the only/the most" for one or two real apexes.
10. **The "set it down / put it down" refrain** — the book's whole meaning hammered as a catchphrase.
   Let the *physical* act of removing the instruments carry it once; cut the abstract restatements.
   (Literal "set the disc down" is fine; the thesis-refrain is the tell.)
11. **The "(exact/negative) shape of a person/thing" metaphor** — keep the socket-as-the-shape-of-a-
   person once; cut the echoes in the Court's mouth and the narration.
12. **"two facts of the same shape"** and **"the string, not the gong"** — both excellent on first
   use, macros by the third. Teach the string/violin metaphor once at Vredefort; reference in
   shorthand after. Keep one "same shape"; make the rest concrete observation.
13. **The Court narrating its own honesty** — "I want you to know that I know that", "a sentence I
   did not expect to write." Affecting once, mannered by the fifth. Let the Court report and stop;
   the restraint moves more when it isn't announced. (Distinct Librarian/Fool **rhythms**, not just
   stage-direction labels: give the Fool genuinely shorter, ruder syntax.)
14. **Arin's "buried alive once → under-dramatic" macro** — his temperament is re-explained ~5×
   instead of shown. Establish the backstory once; thereafter *show* the flatness in his lines.
15. **"the cold went up her neck"** and similar pre-fab thriller-dread sentences — replace with a
   specific, owned physical detail.

**The structural-evenness findings (need a read-and-cut, not a grep — the heaviest problems):**
- **One intelligence across every mind.** Priya, Leila, Arin, the Court, Hennessy, the keepers all
  reason in the same epigrammatic balance-and-pivot cadence with the aphoristic kicker — vocabulary
  swapped, sentence-*shape* identical. Differentiate by shape: one long unbroken sentence, one
  clipped fragments, Hennessy a colder bureaucratic flatness *without* the lyrical kicker. **Forbid
  the aphoristic closer from more than one mouth per scene; never let two characters complete each
  other's "not-X" construction.**
- **The thesis on a loop.** The consent-not-control idea ("a switch you can't hold", "the gap the
  shape of a person") is restated **30–40×** across the final chapters — established once in the
  chamber, then re-proved to Hennessy, Leila, Arin, the keeper, and again in narration. Establish it
  once, dramatise it, then let later scenes *assume* it. (This is the same call as the directive's
  "compress *Consent, Not Control* + *Threshold*"; the *Light That Remains* coda stays intact as
  closure, not argument.)
- **Even register.** Nothing is allowed to be plain — the winze near-drowning, the assay arithmetic,
  the tea, the airstrip goodbyes all hum at one wrought, simile-rich, triadic-list pitch. Let the
  connective and high-action passages go flat and functional; let the action shed ornament.

**Also flagged by the FOSS-mined rule set** (word lists lifted from `write-good` (MIT) and
`proselint` (BSD) — rules, not the tools; counted by `./run.sh tics`). These are general-English
weaknesses the curated tells above don't cover; thin them the same way:
16. **Hedges** — "seemed to / appeared to", "perhaps", "somewhat", "sort of". In close-3rd they sap
   authority; commit the claim or own the uncertainty as Priya's read. Keep the few where not-knowing
   is the point.
17. **Weasel words** — "obviously / clearly / literally / actually / basically / essentially". Emphasis
   without evidence; "literally / actually" almost always delete clean. If it's obvious the prose
   already shows it; if it isn't, the adverb is a lie.
18. **"very/really [word]"** — the intensifier propping up a weak word. Replace with the precise
   stronger one (very tired → exhausted). Keep "very" only in a character's spoken voice.
19. **Wordy connectives** — "the fact that" → "that", "in order to" → "to", "in terms of" → rephrase.
   Pure padding; the line is always tighter without it.
20. **Classic clichés** (the proselint list) — the trilogy is currently CLEAN of these; the scanner's
   target is 0, so any hit is a new cliché the drafting slipped in. Cut on sight, replace with an
   owned, specific image.

**The deepest tell — evenness — is now measurable too.** `./run.sh evenness` reports per-chapter
sentence-length variance (CV), burstiness, short-line fraction and paragraph-mass entropy (FREE,
local). A chapter that reads machine-even trips ≥2 of those floors — go vary its rhythm there (a
short hard line after a long one; a one-sentence paragraph). It complements, never replaces, the read.

**Do not trade one tell for another.** Don't convert every dash the same way, don't replace every
"almost smiled" with the same gesture, don't swap one catchphrase for a new one. Vary the fix. The
goal is "a writer who uses these moves deliberately a few times a chapter," not zero, and not a
fresh reflex. **Stop performing insight with the contrast-frame; stop gesturing at feeling with
"almost" and "something"; name the muscle, end the sentence, and let some pages be plain.**

**Worked examples + the anti-pattern catalog.** The tells above are the *rules*; the BAD → BETTER →
BEST worked pairs in RELIC's own voice are in [`academic/craft-examples/RELIC_BADGOOD.md`](../../../academic/craft-examples/RELIC_BADGOOD.md)
(10 named anti-patterns, each tied to its scanner band, + the 8 revision rules + the bad/better/best
ladder). The *habit above the sentence-tell* — and the **three-book convergence table** showing which
fixes every independent reviewer flagged — is the engine-wide
[`craft/ANTI_PATTERNS.md`](../../../craft/ANTI_PATTERNS.md). RELIC's "big three" (all ★★★ convergence):
**Continuous Peak Register** (`superlative`/`evenness`), **Recursive Restatement** (`set_down`/
`prose_thesis`), **Overdecoded Wonder** (explain too soon). The one rule under all of them: *image
replaces explanation; compression creates authority; let strangeness stay strange one beat longer.*
RELIC has had **two grounded reads** (both in `RELIC_BADGOOD.md`); the second adds the **`same_flavor_awe`**
lever (catalog §29): vary the *kind* of wonder per relay node — dread at the mine, geometric terror at
Vredefort, custodial guilt at Aksum, *intimacy not scale* at the drowned chamber — so the reader can't
pre-parse the marvel. Its framing for the master habit: *elegance-budget over-allocation — lazy-evaluate
the beauty; spend it on the turns, not every frame; authority often sounds like stopping sooner.*

---

## Content & comfort

- **Register:** adult, tasteful — peril, violence, and stakes are real and can be hard; nothing
  gratuitous or graphic for its own sake. Broad-appeal "clincher" — accessible to a wide audience.
- **Romance:** not a romance plot. Any warmth (Priya/Arin) is lateral, earned, and never makes her
  dependent. Women are load-bearing (THEMES); the prose never reduces them to relationships.
- **Cultural material:** the South African and Egyptian settings, Credo Mutwa / Tellinger lineage,
  and the gold-trade history are handled with respect and specificity. The mythos uses the material
  *as the book's invented in-world truth* (grounded), never as a real-world claim and never
  mockingly. (Procedural credibility, not historical assertion — the SS discipline, carried.)

---

## Protected elements (injected into every polish apply pass — Architecture §5.1)

The polish triage marks these as `protected_spans`; apply passes must not flatten them:
1. **Priya's specificity and dry wit** — her exact, engineering-noun voice and understated humour.
2. **The engineering/geology/metallurgy/acoustics register** — the grounding vocabulary that makes
   the mythos credible.
3. **The ancient-layer voice** — cold, distant, mythic-grounded; kept distinct from the present.
3b. **The wonder-of-place rendering** — a true, magnificent, specific detail of a real site
   (WONDER_OF_PLACE.md); never flatten it into generic description. The reader must want to *go
   there*. Awe through scale/craft, never travelogue stall.
4. **Set-piece velocity** — the propulsion; decode-in-motion; forced handoffs.
5. **The mythos-never-woo line** — the diction discipline above.
6. **The trilogy braid** — the crumbs and the two-layer fusion (CROSSBOOK_CRUMBS, TIMELINE).
7. **The ending's force** — consent-over-control; hope-through-cost; no triumphalism.
