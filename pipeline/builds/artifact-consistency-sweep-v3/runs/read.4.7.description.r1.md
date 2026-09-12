Read both files. Description length: **927 chars** (line is 943 bytes including `description: "…"` wrapper and newline) — under the 1024 cap, with ~97 chars of headroom.

```json
{
  "collisions": [
    {
      "sibling": "santa-method",
      "query": "(a) \"I need this output to clear two reviewers who argue until they both pass\"",
      "picked": "santa-method",
      "why": "santa-method owns it by its own words \"two independent adversarial reviewers, converging until both pass\"; the sweep explicitly disclaims it with \"NOT two adversarial reviewers converging over rounds\". Separation is two-sided in substance (rounds/agents vs \"in ONE pass\") though only the sweep names the boundary."
    },
    {
      "sibling": "santa-method",
      "query": "(b) \"the last review was red again — did the review miss anything in this skill?\"",
      "picked": "artifact-consistency-sweep",
      "why": "The sweep quotes these as literal triggers: \"did the review miss anything, the last review was red again\", plus \"in ONE pass\" and \"Ledgers every pair it ruled on\". santa-method has no re-review or missed-finding vocabulary; its scope is a pre-ship gate (\"before it ships\"). Clean pick."
    },
    {
      "sibling": "validation-evidence (Scio)",
      "query": "(a) \"my checker reports clean — make it show what it actually examined\"",
      "picked": "validation-evidence (Scio)",
      "why": "TIGHTEST PAIR. The sibling owns \"designing what a check returns rather than what it concludes\" and \"the one-row-per-examined-pair rule, the planned-count\". But the sweep advertises nearly the same machinery — \"Ledgers every pair it ruled on\", \"a per-step matrix\" — so a router reading both sees pair-ledger vocabulary twice. Decided only by object: a checker being designed vs an artefact being reviewed."
    },
    {
      "sibling": "validation-evidence (Scio)",
      "query": "(b) \"review this runbook for internal contradictions and show every pair you ruled on\"",
      "picked": "artifact-consistency-sweep",
      "why": "\"a skill, a spec, a runbook\", \"internal contradictions\", \"does the body contradict the rules\" appear only here; validation-evidence never names an artefact under review. The sweep's \"NOT designing what a checker returns\" carries the boundary one-directionally."
    },
    {
      "sibling": "skill-contract",
      "query": "(a) \"write/rewrite my SKILL.md fields — which field first, and what goes in the description?\"",
      "picked": "skill-contract",
      "why": "\"writing or rewriting the fields\", \"the order fields are written in, why description is written last\". The sweep disclaims with \"NOT writing a skill's fields\" and only READS the description (\"does the description promise more than the body\")."
    },
    {
      "sibling": "skill-contract",
      "query": "(b) \"review the whole skill — do its steps and rules agree?\"",
      "picked": "artifact-consistency-sweep",
      "why": "\"Triggers on review the whole skill, consistency sweep\" and \"do two steps contradict each other\". Residual risk: skill-contract also reviews (\"a code check and an independent reader are applied to each field\"), so both match \"check my skill\" — split is per-field-authoring vs whole-artefact-pairs, and skill-contract does not name the sweep back."
    },
    {
      "sibling": "receiving-code-review",
      "query": "(a) \"a reviewer left comments I think are wrong — what do I do before implementing them?\"",
      "picked": "receiving-code-review",
      "why": "\"receiving code review feedback, before implementing suggestions\". The sweep disclaims with \"NOT acting on a reviewer's comments\". Mild pull risk from the sweep's \"the last review was red again\", which mentions a prior review; resolved because the sweep re-reads the artefact, not the comments."
    },
    {
      "sibling": "receiving-code-review",
      "query": "(b) \"the review came back red twice — sweep the artefact myself\"",
      "picked": "artifact-consistency-sweep",
      "why": "\"consistency sweep\", \"Ledgers every pair\"; receiving-code-review has no artefact-internal or pair vocabulary."
    },
    {
      "sibling": "oracle-weakening-audit",
      "query": "(a) \"suite went green — did we weaken an assertion to get there?\"",
      "picked": "oracle-weakening-audit",
      "why": "\"an assertion loosened\", \"a numeric tolerance widened\", \"just get it green\". Sweep disclaims: \"NOT checks weakened for a green run\". No overlap in symptoms."
    },
    {
      "sibling": "oracle-weakening-audit",
      "query": "(b) \"which step in this procedure is graded by nothing?\"",
      "picked": "artifact-consistency-sweep",
      "why": "\"does a step end in nothing checkable, which step is graded by nothing\" — unique to the sweep; oracle-weakening-audit is about a red-to-green CI transition, not a step with no check."
    },
    {
      "sibling": "integration-contract-completeness",
      "query": "(a) \"added a parser but not the dumper — is this patch symmetric?\"",
      "picked": "integration-contract-completeness",
      "why": "\"symmetric or multi-variant contract\", \"encode-without-decode\". Sweep disclaims: \"NOT the mirror sides of a code contract\". Both use \"sweep\"/\"completeness\" language, but one sweeps a patch's variant axes, the other an artefact's step-rule pairs."
    },
    {
      "sibling": "integration-contract-completeness",
      "query": "(b) \"is a named file in this skill missing?\"",
      "picked": "artifact-consistency-sweep",
      "why": "\"is a named file missing\", \"does the repo section contradict a step\" — artefact-internal, not a code contract's other half."
    },
    {
      "sibling": "gate-verdicts (Scio)",
      "query": "(a) \"what is my build gate allowed to report when a check could not run?\"",
      "picked": "gate-verdicts (Scio)",
      "why": "\"Decide what a gate is allowed to report\", \"when a check could not run\". Sweep disclaims: \"NOT deciding what a gate may report\". Distinct."
    },
    {
      "sibling": "gate-verdicts (Scio)",
      "query": "(b) \"does the description promise more than the body delivers?\"",
      "picked": "artifact-consistency-sweep",
      "why": "\"does the description promise more than the body\" is quoted verbatim in the sweep; gate-verdicts governs a grader's output vocabulary, not an artefact's internal agreement."
    },
    {
      "sibling": "verification-before-completion",
      "query": "(a) \"about to say it's fixed — prove it\"",
      "picked": "verification-before-completion",
      "why": "\"requires running verification commands and confirming output\". Note: this is the ONE sibling the sweep's NOT list does not name, and the sweep's trigger \"did the review miss anything\" sits near a completion claim. Separation holds only because the sweep contains no run-a-command vocabulary — an implicit discriminator, not a stated one."
    },
    {
      "sibling": "verification-before-completion",
      "query": "(b) \"before shipping, do this spec's parts agree with each other?\"",
      "picked": "artifact-consistency-sweep",
      "why": "\"reviewed for internal contradictions\", \"does the body contradict the rules\"; verification-before-completion checks that work RAN, not that a document agrees with itself."
    }
  ],
  "symptom_words": [
    "review the whole skill",
    "consistency sweep",
    "did the review miss anything",
    "the last review was red again",
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
    "artefact (artifact)",
    "internal contradictions in ONE pass",
    "Ledgers every pair it ruled on",
    "findings with quotes",
    "a per-step matrix",
    "test assertions"
  ],
  "verdict": "pass",
  "reasons": [
    "927 chars, under the 1024 cap, with ~97 chars headroom — any future addition must displace, not append.",
    "Symptom-led: the middle third is a run of literal questions a person types ('which step is graded by nothing', 'is a named file missing') and four quoted trigger phrases. Solution vocabulary ('Ledgers every pair', 'per-step matrix') is present but sits after the symptoms, where it discriminates rather than gatekeeps.",
    "santa-method is separated in both directions on substance: 'in ONE pass' vs 'converging until both pass', plus the explicit 'NOT two adversarial reviewers converging over rounds'. No router query in the set lands ambiguously between them.",
    "Six of eight siblings are named in the NOT tail, and each NOT clause quotes the sibling's own distinguishing words ('mirror sides of a code contract', 'checks weakened for a green run', 'what a gate may report', 'what a checker returns') rather than naming skills by slug — which is what lets a router act on them.",
    "FLAG (not disqualifying): validation-evidence (Scio) is the tightest pair. Both descriptions advertise per-pair ledgering and planned counts; only the OBJECT differs (an artefact under review vs a checker being designed), and the boundary is asserted from one end only.",
    "FLAG: verification-before-completion is the only sibling absent from the NOT tail. Risk is low — no command-running vocabulary overlaps — but with 97 chars spare, the tail cannot absorb it without cutting an existing clause.",
    "FLAG: the leading parenthetical '(artefact) (artifact)' spends ~10 chars on a spelling variant; if headroom is ever needed, that is the cheapest cut."
  ]
}
```