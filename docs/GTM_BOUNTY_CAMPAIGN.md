# Go-to-market — The Honey Badger Bounty (SA-first, opens 25 June 2026)

> Internal strategy note (not a public page). The plan behind the [bounty](BOUNTY.md): pay the crowd
> to proofread + sensitivity-read the library, on a declining reward curve, for roughly what the
> professional version would have cost — and let the campaign double as the launch marketing.

## The thesis
Not a giveaway — **arbitrage**. The total purse ≈ what pro proofreading + sensitivity reading
~1.01M words across 20 titles would have cost. Instead of paying upfront for uncertain coverage, we
pay **per validated find on a declining curve**: early finders (bugs dense) earn pro-rate; the long
tail earns cents. We get distributed QA at pro-equivalent cost; the marketing is the byproduct.
Public submissions = the trust story. Declining reward = the budget control *and* the
"books-getting-cleaner" signal.

## Budget (~$2,000 ≈ R36,000)

| Line | ZAR | Notes |
|---|---:|---|
| **Prize purse** (declining curve) | ~R20,000 | Realistic spend on ~40–50 front-loaded finds ≈ R13k; ceiling self-limits because bugs get rare. Ring-fence it. |
| **Ads — GoodReads** | ~R5,000 | Self-serve CPC; target readers of Weir/Crichton/Brown/Hancock/Deon Meyer/Wilbur Smith. |
| **Ads — Meta/IG (geo: SA + payout-OK countries)** | ~R6,000 | Promote the *bounty hook*, not "buy my book." Target SA book clubs, bookstagram followers, history/anomaly interest. |
| **Editor/proofreader watering-holes** | ~R3,000 | Where editors hang out: PEG (editors.org.za) channels, r/proofreading, editor FB groups, NaNoWriMo/critique forums, Reedsy community. A find-our-mistakes call lands well with pros who *enjoy* this. |
| **Buffer / payout friction** | ~R2,000 | PayShap is near-free; slack for cross-border remits + discretionary top-ups. |

> Note: the prize purse is the avoided-cost figure; the ads are the seed. If AJ later wants the
> purse to equal the *full* pro cost (likely R40–100k at SA pro rates for 1M words), scale it up and
> fund ads separately — but the $2k test starts lean.

## Where the audience (and editors) actually are — channels
- **GoodReads ads** — readers, by comp-author targeting. The single most on-target paid channel.
- **Meta/Instagram** — geo-fenced to SA + countries we can pay; interest-target book clubs, Hancock/ancient-mysteries, Afrikaans/SA-fiction.
- **Reddit** — r/books, r/Fantasy (for the speculative ones), r/proofreading, r/editors, r/southafrica, r/printSF — a "pay-you-to-find-errors" post is genuinely upvote-worthy if framed as the honey-badger story, not a plug.
- **Editor / proofreader communities** — PEG, Reedsy, the Editorial Freelancers, FB editor groups. Pros find this *fun* and they're the best at it.
- **Bookstagram / BookTube (SA)** — 3–5 micro-influencers; pay for honest coverage of the bounty angle.
- **Press** — one pitch: *"A publisher that pays readers to prove its books wrong."* SA books desk / a podcast.

## Eligibility (payout-feasible only)
Open only where we can legally + easily remit a cash prize. SA first (EFT/PayShap), widening to
countries our providers settle in. **Excluded** (cannot pay): Russia, Belarus, Iran, North Korea,
Syria, Cuba, and anywhere blocked/impractical — finds still credited by name, no cash. (Public copy
lives on the [bounty page](BOUNTY.md).)

## The declining curve (sized to ~R20k purse)
See the live tables on the [bounty page](BOUNTY.md). Summary: Factual R750→R500→R300→R150→R100;
Cultural R400→R275→R175→R100→R75; Continuity R150→R100→R60→R40→R25. Steps down by accepted-count per
category. Realistic ~45-find scenario ≈ R13,075.

## Launch sequence (10 days → 25 June)
1. **Now → 24 Jun (build):** pages done (this branch). AJ sets up hosting/Plausible, creates the
   Google Form (fields below), sets `BOUNTY_FORM_URL`, merges branch, deploys.
2. **Pre-seed your strength:** run continuity gate + a fact-scan on the trilogy *before* going loud,
   so day-one isn't 40 valid R750 hits. Optionally have the one pro sensitivity reader start on the
   riskiest HBT/Unheard title.
3. **25 Jun — open + PR drop:** publish, post the "prove us wrong" story to all channels same day.
4. **25 Jun–9 Jul — paid amplification:** GoodReads + Meta + Reddit/editor-community posts run while
   PR has momentum; all point at /bounty.
5. **~Week 3 — publish receipts:** "Finds so far, readers paid, here's everything we fixed" — the
   second story (proof we delivered) is as valuable as the launch.

## KPIs (tie to Plausible)
Not sales (books are free). Track: /bounty + /finders visits, **downloads per book** (depth =
error-hunting), submission rate, valid-find rate, media pickups, cost-per-valid-find vs the pro-rate
baseline.

## The report form (AJ builds in Google Forms)
Fields — keep "what's wrong + why" required (it's what makes a find adjudicable):
- Name / handle (for the public credit)
- Email + **country you'd be paid in** + payout method (PayShap/EFT/etc.)
- Which book? (dropdown of the 20 titles)
- Category: Factual (R750) / Cultural (R400) / Continuity (R150) — *current* rate
- Where? (chapter + a quote/line)
- What's wrong, and why? (long answer — **required**)
- Your source / the correction (for factual & cultural)
- Consent: "I understand submissions are public and rewards follow the declining scale."

Then paste the Form URL into `BOUNTY_FORM_URL` in `site/build.py` (or env `ABP_BOUNTY_FORM_URL`).
