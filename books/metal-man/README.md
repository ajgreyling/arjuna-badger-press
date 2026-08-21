# *The Metal Man*

**A gospel life of Uri Geller.** Original novel, five acts, ~115k target.

> They asked him to bend a spoon because they were afraid to ask what else he could bend.

This book does not ask whether Uri Geller is a magician. It asks: **what if he really could — and the
spoon was the smallest, safest demonstration of what had happened to him?**

The metal does not bend because he applies force. It bends because, for a few seconds, in his
presence, matter stops being certain about its own shape. He is not a psychic. He is a flaw in the
agreement that keeps the physical world solid.

## The two layers

The **famous story** is the surface and is kept documentary-accurate: the Tel Aviv garden and the
flash of light, the compass, the stopped watches, the sealed drawings, the paratrooper wounded in
1967, Puharich, the sealed rooms at Menlo Park, the paper in *Nature*, Carson, Dimbleby, Randi, the
CIA files, fifty years of ridicule and survival.

Underneath it: **nobody was ever interested in spoons.** What the agencies wanted to know was whether
the effect scaled — missile guidance, enrichment cascades, aircraft instrumentation, electronic
locks, nuclear command clocks, the lattice inside a chip. A man who can soften a teaspoon can distort
a firing pin. *That* is why he had to become ridiculous, and by 1973 he was in on it. Ridicule is
cheaper than assassination and works better.

## The central idea

**Metal remembers the shape it was persuaded to hold. Uri can make it remember something else.**

A knife remembers the furnace. A wedding ring remembers every hand that wore it. A crashed aircraft
remembers the instant its metal decided to fail. A fragment of meteorite remembers falling through
the dark before the Earth existed.

He begins believing he bends metal. He ends knowing metal has been talking to him since he was five —
and that something in the oldest iron on Earth is trying to wake.

The physics floor is real and load-bearing: work hardening, residual stress, **annealing** (the
industrial term for making metal forget), Barkhausen noise, **nitinol** — memory metal, which a Naval
Surface Weapons Center scientist really did test Geller with in 1973 — and **Widmanstätten patterns**,
the crystal figures inside iron meteorites that take millions of years to form and cannot be forged.
The novel turns that screw exactly one turn. See
[`canon/THE_MEMORY_OF_METAL.md`](canon/THE_MEMORY_OF_METAL.md).

> **The engine:** two readings held alive to the last page — *a gift* and *an infestation* — and an
> ending that resolves the plot while refusing to arbitrate the question. House all-sides law,
> relocated. [`canon/THE_GOSPEL_PREMISE.md`](canon/THE_GOSPEL_PREMISE.md)

## Shelf

Intended for a new **Impossible Lives** shelf — biographical novels that take the impossible claim as
gospel and write the life from inside it — beside the Ted Owens book. Ted Owens is the storm-caller:
cosmic, sprawling, half prophet and half trickster. **Uri Geller is intimate.** A spoon bends across a
dinner table. A stopped watch starts. A child in front of a television draws the hidden picture. The
impossible enters through ordinary household objects.

## Status

Scaffolded and drafted 2026-08-21. Full canon in [`canon/`](canon/) — 16 files. Complete five-act
draft in [`manuscript/`](manuscript/): 40 chapters plus front matter and four metal-register
interstitials, merged to [`build/BOOK.md`](build/BOOK.md) by [`build.py`](build.py) in the order
given by [`manuscript/ORDER.txt`](manuscript/ORDER.txt).

**~52,500 words.** This is a complete arc at roughly half the 115k target in
[`project.json`](project.json) — every beat in [`canon/PLOT.md`](canon/PLOT.md) is written and every
PP-ID in [`canon/PLANTS_AND_PAYOFFS.md`](canon/PLANTS_AND_PAYOFFS.md) is planted and paid, but the
chapters run lean (~1,300 words against a house norm of 2,800–3,500). The expansion pass is
scene-work, not structure.

### Audits run

- **Number tics** (the *Surgeon* failure mode): "four" was at 1 per 351 words on first draft. Load-
  bearing figures kept — the four grams of iron, the watch's stopped hour, twelve minutes to four,
  the broadcast hour — reflexes varied. Now 1 per ~490, matching the *Surgeon*'s post-fix rate.
  Checked that the replacements did not become the new tic.
- **`tools/prose_tics.py`**: 0 drift sentences, 0 drift 7-grams. Deliberate refrains are listed in
  [`canon/MOTIFS.txt`](canon/MOTIFS.txt) and pass as motifs.
- **Em-dashes**: first draft ran 12.0/1k with spaced dashes throughout. House style is unspaced
  (verdigris, Lacework); spaced dashes closed up, conjunction and appositive dashes commafied. Now
  9.9/1k against 7.5–8.1 for the published house books. **Still above house norm** — the remaining
  pass belongs to `tools/de_llm_pass.py`, not to regex.

### Not done

- No cover. `design/` is empty — Pillow and any image API are absent in this container
  (see `memory/arjuna-badger-press/render-cover-geometry` and `render-gate-remote-container`).
- No EPUB/PDF. The render gate needs pandoc and a GNU `mktemp` shim in-container, and tectonic is
  absent, so PDF would not build here in any case.
- No fact-check pass. [`canon/THE_REAL_RECORD.md`](canon/THE_REAL_RECORD.md) is compiled from
  general knowledge and is **explicitly unverified**.

**Nothing is live.** Not in `PUBLISHED`, no `SERIES` entry for the Impossible Lives shelf, no
`CURATED` tuple.

**Before any publish decision** — the subject is alive, is eighty, and has litigated over his
portrayal for fifty years. The gate is in [`canon/LIVING_PERSONS.md`](canon/LIVING_PERSONS.md) and it
is not optional:

- legal read (defamation + privacy; UK and Israel exposure)
- fact-check pass against primary sources
- Author's Note in front matter — drafted, at [`manuscript/AUTHORS_NOTE.md`](manuscript/AUTHORS_NOTE.md)
- a written approach to the subject, or a recorded decision not to
