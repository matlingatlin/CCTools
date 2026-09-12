# 13 descriptions exceed the spec's 1,024 characters — decided 2026-09-12

**The question, standing since 2026-09-11:** the Agent Skills specification says a `description`
*"Must be 1-1024 characters"*, and 13 of this library's 92 are longer, from 1,037 to 1,446. This
gate's own target is **1,230**, frozen against the host's silent **1,536** truncation wall — a
different constraint answering a different failure. The item was left open because trimming a
description changes **routing**, which this library's own rule says must be proven against a
baseline, and no baseline existed.

## The source, quoted rather than remembered

From the held copy, `knowledge/raw/baseline-2026-09-04/agentskills.io_specification.html`:

> The required `description` field: **Must be 1-1024 characters** · Should describe both what the
> skill does and when to use it · **Should include specific keywords that help agents** …

and the frontmatter table: *"description · Yes · **Max 1024 characters.** Non-empty."*

Both sentences matter. The same field is capped at 1,024 **and** asked to carry the keywords that
make it findable, and this library's house style takes the second instruction seriously: triggers
only, keyword-rich, plus explicit NOT-clauses naming the sibling that owns each neighbouring job.

## The measurement that settles it

Two questions were asked of the overage, in this order.

**1. Is any of it redundant?** For each of the 13, every quoted trigger phrase was tested: could it
be deleted with **no content word lost** from the description as a whole? **In 12 of 13, the answer
was zero phrases.** Every quoted trigger contributes at least one word nothing else in that
description carries. The overage is not a list of restatements.

**2. Could a rewrite reach 1,024 while keeping every content word?** `lossless_floor()` answers it:
strip every connective word and rejoin with single spaces — the shortest the description could
possibly be with its whole keyword surface intact. It is a bound, not a target; real prose needs
some of those words back.

| unit | chars | zero-loss floor | slack to 1,024 |
|---|---|---|---|
| `data-contract-assertions` | 1446 | 1180 | **−156** |
| `llm-eval-harness` | 1445 | 1231 | **−207** |
| `oracle-weakening-audit` | 1442 | 1132 | **−108** |
| `expand-contract-migration` | 1374 | 1152 | **−128** |
| `stage-ablation-attribution` | 1296 | 1049 | **−25** |
| `agent-fault-injection` | 1222 | 1035 | **−11** |
| `llm-redteam-scan` | 1208 | 1040 | **−16** |
| `metric-driven-prompt-optimization` | 1210 | 1012 | +12 |
| `structured-llm-extraction` | 1194 | 981 | +43 |
| `mlops-production-review` | 1147 | 990 | +34 |
| `idempotent-action-design` | 1126 | 927 | +97 |
| `source-grounded-implementation` | 1060 | 863 | +161 |
| `llm-judge-calibration` | 1037 | 862 | +162 |

**Seven of the thirteen are above the spec's maximum with every connective word already deleted.**
For those, complying is not a formatting fix — it requires removing a word the router matches on.
That is a capability cut, and it is the finding the character count alone could never show.

## Decision: do not trim. Report per unit instead.

1. **Trimming the seven is a measured loss against an unmeasured gain.** The harm is known — a
   deleted trigger or NOT-clause is a routing keyword gone. The benefit is compliance with a limit
   **this host does not enforce**: all 13 load and trigger today, and the host's own behaviour is
   to truncate at 1,536, not to reject at 1,024.
2. **Trimming only the six that can comply buys nothing.** A conforming host rejects on the first
   violation regardless of how many others were fixed, so partial compliance leaves the library
   exactly as unusable there while changing routing for six skills that work. **Half a migration is
   worse than either end of it.**
3. **The risk is real and is portability, not correctness** — CLAUDE.md's standing rule is that a
   talent must be usable in any project, and seven of these cannot be, on a conforming host,
   without being made worse. That is worth knowing precisely, which is why it is now reported per
   unit with its floor rather than as a count.

**What would reopen this**, so the decision is recoverable rather than merely made: a host that
actually rejects at 1,024, or a house style that moves NOT-clauses somewhere the router still
reads. The second is the real fix and it is not available today — the description IS the routing
surface; a body is not read until the skill has already been chosen.

## What shipped

`pipeline/queries/desc_headroom.py --gate` now prints each over-spec unit with its length, its
zero-loss floor and its slack, marks the ones that cannot comply, and names this file. Still
**reporting only** — it does not gate, because moving a preregistered threshold after seeing a
result is what preregistration exists to prevent, and a reporting line is not a threshold.

`lossless_floor()` is a pure function with 5 fixtures and 4 mutations. The first version of its
compound-token fixture **let a mutation through**: a separator *between* two words is length-neutral
when split, one character becoming one space, so `CSV/JSON` cannot tell the two implementations
apart. The case that can is punctuation at a token's **edge**, which splitting drops. 21 fixtures
total, no survivors.
