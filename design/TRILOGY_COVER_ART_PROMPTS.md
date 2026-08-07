# The African Gold Trilogy — cover-art prompts (generate, then typeset)

**House tier:** the *novels* (RESONANCE / REVELATION / RELIC) match **`book1-africa` (The Calendar
of Stone)** — a rich, cinematic, illustrated scene with depth, atmosphere, a focal subject, and a
warm gold key-light. NOT the flat companion look.

**How to use**
1. Generate each image below (Midjourney v6 / DALL·E 3 / SDXL — whatever you use). Aspect **2:3**
   (portrait book cover). Render **without text** — type is added in step 3.
2. Save the chosen frame to that book's plate slot (preferred) or art slot:
   - `books/resonance/design/cover-plate.png`  (or `art.png`)
   - `books/revelation/design/cover-plate.png` (or `art.png`)
   - `books/relic/design/cover-plate.png`      (or `art.png`)
3. Run `python3 design/typeset_trilogy_covers.py` — it drops the Atkinson Hyperlegible
   house lockup (eyebrow · numeral · title · tagline · author · Arjuna Badger Press)
   onto each, exports the cover + catalog thumbnail.

**The "set" rules baked into all three prompts** (so they read as one trilogy):
- Same render style: *cinematic matte-painting / photoreal concept art, golden-hour, volumetric
  light, fine grain, dramatic depth*.
- Same palette: **deep teal-to-black sky, warm African-gold key light, bronze/ochre earth.**
- Same composition grammar: a **strong central vertical axis**, a **single small human figure**
  for scale, a **blazing gold light source on the horizon line**, **darker sky at the very top**
  and **darker ground at the very bottom** (negative space reserved for gold type).
- Escalation: **dawn → fire → full molten gold** across books 1 → 2 → 3.

> Tip for Midjourney: end each with `--ar 2:3 --style raw --v 6` and (optionally) a shared
> `--sref` once you pick a book-one render you like, to lock the set's look across all three.

---

## BOOK ONE — RESONANCE  *(South Africa · the deep gold mine · the first tuning)*
**Tagline:** *Some minds were not born. They were tuned.*

> A cinematic matte-painting cover, portrait orientation. Deep underground in an ancient South
> African gold mine: a vast vitrified rock chamber, walls of dark stone shot through with veins of
> glowing gold that hum with resonance. At the centre, a narrow shaft of warm golden light falls
> from far above onto a single small lone figure standing in silhouette, dwarfed by the chamber.
> Concentric rings of light ripple outward from where the figure stands, as if the stone itself is
> ringing like a struck bell. Fine dust motes in the light. Dark, almost black at the very top of
> the frame; warm ochre-gold glow in the centre; deep shadowed rock at the bottom. Mood: awe,
> descent, first contact with something alive in the rock. Cinematic, volumetric light, fine film
> grain, dramatic scale. Teal-black and African-gold palette. No text. --ar 2:3 --style raw --v 6

## BOOK TWO — REVELATION  *(Egypt / the flooded Nile · the edited sacred text · the charge)*
**Tagline:** *Every sacred text was edited. She found the edits.*

> A cinematic matte-painting cover, portrait orientation. A drowned ancient Egyptian temple
> half-submerged in the flooded Nile at dusk: colossal carved stone columns and a great wall of
> hieroglyphs rising from black still water, lit by a fierce low sun the colour of forge-fire. A
> single small lone figure in silhouette stands waist-deep in the water on the central axis,
> looking up at the towering inscribed wall, where one band of the carved symbols glows hot
> red-gold as if freshly cut — the edit, revealed. Reflections of fire on the water. Dark
> storm-teal sky at the very top; blazing red-gold light across the horizon and the glyph-band;
> dark water at the bottom. Mood: forbidden knowledge, a hot dangerous discovery. Cinematic,
> volumetric light, embers in the air, fine film grain. Teal-black, ember-red and gold palette.
> No text. --ar 2:3 --style raw --v 6

## BOOK THREE — RELIC  *(the resonance key found · Adam's Calendar · full molten gold)*
**Tagline:** *The gold was never the treasure. It was the key.*

> A cinematic matte-painting cover, portrait orientation. The great stone circle of Adam's
> Calendar on a high African escarpment at the golden hour: towering monolithic standing stones
> arranged in a ring, the central two stones framing a vast blazing golden sunburst on the horizon.
> At the centre, held aloft in a single small lone figure's hand, a small intricate golden
> artifact — a resonance key — catches the sun and blazes white-gold, sending rays and concentric
> rings of light radiating through the whole stone circle. The stones glow molten amber. Faint
> ancient carvings and a labyrinth pattern visible on the ground. Dark deep-blue sky at the very
> top; overwhelming gold light flooding the centre and horizon; warm shadowed veld grass at the
> bottom. Mood: revelation, triumph, the key that unlocks everything — the warmest, most golden of
> the three. Cinematic, volumetric god-rays, lens flare, fine film grain, epic scale. Teal-black
> and full molten-gold palette. No text. --ar 2:3 --style raw --v 6

---

### Notes / firewall
- These are **place + scene**, no real persons depicted — safe.
- Keep the **figure small and silhouetted** in all three (scale, not a character portrait) — it
  keeps the set coherent and avoids a face mismatch.
- If a render crowds the top or bottom edges with detail, regenerate or pick a frame with cleaner
  dark bands there — the gold type needs those zones. The typeset script darkens them slightly
  anyway, but cleaner art = better type legibility.
