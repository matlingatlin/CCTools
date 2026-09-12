# Data Contract Assertions

Profile a feed that is already arriving, derive an explicit contract from that profile, and
assert it at the ingest boundary before anything downstream reads the batch. Then do the part
that decides whether the contract is usable: take every difference between the arriving batch
and the reference and **split it** — the ones that stop the batch (a silent unit change, a
null-rate collapse, a type or key break) from the ones that **widen the contract** (a new
category, a new partner, a new market the producer legitimately added). Listing the differences
is not the deliverable; assigning each one to a side is, and every difference must land on
exactly one. A batch profiled correctly and then quarantined whole has moved the problem, not
solved it — the onboarding batch is the one that gets refused. Where a bound cannot be derived
from the data in hand, name what it depends on rather than supplying a number that looks
principled.

## When to use
- You depend on a dataset you do not produce, and its producer can change it without telling you.
- A batch has landed and you have a prior batch, a sample, or a reference table to compare it to.
- Someone found bad numbers downstream and the question is "how long has this been wrong?"
- A check went red and nobody can say whether the producer broke something or changed something
  on purpose — and the batch is being held while that is argued.
- You are writing dbt tests, Great Expectations suites, Soda checks or SQL assertions over an
  incoming feed and do not know which to write or where to put the bounds.
- Someone has asked what drift threshold to set, or what number the alert should fire at.
- A feed has a stated SLA (landed by a time, no staler than some lag) that nothing enforces.
- Existing data-quality alerts are noisy enough that people mute, snooze, or ignore them.
- The producer has announced a change — a new column, a renamed field, an added category — and
  the existing checks have to survive it without being switched off.

**When NOT to use:** validating a model's own output against a declared schema
(`structured-llm-extraction`); choosing which production examples become an eval set
(`eval-set-curation`); sweeping the mirror sides of a code contract inside a patch
(`integration-contract-completeness`); reviewing training or serving code in a diff
(`mlops-production-review`); cheap bulk field parsing with an LLM on the tail
(`hybrid-parse-escalation`); auditing an implementation against an external spec
(`external-domain-audit`). This talent inspects the *data that arrives*, not the code that
produces or consumes it.
