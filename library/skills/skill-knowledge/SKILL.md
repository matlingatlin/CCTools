---
name: skill-knowledge
description: Use when deciding whether a skill needs knowledge fetched from outside, and when gathering, quoting, verifying and reconciling claims from papers, documentation, repositories or web pages before they are bundled into an artefact. Covers the coverage check that decides whether to fetch at all, why a claim without a verbatim quote is not a finding, and why whoever gathered a source does not rule on their own gathering.
license: internal
---

# Knowledge that gets bundled

A skill carries its domain knowledge bundled at authoring time, not fetched at run
time. That makes the knowledge cheap and reliable, and it makes it go stale silently:
nothing in the runtime will ever tell you a bundled figure is out of date.

## Important — the fetch question is asked twice, about different things

Whoever proposed the artefact fetched what made the idea worth building. That is not
the same question as what the *observed* gap shows is missing, and the second question
cannot be asked before the probe has run. Ask it after, against the failures the probe
actually produced.

## Steps

**Coverage check first, and log the answer either way.** For each observed failure,
ask whether the claims already in hand cover it. If they do, do not fetch — and record
that the fetch was skipped and why. A skipped fetch and a fetch that was never
considered leave the same trace in a record that logs only what happened.

**Bound the questions before searching.** Write the question list, and write the
out-of-scope list beside it with a reason per entry. Without the second list, every
interesting adjacent finding looks like it belongs.

**Gather as rows, never prose.** One row per claim: the claim, the source, where in the
source, and the verbatim line. A paragraph hides which sentence carries the finding, so
nobody can check it later without re-reading everything.

**No quote, no finding.** This is the gate the rest depends on. Without a verbatim line
a claim is indistinguishable from a reconstruction, and reconstructions drift in the
direction that flatters the argument they were recalled to support.

**Two verdicts, and they are not strong and weak.** *Measured* means a study with
numbers exists and someone read it — so it carries what was measured, the effect and
the sample. *Repeated* means widely asserted with no measurement found. A claim is not
promoted by being asserted more often.

**Someone else verifies.** Whoever gathered a source does not rule on their own
gathering. The verifier returns one of: supported · not supported · not in the source ·
source unreachable · not checkable. The last two are results, not gaps in the process.

**Reconcile into one set.** Merge duplicates. Keep contradictions as their own rows —
collapsing them to the more convenient side is the one edit that cannot be detected
afterwards. Sort by verdict so a reader sees what is measured before what is repeated.

**Date everything, and say what would make it wrong.** Each source carries the date it
was fetched; each claim carries the condition under which it expires. That is the only
mechanism you get for staleness.

`references/claim-rows.md` has the row shape, the verdicts, and what a verifier is
given.

## In this repo (one instance)

Claim rows and their verification outcomes go to `pipeline/ledgers/claims.jsonl`;
verified findings land in `knowledge/notes/` in the same turn they are verified, not
when someone asks for them.
