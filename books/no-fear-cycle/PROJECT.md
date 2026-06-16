# Project — The No-Fear Cycle *(working title)*

> **Type:** fan-corpus spin-off · **Lineage:** Games Workshop *Warhammer 40,000* official canon +
> *Space Marine 2* continuity + the *Secret Level* episode *And They Shall Know No Fear* (Blur Studio,
> 2024) + the collective fan corpus (Astartes, Lexicanum, Black Library tone, military-SF brotherhood
> fic) · **Status:** draft-complete · **Series length:** **5 novels, finite.** · **Demo:** PDF + EPUB for Daniel

## Provenance & legal (binding)

- **Not public domain.** *Warhammer 40,000*, Ultramarines, Lieutenant Demetrian Titus, Sergeant Metaurus,
  and all GW iconography are **Games Workshop intellectual property.** This project is **unauthorised
  fan fiction** — homage and craft exercise under the Arjuna Badger Press house tooling, not a licensed
  product. No claim of ownership; no commercial use implied.
- **Sources ingested (canon hierarchy):**
  1. **Primary:** GW official lore (Codexes, *Space Marine 2*, Warhammer Community articles on the
     *Secret Level* episode).
  2. **Secondary:** the *Secret Level* episode itself (plot, Zsah'uj, the Apostate Relic, Metaurus/Titus
     dynamic, astropath-in-a-box, orbital strike ending).
  3. **Tertiary (fan corpus, not override):** Astartes (Syama Pedersen) aesthetic law — silence, HUD
     biology, weight of armour; Lexicanum/1d4chan consensus on organs and warp physics; Gaunt's Ghosts /
     HH military brotherhood register; Archive-style fic tropes (*the last stand*, *the sus-an sleep*,
     *the bladeguard's last lesson*).
- **This prose is original Arjuna Badger Press work.** Annotations and craft doctrine are ours; the
  setting belongs to Games Workshop.

## Premise (post–Secret Level)

Minutes after the orbital strike on Zsah'uj. One relic destroyed; the thin-veil corridor still bleeding
Warp-taint into the galactic west. **Bladeguard Sergeant Metaurus** — Larraman failing, sus-an primed,
atmospheric seal compromised — has one doctrine left to teach **Lieutenant Titus**, the boy who knew no
fear before the Imperium taught him anything else.

The series follows their squad along the **thin-veil corridor** — worlds where lies from Tzeentch's
Library condense into parchment and eggshell, where vox fails and only a chained astropath's Geller-
analogue field holds — until the **Veil Ordinance Grid** can be completed and fired as one strike.
**Five books. Seven coordinates. One ending.**

## Content-model mapping

| Level | Maps to |
|---|---|
| **Project** | The No-Fear Cycle (this) |
| **Series** | The No-Fear Cycle — finite, 5 novels |
| **Novels** | *Ordinance Pending* · *The Sarcophagus Road* · *Fragments of the Library of Lies* · *Bladeguard* · *They Shall Know* |
| **Act / Chapter / Beat** | military-SF three-act per novel; chapters as mission legs; beats as HUD/silence/combat atoms |

## The series McGuffin (finality engine)

**The Veil Ordinance Grid (VOG)** — seven strike coordinates along the thin-veil corridor, each
certifiable only when a **sarcophagus psyker** anchors a local Geller-analogue field long enough to
log true coordinates to orbit. The Secret Level episode destroyed coordinate **VI** (Zsah'uj) but proved
the method. Books I–IV secure coordinates **I–IV** and recover the doctrine; Book V fires **V–VII** as
one mass strike — including the coordinate only a pre-linguistic mind can sign: **the child Titus was
before the sorcerer looked**.

**Reader who finishes the series gets:** the corridor sealed; Metaurus's arc resolved (sus-an or death
with honour); Titus confirmed as the Imperium's weapon *and* its exception; the orbital strike promise
from the episode fulfilled at series scale.

See [`canon/SERIES_SPINE.md`](canon/SERIES_SPINE.md).

## Canon files

| File | Role |
|---|---|
| [`canon/WORLD.md`](canon/WORLD.md) | Galactic west, thin-veil corridor, Zsah'uj, SM2 geography |
| [`canon/MYTHOS.md`](canon/MYTHOS.md) | Warp physics, organs, Imperial truth — binding rules |
| [`canon/CHARACTERS.md`](canon/CHARACTERS.md) | Cast + voice laws |
| [`canon/SERIES_SPINE.md`](canon/SERIES_SPINE.md) | Five-novel relay + McGuffin chain |
| [`canon/FAN_CORPUS.md`](canon/FAN_CORPUS.md) | Faction map — what the fan tribes demand |
| [`canon/ADAPTATION_DOCTRINE.md`](canon/ADAPTATION_DOCTRINE.md) | GW-true + fan-corpus fidelity |
| [`canon/CROSS_SHELF_BRAID.md`](canon/CROSS_SHELF_BRAID.md) | **The Court** + **Wolf gets the keys** (press house DNA) |

## On the page

| File | Role |
|---|---|
| [`manuscript/FOREWORD--syama-pedersen.md`](manuscript/FOREWORD--syama-pedersen.md) | Foreword (homage voice) |
| [`manuscript/PROLOGUE.md`](manuscript/PROLOGUE.md) | Metaurus HUD — the strike lands |
| [`manuscript/ch-01--ordnance-pending.md`](manuscript/ch-01--ordnance-pending.md) | Book I opening — the cultists come |
| [`canon/DEDICATION_BOOK.md`](canon/DEDICATION_BOOK.md) | **For Daniel** — WH40K fan dedication |
| [`design/cover.jpg`](design/cover.jpg) | **Selected cover E — *Ordinance* enhanced** (6×9 portrait full bleed) |
| [`design/IMAGE_COMPENDIUM.md`](design/IMAGE_COMPENDIUM.md) | All four cover explorations + credits |
| [`build/export/Ordinance Pending.pdf`](build/export/Ordinance%20Pending.pdf) | Demo PDF — cover + prose + compendium |
| [`build/export/Ordinance Pending.epub`](build/export/Ordinance%20Pending.epub) | Demo EPUB — read on device |

### Build

```bash
./scripts/merge_book.py              # assemble build/BOOK.md
./scripts/build_demo_pdf.sh          # 6×9 PDF with cover + alternate covers appendix
./scripts/build_demo_epub.sh         # EPUB (cover embedded)
python3 design/make_cover.py         # regenerate Cover E composite
```
