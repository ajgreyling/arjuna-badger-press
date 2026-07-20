# PLAN — *The Antifragile Trader*

The sibling of *The Antifragile Reader*, with instruments. File order = read order. Each
`book/NN-*.md` follows the five-beat template in [STYLE_GUIDE.md](STYLE_GUIDE.md): **The fire ·
Where the smoke goes · Plainly · The line · Run it.** Every essay pairs with a live exhibit on the
lucid.rodeo Incerto wing (https://lucid.rodeo/incerto/). Status: ✅ drafted · ◻ planned.

| # | File | Essay | Anchored in | Paired instrument | Status |
|---|------|-------|-------------|-------------------|--------|
| — | `_front.md` | About this book + the covenant | all | — | ✅ |
| 00 | `00-proem.md` | **The Number You Can Run** — the guest returns with instruments | all | the wing itself | ✅ |
| 01 | `01-the-turkey.md` | **The Turkey's Ledger** — induction priced daily | *The Black Swan* | `/incerto/turkey/` | ✅ |
| 02 | `02-the-lying-average.md` | **The Average That Lies** | *The Black Swan* + *SCOFT* | `/incerto/mean/` | ◻ |
| 03 | `03-the-lens.md` | **The Lens** — fragility as curvature | *Antifragile* | `/incerto/convexity/` | ◻ |
| 04 | `04-the-two-averages.md` | **The Crowd's Average and Yours** | *Skin in the Game* | `/incerto/ergodicity/` | ✅ |
| 05 | `05-both-ends-priced.md` | **Both Ends, Priced** — the barbell and the cost of patience | *Antifragile* | `/incerto/barbell/` | ◻ |
| 06 | `06-reading-a-tail.md` | **Reading a Tail** — measurement is not a signal | *SCOFT* | `/incerto/tails/` | ◻ |
| 07 | `07-the-barrier.md` | **The Barrier** — ruin ends the game, and the survivors lie | *Skin in the Game* | `/incerto/barrier/` | ◻ |
| 08 | `08-old-things-win.md` | **Old Things Win** — Lindy for instruments and ideas | *Antifragile* | `/incerto/lindy/` | ◻ |
| 09 | `09-the-stubborn-few.md` | **The Stubborn Few** — the minority rule and market microcultures | *Skin in the Game* | `/incerto/minority/` | ◻ |
| 10 | `10-how-to-watch-a-fight.md` | **How to Watch a Fight** — the fence as a reading discipline | all | `/incerto/war-tails/` + `/incerto/var-wars/` | ◻ |
| 11 | `11-coda.md` | **Structure, Never Advice** — what a trader may honestly carry home | all | the wing | ◻ |

## Notes for the drafting threads

- **Two hard rules, equal in rank** (STYLE_GUIDE §"The deltas"). The living-author rule: paraphrase
  + attribute by book; his prose stays his — and in this book **no quotation marks around his words
  at all**, anywhere. *The line* beat is always the marked `plainly:` restatement + "go read it in
  <book>," never a quote. The structure rule: **structure, never advice** — no sentence recommends a
  position, an allocation, a product, or an action with the reader's money. Harm gate on every
  sentence: *can the reader lose money by doing what this says?* If yes, refuse and rewrite as
  payoff shape, not action.
- **State his case at full strength before any pushback.** The guest is generous first.
- **`Where the smoke goes`** carries the honest critique — marked contested, never flattened into
  hagiography or takedown.
- **`Plainly`** lands each idea on the trading or building reader's real ground — a position, a
  drawdown, a payoff — once, cleanly, as description. The moment it reads as what-to-do, it has
  failed the harm gate.
- **`Run it`** is one short paragraph: the exhibit's full URL (https://lucid.rodeo/incerto/<slug>/),
  the one number the reader can check with their own hands, and one honest sentence on what the
  instrument cannot say — a measured tail is the past, not a forecast.
- **Numbers law:** read the paired wing page *before* drafting; numbers in prose come only from that
  page's exact figures or from classroom-derivable arithmetic, sourced in the sentence that carries
  them. Never from memory.
- **Braid law:** an essay ships only when its exhibit is live and verified. **Flag — all eleven
  exhibits (three rings) are committed and verified on lucid-rodeo branch `feat/incerto-first-ring`,
  but NONE are live yet: the branch has not merged to master, and merging deploys.** Every essay's
  Run-it link therefore points at a page that exists in the repo and nowhere on the web. Before the
  book leaves draft: merge the wing branch, curl every /incerto/ URL, and only then promote.
- Drafted this pass (2026-07-20): `_front.md`, `00-proem.md`, `01-the-turkey.md`,
  `04-the-two-averages.md`. Remaining essays follow the same cadence: wing page read → draft →
  cold-read → de-LLM polish → verify exhibit live → ship.
