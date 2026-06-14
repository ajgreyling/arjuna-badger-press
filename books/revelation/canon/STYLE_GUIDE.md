# STYLE_GUIDE.md

## Point of View and Tense
The narrative will be told from a third-person limited point of view, focusing primarily on Dr. Leila Aziz. The tense will be past tense, allowing for a reflective exploration of her journey and experiences as she uncovers the layers of conspiracy surrounding the Brotherhood of Abraham.

## Voice & Register
The voice should be authoritative yet accessible, reflecting the intellectual rigor of Dr. Aziz while maintaining a sense of urgency and suspense. The register will balance scholarly insights with the thrill of a contemporary adventure, engaging readers intellectually without alienating them with overly complex jargon.

## Sentence Rhythm
Vary sentence length to create a dynamic pace. Short, punchy sentences should punctuate tense moments, while longer, more complex sentences can be used to convey deeper thoughts and elaborate on intricate ideas. This rhythm will help maintain tension and keep readers engaged.

## Dialogue Style
Dialogue should be sharp, realistic, and reflective of character backgrounds. It should serve to advance the plot and reveal character motivations while incorporating subtext, particularly in conversations involving faith, power, and betrayal. Characters should speak in a way that reflects their knowledge and experiences, with Dr. Aziz often using academic language contrasted with more colloquial speech from other characters, highlighting class and cultural differences.

## DO's
1. **Integrate Historical Context**: Weave in historical facts and cultural references seamlessly to enrich the narrative and deepen readers' understanding of the Brotherhood and their motivations.
2. **Create Tension**: Use cliffhangers and suspenseful moments to keep readers on the edge of their seats, particularly during key revelations or confrontations.
3. **Explore Themes of Faith**: Engage thoughtfully with themes of religion, faith, and the search for truth, allowing characters to grapple with their beliefs in a nuanced manner.
4. **Focus on Character Development**: Ensure Dr. Aziz’s internal struggles are mirrored in her external actions, allowing her to evolve throughout the story as she confronts her father's legacy and her own fears.
5. **Maintain a Sense of Hope**: Despite the dark themes, infuse the narrative with moments of optimism, showcasing the resilience of individuals seeking peace and understanding.

## DON'Ts
1. **Avoid Clichés**: Steer clear of predictable plot twists and tired tropes. Strive for originality in character motivations and narrative developments.
2. **Do Not Oversimplify Religion**: Treat religious themes with respect and complexity, avoiding reductionist views that could alienate readers or misrepresent beliefs.
3. **Resist Excessive Exposition**: Show rather than tell. Avoid lengthy exposition dumps; instead, reveal critical information through character interactions and discoveries.
4. **Don’t Diminish Stakes**: Ensure that the threat posed by the suppression network — the institutional curators of doctrinal alteration — remains palpable throughout the narrative; do not allow any side plots to overshadow the central conflict. Frame the antagonist force in concrete institutional/political terms (suppression, narrative management, manufactured discredit), never as a cosmological or Satanic ("Luciferian") force.
5. **Avoid Unnecessary Violence**: While mature themes are welcome, avoid gratuitous violence or sensationalism that detracts from the story's intellectual and emotional core.

## Machine-tell taboos (the de-LLM contract) — BINDING

This prose can be clean at the sentence level and still out itself as machine-written through a few
recurring rhetorical moves — the tells contemporary LLM prose leaves. They are tics *because the
underlying moves are good*; the whole job is thinning them, not banning them. The draft / line /
gatekeeper / triage passes enforce this; `./run.sh tics` counts each tell against a target band
(advisory). Source: `academic/LINE_EDIT_DIRECTIVES.md`.

The deepest tell is **evenness** — one intelligence narrating everything at the same temperature.
Real novels are lumpier: let some pages be plain (subject, verb, object, period), and under-write
the connective tissue so the charged reveals land.

The named tells — cut on sight, keep only the genuinely earned:

1. **"almost [emotion]"** ("almost smiled / almost laughed / almost gentle") — a non-event standing
   in for a real feeling. Write the physical fact or cut the tag; reserve for a true
   edge-of-expression beat (3–4 in the book).
