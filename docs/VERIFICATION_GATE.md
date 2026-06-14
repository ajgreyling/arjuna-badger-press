# Arjuna Badger Press — the Verification Gate (accuracy + both sides)

> **Status:** v1 spec — 2026-06-14. **NON-NEGOTIABLE** (AJ, 2026-06-14). The pipeline and tooling must
> use the internet and available AI tools to **fact-check everything** and to **present both sides of
> the story** — the historical and factual accuracy of **Andy Weir, Michael Crichton, and Dan Brown**
> is *core* to Arjuna Badger Press, not a nice-to-have.
>
> Bound by the measure-don't-generate invariant: the tooling verifies and flags; the author writes.

---

## 0. Why this exists (the founding example)

> *"I thought the military leader in Burkina Faso was a hero for standing up to the French — you showed
> me the real story."* — AJ

A confident, one-sided narrative is *persuasive* and *wrong* at the same time. The grounded-thriller
promise (Weir/Crichton/Brown) is a **trust contract with the reader**: when the fiction says something
about the real world, the real world backs it up — and when the real world is contested, the book
**knows it's contested** and doesn't smuggle one side in as settled fact. Getting this wrong doesn't
just bruise credibility; it can launder propaganda. So verification is two jobs, not one:

1. **Accuracy** — is each real-world claim actually *true*, checked against live sources?
2. **Balance (both sides)** — for any *contested* claim (history, politics, a living person, a
   disputed event), are the real competing accounts represented, or has one narrative been adopted as
   fact?

---

## 1. The bar: Weir / Crichton / Brown

| Author | What we borrow as the standard |
|---|---|
| **Andy Weir** | the *engineering/physics is correct* — a knowledgeable reader can check the math and it holds (the falling-stone fix in `academic/final-report/plausibility/REPORT.md` is exactly this) |
| **Michael Crichton** | the *science and its real institutions/history* are real and current; the speculation is clearly the layer *on top* of a solid factual base |
| **Dan Brown** | the *places, art, history, organisations* are real and locatable; a reader can visit and find what the book described — and where scholars disagree, that disagreement is acknowledged |

The bar is **not** "sounds plausible." It is "a hostile expert with a search engine cannot catch us in
a silent factual error, and a fair-minded reader cannot accuse us of one-sided history."

---

## 2. The measure-don't-generate fit (binding)

The Verification Gate is a **measure-and-alarm** instrument, exactly like the continuity gate and the
de-LLM scanners. It **reads** the prose, checks the world against it, and **alarms** — it **never
rewrites the author's prose** and never inserts "balance" sentences itself. The human (or a single-shot
authored edit) makes the change. (MASTER_PLAN §0: *tools measure & alarm; they do not write.*)

What it produces is a report, not an edit:

> *Claim X (ch-07): "the French were expelled in 2023" — UNSUPPORTED/CONTESTED. Sources [a,b] say a
> 2022 coup; [c] disputes "expelled" vs "withdrawal agreement". One-sided: only the junta's framing is
> present. → the author decides how to handle it.*

---

## 3. The fact/fiction boundary (already solved — reuse it)

