---
name: wave-reflect
description: "Use at the end of every iteration of a repeating workflow (and read its output at the start of the next) to make the loop improve itself — record structured per-iteration metrics to a ledger, then derive deterministic lessons that steer future iterations. Computes yield by input/source type (what produces useful output vs waste), flags unused capabilities to prune and overlapping tool descriptions to sharpen, and emits directives the next iteration reads before it picks work. The measure→reflect→learn→read-back engine for any batch, wave, sprint, run, or harvest loop; git-native, deterministic, no server."
---

# wave-reflect — make a repeating loop better every iteration

A loop that only logs repeats itself. This method closes the feedback loop: each
iteration **measures** what it did, **reflects** those numbers into lessons, and the
**next iteration reads them back** before choosing what to work on. Git-native, no
server, and deterministic **given a pinned config** — the same data plus the same recorded
thresholds always yields the same lessons.

Works for any repeating workflow where each pass consumes inputs and produces outputs:
a data-harvest wave, a build/CI run, a research sprint, a content batch, an agent loop.
Below, "iteration" is one pass of the loop, an **input/source** is what a pass draws
from, and an **outcome** is what it produced (kept, adapted, dropped).

## When to use
- **End of every iteration:** append this iteration's metrics row and refresh the lessons file.
- **Start of every iteration (read-back):** read the lessons file plus the last ~10 rows of
  the metrics ledger, and let the lessons steer what work / which sources / which terms you pick.

## Part 1 — Record metrics (end of iteration)
Append ONE JSON line to a metrics ledger (an append-only `metrics.jsonl` or equivalent).
Adapt field names to your domain; a general schema:
```json
{"iter":N,"date":"YYYY-MM-DD","work_type":"<kind of work this pass did>",
 "source":"<what it drew from>","source_type":"<category of that source>",
 "seen":INT,"kept":INT,"adapted":INT,"promoted":INT,
 "rejected":{"<reason>":INT, "...":INT},
 "candidates":INT,            // outputs this pass HANDED ON to a later stage (producer work)
 "yield_rate":FLOAT,          // measure the pass by ITS OWN output: (kept or candidates)/max(seen,1)
 "used":["<capability/step/tool actually run>", ...],  // the chain this pass ran
 "wall_clock_s":INT,          // MEASURED elapsed time (a clock delta across the pass)
 "workers":INT,               // MEASURED count of parallel workers/agents spawned
 "cost_est":INT,              // honest estimate
 "cost_measured":INT|null,    // real spend if a meter exists; null (never faked) otherwise
 "sources_new":INT,           // how many inputs this pass ADDED to the queue (rule 4 needs it)
 "notes":"<one line>"}
```
`used` is the usage signal when you have no runtime telemetry — it is how the health
check below detects unused capabilities. Always fill it honestly. **Log measured time/worker
counts LIVE** — they can't be reconstructed after the pass; keep `cost_measured` `null`
rather than fabricate a number when no meter exists (an estimate dressed as measured poisons
the analysis). Cost, time, and any per-item lineage are the fields lost forever if skipped —
capture them now even if the analysis that consumes them is deferred until volume exists.

## Part 2 — Reflect into a lessons file (deterministic rules)

**Pin the parameters first, at the head of the lessons file.** The rules below are
domain-tunable — which is correct — but a tunable a reader cannot see is not deterministic,
it is arbitrary. Record the values you chose, and change them by editing this block, never
in your head:

```
CONFIG (pinned YYYY-MM-DD)
high_water: 0.50     # yield at or above this -> seek-more
low_water:  0.10     # yield below this, over >= min_iters -> deprioritize
min_iters:  2        # a verdict needs at least this many iterations of that type
window_N:   10       # exact integer, not "about 10" -- the usage window for rule 2
```

The honest claim is therefore **same data + same recorded config → same lessons** — not
"same data → same lessons". With the config unpinned, a high-water of 0.50 and one of 0.03
produce opposite verdicts from identical rows, and nothing in the output reveals which was used.
A directive derived below an unpinned threshold cannot be checked by anyone, including you.

Recompute and rewrite the derived sections of a lessons file (a plain `LESSONS.md` or
equivalent) from ALL metrics rows:

