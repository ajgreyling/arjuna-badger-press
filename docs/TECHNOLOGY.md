# The technology behind the library

> **What this is.** A plain-English, diagram-led tour of the manuscript-craft studio that produces
> the books in this library — written for an engineering leader who wants to see the *system design*,
> not the prose. It describes the architecture and the guardrails. It does **not** publish the
> proprietary engine itself (the prompts, the scoring models, the graph schema, the gate internals);
> those are private IP. This is the blueprint a CTO can read in ten minutes.
>
> *The author of these tools is available for consulting.* — [arjunabadger.press](https://arjunabadger.press)
>
> **For authors & editors** — what the workshop offers, who it is for (including established
> authors), and the upload → wizard → Go → proofread flow → **[The workshop](FOR_AUTHORS.md)**.

---

## 0. The one invariant everything hangs on

**Tools measure and sound the alarm. They do not generate, and they do not drive.**

A human writes the soul of the book. Large models draft and edit *under* that authorship. A layer of
deterministic tooling stands guard — it checks, scores, and **blocks**, but it never writes the
voice. This is the line that separates "AI slop" from a book a person is proud to sign: the machine
is a *gate and a microscope*, not the author.

This single rule is why the output reads like a person wrote it — and it is the rule most AI-content
pipelines get exactly backwards (they let the model drive and bolt a spell-checker on the end).

```mermaid
flowchart LR
    H[Human author<br/>seed · canon · surgical edits] -->|authors| P
    subgraph P[AI draft + multi-role editorial pipeline]
      direction LR
      D[Draft] --> E[Edit]
    end
    P --> G{{Deterministic guards<br/>measure · score · BLOCK}}
    G -->|pass| OUT[Print-ready manuscript]
    G -->|fail: alarm, don't fix| H
    classDef guard fill:#1b1b1b,stroke:#d4af37,color:#fff;
    class G guard;
```

---

## 1. System overview

Three planes: a **generation plane** (multi-provider LLMs), a **state plane** (a continuity graph +
rolling story-state), and a **control plane** (the gates and scorers that decide whether a chapter is
allowed to exist). Generation is the only place tokens are spent; everything else is deterministic.

```mermaid
flowchart TB
    subgraph GEN[Generation plane · metered LLMs]
      O[OpenAI — structure brain<br/>outline · continuity audit · summarise]
      A[Anthropic Opus — prose engine<br/>draft · multi-role polish]
    end
    subgraph STATE[State plane · deterministic]
      SG[(StoryGraph<br/>geospatial-temporal graph DB)]
      SS[Rolling story-state<br/>continuity compression]
    end
    subgraph CTRL[Control plane · deterministic gates]
      VG[Verification gate<br/>accuracy + both sides]
      CG[Continuity gate<br/>8 constraint families]
      NB[NovelBench<br/>manuscript scorer]
      DL[de-LLM loop<br/>machine-tell scanner]
    end
    O --> A --> CG
    A --> SS --> SG
    CG <--> SG
    A --> VG
    A --> NB
    A --> DL
    CG -->|hard block| A
    VG -->|flag| A
    NB -->|score regression| A
    DL -->|tic regression| A
```

| Stage | Provider | Role | Output |
|---|---|---|---|
| 1 · Outline | OpenAI | structure brain (blueprint-aware) | chapter plan |
| 2a · Draft | Anthropic (Opus) | prose engine | raw chapter |
| 2b · Polish | OpenAI + Anthropic | multi-role editorial pipeline (triage → structure → character → line → dialogue → **gatekeeper**) | modulated chapter |
| 2c · Continuity audit | OpenAI | auditor (structured JSON) | issues → one targeted fix pass if errors |
| 2c′ · Graph gate | — | re-ingest + constraint check | **hard block** on any violation |
| 2d · Summarise | OpenAI | continuity compression | rolling story-state |
| 3 · Merge | — | deterministic assembly | print-ready manuscript |

Every chapter is checkpointed; a re-run **resumes** and skips completed work. The polish stage's last
pass is a **style gatekeeper** that may *reject a flattened revision and fall back to the stronger
draft* — an LLM judging an LLM, with the human's protected spans injected so the things that make the
prose human are never edited out.

---

## 2. StoryGraph — a geospatial-temporal continuity graph

The spine of the system. Every chapter is parsed into a graph DB whose nodes are **characters,
places, objects, factions, and events**, and whose edges carry **time** and **space**. Two axes make
it more than a wiki:

- **Temporal** — a *two-layer timeline* (a present-day chronology braided with an ancient one). The
  gate asserts the braid **closes** and that no fragment is orphaned in time.
- **Geospatial** — places and the movement of key objects between them form a tracked route. The gate
  asserts an object's location chain is **unbroken** (you cannot read a relic in Egypt that was last
  seen, unmoved, in South Africa).

