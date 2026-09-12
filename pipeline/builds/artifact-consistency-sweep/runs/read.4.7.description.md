Read both. Here's the review.

```json
{
  "collisions": [
    {
      "sibling": "santa-method",
      "query": "output must clear two independent adversarial reviewers before it ships",
      "picked": "santa-method",
      "why": "santa-method owns 'two independent adversarial reviewers, converging until both pass'; the sweep explicitly cedes it — 'NOT two adversarial reviewers converging over rounds (santa-method)' — and counter-claims 'in ONE pass'. Separated at both ends: reviewer COUNT and round COUNT."
    },
    {
      "sibling": "santa-method",
      "query": "the last review was red again, did it miss anything",
      "picked": "artifact-consistency-sweep",
      "why": "'did the review miss anything, the last review was red again, unconverged review' are verbatim triggers here; santa-method's answer to an unconverged review is another round, and its description says nothing about missed findings or contradictions. Clean, though 'unconverged review' is the one word that leans santa-method-shaped — it survives because the sweep pairs it with 'in ONE pass'."
    },
    {
      "sibling": "integration-contract-completeness",
      "query": "I added a parse path but not the matching serialize — is this change symmetric",
      "picked": "integration-contract-completeness",
      "why": "'symmetric or multi-variant contract', 'encode-without-decode' are its words; the sweep disclaims 'NOT the mirror sides of a CODE contract'. The discriminator that decides it is CODE vs artefact prose — the sweep's subjects are 'a skill, a runbook, a spec'."
    },
    {
      "sibling": "integration-contract-completeness",
      "query": "audit this artefact for completeness — what else should it touch",
      "picked": "integration-contract-completeness",
      "why": "Real residual overlap: 'audit the patch for completeness', 'what else should this touch' is its trigger, and both skills enumerate axes and report per-row verdicts ('covered, missing, or deliberately-narrow' vs the sweep's five verdicts). Only the word 'patch'/'CODE' separates them; a query about a non-code artefact's completeness has no deciding word on either side."
    },
    {
      "sibling": "oracle-weakening-audit",
      "query": "the suite went green but did we weaken an assertion",
      "picked": "oracle-weakening-audit",
      "why": "'assertion loosened', 'tolerance widened', 'snapshot re-recorded' are unique to it; the sweep disclaims 'NOT checks weakened to buy a green run'. No contest."
    },
    {
      "sibling": "oracle-weakening-audit",
      "query": "which step of this procedure is graded by nothing",
      "picked": "artifact-consistency-sweep",
      "why": "'which step is graded by nothing' is a verbatim trigger, and 'graded by nothing' is absent-check, not weakened-check; oracle-weakening-audit's every symptom presupposes a check that EXISTS and was loosened. Boundary asserted from both ends."
    },
    {
      "sibling": "receiving-code-review",
      "query": "a reviewer left feedback that seems technically questionable — what do I do",
      "picked": "receiving-code-review",
      "why": "'receiving code review feedback, before implementing suggestions' vs the sweep's disclaimer 'NOT acting on a reviewer's comments'. The sweep PRODUCES findings; this one CONSUMES them. Clean."
    },
    {
      "sibling": "receiving-code-review",
      "query": "review this whole skill for internal contradictions",
      "picked": "artifact-consistency-sweep",
      "why": "receiving-code-review never claims to perform a review; 'reviewed for internal contradictions in ONE pass' has no rival here."
    },
    {
      "sibling": "skill-contract",
      "query": "write the fields of this skill — what goes in the description",
      "picked": "skill-contract",
      "why": "'writing or rewriting the fields', 'the order fields are written in, why description is written last' — authoring verbs. The sweep's verb is 'has to be reviewed'."
    },
    {
      "sibling": "skill-contract",
      "query": "does this skill's description promise what its body doesn't do",
      "picked": "artifact-consistency-sweep",
      "why": "Closest undisclaimed collision. The sweep names it verbatim — 'does the description promise what the body does not' and the 'description-body' pair type — while skill-contract only offers 'a code check and an independent reader are applied to each field', which is per-field acceptance, not cross-field agreement. Decidable, but skill-contract is not named in the NOT-list and both are skill-shaped; one sentence of separation would harden it."
    },
    {
      "sibling": "verification-before-completion",
      "query": "about to claim this is done — prove it before committing",
      "picked": "verification-before-completion",
      "why": "'running verification commands and confirming output before making any success claims' is about executing the work; the sweep never claims to run anything, it reads text."
    },
    {
      "sibling": "verification-before-completion",
      "query": "before shipping this runbook, check its parts agree",
      "picked": "artifact-consistency-sweep",
      "why": "'A whole artefact is about to be measured or shipped and its parts must agree' vs verification's 'evidence before assertions'. Different objects: a claim about work vs a document's self-agreement."
    },
    {
      "sibling": "gate-verdicts (Scio)",
      "query": "what is this gate allowed to report when a check could not run",
      "picked": "gate-verdicts (Scio)",
      "why": "'when a check could not run', 'a boolean pass or fail', 'whether a gate is the real enforcement point' — it governs a grader's VERDICT VOCABULARY. The sweep is itself a grader, so it is a consumer of that rule, not a rival."
    },
    {
      "sibling": "gate-verdicts (Scio)",
      "query": "this checklist has a step nothing grades",
      "picked": "gate-verdicts (Scio)",
      "why": "Genuine ambiguity. gate-verdicts covers 'reviewing anything that grades output — a build gate... a checklist' and 'a status has to say what nobody actually verified'; the sweep covers 'find the expectation that grades it; none is ungraded'. The deciding word ought to be that the sweep FINDS the gap in one artefact while gate-verdicts DESIGNS what the gate may say — but neither description states that, and gate-verdicts names 'checklist' explicitly while the sweep does not. Undisclaimed, and it is the sweep that should disclaim, being the newer unit."
    },
    {
      "sibling": "validation-evidence (Scio)",
      "query": "make this checker return what it examined so 'found nothing' isn't 'did not run'",
      "picked": "validation-evidence (Scio)",
      "why": "It owns the mechanism outright — 'the one-row-per-examined-pair rule, the planned-count that makes invisible non-execution detectable'. The sweep's step 1 and step 6 ('the plan count the report is checked against', 'a report whose examined count is below its plan count says so on its face') are that same rule applied. Correct pick, but only because the query says 'this checker'."
    },
    {
      "sibling": "validation-evidence (Scio)",
      "query": "consistency sweep of this spec — report every pair examined with its verdict",
      "picked": "artifact-consistency-sweep",
      "why": "'Enumerates every step-rule, step-step, step-check, description-body, file-BOM and claim-rationale pair as a row' names the six pair types and the artefact; validation-evidence names no artefact and no pair type. The scope word 'a whole artefact' decides it — but the shared vocabulary (row per examined pair, planned count) is the strongest lexical overlap in the whole set, and neither description names the other."
    }
  ],
  "symptom_words": [
    "did the review miss anything",
    "the last review was red again",
    "review the whole skill",
    "does the body contradict the rules",
    "does a step end in nothing checkable",
    "which step is graded by nothing",
    "does the description promise what the body does not",
    "is a named file missing",
    "a skill, a runbook, a spec",
    "steps vs rules vs evals"
  ],
  "solution_words": [
    "consistency sweep",
    "unconverged review",
    "step-rule",
    "step-step",
    "step-check",
    "description-body",
    "file-BOM",
    "claim-rationale",
    "pair as a row with a verdict and a quote",
    "findings list",
    "per-step matrix"
  ],
  "verdict": "pass",
  "reasons": [
    "Symptom-first: the opening clause and the whole Triggers sentence are phrased as a person would type them ('did the review miss anything', 'the last review was red again', 'which step is graded by nothing'). The solution vocabulary is quarantined in the third sentence, where it describes output rather than carrying the trigger load — the correct split.",
    "Two solution words are pure internal jargon nobody will ever type: 'file-BOM' and 'claim-rationale'. They cost description budget and earn nothing as triggers; 'unconverged review' is borderline, though it usefully pulls the santa-method-adjacent query toward the right unit.",
    "santa-method is separated at both ends: the sweep says 'in ONE pass' and 'NOT two adversarial reviewers converging over rounds (santa-method)', and santa-method independently says 'converging until both pass'. Reviewer count and round count are the discriminators, and both are quotable. Requirement met.",
    "All four named NOT-siblings (santa-method, integration-contract-completeness, oracle-weakening-audit, receiving-code-review) route correctly in both directions on their own triggers and this skill's.",
    "Length is ~1006 characters against the 1024 cap — under, but with under 20 characters of headroom, so any future edit overflows. Dropping 'file-BOM and claim-rationale' from the pair list would buy ~30 characters at no trigger cost.",
    "Weakest boundary is gate-verdicts (Scio), which is not disclaimed: it explicitly names 'a checklist' and 'a status has to say what nobody actually verified', against this skill's 'which step is graded by nothing'. A query about an ungraded checklist step has no deciding word on either side. Recommend the sweep disclaim it (finds the gap in one artefact vs decides what a gate may report).",
    "Second-weakest is validation-evidence (Scio), which owns the row-per-examined-pair and planned-count mechanism this skill's steps 1 and 6 apply. Currently decidable only by scope ('a whole artefact' vs 'a checker'). Not a router failure, but neither description names the other — a one-sided or absent link that will bite as the library grows.",
    "skill-contract overlaps on 'description promises what the body does not' but loses on verbs (writing/rewriting vs has to be reviewed); worth a brief mention if characters are freed up."
  ]
}
```

Two notes outside the JSON: the character count is a hand count (the `wc` call wasn't approved), so treat ~1006 as ±15 — either way the headroom is thin enough to be worth trimming. And the three unnamed neighbours that matter (gate-verdicts, validation-evidence, skill-contract) all sit in the "decidable but undisclaimed" band; none of them flips a router today, which is why this is a pass rather than red.