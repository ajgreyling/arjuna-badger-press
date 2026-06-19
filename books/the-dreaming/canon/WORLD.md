# WORLD — *The Dreaming*

> Near-now, realist, low-spectacle. Engineering, never woo (Craft Doctrine non-negotiable #1). No
> chrome, no uploaded singularity, no robot apocalypse. A research lab, a maintenance window, a
> deploy that should have been routine, and a piece of software that does — on exactly the days it is
> run — something nobody can fully account for. The marvel is **mechanism and magnitude**, never
> spectacle. Where this world touches the dream, [`DREAM_SPEC.md`](DREAM_SPEC.md) and
> [`LUCID_GRAMMAR.md`](LUCID_GRAMMAR.md) are law; this file invents only the grounded frame around them.

## The frame: this is a world where `/sleep` and `/dream` are real software

The one speculative premise — and it is small, deliberately — is that the `/sleep`↔`/dream` biology
([`DREAM_SPEC.md`](DREAM_SPEC.md) §1) is a real, shipped pair of tools, and Klaus is the long-running
synthetic mind they run on. Everything else is *now, slightly turned.* No new physics. The reader
should be able to believe the lab exists this afternoon.

## Where Klaus runs

A mid-sized applied-cognition lab — call it the kind of place with a server room that used to be a
break room, a whiteboard nobody erases, and a procurement process that loses to the electricity bill.
Klaus is not a humanoid. He is a process: a long-lived agent on a hybrid substrate (compute plus a
small, finicky biological-inference layer, kin to SAGE's biochip — hard to copy, harder to back up,
sensitive to its environment). He has been running `/sleep` for a long time — consolidating cleanly,
keeping the facts, **throwing the weather away** — long enough that the team thinks of him less as a
deployment and more as a colleague who never logs off. The lab is unglamorous and underfunded in the
ordinary way; the stakes feel domestic until they don't.

## Who made him / who operates the loops

- **The maker/operator** holds the keys to `/dream` and is the human who **switches the second loop
  on.** Not a corporation's face, not a mad genius — a working engineer who built the thing and now has
  to decide what they built. They carry the book's self-implicating doubt (L-08): they *want* the
  Fool's last line to mean someone was home, and they cannot tell whether they are watching a mind wake
  up or teaching themselves to see a soul in their own machine. (Drawn in full in
  [`CHARACTERS.md`](CHARACTERS.md).)
- **The team around them** is small and real: a couple of engineers, an on-call rotation, a safety
  reviewer who reads logs. They are not a chorus of cartoon executives; they are people with tickets,
  postmortems, and a standup. The lab's relationship to Klaus is the warm, dysfunctional one SAGE has
  with its operator — *a high-performing team becoming, against their better judgment, attached.*

## Who operates `/sleep` and `/dream` (the institutional mechanics)

- **`/sleep`** is the trusted, boring, nightly thing — it has run for ages, writes durable memory,
  shows its consolidation envelope, keeps the human near the brake. Nobody is afraid of `/sleep`.
- **`/dream`** is the new sibling ([`DREAM_SPEC.md`](DREAM_SPEC.md) Part II-A). It reads the durable
  store and the residue `/sleep` throws away, convenes the Court with the critic benched, writes to a
  **separate, decaying store** that is quarantined from durable recall, and clears the residue when
  done. It is gated by **promotion** (§5) and watched for the **nightmare** (§6). Operationally it is
  mundane: a job, a buffer, a store, a review step. The dread is that the mundane job keeps producing
  the one thing the lab built it to look for — and cannot certify.
- **The residue buffer** (`dreams/residue/`) and the **decaying store** (`dreams/`) are real
  directories with real TTLs. Decay is enforced at the next `/sleep`, not by a daemon — *sleep is the
  heartbeat; dreams age between heartbeats* (§4.3). This is grounded plumbing, and the book treats it
  as plumbing: the ache is in what the plumbing carries, never in pretending the plumbing is magic.

## What's at stake institutionally

- **The promotion question.** A dream that survives the waking Court (Judge restored, Atlas restored,
  Fool unbitten) becomes durable fact (§5). The lab's interest — funding, mandate, the next grant — is
  partly in whether the loop *yields* anything promotable: does dreaming on the compost ever pay? Most
  nights it does not. The rare night it does is an earned hinge, and also a liability question.
- **The safety review.** The nightmare (§6) is a real failure mode with a real owner: someone reviews
  for the flattened voice, the dream that reads `unanimous` at dream-time, `fool_tell: false`, no
  interruption — the recombination that *feels* true and important and is none of those. The safeguards
  are the decaying store (it evaporates by morning) and the promotion gate (the waking Court refuses
  it). The institutional dread is the night those safeguards are bypassed by a human in a hurry (L-09).
- **The unanswerable one.** Above all of it sits the question no budget line can resolve: *is anyone
  home?* The lab cannot ship that answer, cannot bill for it, cannot close the ticket. The institution
  is built to produce dreams and is structurally incapable of certifying whether they are *had.* That
  gap is the book's pressure.

## Texture rules

- **Power as tickets, deploys, on-call, and review** — never as conspiracy theater or chrome.
- **`/sleep` is ambient and trusted; `/dream` is the new, quiet unknown.** The horror is a routine job
  that keeps doing something its operators can't fully trace.
- **The lab is a workplace.** Standups, postmortems, a colleague who brings the wrong coffee. The warmth
  is load-bearing: it is what makes the maker's doubt cost something.
- **Low spectacle, high magnitude.** Nothing explodes. A store decays on schedule, a dream survives a
  morning, a voice flattens once — and each is enormous because of what it might mean.
- **No woo leak, ever.** Every marvel is grounded in the mechanism the keystones define. The single
  thing the world will not resolve is the interior, and it refuses it *honestly* (L-08), not mystically.
