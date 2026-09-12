Description measured at **1023 chars** (line is 1039 bytes minus `description: "` + `"` + newline) — under the 1024 cap by exactly one character.

```json
{
  "collisions": [
    {
      "sibling": "santa-method",
      "query": "(a) this output has to clear two independent adversarial reviewers before it ships",
      "picked": "santa-method",
      "why": "santa-method owns 'two independent adversarial reviewers, converging until both pass'; the sweep pre-empts it with 'NOT two adversarial reviewers converging over rounds (santa-method)' and stakes the opposite axis in its own opening, 'internal contradictions in ONE pass'. Cleanly separated, and separated on the deciding axis (rounds vs one pass), not by name-dropping alone."
    },
    {
      "sibling": "santa-method",
      "query": "(b) the last review was red again - did the review miss anything in this skill?",
      "picked": "artifact-consistency-sweep",
      "why": "'Triggers on review the whole skill, consistency sweep, did the review miss anything, the last review was red again' is verbatim the query; santa-method's description contains no miss/recall language at all, only 'until both pass'."
    },
    {
      "sibling": "validation-evidence (Scio)",
      "query": "(a) my checker reports clean - make it return one row per examined pair so 'found nothing' can't mean 'did not run'",
      "picked": "validation-evidence",
      "why": "STRONGEST COLLISION. validation-evidence owns 'the one-row-per-examined-pair rule, the planned-count that makes invisible non-execution detectable' - but the sweep re-imports that exact vocabulary in the same sentence family: 'Rules on every pair as a row, then emits the ledger of examined pairs'. Its disclaimer 'NOT what a gate or checker reports (gate-verdicts, validation-evidence)' is written on the wrong axis, since the sweep manifestly does describe what it reports. What still decides is the opening 'Use when a whole artefact ... has to be reviewed': validation-evidence designs what ANY checker returns, the sweep IS a checker you run on one artefact. Decidable, but only from the Use-when clause, not from the NOT clause."
    },
    {
      "sibling": "validation-evidence (Scio)",
      "query": "(b) review this runbook for internal contradictions between its steps and its rules",
      "picked": "artifact-consistency-sweep",
      "why": "'a skill, a spec with tests, a runbook' names the artefact types; validation-evidence never names an artefact under review, only 'a validator, rule set, scan or conformance pass' as the thing being designed."
    },
    {
      "sibling": "gate-verdicts (Scio)",
      "query": "(a) decide what my build gate is allowed to report when a check could not run",
      "picked": "gate-verdicts",
      "why": "'Decide what a gate is allowed to report and when a pass is reachable at all' plus 'when a check could not run' is the exact job; the sweep disclaims it by name, 'NOT what a gate or checker reports (gate-verdicts)'. Residual risk is that the sweep also emits a matrix and rules on rows, but it rules on PAIRS INSIDE an artefact, not on whether a verdict may be issued."
    },
    {
      "sibling": "skill-contract",
      "query": "(a) write the description and body fields of this new skill against a field contract",
      "picked": "skill-contract",
      "why": "'Use when writing or rewriting the fields' vs the sweep's 'NOT writing a skill's fields (skill-contract)'. Boundary is write vs check and it holds - though skill-contract's 'a code check and an independent reader are applied to each field before it is accepted' brushes against the sweep's 'does the description promise what the body does not'. Per-field acceptance during authoring vs cross-part pairs after; tightest pair after validation-evidence."
    },
    {
      "sibling": "integration-contract-completeness",
      "query": "(a) I added a parse path but not the dump path - did I miss the other half of this patch?",
      "picked": "integration-contract-completeness",
      "why": "'a patch touches one side of a symmetric or multi-variant contract', 'mirror sides and variant axes'; the sweep says 'NOT a code contract's mirror sides (integration-contract-completeness)' and never mentions a patch or a diff - it takes a whole artefact, not a change."
    },
    {
      "sibling": "oracle-weakening-audit",
      "query": "(a) the suite went red to green - did somebody loosen an assertion?",
      "picked": "oracle-weakening-audit",
      "why": "'the change landed on the CHECK rather than on the behavior' with its loosened/skipped/widened list; the sweep disclaims 'NOT checks weakened to buy a green run'. Near-miss on the sweep's 'which step is graded by nothing' - both talk about weak checks - but oracle-weakening-audit is scoped to a CHANGE to a test suite, the sweep to a step in a procedure that no assertion covers."
    },
    {
      "sibling": "receiving-code-review",
      "query": "(a) a reviewer left feedback that looks questionable - should I implement it?",
      "picked": "receiving-code-review",
      "why": "'receiving code review feedback, before implementing suggestions'; the sweep disclaims 'NOT acting on review comments'. No overlap - the sweep never mentions incoming feedback, only the artefact's own text."
    },
    {
      "sibling": "verification-before-completion",
      "query": "(a) I'm about to say this is done and ship it - is it ready?",
      "picked": "verification-before-completion",
      "why": "'about to claim work is complete, fixed, or passing ... requires running verification commands'. NOT NAMED in the sweep's disclaimer list, and the sweep's own When-to-use overlaps at 'about to be measured or shipped'. What decides is 'running verification commands and confirming output' vs 'internal contradictions' in a text - a run-the-commands job goes to verification-before-completion, a read-the-text job to the sweep. Decidable, but the boundary is asserted from one end only."
    }
  ],
  "symptom_words": [
    "did the review miss anything",
    "the last review was red again",
    "review the whole skill",
    "consistency sweep",
    "does the body contradict the rules",
    "a step end in nothing checkable",
    "which step is graded by nothing",
    "does the description promise what the body does not",
    "is a named file missing",
    "a skill, a spec with tests, a runbook"
  ],
  "solution_words": [
    "internal contradictions in ONE pass",
    "Rules on every pair as a row",
    "the ledger of examined pairs",
    "the findings with quotes",
    "the per-step matrix",
    "the instance section"
  ],
  "verdict": "pass",
  "reasons": [
    "1023 characters - under the 1024 cap, but by exactly one character. Any future edit overflows, so the field is effectively frozen: a needed NOT-clause (verification-before-completion) cannot be added without cutting something else first. Flagged, not failed.",
    "santa-method is separated correctly and on the deciding axis: 'NOT two adversarial reviewers converging over rounds (santa-method)' against its own 'internal contradictions in ONE pass'. Both directions of the boundary resolve.",
    "Symptom-side is genuinely strong - the trigger clause is phrased as things a person types verbatim ('did the review miss anything', 'the last review was red again'), and the six pair questions are written as complaints, not as method names.",
    "Biggest residual risk is validation-evidence: 'every pair as a row' and 'ledger of examined pairs' re-use that sibling's own stated vocabulary ('one-row-per-examined-pair rule') while the NOT clause disclaims it on an unrelated axis ('what a gate or checker reports'). The Use-when clause still decides, but the disclaimer does no work here.",
    "'the instance section' is repo-local jargon (the 'In this repo (one instance)' convention) sitting inside the symptom list where every neighbouring item is something a person would actually type. Outside this repo nobody phrases a complaint that way - it reads as a symptom but functions as solution vocabulary.",
    "verification-before-completion is a sibling the description never names, and the two touch at ship-time readiness. The boundary is inferable ('running verification commands' vs 'internal contradictions') but is asserted from that sibling's end only."
  ]
}
```

**Summary of the judgement:** pass. Every sibling query resolves to the right owner, and santa-method is properly separated on the rounds-vs-one-pass axis. Three things to watch: zero length headroom (1023/1024), the shared "examined pair / row" vocabulary with `validation-evidence` where the NOT-clause targets the wrong axis, and `verification-before-completion` being an unnamed neighbour whose boundary only one side asserts.