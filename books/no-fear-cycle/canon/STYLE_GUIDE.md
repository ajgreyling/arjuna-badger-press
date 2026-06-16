# STYLE GUIDE — *Ordinance Pending*

> Binding voice laws for Book I. Gate + de-LLM scanners enforce these patterns.

## Mantra

**Less emphasis, more trust; less explanation, more embodiment; silence is load-bearing.**

## POV voice architecture (Pass 3 — binding)

### Metaurus (Bladeguard Sergeant, sus-an / litany POV)

- **Sentence shape:** longer in quiet beats; recursive private litany; clauses that drift into memory before snapping back.
- **Observation type:** doctrine-as-grief — he names what he has lost, not what things mean.
- **Permitted:** hesitation, warmth buried in armour, the weight of years, HUD read as elegy.
- **Forbidden:** Titus-style inventory counting; one-word fragment closers; `Not X. Y.` negation snaps.
- **HUD:** organs and skull icons carry emotion; sus-an membrane speaks in fragments he cannot reach vox.

### Titus (Lieutenant, close third)

- **Sentence shape:** stimulus → response; short declaratives; action before interpretation.
- **Observation type:** geometry, mag-count, seal status, vectors — never thesis statements.
- **Permitted:** flat procedural counting; wired vox only; one `I confirm` per scene max.
- **Forbidden:** aphorism closers (`Geometry. Finality.`, `Efficient.`, `Red.`); empty-room restatements after ch-02; `Reading was how they got you` after first boot-stomp; negation-reframe chains.
- **Death beats:** KIA registers in the body first (pause, reload, check seal) — meaning delayed or cut.

### Kael (Enginseer, Mechanicus)

- **Register:** binary under breath, then plain vox; measurements before metaphors.
- **Shape:** `[serial] — [percentage/status]. [protocol step]. [next action].`
- **Forbidden:** aphorisms; sharing Voren's load-order diction.
- **Permitted:** one failure beat where correct protocol costs seconds she did not price.

### Voren (Techmarine, forge adjunct)

- **Register:** serial scans, clamp protocol, load balance; no salute required.
- **Shape:** `[serial] — [status]. [action]. [next step].`
- **Forbidden:** Kael's binary prayer; Everson's chaplain cadence.

### Apothecary Everson

- **Register:** clinical record first; dissent logged in full sentences, not clipped diagnostics.
- **Shape:** speaks to the slate as much as the Marine; names organs; jaw tightens when emotion leaks.
- **Forbidden:** `Logged.` / `Acceptable.` / Titus-register terseness.

### Navy forge adjunct Pell (convoy tender)

- **Register:** letter-writing dread; complaints about paperwork; longer sentences than Voren.
- **Forbidden:** Mechanicus binary; Marine `I confirm` echoes.

### Orte / Corvus / battle-brothers

- **Silhouette only in combat** — heavy, assault, intercessor; speech is orders and cover calls, not philosophy.

### Court channels (Judge / Mother / Wolf / Mercury / Atlas / Librarian)

- **Judge:** formal record, complete sentences, no poetry — `"Primary holder confirmation required. Ground truth telemetry wavering. Confirm receipt."`
- **Wolf:** imperatives only, 3–5 words max — `"Take keys. Hold."` / `"Scouts only. Hold."`
- **Mother:** warmth without aphorism, practical — `"He is stable. Your heart rate is high. Drink if you have water."`
- **Fool:** wrong syntax, interruption, non-sequitur once per book — `"—keys—mud—"` (bleed half a second; Judge does not acknowledge)
- **Librarian / Atlas / Mercury:** domain vocabulary only; no maxim cadence shared with Wolf

### Register modulation (Pass 13 — binding)

- **Combat / undercroft peaks:** wrought syntax permitted; body leads; break sentences under fire
- **Logistics chapters (ch-17/18/99):** plain tired prose — incomplete sentences, vox typos, servitor interruptions, ration-bar mundanity; **no scene-closer epigrams**
- Reader must feel temperature shift between combat and decon/staging/convoy prep

### Dialogue voice examples (Pass 10 — binding)

| Speaker | Example line | Anti-pattern |
|---|---|---|
| Kael | "Node Two. Distance four hundred. Bearing two-seven-zero. Capacitor seven zero." | "The arithmetic is the same. The water is not." |
| Voren | "Clamp two. Green rune. Chain integrity eighty-six. Reclamation at dock." | "That is not doubt. That is procedure." |
| Everson | "Burn tolerance marginal on file. Fifth dissent logged. Captain countersigned without Apothecarium review." | "Logged." / clipped Wolf-channel terseness |
| Castell / Orte | "Knee vent holding. Still in shadow. Do not move your boots." | Philosophy under fire |
| Titus | "Shadow holds." / "I confirm." | Maxims, thesis statements |
| Metaurus (spoken) | "Left flank." / "Stay." | Litany or aphorism in vox to squad |

## Sentence layer

- **End on object/action** — after a dramatized beat (knife placed, skull icon red, bolt through throat), cut the sentence whose only job is to state what it meant. No italic gloss. No nothing/everything antithesis. The test: *can this paragraph end one sentence sooner?*
- **HUD before lore** — organs, seals, skull icons carry emotion; never wiki-speak.
- **Silence-first combat** — long wordless stretches permitted; banter is failure.
- **No quips under fire** — Titus is empty, not witty.
- **Place before clue** — one or two sensory facts per location may exist without mechanism caption.

## Taboos (machine-tells)

