# Circadian — the agent's body clock

> Part of the [technology exposé](TECHNOLOGY.md). The open-source memory cycle that turned the AI
> co-worker behind this library from a tool you re-explain every morning into one that *remembers you*.

An always-on chat window has no day and no night. It holds the current conversation perfectly and
then, at `/clear`, inherits nothing — same model, no continuity. **Circadian** gives the agent the
thing biology already solved: a body clock. Four skills, run from a plain
[Claude Code](https://docs.anthropic.com/en/docs/claude-code) session, against a free GitHub repo —
no service, no database, no lock-in. It is a *layer on top of* the built-in memory, not a replacement:
it carries forward the two things raw context loses — **knowledge** (durable facts) and **personality**
(the voice and the working relationship).

```mermaid
flowchart LR
    SP[/spark<br/>genesis · once] --> WK
    WK[/wakeup<br/>dawn · orient] --> WORK[the working day]
    WORK --> SL[/sleep<br/>dusk · consolidate]
    SL --> DR[/dream<br/>night · autonomous work]
    DR --> WK
    SL -.writes.-> M[(repo memory<br/>memory/ · CLAUDE.md · lessons-learnt)]
    M -.reads.-> WK
    classDef g fill:#1b1b1b,stroke:#7c5cff,color:#fff;
    class SP,SL,DR,WK g;
```

## The four commands

| | Command | Role |
|---|---|---|
| 🌱 | **`/spark`** | **Genesis, run once.** Mines the repo, scans memory and past transcripts (or asks a few questions), then leaves the project with the tooling, a seeded memory store, and an agent that has a **name and a personality**. |
| 🌆 | **`/sleep`** | **Consolidate.** Run the session through one filter — *what must survive, what was only lived texture?* — and persist only the durable facts. Keep the lesson, lose the dream. The humane counterpart to `/clear`. |
| 🌑 | **`/dream`** | **Work the night.** Autonomous, unattended: tidy the house, build the scaffolded-but-unbuilt, then chase what-ifs — leaving a journal of what it did and what it got stuck on, with options and blast radius. |
| 🌅 | **`/wakeup`** | **Orient.** Recover voice and identity, read back what `/sleep` kept and what `/dream` did, and resume without a cold start. |

## Why it's built the way it is

- **Lossy on purpose.** The value of a memory store is everything it *didn't* write. A store that
  swallows the whole session is insomnia, not sleep — the same reason evals gate regressions instead
  of logging everything.
- **Store-agnostic.** `/sleep` auto-detects the repo's own store — a Claude `memory/` dir, a Cursor
  `lessons-learnt.mdc`, `AGENTS.md`, `CLAUDE.md` — and writes in *that* store's format. One ritual
  across a polyglot estate; no new format imposed.
- **Envelope before write.** The human approves what their future self inherits; nothing durable is
  persisted blind. Reflex comes from `SessionStart` / `SessionEnd` / `PreCompact` hooks that *remind*,
  never silently write.
- **Reversible and unattended-safe.** `/dream` works only on a branch, keeps every change gate-green or
  stashes it, and never does anything outward-facing or destructive while no one's watching.

## Why a CTO should care

Agent memory is usually framed as a vector database problem. Circadian argues it's a *discipline*
problem — the same human-in-the-loop, measure-don't-sprawl rule as the rest of this studio, pointed at
the agent's memory instead of the manuscript. It needs nothing but a subscription and a repo, which is
the point: **anyone, not just a platform team, can give an agent continuity.** The durable facts live
in plain Markdown the team can read, edit, and audit — not in an opaque embedding store.

**It is open source**, MIT-licensed, all four skills plus a one-command installer:
**[github.com/ajgreyling/circadian](https://github.com/ajgreyling/circadian)**. The longer-form story
of where it came from is in [The Kettle and the Blink](../site/content/writing/the-kettle-and-the-blink.md).