```mermaid
erDiagram
    CHARACTER ||--o{ EVENT : "acts in"
    PLACE     ||--o{ EVENT : "located at"
    OBJECT    ||--o{ EVENT : "appears in"
    FACTION   ||--o{ CHARACTER : "claims"
    EVENT     ||--|| TIMELINE : "stamped (present|ancient)"
    OBJECT    ||--o{ PLACE : "moves between (route)"
    CHARACTER ||--o{ OBJECT : "carries / hands off"
```

On every chapter the graph is **re-ingested from scratch** and a constraint checker runs across the
whole work — eight families, including the state-machine of who-knows-what, the relay/hand-off chain,
the key-chain of plot-critical objects, the two-layer timeline braid, cross-book payoffs, and the
"physics" rules of the world. **Any violation is a hard block** — the chapter does not pass until it
is fixed. This is the difference between a continuity *editor* (catches some) and a continuity *gate*
(catches all, deterministically, every run).

```mermaid
flowchart LR
    C[New / edited chapter] --> I[Re-ingest whole work<br/>into graph DB]
    I --> K{check_constraints<br/>8 families}
    K -->|clean| PASS([proceed])
    K -->|violation| BLOCK[[BLOCK + precise reason]]
    BLOCK --> FIX[Targeted fix] --> C
```

---

## 3. NovelBench — a read-only manuscript scorer

A genre-aware scorer that grades a finished manuscript on craft dimensions (tension, pacing, agency,
structure conformance, voice, over-explanation, and more) against per-genre targets. It is
**read-only**: it scores, it never rewrites. Its job is to turn "this feels off" into a *number that
moved*, so a revision can be judged by whether it actually improved the book or just changed it.

It runs in two tiers: a free **local/deterministic** pass (sentence-layer metrics) on every build,
and a metered **LLM scorecard** for a deeper read when it's worth the spend.

---

## 4. The de-LLM loop — hunting the machine tells

A closed editorial loop whose only goal is "no obvious craft issues or LLM tells." Three components
chase each other until only material creative changes remain:

1. **A brutal cold-read agent** (sentence layer) and a **structural craft audit** (the layer above —
   voice homogenisation, gravitas inflation, over-polished action, reveal/reaction order) find the
   problems a model's prose falls into.
2. Each finding is **re-incorporated into the engine** — the prompts, the style guide, and a
   deterministic **tic scanner** that counts the specific machine-tells against falling targets.
3. A surgical, human-in-the-loop prose pass fixes them. Then the loop runs again.

```mermaid
flowchart LR
    R[Cold-read + craft audit<br/>find craft issues / LLM tells] --> X[Re-incorporate into engine<br/>prompts · style guide · tic scanner]
    X --> F[Surgical edit pass<br/>human in the loop]
    F --> S{Tic scanner<br/>+ scorers}
    S -->|tells remain| R
    S -->|only creative changes left| DONE([ship])
```

The point: the system **learns from its own failures**. A tell found once becomes a guardrail that
catches it forever after — the prose quality ratchets, it doesn't drift.

---

## 5. The verification gate — accuracy + both sides

Non-negotiable, and documented in full: every real-world claim is fact-checked against live sources,
and every *contested* claim is required to carry **both sides**. The bar is Andy Weir / Michael
Crichton / Dan Brown — "a hostile expert with a search engine cannot catch a silent factual error,
and a fair-minded reader cannot accuse the book of one-sided history."

→ **[Read the Verification Gate spec](VERIFICATION_GATE.md)**

---

## 6. Why a CTO should care

This is a working reference implementation of the things every team is now trying to get right with
generative AI:

| Capability | How it shows up here |
|---|---|
| **Human-in-the-loop by design** | the author drives; the model never has the last word — the gatekeeper can fall back to the human's draft |
| **Guardrails & hard gates** | continuity gate + verification gate **block** bad output; they don't politely suggest |
| **Deterministic evals** | NovelBench + the tic scanner turn quality into numbers that gate regressions, like tests in CI |
| **Multi-provider routing** | the right model for the job — a structure brain and a prose engine, not one model forced to do both |
| **State & memory at scale** | a graph DB + rolling compression hold a 90k-word, multi-book world in continuity |
| **Self-improving loop** | failures are converted into permanent, deterministic checks |
| **Cost discipline** | tokens spent only in the generation plane; everything else is free and deterministic |

The invariant — *measure, don't generate; the human authors, the machine guards* — is portable to any
domain where AI output has to be trustworthy: legal, medical, finance, code. The books are the proof
that it works end to end.

