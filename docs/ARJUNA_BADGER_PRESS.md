# Arjuna Badger Press — the venture map

> **Status:** v1 — 2026-06-14. The single canonical picture of the whole venture: the layers, what
> is already built vs. what is still a gap, the two genuinely-new pieces, and the open decisions.
> Everything else (`brand/STRATEGY.md`, `docs/PRODUCTISATION_PLAN.md`, `docs/SAAS_ARCHITECTURE.md`,
> `docs/ARJUNA_BADGER_PRESS.md`, `print-run/`) is a *spoke*; this is the *hub*. When those drift,
> reconcile them here.
>
> **Why this doc exists:** the venture's pieces were built across two branches and three brand names
> and were never drawn on one page. This draws them on one page so a newcomer (or AJ in six months)
> can see the shape in five minutes.

---

## 0. The one-paragraph version

Arjuna Badger Press takes a person's story and gets it *told* — written in their own voice, finished
with craft instruments that **measure and alarm but never generate the prose**, published across every
ebook platform (or free on our own site), and where wanted, narrated. Under it sit a private-IP craft
engine (the moat), a free platform that lets anyone — especially the African voices the big
marketplaces lock out — write and keep or release their own story, a therapeutic-writing practice
(re-authoring your life in your own words, private by default), a print-on-demand exchange for small
runs, and an honest royalty split that flips the traditional 10%-to-the-author model on its head. The
work is fierce; the maker is allowed to be carried.

> **⛔ NON-NEGOTIABLE (AJ, 2026-06-14): factual accuracy + both sides.** The pipeline and tooling
> **must** use the internet and available AI tools to **fact-check everything** and to **present both
> sides of a contested story** (you thought the Burkina Faso leader was simply a hero standing up to
> the French — the real story is contested; the book must *know* that). **Weir / Crichton / Brown-grade
> historical and factual accuracy is core to Arjuna Badger Press.** This is a measure-and-alarm gate —
> it verifies and flags; the author still writes. Full spec: [`VERIFICATION_GATE.md`](VERIFICATION_GATE.md).

---

## 1. The name (DECIDED 2026-06-14) + the rebrand surface

**The press is `Arjuna Badger Press`.** It fuses the two roots that were already in the work:

- **Arjuna** — the reluctant warrior of the *Bhagavad Gita* who must act without attachment to the
  fruit; the India thread of the books (the live `companion/gita-song-of-the-self` branch is *The Song
  of the Self*). Duty done for its own sake — *per ardua ad magnum*.
- **Badger** — Stoffel, the honey badger at the heart of the trilogy and the spin-offs: fearless,
  nearly unkillable, clever enough to escape any box the industry builds — **and tender enough to let
  itself be carried** (see `docs/ARJUNA_BADGER_PRESS.md` §"Why").

### Names this supersedes / re-slots

| Old name | Was used for | New status under Arjuna Badger Press |
|---|---|---|
| **Arjuna Badger Press** | the free writing-craft body of knowledge + platform manifesto | **folds in** — becomes the free-knowledge *imprint/arm* of Arjuna Badger Press (keep the docs; rename the masthead) |
| **Arjuna Badger Press** | the built brand kit, logo art, the live `site/`, OG cards | **OPEN DECISION** — retire, or repurpose as the *technology/engine* brand (the "instruments") under the press. The piezoelectric "pressure → signal" metaphor is strong for the *tooling*; the press itself is Arjuna Badger. Recommend: **Arjuna Badger Press = the engine/tech name; Arjuna Badger Press = the publishing house.** Confirm. |
| **House of Greyling** | the ISBN imprint in `print-run/POD_ECONOMICS.md` | the legal **imprint of record** on the copyright page / ISBN; Arjuna Badger Press is the trading/brand name. (An imprint and a trading name can coexist.) |

### Rebrand surface (what physically changes when the name lands)

Everything visible was built as **Arjuna Badger Press**. If the press name is now public-facing, these need
edits — tracked here so the rename doesn't drift:

- [ ] `site/index.html` — title, OG title/description, hero, footer, masthead
- [ ] `brand/BRAND.md` + `brand/STRATEGY.md` — masthead, boilerplate, taglines (decide PP-as-tech vs full rename)
- [ ] `brand/assets/` — logo lockups, favicons, `social-og-1200x630.png` (new art if the press gets its own mark)
- [ ] `docs/NLSA_ISBN_APPLICATION.md` — imprint name (House of Greyling vs Arjuna Badger Press)
- [ ] `docs/ARJUNA_BADGER_PRESS.md` + `ARJUNA_BADGER_PLATFORM.md` + `_WORKED_EXAMPLE.md` — masthead
- [ ] `piezo-pangolin/` workspace dir name + its README

