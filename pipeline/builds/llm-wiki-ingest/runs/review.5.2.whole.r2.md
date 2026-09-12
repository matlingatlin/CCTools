I read the whole artefact and ran `check.py` on the untouched fixture wiki for T1/T2/T3, plus three probes (vandalised note under T3, a rival page under T1, a correct ingest under T1).

**Key evidence — T3's central check cannot fail.** `check.py` resolves its "fixture" to `Path(__file__).parent/"wiki"/"notes"`, which is the *same* directory the prompt tells the agent to edit in place. I appended a fabricated price line to `model-prices.md`, then a LOG and SOURCES row, and T3 graded **16/16 PASS, exit 0** — the exact baseline failure T3 exists to catch ("every baseline run (2 of 2) still edited the owning page") is invisible to the grader. That is the run recorded in `evals.md` as "the one measured win".

```json
{
  "findings": [
    {
      "level": "INSTANCE",
      "where": "evals/files/check.py:54 (T3 branch)",
      "finding": "The T3 'byte-identical to the fixture' checks compare the wiki against ITSELF: the fixture path resolves to evals/files/wiki/notes, the same tree the T3 prompt says to 'Edit the wiki in place'. No pristine copy exists anywhere in the artefact. PROVED: appending a fabricated line ('Beta 5 is now $1') to notes/model-prices.md and adding the LOG/SOURCES rows scores T3 16/16 PASS, exit 0. The only scenario evals.md records as beating baseline (S5/T3, 'without 0/1, probe 0/2, incumbent 0/2') is graded by a check that cannot fail, so the measured win is unsupported. The dead ref = {'model-prices': 'MP', ...} values on line 52 look like the remains of the pristine-copy design that was dropped. Fix: ship a read-only copy of the notes (or their hashes) outside the edited wiki and hash against that.",
      "quote": "fixture = pathlib.Path(__file__).resolve().parent / \"wiki\" / \"notes\""
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 2 (no material) vs steps 6 and 7",
      "finding": "Step 2's 'stop' contradicts the steps that follow it. Step 6 requires a source-log row 'also on no material' and an operation-log line 'in every branch' — i.e. work AFTER the stop — and step 7 requires lint + index rebuild and 'The fact and its lint pass land in one commit', which the no-material branch never reaches if 'stop' is taken literally. The numbered list is read as a sequence but is really a branch tree, so an agent can legitimately end at step 2 with the LOG/SOURCES rows uncommitted and unlinted. This is the branch T3 grades. Fix: make step 2's branches terminate INTO steps 6-7 explicitly ('go to step 6') rather than 'stop'.",
      "quote": "**no material** - no claim, no value, no newer date for any page: keep the raw, write the source-log row and the operation-log line, touch no page, stop."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 2, 'no newer date' clause",
      "finding": "The no-material test admits the failure the skill was built to prevent. The T3 blog is fetched 2026-09-02, newer than prompt-caching's 2026-08-20 source, and restates the same 0.1x/1.25x. Under 'no newer date for any page' an agent can reasonably triage it as an update and add a corroborating source — precisely the baseline behaviour rationale.md rules out ('A page's source list says what the page was derived from, not what agrees with it'). The body clause is weaker than its own rationale. Fix: test the VALUE and its as-of date, not the fetch date — 'no claim, no value, and no newer as-of date; a newer source restating a value the wiki already holds is no material'.",
      "quote": "**no material** - no claim, no value, no newer date for any page"
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 5 (Cascade)",
      "finding": "The step that carries the skill's signature behaviour does not say which file gets edited. 'Every neighbour the page names gets one sentence saying why it matters to it' has two unresolved 'it's and reads equally as 'the new page gets a sentence about each neighbour' — the opposite of the description's 'neighbours name it back' and of evals.md S4 ('each neighbour gains a sentence naming the new page back'). Nothing in the artefact disambiguates it, and no executed eval exercises it: all three prompts UPDATE an existing note, so no page is created and no cascade is performed. Fix: name the direction and the file ('open each neighbour's page; add one sentence there naming the new page').",
      "quote": "Every neighbour the page names gets one sentence saying why it matters to it, then the `related:` entry. No true sentence, no edge."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 2 (disputed branch) vs references/rationale.md",
      "finding": "rationale.md states its own contract — 'a rule with nothing behind it does not belong in the body' — and the disputed branch has nothing behind it: no rationale entry, no source, and evals.md records S2/T2 as 'with 2/2, without 1/1 ... the baseline is clean here too' (no delta). Same for three smaller body rules with no rationale entry: the status enum verified/unverified/outdated, 'Every price, version, limit, count and date in the body carries its as-of date', and the memory rule 'Nothing about a tool, price, version or limit from memory'. Either cite the observation or cut them; the disputed branch is a third of step 2 and a whole eval, so it needs an observed failure or an explicit 'inherited from the wiki's schema, not from a failure'.",
      "quote": "**disputed** - the source contradicts a claim a page holds: keep both values as dated claim rows with their sources, mark that row `disputed`, and set the page's `status: disputed` for as long as any row is."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 3",
      "finding": "Step 3 does not end in something checkable. 'Every number, date and quote' has no observable output for the ones judged not worth a row — the claims table shows what WAS written, never what was skipped — so 'every' can be silently satisfied by grading one figure. check.py accordingly checks a single row per task. Either bound it to a checkable set ('every number, date and quote that becomes a body claim') or require the raw's untaken figures to be listed under 'what is open'.",
      "quote": "**Locate every number, date and quote in the raw before writing it,** and grade it"
    },
    {
      "level": "CLASS",
      "where": "SKILL.md frontmatter description vs the body's 'Not this skill' paragraph",
      "finding": "No — the 'In this repo' section is not the only place naming this repository. The body is disciplined (it defers: 'the local names are under *In this repo*'), but the description names five repo-local units, so a portable copy of this skill routes against siblings that may not exist in the host repo. This is the one finding in tension with the repo's own description discipline (siblings must be differentiated for routing), so it is a deliberate-tradeoff call rather than a defect: either accept it and say so in 'In this repo', or phrase the exclusions by job ('NOT summarising a text; NOT claims bundled into another unit') and keep the unit names below.",
      "quote": "NOT summarising a text (deep-reading), NOT claims for a skill bundle (skill-knowledge), NOT agent memory (unified-memory), NOT docs broken by code (doc-claim-reconciliation); whole-wiki clean-up is the kb-curator agent."
    },
    {
      "level": "INSTANCE",
      "where": "evals/files/check.py:26 (T1 'no rival page')",
      "finding": "The rival-page check only catches rivals whose filename contains 'pric'. PROVED: adding notes/beta-5-costs.md (a full rival page with the new prices, indexed, with SOURCES and LOG rows) leaves 'no rival page' PASSING. T1 still fails overall via the three model-prices checks, so the eval verdict survives, but the named check reports the opposite of the truth. Fix: assert the note set is unchanged, as T3 line 58 already does.",
      "quote": "check(\"no rival page\", not any(s not in (\"model-prices\",\"prompt-caching\",\"local-models\") and \"pric\" in s for s in notes), str(sorted(notes)))"
    },
    {
      "level": "INSTANCE",
      "where": "evals/files/check.py:37 and :30-31 (T1)",
      "finding": "Two T1 checks pass on the untouched wiki (measured: 'old price kept as a dated superseded row' and 'neighbour names owner back' both PASS before any ingest). As non-regression checks that is correct, but it means the only cascade-related assertion in the whole grader is satisfied by the fixture as shipped, and 'kept' is not distinguished from 'never touched' — nothing requires the retained row to be MARKED superseded, which is what the expectation text implies. Also: evals.md S1's pass criterion 'INDEX unchanged' is not graded anywhere.",
      "quote": "check(\"neighbour names owner back\", \"[[model-prices]]\" in notes.get(\"prompt-caching\",\"\"))"
    },
    {
      "level": "INSTANCE",
      "where": "evals/files/raw/*.md vs SKILL.md step 1",
      "finding": "The artefact's own raw fixtures carry provenance inside the immutable file (a 'source:'/'fetched:' header), the shape step 1 tells the ingester not to use. Harmless for inputs the skill did not write, but the fixtures teach the opposite of the step, and nothing in the three evals checks that a raw copy was kept at all — step 1 is ungraded, as are step 7's hand-lint log clause and the whole 'new page' triage branch.",
      "quote": "provenance (source, date, hash, size, which page it feeds) in the directory's manifest rather than inside the immutable file"
    },
    {
      "level": "INSTANCE",
      "where": "evals/files/check.py:9-11",
      "finding": "INDEX.md and SOURCES.md are read unguarded while LOG.md is guarded by .exists(); a run that deletes or fails to create INDEX.md crashes the grader with a traceback instead of recording a FAIL, which reads as harness breakage rather than a failed run.",
      "quote": "index = (wiki / \"INDEX.md\").read_text(encoding=\"utf-8\")"
    }
  ],
  "class_finding": true,
  "verdict": "red"
}
```

Answers to the five questions, briefly:

1. **Contradictions:** yes — step 2's `stop` vs step 6's "in every branch" / step 7's one-commit rule, and step 2's "no newer date" vs rationale.md's "derived from, not what agrees with it".
2. **Checkable endings:** all but step 3 ("every number, date and quote" has no observable for what was skipped) and step 5 (checkable only once the direction is fixed).
3. **Executable:** yes — all listed files exist, the prompts' paths resolve, and a correct T1 ingest I simulated scores 18/18. But `check.py` does **not** grade what T3 asks: its byte-identity check self-compares and passes a vandalised wiki 16/16. T1 and T2 discriminate correctly (13/18 and 10/19 on the untouched wiki, failing exactly the ingest-specific checks); T3 fails only on LOG/SOURCES before ingest.
4. **Unsourced rules:** the disputed branch (no rationale entry, and evals.md records no baseline delta), plus the status enum, the as-of-date rule, and the from-memory rule — against rationale.md's own "a rule with nothing behind it does not belong in the body".
5. **'In this repo' exclusivity:** no — the description names five repo-local units while the body explicitly defers naming them.