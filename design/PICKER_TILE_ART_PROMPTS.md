# Visual picker — "Rorschach" tile art prompts

> The `/start` page can offer a **gut-pick grid**: 9 evocative, neutral-but-atmospheric tiles. A
> visitor picks the image they're drawn to (no reading, pure instinct), and it maps deterministically
> to the book to read first. These are **original motif tiles, NOT real book covers** (famous covers
> are copyrighted — never host or print them). Each tile represents a *market*, not a specific book,
> so the pick reads as taste, not a spoiler.

**How to use**
1. Generate each image below (Midjourney/DALL·E/SDXL). **Square, 1:1.** Render **without text**.
2. Save each to `design/picker/<key>.jpg` (the `<key>` is in each heading).
3. Run the tile build step (it copies them to `site/public/assets/picker/` and the picker switches
   from the word-quiz fallback to the visual grid automatically). Until then, `/start` shows the
   3-question word quiz.

**Set rules (so the grid feels like one family):**
- Same treatment across all 9: **cinematic, atmospheric, golden-hour or moody low-key light, a
  single strong focal motif, minimal clutter, no faces** (or only a tiny distant silhouette).
- Shared palette leaning into the house: **deep teal-to-black, warm African-gold, bronze/ochre.**
- Each must read clearly at **thumbnail size** (these are picked on a phone, and printed small on a
  flyer) — one bold idea per tile, high contrast, no fine detail that vanishes when shrunk.
- `--ar 1:1 --style raw --v 6` (Midjourney). Optionally lock a shared `--sref` once you like one.

---

### 1. `mine` → Grounded sci-fi thriller *(resonance; also relic)*
> A narrow shaft of warm golden light falling deep into a vast dark vitrified rock chamber, veins of
> glowing gold threading the stone, fine dust motes, a sense of something alive humming in the rock.
> Awe, descent, science-real wonder. Teal-black + gold. Square, no text, cinematic, high contrast.

### 2. `cipher` → Symbol / code thriller *(revelation; also book1-africa)*
> A wall of ancient carved symbols and glyphs lit by a single raking light, one band of the symbols
> glowing hot gold as if freshly decoded, deep shadow around it. Mystery, hidden meaning, the thrill
> of cracking a code. Teal-black + ember-gold. Square, no text, cinematic.

### 3. `stones` → Ancient mysteries *(book1-africa, book2-india, book3-india-deccan, book5-egypt)*
> A ring of towering monolithic standing stones on a high escarpment at golden hour, the central two
> framing a blazing sunburst on the horizon, long shadows, a tiny lone silhouette for scale. Lost
> civilisations, deep time, the impossible-old. Teal sky + molten gold. Square, no text, epic.

### 4. `anomaly` → Strange-but-true / anomaly *(project-stargate, crop-circles)*
> A single perfect geometric pattern pressed into a moonlit field at night, faint mist, one cold
> shaft of light from above, an eerie stillness, no people. Unexplained, documentary-uncanny, "what
> if it's real". Desaturated teal + a thread of gold. Square, no text, cinematic.

### 5. `veld` → African saga *(jakobus-silver-thread, jakobus-the-recitation; also relic)*
> A lone acacia and a single distant figure on the open African veld at sunset, dust in the gold
> light, a worn Land Cruiser track, vast sky. Wide, weathered, masculine, Wilbur-Smith epic. Bronze
> + gold + dust. Square, no text, cinematic, warm.

### 6. `desert` → True survival / nonfiction *(sheltering-desert)*
> A harsh, beautiful eroded desert canyon under a hard blue sky, raked low light carving the ridges,
> utterly empty, no people — survival country that does not care. Real, stark, true-story gravity.
> Ochre rock + cold sky. Square, no text, photographic, austere.

### 7. `road` → Travel & living peoples *(unheard-mongolia, australia-outback)*
> An open road or track running to a far horizon across vast country (steppe / outback), huge sky,
> warm low sun, a felt tent or a lone marker tiny in the distance. Journey, the road, dignity of
> faraway places. Gold horizon + earth. Square, no text, cinematic, expansive.

### 8. `window` → Quiet literary *(the-loneliest, unheard-japan)*
> A single rain-streaked window at dusk, soft warm interior light behind it, a quiet empty chair just
> visible, muted and still, melancholy and human, no faces. Intimate, literary, slow-burn. Muted
> teal + warm amber glow. Square, no text, cinematic, tender.

### 9. `myth` → Myth & classics / the inward journey *(wrath-of-achilles; also walls-of-uruk, the-song-of-the-self)*
> A weathered bronze Greek helm (or a single classical column) lit by a low gold sun against a dark
> sky, sparks or dust in the air, heroic and ancient and a little sorrowful. Myth retold, the old
> stories. Bronze + gold + shadow. Square, no text, cinematic, mythic.

---

### Tile → book mapping (deterministic; wired in site/build.py)
Picking a tile recommends its **primary** book first, with the cluster's others as runners-up:

| Tile | Read first | Runners-up |
|---|---|---|
| `mine` | RESONANCE | RELIC, REVELATION |
| `cipher` | REVELATION | The Calendar of Stone, RELIC |
| `stones` | The Calendar of Stone | The Engineer of the Gods, The Indian One |
| `anomaly` | The Men Who Opened the Door | The Field of Doors |
| `veld` | The Silver Thread | The Recitation, RELIC |
| `desert` | The Sheltering Desert | The Silver Thread |
| `road` | The Felt and the Sky | The Songlines of Stone |
| `window` | The Loneliest People in the World | The Way That Was Invented |
| `myth` | The Wrath of Achilles | The Walls of Uruk · The Song of the Self |

> Every market is covered; every published book is reachable as a first-pick or a runner-up.

### Firewall / safety
- Original art only — **no real book covers, no real brand imagery, no recognisable real people.**
- A tiny distant silhouette for scale is fine; no portraits.
- If a render crowds the frame with detail that won't survive a thumbnail, pick a cleaner frame —
  these are chosen on phones and printed small.
