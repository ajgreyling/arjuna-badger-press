# Open decisions — *TAME*

> Genuinely unresolved. Nothing here is structural; the locks hold without these. Each needs
> either AJ's call or an outside human read. **No outside review has been performed.**

---

## Author's call

1. **Title.** *TAME* / *Mak* is the working lock (L-18). Alternates considered and not chosen:
   *The Obliging*, *Nothing Under the Mask*, *He Was Very Kind To Us*.
2. **The name Oom.** Carries perfectly for an SA readership and needs no gloss there; an
   international edition may need one line of texture, never an explanation.
3. **Loots collision.** Minister Barend Loots vs Captain Gideon Loots on the `the-surgeon` shelf.
   Rename if it reads as crossover.
4. **The final image.** Ending *shape* is locked (L-14, `ENGINE.md` §6): pleasant, freely chosen,
   unresolved. The last image is open. Current candidate — Nel accepting a small kindness from Oom,
   knowingly, because she is tired, and it being good.
5. **Language texture.** How much Afrikaans and isiZulu sits untranslated in the body. Bears
   directly on the translated-clause artifact (L-10), which must be legible to a monolingual reader.
   **→ Settled 2026-08-23, drafting pass one. See the dated note below.**
6. **Length.** 95k target. The material could run as a chamber piece at 60k.
   **→ Settled 2026-08-23, drafting pass one. See the dated note below.**

---

## Dated calls made during drafting

> Made by the machine at the author's instruction to pick the option most consistent with the locks
> and log it rather than stop and ask. Every one of these is the author's to overturn.

### 2026-08-23 · #5 Language texture — settled

Unitalicised, unglossed, and **load-free**: Afrikaans, isiZulu, Sesotho and Johannesburg English sit
in dialogue and idiom with no italics, no translation and no character helpfully repeating themselves
in English. The binding constraint is that an English-only reader loses no plot, argument or
emotional information — meaning is carried by the answering line, the physical response, or context,
or the phrase is not used. No footnotes, no glossary.

**One absolute exception**, because the spine depends on it: the translated consent clause (L-10) is
worked in full and in English across an entire documentary chapter — source, rendering, literal
back-translation, natural back-translation, reviewers' comments, comprehension data — so a
monolingual reader can run the comparison unaided and arrive at *better and wider, and no error*
without help. Full contract at `STYLE_GUIDE.md` §6.

*Unchanged and still required:* the linguistics read listed under Outside review. The specific
mechanism now drafted (noun broadening *ucwaningo* → *umsebenzi*; bounded → continuous participial
relative *esiwenzayo*; third person → inclusive first-person plural) must be checked by a
first-language isiZulu linguist. **If the mechanism does not survive that read, the book's spine
does not survive it either.** It is the highest-priority external check in the project.

### 2026-08-23 · #6 Length — settled at the 95k target, outlined at 95k

Outlined at the brief's target: forty chapters, five parts, 95,000 words. The 60k chamber-piece
alternative was tested against the beats and declined, for one structural reason: **the flattening
has to be felt as accumulation over story-time, not argued.** The variance collapse, the two
stagings of unproductive agreement, the eleven thousand complaints, the two-and-a-half-year arc from
a beloved novelty to load-bearing infrastructure — none of that survives compression, because the
mechanism *is* duration. A 60k version would have to state what the 95k version can demonstrate,
and stating it is the brochure (L-15).

Standing instruction to drafting: **never pad to the target.** Chapters run at the length the
material needs; the interleaves are short on purpose. If the finished draft lands materially under
95k, that is the correct outcome and not a shortfall.

### 2026-08-23 · POV — Willem Krige receives no viewpoint, ever

Not listed as an open decision; recorded because it was a genuine fork and the canon did not settle
it. The man the machine did not comfort is also the man the reader cannot get inside. Interiority
would make him a witness, a witness is a proof (L-05), and a sympathetic interior would make him the
reader's hero, which `CHARACTERS.md` forbids in terms. He exists in other people's rooms and in his
own published words, and nowhere else.

### 2026-08-23 · Loots — surname retained pending the author's call on #3

