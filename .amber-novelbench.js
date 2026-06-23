export const meta = {
  name: 'amber-novelbench',
  description: 'Full NovelBench metered LLM-judge scorecard for Die Vuur in die Donker: one calibrated judge per NovelBench dimension (the authentic 7-dimension rubric), scoring the polished book, then a synthesis.',
  phases: [{ title: 'Judge' }, { title: 'Synthesise' }],
}

const BOOK = args.book          // full polished BOOK.md text
const EVIDENCE = args.evidence  // deterministic metrics block

const SCALE = [
  "0-2 = broken/amateur. 3-5 = busy, ornamental, info-dense, or flat even if grammatically clean.",
  "6-7 = COMPETENT-BUT-FLAWED (this is where most real prose lands — do not inflate above it without cause).",
  "8 = genuinely controlled and distinctive. 9-10 = an experienced editor would not meaningfully improve it.",
  "Be CALIBRATED, NOT GENEROUS. Use the full range. Reserve 9-10.",
].join(" ")

const BOOKFACTS = [
  "BOOK: 'Die Vuur in die Donker' (Winter sonder Einde, Boek I) — an ADULT historical Norse/Viking saga IN AFRIKAANS, written in André P. Brink's literary register with Kleinboer's frankness, at the ceiling of Arjuna Badger Press's 'The Salt Veil'.",
  "PREMISE/INTENT: Þórdís ('Tóra', 38), the lady (vrou van die huis) of a west-Norwegian fjord-hall, her fire gone to embers under a tender-but-lukewarm 20-year marriage to Hákon (a good, tired man — never a villain). Over one long winter she WAKES: a far-traveller (Eivor) and a shield-maiden (Solveig) winter in the hall; an old seeress (Heiðr) cracks open her latent 'sien' (seiðr) gift; slavers (Styrbjorn) take the thrall Yrsa off the ice and Tóra LEADS the rescue in Hákon's absence. She chooses, openly, to live again — and pays a price. Closed-door ending, no cliffhanger; mirrors the prologue (her hands at the slaughter-post).",
  "DELIBERATE CRAFT: long Brink-style accreting sentences; ATTENTION as the emotional/erotic instrument; the THRESHOLD-CLOSE (intimacy goes up to the act, then the door closes — 'dit is hulle s'n' — never explicit); CHOICE ('oopoog') as the spine of every intimate scene. Three intimate threads (Eivor; Solveig — a true mutual love between two women; the remade marriage), all between consenting adults, all threshold-closed. Hard gates: no minors in any sexual light; consent the engine; violence/un-freedom only ever a wound, never heat.",
  "DO NOT penalise: the threshold-close as 'withholding' (it is the chosen, correct register, like Brink); Afrikaans morphology depressing MATTR (the English NovelBench curves over-punish it — judge the prose on top of the number); recurring load-bearing motifs (the amber stone; 'die sien'; the hnefatafl king-piece 'jy wen deur te weet jy kan loop') where they EARN repetition across the arc.",
].join("\n")

const DIMS = [
  { key: 'reader_experience', title: 'Reader Experience', subs: ['hook','readability','pacing','suspense','momentum','immersion','stickiness','would_continue'],
    lens: "Does it pull a reader in and keep them? Hook, readability, pacing, suspense, momentum, immersion, stickiness, and would_continue (would an adult reader of literary historical fiction keep going / buy book II?)." },
  { key: 'emotional_impact', title: 'Emotional Impact', subs: ['resonance','tension','wonder','grief','hope','fear','catharsis','ending_impact'],
    lens: "Does it land emotionally? The waking, the lukewarm-marriage grief, the heat of being SEEN, the ice-rescue fear, the farewells, the prologue-mirror ending. Score ending_impact on ch-13 specifically." },
  { key: 'character', title: 'Character', subs: ['arc_consistency','emotional_progression','motivation_clarity','dialogue_authenticity','relationship_evolution'],
    lens: "Tóra's arc (keel→fire→leader); Hákon never a villain; Eivor (gentle+reckless); Solveig; Heiðr; Yrsa. Dialogue authenticity in Afrikaans; relationship evolution across the three intimate threads + the marriage." },
  { key: 'story_mechanics', title: 'Story Mechanics', subs: ['setup_payoff','unresolved_threads','plot_coherence','scene_purpose','stakes_escalation','reveal_effectiveness'],
    lens: "Setup/payoff (the amber given in ch-12 & held in ch-13; the hnefatafl king; the seiðr-vision of Styrbjorn's ship paying off in the raid); unresolved_threads (Book I should close its own door cleanly — Sǫlveig leaves with spring, Eivor rows out, by design, NOT dangling); plot coherence; scene purpose; stakes escalation to the ice-rescue; reveal effectiveness." },
  { key: 'prose_quality', title: 'Prose Quality', subs: ['repetition','sentence_variety','over_description','exposition_density','passive_voice','dialogue_ratio','lexical_diversity','register_evenness','scene_cadence'],
    lens: "The Brink/Kleinboer register. Anchor to the EVIDENCE numbers and grade ON TOP. repetition (echoes/tics — a polish pass thinned 'som/oopoog/werktuig'); sentence_variety (CV 1.18 = strong); over_description (lyric AFTER a scene closes?); exposition_density (history lived vs lectured); lexical_diversity (defer to MATTR but DO NOT penalise Afrikaans morphology); register_evenness; scene_cadence. dialogue_ratio reported as a fraction." },
  { key: 'canon_integrity', title: 'Worldbuilding / Canon Integrity', subs: ['contradictions','timeline','location','object_continuity','lore'],
    lens: "9th-c. Norse material culture (longhouse/saal, langvuur, blót/offerfees, hnefatafl/koningspel, seiðr/die sien, oval brooches, the amber-road) — consistent and historically grounded (no horned helmets)? Timeline (one winter, vetrnætr→thaw; Tóra 38; Rognvaldr 17 a boy throughout); location (the fjord, the ice); object continuity (the amber, the whalebone king, Yrsa's wooden cup); lore (how the sien works, its price). Flag any contradiction with a quote." },
  { key: 'place_magnetism', title: 'Place Magnetism', subs: ['site_specificity','sensory_truth','awe_through_craft','dual_lens','no_travelogue_stall','would_visit'],
    lens: "The wonder of the place — the long winter hall, the frozen fjord, the seiðr-night, the feast. Site specificity, sensory truth (smell of the langvuur, salt-fish, wool, mead), awe through craft (not travelogue), no stall, would_visit (does the reader long for this world?)." },
]