> **Want this in your stack?** The author of this system consults on AI pipelines, human-in-the-loop
> design, and guardrail/eval architecture. → [arjunabadger.press](https://arjunabadger.press)

---

## 7. The platform — the studio as a portable, multi-tenant service

The engine above produces *this* library. The same machinery also runs as a **service** other
authors can use: a multi-tenant SaaS where an author brings a manuscript and notes, answers a short
wizard, and gets back a proofread-ready book — the workshop, productised.

It is built **cloud-agnostic on purpose**. State lives in two portable places — a Postgres control
plane and an **S3-compatible** object store (R2 / B2 / S3 / MinIO, chosen by an env var, never a
vendor SDK) — so the whole thing moves between hosts without a rewrite. The web tier is a **stateless
API**; the heavy generation runs in a **broker-free worker queue** (Postgres `FOR UPDATE SKIP
LOCKED`), so workers scale horizontally and a crashed job **resumes** from its last checkpoint rather
than restarting.

```mermaid
flowchart TB
    A[Author] --> API[Stateless API<br/>auth · projects · uploads]
    API --> DB[(Postgres<br/>control plane)]
    API --> OBJ[(Object store<br/>S3-compatible · portable)]
    API -->|enqueue| Q[[Job queue<br/>SKIP LOCKED]]
    Q --> W[Worker<br/>runs the engine · resumable]
    W --> OBJ
    W --> DB
    classDef store fill:#1b1b1b,stroke:#d4af37,color:#fff;
    class DB,OBJ store;
```

A work is **private by default**. It becomes public only when its author asks and the press accepts —
publication and wide distribution (the library, plus any external stores) are tracked as explicit,
auditable states, never an accident. The control plane stays vendor-neutral so an author's work is
never locked to one cloud.

---

## 8. Zero-access encryption — even we can't read it

Some authors write the real stories of vulnerable people. For that, "we promise not to look" is not
good enough. So the platform offers **sealed works**: end-to-end, **zero-access** encryption where the
operator — us — **cannot read the content at all**. The duty of care to the people in those stories is
higher than our convenience as an operator, and the architecture is built to make that literal.

Every work is one of two classes, chosen by the author:

| | **Sealed** *(zero-access)* | **Engine-assisted** |
|---|---|---|
| Who can read it | **Only the author** | the author + the engine |
| AI help (draft / polish / gate) | **None** — the engine never runs on it | full pipeline |
| Stored as | ciphertext the server can't open | server-readable |
| Default for | other people's personal stories | the studio's own books / opt-in work |

This is an honest trade-off, stated plainly: **the engine cannot help with a work it cannot read.**
You get our tooling, or you get zero-access — per work, your choice. Sealed is the default for
anything carrying real PII.

**How "even we can't read it" is true.** Content is encrypted **in the author's own client** under a
key derived from the author's secret. The key hierarchy never hands the server anything that opens it:

```mermaid
flowchart TB
    PW[Author password] -->|Argon2id| ARK[Author Root Key<br/>client-only, never sent]
    REC[Recovery key<br/>author-held, offline] --> RWK[Recovery Wrap Key]
    ARK --> AMK[Author Master Key]
    RWK --> AMK
    AMK --> DEK[Per-work key]
    DEK -->|AES-256-GCM| CT[(Sealed content<br/>ciphertext in object store)]
    classDef store fill:#1b1b1b,stroke:#d4af37,color:#fff;
    class CT store;
```

The server stores only *wrapped* keys, public salts, and a one-way login verifier. **A complete theft
of the database and the object store decrypts nothing** — no password, no plaintext, no PII. That is
the design centre: *a leak, a stolen backup, or a subpoena yields ciphertext, never a vulnerable
person's story.*

**Break-glass support — granted, time-boxed, audited, then re-keyed.** When an author needs help with
a sealed work, *they* open the door, briefly:

```mermaid
flowchart LR
    G[Author grants access<br/>chooses a time window] --> O[Operator reads the ONE work<br/>every access logged]
    O --> R[Issue resolved<br/>grant revoked]
    R --> K[Work re-keyed<br/>fresh key · operator access dies]
    classDef gate fill:#1b1b1b,stroke:#d4af37,color:#fff;
    class K gate;
```

The author re-wraps just that work's key to a support key, for a set window. We can read that single
work while the grant is live — and **every access is written to an audit log the author can read**.
When it's resolved, the work is **re-keyed**: a fresh key, the content re-encrypted, and our prior
access is dead. Support is a temporary, accountable visit, never a standing key.

**Durability without exposure.** Because what's stored is ciphertext, it is safe to replicate widely —
so catastrophic hardware loss never *loses* PII (it's backed up) and a leaked backup never *exposes*
it (it's encrypted). And because there is **no operator escrow**, recovery is the author's own
high-entropy recovery key, held offline. The cost is honest and stated up front: lose both your
password and your recovery key, and the work is unrecoverable — the same property that makes it
unreadable to us makes it unrecoverable without you. **No backdoor is the feature.**

---

## 9. Access & economics — bring your own key, or BadgerBucks

Two ways to power the metered generation, and a deliberate ethic about who pays.

- **BYOK** — bring your own model-provider key; the token cost is yours, and your key is stored
  **envelope-encrypted** (the database never holds it in the clear).
- **BadgerBucks** — the platform's prepaid token credit, for authors who'd rather not manage a key.

The pricing carries a **geo-subsidy**: the first world subsidises the third. The *credit* is the same
everywhere; the *price* of buying it isn't — wealthier regions pay a multiplier, and a set of
lower-income regions (much of Africa, India, and the ex-British colonies) pay the base rate and
receive a small standing grant, so a writer without a card can still use the studio. It is a small,
explicit redistribution baked into the billing, not a marketing line.

---

## 10. `/sleep` — memory consolidation as a first-class step

The table above lists *state & memory at scale* as a capability — a graph DB and rolling compression
holding a multi-book world in continuity. That covers the **engine's** memory. It does not cover the
**agent's** memory: the question of what an AI co-worker should carry from one working session into
the next. That turned out to have a missing primitive, and closing it produced a small, portable tool
that ships on its own.

**The problem.** A coding agent has two memories and, by default, no bridge between them:

- **working memory** — the live session, everything said this turn; and
- **a long-term store** — the durable facts a future session needs (`CLAUDE.md`, a `memory/`
  directory, a Cursor `lessons-learnt.mdc`, an `AGENTS.md`, a docs-of-record table).

The two controls you're handed are both wrong for real work. **`/clear` is death** — it doesn't close
the eye, it deletes the *person*; the next session inherits nothing. **Never clearing is insomnia** —
the context grows without bound (cost, latency) and the durable facts stay trapped in a transcript no
future session will ever read. Biology already solved this with the third option: **sleep** — the
nightly, lossy, *intentional* move that keeps what the day taught and discards the lived texture of
it. You don't keep the dream; you keep the lesson.

```mermaid
flowchart LR
    S[Working session<br/>the lived experience] --> Q{{/sleep<br/>one filter}}
    Q -->|FACT· decisions+why · gotchas<br/>· user prefs · project state| M[(Long-term store<br/>memory/ · lessons-learnt · AGENTS.md)]
    Q -->|EXPERIENCE· play-by-play · dead ends<br/>· emotional weather · already-in-repo| X[evaporates]
    M --> N[Next session<br/>wakes carrying only what mattered]
    classDef gate fill:#1b1b1b,stroke:#d4af37,color:#fff;
    class Q gate;
```

**The mechanism.** `/sleep` runs the whole session through one question — *what must survive the
session ending, and what was only the texture of getting there?* — sorts every item into **FACT**
(persists) or **EXPERIENCE** (evaporates), **auto-detects the repo's own store** and writes in *that*
store's format, **shows the consolidation envelope before writing** (memory is hard to un-write), and
**dedups and prunes** rather than piling up. It is the same human-in-the-loop, measure-don't-sprawl
discipline as the rest of this system, pointed at the agent's memory instead of the manuscript.

| Design choice | Why it matters to an engineering leader |
|---|---|
| **Lossy on purpose** | the value of a memory store is everything it *didn't* write; a store that swallows everything is noise. Signal beats volume — the same reason evals gate regressions instead of logging everything. |
| **Store-agnostic** | one ritual across a polyglot estate — a Cursor repo's `lessons-learnt.mdc` and a Claude-native `memory/` dir are written in their own idioms, no new format imposed. |
| **Envelope before write** | the human approves what their future self inherits; nothing outward-facing or durable is persisted blind. |
| **Reflex via hooks, not magic** | a `PreCompact` / `SessionEnd` hook *reminds*; it never silently writes — the human keeps the brake. |

**It is open source.** The skill, the reminder hook, and the install steps are public, MIT-licensed:
**[github.com/ajgreyling/claude-sleep-skill](https://github.com/ajgreyling/claude-sleep-skill)**. The
longer-form story of where it came from — and the conversation about what it means for a machine to
"remember" at all — is in [The kettle and the blink](../site/content/writing/the-kettle-and-the-blink.md)
on the press site.

> The discipline is the same one this whole document argues for: **the human authors; the machine
> measures, filters, and asks before it commits.** `/sleep` just applies it one layer up — to memory
> itself.