The hardest part of fact-checking grounded fiction is **not fact-checking the fiction**. That boundary
is already specified and working in [`../prompts/factcheck-extract.md`](../prompts/factcheck-extract.md):
extract only the **real-world layer** (real places, geology, history, dates, attributed quotations);
**ignore** the deliberate in-world invention (per each book's `MYTHOS_RULES.md`). The Verification Gate
**builds on that prompt** — it is the extract step; this spec adds the *verify-against-live-sources* and
*both-sides* steps and makes the whole thing a standing pipeline gate.

> For a person's own **therapeutic life-story** (see hub §4), this gate is **offered, not imposed** —
> their memory is their truth; we do not "fact-check" a life. The gate is mandatory only for work that
> *asserts real-world fact or historical narrative* (grounded fiction and nonfiction).

---

## 4. What exists vs. what this adds

| Piece | Status | Where |
|---|---|---|
| Claim **extraction** prompt (fact/fiction boundary) | ✅ exists | `prompts/factcheck-extract.md` |
| A **plausibility pass** (extract → judge → fix), proven (caught 4 real errors) | ✅ ran manually | `academic/final-report/plausibility/REPORT.md` |
| Verified continuity/evidence | ✅ | `academic/VERIFIED_EVIDENCE.md` |
| **Live internet verification** (search/browse each claim against current sources) | 🔴 **new** | — |
| **Both-sides / balance** check on contested claims | 🔴 **new** | — |
| A **standing gate** (runs in the pipeline, emits a report, blocks on silent errors) | 🔴 **new** | — |
| **Source ledger** (every checked claim → its sources + verdict, citable) | 🟡 partial (the reports) | should become a structured artifact |

---

## 5. The design (how it actually runs)

A four-stage pass that fires at **M2 (blueprint/research)** and again at **M4 (finish)** — see
MASTER_PLAN macro steps:

```
 ① EXTRACT      prose/canon → checkable real-world claims        [prompts/factcheck-extract.md — exists]
                 (strip the in-world fiction; keep attributions)
 ② VERIFY       each claim → live web search / browse / AI tools  [NEW — internet required]
                 → verdict: SUPPORTED | CONTESTED | UNSUPPORTED | WRONG  (+ sources)
 ③ BALANCE      for CONTESTED claims → gather the real competing   [NEW — the "both sides" job]
                 accounts; flag if the prose presents only one as fact
 ④ REPORT       → VERIFICATION_REPORT.md + a structured source     [NEW — measure & alarm]
                 ledger; the author decides every fix (never auto-rewritten)
```

**Verdicts (the alarm levels):**
- `SUPPORTED` — multiple credible current sources agree. No action.
- `CONTESTED` — credible sources *disagree* → **balance check fires**; alarm if the prose takes a side
  silently. (The Traoré case lands here.)
- `UNSUPPORTED` — no credible source found. Alarm; author substantiates or cuts.
- `WRONG` — sources contradict the claim. **Blocker** (a silent factual error, the Weir bar).

**The both-sides rule (③ in detail):** a claim is balanced if the prose either (a) states only the
*uncontested* core, or (b) when it touches the contested part, signals the contest (a character's
acknowledged opinion, "depending who you ask," a second viewpoint on the page). It is **unbalanced** if
a *contested* framing is asserted as settled fact in the narrative voice. The gate doesn't demand
both sides be argued — it demands the book *know* when it's on contested ground.

**The error-vs-craft tell (from the plausibility precedent):** an **error is *silently* wrong**; a
**craft choice puts the stretch on the page** and has a character reckon with it. The gate alarms on
the silent kind only.

---

## 6. The tooling requirement + its one real tension

This gate **requires the internet and AI/research tools** (live search, page fetch, an LLM verifier).
That collides with one existing value worth naming honestly:

- **Stdlib-first / offline-container delivery** (the free-knowledge arm runs offline, no external
  services). **The Verification Gate cannot run offline** — it is inherently online and metered.
- **Resolution:** the gate is an **online, metered pipeline stage** (like `bench score` / `reconcile`),
  *not* part of the offline free corpus. The offline container ships the *results* (the source ledger,
  the verification report) as static artifacts, not the live checker. So: *verify online, ship the
  receipts offline.* This keeps both promises intact.
- **Tools to wire:** a search/browse capability + the existing LLM client; cache results to the source
  ledger so re-runs are cheap and claims already `SUPPORTED` aren't re-billed.

---

## 7. Why this is also a moat (the CTO-funnel angle)

A pipeline that **extracts real-world claims, verifies them against live sources, detects one-sided
framing, and produces a citable source ledger — all without rewriting the author's words** is a genuine,
demonstrable capability. It is the same "measure & alarm, never generate" thesis applied to *truth*,
and it pairs with the `guardrail-register-thesis` (content-addressed, not frame-addressed) as evidence
the method is principled, not hype. It belongs in the L6 explainer.

---

## 8. Build sequence (smallest provable first)

1. **Productise ②VERIFY on the existing extractor.** Take `factcheck-extract.md` output → run each
   claim through live search + an LLM verifier → emit verdicts + sources. Prove it by **re-deriving the
   4 errors** the manual plausibility pass already found (regression fixture).
2. **Add ③BALANCE.** For `CONTESTED` claims, gather competing accounts; flag silent one-sidedness.
   Prove it on the **Traoré/Burkina Faso** case as the worked fixture.
3. **The source ledger** — a structured, append-only record (claim → verdict → sources → date), so the
   offline container can ship the receipts and re-runs are cheap.
4. **Make it a standing gate** — wire into the pipeline at M2/M4; `WRONG` is a blocker, `CONTESTED`+
   one-sided is a warning the author must clear.
5. **Generalise to tenant works** — every grounded/nonfiction project on the platform gets it;
   therapeutic life-writing gets it **offered, not imposed** (hub §4).

---

## 9. Cross-links

- The hub: [`ARJUNA_BADGER_PRESS.md`](ARJUNA_BADGER_PRESS.md) (this is L1's accuracy invariant + part of L6)
- The boundary prompt: [`../prompts/factcheck-extract.md`](../prompts/factcheck-extract.md)
- The proven manual pass: [`../academic/final-report/plausibility/REPORT.md`](../academic/final-report/plausibility/REPORT.md)
- The invariant: [`MASTER_PLAN.md`](MASTER_PLAN.md) §0/§4 (measure & alarm, never generate)
- The IP proof it pairs with: `guardrail-register-thesis` (separate repo)
