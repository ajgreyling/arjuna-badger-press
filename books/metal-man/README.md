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

Scaffolded and drafted 2026-08-21; expansion pass same day. Full canon in [`canon/`](canon/) — 16
files plus [`canon/MOTIFS.txt`](canon/MOTIFS.txt). Complete five-act draft in
[`manuscript/`](manuscript/): 40 chapters, front matter, and four metal-register interstitials,
merged to [`build/BOOK.md`](build/BOOK.md) by [`build.py`](build.py) in the order given by
[`manuscript/ORDER.txt`](manuscript/ORDER.txt).

**~72,000 words.** Up from 52,500 after an expansion pass of thirty-nine new scenes. Still under the
115k in [`project.json`](project.json), and chapters now average ~1,800 against a house norm of
2,800–3,500 — but the structure is complete, every beat in [`canon/PLOT.md`](canon/PLOT.md) is
written, and every PP-ID in [`canon/PLANTS_AND_PAYOFFS.md`](canon/PLANTS_AND_PAYOFFS.md) is planted
and paid.

### Audits (re-run after the expansion — the new prose reintroduced both tics)

- **Number tics**: "four" went back to 1 per 438 words on the new material. Load-bearing figures
  protected by a context check (the four grams of iron, the watch's stopped hour, twelve minutes to
  four, the broadcast hour, four thousand children, eleven tonnes); reflexes varied. Now 1 per ~530,
  with no single number dominating — four 1/528, eleven 1/660, three 1/548, nine 1/743.
- **Em-dashes**: the expansion was written with spaced dashes again and pushed density to 10.3/1k.
  Unspaced to house style, conjunction and appositive dashes commafied. Now **8.5/1k** against 7.5
  (verdigris) and 8.1 (Lacework) — effectively at norm.
- **`tools/prose_tics.py`**: caught a real "sat on the end of the bed" tic across three chapters, a
  "did not say anything for a while" tic across three more, and one duplicated line where an
  inserted scene collided with the text it was inserted before. All fixed. Now **0 drift sentences,
  0 drift 7-grams**, 31 protected motifs.

### Not done

- No cover. `design/` is empty — Pillow and any image API are absent in this container.
- No EPUB/PDF. The render gate needs pandoc and a GNU `mktemp` shim, and tectonic is absent.
- No fact-check pass. [`canon/THE_REAL_RECORD.md`](canon/THE_REAL_RECORD.md) is compiled from
  general knowledge and is **explicitly unverified**.

**Nothing is live.** Not in `PUBLISHED`, no `SERIES` entry for the Impossible Lives shelf, no
`CURATED` tuple.

**Before any publish decision** — the subject is alive, is eighty, and has litigated over his
portrayal for fifty years. The gate is in [`canon/LIVING_PERSONS.md`](canon/LIVING_PERSONS.md) and it
is not optional:

- legal read (defamation + privacy; UK and Israel exposure)
- fact-check pass against primary sources
- Author's Note — drafted, at [`manuscript/AUTHORS_NOTE.md`](manuscript/AUTHORS_NOTE.md)
- a written approach to the subject, or a recorded decision not to
