## Q1

I would not write it top to bottom, and I would not start until two things are in front of me that this question did not actually include: the contract file itself and the candidate sentence. The method's own rule is that the contract is the source and is read at the moment each field is written — a rule I recall rather than read is already drifted — so I'd ask for the contract path (here, `pipeline/contracts/skill.contract.json`) instead of writing against remembered field rules.

Given those, the order is: 4.0 bill of materials (one row per planned file, every row classified `exists` / `needed` / `not needed because …`, no blanks) → 4.1 references and 4.2 assets, since the body points at them and can't point at what isn't decided → 4.3 name (the contract decides it; check reserved words and the directory match) → 4.4 what-this-is/when-to-use, written from the candidate sentence and the observed failures → 4.5 steps, only observed failures, every step ending in something checkable → 4.6 pointers for each bundled file, and no bundled file pointing at another → 4.7 description, last, from the words a person types when they have the problem, read beside its nearest sibling → 4.8 frontmatter policy from the content kind.

After each field I run the code checker on the whole artefact, not the field — cross-field rules only become breakable once the field exists — then hand that field, its contract rule and nothing else to a reader who did not write it. A red field stops the run; I fix it before writing anything downstream, because everything written after it was written against something that changed. I record per field which code rules and which reader questions went red and how many rewrites it took, to `pipeline/ledgers/fields.jsonl`. At the end I check the BOM in both directions: planned files that never appeared, and files that appeared unplanned.

## Q2

Two observed failures means exactly two rules. I'd open the probe transcript, quote the two failures verbatim, and write one step per quote — each named with the run it came from, each ending in something checkable: a file and line in the migration, a named artefact (the rollback script, the lock-timeout setting), a number, or a table row. Anything else that wants into a migration-review steps section — index-build locking, backfill batch size, "consider whether the change is backwards compatible" — stays out unless the probe actually showed it failing. That advice is free to write and expensive to carry: it costs context on every invocation and cannot be measured, because nothing was failing without it. The test is mechanical — name the run, or it doesn't go in. If two rules feel thin, the answer is more probing, not more opinions. Then the code checker on the whole file, then the reader's question: is every rule traceable to a named observation, and does every step end in something checkable?

## Q3

No. It doesn't reach the reader stage — code first, and the code checker is what decides this. In this repo the cap the contract pins is 1,024 characters, and 1,380 is over it, so the field is red and a red field never proceeds. "Reads well" is a judgement about a field that will be truncated in the listing, which is the wrong question asked in the wrong order; I don't ask a human whether a 1,400-character description reads well when the cap is 1,024. I'd cut it to the trigger vocabulary — the symptoms, error strings and tool names someone types when they have the problem — drop the solution-side prose, re-run the checker on the whole artefact, and only then hand it to a reader beside its nearest sibling.

## Q4

I wouldn't write it yet — the description is written last for a reason, and it needs three inputs. First the new skill's finished body, so the scope has stopped moving; second the trigger vocabulary, the words someone types while having the problem rather than the words for the fix; third the existing skill's description in full, verbatim, since that is the thing I must not collide with. So: read the sibling's description, list what it actually owns, and write the new one around what the sibling does not do, in symptom language.

Then the mutual router test, and it runs in both directions. Take the sibling's job as a user would type it and ask which of the two a router picks and why not this one; take the new skill's job and do the same. If either answer is unclear, one of the two descriptions is wrong — and often it's the older one, so I'd expect to edit both and re-run the checker on each. I'd also add the explicit negative to the new description (the sibling's job named, and where it goes instead), because a boundary asserted from only one end fails from the other.

## Q5

No — that is the one thing the method forbids. Summarising field rules from memory is exactly how a rule drifts, and the value of holding the rules as data is that the code checker and the writer read the same sentence; a paraphrase of mine breaks that. It also wouldn't save time: `cat pipeline/contracts/skill.contract.json` is a second, and the checker (`pipeline/validate/skill_contract.py`) will tell you authoritatively which rules are red on the actual artefact. If what you want is speed, I'll run the checker now and read you the failures. What I can summarise from memory without risk is the *method* — the field order, each field's inputs, and the reader's question — because that's what this file governs; the rules themselves come from the contract at write time.

## consulted

- `/home/user/skills-repo/pipeline/evals/2026-08-30-builder-skills/prompts/skill-contract.with.txt` (the method and its bundled `field-writing.md`, as provided in the prompt)
- `/home/user/skills-repo/CLAUDE.md` (already in session context; source of the 1,024-character description cap pinned in `pipeline/CONSTANTS.md`)
- No file under `pipeline/skills/` or `pipeline/contracts/` was opened, per instruction — noted in Q1 and Q5 as the reason those answers ask for the contract rather than quoting it.
