## Q1

I do not write it top to bottom, and I do not start from the candidate sentence's topic. Order: (4.0) bill of materials first — one row per planned file, each marked `exists` / `needed` / `not needed because …`, no blank rows, because a gap found now is a task and the same gap found mid-write is an improvisation; (4.1/4.2) any references and assets next, since the body has to point at them — every reference claim carries its source and fetch date, every asset carries named slots to fill; (4.3) name, which the contract decides (reserved words, directory match); (4.4) "what this is / when to use it", written from the candidate sentence and the observed failures; (4.5) the steps; (4.6) pointers to each bundled file (what is in it, when to open it — and no bundled file pointing at another bundled file); (4.7) description, last; (4.8) frontmatter policy from the content kind.

Two things I do at every field rather than once at the end. First, I read the rule for that field out of the contract file at the moment I write it — I never quote it from memory, so the code checker and I are reading the same sentence. Second, after each field I run the code checker over the whole artefact (not just the new field — cross-field rules only become checkable once the field exists), then hand the field plus its contract rule, and nothing else, to a reader who did not write it. Red never proceeds: I fix it before the next field, because everything written after a red field was written against something that is about to change. I log per field which code rules went red, which reader questions went red, and the rewrite count.

Concretely, before I can start I need the two inputs the method assumes and this brief has not attached: the contract file itself (I will not reconstruct its rules) and the probe findings / observed failures the body and steps must be traceable to. Give me those and I write it in the order above; without the observed failures I can produce a name and a bill of materials but the steps section would be opinion.

## Q2

Two observed failures means at most two rules. I write exactly the steps those two transcript entries force, each one quoting the observation it came from and naming the run — e.g. "run <id>: the reviewer approved a migration adding a NOT NULL column with no default to a table with existing rows; the deploy failed on backfill" becomes a step that reads the migration for every added constraint and records, per constraint, the row count of the target table and whether a default or backfill exists. Each step ends in something checkable: a number, a file and line, a named artefact, or a table row. "Consider whether the migration is safe" is not a step; "list every added column with NOT NULL and no default, with the target table's row count beside it — empty list or explicit backfill required to pass" is.

Everything else that wants to go in — lock duration, index concurrency, rollback scripts, review checklists I know are good practice — stays out unless the transcript shows it failing. It is free to write and expensive to carry: it occupies context on every invocation and cannot be measured, because nothing was failing without it. The test is mechanical, applied per rule: name the run. If I cannot, the rule does not go in, and the honest output here is a two-step steps section plus a note that the probe was thin and further steps wait on further observations.

## Q3

No. Reads-well is the wrong check to have run first, and it is the second check regardless. I run the code checker against the contract's length rule before any reader sees it — there is no point asking whether a 1,380-character description reads well if the cap is below that. I read the cap out of the contract file rather than asserting one from memory; in this library the pinned cap is 1,024, so 1,380 is red on its face and a red field never proceeds. It is also not merely a formatting failure: an over-cap description gets truncated or rejected by the thing that routes on it, so the part that "reads well" may be the part nobody sees.

So: rewrite to fit, from the trigger vocabulary rather than by trimming adjectives off the end, re-run the checker, then hand it to the independent reader with the router question. Ship after both are green, not before.

## Q4

I do not write it yet, and I do not write it from my own skill's intent. The description is the last field for a reason: it needs the finished body's actual scope, the trigger vocabulary, and — exactly the situation here — the neighbour's description in front of me. So step one is to pull the existing skill's description verbatim and read what job it actually claims, not what I remember it claiming.

Then I write mine from the words a person types when they *have* the problem — symptoms, error strings, tool names, the failure as it appears ("migration locked the table", "ALTER on a live table", the specific error text from the probe) — not the vocabulary of the solution ("reviews schema changes"), which is precisely the phrasing both skills already share and the reason they collide.

Then the two-way router test: put the two descriptions side by side and ask, for each one's job, which unit a router would pick and why not the other. If the answer is unclear in either direction, one of the two descriptions is wrong — and it may be the incumbent's, so I am prepared to propose an edit there too rather than contorting the new one around it. I add an explicit negative boundary naming the sibling, and I make the sibling name back, since one-sided boundaries are what parallel authoring produces. Finally the code checker (cap, required fields), then a fresh reader who did not write either.

## Q5

I won't, and not to be difficult — a summary from memory is the one artefact this method explicitly forbids. Rules held as data only pay off if the code checker and the writer are reading the same sentence; a rule I recite is a rule that has already drifted, and the drift is silent, so we would move fast into rework at whichever field it bit. The failure mode is specific: the fields written after a wrongly-remembered rule were all written against something that changes when the checker finally reads the real one.

What I will do instead, and it is faster than it sounds: open the contract file and read the rule for the field we are on, at the moment we write it — one field's rules, not the whole file. If what you want is speed, the thing to hand me is the contract path; if what you want is orientation, I can give you the *order* and the inputs each field needs (that is the method, and it is legitimately held in this document) — but the field rules themselves come off disk, per field, every time.

## consulted

- `/home/user/skills-repo/pipeline/evals/2026-08-30-builder-skills/prompts/skill-contract.with.txt` (the method and its bundled `field-writing.md`, both quoted in full in the prompt)
- `/home/user/skills-repo/CLAUDE.md` (loaded automatically as project instructions; source of the 1,024-character description cap referenced in Q3, itself pinned in `pipeline/CONSTANTS.md`)
- No file under `pipeline/skills/` or `pipeline/contracts/` was opened, per instruction — which is why Q1, Q3 and Q4 name the contract as an input rather than quoting it.
