# Buabantu — the language of the people

*OpenRouter, but for register and dialect. African and colloquial language, decoded and spoken back in the voice people actually use.*

---

## The problem this solves

There is a word in Afrikaans — *poes* — that is simultaneously the gravest insult in the language and one of the warmest things one friend can say to another. Aimed at a stranger it ends the conversation. Offered to someone you love it is celebration, blessing, pure affection.

Same four letters. Opposite meaning. Determined entirely by **who is speaking, to whom, from what standing**.

No dictionary entry captures this. No content filter trained on English letter-patterns gets it right. A blanket ban fails the language. Pattern-matching the word fails the people.

This is not an edge case — it is the daily reality of most African languages, where register, relationship, code-switching, and dialect carry more meaning than the words themselves. A machine that cannot read that gap will get the warmth wrong every time: blocking the blessing, passing the insult.

Buabantu exists to read the gap.

**[Read the full *poes* entry →](safari/poes.html)** — the word that made the problem undeniable, and where the *jou lucky poes* rule that governs this engine is explained in full.

---

## What Buabantu does

Buabantu is a register-aware language router for African and colloquial language. You send text and a target — a language, a register, an audience — and get the meaning back in the language people actually speak, not textbook flatness.

It runs in both directions:

**Outbound — corporate → street.** Turn official communication into the register a community actually uses. Marketing, campaigns, support replies, public notices — the message lands because it was written from inside the language, not translated down into it.

**Inbound — street → meaning.** The harder and more valuable half. Decode what people say — slang, code-switching, dialect, the *jou lucky poes* register — into meaning and sentiment a system can act on. This is the direction where the gap kills, and where Buabantu was built to close it.

---

## The VAS bundle — never a dumb pipe

Raw routing is a commodity. Anyone can call OpenRouter. The value in Buabantu is the layer on top — applied to every byte, in both directions:

| Layer | What it does |
|---|---|
| **Corpus-first correction** | Human fixes (weight 100) overlay any engine's raw output — the proprietary ground truth from the SA urban corpus |
| **Register dial** | temp 0 (formal) → 1 (street), tuned to the audience |
| **Faithfulness rules** | Proper names preserved, no translator's notes, per-language-family length-ratio checks |
| **Police + Judge guardrail** | Two-layer safety — the *jou lucky poes* rule: judge by relationship and intent, never letters alone |

The guardrail is the core invention. A word judged by letters alone is a blunt instrument. The same word judged by *who says it, to whom, and why* is a precision tool. Buabantu's moderation judge runs the latter — which is why it can protect the language instead of flattening it.

---

## Why this press has this product

Arjuna Badger Press publishes across eight languages with a parallel translation engine. Every translated book, every register-switched line, every correction a reader suggests — all of it runs through this engine. The press is just one consumer of the API. The product was promoted out of the press's internal tooling because the problem is bigger than one publisher.

The *poes* glossary entry is the proof of concept. A page that a sane person would never put next to their CV — except that it documents, in precise linguistic and cultural detail, exactly the problem the software solves. The word that a foreign-built guardrail gets catastrophically wrong is the word that taught this engine to read intent. That is not a coincidence. It is the thesis.

---

## Status

**Closed beta** — ABP account required. If you are a developer, publisher, or company working with African or colloquial South African language and want early access, write to [info@arjunabadger.press](mailto:info@arjunabadger.press).

**[Full technical specification →](safari/tech-buabantu.html)**

---

*Buabantu — the language of the people. Not the textbook. Not the filter. The actual thing.*
