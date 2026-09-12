---
name: systematic-debugging
description: Use when encountering a specific bug, test failure, build error, or unexpected behavior and tempted to fix it — enforces root-cause investigation before any fix. For one concrete defect; not aggregate error patterns across a dataset (error-analysis-taxonomy) or LLM agent trajectory debugging (agent-introspection-debugging).
---

# Systematic Debugging

## Overview

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

Use for ANY technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:**
- Issue seems simple (simple bugs have root causes too)
- You're in a hurry (rushing guarantees rework)
- Manager wants it fixed NOW (systematic is faster than thrashing)

## The Four Phases

You MUST complete each phase before proceeding to the next.

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages Carefully**
   - Don't skip past errors or warnings
   - They often contain the exact solution
   - Read stack traces completely
   - Note line numbers, file paths, error codes

2. **Build a Repro LOOP — and raise the reproduction RATE, don't punt on it**

   A single manual reproduction is not the goal; a fast, deterministic command you can re-run
   on demand is. **Hard gate: no already-run red command → no hypothesis.** If you cannot point
   at a command you have executed that fails right now, you are guessing, and Phase 3 is closed
   to you.

   Aim for a loop that is:
   - **Fast** — seconds, not minutes. Cut setup, fixtures, and unrelated suites until only the
     failing path remains. You will run this hundreds of times.
   - **Deterministic** — same input, same failure. A loop that fails sometimes cannot tell you
     whether your change helped.
   - **Sharp** — it fails for the reason you are chasing and nothing else, so a pass is evidence.

   **"Not reproducible" is a reproduction RATE, not a wall.** A bug that appears 1 run in 50 is
   reproducible at 2%; the job is to raise that number until the loop is useful. Ways to raise
   it, roughly in order of what to try first:
   1. Run it in a loop (`for i in $(seq 100)`) and count failures — establish the real rate before
      concluding anything.
   2. Narrow to the smallest failing unit — one test, one function, one request.
   3. Remove the parts that pass; every removal that keeps it red sharpens the signal.
   4. Run the loop in parallel to multiply attempts per minute.
   5. For races: inject sleeps or scheduling jitter at the suspected interleaving point.
   6. Pin the non-determinism you do not care about — fixed seed, frozen clock, fixed ordering.
   7. Force the unlikely branch directly (fault injection, a stub that fails) instead of waiting
      for it.
   8. Raise concurrency, load, or data volume if the failure is contention- or scale-shaped.
   9. Match the environment where it does reproduce (same version, same platform, same data).
   10. If it only fails in CI, make CI print state (Phase 1 step 4) and reproduce from that
       evidence rather than from imagination.

   Record the rate. A loop that went from 2% to 90% is the single highest-value artifact of a
   debugging session — but only if you use it twice.

   **The rate is the acceptance test for the FIX, not just for the loop.** Measure it three times,
   and say which you are quoting: before raising it, after raising it, and again on the patched
   code over the same number of runs. "The test passes now" is not evidence on a bug that was
   intermittent — it is what you would see anyway. A failure that reproduced 1 run in 50 gives a
   green single run 98% of the time with no fix at all; at the raised rate of 90%, one green run
   still happens 1 time in 10.

   So: re-run the loop the same number of times you used to establish the rate, and require the
   observed failures to drop to zero (or to a rate whose confidence interval excludes the old one).
   Quote both numbers when you claim the fix works — "0/200 after, 180/200 before" is a claim
   someone can check; "the test passes" is not. If you could not raise the rate and are shipping a
   mitigation, say that explicitly rather than letting a green run imply a root-cause fix.

   This closes an asymmetry that is easy to miss: entry to hypothesis is gated on measured
   evidence, so exit must be too. Otherwise the discipline stops exactly where the temptation
   starts.

   **Only when the rate cannot be raised at all** should you fall back to gathering more evidence
   (step 4's instrumentation). "Cannot be raised" is a claim that needs backing, not a feeling:
   name at least three of the techniques above that you actually tried and what each produced.
   Then say so explicitly, and go to the terminal branch below (`When Process Reveals "No Root
   Cause"`) rather than sliding into hypothesising without a red command — that branch is where a
   mitigation is legitimately shipped, and it requires the measured rate as its input too.

3. **Check Recent Changes**
   - What changed that could cause this?
   - Git diff, recent commits
   - New dependencies, config changes
   - Environmental differences

4. **Gather Evidence in Multi-Component Systems**

   **WHEN system has multiple components (CI → build → signing, API → service → database):**

   **BEFORE proposing fixes, add diagnostic instrumentation:**
   ```
   For EACH component boundary:
     - Log what data enters component
     - Log what data exits component
     - Verify environment/config propagation
     - Check state at each layer

   Run once to gather evidence showing WHERE it breaks
   THEN analyze evidence to identify failing component
   THEN investigate that specific component
   ```

   **Example (multi-layer system):**
   ```bash
   # Layer 1: Workflow
   echo "=== Secrets available in workflow: ==="
   echo "IDENTITY: ${IDENTITY:+SET}${IDENTITY:-UNSET}"

   # Layer 2: Build script
   echo "=== Env vars in build script: ==="
   env | grep IDENTITY || echo "IDENTITY not in environment"

   # Layer 3: Signing script
   echo "=== Keychain state: ==="
   security list-keychains
   security find-identity -v

   # Layer 4: Actual signing
   codesign --sign "$IDENTITY" --verbose=4 "$APP"
   ```

   **This reveals:** Which layer fails (secrets → workflow ✓, workflow → build ✗)

5. **Trace Data Flow**

   **WHEN error is deep in call stack:**

   See `root-cause-tracing.md` in this directory for the complete backward tracing technique.

   **Quick version:**
   - Where does bad value originate?
   - What called this with bad value?
   - Keep tracing up until you find the source
   - Fix at source, not at symptom

### Phase 2: Pattern Analysis

**Find the pattern before fixing:**

1. **Find Working Examples**
   - Locate similar working code in same codebase
   - What works that's similar to what's broken?

2. **Compare Against References**
   - If implementing pattern, read reference implementation COMPLETELY
   - Don't skim - read every line
   - Understand the pattern fully before applying

3. **Identify Differences**
   - What's different between working and broken?
   - List every difference, however small
   - Don't assume "that can't matter"

4. **Understand Dependencies**
   - What other components does this need?
   - What settings, config, environment?
   - What assumptions does it make?

### Phase 3: Hypothesis and Testing

**Scientific method:**

1. **Form Single Hypothesis**
   - State clearly: "I think X is the root cause because Y"
   - Write it down
   - Be specific, not vague

2. **Test Minimally**
   - Make the SMALLEST possible change to test hypothesis
   - One variable at a time
   - Don't fix multiple things at once

3. **Verify Before Continuing**
   - Did it work? Yes → Phase 4
   - Didn't work? Form NEW hypothesis
   - DON'T add more fixes on top

4. **When You Don't Know**
   - Say "I don't understand X"
   - Don't pretend to know
   - Ask for help
   - Research more

### Phase 4: Implementation

**Fix the root cause, not the symptom:**

1. **Create Failing Test Case**
   - Simplest possible reproduction
   - Automated test if possible
   - One-off test script if no framework
   - MUST have before fixing
   - Use the `test-driven-development` skill for writing proper failing tests

2. **Implement Single Fix**
   - Address the root cause identified
   - ONE change at a time
   - No "while I'm here" improvements
   - No bundled refactoring

3. **Verify Fix**
   - Test passes now?
   - No other tests broken?
   - Issue actually resolved?
   - Use the `verification-before-completion` skill before claiming success

4. **If Fix Doesn't Work**
   - STOP
   - Count: How many fixes have you tried?
   - If < 3: Return to Phase 1, re-analyze with new information
   - **If ≥ 3: STOP and question the architecture (step 5 below)**
   - DON'T attempt Fix #4 without architectural discussion

5. **If 3+ Fixes Failed: Question Architecture**

   **Pattern indicating architectural problem:**
   - Each fix reveals new shared state/coupling/problem in different place
   - Fixes require "massive refactoring" to implement
   - Each fix creates new symptoms elsewhere

   **STOP and question fundamentals:**
   - Is this pattern fundamentally sound?
   - Are we "sticking with it through sheer inertia"?
   - Should we refactor architecture vs. continue fixing symptoms?

   **Discuss with your human partner before attempting more fixes**

   This is NOT a failed hypothesis - this is a wrong architecture.

## Red Flags - STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "We can't reproduce it" (a reproduction RATE was never measured — 1-in-50 is not "can't")
- "The test passes now" (on an intermittent bug, one green run is what you'd see with no fix)
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals new problem in different place**

**ALL of these mean: STOP. Return to Phase 1.**

**If 3+ fixes failed:** Question the architecture (see Phase 4.5)

## your human partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Is that not happening?" - You assumed without verifying
- "Will it show us...?" - You should have added evidence gathering
- "Stop guessing" - You're proposing fixes without understanding
- "Ultra-think this" - Question fundamentals, not just symptoms
- "We're stuck?" (frustrated) - Your approach isn't working

**When you see these:** STOP. Return to Phase 1.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question pattern, don't fix again. |
| "It's not reproducible, so we have to guess" | Not-reproducible is a RATE. Measure it, then raise it. 1-in-50 is 2%, not zero. |
| "The fix worked — the test passed" | On an intermittent bug that is the expected outcome WITHOUT a fix. Re-run the loop the same number of times and quote both rates. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare | Identify differences |
| **3. Hypothesis** | Form theory, test minimally | Confirmed or new hypothesis |
| **4. Implementation** | Create test, fix, verify | Bug resolved, tests pass |

## When Process Reveals "No Root Cause"

If systematic investigation reveals issue is truly environmental, timing-dependent, or external:

1. You've completed the process
2. Document what you investigated
3. Implement appropriate handling (retry, timeout, error message)
4. Add monitoring/logging for future investigation

**But:** 95% of "no root cause" cases are incomplete investigation.

## Supporting Techniques

These techniques are part of systematic debugging and available in this directory:

- **`root-cause-tracing.md`** - Trace bugs backward through call stack to find original trigger
- **`defense-in-depth.md`** - Add validation at multiple layers after finding root cause
- **`condition-based-waiting.md`** - Replace arbitrary timeouts with condition polling
