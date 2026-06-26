# Narrator + Audition forms — setup (Google Forms)

Two separate Google Forms back the two pages:

- **narrators.html** → "Become a narrator" (the profile / waitlist intake)
- **audition.html** → "Narrator auditions" (the audition-note intake)

The pages link OUT to these forms (a button), so they work on every device — no fragile
mailto, no broken on-page POST. You create the forms; paste the two share URLs back and the
build wires them in.

---

## 1. Narrator profile form

Create a form titled **"Arjuna Audio — Narrator profile"**. Add these questions, in order.
(These mirror narrators.html exactly. Mark *Required* where noted.)

| # | Question | Type | Required |
|---|----------|------|----------|
| 1 | Name | Short answer | ✅ |
| 2 | Email | Short answer (Response validation → Email) | ✅ |
| 3 | Country | Short answer | ✅ |
| 4 | Languages you can narrate | Short answer (help text: "English, isiZulu, Afrikaans, Swahili…") | ✅ |
| 5 | Accent / voice notes | Paragraph (help text: "South African English, warm baritone, character voices…") | — |
| 6 | Preferred genres | Paragraph (help text: "Fiction, non-fiction, children's, thriller, memoir…") | — |
| 7 | Commercial preference | Multiple choice — options below | ✅ |
| 8 | Voice sample link | Short answer (help text: "Upload a sample anywhere you control, then paste the link") | ✅ |
| 9 | Anything we should know | Paragraph (help text: "Home studio setup, rates, availability, books you love…") | — |

**Q7 "Commercial preference" options (exactly these three):**
- Cash upfront plus 5% royalty floor
- Reduced upfront plus higher royalty
- Royalty-only for the right book

---

## 2. Audition note form

Create a form titled **"Arjuna Audio — Audition note"**. Add these questions, in order.
(These mirror audition.html exactly.)

| # | Question | Type | Required |
|---|----------|------|----------|
| 1 | Name | Short answer | ✅ |
| 2 | Email | Short answer (Response validation → Email) | ✅ |
| 3 | Country | Short answer | ✅ |
| 4 | Device | Short answer (help text: "MacBook Air, iPhone 13, Samsung A-series, USB mic…") | — |
| 5 | Recording space | Short answer (help text: "Bedroom, closet, parked car, quiet garden room…") | — |
| 6 | Voice sample link | Short answer (help text: "https://…") | — |
| 7 | What gear or room problem do you have | Paragraph (help text: "Echo, traffic, fan noise, plosives, low volume, hiss…") | — |

---

## 3. Get the share URL for each form

For each form: **Send → 🔗 link tab → copy.** You'll get a link like
`https://forms.gle/XXXXXXXX` (or the long `https://docs.google.com/forms/d/e/…/viewform`).
Either form of the URL is fine — paste it as-is.

> Tip: in form **Settings → Responses**, turn on "Collect email addresses" off (the form already
> asks for email) and decide whether to email yourself on each response (Responses tab →
> ⋮ → "Get email notifications for new responses").

---

## 4. Hand them back

Reply with the two URLs, e.g.:

```
NARRATOR_FORM_URL = https://forms.gle/aaaaaaa
AUDITION_FORM_URL = https://forms.gle/bbbbbbb
```

I set `ABP_NARRATOR_FORM_URL` + `ABP_AUDITION_FORM_URL`, rebuild, and deploy. The pages then
show an "Open the form →" button instead of the mailto fallback.
