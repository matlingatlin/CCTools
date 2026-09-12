Reviewed the `description` field only, against all eight siblings.

```json
{
  "collisions": [
    {
      "sibling": "santa-method",
      "query": "this output has to clear two independent reviewers before it ships",
      "picked": "santa-method",
      "why": "sibling owns it on 'two independent adversarial reviewers, converging until both pass'; this skill cedes explicitly with 'NOT two adversarial reviewers converging over rounds' and claims the opposite mode in its positive half, 'in ONE pass'. Separation is stated from both ends and the two vocabularies (converge/rounds vs one pass) do not overlap."
    },
    {
      "sibling": "santa-method",
      "query": "review this whole skill for internal contradictions, the last review was red again",
      "picked": "artifact-consistency-sweep",
      "why": "'review the whole skill, consistency sweep, did the review miss anything, the last review was red again' are verbatim triggers here; santa-method's text names no artefact-internal contradiction, only a 'dual-agent adversarial gate'."
    },
    {
      "sibling": "validation-evidence (Scio)",
      "query": "make the checker return one row per pair it examined so 'found nothing' can't be mistaken for 'did not run'",
      "picked": "validation-evidence (Scio)",
      "why": "sibling is decided by 'designing what a check returns rather than what it concludes' and 'the one-row-per-examined-pair rule, the planned-count'. This skill routes away only on its final clause 'NOT designing what a checker returns' — its positive half ('Ledgers every pair it ruled on', 'a per-step matrix') uses the same per-pair/ledger vocabulary. Correct but the tightest row: the discriminator lives entirely in the NOT clause, not in the positive half."
    },
    {
      "sibling": "validation-evidence (Scio)",
      "query": "did this runbook's steps end in anything checkable, and which step is graded by nothing",
      "picked": "artifact-consistency-sweep",
      "why": "'does a step end in nothing checkable, which step is graded by nothing' is verbatim here and is a finding ABOUT an artefact; the sibling's subject is a checker's own return shape ('when a validator, rule set, scan or conformance pass reports clean')."
    },
    {
      "sibling": "oracle-weakening-audit",
      "query": "the build went green after I loosened an assertion — did we weaken anything",
      "picked": "oracle-weakening-audit",
      "why": "sibling owns 'an assertion loosened … a numeric tolerance widened … green build but did we weaken anything'; this skill cedes with 'NOT checks weakened for a green run'. Watch item: this skill's trigger 'the last review was red again' sits near the sibling's 'CI is red before the release'. The words that keep them apart are 'review' (a verdict on a text) vs 'suite'/'CI' (a test run) — carried, but only by that one noun."
    },
    {
      "sibling": "oracle-weakening-audit",
      "query": "the spec's rules and its test assertions disagree with each other",
      "picked": "artifact-consistency-sweep",
      "why": "'with or without test assertions … reviewed for internal contradictions' — the sibling only fires when a check CHANGED to buy green ('the change landed on the CHECK rather than on the behavior'); nothing changed here."
    },
    {
      "sibling": "skill-contract",
      "query": "write the description and body fields for this new skill",
      "picked": "skill-contract",
      "why": "sibling: 'writing or rewriting the fields of a Claude Code skill … why description is written last'. Ceded by 'NOT writing a skill's fields'."
    },
    {
      "sibling": "skill-contract",
      "query": "does this skill's description promise more than its body delivers",
      "picked": "artifact-consistency-sweep",
      "why": "verbatim: 'does the description promise more than the body'. Both descriptions name description+body; the discriminator is authoring vs auditing, and it is present on both sides ('writing or rewriting' vs 'has to be reviewed')."
    },
    {
      "sibling": "integration-contract-completeness",
      "query": "I added a parse path but not the dump path — did I miss the other half",
      "picked": "integration-contract-completeness",
      "why": "sibling: 'encode-without-decode, request-without-respon…', 'mirror sides and variant axes'. Ceded by 'NOT the mirror sides of a code contract'."
    },
    {
      "sibling": "receiving-code-review",
      "query": "a reviewer left comments I'm not sure about — should I implement them",
      "picked": "receiving-code-review",
      "why": "sibling: 'receiving code review feedback, before implementing suggestions'. Ceded by 'NOT acting on a reviewer's comments'. Note the near-word 'did the review miss anything' here is about a review THIS side ran, not incoming feedback."
    },
    {
      "sibling": "gate-verdicts (Scio)",
      "query": "what is this build gate allowed to report when the check could not run",
      "picked": "gate-verdicts (Scio)",
      "why": "sibling: 'Decide what a gate is allowed to report and when a pass is reachable at all'. Ceded by 'NOT deciding what a gate may report'."
    },
    {
      "sibling": "verification-before-completion",
      "query": "I'm about to say this is done — can I claim it passes",
      "picked": "verification-before-completion",
      "why": "sibling: 'about to claim work is complete … requires running verification commands'. This skill has NO negative clause naming it, but also no competing claim: it never mentions completion, commits, PRs or running commands. Low risk, uncovered by design rather than by wording."
    },
    {
      "sibling": "verification-before-completion",
      "query": "before shipping this runbook, do its parts agree with each other",
      "picked": "artifact-consistency-sweep",
      "why": "'has to be reviewed for internal contradictions in ONE pass' — the sibling verifies the WORK by running commands, this reads the text's parts against each other."
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
    "in ONE pass",
    "Ledgers every pair it ruled on",
    "findings with quotes",
    "a per-step matrix",
    "artefact (artifact)",
    "internal contradictions"
  ],
  "verdict": "pass",
  "reasons": [
    "939 chars of description content (line measures 955 bytes including the 'description: ' key, quotes and newline) — under the 1024 cap, but only ~85 chars of headroom, so any added NOT clause has to displace text rather than append.",
    "Symptom-led, not solution-led: eleven of the routable phrases are questions or complaints a person types ('did the review miss anything', 'the last review was red again', 'is a named file missing'); the solution vocabulary ('per-step matrix', 'ledgers every pair') is confined to one sentence of mechanism after the triggers, which is the right order.",
    "santa-method is separated cleanly and from both ends: 'NOT two adversarial reviewers converging over rounds' here, 'Dual-agent adversarial gate' with no internal-consistency claim there. The positive halves also differ on mode — 'in ONE pass' vs 'converging until both pass' — so the separation does not rest on the NOT clause alone.",
    "All six other siblings whose jobs could be confused are named by a NOT clause and route correctly in both directions.",
    "At-risk row 1 — validation-evidence (Scio): 'Ledgers every pair it ruled on' / 'per-step matrix' shares the sibling's 'one-row-per-examined-pair rule' vocabulary. Routing is only saved by the trailing 'NOT designing what a checker returns'. If that clause is ever trimmed for length, this becomes a genuine collision; consider making the positive half say the pairs are pairs OF AN ARTEFACT.",
    "At-risk row 2 — oracle-weakening-audit: 'the last review was red again' vs the sibling's 'CI is red before the release'. The only discriminating noun is review vs CI/suite. Not a fail, but the phrase that is closest to a false trigger.",
    "verification-before-completion is the one sibling with no NOT clause; acceptable here because there is zero vocabulary overlap, unlike the two rows above.",
    "Caution, not a fail: the description enumerates eight pair questions while the body states 'the seven pair types'. Whether two of the eight ('ends in nothing checkable' / 'graded by nothing') are one type is not decidable from the description field alone, but the count promised to a router should match the count the body defines."
  ]
}
```