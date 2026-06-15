<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="brand/assets/logo-master.png">
    <img src="brand/assets/logo-on-light.png" width="340" alt="Arjuna Badger Press">
  </picture>
</p>

<h1 align="center">Arjuna Badger Press — the library</h1>

> A free, open reading library. Every book is free to **download** as EPUB or PDF, or to **read
> online**. No paywall, no account, no catch.
>
> *The archer's eye. The badger's nerve.* — [arjunabadger.press](https://arjunabadger.press)

**EPUB** is best for e-readers and phones · **PDF** is the print-faithful 6×9 edition · **Read**
opens the full manuscript in your browser. *(On GitHub, open a file then use the **Download / raw**
button to save it.)*

Each book has **one canonical EPUB and one PDF** under `books/<title>/build/export/` (or
`…/export/` for companions). The live site at [arjunabadger.press](https://arjunabadger.press) copies
those files at build time — run `python3 site/build.py` to refresh `site/public/`; do not commit that
folder.

> **For engineers & CTOs** — how this library is made: the AI pipeline, the StoryGraph geospatial-temporal continuity graph, NovelBench, the de-LLM loop, and the human-in-the-loop guardrails & gates → **[The technology](docs/TECHNOLOGY.md)**.

> **For authors & editors** — why the press is not just for beginners: dump your manuscripts and notes, answer ~20 wizard questions, click Go, come back to a proofread-ready book → **[The workshop](docs/FOR_AUTHORS.md)**.

> **For writers** — free degree-level creative-writing craft (structure, character, sentence, anti-patterns, machine-tell audit) mined from finishing this catalogue → **[Craft Library](docs/craft/README.md)** · read online at [arjunabadger.press/craft/](https://arjunabadger.press/craft/index.html).

## The catalogue

| Book | What it is — and who it's for | EPUB | PDF | Read |
|---|---|---|---|---|
| <img src="covers/resonance.jpg" width="92" alt="RESONANCE cover"><br>**RESONANCE** <br><sub>The African Gold Trilogy · I</sub> | A neurodiverse engineer builds a mind that proves it is a person — and must decide what he owes the thing he made. <br>*For readers of Andy Weir, Michael Crichton & Dan Brown.* | [EPUB](books/resonance/build/export/RESONANCE.epub) | [PDF](books/resonance/build/export/RESONANCE.pdf) | [Read](books/resonance/build/BOOK.md) |
| <img src="covers/revelation.jpg" width="92" alt="REVELATION cover"><br>**REVELATION** <br><sub>The African Gold Trilogy · II</sub> | A linguist uncovers who really gets to mediate a destabilising truth — and what it costs to be the one who tells it. <br>*For readers of Dan Brown, James Rollins & Steve Berry.* | [EPUB](books/revelation/build/export/REVELATION.epub) | [PDF](books/revelation/build/export/REVELATION.pdf) | [Read](books/revelation/build/BOOK.md) |
| <img src="covers/relic.jpg" width="92" alt="RELIC cover"><br>**RELIC** <br><sub>The African Gold Trilogy · III</sub> | An engineer reads an ancient machine and must decide who may switch it on — the cinematic capstone of the trilogy. <br>*For readers of Michael Crichton, Clive Cussler & Wilbur Smith.* | [EPUB](books/relic/build/export/RELIC.epub) | [PDF](books/relic/build/export/RELIC.pdf) | [Read](books/relic/build/BOOK.md) |
| <img src="covers/book1-africa.jpg" width="92" alt="The Calendar of Stone cover"><br>**The Calendar of Stone** <br><sub>History Before Time · I</sub> | At Adam's Calendar in South Africa — a ring of stone older than the pyramids — the case for a forgotten African deep past stops being a fringe theory. <br>*For readers of Graham Hancock & Dan Brown.* | [EPUB](books/history-before-time/books/book1-africa/build/export/The%20Calendar%20of%20Stone.epub) | [PDF](books/history-before-time/books/book1-africa/build/export/The%20Calendar%20of%20Stone.pdf) | [Read](books/history-before-time/books/book1-africa/build/BOOK.md) |
| <img src="covers/book2-india.jpg" width="92" alt="The Indian One cover"><br>**The Indian One** <br><sub>History Before Time · II</sub> | The Kailasa temple at Ellora — carved top-down from a single mountain — and the shore temples of Mahabalipuram: India's impossible stone. <br>*For readers of Graham Hancock & James Rollins.* | [EPUB](books/history-before-time/books/book2-india/build/export/The%20Indian%20One.epub) | [PDF](books/history-before-time/books/book2-india/build/export/The%20Indian%20One.pdf) | [Read](books/history-before-time/books/book2-india/build/BOOK.md) |
| <img src="covers/book3-india-deccan.jpg" width="92" alt="The Temple in the Rock cover"><br>**The Temple in the Rock — Deccan** <br><sub>History Before Time · III</sub> | Deeper into the Deccan's rock-cut wonders — how Ellora and Kailasa were really hewn from living stone, and by whom. <br>*For readers of Graham Hancock & Douglas Preston.* | [EPUB](books/history-before-time/books/book3-india-deccan/build/export/The%20Temple%20in%20the%20Rock.epub) | [PDF](books/history-before-time/books/book3-india-deccan/build/export/The%20Temple%20in%20the%20Rock.pdf) | [Read](books/history-before-time/books/book3-india-deccan/build/BOOK.md) |
| <img src="covers/book4-india-tamil.jpg" width="92" alt="The Shore That Remembers cover"><br>**The Shore That Remembers** <br><sub>History Before Time · IV</sub> | Mahabalipuram and sunken Poompuhar — a Tamil coast that still remembers the shoreline the sea took. <br>*For readers of Graham Hancock & Clive Cussler.* | [EPUB](books/history-before-time/books/book4-india-tamil/build/export/The%20Shore%20That%20Remembers.epub) | [PDF](books/history-before-time/books/book4-india-tamil/build/export/The%20Shore%20That%20Remembers.pdf) | [Read](books/history-before-time/books/book4-india-tamil/build/BOOK.md) |
| <img src="covers/book5-egypt.jpg" width="92" alt="The Engineer of the Gods cover"><br>**The Engineer of the Gods** <br><sub>History Before Time · V</sub> | Giza and the Great Pyramid — the engineering mind that could have raised them, read from the stone itself. <br>*For readers of Graham Hancock & Michael Crichton.* | [EPUB](books/history-before-time/books/book5-egypt/build/export/The%20Engineer%20of%20the%20Gods.epub) | [PDF](books/history-before-time/books/book5-egypt/build/export/The%20Engineer%20of%20the%20Gods.pdf) | [Read](books/history-before-time/books/book5-egypt/build/BOOK.md) |
| <img src="covers/australia-outback.jpg" width="92" alt="The Songlines of Stone cover"><br>**The Songlines of Stone** <br><sub>History Before Time · VI</sub> | Murujuga's million rock engravings and the songlines of Aboriginal Australia — the oldest continuous human memory on Earth. <br>*For readers of Graham Hancock & Bruce Chatwin.* | [EPUB](books/history-before-time/books/australia-outback/build/export/The%20Songlines%20of%20Stone.epub) | [PDF](books/history-before-time/books/australia-outback/build/export/The%20Songlines%20of%20Stone.pdf) | [Read](books/history-before-time/books/australia-outback/build/BOOK.md) |
| <img src="covers/project-stargate.jpg" width="92" alt="The Men Who Opened the Door cover"><br>**The Men Who Opened the Door** <br><sub>History Before Time · VII</sub> | The true story of the CIA's Project Stargate — the men who tried to weaponise the mind, and what they found at the edge of it. <br>*For readers of Annie Jacobsen & Jon Ronson.* | [EPUB](books/history-before-time/books/project-stargate/build/export/The%20Men%20Who%20Opened%20the%20Door.epub) | [PDF](books/history-before-time/books/project-stargate/build/export/The%20Men%20Who%20Opened%20the%20Door.pdf) | [Read](books/history-before-time/books/project-stargate/build/BOOK.md) |
| <img src="covers/jakobus-silver-thread.jpg" width="92" alt="The Silver Thread cover"><br>**The Silver Thread** <br><sub>A Jakobus Swart story</sub> | Before the saga, the soldier — the years between the Border War and the man we later meet, and how an unkillable gentleness was forged. <br>*For readers of Deon Meyer, John le Carré & Wilbur Smith.* | [EPUB](books/history-before-time/books/jakobus-silver-thread/build/export/The%20Silver%20Thread.epub) | [PDF](books/history-before-time/books/jakobus-silver-thread/build/export/The%20Silver%20Thread.pdf) | [Read](books/history-before-time/books/jakobus-silver-thread/build/BOOK.md) |
| <img src="covers/jakobus-the-recitation.jpg" width="92" alt="The Recitation cover"><br>**The Recitation** <br><sub>A Jakobus Swart story</sub> | Jakobus among the San — a story of the Kalahari, of debt and grace, and of the oldest way there is of telling. <br>*For readers of Wilbur Smith & Laurens van der Post.* | [EPUB](books/history-before-time/books/jakobus-the-recitation/build/export/The%20Recitation.epub) | [PDF](books/history-before-time/books/jakobus-the-recitation/build/export/The%20Recitation.pdf) | [Read](books/history-before-time/books/jakobus-the-recitation/build/BOOK.md) |
| <img src="covers/the-jakobus-file.svg" width="92" alt="A Man They All Read Wrong cover"><br>**A Man They All Read Wrong** <br><sub>The Jakobus Swart File</sub> | After his death, the man assembled from everyone who knew him — and everyone who only thought they did. Each reads a different Jakobus Swart; each finds out they read him wrong. <br>*For readers of Max Brooks (*World War Z*) & John le Carré.* | [EPUB](books/history-before-time/books/the-jakobus-file/build/export/A%20Man%20They%20All%20Read%20Wrong%20%E2%80%94%20The%20Jakobus%20Swart%20File.epub) | — | [Read](books/history-before-time/books/the-jakobus-file/build/BOOK.md) |
| <img src="covers/crop-circles.svg" width="92" alt="The Field of Doors cover"><br>**The Field of Doors** <br><sub>The Why Files · I</sub> | The official story played straight — the Wessex chalk, the one genuinely-unresolved hole, and the maybe left open. <br>*For readers of Graham Hancock & Jon Ronson.* | [EPUB](books/history-before-time/books/crop-circles/build/export/The%20Field%20of%20Doors.epub) | [PDF](books/history-before-time/books/crop-circles/build/export/The%20Field%20of%20Doors.pdf) | [Read](books/history-before-time/books/crop-circles/build/BOOK.md) |
| <img src="covers/unheard-japan.svg" width="92" alt="The Way That Was Invented cover"><br>**The Way That Was Invented** <br><sub>The Unheard · Japan</sub> | Japan — Ainu, burakumin, and the living hands the brochure paints over. Jakobus on the road, never the lead. <br>*For readers of Kazuo Ishiguro & Haruki Murakami.* | [EPUB](books/the-unheard/books/japan-ainu/build/export/The%20Way%20That%20Was%20Invented.epub) | [PDF](books/the-unheard/books/japan-ainu/build/export/The%20Unheard%20%E2%80%94%20Japan.pdf) | [Read](books/the-unheard/books/japan-ainu/build/BOOK.md) |
| <img src="covers/unheard-mongolia.jpg" width="92" alt="The Felt and the Sky cover"><br>**The Felt and the Sky** <br><sub>The Unheard · Mongolia</sub> | A herder's daughter sent back as the friendly face of the survey that will fence her father's pasture — the crew who came for Genghis's empty land learns the steppe is the most precisely known ground on earth. <br>*For readers of Bruce Chatwin & Wilbur Smith.* | [EPUB](books/the-unheard/books/mongolia-steppe/build/export/The%20Felt%20and%20the%20Sky.epub) | [PDF](books/the-unheard/books/mongolia-steppe/build/export/The%20Felt%20and%20the%20Sky.pdf) | [Read](books/the-unheard/books/mongolia-steppe/build/BOOK.md) |
| <img src="covers/sheltering-desert.jpg" width="92" alt="The Sheltering Desert cover"><br>**The Sheltering Desert** <br><sub>A standalone novel · true story</sub> | In May 1940 two German geologists drove into the Namib rather than be interned — and survived two and a half years by real bushcraft against a desert that did not care whether they lived. <br>*For readers of Laurens van der Post & Wilbur Smith.* | [EPUB](books/the-sheltering-desert/build/export/The%20Sheltering%20Desert.epub) | [PDF](books/the-sheltering-desert/build/export/The%20Sheltering%20Desert.pdf) | [Read](books/the-sheltering-desert/build/BOOK.md) |
| <img src="covers/the-loneliest.svg" width="92" alt="The Loneliest People in the World cover"><br>**The Loneliest People in the World** <br><sub>A standalone novella</sub> | A boy whose one gift is reading people is sent to get close to the daughter of a feared man — and instead recognises himself. Two people truly seen, once, and never allowed to know what it meant. <br>*For readers of Kazuo Ishiguro & Patricia Highsmith.* | [EPUB](books/the-loneliest/build/export/The%20Loneliest%20People%20in%20the%20World.epub) | [PDF](books/the-loneliest/build/export/The%20Loneliest%20People%20in%20the%20World.pdf) | [Read](books/the-loneliest/build/BOOK.md) |
| <img src="covers/the-song-of-the-self.svg" width="92" alt="The Song of the Self cover"><br>**The Song of the Self** <br><sub>A companion</sub> | The Bhagavad Gita's quiet question — *who acts, and for whom?* — carried into the History Before Time world. <br>*For readers of Hermann Hesse (*Siddhartha*) & Paulo Coelho.* | [EPUB](books/history-before-time/companions/the-song-of-the-self/export/The%20Song%20of%20the%20Self.epub) | [PDF](books/history-before-time/companions/the-song-of-the-self/export/The%20Song%20of%20the%20Self.pdf) | [Read](https://arjunabadger.press/read/the-song-of-the-self.html) |
| <img src="covers/wrath-of-achilles.jpg" width="92" alt="The Wrath of Achilles cover"><br>**The Wrath of Achilles** <br><sub>Homer's Iliad · companion</sub> | The whole *Iliad* — its story and what each of its twenty-four books asks of a human life — told plainly for every reader who never cracked a Classics syllabus. <br>*For readers of Homer, Madeline Miller & Mary Renault.* | [EPUB](books/history-before-time/companions/the-wrath-of-achilles/export/The%20Wrath%20of%20Achilles.epub) | [PDF](books/history-before-time/companions/the-wrath-of-achilles/export/The%20Wrath%20of%20Achilles.pdf) | [Read](https://arjunabadger.press/read/wrath-of-achilles.html) |

## The other half — a sister proof

Part of this library is a unified theory turned into people and places. The theory is the work of a
man this library names only as *the author of the unified theory*; the independent, executable check
of it is mine. The theory: [the420code.org](https://the420code.org). The proof:
[github.com/ajgreyling/the420code-proof](https://github.com/ajgreyling/the420code-proof).

## Accuracy + both sides

Every book is fact-checked against live sources and tells contested stories from **both sides** —
Weir / Crichton / Brown-grade historical and factual accuracy, *core*, not a nice-to-have.

## Rights

All works © Andries J. Greyling. **Free to read and download for personal use; all rights reserved.**
Not licensed for redistribution, resale, adaptation, audio production, or machine-learning training
without written permission. See [`LICENSE`](LICENSE).

---

<p align="center">
  <img src="brand/assets/house-of-greyling-crest.png" width="260" alt="The House of Greyling crest — a honey badger between a griffin and a wolf, beneath a sword in sun">
  <br><sub><em>House of Greyling · Per Ardua Ad Magnum</em></sub>
</p>