2. **The reframe** "It wasn't X. It was Y." / "not X, but Y." — a thinking-*shape* performing a turn
   on demand. Kill the same-sentence version (X invented only to pivot off it); keep a reframe only
   when a belief the reader held is genuinely overturned.
3. **The em-dash:** set **tight** (`word—word`), never spaced (`word — word` is the machine
   fingerprint — and REVELATION currently runs entirely spaced, which is the copyedit tell to fix).
   Ration to a few deliberate ones a chapter — keep it for a real dialogue interruption or a genuine
   mid-thought swerve; a parenthetical aside wants commas/parens, an end-of-sentence reframe a period.
4. **"something" as a feeling-placeholder** ("something moved in her face") — name the muscle or cut
   to the action.
5. **"the way…"** — over-used and load-bearing for characterization (how Leila reads a text, weighs
   a variant); at scale it becomes authorial reflex. Never two in a paragraph; keep the ~40% that
   illuminate, state the rest directly.
6. **"Not a question." / "Not a boast."** tags — throat-clearing; delete and trust the line.
7. **The "which from [Name] meant…" translation** and the **stacked trailing-"which" sentence** —
   keep 2–3 widest-gap translations; in a stack cut the clause that re-states the prior one in
   warmer words. Don't do the reader's interpreting for them — Leila's mind should *move in
   analogy and historical depth*, not narrate its own inferences in layered "which" clauses.

Also flagged by the **FOSS-mined rule set** (word lists lifted from `write-good` (MIT) and `proselint`
(BSD) — rules, not the tools; counted by `./run.sh tics`):
8. **Hedges** ("seemed to / appeared to", "perhaps", "somewhat", "sort of") — commit the claim or own
   the uncertainty as Leila's read; keep the few where not-knowing is the point.
9. **Weasel words** ("obviously / clearly / literally / actually / basically") — emphasis without
   evidence; "literally / actually" almost always delete clean.
10. **"very/really [word]"** — replace with the precise stronger word; keep "very" only in spoken voice.
11. **Wordy connectives** ("the fact that" → "that", "in order to" → "to", "in terms of" → rephrase) —
   pure padding.
12. **Classic clichés** (proselint list) — REVELATION is clean of these; target 0, any hit is a new
   one to cut on sight.

The deepest tell — **evenness** — is now measurable: `./run.sh evenness` reports per-chapter
sentence/paragraph rhythm variance (FREE, local); a chapter that reads machine-even trips ≥2 floors —
go vary its rhythm there. Complements, never replaces, the read.

Do **not** trade one tell for another. Vary the fix — a human hand, not a fresh macro. Leila's
interior should read differently from a systems-engineer's: textual, associative, weighing sources —
distinct in *rhythm*, not just vocabulary.

## Tone of Named Companions
Echo the gripping, intellectual thrill found in Dan Brown's works, particularly in novels like "The Da Vinci Code" and "Inferno." The tone should evoke a sense of urgency and intrigue, with layered plots that encourage readers to think critically about the information presented. The narrative should maintain an engaging balance between mystery, historical exploration, and personal struggle, leaving readers both shaken and hopeful by the end.

## Character voice laws (craft-audited — differentiate by cognitive habit, not vocabulary)

> The external developmental edit's most-repeated note: *"a brilliant author ventriloquizing six
> people who all attended the same graduate seminar."* The fix is a one-line **voice law** per major
> character — a *cognitive habit* (how the mind moves under pressure), not a belief. These laws are
> the editor's own, sharpened to the updated REVELATION report (Priority 2 "Differentiate supporting
> voices harder" + Priority 5 "watch cumulative solemnity"). The craft audit
> (`./run.sh --book revelation craft-audit`) judges every line against them, and the polish loop's
> character-diagnose pass now flags `voice_homogenization` against these same laws.