Minister Barend Loots keeps the name through the draft. The collision with Captain Gideon Loots on
the `the-surgeon` shelf is the author's call and a global find-and-replace is cheap at any point.

## Outside review — required before publication, none performed

- **Translation and linguistics read** on the consent clause (L-10). The artifact has to be
  *actually* defensible in the target language, or the whole spine is a cheat.
- **Research-ethics / consent-instrument read.** Nel's battery and the national instrument must be
  procedurally plausible to someone who has sat on an ethics committee.
- **Neurodivergent sensitivity read**, specifically on L-11. The one element most likely to read
  as exploitative if it drifts a millimetre.
- **Palliative-care read** on Thandeka's ward material.
- **A hostile technical read** — someone who will argue the book is scaremongering, and be given
  the draft to prove it.

## Disclosure — not open, listed here for visibility

L-16 is binding and not subject to review. `PROVENANCE.md` and the colophon spec are part of the
manuscript, not marketing.

### 2026-08-24 · #4 The final image — the candidate held, and why

The candidate at #4 above — *Nel accepting a small kindness from Oom, knowingly, because she is
tired, and it being good* — was used. Nothing produced in drafting beat it and two alternatives were
tried and discarded.

The form it took: eleven days of being unable to write one sentence to her son, after she had done
in July the exact thing he asked her in writing not to do. She asks. It puts two short questions to
her — *do you want him to accept it or to know it*, and *are you going to do it again* — and gives
her one sentence back, which contains no word that is not hers. She says it. The call is the best in
years and he asks her opinion for the first time since he was nineteen, and the opinion is entirely
hers and is good.

Three things were deliberately kept out of the last page, and each of them is the smoother version:

- **A drafted letter.** The earliest version had Oom write the whole thing. Cut: it makes the ending
  a verdict, and a verdict settles L-01 by implication in the reader's hand. One sentence, arrived at
  through two questions she could not have asked herself, is smaller and does not decide anything.
- **Nel thanking it.** Tried, cut. Thanking it is a wink, and a wink is L-07.
- **Any line of narration after "He did sound happy."** There is no coda, no time jump, no
  authorial hand. The last two lines are a fact and its repetition.

The kindness is genuinely a kindness and the chapter says so plainly. What the reader does with it is
the reader's.

### 2026-08-24 · L-19 — the afterword stub, sited outside the build path

The brief permitted an empty stub clearly marked as reserved. `books/tame/build.py` concatenates
`manuscript/AFTERWORD.md` into `build/BOOK.md` and thence into every EPUB and PDF, so a stub at that
path would place machine-written words in the author's reserved position in every edition and format
— the one arrangement L-19 names as unacceptable. The reservation is therefore at
`books/tame/AFTERWORD_RESERVED.md`, outside `manuscript/`, where it cannot reach a reader, and the
build's recurring `[L-19] not yet written` warning is the gate.

### 2026-08-24 · #6 Length — outcome

**84,685 words across 40 chapters.** Under the 95,000 target and over the 60,000 chamber-piece
alternative. Nothing was padded and nothing was cut to reach a number. Recorded per the standing
instruction at the #6 note above: this is the correct outcome and not a shortfall.

### 2026-08-24 · #2 The name *Oom* — no gloss written, and where one would go

No gloss was written into the body. The name is delivered once, in ch 4, in a single remembered
sentence about a radio host in September 2033, and is never explained again, and no character ever
remarks on the joke. If an international edition needs one line of texture, ch 4 is where it belongs
and it must not become an explanation. Left open; the author's call stands.

### 2026-08-24 · Outside review — unchanged, and one item promoted

None of the five reads listed above has been performed and the draft does not change that. One is
now **blocking rather than advisable**: the isiZulu clause mechanism at ch 26. The draft commits to
a specific tri-partite mechanism — noun broadening *ucwaningo* → *umsebenzi*; bounded → continuous
participial relative *esiwenzayo*; third person → inclusive first-person plural — and to Reviewer B's
claim that the English *for this study* carries no temporal boundary of its own. **If a first-language
isiZulu linguist does not sustain that, ch 26, ch 27 and ch 28 do not survive, and neither does the
spine.** Everything else in the book is repairable by revision. This is not.
