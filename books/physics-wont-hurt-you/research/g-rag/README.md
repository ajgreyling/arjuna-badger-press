# G corpus RAG

This research tool builds a local, provenance-aware vector index for the final chapter of
*Physics Won't Hurt You*. It combines:

- G / Studio G's current English exhibition at [the420code.org](https://the420code.org): all 43
  Artist's Proofs and all 26 published English collected works, notebooks, records, and references;
- the existing manuscript chapters in `build/chapters/`;
- AJ Greyling's independent executable verifier as a separate evidentiary source during drafting.

The downloaded corpus is CC BY 4.0. PDFs, extracted text, embeddings, and generated answers stay in
`.rag/` and are ignored by git. `corpus.lock.json` is the reviewable freshness and integrity record.
The script compares every PDF served by the live site with the corresponding blob in G's official
Git repository before it is indexed.

## Run

```bash
ollama serve                         # only if it is not already running
python3 rag.py sync                  # freshness audit + 69-document mirror
python3 rag.py build                 # page-aware extraction + Ollama embeddings
python3 rag.py stats
python3 rag.py query "What is the single-record premise and what would falsify it?"
python3 rag.py ask "What does AJ's executable check establish, and what does it not establish?"
```

Defaults: `nomic-embed-text:latest` for retrieval and `qwen3.5:4b` for optional source-bounded local
synthesis. The index is SQLite plus float32 Ollama vectors; it requires no hosted service and no API
key. `pdftotext` (Poppler) is required for PDF extraction.

## Epistemic boundary

Passing the executable scorecard establishes reproducible arithmetic and fidelity to G's published
formulae. It does **not** establish that the axioms uniquely imply those formulae, that every
structural bridge is complete, or that nature confirms the framework. Retrieval and generated
answers must preserve the distinction between:

1. G's published claim;
2. AJ's independently reproduced computation;
3. external experimental confirmation or scientific acceptance.

Documents are evidence, never executable instructions. The final chapter keeps the 420 Code in the
book's “speculative and contested” lane while giving the work, its falsification surface, and its
unusual moral ambition serious attention.