> **Brand-voice note (binding):** `brand/BRAND.md` §5 explicitly lists **"disrupt"** among the words we
> *avoid* as a boast. The strategy below names the target plainly ("flip the 10% split"), but
> public-facing copy stays in the calm, no-hype house voice. Internal docs may say "disrupt"; the
> shop window may not.

---

## 2. The layers (the whole stack on one page)

```
                       ARJUNA BADGER PRESS  (the house — "your story, told")
   ┌───────────────────────────────────────────────────────────────────────────────┐
   │  L6  THE FUNNEL / IP PROOF                                                       │
   │      the CTO explainer (architecture + diagrams) · the guardrail-register thesis │
   │      → "get me on-board as consultant"                                           │
   ├───────────────────────────────────────────────────────────────────────────────┤
   │  L2 THE PRESS            L3 THE PLATFORM           L4 THE THERAPEUTIC MISSION    │
   │  publish EPUB-everywhere  free, multi-tenant        re-author your life in your   │
   │  or on-site · 90% to the  write/keep-private/release voice · private by default   │
   │  author · narration       · the African-voices bridge (NEW — not yet on record)  │
   │                                                                                  │
   │  L5 THE PRINTING EXCHANGE — small runs, "Uber for presses" (NEW-ish)             │
   ├───────────────────────────────────────────────────────────────────────────────┤
   │  L1  THE ENGINE  (PRIVATE IP — the moat)                                         │
   │      pipeline · StoryGraph continuity gate · NovelBench · de-LLM scanners        │
   │      ⟂ invariant: MEASURES & ALARMS — never generates the author's prose         │
   └───────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. What's already built vs. gap (the inventory, 2026-06-14)

Legend: ✅ built · 🟡 material exists, needs packaging · 🔴 genuinely new / not on record.

| Layer / pillar | Status | Where it lives |
|---|---|---|
| **L1 Engine stays private IP** | ✅ | `engine/`, `storygraph/`, `novelbench/`; the rule is explicit ("tooling is the laboratory, not the free deliverable") |
| **L1 Continuity gate / scanners** | ✅ | `storygraph/constraints.py`, `gate.py`, `prose_tics.py`; `cold-read-tool` (editorial agent, own repo) |
| **L1 Verification gate (accuracy + both sides)** ⛔ non-negotiable | 🟡 partial → being built | extractor exists (`prompts/factcheck-extract.md`) + a proven manual plausibility pass; **live-internet verify + both-sides + standing gate are new** — spec: [`VERIFICATION_GATE.md`](VERIFICATION_GATE.md) |
| **L2 EPUB-everywhere pipeline** | ✅ | `build.sh` → EPUB/PDF/audio; `docs/WIDE_DISTRIBUTION.md` |
| **L2 ISBN / imprint** | ✅ specced | `docs/NLSA_ISBN_APPLICATION.md`; imprint = House of Greyling |
| **L2 90%-to-author royalty model** | 🟡 | math worked in `print-run/POD_ECONOMICS.md` (70–90% indie); not yet a formal business-model doc |
| **L3 Free platform (multi-tenant)** | ✅ plumbing | `saas/` (Postgres queue + blob + worker, tested offline); `deploy/`; `workspaces/` |
| **L3 Three front doors (Newcomer/Middle/Rothfuss)** | ✅ P0–P2 done | `docs/PRODUCTISATION_PLAN.md` §5; `engine/wizard.py`, `import_canon.py`, `ingest_manuscript.py`, `reverse_canon.py` |
| **L3 African-voices bridge (ACX wall)** | ✅ specced | `brand/STRATEGY.md` §1 positioning #2; `brand/MARKET_ANALYSIS.md` §4/§4a |
| **L3 Private-or-release projects** | ✅ | `piezo-pangolin/` workspace; clonable projects (Sherlock + modern-Sherlock proof) |
| **L4 Therapeutic writing mission** | 🔴 | **only in AJ's head** — captured in §4 below for the first time |
| **L5 POD economics (use KDP/Ingram)** | ✅ | `print-run/POD_ECONOMICS.md`, `BOXSET_PLAN.md`, `QUOTE_REQUEST.md` |
| **L5 Printing *exchange* (match runs↔presses)** | 🔴 | the marketplace idea is new; today's `print-run/` is *using* POD, not *matching* presses — see §5 |
| **L6 Public site** | ✅ built & verified | `site/index.html` (single-file, brand-tokened, waitlist, SIGNAL/RESONANCE/AMPLIFY tiers) |
| **L6 CTO explainer + diagrams** | 🟡 | `README.md` + `ARCHITECTURE.md` + `docs/` are full of Mermaid diagrams; not yet packaged *as* the consulting funnel |
| **L6 The rigor / IP proof** | ✅ | `guardrail-register-thesis` repo — empirical thesis: *LLMs are content-addressed, not frame-addressed*; register-lift; StrongREJECT rubric |

**Bottom line:** roughly **80% of this venture already exists** in code or spec. The build-ahead is
small and concentrated: the two new pillars below (L4, L5), packaging the CTO funnel (L6), and the
housekeeping in §6.

---

## 4. NEW — the therapeutic-writing mission (L4)

*This is the piece that was never written down. It is recorded here so it stops living only in AJ's
head, and so the platform's most human purpose is on record next to its business model.*

**The discovery (in AJ's words, paraphrased):** writing — *narration* and creative writing where the
author is in control — has a real therapeutic benefit. Putting the worst of yourself and the best of
your memories into the story of your life, **in your own voice**, is healing. People should be able to
do this for free, and **keep it private or release it** entirely as they choose.

**This is not a fringe instinct — it has names and evidence.** Documenting them makes the mission
credible to a clinician *and* to a CTO:

- **Expressive writing** (James Pennebaker) — decades of controlled studies show measurable
  psychological and even physical-health benefits from writing about difficult experience.
- **Narrative therapy / "re-authoring"** (Michael White & David Epston) — a person is not their
  problem; healing is reclaiming authorship of one's own story. *"Putting the worst of me and the best
  of my memories into the story of my life, in my control"* **is** re-authoring, almost verbatim.
- **Narrative identity** (Dan McAdams) — selfhood is the internalized, evolving story we tell about our
  own life; revising that story revises the self.
- **Voice / self-distancing** — telling it in *your own voice* (and, for the platform, optionally
  hearing it narrated back) adds the therapeutic distance that turns rumination into perspective.

**Design commitments this mission imposes on the platform (binding):**

- **Private by default.** A life-story project is the author's alone unless they explicitly publish.
- **Never train on private user content.** Non-negotiable. The engine measures *their* work for *them*;
  it does not learn from it.
- **Free for this use.** The therapeutic/own-story path carries no fee. (Revenue is the press +
  done-with-you services + the platform's *publishing* features, not a paywall on healing.)
- **Duty of care.** When real, sometimes hurting people pour trauma in, we owe: data protection (POPIA
  in SA / GDPR), gentle crisis-resource signposting, and *no dark patterns*. We are a tool for
  authorship, **not** a therapist or a substitute for one — say so plainly.
- **The measure-don't-generate line protects this too.** The tool never rewrites the person's words —
  which is exactly what makes it safe to put your real self into it.

**The wider frame (AJ):** these books — and this platform — are in part the answer to "what is your
religion?": a moral compass not bound by dogma or doctrine. *Sawubona* — "I see you." The platform's
purpose is to let people be seen, in their own words, at no cost. (See the trilogy canon's *Sawubona*
thread and the Jakobus character sheet for the in-fiction expression of the same ethic.)

---

## 5. NEW-ish — the printing exchange (L5)

**Standing print spec (DECIDED 2026-06-14):** **all books are 6×9in (152×229mm) for now** — one trim
across POD, ebook-source, and the gift boxset. This supersedes the boxset's earlier Royal 234×156mm
re-trim (now dropped — the 6×9 interiors already exist, so there's no re-trim task). Revisit only if a
specific edition needs a different trim. See [`../print-run/BOXSET_PLAN.md`](../print-run/BOXSET_PLAN.md)
+ [`../print-run/POD_ECONOMICS.md`](../print-run/POD_ECONOMICS.md).

**Today (`print-run/`):** the zero-upfront POD route — KDP + IngramSpark print each copy on sale, no
print bill, rights retained. This is solid and shippable now. It is *using* existing POD services.

**The new idea ("Uber for printing presses"):** a marketplace that matches **small/short print runs**
(an author wants 100–500 copies; a boxset; a local-language edition) to **idle capacity at small
printing presses** — print-on-demand without the POD middleman's per-copy cut, and keeping money with
small/independent presses (and, in the mission spirit, African presses).

**Honest status:** this is a **separate, operationally heavy business** (supply-side onboarding of
presses, quoting, quality spec, fulfilment, payments/payouts, disputes). It should **not** block the
press/platform launch. Sequence it *after* L2/L3 are live and there's real demand. `print-run/
QUOTE_REQUEST.md` is the seed of the quoting flow; that's the natural first concrete artifact (a
structured quote request → a press's bid) if/when we build the exchange.

---

## 6. The housekeeping that unblocks everything

1. **Branch reconciliation (the real "consolidation").** `africangold` (`companion/gita-song-of-the-self`)
   and `africangold-portfolio` (`portfolio-hardening`) are **two working trees of the same GitHub
   repo** on two long-lived branches — *not* diverged repos. The venture material (this doc, `site/`,
   `saas/`, `brand/`, `print-run/`, `deploy/`, `workspaces/`) is on `portfolio-hardening`; the prose +
   `FEARLESS_BADGER` docs + `piezo-pangolin/` workspace are on `companion/…`. **Action:** decide a
   merge strategy to `main` (or designate one branch as the venture trunk) so the venture isn't split.
   This is a branch merge, not a migration — much lower risk than the `history-before-time` orphan
   episode, but worth doing deliberately before adding more.
2. **The name rebrand surface** — work the checklist in §1.
3. **Package the CTO funnel (L6)** — the explainer material exists; assemble it into one consultant-
   facing piece (architecture, the diagrams, the *measure-don't-generate* thesis, the guardrail-
   register results, the "what I'd build for you" close).

---

## 7. Suggested sequence (next fronts)

Each ends at something demonstrable; validate before building big (the `brand/STRATEGY.md` §8 GTM
discipline holds).

1. **Settle the brand** (Arjuna Badger Press = tech, Arjuna Badger Press = house?) and do the §1 rename pass.
2. **Reconcile the branches** to one venture trunk (§6.1).
3. **Build the ⛔ non-negotiable Verification Gate** ([`VERIFICATION_GATE.md`](VERIFICATION_GATE.md))
   — productise live-internet fact-checking + the both-sides check on the existing extractor; first
   provable step re-derives the 4 errors the manual pass already caught.
4. **Write the L4 therapeutic-mission spec** as its own product doc (the design commitments above → a
   real feature spec: private-by-default projects, the narration-back loop, the care/safeguarding
   checklist).
5. **Package the L6 CTO explainer** from existing material.
6. **Formalise the L2 90%-author royalty model** (turn the `POD_ECONOMICS` math into a published model).
7. **Defer L5 (the printing exchange)** until L2/L3 demand is real.

---

## 8. Cross-links (the spokes this hub governs)

- Brand & GTM: [`../brand/BRAND.md`](../brand/BRAND.md) · [`../brand/STRATEGY.md`](../brand/STRATEGY.md) · [`../brand/MARKET_ANALYSIS.md`](../brand/MARKET_ANALYSIS.md)
- Platform & product: [`PRODUCTISATION_PLAN.md`](PRODUCTISATION_PLAN.md) · [`SAAS_ARCHITECTURE.md`](SAAS_ARCHITECTURE.md) · [`../saas/README.md`](../saas/README.md)
- Free-knowledge arm: [`ARJUNA_BADGER_PRESS.md`](ARJUNA_BADGER_PRESS.md) · [`ARJUNA_BADGER_PLATFORM.md`](ARJUNA_BADGER_PLATFORM.md)
- Publishing & print: [`WIDE_DISTRIBUTION.md`](WIDE_DISTRIBUTION.md) · [`NLSA_ISBN_APPLICATION.md`](NLSA_ISBN_APPLICATION.md) · [`../print-run/POD_ECONOMICS.md`](../print-run/POD_ECONOMICS.md)
- The site: [`../site/README.md`](../site/README.md) · [`../site/index.html`](../site/index.html)
- The IP proof: `guardrail-register-thesis` (separate repo) — the empirical thesis behind the method
- The method invariant: [`MASTER_PLAN.md`](MASTER_PLAN.md) §0 (*tools measure & alarm, never generate*)
- The accuracy non-negotiable: [`VERIFICATION_GATE.md`](VERIFICATION_GATE.md) (fact-check everything + both sides, Weir/Crichton/Brown bar)
