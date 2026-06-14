# JOURNEY — geospatial + natural-world keel (Book I, Africa) (binding)

> **Place magnetism is a protected strength of this book — do not cut it; if anything, lean in.** The
> prose already renders South Africa with real love and real accuracy (the southeaster pouring over
> the mountain, the Karoo dissolving to silver, the eastern Free State sandstone "banded ochre and
> rust," the dead Boland heat). This file exists to *keep it true* as the manuscript grows: every
> mention of the natural world must be **factually, spatially, and seasonally coherent** — right
> biome, right flora, right geology, right month. The runnable guard is
> [`../../tools/natural_world_check.py`](../../tools/natural_world_check.py); the map is
> [`build/maps/journey.png`](build/maps/journey.png). **Tools measure & alarm; they do not write.**

## The route (single source of truth — the tools read this block)

```yaml
season: "winter journey up the spine — the bulk of the road is May to July (frost on the highveld, winter-dry pale grass, low gold light); reconcile the late-summer Paarl opening, see Findings"
legs:
  - id: cape-town
    name: Cape Town (Observatory)
    lat: -33.94
    lon: 18.47
    region: cape-fynbos
    season: winter (July — explicit, ch-3)
    note: her ruined life; the southeaster pours cloud over Table Mountain; cold flat winter light
  - id: paarl
    name: Paarl (the Boland)
    lat: -33.73
    lon: 18.96
    region: cape-fynbos
    season: late summer (Feb–Mar — the dig; see Findings re the gap to July)
    note: dead valley heat; granite domes; vineyards; the lavender + tar-melt palette (see below)
  - id: hex-river
    name: Hex River Pass / De Doorns
    lat: -33.49
    lon: 19.62
    region: cape-fold
    season: winter
    note: the N1 hauls up over the Cape Fold Belt — folded, tilted sandstone; the last of the vines
  - id: karoo
    name: Great Karoo (Beaufort West)
    lat: -32.36
    lon: 22.58
    region: karoo
    season: winter (hot still days, hard cold nights)
    note: flat red earth, grey scrub, koppies floating on heat-shimmer, windpumps, merino, kudu, dolerite
  - id: bloemfontein
    name: Bloemfontein (Free State)
    lat: -29.12
    lon: 26.21
    region: highveld-grassland
    season: winter
    note: the great flat maize lands gone gold; the second lab; the geology lesson (Karoo Supergroup)
  - id: eastern-free-state
    name: Eastern Free State sandstone (Clarens / Golden Gate)
    lat: -28.51
    lon: 28.62
    region: highveld-sandstone
    season: winter
    note: Clarens Formation — cliffs of sandstone banded ochre/rust/arterial-red at dawn (already in ch-4)
  - id: adams-calendar
    name: Adam's Calendar (Mpumalanga escarpment, nr Kaapsehoop)
    lat: -25.58
    lon: 30.85
    region: mpumalanga-grassland
    season: winter (frost at the dawn reading — ch-5/6)
    note: dolerite stone arrangement on the escarpment; long grass silvering; crowned cranes; mist
  - id: witwatersrand
    name: The Witwatersrand deep-gold country (Carletonville)
    lat: -26.36
    lon: 27.40
    region: highveld-grassland
    season: winter
    note: the four-kilometre mine; the cage; mine dumps; the worked-gold link
  - id: great-zimbabwe
    name: Great Zimbabwe
    lat: -20.27
    lon: 30.93
    region: zimbabwe-miombo
    season: winter (dry; go-away birds; granite kopjes)
    note: drystone city; msasa woodland; the inheritance node
  - id: aksum
    name: Aksum (Ethiopian highlands)
    lat: 14.13
    lon: 38.72
    region: ethiopian-highlands
    season: highland dry season
    note: the stelae; eucalyptus; the highland cold (the shemag head-wrap, ch-14)
```

## Per-region natural-world palette (use these; the scanner enforces them)

- **cape-fynbos (Cape Town / Paarl / West Coast).** *Winter-rainfall.* Fynbos, proteas, restios,
  oaks and planted vineyards (the Boland), the southeaster, Table Mountain sandstone + granite. **No
  jacaranda iconography** (a few planted street trees exist, but they are NOT a Cape signature — see
  Findings on the ch-3 line, which is already handled as *flowerless in winter*). Fynbos & proteas
  belong **here**, not on the highveld or up-continent.
- **cape-fold (Hex River / the passes).** Folded, tilted, weathered sandstone of the Cape Fold Belt —
  the rock stands on its *end*, not in flat sheets. The vineyards give out; the Karoo begins on the
  far side.
- **karoo.** *Semi-arid; hot still days, hard cold nights.* Nama/succulent-Karoo scrub, dolerite
  koppies, windpumps, merino sheep, kudu, sweet-thorn; the silver heat-shimmer. **Flat-lying** Karoo
  Supergroup sediments capped by **dolerite sills** (the "striated sheets" of the Bloem→CT geology
  lesson — see below). Quiver trees are Northern-Cape/Namaqualand, not the N1 Karoo — don't import.
- **highveld-grassland (Free State / Gauteng / Witwatersrand).** *Summer-rainfall; winter frost & dry
  gold grass; spectacular summer thunderstorms.* Maize lands, Themeda grassland, crowned cranes,
  planted bluegums, mine dumps on the Rand. **Cosmos** (pink/white) is an **autumn** roadside bloom
  (Mar–Apr) — do not put it in a winter or midsummer scene. **Jacarandas** (Johannesburg/Pretoria,
  iconic) **bloom Oct–Nov (spring)** — never in the winter journey; flowerless or bare if shown at all.
- **highveld-sandstone (eastern Free State).** Clarens Formation sandstone — ochre/rust/red banded
  cliffs, rounded overhangs (already rendered beautifully in ch-4; this is the gold standard).
- **mpumalanga-grassland / escarpment.** Long highland grass silvering in wind, the blue escarpment
  line, mist belt, crowned cranes; frost at altitude in winter. (Lowveld fever-trees/marula are *below*
  the escarpment — don't place them up on the calendar ridge.)
- **zimbabwe-miombo.** Msasa & miombo woodland (msasa flushes **red-gold in spring, ~Aug–Sep**;
  green/dry otherwise), granite kopjes stacked like a giant's blocks, go-away (grey lourie) birds,
  Great Zimbabwe drystone. **Msasa belongs only here / up-continent**, never in SA proper.
- **ethiopian-highlands.** High dry plateau, eucalyptus, cool highland air, the stelae fields. A
  different world from the lowland desert that comes later (Book V).

## The Paarl palette (LOCKED — author-sourced; the dead-of-summer Boland)

Paarl sits in a **valley**, and in **February–March** the heat *pools* there and does not move.
Binding sensory facts for any Paarl scene:
- **No air moves in the middle of the day.** The heat is a physical weight; you wear it. Midday is
  near-impossible; life moves to the cool — people **walk at night, between the houses**, because the
  day is unwalkable.
- **The tar melts.** Real, not legend — soft summer **bitumen takes a boot-print** on the road.
- **Lavender.** There is a great deal of it, and on a hot summer **night** the scent **envelops** you,
  surreal and total — **45 °C still at 20:00**, and the whole dark smelling of lavender. *(This is a
  night palette; the existing ch-2 dig is daytime dead-heat — both true, different hours. Lavender is
  the signature; if a Paarl night beat is ever written, the lavender is the thing the reader keeps.)*
- Granite domes (Paarl Mountain) shimmering by mid-morning; fiscal shrikes; figs; vineyards.

## The Bloemfontein ↔ Cape Town geology (LOCKED — the "striated sheets" lesson)

The N1 between Bloemfontein and Cape Town is a **cross-section through deep time**, and a well-
informed passenger really would explain it (the book can stage this with Jakobus, or a remembered
lift):
- Across the **Karoo**, the near-horizontal **striated sheets** are the **Karoo Supergroup** —
  hundreds of metres of mudstone and sandstone laid down layer on patient layer in a vast inland basin
  over ~100 million years (Carboniferous→Jurassic), as Gondwana drifted off the South Pole: glacial
  till at the bottom, then black shales, then river sandstones, the whole thing **capped and intruded
  by dolerite sills** (molten rock that squeezed between the layers as Gondwana broke up ~180 Ma and
  now armours the flat-topped koppies). *That* is the layering — flat, banded, ruled across the
  landscape — and it is exactly right; it is the same "strata stacked like the pages of a book nobody
  was allowed to read" the prose already reaches for (ch-4).
- Near the **Hex River**, the rock changes character entirely: the **Cape Fold Belt** — older
  sandstones (Table Mountain Group) **crumpled and stood on end** when Gondwana collided ~250 Ma. Flat
  sheets in the Karoo; folded, tilted ramparts at the Cape. A reader feels the difference through the
  windscreen, and a good explainer names it. **This is gold; keep and grow it.**

## Season timeline (the winter journey)

The road is a **winter** journey (May–July): frost at the calendar dawn (ch-5/6), winter-dry pale
grass, low gold light, hard cold nights — all coherent and consistent up the spine and into Zimbabwe.
The **opening** is the wrinkle: the **Paarl dig reads "late summer"** (Feb–Mar) while **Cape Town
reads "July / winter"** days later (ch-2/3). Reconcile with an explicit gap (the dig was an earlier
job; the ruin dragged through autumn into winter before Jakobus came) or settle one season. See
Findings.

## FINDINGS (open — author's call; the scanner re-flags these)

| # | Sev | Finding | Note / fix |
|---|---|---|---|
| 1 | **H** | **Season jump at the open:** Paarl dig = "late-summer" (ch-2) vs Cape Town = "July/winter" (ch-2/3), apparently days apart. | Insert an explicit time-gap (the dig was months back; the limbo ran into winter) or align the seasons. |
| 2 | **M** | **Canon vs prose start point:** `WORLD.md` relay map opens at **Durban/Johannesburg**; the prose opens in **Cape Town / Paarl** and drives the **N1**. | Update WORLD.md's relay map to the real Cape start, or reconcile. |
| 3 | **M** | **ch-10 route, not flora:** the fynbos/proteas are *correct* — ch-10 explicitly puts them back in the **Cape ranges** ("the real mountains came up out of the south... a smell of water and fynbos"). The natural world is right; the **route** is the question — they're in the Cape *after* the Witwatersrand mine (ch-9) and before "Ma's waiting." | Confirm the post-mine geography and where Ma's farm sits; the leg block above is a first pass from WORLD.md + the early chapters and needs reconciling with the mid-book route (the relay "up the spine" vs. the actual Cape-ranges return). |
| 4 | n | **ch-3 jacaranda (Observatory):** botanically a planted CT street tree, and the line correctly says *no flowers in winter.* | Author rule "no jacarandas in Cape Town" — keep (it's flowerless/incidental) or cut for purity. Decision noted. |
| 5 | n | **Jacaranda bloom = Oct–Nov (Highveld).** | If a Witwatersrand scene ever shows jacarandas in flower, it must be spring, not the winter journey. |

## How this stays coherent

1. Edit a place/season/flora detail → update the route block / palette here.
2. Run `python3 tools/natural_world_check.py` (region-flora + season-jump scan) and rebuild the map
   with `python3 tools/journey_map.py`.
3. A deliberate exception (a simile, a remembered Cape in the north) is legitimate — note it so the
   scanner's flag is explainable.
