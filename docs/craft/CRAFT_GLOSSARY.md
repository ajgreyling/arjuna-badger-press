# Craft Glossary & Body of Knowledge — Arjuna Badger Press

The working vocabulary of this studio **and** a synthesized creative-writing + editorial
body of knowledge — the craft an MFA and an editorial certificate teach, distilled into
checkable rules and named failure-modes. In plain English. This is a **learning reference**
for writers — not a private canon spec.

> **Part of *Arjuna Badger Press*** — the free, portable writing-craft body of knowledge (see
> [The technology](../TECHNOLOGY.md) for how the studio uses it). Authoring standard for every entry:
> **concept-first and attributed** (the teachable idea leads, named to its source), with all
> **project-specifics fenced** into the `In this project:` / `See:` lines so the craft lifts out
> clean. Write each entry to survive being read by someone who has never seen this repo.


**How to read this file (for Claude, drafting or editing):** every entry states the concept,
then — where it earns it — a **Rule** (what to do) and a **Fail** (the failure-mode to detect
and avoid). When drafting, the Rules are your priors; when editing or cold-reading, the Fails
are your checklist. The single most load-bearing section for AI-authored prose is
**Pitfalls & Machine-Tells** at the end — read it as a self-audit.

**Sections:** **The Craft of Making a Novel** *(the process / the steps)* · **Structure &
Story** · **Character & Dialogue** · **The Craft of the Sentence** · **Point of View, Setting
& World** · **Series & Trilogy Architecture** *(incl. the **Triptych / Tryptych form**)* · **The Editorial Ladder** · **Pitfalls &
Machine-Tells** *(the self-audit)* · **The Machinery (this repo's tools)** · **Book
Furniture** · **Sources**.

> Degree-level craft is not rules-for-their-own-sake. The whole point of knowing the
> conventions is to **break them on purpose, in the right place**. Where this file says
> "Rule", read "default that needs a reason to violate" — earned violation is craft;
> accidental violation is error. This is the same logic as the repo's `keep_if` guard, which
> exists precisely so de-LLM passes don't sand away an *earned* voice choice.

---

## The Craft of Making a Novel *(the process / the steps)*

The order operations actually happen in. Tools in this repo **measure and alarm** at each
stage; they do not drive — a human seed plus single-shot drafting plus surgical edits writes
the prose (see [`docs/MASTER_PLAN.md`](MASTER_PLAN.md) §0 and the *history engine-regression
finding*: the multi-pass rewrite engine measurably *regressed* prose vs single-shot).

### Premise / hook / "what if"
**Plain English:** The compressed engine of the whole book — the single dramatic question or
"what if" that a reader could repeat in one sentence and want the answer to. Premise ≠ plot
(the events) ≠ theme (the meaning underneath). It's the *promise* the cover makes.
**Rule:** Be able to say the book in one sentence with a *specific* irony or collision in it
("a neurodiverse engineer who reads ancient machines must outrun the people who built the
myth"). If the one-liner is generic, the book underneath usually is too.
**Fail:** The "average Tuesday" premise — a situation, not a question; nothing is *about to
change*. Most novels start a chapter or two before the real premise ignites.
**See:** `books/relic/canon/SEED_STORY.md` · [`CLAUDE.md`](../CLAUDE.md) (locked creative DNA)

### Theme / controlling idea
**Plain English:** What the book argues about life, underneath the plot. The *controlling
idea* (Story Grid / Robert McKee) states it as cause→value: e.g. "*The cost of knowing is
real, but ignorance costs more.*" Theme is the lighthouse — anything in character or plot
that doesn't serve it is probably extraneous.
**Rule:** Know (or discover by draft's end) your one controlling idea; let it silently decide
what stays. Theme is an *active force* working on the protagonist, proven by the ending's
value-shift — not a moral pinned on at the end.
**Fail:** **Theme-said-aloud** (see *Thesis* below) — a character or narrator announcing the
meaning the scenes already earned. Few good books start *from* theme; most discover it in
draft and then sharpen toward it. Don't reverse-engineer a draft into a sermon.
**See:** *Thesis / theme-said-aloud* (this file) · `storygraph/prose_thesis.py`

### Outlining vs. discovery ("plotters vs. pantsers")
**Plain English:** Two legitimate routes to a draft — plan the structure first (outline), or
write to find out what happens (discovery / "pantsing"). Most working novelists are hybrids:
a skeleton outline, discovery inside the scene.
**Rule:** Match the method to the book. A tightly-plotted set-piece adventure (RELIC's
quest-relay) needs the outline up front so the key-chain can't break; a character/voice piece
can afford more discovery. Whatever the route, the *revision* is where the book is actually
made.
**Fail:** Treating the outline as a cage (killing a better idea the draft surfaces) or
treating "pantsing" as a license to skip structural revision.
**See:** [`CLAUDE.md`](../CLAUDE.md) (pipeline stage 1) · *Outline* (this file)

### Drafting / the rough first draft
**Plain English:** Getting the whole shape down, badly, all the way to the end. The first
draft's only job is to *exist* so it can be revised. Anne Lamott's "shitty first drafts" and
"bird by bird" (one manageable piece at a time) are the canonical permission slips.
**Rule:** Finish the draft before polishing it. Forward momentum in drafting beats sentence-
perfection; you cannot edit a blank page, and you will cut much of what you over-polish.
**Fail:** Polishing chapter one forty times and never reaching the end ("the perfectionist
spiral"). Also: confusing a clean *sentence* draft with a sound *story* draft — they're
different layers fixed by different passes (see *The Editorial Ladder*).

### Rest / the drawer / fresh eyes
**Plain English:** Time away from the manuscript before revising, so you read it as a stranger
would. Weeks, ideally.
**Rule:** Build distance before each big revision pass. The repo's analogue is the **cold
read** — a reader given *no* context, notes, or intentions, judging only what's on the page.
**Fail:** Revising while still in love with (or sick of) the draft — you'll defend lines a
stranger would trip on, or gut lines that actually work.
**See:** *Cold read* (this file) · `./run.sh cold-read`

## Structure & Story

> The named "structures" below (three-act, the Journey, Save the Cat, scene-and-sequel) are
> **the same skeleton at different zoom levels**: a protagonist in a normal world is forced
> out of it, struggles against escalating opposition, hits a low point, and resolves changed.
> They are descriptive lenses, not formulas to fill — pick the lens that makes *this* book's
> weak joint visible, then ignore the rest.

### Three-act structure
**Plain English:** The oldest macro-shape. **Act I** (setup, ~25%): the normal world, the
protagonist, the **inciting incident** that disturbs it, ending on a point-of-no-return.
**Act II** (confrontation, ~50%): escalating obstacles in a "new world", a **midpoint** that
raises stakes or flips the goal, then a collapse. **Act III** (resolution, ~25%): climax and
new equilibrium.
**Rule:** Whatever blueprint you use, you can locate these four load-bearing moments (incite,
first turn, midpoint, climax). If you can't find the midpoint, Act II is probably a flat
"and-then" sag.
**Fail:** The **saggy middle** — Act II as a string of incidents with no midpoint pivot and no
rising cost. Each scene should change the situation, not just extend it.

### The Hero's Journey *(monomyth, Campbell/Vogler)*
**Plain English:** A mythic overlay on the three acts: Ordinary World → Call to Adventure →
Refusal → Mentor → Crossing the Threshold → Tests/Allies/Enemies → Ordeal → Reward → Road
Back → Resurrection → Return with the Elixir. Departure / Initiation / Return map to the
three acts.
**Rule:** Useful for diagnosing *what's missing* (no real threshold-crossing? no cost at the
ordeal? the hero returns unchanged?). The "elixir" is the thematic payoff carried home.
**Fail:** Slavish beat-ticking that produces a generic chosen-one arc. The monomyth is a
description of many stories, not a recipe for a good one; subvert freely.

### Save the Cat beat sheet *(Blake Snyder)*
**Plain English:** A 15-beat commercial template (Opening Image, Theme Stated, Setup,
Catalyst, Debate, Break into Two, B-Story, Fun and Games, Midpoint, Bad Guys Close In, All Is
Lost, Dark Night of the Soul, Break into Three, Finale, Final Image) sitting inside the three
acts. The "save the cat" moment = an early beat that makes us root for the hero.
**Rule:** Best used as a *checklist for pace* — by ~the 50% mark you should be at a real
midpoint; "All Is Lost" should land near 75%. Good for catching a story that ignites too late
or has no low point.
**Fail:** Treating "Theme Stated" as license to *say the theme out loud* (see *Thesis*), or
hitting beats on a metronome so the structure becomes visible to the reader.
**See:** *Velocity* (this file) — in a cinematic adventure, the "Fun and Games" promise-of-
the-premise beats are the set-pieces.

### Scene & sequel *(Dwight Swain, mid-level structure)*
**Plain English:** The engine *below* the act, *above* the line. A **scene** is a unit of
conflict with three parts — **Goal** (what the POV character wants *now*), **Conflict** (the
opposition that tests how badly), **Disaster** (a setback with stakes that changes what comes
next). A **sequel** is the connective tissue that follows — **Reaction** (emotional fallout),
**Dilemma** (the now-worse set of options), **Decision** (the new goal that launches the next
scene). Scene = proactive; sequel = reactive.
**Rule:** Every scene should end *worse* or *changed*, not tidy — the disaster is the hook into
the next scene. Sequels control tempo: a long sequel slows the breath after a big set-piece; a
near-zero sequel (cut straight to the next goal) accelerates. Match sequel length to desired
pace.
**Fail:** Scenes with no scene-goal (the character is passive, things merely happen *to* them);
or all-scene-no-sequel relentlessness (exhausting, no emotional processing) or all-sequel-no-
scene (navel-gazing, no forward motion). The repo's **velocity** guard is essentially "don't
let a sequel flatten a set-piece."
**See:** *Beat* · *Velocity* · *Quest-relay* (this file)

### Stakes
**Plain English:** What the POV character stands to lose. Stakes can be external (death, the
artifact), internal (self-worth, a belief), and relational (a bond). Strong stakes are
*specific and personal*, escalate, and are *felt* before they're stated.
**Rule:** The reader must know what's at risk and *care* before the risk pays off. Raise
stakes across the midpoint. Tie the external stakes to an internal need so the plot and the
character arc resolve in the same blow.
**Fail:** "Save the world" abstraction with no personal cost; or stakes asserted ("everything
depended on it") but never dramatized. Also **stakes that don't escalate** — the saggy middle
again.

### Inciting incident / point of no return
**Plain English:** The event that knocks the protagonist out of equilibrium and *starts the
actual story* (inciting incident), and the slightly later moment they can no longer go back to
normal life (first plot point / "break into two").
**Rule:** Start the book *at or just before* the incite — "the day their life changes", not the
ordinary day before it. Backstory and normal-world texture are delivered *after* the reader is
already hooked, in small doses.
**Fail:** Pages of throat-clearing — waking up, commuting, mirror-describing, weather — before
anything is at stake. The #1 reason agents stop reading (see *Opening / hook*).

### Opening / hook
**Plain English:** The first line, paragraph, page, and chapter — the audition. Agents and
readers decide fast and look for reasons to *stop*.
**Rule:** Open with a situated voice and a sense that *something is about to happen* — a
character wanting something, in a specific place, with an implied imminent change. Establish
voice and stakes before exposition.
**Fail:** Opening on info-dump, backstory, weather, or an "average Tuesday"; a generic or
performative voice; or action with no meaningful implication behind it (a car chase we have no
reason to care about yet).
**See:** *Premise / hook* · *Velocity* (this file)

### Causality / the "therefore, but" test
**Plain English:** Scenes should connect by *consequence*, not mere sequence. The South Park
test: events should read "*this happened, **therefore** that, **but** then…*" — never
"*and then… and then…*".
**Rule:** If you can reorder two adjacent scenes without breaking anything, the causal chain
is weak. Each scene's disaster should *cause* the next scene's goal (the scene→sequel→scene
loop is this chain in miniature; the **key-chain** is its enforced form).
**Fail:** "And-then" plotting — episodic incidents with no causal pressure. The repo's gate
enforces this with **plant-must-precede-payoff** and the unbroken **key-chain**.
**See:** *Quest-relay* · *Plant & payoff* (this file)

### Architectural blueprint *(or just "blueprint")*
**Plain English:** The locked, top-level decision about *how a book is shaped* — its
skeleton — chosen before a word is drafted. Like an architect's drawing: it doesn't say what
colour the walls are, it says where the load-bearing walls go.
**In this project:** RELIC's blueprint is the **quest-relay / set-piece chain** (deliberately
unlike book 1's crisis-loop or book 2's chain-of-proof). The blueprint decides the rules
everything else obeys.
**See:** [`ARCHITECTURE.md`](../ARCHITECTURE.md) (decision D3) · [`craft/CRAFT_DOCTRINE.md`](../craft/CRAFT_DOCTRINE.md) · `storygraph/blueprint_tags.py` (tooling that checks scenes against the blueprint)

### Quest-relay / relay / key-chain
**Plain English:** A story shape where each scene is a baton-pass. The hero **ARRIVES** at a
node, hits an **OBSTACLE**, **READS** the puzzle, pays a **COST**, gets a **KEY**, and
**HANDS OFF** to the next node. The "key-chain" is the unbroken sequence of those keys —
each scene must hand the next one something it needs, so the story can't stall.
**In this project:** The spine of RELIC. The continuity gate hard-fails if the key-chain is
broken (a scene that takes a key it was never handed, or hands off nothing).
**See:** [`CLAUDE.md`](../CLAUDE.md) (pipeline gate) · `books/relic/canon/SET_PIECE_LEDGER.md` · `storygraph/setpieces.py`

### Beat / beats
**Plain English:** The smallest unit of *story movement* — one thing happening that changes
the situation. A scene is made of beats. "The beats of a scene" = its step-by-step pulse.
**In this project:** Beats are the atoms the StoryGraph tracks; continuity, causal order, and
POV are all checked at the beat level.
**See:** `storygraph/DESIGN.md` ("beats/threads are the polygon mesh") · `books/relic/build/log/outline.raw.md` (beats listed per scene)

### Set-piece
**Plain English:** A big, memorable, self-contained dramatic sequence — the chase, the
collapsing tunnel, the flooded chamber. The "money shots" a cinematic adventure is built
around.
**In this project:** Each relay node is a set-piece. There's a literal **Set-Piece Ledger**
tracking every one. A *stalled* or over-explained set-piece is treated as a defect (see
**velocity**).
**See:** `books/relic/canon/SET_PIECE_LEDGER.md` · [`craft/CRAFT_DOCTRINE.md`](../craft/CRAFT_DOCTRINE.md) ("a stalled set-piece is a defect")

### Plant & payoff *(setup / payoff)*
**Plain English:** A **plant** is a detail dropped early and quietly. The **payoff** is the
later moment that detail makes possible or meaningful. Plant the gun in act one; fire it in
act three. Good craft: plant *once*, quietly, then let later scenes assume it.
**In this project:** The gate enforces causal order — a plant must come before its payoff in
beat order.
**See:** [`craft/CRAFT_DOCTRINE.md`](../craft/CRAFT_DOCTRINE.md) (L-02: "plant the climax rhyme early and quietly") · `storygraph/DESIGN.md` ("plant must precede payoff")

### Reverse-payoff / crumb
**Plain English:** A payoff that points *backward* into earlier books. A **crumb** is a small
planted detail that rewards a reader who's read books 1–2 — but must never be *required* to
understand book 3. The rule: crumbs **reward, never require**.
**In this project:** Tracked so none dangles (planted but never paid off) and none is
load-bearing for a newcomer.
**See:** `books/relic/canon/CROSSBOOK_CRUMBS.md` · `storygraph/crumbs.py` · [`CLAUDE.md`](../CLAUDE.md)

### MacGuffin *(McGuffin)*
**Plain English:** An object everyone in the story chases that's really just an excuse to
drive the plot — its *specific nature* doesn't matter (the briefcase, the microfilm).
**In this project:** Deliberately *avoided* as a trap. The gold is **not** a MacGuffin — it's
a functional resonance key that actually does something (tunes the ancient machines). The
distinction is a design rule.
**See:** `books/relic/canon/GOLD.md` · `books/relic/canon/SEED_STORY.md` ("gold is not a MacGuffin") · `DECISIONS.md`

### Outline
**Plain English:** The structured plan of the whole book — scene by scene, with beats,
setting, and POV — written before drafting.
**In this project:** Stage 1 of the pipeline; an AI "structure brain" produces it, blueprint-
aware. Output is machine-readable.
**See:** [`CLAUDE.md`](../CLAUDE.md) (pipeline stage 1) · `books/relic/build/log/outline.raw.md`

### Coda
**Plain English:** A short closing passage *after* the climax — the final chord, the "and
afterward…" that gives a sense of rest. (Italian for "tail".)
**In this project:** RELIC's *Light That Remains* coda. A recurring craft note warns against a
coda that **re-explains the theme one last time** instead of just closing.
**See:** `books/relic/canon/STYLE_GUIDE.md` · `academic/craft/relic-20260602T1157.md` ("the coda re-poeticizes it a fourth time")

### Thesis / theme-said-aloud
**Plain English:** Your **theme** is what the book is *about* underneath (here: the cost of
knowing, consciousness-based reality). A **thesis statement** is the bad habit of having a
character or narrator *say the theme out loud*. Theme should be **embodied** in choices, not
announced.
**In this project:** A named failure mode the engine hunts — "the climax is a forty-page
thesis." There's a tool that ranks thesis-like sentences for cutting.
**See:** [`craft/CRAFT_DOCTRINE.md`](../craft/CRAFT_DOCTRINE.md) ("embody, don't state") · `storygraph/prose_thesis.py` · `academic/craft/relic-20260602T1157.md`

### Dramatic embodiment / "show, don't tell"
**Plain English:** Let the reader *experience* an emotion or fact through action and concrete
detail, rather than being *told* it. "She was furious" (telling) vs. the scene that makes you
feel it (showing/embodiment).
**In this project:** A non-negotiable. Editorial pass: *"is there a line that states what was
already dramatised? Cut it."*
**See:** [`craft/CRAFT_DOCTRINE.md`](../craft/CRAFT_DOCTRINE.md)

### Velocity / propulsive
**Plain English:** Forward momentum — the sense that the story is *pulling* you. A propulsive
book never lets you set it down. In a cinematic adventure, velocity is sacred.
**In this project:** Protected even by the editorial gatekeeper — it will *reject* an edit
that made the prose "better" but smothered the momentum.
**See:** [`ARCHITECTURE.md`](../ARCHITECTURE.md) (D3, D21) · [`craft/CRAFT_DOCTRINE.md`](../craft/CRAFT_DOCTRINE.md) ("velocity is sacred")

### POV (point of view)
**Plain English:** Whose eyes and head we're inside for a given scene. "Sole POV" = the whole
book is filtered through one character.
**In this project:** **Priya Ellis is the sole POV** of RELIC — the co-stars never get the
camera.
**See:** [`CLAUDE.md`](../CLAUDE.md) (creative DNA) · `novelbench/prompts/score-character.md`

### Canon
**Plain English:** The "official truth" of the story world — names, facts, history, rules.
Anything not in canon can be invented; anything that contradicts canon is wrong.
**In this project:** `canon/` is the binding source of truth; the gate enforces it.
**See:** [`ARCHITECTURE.md`](../ARCHITECTURE.md) ("locked story bible") · `books/relic/canon/` · `novelbench/prompts/score-canon-integrity.md`

### Mythos
**Plain English:** The invented belief-system / cosmology of the world (here: Adam's Calendar,
ancient machines, resonance). The **mythos rules** define what's literally true, what's
physically possible, and what stays mystery.
**In this project:** Must read as **grounded engineering, never woo**. A gate flags "woo
leakage" and over-explained mysteries.
**See:** `books/relic/canon/MYTHOS_RULES.md` · `storygraph/mythos.py` · [`ARCHITECTURE.md`](../ARCHITECTURE.md) (D4)

### Two-layer timeline / braid
**Plain English:** Two chronologies running at once — the present-day quest and the ancient
past — that **braid** together (converge) by the end. The braid "closing" means both threads
resolve into one.
**In this project:** The gate asserts the braid closes in Act III and no time-fragment is left
orphaned.
**See:** `books/relic/canon/TIMELINE.md` · `storygraph/timeline2.py` · [`CLAUDE.md`](../CLAUDE.md)

---

## Character & Dialogue

### Character arc / transformation
**Plain English:** How the protagonist *changes* over the book — usually from believing a
**Lie** (a false belief about themselves or the world) toward a **Truth**, paid for in the
climax. Arcs come in three shapes: **positive change** (grows past the Lie), **flat/testing**
(already holds the Truth; the world tests it and they hold), and **negative/fall** (consumed
by the Lie).
**Rule:** Tie the arc to the plot — the external climax should *force* the internal choice, so
story and character resolve in one stroke. Theme is what the arc *proves*.
**Fail:** A protagonist who ends identical to how they began (no arc, or a flat arc with no
real testing pressure); or an arc "told" in a closing monologue rather than *earned* by
choices under cost.
**See:** *Theme / controlling idea* · *Series & Trilogy Architecture* (the Lie/Truth spread
across books)

### Want vs. need *(external goal vs. internal lack)*
**Plain English:** The **want** is the conscious external goal (the artifact, the win); the
**need** is the unconscious internal lack the story actually heals (connection, self-trust).
Great endings often grant the need by *denying or complicating* the want.
**Rule:** Make the want concrete and pursuable scene to scene; let the need surface obliquely,
through choices and contradictions, never as a stated diagnosis.
**Fail:** A character who only has a want (a plot-puppet, no inner life) or only a need (mopey,
no engine). On-the-nose self-analysis ("I realised I'd never let anyone in") states the need
the scenes should embody.

### Agency
**Plain English:** The protagonist *drives* the story through choices, rather than being swept
along by events and rescued by others.
**Rule:** At each turn, the POV character should be making a *decision under pressure* — even
a wrong one. Their choices should cause the next complication.
**Fail:** The passive protagonist — coincidence, other characters, or luck solve the problems;
the hero merely witnesses. (Closely related to the no-scene-goal failure under *Scene &
sequel*.)

### Flat vs. round / static vs. dynamic
**Plain English:** **Round** characters have contradictions and interiority; **flat** ones are
a single note (fine for minor roles). **Dynamic** characters change; **static** ones don't
(also fine, in support).
**Rule:** Spend roundness where it pays — POV and the antagonist especially. A great
antagonist has a coherent want and believes they're right.
**Fail:** A cardboard antagonist who is evil-for-evil's-sake; or every minor character
sketched with main-character depth, drowning the throughline.

### Characterization by contradiction
**Plain English:** People feel real when they *don't fully add up* — the tough one who flinches
at the dentist, the genius who can't park a car. Lamott: pay attention to quirks and
contradictions.
**Rule:** Give important characters at least one telling contradiction, *shown* in behavior.
**Fail:** The "sainted genius" — a character whose only flaw is being too brilliant or too
good. (This repo's editor-feedback method fixes a sainted figure with *un-noble cost to
others*, grafted onto existing scenes, with the narrator refusing to excuse it.)
**See:** *Editor-feedback craft method* (memory) · `academic/EXTERNAL_EDITORIAL_FEEDBACK.md`

### The implicated subject *(Rothberg) — and why it isn't "irony"*
**Plain English:** A precise critical term (Michael Rothberg, *The Implicated Subject: Beyond
Victims and Perpetrators*, 2019) for a person who is **neither perpetrator nor victim** of a
historical wrong, yet is *entangled in and benefits from* the structure that wrong built — and, in
the strong case, can *see* it. The beneficiary who inherits the gift and the wrong together and
refuses to pretend they come apart. It is one of the richest moral positions a character can occupy,
because it has no clean exit: not guilt to be confessed, not innocence to be claimed.
**Rule:** When a character stands in the middle of an injustice they did not commit but live off of,
name the stance **implication**, not *irony*. Build them to **see clearly and act usefully without
asking absolution** — the seeing is the character; the refusal to self-absolve is the dignity.
**Fail:** Reaching for **"irony"** (or *hypocrisy*, *coincidence*, *contradiction*) — each too cold
or too accusatory, and each flattening a lived moral bind into a clever device. Keep the near-words
straight:
> - **Irony** — incongruity observed *from outside*; detached, literary, no skin in it. *(The wrong word here — it stands above the bind instead of inside it.)*
> - **Hypocrisy** — saying one thing while doing another; accusatory, implies bad faith. *(Usually unjust to the beneficiary who actually sees.)*
> - **Contradiction / coincidence** — names a logical clash or a chance, not a moral position.
> - **Ambivalence** — the *felt* version: holding two true, opposing things at once. *(The emotion of implication.)*
> - **Inheritor** — the *plain-image* version: heir to both the gift and the wrong.
> - **Implication** — the *precise* version: structurally entangled, benefiting, responsible-without-being-culpable.
**In this project:** The trilogy's "empire as impact" theme and **Jakobus** are this stance made
flesh — victim of one empire, beneficiary of the next, a man who *sees* — and it is the author's own
ground. Carried as theme and character only, never stated on the page (see *Thesis*; MYTHOS_RULES
Rule 7).
**See:** `books/relic/canon/THEMES.md` ("Empire as impact") · `books/resonance/canon/CHARACTERS.md`
(Jakobus, "Inherited wound") · *Characterization by contradiction* · *Thesis / theme-said-aloud*
(this file)

### Dialogue — subtext
**Plain English:** What characters *mean* under what they *say*. People rarely state feelings
directly; they deflect, fence, and talk around the real subject. The gap between text and
intent is where dialogue lives.
**Rule:** Let characters pursue goals *through* talk; the scene's real subject often goes
unspoken. Trust the reader to read the gap.
**Fail:** **On-the-nose dialogue** — characters saying exactly what they feel and mean ("I'm
angry because you betrayed me"). Flat, and it kills nuance.

### Dialogue — distinct voices *(the noun-swap test)*
**Plain English:** Each character should sound like *only themselves* — diction, rhythm,
register, what they notice — shaped by background and personality.
**Rule:** Run the **noun-swap test**: cover the dialogue tags; if you can't tell who's speaking
from the lines alone, the voices have collapsed. (This is exactly the repo's craft-audit
test.)
**Fail:** **Voice homogenization** — everyone speaking in the same articulate narrator-voice.
The single most common AI-prose failure in dialogue.
**See:** *Voice / voice homogenization* (this file) · `books/<book>/canon/STYLE_GUIDE.md`
(cast voice laws)

### Dialogue — tags & beats
**Plain English:** A **tag** is "she said"; an **action beat** is a bit of business attached to
a line ("She set down the cup. 'Fine.'"). Beats attribute *and* characterize *and* pace.
**Rule:** Default to "said/asked" (they're invisible); attribute only when the reader would
otherwise lose track; prefer an action beat when you also want to show emotion or control
rhythm.
**Fail:** **Said-bookism** — straining for "expostulated / opined / hissed"; adverb-stuffed
tags ("she said angrily") that *tell* the emotion the line should *show*; tagging every line
in an established two-hander (redundant, breaks flow).

### Dialogue — exposition & small talk
**Plain English:** Using dialogue to feed the reader facts the characters already know, or
filling space with hellos and weather.
**Rule:** Cut greetings and logistics; enter late and leave early ("**get in, get out**").
When characters must convey information, give them a *reason* to say it now and an emotion
to say it through; break it across action and reaction.
**Fail:** **"As you know, Bob"** — info-dump-via-dialogue ("As you know, Captain, our ship runs
on dilithium"). And static talking-heads: big undifferentiated blocks with no body, no
setting, no back-and-forth.

### Interiority / thought
**Plain English:** The POV character's inner stream — reactions, judgments, associations — that
prose can render and film can't. The reason to be in a head at all.
**Rule:** Use interiority to *characterize and color*, not to narrate emotion flatly. In close
third, prefer **free indirect style** (see that entry) over tagged "she thought".
**Fail:** **Emotion-naming** ("she felt afraid") instead of rendering the fear; or endless
rumination that stalls the scene (interiority as a substitute for action).

### Rendering genius / augmented cognition *(the deduction cascade; "the interface is the mind")*
**Plain English:** How to put the reader *inside* an exceptional mind so its brilliance is
*experienced*, not asserted. The family of moves: the **deduction cascade** — perception → inference
→ consequence shown as a chain the reader can follow (the red nose, *therefore* years of drinking,
*therefore* the liver is the target); **time-dilation** — the world slows while the mind computes
(Guy Ritchie's pre-visualised fight); the **mind-as-interface reveal** — the viewer assumes a gadget
(AR glasses, floating on-screen text) and then realises the augmentation *is the character's
cognition*, which makes an ordinary-looking person extraordinary; and **characterisation by
omission/contempt** — BBC Sherlock refusing to know the Earth orbits the Sun ("useless to my mind"):
genius defined by what it *won't* hold.
**Rule:** Render genius as a **process the reader can run**, not a magic conclusion — show enough of
the chain that the leap is *earned and thrilling*, never arbitrary. If you use an interface conceit,
**reveal it as the mind**, not the tech. Characterise the mind by its blind spots, costs, and disdain
as much as its powers. Give the antagonist the *same* gift turned to a different end (the mirror:
Moriarty is "almost more interesting" because intellect-as-weapon is the hero's own power without the
brake).
**Fail:** The **informed genius** — *told* brilliant, never *shown* the cascade. The **unearned leap**
— a conclusion with no visible chain (reads as the author cheating). The **over-captioned cascade** —
explaining every step until the magic dies. The **likeable-by-default genius** — sanding off the
contempt and cost that should make the mind *cost* something.
**In this project:** This *is* Priya's and Arin's POV — neurodiverse **pattern-cognition** that
"reads ancient machines"; the trilogy runs the cascade on *engineering* instead of crime. Mercury's
**Moriarty channel** is the intellect-as-weapon mirror, in canon. And the study-Bible reader is
itself a "the-interface-is-the-mind" device — the commentary panel makes the *author's* craft-
cognition visible the way the films make the detective's visible.
**See:** *Interiority / thought* · *Free indirect style* · *Show, don't tell* (this file) ·
`books/resonance/canon/CHARACTERS.md` (Arin; Mercury/Moriarty) · `books/relic/canon/CHARACTERS.md` (Priya)
**References (worked):** Guy Ritchie, *Sherlock Holmes* (2009) — fight pre-visualisation + the
diagnostic read; BBC *Sherlock* (Cumberbatch) — on-screen deduction, the mind palace, the "I deleted
it" solar-system beat; *Elementary* (Jonny Lee Miller).

---

## The Craft of the Sentence

### Show, don't tell *(and when to tell)*
**Plain English:** Render experience through concrete action, sensory detail, dialogue, and
subtext so the reader *feels* it — rather than summarizing it for them. "She was nervous"
(tell) vs. the bitten thumbnail and the unanswered question (show).
**Rule:** Dramatize the moments that *matter* — the emotional and turning beats. **But "show
don't tell" is a half-truth:** *tell* to compress what doesn't matter (transitions, time-
skips, low-stakes logistics) and to control pace. Good prose is mostly judicious telling with
showing reserved for the load-bearing beats.
**Fail:** Two opposite failures — (1) telling the beats that should land ("the climax was
devastating"); (2) *over-showing* trivia, so a character can't cross a room without three
sensory clauses. The repo names a specific case: **stating a line that re-explains what was
already dramatized — cut it.**
**See:** *Dramatic embodiment* (this file)

### Sentence rhythm & length variation
**Plain English:** Prose has a pulse, set mostly by sentence length and structure. Short
sentences punch — urgency, impact. Long sentences flow — atmosphere, contemplation. The mix
*is* the pacing. A short sentence after several long ones lands like a blow; a long one after
clipped dialogue is an exhale.
**Rule:** Vary length and structure deliberately. Speed a scene with short, monosyllabic,
hard-consonant words; slow it with longer, polysyllabic, softer ones. Read aloud — the ear
catches what the eye skims.
**Fail:** **Even cadence** — every sentence roughly the same length and shape, producing a
flat, hypnotic, "mathematically even" rhythm. This is *the* deep machine-tell (see *Evenness
of register*) and the thing the **evenness** scanner exists to catch.
**See:** *Modulation* · *Evenness of register* (this file) · `./run.sh evenness`

### Filter words / distancing
**Plain English:** Words that insert the observer between reader and experience: *saw, heard,
felt, noticed, realized, watched, seemed, looked, thought, decided.* "She saw the door open"
distances; "The door opened" puts us *there*.
**Rule:** In close POV, cut the filter and render the perception directly. Reserve filter
verbs for when the *act of perceiving* is itself the point.
**Fail:** Filter-word fog — every observation routed through "she noticed / she felt / she
saw", flattening immediacy and diluting voice.

### The telling detail / specificity
**Plain English:** One precise, concrete, slightly unexpected detail does more than a pile of
adjectives. The specific (the "first train-coupling device") beats the generic ("a
revolutionary invention"). Concrete nouns and strong verbs over abstraction and modifiers.
**Rule:** Choose the one detail that *implies* the rest; let it carry weight. Prefer the
strong verb to verb-plus-adverb, the exact noun to noun-plus-adjective.
**Fail:** Generic abstraction and "stock" imagery (LLMs default here — replacing the specific
with the smoothly generic). Also **adjective/adverb pile-up** masquerading as richness.

### Purple prose / overwriting
**Plain English:** Prose so ornate it draws attention to itself and away from the story —
straining metaphors, lyricism with no occasion, every noun chaperoned by an adjective.
**Rule:** Earn your lyrical moments by surrounding them with plainness; let ordinary moments
be plainly written. Contrast is what makes the lyrical beat *land*.
**Fail:** **Gravitas inflation** — making *every* moment sound profound, so nothing can be
plain (see *Gravitas / evenness*). Purple prose and AI "elevated" register are the same
disease: relentless significance.

### Clichés & dead metaphor
**Plain English:** Phrases so worn they no longer create an image ("heart pounding", "blood
ran cold", "time stood still", "a shiver down her spine").
**Rule:** Replace the cliché with the *specific* physical truth of *this* character in *this*
moment, or cut it.
**Fail:** Reaching for the nearest stock phrase for any strong feeling — the path of least
resistance, and exactly the statistically-likely path an LLM takes.

### Free indirect style *(free indirect discourse)*
**Plain English:** Close third-person that takes on the *character's* voice and idiom without
tag or quotation marks — the narration thinks in the character's words. "Was she supposed to
just *wait* here? Typical." We're in her head without "she thought".
**Rule:** In close third, slide into the character's diction and judgments; drop the filter
("she thought / she wondered"). It fuses showing and interiority and is the workhorse of
modern close-third fiction.
**Fail:** Whiplash between a neutral narrator and the character's voice; or never committing,
so every thought is tag-bound and distanced.
**See:** *Interiority* · *Filter words* (this file)

### Voice / voice homogenization
**Plain English:** A character's **voice** is their distinctive way of speaking and thinking —
word choice, rhythm, register. **Voice homogenization** is the failure where *everyone sounds
the same* (and usually like an articulate narrator). The test: swap a name on a line of
dialogue — if you can't tell who said it, the voices have collapsed.
**In this project:** Priya's voice (clipped, dry, engineering nouns) is "the spine." The
craft audit runs the noun-swap test.
**See:** `books/relic/canon/STYLE_GUIDE.md` (voice laws) · [`craft/CRAFT_DOCTRINE.md`](../craft/CRAFT_DOCTRINE.md) · [`.claude/skills/de-llm-loop/SKILL.md`](../.claude/skills/de-llm-loop/SKILL.md)

### Modulation
**Plain English:** Variety in the *texture* of the prose — fast vs. slow, plain vs. lyrical,
loud vs. quiet. Without modulation everything reads at the same pitch and the reader goes
numb. "Less polish everywhere, more contrast in the right places."
**In this project:** A structural-audit dimension; the opposite is "evenness of register"
(see below).
**See:** [`.claude/skills/de-llm-loop/SKILL.md`](../.claude/skills/de-llm-loop/SKILL.md) · [`CLAUDE.md`](../CLAUDE.md) (polish mantra)

### Gravitas (inflation) / evenness of register
**Plain English:** **Gravitas** = weight, seriousness. **Gravitas inflation** is the habit of
making *every* moment sound profound and grand — so nothing is allowed to be plain. The
result is **evenness of register**: a flat, uniformly "important" tone that's actually one of
the deepest machine tells.
**In this project:** Flagged as "the gravitas reflex"; the fix is letting ordinary moments
stay ordinary.
**See:** `academic/craft/relic-20260602T1157.md` · `academic/feedback/relic-20260602T1353.md` · [`.claude/skills/de-llm-loop/SKILL.md`](../.claude/skills/de-llm-loop/SKILL.md)

### Reframe ("Not X. Y." device)
**Plain English:** A rhetorical pattern: *"It wasn't fear. It was recognition."* Negate one
thing, assert another. Powerful once — a tic when overused, because it becomes the LLM's
default way of sounding deep.
**In this project:** Capped deliberately (target ~8–10 across the whole trilogy); whole skills
exist to hunt and thin them.
**See:** `prompts/de-llm-pass.md` · `relic-climax-protected-lines` (memory) · [`.claude/skills/de-llm-final-sweep/SKILL.md`](../.claude/skills/de-llm-final-sweep/SKILL.md)

### Tic / machine-tell / LLM tell
**Plain English:** A recurring small habit that gives away the writer — and for AI prose, a
"machine-tell" is a pattern that makes text read as machine-written (over-balanced sentences,
the reframe, em-dash addiction, "the way she…"). The whole de-LLM effort is about removing
these so it "reads like a person wrote it."
**In this project:** Counted by a deterministic scanner against target bands; you can run
`./run.sh tics`.
**See:** `storygraph/prose_tics.py` · [`.claude/skills/de-llm-loop/SKILL.md`](../.claude/skills/de-llm-loop/SKILL.md) · `de-llm-tooling` (memory)

---

## Point of View, Setting & World

### POV types
**Plain English:** Whose consciousness mediates the story, and at what distance.
- **First person** ("I"): maximum intimacy and voice; limited to one knower; risks "I"-fatigue.
- **Second person** ("you"): rare, hypnotic, hard to sustain.
- **Third limited / close third**: "she", anchored to one head per scene; the modern default —
  intimacy of first with the flexibility of third (pairs with *free indirect style*).
- **Third omniscient**: a narrator who knows all heads and facts; powerful for scope, easy to
  turn cold and distant; out of fashion but not wrong.
- **Distance** runs on a slider from *deep* (inside the skull, the character's diction) to
  *distant* (a camera overhead). You can glide along it deliberately within a scene.
**Rule:** Choose a POV and distance that serve the book's intimacy needs, and hold it
consistently within a scene. RELIC is **sole close-third on Priya** — the co-stars never get
the camera.
**Fail:** See *Head-hopping* below.

### Head-hopping vs. omniscient
**Plain English:** **Head-hopping** is *accidentally* slipping into another character's
interiority mid-scene in a limited POV ("She smiled, not knowing he found her annoying").
True omniscient is a *controlled, consistent* all-knowing narrator — a different choice, not
an accident.
**Rule:** In limited POV, you may only report what the POV character could perceive or infer.
Change heads only at a scene/chapter break, clearly signposted.
**Fail:** Unsignaled mid-scene head-hops — the most common POV error; reads as carelessness
and breaks immersion.

### Psychic distance / the camera
**Plain English:** How far "back" the narration stands from the character's mind in any given
sentence — from "It was a cold morning" (far) to "God, would it never warm up?" (deep).
**Rule:** Open a scene at a slightly greater distance, then move *closer* as you engage — and
don't jump the slider abruptly (far→deep in one sentence jars).
**Fail:** Random distance flapping sentence to sentence; or staying so far back the whole book
that nothing is ever felt.

### Tense
**Plain English:** Past tense (default, invisible, flexible) vs. present tense (immediate,
"you-are-there", intense — and tiring over a long book).
**Rule:** Past is the safe default and disappears; choose present only for a deliberate
immediacy effect, and stay consistent.
**Fail:** Unintended tense-slipping mid-scene; or present tense chosen by fashion and then
fighting you across 90k words.

### Setting as character / sense of place
**Plain English:** Place rendered so vividly and specifically that it shapes mood and feels
alive — not a painted backdrop. The repo calls the felt version **place magnetism / wonder of
place**.
**Rule:** Filter setting *through the POV character* — they notice what their history,
profession, and mood make salient (Priya reads a chamber as an engineer would). One precise,
sensory, character-colored detail beats a paragraph of survey.
**Fail:** **Travel-guide / real-estate-listing description** — "nestled", "vibrant", "boasts" —
generic scenery with no POV filter (also a textbook AI tell). Or the opposite: no grounding at
all, characters talking in a white void.
**See:** *Place Magnetism is a trilogy payoff* (memory) · `novelbench` place-magnetism dimension

### Worldbuilding & internal consistency
**Plain English:** The invented rules of the world — its physics, magic, tech, economy,
history — and the discipline of obeying them once set. (For this project, the **mythos rules**
and the grounded-engineering contract.)
**Rule:** Define the rules early and *keep* them; consistency is what buys belief. Track
geography and travel-time so distances stay sane (the "can a bakkie carry that?" class of
check). Reveal the world through *use* and need, not lecture.
**Fail:** Breaking your own rules for plot convenience (a power that vanishes when
inconvenient); **info-dump worldbuilding** (the encyclopedia entry dropped into chapter one);
and the **physical-plausibility gap** — a load, a lift, a travel time that internal continuity
*can't* catch because nothing contradicts it on the page, it's just physically impossible.
**See:** *Mythos* (this file) · *Real-world plausibility gap* (memory) · `storygraph/mythos.py`
· `./run.sh factcheck`

### Exposition / "the iceberg"
**Plain English:** Background the reader needs (history, rules, relationships) and the art of
delivering it invisibly. Hemingway's iceberg: most of what the author knows stays *under* the
water; the prose shows the tip and is stronger for the unseen mass.
**Rule:** Deliver exposition **on a need-to-know basis, late, and in motion** — woven into
action and conflict, never in a standalone lump. Trust the reader to infer; withhold to create
questions.
**Fail:** The **info-dump / "maid-and-butler" exposition**; front-loading backstory before the
reader is invested; explaining what the scene already implied (the over-explanation tell).
**See:** *Dialogue — exposition & small talk* · *Opening / hook* (this file)

---

## Series & Trilogy Architecture

> A trilogy is the three-act structure at the *series* scale: book 1 ≈ Act I (the world and the
> Lie established), book 2 ≈ Act II (the deepening, the false victory/defeat), book 3 ≈ Act III
> (the Truth claimed). The acts don't divide cleanly at the book seams — the overarching Act II
> typically opens ~¾ through book 1 and closes ~¼ into book 3.
>
> **Named form in this house:** the **Triptych Trilogy** (*Tryptych form*) — three panel-complete
> novels, weave-closed, readable in any order. Distinct from a serial trilogy (must read 1→2→3)
> and from a loose shared universe. See the dedicated entry below.

### Triptych Trilogy · *Tryptych form*
**Plain English:** A named three-novel form AJ Greyling claims and demonstrated in *The African Gold
Trilogy*: three **panels** (each a complete novel), hinged by **weave motifs** (recurring objects,
characters, ideas, images) into one closed work — and readable in **any order**. Like a painted
triptych altarpiece: each wing is a finished image; together they mean more; the eye may begin at
any panel. The house sometimes spells it **Tryptych** (the D-006 coinage: the *try* of any-order
reading + the art-historical *triptych*).

**The three proof obligations (falsifiable):**
1. **Panel-completeness (standalone-intact)** — each volume satisfies alone; a newcomer to any one
   book is never confused and reaches a satisfying close. No weave appearance is *load-bearing* for
   its own panel's plot.
2. **Weave-closure** — motifs span ≥2 panels and resolve across the set; **spine motifs** span all
   three and carry the load-bearing braid. The whole exceeds the sum of its panels.
3. **Order-independence (any-order readability)** — every reading permutation is valid, complete,
   and enriched. There is no privileged "book 1."

**Rule:** Design **mutual** appearances — a panel both *seeds* forward and *lands* something seeded
elsewhere — so no panel is pure setup or pure payoff. That is what frees reading order. Track every
weave motif; enforce standalone-intactness as a hard constraint, not a hope. Order-independence is
**not** order-invariance: each order produces a *distinct* trajectory (e.g. enter through the
cinematic capstone → pure reverse-payoff afterward). Differences must be **enrichments, never
requirements**.

**Fail:** A **serial trilogy** masquerading as a triptych (volume 3 requires 1→2); a **loose shared
universe** with no closed weave; **load-bearing crumbs** (newcomer lost); claiming all orders feel
*identical* (weaker and false); a middle panel that is only connective tissue with no arc of its own.

**Vocabulary:** *panel* · *hinge* · *weave motif / crumb* · *seed / landing / mutual* · *spine motif*
· *reverse-payoff* · *standalone-intactness*.

**In this project:** exemplified by *The African Gold Trilogy* (RESONANCE · REVELATION · RELIC) —
three distinct genres as deliberate **contrast** (low cross-book structural resemblance is the
design, not a defect). Five spine motifs: resonance-gold, the-court, stewardship, all-the-same,
builders-deep-history.

**See:** *Standalone-completeness rule* · *Reverse-payoff / crumb* · *Capstone / finale form* (this
file)

### Overarching arc vs. per-book arc
**Plain English:** A series runs *two* structures at once: each book is a **complete arc**
(its own incite, midpoint, climax, resolution), *and* every book advances a **series arc** that
only completes in the finale. The protagonist gets a "mini" transformation per book that is a
**symptom** of the larger Lie they finally shed at series' end.
**Rule:** Plan the *overarching* plot and the Lie→Truth journey first; then decide where each
book begins and ends within it; then outline each book to be self-contained. Each book pays off
*its own* promise while planting the next.
**Fail:** A "book" that is really just act two of a longer thing — no inciting incident of its
own, no resolution, just a middle that stops. Readers feel cheated; the volume can't stand
alone.

### Standalone-completeness rule
**Plain English:** Each volume must satisfy on its own — a newcomer starting at book 3 should
get a complete, comprehensible story — while rewarding the series reader more.
**Rule:** In this project this is **D-locked**: RELIC is *100% standalone* for a newcomer and
*openly the finale* for a series reader. Series payoffs **reward, never require**.
**Fail:** Load-bearing dependence on prior books (a newcomer is lost), *or* the opposite —
amnesiac standalone-ness that ignores the series and gives returning readers nothing.
**See:** *Reverse-payoff / crumb* (this file) · `books/relic/canon/CROSSBOOK_CRUMBS.md`

### Reverse-payoff / crumb *(series-scale plant & payoff)*
**Plain English:** A detail in a later book that pays off *backward* into earlier ones,
rewarding the reader who's read them — without ever being required to follow the current book.
(Full entry under *Reverse-payoff / crumb* in Structure & Story.)
**Rule:** Track every crumb so none dangles and none becomes load-bearing for a newcomer.
**See:** *Reverse-payoff / crumb* (this file) · `storygraph/crumbs.py`

### Second-book syndrome / "middle book" problem
**Plain English:** The classic trap: the middle volume sags because it neither sets up (book 1
did) nor resolves (book 3 will), so it becomes connective tissue with no spine of its own.
**Rule:** Give the middle book its *own* dramatic question, midpoint, and resolution — a
complete arc that *also* turns the series. Raise the series stakes here; end on a genuine
reversal, not just a cliffhanger comma.
**Fail:** A middle book that is all setup-for-book-3 and table-setting; a "to be continued"
with no satisfaction of its own.

### Capstone / finale form
**Plain English:** The final volume must close *both* structures — resolve its own plot *and*
deliver the series-arc Truth and the accumulated reverse-payoffs — without collapsing into a
checklist of callbacks.
**Rule:** Pay off the series promises through the *same* climactic action that resolves the
finale's own plot; let the Truth be *demonstrated*, not narrated. (The **Triptych Trilogy / Tryptych
form** judge tests exactly this at series scale: do the panels stand alone, do the spine motifs all
resolve, does the capstone land?)
**Fail:** A finale that becomes a museum tour of earlier books; or one that resolves the series
theme by *saying it aloud* in a closing coda (the theme-said-aloud tell, at series scale).
**See:** *Triptych Trilogy · Tryptych form* · *Coda* · *Thesis* (this file)

### Adaptation — transposition vs. reskinning *(deep-structure fidelity)*
**Plain English:** Adapting or modernising a story *well* means carrying its **deep structure** — the
arc, the theme/moral, and the craft engine (the POV frame, the central device, the antagonist
relation) — into a new setting, and changing surfaces **only where the deep structure demands it.**
*Reskinning* is the failure mode: swapping props (horses → taxis) while leaving the engine untouched,
so nothing that matters has actually moved.
**Rule:** For each element ask "**what is the engine here, and what in the new world produces the same
engine?**" Transpose the engine; let surfaces follow. A great modernisation is as *of its own moment*
as the original was of its — the author's and reader's shared present (its wars, technologies,
anxieties) carried as theme **in the characters' interior lives**, not as set-dressing.
**Fail:** **Reskinning** (cosmetic swaps over a dead structure); **setting-as-decor** (the new era is
scenery, never felt inside anyone); **fidelity-as-taxidermy** (so reverent to the original's surfaces
it forgets the original was *alive in its own time*, which is the very thing to reproduce).
**In this project:** the `modern-sherlock` spin-off's binding doctrine — reproduce each Doyle work's
arc/moral/structure/craft, transposed to a post-9/11, social-media, surveillance present. Also the
deep-vs-shallow distinction behind the platform's **clone** feature.
**See:** *Reverse-payoff / crumb* · *Rendering genius / augmented cognition* · *Theme / controlling
idea* (this file) · `arjuna-badger-press/projects/modern-sherlock/canon/ADAPTATION_DOCTRINE.md`

### Consistency bible / story bible
**Plain English:** The maintained record of canon across the series — names, dates, rules,
descriptions, who-knows-what-when — so book 3 doesn't contradict book 1.
**Rule:** Keep a single source of truth and consult it; in this project that's `canon/` plus
the StoryGraph, the **two-layer timeline**, and the **set-piece ledger**, enforced by the gate.
**Fail:** Drift — an eye color, a death, a travel-time, a capability that changes between
volumes because no one kept the ledger.
**See:** *Canon* · *Continuity* · *Two-layer timeline* (this file)

---

## The Editorial Ladder

> Editing is **not one task** — it's a sequence of passes from the largest structural concern
> down to the smallest mark, done **in that order** (fixing commas before fixing the plot is
> wasted work, because the plot fix deletes the sentences). Each rung is a distinct skill an
> editorial course teaches as a separate discipline. The cardinal rule between rungs: **get
> distance first** (see *Rest / fresh eyes*).

### 1 · Developmental / structural edit *(the "big picture")*
**Plain English:** The highest rung. Does the *story* work? — premise, plot architecture,
character arcs, pacing, stakes, theme, POV strategy, the saggy middle, whether scenes earn
their place. Wholesale: scenes get cut, added, reordered, rewritten.
**Rule:** Do this **first** and alone, on the cold read. Ask of every scene: *does it turn?
does it advance plot or character? would the book survive its deletion?* If yes to the last,
cut it.
**Fail:** Skipping it (polishing prose on a broken structure) — the most expensive mistake in
revision.
**See:** *Craft audit* (this file) · `./run.sh craft-audit`

### 2 · Line edit *(the prose layer)*
**Plain English:** Sentence-by-sentence *craft* (not correctness): rhythm, word choice, voice,
clarity, imagery, cutting flab, killing clichés and filter words, varying cadence, sharpening
specificity. The art-level pass.
**Rule:** Read for the ear; cut what doesn't earn its place; protect *earned* voice (the
`keep_if` guard — don't sand a deliberate roughness into smooth nothing). This is the rung the
**de-llm-loop** and **cold read** operate on.
**Fail:** Over-sanding to a uniform "correct" smoothness — which is itself the evenness machine-
tell. A line edit can *create* AI-flavor if it homogenizes.
**See:** *The Craft of the Sentence* (whole section) · *Cold read* · [`.claude/skills/de-llm-loop/SKILL.md`](../.claude/skills/de-llm-loop/SKILL.md)

### 3 · Copy edit *(correctness & consistency)*
**Plain English:** Grammar, usage, punctuation, spelling, tense consistency, and *continuity*
of fact (eye color, timeline, who-knows-what). Conforms the text to a style sheet.
**Rule:** Mechanical correctness *and* internal consistency. In this project the continuity
half is enforced by the **gate** (re-ingest + check_constraints); the language half is a human/
style-sheet pass.
**Fail:** Letting continuity errors through (the object in two places, the forgotten fact) —
the class the **StoryGraph** and **timeline** exist to catch.
**See:** *Continuity* · *Gate* · *Two-layer timeline* (this file)

### 4 · Proofread *(the last look)*
**Plain English:** The final sweep on the typeset/near-final text — typos, stray spaces, bad
breaks, formatting slips. No story or style changes; just catching what survived.
**Rule:** Last rung, on the formatted artifact, ideally fresh eyes. Read slowly; the brain
auto-corrects what it expects.
**Fail:** Treating proofreading as editing (or vice versa) — conflating the rungs wastes both.

### Beta readers / fresh eyes
**Plain English:** Real outside readers who report where they were bored, confused, or pulled
out — catching motivation holes and "doesn't-feel-right" beats the author is blind to.
**Rule:** Use them *after* your own developmental pass, *before* the final polish; weight
*patterns* across readers over any single reaction. (The repo's analogue: multiple independent
agent reads + the convergence rule — convergence across reviewers is the signal; a lone cold
read can misread series intent.)
**Fail:** Acting on one reader's idiosyncrasy as if it were consensus; or skipping outside eyes
entirely and trusting your own blind spots.
**See:** *Editor-feedback craft method* · *NovelBench judge noise* (memory)

---

## Pitfalls & Machine-Tells *(the self-audit)*

> **The most important section for AI-authored prose.** Read it as a checklist when editing or
> cold-reading. The deepest tells are not individual words — they are *statistical habits*:
> over-balance, over-evenness, over-significance, and the absence of a situated speaker. The
> word-lists are downstream symptoms; the rhythm and stance are the disease. The history-
> scoring finding in this repo is blunt about it: single-shot Claude on a human premise drafted
> *cleaner* (~22–27 tells/10k) than the multi-pass engine (~91) — so leverage lives at the
> *prompt and surgical-edit* layer, not in another rewrite pass.

> **The habit above the tell.** This section lists *sentence-level* tells. The recurring craft
> *habits* one level up — the protagonist always right, the scene that explains itself, the world
> omniscient when convenient, every reveal "a deeper layer", every relationship a tidy mirror — are
> catalogued as 16 named anti-patterns (software-smell style, BAD→GOOD demos, tagged to the engine
> layer that prevents each) in [`craft/ANTI_PATTERNS.md`](../craft/ANTI_PATTERNS.md). The structural
> ones can only be designed out at *outline* time; the line-level ones at *draft* time. The master
> anti-pattern, **interpretive overcompletion**, is the same rule as the one-revision-rule below.

> **Worked examples (few-shot) — the companion to this section.** Abstract failure-names are
> weaker teachers than a real BAD→GOOD pair in the book's own voice. The canonical bank is
> [`academic/craft-examples/RESONANCE_BADGOOD.md`](../academic/craft-examples/RESONANCE_BADGOOD.md):
> 15 verbatim line-level fixes from an external read, each tagged to the de-llm-pass move and the
> `prose_tics` pattern it exercises, plus the 7 named recurring errors (telegraphed inevitability,
> interpretive redundancy, aphoristic overreach, mythic inflation, retrospective sanctification,
> conceptual overclarification, prestige-TV cadence) and the one revision rule below. Read the
> matching pair there before making a cut you're unsure of.

### The root cause: no situated speaker
**Plain English:** AI prose tends to emerge "from nowhere, addressed to no one, with no stake
in its claims." Agency is systematically obscured; it reads as compulsively revised but never
*improvised* — frictionless transitions, mathematically even cadence, uniform sentiment with
no abrupt emotional modulation.
**Fix:** Anchor every passage in a *specific* consciousness with a *stake* (in fiction: the
POV character's want, mood, history, and bias coloring every observation). Let sentiment lurch
where a real mind would lurch. Allow friction, asymmetry, the unsmoothed edge.
**See:** *Free indirect style* · *Voice* · *Evenness of register* (this file)

### Negative parallelism / the reframe *("Not X, but Y")*
**Plain English:** "It wasn't fear. It was recognition." / "Not just X, but Y." / "No A, no B —
just C." A genuine rhetorical move that LLMs reach for compulsively as their default way of
*sounding deep*. (Roughly 6% of ChatGPT messages contain a "not just X, but Y" variant.)
**Fix:** Powerful **once**; a tell in bulk. This project caps it deliberately (target ~8–10
across the *whole trilogy*) and runs skills to hunt and thin it. Replace with a single direct
assertion, or with the dramatized thing itself.
**See:** *Reframe ("Not X. Y." device)* (this file) · `prompts/de-llm-pass.md` · *RELIC climax
protected lines* (memory — note which reframes are real vs. paraphrase)

### Gravitas inflation / evenness of register
**Plain English:** Every moment made to sound profound; nothing allowed to be plain or
throwaway. Produces a flat, uniformly "important" tone — one of the deepest tells, because real
prose breathes between high and low.
**Fix:** Let ordinary moments stay ordinary. Earn the lyrical beat with surrounding plainness.
Vary the *pitch*, not just the sentence length.
**See:** *Gravitas (inflation) / evenness of register* · *Modulation* (this file) · `./run.sh
evenness`

### The "AI vocabulary" cluster
**Plain English:** Words and connectives that spike in LLM output: *delve, intricate,
underscore, tapestry, testament, showcase, vibrant, robust, meticulous, pivotal, crucial,
landscape, realm, foster, garner, navigate (figurative), interplay, nuanced, multifaceted,
underscore, boasts, nestled,* plus connective tics *moreover, furthermore, additionally,
notably, importantly.*
**Fix:** Not a banned-word list to mechanically purge (that's cargo-cult — see memory), but a
*flag*: a cluster of these in a passage usually means the prose has drifted to generic register.
Rewrite the passage for specificity and a situated voice; the words fall away on their own.
**See:** *Guardrail register thesis* (memory — framing alone doesn't evade; grounding does) ·
`storygraph/prose_tics.py` · `./run.sh tics`

### Rule-of-three overuse
**Plain English:** Three adjectives, three parallel clauses, three-item lists — everywhere. The
triad is satisfying *once*; as a default rhythm it's a metronome.
**Fix:** Break the pattern — use two, or four, or one. Let lists be uneven.

### "Serves as / stands as / represents" *(verb-of-significance)*
**Plain English:** Avoiding plain *is/has/was* in favor of inflated linking verbs: "the chamber
*serves as* a key", "she *stands as* a reminder", "it *represents* a shift." Pairs with
unsupported claims about what things "highlight" or "underscore."
**Fix:** Prefer the plain verb. If a thing's significance matters, *dramatize* it; don't assert
it with a fancy copula.

### Frictionless transitions / textbook paragraphing
**Plain English:** Every paragraph a tidy topic-sentence-then-support; every transition a smooth
connective; no jump-cuts, no white-space leaps, no trusting the reader to bridge a gap.
**Fix:** Allow hard cuts and juxtaposition. Real narrative leaps; it doesn't escort the reader
across every threshold by the elbow.

### Em-dash & punctuation tics
**Plain English:** Over-reliance on the em dash where a comma, colon, or full stop belongs; also
curly-quote/formatting artifacts and over-bolding when prose bleeds in from a chat context.
**Fix:** Vary the punctuation; reserve the em dash for genuine interruption or apposition. (This
project tracks dash density per book.)
**See:** `./run.sh tics` · the de-llm dash skills

### Over-explanation / the caption tell
**Plain English:** Stating the meaning of an image or action *right after* showing it — the
narrative equivalent of captioning a photo you can already see. "She slammed the door. She was
furious."
**Fix:** **Trust the reader.** If the action carried it, cut the caption. The repo's standing
editorial question: *"is there a line that states what was already dramatised? Cut it."*
**See:** *Show, don't tell* · *Dramatic embodiment* · *Thesis* (this file)

### The hedge / the gentle wrap-up
**Plain English:** Reflexive softeners and tidy summarizing closers — "it's understandable
that…", "ultimately…", "in many ways…", an ending that gently restates everything. AI sounds
*friendly in a way no adult actually sounds.*
**Fix:** Cut the hedge; end on the image or the beat, not a summary of it. Let endings be
abrupt where abruptness is truer.

### Generic over specific *(the smoothing tell)*
**Plain English:** LLMs replace the precise, unusual, load-bearing detail with a smoother,
more-positive generic one (the "inventor of the first train-coupling device" becomes "a
revolutionary titan of industry").
**Fix:** Hunt the generic noun/claim and restore the *specific* one — the odd, true, exact
detail. Specificity is the antidote to nearly every tell in this section.
**See:** *The telling detail / specificity* (this file)

---

### Human pitfalls *(not AI-specific, but degree-level basics)*

- **Info-dumping / the "as you know, Bob":** backstory or worldbuilding delivered in a lump,
  often via dialogue. → Distribute, delay, dramatize. *(See Exposition.)*
- **The saggy middle:** Act II with no midpoint pivot and no escalating stakes. → Give the
  middle its own turn and rising cost. *(See Three-act, Stakes.)*
- **Passive protagonist:** events happen *to* the hero; coincidence solves problems. → Restore
  agency and scene-goals. *(See Agency, Scene & sequel.)*
- **Mary Sue / sainted character:** flawless, unchallenged, beloved by all. → Add a real flaw
  with cost to others. *(See Characterization by contradiction.)*
- **On-the-nose dialogue & emotion-naming:** characters state feelings directly. → Subtext;
  render, don't label. *(See Dialogue — subtext, Interiority.)*
- **Purple prose:** ornament with no occasion. → Earn lyricism with surrounding plainness.
- **Head-hopping:** unsignaled POV slips. → Hold one head per scene. *(See POV.)*
- **Deus ex machina:** an unearned external rescue resolves the climax. → The resolution must
  be *paid for* by the protagonist's choices and the planted setups.
- **Telling the climax / unearned emotion:** asserting the big feeling instead of building to
  it. → The reader must be *invested* before the payoff; dramatize the beats that matter.
- **Cliffhanger-as-substitute-for-arc:** ending a volume on a comma instead of a resolution.
  → Each book completes its own promise. *(See Standalone-completeness.)*
- **Starting too early:** the "average Tuesday" opening. → Start at the change. *(See Opening.)*
- **Physical-plausibility gap:** a load/lift/travel-time that's internally consistent but
  physically impossible — continuity tools *cannot* catch it. → A deliberate physical-limits
  read. *(See Worldbuilding; memory: real-world plausibility gap.)*

### The one revision rule *(the self-audit, distilled)*
After every strong paragraph, ask: **"Did I dramatize this — or dramatize it *and then certify
its importance*?"** If the second, cut the certification. This single question catches the
largest class of tells in this section (over-explanation, the caption, theme-said-aloud,
aphoristic overreach, post-beat interpretation) in one pass. The companion bank shows it on 15
real cases: [`academic/craft-examples/RESONANCE_BADGOOD.md`](../academic/craft-examples/RESONANCE_BADGOOD.md).

---

## The Machinery (this repo's quality tools)

### Rubric
**Plain English:** A scoring grid — the explicit criteria something is judged against, with
weights. "By the rubric" = measured against agreed standards, not vibes.
**In this project:** Each book is scored on a rubric weighted to fit its blueprint
(*rubric ≈ blueprint*) — character, story-mechanics, place-magnetism, reader-experience,
emotional-impact.
**See:** `novelbench/config.py` · `novelbench/prompts/score-*.md` · `craft/QUALITY_BAR.md`

### Gate / gatekeeper
**Plain English:** A **gate** is an automatic checkpoint that *blocks* progress if rules are
broken (continuity, key-chain, timeline, mythos). A **gatekeeper** here also means the final
*editorial* judge that can reject a polish pass for hurting the book (e.g. killing velocity).
**In this project:** A hard pre-commit check; `./run.sh gate`.
**See:** [`CLAUDE.md`](../CLAUDE.md) (pipeline stage 2c′) · [`.claude/skills/novel-engine/SKILL.md`](../.claude/skills/novel-engine/SKILL.md)

### Continuity
**Plain English:** Internal consistency over time — the same object can't be in two places at
once, eye colour can't change, yesterday's event must stay happened.
**In this project:** Audited per chapter (stage 2c) and enforced by the StoryGraph.
**See:** [`CLAUDE.md`](../CLAUDE.md) · `storygraph/DESIGN.md` · `prompts/continuity.md`

### Cold read
**Plain English:** Reading a manuscript with *fresh eyes and no context* — no notes, no
intentions — to judge how it actually lands for a stranger. The most honest critique.
**In this project:** A brutal editorial agent given no canon/prompts, so it judges the prose
cold at the sentence layer.
**See:** [`.claude/skills/de-llm-loop/SKILL.md`](../.claude/skills/de-llm-loop/SKILL.md) · `./run.sh cold-read`

### Craft audit
**Plain English:** A structural critique one level *above* the sentence — voice, modulation,
reveal order, abstract drift. The "second pair of eyes" on architecture, not commas.
**In this project:** Encodes three real external professional edits; `./run.sh craft-audit`.
**See:** [`.claude/skills/de-llm-loop/SKILL.md`](../.claude/skills/de-llm-loop/SKILL.md) · `academic/EXTERNAL_EDITORIAL_FEEDBACK.md`

---

## Book Furniture (the parts that aren't the story)

### Front matter
**Plain English:** Everything before chapter one — title page, copyright, dedication,
epigraph. "Back matter" is the stuff after the last chapter.
**In this project:** Built by `merge()`; the dedication/crest live in repo front matter, not
inside the story.
**See:** [`ARCHITECTURE.md`](../ARCHITECTURE.md) (D9) · `print-frontmatter` (memory)

### Epigraph
**Plain English:** A short quotation at the start of a book or chapter that sets a mood or
theme. Must *earn its place* — never decoration.
**See:** `books/relic/canon/EPIGRAPHS.md` · `books/relic/canon/STYLE_GUIDE.md`

### Colophon
**Plain English:** A small publisher's/printer's mark or note (often a logo or a line about
how the book was made), traditionally at the very end or on the title page.
**In this project:** The gold-thread house mark; works small as a spine colophon.
**See:** `design/COVER_SYSTEM.md` · [`ARCHITECTURE.md`](../ARCHITECTURE.md)

---

## Sources & Further Reading

The taught-craft sections above synthesize freely-available creative-writing and editorial
resources. Primary anchors:

**Open textbooks & courses**
- [*Elements of Creative Writing* (2nd ed.), Morgan/Schraffenberger/Tracey — Open Textbook Library](https://open.umn.edu/opentextbooks/textbooks/1483) — free OER textbook; fiction chapters on plotting, showing & telling, characterization, dialogue, setting/voice, POV, the unwritten rules.
- [*Write or Left* — Open Textbook Library](https://open.umn.edu/opentextbooks/textbooks/1127) · *The Anti-Textbook of Writing* (OER).
- [MIT OpenCourseWare — free writing courses](https://openlearning.mit.edu/news/fuel-your-passion-storytelling-16-free-online-courses-mit) (Playwriting, the Essay, Reading & Writing Autobiography).
- [NYU Creative Writing research guides](https://guides.nyu.edu/creative-writing/resources-by-genre).

**Structure**
- [Save the Cat beat sheet — Jessica Brody](https://www.jessicabrody.com/2020/11/how-to-write-your-novel-using-the-save-the-cat-beat-sheet/) · [Savannah Gilbo](https://www.savannahgilbo.com/blog/plotting-save-the-cat) · [Kindlepreneur](https://kindlepreneur.com/save-the-cat-beat-sheet/).
- [Scene & sequel (Dwight Swain) — September C. Fawkes](https://www.septembercfawkes.com/2021/09/scene-structure-according-to-dwight-v.html) · [Wikipedia: Scene and sequel](https://en.wikipedia.org/wiki/Scene_and_sequel) · [Advanced Fiction Writing — "Writing the Perfect Scene"](https://www.advancedfictionwriting.com/articles/writing-the-perfect-scene/).
- [Three-act vs. Hero's Journey — Darling Axe](https://darlingaxe.com/blogs/news/three-act-hero-journey).
- [Theme / controlling idea — Story Grid](https://storygrid.com/story-theme/) · [Helping Writers Become Authors](https://www.helpingwritersbecomeauthors.com/the-secret-to-writing-strong-themes/).
- [Opening pages — what agents see (Alyssa Matesic)](https://www.alyssamatesic.com/free-writing-resources/mistakes-in-your-first-ten-pages) · [getaliteraryagent.com](https://getaliteraryagent.com/writers-first-pages-chapters-literary-agents/).

**Character, dialogue, prose**
- [Show, don't tell — Writers.com](https://writers.com/show-dont-tell-writing) · [the "big myth" counterpoint — PenUltimate](https://penultimateword.com/editing-blogs/why-show-dont-tell-is-the-big-myth-of-fiction-writing/).
- [Dialogue tips — The Center for Fiction](https://centerforfiction.org/writing-tools/tips-for-writing-dialogue/) · [NY Book Editors](https://nybookeditors.com/2017/05/your-guide-to-writing-better-dialogue/).
- [Sentence rhythm & pacing — River Editor](https://rivereditor.com/guides/how-to-vary-sentence-structure-control-reading-rhythm-2026) · [Novela Studio](https://novela.so/en/blog/how-to-use-prose-rhythm).
- Foundational craft books (not free, but canonical): Anne Lamott, *Bird by Bird* ([PDF excerpt](https://publish.illinois.edu/marylucillehays/files/2014/07/Lamott_Bird-by-Bird-1.pdf)); Stephen King, *On Writing*; Dwight Swain, *Techniques of the Selling Writer*; Robert McKee, *Story*; Ursula K. Le Guin, *Steering the Craft*.

**Continuity, worldbuilding, series**
- [Plot holes — ProWritingAid](https://prowritingaid.com/art/1603/plot-holes-and-how-to-fix-them.aspx) · [the 7 types — BlurbBio](https://app.blurbbio.com/blog/fix-plot-holes).
- [Worldbuilding resources — Richie Billing](https://richiebilling.com/worldbuilding/worldbuilding-resources) · SFWA Fantasy Worldbuilding Questions.
- [Series/character arcs — Helping Writers Become Authors](https://www.helpingwritersbecomeauthors.com/character-arcs-in-a-series/) · [Four ways to plot a trilogy — Well-Storied](https://www.well-storied.com/blog/4-ways-to-plot-a-trilogy) · [Second-book syndrome — GoBookMart](https://gobookmart.com/how-to-write-a-trilogy-without-falling-victim-to-second-book-syndrome/).

**Editorial process & the LLM-tell layer**
- [Editing levels (free mini-course) — Louise Harnby](https://www.louiseharnbyproofreader.com/editing-levels.html) — proofread vs. copy vs. line vs. developmental, and the order of play.
- [From first draft to final manuscript — BubbleCow](https://bubblecow.com/blog/book-editing/editorial-process/from-first-draft-to-final-manuscript-the-editing-journey/) · [the revision flowchart — Lisa Poisso](https://www.lisapoisso.com/2018/04/11/editing-and-revision-process/).
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) — the most rigorous public catalog of LLM tells (vocabulary, negative parallelism, rule-of-three, significance-inflation, formatting artifacts).
- [How AI prose diverges from human writing — Reuters Institute](https://reutersinstitute.politics.ox.ac.uk/news/how-ai-generated-prose-diverges-human-writing-and-why-it-matters) · ['AI tells' detection rubric](https://gist.github.com/lmmx/d91de290ea4e6d9631e32c2dd43da413).

**Worked-example banks (few-shot, this project's own)**
- [`craft/ANTI_PATTERNS.md`](../craft/ANTI_PATTERNS.md) — the book-agnostic **anti-pattern catalog**: 20 named craft smells (the habit above the sentence-tell), BAD→GOOD demos, each tagged to the engine layer (outline/draft/edit) and its scanner that prevents/measures it, + the **three-book convergence table** (the root smells all three independent reviews flagged — the engine's top-priority fixes) + the 5-pass revision protocol. Synthesized from all three external reads; binds all books.
- [`academic/craft-examples/RESONANCE_BADGOOD.md`](../academic/craft-examples/RESONANCE_BADGOOD.md) — 15 BAD→GOOD line-level fixes in RESONANCE's voice + 7 named errors + the one revision rule.
- [`academic/craft-examples/RELIC_BADGOOD.md`](../academic/craft-examples/RELIC_BADGOOD.md) — 10 named anti-patterns with a BAD→BETTER→BEST ladder, each tied to its existing `prose_tics` scanner band, + 8 runnable revision rules. (REVELATION's worked pairs live in the catalog itself.) Each book's bank keeps BAD exact and GOOD in *that book's* voice; grows per book.
- [`academic/EXTERNAL_EDITORIAL_FEEDBACK.md`](../academic/EXTERNAL_EDITORIAL_FEEDBACK.md) — the three external professional developmental edits and where each note is encoded in the engine.
- [`academic/LINE_EDIT_DIRECTIVES.md`](../academic/LINE_EDIT_DIRECTIVES.md) — the canonical internal line-edit, source of the tic target bands.

> These are *starting points*, not authorities — the binding craft for this project is in
> `craft/CRAFT_DOCTRINE.md`, each book's `STYLE_GUIDE.md`, and the external professional edits
> recorded in `academic/EXTERNAL_EDITORIAL_FEEDBACK.md`. Where the general advice and a real
> editor's note on *these* books disagree, the editor's note wins. The worked-example banks are
> the few-shot layer: when an abstract rule and a concrete pair both apply, follow the pair.

---

*Want a term added or one explained deeper? It belongs here — this file is meant to grow.
Concepts come from the craft tradition; the **Rule/Fail** framing and repo cross-links are
this project's own, tuned for an editor-in-the-loop AI workflow.*