> **Measure each pass by its OWN output, not a downstream stage's.** A pass that PRODUCES
> inputs for a later stage (harvest, scout, triage) scores its yield on `candidates` handed on,
> never on what some later pass eventually kept. Scoring a producer by the consumer's outcome
> reads as 0.00 for work that was excellent, and rule 1 will then deprioritize your best source
> type on a metric that measured the wrong stage. Verified in this repo: two harvest waves over
> practitioner repos produced 10 candidate methods, 7 build-worthy, and were recorded
> `adopted: 0 → yield 0.00`, which computes to *deprioritize* — the exact opposite of the
> CONFIRMED lesson those same waves produced. The row's own note said "candidates queued for
> build"; the number did not. **When a computed verdict contradicts a lesson you trust, suspect
> the metric before you obey the rule.**

1. **Source-yield table.** Group rows by `source_type`; compute count, total seen, total
   kept, mean yield_rate. Verdict per type, using the pinned CONFIG above (never ad-hoc values):
   - yield ≥ `high_water` → **seek-more** (go find similar sources).
   - yield < `low_water` over ≥ `min_iters` iterations → **deprioritize** (push that shape down the
     queue; e.g. prefer deep-reading single primary sources over shallow aggregate lists).
2. **Capability health (auto-prune candidates).** Union `used` across the last `window_N`
   iterations (the exact integer from CONFIG — a capability used only in iteration 15 is a prune
   candidate at N=9 and not at N=10, so "about ten" is not a rule). Any adopted capability/tool/step in your inventory NOT used in that window →
   list as **review-for-prune** (maybe it never triggers, or isn't needed). Do NOT
   auto-delete — deletion is irreversible → human gate. Just flag it with the reason.
3. **Description precision.** Overlap is only actionable when it is **operational**, so apply
   this test rather than eyeballing prose: name a CONCRETE task whose correct handler is
   ambiguous between two capabilities. If you cannot name one, there is no finding — topic
   similarity alone is not overlap. Only pairs that pass this test are listed → **sharpen**
   (differentiate on TRIGGER, not topic; auto-allowed because it is reversible). Without the
   test this rule scales as pairs-squared (65 items = 2,080 pairs) and reliably produces nothing,
   which is exactly how it fails: silently, by never firing.
4. **Diminishing returns.** If the last `min_iters` iterations all have kept=0 AND
   `sources_new`=0 → write a **pause** directive (the loop stops chaining and asks a human).
   Both terms must be answerable from the ledger; a halt rule resting on a field you do not
   record cannot fire, and its silence looks identical to "things are fine".

## Part 3 — Emit directives the next iteration reads
At the top of the lessons file, keep a short **ACTIVE DIRECTIVES** list (imperative, dated),
e.g. `- [YYYY-MM-DD] deprioritize source_type=aggregate-list (yield 0.00 over 2 iters)` ·
`- sharpen: capability-A vs capability-B descriptions` · `- seek more single-source primary
inputs (type=X yield 0.10)`. The next iteration's read-back applies these before picking work;
whatever component chooses sources consumes the source-yield verdicts.

## Rules
- **Deterministic given a pinned config:** lessons are computed from metrics, not vibes —
  same data + same recorded CONFIG → same lessons. An unpinned threshold makes the output
  unrepeatable and unauditable, which is the same failure as vibes with extra steps.
- **Reversible only:** this method sharpens descriptions, reprioritizes queues, and flags
  prunes — it NEVER deletes anything or takes an irreversible action (human gate for those).
- **Read-back is mandatory:** metrics that no iteration reads back improve nothing. Step 1 of
  every iteration must consume the lessons file before choosing work.
- **Link lessons into your knowledge base** (wikilinks, doc refs, an index) so it grows with the loop.

## In this repo (one concrete instance)
The `/piano` harvest loop is one instance of this method. There, an iteration is a "wave",
the ledger is `pipeline/metrics.jsonl`, the lessons file is `pipeline/LESSONS.md`, sources are
GitHub repos / web-top-n / papers, outcomes are talents adopted into `.claude/skills/`, `used`
is `talents_used`, and it pairs with `skill-stocktake`, `research-scout`, and `learn-eval`.
Those are examples of the general roles above, not the only way to run this method.
