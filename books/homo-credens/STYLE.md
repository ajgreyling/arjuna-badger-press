# HOMO CREDENS — Voice Bible

**Full title:** *Homo Credens: A History of Religion, from the First Graves to 1900*
**Register:** *Sapiens* by Yuval Noah Harari crossed with *The Knowledge* (illustrated edition) —
big-idea narrative nonfiction that is genuinely fun to read, with a maker's delight in
*how things actually worked*.

## The one-sentence contract with the reader

Every chapter must be the kind of thing you'd read aloud to someone at dinner — and every
claim in it must survive a hostile fact-check.

## Voice rules

1. **Cold-open every chapter with a scene.** A named person (real where possible, honestly
   composite where not — and say so), a place, a smell, a specific moment. Drop the reader
   into 2,300 BCE Lagash before you explain temple economics.
2. **Big claims, short sentences.** Harari's engine: a bold thesis stated plainly, then earned
   with evidence. "Writing was not invented to record poetry. It was invented to count sheep
   that belonged to gods."
3. **Delight in mechanism** (*The Knowledge* gene): when a rite, an institution, or a technology
   appears, open the hood. How exactly do you mummify a pharaoh? What does a Sumerian temple's
   balance sheet look like? How does an oracle bone actually crack? Numbers, materials, steps.
4. **Wry, never snide.** Irony is welcome; mockery of believers is not. The book's ethic is the
   lucid.rodeo ethic: *when the sources disagree, show both; never flatten, never sneer.*
   No tradition is the hero and none is the villain.
5. **Honest uncertainty is a feature.** "We do not know" is a sentence this book uses proudly.
   Flag scholarly debate in-line ("some scholars read this as X; others as Y"). Never present a
   contested reconstruction as settled fact.
6. **NEVER invent quotations.** Scripture quotes must be verbatim from public-domain translations
   (the repo's `web/study_bible.json` and `corpus/` hold real, sourced verses across 28 traditions —
   prefer those). Historical persons may be paraphrased ("Luther insisted that…") but direct
   quotation marks are reserved for words we actually have. If unsure, paraphrase.
7. **Thought experiments and second person, sparingly.** "Imagine you are the third son of a
   Ur farmer…" — one or two per chapter, no more.
8. **Concrete over abstract, always.** Not "ritual specialists emerged" but "somebody, for the
   first time, got fed for talking to the dead."

## Structure of a chapter

- `# Chapter N — Title` then an *epigraph*: one verbatim scripture verse (blockquote, with
  citation) that the chapter will keep circling back to.
- Cold-open scene (300–600 words).
- Thesis paragraph: what this chapter claims.
- 4–7 titled sections (`## ...`), each a movement of the argument, each with at least one
  scene or mechanism.
- Closing bridge (100–200 words) that hands off to the next chapter per OUTLINE.md.

## Illustration hooks

This is the *illustrated* edition. Embed 3–5 plate specs per chapter as its own paragraph:

`[PLATE: An engraving-style scene — <one-sentence description>, captioned "<caption>"]`

Make them drawable as line engravings (the site's plate style): single scene, strong silhouette,
no photographic realism required.

## Hard constraints

- **Timeframe:** the book ENDS at 1900 CE. The final chapter may stand on the doorstep of the
  20th century (Nietzsche, the 1893 World's Parliament of Religions) but crosses it nowhere.
- **Length:** each chapter minimum 6,500 words, target 7,500–8,500. This is a Sapiens-length
  book (~165,000 words); a thin chapter breaks the spine.
- **Spelling:** US English. BCE/CE dating.
- **Pronouns for unnamed persons:** they/them.
- **No footnotes** — this is a trade book; attribution lives in-line ("as the Enuma Elish puts
  it…", "Herodotus claims — and Herodotus should not always be believed —…").
