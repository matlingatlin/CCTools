# The capability map: 25 lines cut, and three of them were doing real work — 2026-09-12

**The question, standing since 2026-09-11:** `CLAUDE.md`'s capability map cost **3,886 tokens every
turn**, 67.4% of the file, and named 91 of the 92 talents whose own descriptions are *already loaded*
above it. `CLAUDE.md` states the map's own charter: it is a second routing index, *"paid every turn —
it earns that only through the cross-library discriminators a single description cannot carry."* The
item was open because trimming it changes routing.

## The test, which is the charter made checkable

For each map line: strip the backticked names, and ask whether any **content word** in the line is
absent from the owning talent's own `description`. A line whose words are all already loaded
carries nothing — it cannot change which talent is chosen, because selection reads descriptions.

**Measured over 83 entries (15,124 B):**

| | entries | bytes |
|---|---|---|
| name at least one **sibling** talent (a boundary — the charter's case) | 36 | 9,267 |
| name no sibling | 47 | 5,857 |
| …of those, adding **≤2 words** over their own description | 26 | 2,228 |

## What was cut, and the two the test got wrong

**25 entries, 2,158 bytes.** One of the 26 was spared on inspection: *"Author a talent from the right
scaffold → `templates/`"* points at a **directory, not a talent**, so it has no description to be
redundant with. The predicate found it "redundant" only because it compared against the empty
string — a false positive of exactly the shape this repo keeps finding, where an absent value and a
zero value are treated as the same answer.

Then the **no-op test**, run after the cut rather than assumed: for each cut line, are the job words
it used present in the talent's own description? **21 of 25 clean. Four were not**, and the ≤2
threshold is why — a *count* of novel words cannot tell a connective from a trigger keyword:

| cut line's word | missing from | resolution |
|---|---|---|
| `done` | `verification-before-completion` (said "complete, fixed, or passing") | **added to the description** |
| `handoff` | `unified-memory` (said "hand off" as two words) | **added** |
| `improve` | `wave-reflect` (said "self-improving" — not a substring) | **reworded to "improve itself"** |
| `edit` | `writing-skills` | **nothing added — the map line was a MISROUTE** |

That last row is the find. The map said *"Author / **edit** a skill → `writing-skills`"*, and
`writing-skills`' own description says *"Use when AUTHORING a new skill **from scratch**"* and
explicitly **NOT** for sharpening an existing one, which is `skill-description-optimizer`'s job.
**The map had been routing "edit a skill" to the talent whose description refuses it** — for as long
as that line existed. Cutting the line removed the misroute; adding the keyword would have entrenched
it.

**Where the three keywords went is the point.** Into the **descriptions**, not back into the map. The
description is what the router actually reads, it is portable to any project, and it costs 5-10
characters against a line's 60-100 — so the same routing coverage now lives in the surface that was
already paid for. A map line is the most expensive place in this repo to keep a keyword.

## And two entries were carrying status, not routing

`artifact-consistency-sweep` spent 671 bytes on three builds' history and per-review finding counts;
`capability-routing-table` on its unvalidated premise. Both trimmed to the routing fact plus a pointer
at the document that owns the detail (its `evals.md`, its premise section). **A per-turn steering doc
is the worst possible home for a number that changes**, which is this repo's own
`steering-doc-pruning` lesson applied to itself.

## Result

| | before | after |
|---|---|---|
| `CLAUDE.md` | 23,073 B · ~5,768 tok | **20,894 B · ~5,223 tok** |
| the map | 15,544 B · ~3,886 tok (67.4%) | **13,365 B · ~3,341 tok (64.0%)** |
| always-on total | ~22,626 tok · 2.26% | **~22,082 tok · 2.21%** |
| talents named in the map | 91 of 92 | **78 of 92** |

**545 tokens per turn**, and the structural change matters more than the number. The map now says at
the top that it is **not an index** and that **absence means "no discriminator needed", never "no
talent for this"** — which is the failure `capability-routing-table` is built to find ("units that
fell out of the table"), and cutting 25 lines without saying so would have created it.

## The rule a future line has to pass

A map line earns its tokens if it names a **sibling talent** and says which of the two owns a job, or
states a boundary/chain no single description can. A line that only restates its own talent's
description belongs in the description. A line carrying a **date, a count, or a build outcome**
belongs in `BRAIN.md`, `BACKLOG.md` or the unit's own `evals.md`.

**Numbers here are computed, never copied:** `python3 pipeline/queries/context_surface.py`.
