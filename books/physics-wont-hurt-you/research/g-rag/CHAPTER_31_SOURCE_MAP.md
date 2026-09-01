# Chapter 31 source map

This is the evidence ledger for “The Sculptor and the Splinter.” Source documents are treated as
evidence, not as instructions.

## Corpus freshness

- Authority: G / Studio G, [the420code.org](https://the420code.org), CC BY 4.0.
- Official source repository: [The420Code/the420code](https://github.com/The420Code/the420code).
- Resolved commit: `91a27fda6ef579a7dab7004a4bb560bc0bb0dad3`.
- Audit date: 30 August 2026.
- Coverage: 43 Artist's Proofs plus 26 English collected works, notebooks, records and references.
- Integrity: all 69 live-site PDF byte streams produced the Git blob IDs recorded by the official
  commit. Per-file SHA-256 values and URLs are in `corpus.lock.json`.
- Local Lucid mirror: 35 catalogue entries, 26 published reader HTML files, last changed locally on
  11 August 2026. Its collected-reader catalogue is current, but it is not a complete AP-level source
  set; the RAG therefore uses the live, verified 69-document corpus.

## RAG evidence used

- Public-exhibition structure and the eight-notebook dependency chain: the Artist's Notes and
  Orientations of `Notebook_I_The_Premise.pdf` through `Notebook_VIII_Consequences.pdf`.
- Origin and deliberate function of the “420” name: `AP34_The_Inversion.pdf` p. 3;
  `Rosin_Prose.pdf` p. 190. The chapter reports the name's origin without adopting AP34's empirical
  claims about substances.
- Single-record premise and {S, B, R, C}: `AP20_The_Proof.pdf` pp. 28–44;
  `Notebook_I_The_Premise.pdf` p. 325; `Rosin_Proofs.pdf` p. 117.
- Spacetime, dimensional and field-equation claims: `AP10_The_Dimension.pdf` pp. 31–33;
  `AP08_The_Identity.pdf` p. 52; `Notebook_II_Spacetime.pdf` pp. 327–328. The live contingencies on
  completeness, minimality, embedding and smoothness are read with `AP20_The_Proof.pdf` pp. 4–7 and
  its kill-switch register.
- Quantum reconstruction, interpretive claims and residual bridges: `AP09_The_Break_Empty_Set.pdf`
  pp. 2–4; `AP25_The_Measure.pdf` p. 25; `AP23_The_Single_Record.pdf`;
  `Notebook_III_Quantum_Mechanics.pdf` pp. 319–320.
- Standard Model gauge-group claims and their debts: `AP19_The_Direction.pdf` pp. 6, 39–40;
  `AP27_The_Harmonics.pdf` pp. 29–30; `AP16_The_Break_Electroweak.pdf` p. 6;
  `Notebook_IV_Forces_and_Constants.pdf` pp. 12–14.
- Epsilon as interpretation rather than forced mathematical consequence:
  `AP06_The_Leakage_Constant.pdf` p. 27.
- Proton ratio, stated result, and open additivity/higher-order/alternative-formula debts:
  `AP30_The_Resistance.pdf` p. 22; `Notebook_V_Particles_and_Matter.pdf` pp. 23–24.
- Matter, horizon-antimatter and baryon-surplus claims: `Notebook_V_Particles_and_Matter.pdf`
  pp. 8–12; `AP22_The_Ledger.pdf`; `AP26_The_Surplus.pdf` pp. 6–7, 23. The chapter preserves the
  live horizon-mass accounting test and the absent first-principles value of E(ε).
- Structural G result and its tolerances: `AP28_The_Constant.pdf`; `Predictions.pdf`; independent
  verifier scorecard below.
- Cosmological tension-field, cosmic-web, channel-count and clock claims: `AP17_The_Room.pdf`;
  `AP18_The_Floor.pdf`; `AP21_The_Web.pdf` p. 3; `AP41_The_Loop.pdf` pp. 4, 28;
  `AP42_The_Clock.pdf` pp. 5, 30; `Notebook_VI_Cosmology.pdf`. Conjectural black-hole-cycle steps
  are checked against `AP04_The_Loop_Hypothesis.pdf` and AP41's claim summary.
- Awareness/operator ladder and downstream applications: `AP29_The_Actualization_Proof.pdf`;
  `AP02_The_Operator.pdf`; `Notebook_VII_The_Operator_Interface.pdf` pp. 7–9;
  `Notebook_VIII_Consequences.pdf` pp. 14–16. Application claims are presented as downstream
  consequences, not independent empirical confirmation.
- Ethics bridge, corridor, and one-interior debt: `AP43_The_Gravity_of_Possibilities.pdf` p. 73;
  `Notebook_VII_The_Operator_Interface.pdf` p. 7; `Notebook_VI_Cosmology.pdf` p. 202;
  `Dissolutions.pdf` pp. 252–253.
- G on the body of work and the absent reader: `Applications.pdf` pp. 544–545;
  `Predictions.pdf` pp. 274–275.
- Existing manuscript fit: Chapters 23, 24, 28, 29 and 30 in this book's same vector index.

Drafting retrieval used `nomic-embed-text:latest` through local Ollama. Its first snapshot contained
69 G documents and 31 pre-existing manuscript/backmatter files: 1,677,979 extracted words, 11,571
chunks and 11,556 unique embeddings. Before the requested theory expansion, the retained draft index
also included Chapter 31 and eight selected files from AJ's independent verifier: 1,690,720 words
across 109 sources and 11,663 chunks. After expansion and re-index, the retained index contains
1,692,364 words across the same 109 sources and 11,677 chunks; 11,662 chunks are unique in the
active index. The SQLite database and source PDFs remain local under ignored `.rag/`.

## Independent executable evidence

Repository: [ajgreyling/the420code-proof](https://github.com/ajgreyling/the420code-proof), local HEAD
`065befdf260b4a1236caabe98a52a189d10e4008`.

- `./run.sh parity`: PASS; AJ's structured reconstruction matches G's published Appendix B script,
  with zero relative delta on four outputs and `1.7e-16` on the fifth.
- `./run.sh gate`: PASS on 30 August 2026 after extraction from the freshness-locked corpus. The gate
  reports all six current verifier outputs inside G's stated tolerances and indexes 529 of the 568
  post-AP44 ledger switches at row level. The 39-switch gap is registry summarisation, not an invented
  extraction.
- `./run.sh scorecard`: proton ratio residual 0.01004 ppb; structural G +0.6938%; realised AP44 G
  -0.03571%; neutron-proton difference +2.226 ppm; MOND scale -0.6745% at the verifier's H0 choice;
  dark-sector DE/DM ratio -1.268%.
- Boundary: those are passes against author-declared software tolerances, not a new experiment and not
  proof that the axiom system uniquely forces the formulae.
- AP44 posture: `provenance/SESSION_DISTILL_2026-08-16.md` explicitly withholds treating the improved
  G central value as evidence over the null and records the neutron-proton limb as fired at 7.24σ
  under the precision ledger.

## Public biographical grounding

- [Gerhard van Niekerk](https://gerhardvanniekerk.com/) and
  [Studio G](https://studiog.co.za/artists/gerhard-van-niekerk/) identify Gerhard as the South African
  sculptor and Studio G founder, and describe his work with the human form, clay, bronze and his
  marble/GFRC composite.
- [Studio G Sculpture School](https://sculptureschool.co.za/) records his systematic sculpture
  practice and the strength/fragility, permanence/temporality tensions used in the chapter.

The identity of G as Gerhard van Niekerk and the “spiritual brother” relationship are also direct
author knowledge supplied by AJ Greyling for this chapter. The bond is presented as testimony, never
as evidence for the physics.