const DIM_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['dimension','score','sub_scores','standout_moments','drag_sections','editor_notes'],
  properties: {
    dimension: { type: 'string' },
    score: { type: 'number', description: '0-10 judged whole (not a mechanical average)' },
    sub_scores: { type: 'object', additionalProperties: { type: 'number' }, description: 'one 0-10 per sub-metric (dialogue_ratio as a fraction)' },
    standout_moments: { type: 'array', items: { type: 'string' }, description: 'quote-anchored highs' },
    drag_sections: { type: 'array', items: { type: 'string' }, description: 'quote-anchored lows / what to fix' },
    editor_notes: { type: 'string', description: 'blunt, actionable, quote-grounded' },
  },
}

phase('Judge')
const scores = await parallel(DIMS.map(d => () => agent(
  `Jy is 'n GEKALIBREERDE ontwikkelingsredakteur wat EEN dimension van 'n volledige roman beoordeel volgens die NovelBench-rubriek. Jy lees Afrikaans vlot en beoordeel dit as Afrikaanse letterkunde.

DIMENSION: ${d.title}
SUB-METRIEKE (gee elk 'n 0-10, behalwe dialogue_ratio = breuk): ${d.subs.join(', ')}
LENS: ${d.lens}

SKAAL: ${SCALE}

DIE BOEK SE BEDOELING (beoordeel die prosa hierteen):
${BOOKFACTS}

DETERMINISTIESE BEWYS (vooraf gemeet — behandel as grondwaarheid; beoordeel BO-OP die syfers):
${EVIDENCE}

METODE: (1) lees teen die bedoeling; anker aan die bewys-syfers waar gegee. (2) elke sub-telling se rasionaal MOET 'n aangehaalde stuk teks of presiese plek noem — 'n telling sonder aanhaling word nie vertrou nie. (3) rol op tot EEN 'score' (0-10) as 'n beoordeelde geheel, nie 'n meganiese gemiddeld nie. (4) wees bot en konkреet in editor_notes. Moenie die drumpel-sluit as 'n fout straf nie (dis die gekose register). Moenie Afrikaans straf vir lae MATTR nie.

DIE VOLLE BOEK:
${BOOK}`,
  { label: `judge:${d.key}`, phase: 'Judge', schema: DIM_SCHEMA, effort: 'high' }
).then(r => ({ key: d.key, title: d.title, ...(r || { score: null }) }))))

const valid = scores.filter(s => s && typeof s.score === 'number')
const overall = valid.length ? Math.round((valid.reduce((a, s) => a + s.score, 0) / valid.length) * 10) / 10 : null

phase('Synthesise')
const summary = await agent(
  `Jy is die NovelBench-hoofredakteur. Hier is die dimensie-tellings vir 'Die Vuur in die Donker' (Afrikaanse Viking-saga, Brink-register). Skryf 'n bondige, eerlike scorecard-opsomming: die boek se werklike sterktes, sy 2-3 grootste swakhede (kwoteer), en 'n finale oordeel oor of dit publikasie-gereed is vir 'n volwasse Afrikaanse letterkunde-leser. Wees gekalibreer, nie vleiend nie.

OORHOOFSE GEMIDDELD: ${overall}
DIMENSIE-TELLINGS:
${valid.map(s => `- ${s.title}: ${s.score}/10 — ${s.editor_notes}`).join("\n")}`,
  { label: 'synthesis', phase: 'Synthesise', effort: 'high' }
)

return { overall, dimensions: valid.map(s => ({ dimension: s.title, score: s.score, sub_scores: s.sub_scores, standout_moments: s.standout_moments, drag_sections: s.drag_sections, editor_notes: s.editor_notes })), synthesis: summary }
