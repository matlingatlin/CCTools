I read the description and the eight sibling descriptions, and routed each pair in both directions.

```json
{
  "collisions": [
    {
      "sibling": "santa-method",
      "query": "the last review came back red again — get this reviewed properly",
      "picked": "contested; resolves to artifact-consistency-sweep only on a literal trigger match",
      "why": "Ours claims this verbatim: \"Triggers on ... did the review miss anything, the last review was red again\". But santa-method owns \"output must clear two independent adversarial reviewers, converging until both pass\" — a repeatedly-red review IS a non-converged convergence loop. The discriminator that saves it is our \"NOT two adversarial reviewers converging over rounds\" plus \"in ONE pass\": one pass vs rounds. A router matching the symptom rather than the mechanism can still land on santa-method. Reverse direction is clean: \"must clear two reviewers before it ships\" → santa-method, nothing in ours claims a second reviewer or a ship gate."
    },
    {
      "sibling": "validation-evidence (Scio)",
      "query": "my checker reports clean and I can't tell it actually ran",
      "picked": "validation-evidence",
      "why": "Sibling: \"when designing what a check returns rather than what it concludes\" and it \"Carries the one-row-per-examined-pair rule, the planned-count that makes invisible non-execution detectable\". Ours names the exit: \"NOT designing what a checker returns\". Sharpest vocabulary overlap in the set — our \"Ledgers every pair it ruled on\" is that sibling's own mechanism applied, so a router matching on ledger/examined-pair language can tip the wrong way. Reverse: \"review this runbook for internal contradictions\" → ours, on \"has to be reviewed for internal contradictions in ONE pass\"; the sibling designs a checker's return shape, it never reviews an artefact."
    },
    {
      "sibling": "gate-verdicts (Scio)",
      "query": "what is this gate allowed to report, and is a pass even reachable",
      "picked": "gate-verdicts",
      "why": "Sibling's first sentence: \"Decide what a gate is allowed to report and when a pass is reachable at all\". Ours exits explicitly: \"NOT deciding what a gate may report\". Residual tension: sibling covers \"when a report pads itself with things it checked but did not change\", while ours mandates \"Ledgers every pair it ruled on\" — the two give opposite advice about reporting unchanged examinations, but the routing query separates them (design the verdict policy vs run the sweep)."
    },
    {
      "sibling": "skill-contract",
      "query": "write / rewrite this skill's description and body fields",
      "picked": "skill-contract",
      "why": "Sibling: \"writing or rewriting the fields of a Claude Code skill ... against a field contract\". Ours: \"NOT writing a skill's fields\". Reverse: \"review the whole skill\" → ours, decided by \"a whole artefact ... reviewed for internal contradictions in ONE pass\" against the sibling's per-field scope (\"a code check and an independent reader are applied to each field\"). Softest of the clean pairs: both contain review-a-skill language, and the whole-vs-each-field split is the only thing carrying it."
    },
    {
      "sibling": "integration-contract-completeness",
      "query": "did this patch miss the other half of the contract",
      "picked": "integration-contract-completeness",
      "why": "Sibling: \"a patch touches one side of a symmetric or multi-variant contract\"; ours: \"NOT the mirror sides of a code contract\". Reverse is clean because ours scopes the object to \"a whole artefact ... a skill, a spec, a runbook\", never a patch or diff, despite both using the word 'sweep'."
    },
    {
      "sibling": "oracle-weakening-audit",
      "query": "the build went green — did we weaken a check to get there",
      "picked": "oracle-weakening-audit",
      "why": "Sibling: \"a suite went from red to green and the change landed on the CHECK rather than on the behavior\"; ours: \"NOT checks weakened for a green run\". Reverse clean: ours claims contradictions between parts of a text, never assertion strength."
    },
    {
      "sibling": "receiving-code-review",
      "query": "a reviewer left feedback — what do I do with it",
      "picked": "receiving-code-review",
      "why": "Sibling: \"receiving code review feedback, before implementing suggestions\"; ours: \"NOT acting on a reviewer's comments\". Reverse clean: \"did the review miss anything\" is claimed only by ours; the sibling covers responding to feedback, not auditing its coverage."
    },
    {
      "sibling": "verification-before-completion",
      "query": "about to say it's done — can I commit",
      "picked": "verification-before-completion",
      "why": "Sibling: \"about to claim work is complete, fixed, or passing ... requires running verification commands\". Ours never claims a completion gate or command execution; its object is a text's internal agreement, so neither direction is contested."
    }
  ],
  "symptom_words": [
    "did the review miss anything",
    "the last review was red again",
    "review the whole skill",
    "does the body contradict the rules",
    "do two steps contradict each other",
    "does a step end in nothing checkable",
    "which step is graded by nothing",
    "does the description promise more than the body",
    "is a named file missing",
    "does a rule have no rationale",
    "does the repo section contradict a step",
    "a skill, a spec, a runbook"
  ],
  "solution_words": [
    "consistency sweep",
    "internal contradictions",
    "in ONE pass",
    "Ledgers every pair it ruled on",
    "findings with quotes",
    "a per-step matrix",
    "artefact",
    "test assertions",
    "the repo section"
  ],
  "verdict": "pass",
  "reasons": [
    "Length ~930 characters (hand-counted from the quoted field, not tool-measured) — under the 1024 cap with roughly 90 characters of headroom.",
    "Symptom-first: the whole middle clause is eight questions in the words a person would type ('does the body contradict the rules', 'is a named file missing'), not the method's vocabulary. Solution terms are confined to the naming clause and the one output-shape sentence, which is where they belong.",
    "All eight neighbours route correctly in both directions with a quotable discriminator; seven exits are named explicitly in the NOT list, which is what makes the reverse direction decidable rather than inferred.",
    "Weakest row is santa-method: the trigger 'the last review was red again' is a symptom that also fits 'converging until both pass'. It resolves only because ours says 'in ONE pass' and NOT-lists convergence-over-rounds. If the collision is ever observed live, tighten by making the one-pass claim part of the trigger phrase rather than the naming clause.",
    "Second weakest is validation-evidence: ours advertises that sibling's own mechanism ('Ledgers every pair it ruled on', plan counts in the body). The NOT clause 'NOT designing what a checker returns' is the only thing separating apply-the-mechanism from design-the-mechanism.",
    "'artefact (artifact)' correctly covers both spellings, so the British spelling does not cost a match.",
    "Third person, triggers-only, no imperative-to-the-model phrasing — conforms to description discipline."
  ]
}
```