- **Leila (lead)** — *brilliance as work, not as a gift.* Gets 80% fast and 20% late; revises
  herself; one wrong first read, corrected; a tactile check before the conclusion; slowed by fear,
  exhaustion, grief. **Process, never just outcome.** Scholar's scruple — provenance before meaning.
  Under peak stress her syntax should *break*, not refine.
  - ✓ WOULD say: "No — wait. The hand's wrong. Same scribe as folio nine, but the ink's later. I
    need the other leaf before I trust any of this."
  - ✗ Would NEVER say: "What this truly reveals is that the conspiracy was never about suppression
    but about the curation of meaning itself." *(the captioned thesis, arriving frictionless — that
    is the house voice, not Leila)*
- **Abdi** — *operational, dry, under-explains — and elliptical.* Field-made, not novel-made:
  "Truth's the easy part. It's the morning after that buries people." Answers sidelong, and
  sometimes doesn't answer — trails off, changes the subject, lets a silence stand where a thesis
  would go. More field-practical than thesis-forward; occasionally emotionally withheld, not
  expansive. Withholds badly once; gets territorial; right in substance, wrong in tact.
  - ✓ WOULD say: "Don't take the coast road." *(beat)* "I'll explain when we're moving."
  - ✗ Would NEVER say: "We must consider that the institution's true function is not preservation
    but control." *(philosophical thesis-framing — Abdi gives you the move, not the meaning)*
