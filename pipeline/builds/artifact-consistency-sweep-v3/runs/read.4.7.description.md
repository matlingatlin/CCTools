Read the description (line 3, 955 chars of value) and all 8 siblings. Here's the review.

```json
{
  "collisions": [
    {
      "sibling": "validation-evidence (Scio)",
      "query": "(a) neighbour's job — \"my validator reported clean; make it return what it examined so found-nothing can't be mistaken for did-not-run\"",
      "picked": "validation-evidence, but only narrowly",
      "why": "Neighbour owns \"one-row-per-examined-pair rule, the planned-count that makes invisible non-execution detectable\". This skill's description claims the SAME machinery verbatim in kind: \"Rules on every planned pair of one artefact's parts; emits its ledger of examined pairs\". Nothing in either description separates them, and neither names the other in a NOT clause. The only discriminator a router has is this skill's object — \"a whole artefact ... a skill, a spec, a runbook\" and \"internal contradictions\" — versus the neighbour's \"a validator, rule set, scan or conformance pass\". That is inferred, not asserted. This is the one boundary claimed from neither end."
    },
    {
      "sibling": "validation-evidence (Scio)",
      "query": "(b) this skill's job — \"review the whole skill, did the review miss anything\"",
      "picked": "artifact-consistency-sweep",
      "why": "\"review the whole skill, consistency sweep, did the review miss anything, the last review was red again\" are literal typed strings only this description carries; the neighbour has no review-an-artefact trigger. Direction (b) is safe; direction (a) is the leak."
    },
    {
      "sibling": "santa-method",
      "query": "(a) \"output must clear two independent adversarial reviewers before it ships\"",
      "picked": "santa-method",
      "why": "Cleanly separated from both ends. Neighbour: \"two independent adversarial reviewers, converging until both pass\". This skill excludes it in the same words — \"NOT two adversarial reviewers converging over rounds\" — and asserts the opposite mode positively: \"reviewed for internal contradictions in ONE pass\". A router cannot cross this."
    },
    {
      "sibling": "santa-method",
      "query": "(b) \"the last review was red again — did it miss anything\"",
      "picked": "artifact-consistency-sweep",
      "why": "\"the last review was red again\" and \"Rules on every planned pair\" beat santa's ship-gate framing; santa says nothing about missed contradictions or coverage of parts."
    },
    {
      "sibling": "gate-verdicts (Scio)",
      "query": "(a) \"what is this build gate allowed to report when a check could not run\"",
      "picked": "gate-verdicts",
      "why": "Excluded by \"NOT deciding what a gate or checker may report\" — near-verbatim against the neighbour's \"Decide what a gate is allowed to report\". Separated, but from one end only: gate-verdicts does not name this skill back, so the boundary rests entirely on this description holding."
    },
    {
      "sibling": "gate-verdicts (Scio)",
      "query": "(b) \"does the description promise more than the body\"",
      "picked": "artifact-consistency-sweep",
      "why": "\"does the description promise more than the body, is a named file missing, does a rule have no rationale\" are artefact-part pairs; gate-verdicts governs a grader's verdict vocabulary, not an artefact's internal agreement."
    },
    {
      "sibling": "oracle-weakening-audit",
      "query": "(a) \"CI went red to green — did we weaken an assertion\"",
      "picked": "oracle-weakening-audit",
      "why": "\"NOT checks weakened for a green run\" excludes it explicitly. Residual friction: this skill's trigger \"the last review was red again\" sits close to the neighbour's \"CI is red before the release\" / 'green build but did we weaken anything'. \"internal contradictions\" and \"review\" (not suite/assertion) is what decides it — thinner than the other exclusions."
    },
    {
      "sibling": "integration-contract-completeness",
      "query": "(a) \"added a parse path but not the matching dump — is this change symmetric\"",
      "picked": "integration-contract-completeness",
      "why": "\"NOT the mirror sides of a code contract\" maps directly onto \"Sweeps the contract's mirror sides and variant axes\". Both are pair-sweeps, so the discriminator carries real weight — and it is the object that does it: a patch's variants vs \"one artefact's parts\"."
    },
    {
      "sibling": "skill-contract",
      "query": "(a) \"write the SKILL.md frontmatter, name, description, body against the field contract\"",
      "picked": "skill-contract",
      "why": "\"NOT writing a skill's fields\" vs \"writing or rewriting the fields of a Claude Code skill\". Clean. Note the shared surface: both reason about \"description\" vs body — but this skill only CHECKS agreement (\"does the description promise more than the body\"), never authors."
    },
    {
      "sibling": "receiving-code-review",
      "query": "(a) \"a reviewer left feedback — what do I do with it\"",
      "picked": "receiving-code-review",
      "why": "\"NOT acting on a reviewer's comments\" against \"receiving code review feedback, before implementing suggestions\". Clean."
    },
    {
      "sibling": "verification-before-completion",
      "query": "(a) \"about to claim this skill is done — has everything been checked\"",
      "picked": "ambiguous, leaning verification-before-completion",
      "why": "The neighbour owns \"about to claim work is complete ... running verification commands\" and carries two NOT clauses of its own, naming neither this skill. This description's \"about to be measured or shipped and its parts must agree\" is body text, not description text; in the description, only \"internal contradictions\" separates them. Second boundary asserted from neither end, though the collision is milder than validation-evidence's."
    }
  ],
  "symptom_words": [
    "review the whole skill",
    "consistency sweep",
    "did the review miss anything",
    "the last review was red again",
    "does the body contradict the rules",
    "do two steps contradict each other",
    "does the description promise more than the body",
    "is a named file missing",
    "does a rule have no rationale",
    "which step is graded by nothing",
    "a skill, a spec, a runbook"
  ],
  "solution_words": [
    "artefact (artifact)",
    "internal contradictions in ONE pass",
    "Rules on every planned pair of one artefact's parts",
    "emits its ledger of examined pairs",
    "findings with quotes",
    "per-step matrix",
    "does a step end in nothing checkable",
    "does the repo section contradict a step"
  ],
  "verdict": "red",
  "reasons": [
    "Length passes: 955 chars of description value (971-byte line including the `description: \"` wrapper), under the 1024 cap — but with only ~69 chars of headroom, which is a problem given the fix below needs a new NOT clause.",
    "santa-method IS separated, and separated well: 'reviewed for internal contradictions in ONE pass' asserts the mode positively and 'NOT two adversarial reviewers converging over rounds' excludes the neighbour in the neighbour's own words. This is the strongest boundary in the description.",
    "RED — validation-evidence (Scio) is the uncovered collision. The description sells this skill in that neighbour's exact machinery ('every planned pair', 'ledger of examined pairs') while the neighbour's own description claims 'the one-row-per-examined-pair rule, the planned-count that makes invisible non-execution detectable'. Six NOT clauses name six siblings; the one sibling sharing this skill's core vocabulary is named by neither side. A router asked to make a check report what it examined has no worded reason to prefer either.",
    "Symptom/solution balance is acceptable but the payload sentence is not. The trigger list is genuinely typed language ('did the review miss anything', 'the last review was red again') and the pair questions are phrased as symptoms rather than as pair-type jargon — good. But the closing claim sentence ('Rules on every planned pair ... per-step matrix') is pure solution vocabulary and is exactly where the validation-evidence overlap lives; it buys little routing power and costs the boundary.",
    "Two smaller one-way boundaries: gate-verdicts and oracle-weakening-audit are excluded from this end only, and verification-before-completion is not excluded at all despite owning the adjacent 'is it done / has it been checked' query.",
    "Suggested fix within the cap: compress 'Rules on every planned pair of one artefact's parts; emits its ledger of examined pairs, findings with quotes, per-step matrix' to something like 'Ledgers every pair it ruled on, with quotes', and spend the reclaimed chars on 'NOT designing what a checker returns' to close the validation-evidence gap."
  ]
}
```

The one thing to act on: six NOT clauses cover six siblings, and the sibling that shares this skill's own vocabulary — validation-evidence's planned-count and one-row-per-examined-pair — is the one nobody excluded.