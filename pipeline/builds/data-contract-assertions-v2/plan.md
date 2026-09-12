# Field decomposition — data-contract-assertions-v2

Written at 4.0, before any field. Order is skill-contract's, not file order.

| # | Phase | Field | Depends on | Drafted by | Reader group |
|---|---|---|---|---|---|
| 1 | 4.0 | bill of materials | scope sentence + probe findings | coordinator | with 4.1/4.2 brief |
| 2 | 4.1/4.2 | references, assets | the claim set (13 claims, 3 contradictions) | DISPATCHED writer | one reader, batched |
| 3 | 4.3 | name | the directory | coordinator (contract-decided) | batched with 4.8 |
| 4 | 4.4 | body: what and when | scope sentence + observed failures | DISPATCHED writer | own reader |
| 5 | 4.5 | body: steps | observed failures, quoted + claim set | DISPATCHED writer | own reader, NEVER batched |
| 6 | 4.6 | pointers | the finished bundle | DISPATCHED writer | own reader |
| 7 | 4.7 | description | finished body + trigger terms + siblings | DISPATCHED writer | own reader, NEVER batched |
| 8 | 4.8 | frontmatter | content_kind + what was bundled | coordinator (contract-decided) | batched with 4.3 |

Two fields are NOT dispatched, and the reason is the experiment's own escape clause:
name and frontmatter are decided by the contract, not by judgement. The brief that
would let a writer decide `name: data-contract-assertions` is longer than the line
itself, and adjudicating the draft would cost strictly more than writing it. Recorded
per field at 4.3 and 4.8.

## Bill of materials

| file | kind | why it is needed | status |
|---|---|---|---|
| `SKILL.md` | required | the unit itself | needed — rewritten from the incumbent's 190-line body |
| `references/threshold-evidence.md` | reference | the 13 verified claims with verbatim quotes and fetch dates, and the three contradictions the package refuses to resolve. The incumbent has 0 references and 0 URLs, so every number in its body is currently unsourced. This is also the only place the NEGATIVE finding can be carried with its source: no primary source publishes a mapping from drift magnitude to expected harm. | needed |
| `assets/` | template | — | **not needed because** the artefact the steps emit is a per-column checks table whose columns are named in the body. A separate template would restate those column names in a second place, and the two would drift. Re-checked at 4.6: no pointer wanted one. |
| `evals/evals.json` | eval set | `package.verifiable` is true, so `eval.exists` is an ERROR without it. The incumbent has `evals.md` carrying JUDGED PREDICTIONS and no runnable evals at all — which is exactly why the extend gate came back UNDECIDABLE at 1.1b. | needed |
| `scripts/` | script | — | **decided at 7.1, not here.** The contract's own rule is that scripts are DISCOVERED from the eval transcripts (`content_source: DISCOVERED ... Not designed up front`), so a row that pre-committed one would be an improvisation dressed as a plan. |

Checked in both directions at 8.2: planned files that never appeared, and files that appeared unplanned.
