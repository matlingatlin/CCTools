**VERDICT: RED**

**Routing table**

| # | Request | Route | Runner-up (why not) |
|---|---|---|---|
| R1 | 4 stages unit-tested, run off by 100x | candidate (seam audit) | stage-ablation-attribution — genuinely close; "where do we look" reads as much like "which stage" as "which seam" |
| R2 | Coverage 61%→80% | test-coverage | candidate excludes intra-unit reachability |
| R3 | Added encoder, not decoder | integration-contract-completeness | candidate excludes "patch's mirror sides" |
| R4 | RAG mediocre, retriever or generator? | stage-ablation-attribution | clean |
| R5 | CI red→green before release | oracle-weakening-audit | clean |
| R6 | Vendor CSV changed, check before load | data-contract-assertions | candidate excludes "incoming third-party feed" |
| R7 | test_parse fails on one input, fix it | systematic-debugging | candidate excludes "reproducing failing test" |
| R8 | "Where should the seam go" storage↔API | interface-depth-design | candidate's bare trigger word "seam" literally overlaps this sibling's exact trigger phrase |
| R9 | "What can this test suite not catch?" | candidate | clean, matches candidate trigger verbatim |
| R10 | "Added a control, are we covered now?" | candidate | clean, matches candidate trigger verbatim |

**Per-sibling collision check**

- **test-coverage**: NONE — "inside units" vs "between units" split holds.
- **integration-contract-completeness**: COLLISION risk — candidate's trigger "integration gap" is generic enough that a patch-symmetry question ("did I miss the other half, is there an integration gap here?") could misroute either way; the two skills answer different questions (mirror-side sweep of a diff vs. full seam-fault table of a system) but share vocabulary.
- **stage-ablation-attribution**: COLLISION — R1-style prompts ("tests pass, end-to-end is wrong/off, where do we look") satisfy both descriptions almost equally; candidate answers "which fault type slips which seam," stage-ablation answers "which stage has the most headroom," but a user rarely phrases the request in those terms.
- **oracle-weakening-audit**: NONE — direction of causality (check was weakened vs. check never existed) keeps them apart.
- **agent-fault-injection**: soft COLLISION — both literally "inject faults and grade whether caught." Candidate scopes to seams between units generally (incl. non-agent pipelines); a generic "what happens if this pipeline step returns garbage, do we catch it?" without agent/tool language could land on either.
- **data-contract-assertions**: NONE — "arriving from upstream/external" vs. "between our own internal units" is a clean boundary.
- **systematic-debugging**: NONE — "one reproducing failure" vs. "nothing fails but answer is wrong" is a clean boundary.
- **interface-depth-design**: COLLISION (clearest one) — candidate lists the bare trigger word **"seam"**, which is also verbatim in interface-depth-design's own trigger ("where should the seam go"). R8 shows this directly: same word, opposite intent (design placement of a boundary vs. auditing fault-catching at existing boundaries).

The interface-depth-design word-collision on "seam" plus the stage-ablation-attribution phrasing overlap are enough real router ambiguity to call this RED as written — the candidate needs to drop the bare "seam" trigger (or qualify it, e.g. "seam that faults slip through") and sharpen the stage-ablation boundary (e.g. explicitly key on "controls/checks" vs. "score/headroom" language) before it's safe to add.