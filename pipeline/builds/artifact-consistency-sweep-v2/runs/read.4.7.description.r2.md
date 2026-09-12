Read both files. Description length: **1018 chars** (the quoted value; 1020 with quotes) — under 1024, but with only ~6 chars of headroom, which matters for the fix below.

```json
{
  "collisions": [
    {
      "sibling": "santa-method",
      "query": "(a) this output has to clear two independent adversarial reviewers before it ships",
      "picked": "santa-method",
      "why": "santa-method owns \"two independent adversarial reviewers, converging until both pass\"; the sweep's own text forecloses it twice — positively with \"reviewed for internal contradictions in ONE pass\" and negatively with \"NOT two adversarial reviewers converging over rounds (santa-method)\". The ONE-pass/over-rounds axis is the decider and it is stated from both ends. Separated."
    },
    {
      "sibling": "santa-method",
      "query": "(b) review the whole skill for internal contradictions, the last review was red again",
      "picked": "artifact-consistency-sweep",
      "why": "\"review the whole skill\", \"the last review was red again\", \"internal contradictions\" are verbatim triggers here; santa-method names no artefact parts, no contradictions, and gates shipping rather than enumerating pairs."
    },
    {
      "sibling": "validation-evidence (Scio)",
      "query": "(a) make the checker report what it examined so \"found nothing\" can't be mistaken for \"did not run\"",
      "picked": "AMBIGUOUS — should be validation-evidence",
      "why": "REAL, UNMITIGATED. validation-evidence claims exactly this mechanism: \"the one-row-per-examined-pair rule, the planned-count that makes invisible non-execution detectable\". This description advertises the same vocabulary — \"Rules on every pair; emits the ledger of examined pairs\" plus step 1's plan counts — and adds the trigger \"did the review miss anything\", which is the same worry in user words. Nothing in either description states the discriminator: validation-evidence DESIGNS what any checker returns; this one RULES on one artefact's pairs and emits a ledger as a byproduct. It is the only sibling with no NOT-clause here."
    },
    {
      "sibling": "validation-evidence (Scio)",
      "query": "(b) review this runbook for internal contradictions between its rules and its steps",
      "picked": "artifact-consistency-sweep",
      "why": "Safe in this direction: \"a skill, a spec, a runbook\", \"does the body contradict the rules\", \"do two steps contradict each other\" have no counterpart in validation-evidence, which names \"a validator, rule set, scan or conformance pass\" and never a contradiction."
    },
    {
      "sibling": "gate-verdicts (Scio)",
      "query": "(a) decide whether my reviewer may report a boolean pass/fail when a check could not run",
      "picked": "gate-verdicts",
      "why": "gate-verdicts owns \"what a gate is allowed to report and when a pass is reachable\", \"someone proposes a boolean pass or fail\". The sweep's closing clause \"NOT deciding what a gate or checker may report\" mirrors it almost word for word — but it is the ONLY NOT-clause that does not name its sibling in parentheses, so the exclusion is legible to a reader and weaker to a name-matching router."
    },
    {
      "sibling": "gate-verdicts (Scio)",
      "query": "(b) rule on every pair in this spec and tell me which step is graded by nothing",
      "picked": "artifact-consistency-sweep",
      "why": "\"which step is graded by nothing\", \"per-step matrix\" are here only; gate-verdicts governs a gate's verdict vocabulary, not an artefact's internal pairs."
    },
    {
      "sibling": "integration-contract-completeness",
      "query": "(a) I added a parse path but not the dump — did I miss the other half?",
      "picked": "integration-contract-completeness",
      "why": "\"one side of a symmetric or multi-variant contract\", \"encode-without-decode\" decide it; the sweep excludes it as \"NOT a code contract's mirror sides\". Residual risk: their trigger \"did I miss the other half\" and this one's \"did the review miss anything\" are near-homophones. The saving discriminator is the object — \"a patch\" vs \"a whole artefact that has a procedure, rules and test assertions - a skill, a spec, a runbook\" — which is stated positively here, so it holds."
    },
    {
      "sibling": "oracle-weakening-audit",
      "query": "(a) green build but did we weaken anything — the assertion got loosened",
      "picked": "oracle-weakening-audit",
      "why": "\"red to green and the change landed on the CHECK\", \"I relaxed the assertion\"; excluded here as \"NOT checks weakened for a green run (oracle-weakening-audit)\". Note both descriptions use \"red\" — \"the last review was red again\" vs \"CI is red before the release\" — but review-vs-CI and contradiction-vs-loosened-assertion separate them cleanly."
    },
    {
      "sibling": "receiving-code-review",
      "query": "(a) a reviewer left feedback I think is wrong — how do I respond?",
      "picked": "receiving-code-review",
      "why": "\"receiving code review feedback, before implementing suggestions\"; excluded as \"NOT acting on review comments (receiving-code-review)\". No overlap: this sweep PRODUCES review findings, it never consumes them."
    },
    {
      "sibling": "skill-contract",
      "query": "(a) write the frontmatter and description for this new skill",
      "picked": "skill-contract",
      "why": "\"writing or rewriting the fields of a Claude Code skill\"; excluded as \"NOT writing a skill's fields (skill-contract)\". The verb split write-vs-review carries it, despite both descriptions containing \"skill\" and \"description\"."
    },
    {
      "sibling": "verification-before-completion",
      "query": "(a) I'm about to say this is done — check it first",
      "picked": "verification-before-completion",
      "why": "\"about to claim work is complete... requires running verification commands\". Not named in this description's NOT list, but the objects differ sharply: running commands to prove YOUR work passes vs reading one artefact's parts against each other. Acceptable as-is; lowest-priority gap."
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
    "Rules on every pair",
    "ledger of examined pairs",
    "findings with quotes",
    "per-step matrix",
    "artefact",
    "procedure, rules and test assertions"
  ],
  "verdict": "red",
  "reasons": [
    "PASS on the santa-method separation asked about: the one-pass/over-rounds axis is stated from both ends — positively (\"reviewed for internal contradictions in ONE pass\") and negatively (\"NOT two adversarial reviewers converging over rounds (santa-method)\"). A router picks santa-method for a two-reviewer ship gate and this for a one-pass contradiction review.",
    "PASS on symptom vocabulary: the trigger block is unusually strong — nine of the eleven cues are questions a person actually types about a document (\"did the review miss anything\", \"which step is graded by nothing\", \"is a named file missing\"), not method names. Solution vocabulary is confined to the tail (\"ledger\", \"per-step matrix\"), where it describes outputs rather than gating retrieval.",
    "PASS on length: 1018 chars of description content, under the 1024 cap — but with ~6 chars spare, so any fix must trade text out, not add.",
    "RED: the collision with validation-evidence (Scio) is real and completely unmitigated. That sibling's description claims \"the one-row-per-examined-pair rule, the planned-count that makes invisible non-execution detectable\"; this description advertises \"Rules on every pair; emits the ledger of examined pairs\" and the trigger \"did the review miss anything\". Same mechanism, same words, no NOT-clause, no stated discriminator. It is the one sibling in the file the description does not address in any direction.",
    "The fix, within budget: state the object split rather than adding a tenth NOT-clause. Replace \"Rules on every pair; emits the ledger of examined pairs\" with something like \"Rules on every pair of ONE artefact; emits its ledger\" and spend the freed characters naming validation-evidence in the existing gate clause (\"NOT designing what a checker returns (validation-evidence)\"). Something must be cut to pay for it — the weakest candidate is \"does the repo section contradict a step\", the most repo-shaped of the nine cues.",
    "Secondary: the final clause \"NOT deciding what a gate or checker may report\" is the only exclusion that does not name its sibling, while every other one does. gate-verdicts should be named in parentheses for consistency with the rest of the field.",
    "Secondary (retrievability, not routing): the description spells the object \"artefact\" throughout while the skill's own name is artifact-consistency-sweep. A user typing \"review this artifact for contradictions\" matches the name but not a single word of the body. Worth carrying one \"artifact\" spelling if characters can be found."
  ]
}
```