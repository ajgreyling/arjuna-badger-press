# Feedback & per-book reader-response — design

*How readers tell us things on a static (GitHub Pages) site, and how that funnel relates to the
Honey Badger Bounty. Internal planning doc; not published to the site.*

## The constraint

arjunabadger.press is a **static site** (GitHub Pages, no backend). We cannot run a server-side
inbox or store submissions ourselves. So every "send us something" path resolves to one of two
things:

1. **An embedded/linked form** hosted by a third party (Google Forms or Tally) whose responses land
   in a sheet/dashboard the press reads. *Chosen primary channel.*
2. **A `mailto:` link** — opens the visitor's mail client, pre-addressed and pre-subjected. *Used as
   the always-works fallback so no button is ever a dead end.*

Public address: **info@arjunabadger.press**. Private inbox feedback is forwarded to:
**j@arjunabadger.press** (the mailto fallback targets j@ directly).

## One funnel (decided)

A single entry point — **"Tell us something"** — that branches into two intents:

- **General feedback** — praise, a typo, "I loved X", a thought. Low-stakes, unpaid. Goes to the
  feedback form / j@.
- **Report a find (paid)** — a confirmed factual / cultural / continuity issue, eligible for the
  **Honey Badger Bounty**. Routed to the *bounty* surface, which already exists (`BOUNTY.md`,
  gated until 25 June 2026). The feedback page links across to it rather than duplicating its rules.

Rationale: fewer entry points for the reader; one mental model ("I want to tell the press
something"); the paid/serious path stays clearly distinct so we don't drown real bounty finds in
praise, and so the bounty's anti-scam framing isn't diluted.

```
                 ┌─────────────────────────────┐
  reader  ─────► │  /feedback.html  "Tell us"   │
                 └──────────────┬───────────────┘
                                │
              ┌─────────────────┴───────────────────┐
              ▼                                      ▼
   General feedback / typo / praise        Confirmed factual/continuity issue
   → FEEDBACK_FORM_URL (or mailto j@)       → /bounty.html  (paid, gated, its own rules)
```

## Configuration (mirrors the bounty's form pattern)

Three env-driven constants in `site/build.py`, all with safe fallbacks:

| Constant | Default | Effect when empty |
|---|---|---|
| `PRIVATE_EMAIL` | `j@arjunabadger.press` | — (always set) |
| `FEEDBACK_FORM_URL` (`ABP_FEEDBACK_FORM_URL`) | `""` | all feedback buttons fall back to a pre-filled `mailto:j@` |
| `FEEDBACK_FORM_BOOK_PARAM` (`ABP_FEEDBACK_BOOK_PARAM`) | `entry.book` | the query param used to pre-fill the book field in the Google Form |

When `FEEDBACK_FORM_URL` is set, buttons point at the form; per-book buttons append
`?<book_param>=<Book Title>` so the form opens with the book pre-selected. Until then they open
`mailto:j@arjunabadger.press?subject=Feedback: <Book Title>` so the channel works **today** with zero
external setup.

### Wiring a Google Form (when ready)
1. Create a Form with a short-answer/dropdown field "Which book?" and a long-answer "Your feedback".
2. Pre-fill link → copy the field's `entry.NNN` id; set `FEEDBACK_FORM_BOOK_PARAM=entry.NNN`.
3. Paste the form's base URL into `ABP_FEEDBACK_FORM_URL` (or the constant) and rebuild.
4. Responses collect in the linked Google Sheet — that is the "read feedback" dashboard.

## What gets built now

- A `feedback_href(book_title=None)` helper (form-or-mailto, book-tagged).
- A standalone **`/feedback.html`** page (the funnel: general vs bounty), in the house letter style.
- A **per-book feedback button** on every `book/<id>.html` page, pre-tagged with that book's title.
- A **nav link** ("Feedback") in the About dropdown.
- No backend, no new dependency. Bounty left exactly as-is (gated).

## Per-book feedback — why pre-tagging matters

A reader on *The Calendar of Stone* who spots something should not have to tell us *which* book.
The button on that page carries the title, so:

- **mailto fallback:** `subject=Feedback: The Calendar of Stone` — arrives pre-labelled in j@.
- **form mode:** `?entry.book=The Calendar of Stone` — the "Which book?" field is pre-filled.

This makes per-book response effectively free once the general funnel exists: it is the same funnel
with the book carried in.

## Future (not now)

- Per-book *structured* feedback (ratings, "favourite chapter") — only worth it if volume justifies;
  the Google Sheet can hold extra columns when needed.
- A public "what readers said" wall — only with explicit opt-in consent on the form; privacy first.
