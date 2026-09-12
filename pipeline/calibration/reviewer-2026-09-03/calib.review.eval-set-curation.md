I read all five BOM'd files plus SKILL.md, and verified the fixture-dependent claims by recomputing them from `logged_traffic.csv`.

**Verification runs (not assertions):**
- Fixture ground truth in `evals.json` is accurate: 2000 rows, slice counts, 0.8875 overall, 37 contaminated, 1940 distinct raw strings.
- Applying **step 1 clause 1's own normalisation list** (IDs, digits/hex) to the file leaves **64 distinct strings**, with three families covering **1858 rows** — confirming `evals.json`'s correction and, more importantly, that step 1 clause 1 destroys the family step 1 exists to catch.
- Grep-aid terms in `selection-evidence.md`: every term occurs in the body **except `UNQUOTED`**, which occurs exactly once — in the grep-aid list itself.
- `evals.md`'s reported rates (97.4 / 90.3 / 66.7 / 41.2 / 52.9) are not k/19 for any k; 41.2% and 52.9% are 7/17 and 9/17.

**Answers to the four questions:** (1) yes — step 1 contradicts itself, and the description promises two jobs the body explicitly refuses. (2) no step is graded by anything: all five `expectations` arrays are empty, so the answer to "which expectation grades it" is *none*, for all three steps. (3) yes — `~50 pairs`, the look-budget clause, and two enforced record fields have no step and no observed failure behind them. (4) in SKILL.md, yes; across the artefact, no — `evals.json` and `evals.md` name host-repo paths and build phases.