> **Pass 11 changelog (2026-06-15):** `nfc_hud_repeat` tell; one HUD block per combat scene rule.
> **Pass 12 changelog (2026-06-15):** `nfc_looking_was` tell; looking-was-how cluster ban (≤3 book-wide).
> **Pass 13 changelog (2026-06-15):** `nfc_theme_caption` tell; channel voice split (Judge/Wolf/Mother/Fool); register modulation in Act III logistics; Castell bearing callbacks Mace + Dyrias only; `reframe_fragment` target ≤8.
> **Pass 15 changelog (2026-06-15):** `nfc_hold_closer` max 4; `nfc_parchment_step` max 12; `nfc_inventory_check` one full scene (ch-17); relay nodes ch-07 impedance / ch-10 bleed / ch-13 choke / ch-15 pod-ring.
> **Pass 16 changelog (2026-06-16):** `nfc_parchment_step` max **10**; `nfc_caption_after` / `nfc_caption_pair` max **2** each; Castell timeline locked (ch-02 wrong bearing → hour-14 KIA; ch-04 drop-pod Marine is **Vess**); Act III tail — ch-17 transit only, ch-18 Novahistorium + Apothecarium, ch-99 sole departure anchor; one HUD stake block per act in undercroft (ch-09/10/11); foreword meta trimmed.

### Caption sweep checklist (apply before merge — Pass 16)

After every action/HUD/kill paragraph, ask:

1. **Can this end one sentence sooner?** If the last sentence only glosses what the boot/knife/HUD already said — cut it.
2. **Antithesis pair?** (`X was nothing. X was everything.` / `Symmetry was not comfort.`) — delete the second sentence.
3. **Thesis tail?** (`That was the point of…`, `Minutes were a language…`, `because counting kept him…`) — cut unless load-bearing once per act.
4. **Prophecy robe?** Forward-narration of payoff — cut; end on object (knife chip, seal print, skull icon).

- "almost [emotion]" as crutch
- Spaced em-dash ` — ` as fingerprint (prefer tight or period)
- **"Not X. Y." reframe** — max **1 per scene**; **`reframe_fragment` ≤8 book-wide**; strip from chapter closes (keep Corvus dialogue `Not fear. Fact.` only)
- **HUD status blocks** — **one consolidated block per combat scene max**; prose carries between. Cut verbatim refrains (`bead pulsed bronze`, `breathed once per minute`, `did not flicker`) to ≤3 book-wide (`nfc_hud_repeat`)
- **Hour-stamp HUD ledgers** — `Hour one:` / `At hour sixty` — **one block per act max**; collapse lists to one compressed paragraph + one dramatized exchange
- **Conserve-chain ladders** — `X conserved Y. Y conserved Z.` — state causal link once; no four-rung recursion
- **Caption-after-beat** — cut restating sentence after discovery/kill; end one sentence sooner (see `EXTERNAL_EDITORIAL_FEEDBACK.md`)
- **Parchment loop** — max **10 step-on beats book-wide** (`nfc_parchment_step`); cut explanation lines ("Library reaching", "lies were how it kept accounts"); vary cost once (true lie, or stepping is error)
- **Hold-closer ban** — max **4 book-wide** (`nfc_hold_closer`): ridge keys-handoff (ch-01), Orte death (ch-04), 98% certification, one epilogue beat; end other sections on object/vox/unfinished action
- **Inventory checklist** — **one full decon/armoury scene** (ch-17); summary elsewhere in ch-16/18/99 (`nfc_inventory_check`)
- **Did-not-read macro** — `did not read` / `stepped on it` / `crushed without reading` — max **3 book-wide** (ch-02 establishment, ch-13 payoff, one mid); vary physical action elsewhere
- **Looking-was-how macro** — `Looking was angle lost` / `[gerund] was how [X]` / `Names were for` — max **3 book-wide** (`nfc_looking_was`); delete gloss, let action stand
- Fragment caption tags (`Efficient.`, `Red.`, `Geometry. Finality.`) — max one per chapter
- **Bold one-word closers** — max one per chapter
- "empty place/room/quarter where fear should live" after ch-02 and Red Field
- "Hold was currency" / "Minutes were the only currency" / "Four minutes was the bank" — **one act max**
- "Reading was how they got you" — show boot-stomp alone after first instance
- "she realised" / "he understood" discovery crutches
- Characters explaining the Warp to each other
- Sorcerer rematch (Book I)
- Chaos sympathy
- Duplicate decon/armoury/Apothecarium beats across ch-17/18/99
- **Thesis caption closers** — `Procedure continued.` / `Departure was not victory.` / `Doctrine was the cage` / `Someone always gets in the box` — cut; max **1 theme statement per act** (`nfc_theme_caption` ≤2)

## Protected spans

- Metaurus sus-an litany (Prologue, ch-05 Red Field memory)
- Titus child-interior (Book IV only — not Book I)
- Bolter physics / frozen bolt detail (modulate under pressure — break syntax at brother-deaths)
- Wolf-get-keys interlock (Ch 1, Ch 16)
- `I confirm` / `Keys accepted` ritual refrain (intentional, spaced)

## Act III requirements

- Each chapter ≥2.5k words
- ch-16: Voren load protocol + auspex wrong-first read + ground-truth cost
- ch-17: convoy staging, armoury/decon spoken exchange, ridge weather on departure
- ch-18: Novahistorium channel walk; single Apothecarium beat; no duplicate decon
- ch-99: Everson handoff, *Sarcophagus Road* seed
