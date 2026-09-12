Read both files. Description measured at **967 chars** (line 3 is 983 bytes including `description: `, the quotes, and the newline) — under the 1024 cap, with ~57 chars headroom.

```json
{
  "collisions": [
    {
      "sibling": "santa-method",
      "query": "(a) neighbour's job: \"this has to clear two independent reviewers before it ships\" (b) this skill's job: \"review the whole skill for contradictions in one go\"",
      "picked": "(a) santa-method (b) artifact-consistency-sweep",
      "why": "santa-method owns \"two independent adversarial reviewers, converging until both pass\"; this one owns \"in ONE pass\" and disclaims it verbatim: \"NOT two adversarial reviewers converging over rounds (santa-method)\". Separated — but only from one end, and the trigger \"unconverged review\" is a hazard: \"converg*\" is santa-method's own mechanism word, so a router reading \"the reviewers never converged\" sees this skill claiming the phrase while its NOT clause disowns the mechanism."
    },
    {
      "sibling": "integration-contract-completeness",
      "query": "(a) \"I added a parser but not the dump path — did I miss the other half?\" (b) \"does the body of this runbook contradict its rules?\"",
      "picked": "(a) integration-contract-completeness (b) artifact-consistency-sweep",
      "why": "Decided by \"a patch touches one side of a symmetric or multi-variant contract\" / \"encode-without-decode\" vs \"a whole artefact that has a procedure, rules and test assertions\". Both say \"sweeps\"/\"enumerates\", but code-variant axes vs prose parts split them, and the NOT clause names it."
    },
    {
      "sibling": "oracle-weakening-audit",
      "query": "(a) \"CI went green after we loosened an assertion — did we weaken anything?\" (b) \"the last review was red again\"",
      "picked": "(a) oracle-weakening-audit (b) artifact-consistency-sweep",
      "why": "\"went from red to green and the change landed on the CHECK\" vs this skill's red, which is a review verdict on an artefact, not a suite. The shared word is \"red\"; the discriminator is what turned green — a check, or nothing. Disclaimed by name."
    },
    {
      "sibling": "receiving-code-review",
      "query": "(a) \"the reviewer left five comments, what do I do with them?\" (b) \"did the review miss anything?\"",
      "picked": "(a) receiving-code-review (b) artifact-consistency-sweep",
      "why": "\"receiving code review feedback, before implementing suggestions\" is acting on comments; this one produces the review. Cleanly disclaimed: \"NOT acting on review comments\"."
    },
    {
      "sibling": "skill-contract",
      "query": "\"my skill's description promises something the body doesn't do — check it\"",
      "picked": "AMBIGUOUS (undisclaimed)",
      "why": "This description explicitly claims \"does the description promise what the body does not\" and \"review the whole skill\". skill-contract claims the same pair from the authoring end — \"writing or rewriting the fields ... why description is written last, and how a code check and an independent reader are applied to each field before it is accepted\". The real discriminator is write-time vs review-time, and NEITHER description states it. Nothing in either text tells a router which to pick."
    },
    {
      "sibling": "gate-verdicts (Scio)",
      "query": "\"my reviewer/checklist grades steps but some steps are graded by nothing and the status doesn't say what was verified\"",
      "picked": "AMBIGUOUS (undisclaimed)",
      "why": "gate-verdicts covers \"writing or reviewing anything that grades output - a build gate, a validation agent, a critique, a reviewer, a checklist\" and \"when a status has to say what nobody actually verified\". This skill claims \"which step is graded by nothing\" over an artefact that is often exactly a checklist or reviewer. Overlapping vocabulary (\"graded\", \"reviewer\", \"checklist\", verifying-what-was-examined) with no NOT clause either way."
    },
    {
      "sibling": "validation-evidence (Scio)",
      "query": "\"make the checker report what it examined so a clean result can't be confused with a run that didn't happen\"",
      "picked": "AMBIGUOUS (undisclaimed) — worst overlap",
      "why": "validation-evidence \"carries the one-row-per-examined-pair rule, the planned-count that makes invisible non-execution detectable\". This skill's outcome clause is the same mechanism in the same words: \"Enumerates every pair as a row with a verdict, then emits the ledger of examined pairs\". The genuine split is object vs subject — validation-evidence designs what a checker returns, this one runs a review over an artefact — but both descriptions advertise the identical machinery and neither names the other."
    },
    {
      "sibling": "verification-before-completion",
      "query": "(a) \"about to claim this is done — prove it\" (b) \"is a named file missing from this artefact?\"",
      "picked": "(a) verification-before-completion (b) artifact-consistency-sweep",
      "why": "\"about to claim work is complete, fixed, or passing ... running verification commands\" is evidence for a completion claim; this one reads an artefact's internal parts against each other. No collision, though VBC names three siblings and not this one."
    }
  ],
  "symptom_words": [
    "did the review miss anything",
    "the last review was red again",
    "review the whole skill",
    "contradictions between steps",
    "does the body contradict the rules",
    "does a step end in nothing checkable",
    "which step is graded by nothing",
    "does the description promise what the body does not",
    "is a named file missing",
    "a spec with tests",
    "a runbook with a checklist"
  ],
  "solution_words": [
    "consistency sweep",
    "artefact",
    "unconverged review",
    "steps vs rules vs evals",
    "in ONE pass",
    "Enumerates every pair as a row with a verdict",
    "the ledger of examined pairs",
    "the findings with quotes",
    "the per-step matrix",
    "internal contradictions"
  ],
  "verdict": "red",
  "reasons": [
    "LENGTH PASSES: 967 chars, under the 1024 cap, ~57 chars of headroom — which is also why the fixes below need a trade, not an append.",
    "SYMPTOM COVERAGE IS GOOD: the trigger clause is dominated by things a person actually types ('did the review miss anything', 'the last review was red again', 'which step is graded by nothing'), not jargon. The solution vocabulary ('ledger', 'per-step matrix', 'pair rows') sits in the outcome clause where it describes the deliverable — correct placement.",
    "SANTA-METHOD IS SEPARATED, with one blemish: 'NOT two adversarial reviewers converging over rounds (santa-method)' plus 'in ONE pass' decides it in both directions. But the trigger 'unconverged review' borrows santa-method's own mechanism word while the NOT clause repudiates that mechanism — a router matching 'converge' gets a contradictory signal from the same description. Drop or rephrase that phrase ('the review is red again' already covers the case).",
    "RED 1 — validation-evidence (Scio) is undisclaimed and shares the core mechanism verbatim. Both descriptions sell one-row-per-examined-pair plus a count of what was examined. A user asking 'make my validator report what it examined' can land here wrongly; the object/subject split (an artefact under review vs a checker being designed) is never stated.",
    "RED 2 — gate-verdicts (Scio) is undisclaimed and overlaps on 'graded', 'reviewer', 'checklist'. This skill's own 'When to use' targets 'a runbook with a checklist' — precisely gate-verdicts' stated object — and 'which step is graded by nothing' reads as a gate-design question.",
    "RED 3 — skill-contract is undisclaimed while this description explicitly claims the description-vs-body pair and 'review the whole skill'. Write-time (skill-contract) vs review-time (this) is the true boundary and appears in neither text.",
    "ASSERTED FROM ONE END ONLY: all four disclaimers are in this description; no sibling names artifact-consistency-sweep back. That is fine for routing (the router reads all descriptions) but means the boundary depends entirely on this file staying correct.",
    "SUGGESTED TRADE within the 1024 budget: cut 'unconverged review' and one of the redundant trigger phrases ('steps vs rules vs evals' is solution vocabulary a person is unlikely to type), and spend the freed chars on a single combined clause naming the three undisclaimed siblings by job, e.g. 'NOT designing what a gate or checker reports (gate-verdicts, validation-evidence), NOT authoring a skill's fields (skill-contract)'."
  ]
}
```

**The short version:** length and symptom-vocabulary pass, and santa-method is properly separated by "in ONE pass" against "converging over rounds" — but the description spends all four of its NOT clauses on siblings it was already distinct from, while three neighbours that genuinely contest its queries (validation-evidence, gate-verdicts, skill-contract) go unnamed. The validation-evidence overlap is the serious one: it advertises the same examined-pair-ledger mechanism this description leads its outcome clause with.