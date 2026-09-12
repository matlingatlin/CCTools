Reviewed the `description` only, against all eight neighbours in `siblings.json`.

```json
{
  "collisions": [
    {
      "sibling": "santa-method",
      "query": "this output has to clear two independent adversarial reviewers before it ships",
      "picked": "santa-method",
      "why": "santa-method owns 'two independent adversarial reviewers, converging until both pass'; the sweep explicitly disclaims it — 'NOT two adversarial reviewers converging over rounds (santa-method)' — and stakes the opposite mode with 'in ONE pass' and 'Enumerates every pair as a row with a verdict'. Separation is explicit at both ends."
    },
    {
      "sibling": "santa-method",
      "query": "the last review was red again on a different set of findings — did it miss anything",
      "picked": "artifact-consistency-sweep",
      "why": "The literal strings 'did the review miss anything', 'the last review was red again' and 'unconverged review' are in this description and nowhere in santa-method's, whose only trigger is the ship-gate ('before it ships'). The repeat-red symptom routes here."
    },
    {
      "sibling": "integration-contract-completeness",
      "query": "I added a parse path but not the matching dump — is this change symmetric",
      "picked": "integration-contract-completeness",
      "why": "'symmetric or multi-variant contract', 'mirror sides and variant axes', 'encode-without-decode' are all its words; the sweep names it out with 'NOT a code contract's mirror sides'. The sweep's subject is 'a whole artefact that has a procedure, rules and test assertions', not a patch."
    },
    {
      "sibling": "integration-contract-completeness",
      "query": "review the whole skill — do the steps, rules and evals agree with each other",
      "picked": "artifact-consistency-sweep",
      "why": "'steps vs rules vs evals', 'review the whole skill', 'contradictions between steps' are exclusive to this description; the sibling is scoped to 'a patch touches one side' of a contract."
    },
    {
      "sibling": "oracle-weakening-audit",
      "query": "the suite went green — did we relax an assertion to get there",
      "picked": "oracle-weakening-audit",
      "why": "'assertion loosened', 'tolerance widened', 'just get it green' are its vocabulary; the sweep disclaims with 'NOT checks weakened to buy a green run'. The sweep never mentions red-to-green history — it asks 'which step is graded by nothing', a presence question, not a strength question."
    },
    {
      "sibling": "receiving-code-review",
      "query": "a reviewer left comments I think are wrong — what do I do with them",
      "picked": "receiving-code-review",
      "why": "'receiving code review feedback, before implementing suggestions' vs the sweep's 'NOT acting on review comments (receiving-code-review)'. The sweep produces findings; it does not consume them."
    },
    {
      "sibling": "skill-contract",
      "query": "write the description and body fields of this new skill against a field contract",
      "picked": "skill-contract",
      "why": "'writing or rewriting the fields', 'the order fields are written in', 'why description is written last' are authoring words; the sweep's verb is 'has to be reviewed'. But the sweep's clause 'does the description promise what the body does not' overlaps skill-contract's 'an independent reader are applied to each field', and skill-contract is NOT in the NOT-list. Resolvable by write-vs-review, only just."
    },
    {
      "sibling": "verification-before-completion",
      "query": "I'm about to claim this is done — prove it",
      "picked": "verification-before-completion",
      "why": "'about to claim work is complete... running verification commands' is about the work passing; the sweep is about the artefact's parts agreeing internally ('internal contradictions'). No shared trigger phrase; clean."
    },
    {
      "sibling": "gate-verdicts (Scio)",
      "query": "this step is graded by nothing — what is my gate allowed to report",
      "picked": "gate-verdicts (Scio)",
      "why": "REAL collision. gate-verdicts owns 'reviewing anything that grades output... whether a gate is the real enforcement point', and this description advertises 'which step is graded by nothing'. A router seeing only the two descriptions gets no discriminator: the sweep never says it reports the ungraded step rather than designing the grader. gate-verdicts is not in the NOT-list."
    },
    {
      "sibling": "validation-evidence (Scio)",
      "query": "make the checker report what it examined so 'found nothing' can't mean 'didn't run'",
      "picked": "validation-evidence (Scio)",
      "why": "STRONGEST collision. validation-evidence 'Carries the one-row-per-examined-pair rule, the planned-count that makes invisible non-execution detectable' — which is verbatim this sweep's mechanism: 'Enumerates every pair as a row with a verdict, then emits the ledger of examined pairs'. The sweep is the APPLICATION of that rule to one artefact review; validation-evidence is the rule for designing any checker's output. Nothing in either description states that boundary, and neither names the other."
    }
  ],
  "symptom_words": [
    "did the review miss anything",
    "the last review was red again",
    "contradictions between steps",
    "does the body contradict the rules",
    "which step is graded by nothing",
    "is a named file missing",
    "does the description promise what the body does not",
    "review the whole skill",
    "a skill, a spec with tests, a runbook with a checklist"
  ],
  "solution_words": [
    "consistency sweep",
    "unconverged review",
    "steps vs rules vs evals",
    "Enumerates every pair as a row with a verdict",
    "the ledger of examined pairs",
    "the per-step matrix",
    "in ONE pass"
  ],
  "verdict": "pass",
  "reasons": [
    "Length ~960 characters, under the 1024 cap.",
    "santa-method is separated at both ends: the sweep says 'NOT two adversarial reviewers converging over rounds (santa-method)' and positively claims 'in ONE pass'; the repeat-red symptoms ('the last review was red again', 'unconverged review') sit only here, so neither direction of the pair is ambiguous.",
    "Symptom-first on balance: the clause list is written as questions a person types about their own artefact ('is a named file missing', 'did the review miss anything'), not as method vocabulary. Solution words appear mostly in the outputs sentence, where they describe the deliverable rather than compete for the trigger.",
    "Two solution-only phrases carry trigger weight they cannot earn: 'consistency sweep' and 'unconverged review' are terms someone would only type if they already knew this unit exists. 'steps vs rules vs evals' is also house vocabulary. These are additions rather than substitutes, so they cost nothing, but they are not doing routing work.",
    "Unnamed collision with validation-evidence (Scio): both descriptions carry the one-row-per-examined-pair and planned-count mechanism, and neither states the boundary (apply-to-one-artefact vs design-any-checker's-output). Recommend a NOT clause naming it.",
    "Unnamed collision with gate-verdicts (Scio) on the ungraded-step trigger: 'which step is graded by nothing' vs 'reviewing anything that grades output'. Discriminator would be that this REPORTS which step nothing grades, while gate-verdicts decides what a grader may say.",
    "Minor unnamed overlap with skill-contract on 'does the description promise what the body does not'; the write-vs-review verb split resolves it, so no change is required."
  ]
}
```