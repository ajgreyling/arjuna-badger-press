# Craft Anti-Patterns — the engine's named-smell catalog (book-agnostic)

The **generative** craft contract for the trilogy engine: a catalog of recurring literary
anti-patterns — named like software smells (Name · Why it's bad · BAD · GOOD · Craft motivation) —
that the engine must **design out at draft and outline time**, not merely clean up afterward. This
sits beside the *sentence-level* tells in [`CRAFT_GLOSSARY.md`](CRAFT_GLOSSARY.md) (Pitfalls) and
the per-book worked-line banks the studio maintains privately. Those catch the *phrase*; this catches the *habit above the phrase* — the protagonist who is
always right, the scene that explains itself, the world that is omniscient when convenient.

**Provenance.** Synthesized from **three independent external developmental reads — one per book** —
all framed as software-smell reviews (REVELATION 2026-06-03; RELIC 2026-06-03 "brutal code-review";
RESONANCE line-level, see `academic/craft-examples/RESONANCE_BADGOOD.md`). The worked snippets vary by
book, but the *anti-patterns are cross-book law* — they describe any protagonist-driven intelligent
thriller, so the whole trilogy (and any future book) inherits them. The prior per-book developmental
edits (`academic/external-editorial-feedback/*.md`) are already encoded into each book's voice laws;
this catalog adds the *named taxonomy*, the generative outline-level discipline, the five-pass
protocol, and — most important — the **three-book convergence table** (below) that ranks which fixes
the engine must prioritize because every independent reviewer flagged them. Per-book *verbatim* worked
banks: `academic/craft-examples/{RESONANCE,REVELATION,RELIC}_BADGOOD.md`.

**Where each smell is enforced** (the layer that can actually prevent it):
- **OUTLINE-level** smells must be designed out before a word is drafted → `prompts/outline.md`
  (friction, reveal-variety, support-character cross-purposes, asymmetry, capped reveal-nesting).
- **DRAFT-level** smells are generative habits → `prompts/draft-chapter.md` (the prose is written
  to avoid them in the first place).
- **EDIT-level** smells are caught by the diagnosis/cleanup loop → `prompts/polish-triage.md`,
  `polish-line-apply.md`, `prompts/de-llm-pass.md`, the craft audit.

> **The one master rule** (it subsumes a third of the list — see §16): *you have the scene, the
> object, the pattern — then you add the sentence that explains what it means. That sentence is
> usually the cut.* **Trust drama over explanation; trust character limitation over protagonist
> brilliance.** That is the leap from "excellent intelligent manuscript" to "novel that lives."

---

## 1 · Competence Porn Cascade  · `competence_cascade` · OUTLINE + DRAFT

**Smell:** Every scene proves the protagonist is the smartest person in the room. She *instantly*
notices the hidden relay, the cropped margin, the forged transliteration, the staple-shadow, the
institutional tone — every level, no misses.
**Why it's bad:** Tension drops, supporting characters flatten, discovery feels preordained, and the
lead stops being a person and becomes an omniscient parser. Reader fatigue: "and then she saw what
no one else could see" stops impressing and starts provoking resistance.

**BAD** (too many wins in one chapter)
> The metadata had been scrubbed clean… The sender was in the building… You did not crop a margin by
> accident… She understood that whoever had sent her the photograph had wanted her down here, reading,
> when the door locked… Two people, then, at the least.

**GOOD** — three fixes, rotate them:
- *Right, but slower (process):* "The metadata fields were empty. Too empty. She nearly closed the
  window — then a buried relay tag caught her eye, not because she understood it but because she knew
  the Institute's naming convention from years of basement scanner outages. She stared a long second
  before the implication arrived."
- *Wrong once, then recover:* "The cropped photocopy annoyed her before it alarmed her. She took it
  for lazy duplication. Only after she pulled her father's published plate did the omission become
  what it was: not sloppiness, design."
- *Give the discovery to someone else:* "'You're looking at the words,' Kebede said. 'Look at the
  edge.' She did — and saw the missing margin."

**Craft motivation:** Process makes conclusions feel earned over beats, not snapped into existence.
Error and revision humanize brilliance — readers bond to a mind that *works*, not one that *knows*.
Distributed competence makes the world feel inhabited and the lead's brilliance believable among
peers, not mannequins.
**Engine:** OUTLINE — when planning a discovery beat, vary the *solver* and the *speed* (see the
draft-prompt rule + outline reveal-ledger). DRAFT — `draft-chapter.md` "process not just outcome"
(already a Leila voice law: *gets 80% fast, 20% late; one wrong first read, corrected*).

---

## 2 · One-Paragraph Total Epiphany  · `total_epiphany` · DRAFT

**Smell:** A single visual clue yields a complete, correct theory of the whole tactical situation.
**Why it's bad:** Readers grant one inferential leap, not a chain of six. A clue that generates full
operational truth reads as *authored*, not observed.

**BAD**
> They had not come to find out what her father knew. They already had it. They had come to take the
> last copy that wasn't theirs, and they had timed it for the morning someone finally went looking.

(That is a great deal inferred from "a man printing papers into a box.")

**GOOD** — reduce certainty, or defer the parse:
> Whoever was at the printer wasn't improvising. Batches, a box, a rhythm. That meant preparation.
> Whether they were stealing, preserving, or destroying, she couldn't yet tell. But they were acting
> before she could.

or let the scene answer later: *"He was boxing the pages as if they mattered. She left before she
learned whether that meant rescue or theft."* → (in the car) *"…not archiving. Replacement."*

**Craft motivation:** Uncertainty is suspense, not weakness. Deferred cognition is a reason to keep
reading — the reader stays for the final parse.
**Engine:** DRAFT — cap the inference depth per clue; one leap to *suspicion*, the full theory earned
across beats. Same family as the glossary's *over-explanation* and §16 below.

---

## 3 · Atmospheric Overwrite  · `atmospheric_overwrite` · DRAFT + EDIT · *aka Continuous Peak Register / Everything Is Significant / No Baseline (RELIC) · scanner: `superlative`, `./run.sh evenness`*

**Smell:** The prose insists on peak intensity at all times — every sentence sharpened, weighted,
paradoxed, or epigrammatic. The novelistic version of logging every variable at ERROR level.
**Why it's bad:** If every line strains to be the quotable one, none stands out. The prose becomes
self-drunk; the density of "final lines" is too high.

**BAD** (four mic-drops in a row, each fine alone)
> …the way you draw a sheet over furniture. […] You discredited it in advance. […] the evidence was
> being manufactured from more than one direction at once. […] They were closing the building around
> her…

**GOOD** — mix voltage; flat syntax before insight:
> The lobby was empty. Her account no longer worked. The guard who usually waved her through was gone.
> Only then did the pattern emerge.

and save the aphorism for the real turn — sharper and simpler: *"They didn't need her dead. They
needed her ridiculous."* (not "They wanted her disbelieved, which is the more permanent thing to be.")
**Craft motivation:** Flat syntax gives the insight room to land. This is the same disease as the
glossary's **evenness / gravitas inflation**, seen from the high side: relentless significance.
**Engine:** DRAFT — `draft-chapter.md` "one maxim-mouth per scene, not every scene" + the plain-pages
rule. EDIT — `de-llm-pass.md` §8 (roughen one-third of the quote-card lines) + §9 (deliberate
flattening); `./run.sh evenness`.

---

## 4 · Thesis Leakage  · `thesis_leakage` · DRAFT + EDIT · *aka Recursive Restatement / Triple Commit / Theme Compiler (RELIC) · scanner: `set_down`, `prose_thesis`*

**Smell:** The novel explains its own intellectual argument *immediately after dramatizing it*. Show
the forged document, then explain the strategy; show the page-swap, then explain witness
destabilization.
**Why it's bad:** Drama becomes annotated lecture notes. Interpretive closure statements choke
subtext and rereadability.

**BAD**
> They didn't do it to hide the alteration… They did it so that *I* would doubt what I'd seen.

**GOOD** — stop one beat earlier, OR put the meaning in *contested* dialogue:
> The page by Hakim's hands was gone. In its place sat a clean opening she had not seen before. For
> one humiliating second she doubted her own eyes. Then she ran.

or — *"'They weren't hiding the alteration,' Leila said. 'No,' Tewodros said. 'They were hiding* you
*from yourself.*'"*
**Craft motivation:** Leave the reader the final assembly — participation creates ownership. If
meaning must be spoken, let it be *relational/contested*; dialogue carries interpretation better than
narration because it stays dynamic.
**Engine:** DRAFT — event→reaction→interpretation order; prefer dialogue for any necessary
interpretation. EDIT — line-apply "stop defending landed metaphors / a restated theme is not covered
by thematic protection"; the glossary's *Thesis / theme-said-aloud*.

---

## 5 · Universal Institutional Omniscience  · `villain_cloud` · OUTLINE

**Smell:** Every opposing institution is hypercompetent exactly when the plot needs it and porous
exactly when the plot needs *that* — scrubs metadata but leaves a relay; disables her badge at the
perfect second; knows her flight; yet lets her escape with the crucial evidence every time.
**Why it's bad:** "Villain cloud architecture" — immense capability with conveniently patchy
implementation. Readers accept intelligence networks; they distrust godhood.

**BAD:** total surveillance implied, then a convenient gap whenever she needs to escape.
**GOOD** — make opposition competence *local and human*, and give failures a *reason*:
> They hadn't predicted every move. They'd predicted her habits. That was worse, and more believable.

> The summit floor was Devlin's. The loading dock belonged to Ethiopian contractors who hadn't been
> paid enough to care who slipped through it.

**Craft motivation:** Specificity creates plausibility; systems are *uneven*. Humanize the apparatus
through patterns and resource limits, not omniscience.
**Engine:** OUTLINE — when planning antagonist capability, define what they *can't* see and *why* each
gap exists (budget, jurisdiction, human laziness), not "the plot needs her to escape." (RELIC analogue:
the adversary's reach is institutional, not magical — give it seams.)

---

## 6 · Sacred Reveal Inflation  · `reveal_inflation` · OUTLINE

**Smell:** Repeatedly "actually the *real* thing is one level deeper" — library under the church,
decoy library vs. real, Brotherhood behind archives, Vatican behind that, committee behind Devlin,
mythic "makers" beneath all of it. Sequel-bait nesting inside one book.
**Why it's bad:** Once the reader expects the trapdoor, each new floor loses force; closure pressure
erodes.
**GOOD** — two disciplines:
- **Cap the hierarchy:** pick one final level and make it truly final *for this book*. Don't also
  heavily seed deeper mythic strata in the same argumentative band unless that is *definitely* the
  next book's engine.
- **Vary the kind of revelation:** not every escalation is "a bigger secret." Rotate **moral,
  emotional, self-, and strategic** revelation. (REVELATION already does this with the Covenant being
  *derivative* — do more of that, less chamber-within-chamber.)

**Craft motivation:** A thriller needs closure pressure; endless depth reads like nested DLC. Variety
of revelation-kind prevents fatigue.
**Engine:** OUTLINE — maintain a **reveal-kind ledger**: tag each reveal moral/emotional/self/
strategic/secret-deeper, and forbid more than ~2 consecutive "secret-deeper" reveals; declare the
final level. (RELIC: the relay already escalates by *node*; ensure not every node's payoff is "an
older, truer layer.")

---

## 7 · Everyone Speaks Like the Narrator  · `voice_homogenization` · DRAFT (voice laws)

**Smell:** Too many characters speak in the same polished, aphoristic, essayed cadence — distinct in
worldview, identical in sentence architecture (measured, epigrammatic, compressed, thematic).
**Why it's bad:** Tonal authority at the cost of dramatic texture. "A brilliant author ventriloquizing
six people who all attended the same graduate seminar."

**BAD** (all the same family of good line)
> "Dead scholars don't reorganize their own shelves." · "Truth is a blade…" · "Interpretation is what
> stands between scripture and slaughter." · "Truth is an aftermath…"

**GOOD** — differentiate by *cognitive habit*, not vocabulary:
- Make one major character syntactically *messy* (Miriam): *"Okay, no, stop. Back up. If this is real
  it's disgusting. If it's fake it's elegant. Either way I hate it. Show me the margins again."*
- Blunt the field operator (Abdi): *"Truth gets people killed if you carry it badly."* (not "Truth is
  a blade, Dr. Aziz…")
- Flatten the bureaucrat (Devlin): *"You mistake preservation for malice. Institutions triage. Always
  have."* — a bureaucrat's menace is *flatter*, therefore scarier.

**Craft motivation:** Messiness signals personhood; not everyone speaks in engraved stone. Diction
that reflects training and class differentiates the cast.
**Engine:** DRAFT — the **noun-swap test** is binding (`STYLE_GUIDE.md` Character voice laws — already
sharpened to this read). The craft audit + character-diagnose pass judge `voice_homogenization`
against those laws. One quotable closer per scene, in one mouth.

---

## 8 · Elegance at the Expense of Immediate Human Reaction  · `analysis_before_body` · DRAFT

**Smell:** Characters react to shock with *analysis before body* — straight to interpretation,
skipping the involuntary first beat (nausea, denial, adrenaline stupidity, absurd noticing).
**Why it's bad:** Even cerebral people have physiology. Converting shock instantly into meaning costs
emotional truth.

**BAD:** father's letter / the body / the betrayal → immediately parsed for significance.
**GOOD** — body before thought; let her think *stupidly* once:
> She read the line about her mother twice, then a third time, because the first two had passed through
> her without sticking. Only after that did the instruction register.

> For an idiotic second she thought he was asleep, and was ashamed of herself only after the neck angle
> resolved.

**Craft motivation:** Cognition follows impact — preserving that order increases emotional truth.
Micro-failure = humanity.
**Engine:** DRAFT — `draft-chapter.md` "body-first under pressure" + reveal-order rule (already a
de-llm-pass §10 structural move; this is its *generative* form). Leila voice law: *under peak stress
her syntax breaks, not refines.*

---

## 9 · Theme Declared Instead of Emerged  · `theme_declared` · DRAFT + EDIT

**Smell:** Explicitly stating thematic concerns (control of truth, discrediting witnesses, stewardship
vs. ownership) on top of dramatizing them.
**Why it's bad:** With the machinery to let theme emerge through pattern, also saying it makes the book
grade its own exam.
**GOOD** — turn theme into **motif**, then trust recurrence: let cropped margins, erased undertext,
swapped leaves, sealed drawers, relabeled boxes recur — and *don't* caption them. If the reader sees
forge→destabilize→salt→curate four times, they have the theme.
**Craft motivation:** Themes are memorable when embodied, not announced. Readers like being respected.
**Engine:** DRAFT — plant a *physical motif* for each theme; forbid the abstract restatement after the
2nd embodiment. EDIT — same as §4. (Glossary: *Thesis / theme-said-aloud*; `storygraph/prose_thesis.py`
ranks restatements.)

---

## 10 · Clue Density Without Friction  · `frictionless_clues` · OUTLINE

**Smell:** Major clue after major clue with no dead air, failed search, or wasted effort — every room
holds the next critical object. Investigation reads like *file download*.
**Why it's bad:** Friction is what makes inquiry feel like inquiry. Noise validates signal.
**GOOD** — design in friction at outline time:
- One genuine **dead end** — a half-chapter chase that proves irrelevant, or true-but-unusable.
- Make retrieval **costly, not just dangerous**: translation labor, reconstruction, persuading a
  witness, comparing three sources, or *giving something up* to get it.

**Craft motivation:** Real inquiry wastes time; cost creates value.
**Engine:** OUTLINE — `prompts/outline.md` discovery discipline: not every chapter hands over its key
intact; at least one node's key is *partial/damaged/costly* to obtain, and at least one promising lead
in the book is a dead end. (Maps onto the ledger's "every node COSTS" — extend cost from danger to
*effort and waste*.)

---

## 11 · Secondary Characters as Delivery Systems  · `delivery_system_characters` · OUTLINE

**Smell:** Support characters arrive with exactly the next needed category of knowledge — one warns,
one unlocks, one escorts, one tests-and-explains, one contextualizes, one reframes, one articulates
the anti-thesis. Useful, but too *nakedly* functional: clean interfaces, not people.
**Why it's bad:** Characters become people when they stop being clean interfaces.
**GOOD** — give support characters **cross-purposes that obstruct**, and let one *fail* at their
function: the ally helps once and hurts once; the journalist misreads because she wants the story; the
operator is right tactically, wrong interpretively; the elder's test is miscalibrated; the keeper opens
the *wrong* drawer first.
**Craft motivation:** Imperfection deepens ecosystem realism.
**Engine:** OUTLINE — for each recurring support character, define one beat where their function
*fails or conflicts* with the lead's need. (REVELATION voice laws already seed this: *Amara helps once
/ hurts once; Miriam misreads once; Abdi right-tactically-wrong-interpretively; Samuel withholds the
useful thing for emotional not strategic reasons.*) Make the outline honor those.

---

## 12 · Prestige Sentence Addiction  · `prestige_sentence` · DRAFT + EDIT · *aka Prestige Voice Over Scene Needs (RELIC — voice must downshift under danger) · scanner: `./run.sh evenness`*

**Smell:** Too many paragraphs end on a mic-drop cadence; the reader starts hearing the mechanism.
**Why it's bad:** When every paragraph lands its best line, the reader hears the machine instead of
the meaning.

**BAD endings (each fine; too many together):** "…because looking back was what they would be watching
for." · "…toward the long unstaged road north." · "…the meaning was the war."
**GOOD** — end some paragraphs on *utility*, and vary the music:
> She copied the folio number into her notes and moved to the next shelf.

Mix clipped stops, mid-thought continuations, awkward natural endings, interrupted beats.
**Craft motivation:** Functional endings make the poetic endings *hit harder*. Rhythmic variation is
invisible power. (Sibling of §3; the glossary's *Sentence rhythm & length variation*.)
**Engine:** DRAFT — don't engineer every paragraph-end to be quotable. EDIT — de-llm-pass §8/§9;
`./run.sh evenness` (paragraph-end cadence is part of the rhythm variance).

---

## 13 · Research Display Syndrome  · `research_display` · OUTLINE + DRAFT

**Smell:** The book knows a great deal and can't resist showing it — the dramatic frame pauses to
admire its own sophistication (e.g. a comparative-mythology / fringe-lore band imported from a
different register, threatening genre drift).
**Why it's bad:** Research should create *pressure*, not just atmosphere; lore seduction stalls story.
**GOOD** — two tests:
- *Does the detail change the protagonist's next decision?* If not, cut or defer.
- *Collapse to the most decision-relevant image:* "Every tradition had preserved some rumor of builders
  before history. She wrote it down and moved on, because tonight she needed a door, not a cosmology."

**Craft motivation:** Story priority over lore. (Direct RELIC relevance: the mythos must stay *grounded
engineering*, surfaced through use and need — never a lecture. This is `villain_cloud`'s cousin for
exposition.)
**Engine:** OUTLINE — gate lore against decision-relevance; keep designated mysteries unresolved. DRAFT
— deliver worldbuilding on need-to-know, in motion (glossary *Exposition / the iceberg*; MYTHOS_RULES).

---

## 14 · Too Many Perfectly Timed Warnings  · `timed_warnings` · OUTLINE

**Smell:** Characters say the exact ominous thing right before the exact relevant discovery, repeatedly.
**Why it's bad:** Reads as orchestration — the author's hand showing.
**GOOD** — make warnings *partially wrong*:
> "Don't start with the boxes labelled in his hand." She did. And found nothing. Only afterward did she
> understand what Amara had actually meant.

**Craft motivation:** Partial misdirection makes advice feel lived-in rather than authored.
**Engine:** OUTLINE — when a mentor/elder warning precedes a payoff, plan at least one where the warning
is *misread or partial*, paying off obliquely.

---

## 15 · Grand Moral Symmetry Overload  · `moral_symmetry` · OUTLINE

**Smell:** Every relationship resolves into elegant duality — Vatican and Brotherhood both curate
truth; two men both manage timing; text-altered / witness-altered; secrecy / release; archive /
anti-archive.
**Why it's bad:** Intellectually satisfying, but too much mirroring makes the novel feel *diagrammed*.
**GOOD** — introduce **asymmetry**: make one side *not mirrorable*. One antagonist coldly coherent, the
other self-deceivingly paternal — *rhyming, not equivalent.*
**Craft motivation:** Messier moral geometry feels human, not thesis-built.
**Engine:** OUTLINE — when two forces mirror, deliberately break one axis of the symmetry so the
structure rhymes rather than diagrams. (Trilogy-level: the Court/Brotherhood "in a different form"
should not perfectly mirror their book-1/2 selves.)

---

## 16 · Interpretive Overcompletion  · `interpretive_overcompletion` · THE MASTER PATTERN · DRAFT + EDIT · *all three reviews name this the #1 line-level habit*

**Smell:** The single most important line-level habit. You have the scene, the object, the pattern —
then you add the sentence that explains what it means. That extra sentence is frequently the cut.

**BAD**
> The page was not sitting still to be found. It was being moved while she stood over it.

**GOOD**
> When she looked back, it was a different opening.

**Craft motivation:** Trust the image. Readers are smarter than the explanatory sentence.
**Engine:** This is the unifying rule under §2, §4, §9, §12 and the glossary's *over-explanation /
the caption / one revision rule*. It already powers de-llm-pass §8 ("can this paragraph end one
sentence sooner?") and the line-apply prompt. Treat it as the engine's prime line-level directive.

---

## 17 · Metaphor Stack Overflow  · `metaphor_stack` · DRAFT + EDIT · scanner (RELIC): `shape_of`, `string_gong`, `two_same_shape`

**Smell:** Many comparisons for one object in a short span — a throat AND an instrument AND a keyway
AND a waveguide AND an ear AND a seat AND a switch. Each fine alone; the problem is *concurrency* —
the reader normalizes metaphor instead of absorbing meaning. (Surfaced by the RELIC re-read.)
**GOOD:** one *governing* metaphor per passage (acoustics OR key/lock, not interleaved); escalate by
*sequence* not pile (coin → part → resonator → key → planetary instrument, each owning its chapter);
cut the second metaphor when the first works.
**Craft motivation:** Stabilize the reader's conceptual model; reveal understanding in stages.
**Engine:** DRAFT — `draft-chapter.md` one-metaphor-family-per-paragraph rule. EDIT — the RELIC
scanners cap the worst echoes (`shape_of` ≤2, `string_gong` ≤2). Worked demo: `RELIC_BADGOOD.md` #3.

## 18 · Character Thinks in Finished Prose  · `finished_interiority` · DRAFT · scanner (RELIC): `arin_macro`, `ai_meta`

**Smell:** Interiority polished to publishable final form — a person under pressure thinking in
maxims. Blurs the line between the character's immediate cognition and the novel's authorial voice,
so the lead reads as a delivery vector for the book's conclusions, not a person in time.
**GOOD:** let stress *break* the syntax ("Understanding wasn't the same as permission. She knew that.
God, she knew that."); alternate clean thought with sensory interruption (the cold tea between two
clauses of reasoning); reserve the fully-sharpened aphorism for a genuine crystallization — one per
scene-end feels like revelation, six feel like authorial throughput.
**Craft motivation:** Thought feels embodied and immediate; insight feels discovered, not preloaded.
**Engine:** DRAFT — already a Leila/Priya voice law (*under peak stress the syntax breaks, not
refines*). The RELIC `arin_macro` scanner flags a *re-explained* temperament; show it, don't gloss.
Worked demo: `RELIC_BADGOOD.md` #4. (Sibling of §8 analysis-before-body.)

## 19 · Overdecoded Wonder  · `overdecoded_wonder` · DRAFT + EDIT

**Smell:** The significance of a thing is explained immediately after it's shown — what it implies,
why it matters, how it fits the framework. Mystery breathes in *delay*; the best material is
strongest when the reader sits in the object's weirdness before the systematizing mind closes around
it. (One of the RELIC re-read's "big three".)
**GOOD:** a beat of *unassimilated strangeness* first ("The bore was round. Not roughly. Not
functionally. Round the way a thought is round before it becomes language." — diagnosis comes later);
let a character *misread* first.
**Craft motivation:** Preserve awe before analysis — image first, meaning second.
**Engine:** DRAFT — reveal-order rule (event → reaction → interpretation); OUTLINE — `total_epiphany`
cap. Direct kin of §2 and §16. Worked demo: `RELIC_BADGOOD.md` #9.

## 20 · Climactic Self-Explanation  · `climactic_self_explanation` · EDIT (the ending guard)

**Smell:** The ending becomes discursive about its own themes (consent vs control, custody vs
seizure) where readers want image, action, residue, irreducible feeling. The closer to the climax,
the more the prose risks printing the thesis. (The RELIC re-read's ending note.)
**GOOD:** let the final act be *smaller than the idea* ("The disc is in the hollow, not the socket." —
that image carries the book; don't add the paragraph explaining it); trust symbolic repetition
(prologue's chamber/socket/sleeping-gold ↔ ending's chamber/hollow/unseated-gold already builds the
resonance — echo, don't annotate).
**Craft motivation:** Contain scale through image; image replaces explanation; this is what mature
fiction does when it trusts its structure.
**Engine:** EDIT — the gatekeeper + line-apply ending check; the de-llm-pass §10 "plainer at the
peak". **Protected exception:** the earned climax reframe's *first* statement (see `RELIC_BADGOOD.md`
#10 + `relic-climax-protected-lines` memory). Worked demo: `RELIC_BADGOOD.md` #10.

## 21 · Echo-Chamber Themeing / motif over-binding  · `motif_overbinding` · DRAFT + EDIT

**Smell:** Good motifs (pressure→wealth/death, *build the thing right*, *bring them home*, *the land
remembers*, scars/wounds/memory) repeated in **too-recognizable, too-finished forms**, so the reader
sees the symbolic *framework* instead of the story — the book feels *authored*, not *lived*. The
motifs are too tightly coupled and too frequently invoked. (RESONANCE software-smell read, 2026-06-03.)
**GOOD:** (a) **let motifs mutate** — same thematic family, fresh phrasing each time ("pressure
becomes power" → later "The suit fed on impact the way the mines fed on depth"); (b) **asymmetry** —
echoes should be *off-angle*, never self-quoted exactly; (c) **skip one expected echo** — at a beat
where the reader expects "bring them home", don't say it; let the absence ring.
**Craft motivation:** A motif should *evolve*, not repeat; strategic omission creates power.
**Engine:** DRAFT — vary motif phrasing across recurrences; never restate a motif in its coined form
more than once. EDIT — flag exact-form motif repeats. Distinct from §9 (theme *declared*): this is the
*image/phrase* over-recurring, not an abstract restatement. Scanner kin: `prose_thesis` (embedding
repetition). Worked demos: `RESONANCE_BADGOOD.md` (Echo-Chamber Themeing).

## 22 · Bandwidth Violation / narrative cognition leakage  · `bandwidth_violation` · DRAFT

**Smell:** **The consciousness in the sentence exceeds the consciousness of the moment.** At close
psychic distance (child-Arin, exhausted-Arin, panic), the narration carries fully-mature symbolic
framing / perfect thematic adjacency / too-clean causal meaning — the author's hand shows. Not purple
prose; subtler. (RESONANCE read; close kin of §18 finished-interiority, but keyed to *POV pressure*.)
**GOOD:** (a) **lower the abstraction at close distance** — "A thing built poorly under great pressure
on bad ground would fail." → "Bad ground made bad things fail faster."; (b) **sensory proxy for
thought** — let cognition arrive through an object ("He pressed the bed again. The wheel rose,
settled, rose true. Good."); (c) **delay the elegant sentence** — move the gorgeous thematic line to a
later reflective passage, or give it to another character.
**Craft motivation:** Match sentence-intelligence to viewpoint pressure; child logic, no adult overlay.
**Engine:** DRAFT — the test: *could this exact sentence occur in this character's nervous system at
this moment?* If not, simplify / externalize / relocate. (Already a Priya/Leila voice law: *under peak
stress the syntax breaks, not refines* — extend to every close-POV moment, esp. childhood/crisis.)

## 23 · Emotional Redundancy / redundant affect signaling  · `emotional_redundancy` · DRAFT + EDIT

**Smell:** A strong event is signalled on **too many channels in sequence**: body reaction + thought
reaction + thematic framing (he stops breathing → grips the bench → white-noise skull → "the whole of
his intelligence went white" → significance gloss). Too many signals paradoxically *flatten* the
moment. (RESONANCE read.)
**GOOD:** **pick one channel** — the body ("His hand came off the bench.") *or* the interior ("The
whole of his intelligence went white."), rarely both; let **dialogue carry the shock** ("'You're
real,' he said."); or **trust silence** — stop sooner after a reveal.
**Craft motivation:** Emotion lands harder through singular precision; omission creates aftershock.
**Engine:** DRAFT/EDIT — at an emotional peak, count the signal channels; keep the single strongest,
cut the rest. Kin of §8 analysis-before-body (which is about *order*; this is about *quantity*).

## 24 · Trailer Voice / everything arrives as a moment  · `trailer_voice` · DRAFT + EDIT

**Smell:** Sections perpetually *enter like a trailer beat* — "Then came the men." / "Later, a boy." /
"And then there was one." / "The simulation died at 02:14." / "The signal arrived as a jolt." Used
well but *too often*, so the reader anticipates the drum hit and the book feels teaserized. (RESONANCE
read.)
**GOOD:** (a) **enter sideways** sometimes ("Brand almost missed the anomaly because she was looking
at the wrong graph." instead of "The signal arrived as a jolt."); (b) **continuity over fanfare**
("After Mother, the suit held only one voice." instead of "And then there was one."); (c) **reserve
the trailer line for actual hinge points** — scarcity is force.
**Craft motivation:** Vary the narrative attack-angle; not every transition should announce itself.
**Engine:** DRAFT — don't open consecutive scenes on the declarative drum-hit; vary entries. Sibling
of §3/§12 (peak register / prestige sentence) at the *scene-opening* position.

## 25 · Competence Saturation  · `competence_saturation` · DRAFT (voice laws) · *ensemble variant of §1*

**Smell:** Everyone — Arin, Priya, Brand, Venter, Theo, the Court — perceives and speaks at the same
high level of dry, precise insight, so the *tonal field flattens*. Characters are differentiated by
ethics/function/history but not by **sentence behaviour under pressure**. (RESONANCE read; the
ensemble form of §1 competence_cascade.)
**GOOD:** (a) **a distinctive cognitive failure each** — Arin over-completes systems / under-reads
people; Priya trusts instrument over instinct until too late; Brand delays to avoid past overreach;
Venter sees truth fast, says it late; (b) **let someone be wrong in a mundane way** — misread a room,
snap unfairly, miss a practical detail (not just grand ethical error); (c) **let brilliance sound
different** — Atlas structurally precise, Mercury socially adaptive, Brand administratively surgical,
Theo psychologically oblique, Venter materially taciturn.
**Craft motivation:** Distinction through *limitation*; intelligence is not one voice.
**Engine:** DRAFT — the STYLE_GUIDE voice laws already assign cognitive habits; this says also assign
each a **failure mode** and let it show in dialogue texture. Craft-audit `voice_homogenization` is the
detector.

## 26 · Last-Line Grooming  · `last_line_grooming` · EDIT (the ending guard) · *kin of §12/§20*

**Smell:** *So many* scene/chapter endings are sculpted to a resonant, polished close ("the land
remembers", "they chose", "the only bargain that ever mattered") that the reader feels the author
stepping in to place the closing weight every time. An ending needn't be the best sentence in the
section. (RESONANCE read.)
**GOOD:** (a) **unresolved motion** — "He reached for the phone."; (b) **concrete consequence** —
"The requisition terminal was still open when the cadence changed."; (c) **occasionally end below the
register** — "'Fine,' she said. 'Then show me the logs.'" Deflate deliberately so the genuinely
sculpted endings spike.
**Craft motivation:** Close the *consequence*, not the *meaning*; leave residue, not summary.
**Engine:** EDIT — vary ending-register across scenes; not every chapter ends on a maxim. Measured by
the same `evenness` paragraph-end-cadence signal as §12; the gatekeeper/line-apply ending check.

## 27 · Prebuttal / reader pre-emption  · `prebuttal` · DRAFT + EDIT

**Smell:** The prose anticipates objections and **litigates its own case** — built-in defences against
imagined criticism, recurring as "not X, it is Y" / "not paranoia, [right]" / "not fake, derivative" /
"not revelation, aftermath" / "not the oldest, the defensible". Intelligent distinctions, but at scale
the prose acquires a **prosecutorial texture** — the book sounds like it knows it's vulnerable and is
constantly arguing against a reviewer; the reader feels the author's *anxiety about interpretation*.
(REVELATION software-smell read, 2026-06-03. NB: this is the *defensive* cousin of §16/the reframe
tic — the negation here exists to pre-empt a doubt, not to discover.)
**GOOD:** let some vulnerability sit **unpatched in the moment**; deal with it later through
*consequence*, not an immediate defensive distinction. Confidence includes allowing temporary
ambiguity.
**Craft motivation:** A book that doesn't litigate itself reads as confident; the reader trusts a
narrator who isn't defending against them.
**Engine:** EDIT — flag the defensive "not X, it is Y" (distinct from the discovery-reframe: ask *is
this negation pre-empting a reader's objection?* If yes, cut or defer). DRAFT — don't pre-answer the
skeptic mid-scene. Scanner kin: the `reframe` family (but judged by *function*, not form).

## 28 · No Negative Space / every beat translated  · `negative_space` · DRAFT + EDIT

**Smell:** Scenes are so semantically active that *even the pauses contain analysis* — every gesture,
silence, and object is assigned interpretive value, so the book becomes **airless**. A novel
(especially one about texts and interpretation) needs silence: places the reader can inhabit
uncertainty, dread, longing, confusion. (REVELATION read; the positive-prescription inverse of §16 —
not just "cut the caption" but "leave a margin where no caption goes".)
**GOOD:** add sensory beats with **no thesis attached**; gestures that go unexplained; reactions that
stay unreadable; scenes that end one beat early. ("She understood X about Y and therefore Z." → "She
put the page back in the folder upside down and did not correct it." — the reader enters the gap.)
**Craft motivation:** Meaning intensifies in proportion to the silence around it. Negative space is
where the reader *participates*.
**Engine:** DRAFT — deliberately leave some beats un-glossed (the meta-fix kin of de-llm-pass §9's
"let some pages be plain", applied to *meaning* not just *register*). The test: *what is withheld in
this scene?* If nothing, it's over-translated.

## 29 · Same Flavor of Awe / monotone wonder  · `same_flavor_awe` · DRAFT + OUTLINE

**Smell:** The *awe register* is consistently excellent but consistently the **same** — every
revelation is "someone made this **on purpose / impossibly well / before us / for a function**." True,
but repetitious in *sensation*: the reader begins to **pre-parse the wonder before it arrives**, so
each new marvel lands softer than the last. (RELIC software-smell read, 2026-06-03.)
**GOOD:** give each node a **different *kind* of wonder**, not just a bigger one — dread / industrial
wrongness (the mine) · abstract geometric terror (Vredefort) · public archaeology becoming instrument
(the stone circle) · inheritance and custodial guilt (Aksum) · *intimacy, not scale* (the drowned
chamber). And occasionally **use banality as contrast**: "It looked, for a second, disappointingly
practical. Then she saw the tolerance." — the ordinary sharpens the extraordinary.
**Craft motivation:** Variation in the *texture* of awe keeps revelation fresh; a marvel the reader
can predict the emotional shape of is no longer a marvel. (This is §3 evenness applied to the
*wonder* axis specifically — the relay's escalating nodes especially risk it.)
**Engine:** OUTLINE — tag each set-piece node with its *distinct* intended reader-experience (not just
its rank); forbid two adjacent nodes resolving into the same flavor of awe. DRAFT — vary the sensory
and emotional register of each reveal; let one land as intimacy, one as dread, one as guilt.

---

## The master directive — "write 10–15% less meaning"

The single ruthless instruction the RESONANCE read distilled, and the thread under §1/§16/§21/§23/§26:
**not less story, not less intelligence — less *declared* meaning.** Build the circuitry; trust the
current to run without labelling every wire. The reader feels the meaning before you state it; then
stating it costs participation, ambiguity, and aftershock. Operationally: **stop half a beat earlier,
and trust the reader sooner.** Every "explain / summarize / universalize / moralize / echo-theme"
sentence *after a strong image* is a cut candidate — if the previous sentence already did the job,
delete it. This is the generative form of the de-llm-pass §8 "end one sentence sooner" and the
master pattern §16.

---

## Three-book convergence — the highest-priority signals

> **The overkill payoff.** **Six grounded independent reads** — RESONANCE ×2 (line-level +
> software-smell), REVELATION ×2 (a developmental edit + a software-smell read), and RELIC ×2 (a
> brutal code-review + a software-smell read) — converge on the same root anti-patterns. (A 7th
> purported RELIC read was **rejected as ungrounded** — it couldn't quote the manuscript and pushed
> toward the house tells; see "Reads that did NOT converge" below. Convergence-weighting cuts both
> ways.) Convergence across independent instruments is the locked operating model's definition of
> *signal* (a lone read is a lead; agreement is a verdict). The patterns every reviewer flagged are
> the engine's top-priority fixes — most have a deterministic scanner, so they are *measurable*. **Every
> book has now been read twice at depth, all converging on one master fix: write less *declared*
> meaning, trust the reader sooner.**

| Root anti-pattern | RESONANCE reads (×2) | REVELATION read | RELIC read | Engine detector | Weight |
|---|---|---|---|---|---|
| **Over-explanation / interpretive overcompletion** (§16) | "interpretive redundancy" + "Double-Stamping" (#1) | "Thesis Leakage" + master "Interpretive Overcompletion" | "Recursive Restatement" (#2) + "Theme Compiler" (#6) | `set_down`, `prose_thesis`; de-llm §8 | ★★★ all 3 |
| **Continuous peak register / evenness** (§3) | "aphoristic overreach" + "Clause Creep" (#3) | "Atmospheric Overwrite" (#3) + "Prestige Sentence" (#12) | "Continuous Peak Register" (#1) + "Everything Is Significant" (#7) | `superlative`, `./run.sh evenness`; de-llm §9 | ★★★ all 3 |
| **Theme declared, not embodied** (§9) | "theme-said-aloud" / coda | "Theme Declared" (#9) | "Theme Compiler" (#6) + "Climactic Self-Explanation" (#10) | `prose_thesis`; glossary *Thesis* | ★★★ all 3 |
| **Voice homogenization** (§7) | noun-swap + "Competence Saturation" (#9) | "Everyone Speaks Like the Narrator" (#7) | "voices blur under the house style" (prior edit §3) | noun-swap test; craft-audit `voice_homogenization` | ★★★ all 3 |
| **Prestige-sentence / last-line grooming** (§12,§26) | "Quotation Machine" (#12) + "Last-Line Grooming" (#11) | "Prestige Sentence Addiction" (#12) | "Prestige Voice Over Scene Needs" (#8) | `./run.sh evenness` (paragraph-end cadence); de-llm §8 | ★★★ all 3 |
| **Overdecoded wonder / explain-too-soon** (§19) | "prophecy" (caption *early*) | "One-Paragraph Total Epiphany" (#2) | "Overdecoded Wonder" (#9) | `prophecy`; reveal-order rule | ★★★ all 3 |
| **Mythic / atmospheric inflation** (§3,§13) | "Mythic Inflation" (#10) + "mythic inflation" | "Research Display" (#13) | "Research Display Leaking into Runtime" (#5) | MYTHOS_RULES gate; lore-changes-a-decision | ★★★ all 3 |
| **Sainted / finished protagonist** (§1,§18,§22) | "retrospective sanctification" + "Bandwidth Violation" (#4) | "Competence Porn Cascade" (#1) | "Character Thinks in Finished Prose" (#4) | `protagonist_sainting`, `arin_macro` | ★★★ all 3 |
| **Rule-of-three dependency** (rule-of-three) | "Rule-of-Three Dependency" (#5) | "rule of three" (catalog) | (triadic lists) | (no scanner; read-level) | ★★☆ |
| **Metaphor stack** (§17) | "Metaphor Stack Overflow" (#6) | — | "Metaphor Pileup" (#4, both reads) | `shape_of`, `string_gong`, `two_same_shape` | ★★☆ |
| **Same flavor of awe** (§29) | — | — | "Technical Sublime w/o Texture Break" (#10) | OUTLINE — distinct reader-experience per node | ★☆☆ RELIC |
| **Emotional redundancy** (§23) | "Redundant Affect Signaling" (#7) | — | — | read-level; kin of `analysis_before_body` | ★☆☆ RESONANCE |
| **Trailer voice** (§24) | "Trailer Voice Syndrome" (#8) | — | — | read-level (scene-opening cadence) | ★☆☆ RESONANCE |
| **Prebuttal / reader pre-emption** (§27) | — | "Prebuttal Syndrome" (#9) — "not X, it is Y" as self-defense | (defensive reframes) | EDIT — `reframe` family by function | ★☆☆ REVELATION |
| **No negative space / airless** (§28) | "every pause contains analysis" | "Too Little Negative Space" (#10) | "even register" | DRAFT — leave beats un-glossed | ★★☆ |
| **Frictionless/convenient plot** (§5,§10,§11,§14,§15) | — | "Clue Density", "Villain Cloud", "Delivery-System", "Timed Warnings", "Moral Symmetry" | "structure is baggy" (prior edit §4) | OUTLINE-level (`prompts/outline.md`) | ★★☆ |

**Reading the table:** the ★★★ rows are the engine's standing priorities — every book, every read,
plus a scanner. They are *already* the bands `./run.sh tics` and `./run.sh evenness` enforce and the
moves `prompts/de-llm-pass.md` ranks. This catalog's job is to keep the *generative* layer
(outline + draft) from producing them in the first place, so cleanup has less to do. The single
unifying directive across all ★★★ rows: **trust drama over explanation; image over interpretation;
compression over restatement; character limitation over protagonist brilliance.**

### Reads that did NOT converge — the negative example of convergence-weighting

Convergence-weighting cuts both ways: a read is a *lead*, and a lead that fails the test is
**discounted, with reasons recorded** so it isn't silently applied or re-litigated. One on file: a
purported RELIC "ant-patterns" read (2026-06-03) was **rejected** on two hard tells — (1) **4 of its 5
BAD snippets did not exist in the manuscript** (fabricated, where every grounded read quotes real,
often scanner-confirmed lines), and (2) its "good" alternatives pushed *toward* the house tells the
six grounded reads remove (purple prose, emotion-naming, the `cold_dread` cliché). Its one real-line
fix would have *flattened* a characterful clause. **No cuts applied.** The lesson is the meta-rule:
weight a read by whether it quotes the real text and converges with the instruments; a fluent read
that does neither is noise, however confident.

---

## The five-pass revision protocol (a brutal, runnable self-edit)

When revising any chapter, run these in order. They operationalize the catalog.

1. **Cut 25% of the "therefore" sentences.** Any sentence beginning "which meant," "that was," "what
   mattered was," "the point was," or that summarizes the significance of the preceding image — ask
   *can I delete this and keep the meaning?* If yes, delete. (§16, §4, §9.)
2. **Mark every instant-mastery moment.** For every three, keep one immediate, make one *delayed*,
   make one *partially wrong*. (§1, §2.)
3. **De-engrave dialogue.** For each major support character fix sentence length, abstraction
   tolerance, favorite mode (image / argument / joke / procedure / command), diction-by-education, and
   *what they avoid saying* — then revise so no two are equally quotable. (§7.)
4. **Reduce clue convenience.** For each major discovery ask: why is this here? why wasn't it already
   destroyed? what did it cost to get? what if it's incomplete, damaged, or misleading? (§10, §11.)
5. **Lower the voltage every third paragraph.** Insert deliberately plain sentences. ("The room held
   the silence of institutional guilt, old and climate-controlled." → "No one spoke. The scanner fan
   kept running.") (§3, §12.)

## The before/after that anchors the whole catalog

**House tendency (over-built):**
> Someone had planted a fake Brotherhood document in her father's restricted file. The finding was
> real, the plate beside it genuine. They had built the forgery to *poison* it — to sit a forgery next
> to the truth so that when the truth surfaced, an opponent could hold up the fake, prove it false in
> an afternoon, and let the real plate drown in the laughter. You did not hide a thing this way. You
> discredited it in advance.

**Upgraded (compressed, trusts the reader):**
> The stamp was wrong by one letter. The plate beside it was real. She looked from one to the other and
> felt the strategy click into place. Not concealment. Contamination.

*Still intelligent; more muscular; less over-explained; stronger rhythm; trusts compression.*

---

## What the engine is already good at (do not "fix" these)

Material intelligence (objects legible and meaningful) · institutional menace (power as paperwork,
timing, procedure) · scholarly suspense · motif recurrence (margins, variants, undertext, custody) ·
moral seriousness. The growth edge is **not** "be smarter" or "research more." It is: **trust drama
more than explanation, and character limitation more than protagonist brilliance.** Keep the
strengths; thin the reflexes.

---

*This catalog is book-agnostic engine law. The REVELATION snippets illustrate; the rules bind all
books. Per-book *verbatim* line pairs live in `academic/craft-examples/<BOOK>_BADGOOD.md`. When a new
external/cold read names a recurring habit not here, add it as a numbered smell with an `engine:` tag
saying which layer (outline/draft/edit) can actually prevent it.*
