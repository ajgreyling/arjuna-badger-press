# RESONANCE — Timeline (canonical chronology)

Binding chronology anchor for the continuity auditor and the author timeline view. This fixes
**ages, the order of backstory events, and elapsed time between acts** so contradictions
(Arin's age drifting, time collapsing or stretching between chapters) are catchable.

The novel is a near-future South African competence-thriller; it deliberately avoids hard
calendar dates. Time is therefore tracked **relative to two anchors**:

- **T0** = the present-day opening of Act I (Arin in the Guardian workshop).
- The **STORY CLOCK** in the rolling story-state counts days/weeks since T0 (and since the
  Preservation Run once it occurs). Each chapter should be placeable on this clock.

> Authoring rule: if a chapter implies a specific elapsed interval, it must agree with the
> STORY CLOCK and with the ages below. When a draft contradicts this file, the continuity
> audit flags it as an **error**.

---

## Fixed ages & facts

| Fact | Value | Source |
|---|---|---|
| Arin Ndlela, present day (Act I onward) | **23** | SEED_STORY.md, STORY_BIBLE.md |
| Arin at the wire-push-car flashback | **~8–10** | PLOT.md (prologue/opening flashback) |
| Themba Ndlela (father) | deceased before T0 (mine accident, Arin's boyhood) | canon |
| Siyanda Nkosi | similar age to Arin | CHARACTERS.md |
| Setting | KwaZulu-Natal / Johannesburg (AugmenTech, University Research Park) / Durban | WORLD.md |

Arin must not be described as a different age within the present-day span — the whole novel's
present (Acts I–IV + epilogue) elapses over **months, not years**; he stays 23.

---

## Backstory (before T0) — fixed order

1. **Deep time.** Vredefort impact; the land as living memory (Prologue — mythic register).
2. **Arin's boyhood (~age 8–10).** The wire push car; Themba teaches load paths and the
   wobble lesson ("wire is good for the frame because it stays; bad for the spring because it
   stays"). The inheritance that becomes Guardian.
3. **Themba's death.** Mine accident in the KwaZulu-Natal region. Arin a boy. The grief that
   the whole engineering project is built around.
4. **Arin grows up, trains, joins AugmenTech.** Becomes an ND systems engineer; begins the
   secret Guardian R&D effort and the SAGE multi-agent system.

---

## Present day — act chronology (relative to T0)

| Phase | Clock | Key events |
|---|---|---|
| **Prologue** | — (timeless) | The land remembers → narrows to the boy. |
| **Act I · Creation** | T0 → ~weeks | Guardian workshop; SAGE/the Court instability; the Joker/Fool enters and stabilises the Court; the Court first speaks coherently. |
| **Act II · Learning** | weeks → ~months | Arin speaks with SAGE regularly; the Court becomes an ensemble; Theo subplot deepens; Guardian field testing; **the Preservation Run** (Act II setpiece — becomes the *second* clock anchor); SAGE learns humanity. |
| **Act III · Exposure** | following weeks | IAOC notices anomalies; corporate pressure (Okonkwo); Priya reads the logs; public leak; Jakobus subplot; the Iron Ridge fault / the Disaster; rescue called off; Arin identifies the survivable path. |
| **Act IV · Descent** | days → hours (compresses hard) | Conscious-rescue climax; underground descent; trapped miners found; surface support failure; Guardian catastrophic failure; the Court chooses sacrifice; Fool's final moment. |
| **Epilogue · Black Box** | after (weeks/months later) | The black box; the new Court simulation with the Joker running; Theo coda. |

**Clock notes for the auditor:**
- Acts I–III unfold over **months**; Act IV compresses to **days then hours** during the
  descent. A chapter implying years have passed in the present day is an error.
- The **Preservation Run** (Act II) is the second anchor: later chapters may be dated "since
  the Preservation Run."
- Events must not reference a consequence before its cause (e.g. the public leak before the
  logs are read; the sacrifice before the descent).

---

## How this file is used

- **Continuity audit** ([`prompts/continuity.md`](../prompts/continuity.md)) checks each
  chapter's stated/implied ages and intervals against this file and the STORY CLOCK.
- **Author timeline view** (`./run.sh viz` → `build/viz/timeline.md`) renders this chronology
  plus the per-chapter clock for scanning.
- When canon changes, update this file first; it loads after `PLOT.md` in the canon stack so
  it overrides looser chronology in the earlier prose-oriented bibles. (`NAMES.md` and
  `CANON_CHOICES.md` remain last as the highest-priority locks.)