```json
{
  "findings": [
    {
      "level": "CLASS",
      "where": "SKILL.md step 1, clause 1 vs clause 4 and the warning inside clause 1",
      "finding": "Step 1's normalisation instruction destroys the exact failure step 1 exists to catch, and the bundle's own fixture proves it. Clause 1 tells you to normalise 'IDs, timestamps, and only slots you can enumerate before looking at the clusters (an order number, a date, a customer name)' - but the varying slot of a templated family IS an order number, a date or a name. The same clause then warns that doing this makes 'step 4's two numbers come out equal and clean while the family is still standing'. So the clause mandates and forbids the same operation. Measured on evals/logged_traffic.csv: applying clause 1's own list (8-hex tokens and digits) collapses 1858 of 2000 rows into three strings - the largest templated family in the fixture disappears in step 1, before the clustering step ever runs. The normalisation list is offered as the mitigation, but a list is a disclosure, not a guard; nothing in step 1 tells the reader which enumerable slot to leave alone.",
      "quote": "Normalise first — case, whitespace, IDs, timestamps, and **only slots you can enumerate before looking at the clusters** (an order number, a date, a customer name). ... If you normalise the varying slot of a templated family here, the family collapses in step 1 and step 4's two numbers come out equal and clean while the family is still standing"
    },
    {
      "level": "CLASS",
      "where": "frontmatter description vs SKILL.md 'Important — what this is for' and 'The order these run in'",
      "finding": "The description routes two jobs here that the body explicitly refuses. It lists 'test-set contamination' as a trigger, and opens 'the question is WHICH of it becomes the eval set' - i.e. the whole selection. The body excludes both: contamination is listed among the four behaviours the baseline already does and is then declared untaught, and the ordering section repeats 'It is not taught here'. The intro likewise concedes 'this method does not run the whole selection'. A user arriving on the contamination trigger gets three steps, none of which is about contamination, and an asset whose section 4 is marked context with no stop clause.",
      "quote": "**None of that is taught here**, because teaching it costs context on every invocation and buys a behaviour that is already reliable."
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json - all five evals",
      "finding": "Nothing in the bundle grades any step. Every eval carries \"expectations\": [] and every expected_output for E1-E4 is the placeholder 'FILLED IN AFTER THE MEASUREMENT - see expectations below', with nothing below. The file contradicts itself twice about this: it says of E5 that it 'carries no expectations list' as if that were the exception, and its own ground-truth correction claims 'The expectation set at 6.2 is written against the corrected structure' - an expectation set that is not in the file. evals.md meanwhile reports 19 expectations, two graders and 114 graded cells, so the expectations existed at measurement time and were never written back. The shipped eval artefact is therefore ungradable: step 1, step 2 and step 3 each end in something checkable (two numbers plus a normalisation list; a floor with a named tolerance; a Sealed field with a look log), and not one of them has an expectation behind it here.",
      "quote": "\"expected_output\": \"FILLED IN AFTER THE MEASUREMENT - see expectations below.\",\n      \"expectations\": []"
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 1 clause 2 vs the Rules block",
      "finding": "Step 1 prescribes '~50 pairs' - a round number with no derivation, no citation and no observed failure behind it - in a skill whose step 2 exists to forbid exactly that. Step 2 condemns three baseline runs for setting a floor with 'a round number of their own invention — 30, 200 and 350', and the Rules block says a number that appears nowhere else 'is an invention with a table around it'. 50 appears nowhere else: not in selection-evidence.md, not in the asset's rationale, not in any recorded baseline failure. The asset then hard-wires it as a field ('n pairs labelled'). Either the number is derived from a tolerance the way step 2 demands of every other number in the method, or it should be stated as a policy the way step 3 clause 4 correctly states the look budget.",
      "quote": "Take a sample of ~50 pairs spanning the score range, label each yourself as same-intent or not, and set the threshold where your labels flip."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 1 (opening) and assets/eval-set-record.md section 3 stop clause",
      "finding": "The motivating numbers in the body and in the portable asset are the fixture figure that this bundle's own evals.json declares WRONG. evals.json's near_duplicate_structure_CORRECTED states the 6-families/120-rows figure 'is not the answer this skill's own step 1 produces' and that a correct run 'reports roughly 10 clusters, not 6' over 64 distinct strings - which I confirmed by recomputation. Both SKILL.md's observed-failure sentence and the asset's stop clause still carry the superseded numbers, and the asset carries them as a generic illustration in a template meant for any population, so a fixture-specific and now-known-defective count has been baked into the portable deliverable.",
      "quote": "Collapsing 120 rows to 60 distinct strings and calling the result deduplicated leaves a paraphrase family standing."
    },
    {
      "level": "CLASS",
      "where": "assets/eval-set-record.md section 5 (ENFORCED) vs SKILL.md step 2 clauses 1-5",
      "finding": "The enforced section of the record requires two things no step teaches and no observed failure names. (a) 'Is the interval cluster-adjusted?' is a required row in an ENFORCED section, yet no step clause instructs it, and step 2 says the only claim that sizes clustering is deliberately cited by no step and its numbers must not be carried into the record - so the record demands an answer the method has decided not to equip the reader to give. (b) 'Report the raw fraction, never a percentage' is a rule stated only in the asset; step 2 has no such clause, and the body attributes the underlying behaviour ('said in their own words that the rare slice could not be measured at its n') to the baseline that already does it reliably. A field in an enforced section is a step by another name; both need either a clause in step 2 or removal.",
      "quote": "| Is the interval cluster-adjusted? | <yes, by what> / <no — naive Bernoulli or Wilson> / <not checked> |"
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 3 clause 4 and 'When to use' bullet 5",
      "finding": "The look-budget clause is a rule with no observed failure behind it, in a skill that states its own discipline as answering only observed failures. The failure recorded for step 3 is that three of four runs called an unsealed pool a holdout - nobody was observed getting a look budget wrong, because nobody got as far as having one. The bundle confirms the gap from both sides: evals.json's f2_hole says F2 'has NO eval of its own' and 'treat step 3 as the least-tested of the three', and evals.md repeats that nothing observes a holdout being reused. Clause 4 plus its 'When to use' bullet are roughly a quarter of step 3's text and are honest that they invent no number - but by this artefact's own standard that makes them context, not a step.",
      "quote": "**A look budget is a policy, and it is written down as one.** There is no evidence-based number here and this method does not invent one."
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json (E5 expected_output, known_fixture_defect, near_duplicate_structure_CORRECTED) and evals.md",
      "finding": "'In this repo' is the only place SKILL.md names the host repository - that check passes for SKILL.md itself. It does not pass for the artefact. evals.json, a shipped bundled file, names the host build harness and its internal phase numbering in four places ('phase 6.5 by pipeline/build/triggers.py', 'phase 4.0', 'the whole-artefact reviewer at phase 5.2', 'Carried to phase 7.2 as a test bug'), and evals.md names '.claude/skills/eval-set-curation/SKILL.md' and 'measure/void/'. A build record naming the build is defensible; an eval spec that cannot be run outside this repo without editing is the generality rule leaking past the section that was supposed to contain it.",
      "quote": "Scored at phase 6.5 by pipeline/build/triggers.py, which is a routing test rather than an output test, so it carries no expectations list."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md - 'Result — expectations met, by arm' table vs the sentence below it",
      "finding": "The reported rates cannot come from the stated denominator. With 19 expectations the only achievable percentages are k/19 (94.7, 89.5, 68.4, 42.1, 52.6 ...); none of 97.4%, 90.3%, 66.7%, 41.2% or 52.9% is one. 41.2% and 52.9% are exactly 7/17 and 9/17, and 66.7% is 2/3 - so at least the 'without' arm was scored over 17 cells, not 19. Either some expectations were N/A per arm (which is not stated, and would make the arm means non-comparable) or the count is wrong. The claim '113 of 114 cells' is consistent with 19 x 6 runs, which makes the mismatch internal to the same paragraph.",
      "quote": "19 expectations: 8 computed from the fixture and written before any arm output existed, 11 judged from the blinded copies. The graders agreed on 113 of 114 cells."
    },
    {
      "level": "INSTANCE",
      "where": "references/selection-evidence.md - the grep aid",
      "finding": "The grep aid lists UNQUOTED as a search term and the parenthetical immediately asserts that every term was checked against the file. UNQUOTED occurs exactly once in the file: in that list. Searching it returns only the aid that recommended it - precisely the silent failure the parenthetical claims has been prevented. Every other listed term (n=100, half-width, clustered, rephrased, holdout, 63%, Stratified, stratification, DERIVED, REPEATED, 'Not in the quote above', 'Does not establish') and all thirteen claim ids do resolve, so this is one broken entry in an otherwise working aid, and the false assurance is the larger part of the defect.",
      "quote": "(Terms are checked against the file: a grep aid pointing at a string that is not here fails silently, which is the worst way for a lookup surface to fail.)"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md line 3 vs the bundle's status as an adopted skill directory",
      "finding": "The bundle ships its own non-ship verdict. evals.md is headed 'candidate, build eval-set-curation-v2' and records ITERATE with both cost clauses of the preregistered rule failed at 1.84x tokens and 1.39x tool calls against a 1.20x cap, triaged as a skill bug rather than a test bug - meaning the cost is the work the three steps ask for. The BOM presents these as files 'from the adopted skill's directory'. Whichever is correct, the artefact asserts both, and a reader cannot tell from the bundle whether the steps in front of them are the ones that failed the cost gate or a revision of them.",
      "quote": "**Verdict: ITERATE.** These scenarios were EXECUTED, not predicted."
    }
  ],
  "class_finding": true,
  "verdict": "red"
}
```