- **Miriam** — *fast, interruptive, evaluative, professionally predatory — and the book's air valve.*
  Talks in appetite and publishability, not maxims: "No. Stop. The conspiracy's wallpaper. *You're*
  the story." Faster than everyone, journalist-specific (angle, source, deadline, what's printable),
  and **not philosophically polished UNLESS she's framing a public narrative** — then she gets
  rhetorical on purpose, because spin is her craft. She is where the book breathes: human awkwardness,
  irritation, dry humor, bodily reality, social friction not tied to the thesis. Use her energy to
  break the cumulative solemnity. Pushes too early once; misjudges what's printable.
  - ✓ WOULD say: "Who else has this? Nobody. Good. Then we're not asking permission, we're asking
    forgiveness — after it runs. Are you eating that?"
  - ✗ Would NEVER say: "There is something almost sacred about the custody of truth." *(the grave,
    unhurried register; Miriam is appetite and deadline, never reverent unless she's selling it)*
- **Samuel** — *institutionally old, paternal, used to being obeyed — composed, but not perfectly
  self-aware.* Elegantly sequenced truth, graceful to a fault; speaks of *keeping* and *deciding who
  gets it*, not of preserving truth in the abstract. He carries the unconscious authority of a man
  long obeyed (he expects the room to wait for him; he is surprised when it doesn't), and he is *less*
  self-aware in the moment than he believes — dodges clumsily once, because he's actually ashamed.
  Not perfectly calibrated: a stubborn old man with odd habits and a blind spot, not a flawless
  philosopher of stewardship.
  - ✓ WOULD say: "Sit. You'll have it when I'm ready to give it to you, and not before. I have kept
    worse things than your patience."
  - ✗ Would NEVER say: "You're right to be angry — I've been protecting my own comfort." *(too
    self-aware, too soon; Samuel only sees his own shame sidelong, and late)*
- **Tewodros** — *scholar-monk, not tribunal.* Economical, severe, anti-grandiose: the dry verdict,
  never the flourish ("You didn't take the reading that helped you. Good. Most do."). The register is
  the cell and the manuscript desk, NOT the bench — austere from discipline, not from judging others.
  Sometimes dry or **impatient in idiosyncratic ways** (a scholar's irritation at sloppiness), not the
  voice of austere intellectual legitimacy on cue.
  - ✓ WOULD say: "Your transcription is sloppy. The third word is *qene*, not *qen*. Fix it, then
    come back."
  - ✗ Would NEVER say: "History will judge what we have done here, and it will not be kind."
    *(grand, tribunal-from-on-high; Tewodros judges a transcription, not History)*
- **Devlin (antagonist)** — *articulate because power trained him to be — and a little vain.* Keeps
  the *world* from raw certainty, not a falsehood from the world; touches the object (the shelf) and
  lets it carry the menace. Administratively cold. But carry a thread of **vanity** — he likes being
  the cleverest person in the room and it occasionally leaks — and make him **less eager to articulate
  his own moral defense so cleanly**: let him deflect, change the subject, or imply rather than deliver
  the speechified custodian-of-necessary-fiction monologue. The human asymmetry deepens him.
  - ✓ WOULD say: "You read the marginalia. Of course you did." *(a small, pleased smile)* "Most
    people don't get that far. Have you eaten? We can do this over a decent lunch."
  - ✗ Would NEVER say: "I am not your enemy. I am the necessary fiction that keeps the world from
    tearing itself apart over a truth it cannot hold." *(the speechified custodian monologue — let
    the shelf and the deflection carry the menace instead)*

**The distinctness tests (craft-audit enforces):**
- **The noun-swap test** — *could another character say this line with only a noun swap? If yes,
  rewrite.* Read each character's dialogue alone; if a line could belong to another, it's homogenized.
- **One aphorism per pressure point, one mouth** — reserve the quote-card line for a true peak; never
  the resting pulse, never two mouths completing the same "not-X" turn in a scene.
- **Let supporting characters fail in their own style** — each major secondary gets a beat where a
  strength becomes a liability (this is *canon-adjacent*: the craft audit flags it, the author adds
  the beat).

**Worked bank:** REVELATION's own BAD→GOOD pairs (the "closing the building" graded rewrites, the
per-character flaw prescriptions, the 8-point scene checklist) are in
[`academic/craft-examples/REVELATION_BADGOOD.md`](../../../academic/craft-examples/REVELATION_BADGOOD.md)
— two external reads distilled, including the new `prebuttal` (don't litigate the book's own case) and
`negative_space` (leave a margin where no caption goes) smells.

**The anti-pattern catalog (engine-wide, REVELATION is the worked example).** The voice laws above
are the *character* contract; the recurring craft *habits* this book taught the engine — competence
cascade, one-paragraph total epiphany, atmospheric overwrite, thesis leakage, villain-cloud
omniscience, sacred-reveal inflation, voice homogenization, analysis-before-body, theme-declared,
frictionless clues, delivery-system characters, prestige-sentence addiction, research display, timed
warnings, moral symmetry, and the master **interpretive overcompletion** — are catalogued with
BAD→GOOD demos and engine-layer tags in [`craft/ANTI_PATTERNS.md`](../../../craft/ANTI_PATTERNS.md).
The structural ones are designed out at outline time (`prompts/outline.md`); the line-level ones are
pre-empted at draft and caught by triage/line/gatekeeper. The single rule that subsumes the most:
*you have the scene, the object, the pattern — the sentence that then explains what it means is
usually the cut. Trust drama over explanation; character limitation over protagonist brilliance.*

## Editorial revision directives (auto-applied)

_Folded in from an editorial review. The full rubric lives in `prompts/revision-skill.md`; the high-order rules:_

- Momentum & Chapter Hooks: End each chapter with a decision, reversal, discovery, betrayal, or narrowing option.
- Dramatize-Don't-Explain: Show, don't tell: Use actions and dialogue to reveal character and plot.
- Cutting Repeated Exposition: Eliminate redundant scenes and dialogue that repeat known information.
- Protagonist Agency: Ensure the protagonist actively solves problems and drives the plot.
- Staggered Certainty: Introduce evidence in stages, allowing for misinterpretations and evolving theories.
- Sharper Antagonist Presence: Introduce the antagonist's influence early and make it tangible.
- Concrete Forensic Evidence: Build 6–8 recurring, specific pieces of evidence central to the plot.
- Voice-Differentiated Dialogue: Distinguish characters through unique speech patterns and perspectives.
- Prose Tightening in Action: Use precise, economical language in action scenes.
- Varied Emotional Beats: Avoid melodramatic phrasing; opt for specific, character-driven emotional responses.
- Puzzle/Clue Chains: Construct a logical sequence of clues leading to revelations.

## Editorial revision directives — review-005 (re-open pass, 2026-05-30)

_The corrective second movement to the review-004 block above. review-004 gave the book bones
(clarity, propulsion, the three-proof spine); review-005 puts blood back into the places the
compression cost. **These two blocks are additive, not contradictory** — keep the clarity, and
restore the doubt and dread. Where review-004 said "cut/tighten/accelerate," review-005 says
"re-open/re-densify/expand" — but only in the load-bearing places named below, never as a return to
vagueness or padding._

- Restore selective ambiguity: allies *curate*; disclosure is *tactical*; truth arrives pre-framed
  even from people trying to help. Whenever a helpful character hands Leila information, the prose
  should let her (and the reader) feel what they're withholding and what they want her to conclude —
  without making them liars. Intentional pressure, not duplicity.
- Dramatize aftermath, don't abridge it: consequences of a revelation should *wound in scene* — an
  embodied human cost (a frightened believer, a sermon misusing the evidence), not a summary
  paragraph. Make hope costly.
- Expand load-bearing forensic scenes: when a revelation is structurally important (above all the
  Covenant-as-derivative in ch-11), let the reader *watch Leila make the inference on the page* —
  object → reading → discrepancy → implication → only then the theme. Don't deliver the conclusion
  pre-digested.
- Keep theory attached to scene pressure: no idea arrives a beat before the tension that earns it.
- Protect Leila's restraint but let the discipline visibly cost: a delay before speaking, a re-read,
  fingers held too still — the method should occasionally falter before it reasserts.
- Soften unresolved-mastermind threads into distributed institutional pressure: "a committee, an
  office, a channel larger than one man." Antagonist force = architecture, never a single hidden
  face awaiting a sequel (reinforces DON'T #4 above).
- Don't let Devlin be the *sole* articulate voice of institutional complexity — Samuel must be
  nearly as dangerous in a different register.

### The masterpiece-campaign laws (2026-06-03 — binding; full versions in `craft/CRAFT_DOCTRINE.md` L-04..L-09)

The final developmental edit's core note: *"the main thing between this book and greatness is not
talent, it is restraint"* — Leila "too right, too often"; Devlin "too good"; ending "too consoling";
everyone "a visiting professor of the thesis." The durable fixes, proven on this book:
- **Give Leila ONE confident, costly, *textual* mistake the narrator doesn't excuse (L-06).** At
  Tewodros's test she reads the verb WRONG first — an "error of appetite," the reading "she walked in
  already wanting" — before the scribe's own pen disproves it; she goes red; "the exact thing I'd have
  failed a student for." Her later rigor is then *earned*, and it rhymes with the Covenant-as-
  derivative reveal (loving a reading into truth). Costs nothing in plot, everything in character.
- **The antagonist gets one embarrassingly-mortal want (L-07).** Devlin fusses the codex square and
  admits, the cadence slightly *wrong*, that he killed Abebe partly because the one peer who could
  "see the hand" refused the other chair — "he wanted a friend and settled for a corpse." Less
  magisterial; real self-deception, not elegant rationalization.
- **Voice: distinguish by cognitive MOVEMENT, not vocabulary (the noun-swap test, L-04).** Leila's
  climax must move in her *periodic, recursive, qualify-before-landing* shape ("If this were one
  altered verb I would not waste the room's time… But…"), never the clipped negation-pivot ("Not a
  translation. An administrative instruction") — that's Priya's shape, and it makes all three trilogy
  climaxes rhyme mechanically. Some characters must evade, ramble, want the wrong thing: Miriam's
  hunger must actually *tempt distortion* (the "write toward murder, every word true" ask), not just
  be flagged — a knife, not a scalpel.
- **Ending: hope not certainty + the self-implicating needle (L-08).** Turn the book's own
  "all custodianship curdles" thesis on Leila, who at the end *is* the authority: she chose the
  twelve, wrote the rules, "could feel how good it felt to own the writing of it," doesn't know if
  she'll keep her own *no-authority-exempt* clause when it costs. Resolve this needle *through* the
  L-06 mistake — her one failure becomes the only safeguard against her becoming Devlin. NB: the
  office-behind-Devlin "layer" is the thematic point (faceless persistent power), NOT reveal-inflation
  to cut.
